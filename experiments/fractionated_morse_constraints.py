"""Exact local necessary constraints for an arbitrary Fractionated Morse alphabet."""
import argparse,hashlib,itertools,json,math,random,time
from collections import Counter
from pathlib import Path
import masking_pilots as old
ROOT=old.ROOT;AZ='ABCDEFGHIJKLMNOPQRSTUVWXYZ';TRIPLES=tuple(''.join(t) for t in itertools.product('.-x',repeat=3) if ''.join(t)!='xxx');N=26;FULL=(1<<N)-1
MORSE=old.read_spec(old.FM_SPEC)['Morse'];SPEC='research/FRACTIONATED-MORSE-ARBITRARY-SPEC.md'
MASKS={(i,c):sum(1<<j for j,t in enumerate(TRIPLES) if t[i]==c) for i in range(3) for c in '.-x'}

def pattern(word,mask):return ''.join(MORSE[c]+('x'*(1+((mask>>i)&1)) if i<len(word)-1 else '') for i,c in enumerate(word))
def window(cipher,offset,raw,initial=None):
    if offset<0 or offset+len(raw)>3*len(cipher):raise ValueError('window outside ternary stream')
    domains=list(initial) if initial is not None else [FULL]*26
    for j,symbol in enumerate(raw,offset):
        c=AZ.index(cipher[j//3]);domains[c]&=MASKS[j%3,symbol]
        if not domains[c]:return None
    return domains

def completions(domains,q=26,cap=100000):
    if len(domains)!=q:raise ValueError('one domain per alphabet symbol required')
    full=(1<<q)-1;domains=[d&full for d in domains]
    if any(not d for d in domains):return dict(completed=True,count='0',reason='empty_domain',witness=None,branches=0)
    fixed={i:d.bit_length()-1 for i,d in enumerate(domains) if bin(d).count('1')==1};used=sum(1<<x for x in set(fixed.values()))
    if len(set(fixed.values()))!=len(fixed):return dict(completed=True,count='0',reason='singleton_injectivity_collision',witness=None,branches=0)
    constrained=[i for i,d in enumerate(domains) if i not in fixed and d!=full];constrained.sort(key=lambda i:bin(domains[i]).count('1'));free=q-len(fixed)-len(constrained);total=0;witness=None;branches=0
    def visit(j,taken,assignment):
        nonlocal total,witness,branches
        branches+=1
        if branches>cap:raise OverflowError
        if j==len(constrained):
            total+=math.factorial(free)
            if witness is None:
                witness=assignment.copy();available=[x for x in range(q) if not(taken>>x)&1];remaining=[i for i in range(q) if i not in witness];witness.update(zip(remaining,available))
            return
        i=constrained[j];choices=domains[i]&~taken
        while choices:
            bit=choices&-choices;choices-=bit;assignment[i]=bit.bit_length()-1;visit(j+1,taken|bit,assignment);del assignment[i]
    try:visit(0,used,dict(fixed))
    except OverflowError:return dict(completed=False,count=None,reason='completion_budget_unresolved',witness=None,branches=branches)
    return dict(completed=True,count=str(total),reason='compatible_local_constraints' if total else 'injectivity_Hall_obstruction',witness=[witness[i] for i in range(q)] if witness else None,branches=branches)

def blocks(cipher,word,lo,hi,seconds=120,cap=400000):
    started=time.monotonic();tally=Counter();records={};contexts=0;completed=True
    for mask in range(1<<(len(word)-1)):
        raw=pattern(word,mask)
        for offset in range(lo,min(hi,3*len(cipher)-len(raw))+1):
            if contexts>=cap or time.monotonic()-started>seconds:completed=False;break
            contexts+=1;domains=window(cipher,offset,raw)
            if domains is None:tally['repeated_cipher_empty_domain']+=1;continue
            r=completions(domains)
            if not r['completed']:completed=False;tally['completion_budget_unresolved']+=1;break
            tally[r['reason']]+=1
            if r['count']!='0':
                key=tuple(domains)
                if key not in records:records[key]=dict(domains=list(domains),local_key_count=r['count'],witness=r['witness'],contexts=[])
                records[key]['contexts'].append(dict(offset=offset,word_break_mask=mask,length=len(raw)))
        if not completed:break
    return dict(completed=completed,status='complete_local_compatibility' if completed and records else ('impossible_local_constraints' if completed else 'budget_unresolved'),raw_contexts=contexts,word_break_masks=1<<(len(word)-1),rejection_tally=dict(tally),unique_domain_records=len(records),compatible_contexts=sum(len(r['contexts']) for r in records.values()),records=list(records.values()),seconds=time.monotonic()-started)

def joint(cipher,first,seconds=120,cap=2000000):
    started=time.monotonic();tally=Counter();records={};contexts=0;completed=True
    for r in first['records']:
        for c in r['contexts']:
            for mask in range(1024):
                raw=pattern('BERLINCLOCK',mask);lo=max(126,c['offset']+c['length']+59);hi=min(378,3*len(cipher)-len(raw),c['offset']+c['length']+176)
                for offset in range(lo,hi+1):
                    if contexts>=cap or time.monotonic()-started>seconds:completed=False;break
                    contexts+=1;domains=window(cipher,offset,raw,r['domains'])
                    if domains is None:tally['repeated_cipher_empty_domain']+=1;continue
                    count=completions(domains)
                    if not count['completed']:completed=False;tally['completion_budget_unresolved']+=1;break
                    tally[count['reason']]+=1
                    if count['count']!='0':
                        key=tuple(domains)
                        if key not in records:records[key]=dict(domains=list(domains),local_key_count=count['count'],witness=count['witness'],contexts=[])
                        records[key]['contexts'].append(dict(first=c,second=dict(offset=offset,word_break_mask=mask,length=len(raw)),previously_unconstrained_cipher_symbols=[AZ[i] for i in range(26) if r['domains'][i]==FULL and domains[i]!=FULL],changed_old_domains=[AZ[i] for i in range(26) if r['domains'][i]!=FULL and domains[i]!=r['domains'][i]]))
                if not completed:break
            if not completed:break
        if not completed:break
    return dict(completed=completed,status='compatible_necessary_conditions_only' if records else ('impossible_local_constraints' if completed else 'budget_unresolved'),raw_contexts=contexts,rejection_tally=dict(tally),unique_domain_records=len(records),compatible_contexts=sum(len(r['contexts']) for r in records.values()),records=list(records.values()),seconds=time.monotonic()-started)

def direct_oracle(cipher,offset,raw):
    constraints={};end=offset+len(raw)
    for i,c in enumerate(cipher):
        start=3*i
        if start>=end or start+3<=offset:continue
        allowed={j for j,t in enumerate(TRIPLES) if all(t[k-start]==raw[k-offset] for k in range(max(start,offset),min(start+3,end)))}
        constraints[c]=constraints.get(c,set(range(26)))&allowed
    return [sum(1<<x for x in constraints.get(c,set(range(26)))) for c in AZ]

def controls():
    reference=old.read_spec(old.FM_SPEC)['controls']['ACA_example'];assert old.morse_encode(reference['plaintext'],reference['alphabet'])['ciphertext']==reference['ciphertext'];assert old.morse_decode(reference['ciphertext'],reference['alphabet'])['spaced_plaintext']==reference['plaintext']
    rng=random.Random(71023);tiny=[]
    for q in range(2,7):
        for case in range(20):
            domains=[rng.randrange(1<<q) for _ in range(q)];expected=[list(p) for p in itertools.permutations(range(q)) if all(domains[i]>>p[i]&1 for i in range(q))];r=completions(domains,q)
            assert r['completed'] and int(r['count'])==len(expected)
            if expected:assert r['witness'] in expected
            tiny.append(dict(q=q,case=case,count=len(expected)))
    plants=[];direct=0
    for seed in range(6):
        p=[rng.choice(AZ) for _ in range(97)];p[21:34]='EASTNORTHEAST';p[63:74]='BERLINCLOCK';breaks=[rng.randrange(2) for _ in range(96)];message=''.join(c+(' ' if i<96 and breaks[i] else '') for i,c in enumerate(p));alphabet=list(AZ);rng.shuffle(alphabet);alphabet=''.join(alphabet);encoded=old.morse_encode(message,alphabet);cipher=encoded['ciphertext'];true=[TRIPLES.index(t) for c in AZ for t,v in old.triple_table(alphabet).items() if v==c];windows=[]
        for start,word in ((21,'EASTNORTHEAST'),(63,'BERLINCLOCK')):
            mask=sum(breaks[start+i]<<i for i in range(len(word)-1));offset=sum(len(MORSE[p[i]])+1+breaks[i] for i in range(start));raw=pattern(word,mask);domains=window(cipher,offset,raw);oracle=direct_oracle(cipher,offset,raw);assert domains==oracle;direct+=1;assert all(domains[i]>>true[i]&1 for i in range(26));r=completions(domains);assert r['completed'] and int(r['count'])>0
            assert 2*start<=offset<=6*start;windows.append(dict(start=start+1,offset=offset,mask=mask,local_key_count=r['count'],true_key_retained=True))
        selected=blocks(cipher,'EASTNORTHEAST',42,126);assert selected['completed'];truth=windows[0];assert any(context['offset']==truth['offset'] and context['word_break_mask']==truth['mask'] and all(record['domains'][i]>>true[i]&1 for i in range(26)) for record in selected['records'] for context in record['contexts'])
        decoded=old.morse_decode(cipher,alphabet);assert decoded['spaced_plaintext']==message;assert old.morse_encode(decoded['spaced_plaintext'],alphabet)['ciphertext']==cipher
        # Independent direct constraints also cover all three partial-boundary phases.
        for offset in range(3):
            for word in ('A','E','T','Q','EAST'):
                raw=pattern(word,0);expected=direct_oracle(cipher,offset,raw);assert window(cipher,offset,raw)==(expected if all(expected) else None);direct+=1
        plants.append(dict(complete_first_selector_contexts=selected['raw_contexts'],complete_first_selector_truth_retained=True,seed=seed,alphabet=alphabet,plaintext_letters=97,ciphertext_letters=len(cipher),full_roundtrip=True,windows=windows))
    assert completions([1,1],2)['count']=='0';assert completions([0,3],2)['count']=='0';assert not completions([3,3],2,cap=0)['completed']
    return dict(ACA_example_verified=True,complete_small_permutation_comparisons=tiny,literal_crib_plants=plants,direct_substring_checks=direct,injectivity_mutation_rejected=True,empty_domain_mutation_rejected=True,budget_unresolved_not_rejection=True)

def normalized(value):return json.loads(json.dumps(value))
def actual():
    data=json.loads((ROOT/'data/k4.json').read_text());first=blocks(data['ciphertext'],'EASTNORTHEAST',42,126);second=joint(data['ciphertext'],first) if first['completed'] and first['records'] else None
    return dict(first=first,second=second,second_stage_evaluated=second is not None,scope='Local necessary-condition relaxation only; no global prefix/gap parsing or full plaintext claim',crib_positions_are_decoded_letter_positions=True,cipher_positions_not_assumed_equal=True,key_counts_across_contexts_not_added=True)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--controls',action='store_true');ap.add_argument('--actual',action='store_true');ap.add_argument('--output',required=True);args=ap.parse_args();out={}
    if args.controls:out['controls']=controls()
    if args.actual:out['actual']=actual()
    out['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),ROOT/SPEC,ROOT/old.FM_SPEC,ROOT/'experiments/masking_pilots.py',ROOT/'data/k4.json')};Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
