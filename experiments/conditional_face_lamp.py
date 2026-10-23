"""Approved finite face/lamp pilots; controls and actual evaluation are separate."""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import time
from bounded_models import model_encrypt,model_decrypt,inverse_permutation
from face_row_coverage import coverage,occupied_cells,catalogue

ROOT=Path(__file__).resolve().parents[1]
ALPHABETS={'AZ':'ABCDEFGHIJKLMNOPQRSTUVWXYZ','KRYPTOS':'KRYPTOSABCDEFGHIJLMNQUVWXZ'}
WINDOWS=((21,'EASTNORTHEAST'),(63,'BERLINCLOCK'))
SPEC=ROOT/'research/CONDITIONAL-FACE-LAMP-SPEC.md'
FROZEN='cdefbb4bc4cf6f2420789bba9876149d8e8dad57'


def limits(start,seconds=120):
    if time.monotonic()-start>seconds:raise TimeoutError('frozen stage budget exceeded; unresolved')


def inputs():
    paths=[SPEC,Path(__file__),ROOT/'data/k4.json',ROOT/'results/FACE-ROW-001-COVERAGE.json']
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def face_cases():
    old=json.loads((ROOT/'results/FACE-ROW-001-COVERAGE.json').read_text())
    fresh=coverage()
    assert old==fresh,'coverage or source changed'
    rows=[r for r in fresh['records'] if not r['prior_coverage']]
    assert len(rows)==92
    return rows


def face_fit(cipher,case):
    a=ALPHABETS[case['alphabet']];p=case['period'];inv=inverse_permutation(case['permutation'])
    assigned={};constraints=[];conflicts=[]
    for offset,plain in enumerate(WINDOWS[0][1]):
        i=21+offset;j=inv[i];phase=(i if case['order']=='sub_then_route' else j)%p
        value=(a.index(cipher[j])+(-1 if case['equation']=='plus' else 1)*a.index(plain))%26
        row={'plaintext_position':i+1,'ciphertext_position':j+1,'plaintext':plain,'ciphertext':cipher[j],'phase':phase,'required_key':value}
        if phase in assigned and assigned[phase]['required_key']!=value:conflicts.append({'first':assigned[phase],'second':row})
        assigned.setdefault(phase,row);constraints.append(row)
    assert len(assigned)==p,'training must determine every phase, even when inconsistent'
    return {'consistent':not conflicts,'constraints':constraints,'first_conflict':conflicts[0] if conflicts else None,
            'fitted_key_entries':p,'redundant_training_equalities':13-p,'unfitted_entries':0,
            'key':[assigned[j]['required_key'] for j in range(p)] if not conflicts else None}


def face_select(cipher,cases):
    out=[]
    for case in cases:
        fit=face_fit(cipher,case)
        row={k:case[k] for k in ('case_id','alphabet','period','equation','order','aliases')};row['training']=fit
        row['berlin_evaluated']=fit['consistent'];row['all_pass']=False
        if fit['consistent']:
            a=ALPHABETS[case['alphabet']];plain=model_decrypt(cipher,fit['key'],a,case['equation'],case['permutation'],case['order'])
            assert plain[21:34]==WINDOWS[0][1]
            regen=model_encrypt(plain,fit['key'],a,case['equation'],case['permutation'],case['order'])==cipher
            assert regen
            row.update(predicted_berlin=plain[63:74],berlin_matches=sum(x==y for x,y in zip(plain[63:74],WINDOWS[1][1])),
                       predicted_positions=11,all_pass=plain[63:74]==WINDOWS[1][1],full_regeneration=regen,
                       plaintext=plain,plaintext_sha256=hashlib.sha256(plain.encode()).hexdigest())
        if fit['consistent']:
            key=fit['key'];row['minimal_repeating_key_period']=next(d for d in range(1,len(key)+1) if len(key)%d==0 and all(v==key[j%d] for j,v in enumerate(key)))
        out.append(row)
    return out


def direct_face_encode(plain,case,key,wrong_rows=False,phase_shift=0):
    # Independent reflected-cell matrix, not the route cipher's permute routine.
    cells=[divmod(i,31) for i in range(97)] if wrong_rows else occupied_cells()
    ordered=sorted(((r,30-c),i) for i,(r,c) in enumerate(cells));a=ALPHABETS[case['alphabet']];out=[]
    for j,(_,i) in enumerate(ordered):
        phase=(i if case['order']=='sub_then_route' else j)+phase_shift
        k=key[phase%len(key)];p=a.index(plain[i]);out.append(a[((p+k) if case['equation']=='plus' else (k-p))%26])
    return ''.join(out)


def literal_plant():
    phrase='THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG'
    p=list((phrase*3)[:97])
    for start,word in WINDOWS:p[start:start+len(word)]=word
    return ''.join(p)


def face_controls(cases):
    started=time.monotonic();plain=literal_plant();plants=[];wrong_rows=0;wrong_timing=0
    for case in cases:
        a=ALPHABETS[case['alphabet']];key=[(7*j+11*case['period']+3)%26 for j in range(case['period'])]
        cipher=model_encrypt(plain,key,a,case['equation'],case['permutation'],case['order'])
        assert cipher==direct_face_encode(plain,case,key)
        assert model_decrypt(cipher,key,a,case['equation'],case['permutation'],case['order'])==plain
        records=face_select(cipher,cases);good=[r for r in records if r['all_pass']]
        true=next(r for r in good if r['case_id']==case['case_id'])
        assert true['training']['key']==key and true['plaintext']==plain
        retained=[{'case_id':r['case_id'],'key':r['training']['key'],'plaintext_sha256':r['plaintext_sha256']} for r in good]
        plants.append({'planted_case':case['case_id'],'key':key,'truth_retained':True,'compatible_models':retained,
                       'distinct_full_plaintexts':len({r['plaintext_sha256'] for r in good})})
        assert direct_face_encode(plain,case,key,wrong_rows=True)!=cipher;wrong_rows+=1
        if case['period']>1:
            assert direct_face_encode(plain,case,key,phase_shift=1)!=cipher;wrong_timing+=1
        limits(started)
    incompatible=face_select('A'*97,cases)
    assert not any(r['all_pass'] for r in incompatible)
    return {'literal_plants':plants,'selector_descriptions':92*92,'wrong_row_mutations_detected':wrong_rows,
            'phase_shift_mutations_detected':wrong_timing,'period_one_timing_mutation':'equivalent; not counted as negative',
            'constant_cipher_full_selector_survivors':0,'seconds':time.monotonic()-started}


def lamp_bits(minute,phase):
    if type(minute) is not int or not 0<=minute<1440 or type(phase) is not int or phase not in (0,1):raise ValueError('invalid minute or indicator state')
    h,m=divmod(minute,60);counts=(h//5,h%5,m//5,m%5)
    return (phase,)+tuple(int(j<n) for n,size in zip(counts,(4,4,11,4)) for j in range(size))


def lamp_inverse(bits):
    bits=tuple(bits)
    if len(bits)!=24 or any(type(b) is not int or b not in (0,1) for b in bits):raise ValueError('24 binary fields required')
    counts=[];offset=1
    for size in (4,4,11,4):
        row=bits[offset:offset+size];n=sum(row)
        if row!=(1,)*n+(0,)*(size-n):raise ValueError('nonconsecutive row lamps')
        counts.append(n);offset+=size
    a,b,c,d=counts;h=5*a+b;m=5*c+d
    if h>=24 or m>=60:raise ValueError('invalid civil time')
    return 60*h+m,bits[0]


def lamp_code(minute,phase):
    return sum(b<<j for j,b in enumerate(lamp_bits(minute,phase)))


def lamp_oracle(minute,phase):
    h=minute//60;m=minute-60*h;bits=[phase]
    for value,width,unit in ((h,4,5),(h%5,4,1),(m,11,5),(m%5,4,1)):
        for _ in range(width):
            on=int(value>=unit);bits.append(on);value-=unit*on
    return int(''.join(map(str,reversed(bits))),2)


def lamp_streams():
    values=[[lamp_code(t,p)%26 for t in range(1440)] for p in (0,1)]
    groups={}
    for t,p in itertools.product(range(1440),(0,1)):
        stream=tuple(values[p][(t+i)%1440] for i in range(97))
        groups.setdefault(stream,[]).append({'start_minute':t,'indicator':p})
    return [{'stream_id':'LS-%04d'%i,'key':list(key),'aliases':aliases} for i,(key,aliases) in enumerate(groups.items())]


def lamp_crypt(text,key,alphabet,equation,decrypt=False):
    if len(text)!=len(key) or any(c not in alphabet for c in text):raise ValueError('framed uppercase text and matching key needed')
    if equation not in ('plus','beaufort'):raise ValueError('unknown equation')
    values=[alphabet.index(c) for c in text]
    return ''.join(alphabet[((v-k if decrypt else v+k) if equation=='plus' else k-v)%26] for v,k in zip(values,key))


def required_keys(cipher,alphabet,equation,windows=WINDOWS):
    sign=-1 if equation=='plus' else 1
    return [(start+j,(alphabet.index(cipher[start+j])+sign*alphabet.index(p))%26)
            for start,word in windows for j,p in enumerate(word)]


def parity_certificate(cipher,alphabet,equation):
    rows=required_keys(cipher,alphabet,equation,WINDOWS[:1])
    pair=next(((i,k,j,l) for n,(i,k) in enumerate(rows) for j,l in rows[n+1:] if k%2!=l%2),None)
    return {'required_training_keys':[{'position':i+1,'key':k,'parity':k%2} for i,k in rows],
            'constant_parity_possible':pair is None,'witness':None if pair is None else
            {'positions':[pair[0]+1,pair[2]+1],'required_keys':[pair[1],pair[3]],'required_parities':[pair[1]%2,pair[3]%2]}}


def lamp_selector(cipher,streams):
    out=[];logical=0;pruned=0;unique_scored=0;raw_scored=0
    for name,a in ALPHABETS.items():
        for eq in ('plus','beaufort'):
            cert=parity_certificate(cipher,a,eq)
            if not cert['constant_parity_possible']:
                logical+=2880;pruned+=2880;continue
            first=required_keys(cipher,a,eq,WINDOWS[:1]);second=required_keys(cipher,a,eq,WINDOWS[1:])
            for row in streams:
                logical+=len(row['aliases']);raw_scored+=len(row['aliases']);unique_scored+=1;key=row['key']
                if not all(key[i]==v for i,v in first):continue
                if not all(key[i]==v for i,v in second):continue
                plain=lamp_crypt(cipher,key,a,eq,True)
                assert all(plain[s:s+len(w)]==w for s,w in WINDOWS)
                assert lamp_crypt(plain,key,a,eq)==cipher
                out.append({'alphabet':name,'equation':eq,'stream_id':row['stream_id'],'aliases':row['aliases'],
                            'plaintext_sha256':hashlib.sha256(plain.encode()).hexdigest()})
    assert logical==11520
    return {'compatible':out,'raw_compatible_descriptions':sum(len(r['aliases']) for r in out),
            'distinct_full_plaintexts':len({r['plaintext_sha256'] for r in out}),
            'raw_descriptions_accounted':logical,'parity_pruned_descriptions':pruned,
            'unique_stream_models_checked':unique_scored,'raw_after_parity_checked':raw_scored,'full_plaintext_decryptions':len(out)}


def stream_overlap(stream):
    # Exact complete-stream membership in prior period/progressive domains, no crib fitting.
    periodic=[];progressive=[]
    for p in range(1,13):
        d=(stream[p]-stream[0])%26
        if all((stream[i]-stream[i-p])%26==d for i in range(p,97)):
            progressive.append({'period':p,'drift':d})
            if d==0:periodic.append(p)
    return {'periods_1_to_12':periodic,'progressive_p1_to12_d0_to25':progressive}


def lamp_controls(streams):
    started=time.monotonic();patterns=set();invalid=0
    for t,p in itertools.product(range(1440),(0,1)):
        bits=lamp_bits(t,p);code=lamp_code(t,p)
        assert lamp_inverse(bits)==(t,p) and code==lamp_oracle(t,p)
        assert code%2==p and (code%26)%2==p;patterns.add(code)
    assert len(patterns)==2880
    bad=[(),(0,)*23,(2,)+(0,)*23,(0,0,1)+(0,)*21,(0,)+(1,)*8+(0,)*15]
    for bits in bad:
        try:lamp_inverse(bits)
        except ValueError:invalid+=1
        else:raise AssertionError('invalid display accepted')
    by_alias={(a['start_minute'],a['indicator']):r for r in streams for a in r['aliases']}
    plain=literal_plant();plants=[];timing=0
    for t,p,name,eq in itertools.product((0,58,719,1438),(0,1),ALPHABETS,('plus','beaufort')):
        a=ALPHABETS[name];row=by_alias[t,p];key=row['key'];cipher=lamp_crypt(plain,key,a,eq)
        assert lamp_crypt(cipher,key,a,eq,True)==plain
        # Independently decode directly from the subtractive lamp oracle.
        independent=[]
        for i,c in enumerate(cipher):
            k=lamp_oracle((t+i)%1440,p)%26;v=a.index(c)
            independent.append(a[((v-k) if eq=='plus' else k-v)%26])
        assert ''.join(independent)==plain
        selected=lamp_selector(cipher,streams)
        assert any(r['alphabet']==name and r['equation']==eq and {'start_minute':t,'indicator':p} in r['aliases'] for r in selected['compatible'])
        plants.append({'start_minute':t,'indicator':p,'alphabet':name,'equation':eq,'truth_retained':True,**selected})
        wrong=[lamp_oracle((t+i+1)%1440,p)%26 for i in range(97)]
        assert lamp_crypt(plain,wrong,a,eq)!=cipher;timing+=1;limits(started)
    incompatible=lamp_selector('A'*97,streams);assert not incompatible['compatible']
    return {'display_states':2880,'distinct_full_patterns':len(patterns),'invalid_patterns_rejected':invalid,
            'literal_plants':plants,'selector_descriptions':32*11520,'timing_mutants_detected':timing,
            'constant_cipher_control':incompatible,'seconds':time.monotonic()-started}


def run_controls():
    start=time.monotonic();cases=face_cases();streams=lamp_streams()
    out={'kind':'controls before actual K4 evaluation','frozen_protocol_commit':FROZEN,'source_sha256':inputs(),
         'face':face_controls(cases),'lamp':lamp_controls(streams),'lamp_streams':streams,
         'raw_clock_states':2880,'distinct_lamp_streams':len(streams)}
    for row in streams:row['prior_stream_overlap']=stream_overlap(row['key'])
    out['prior_stream_overlap_summary']={'periodic_streams':sum(bool(r['prior_stream_overlap']['periods_1_to_12']) for r in streams),
        'progressive_streams':sum(bool(r['prior_stream_overlap']['progressive_p1_to12_d0_to25']) for r in streams),
        'fixed_repeating_words':'subsets of the periodic stream domain; no wider fixed/autokey equivalence claim'}
    out['total_seconds']=time.monotonic()-start
    return out


def actual():
    started=time.monotonic();cases=face_cases();data=json.loads((ROOT/'data/k4.json').read_text());cipher=data['ciphertext']
    assert [(c['start']-1,c['plaintext']) for c in data['cribs']]==list(WINDOWS)
    face=face_select(cipher,cases);limits(started)
    certs=[{'alphabet':name,'equation':eq,**parity_certificate(cipher,a,eq)} for name,a in ALPHABETS.items() for eq in ('plus','beaufort')]
    # Stop at the proved obstruction; a non-rejection would remain unresolved, not silently become an expanded scan.
    lamp_reject=all(not r['constant_parity_possible'] for r in certs)
    out={'frozen_protocol_commit':FROZEN,'source_sha256':inputs(),
         'face':{'models_tested':92,'previously_covered_skipped':280,'records':face,
                 'first_crib_survivors':sum(r['training']['consistent'] for r in face),
                 'all_crib_survivors':sum(r['all_pass'] for r in face),
                 'distinct_training_plaintexts':len({r['plaintext_sha256'] for r in face if r['training']['consistent']}),
                 'distinct_all_crib_plaintexts':len({r['plaintext_sha256'] for r in face if r['all_pass']})},
         'lamp':{'status':'analytical_exclusion' if lamp_reject else 'unresolved_requires_planned_enumeration',
                 'certificates':certs,'raw_descriptions_excluded_by_proof':11520 if lamp_reject else None,
                 'actual_phase_models_enumerated':0,'berlin_consulted':False,
                 'compatible_full_plaintexts':0 if lamp_reject else None},
         'seconds':time.monotonic()-started}
    return out

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('controls','actual'));parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    result=run_controls() if args.stage=='controls' else actual()
    encoded=json.dumps(result,indent=2)+'\n';assert len(encoded.encode())<(128 if args.stage=='controls' else 64)*1024**2
    args.output.write_text(encoded)
