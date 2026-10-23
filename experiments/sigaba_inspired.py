"""Custom SIGABA-inspired machine; explicitly NOT an authentic SIGABA emulator."""
import argparse,hashlib,itertools,json,time
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/sigaba-inspired-v1.json';SPEC=ROOT/'research/GREEK-SIGABA-CANDIDATE-SPEC.md';AZ='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
WINDOWS=((21,'EASTNORTHEAST'),(63,'BERLINCLOCK'))
PLANTS=((0,0,0),(25,25,9),(7,14,3),(13,2,4),(1,8,5),(24,3,8),(5,21,1),(19,10,6),(11,17,2),(3,23,7),(16,6,0),(22,12,9))


def tables(wirings,n):
    forward=[];reverse=[]
    for w in wirings:
        assert sorted(w)==list(range(n))
        rotor=[[(w[(x+p)%n]-p)%n for x in range(n)] for p in range(n)]
        forward.append(rotor);reverse.append([[row.index(x) for x in range(n)] for row in rotor])
    return forward,reverse


def machine():
    d=json.loads(DATA.read_text());cw=[[AZ.index(c) for c in s] for s in d['cipher_wirings']];sw=[[AZ.index(c) for c in s] for s in d['control_wirings']]
    cf,ci=tables(cw,26);sf,_=tables(sw,26);xf,_=tables(d['index_wirings'],10)
    return {'data':d,'cipher':cf,'inverse':ci,'control':sf,'index':xf,'cipher_raw':cw,'control_raw':sw}


def advance_control(pos):
    pos[2]=(pos[2]+1)%26
    if pos[2]==0:
        pos[3]=(pos[3]+1)%26
        if pos[3]==0:pos[1]=(pos[1]+1)%26


def schedule(m,q,r,length=97):
    pos=[0,0,q,0,0];ticks=[0]*5;out=[];masks=[]
    for _ in range(length):
        out.append(tuple(ticks));selected=set()
        for signal in m['data']['live_control_inputs']:
            x=signal
            for j in range(5):x=m['control'][j][pos[j]][x]
            x%=10
            for j in range(5):x=m['index'][j][r][x]
            selected.add(x//2)
        assert 1<=len(selected)<=4
        masks.append(tuple(sorted(selected)))
        for j in selected:ticks[j]=(ticks[j]+1)%26
        advance_control(pos)
    return tuple(out),masks


def schedule_oracle(m,q,r,length=97):
    counts=[0]*5;states=[]
    for i in range(length):
        states.append(tuple(x%26 for x in counts));z=q+i
        pos=[0,(z//676)%26,z%26,(z//26)%26,0];hits=[]
        for x in (5,6,7,8):
            for w,o in zip(m['control_raw'],pos):x=(w[(x+o)%26]-o)%26
            x%=10
            for w in m['data']['index_wirings']:x=(w[(x+r)%10]-r)%10
            hits.append(x//2)
        counts=[v+int(j in hits) for j,v in enumerate(counts)]
    return tuple(states)


def schedules(m):
    found={};hist=Counter()
    for q,r in itertools.product(range(26),range(10)):
        states,masks=schedule(m,q,r);assert states==schedule_oracle(m,q,r)
        hist.update(len(x) for x in masks)
        found.setdefault(states,[]).append({'q':q,'r':r})
    return [{'schedule_id':'S-%03d'%i,'states':[list(x) for x in st],'aliases':aliases} for i,(st,aliases) in enumerate(found.items())],dict(hist)


def letter(x,m,state,c,decrypt=False):
    for j in (range(4,-1,-1) if decrypt else range(5)):
        x=m['inverse' if decrypt else 'cipher'][j][(state[j]+c)%26][x]
    return x


def crypt(text,m,states,c,decrypt=False):
    if len(text)>len(states) or any(x not in AZ for x in text):raise ValueError('invalid framed input or schedule')
    return ''.join(AZ[letter(AZ.index(x),m,states[i],c,decrypt)] for i,x in enumerate(text))


def direct_crypt(text,m,q,c,r,decrypt=False):
    st=schedule_oracle(m,q,r,len(text));out=[]
    for i,ch in enumerate(text):
        x=AZ.index(ch)
        for j in (range(4,-1,-1) if decrypt else range(5)):
            w=m['cipher_raw'][j];o=(st[i][j]+c)%26
            x=((w.index((x+o)%26) if decrypt else w[(x+o)%26])-o)%26
        out.append(AZ[x])
    return ''.join(out)


def select(cipher,m,groups,details=False):
    started=time.monotonic();rows=[];good=[];first_count=0;raw_first=0;raw=0;canonical=0
    cv=[AZ.index(x) for x in cipher]
    for group in groups:
        states=group['states']
        for c in range(26):
            raw+=len(group['aliases']);canonical+=1;first=None
            for off,p in enumerate(WINDOWS[0][1]):
                i=21+off;expected=letter(AZ.index(p),m,states[i],c)
                if expected!=cv[i]:first={'position':i+1,'expected_cipher':AZ[expected],'actual_cipher':cipher[i],'cipher_positions':[(v+c)%26 for v in states[i]]};break
            row={'schedule_id':group['schedule_id'],'cipher_offset':c,'raw_keys':group['aliases'],'first_conflict':first,'berlin_evaluated':first is None}
            if first is None:
                first_count+=1;raw_first+=len(group['aliases']);matches=[]
                for off,p in enumerate(WINDOWS[1][1]):
                    i=63+off;matches.append(letter(AZ.index(p),m,states[i],c)==cv[i])
                row['berlin_matches']=sum(matches)
                if all(matches):
                    plain=crypt(cipher,m,states,c,True);assert crypt(plain,m,states,c)==cipher
                    assert all(plain[s:s+len(w)]==w for s,w in WINDOWS)
                    cand={**row,'plaintext':plain,'plaintext_sha256':hashlib.sha256(plain.encode()).hexdigest(),'full_regeneration':True};good.append(cand)
            if details:rows.append(row)
        if time.monotonic()-started>120:raise TimeoutError('SIGABA-inspired selector unresolved')
    assert raw==6760
    return {'raw_keys_accounted':raw,'schedule_normalized_models_checked':canonical,'training_survivors':first_count,
            'raw_training_survivors':raw_first,'raw_compatible_keys':sum(len(g['raw_keys']) for g in good),
            'compatible':good,'distinct_full_plaintexts':len({r['plaintext_sha256'] for r in good}),
            'records':rows,'seconds':time.monotonic()-started}


def plant_plain():
    text=list(('THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG'*3)[:97])
    for s,w in WINDOWS:text[s:s+len(w)]=w
    return ''.join(text)


def controls(m,groups):
    started=time.monotonic();count=0
    for wirings,n in ((m['cipher_raw'],26),(m['control_raw'],26),(m['data']['index_wirings'],10)):
        forwards,inverses=tables(wirings,n)
        for f,inv in zip(forwards,inverses):
            for p in range(n):
                for x in range(n):assert inv[p][f[p][x]]==x;count+=1
    for q,r in ((0,0),(25,9),(7,3)):
        st,_=schedule(m,q,r,805);assert st==schedule_oracle(m,q,r,805)
    plain=plant_plain();plants=[];timing=0
    for q,c,r in PLANTS:
        states,_=schedule(m,q,r);cipher=crypt(plain,m,states,c)
        assert crypt(cipher,m,states,c,True)==plain
        assert direct_crypt(plain,m,q,c,r)==cipher and direct_crypt(cipher,m,q,c,r,True)==plain
        for msg in ('',AZ,AZ[::-1],'IRREGULARSTEPPINGISANEXPLICITMODEL'):
            ct=crypt(msg,m,states,c);assert crypt(ct,m,states,c,True)==msg
        selected=select(cipher,m,groups)
        assert any(g['cipher_offset']==c and {'q':q,'r':r} in g['raw_keys'] for g in selected['compatible'])
        plants.append({'q':q,'c':c,'r':r,'truth_retained':True,'compatible':selected['compatible'],
                       'distinct_full_plaintexts':selected['distinct_full_plaintexts'],'raw_compatible_keys':selected['raw_compatible_keys']})
        longer,_=schedule(m,q,r,98);assert crypt(plain,m,longer[1:],c)!=cipher;timing+=1
        if time.monotonic()-started>120:raise TimeoutError('SIGABA-inspired controls unresolved')
    bad=select('A'*97,m,groups);assert not bad['compatible']
    # Grouping supports every allowed selector cardinality, independent of actual frequency.
    for n in range(1,5):assert len({x//2 for x in range(0,2*n,2)})==n
    return {'rotor_inverse_checks':count,'long_counter_checks':3,'plants':plants,'full_selectors':12,
            'raw_keys_accounted':12*6760,'timing_mutations_detected':timing,
            'constant_cipher_survivors':0,'seconds':time.monotonic()-started}


def metadata():
    return {'specification_commit':'7bc893f','authentic_SIGABA':False,'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (SPEC,DATA,Path(__file__),ROOT/'data/k4.json')}}

def matched_null(cipher,m,groups,observed):
    import random
    if observed==0:return {'executed':False,'reason':'zero complete survivors; no significance claim'}
    rng=random.Random(2026102302);started=time.monotonic();counts=[]
    for _ in range(199):
        letters=list(cipher);rng.shuffle(letters);found=select(''.join(letters),m,groups)
        counts.append(found['raw_compatible_keys'])
        if time.monotonic()-started>120:raise TimeoutError('SIGABA-inspired null calibration unresolved')
    return {'executed':True,'seed':2026102302,'draws':199,'statistic':'complete compatible raw keys','observed':observed,'null_counts':counts,'plus_one_p':(1+sum(x>=observed for x in counts))/200}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('controls','actual'));parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();m=machine();groups,hist=schedules(m);result=metadata()
    result.update(raw_starting_keys=6760,distinct_stepping_schedules=len(groups),schedule_aliases=groups,selector_cardinality_histogram=hist)
    if args.stage=='controls':result['controls']=controls(m,groups)
    else:
        cipher=json.loads((ROOT/'data/k4.json').read_text())['ciphertext'];result['actual']=select(cipher,m,groups,True)
        result['null']=matched_null(cipher,m,groups,result['actual']['raw_compatible_keys'])
    encoded=json.dumps(result,indent=2)+'\n';assert len(encoded.encode())<128*1024**2
    args.output.write_text(encoded)
