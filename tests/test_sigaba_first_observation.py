import filecmp,itertools,sys,tempfile,unittest
from unittest.mock import patch
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import sigaba_joint_toy as t
import sigaba_joint_toy_oracle as o
import sigaba_first_observation as a

def correlated(result):
 out={}
 for row in result['relations']:
  for rel in row['relations']:
   for h in t.bits(int(rel['index_classes'],16)):
    key=tuple(row['control']),h
    if key in out:raise AssertionError('duplicate class')
    out[key]=(int(rel['cipher_starts'],16),tuple(rel['final_offsets']))
 return out
class FirstObservationTests(unittest.TestCase):
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
  with patch('sigaba_first_observation.prefix_delta',side_effect=lambda m,d,h,x,b:original(m,d,0,x,b)):
   wrong=a.solve(t.Model(f),obs,t.Budget(15))
  self.assertNotEqual(correlated(wrong),expected)
  broken=t.Model(f);digits=broken.digits
  def skipped(control,length):
   values=digits(control,length)
   if length>5:values[5]=values[0]
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
