"""Exact cyclic-disc invariant and two-round additive Feistel constraints."""
import argparse,hashlib,itertools,json,math,time
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
AZ='ABCDEFGHIJKLMNOPQRSTUVWXYZ';KR='KRYPTOSABCDEFGHIJLMNQUVWXZ'

def assign(table,reasons,x,value,source,kind):
    if x in table and table[x]!=value:
        return dict(function=kind,input=x,first_value=table[x],second_value=value,first_source=reasons[x],second_source=source)
    table[x]=value;reasons[x]=source
    return None

def infer(rows,q=26,budget=5):
    start=time.monotonic();f={};g={};fr={};gr={};failures=[]
    for row in rows:
        if row['R'] is not None:
            cert=assign(g,gr,row['X'],(row['Y']-row['R'])%q,row['positions'],'G')
            if cert:return dict(branches=[],key_count='0',contradictions=[cert],completed=True)
    for row in rows:
        if row['L'] is not None and row['R'] is not None:
            cert=assign(f,fr,row['R'],(row['X']-row['L'])%q,row['positions'],'F')
            if cert:return dict(branches=[],key_count='0',contradictions=[cert],completed=True)
    branches=[dict(F=f,G=g)]
    for row in rows:
        if row['L'] is None or row['R'] is not None:continue
        new=[]
        for branch in branches:
            choices=[branch['G'][row['X']]] if row['X'] in branch['G'] else range(q)
            for val in choices:
                r=(row['Y']-val)%q;required=(row['X']-row['L'])%q
                if r in branch['F'] and branch['F'][r]!=required:continue
                ff=branch['F'].copy();gg=branch['G'].copy();ff[r]=required;gg[row['X']]=val;new.append(dict(F=ff,G=gg))
        branches=new
        if len(branches)>10000 or time.monotonic()-start>budget:return dict(branches=None,key_count=None,completed=False,reason='branch/time budget-unresolved')
    return dict(branches=branches,key_count=str(sum(q**(2*q-len(b['F'])-len(b['G'])) for b in branches)),contradictions=failures,completed=True,branch_disjointness='Every branch split fixes a previously free G entry to a different value; descendants retain it.')

def pairs(cipher,known,origin):
    return [dict(positions=[i+1,i+2],L=known.get(i),R=known.get(i+1),X=cipher[i],Y=cipher[i+1]) for i in range(origin-1,len(cipher)-1,2) if i in known or i+1 in known]

def encrypt_pair(l,r,f,g,q):
    x=(l+f[r])%q;return x,(r+g[x])%q

def decrypt_pair(x,y,f,g,q):
    r=(y-g[x])%q;return (x-f[r])%q,r

def crypt(text,f,g,ai=AZ,ao=AZ,origin=1,decrypt=False):
    out=list(text)
    for i in range(origin-1,len(text)-1,2):
        if decrypt:
            l,r=decrypt_pair(ao.index(text[i]),ao.index(text[i+1]),f,g,len(ai));out[i:i+2]=[ai[l],ai[r]]
        else:
            x,y=encrypt_pair(ai.index(text[i]),ai.index(text[i+1]),f,g,len(ai));out[i:i+2]=[ao[x],ao[y]]
    return ''.join(out)

def domains(cipher,branches,q):
    if not branches:return None
    out=[]
    for x,y in cipher:
        ls=set();rs=set()
        for b in branches:
            for gv in ([b['G'][x]] if x in b['G'] else range(q)):
                r=(y-gv)%q;rs.add(r)
                for fv in ([b['F'][r]] if r in b['F'] else range(q)):ls.add((x-fv)%q)
        out.extend([sorted(ls),sorted(rs)])
    return out

def contains(branches,f,g):return any(all(f[x]==v for x,v in b['F'].items()) and all(g[x]==v for x,v in b['G'].items()) for b in branches)

def cyclic(w,p,d):return w[(w.index(p)+d)%len(w)]

def controls():
    inverse=0
    for n in range(2,7):
        for w in itertools.permutations(range(n)):
            for d in range(n):
                got=[cyclic(w,p,d) for p in range(n)];assert sum(p==c for p,c in enumerate(got))==(n if d==0 else 0)
                assert all(cyclic(w,c,-d)==p for p,c in enumerate(got));inverse+=n
    small=[]
    for q,v in itertools.product((2,3,4),range(4)):
        f=tuple((x*x+v)%q for x in range(q));g=tuple((x*x*x+x+v)%q for x in range(q));plain=[(i*i+v)%q for i in range(6)];cipher=[]
        for i in range(0,6,2):cipher.extend(encrypt_pair(plain[i],plain[i+1],f,g,q))
        known={i:plain[i] for i in (0,1,3,4)};rows=pairs(cipher,known,1);s=infer(rows,q);full=set()
        for ff,gg in itertools.product(itertools.product(range(q),repeat=q),repeat=2):
            if all((row['L'] is None or decrypt_pair(row['X'],row['Y'],ff,gg,q)[0]==row['L']) and (row['R'] is None or decrypt_pair(row['X'],row['Y'],ff,gg,q)[1]==row['R']) for row in rows):full.add(ff+gg)
        represented={ff+gg for ff,gg in itertools.product(itertools.product(range(q),repeat=q),repeat=2) if contains(s['branches'],ff,gg)}
        assert full==represented and int(s['key_count'])==len(full) and f+g in full;small.append(dict(modulus=q,case=v,key_count=len(full),sets_equal=True))
    plants=[];roundtrips=0
    p=list((AZ*4)[:97]);p[21:34]='EASTNORTHEAST';p[63:74]='BERLINCLOCK';p=''.join(p)
    for ai,ao,origin,v in itertools.product((AZ,KR),(AZ,KR),(1,2),range(2)):
        f=[(x*x+3*x+7)%26 if v==0 else 5 for x in range(26)];g=[(5*x*x+x+11)%26 if v==0 else (x*x*x+13*x+2)%26 for x in range(26)]
        for l,r in itertools.product(range(26),repeat=2):assert decrypt_pair(*encrypt_pair(l,r,f,g,26),f,g,26)==(l,r);roundtrips+=1
        c=crypt(p,f,g,ai,ao,origin);assert crypt(c,f,g,ai,ao,origin,True)==p
        known={i:ai.index(x) for start,word in ((21,'EASTNORTHEAST'),(63,'BERLINCLOCK')) for i,x in enumerate(word,start)}
        result=infer(pairs([ao.index(x) for x in c],known,origin));assert result['completed'] and contains(result['branches'],f,g)
        plants.append(dict(input=ai,output=ao,origin=origin,function_case=v,truth_included=True,key_count=result['key_count'],branches=len(result['branches'])))
    bad=[dict(positions=[1,2],L=0,R=0,X=1,Y=1),dict(positions=[3,4],L=0,R=0,X=1,Y=2)]
    assert infer(bad)['key_count']=='0'
    return dict(cyclic_inverse_symbol_checks=inverse,tiny_complete_function_set_comparisons=small,literal_crib_plants=plants,full_pair_roundtrips=roundtrips,repeated_entry_mutation_rejected=True)

def actual():
    data=json.loads((ROOT/'data/k4.json').read_text());c=data['ciphertext'];known={i:p for crib in data['cribs'] for i,p in enumerate(crib['plaintext'],crib['start']-1)}
    fixed=[i for i,p in known.items() if c[i]==p];witnesses=[]
    for i in fixed:
        j=next((j for j,p in known.items() if j//25==i//25 and c[j]!=p),None)
        if j is not None:witnesses.append(dict(fixed_position=i+1,fixed_plain=known[i],fixed_cipher=c[i],changed_position=j+1,changed_plain=known[j],changed_cipher=c[j],block_one_based=i//25+1,reason='Fixed symbol forces row displacement0; changed symbol in same block forbids0, for any valid cyclic disc alphabets.'))
    assert witnesses
    records=[]
    for ai,ao,origin in itertools.product((AZ,KR),(AZ,KR),(1,2)):
        cv=[ao.index(x) for x in c];train={i:ai.index(p) for i,p in known.items() if i<34};allknown={i:ai.index(p) for i,p in known.items()}
        tr=infer(pairs(cv,train,origin));full=infer(pairs(cv,allknown,origin)) if tr['completed'] and tr['branches'] else None;pred=[]
        if tr['branches']:
            ds=domains([(cv[i],cv[i+1]) for i in range(origin-1,96,2)],tr['branches'],26)
            for i in range(63,74):
                k=i-(origin-1)
                if 0<=k<len(ds) and len(ds[k])==1:pred.append(dict(position=i+1,predicted=ai[ds[k][0]],required=known[i]))
        records.append(dict(input_alphabet=ai,output_alphabet=ao,pair_origin=origin,training=tr,all_cribs=full,second_stage_evaluated=full is not None,all_crib_compatible_keys='0' if tr['completed'] and tr['key_count']=='0' else (full['key_count'] if full is not None else None),training_forced_Berlin_letters=pred,Berlin_is_public=True))
    return dict(cyclic_disc_analytical_witnesses=witnesses,disc_keys_enumerated=0,feistel_structures=records)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--controls',action='store_true');ap.add_argument('--actual',action='store_true');ap.add_argument('--output',required=True);a=ap.parse_args();out={}
    if a.controls:out['controls']=controls()
    if a.actual:out['actual']=actual()
    out['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),ROOT/'research/NONROTOR-STRUCTURAL-SPEC.md',ROOT/'data/k4.json')}
    Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
