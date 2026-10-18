"""Direct aligned reflector-model boundary; no rotor or key search."""
import json
from pathlib import Path
import random
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DirectEnigmaBoundaryTests(unittest.TestCase):
    def test_position_74_is_a_confirmed_fixed_point(self):
        data = json.loads((ROOT / 'data/k4.json').read_text())
        crib = next(c for c in data['cribs'] if c['start'] <= 74 <= c['end'])
        self.assertEqual(crib['plaintext'][74 - crib['start']], 'K')
        self.assertEqual(data['ciphertext'][74 - 1], 'K')

    def test_conjugation_preserves_no_fixed_points(self):
        # Toy paired reflector, not historical wiring or an Enigma simulation.
        reflector = [i ^ 1 for i in range(26)]
        rng = random.Random(20261018)
        for _ in range(26):
            outward = list(range(26))
            rng.shuffle(outward)
            inverse = [0] * 26
            for i, value in enumerate(outward):
                inverse[value] = i
            encrypted = [inverse[reflector[outward[i]]] for i in range(26)]
            self.assertTrue(all(i != value for i, value in enumerate(encrypted)))
            self.assertEqual(sorted(encrypted), list(range(26)))


if __name__ == '__main__':
    unittest.main()
