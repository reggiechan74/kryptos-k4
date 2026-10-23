import hashlib,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
class SparseArtifactTests(unittest.TestCase):
 def test_fixtures_and_unknown_coverage_are_preserved(self):
  for n in (0,1):
   a=json.loads((ROOT/f'results/sigaba-real-adapter/case-{n}.json').read_text());b=json.loads((ROOT/f'results/sigaba-sparse-ownership/case-{n}.json').read_text());s=b['solver'];self.assertEqual(a['fixture'],b['fixture']);self.assertEqual(a['preflight'],b['preflight']);self.assertEqual(a['index_quotient_sha256'],b['index_quotient_sha256']);self.assertFalse(s['completed']);self.assertIsNone(s['exact_raw_key_count']);self.assertEqual(s['control_starts_completed'],0);self.assertEqual(b['K4_evaluations'],0);self.assertFalse(b['real_sized_gate_passed'])
   self.assertEqual(s['peak_index_owners'],66058);self.assertLessEqual(s['backend_metrics']['total_cache_peak_accounting_upper_bound'],64<<20)
   for p,h in b['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),h)
 def test_measured_bottlenecks_and_latest_scope(self):
  a=json.loads((ROOT/'results/sigaba-sparse-ownership/case-0.json').read_text())['solver'];b=json.loads((ROOT/'results/sigaba-sparse-ownership/case-1.json').read_text())['solver']
  self.assertEqual(a['backend_metrics']['zero_offset_builds'],3);self.assertEqual(a['backend_metrics']['calls'],202);self.assertEqual(b['backend_metrics']['calls'],0)
  import exclusion_scope_audit as audit,frontier_assessment as f
  self.assertEqual(audit.run(),json.loads((ROOT/'results/EXCLUSION-SCOPE-AUDIT-011.json').read_text()));self.assertEqual(f.assess(),json.loads((ROOT/'results/FRONTIER-015.json').read_text()))
