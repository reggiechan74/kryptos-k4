import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import sigaba_support_signature_041 as n
import check_sigaba_support_signature_041 as check
class SupportSignature041Tests(unittest.TestCase):
 def test_complete_independent_physical_sets_and_cache_caps(self):
  r=check.run();self.assertTrue(r['complete']);self.assertEqual(r['complete_independent_root_graphs'],70);self.assertEqual(r['complete_raw_truth_streams'],12);self.assertEqual(r['complete_cap_invariance_cases'],36);self.assertEqual(r['varying_input_supplement'],dict(independent_controller_graphs=124,full_raw_truth_streams=12,varying_fixtures=4));self.assertGreater(r['root_cache_hits'],0)
 def test_signature_retains_partition_masks_observations_and_model(self):
  class Model:
   def mask_groups(self,B):return [(1,1)] if B==(9,) else [(1,1),(2,1)]
  m=Model();c=n.SupportCache();b=n.toy.Budget(1);obs=[(i,0,0) for i in range(3)]
  f=lambda digits:c.signature(m,obs,digits,b)[0]
  self.assertEqual(f([(1,),(1,)]),f([(2,),(2,)]));self.assertNotEqual(f([(1,),(1,)]),f([(1,),(2,)]));self.assertNotEqual(f([(1,),(1,)]),f([(9,),(9,)]))
  with self.assertRaises(ValueError):c.signature(Model(),obs,[(1,),(1,)],b)
 def test_unfinished_calculation_is_not_cached(self):
  m=n.toy.Model(n.toy.fixture(2,3));b=n.toy.Budget(-1);cache=n.SupportCache();pred=n.ReservedPredicates(m,b,0)
  with self.assertRaises(n.toy.Limit):cache.evaluate(m,[(2,0,0)],m.digits((0,0,0),3),b,pred)
  self.assertEqual(cache.bytes,0);self.assertFalse(cache.cache)
