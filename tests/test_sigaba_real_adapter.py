import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import sigaba_csp889 as sig
import sigaba_real_adapter as real
import sigaba_joint_toy as toy
class RealAdapterTests(unittest.TestCase):
 def test_all_twelve_external_vectors_adapter_and_physical(self):
  for v in sig.data()['vectors']:
   m=real.RealModel(v,quotient=False)
   for back in (False,True):
    p,c=(v['output'],v['input']) if back else (v['input'],v['output'])
    self.assertEqual(m.stream(p,decrypt=back),c)
    self.assertEqual(real.physical(p,v,back),c)
    self.assertEqual(sig.Machine(v).crypt(p,back),c)
 def test_complete_coupled_kernel_matches_all_tiny_relations(self):
  for q in (2,3):
   for mask in ('empty','short','long'):
    f=toy.fixture(q,3,mask=mask);m=toy.Model(f)
    # The old independent oracle supplies ciphertext; kernel observes no plant fields.
    import sigaba_joint_toy_oracle as oracle
    c=oracle.simulate(f,f['plaintext'],f['plant']['control'],f['plant']['index'],f['plant']['cipher'])
    observations=[(i,f['plaintext'][i],c[i]) for i in f['observed_positions']]
    old=toy.solve(f,observations);new=real.guarded_solve(m,observations,toy.Budget(10),cache_cap=0)
    self.assertTrue(new['completed']);self.assertEqual(new['exact_raw_key_count'],old['exact_raw_key_count']);self.assertEqual(toy.relation_masks(new),toy.relation_masks(old))
 def test_declared_fixtures_and_resource_failure_are_not_false_negatives(self):
  for i in (0,1):
   f=real.fixture(i);m=real.RealModel(f['key'],quotient=False)
   self.assertEqual(m.stream(f['plaintext']),f['ciphertext']);self.assertEqual(real.physical(f['plaintext'],f['key']),f['ciphertext'])
  f=toy.fixture(3,3);r=real.guarded_solve(toy.Model(f),[(0,1,1)],toy.Budget(10),domain_cap=1)
  self.assertFalse(r['completed']);self.assertIsNone(r['exact_raw_key_count']);self.assertEqual(r['control_starts_completed'],0)
