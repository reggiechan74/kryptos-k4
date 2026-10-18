import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'experiments'))
from gromark_alphabet import expand, prepare, solve, verify, decrypt, encrypt
from gromark_alphabet_controls import controls
from run_gromark_alphabet import audit, SPEC, FIXTURE
from run_bounded import validated_baseline


class GromarkAlphabetTests(unittest.TestCase):
    def setUp(self):
        self.spec = json.loads((ROOT / SPEC).read_text())

    def test_independent_exhaustive_oracle_and_synthetic_plants(self):
        r = controls(self.spec)
        self.assertEqual((r['exhaustive_toy_graphs'], r['full_permutation_pairs']), (231, 9396))
        self.assertEqual(len(r['synthetic_full_alphabet_plants']), 8)

    def test_cross_component_obstruction_passes_local_filter(self):
        sat, unsat = self.spec['controls']['toy_oracle']['modulus4_fixtures']
        self.assertTrue(prepare('ABCD', unsat['edges'])['local_filter_passed'])
        bad = solve('ABCD', unsat['edges'])
        self.assertEqual(bad['feasibility'], 'unsatisfiable')
        self.assertTrue(bad['exhausted'])
        self.assertEqual(bad['reason'], 'global_offsets_exhausted')
        good = solve('ABCD', sat['edges'])
        self.assertEqual(good['feasibility'], 'satisfiable')

    def test_cycle_and_same_side_collisions(self):
        cycle = [('A', 'A', 0), ('A', 'A', 1)]
        collision = [('A', 'A', 0), ('B', 'A', 0)]
        self.assertIsNotNone(prepare('ABC', cycle)['first_cycle_conflict'])
        self.assertIsNotNone(prepare('ABC', collision)['first_same_side_collision'])
        for edges in (cycle, collision):
            self.assertEqual(solve('ABC', edges)['reason'], 'local_filter_rejected')

    def test_empty_and_unobserved_symbols_complete_to_bijections(self):
        for edges in ([], [('A', 'A', 0)]):
            result = solve('ABC', edges)
            w = result['witness']
            self.assertTrue(verify('ABC', edges, w['plain_alphabet'], w['cipher_alphabet']))
            self.assertEqual(w['plain_alphabet'], 'ABC')
            self.assertEqual(w['cipher_alphabet'], 'ABC')

    def test_resource_caps_are_unresolved_not_unsatisfiable(self):
        fixture = self.spec['controls']['toy_oracle']['modulus4_fixtures'][0]
        r = solve('ABCD', fixture['edges'], max_states=0)
        self.assertEqual(r['feasibility'], 'unresolved')
        self.assertFalse(r['exhausted'])
        with self.assertRaises(TimeoutError):
            solve('ABC', [], limit=-1)

    def test_invalid_inputs_and_hand_stream(self):
        for args in [(1, [0], [1, 2], 3), (10, [10, 1], [1, 2], 3),
                     (10, [1, 2], [1, 1], 3), (10, [1, 2], [1, 3], 3),
                     (10, [1, 2], [1, 2], 1)]:
            with self.assertRaises(ValueError):
                expand(*args)
        for alphabet, edges in [('A', []), ('ABA', []), ('ABC', [('Z', 'A', 0)]),
                                ('ABC', [('A', 'A', 3)]), ('ABC', [('A', 'A', True)])]:
            with self.assertRaises(ValueError):
                prepare(alphabet, edges)
        self.assertEqual(expand(10, [1, 2], [1, 2], 10), [1, 2, 3, 5, 8, 3, 1, 4, 5, 9])

    def test_source_tuple_and_independently_supplied_witness(self):
        data = validated_baseline(ROOT / 'data/k4.json')
        fixture = json.loads((ROOT / FIXTURE).read_text())
        r = audit(data, self.spec, fixture)
        self.assertEqual(r['feasibility'], 'satisfiable')
        self.assertEqual((r['graph']['observed_nodes'], r['graph']['edges'], r['graph']['component_count']), (27, 24, 5))
        edges = [(e['plain'], e['cipher'], e['key']) for e in r['known_edges']]
        # Supplied after specification, never used to initialize the solver.
        pa = 'OCIBDFGLJRMSPQUVETWKNXYHZA'
        ca = 'FKTMGNQABLCZDPEHYRIVJSOUWX'
        self.assertTrue(verify('ABCDEFGHIJKLMNOPQRSTUVWXYZ', edges, pa, ca))
        plain = decrypt(data['ciphertext'], r['stream'], pa, ca)
        self.assertEqual(plain[21:34], 'EASTNORTHEAST')
        self.assertEqual(plain[63:74], 'BERLINCLOCK')
        self.assertEqual(encrypt(plain, r['stream'], pa, ca), data['ciphertext'])


if __name__ == '__main__':
    unittest.main()
