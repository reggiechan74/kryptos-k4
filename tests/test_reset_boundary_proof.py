"""Exact witness regressions; frozen known-witness verification scope."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'experiments'))
from reset_boundary_proof import analyze


class ResetBoundaryProofTests(unittest.TestCase):
    def test_pinned_bijection_witness(self):
        data = json.loads((ROOT / 'data/k4.json').read_text())
        result = analyze(data)['identical_reset_bijection_witness']
        self.assertEqual(result['positions_one_based'], [25, 67])
        self.assertEqual(result['zero_based_offsets_after_resets'], [3, 3])
        self.assertEqual(result['ciphertext'], ['V', 'V'])
        self.assertEqual(result['plaintext'], ['T', 'L'])
        self.assertTrue(result['contradiction'])

    def test_arithmetic_witnesses_against_independent_forward_trials(self):
        data = json.loads((ROOT / 'data/k4.json').read_text())
        result = analyze(data)
        self.assertEqual(result['candidate_keys_tested'], 0)
        self.assertEqual(len(result['arithmetic_witnesses']), 12)
        for record in result['arithmetic_witnesses']:
            alphabet = record['alphabet']
            first, second = record['positions_one_based']
            # Independent crib transcription and complete finite single-key
            # forward truth table, used only as a regression control.
            p1, p2 = ('E', 'B') if second == 64 else ('E', 'S')
            c1, c2 = ('F', 'N') if second == 64 else ('F', 'S')
            def encode(p, key):
                value = alphabet.index(p)
                if record['equation'] == 'plus': value += key
                elif record['equation'] == 'minus': value -= key
                else: value = key - value
                return alphabet[value % 26]
            keys1 = [k for k in range(26) if encode(p1, k) == c1]
            keys2 = [k for k in range(26) if encode(p2, k) == c2]
            self.assertEqual([keys1[0], keys2[0]], record['required_key_values'])
            self.assertFalse(set(keys1) & set(keys2))
            self.assertTrue(record['contradiction'])

    def test_noncontradictory_synthetic_fixture_is_not_rejected(self):
        # Same input and output at equal offsets is compatible with a bijection.
        data = {'ciphertext': 'A' * 97,
                'cribs': [{'start': 22, 'end': 34, 'plaintext': 'B' * 13},
                          {'start': 64, 'end': 74, 'plaintext': 'B' * 11}]}
        self.assertFalse(analyze(data)['identical_reset_bijection_witness']['contradiction'])


if __name__ == '__main__':
    unittest.main()
