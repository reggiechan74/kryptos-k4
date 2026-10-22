from pathlib import Path
import sys
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'experiments'))
from k3_clock_routes import (A, analyze_sandwich, analyze_single, composite_route, controls,
                            preflight, scan_single, single_transform, up_order)


class K3ClockRouteTests(unittest.TestCase):
    def test_k3_all336_and_prior_exact_skip_receipts(self):
        pre = preflight()
        self.assertTrue(pre['k3_all336_known_answer'])
        self.assertTrue(pre['k3_existing_position_permutation'])
        self.assertTrue(pre['independent_matrix_oracle'])
        self.assertEqual(pre['previous_catalogue_size'], 66)
        self.assertEqual(pre['new_single_cases'], 372)
        skips = [c for c in pre['formal_single_cases'] if c['status'] == 'skipped_prior_exact_equivalent']
        self.assertEqual(len(skips), 16)
        self.assertEqual({x['route_id'] for c in skips for x in c['prior_equivalents']}, {'R036', 'R040', 'R038', 'R042'})
        self.assertTrue(all(not x['previous_compatible'] for c in skips for x in c['prior_equivalents']))

    def test_all_planted_models_and_exhaustive_toy_counts(self):
        r = controls(preflight())
        self.assertEqual(r, dict(single_planted_roundtrips=372, single_mutated_rejections=372,
                                 sandwich_planted_roundtrips=2, sandwich_mutated_cycle_rejections=2,
                                 exhaustive_graph_cases=5, toy_key_assignments=1215, explicit_graph_controls=4))

    def test_hand_indexed_modular_layer_orders(self):
        pi = [2, 0, 3, 1]
        self.assertEqual(single_transform('KRYP', [1, 2], pi, 'sub_then_route'), 'PROP')
        self.assertEqual(single_transform('KRYP', [1, 2], pi, 'route_then_sub'), 'PYTP')
        for order, cipher in [('sub_then_route', 'PROP'), ('route_then_sub', 'PYTP')]:
            self.assertEqual(single_transform(cipher, [1, 2], pi, order, True), 'KRYP')
            record = analyze_single(cipher, dict(enumerate('KRYP')), pi, 2, order)
            self.assertTrue(record['compatible'])
            self.assertEqual(record['key'], [1, 2])
        self.assertEqual(up_order(8, 3), [6, 3, 0, 7, 4, 1, 5, 2])

    def test_frozen_training_never_predicts_across_components(self):
        known = {i: 'K' for i in list(range(21, 34)) + list(range(63, 74))}
        for m, n in ((8, 10), (10, 8)):
            r = analyze_sandwich('K' * 97, known, composite_route(97), m, n)
            self.assertTrue(r['compatible'])
            self.assertGreaterEqual(r['c_train'], 5)
            self.assertEqual(r['exact_key_assignments'], 26 ** r['c_all24'])
            self.assertEqual(r['distinct_compatible_plaintexts'], 26 ** (r['c_all24'] - r['d_full']))
            self.assertEqual(r['joint_independent_heldout_checks'], 11 - (r['c_train'] - r['c_all24']))
            for p in r['heldout']:
                if not p['endpoints_connected_in_training']:
                    self.assertFalse(p['predictable_from_frozen_training'])
                    self.assertIsNone(p['predicted_delta'])
                    self.assertIsNone(p['matches'])
            if r['remaining_plaintext_relevant_offsets'] > 0:
                self.assertNotIn('plaintext', r)

    def test_expired_deadline_prevents_cipher_scan(self):
        with self.assertRaises(TimeoutError):
            scan_single('K' * 97, {}, preflight(), 'F1', time.monotonic() - 1)


if __name__ == '__main__':
    unittest.main()
