from pathlib import Path
import hashlib
import json
import subprocess
import unittest

ROOT=Path(__file__).resolve().parents[1]


class AutonomousArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base=ROOT/'results/autonomous-recurrence-runs'
        pointer=json.loads((base/'latest.json').read_text());cls.folder=base/pointer['run_id']
        cls.manifest=json.loads((cls.folder/'manifest.json').read_text())
        cls.result=json.loads((cls.folder/'AUTONOMOUS-RECURRENCE-001.json').read_text())

    def test_frozen_provenance_and_all_algebraic_contradictions(self):
        r,m=self.result,self.manifest
        self.assertEqual(m['status'],'completed')
        b=(self.folder/'AUTONOMOUS-RECURRENCE-001.json').read_bytes()
        self.assertEqual(hashlib.sha256(b).hexdigest(),m['artifacts']['AUTONOMOUS-RECURRENCE-001.json']['sha256'])
        subprocess.run(['git','merge-base','--is-ancestor',r['spec_commit'],r['code_commit']],cwd=ROOT,check=True)
        for name,expected in r['file_sha256'].items():
            raw=subprocess.check_output(['git','show',r['code_commit']+':'+name],cwd=ROOT)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),expected)
        self.assertEqual(len(r['structures']),20)
        for row in r['structures']:
            self.assertEqual(row['status'],'impossible')
            self.assertEqual(row['training_coefficient_count'],'0')
            self.assertIsNone(row['training_prediction_sets'])
            for f in row['coefficient_space']['fields']:
                if f['consistent']:continue
                weights=f['contradiction']['equation_weights'];p=f['prime']
                for col in range(f['variables']):
                    self.assertEqual(sum(w*a[col] for w,a in zip(weights,row['training_matrix']))%p,0)
                self.assertNotEqual(sum(w*b for w,b in zip(weights,row['training_rhs']))%p,0)

    def test_identical_parity_contexts_and_affine_order_six_ranks(self):
        r=self.result
        for ctx in r['parity_contexts']:
            v=ctx['training_key_values'];w=ctx['parity_witness']
            states=[[v[i-22]%2 for i in range(lo,hi+1)] for lo,hi in w['windows_one_based']]
            self.assertEqual(states[0],states[1])
            self.assertNotEqual(*w['target_parities'])
            for order in range(2,7):self.assertEqual(states[0][-order:],states[1][-order:])
        rows=[x for x in r['structures'] if x['order']==6 and x['constant_mode']=='fitted']
        self.assertEqual(len(rows),2)
        for x in rows:
            self.assertEqual([(f['rank'],f['augmented_rank']) for f in x['coefficient_space']['fields']],[(6,7),(7,7)])
        self.assertEqual(r['budget_used'],{'coefficients':0,'union_terms':0})

    def test_literal_controls_and_singular_prefixes_retained(self):
        c=self.result['controls']
        self.assertEqual(c['literal_plant_count'],80)
        self.assertEqual(c['small_ring_count'],12)
        self.assertEqual(c['ambiguous_planted_prefixes'],60)
        for plant in c['literal_plants']:
            self.assertEqual(plant['plaintext'][21:34],'EASTNORTHEAST')
            self.assertEqual(plant['plaintext'][63:74],'BERLINCLOCK')
            self.assertTrue(plant['coefficient_set_contains_truth'])
            self.assertTrue(plant['prefix_set_contains_truth'])
        self.assertEqual(c['startup_alias_example'],{'reachable_seeds':26,'globally_reduced_seeds':1})
        self.assertTrue(c['unreachable_internal_fit_rejected'])


    def test_independent_oracle_exact_source_output_and_ranks(self):
        root=ROOT/'independent/2026-10-22/autonomous-recurrence'
        self.assertEqual(hashlib.sha256((root/'k4_recurrence_oracle.js').read_bytes()).hexdigest(),'a2a4b1f6ba6bbd0826a769f354090c224539f2b1bc5c86e56284992818f933e3')
        self.assertEqual(hashlib.sha256((root/'results.json').read_bytes()).hexdigest(),'d7dce355c9ba01adab6fe1901fa965f4d58f3edbc1e71396e8d1c5c31128e763')
        other=json.loads((root/'results.json').read_text())
        self.assertEqual(other['controls']['checks'],231)
        self.assertEqual(other['controls']['failures'],[])
        self.assertEqual(other['conclusion']['berlinEvaluations'],0)
        self.assertEqual(other['conclusion']['budgetUnresolved'],0)
        for ours,theirs in zip(self.result['structures'],other['structures']):
            self.assertEqual(ours['order'],theirs['order'])
            self.assertEqual(ours['constant_mode']=='fitted',theirs['affine'])
            for f,label in zip(ours['coefficient_space']['fields'],['field2','field13']):
                self.assertEqual((f['rank'],f['augmented_rank'],f['cardinality']),(theirs[label]['rank'],theirs[label]['augmentedRank'],theirs[label]['solutionCount']))


if __name__=='__main__':unittest.main()
