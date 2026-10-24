import hashlib,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import cover_selector_038 as s
class CoverSelector038Tests(unittest.TestCase):
 def test_complete_independent_small_systems_and_plants(self):
  self.assertEqual(s.controls(),dict(complete_tiny_selector_distribution_comparisons=960,selector_plants=40,complete_full_key_relations=8))
 def test_complete_saved_distributions_scope_and_source_pins(self):
  r=json.loads((ROOT/'results/COVER-SELECTOR-038-ORIGINAL.json').read_text());self.assertEqual(r['selector_descriptions'],120);self.assertEqual(r['previous_distribution_equalities'],36);self.assertEqual(r['new_K4_outer_cipher_trials'],0);self.assertEqual(r['key_freedom']['compatible_full_length_key_plaintext_pairs'],26**73)
  for path,sha in r['source_hashes'].items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),sha)
  for name,m in r['models'].items():
   self.assertEqual(len(m['selectors']),40)
   for d in m['selectors'].values():self.assertEqual(sum(d['coverwords'].values()),d['total']);self.assertEqual(sum(d['output_lengths'].values()),d['total'])
 def test_phase_and_selected_short_word_are_not_silently_skipped(self):
  h=s.p.Lexicon({'A','BBBB'}).hist('ABBBBA');self.assertEqual(s.p.distribution(h,2,1,0)['total'],0);self.assertEqual(s.p.distribution(h,2,3,1)['total'],1);self.assertEqual(s.p.distribution(h,2,3,0)['total'],0)
