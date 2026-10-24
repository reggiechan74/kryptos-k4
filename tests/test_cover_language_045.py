import hashlib,json,sys,unittest
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import cover_language_045 as c
class CoverLanguage045Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads((ROOT/'results/COVER-LANGUAGE-045-ORIGINAL.json').read_text());cls.table=c.table_from_counts(json.loads((ROOT/'data/cover-trigrams-045.json').read_text())['counts'],26)
 def test_complete_tiny_fraction_reference_positive_support_and_source_pins(self):
  self.assertEqual(c.controls()['complete_small_string_mask_fraction_checks'],254);r=self.r
  for p,h in r['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),h)
  self.assertEqual(hashlib.sha256((ROOT/'data/cover-trigrams-045.json').read_bytes()).hexdigest(),r['counts_sha256']);self.assertTrue(all(x>0 for x in self.table['numerators']))
 def test_actual_and_reused_nulls_repeat_whole_family_exact_maxima(self):
  r=self.r;prior=json.loads((ROOT/'results/PROSE-COVER-035-ORIGINAL.json').read_text());known={int(i)-1:x for i,x in prior['known_one_based'].items()};terms=c.indices(97,known);self.assertEqual(len(terms),67);self.assertEqual(r['stages']['actual']['model_key_descriptions'],105456);self.assertEqual(r['stages']['nulls']['exceedances'],2)
  for record,cipher in [(r['stages']['actual'],prior['canonical_ciphertext'])]+[(x['search'],x['ciphertext']) for x in r['stages']['nulls']['records']]:
   self.assertTrue(record['complete']);self.assertEqual(len(record['model_rows']),6);self.assertEqual(record['model_key_descriptions'],105456);f=record['max_score'];target=Fraction(int(f['numerator']),int(f['denominator']))
   for row in record['maxima']:
    self.assertEqual(c.reference_score(row['plaintext'],terms,self.table),target);self.assertTrue(all(row['plaintext'][i]==v for i,v in known.items()));self.assertEqual(c.p.ak.transform(row['plaintext'],row['primer'],c.p.ALPHABETS[row['alphabet']],row['equation'],'plaintext'),cipher)
 def test_calibration_retains_K3_but_planted_rank_failure_prevents_recovery_claim(self):
  r=self.r;self.assertTrue(r['calibration_gate_passed']);self.assertEqual([x['at_least_as_large'] for x in r['stages']['calibration']],[0,0,0]);self.assertTrue(all(x['positive_support'] for x in r['stages']['calibration']));plants=r['stages']['plants'];self.assertEqual(len(plants),6);self.assertTrue(all(x['search']['plant']['true_pair_enumerated'] for x in plants));self.assertEqual(sum(x['search']['plant']['truth_among_global_maxima'] for x in plants),5);self.assertFalse(r['positive_K4_identification']);self.assertFalse(r['new_outer_cipher_domain']);self.assertEqual(r['new_hidden_extraction_trials'],0)
