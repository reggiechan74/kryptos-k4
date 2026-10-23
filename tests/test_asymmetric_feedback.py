from pathlib import Path
import sys
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'experiments'))
from asymmetric_feedback import analyze, configurations, controls, root_requirements, scan, transform


class AsymmetricFeedbackTests(unittest.TestCase):
    def test_planted_exhaustive_toy_and_shared_alphabet_controls(self):
        self.assertEqual(controls(), dict(planted_roundtrips=72, root_recoveries=72, mutated_rejections=72,
                                         exhaustive_toy_cases=108, toy_primer_decryptions=1080,
                                         same_alphabet_comparisons=24))

    def test_hand_checked_reindexing_and_unknown_intermediate(self):
        cfg = dict(Ap='ABCD', Ac='ABCD', Ak='CADB', equation='plus', lag=2)
        self.assertEqual(transform('ABCDABC', 'BD', cfg), 'DDDCADD')
        self.assertEqual(transform('DDDCADD', 'BD', cfg, True), 'ABCDABC')
        known = {2: 'C', 6: 'C'}
        result = analyze('DDDCADD', known, cfg)
        self.assertTrue(result['compatible'])
        self.assertEqual([r['required_root'] for r in result['requirements']], [0, 0])
        self.assertEqual(result['requirements'][1]['root_to_known_positions_one_based'], [1, 3, 5, 7])
        self.assertEqual(result['exact_solution_count'], 4)
        rejected = analyze('DDDCADD', {2: 'C', 6: 'D'}, cfg)
        self.assertFalse(rejected['compatible'])

    def test_formal_parameter_count_and_information_counts(self):
        cases = list(configurations())
        self.assertEqual(len(cases), 72)
        self.assertEqual(len({tuple(c.items()) for c in cases}), 72)
        for cfg in cases:
            self.assertTrue(9 <= cfg['lag'] <= 12)
            self.assertGreater(len({cfg[k] for k in ('Ap', 'Ac', 'Ak')}), 1)
        cfg = dict(Ap='ABCD', Ac='CADB', Ak='ABCD', equation='beaufort', lag=2)
        empty = analyze('ABCDACB', {}, cfg)
        self.assertEqual(empty['exact_solution_count'], 16)
        self.assertEqual(empty['independent_equality_checks'], 0)
        self.assertFalse(empty['candidate_gate'])

    def test_deadline_stops_scan_before_work(self):
        with self.assertRaises(TimeoutError):
            scan('A' * 97, {}, time.monotonic() - 1)

    def test_validation_rejects_incompatible_alphabets(self):
        cfg = dict(Ap='ABCD', Ac='ABCC', Ak='ABCD', equation='plus', lag=2)
        with self.assertRaises(ValueError):
            root_requirements('ABCD', {}, cfg)


if __name__ == '__main__':
    unittest.main()
