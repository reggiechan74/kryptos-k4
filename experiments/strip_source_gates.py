"""Item7 conditional cyclic-strip proof; not an admitted historical key table."""
from collections import defaultdict
import itertools,json,random,time
from pathlib import Path
from conditional_face_lamp import WINDOWS,literal_plant
ROOT=Path(__file__).resolve().parents[1];AZ='ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def validate_strips(strips,alphabet=AZ):
 if not strips or len(set(alphabet))!=len(alphabet):raise ValueError('nonempty strips and unique alphabet required')
 for i,w in enumerate(strips):
  if len(w)!=len(alphabet) or set(w)!=set(alphabet):raise ValueError('strip %d is not a permutation; no silent repair'%i)
 return True


def crypt(text,strips,origin,rows,decrypt=False,alphabet=AZ):
 validate_strips(strips,alphabet);width=len(strips);out=[]
 if any(c not in alphabet for c in text):raise ValueError('literal alphabet framing required')
 for i,c in enumerate(text):
  block,slot=divmod(i-origin,width);w=strips[slot];d=rows[block]%len(alphabet)
  out.append(w[(w.index(c)+(-d if decrypt else d))%len(w)])
 return ''.join(out)


def observations(cipher,windows=WINDOWS[:1]):
 return [dict(position=s+j+1,plaintext=p,ciphertext=cipher[s+j],fixed=p==cipher[s+j]) for s,word in windows for j,p in enumerate(word)]


def classify(obs,width,origin,allow_zero=True):
 if type(width) is not int or width<1 or not 0<=origin<width:raise ValueError('invalid block frame')
 if not allow_zero:
  fixed=next((o for o in obs if o['fixed']),None)
  return dict(necessary_condition_pass=fixed is None,witness=[] if fixed is None else [fixed])
 groups=defaultdict(list)
 for row in obs:groups[(row['position']-1-origin)//width].append(row)
 for block,rows in sorted(groups.items()):
  fixed=[r for r in rows if r['fixed']];changed=[r for r in rows if not r['fixed']]
  if fixed and changed:return dict(necessary_condition_pass=False,block=block,witness=[fixed[0],changed[0]])
 return dict(necessary_condition_pass=True,witness=[],not_a_complete_key_fit=True)


def reference_pass(obs,width,origin):
 # Explicit interval membership instead of quotient/remainder grouping.
 positions=[r['position']-1 for r in obs]
 if not positions:return True
 start=origin
 while start>min(positions):start-=width
 while start+width<=max(positions):
  group=[r['fixed'] for r in obs if start<=r['position']-1<start+width]
  if group and any(group) and not all(group):return False
  start+=width
 group=[r['fixed'] for r in obs if start<=r['position']-1<start+width]
 return not (group and any(group) and not all(group))


def controls():
 start=time.monotonic();permutations=0;symbol_checks=0
 for q in range(2,7):
  alphabet=AZ[:q]
  for xs in itertools.permutations(alphabet):
   w=''.join(xs);permutations+=1
   for d in range(q):
    rows={0:d};got=crypt(alphabet,[w]*q,0,rows,alphabet=alphabet)
    # Independent letter-to-letter matrix for a whole circular row.
    table=dict(zip(w,w[d:]+w[:d]));assert got==''.join(table[p] for p in alphabet)
    assert crypt(got,[w]*q,0,rows,True,alphabet)==alphabet
    assert sum(p==c for p,c in zip(alphabet,got))==(q if d==0 else 0);symbol_checks+=q
 rng=random.Random(270024);plants=[];plain=literal_plant();partition_checks=0
 for width in (2,3,5,25,30,30):
  for case in range(4):
   origin=(case*(width-1))//3;strips=[]
   for _ in range(width):
    xs=list(AZ);rng.shuffle(xs);strips.append(''.join(xs))
   blocks=range((0-origin)//width,(96-origin)//width+1)
   rows={b:(1 if case==0 else 0 if case==1 else 13*(b%2) if case==2 else (b+case)%26) for b in blocks}
   cipher=crypt(plain,strips,origin,rows);assert crypt(cipher,strips,origin,rows,True)==plain
   out=[]
   for b in blocks:
    mapping=[dict(zip(w,w[rows[b]:]+w[:rows[b]])) for w in strips]
    for i in range(max(0,origin+b*width),min(97,origin+(b+1)*width)):out.append(mapping[i-origin-b*width][plain[i]])
   assert ''.join(out)==cipher
   obs=observations(cipher,WINDOWS);assert classify(obs,width,origin)['necessary_condition_pass'];assert reference_pass(obs,width,origin)
   plants.append(dict(width=width,origin=origin,case=case,full_roundtrip=True,independent_matrix_equal=True,necessary_condition_pass=True,zero_rows=sum(d==0 for d in rows.values())))
   for w in range(1,31):
    for phase in range(w):
     assert classify(obs,w,phase)['necessary_condition_pass']==reference_pass(obs,w,phase);partition_checks+=1
 for bad in ('A'*26,AZ[:-1],AZ[:-1]+'A'):
  try:validate_strips([bad])
  except ValueError:pass
  else:raise AssertionError('invalid strip accepted')
 assert time.monotonic()-start<60
 return dict(status='passed',synthetic_not_historical=True,toy_permutations=permutations,toy_symbol_checks=symbol_checks,literal_plants=plants,complete_partition_comparisons=partition_checks,invalid_tables_rejected=3,elapsed_seconds=time.monotonic()-start)


def actual():
 cipher=json.loads((ROOT/'data/k4.json').read_text())['ciphertext'];obs=observations(cipher);rows=[]
 for width in range(1,31):
  for origin in range(width):rows.append(dict(width=width,origin_zero_based=origin,**classify(obs,width,origin)))
 triple=[o for o in obs if 32<=o['position']<=34];assert [r['fixed'] for r in triple]==[False,True,False]
 assert sum(r['necessary_condition_pass'] for r in rows)==1
 return dict(kind='conditional_cyclic_strip_invariant_not_historical_inventory_search',scope='Permutation strip at every column, one common row offset per fixed-width block; direct aligned English. Table/order can be arbitrary.',first_crib_observations=obs,non_plaintext_row=classify(obs,1,0,False),zero_row_relaxation=rows,raw_width_origin_descriptions=len(rows),rejected=464,necessary_only_unrejected=[r for r in rows if r['necessary_condition_pass']],all_width_at_least_two_witness=triple,infinite_width_argument='A block containing the middle of changed/fixed/changed contains a neighbor whenever width>=2; its common row would need both zero and nonzero displacement.',prior_overlap='Width25 origin0 and fixed-point theorem are reused from NONROTOR-STRUCTURAL-004; new audit removes registration restriction. No novelty or independent-key count.',historical_M138A_admission='Pending source review; theorem is conditional on the authentic row procedure.',actual_key_enumerations=0,berlin_evaluated=False,puzzle_solved=False)
