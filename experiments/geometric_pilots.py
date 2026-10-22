"""Frozen geometric-alphabet pilots; no adaptive scope or partial-score ranking."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import random
import time
from alphabet_geometry import load_schema, codebook, encode_array, SCHEMA

ROOT = Path(__file__).resolve().parents[1]
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
KR = 'KRYPTOSABCDEFGHIJLMNQUVWXZ'
WIDTH = 35
MASK = (1 << WIDTH)-1
EXPECTED = '6a5c6eae644dedf88afb68df911f0c3161a969af3815972aa5694479155aa010'
TRAIN = {21+i: c for i,c in enumerate('EASTNORTHEAST')}
BERLIN = {63+i: c for i,c in enumerate('BERLINCLOCK')}


def frozen_codes():
    if hashlib.sha256(SCHEMA.read_bytes()).hexdigest() != EXPECTED:
        raise ValueError('schema hash changed')
    return {c: encode_array(v) for c,v in codebook(load_schema()).items()}


def rotl35(state, rotation):
    if type(state) is not int or not 0 <= state <= MASK or type(rotation) is not int or not 0 <= rotation < WIDTH:
        raise ValueError('invalid 35-bit state or rotation')
    return ((state << rotation) | (state >> (WIDTH-rotation))) & MASK


def bitlist_rotation(state, rotation):
    bits = [(state >> i)&1 for i in range(WIDTH)]
    out = [0]*WIDTH
    for i,bit in enumerate(bits):out[(i+rotation)%WIDTH] = bit
    return sum(bit*2**i for i,bit in enumerate(out))


def model_domain():
    return [(name,source,r,seed) for name in ('AZ','KRYPTOS') for source in ('C','P') for r in range(35) for seed in AZ]


def feedback_decrypt(ciphertext, model, codes):
    name, source, r, seed = model
    alphabet = AZ if name=='AZ' else KR
    index = {c:i for i,c in enumerate(alphabet)}
    state = codes[seed]
    out = []
    # Local exact integer operations, separate from the bit-list encoder below.
    for c in ciphertext:
        p = alphabet[(index[c] - state%26)%26]
        out.append(p)
        state = (((state << r) | (state >> (35-r))) & MASK) ^ codes[c if source=='C' else p]
    return ''.join(out)


def feedback_encrypt(plaintext, model, codes, nearby=False):
    name, source, r, seed = model
    alphabet = AZ if name=='AZ' else KR
    state = codes[seed]
    result = []
    for p in plaintext:
        c = alphabet[(alphabet.index(p)+state%26)%26]
        result.append(c)
        value = codes[c if source=='C' else p]
        # Independently written rotation; nearby changes operation order.
        state = bitlist_rotation(state ^ value, r) if nearby else bitlist_rotation(state,r) ^ value
    return ''.join(result)


def deadline_check(start, budget):
    if time.monotonic()-start > budget:
        raise TimeoutError('frozen runtime budget exceeded')


def feedback_select(ciphertext, codes, budget=120):
    start = time.monotonic()
    rows = []
    outputs = Counter()
    survivors = []
    train_survivors = []
    for model in model_domain():
        deadline_check(start,budget)
        plaintext = feedback_decrypt(ciphertext,model,codes)
        outputs[plaintext] += 1
        matches = [plaintext[i]==p for i,p in TRAIN.items()]
        good = all(matches)
        berlin = [plaintext[i]==p for i,p in BERLIN.items()] if good else None
        row = {'model':list(model), 'training_matches':sum(matches),
               'training_first_mismatch_one_based':next((i+1 for i,p in TRAIN.items() if plaintext[i]!=p),None),
               'berlin_matches':sum(berlin) if good else None,
               'plaintext':plaintext}
        rows.append(row)
        if good:
            train_survivors.append(list(model))
            if all(berlin):
                assert feedback_encrypt(plaintext,model,codes)==ciphertext
                survivors.append(row)
    return {'raw_models':len(rows),'unique_full_outputs':len(outputs),
            'duplicate_output_descriptions':len(rows)-len(outputs),
            'duplicate_output_groups':[{'plaintext':p,'descriptions':n} for p,n in outputs.items() if n>1],
            'training_survivors':train_survivors,'all24_survivors':survivors,
            'fitted_positions_one_based':list(range(22,35)),
            'public_second_stage_positions_one_based':list(range(64,75)),
            'rows':rows,'runtime_seconds':round(time.monotonic()-start,6)}


def periodic_transform(text, alphabet, key, equation, decrypt=False):
    index={c:i for i,c in enumerate(alphabet)}
    if equation=='plus':
        return ''.join(alphabet[(index[c]+(-1 if decrypt else 1)*key[i%len(key)])%26] for i,c in enumerate(text))
    return ''.join(alphabet[(key[i%len(key)]-index[c])%26] for i,c in enumerate(text))


def primitive_period(key):
    return next(d for d in range(1,len(key)+1) if len(key)%d==0 and all(key[i]==key[i%d] for i in range(len(key))))


def periodic_select(ciphertext, codes, budget=120):
    start=time.monotonic()
    alphabet=''.join(sorted(AZ,key=codes.get));index={c:i for i,c in enumerate(alphabet)}
    rows=[];survivors=[];outputs=Counter()
    for period in range(1,13):
        for equation in ('plus','beaufort'):
            deadline_check(start,budget)
            slots={};contradictions=[];checks=0
            for i,p in TRAIN.items():
                value=(index[ciphertext[i]] + (-index[p] if equation=='plus' else index[p]))%26
                residue=i%period
                if residue in slots:
                    checks+=1
                    old=slots[residue]
                    if old['value']!=value:
                        contradictions.append({'key_residue':residue,'first_position_one_based':old['position']+1,
                                               'second_position_one_based':i+1,'first_value':old['value'],'second_value':value})
                else:slots[residue]={'value':value,'position':i}
            free=[i for i in range(period) if i not in slots]
            assert not free
            row={'period':period,'equation':equation,
                 'coverage':'new_geometric_alphabet' if period in (8,11,12) else 'alphabet_independent_baseline_recheck',
                 'parameter_slots':period,'training_repeated_slot_checks':checks,
                 'free_key_slots':free,'training_contradictions':contradictions,
                 'training_compatible_key_assignments':0 if contradictions else 1,
                 'key':None,'berlin_matches':None,'plaintext':None}
            if not contradictions:
                key=[slots[i]['value'] for i in range(period)]
                plaintext=periodic_transform(ciphertext,alphabet,key,equation,True)
                assert all(plaintext[i]==p for i,p in TRAIN.items())
                assert periodic_transform(plaintext,alphabet,key,equation)==ciphertext
                row.update(key=key,primitive_key_period=primitive_period(key),plaintext=plaintext,
                           berlin_matches=sum(plaintext[i]==p for i,p in BERLIN.items()))
                outputs[plaintext]+=1
                if row['berlin_matches']==11:survivors.append(row)
            rows.append(row)
    return {'alphabet':alphabet,'formal_structures':24,'new_geometric_checks':6,'baseline_rechecks':18,
            'training_survivors':sum(not x['training_contradictions'] for x in rows),
            'all24_survivors':survivors,'unique_training_outputs':len(outputs),
            'duplicate_training_outputs':sum(outputs.values())-len(outputs),
            'rows':rows,'runtime_seconds':round(time.monotonic()-start,6)}


def literal_plaintext():
    rng=random.Random(20261022)
    p=[rng.choice(AZ) for _ in range(97)]
    for i,c in {**TRAIN,**BERLIN}.items():p[i]=c
    return ''.join(p)


def controls(codes, budget=300):
    start=time.monotonic();plaintext=literal_plaintext();plants=[]
    for name in ('AZ','KRYPTOS'):
        for source in ('C','P'):
            for r in (0,1,17,34):
                for seed in ('A','M','Z'):
                    deadline_check(start,budget)
                    model=(name,source,r,seed)
                    cipher=feedback_encrypt(plaintext,model,codes)
                    assert feedback_decrypt(cipher,model,codes)==plaintext
                    selected=feedback_select(cipher,codes,max(.01,budget-(time.monotonic()-start)))
                    models=[tuple(x['model']) for x in selected['all24_survivors']]
                    assert model in models
                    changed=list(cipher);changed[21]=AZ[(AZ.index(changed[21])+1)%26]
                    mutation=feedback_decrypt(''.join(changed),model,codes)
                    assert not all(mutation[i]==p for i,p in TRAIN.items())
                    nearby=feedback_encrypt(plaintext,model,codes,nearby=True)
                    incompatible = None if r==0 else feedback_decrypt(nearby,model,codes)!=plaintext
                    assert incompatible is not False
                    plants.append({'model':list(model),'roundtrip':True,'truth_included':True,
                                   'compatible_parameter_descriptions':len(models),
                                   'distinct_compatible_plaintexts':len({x['plaintext'] for x in selected['all24_survivors']}),
                                   'mutation_target_rejected':True,'nearby_operation_order_rejected':incompatible})
    alphabet=''.join(sorted(AZ,key=codes.get));periodic=[]
    for m in range(1,13):
        for equation in ('plus','beaufort'):
            key=[(3+i*5)%26 for i in range(m)]
            cipher=periodic_transform(plaintext,alphabet,key,equation)
            assert periodic_transform(cipher,alphabet,key,equation,True)==plaintext
            selected=periodic_select(cipher,codes)
            truth=[row for row in selected['all24_survivors'] if row['period']==m and row['equation']==equation]
            assert len(truth)==1 and truth[0]['key']==key and truth[0]['plaintext']==plaintext
            changed=list(cipher);changed[21]=alphabet[(alphabet.index(changed[21])+1)%26]
            assert periodic_transform(''.join(changed),alphabet,key,equation,True)[21]!=plaintext[21]
            periodic.append({'period':m,'equation':equation,'truth_included':True,'roundtrip':True,
                             'compatible_structures':len(selected['all24_survivors']),'mutation_target_rejected':True})
    rotation_checks=0
    for value in [0,MASK,1,1<<34]+[1<<i for i in range(35)]:
        for r in range(35):
            assert rotl35(value,r)==bitlist_rotation(value,r)
            assert rotl35(rotl35(value,r),(35-r)%35)==value
            rotation_checks+=1
    assert periodic_transform(plaintext,alphabet,[7]*8,'plus')==periodic_transform(plaintext,alphabet,[7],'plus')
    assert primitive_period([7]*8)==1
    return {'source_sha256':EXPECTED,'literal_cribs_preserved':True,'feedback_plants':plants,
            'periodic_plants':periodic,'rotation_checks':rotation_checks,
            'periodic_alias_control':True,'runtime_seconds':round(time.monotonic()-start,6),
            'interpretation':'Truth inclusion is tested, not assumed unique recovery. Nearby and mutation controls reject the fixed altered mechanism; no null p-value is claimed.'}


def run_actual(codes):
    fixture=json.loads((ROOT/'data/k4.json').read_text())
    cipher=fixture['ciphertext']
    assert len(cipher)==97 and cipher[21:25]=='FLRV' and cipher[25:34]=='QQPRNGKSS' and cipher[63:74]=='NYPVTTMZFPK'
    return {'source_sha256':EXPECTED,'ciphertext_sha256':hashlib.sha256(cipher.encode()).hexdigest(),
            'pilot_a':periodic_select(cipher,codes),'pilot_b':feedback_select(cipher,codes),
            'stopping_rule':'No scope expansion. Exact survivor requires separately frozen full-family null calibration; no partial-score significance.'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('mode',choices=['controls','actual'])
    args=p.parse_args();codes=frozen_codes()
    value=controls(codes) if args.mode=='controls' else run_actual(codes)
    print(json.dumps(value,indent=2))

if __name__=='__main__':main()
