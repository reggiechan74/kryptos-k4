"""Independent verification of the two continuation snapshots; no new search."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
ASYM = ROOT / 'results/asymmetric-feedback-001-runs/20261022T191952Z-44bf1543c641497e82f4b948d0cd94ea'
SPLIT = ROOT / 'results/split-coordinate-001-runs/20261022T192126Z-2ff96ae3a6914cab8db6cd9c0c7ceb5c'


class ContinuationArtifacts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = json.loads((ASYM / 'ASYMMETRIC-FEEDBACK-001.json').read_text())
        cls.s = json.loads((SPLIT / 'SPLIT-COORDINATE-001.json').read_text())
        cls.baseline = json.loads((ROOT / 'data/k4.json').read_text())
        cls.known = {c['start'] - 1 + j: p for c in cls.baseline['cribs'] for j, p in enumerate(c['plaintext'])}

    def test_hashes_and_prior_specification_ancestry(self):
        for folder, result in ((ASYM, self.a), (SPLIT, self.s)):
            manifest = json.loads((folder / 'manifest.json').read_text())
            self.assertEqual(manifest['status'], 'completed')
            for name, meta in manifest['artifacts'].items():
                raw = (folder / name).read_bytes()
                self.assertEqual(hashlib.sha256(raw).hexdigest(), meta['sha256'])
                self.assertEqual(len(raw), meta['bytes'])
            for name, digest in result['file_sha256'].items():
                self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), digest)
                raw = subprocess.check_output(['git', 'show', result['code_commit'] + ':' + name], cwd=ROOT)
                self.assertEqual(hashlib.sha256(raw).hexdigest(), digest)
            subprocess.run(['git', 'merge-base', '--is-ancestor', result['spec_commit'], result['code_commit']], cwd=ROOT, check=True)
            self.assertNotEqual(result['spec_commit'], result['code_commit'])

    def test_all_asymmetric_roots_by_forward_exhaustive_lane_oracle(self):
        cipher = self.baseline['ciphertext']
        coeff = {'plus': (1, 1), 'minus': (1, -1), 'beaufort': (-1, 1)}
        self.assertEqual(len(self.a['records']), 72)
        survivor_count = 0
        for r in self.a['records']:
            ap, ac, ak = (r[k] for k in ('Ap', 'Ac', 'Ak'))
            sigma, tau = coeff[r['equation']]
            lag = r['lag']
            self.assertEqual(r['primer_parameters_before_constraints'], lag)
            self.assertEqual(r['occupied_lanes'], lag)
            self.assertEqual(r['free_lanes'], 0)
            self.assertEqual(r['independent_equality_checks'], 24 - lag)
            self.assertEqual(r['training_occupied_lanes'], lag)
            self.assertEqual(r['training_equality_checks'], 13 - lag)
            actual = {}
            for req in r['requirements']:
                i, lane = req['position_one_based'] - 1, req['lane']
                candidates = []
                for root in range(26):
                    value = ap[root]
                    for j in range(lane + lag, i + 1, lag):
                        value = ap[sigma * (ac.index(cipher[j]) - tau * ak.index(value)) % 26]
                    if value == self.known[i]:
                        candidates.append(root)
                self.assertEqual(candidates, [req['required_root']])
                self.assertEqual(req['root_to_known_positions_one_based'], list(range(lane + 1, i + 2, lag)))
                actual[i + 1] = req['required_root']
            w = r['first_conflict']
            self.assertFalse(r['compatible'])
            self.assertEqual(r['exact_solution_count'], 0)
            self.assertEqual([actual[p] for p in w['known_positions_one_based']], w['required_roots'])
            self.assertNotEqual(*w['required_roots'])
            if r['training_compatible']:
                survivor_count += 1
                roots = {v['lane']: v['required_root'] for v in r['requirements'] if 22 <= v['position_one_based'] <= 34}
                plain = [ap[roots[j]] for j in range(lag)]
                for i in range(lag, 97):
                    plain.append(ap[sigma * (ac.index(cipher[i]) - tau * ak.index(plain[i - lag])) % 26])
                for prediction in r['heldout']:
                    i = prediction['position_one_based'] - 1
                    self.assertEqual(prediction['predicted'], plain[i])
                    self.assertEqual(prediction['matches'], plain[i] == self.known[i])
                self.assertEqual(len(r['heldout']), 11)
                self.assertEqual(sum(v['matches'] for v in r['heldout']), 2)
        self.assertEqual(survivor_count, 1)

    def test_every_split_output_symbol_against_explicit_route(self):
        def route(values, width, inverse):
            order = sorted(range(len(values)), key=lambda i: (i % width, i // width))
            if inverse:
                out = [None] * len(values)
                for value, index in zip(values, order):
                    out[index] = value
                return out
            return [values[i] for i in order]
        cipher = self.baseline['ciphertext']
        self.assertEqual(len(self.s['records']), 32)
        self.assertEqual(len(self.s['equivalence_classes']), 32)
        for record in self.s['records']:
            plain = record['plaintext']
            alphabet, width = record['alphabet'], record['grid_columns']
            rows, cols = zip(*(divmod(alphabet.index(c), width) for c in plain))
            rows = route(rows, record['row_width'], record['row_inverse'])
            cols = route(cols, record['column_width'], record['column_inverse'])
            reconstructed = ''.join(alphabet[row * width + col] for row, col in zip(rows, cols))
            self.assertEqual(reconstructed, cipher)
            matches = [i + 1 for i, p in sorted(self.known.items()) if plain[i] == p]
            self.assertEqual(matches, record['matched_positions_one_based'])
            self.assertEqual(len(matches), record['matched_crib_letters'])
            self.assertEqual(record['free_parameters'], 0)
            self.assertFalse(record['all24_match'])
            self.assertEqual(record['evidence_class'], 'rejected_model_output')

    def test_null_maxima_and_complete_scope(self):
        for result, key in ((self.a, 'max_agreements'), (self.s, 'max_matches')):
            self.assertEqual(len(result['nulls']), 199)
            exceed = sum(n[key] >= result['observed'][key] for n in result['nulls'])
            self.assertEqual(exceed, result['exceedances'])
            self.assertEqual((exceed + 1) / 200, result['plus_one_conditional_tail'])
        self.assertEqual(self.a['model_evaluations'], 14400)
        self.assertTrue(all(n['models'] == 72 for n in self.a['nulls']))
        self.assertEqual(self.s['formal_model_evaluations'], 6400)
        self.assertEqual(self.s['distinct_model_evaluations'], 6400)
        self.assertTrue(all(n['distinct_models'] == 32 for n in self.s['nulls']))
        self.assertTrue(all(max(n['per_model_matches']) == n['max_matches'] for n in self.s['nulls']))
        for start, end, segment in ((22, 25, 'FLRV'), (26, 34, 'QQPRNGKSS'), (64, 69, 'NYPVTT'), (70, 74, 'MZFPK')):
            self.assertEqual(self.baseline['ciphertext'][start - 1:end], segment)


if __name__ == '__main__':
    unittest.main()
