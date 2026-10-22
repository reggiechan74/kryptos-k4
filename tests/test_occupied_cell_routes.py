from pathlib import Path
import sys
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'experiments'))
from occupied_cell_routes import controls, mask, phased_key, preflight, route_catalogue, scan


class OccupiedCellRouteTests(unittest.TestCase):
    def test_all_planted_models_and_independent_oracles(self):
        self.assertEqual(controls(preflight()), dict(route_unique_index_oracles=8, single_symbol_roundtrips=676,
                                                   planted_full_recoveries=288, planted_crib_recoveries=288,
                                                   explicit_encoder_comparisons=288, altered_crib_rejections=288))

    def test_exact_mask_and_corner_readings(self):
        cells = mask()
        self.assertEqual(len(set(cells)), 97)
        self.assertEqual(cells[:4], [(0, 27), (0, 28), (0, 29), (0, 30)])
        self.assertEqual(cells[4], (1, 0))
        self.assertEqual(cells[-1], (3, 30))
        route = route_catalogue()[0]['permutation']
        self.assertEqual(route[:3], [4, 35, 66])
        self.assertEqual(route[81:85], [0, 31, 62, 93])
        self.assertEqual(route[-4:], [3, 34, 65, 96])

    def test_key_phases_and_fixed_coverage_counts(self):
        self.assertEqual(phased_key('ABSCISSA', 1), 'BSCISSAA')
        self.assertEqual(phased_key('ABSCISSA', 7), 'AABSCISS')
        pre = preflight()
        self.assertTrue(pre['fixture_mask_verified'])
        self.assertEqual(pre['prior_stronger_skips'], 0)
        self.assertEqual(pre['distinct_routes'], 8)
        self.assertEqual(pre['exact_unique_new_cases'], 288)
        self.assertTrue(all(c['status'] == 'new_to_test' for c in pre['cases']))

    def test_deadline_prevents_scan(self):
        with self.assertRaises(TimeoutError):
            scan('K' * 97, {}, preflight(), time.monotonic() - 1)


if __name__ == '__main__':
    unittest.main()
