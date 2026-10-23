import hashlib,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
class AnchorArtifactTests(unittest.TestCase):
 def test_official_fixtures_unknown_totals_and_reached_observations(self):
  for n in (0,1):
   old=json.loads((ROOT/f'results/sigaba-domain-identity/case-{n}.json').read_text());new=json.loads((ROOT/f'results/sigaba-first-observation/case-{n}.json').read_text());self.assertEqual(old['fixture'],new['fixture']);self.assertEqual(old['preflight'],new['preflight']);s=new['solver'];self.assertFalse(s['completed']);self.assertIsNone(s['exact_raw_key_count']);self.assertEqual(s['control_starts_completed'],0);self.assertEqual(new['K4_evaluations'],0);self.assertFalse(new['real_sized_gate_passed'])
   for p,h in new['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),h)
  s=json.loads((ROOT/'results/sigaba-first-observation/case-1.json').read_text())['solver'];self.assertEqual(s['first_observed_time'],21);self.assertEqual(s['current_time_zero_based'],24);self.assertEqual(s['backend_metrics']['calls'],318)
 def test_chronology_and_literature_are_not_search_claims(self):
  r=json.loads((ROOT/'results/ANCHOR-017-chronology.json').read_text());self.assertTrue(r['premature_receipts_are_not_official_benchmark']);self.assertFalse(r['implementation_algorithm_changed_after_premature_run'])
  for n in (0,1):self.assertTrue((ROOT/f'results/sigaba-first-observation-premature/case-{n}.json').exists())
  r=json.loads((ROOT/'sources/sigaba-literature-anchoring-2026-10-23.json').read_text());self.assertEqual(hashlib.sha256((ROOT/'research/SIGABA-LITERATURE-AND-FILTER-REVIEW.md').read_bytes()).hexdigest(),r['synthesis_sha256'])
  r=json.loads((ROOT/'results/CSP889-ANCHOR-017.json').read_text());self.assertFalse(r['filter_diagnostic_executed']);self.assertFalse(r['premature_receipts_counted_as_coverage']);self.assertEqual(r['complete_tiny_raw_sets'],8)
 def test_latest_scope_and_readiness(self):
  import exclusion_scope_audit as a,frontier_assessment as f
  self.assertEqual(a.run()['fresh_analytical_replay'],json.loads((ROOT/'results/EXCLUSION-SCOPE-AUDIT-013.json').read_text())['fresh_analytical_replay']);self.assertEqual(json.loads((ROOT/'results/FRONTIER-017.json').read_text())['ready_new_K4_experiments'],0)
