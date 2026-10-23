from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'experiments'))
from asymmetric_primer import AZ, KR, PRIMER, configurations, controls, decrypt, encrypt


class AsymmetricPrimerTests(unittest.TestCase):
    def test_exhaustive_symbols_planted_cribs_and_numeric_oracle(self):
        self.assertEqual(controls(), dict(symbol_roundtrips=4056, planted_full_recoveries=6,
                                         planted_crib_recoveries=6, mutated_crib_rejections=6,
                                         random_oracle_comparisons=48))

    def test_manually_indexed_answers_distinguish_roles(self):
        # AZ(A)=0, AZ(P)=15, KR[15]=I.
        cfg = dict(Ap='AZ', Ac='KR', Ak='AZ')
        self.assertEqual(encrypt('A', cfg), 'I')
        self.assertEqual(decrypt('I', cfg), 'A')
        # KR(A)=7, AZ(P)=15, AZ[22]=W.
        cfg = dict(Ap='KR', Ac='AZ', Ak='AZ')
        self.assertEqual(encrypt('A', cfg), 'W')

    def test_lag10_literal_feedback_and_no_unknown_parameter(self):
        cfg = dict(Ap='AZ', Ac='AZ', Ak='KR')
        # At position11, feedback is first plaintext A (KR index7), not primer P.
        cipher = encrypt('A' * 11, cfg)
        self.assertEqual(cipher[10], 'H')
        self.assertEqual(decrypt(cipher, cfg), 'A' * 11)
        self.assertEqual(len(PRIMER), 10)

    def test_six_distinct_role_triples(self):
        cases = list(configurations())
        self.assertEqual(len(cases), 6)
        self.assertTrue(all(len(set(c.values())) > 1 for c in cases))
        self.assertEqual(len({tuple(c.items()) for c in cases}), 6)
        self.assertEqual(set(AZ), set(KR))


if __name__ == '__main__':
    unittest.main()
