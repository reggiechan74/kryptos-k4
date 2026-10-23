import hashlib,json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import wheatstone_transition as w
import exclusion_scope_audit as scope

def read(name):return json.loads((ROOT/'results'/name).read_text())
class WheatstoneTransitionTests(unittest.TestCase):
    def test_published_processed_stream_vectors_and_inverse(self):
        data=json.loads((ROOT/'data/wheatstone-reference-vectors.json').read_text());self.assertEqual(len(data['vectors']),2)
        for v in data['vectors']:
            args=(v['outer'],v['inner'],v['initial_outer'],v['initial_inner']);cipher,_=w.crypt(v['processed_message'],*args)
            self.assertEqual(cipher,v['ciphertext']);self.assertEqual(w.crypt(cipher,*args,True)[0],v['processed_message'])
            self.assertEqual(w.tooth_oracle(v['processed_message'],*args),cipher);self.assertEqual(w.tooth_oracle(cipher,*args,True),v['processed_message'])
            self.assertNotEqual(v['original_message'].replace(' ','_'),v['processed_message'])
    def test_repeated_cipher_not_repeated_plaintext(self):
        cipher,trace=w.crypt('BA','_'+w.AZ,w.AZ);self.assertEqual(cipher[0],cipher[1]);self.assertEqual(trace[1]['steps'],26)
        self.assertEqual(w.crypt(cipher,'_'+w.AZ,w.AZ,decrypt=True)[0],'BA')
        with self.assertRaises(ValueError):w.crypt('AA','_'+w.AZ,w.AZ)
        with self.assertRaises(ValueError):w.crypt('_','_'+w.AZ,w.AZ)
        with self.assertRaises(ValueError):w.validate('AAB','AB')
    def test_complete_controls_and_rotational_quotient_replay(self):
        r=read('WHEATSTONE-TRANSITION-008-controls.json')['controls'];self.assertEqual(w.controls(),r)
        self.assertEqual(r['toy']['state_transition_comparisons'],443976);self.assertEqual(len(r['continuous_literal_crib_plants']),24)
        for row in r['toy']['rotation_quotient_rows']:
            self.assertEqual(row['represented_outer_permutations'],row['outer_rotation_representatives']*row['outer_size'])
            self.assertEqual(row['represented_inner_permutations'],row['inner_rotation_representatives']*row['inner_size'])
        self.assertEqual([x['comparisons'] for x in r['toy']['naive_complete_size3_size4']],[144,5184])
    def test_independent_displacement_relaxation(self):
        raw=subprocess.check_output(['/opt/homebrew/bin/node',str(ROOT/'experiments/wheatstone_transition_oracle.mjs')]);r=json.loads(raw);self.assertEqual(r,read('WHEATSTONE-TRANSITION-008-independent.json'))
        self.assertEqual(r['injective_key_controls'],3446);self.assertFalse(r['first']['consistent']);self.assertEqual(r['first']['contradictions'][0]['pair'],'ST');self.assertEqual(r['first']['contradictions'][0]['allowed_displacements_mod26'],[])
    def test_first_crib_certificate_does_not_use_berlin_or_search(self):
        r=read('WHEATSTONE-TRANSITION-008.json')['actual'];self.assertEqual(w.actual(),r);self.assertEqual(r['K4_keys_enumerated'],0);self.assertFalse(r['second_stage_evaluated']);self.assertIsNone(r['second'])
        cert=r['first']['certificates'][0];self.assertEqual(cert['first']['positions'],[24,25]);self.assertEqual(cert['second']['positions'],[33,34])
        self.assertEqual(cert['first']['plaintext_pair'],cert['second']['plaintext_pair']);self.assertNotEqual(cert['first']['equal_cipher'],cert['second']['equal_cipher'])
        d=json.loads((ROOT/'data/k4.json').read_text())
        for x in (cert['first'],cert['second']):self.assertEqual(d['ciphertext'][x['positions'][0]-1:x['positions'][1]],x['ciphertext_pair'])
    def test_same_transition_equality_mutation_and_alignment_scope(self):
        self.assertTrue(w.constraints('ABAB','CCDD')['compatible_necessary_condition']);self.assertFalse(w.constraints('ABAB','CCDE')['compatible_necessary_condition'])
        with self.assertRaises(ValueError):w.constraints('AB','ABC')
        # Enciphered spaces emit symbols; removing them is not an allowed alignment repair.
        key='SAMZEBNCDORFPGQTHUKIVJWYLX';cipher,_=w.crypt('A_B_','_'+w.AZ,key);self.assertEqual(len(cipher),4);self.assertEqual(w.crypt(cipher,'_'+w.AZ,key,decrypt=True)[0],'A_B_')
    def test_current_sources_and_registry_scope(self):
        for n in ('WHEATSTONE-TRANSITION-008.json','WHEATSTONE-TRANSITION-008-controls.json'):
            for p,h in read(n)['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),h)
        r=read('EXCLUSION-SCOPE-AUDIT-006.json');self.assertEqual(scope.run(),r);records={x['id']:x for x in r['canonical_entries']};self.assertEqual(len(records),60);self.assertEqual(records['H-WHEATSTONE']['status'],'analytical exclusion')
        source=json.loads((ROOT/'sources/wheatstone-historical-conventions-2026-10-23.json').read_text());self.assertFalse(source['third_party_software_executed']);self.assertIn('403',source['access_limits'][0]['outcome'])
