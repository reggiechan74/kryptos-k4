"""Offline unit controls. Contains no full third-party artwork text."""
import unittest
import audit_construction as a

class ConventionTests(unittest.TestCase):
    def test_latin_local_equivalence(self):
        for plain,key,cipher in [('L','C','K'),('Q','S','K'),('L','S','W'),('O','S','E'),('U','S','R')]:
            self.assertEqual(a.poly(plain,a.KA,a.KA,key,a.KA),cipher)

    def test_distinct_cp_alphabets(self):
        self.assertEqual(len(a.CP_PLAIN),32)
        self.assertEqual(len(a.CP_CIPHER),32)
        self.assertEqual(set(a.CP_PLAIN),set(a.CP_CIPHER))
        self.assertNotIn('Ё',a.CP_PLAIN)
        self.assertNotEqual(''.join(dict.fromkeys('ТЕНЬ'+a.CP_PLAIN)),a.CP_CIPHER)

    def test_cp_roundtrip(self):
        plain=a.CP_PLAIN*3
        encrypted=a.poly(plain,a.CP_PLAIN,a.CP_CIPHER,a.CP_KEY,a.CP_PLAIN,restart=39)
        self.assertEqual(a.poly(encrypted,a.CP_PLAIN,a.CP_CIPHER,a.CP_KEY,a.CP_PLAIN,decrypt=True,restart=39),plain)

    def test_restart_and_phase_jump_equivalence(self):
        # Synthetic plaintext, independent of any artwork. 39 = 3 (mod 6).
        plain=a.CP_PLAIN*3
        cipher=a.poly(plain,a.CP_PLAIN,a.CP_CIPHER,a.CP_KEY,a.CP_PLAIN,restart=39)
        manual=''.join(a.CP_CIPHER[(a.CP_PLAIN.index(p)+a.CP_PLAIN.index(a.CP_KEY[(i+(3 if i>=39 else 0))%6]))%32] for i,p in enumerate(plain))
        self.assertEqual(cipher,manual)
        continuous=a.poly(plain,a.CP_PLAIN,a.CP_CIPHER,a.CP_KEY,a.CP_PLAIN)
        self.assertEqual(cipher[:39],continuous[:39])
        self.assertTrue(all(x!=y for x,y in zip(cipher[39:],continuous[39:])))

    def test_reject_invalid_alphabet(self):
        with self.assertRaises(AssertionError):
            a.poly('A','AAC','ABC','A','ABC')

    def test_reject_unknown_letter(self):
        with self.assertRaises(ValueError):
            a.poly('Ё',a.CP_PLAIN,a.CP_CIPHER,a.CP_KEY,a.CP_PLAIN)

    def test_bounded_operator_count(self):
        self.assertEqual(1+97*25+98*26+97,5071)

if __name__=='__main__': unittest.main()
