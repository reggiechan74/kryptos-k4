"""Fixed CL spelling adaptation: synthetic recovery and inherited K4 witnesses."""
import argparse
from collections import defaultdict
import hashlib
from itertools import product
import json
from pathlib import Path
import random
import time
from bounded_models import ALPHABETS,EQUATIONS,required_key
ROOT=Path(__file__).resolve().parents[1]
AZ='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
KA='KRYPTOSABCDEFGHIJLMNQUVWXZ'

def mask_text(text,mask):
    if not text or any(c not in AZ for c in text):raise ValueError('uppercase AZ stream required')
    if mask=='identity':return text
    if mask!='CL':raise ValueError('unknown mask')
    return ''.join('K' if c=='C' and i+1<len(text) and text[i+1]=='L' else c for i,c in enumerate(text))

def known_original():
    return {i:c for start,word in [(21,'EASTNORTHEAST'),(63,'BERLINCLOCK')] for i,c in enumerate(word,start)}

def mask_known(known,length,mask):
    if mask=='identity':return dict(known)
    if mask!='CL':raise ValueError('unknown mask')
    result={}
    for i,c in known.items():
        if c=='C' and i+1<length and i+1 not in known:raise ValueError('unknown context after C')
        result[i]='K' if c=='C' and known.get(i+1)=='L' else c
    return result

def crypt(text,key,alphabet,equation,decrypt=False):
    n=len(alphabet);out=[]
    for i,c in enumerate(text):
        v=alphabet.index(c);k=key[i%len(key)]
        if equation=='plus':v=v-k if decrypt else v+k
        elif equation=='minus':v=v+k if decrypt else v-k
        elif equation=='beaufort':v=k-v
        else:raise ValueError('equation')
        out.append(alphabet[v%n])
    return ''.join(out)

def inferred(cipher,known,mask,period,alphabet=AZ,equation='plus'):
    target=mask_known(known,len(cipher),mask);key=[None]*period;n=len(alphabet)
    for i,p in sorted(target.items()):
        c=alphabet.index(cipher[i]);p=alphabet.index(p)
        k=((c-p) if equation=='plus' else (p-c) if equation=='minus' else (c+p))%n
        phase=i%period
        if key[phase] is not None and key[phase]!=k:return {'status':'contradiction'}
        key[phase]=k
    if any(v is None for v in key):return {'status':'underdetermined','free_phases':sum(v is None for v in key),'key':key}
    q=crypt(cipher,key,alphabet,equation,True)
    if mask_text(q,mask)!=q:return {'status':'outside_mask_image'}
    assert crypt(q,key,alphabet,equation)==cipher
    return {'status':'recovered_transformed_stream','key':key,'transformed':q}

def primitive(key):
    for n in range(1,len(key)+1):
        if len(key)%n==0 and all(v==key[i%n] for i,v in enumerate(key)):return tuple(key[:n])

def select(cipher,known,alphabets=None,equations=None):
    records=[];groups=defaultdict(list)
    for mask in ('identity','CL'):
        for name,a in (alphabets or [('AZ',AZ)]):
            for eq in (equations or ['plus']):
                for p in range(1,13):
                    r=inferred(cipher,known,mask,p,a,eq)
                    if r['status']=='recovered_transformed_stream':
                        item={'mask':mask,'alphabet':name,'equation':eq,'period':p,'key':r['key'],'primitive_key':list(primitive(r['key']))}
                        records.append(item);groups[(mask,r['transformed'])].append(item)
    return records,groups

def overlay(text):
    text=list((text*97)[:97]);text[0:2]=list('CL')
    for i,c in known_original().items():text[i]=c
    return ''.join(text)

def controls():
    started=time.monotonic();known=known_original();primary=[];supplement=[]
    expected={'CLOCK':'KLOCK','CL':'KL','KL':'KL','CK':'CK','CYCLE':'CYKLE'}
    assert all(mask_text(k,'CL')==v for k,v in expected.items())
    for seed,mask,p in [(104729,'CL',5),(130363,'CL',7),(155921,'CL',11),(196613,'identity',7)]:
        rng=random.Random(seed);original=overlay(''.join(rng.choice(AZ) for _ in range(97)));key=[rng.randrange(26) for _ in range(p)]
        q=mask_text(original,mask);cipher=crypt(q,key,AZ,'plus');models,groups=select(cipher,known)
        correct=(mask,q) in groups and any(x['period']==p and x['key']==key for x in groups[(mask,q)])
        if not correct or len(groups)!=1:raise AssertionError('primary recovery failure/ambiguity; stop before K4')
        assert all(x['primitive_key']==list(primitive(key)) for x in models)
        corrupted=list(cipher);corrupted[21]=AZ[(AZ.index(corrupted[21])+1)%26];corrupted=''.join(corrupted)
        assert inferred(corrupted,known,mask,p)['status']=='contradiction'
        alternatives=select(corrupted,known)[0]
        second='K'+original[1:]
        loss=mask=='CL' and second!=original and mask_text(second,mask)==q
        if mask=='CL':assert loss
        primary.append({'seed':seed,'mask':mask,'period':p,'key_recovered':True,'transformed97_recovered':True,'canonical_model_groups':len(groups),'parameter_alias_count':len(models),'wrong_cipher_planted_model_rejected':True,'corrupted_cipher_other_candidates':len(alternatives),'original_spelling_unique_under_planted_mask':not loss,'two_original_preimages_demonstrated':loss,'transformed_sha256':hashlib.sha256(q.encode()).hexdigest()})
    # Literal, independently specified fixture sequences; no English/language score.
    for fixture,text in [('alphabet',AZ),('CLACKCLOCK','CLACKCLOCK')]:
        original=overlay(text)
        for mask in ('identity','CL'):
            q=mask_text(original,mask)
            for name,a in ALPHABETS:
                for eq in EQUATIONS:
                    for p in range(1,13):
                        key=[a.index(c) for c in KA[:p]];cipher=crypt(q,key,a,eq)
                        answer=inferred(cipher,known,mask,p,a,eq)
                        assert answer['status']=='recovered_transformed_stream' and answer['key']==key and answer['transformed']==q
                        other='CL' if mask=='identity' else 'identity'
                        assert inferred(cipher,known,other,p,a,eq)['status']=='contradiction'
                        changed=list(cipher);changed[21]=a[(a.index(changed[21])+1)%26]
                        assert inferred(''.join(changed),known,mask,p,a,eq)['status']=='contradiction'
                        models,groups=select(cipher,known,ALPHABETS,EQUATIONS)
                        assert (mask,q) in groups
                        supplement.append({'fixture':fixture,'mask':mask,'alphabet':name,'equation':eq,'period':p,'key_and_transformed97_recovered':True,'wrong_mask_rejected':True,'mutation_rejected':True,'normalized_model_groups':len(groups),'parameter_aliases':len(models)})
    assert len(supplement)==288
    low=inferred(crypt('A'*97,[1,2,3,4,5],AZ,'plus'),{21:'A'},'identity',5)
    assert low['status']=='underdetermined' and low['free_phases']==4 and 'transformed' not in low
    try:mask_known({1:'C'},97,'CL')
    except ValueError:pass
    else:raise AssertionError('unknown context guessed')
    oracle_cases=0
    for original in ('CLACKLA','AKLACLA'):
        for mask in ('identity','CL'):
            q=mask_text(original,mask)
            for p in (1,2,3):
                for planted in ((0,1,2),(3,2,1)):
                    a='ACKL';key=list(planted[:p]);cipher=crypt(q,key,a,'plus');known={i:original[i] for i in (0,1,2,4,5)}
                    got=inferred(cipher,known,mask,p,a,'plus');target=mask_known(known,len(original),mask)
                    brute=[]
                    for candidate in product(range(4),repeat=p):
                        # Independently encrypt known transformed symbols, then check full image.
                        if all(a[(a.index(v)+candidate[i%p])%4]==cipher[i] for i,v in target.items()):
                            decoded=''.join(a[(a.index(c)-candidate[i%p])%4] for i,c in enumerate(cipher))
                            if mask_text(decoded,mask)==decoded:brute.append(list(candidate))
                    actual=[] if got['status']!='recovered_transformed_stream' else [got['key']]
                    assert actual==brute;oracle_cases+=1
    elapsed=time.monotonic()-started
    assert elapsed<10,'controls cap exceeded; no K4 proof'
    return {'status':'passed','primary_seeded_recovery_cases':primary,'supplementary_recovery_cases':supplement,'supplementary_count':288,'small_alphabet_oracle_cases':oracle_cases,'low_information_reports_four_free_phases':True,'unsupported_context_rejected':True,'elapsed_seconds':round(elapsed,6),'original_text_recovery_claim':'CL mask is lossy; only transformed stream/key recovered. Identity/parameter aliases retained. Synthetic letterstreams are not a natural-language or historical validation benchmark.'}

def inherited_proof():
    data=json.loads((ROOT/'data/k4.json').read_text());known=known_original();first=list(range(21,34));witnesses=[];spans=[]
    expected={('AZ','plus'):'BLZCDCYYGCKAZ',('KRYPTOS','plus'):'RDUMRIYWOYNKY',('AZ','beaufort'):'JLJODEGKUKKKL',('KRYPTOS','beaufort'):'WXAKGZTOAXAFD'}
    targets={m:mask_known(known,97,m) for m in ('identity','CL')}
    assert [i+1 for i in known if known[i]!=targets['CL'][i]]==[70]
    for name,a in ALPHABETS:
        for eq in EQUATIONS:
            values=[required_key(known[i],data['ciphertext'][i],a,eq) for i in first];span=''.join(a[v] for v in values)
            if (name,eq) in expected:assert span==expected[(name,eq)]
            spans.append({'alphabet':name,'equation':eq,'first13_required_key_symbols':span,'zero_based_values':values})
            for mask in ('identity','CL'):
                assert all(targets[mask][i]==known[i] for i in first)
                for p in range(1,13):
                    seen={};conflict=None
                    for i,k in zip(first,values):
                        phase=i%p
                        if phase in seen and seen[phase][1]!=k:
                            conflict=(seen[phase][0],i,seen[phase][1],k);break
                        seen[phase]=(i,k)
                    assert conflict is not None
                    i,j,u,v=conflict
                    witnesses.append({'mask':mask,'alphabet':name,'equation':eq,'period':p,'one_based_positions':[i+1,j+1],'required_values':[u,v],'avoids_changed_position70':True,'status':'inherited_contradiction'})
    return {'classification':'Inherited ROUTE-001 exclusion, not new K4 search coverage','original_cribs':['EASTNORTHEAST','BERLINCLOCK'],'transformed_CL_cribs':['EASTNORTHEAST','BERLINKLOCK'],'changed_one_based_positions':[70],'required_key_spans':spans,'inherited_witnesses':witnesses,'inherited_case_count':144,'new_K4_key_searches':0,'full_K4_plaintexts_emitted':False,'scope':'Only direct AZ/KRYPTOS plus/minus/trueBeaufort, periods1-12, and these two masks; any preprocessing leaving first13 known English letters unchanged inherits these same witnesses under unchanged alignment.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--spec-commit',required=True);p.add_argument('--code-commit',required=True);args=p.parse_args()
    checked=controls();begun=time.monotonic();proof=inherited_proof();assert time.monotonic()-begun<5
    files=['experiments/phonetic_cl.py','tests/test_phonetic_cl.py','research/specifications/PHONETIC-CL-001.json','data/k4.json','experiments/bounded_models.py']
    print(json.dumps({'experiment':'PHONETIC-CL-001','spec_commit':args.spec_commit,'code_commit':args.code_commit,'input_sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files},'controls':checked,'proof':proof},indent=2))
