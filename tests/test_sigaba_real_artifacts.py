import hashlib,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import sigaba_real_adapter as real
class RealArtifactTests(unittest.TestCase):
 def test_frozen_resource_failures_are_unknown_not_negatives(self):
  old=json.loads((ROOT/'results/SIGABA-JOINT-FEASIBILITY-003.json').read_text())
  for n in (0,1):
   r=json.loads((ROOT/f'results/sigaba-real-adapter/case-{n}.json').read_text());s=r['solver']
   self.assertEqual(r['fixture'],json.loads(json.dumps(real.fixture(n))))
   self.assertEqual(r['index_quotient_sha256'],old['classes_sha256']);self.assertEqual(r['preflight']['index_functions'],66058)
   self.assertFalse(s['completed']);self.assertIsNone(s['exact_raw_key_count']);self.assertEqual(s['control_starts_completed'],0);self.assertFalse(r['real_sized_gate_passed']);self.assertFalse(r['independent_full_compatible_set_validation']);self.assertEqual(r['K4_evaluations'],0)
   for p,h in r['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),h)
   self.assertLess(s['budget']['peak_RSS_bytes'],1<<30)
 def test_current_scope_and_readiness_are_pinned(self):
  import exclusion_scope_audit as a,frontier_assessment as f
  self.assertEqual(a.run()['fresh_analytical_replay'],json.loads((ROOT/'results/EXCLUSION-SCOPE-AUDIT-010.json').read_text())['fresh_analytical_replay'])
  self.assertEqual(json.loads((ROOT/'results/FRONTIER-014.json').read_text())['ready_new_K4_experiments'],0)
 def test_cross_version_receipts_preserve_exact_tail_decisions(self):
  for name in ('python39','python312'):
   r=json.loads((ROOT/f'results/STAT-CROSSVERSION-014-{name}.json').read_text());self.assertTrue(r['exact_integer_draws_and_tail_decisions']);self.assertTrue(r['rational_mean_variance_reference'])
   for v in r['fields'].values():self.assertLessEqual(v['max_cross_version_scaled_ULP'],2)
