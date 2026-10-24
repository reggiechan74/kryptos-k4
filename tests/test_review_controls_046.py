import hashlib,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import review_controls_046 as r
class ReviewerControls046Tests(unittest.TestCase):
 def test_active_calculation_interruption_caches_no_partial_root(self):
  v=r.active_cache_control();self.assertEqual(v['active_stage']['layers_built'],4);self.assertTrue(v['partial_entry_absent']);self.assertTrue(v['subsequent_cache_hit'])
 def test_explicit_wrong_DST_and_valid_magic_invalid_flags(self):
  self.assertEqual(r.wrong_shared_dst_control()['difference_disagreements'],840);self.assertEqual(r.invalid_flags_control()['valid_magic_invalid_flag_transport_checks'],48)
 def test_saved_late_control_source_hashes(self):
  saved=json.loads((ROOT/'results/REVIEW-CONTROLS-046.json').read_text());self.assertEqual(saved['new_K4_trials'],0)
  for p,h in saved['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),h)
