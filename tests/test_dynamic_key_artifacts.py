"""Verify the saved negative result independently of the search evaluator."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / 'results/dynamic-key-runs/20261022T120128Z-c15ba5ffeb55479490d2be553daf60f0'


class DynamicArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads((RUN / 'DYNAMIC-KEY-001.json').read_text())
        cls.data = json.loads((ROOT / 'data/k4.json').read_text())

    def test_hashes_and_chronology(self):
        manifest = json.loads((RUN / 'manifest.json').read_text())
        self.assertEqual(manifest['status'], 'completed')
        for name, meta in manifest['artifacts'].items():
            raw = (RUN / name).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), meta['sha256'])
            self.assertEqual(len(raw), meta['bytes'])
        for name, digest in self.r['file_sha256'].items():
            if name not in ('experiments/run_io.py','experiments/run_bounded.py'):
                self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), digest)
            committed = subprocess.check_output(['git', 'show', self.r['code_commit'] + ':' + name], cwd=ROOT)
            self.assertEqual(hashlib.sha256(committed).hexdigest(), digest)
        parent = subprocess.check_output(['git', 'rev-parse', self.r['code_commit'] + '^'], cwd=ROOT, text=True).strip()
        self.assertEqual(parent, self.r['spec_commit'])

    def test_every_rejection_has_independent_conflict(self):
        known = {c['start'] - 1 + j: letter for c in self.data['cribs'] for j, letter in enumerate(c['plaintext'])}
        cipher = self.data['ciphertext']
        self.assertEqual(len(self.r['records']), 1344)
        for r in self.r['records']:
            self.assertFalse(r['compatible'])
            w = r['first_conflict']
            requirements = []
            for position in w['positions_one_based']:
                i = position - 1
                cursor = i if r['family'] == 'progressive' else i + sum(c in r['variant'] for c in cipher[:i])
                self.assertEqual(cursor % r['period'], w['phase'])
                offset = r['variant'] * (i // r['period']) if r['family'] == 'progressive' else 0
                requirements.append((r['alphabet'].index(cipher[i]) - r['sigma'] * r['alphabet'].index(known[i]) - offset) % 26)
            self.assertEqual(requirements, w['required_keys'])
            self.assertNotEqual(*requirements)

    def test_complete_null_family_and_holdout_accounting(self):
        r = self.r
        self.assertEqual(r['model_evaluations'], 268800)
        self.assertEqual(len(r['nulls']), 199)
        for family, size in [('progressive', 1248), ('ciphertext_step', 96)]:
            records = [v for v in r['records'] if v['family'] == family]
            observed = r['observed'][family]
            self.assertEqual(len(records), size)
            self.assertEqual(max(v['best_same_data_agreements'] for v in records), observed['max_agreements'])
            self.assertEqual(sum(v['compatible'] for v in records), observed['compatible'])
            for draw in r['nulls']:
                self.assertEqual(draw[family]['models'], size)
            exceed = sum(v[family]['max_agreements'] >= observed['max_agreements'] for v in r['nulls'])
            self.assertEqual(r['tails'][family]['plus_one_conditional_tail'], (exceed + 1) / 200)
        survivors = [v for v in r['records'] if v['training_compatible']]
        self.assertEqual(len(survivors), 4)
        self.assertEqual(Counter(sum(x['matches'] is True for x in v['heldout']) for v in survivors), {0: 2, 1: 2})
        self.assertTrue(all(len(v['heldout']) == 11 and all(x['matches'] is not None for x in v['heldout']) for v in survivors))


if __name__ == '__main__':
    unittest.main()
