from pathlib import Path
import sys
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'experiments'))
from split_coordinate import ALPHABETS, catalogue, configurations, controls, function_signature, route_order, scan, transform


class SplitCoordinateTests(unittest.TestCase):
    def test_all_planted_and_independent_oracle_controls(self):
        self.assertEqual(controls(), dict(planted_roundtrips=32, planted_crib_recoveries=32,
                                         mutated_rejections=32, oracle_comparisons=64,
                                         source_pair_grid_checks=21632, ragged_route_checks=24,
                                         equivalence_checks=3))

    def test_ragged_route_hand_answer(self):
        self.assertEqual(route_order(8, 3), [0, 3, 6, 1, 4, 7, 2, 5])
        self.assertEqual(route_order(8, 3, True), [0, 3, 6, 1, 4, 7, 2, 5])
        self.assertEqual(route_order(10, 3), [0, 3, 6, 9, 1, 4, 7, 2, 5, 8])
        self.assertEqual(route_order(10, 3, True), [0, 4, 7, 1, 5, 8, 2, 6, 9, 3])

    def test_coordinate_repairing_can_change_letter_histogram(self):
        cfg = dict(alphabet=ALPHABETS[0], grid_rows=2, grid_columns=13,
                   row_width=2, column_width=3, row_inverse=False, column_inverse=False)
        plain = 'ANBOCPDQ'
        cipher = transform(plain, cfg)
        self.assertNotEqual(sorted(plain), sorted(cipher))
        self.assertEqual(transform(cipher, cfg, True), plain)

    def test_catalogue_and_exact_signatures(self):
        cases, groups = catalogue()
        self.assertEqual(len(cases), 32)
        self.assertEqual(sum(len(v) for v in groups.values()), 32)
        self.assertEqual(len({tuple(c.items()) for c in configurations()}), 32)
        self.assertEqual(len({c['function_signature_sha256'] for c in cases}), len(groups))
        self.assertTrue(all(c['case_id'] in groups[c['canonical_case_id']] for c in cases))

    def test_deadline_rejects_work(self):
        cases, groups = catalogue()
        with self.assertRaises(TimeoutError):
            scan('A' * 97, {}, cases, groups, time.monotonic() - 1)


if __name__ == '__main__':
    unittest.main()
