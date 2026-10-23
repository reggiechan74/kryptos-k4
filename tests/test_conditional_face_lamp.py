import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments'))
from conditional_face_lamp import (face_cases,face_fit,literal_plant,direct_face_encode,ALPHABETS,
    model_encrypt,model_decrypt,lamp_bits,lamp_inverse,lamp_code,lamp_oracle,lamp_streams,
    lamp_crypt,parity_certificate,stream_overlap)

class ConditionalCipherTests(unittest.TestCase):
    def test_face_complete_first_key_and_independent_encoder(self):
        p=literal_plant()
        for r in face_cases():
            key=[(7*j+3)%26 for j in range(r['period'])];a=ALPHABETS[r['alphabet']]
            c=model_encrypt(p,key,a,r['equation'],r['permutation'],r['order'])
            self.assertEqual(c,direct_face_encode(p,r,key))
            fitted=face_fit(c,r)
            self.assertTrue(fitted['consistent']);self.assertEqual(fitted['key'],key)
            self.assertEqual(fitted['unfitted_entries'],0)
            self.assertEqual(model_decrypt(c,key,a,r['equation'],r['permutation'],r['order']),p)

    def test_face_training_conflict_is_explicit_not_free_key_fill(self):
        r=next(r for r in face_cases() if r['period']==1)
        p=literal_plant();key=[3];c=list(direct_face_encode(p,r,key));j=r['permutation'].index(21);a=ALPHABETS[r['alphabet']]
        c[j]=a[(a.index(c[j])+1)%26]
        fit=face_fit(''.join(c),r)
        self.assertFalse(fit['consistent']);self.assertIsNone(fit['key'])
        self.assertNotEqual(fit['first_conflict']['first']['required_key'],fit['first_conflict']['second']['required_key'])

    def test_display_hand_vectors_boundaries_and_invalids(self):
        self.assertEqual(lamp_code(0,0),0);self.assertEqual(lamp_code(0,1),1)
        self.assertEqual(lamp_code(1,0),1<<20)
        self.assertEqual(lamp_code(5,0),1<<9)
        self.assertEqual(lamp_code(60,0),1<<5)
        expected=tuple(map(int,'1'+'1111'+'1110'+'11111111111'+'1111'))
        self.assertEqual(lamp_bits(1439,1),expected)
        self.assertEqual(lamp_inverse(expected),(1439,1))
        for t,p in ((0,0),(59,1),(60,1),(719,0),(1439,1)):
            self.assertEqual(lamp_inverse(lamp_bits(t,p)),(t,p))
            self.assertEqual(lamp_code(t,p),lamp_oracle(t,p))
        for b in ((0,)*23,(0,0,1)+(0,)*21,(0,)+(1,)*8+(0,)*15):
            with self.assertRaises(ValueError):lamp_inverse(b)
        with self.assertRaises(ValueError):lamp_bits(1440,0)

    def test_full_lamp_states_stream_aliases_and_parity(self):
        rows=lamp_streams()
        self.assertEqual(len(rows),2832)
        self.assertEqual(sum(len(r['aliases']) for r in rows),2880)
        self.assertEqual(len({tuple(r['key']) for r in rows}),len(rows))
        for r in rows:
            for alias in r['aliases']:
                self.assertEqual(r['key'],[lamp_oracle((alias['start_minute']+i)%1440,alias['indicator'])%26 for i in range(97)])
                self.assertEqual({k%2 for k in r['key']},{alias['indicator']})
        self.assertFalse(any(stream_overlap(r['key'])['progressive_p1_to12_d0_to25'] for r in rows))

    def test_fixed_cipher_roundtrips_and_incompatible_parity_control(self):
        p=literal_plant();key=[lamp_code((1438+i)%1440,1)%26 for i in range(97)]
        for a in ALPHABETS.values():
            for eq in ('plus','beaufort'):
                c=lamp_crypt(p,key,a,eq);self.assertEqual(lamp_crypt(c,key,a,eq,True),p)
                self.assertTrue(parity_certificate(c,a,eq)['constant_parity_possible'])
                bad=parity_certificate('A'*97,a,eq)
                self.assertFalse(bad['constant_parity_possible'])
                self.assertEqual(len(set(bad['witness']['required_parities'])),2)

    def test_control_receipt_preserves_full_selector_ambiguity(self):
        r=json.loads((ROOT/'results/CONDITIONAL-FACE-LAMP-001-controls.json').read_text())
        self.assertEqual(len(r['face']['literal_plants']),92)
        self.assertTrue(all(p['truth_retained'] for p in r['face']['literal_plants']))
        self.assertTrue(any(p['distinct_full_plaintexts']>1 for p in r['face']['literal_plants']))
        self.assertEqual(len(r['lamp']['literal_plants']),32)
        self.assertTrue(all(p['truth_retained'] and p['raw_descriptions_accounted']==11520 for p in r['lamp']['literal_plants']))

    def test_actual_row_predictions_and_lamp_exact_certificates(self):
        import hashlib
        r=json.loads((ROOT/'results/CONDITIONAL-FACE-LAMP-001.json').read_text())
        for path,sha in r['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),sha)
        face=r['face'];self.assertEqual((face['models_tested'],face['previously_covered_skipped'],face['first_crib_survivors'],face['all_crib_survivors']),(92,280,2,0))
        trained=[x for x in face['records'] if x['training']['consistent']]
        self.assertEqual({x['predicted_berlin'] for x in trained},{'HSTZCLZPDSB','LQHXLMKCWIQ'})
        self.assertTrue(all(x['training']['fitted_key_entries']==12 and x['training']['redundant_training_equalities']==1 and x['predicted_positions']==11 and x['berlin_matches']==0 and x['full_regeneration'] for x in trained))
        by={x['case_id']:x for x in face_cases()}
        for row in face['records']:
            if row['training']['consistent']:continue
            cert=row['training']['first_conflict'];a=ALPHABETS[row['alphabet']]
            self.assertEqual(cert['first']['phase'],cert['second']['phase'])
            self.assertNotEqual(cert['first']['required_key'],cert['second']['required_key'])
            for edge in cert.values():
                k=(a.index(edge['ciphertext'])+(-1 if row['equation']=='plus' else 1)*a.index(edge['plaintext']))%26
                self.assertEqual(k,edge['required_key'])
        lamp=r['lamp'];self.assertEqual(lamp['status'],'analytical_exclusion')
        self.assertEqual(lamp['actual_phase_models_enumerated'],0);self.assertFalse(lamp['berlin_consulted'])
        for c in lamp['certificates']:
            self.assertFalse(c['constant_parity_possible'])
            self.assertEqual(len(set(c['witness']['required_parities'])),2)
        reg=json.loads((ROOT/'results/HYPOTHESIS-REGISTER-003.json').read_text())
        for path,sha in reg['source_sha256'].items():
            import subprocess
            snapshot=subprocess.check_output(['git','show','7de429dc1ced9e0226173e325831761b4c67f03e:'+path],cwd=ROOT)
            self.assertEqual(hashlib.sha256(snapshot).hexdigest(),sha)

    def test_post_run_javascript_oracle_agrees_on_complete_domain(self):
        import shutil,subprocess
        p=ROOT/'results/CONDITIONAL-FACE-LAMP-001-independent.json'
        oracle=json.loads(p.read_text());actual=json.loads((ROOT/'results/CONDITIONAL-FACE-LAMP-001.json').read_text())
        by={(r['alphabet'],r['equation'],r['period'],r['order']):r for r in oracle['face']}
        self.assertEqual(len(by),92)
        for r in actual['face']['records']:
            q=by[r['alphabet'],r['equation'],r['period'],r['order']]
            self.assertEqual(r['training']['consistent'],q['training_consistent'])
            if q['training_consistent']:
                self.assertEqual(q['plaintext'],r['plaintext']);self.assertEqual(q['key'],r['training']['key'])
        for r,q in zip(actual['lamp']['certificates'],oracle['lamp_parity']):
            self.assertEqual(r['witness']['positions'],q['positions']);self.assertEqual(r['witness']['required_keys'],q['required_keys'])
        node=shutil.which('node') or '/opt/homebrew/bin/node'
        if not Path(node).is_file():self.skipTest('Node unavailable for independent replay')
        result=subprocess.run([node,str(ROOT/'experiments/conditional_face_lamp_oracle.mjs')],capture_output=True,text=True,timeout=30)
        self.assertEqual(result.returncode,0,result.stderr);self.assertEqual(json.loads(result.stdout),oracle)
