"""Frozen Cambridge-US IPA preprocessing checks; no dialect or index search."""
from collections import defaultdict
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random
import time
from exact_linear import solve_ring,ring_vectors,contains

ROOT=Path(__file__).resolve().parents[1]
AZ='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
KR='KRYPTOSABCDEFGHIJLMNQUVWXZ'
ORDINARY={'i':'I','s':'S','t':'T','n':'N','r':'R','b':'B','l':'L','k':'K'}
SPECIAL=('ː','ɔ','θ')
NEW_SPECIAL=('ɝ','ɪ','ɑ')
WINDOWS=((21,'iːstnɔːrθiːst'),(63,'bɝːlɪnklɑːk'))


def normalize(text):
    text=text.strip()
    if text.startswith('/') or text.endswith('/'):
        if not (text.startswith('/') and text.endswith('/')):raise ValueError('unbalanced IPA delimiters')
        text=text[1:-1]
    return ''.join(c for c in text if c not in 'ˈˌ.' and not c.isspace())


def long_vowel_tokens(text):
    """Limited decomposition for the disclosed inventory, not a full IPA parser."""
    out=[]
    for c in normalize(text):
        if c=='ː':
            if not out or out[-1].endswith('ː'):raise ValueError('orphan or repeated length mark')
            out[-1]+='ː'
        else:out.append(c)
    return out


def input_audit(data):
    entries=data['entries']
    first=normalize(entries['east'])+normalize(entries['northeast'])
    second=normalize(entries['berlin'])+normalize(entries['clock'])
    assert first==normalize(entries['east-northeast'])==WINDOWS[0][1]
    assert second==WINDOWS[1][1]
    r1=[long_vowel_tokens(first),long_vowel_tokens(second)]
    assert list(map(len,r1))==[10,9]
    assert list(map(len,[first,second]))==[13,11]
    inventory=set(first+second)
    assert inventory==set(ORDINARY)|set(SPECIAL)|set(NEW_SPECIAL) and len(inventory)==14
    return {'R1_segments':r1,'R1_lengths':[10,9],'R1_fixed_span_length_preserving_transport_rejected':True,
            'R2_windows':[first,second],'R2_lengths':[13,11],
            'R2_codepoints':[[{'symbol':c,'unicode':'U+%04X'%ord(c)} for c in w] for w in [first,second]],
            'disclosed_inventory_size':14,
            'alignment_assumption':'Phonetic windows at the English disclosure indices; cumulative unknown-prefix alignment unproved.'}


def phase_conflicts(pairs,period):
    out=[]
    for (i,x,c),(j,y,d) in itertools.combinations(pairs,2):
        if (j-i)%period==0 and ((x==y)!=(c==d)):
            out.append({'positions':[i+1,j+1],'IPA':[x,y],'ciphertext':[c,d],
                        'reason':'same IPA, different ciphertext' if x==y else 'different IPA, same ciphertext'})
    return out


def expression(symbol,alphabet):
    if symbol in ORDINARY:return alphabet.index(ORDINARY[symbol]),[0,0,0]
    if symbol not in SPECIAL:raise ValueError('not a first-window symbol')
    return 0,[int(symbol==s) for s in SPECIAL]


def constraints(ciphertext,alphabet,equation,period):
    sign=1 if equation=='add' else -1
    origins={};matrix=[];rhs=[];equations=[]
    for i,symbol in enumerate(WINDOWS[0][1],21):
        constant,vector=expression(symbol,alphabet);cipher=alphabet.index(ciphertext[i]);residue=i%period
        if residue not in origins:origins[residue]=(i,symbol,constant,vector,cipher)
        else:
            j,old,old_const,old_vec,old_cipher=origins[residue]
            row=[sign*(x-y)%26 for x,y in zip(vector,old_vec)]
            value=(cipher-old_cipher-sign*(constant-old_const))%26
            matrix.append(row);rhs.append(value)
            equations.append({'positions':[j+1,i+1],'key_residue':residue,'IPA':[old,symbol],
                              'coefficients':row,'rhs':value})
    assert len(origins)==period
    return matrix,rhs,equations


def fixed_anchor_conflicts(ciphertext,alphabet,equation,period):
    """Independent all-pairs test: no aliases, solver, or key table."""
    sign=1 if equation=='add' else -1;anchors=[];out=[]
    for i,s in enumerate(WINDOWS[0][1],21):
        if s in ORDINARY:anchors.append((i,s,alphabet.index(ciphertext[i]),alphabet.index(ORDINARY[s])))
    for left,right in itertools.combinations(anchors,2):
        i,p,c,x=left;j,q,d,y=right
        if (j-i)%period==0:
            u=(c-sign*x)%26;v=(d-sign*y)%26
            if u!=v:out.append({'positions':[i+1,j+1],'IPA':[p,q],'required_key_values':[u,v]})
    return out


def recover_key(ciphertext,alphabet,equation,period,values):
    """Full conditional key from one alias assignment; fail on contradictions."""
    sign=1 if equation=='add' else -1;slots={}
    for i,s in enumerate(WINDOWS[0][1],21):
        p=alphabet.index(ORDINARY[s]) if s in ORDINARY else values[SPECIAL.index(s)]
        k=(alphabet.index(ciphertext[i])-sign*p)%26;r=i%period
        if r in slots and slots[r]!=k:return None
        slots[r]=k
    return tuple(slots[r] for r in range(period))


def injective_first(values,alphabet):
    return len(set(values))==3 and not set(values)&{alphabet.index(c) for c in ORDINARY.values()}


def second_stage(ciphertext,alphabet,equation,key,values):
    mapping={s:alphabet.index(c) for s,c in ORDINARY.items()}
    mapping.update(zip(SPECIAL,values));new={};predictions=[]
    for i,s in enumerate(WINDOWS[1][1],63):
        c=alphabet.index(ciphertext[i]);k=key[i%len(key)]
        p=(c-k)%26 if equation=='add' else (k-c)%26
        if s in mapping:
            predictions.append({'position':i+1,'symbol':s,'required_index':mapping[s],'recovered_index':p,'matches':p==mapping[s]})
        elif s in new and new[s]!=p:return None
        else:new[s]=p
    assert set(new)==set(NEW_SPECIAL) and len(predictions)==8
    if len(set(new.values()))!=3 or set(new.values())&set(mapping.values()):return None
    return {'predicted_existing_symbol_positions':predictions,'new_aliases_fitted_not_predicted':new,
            'new_alias_fit_positions':[65,68,72],
            'compatible':all(x['matches'] for x in predictions)}


def select(ciphertext,include_second=True,budget=120):
    started=time.monotonic();rows=[]
    for name,alphabet in [('AZ',AZ),('KRYPTOS',KR)]:
        for equation in ('add','beaufort'):
            for period in range(1,13):
                if time.monotonic()-started>budget:raise TimeoutError('frozen IPA runtime budget')
                matrix,rhs,eqs=constraints(ciphertext,alphabet,equation,period)
                space=solve_ring(matrix,rhs,26,3)
                anchors=fixed_anchor_conflicts(ciphertext,alphabet,equation,period)
                if anchors:assert not space['consistent']
                assignments=[]
                if space['consistent']:
                    for values in ring_vectors(space):
                        if time.monotonic()-started>budget:raise TimeoutError('frozen IPA runtime budget')
                        key=recover_key(ciphertext,alphabet,equation,period,values)
                        assert key is not None
                        if not injective_first(values,alphabet):continue
                        stage=second_stage(ciphertext,alphabet,equation,key,values) if include_second else None
                        assignments.append({'special_indices':list(values),'conditional_key':list(key),'second_stage':stage})
                rows.append({'alphabet':name,'equation':equation,'period':period,
                             'special_variable_order':list(SPECIAL),'modular_constraints':eqs,
                             'relaxed_solution_space':space,'relaxed_alias_assignment_count':space['cardinality'],
                             'fixed_ordinary_anchor_conflicts':anchors,
                             'injective_first_assignments':assignments,
                             'training_key_free_slots_conditional_on_aliases':[],
                             'second_window_evaluated':bool(space['consistent'] and include_second)})
    return rows


def encoded_plain(ipa,alphabet,alias):
    mapping={**ORDINARY,**alias}
    try:out=''.join(mapping[s] for s in ipa)
    except KeyError as exc:raise ValueError('unmapped IPA symbol') from exc
    if any(c not in alphabet for c in out):raise ValueError('alias outside outer alphabet')
    return out


def crypt(letters,alphabet,key,equation,decrypt=False):
    if equation=='add':return ''.join(alphabet[(alphabet.index(c)+(-1 if decrypt else 1)*key[i%len(key)])%26] for i,c in enumerate(letters))
    return ''.join(alphabet[(key[i%len(key)]-alphabet.index(c))%26] for i,c in enumerate(letters))


def controls():
    started=time.monotonic()
    aliases=dict(zip(SPECIAL+NEW_SPECIAL,'ADEFGH'))
    mapping={**ORDINARY,**aliases};assert len(set(mapping.values()))==14
    rng=random.Random(20261023);tokens=[rng.choice(list(mapping)) for _ in range(97)]
    for start,text in WINDOWS:tokens[start:start+len(text)]=text
    latin=''.join(mapping[s] for s in tokens);plants=[]
    for name,alphabet in [('AZ',AZ),('KRYPTOS',KR)]:
        values=tuple(alphabet.index(aliases[s]) for s in SPECIAL)
        for equation in ('add','beaufort'):
            for period in range(1,13):
                key=[(3+7*j)%26 for j in range(period)]
                cipher=crypt(latin,alphabet,key,equation)
                assert crypt(cipher,alphabet,key,equation,True)==latin
                remaining=300-(time.monotonic()-started)
                if remaining<=0:raise TimeoutError('frozen IPA control budget')
                selected=select(cipher,budget=remaining)
                true=next(x for x in selected if (x['alphabet'],x['equation'],x['period'])==(name,equation,period))
                assert contains(true['relaxed_solution_space'],values)
                matching=[x for x in true['injective_first_assignments'] if x['special_indices']==list(values)]
                assert len(matching)==1 and matching[0]['conditional_key']==key
                stage=matching[0]['second_stage'];assert stage is not None and stage['compatible']
                assert stage['new_aliases_fitted_not_predicted']=={s:alphabet.index(aliases[s]) for s in NEW_SPECIAL}
                assert not injective_first((values[0],values[0],values[2]),alphabet)
                mutated=list(cipher);mutated[21]=alphabet[(alphabet.index(mutated[21])+1)%26]
                assert recover_key(''.join(mutated),alphabet,equation,period,values) is None
                plants.append({'alphabet':name,'equation':equation,'period':period,'full_selector_models':len(selected),
                               'true_aliases_and_key_retained':True,'roundtrip':True,'mutation_target_rejected':True,
                               'injective_first_assignment_count':len(true['injective_first_assignments']),
                               'compatible_second_stage_assignments':sum(x['second_stage'] is not None and x['second_stage']['compatible'] for x in true['injective_first_assignments'])})
    # Independent tiny complete alias domains test all free/singular solutions.
    tiny=[]
    for modulus in (2,3,6):
        for matrix,rhs in [([[1,1,0]],[1]),([[2,0,0],[0,1,1]],[0,1]),([[0,0,0]],[1])]:
            s=solve_ring(matrix,rhs,modulus,3)
            brute={x for x in itertools.product(range(modulus),repeat=3) if all(sum(a*b for a,b in zip(row,x))%modulus==y%modulus for row,y in zip(matrix,rhs))}
            assert set(ring_vectors(s))==brute
            tiny.append({'modulus':modulus,'solution_count':len(brute),'complete_sets_equal':True})
    return {'literal_IPA_windows':True,'plant_count':len(plants),'plants':plants,'complete_small_ring_comparisons':tiny,
            'interpretation':'Truth inclusion and counts; new Berlin aliases are fitted parameters, not predictions.'}


def run(data,ciphertext):
    audit=input_audit(data)
    pairs=[(i,s,ciphertext[i]) for start,text in WINDOWS for i,s in enumerate(text,start)]
    phase={str(p):phase_conflicts(pairs,p) for p in range(1,13)}
    diagnostics={}
    for period in range(1,13):
        paired=[(a,b) for a,b in itertools.combinations(pairs,2) if (a[0]-b[0])%period==0]
        diagnostics[str(period)]={'same_phase_pairs':len(paired),
            'repeated_IPA_pairs':sum(a[1]==b[1] for a,b in paired),
            'repeated_ciphertext_pairs':sum(a[2]==b[2] for a,b in paired)}
    rows=select(ciphertext)
    return {'experiment':'IPA-PREPROCESSING-001','normalization':audit,
            'mapping_independent_periods':{'rejected':[p for p in range(1,13) if phase[str(p)]],
                                         'not_contradicted':[p for p in range(1,13) if not phase[str(p)]],
                                         'witnesses':phase,'pair_diagnostics':diagnostics},
            'fixed_Latin_model_structures':48,
            'ordinary_anchor_rejected_structures':sum(bool(r['fixed_ordinary_anchor_conflicts']) for r in rows),
            'non_anchor_modular_rejected_structures':sum(not r['fixed_ordinary_anchor_conflicts'] and not r['relaxed_solution_space']['consistent'] for r in rows),
            'actual_alias_assignments_enumerated':sum(r['relaxed_alias_assignment_count'] for r in rows),
            'relaxed_training_survivor_structures':sum(r['relaxed_alias_assignment_count']>0 for r in rows),
            'rows':rows,'scope':'Fixed Cambridge US normalization, unchanged disclosed window indices, two named outer equations/alphabets, periods 1-12. No universal IPA or English spelling inverse claim.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=['controls','actual'])
    args=parser.parse_args()
    if args.mode=='controls':value=controls()
    else:
        data=json.loads((ROOT/'data/ipa-cambridge-us-v1.json').read_text())
        fixture=json.loads((ROOT/'data/k4.json').read_text())
        assert fixture['ciphertext'][21:34]=='FLRVQQPRNGKSS'
        assert [(x['start'],x['end'],x['plaintext']) for x in fixture['cribs']]==[(22,34,'EASTNORTHEAST'),(64,74,'BERLINCLOCK')]
        value=run(data,fixture['ciphertext'])
        value['source_sha256']={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['data/ipa-cambridge-us-v1.json','data/k4.json','research/IPA-PREPROCESSING-SPEC.md','experiments/ipa_preprocessing.py']}
    serialized=json.dumps(value,ensure_ascii=False,indent=2)+'\n'
    if len(serialized.encode())>256*1024*1024:raise MemoryError('frozen retained-result budget exceeded')
    print(serialized,end='')

if __name__=='__main__':main()
