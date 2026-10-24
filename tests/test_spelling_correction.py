import json,sys,unittest,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import spelling_correction as s
import spelling_correction_reference as r
class SpellingCorrectionTests(unittest.TestCase):
 def test_minimal_edits_and_missing_E_are_not_dropped(self):
  for a,b,d in [('IQLUSION','ILLUSION',1),('UNDERGRUUND','UNDERGROUND',1),('DESPARATLY','DESPERATELY',2),('MISTSKE','MISTAKE',1)]:
   x=s.alignments(a,b);self.assertEqual(x['distance'],d);self.assertEqual(len(x['alignments']),1)
  edits=[x for x in s.alignments('DESPARATLY','DESPERATELY')['alignments'][0] if x['op']!='M'];self.assertEqual([(c['source'],c['target']) for c in edits],[('A','E'),('','E')]);self.assertEqual(edits[1]['target_index'],8)
 def test_ambiguous_identical_deletion_strings_keep_alignments(self):
  x=s.alignments('AA','A');self.assertEqual(x['distance'],1);self.assertEqual(len(x['alignments']),2)
  for cols in x['alignments']:self.assertEqual(s.apply_script(s.apply_script('AA',cols),s.inverse(cols)),'AA')
 def test_global_function_conflict_with_unchanged_letters(self):
  f=s.infer_function([('K1','ILLUSION','IQLUSION')]);self.assertFalse(f['compatible']);self.assertEqual(f['reason'],'one input requires different outputs')
  f=s.infer_function([('K2','UNDERGRUUND','UNDERGROUND')]);self.assertFalse(f['compatible']);self.assertEqual({x['target'] for x in f['witness']},{'O','U'})
 def test_error_only_affine_reference(self):
  for abc in s.ALPHABETS.values():self.assertEqual(s.affine_candidates([('Q','L'),('U','O')],abc),[]);self.assertEqual(r.congruence_candidates([('Q','L'),('U','O')],abc,True),[])
  self.assertEqual(s.affine_candidates([('Q','L'),('U','O')],s.KRYPTOS,False),[dict(a=14,b=23,invertible=False)])
 def test_map_completion_counts_and_injectivity(self):
  self.assertEqual(s.infer_function([('x','A','B')],'ABC')['completion_count'],9);self.assertEqual(s.infer_function([('x','A','B')],'ABC',True)['completion_count'],2);self.assertFalse(s.infer_function([('x','AB','AA')],'ABC',True)['compatible'])
 def test_keyboard_vector_and_domain(self):
  k=s.keyboard_coordinates();self.assertEqual(k['L'],(33,1));self.assertEqual(k['Q'],(0,0));self.assertNotEqual((33,1),(8,0));self.assertEqual(s.keyboard_apply('ASDF',(4,0)),'SDFG')
  with self.assertRaises(ValueError):s.keyboard_apply('L',(4,0))
 def test_masks_retain_all_neutral_positions(self):
  a=s.masks(s.AZ);self.assertEqual(a['changed_only'],[21,20]);self.assertEqual(len(a['neutral_padded_word_pair']),19);self.assertEqual([i for i,v in enumerate(a['neutral_padded_word_pair']) if v],[1,15]);self.assertEqual(s.translate('IQLUSIONUNDERGRUUND',a['neutral_padded_word_pair'],s.AZ),'ILLUSIONUNDERGROUND')
 def test_full_source_comparisons_only_replace_declared_word(self):
  c=json.loads((ROOT/'data/controls.json').read_text());rows=s.full_sources(c);self.assertEqual(len(rows),3)
  for row in rows:self.assertEqual(len(row['literal'])-len(row['comparison']),-1 if row['id']=='K3' else 0)
  self.assertTrue(rows[1]['literal'].endswith('WESTIDBYROWS'));self.assertTrue(rows[1]['comparison'].endswith('WESTIDBYROWS'))
 def test_corrupted_script_is_rejected(self):
  with self.assertRaises(ValueError):s.apply_script('WRONG',s.alignments('AA','A')['alignments'][0])
