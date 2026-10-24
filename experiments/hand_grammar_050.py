"""Complete fixed-key depth0..3 hand-operation grammar, not every hand cipher."""
import collections,gzip,hashlib,itertools,json,random
from pathlib import Path
import finite_hand_operators as f
import candidate_first_048 as c
ROOT=Path(__file__).resolve().parents[1]
def reference(values,d):
 v=list(values);n=len(v);kind=d['kind']
 if kind=='reversal':return bytes(v[::-1])
 if kind=='skip':
  step=d['step'] if d['direction']=='direct' else pow(d['step'],-1,n);pos=0;out=[]
  for _ in v:out.append(v[pos]);pos=(pos+step)%n
  return bytes(out)
 if kind=='columnar':
  w=len(d['key']);rows=[v[i:i+w] for i in range(0,n,w)];columns=sorted(range(w),key=lambda i:(d['key'][i],i))
  if d['direction']=='direct':return bytes(row[j] for j in columns for row in rows if j<len(row))
  matrix=[[None]*len(row) for row in rows];it=iter(v)
  for j in columns:
   for row in matrix:
    if j<len(row):row[j]=next(it)
  return bytes(x for row in matrix for x in row)
 k=[f.A.index(d['key'][i%len(d['key'])]) for i in range(n)]
 if d['equation']=='plus':return bytes((a+b)%26 for a,b in zip(v,k))
 if d['equation']=='minus':return bytes((a-b)%26 for a,b in zip(v,k))
 return bytes((b-a)%26 for a,b in zip(v,k))
def compile_grammar(budget):
 raw=f.primitives();unique_primitives={}
 for d,op in raw:unique_primitives.setdefault(f.signature(op),dict(op=op,aliases=[]))['aliases'].append(d)
 prim=list(unique_primitives.values());count=len(prim);operators={};levels=[];prefix={():f.identity()};rng=random.Random(50000);sample=bytes(rng.randrange(26) for _ in range(97));comparisons=0
 for depth in range(4):
  signatures=set();total=0
  for word in itertools.product(range(count),repeat=depth):
   if total%128==0:budget.check()
   op=f.identity() if not word else f.compose(prefix[word[:-1]],prim[word[-1]]['op']);prefix[word]=op;sig=f.signature(op);signatures.add(sig);total+=1
   ref=sample
   for index in word:ref=reference(ref,prim[index]['aliases'][0])
   assert f.apply(sample,op)==ref;assert f.apply(f.apply(sample,op),f.invert(op))==sample;comparisons+=1
   if sig not in operators:operators[sig]=dict(op=op,aliases=[])
   operators[sig]['aliases'].append(list(word))
  levels.append(dict(depth=depth,raw_descriptions=total,distinct_operators_at_depth=len(signatures)))
 return prim,operators,dict(raw_primitive_descriptions=len(raw),unique_primitives=count,levels=levels,all_description_independent_reference_comparisons=comparisons,all_description_inverse_roundtrips=comparisons)
def score(C,known,operators,budget,keep=False):
 positions=sorted(known);input_values=bytes(f.A.index(x) for x in C);targets=[f.A.index(known[i]) for i in positions];lo,hi=f.match_constants(len(positions));best=-1;hits=[];distinct=set()
 for num,(sig,record) in enumerate(operators.items()):
  if num%128==0:budget.check()
  p,s,b=record['op'];obs=int.from_bytes(bytes(input_values[p[i]] for i in positions),'big');expect=int.from_bytes(bytes(s*(v-b[i])%26 for i,v in zip(positions,targets)),'big');count=f.fast_matches(obs,expect,lo,hi);best=max(best,count)
  if count==len(positions):
   P=f.apply(input_values,record['op']);assert all(f.A[P[i]]==v for i,v in known.items());assert f.apply(P,f.invert(record['op']))==input_values;text=''.join(f.A[x] for x in P);distinct.add(text);hits.append(dict(operator_sha256=hashlib.sha256(sig).hexdigest(),plaintext=text,representative=record['aliases'][0],descriptor_aliases=len(record['aliases'])))
 return dict(complete=True,operators_evaluated=len(operators),max_crib_matches=best,exact_operator_hits=len(hits),distinct_compatible_plaintexts=len(distinct),hits=hits if keep else None)
def controls(prim):
 # Exhaustive small-alphabet composition action, including noncommuting permutation/offset.
 count=0
 for q in (3,5):
  atoms=[(bytes([0,1,2]),1,bytes([1,2,0])),(bytes([2,0,1]),1,bytes(3)),(bytes([0,1,2]),-1,bytes([2,1,0]))]
  for depth in range(4):
   for word in itertools.product(range(len(atoms)),repeat=depth):
    op=f.identity(3)
    for j in word:op=f.compose(op,atoms[j],q)
    for vector in itertools.product(range(q),repeat=3):
     expected=list(vector)
     for j in word:
      p,s,b=atoms[j];expected=[(s*expected[p[i]]+b[i])%q for i in range(3)]
     assert f.apply(vector,op,q)==bytes(expected);assert f.apply(f.apply(vector,op,q),f.invert(op,q),q)==bytes(vector);count+=1
 known=json.loads((ROOT/'data/controls.json').read_text());kat=[]
 for name in ('k1','k2_as_inscribed','k2_restored_s'):
  row=known[name];key=row['key'];result=[];position=0
  # Historical literal? passes through without advancing key; K4 itself is97A-Z.
  for x in row['plaintext']:
   if x=='?':result.append('?')
   else:result.append(f.A[(f.A.index(x)+f.A.index(key[position%len(key)]))%26]);position+=1
  assert ''.join(result)==row['ciphertext'];kat.append(dict(name=name,symbols=len(result),letters=position,question_marks=len(result)-position,forward_exact=True))
 for record in prim:
  d=record['aliases'][0];op=record['op']
  for constant in range(26):
   vector=bytes([constant]*97);assert f.apply(vector,op)==reference(vector,d)
 return dict(complete_small_alphabet_input_composition_checks=count,historical_known_answers=kat,all_primitive_input_symbol_checks=len(prim)*26)
def prior_overlap(operators):
 oldpath=ROOT/'results/ROUTE-001.json.gz';old=json.loads(gzip.decompress(oldpath.read_bytes()));oldp={bytes(r['permutation']) for r in old['route_catalogue']};newpath=ROOT/'results/ENE-ROUTE-049-CATALOGUE.json.gz';newp={bytes(r['permutation']) for r in json.loads(gzip.decompress(newpath.read_bytes()))};arith={(s,b) for d,(p,s,b) in f.primitives() if d['kind']=='arithmetic'}|{(1,bytes(97))};oldcovered=0;recent=0
 for record in operators.values():
  p,s,b=record['op']
  if p in oldp and any(all(b[i]==b[i%L] for i in range(97)) for L in range(1,97 if p==bytes(range(97)) else 17)):oldcovered+=1
  if p in newp and (s,b) in arith:recent+=1
 return dict(previous_route_family_exact_operator_subset=oldcovered,previous_route_receipt_sha256=hashlib.sha256(oldpath.read_bytes()).hexdigest(),recent049_fixed_operator_intersection=recent,recent049_catalogue_sha256=hashlib.sha256(newpath.read_bytes()).hexdigest(),overlap_not_counted_as_independent_negative=True,foreign_depth_three_audit='Author reports substitution/columnar/substitution domains and gaps; no unverified proof/numerical total inherited, no worldwide novelty claim.')
def run(output):
 start=c.utc();compile_budget=c.Budget(180);prim,operators,checks=compile_grammar(compile_budget);checks.update(controls(prim));compile_budget.check();overlap=prior_overlap(operators);data=json.loads((ROOT/'data/k4.json').read_text());known={r['start']-1+i:v for r in data['cribs'] for i,v in enumerate(r['plaintext'])};rng=random.Random(50002);P=[rng.choice(f.A) for _ in range(97)]
 for i,v in known.items():P[i]=v
 P=''.join(P);v=bytes(f.A.index(x) for x in P);budget=c.Budget(600);plant_words=[[]]+[[i] for i in range(len(prim))]+[[0,1],[3,17],[4,25,37],[36,9,2]];plants=[]
 for word in plant_words:
  op=f.identity()
  for j in word:op=f.compose(op,prim[j]['op'])
  assert f.signature(op) in operators;cipher=''.join(f.A[x] for x in f.apply(v,f.invert(op)));res=score(cipher,known,operators,budget,True);assert any(h['plaintext']==P for h in res['hits']);plants.append(dict(word=word,full_selector_true_plaintext_recovered=True,exact_operator_hits=res['exact_operator_hits'],distinct_plaintexts=res['distinct_compatible_plaintexts']))
 catalog=[dict(signature_hex=sig.hex(),aliases=record['aliases']) for sig,record in sorted(operators.items())];raw=json.dumps(catalog,separators=(',',':')).encode();path=ROOT/'results/HAND-GRAMMAR-050-CATALOGUE.json.gz'
 if path.exists():assert gzip.decompress(path.read_bytes())==raw
 else:path.write_bytes(gzip.compress(raw,mtime=0))
 actual=score(data['ciphertext'],known,operators,budget,True);nulls=[];free=[i for i in range(97) if i not in known];rng=random.Random(50001)
 for j in range(31):
  chars=[data['ciphertext'][i] for i in free];rng.shuffle(chars);C=list(data['ciphertext'])
  for i,x in zip(free,chars):C[i]=x
  nulls.append(dict(index=j,**score(''.join(C),known,operators,budget)))
 out=dict(id='FIXED-KEY-HAND-GRAMMAR-050',started_at_utc=start,finished_at_utc=c.utc(),complete=True,controls=checks,primitive_inventory=[p['aliases'] for p in prim],unique_operators=len(operators),catalogue_uncompressed_sha256=hashlib.sha256(raw).hexdigest(),prior_overlap=overlap,full_selector_plants=plants,actual=actual,nulls=nulls,null_seed=50001,columnar_widths=[7,10,8],literal_keys=list(f.KEYS),unrestricted_keys_tested=False,other_hand_ciphers_excluded=False,pushed=False,source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['research/HAND-GRAMMAR-050-SPEC.md','experiments/hand_grammar_050.py','experiments/finite_hand_operators.py','data/k4.json']});Path(output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(id=out['id'],primitives=len(prim),descriptions=sum(x['raw_descriptions'] for x in checks['levels']),unique_operators=len(operators),actual_max=actual['max_crib_matches'],actual_hits=actual['exact_operator_hits'],null_maxima=[x['max_crib_matches'] for x in nulls],full_selector_plants=len(plants))))
if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();run(args.output)
