import filecmp,itertools,sys,tempfile,unittest
from unittest.mock import patch
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import sigaba_joint_toy as t
import sigaba_joint_toy_oracle as o
import sigaba_compressed_ownership as native
from sigaba_compact_domain import Domain,legacy
import types
def solve_legacy(*args,**kwargs):return legacy(native.solve(*args,**kwargs))
a=types.SimpleNamespace(solve=solve_legacy,prefix_delta=native.prefix_delta,ReservedPredicates=native.ReservedPredicates)

def correlated(result):
 out={}
 for row in result['relations']:
  for rel in row['relations']:
   for h in t.bits(int(rel['index_classes'],16)):
    key=tuple(row['control']),h
    if key in out:raise AssertionError('duplicate class')
    out[key]=(int(rel['cipher_starts'],16),tuple(rel['final_offsets']))
 return out
class CompressedOwnershipTests(unittest.TestCase):
 def test_complete_original_sets_and_offsets_with_prefix_and_gap(self):
  for q in (2,3):
   for mask in ('empty','short','long'):
    f=t.fixture(q,3,mask=mask);p=f['plant'];cipher=o.simulate(f,f['plaintext'],p['control'],p['index'],p['cipher']);obs=[(i,f['plaintext'][i],cipher[i]) for i in f['observed_positions']];old=t.solve(f,obs)
    for cap in (0,1024,64<<20):
     r=a.solve(t.Model(f),obs,t.Budget(15),cache_cap=cap);self.assertTrue(r['completed']);self.assertEqual(r['exact_raw_key_count'],old['exact_raw_key_count']);self.assertEqual(correlated(r),correlated(old));self.assertEqual(r['first_observed_time'],min(f['observed_positions'],default=0))
    with tempfile.TemporaryDirectory() as td:
     x=Path(td)/'anchored';y=Path(td)/'physical';b=t.Budget(15);t.write_keys(r,f,x,b);o.truth(f,obs,y,b.check,t.Limit);self.assertTrue(filecmp.cmp(x,y,shallow=False))
 def test_all_small_subset_preimages_and_distinct_map_prefixes(self):
  f=t.fixture(2,3);m=t.Model(f);b=t.Budget(15);pred=a.ReservedPredicates(m,b,0)
  for subset in range(256):
   for delta in itertools.product(range(2),repeat=3):
    expected=0
    for i,seed in enumerate(itertools.product(range(2),repeat=3)):
     shifted=tuple((x+d)%2 for x,d in zip(seed,delta));j=0
     for x in shifted:j=j*2+x
     if subset>>j&1:expected|=1<<i
    self.assertEqual(pred.translate(subset,delta),expected)
  # Independently compare every map's accumulated prefix against physical schedules.
  offsets=set()
  for control in itertools.product(range(2),repeat=3):
   digits=m.digits(control,10)
   for h,aliases in enumerate(m.aliases):
    got=a.prefix_delta(m,digits,h,7,b);physical=o.schedule(f,control,aliases[0],8)[7];self.assertEqual(got,physical);offsets.add(got)
  self.assertGreater(len(offsets),1)
 def test_shared_wrong_prefix_and_skipped_gap_are_detected(self):
  f=t.fixture(3,3,mask='short');p=f['plant'];c=o.simulate(f,f['plaintext'],p['control'],p['index'],p['cipher']);obs=[(i,f['plaintext'][i],c[i]) for i in f['observed_positions']];r=a.solve(t.Model(f),obs,t.Budget(15));expected=correlated(t.solve(f,obs));self.assertEqual(correlated(r),expected)
  mutated={k:(v[0],tuple((x+1)%3 for x in v[1])) for k,v in correlated(r).items()};self.assertNotEqual(mutated,expected)
  original=a.prefix_delta
  with patch('sigaba_compressed_ownership.prefix_delta',side_effect=lambda m,d,h,x,b:original(m,d,0,x,b)):
   wrong=a.solve(t.Model(f),obs,t.Budget(15))
  self.assertNotEqual(correlated(wrong),expected)
  broken=t.Model(f);digits=broken.digits
  def skipped(control,length):
   values=digits(control,length)
   if length>5:values[5]=()
   return values
  broken.digits=skipped
  self.assertNotEqual(correlated(a.solve(broken,obs,t.Budget(15))),expected)
  # A real removed unknown step changes at least one physical cumulative offset.
  m=t.Model(f);digits=m.digits([0]*3,10);self.assertTrue(any(a.prefix_delta(m,digits,h,6,t.Budget(10))!=a.prefix_delta(m,digits,h,7,t.Budget(10)) for h in range(len(m.maps))))
 def test_restricted_start_requests_are_not_silently_relaxed(self):
  f=t.fixture(2,3)
  with self.assertRaises(ValueError):a.solve(t.Model(f),[(3,0,0)],t.Budget(10),full_initial_domain=False)
  r=a.solve(t.Model(f),[(3,0,0),(3,0,1)],t.Budget(10));self.assertTrue(r['completed']);self.assertEqual(r['exact_raw_key_count'],'0')

 def test_delayed_single_observation_complete_truth_and_aliases(self):
  has_alias=False
  for q in (2,3):
   f=t.fixture(q,3);p=f['plant'];cipher=o.simulate(f,f['plaintext'],p['control'],p['index'],p['cipher']);at=7 if q==2 else 10;obs=[(at,f['plaintext'][at],cipher[at])];model=t.Model(f);has_alias|=any(len(rows)>1 for rows in model.aliases);old=t.solve(f,obs)
   for cap in (0,1024,64<<20):
    r=a.solve(model,obs,t.Budget(15),cache_cap=cap);self.assertTrue(r['completed']);self.assertEqual(correlated(r),correlated(old))
   with tempfile.TemporaryDirectory() as td:
    x=Path(td)/'anchored';y=Path(td)/'physical';budget=t.Budget(15);t.write_keys(r,f,x,budget);o.truth(f,obs,y,budget.check,t.Limit);self.assertTrue(filecmp.cmp(x,y,shallow=False))
  self.assertTrue(has_alias)

 def test_nonfull_contact_absolute_time_and_gap_trace(self):
  f=t.fixture(5,3);m=t.Model(f);control=f['plant']['control'];seed=tuple(f['plant']['cipher']);digits=m.digits(control,74);anchor=21;chosen=None
  for h,aliases in enumerate(m.aliases):
   def mask_at(time):return {m.maps[h][d] for d in digits[time]}
   if any(mask_at(time)!=mask_at(time-anchor) for time in range(anchor,73)):
    chosen=h;break
  self.assertIsNotNone(chosen);h=chosen;index=m.aliases[h][0];cipher=o.simulate(f,f['plaintext'],control,index,seed);physical=o.schedule(f,control,index,74);prefix=a.prefix_delta(m,digits,h,anchor,t.Budget(10));self.assertEqual(prefix,physical[anchor]);state=tuple((seed[j]+prefix[j])%5 for j in range(3));self.assertEqual(tuple((state[j]-prefix[j])%5 for j in range(3)),seed);wrong=state;timing_mutation_detected=False
  for time in range(anchor,74):
   self.assertEqual(state,tuple((seed[j]+physical[time][j])%5 for j in range(3)))
   x=f['plaintext'][time]
   for j in range(3):x=m.cf[j][state[j]][x]
   self.assertEqual(x,cipher[time])
   actual={m.maps[h][d] for d in digits[time]};shifted={m.maps[h][d] for d in digits[time-anchor]}
   state=tuple((v-(j in actual))%5 for j,v in enumerate(state));wrong=tuple((v-(j in shifted))%5 for j,v in enumerate(wrong));timing_mutation_detected|=wrong!=state
  self.assertTrue(timing_mutation_detected)

 def test_forced_representations_preserve_all_tiny_sets_and_cache_policies(self):
  for q in (2,3):
   for mask in ('empty','short','long','one'):
    f=t.fixture(q,3,mask='long' if mask=='one' else mask);p=f['plant'];cipher=o.simulate(f,f['plaintext'],p['control'],p['index'],p['cipher']);positions=[7 if q==2 else 10] if mask=='one' else f['observed_positions'];obs=[(i,f['plaintext'][i],cipher[i]) for i in positions];expected=correlated(t.solve(f,obs))
    for policy in ('bitmap','packed'):
     for cap in (0,1024,64<<20):
      r=legacy(native.solve(t.Model(f),obs,t.Budget(20),cache_cap=cap,storage_policy=policy));self.assertTrue(r['completed']);self.assertEqual(correlated(r),expected)
     with tempfile.TemporaryDirectory() as td:
      x=Path(td)/'compact';y=Path(td)/'physical';b=t.Budget(20);t.write_keys(r,f,x,b);o.truth(f,obs,y,b.check,t.Limit);self.assertTrue(filecmp.cmp(x,y,shallow=False))
 def test_exhaustive_exact_set_encoding_intersection_hash_and_inverse(self):
  m=t.Model(t.fixture(2,3));pred=a.ReservedPredicates(m,t.Budget(20),0)
  for policy in ('auto','bitmap','packed'):
   for subset in range(256):
    d=Domain(subset,policy);self.assertEqual(d.to_bits(),subset);self.assertEqual(hash(d),hash(subset));self.assertEqual(d,Domain.from_ids([i for i in range(8) if subset>>i&1],policy));self.assertEqual(Domain.decode(d.encode()),d)
    for other in range(256):self.assertEqual(d.meet_bitmap(other).to_bits(),subset&other)
    for delta in itertools.product(range(2),repeat=3):self.assertEqual(d.preimage(delta,m,pred,t.Budget(20)).to_bits(),pred.translate(subset,delta))
  empty=Domain(0,'packed');collision=Domain(sys.hash_info.modulus,'packed');self.assertEqual(hash(empty),hash(collision));self.assertNotEqual(empty,collision);self.assertEqual(len({empty,collision}),2)
  with self.assertRaises(AttributeError):collision.payload=b''
  for ids in ([1,1],[2,1],[-1],[2**32]):
   with self.assertRaises(ValueError):Domain.from_ids(ids)
  with self.assertRaises(ValueError):Domain.decode({'encoding':'u32lehex','data':'00','cardinality':1})

 def test_real_packed_filter_matches_physical_contacts_on_pinned_layouts(self):
  import sigaba_csp889 as sig
  import sigaba_real_adapter as real
  d=sig.data()
  for number,key in enumerate(d['vectors']):
   model=real.RealModel(key,quotient=False);seed=0
   for ch in key['cipherposition']:seed=seed*26+sig.AZ.index(ch)
   ids=sorted({(seed+137*i)%(26**5) for i in range(6)});delta=tuple((number+3*j)%26 for j in range(5));p=sig.AZ.index(key['input'][0]);outs={}
   for index in ids:
    state=t.unpack(index,26,5);x=p
    for j,wheel in enumerate(model.orders[0]):
     wire=[sig.AZ.index(ch) for ch in d['large'][wheel-1]];x=sig.contact_oracle(wire,(state[j]+delta[j])%26,model.rev[0][j])[x]
    outs[index]=x
   target=outs[ids[0]];expected=[i for i in ids if outs[i]==target]
   for policy in ('auto','packed'):
    domain=Domain.from_ids(ids,policy);self.assertEqual(domain.kind,'u32le');actual,checks=domain.intersect(delta,p,target,model,a.ReservedPredicates(model,t.Budget(10),0),t.Budget(10));self.assertEqual(list(actual.ids()),expected);self.assertEqual(checks,len(ids))
