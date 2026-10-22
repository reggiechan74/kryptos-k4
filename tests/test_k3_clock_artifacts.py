"""Verify exact certificates and prior-domain skip receipts without rescanning."""
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / 'results/k3-clock-routes-001-runs/20261022T193238Z-99bf9337176c469e9d7742f2a21f2aca'
A = 'KRYPTOSABCDEFGHIJLMNQUVWXZ'


def components(vertex_count, edges):
    parent = list(range(vertex_count))
    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x
    for u, v in edges:
        parent[find(u)] = find(v)
    labels = [find(x) for x in range(vertex_count)]
    return labels, len(set(labels))


class K3ClockArtifacts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = json.loads((RUN / 'K3-CLOCK-ROUTES-001.json').read_text())
        cls.data = json.loads((ROOT / 'data/k4.json').read_text())
        cls.known = {c['start'] - 1 + j: p for c in cls.data['cribs'] for j, p in enumerate(c['plaintext'])}
        cls.routes = {r['route_id']: r['permutation'] for r in cls.result['preflight']['routes']}

    def test_hashes_chronology_and_completed_scope(self):
        r = self.result
        manifest = json.loads((RUN / 'manifest.json').read_text())
        self.assertEqual(manifest['status'], 'completed')
        for name, meta in manifest['artifacts'].items():
            raw = (RUN / name).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), meta['sha256'])
            self.assertEqual(len(raw), meta['bytes'])
        for name, digest in r['file_sha256'].items():
            raw = (ROOT / name).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), digest)
            committed = subprocess.check_output(['git', 'show', r['code_commit'] + ':' + name], cwd=ROOT)
            self.assertEqual(hashlib.sha256(committed).hexdigest(), digest)
        subprocess.run(['git', 'merge-base', '--is-ancestor', r['spec_commit'], r['code_commit']], cwd=ROOT, check=True)
        self.assertNotEqual(r['spec_commit'], r['code_commit'])
        self.assertEqual(r['actual_new_models'], 374)
        self.assertEqual(r['skipped_prior_exact'], 16)
        self.assertEqual(r['raw_structures'], 390)
        self.assertTrue(all(x['compatible'] == 0 for x in r['families'].values()))
        self.assertTrue(all(x['status'] == 'not_needed_all_models_contradicted' and x['draws'] == [] for x in r['nulls'].values()))

    def test_every_single_key_rejection_uses_exact_crib_positions(self):
        r, cipher = self.result, self.data['ciphertext']
        records = r['records']['F1'] + r['records']['F3']
        self.assertEqual(len(records), 372)
        for case in records:
            pi = self.routes[case['route_id']]
            inverse = {source: j for j, source in enumerate(pi)}
            self.assertFalse(case['compatible'])
            self.assertEqual(case['exact_key_assignments'], 0)
            values = {}
            for req in case['requirements']:
                i, j = req['plain_position_one_based'] - 1, req['cipher_position_one_based'] - 1
                self.assertEqual(j, inverse[i])
                phase = (i if case['order'] == 'sub_then_route' else j) % case['period']
                value = (A.index(cipher[j]) - A.index(self.known[i])) % 26
                self.assertEqual((phase, value), (req['phase'], req['key_value']))
                values[i + 1] = (phase, value)
            w = case['first_conflict']
            first, second = w['conflicting_requirements']
            self.assertEqual(values[first['plain_position_one_based']][0], values[second['plain_position_one_based']][0])
            self.assertNotEqual(values[first['plain_position_one_based']][1], values[second['plain_position_one_based']][1])
            self.assertFalse(case['training_compatible'])
            self.assertNotIn('plaintext', case)

    def test_graph_components_and_cycle_certificates(self):
        cipher = self.data['ciphertext']
        pi = self.routes['K3-COMPOSITE-97']
        inverse = {source: j for j, source in enumerate(pi)}
        for record in self.result['records']['F2']:
            m, n = record['period_pair']
            for edge in record['edges']:
                i = edge['plain_position_one_based'] - 1
                j = inverse[i]
                self.assertEqual(edge['cipher_position_one_based'], j + 1)
                self.assertEqual((edge['u'], edge['v']), (i % m, m + j % n))
                self.assertEqual(edge['delta'], (A.index(cipher[j]) - A.index(self.known[i])) % 26)
            train_labels, c_train = components(18, [(e['u'], e['v']) for e in record['training_edges']])
            _, c_all = components(18, [(e['u'], e['v']) for e in record['edges']])
            _, d_full = components(18, [(i % m, m + j % n) for j, i in enumerate(pi)])
            self.assertEqual((c_train, c_all, d_full), (5, 1, 1))
            self.assertEqual((record['c_train'], record['c_all24'], record['d_full']), (c_train, c_all, d_full))
            self.assertEqual(record['training_graph']['independent_cycle_checks'], 0)
            self.assertEqual(record['training_plaintext_relevant_offsets'], 4)
            self.assertEqual(record['joint_independent_heldout_checks'], 7)
            self.assertEqual(record['remaining_plaintext_relevant_offsets'], 0)
            self.assertEqual(record['exact_key_assignments'], 0)
            self.assertEqual(record['distinct_compatible_plaintexts'], 0)
            self.assertNotIn('plaintext', record)
            w = record['all_crib_graph']['first_conflict']
            closing = record['edges'][w['closing_edge_index']]
            node, implied = closing['u'], 0
            for step in w['tree_path']:
                self.assertEqual(step['source'], node)
                edge = record['edges'][step['edge_index']]
                if (step['source'], step['target']) == (edge['u'], edge['v']):
                    value = edge['delta']
                else:
                    self.assertEqual((step['target'], step['source']), (edge['u'], edge['v']))
                    value = -edge['delta']
                implied += value
                self.assertEqual(step['potential_difference_mod'], value % 26)
                node = step['target']
            self.assertEqual(node, closing['v'])
            self.assertEqual(implied % 26, w['implied_delta'])
            self.assertEqual((implied - closing['delta']) % 26, w['residual'])
            self.assertNotEqual(w['residual'], 0)
            for prediction in record['heldout']:
                edge = next(e for e in record['edges'] if e['plain_position_one_based'] == prediction['plain_position_one_based'])
                connected = train_labels[edge['u']] == train_labels[edge['v']]
                self.assertEqual(prediction['predictable_from_frozen_training'], connected)
                if not connected:
                    self.assertIsNone(prediction['predicted_delta'])
                    self.assertIsNone(prediction['matches'])
                else:
                    self.assertFalse(prediction['matches'])

    def test_skips_include_full_prior_key_domain_and_layer_order(self):
        old = json.loads(gzip.decompress((ROOT / 'results/ROUTE-001.json.gz').read_bytes()))
        old_routes = {r['id']: r['permutation'] for r in old['route_catalogue']}
        spec = (ROOT / 'research/BOUNDED-SPEC.md').read_text()
        self.assertIn('periods\n1–16', spec)
        self.assertIn('substitution before/after the route', spec)
        self.assertIn('Derive each key-phase constraint', spec)
        skips = [c for c in self.result['preflight']['formal_single_cases'] if c['status'] == 'skipped_prior_exact_equivalent']
        self.assertEqual(len(skips), 16)
        for case in skips:
            self.assertEqual(case['family'], 'F3')
            for prior in case['prior_equivalents']:
                self.assertEqual(self.routes[case['route_id']], old_routes[prior['route_id']])
                self.assertEqual(case['period'], prior['period'])
                self.assertEqual(case['order'], prior['order'])
                self.assertFalse(prior['previous_compatible'])
                self.assertFalse(any(s['route'] == prior['route_id'] and s['period'] == prior['period']
                                     and s['alphabet'] == 'KRYPTOS' and s['equation'] == 'plus'
                                     and s['order'] == prior['order'] for s in old['survivors']))


if __name__ == '__main__':
    unittest.main()
