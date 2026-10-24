"""Literal2:1 and explicitly rounded22.5degree routes, without invented letter padding."""
import collections,decimal,gzip,hashlib,json,math,random,sys,time
from pathlib import Path
from datetime import datetime,timezone
import candidate_first_048 as c
import finite_hand_operators as f
ROOT=Path(__file__).resolve().parents[1];KINDS=('literal_no_wrap','literal_torus','digital_ene_no_wrap')
def route(width,start,kind,n=97):
 h=(n+width-1)//width;used=[False]*n;out=[];root=start;smallest=0
 while len(out)<n:
  r,col=divmod(root,width);j=0;v=root
  while not used[v]:
   used[v]=True;out.append(v);j+=1
   if kind=='literal_torus':
    for attempts in range(1,width*h+1):
     col=(col+2)%width;r=(r-1)%h;v=r*width+col
     if v<n:break
    else:raise AssertionError('finite orbit containing current actual cell lost all actual cells')
   else:
    rr,cc=(r-j,col+2*j) if kind=='literal_no_wrap' else (r-(math.isqrt(2*j*j)-j),col+j)
    if not (0<=rr<h and 0<=cc<width) or rr*width+cc>=n:break
    v=rr*width+cc
  while smallest<n and used[smallest]:smallest+=1
  if smallest<n:root=smallest
 assert sorted(out)==list(range(n));return bytes(out)
def reference(width,start,kind,n=97):
 cells={(i//width,i%width):i for i in range(n)};remaining=set(cells.values());out=[];origin=start;h=(n+width-1)//width
 with decimal.localcontext() as ctx:
  ctx.prec=60;slope=decimal.Decimal(2).sqrt()-1
  while remaining:
   rr,cc=divmod(origin,width);j=0;point=origin
   while point in remaining:
    out.append(point);remaining.remove(point);j+=1
    if kind=='literal_torus':
     row,col=divmod(point,width);poss=[((row-k)%h,(col+2*k)%width) for k in range(1,width*h+1)];coord=next(x for x in poss if x in cells)
    elif kind=='literal_no_wrap':coord=rr-j,cc+2*j
    else:coord=rr-int(decimal.Decimal(j)*slope),cc+j
    if coord not in cells:break
    point=cells[coord]
   if remaining:origin=min(remaining)
 return bytes(out)
def variants():
 out=[dict(label='no_arithmetic',alphabet=None,key=None,s=1,t=0)]
 for name,a in c.ALPHABETS.items():
  for eq,(s,t) in c.EQUATIONS.items():
   for key in f.KEYS:out.append(dict(label=name+'/'+eq+'/'+key,alphabet=a,key=key,s=s,t=t))
 assert len(out)==19;return out
def decode(C,p,v):
 R=''.join(C[j] for j in p)
 if v['key'] is None:return R
 a=v['alphabet'];return ''.join(a[v['s']*(a.index(x)-v['t']*a.index(v['key'][i%len(v['key'])]))%26] for i,x in enumerate(R))
def encode(P,p,v):
 R=P if v['key'] is None else ''.join(v['alphabet'][(v['s']*v['alphabet'].index(x)+v['t']*v['alphabet'].index(v['key'][i%len(v['key'])]))%26] for i,x in enumerate(P))
 C=['']*len(P)
 for i,j in enumerate(p):C[j]=R[i]
 return ''.join(C)
def requirements(known,v):
 return bytes(ord(x) if v['key'] is None else ord(v['alphabet'][(v['s']*v['alphabet'].index(x)+v['t']*v['alphabet'].index(v['key'][i%len(v['key'])]))%26]) for i,x in sorted(known.items()))
def compile_routes(budget):
 unique={};counts=collections.Counter();refchecks=0
 for kind in KINDS:
  for width in range(1,98):
   budget.check()
   for start in range(97):
    p=route(width,start,kind);assert p==reference(width,start,kind);refchecks+=1
    for direction,pp in [('direct',p),('inverse',f.invperm(p))]:
     assert f.invperm(f.invperm(pp))==pp;unique.setdefault(pp,[]).append([kind,width,start,direction]);counts[kind]+=1
 return unique,dict(raw_route_descriptions=sum(counts.values()),by_geometry=dict(counts),complete_independent_coordinate_route_checks=refchecks,both_inverse_directions_checked=True,finite_blank_orbits_asserted=True)
def score(C,known,routes,vs,budget,keep=False):
 positions=sorted(known);expected=[int.from_bytes(requirements(known,v),'big') for v in vs];lo,hi=f.match_constants(len(positions));best=-1;hits=[];plain=set();models=0
 for number,p in enumerate(routes):
  if number%128==0:budget.check()
  packed=int.from_bytes(bytes(ord(C[p[i]]) for i in positions),'big')
  for j,e in enumerate(expected):
   matches=f.fast_matches(packed,e,lo,hi);models+=1;best=max(best,matches)
   if matches==len(positions):
    P=decode(C,p,vs[j]);assert all(P[i]==v for i,v in known.items());assert encode(P,p,vs[j])==C;plain.add(P);hits.append(dict(route_sha256=hashlib.sha256(p).hexdigest(),variant=vs[j]['label'],plaintext=P))
 return dict(complete=True,operator_evaluations=models,max_crib_matches=best,distinct_full_plaintexts=len(plain),exact_model_hits=len(hits),hits=hits if keep else None)
def overlap(routes):
 path=ROOT/'results/ROUTE-001.json.gz';old=json.loads(gzip.decompress(path.read_bytes()));previous={bytes(r['permutation']) for r in old['route_catalogue']};common=len(set(routes)&previous)
 return dict(prior_receipt='results/ROUTE-001.json.gz',prior_receipt_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),prior_route_count=len(previous),exact_route_intersection=common,conservative_old_fixed_arithmetic_subset=common*18,pure_route_family_already_count_excluded=True,repeated_for_shared_null_calibration_not_new_negative=True,other_prior_families='K3/clock384 and occupied-cell route/key families reviewed as additional scope; full worldwide operator census not claimed.')
def run(output):
 start=c.utc();budget=c.Budget(600);routes,checks=compile_routes(budget);vs=variants();prior=overlap(routes);rng=random.Random(49000);data=json.loads((ROOT/'data/k4.json').read_text());known={x['start']-1+j:p for x in data['cribs'] for j,p in enumerate(x['plaintext'])};P=[rng.choice(c.ALPHABETS['AZ']) for _ in range(97)]
 for i,v in known.items():P[i]=v
 P=''.join(P);plants=0
 for kind in KINDS:
  for width in range(1,98):
   p=route(width,37*width%97,kind)
   for pp in (p,f.invperm(p)):
    assert pp in routes
    for v in vs:
     cipher=encode(P,pp,v);assert decode(cipher,pp,v)==P;packed=int.from_bytes(bytes(ord(cipher[pp[i]]) for i in sorted(known)),'big');want=int.from_bytes(requirements(known,v),'big');assert f.packed_matches(packed,want,24)==24;plants+=1
 checks.update(all_width_inverse_arithmetic_plants=plants,all_starts_covered_by_bijection_controls=True)
 # Six actual whole-selector positive controls, no K4 use before completion.
 fullplants=[]
 for j,(kind,direction) in enumerate((k,d) for k in KINDS for d in range(2)):
  p=route(17,71,kind);p=f.invperm(p) if direction else p;v=vs[j];cipher=encode(P,p,v);res=score(cipher,known,routes,vs,budget);assert res['exact_model_hits']>=1;fullplants.append(dict(kind=kind,inverse=bool(direction),planted_full_plaintext_present=any(decode(cipher,pp,vv)==P for pp in (p,) for vv in (v,)),selector_hits=res['exact_model_hits']))
 catalog=[dict(permutation=list(p),aliases=aliases) for p,aliases in sorted(routes.items())];raw=json.dumps(catalog,separators=(',',':')).encode();catalogpath=ROOT/'results/ENE-ROUTE-049-CATALOGUE.json.gz'
 if catalogpath.exists():assert gzip.decompress(catalogpath.read_bytes())==raw
 else:catalogpath.write_bytes(gzip.compress(raw,mtime=0))
 actual=score(data['ciphertext'],known,routes,vs,budget,True);nulls=[];free=[i for i in range(97) if i not in known];rng=random.Random(49001)
 for j in range(31):
  chars=[data['ciphertext'][i] for i in free];rng.shuffle(chars);C=list(data['ciphertext'])
  for i,v in zip(free,chars):C[i]=v
  nulls.append(dict(index=j,**score(''.join(C),known,routes,vs,budget)))
 out=dict(id='ENE-ROUTE-049',started_at_utc=start,finished_at_utc=c.utc(),complete=True,controls=checks,full_selector_plants=fullplants,unique_routes=len(routes),arithmetic_variants=len(vs),catalogue_uncompressed_sha256=hashlib.sha256(raw).hexdigest(),prior_overlap=prior,actual=actual,nulls=nulls,null_seed=49001,literal_angle_degrees=math.degrees(math.atan(.5)),digital_angle_degrees=22.5,free_key_family_tested=False,worldwide_novelty_claimed=False,pushed=False,source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['research/ENE-ROUTE-049-SPEC.md','experiments/ene_route_049.py','experiments/finite_hand_operators.py','data/k4.json']});Path(output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(id=out['id'],raw_routes=checks['raw_route_descriptions'],unique_routes=len(routes),operators=actual['operator_evaluations'],max_crib=actual['max_crib_matches'],hits=actual['exact_model_hits'],null_maxima=[x['max_crib_matches'] for x in nulls],controls=checks)))
if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();run(args.output)
