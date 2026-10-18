import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'experiments'))
from gromark_identifiability import difference, check_counterexample
from gromark_identifiability_controls import controls, all_pairs
from run_gromark_identifiability import audit, context, SPEC, PRIOR_SPEC, POOL
from run_bounded import validated_baseline


class GromarkIdentifiabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = validated_baseline(ROOT / 'data/k4.json')
        cls.spec = json.loads((ROOT / SPEC).read_text())
        cls.pool = json.loads((ROOT / POOL).read_text())['witnesses']
        cls.result = audit(cls.data, cls.spec, cls.pool)

    def test_independent_exhaustive_difference_oracle(self):
        r = controls(json.loads((ROOT / PRIOR_SPEC).read_text()))
        self.assertEqual((r['base_graphs'], r['base_permutation_pairs']), (231, 9396))
        self.assertEqual((r['toy_difference_queries'], r['query_permutation_pairs']), (515, 27052))
        self.assertTrue(r['marginal_variability_does_not_imply_joint_freedom'])

    def test_final_map_matches_independently_supplied_conditional_predictions(self):
        self.assertEqual(self.result['classification_counts'], {'forced': 10, 'variable': 63, 'unresolved': 0})
        actual = {r['position_one_based']: r['letter'] for r in self.result['forced_model_conditional_letters']}
        self.assertEqual(actual, {12: 'A', 38: 'E', 42: 'O', 44: 'S', 47: 'L', 61: 'B', 62: 'E', 79: 'L', 81: 'I', 86: 'I'})
        protected = set(range(22, 35)) | set(range(64, 75))
        self.assertEqual({r['position_one_based'] for r in self.result['records']}, set(range(1, 98)) - protected)
        self.assertEqual(self.result['queries_attempted'], 73)

    def test_every_variable_record_has_a_checked_complete_counterexample(self):
        reference, stream, known, edges = context(self.data, self.spec, self.pool)
        for r in self.result['records']:
            if r['classification'] != 'variable':
                self.assertTrue(r['certificate']['proof_complete'])
                continue
            i = r['position_one_based'] - 1
            self.assertTrue(check_counterexample('ABCDEFGHIJKLMNOPQRSTUVWXYZ', edges, reference,
                                                r['counterexample'], self.data['ciphertext'][i], stream[i]))
            self.assertTrue(all(r['acceptance'].values()))

    def test_transitive_forced_positions_are_not_just_repeated_pairs(self):
        _, stream, known, _ = context(self.data, self.spec, self.pool)
        for position in (38, 86):
            r = next(r for r in self.result['records'] if r['position_one_based'] == position)
            self.assertEqual(r['method'], 'same_component_invariant')
            i = position - 1
            self.assertFalse(any(c == self.data['ciphertext'][i] and stream[j] == stream[i] for j, c, _ in known))

    def test_global_forced_single_unused_symbols_and_caps(self):
        ref = {'plain_alphabet': 'AB', 'cipher_alphabet': 'AB'}
        edges = [('A', 'A', 0)]
        r = difference('AB', edges, ref, 'B', 0)
        self.assertEqual(r['classification'], 'forced')
        self.assertEqual(r['method'], 'exhausted_difference_CSP')
        self.assertTrue(r['certificate']['missing_endpoints_included'])
        self.assertEqual(difference('AB', edges, ref, 'B', 0, max_states=0)['classification'], 'unresolved')
        self.assertEqual(difference('AB', edges, ref, 'B', 0, limit=0)['classification'], 'unresolved')

    def test_invalid_references_and_false_counterexamples_are_rejected(self):
        ref = {'plain_alphabet': 'ABC', 'cipher_alphabet': 'ABC'}
        self.assertFalse(check_counterexample('ABC', [], ref, ref, 'A', 0))
        for bad in ({'plain_alphabet': 'AAC', 'cipher_alphabet': 'ABC'},
                    {'plain_alphabet': 'ABC', 'cipher_alphabet': 'ACB'}):
            with self.assertRaises(ValueError):
                difference('ABC', [('B', 'B', 0)], bad, 'A', 0)
        for cipher, key in [('Z', 0), ('A', True), ('A', 3)]:
            with self.assertRaises(ValueError):
                difference('ABC', [], ref, cipher, key)

    def test_aggregate_budget_preserves_unresolved_records(self):
        r = audit(self.data, self.spec, self.pool, limit=-1)
        self.assertEqual(r['classification_counts'], {'forced': 0, 'variable': 0, 'unresolved': 73})
        self.assertEqual(r['queries_attempted'], 0)
        self.assertTrue(all(not x['query_attempted'] for x in r['records']))

    def test_marginally_variable_does_not_mean_jointly_free(self):
        ref = {'plain_alphabet': 'AB', 'cipher_alphabet': 'AB'}
        for cipher in 'AB':
            self.assertEqual(difference('AB', [], ref, cipher, 0)['classification'], 'variable')
        self.assertFalse(any(p[c.index('A')] == p[c.index('B')] == 'A' for p, c, _ in all_pairs('AB', [])))


if __name__ == '__main__':
    unittest.main()
