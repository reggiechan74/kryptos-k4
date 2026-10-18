import json
from pathlib import Path
import random
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'experiments'))
from structural_checks import known_pairs, periodic_conflicts, encode_pairs, decode_pairs, run
from ciphers import vigenere, KRYPTOS


class StructuralTests(unittest.TestCase):
    def test_permutation_only_contradiction(self):
        result = run()
        self.assertEqual(result['ciphertext_counts']['E'], 2)
        self.assertEqual(result['crib_required_counts']['E'], 3)
        self.assertEqual(result['permutation_only']['deficits'], {'E': {'required_by_disjoint_cribs': 3, 'available_ciphertext': 2}})
        # Any permutation preserves the entire multiset, not just E.
        data = json.loads((ROOT / 'data/k4.json').read_text())
        from collections import Counter
        self.assertEqual(Counter(data['ciphertext'][::-1]), Counter(data['ciphertext']))

    def test_independent_proposed_period_list_through_50(self):
        expected = [1,2,3,4,5,6,7,9,10,14,15,17,21,25,34,42,43,45,50]
        result = run()['periodic_bijective']['contradicted']
        self.assertEqual([p for p in result if p <= 50], expected)

    def test_both_directions_of_bijection(self):
        self.assertTrue(periodic_conflicts([(0,'Q','N'),(1,'Q','O')], 1))
        self.assertTrue(periodic_conflicts([(0,'F','E'),(1,'Y','E')], 1))
        self.assertFalse(periodic_conflicts([(0,'Q','N'),(1,'Q','O')], 2))

    def test_period_42_witness(self):
        data = json.loads((ROOT / 'data/k4.json').read_text())
        w = periodic_conflicts(known_pairs(data), 42)
        self.assertIn({'positions_one_based':[25,67], 'cipher':'VV', 'plain':'TL', 'reason':'same cipher, different plain'}, w)

    def test_synthetic_period_recovery_control(self):
        rng = random.Random(20261018)
        for period in [1, 2, 7, 8, 10, 21, 42]:
            plain = ''.join(rng.choice(KRYPTOS) for _ in range(97))
            key = ''.join(rng.choice(KRYPTOS) for _ in range(period))
            cipher = vigenere(plain, key)
            pairs = [(i,c,p) for i,(c,p) in enumerate(zip(cipher,plain))]
            self.assertFalse(periodic_conflicts(pairs, period))

    def test_pair_codec_all_symbols_and_sequences(self):
        rng = random.Random(20261018)
        for values in [[], list(range(48)), [47]*10, [rng.randrange(48) for _ in range(97)]]:
            self.assertEqual(decode_pairs(encode_pairs(values)), values)
        self.assertEqual(len(encode_pairs(list(range(48)))), 96)
        with self.assertRaises(ValueError): decode_pairs('A'*97)
        for invalid in ['ZZ', 'aA', 'A?', '']:
            if invalid:
                with self.assertRaises(ValueError): decode_pairs(invalid)
        with self.assertRaises(ValueError): encode_pairs([48])


if __name__ == '__main__': unittest.main()
