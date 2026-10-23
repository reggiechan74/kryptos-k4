"""Independent symbol-by-symbol checks of the two fixed-pilot result snapshots."""
import hashlib
import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
RUNS = [
    ('asymmetric-primer-runs', '20261022T120817Z-ef4199fc397e4bd9bc6ca2fb3bfdc2e2', 'ASYMMETRIC-PRIMER-001', 6),
    ('plaintext-step-runs', '20261022T121001Z-38f7134c1bc3445ea7bf00efc70d2e11', 'PLAINTEXT-STEP-001', 12),
]
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
KR = 'KRYPTOSABCDEFGHIJLMNQUVWXZ'


class FixedPilotArtifacts(unittest.TestCase):
    def load_runs(self):
        for family, runid, label, count in RUNS:
            path = ROOT / 'results' / family / runid
            yield path, json.loads((path / (label + '.json')).read_text()), count

    def test_saved_hashes_and_committed_chronology(self):
        for path, r, _ in self.load_runs():
            manifest = json.loads((path / 'manifest.json').read_text())
            self.assertEqual(manifest['status'], 'completed')
            for name, meta in manifest['artifacts'].items():
                raw = (path / name).read_bytes()
                self.assertEqual(hashlib.sha256(raw).hexdigest(), meta['sha256'])
                self.assertEqual(len(raw), meta['bytes'])
            for name, digest in r['file_sha256'].items():
                self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), digest)
                committed = subprocess.check_output(['git', 'show', r['code_commit'] + ':' + name], cwd=ROOT)
                self.assertEqual(hashlib.sha256(committed).hexdigest(), digest)
            parent = subprocess.check_output(['git', 'rev-parse', r['code_commit'] + '^'], cwd=ROOT, text=True).strip()
            self.assertEqual(parent, r['spec_commit'])

    def test_every_saved_symbol_and_crib_gate(self):
        data = json.loads((ROOT / 'data/k4.json').read_text())
        known = {c['start'] - 1 + j: p for c in data['cribs'] for j, p in enumerate(c['plaintext'])}
        cipher = data['ciphertext']
        for _, r, size in self.load_runs():
            self.assertEqual(len(r['observed']), size)
            for record in r['observed']:
                plain = record['plaintext']
                self.assertEqual(len(plain), 97)
                cursor = 0
                for i, p in enumerate(plain):
                    if r['id'] == 'ASYMMETRIC-PRIMER-001':
                        ap, ac, ak = ({'AZ': AZ, 'KR': KR}[record[k]] for k in ('Ap', 'Ac', 'Ak'))
                        key = 'PALIMPSEST'[i] if i < 10 else plain[i - 10]
                        expected = ac[(ap.index(p) + ak.index(key)) % 26]
                    else:
                        a = record['alphabet']
                        key = record['word'][cursor % len(record['word'])]
                        expected = a[(a.index(p) + a.index(key)) % 26]
                        cursor += 2 if p in record['trigger'] else 1
                    self.assertEqual(cipher[i], expected)
                matches = [i + 1 for i, p in sorted(known.items()) if plain[i] == p]
                self.assertEqual(matches, record['matched_positions_one_based'])
                self.assertEqual(len(matches), record['matched_crib_letters'])
                self.assertEqual(record['free_parameters'], 0)
                self.assertFalse(record['all24_match'])
                self.assertEqual(record['evidence_class'], 'rejected_model_output')
                self.assertTrue(record['full97_regeneration'])

    def test_null_and_acceptance_accounting(self):
        for _, r, size in self.load_runs():
            self.assertEqual(len(r['nulls']), 199)
            self.assertEqual(r['model_evaluations'], size * 200)
            best = max(v['matched_crib_letters'] for v in r['observed'])
            self.assertEqual(best, r['best_matches'])
            for draw in r['nulls']:
                self.assertEqual(len(draw['per_model_matches']), size)
                self.assertEqual(max(draw['per_model_matches']), draw['max_matches'])
                self.assertEqual(sum(n == 24 for n in draw['per_model_matches']), draw['candidates'])
            exceed = sum(d['max_matches'] >= best for d in r['nulls'])
            self.assertEqual(exceed, r['exceedances'])
            self.assertEqual((exceed + 1) / 200, r['plus_one_conditional_tail'])


if __name__ == '__main__':
    unittest.main()
