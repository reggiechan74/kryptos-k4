"""Four preregistered crossed-coordinate affine digraph necessary conditions."""
import argparse,hashlib,itertools,json,time
from pathlib import Path
from exact_linear import solve_ring,contains,ring_vectors
ROOT=Path(__file__).resolve().parents[1]
AZ='ABCDEFGHIJKLMNOPQRSTUVWXYZ';KR='KRYPTOSABCDEFGHIJLMNQUVWXZ'

def pairs(origin,start,end):return [i for i in range(origin-1,96,2) if start<=i and i+1<end]

def system(cipher,plain,ai,ao,origin,start,end):
    starts=pairs(origin,start,end);A=[[ai.index(plain[i]),ai.index(plain[i+1]),1] for i in starts]
    ys=[[ao.index(cipher[i+j]) for i in starts] for j in range(2)]
    return dict(pair_starts_one_based=[i+1 for i in starts],matrix=A,rhs=ys,rows=[solve_ring(A,y,26,3) for y in ys])

def verify_certificate(A,y,field):
    if field['consistent']:return
    p=field['prime'];weights=field['contradiction']['equation_weights']
    assert all(sum(w*row[j] for w,row in zip(weights,A))%p==0 for j in range(3))
    assert sum(w*v for w,v in zip(weights,y))%p==field['contradiction']['rhs']!=0

def analyze(cipher,plain):
    records=[]
    for ni,ai,no,ao in (('AZ',AZ,'KRYPTOS',KR),('KRYPTOS',KR,'AZ',AZ)):
        for origin in (1,2):
            tr=system(cipher,plain,ai,ao,origin,21,34)
            for y,row in zip(tr['rhs'],tr['rows']):
                for f in row['fields']:verify_certificate(tr['matrix'],y,f)
            count=tr['rows'][0]['cardinality']*tr['rows'][1]['cardinality']
            row=dict(input=ni,output=no,pair_origin=origin,training=tr,training_parameter_tuples=str(count),second_stage_evaluated=False)
            if count:
                full=system(cipher,plain,ai,ao,origin,63,74)
                A=tr['matrix']+full['matrix'];ys=[x+y for x,y in zip(tr['rhs'],full['rhs'])]
                spaces=[solve_ring(A,y,26,3) for y in ys]
                row.update(second_stage_evaluated=True,all_crib_rows=spaces,all_crib_parameter_tuples=str(spaces[0]['cardinality']*spaces[1]['cardinality']),status='compatible_relaxation_not_candidate' if all(s['consistent'] for s in spaces) else 'impossible_second_stage')
            else:row.update(status='impossible_training',all_crib_parameter_tuples='0')
            records.append(row)
    return records

def encrypt(p,ai,ao,origin,M,b):
    out=list(p)
    for i in range(origin-1,len(p)-1,2):
        x=[ai.index(p[i]),ai.index(p[i+1])]
        for j in range(2):out[i+j]=ao[(sum(a*v for a,v in zip(M[j],x))+b[j])%26]
    return ''.join(out)

def controls():
    p=list((AZ*4)[:97]);p[21:34]='EASTNORTHEAST';p[63:74]='BERLINCLOCK';p=''.join(p);plants=[]
    for ai,ao,origin,M in itertools.product((AZ,KR),(AZ,KR),(1,2),([[1,0],[0,1]],[[1,2],[3,5]],[[0,0],[0,0]],[[2,0],[0,2]])):
        if ai==ao:continue
        b=[5,7];c=encrypt(p,ai,ao,origin,M,b);s=system(c,p,ai,ao,origin,21,34)
        assert all(contains(sp,list(m)+[offset]) for sp,m,offset in zip(s['rows'],M,b))
        plants.append(dict(origin=origin,input='AZ' if ai==AZ else 'KRYPTOS',matrix=M,truth_included=True))
    comparisons=0
    for q in (2,3,6):
        for n in range(12):
            A=[[1,(j+n)%q,(j*j+2*n)%q] for j in range(4)];y=[(j*3+n)%q for j in range(4)]
            expected={v for v in itertools.product(range(q),repeat=3) if all(sum(a*b for a,b in zip(row,v))%q==value for row,value in zip(A,y))}
            actual=set(ring_vectors(solve_ring(A,y,q,3)));assert actual==expected;comparisons+=1
    return dict(literal_crib_plants=plants,complete_small_ring_comparisons=comparisons)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--controls',action='store_true');ap.add_argument('--actual',action='store_true');ap.add_argument('--output',required=True);a=ap.parse_args();out={}
    if a.controls:out['controls']=controls()
    if a.actual:
        d=json.loads((ROOT/'data/k4.json').read_text());p=['?']*97
        for c in d['cribs']:p[c['start']-1:c['end']]=c['plaintext']
        start=time.monotonic();out['structures']=analyze(d['ciphertext'],''.join(p));assert time.monotonic()-start<1
    out['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),ROOT/'research/AFFINE-DIGRAPH-CROSSED-SPEC.md',ROOT/'experiments/exact_linear.py',ROOT/'data/k4.json')}
    Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
