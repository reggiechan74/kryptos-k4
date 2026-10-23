import hashlib,json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import feistel_symmetry as symmetry
import feistel_three as three
import tree_state_support as tree
import exclusion_scope_audit as audit

def read(name):return json.loads((ROOT/'results'/name).read_text())
def normalized(value):return json.loads(json.dumps(value))

class FeistelTreeExtensions(unittest.TestCase):
    def test_nonalias_certificates_are_local_function_contradictions(self):
        r=read('FEISTEL-SYMMETRY-005-controls.json')['alias_audit'];labels={x['id']:x for x in symmetry.labels()}
        self.assertEqual(len(r['nonalias_certificates']),120);self.assertFalse(r['unresolved_comparisons'])
        pairs=set()
        for cert in r['nonalias_certificates']:
            pairs.add(tuple(sorted((cert['source'],cert['target']))));observations=[]
            for w in cert['witness_pairs']:
                self.assertEqual(symmetry.pairmap(w['physical_input'],labels[cert['source']],cert['F'],cert['G']),w['physical_output'])
                observations.extend(symmetry.rows(w['physical_output'],dict(enumerate(w['physical_input'])),labels[cert['target']],1))
            function=cert['contradiction']['function'];arguments=[];values=[]
            for o in observations:
                arguments.append(o['R'] if function=='F' else o['X'])
                values.append(((o['X']-o['L']) if function=='F' else (o['Y']-o['R']))%26)
            self.assertEqual(arguments[0],arguments[1]);self.assertNotEqual(values[0],values[1])
        self.assertEqual(len(pairs),120)
        for w in r['across_origin_endpoint_witnesses']:
            f,g=symmetry.probes()[w['probe']];label=labels[w['source_label']]
            self.assertEqual(symmetry.pairmap(w['physical_input_pair'],label,f,g),w['physical_output_pair'])
            self.assertNotEqual(w['physical_input_pair'][0],w['physical_output_pair'][0])
        self.assertEqual(len(r['across_origin_endpoint_witnesses']),16)
    def test_wrapped_plants_and_staged_actual_replay(self):
        self.assertEqual(normalized(symmetry.controls()),read('FEISTEL-SYMMETRY-005-controls.json')['controls'])
        r=read('FEISTEL-SYMMETRY-005.json')['actual'];self.assertEqual(normalized(symmetry.actual({'all_32_proved_distinct':True})),r)
        self.assertTrue(r['old_eight_skipped']);self.assertEqual(len(r['new_records']),24)
        self.assertEqual(sum(x['second_stage_evaluated'] for x in r['new_records']),12)
        self.assertTrue(all(x['compatible_keys']=='0' for x in r['new_records']))
    def test_three_round_complete_small_system_controls(self):
        controls=three.controls();self.assertEqual(normalized(controls),read('FEISTEL-THREE-005-controls.json')['controls'])
        self.assertEqual(len(controls['full_small_function_enumerations']),8)
        self.assertEqual(len(controls['weighted_mod4_full_F_H_enumerations']),5)
        self.assertEqual(len(controls['singleton_weight_independent_enumerations']),16)
        self.assertEqual(len(controls['literal_crib_plants']),4)
    def test_three_round_gauge_duplicate_scope_and_budget(self):
        rows=[dict(L=0,R=1,X=1,Y=2,positions=[1,2])]
        a=three.count(rows,3);b=three.count(rows*2,3)
        self.assertEqual(a['raw_key_count'],b['raw_key_count']);self.assertEqual(int(a['raw_key_count']),3*int(a['gauge_fixed_key_count']))
        self.assertEqual(three.count([],3)['raw_key_count'],str(3**9))
        with self.assertRaises(ValueError):three.count([dict(L=0,R=None,X=1,Y=2,positions=[1,2])],3)
        limited=three.count(rows,3,cap=0);self.assertFalse(limited['completed']);self.assertIsNone(limited['raw_key_count']);self.assertEqual(limited['status'],'budget_unresolved')
    def test_three_round_independent_exact_counter(self):
        fresh=json.loads(subprocess.check_output(['/opt/homebrew/bin/node',str(ROOT/'experiments/feistel_three_oracle.mjs')]))
        self.assertEqual(fresh,read('FEISTEL-THREE-005-independent.json'));self.assertEqual(len(fresh['controls']),6)
        for a,b in zip(read('FEISTEL-THREE-005.json')['actual'],fresh['records']):
            self.assertEqual(a['input_alphabet'],b['input_alphabet']);self.assertEqual(a['output_alphabet'],b['output_alphabet'])
            for stage in ('training','all_cribs'):
                for key in ('raw_key_count','gauge_fixed_key_count','core_assignments','free_F_H_entries'):self.assertEqual(a[stage][key],b[stage][key])
    def test_full_plaintext_ambiguity_is_verified_not_inferred_from_key_count(self):
        d=json.loads((ROOT/'data/k4.json').read_text());known={i:p for crib in d['cribs'] for i,p in enumerate(crib['plaintext'],crib['start']-1)}
        for r in read('FEISTEL-THREE-005.json')['actual']:
            self.assertGreater(int(r['all_cribs']['raw_key_count']),10**75)
            self.assertEqual(r['all_cribs']['free_F_H_entries'],30);self.assertEqual(r['all_cribs']['core_assignments'],26)
            self.assertEqual(len(r['plaintext_witnesses']),2);plaintexts=[]
            for w in r['plaintext_witnesses']:
                p=three.crypt(d['ciphertext'],w['key'],r['input_alphabet'],r['output_alphabet'],True);plaintexts.append(p)
                self.assertEqual(p,w['plaintext']);self.assertEqual(len(p),97)
                self.assertTrue(all(p[i]==c for i,c in known.items()))
                self.assertEqual(three.crypt(p,w['key'],r['input_alphabet'],r['output_alphabet']),d['ciphertext'])
            self.assertNotEqual(*plaintexts);self.assertEqual(r['independently_unseen_plaintext_checks'],0)
    def test_tree_all_local_states_and_complete_toy_controls(self):
        self.assertEqual(normalized(tree.controls()),read('TREE-STATE-SUPPORT-006-controls.json')['controls'])
        actual=read('TREE-STATE-SUPPORT-006.json')['actual'];self.assertEqual(normalized(tree.actual()),actual);self.assertEqual(len(actual),4)
        for r in actual:
            self.assertTrue(r['global_key_count_not_computed']);self.assertTrue(r['local_counts_not_multiplied'])
            for window in r['local_windows']:
                self.assertFalse(window['compatible']);self.assertEqual(window['local_start_state_count'],'0')
                first,second=[window['contradiction'][k] for k in ('first','second')]
                if first['initial_slot']==second['initial_slot']:self.assertNotEqual(first['ciphertext'],second['ciphertext'])
                else:self.assertEqual(first['ciphertext'],second['ciphertext'])
    def test_current_receipts_pin_inputs(self):
        for n in ('FEISTEL-SYMMETRY-005','FEISTEL-SYMMETRY-005-controls','FEISTEL-THREE-005','FEISTEL-THREE-005-controls','TREE-STATE-SUPPORT-006','TREE-STATE-SUPPORT-006-controls'):
            hashes=read(n+'.json')['source_sha256'];self.assertIn('data/k4.json',hashes)
            for p,h in hashes.items():self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),h)
    def test_current_register_and_exclusion_receipt(self):
        r=read('EXCLUSION-SCOPE-AUDIT-004.json');self.assertEqual(audit.run()['fresh_analytical_replay'],r['fresh_analytical_replay'])
        entries={x['id']:x for x in r['canonical_entries']};self.assertEqual(len(entries),60)
        self.assertEqual(entries['H-FEISTEL-2ROUND']['status'],'analytical exclusion')
        self.assertEqual(entries['H-FEISTEL-3ROUND']['status'],'non-identifiable')
        self.assertEqual(entries['H-NONLINEAR-BLOCK']['status'],'non-identifiable')
