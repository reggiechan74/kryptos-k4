import hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class SupportSignatureArtifacts(unittest.TestCase):
 def test_fixed_comparison_receipts_have_partial_coverage_not_a_negative(self):
  r=json.loads((ROOT/'results/SIGABA-SUPPORT-SIGNATURE-041-SUMMARY.json').read_text());self.assertEqual(len(r['comparisons']),4);self.assertFalse(r['real_sized_gate_passed']);self.assertEqual(r['K4_evaluations'],0);self.assertEqual(len(r['published_simulator_vectors']),12)
  for path,sha in r['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),sha)
  for row in r['comparisons']:
   d=json.loads((ROOT/row['receipt']).read_text());s=d['solver'];self.assertFalse(s['completed']);self.assertEqual(s['reason'],'wall_budget_unresolved');self.assertIsNone(s['exact_raw_key_count']);self.assertEqual(s['control_starts_requested'],26**5);self.assertEqual(s['index_classes'],66058);self.assertEqual(s['index_raw_states'],100000);self.assertLess(s['budget']['peak_RSS_bytes'],1<<30);self.assertEqual(s['found_raw_keys_lower_bound'],'0')
   if row['backend']=='cached':self.assertEqual(s['support_cache']['hits'],0);self.assertLessEqual(s['support_cache']['peak_bytes'],64<<20)
 def test_benchmark_fixtures_are_unchanged_and_prefixes_overlap(self):
  for case in (0,1):
   original=json.loads((ROOT/f'results/sigaba-real-adapter/case-{case}.json').read_text())['fixture'];u=json.loads((ROOT/f'results/SIGABA-SUPPORT-SIGNATURE-041-uncached-case{case}.json').read_text());c=json.loads((ROOT/f'results/SIGABA-SUPPORT-SIGNATURE-041-cached-case{case}.json').read_text());self.assertEqual(u['fixture'],original);self.assertEqual(c['fixture'],original);self.assertEqual(u['solver']['control_starts_completed'],12);self.assertEqual(c['solver']['control_starts_completed'],12-case)
 def test_additional_outer_mask_can_remove_direct_strip_fixedpoint_invariant(self):
  # Complete, reversible synthetic counterexample, not a sourced composite K4 cipher.
  a='ABCDEFGHIJKLMNOPQRSTUVWXYZ';strip=lambda t:''.join(a[(a.index(x)+1)%26] for x in t);mask=lambda t:''.join(a[(a.index(x)-1)%26] for x in t);self.assertEqual(mask(strip(a)),a);self.assertEqual(strip(mask(a)),a)
