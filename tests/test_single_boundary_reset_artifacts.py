from pathlib import Path
import hashlib
import itertools
import json
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments'))
from single_boundary_reset import ALPHABETS,BOUNDARIES,configurations,recency_oracle


class SingleResetArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base=ROOT/'results/single-boundary-reset-runs'
        pointer=json.loads((base/'latest.json').read_text());cls.folder=base/pointer['run_id']
        cls.manifest=json.loads((cls.folder/'manifest.json').read_text())
        cls.result=json.loads((cls.folder/'SINGLE-BOUNDARY-RESET-001.json').read_text())

    def test_complete_snapshot_hashes_and_frozen_chronology(self):
        r,m=self.result,self.manifest
        self.assertEqual(m['status'],'completed')
        self.assertTrue(all(x['status']=='completed' for x in m['jobs']))
        b=(self.folder/'SINGLE-BOUNDARY-RESET-001.json').read_bytes()
        self.assertEqual(hashlib.sha256(b).hexdigest(),m['artifacts']['SINGLE-BOUNDARY-RESET-001.json']['sha256'])
        subprocess.run(['git','merge-base','--is-ancestor',r['spec_commit'],r['code_commit']],cwd=ROOT,check=True)
        for name,expected in r['file_sha256'].items():
            data=subprocess.check_output(['git','show',r['code_commit']+':'+name],cwd=ROOT)
            self.assertEqual(hashlib.sha256(data).hexdigest(),expected)

    def test_full_mtf_outputs_independent_recency_and_truth_sets(self):
        r=self.result;k=json.loads((ROOT/'data/k4.json').read_text())
        self.assertEqual(len(r['mtf']['per_case']),388)
        for (cfg,b),row in zip(itertools.product(configurations(),BOUNDARIES),r['mtf']['per_case']):
            self.assertEqual(recency_oracle(k['ciphertext'],cfg,b),row['plaintext'])
            self.assertFalse(row['training_compatible'])
            self.assertEqual(row['first_contradiction']['position_one_based'],22)
        summary=r['controls']['summary']
        self.assertEqual(summary['truth_included'],32)
        self.assertEqual(summary['unique_plaintexts'],16)
        self.assertEqual(summary['ambiguous_plaintexts'],16)
        for plant in r['controls']['mtf_plants']:
            self.assertIn(plant['true_case'],plant['selection']['compatible_case_ids'])
            self.assertIn(hashlib.sha256(plant['plaintext'].encode()).hexdigest(),plant['selection']['compatible_plaintext_sha256'])
        self.assertTrue(any(x['selection']['unforced_noncrib_positions'] for x in r['controls']['mtf_plants']))

    def test_parity_and_phase_counts_without_inflating_new_coverage(self):
        r=self.result
        for block in r['recurrence']['results']:
            self.assertEqual(block['coefficient_triples_checked'],26**3)
            self.assertEqual(block['triples_after_internal_training_filter'],0)
            for row in block['schedule_proofs']:
                x,y=row['parity_witness'];a,b=x['triple'],y['triple']
                self.assertEqual((a[0]%2,a[1]%2),(b[0]%2,b[1]%2))
                self.assertNotEqual(a[2]%2,b[2]%2)
                self.assertNotEqual(x['to_position_one_based'],row['boundary_before_one_based'])
                self.assertNotEqual(y['to_position_one_based'],row['boundary_before_one_based'])
        p=r['periodic']
        self.assertEqual(p['raw_shapes'],6984)
        self.assertEqual(p['canonical_shapes'],4*sum(97-96//period for period in range(1,13)))
        self.assertEqual(p['covered_canonical_baselines'],48)
        self.assertEqual(p['new_canonical_schedules'],3428)
        self.assertEqual(sum(len(x['aliases']) for x in p['per_case']),6984)
        self.assertTrue(all(not x['training_compatible'] for x in p['per_case']))
        self.assertEqual(p['canonical_compatible'],0)


    def test_independent_archive_replay_and_scoped_analytic_corollary(self):
        base=ROOT/'independent/2026-10-22/single-boundary-reset'
        r=json.loads((base/'TRANSFER-RECEIPT.json').read_text())
        for name,record in r['original_files'].items():
            data=(base/name).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(),record['sha256'])
        d=json.loads((base/'results.json').read_text())
        self.assertEqual(d['summary']['mtf_survivors'],0)
        self.assertEqual(d['summary']['recurrence_surviving_parameter_settings'],0)
        self.assertIsNone(d['summary']['forced_positions'])
        self.assertEqual(d['summary']['periodic_surviving_settings'],0)
        rows=d['analytic_consequence_fixed_mtf_arbitrary_same_state_resets']
        self.assertEqual([x['with_reset_before27'] for x in rows],['Q','U','J','Q'])
        self.assertTrue(all('O' not in [x['without_reset_before27'],x['with_reset_before27']] for x in rows))
        replay=json.loads((ROOT/'results/SINGLE-RESET-INDEPENDENT-LOCAL-REPLAY-001.json').read_text())
        self.assertTrue(replay['all_results_equal'])


if __name__=='__main__':unittest.main()
