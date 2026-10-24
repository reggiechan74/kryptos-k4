import collections,hashlib,itertools,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import prose_cover as p
import audit_prose_cover as reference
class ProseArtifactTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=json.loads((ROOT/'results/PROSE-COVER-035-ORIGINAL.json').read_text())
 def test_sources_complete_domains_and_exact_language_limit(self):
  r=self.r
  for path,sha in r['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),sha)
  self.assertEqual({k:v['words'] for k,v in r['vocabularies'].items()},{'S':40210,'J':45820,'O':45826});self.assertTrue(r['stages']['mask_constraints']['complete']);self.assertFalse(r['puzzle_solved'])
  for name,row in r['stages']['mask_constraints']['models'].items():
   self.assertEqual(len(row['selectors']),12)
   for key,d in row['selectors'].items():self.assertEqual(sum(d['coverwords'].values()),d['total']);self.assertEqual(sum(d['output_lengths'].values()),d['total'])
  self.assertEqual((min(map(int,r['stages']['mask_constraints']['models']['J']['selectors']['k1:N1:p0']['coverwords'])),max(map(int,r['stages']['mask_constraints']['models']['J']['selectors']['k1:N1:p0']['coverwords']))),(7,79))
 def test_actual_complete_and_full_independent_set_replay(self):
  a=self.r['stages']['actual'];self.assertTrue(a['complete']);self.assertEqual(a['model_key_descriptions'],105456);self.assertEqual(len(a['models']),6);self.assertEqual(a['candidates'],[])
  for row in a['models']:self.assertEqual((row['free_symbols'],row['processed'],row['expected']),(3,17576,17576))
  independent=json.loads((ROOT/'results/PROSE-COVER-035-INDEPENDENT-AUDIT.json').read_text());self.assertTrue(independent['complete']);self.assertEqual(independent['model_key_descriptions'],105456)
  for row in independent['model_rows']:self.assertTrue(row['complete_plaintext_set_equal']);self.assertEqual(row['independent_wordbreak_survivors'],0)
 def test_matched_nulls_preserve_all_crib_cipher_pairs(self):
  n=self.r['stages']['nulls'];self.assertTrue(n['complete']);self.assertEqual(len(n['records']),31);original=self.r['canonical_ciphertext'];known={int(i)-1:v for i,v in self.r['known_one_based'].items()};indices=n['shuffled_positions'];self.assertEqual(len(indices),73)
  for record in n['records']:
   c=record['ciphertext'];self.assertEqual(collections.Counter(c[i] for i in indices),collections.Counter(original[i] for i in indices));self.assertTrue(all(c[i]==original[i] for i in known));self.assertTrue(record['search']['complete']);self.assertEqual(record['search']['model_key_descriptions'],105456);self.assertEqual(record['search']['distinct_lexical_plaintexts'],0)
 def test_real_sized_plants_retained_with_ambiguity_and_reencryption(self):
  records=self.r['stages']['plants']['records'];self.assertTrue(self.r['stages']['plants']['complete']);self.assertEqual([r['search']['distinct_lexical_plaintexts'] for r in records],[1,4,1,1,12,3])
  for record in records:
   self.assertEqual(len(record['truth']),97);self.assertTrue(record['truth_recovered']);self.assertIn(record['truth'],[x['plaintext'] for x in record['search']['candidates']]);a=p.ALPHABETS[record['alphabet']]
   for row in record['search']['candidates']:self.assertEqual(p.ak.transform(row['plaintext'],row['primer'],a,record['equation'],'plaintext'),record['ciphertext'])
 def test_calibration_records_false_negative_risk(self):
  c=self.r['calibration'];self.assertEqual(c['k1']['models']['S']['total'],0);self.assertEqual(c['k1']['models']['O']['total'],2);self.assertGreater(c['k2_restored_s']['models']['O']['total'],1);self.assertEqual(c['k3']['models']['O']['total'],0)
 def test_independent_reference_against_all_tiny_primers(self):
  alphabet='ABC';cipher='ABCAABBC'
  for e in p.ak.COEFFICIENTS:
   for known in ({},{0:'A'},{0:'A',3:'B'}):self.assertEqual(set(reference.reference_plaintexts(cipher,known,alphabet,e,3)),set(p.plaintexts(cipher,known,alphabet,e,3)))
