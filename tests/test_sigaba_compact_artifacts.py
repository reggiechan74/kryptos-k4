import hashlib,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
class CompactArtifactTests(unittest.TestCase):
 def test_density_profiles_support_exact_storage_choice(self):
  for n in (0,1):
   r=json.loads((ROOT/f'results/sigaba-payload-profile/case-{n}.json').read_text());p=r['solver']['payload_profile'];self.assertGreater(p['integer_payload_bytes'],p['packed_u32_payload_estimated_bytes']*100)
   self.assertEqual(sum(p['cardinality_histogram'].values()),p['distinct_payload_objects'])
   for name,h in r['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),h)
 def test_fixture_domain_cache_and_partial_coverage_are_exact(self):
  for n in (0,1):
   old=json.loads((ROOT/f'results/sigaba-first-observation/case-{n}.json').read_text());new=json.loads((ROOT/f'results/sigaba-compressed-ownership/case-{n}.json').read_text());s=new['solver'];self.assertEqual(old['fixture'],new['fixture']);self.assertEqual(old['preflight'],new['preflight']);self.assertFalse(s['completed']);self.assertIsNone(s['exact_raw_key_count']);self.assertGreater(s['control_starts_completed'],0);self.assertEqual(new['K4_evaluations'],0);self.assertFalse(new['real_sized_gate_passed']);self.assertLess(s['budget']['peak_RSS_bytes'],1<<30);self.assertLessEqual(s['backend_metrics']['total_cache_peak_accounting_upper_bound'],64<<20)
   for name,h in new['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),h)
 def test_current_scope_and_local_only_frontier(self):
  import exclusion_scope_audit as a,frontier_assessment as f
  self.assertEqual(a.run()['fresh_analytical_replay'],json.loads((ROOT/'results/EXCLUSION-SCOPE-AUDIT-014.json').read_text())['fresh_analytical_replay']);self.assertEqual(json.loads((ROOT/'results/FRONTIER-018.json').read_text())['ready_new_K4_experiments'],0)
  r=json.loads((ROOT/'results/CSP889-COMPACT-018.json').read_text());self.assertEqual(r['real_controllers_completed'],[12,14]);self.assertFalse(r['real_sized_gate_passed'])
