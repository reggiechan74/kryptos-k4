import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'experiments'))
from clock_boundary_regression import controls, phases, transform, verify_certificates, SPEC
from run_bounded import validated_baseline


class ClockBoundaryRegressionTests(unittest.TestCase):
    def test_exact_declared_controls(self):
        spec = json.loads((ROOT / SPEC).read_text())
        result = controls(spec)
        self.assertEqual(result['primitive_cases'], 4056)
        self.assertEqual(result['independent_phase_comparisons'], 388)
        self.assertEqual(result['synthetic_97letter_roundtrips'], 24)
        self.assertEqual(result['altered_position33_negative_fixtures'], 24)

    def test_all_known_certificates(self):
        spec = json.loads((ROOT / SPEC).read_text())
        result = verify_certificates(validated_baseline(ROOT / 'data/k4.json'), spec)
        self.assertEqual(result['certificate_count'], 13)
        self.assertEqual(result['formal_cases_subsumed_analytically'], 72)
        self.assertEqual(result['candidate_keys_tested'], 0)

    def test_strict_schedule_and_deadline(self):
        for starts in ((), (0,), (1, 1), (1, 98), (1, True), [1, 22]):
            with self.assertRaises(ValueError):
                phases(97, starts)
        with self.assertRaises(TimeoutError):
            controls(json.loads((ROOT / SPEC).read_text()), -1)

    def test_reset_applies_before_start(self):
        p = phases(97, (1, 22, 64))
        self.assertEqual([p[i] for i in (0, 20, 21, 32, 62, 63, 66)], [0, 9, 0, 0, 8, 0, 3])
        self.assertEqual(transform('AAAAAAAAAAAA', 'KEY', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'plus', (1, 5, 10)), 'KEYKKEYKEKEY')


if __name__ == '__main__':
    unittest.main()
