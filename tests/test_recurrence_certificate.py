from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments'))
from recurrence_certificate import determinant,run


class RecurrenceCertificateTests(unittest.TestCase):
    def test_supplied_certificates_recomputed_from_fixed_crib(self):
        r=run()
        self.assertFalse(r['parameter_search_executed'])
        self.assertEqual(r['parameter_descriptions'],913952)
        self.assertEqual(r['training_compatible'],0)
        self.assertTrue(all(x['contradicted'] for x in r['proofs']))
        self.assertEqual(r['proofs'][1]['predicted_key'],21)
        self.assertEqual(r['proofs'][1]['required_key'],1)

    def test_determinant_can_detect_nonunit(self):
        self.assertEqual(determinant([[1,0,0],[0,1,0],[0,0,1]]),1)
        self.assertEqual(determinant([[2,0,0],[0,1,0],[0,0,1]]),2)


if __name__=='__main__':unittest.main()
