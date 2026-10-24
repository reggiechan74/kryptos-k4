import hashlib,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import review_controls_045 as c
class ReviewControls045Tests(unittest.TestCase):
 def test_changed_crib_late_supplement_preserves_exact_free_key_ambiguity(self):
  r=c.run();self.assertEqual(r['changed_crib_complete_systems'],8)
  for row in r['records']:self.assertTrue(row['disjoint_key_sets']);self.assertTrue(row['old_keys_all_fail_changed_crib']);self.assertTrue(row['new_free_keys_remain_admitted']);self.assertEqual(row['contradictory_duplicate_crib_keys'],0)
  saved=json.loads((ROOT/'results/REVIEW-CONTROLS-045.json').read_text())
  for p,h in saved['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),h)
