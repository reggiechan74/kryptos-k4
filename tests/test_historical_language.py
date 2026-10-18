import json
from pathlib import Path
import sys,unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
from historical_language import GostCode,mapping_controls,suffix_trace

class HistoricalLanguageTests(unittest.TestCase):
    def setUp(self):
        self.manifest=json.loads((ROOT/'data/gost1981_table2_russian.json').read_text())
        self.code=mapping_controls(self.manifest)
    def test_exact_source_column_and_suffix_sets(self):
        self.assertEqual(suffix_trace(self.manifest['mapping'].values()),([['H','HH'],[]],True))
        self.assertEqual(len(self.manifest['mapping']),33)
    def test_hard_sign_is_not_two_soft_signs(self):
        self.assertEqual(self.code.decode('"'),'Ъ')
        self.assertEqual(self.code.decode("''"),'ЬЬ')
        self.assertEqual(self.code.decode('SHH'),'Щ')
    def test_domain_and_complete_parsing(self):
        for invalid in ['Q','X','W','H','J','KHQ']:
            with self.assertRaises(ValueError):self.code.decode(invalid)
        for invalid in ['б','Б Б',"'",'*','Ѣ']:
            with self.assertRaises(ValueError):self.code.encode(invalid)
    def test_apostrophe_exception_and_lossy_stripping(self):
        output=set(''.join(self.manifest['mapping'].values()));self.assertEqual(len(output),25)
        extended=dict(self.manifest['mapping']);extended["'"]='*'
        self.assertEqual(len(set(''.join(extended.values()))),26)
        self.assertEqual(GostCode(extended).decode('*'),"'")
        self.assertEqual({''.join(c for c in self.code.encode(s) if 'A'<=c<='Z') for s in ['Б','БЬ','БЪ']},{'B'})

if __name__=='__main__':unittest.main()
