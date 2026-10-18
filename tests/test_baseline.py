"""Catch transcription drift, off-by-one indexing, and malformed baselines."""
import copy
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))
from check_baseline import DATA_PATH, one_based_slice, validate


class BaselineTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(DATA_PATH.read_text(encoding="utf-8"))

    def test_baseline(self):
        self.assertEqual(len(validate(self.data)), 97)

    def test_crib_ciphertext_anchors(self):
        text = self.data["ciphertext"]
        self.assertEqual(one_based_slice(text, 22, 34), "FLRVQQPRNGKSS")
        self.assertEqual(one_based_slice(text, 64, 74), "NYPVTTMZFPK")

    def test_boundary_indexing(self):
        self.assertEqual(one_based_slice("ABCDE", 1, 1), "A")
        self.assertEqual(one_based_slice("ABCDE", 5, 5), "E")
        self.assertEqual(one_based_slice("ABCDE", 1, 5), "ABCDE")

    def test_invalid_ranges(self):
        for start, end in [(0, 1), (1, 6), (3, 2), (-1, 2)]:
            with self.subTest(start=start, end=end), self.assertRaises(ValueError):
                one_based_slice("ABCDE", start, end)

    def test_rejects_corrupt_length_and_alphabet(self):
        text = self.data["ciphertext"]
        for bad in [text[:-1], text + "A", "a" + text[1:], "É" + text[1:], " " + text[1:]]:
            data = copy.deepcopy(self.data)
            data["ciphertext"] = bad
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                validate(data)

    def test_rejects_crib_drift(self):
        for field, bad in [("start", 21), ("end", 35), ("plaintext", "EASTNORTHEASX")]:
            data = copy.deepcopy(self.data)
            data["cribs"][0][field] = bad
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate(data)


if __name__ == "__main__":
    unittest.main()
