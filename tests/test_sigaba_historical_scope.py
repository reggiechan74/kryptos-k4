import hashlib,json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import sigaba_csp889 as sig
import affine_digraph_crossed as crossed
import exclusion_scope_audit as scope

class HistoricalSigabaScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.d=sig.data();cls.t=sig.wheel_tables(cls.d)
    def test_all_external_vectors_both_directions(self):
        for v in self.d['vectors']:
            with self.subTest(vector=v['n']):
                self.assertEqual(sig.Machine(v,self.d,self.t).crypt(v['input']),v['output'])
                self.assertEqual(sig.Machine(v,self.d,self.t).crypt(v['output'],True),v['input'])
        self.assertEqual(len(self.d['vectors']),12)
    def test_fixture_translation_is_explicit_and_strings_unchanged(self):
        for old,new in zip(self.d['original_vector_settings'],self.d['vectors']):
            self.assertEqual(old['input'],new['input']);self.assertEqual(old['output'],new['output'])
            self.assertEqual(new['cipherrotors'],[x%10+1 for x in old['cipherrotors']])
            self.assertEqual(new['controlrotors'],[x%10+1 for x in old['controlrotors'][::-1]])
            self.assertEqual(new['controlposition'],old['controlposition'])
            self.assertEqual(new['controlorientation'],old['controlorientation'][::-1])
    def test_physical_contacts_and_independent_counter_long_trace(self):
        for q,r,layout in ((0,0,0),(25,9,1),(14,3,0)):
            self.assertEqual(sig.schedule(q,r,layout,self.t,self.d,805),sig.schedule(q,r,layout,self.t,self.d,805,True))
        for typ,n in (('large',26),('index',10)):
            for s in self.d[typ]:
                w=[sig.AZ.index(x) for x in s] if n==26 else list(map(int,s))
                for rev in (False,True):
                    for p in range(n):
                        mapping=sig.contact_oracle(w,p,rev)
                        for x in range(n):
                            y=sig.rotor(w,p,x,rev);self.assertEqual(mapping[x],y)
                            self.assertEqual(sig.rotor(w,p,y,rev,True),x)
    def test_held_state_and_raw_framing(self):
        k=sig.key(1,25,14,9);p='UNRELATEDMESSAGETESTWITHUNKNOWNGAPS'
        c=sig.Machine(k,self.d,self.t).crypt(p)
        self.assertEqual(sig.Machine(k,self.d,self.t).crypt(c,True),p)
        with self.assertRaises(ValueError):sig.Machine(k,self.d,self.t).crypt('A A')
        m=sig.Machine(k,self.d,self.t);self.assertEqual(m.crypt(p[:10])+m.crypt(p[10:]),c)
    def test_complete_actual_certificates_and_output_accounting(self):
        result=json.loads((ROOT/'results/SIGABA-CSP889-001.json').read_text());a=result['actual'];prep=sig.prepare()
        self.assertEqual(sig.evaluate(json.loads((ROOT/'data/k4.json').read_text())['ciphertext'],prep),a)
        self.assertEqual(a['raw_keys'],13520);self.assertEqual(a['first_stage_raw_survivors'],0)
        self.assertEqual(a['distinct_full_decryption_sha256'],13520)
        self.assertFalse(any(r['berlin_evaluated'] for r in a['records']))
        self.assertEqual(sum(a['mismatch_histogram'].values()),13520)
    def test_control_receipts_and_frozen_source_hashes(self):
        for name in ('SIGABA-CSP889-001-controls.json','SIGABA-CSP889-001.json','AFFINE-DIGRAPH-CROSSED-001-controls.json','AFFINE-DIGRAPH-CROSSED-001.json'):
            r=json.loads((ROOT/'results'/name).read_text())
            for p,h in r['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),h)
        r=json.loads((ROOT/'results/SIGABA-CSP889-001-controls.json').read_text())['controls']
        self.assertEqual(r['contact_and_inverse_checks'],14520)
        self.assertTrue(all(p['truth_included'] for p in r['plants']))
        self.assertTrue(r['constant_negative']);self.assertTrue(r['mutated_vector_rejected'])
    def test_crossed_exact_constraints_and_small_ring_counts(self):
        control=json.loads((ROOT/'results/AFFINE-DIGRAPH-CROSSED-001-controls.json').read_text())['controls']
        self.assertEqual(crossed.controls(),control);self.assertEqual(len(control['literal_crib_plants']),16)
        self.assertEqual(control['complete_small_ring_comparisons'],36)
        rows=json.loads((ROOT/'results/AFFINE-DIGRAPH-CROSSED-001.json').read_text())['structures']
        for row in rows:
            self.assertEqual(row['training_parameter_tuples'],'0');self.assertFalse(row['second_stage_evaluated'])
            for y,s in zip(row['training']['rhs'],row['training']['rows']):
                for f in s['fields']:crossed.verify_certificate(row['training']['matrix'],y,f)
    def test_scope_inventory_replays_and_current_receipt(self):
        actual=scope.run();saved=json.loads((ROOT/'results/EXCLUSION-SCOPE-AUDIT-001.json').read_text())
        self.assertEqual(actual,saved);self.assertEqual(len(saved['canonical_entries']),57)
        self.assertEqual(len(set(x['id'] for x in saved['canonical_entries'])),57)
        self.assertTrue(saved['fresh_analytical_replay']['structural_receipt_exact_match'])
        for d in saved['documents']:
            self.assertEqual(hashlib.sha256((ROOT/d['path']).read_bytes()).hexdigest(),d['sha256'])
        reg=json.loads((ROOT/'results/HYPOTHESIS-REGISTER-005.json').read_text())
        for p,h in reg['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),h)
