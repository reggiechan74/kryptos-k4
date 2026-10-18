import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'experiments'))
from silk_periodic import validate_chart, transform, required_key, compatibility, controls, audit, CHART, RECEIPT
from run_bounded import validated_baseline


class SilkPeriodicTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chart = json.loads((ROOT / CHART).read_text())
        cls.receipt = json.loads((ROOT / RECEIPT).read_text())

    def test_structure_known_answers_and_toy_controls(self):
        r = controls(self.chart, self.receipt)
        self.assertEqual(r['table_cell_roundtrips'], 676)
        self.assertEqual((r['toy_roundtrips'], r['shifted_positive_checks'], r['shifted_negative_checks']), (39, 117, 117))
        self.assertEqual(r['modern_worked_example_computed'], 'ZEAAIZXQOTFL')

    def test_required_segments_and_all12exact_witnesses(self):
        r = audit(validated_baseline(ROOT / 'data/k4.json'), self.chart)
        self.assertEqual(r['required_key_segments'], ['JICEHTUFLMSXZ', 'TCUFDISXLFX'])
        self.assertTrue(r['first_segment13distinct'])
        self.assertEqual(r['compatible_periods'], [])
        self.assertEqual(r['contradicted_periods'], list(range(1, 13)))
        self.assertEqual(len(r['required_key_lookups']), 24)
        for record, witness in zip(r['period_records'], r['short_proof_witnesses']):
            p = record['period']
            self.assertEqual(record['independent_phase_comparisons'], 24 - p)
            self.assertEqual(record['first_conflict']['positions_one_based'], [22, 22 + p])
            self.assertNotEqual(*witness['required_keys'])
            self.assertEqual((witness['positions_one_based'][1] - witness['positions_one_based'][0]) % p, 0)

    def test_fixed_points_do_not_support_Enigma_exclusion(self):
        self.assertEqual(required_key('S', 'S', self.chart), 'X')
        self.assertEqual(required_key('K', 'K', self.chart), 'X')
        self.assertEqual(transform('SK', 'X', self.chart), 'SK')

    def test_every_row_has_unique_reproduced_key_lookup(self):
        alphabet = self.chart['plaintext_order']
        for p in alphabet:
            for c in alphabet:
                k = required_key(p, c, self.chart)
                self.assertEqual(transform(p, k, self.chart), c)

    def test_low_information_cases_are_not_false_rejections(self):
        r = compatibility([{'position_one_based': 100, 'required_key': 'A'}], 12)
        self.assertTrue(r['compatible'])
        self.assertEqual((r['independent_phase_comparisons'], r['unassigned_key_phases']), (0, 11))
        self.assertTrue(compatibility([], 12)['compatible'])

    def test_invalid_inputs_and_nonreciprocal_chart(self):
        for text, key in [('abc', 'A'), ('ABC', ''), ('A A', 'A'), ('ABC', '?')]:
            with self.assertRaises(ValueError):
                transform(text, key, self.chart)
        for p in (0, True, -1):
            with self.assertRaises(ValueError):
                compatibility([], p)
        bad = {'plaintext_order': 'ABC', 'key_order': 'ABC', 'columns': {'A': 'ABC', 'B': 'BCA', 'C': 'CAB'}}
        with self.assertRaises(ValueError):
            validate_chart(bad)


if __name__ == '__main__':
    unittest.main()
