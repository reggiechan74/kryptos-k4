import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'experiments'))
from autokey_constraints import analyze, transform
from autokey_constraint_controls import controls
from run_autokey_constraints import audit, SPEC
from run_bounded import validated_baseline
from structural_checks import known_pairs


class AutokeyConstraintTests(unittest.TestCase):
    def setUp(self):
        self.data = validated_baseline(ROOT / 'data/k4.json')
        self.spec = json.loads((ROOT / SPEC).read_text())
        self.known = {i: p for i, _, p in known_pairs(self.data)}

    def test_independent_synthetic_and_exhaustive_toy_oracles(self):
        r = controls(list(self.spec['alphabets'].values()))
        self.assertEqual(r['synthetic_roundtrips_and_planted_positives'], 1152)
        self.assertEqual(r['planted_negative_rejections'], 732)
        self.assertEqual(r['vacuous_mutations_still_compatible'], 420)
        self.assertEqual((r['oracle_cases'], r['toy_primer_decryptions']), (5220, 40536))

    def test_complete_audit_matches_independently_supplied_lag_sets(self):
        r = audit(self.data, self.spec)
        self.assertEqual(r['tested_cases'], 1152)
        self.assertEqual(r['classification_counts'], {'contradicted': 732, 'compatible_but_underdetermined': 420})
        self.assertEqual(r['untested_cases'], 0)
        self.assertEqual(r['compatible_with_positive_consistency_checks'], 0)
        for group in r['groups']:
            expected = list(range(1, 27)) + list(range(30, 53)) if group['feedback'] == 'plaintext' else list(range(1, 74))
            self.assertEqual(group['contradicted_lags'], expected)
            self.assertEqual(group['compatible_underdetermined_lags'], [L for L in range(1, 97) if L not in expected])
            self.assertEqual(group['vacuous_lags'], group['compatible_underdetermined_lags'])
        for record in r['records']:
            L = record['lag']
            anchored = (len({i % L for i in self.known}) if record['feedback'] == 'plaintext'
                        else sum(i < L for i in self.known))
            self.assertEqual(record['independent_consistency_checks'], 24 - anchored)
            self.assertEqual(record['free_primer_symbols_if_compatible'], L - anchored)

    def test_plaintext_lag26_propagates_through_unknown_position48(self):
        self.assertFalse(any(i - 26 in self.known for i in self.known))
        r = analyze(self.data['ciphertext'], self.known, self.spec['alphabets']['AZ'], 'plus', 'plaintext', 26)
        self.assertEqual(r['independent_consistency_checks'], 1)
        self.assertEqual(r['classification'], 'contradicted')
        w = r['first_conflict']
        self.assertEqual(w['known_positions_one_based'], [22, 74])
        self.assertEqual(w['chain_positions_between_knowns_one_based'], [22, 48, 74])
        self.assertEqual(w['predicted_plaintext_at_known_position'], 'P')
        self.assertEqual(w['confirmed_plaintext'], 'K')

    def test_ciphertext_lag73_checks_last_crib_but74_is_vacuous(self):
        r73 = analyze(self.data['ciphertext'], self.known, self.spec['alphabets']['AZ'], 'plus', 'ciphertext', 73)
        r74 = analyze(self.data['ciphertext'], self.known, self.spec['alphabets']['AZ'], 'plus', 'ciphertext', 74)
        self.assertEqual(r73['independent_consistency_checks'], 1)
        self.assertEqual(r73['first_conflict']['position_one_based'], 74)
        self.assertEqual(r74['independent_consistency_checks'], 0)
        self.assertEqual(r74['classification'], 'compatible_but_underdetermined')
        self.assertEqual(r74['exact_solution_count'], {'base': 26, 'exponent': 50})

    def test_empty_single_full_and_whole_message_primers(self):
        for feedback in ('plaintext', 'ciphertext'):
            empty = analyze('ABCD', {}, 'ABCD', 'plus', feedback, 4)
            single = analyze('ABCD', {1: 'A'}, 'ABCD', 'plus', feedback, 4)
            full = analyze('ABCD', {i: c for i, c in enumerate('BCDA')}, 'ABCD', 'plus', feedback, 4)
            self.assertEqual(empty['exact_solution_count'], {'base': 4, 'exponent': 4})
            self.assertEqual(single['exact_solution_count'], {'base': 4, 'exponent': 3})
            self.assertEqual(full['classification'], 'compatible_fully_constrained')
            self.assertEqual(full['exact_solution_count'], {'base': 4, 'exponent': 0})
            for lag in (1, 3, 4):
                cipher = transform('ABCD', 'B' * lag, 'ABCD', 'minus', feedback)
                self.assertEqual(transform(cipher, 'B' * lag, 'ABCD', 'minus', feedback, True), 'ABCD')

    def test_invalid_inputs_are_not_normalized(self):
        base = ['ABCD', {}, 'ABCD', 'plus', 'plaintext', 1]
        for field, value in [(0, ''), (0, 'AbCD'), (1, {True: 'A'}), (1, {-1: 'A'}),
                             (1, {4: 'A'}), (1, {0: 'AA'}), (1, {0: 'Z'}),
                             (2, 'ABCA'), (3, 'unknown'), (4, 'backward'),
                             (5, 0), (5, 5), (5, True)]:
            args = list(base)
            args[field] = value
            with self.assertRaises(ValueError):
                analyze(*args)
        with self.assertRaises(ValueError):
            transform('ABCD', '', 'ABCD', 'plus', 'plaintext')

    def test_deadlines_fail_before_new_work(self):
        with self.assertRaises(TimeoutError):
            controls(list(self.spec['alphabets'].values()), -1)
        with self.assertRaises(TimeoutError):
            audit(self.data, self.spec, -1)


if __name__ == '__main__':
    unittest.main()
