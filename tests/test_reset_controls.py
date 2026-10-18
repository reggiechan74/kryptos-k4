"""Synthetic preparation only; actual scanner recovery waits for frozen spec."""
from pathlib import Path
import random
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'experiments'))
from bounded_models import crypt
from ciphers import KRYPTOS
from reset_control_reference import reference_encrypt


class ResetControlPreparationTests(unittest.TestCase):
    def test_hand_vector_reset_before_index_four(self):
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.assertEqual(reference_encrypt('ATTACKATDAWN', 'KEY', alphabet,
                                          'plus', (0, 4)), 'KXRKMOYDHYGR')
        self.assertEqual(reference_encrypt('A' * 12, 'KEY', alphabet,
                                          'plus', (0, 4, 9)), 'KEYKKEYKEKEY')

    def test_independent_encoder_and_segment_inverse(self):
        rng = random.Random(20261018)
        for alphabet in ('ABCDEFGHIJKLMNOPQRSTUVWXYZ', KRYPTOS):
            plain = ''.join(rng.choice(alphabet) for _ in range(97))
            for equation in ('plus', 'minus', 'beaufort'):
                for starts in ((0,), (0, 4), (0, 21, 63), (0, 1, 96)):
                    key = 'RIVER'
                    cipher = reference_encrypt(plain, key, alphabet, equation, starts)
                    boundaries = starts + (len(plain),)
                    recovered = ''.join(crypt(cipher[a:b], [alphabet.index(c) for c in key],
                                              alphabet, equation, True)
                                        for a, b in zip(boundaries, boundaries[1:]))
                    self.assertEqual(recovered, plain)
                    regenerated = ''.join(crypt(recovered[a:b], [alphabet.index(c) for c in key],
                                                alphabet, equation)
                                          for a, b in zip(boundaries, boundaries[1:]))
                    self.assertEqual(regenerated, cipher)

    def test_wrong_boundary_is_detected(self):
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        plain = 'ATTACKATDAWN'
        actual = reference_encrypt(plain, 'KEY', alphabet, 'plus', (0, 4))
        for wrong in ((0,), (0, 3), (0, 5)):
            self.assertNotEqual(reference_encrypt(plain, 'KEY', alphabet, 'plus', wrong), actual)

    def test_no_ambiguous_boundary_normalization(self):
        for starts in ((), (1,), (0, 0), (0, -1), (0, 12), (0, True), [0, 4]):
            with self.assertRaises(ValueError):
                reference_encrypt('ATTACKATDAWN', 'KEY', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'plus', starts)


if __name__ == '__main__':
    unittest.main()
