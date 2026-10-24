import json,hashlib,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import spelling_morphism_review_045 as m
class SpellingMorphismReview045Tests(unittest.TestCase):
 def test_non_erasing_length_bound_and_erasing_fixed_length_collision(self):
  r=m.run();self.assertEqual(r['complete_binary_length_cases'],5880);self.assertTrue(all(not x['uniform_permutation_fit']['compatible'] for x in r['source_constraints']));a=r['full_fixed97_erasing_collision'];self.assertEqual(len(a['first']),97);self.assertEqual(len(a['second']),97);self.assertNotEqual(a['first'],a['second']);self.assertEqual(a['first'].replace('A',''),a['second'].replace('A',''))
  saved=json.loads((ROOT/'results/SPELLING-MORPHISM-REVIEW-045.json').read_text())
  for p,h in saved['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),h)
