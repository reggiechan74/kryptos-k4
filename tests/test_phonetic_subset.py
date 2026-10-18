from pathlib import Path
import json,sys,unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
from phonetic_subset import respell_word,controls

class PhoneticSubsetTests(unittest.TestCase):
    def test_three_rules_and_loss_example(self):
        self.assertEqual(respell_word('WORD'),'VORT');self.assertEqual(respell_word('WEDDING'),'VEDDINK');self.assertEqual(respell_word('DOG'),'DOK');self.assertTrue(controls()['WET_VET_loss_collision'])
    def test_all_four_crib_words_unchanged_without_TH_or_I_rules(self):
        for word in ['EAST','NORTHEAST','BERLIN','CLOCK']:self.assertEqual(respell_word(word),word)
        self.assertEqual(respell_word('THIN'),'THIN');self.assertEqual(respell_word('I'),'I')
    def test_no_silent_case_or_segmentation(self):
        for word in ['word','WORD WORD','',"WORD'"]:
            with self.assertRaises(ValueError):respell_word(word)
    def test_registered_result_and_hashes(self):
        import hashlib
        paths=[ROOT/'results/phonetic-subset-runs/20261018T113329Z-3d5c35d85cbb4e2a9b9864410c053c54/manifest.json']
        manifest=json.loads(paths[0].read_text());self.assertEqual(manifest['status'],'completed')
        result=json.loads((paths[0].parent/'PHONETIC-SUBSET-001.json').read_text());self.assertEqual(result['rescued_models'],0);self.assertEqual(result['existing_models_checked'],12)
        for path,sha in result['run_metadata']['file_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),sha)

if __name__=='__main__':unittest.main()
