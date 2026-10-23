import hashlib,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
class DomainArtifactTests(unittest.TestCase):
 def test_profile_evidence_and_inputs_are_retained(self):
  for n in (0,1):
   r=json.loads((ROOT/f'results/sigaba-domain-profile/case-{n}.json').read_text());self.assertEqual(r['K4_evaluations'],0)
   for p,h in {**r['source_sha256'],**r['result']['source_sha256']}.items():self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),h)
  r=json.loads((ROOT/'results/sigaba-domain-profile/case-1.json').read_text());top=r['function_table'][0];self.assertEqual(top['function'],'merge');self.assertGreater(top['self_seconds']/r['profile_total_seconds'],.9)
 def test_unchanged_fixtures_and_unknown_counts(self):
  for n in (0,1):
   a=json.loads((ROOT/f'results/sigaba-sparse-ownership/case-{n}.json').read_text());b=json.loads((ROOT/f'results/sigaba-domain-identity/case-{n}.json').read_text());s=b['solver'];self.assertEqual(a['fixture'],b['fixture']);self.assertEqual(a['preflight'],b['preflight']);self.assertFalse(s['completed']);self.assertIsNone(s['exact_raw_key_count']);self.assertEqual(s['control_starts_completed'],0);self.assertFalse(b['real_sized_gate_passed']);self.assertEqual(b['K4_evaluations'],0)
   for p,h in b['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),h)
  r=json.loads((ROOT/'results/sigaba-domain-identity/case-1.json').read_text())['solver'];self.assertEqual(r['current_time_zero_based'],17);self.assertEqual(r['backend_metrics']['calls'],0)
 def test_latest_scope_and_summary_are_consistent(self):
  import exclusion_scope_audit as a,frontier_assessment as f
  self.assertEqual(a.run()['fresh_analytical_replay'],json.loads((ROOT/'results/EXCLUSION-SCOPE-AUDIT-012.json').read_text())['fresh_analytical_replay']);self.assertEqual(json.loads((ROOT/'results/FRONTIER-016.json').read_text())['ready_new_K4_experiments'],0)
  r=json.loads((ROOT/'results/CSP889-DOMAIN-016.json').read_text());self.assertEqual(r['real_controllers_completed'],0);self.assertFalse(r['real_sized_gate_passed'])
