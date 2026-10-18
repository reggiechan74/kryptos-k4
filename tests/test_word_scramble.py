from pathlib import Path
import sys,unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
from word_scramble import *

class WordScrambleTests(unittest.TestCase):
    def test_all24_planted_models_and_both_negative_controls(self):
        c=controls();self.assertEqual(c['actual_scanner_planted_acceptances'],24);self.assertEqual(c['endpoint_rejections'],24);self.assertEqual(c['interior_multiset_rejections'],24)
    def test_SALT_SLAT_no_unique_inverse_without_schedule(self):
        self.assertTrue(word_invariants('SALT','SLAT')['compatible']);self.assertTrue(word_invariants('SLAT','SALT')['compatible'])
        self.assertEqual(apply_schedule('SALT',[{'start':1,'end':4}],[[1,0]]),'SLAT')
        self.assertEqual(apply_schedule('SLAT',[{'start':1,'end':4}],[[1,0]],True),'SALT')
    def test_endpoints_counts_and_lengths_are_separate_gates(self):
        self.assertEqual(word_invariants('XALT','SALT')['first_rejecting_condition'],'endpoint_mismatch')
        self.assertEqual(word_invariants('SZLT','SALT')['first_rejecting_condition'],'interior_multiset_mismatch')
        self.assertEqual(word_invariants('SALLT','SALT')['first_rejecting_condition'],'word_length')
    def test_explicit_schedule_and_span_validation(self):
        with self.assertRaises(ValueError):apply_schedule('SALT',[{'start':1,'end':4}],[[0,0]])
        with self.assertRaises(ValueError):apply_schedule('SALT',[{'start':1,'end':4},{'start':2,'end':4}],[[0,1],[0]])
    def test_initial_deadline(self):
        with self.assertRaises(TimeoutError):word_scan({'ciphertext':'A'*97},[],-1)

if __name__=='__main__':unittest.main()
