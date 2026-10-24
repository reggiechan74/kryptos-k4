import json,math,hashlib,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import spelling_correction as s
import run_spelling_correction as runner
class SpellingCorrectionArtifactTests(unittest.TestCase):
 def test_original_source_results_and_hashes_reproduce(self):
  d=json.loads((ROOT/'results/SPELLING-CORRECTION-032-ORIGINAL.json').read_text());self.assertEqual(s.investigate(json.loads((ROOT/'data/controls.json').read_text())),d['study']);self.assertEqual(d['K4_trials'],0);self.assertFalse(d['pushed']);self.assertFalse(d['Site_changed']);self.assertLess(d['elapsed_seconds'],60);self.assertLess(d['peak_rss_bytes'],256*1024**2)
  for path,sha in d['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),sha,path)
 def test_controls_and_all_source_phase_failures(self):
  d=json.loads((ROOT/'results/SPELLING-CORRECTION-032-ORIGINAL.json').read_text());self.assertEqual(runner.controls(),d['controls']);self.assertEqual(d['study']['source_mask_descriptions'],42);self.assertEqual(d['study']['full_source_mask_tests'],84)
  self.assertTrue(all(not c['exact_match'] for row in d['study']['source_mask_phase_records'] for c in row['source_checks']));self.assertFalse(any(d['study']['source_rule_feasibility'].values()))
 def test_no_insertion_or_intention_overstatement(self):
  d=json.loads((ROOT/'results/SPELLING-CORRECTION-032-ORIGINAL.json').read_text());e=d['study']['ordered_correction_extraction'];self.assertEqual(''.join(x['source'] for x in e),'QUA');self.assertEqual(''.join(x['target'] for x in e),'LOEE');self.assertEqual(e[-1]['source'],'');self.assertIn('not established',d['study']['inventory'][2]['intent'])
  oracle=s.infer_function([('changed_only','QU','LO')],injective=True);self.assertEqual(oracle['completion_count'],math.factorial(24))
