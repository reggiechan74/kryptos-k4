"""Read-only checks of the occupied-cell run and independent simple certificates."""
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / 'results/occupied-cell-routes-001-runs/20261022T193953Z-6f4f8efe83e345168a18fdc2f134d845'
A = 'KRYPTOSABCDEFGHIJLMNQUVWXZ'


class OccupiedCellArtifacts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = json.loads((RUN / 'OCCUPIED-CELL-ROUTES-001.json').read_text())
        cls.data = json.loads((ROOT / 'data/k4.json').read_text())
        cls.known = {c['start'] - 1 + j: p for c in cls.data['cribs'] for j, p in enumerate(c['plaintext'])}

    def test_hashes_prior_specification_and_scope(self):
        r = self.result
        manifest = json.loads((RUN / 'manifest.json').read_text())
        self.assertEqual(manifest['status'], 'completed')
        for name, meta in manifest['artifacts'].items():
            raw = (RUN / name).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), meta['sha256'])
            self.assertEqual(len(raw), meta['bytes'])
        for name, digest in r['file_sha256'].items():
            self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), digest)
            raw = subprocess.check_output(['git', 'show', r['code_commit'] + ':' + name], cwd=ROOT)
            self.assertEqual(hashlib.sha256(raw).hexdigest(), digest)
        subprocess.run(['git', 'merge-base', '--is-ancestor', r['spec_commit'], r['code_commit']], cwd=ROOT, check=True)
        self.assertNotEqual(r['spec_commit'], r['code_commit'])
        self.assertEqual(r['actual_model_evaluations'], 288)
        self.assertEqual(r['nulls'], dict(status='not_needed_all_fixed_models_contradicted', draws=[]))

    def test_fixed_mask_and_full_prior_catalogue_coverage(self):
        pre = self.result['preflight']
        cells = [tuple(x) for x in pre['occupied_cells_zero_based']]
        self.assertEqual(cells[:4], [(0, c) for c in range(27, 31)])
        self.assertEqual(cells[4:], [(r, c) for r in range(1, 4) for c in range(31)])
        earlier = json.loads(gzip.decompress((ROOT / 'results/ROUTE-001.json.gz').read_bytes()))
        newer = json.loads((ROOT / 'results/k3-clock-routes-001-runs/20261022T193238Z-99bf9337176c469e9d7742f2a21f2aca/K3-CLOCK-ROUTES-001.json').read_text())
        old_routes = {tuple(r['permutation']) for r in earlier['route_catalogue'] + newer['preflight']['routes']}
        for route in pre['routes']:
            direct = sorted(range(97), key=lambda i: (route['horizontal'] * cells[i][1], route['vertical'] * cells[i][0]))
            if route['inverse']:
                direct = [direct.index(i) for i in range(97)]
            self.assertEqual(direct, route['permutation'])
            self.assertNotIn(tuple(direct), old_routes)
        self.assertEqual(pre['prior_stronger_skips'], 0)
        self.assertEqual(pre['exact_unique_new_cases'], 288)
        self.assertTrue(all(c['prior_equivalents'] == [] and c['status'] == 'new_to_test' for c in pre['cases']))

    def test_every_actual_output_symbol_and_crib_rejection(self):
        r = self.result
        routes = {x['route_id']: x['permutation'] for x in r['preflight']['routes']}
        scores, signatures = [], set()
        for record in r['records']:
            plain, pi = record['plaintext'], routes[record['route_id']]
            self.assertEqual(len(plain), 97)
            shifts = []
            for j, i in enumerate(pi):
                position = i if record['order'] == 'sub_then_route' else j
                shift = A.index(record['word'][(position + record['phase']) % len(record['word'])])
                shifts.append(shift)
                self.assertEqual(A[(A.index(plain[i]) + shift) % 26], self.data['ciphertext'][j])
            signatures.add((tuple(pi), tuple(shifts)))
            matches = [i + 1 for i, p in sorted(self.known.items()) if plain[i] == p]
            self.assertEqual(matches, record['matched_positions_one_based'])
            self.assertEqual(len(matches), record['matched_crib_letters'])
            self.assertEqual(record['fitted_parameters'], 0)
            self.assertFalse(record['all24_match'])
            self.assertEqual(record['evidence_class'], 'rejected_model_output')
            scores.append(len(matches))
        self.assertEqual(len(signatures), 288)
        self.assertEqual(scores, r['observed']['per_model_matches'])
        self.assertEqual(max(scores), 5)
        self.assertEqual(r['observed']['compatible'], 0)

    def test_independent_simple_sandwich_pairs_match_saved_equations(self):
        r = json.loads((ROOT / 'results/k3-clock-routes-001-runs/20261022T193238Z-99bf9337176c469e9d7742f2a21f2aca/K3-CLOCK-ROUTES-001.json').read_text())
        for pair, positions, values, key_indices in (([8, 10], [32, 64], [25, 18], [7, 3]),
                                                     ([10, 8], [29, 69], [4, 10], [8, 1]),
                                                     ([10, 8], [30, 70], [3, 15], [9, 7])):
            record = next(x for x in r['records']['F2'] if x['period_pair'] == pair)
            edges = [next(e for e in record['edges'] if e['plain_position_one_based'] == p) for p in positions]
            self.assertEqual([e['delta'] for e in edges], values)
            self.assertEqual((edges[0]['u'], edges[0]['v']), (edges[1]['u'], edges[1]['v']))
            self.assertEqual([edges[0]['u'], edges[0]['v'] - pair[0]], key_indices)
            self.assertNotEqual(*values)


if __name__ == '__main__':
    unittest.main()
