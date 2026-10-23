import hashlib,itertools,json,math,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import nonrotor_structural as nr
import sigaba_joint_feasibility as joint
import exclusion_scope_audit as scope

class JointNonrotorTests(unittest.TestCase):
    def test_exact_index_quotient_and_resource_classification(self):
        saved=json.loads((ROOT/'results/SIGABA-JOINT-FEASIBILITY-003.json').read_text());fresh=joint.run()
        for key in ('index_position_tuples','distinct_magnet_functions','connected_digit_functions','class_multiplicities','classes_sha256','allowed_mask_relaxation_class_counts','control_start_tuples','moving_control_cycle_states','two_layout_quotient_controller_descriptions','raw_full_machine_start_descriptions','K4_evaluations','status'):
            self.assertEqual(saved[key],fresh[key])
        self.assertEqual(sum(int(k)*v for k,v in saved['class_multiplicities'].items()),100000)
        self.assertEqual(sum(saved['class_multiplicities'].values()),66058)
        self.assertEqual(sum(saved['allowed_mask_relaxation_class_counts'].values()),66058)
        self.assertFalse(saved['projection_is_lower_bound']);self.assertEqual(saved['K4_evaluations'],0)
    def test_cyclic_invariant_all_toy_keys_and_zero_shift(self):
        for n in (2,3,4,5):
            for w in itertools.permutations(range(n)):
                for shift in range(n):
                    out=[nr.cyclic(w,p,shift) for p in range(n)]
                    self.assertEqual(sum(x==p for p,x in enumerate(out)),n if shift==0 else 0)
        r=json.loads((ROOT/'results/NONROTOR-STRUCTURAL-004.json').read_text())['actual']
        self.assertEqual(r['disc_keys_enumerated'],0);self.assertTrue(r['cyclic_disc_analytical_witnesses'])
        for w in r['cyclic_disc_analytical_witnesses']:
            self.assertEqual((w['fixed_position']-1)//25,(w['changed_position']-1)//25)
            self.assertEqual(w['fixed_plain'],w['fixed_cipher']);self.assertNotEqual(w['changed_plain'],w['changed_cipher'])
    def test_rejected_table_is_not_silently_repaired(self):
        r=json.loads((ROOT/'data/m94-source-quality.json').read_text());self.assertEqual(len(r['source_disc_strings']),25)
        self.assertEqual([x['disc'] for x in r['invalid_rows']],[5,25]);self.assertFalse(r['admitted_as_crypto_key_inventory']);self.assertFalse(r['repairs_performed']);self.assertFalse(r['known_answer_validation_completed'])
        self.assertEqual(r['invalid_rows'][0]['missing'],['Y']);self.assertEqual(r['invalid_rows'][1]['missing'],['H'])
    def test_complete_function_set_controls_and_inverse(self):
        r=json.loads((ROOT/'results/NONROTOR-STRUCTURAL-004-controls.json').read_text())['controls'];self.assertEqual(nr.controls(),r)
        self.assertEqual(len(r['tiny_complete_function_set_comparisons']),12);self.assertEqual(len(r['literal_crib_plants']),16)
        self.assertEqual(r['full_pair_roundtrips'],10816);self.assertTrue(all(p['truth_included'] for p in r['literal_crib_plants']))
    def test_unknown_partner_branches_have_exact_marginals(self):
        q=4;f=[0,1,0,2];g=[1,1,3,0];p=[1,2,3,0];c=[]
        for i in (0,2):c.extend(nr.encrypt_pair(p[i],p[i+1],f,g,q))
        known={0:p[0],3:p[3]};s=nr.infer(nr.pairs(c,known,1),q)
        self.assertTrue(nr.contains(s['branches'],f,g));domains=nr.domains(list(zip(c[::2],c[1::2])),s['branches'],q)
        for i,v in known.items():self.assertEqual(domains[i],[v])
        brute=[]
        for ff,gg in itertools.product(itertools.product(range(q),repeat=q),repeat=2):
            if nr.contains(s['branches'],ff,gg):brute.append((ff,gg))
        self.assertEqual(int(s['key_count']),len(brute));self.assertGreater(len(brute),1)
    def test_actual_staging_and_public_nonfit_prediction(self):
        r=json.loads((ROOT/'results/NONROTOR-STRUCTURAL-004.json').read_text())['actual'];self.assertEqual(json.loads(json.dumps(nr.actual())),r)
        rows=r['feistel_structures'];self.assertEqual(len(rows),8)
        self.assertEqual(sum(x['second_stage_evaluated'] for x in rows),4)
        for row in rows:
            self.assertEqual(row['all_crib_compatible_keys'],'0')
            if row['training']['key_count']!='0':
                self.assertEqual(int(row['training']['key_count']),26**39)
                self.assertEqual([p['position'] for p in row['training_forced_Berlin_letters']],[68])
                self.assertNotEqual(row['training_forced_Berlin_letters'][0]['predicted'],'I')
            else:self.assertIsNone(row['all_cribs'])
    def test_independent_certificates_and_source_hashes(self):
        source=ROOT/'experiments/nonrotor_structural_oracle.mjs';raw=subprocess.check_output(['/opt/homebrew/bin/node',str(source)])
        oracle=json.loads(raw);self.assertEqual(oracle,json.loads((ROOT/'results/NONROTOR-STRUCTURAL-004-independent.json').read_text()))
        native=json.loads((ROOT/'results/NONROTOR-STRUCTURAL-004.json').read_text())['actual']['feistel_structures']
        for a,b in zip(native,oracle['structures']):
            stage='all_cribs' if a['second_stage_evaluated'] else 'training';self.assertEqual(a[stage]['contradictions'][0],b[stage]['contradiction'])
        for name in ('NONROTOR-STRUCTURAL-004.json','NONROTOR-STRUCTURAL-004-controls.json','SIGABA-JOINT-FEASIBILITY-003.json'):
            r=json.loads((ROOT/'results'/name).read_text())
            for p,h in r['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),h)
    def test_current_scope_has_no_false_joint_exclusion(self):
        saved=json.loads((ROOT/'results/EXCLUSION-SCOPE-AUDIT-003.json').read_text());self.assertEqual(scope.run()['fresh_analytical_replay'],saved['fresh_analytical_replay'])
        self.assertEqual(len(saved['canonical_entries']),58)
        records={r['id']:r for r in saved['canonical_entries']};self.assertIn('budget-unresolved',records['H-SIGABA']['unexcluded_scope'])
        self.assertEqual(records['H-M94-CYCLIC']['status'],'analytical exclusion');self.assertEqual(records['H-NONLINEAR-BLOCK']['status'],'narrow negative')
        reg=json.loads((ROOT/'results/HYPOTHESIS-REGISTER-007.json').read_text())
        for p,h in reg['source_sha256'].items():
            old=subprocess.check_output(['git','show','4b4d6771e0eed9429034ac4fd6434816641fa664:'+p],cwd=ROOT)
            self.assertEqual(hashlib.sha256(old).hexdigest(),h)
