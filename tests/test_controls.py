import json
from pathlib import Path
import random
import sys
from string import ascii_uppercase
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'experiments'))
from ciphers import KRYPTOS, vigenere, rotate_clockwise, k3_permutation, permute
from check_controls import run


class ControlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / 'data/controls.json').read_text())

    def test_full_known_answers(self):
        self.assertEqual(len(run()['checks']), 4)

    def test_independent_opening_vector(self):
        self.assertEqual(vigenere('BETWEENSUB', 'PALIMPSEST'), 'EMUFPHZLRF')
        self.assertEqual(vigenere('BETWEENSUB', 'PALIMPSEST', ascii_uppercase), 'QEEEQTFWMU')

    def test_physical_transcription_boundaries(self):
        panels = self.data['transcription_panels']
        self.assertEqual(''.join(panels['upper_rows']), self.data['k1']['ciphertext'] + self.data['k2_as_inscribed']['ciphertext'])
        lower = ''.join(panels['lower_rows'])
        k4 = json.loads((ROOT / 'data/k4.json').read_text())['ciphertext']
        self.assertEqual(lower, self.data['k3']['ciphertext'] + '?' + k4)

    def test_correction_is_exactly_one_insertion(self):
        original = self.data['k2_as_inscribed']['ciphertext']
        corrected = self.data['k2_restored_s']['ciphertext']
        self.assertEqual(corrected, original[:-8] + 'S' + original[-8:])
        self.assertEqual(self.data['k2_restored_s']['plaintext'][:-9], self.data['k2_as_inscribed']['plaintext'][:-8])
        self.assertIn('IQLUSION', self.data['k1']['plaintext'])
        self.assertIn('UNDERGRUUND', self.data['k2_restored_s']['plaintext'])
        self.assertIn('DESPARATLY', self.data['k3']['plaintext'])

    def test_question_marks_do_not_advance_key(self):
        self.assertEqual(vigenere('BET?WEENSUB', 'PALIMPSEST'), 'EMU?FPHZLRF')
        self.assertEqual(vigenere('???', 'ABSCISSA'), '???')

    def test_rotation_is_clockwise(self):
        self.assertEqual(rotate_clockwise('ABCDEF', 2, 3), 'DAEBFC')
        self.assertEqual(rotate_clockwise('DAEBFC', 3, 2), 'FEDCBA')

    def test_k3_every_position_is_bijective(self):
        p = k3_permutation()
        self.assertEqual(sorted(p), list(range(336)))
        labels = [chr(0x1000 + i) for i in range(336)]
        text = ''.join(labels)
        self.assertEqual(permute(permute(text, p), p, inverse=True), text)

    def test_synthetic_round_trips(self):
        rng = random.Random(20261018)
        for alphabet in [ascii_uppercase, KRYPTOS]:
            for n in [1, 2, 26, 63, 97, 369]:
                for _ in range(10):
                    text = ''.join(rng.choice(ascii_uppercase + '?') for _ in range(n))
                    key = ''.join(rng.choice(ascii_uppercase) for _ in range(8))
                    self.assertEqual(vigenere(vigenere(text, key, alphabet), key, alphabet, decrypt=True), text)

    def test_invalid_inputs_fail_explicitly(self):
        for text, key, alphabet in [('abc','A',KRYPTOS), ('A B','A',KRYPTOS), ('AB','',KRYPTOS), ('AB','A','A'*26)]:
            with self.assertRaises(ValueError): vigenere(text, key, alphabet)
        with self.assertRaises(ValueError): rotate_clockwise('ABCDE', 2, 3)
        with self.assertRaises(ValueError): permute('AB', [0, 0])


if __name__ == '__main__': unittest.main()
