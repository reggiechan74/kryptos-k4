import filecmp,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import sigaba_joint_toy as t
import sigaba_joint_toy_oracle as o
import sigaba_domain_identity as s
class DomainIdentityTests(unittest.TestCase):
 def test_complete_relations_and_raw_truth_under_cache_policies(self):
  for q in (2,3):
   for mask in ('empty','short','long'):
    f=t.fixture(q,3,mask=mask);p=f['plant'];c=o.simulate(f,f['plaintext'],p['control'],p['index'],p['cipher']);obs=[(i,f['plaintext'][i],c[i]) for i in f['observed_positions']];old=t.solve(f,obs)
    for cache in (0,1024,64<<20):
     result=s.solve(t.Model(f),obs,t.Budget(10),cache_cap=cache);self.assertTrue(result['completed']);self.assertEqual(t.relation_masks(old),t.relation_masks(result));self.assertEqual(result['exact_raw_key_count'],old['exact_raw_key_count']);self.assertLessEqual(result['peak_index_owners'],len(t.Model(f).maps))
    with tempfile.TemporaryDirectory() as td:
     a=Path(td)/'native';b=Path(td)/'physical';budget=t.Budget(10);t.write_keys(result,f,a,budget);o.truth(f,obs,b,budget.check,t.Limit);self.assertTrue(filecmp.cmp(a,b,shallow=False))
 def test_all_small_torus_predicates_and_mask_accounting(self):
  import itertools
  f=t.fixture(3,3);m=t.Model(f)
  for cap in (0,1024,64<<20):
   pred=s.ReservedPredicates(m,t.Budget(10),cap);direct=t.Predicates(m,t.Budget(10),0)
   for delta in itertools.product(range(3),repeat=3):
    for p,c in itertools.product(range(3),repeat=2):self.assertEqual(pred.get(delta,p,c),direct.get(delta,p,c))
   self.assertLessEqual(pred.metrics()['total_cache_peak_accounting_upper_bound'],cap)
 def test_conflicts_and_budget_do_not_become_false_negatives(self):
  f=t.fixture(3,3);r=s.solve(t.Model(f),[(0,1,1),(0,1,2)],t.Budget(10));self.assertTrue(r['completed']);self.assertEqual(r['exact_raw_key_count'],'0')
  r=s.solve(t.Model(f),[(0,1,1)],t.Budget(10),domain_cap=1);self.assertFalse(r['completed']);self.assertIsNone(r['exact_raw_key_count'])

 def test_hash_collisions_never_merge_unequal_domains(self):
  a=s.Domain(0);b=s.Domain(sys.hash_info.modulus);same=s.Domain(sys.hash_info.modulus)
  self.assertEqual(hash(a),hash(b));self.assertNotEqual(a,b);self.assertEqual(b,same)
  domains={((),a):[1],((),b):[2]};self.assertEqual(len(domains),2)
  self.assertEqual(domains[(),same],[2]);self.assertIs(b.meet(b.bits),b)
  self.assertEqual(b.meet(0),a)
  with self.assertRaises(AttributeError):b.bits=0
  with self.assertRaises(ValueError):s.Domain(-1)
