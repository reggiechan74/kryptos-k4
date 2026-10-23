import itertools
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'experiments'))
from route_key_graph import solve_graph


class RouteKeyGraphTests(unittest.TestCase):
    def test_isolates_and_parallel_edges(self):
        r = solve_graph(18, [])
        self.assertEqual(r['component_count'], 18)
        self.assertEqual(r['exact_key_assignments'], 26 ** 18)
        r = solve_graph(4, [dict(u=0, v=2, delta=3), dict(u=0, v=2, delta=3)])
        self.assertTrue(r['compatible'])
        self.assertEqual(r['component_count'], 3)
        self.assertEqual(r['independent_cycle_checks'], 1)
        bad = solve_graph(4, [dict(u=0, v=2, delta=3), dict(u=0, v=2, delta=4)])
        self.assertFalse(bad['compatible'])
        self.assertEqual(bad['exact_key_assignments'], 0)

    def test_cycle_certificate_is_direct_modular_sum(self):
        edges = [dict(u=0, v=2, delta=1), dict(u=1, v=2, delta=2),
                 dict(u=1, v=3, delta=3), dict(u=0, v=3, delta=4)]
        r = solve_graph(4, edges)
        self.assertFalse(r['compatible'])
        w = r['first_conflict']
        closing = edges[w['closing_edge_index']]
        node = closing['u']
        total = 0
        for step in w['tree_path']:
            self.assertEqual(step['source'], node)
            edge = edges[step['edge_index']]
            expected = edge['delta'] if (step['source'], step['target']) == (edge['u'], edge['v']) else -edge['delta']
            self.assertEqual(step['potential_difference_mod'], expected % 26)
            total += expected
            node = step['target']
        self.assertEqual(node, closing['v'])
        self.assertEqual(total % 26, w['implied_delta'])
        self.assertEqual((total - closing['delta']) % 26, w['residual'])
        self.assertNotEqual(w['residual'], 0)

    def test_solution_counts_against_exhaustive_assignments(self):
        for edges in ([], [dict(u=0, v=2, delta=1)],
                      [dict(u=0, v=2, delta=1), dict(u=1, v=2, delta=2)],
                      [dict(u=0, v=2, delta=1), dict(u=0, v=2, delta=2)]):
            r = solve_graph(3, edges, modulus=3)
            exact = sum(all((x[e['u']] - x[e['v']]) % 3 == e['delta'] for e in edges)
                        for x in itertools.product(range(3), repeat=3))
            self.assertEqual(exact, r['exact_key_assignments'])

    def test_component_join_spends_one_offset(self):
        before = solve_graph(4, [dict(u=0, v=2, delta=1), dict(u=1, v=3, delta=2)])
        after = solve_graph(4, [dict(u=0, v=2, delta=1), dict(u=1, v=3, delta=2), dict(u=0, v=3, delta=7)])
        self.assertNotEqual(before['component_labels'][0], before['component_labels'][3])
        self.assertEqual(before['exact_key_assignments'], 26 * after['exact_key_assignments'])
        self.assertEqual(before['independent_cycle_checks'], after['independent_cycle_checks'])


if __name__ == '__main__':
    unittest.main()
