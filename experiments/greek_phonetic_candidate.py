"""Fixed approximate Greek rendering plus periodic cipher, with unknown alignment."""
import argparse,hashlib,json,time,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/greek-phonetic-v1.json'
SPEC=ROOT/'research/GREEK-SIGABA-CANDIDATE-SPEC.md'
FROZEN='7bc893f'


def schema():
    d=json.loads(DATA.read_text());g=d['greek_alphabet']
    assert len(g)==len(set(g))==24
    source=json.loads((ROOT/d['source_fixture']).read_text())['entries']
    clean=lambda s:''.join(c for c in s if c not in '/ˈˌ .-' and not c.isspace())
    assert ''.join(d['first_phones'])==clean(source['east-northeast'])
    assert ''.join(d['second_phones'])==clean(source['berlin']+source['clock'])
    assert transcribe(d['first_phones'],d)==d['first_greek']
    assert transcribe(d['second_phones'],d)==d['second_greek']
    assert [len(d[k]) for k in ('first_greek','second_greek')]==[10,11]
    return d


def transcribe(phones,d):
    try:return ''.join(d['phone_map'][p] for p in phones)
    except KeyError as exc:raise ValueError('phone outside frozen observed inventory') from exc


def crypt(text,key,alphabet,equation,d,decrypt=False):
    if unicodedata.normalize('NFC',text)!=text:raise ValueError('NFC required')
    if not key or any(type(k) is not int or not 0<=k<26 for k in key):raise ValueError('nonempty modular key needed')
    if equation not in ('plus','beaufort'):raise ValueError('unknown equation')
    source=alphabet if decrypt else d['greek_alphabet'];target=d['greek_alphabet'] if decrypt else alphabet
    if any(c not in source for c in text):raise ValueError('character outside declared domain')
    out=[]
    for i,c in enumerate(text):
        v=source.index(c);k=key[i%len(key)]
        n=((v-k if decrypt else v+k) if equation=='plus' else k-v)%26
        if n>=len(target):raise ValueError('invalid Greek rank at position '+str(i+1))
        out.append(target[n])
    return ''.join(out)


def fit_first(cipher,a,eq,p,u,d):
    g=d['greek_alphabet'];sign=-1 if eq=='plus' else 1
    key=[None]*p;first={};conflict=None
    for j,plain in enumerate(d['first_greek']):
        i=u+j;phase=i%p;k=(a.index(cipher[i])+sign*g.index(plain))%26
        row={'position':i+1,'greek':plain,'cipher':cipher[i],'phase':phase,'required_key':k}
        if key[phase] is not None and key[phase]!=k and conflict is None:conflict={'first':first[phase],'second':row}
        if key[phase] is None:key[phase]=k;first[phase]=row
    assert None not in key
    return key if conflict is None else None,conflict


def select(cipher,d,details=False):
    assert len(cipher)==97
    start=time.monotonic();records=[];accepted=[];raw=0;first_count=0;second_checks=0;crib_only=[]
    g=d['greek_alphabet'];second_vals=[g.index(x) for x in d['second_greek']]
    for name,a in d['cipher_alphabets'].items():
        cv=[a.index(c) for c in cipher]
        for eq in d['equations']:
            sigma=1 if eq=='plus' else -1
            for p in d['periods']:
                for u in range(77):
                    n=77-u;raw+=n;key,conflict=fit_first(cipher,a,eq,p,u,d)
                    row={'alphabet':name,'equation':eq,'period':p,'first_start':u+1,'second_start_range':[u+11,87],
                         'raw_placements':n,'key_parameters':p,'extra_training_checks':10-p,'key':key,'training_conflict':conflict}
                    if key is not None:
                        first_count+=1;checks=[]
                        for v in range(u+10,87):
                            second_checks+=1;pred=[(sigma*x+key[(v+j)%p])%26 for j,x in enumerate(second_vals)]
                            mismatch=next((j for j,x in enumerate(pred) if x!=cv[v+j]),None)
                            rec={'second_start':v+1,'first_mismatch':None if mismatch is None else v+mismatch+1}
                            if mismatch is not None:
                                rec.update(expected_cipher=a[pred[mismatch]],actual_cipher=cipher[v+mismatch])
                            else:
                                candidate={'alphabet':name,'equation':eq,'period':p,'first_start':u+1,'second_start':v+1,'key':key}
                                try:plain=crypt(cipher,key,a,eq,d,True)
                                except ValueError as exc:
                                    candidate['invalid_Greek_domain']=str(exc);crib_only.append(candidate);rec['invalid_Greek_domain']=str(exc)
                                else:
                                    assert plain[u:u+10]==d['first_greek'] and plain[v:v+11]==d['second_greek']
                                    assert crypt(plain,key,a,eq,d)==cipher
                                    candidate.update(greek_plaintext=plain,plaintext_sha256=hashlib.sha256(plain.encode()).hexdigest(),full_regeneration=True)
                                    accepted.append(candidate)
                            checks.append(rec)
                        row['second_checks']=checks
                    if details:records.append(row)
                if time.monotonic()-start>120:raise TimeoutError('Greek selector unresolved: budget exceeded')
    assert raw==120120
    return {'raw_structural_alignment_descriptions':raw,'structural_families':40,'ordered_window_pairs':3003,
            'first_window_fits':first_count,'second_window_checks':second_checks,'crib_fits_invalid_Greek_domain':crib_only,
            'compatible':accepted,'distinct_full_Greek_plaintexts':len({r['plaintext_sha256'] for r in accepted}),
            'records':records,'seconds':time.monotonic()-start}


def controls(d):
    start=time.monotonic();g=d['greek_alphabet'];plants=[]
    for a in d['cipher_alphabets'].values():
        for eq in d['equations']:
            for p in d['periods']:
                key=[(7*j+9)%26 for j in range(p)]
                plain=list((g*5)[:97]);plain[7:17]=d['first_greek'];plain[55:66]=d['second_greek'];plain=''.join(plain)
                cipher=crypt(plain,key,a,eq,d);assert crypt(cipher,key,a,eq,d,True)==plain
                # Independent direct-index encoder and inverse, no crypt helper.
                sigma=1 if eq=='plus' else -1
                direct=''.join(a[(sigma*g.index(c)+key[i%p])%26] for i,c in enumerate(plain))
                assert direct==cipher
                back=[(sigma*(a.index(c)-key[i%p]))%26 for i,c in enumerate(cipher)]
                assert ''.join(g[v] for v in back)==plain
                found=select(cipher,d)
                name=next(n for n,x in d['cipher_alphabets'].items() if x==a)
                assert any(r['alphabet']==name and r['equation']==eq and r['period']==p and r['first_start']==8 and r['second_start']==56 and r['key']==key for r in found['compatible'])
                plants.append({'alphabet':name,'equation':eq,'period':p,'true_key':key,'true_starts':[8,56],
                               'truth_retained':True,'compatible':found['compatible'],
                               'distinct_full_Greek_plaintexts':found['distinct_full_Greek_plaintexts']})
                all_letters=crypt(g,key,a,eq,d);assert crypt(all_letters,key,a,eq,d,True)==g
                if time.monotonic()-start>120:raise TimeoutError('Greek controls unresolved: budget exceeded')
    # Loss is explicit, not silently assigned an English inverse.
    assert transcribe(['iː'],d)==transcribe(['ɪ'],d)=='Ι'
    invalid=0
    for op in [lambda:transcribe(['unknown'],d),lambda:crypt('A',[0],list(d['cipher_alphabets'].values())[0],'plus',d),
               lambda:crypt('Y',[0],d['cipher_alphabets']['AZ'],'plus',d,True),
               lambda:crypt('Ι\u0301',[0],d['cipher_alphabets']['AZ'],'plus',d)]:
        try:op()
        except ValueError:invalid+=1
        else:raise AssertionError('invalid input accepted')
    incompatible=select('A'*97,d);assert not incompatible['compatible']
    return {'plants':plants,'full_selectors':40,'raw_descriptions_accounted':40*120120,
            'phone_collision':[['iː'],['ɪ'],'Ι'],'invalid_inputs_rejected':invalid,
            'incompatible_constant_cipher_survivors':0,'seconds':time.monotonic()-start}


def metadata():
    return {'specification_commit':FROZEN,'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (SPEC,DATA,Path(__file__),ROOT/'data/k4.json',ROOT/'data/ipa-cambridge-us-v1.json')}}

def matched_null(cipher,d,observed):
    import random
    if observed==0:return {'executed':False,'reason':'zero complete survivors; no significance claim'}
    rng=random.Random(2026102301);started=time.monotonic();counts=[]
    for _ in range(199):
        letters=list(cipher);rng.shuffle(letters);text=''.join(letters);found=select(text,d)
        counts.append(len(found['compatible']))
        if time.monotonic()-started>120:raise TimeoutError('Greek null calibration unresolved')
    return {'executed':True,'seed':2026102301,'draws':199,'statistic':'complete compatible model/alignment descriptions','observed':observed,'null_counts':counts,'plus_one_p':(1+sum(x>=observed for x in counts))/200}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('controls','actual'));parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();d=schema();result=metadata()
    if args.stage=='controls':result['controls']=controls(d)
    else:
        cipher=json.loads((ROOT/'data/k4.json').read_text())['ciphertext'];result['actual']=select(cipher,d,True)
        result['null']=matched_null(cipher,d,len(result['actual']['compatible']))
    raw=json.dumps(result,ensure_ascii=False,indent=2)+'\n';assert len(raw.encode())<128*1024**2
    args.output.write_text(raw)
