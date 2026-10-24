import itertools,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import one_edit_channel as c
import one_edit_models as m
import one_edit_reference as r

class OneEditCoreTests(unittest.TestCase):
 def test_all_5071_tagged_maps_and_forward_channels(self):
  source=(c.AZ*4)[:97];rows=list(c.edits(source));self.assertEqual(len(rows),5071)
  for e in rows:
   latent,o,l=r.tagged(source,e);self.assertEqual(c.repair(source,e),latent);self.assertEqual(c.index_maps(97,e),(o,l));self.assertEqual(c.forward(latent,e),source);self.assertEqual(r.reflected_forward(latent,e),source)
 def test_alignment_never_drops_or_splits_a_phrase(self):
  src=(c.AZ*4)[:97];cat=c.catalog(src);self.assertEqual(len(cat['alignment_inadmissible']),596);self.assertEqual(cat['admissible_alignment_descriptions'],9546)
  for i in cat['instances']:
   self.assertEqual(len(c.mask(i['starts'])),24)
  e=dict(kind='delete_observed',position=21,latent_char=None,observed_char=src[21]);self.assertEqual(c.anchors(97,e,'ENGLISH_FIXED')[0],(21,63));self.assertIsNone(c.anchors(97,e,'OBSERVED_CELL_TRANSPORT')[0])
  e=dict(kind='insert_latent',position=22,latent_char='A',observed_char=None);self.assertEqual(c.anchors(97,e,'OBSERVED_CELL_TRANSPORT')[1],'split_known_phrase')
  e['position']=21;self.assertEqual(c.anchors(97,e,'OBSERVED_CELL_TRANSPORT')[0],(22,64))
 def test_complete_tiny_key_and_permutation_sets(self):
  result=r.tiny_controls();self.assertEqual(result,dict(complete_permutation_truth_cases=24,complete_periodic_key_truth_cases=96))
 def test_exact_permutation_counts_and_witness_routes(self):
  known={0:'A',3:'B'};latent='AABBCC';pc=m.permutation_counts(latent,known);self.assertTrue(pc['compatible']);ws=m.permutation_witnesses(latent,known);self.assertEqual(len(ws),2);self.assertNotEqual(ws[0]['plaintext'],ws[1]['plaintext'])
  for w in ws:
   p=w['plaintext'];route=w['latent_position_at_each_plaintext_position_zero_based'];self.assertEqual(''.join(latent[j] for j in route),p)
 def test_period12_first_fit_is_guaranteed_by_one_substitution(self):
  source=(c.AZ*4)[:97]
  for name,eq in itertools.product(m.ALPHABETS,('plus','beaufort')):
   a=m.ALPHABETS[name];sign=1 if eq=='plus' else -1;need=(a.index(source[21])-sign*a.index('E')+sign*a.index('T'))%26;changed=source[:33]+a[need]+source[34:]
   mi=next(i for i,x in enumerate(m.MODELS) if x==dict(alphabet=name,equation=eq,period=12));self.assertIsNotNone(m.training(changed[21:34])[mi])
 def test_incomplete_training_or_berlin_span_rejected(self):
  with self.assertRaises(ValueError):m.training('A'*12)
  with self.assertRaises(ValueError):m.forecast('A'*10,[1],m.MODELS[0],42)
