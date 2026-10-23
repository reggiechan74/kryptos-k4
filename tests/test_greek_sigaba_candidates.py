import hashlib,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments'))
import greek_phonetic_candidate as greek
import sigaba_inspired as sig

class GreekSigabaCandidateTests(unittest.TestCase):
    def test_source_fixed_phone_rendering_lengths_and_loss(self):
        d=greek.schema()
        self.assertEqual(greek.transcribe(d['first_phones'],d),'ΙΣΤΝΟΡΘΙΣΤ')
        self.assertEqual(greek.transcribe(d['second_phones'],d),'ΜΠΕΡΛΙΝΚΛΑΚ')
        self.assertEqual([len(d[k]) for k in ('first_greek','second_greek')],[10,11])
        self.assertEqual(greek.transcribe(['iː'],d),greek.transcribe(['ɪ'],d))
        with self.assertRaises(ValueError):greek.transcribe(['unknown'],d)
        # Digraphs remain two characters; Greek is not a renamed 26-letter alphabet.
        self.assertEqual(greek.transcribe(['b'],d),'ΜΠ');self.assertEqual(len(d['greek_alphabet']),24)

    def test_greek_cipher_exact_inverse_and_rejected_outside_domain(self):
        d=greek.schema();g=d['greek_alphabet'];key=[0,7,25]
        for a in d['cipher_alphabets'].values():
            for eq in d['equations']:
                text=g+g[::-1];c=greek.crypt(text,key,a,eq,d)
                self.assertEqual(greek.crypt(c,key,a,eq,d,True),text)
        for text in ('Y','Z'):
            with self.assertRaises(ValueError):greek.crypt(text,[0],d['cipher_alphabets']['AZ'],'plus',d,True)
        with self.assertRaises(ValueError):greek.crypt('Ι\u0301',[0],d['cipher_alphabets']['AZ'],'plus',d)

    def test_unknown_alignment_first_fit_is_complete_not_english_offset(self):
        d=greek.schema();g=d['greek_alphabet'];p=list((g*5)[:97]);p[7:17]=d['first_greek'];p=''.join(p)
        for a in d['cipher_alphabets'].values():
            for eq in d['equations']:
                for m in range(1,11):
                    key=[(7*j+9)%26 for j in range(m)];c=greek.crypt(p,key,a,eq,d)
                    recovered,conflict=greek.fit_first(c,a,eq,m,7,d)
                    self.assertIsNone(conflict);self.assertEqual(recovered,key)
        self.assertEqual(sum(77-u for u in range(77)),3003)

    def test_sigaba_style_every_bank_permutation_and_long_counter(self):
        m=sig.machine()
        for w,n in ((m['cipher_raw'],26),(m['control_raw'],26),(m['data']['index_wirings'],10)):
            f,b=sig.tables(w,n)
            for fw,bw in zip(f,b):
                for p in range(n):self.assertEqual([bw[p][fw[p][x]] for x in range(n)],list(range(n)))
        for q,r in ((0,0),(25,9),(7,3)):
            st,masks=sig.schedule(m,q,r,805)
            self.assertEqual(st,sig.schedule_oracle(m,q,r,805))
            self.assertTrue(all(1<=len(x)<=4 for x in masks))
        self.assertFalse(m['data']['historical_SIGABA'])

    def test_rotor_fixed_inverse_and_unrelated_message(self):
        m=sig.machine();st,_=sig.schedule(m,25,9)
        for p in ('',sig.AZ,sig.AZ[::-1],'ROTORSSTEPCONTINUOUSLYTHROUGHTHEGAPS'):
            c=sig.crypt(p,m,st,25)
            self.assertEqual(sig.crypt(c,m,st,25,True),p)
            self.assertEqual(sig.direct_crypt(p,m,25,25,9),c)
            self.assertEqual(sig.direct_crypt(c,m,25,25,9,True),p)

    def test_full_selector_control_receipts_and_preserved_aliases(self):
        g=json.loads((ROOT/'results/GREEK-PHONETIC-001-controls.json').read_text())
        self.assertEqual(len(g['controls']['plants']),40)
        self.assertEqual(g['controls']['raw_descriptions_accounted'],4804800)
        self.assertTrue(all(p['truth_retained'] for p in g['controls']['plants']))
        self.assertTrue(any(len(p['compatible'])>1 for p in g['controls']['plants']))
        s=json.loads((ROOT/'results/SIGABA-INSPIRED-001-controls.json').read_text())
        self.assertEqual(s['raw_starting_keys'],6760);self.assertEqual(s['distinct_stepping_schedules'],130)
        self.assertEqual(len(s['controls']['plants']),12)
        self.assertEqual(s['controls']['rotor_inverse_checks'],7260)
        self.assertTrue(all(p['truth_retained'] and p['raw_compatible_keys']==2 for p in s['controls']['plants']))
        self.assertEqual(sum(len(row['aliases']) for row in s['schedule_aliases']),260)
        for receipt in (g,s):
            for p,sha in receipt['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),sha)

    def test_actual_greek_complete_alignment_records_and_mismatches(self):
        r=json.loads((ROOT/'results/GREEK-PHONETIC-001.json').read_text());d=greek.schema();actual=r['actual']
        self.assertEqual(actual['raw_structural_alignment_descriptions'],120120)
        self.assertEqual(len(actual['records']),3080)
        self.assertEqual(actual['first_window_fits'],324);self.assertEqual(actual['second_window_checks'],12664)
        self.assertEqual(actual['compatible'],[]);self.assertEqual(actual['crib_fits_invalid_Greek_domain'],[])
        self.assertFalse(r['null']['executed'])
        cipher=json.loads((ROOT/'data/k4.json').read_text())['ciphertext'];count=0
        for row in actual['records']:
            a=d['cipher_alphabets'][row['alphabet']];key=row['key']
            if key is None:
                cert=row['training_conflict'];self.assertEqual(cert['first']['phase'],cert['second']['phase'])
                self.assertNotEqual(cert['first']['required_key'],cert['second']['required_key'])
            else:
                count+=len(row['second_checks']);self.assertEqual(len(key),row['period'])
                for failure in row['second_checks']:
                    i=failure['first_mismatch']-1;off=i-(failure['second_start']-1)
                    v=d['greek_alphabet'].index(d['second_greek'][off]);sigma=1 if row['equation']=='plus' else -1
                    expected=a[(sigma*v+key[i%len(key)])%26]
                    self.assertEqual(expected,failure['expected_cipher']);self.assertNotEqual(expected,cipher[i])
        self.assertEqual(count,12664)
        for path,sha in r['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),sha)

    def test_actual_rotor_all_certificates_and_scoped_registry(self):
        r=json.loads((ROOT/'results/SIGABA-INSPIRED-001.json').read_text());m=sig.machine();actual=r['actual']
        self.assertFalse(r['authentic_SIGABA']);self.assertEqual(actual['raw_keys_accounted'],6760)
        self.assertEqual(actual['schedule_normalized_models_checked'],3380)
        self.assertEqual(actual['training_survivors'],0);self.assertEqual(actual['compatible'],[])
        self.assertFalse(r['null']['executed'])
        groups={g['schedule_id']:g for g in r['schedule_aliases']}
        cipher=json.loads((ROOT/'data/k4.json').read_text())['ciphertext']
        for row in actual['records']:
            self.assertFalse(row['berlin_evaluated']);fail=row['first_conflict'];i=fail['position']-1
            self.assertIn(i,range(21,25));states=groups[row['schedule_id']]['states']
            v=sig.AZ.index('EASTNORTHEAST'[i-21]);expected=sig.AZ[sig.letter(v,m,states[i],row['cipher_offset'])]
            self.assertEqual(expected,fail['expected_cipher']);self.assertNotEqual(expected,cipher[i])
        for path,sha in r['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),sha)
        reg=json.loads((ROOT/'results/HYPOTHESIS-REGISTER-004.json').read_text())
        self.assertEqual(reg['entries'],57);self.assertFalse(reg['authentic_SIGABA_tested'])
        for path,sha in reg['source_sha256'].items():
            import subprocess
            historical=subprocess.check_output(['git','show','2985205002f1b4169fd77d219a6b72fa1e85ad68:'+path],cwd=ROOT)
            self.assertEqual(hashlib.sha256(historical).hexdigest(),sha)

    def test_independent_JS_replay_and_complete_domain_agreement(self):
        import shutil,subprocess
        o=json.loads((ROOT/'results/GREEK-SIGABA-001-independent.json').read_text())
        g=json.loads((ROOT/'results/GREEK-PHONETIC-001.json').read_text())['actual']
        by={(r['alphabet'],r['equation'],r['period'],r['first_start']):r for r in o['greek']['records']}
        for r in g['records']:
            v=by[r['alphabet'],r['equation'],r['period'],r['first_start']]
            self.assertEqual(r['key'] is not None,v['fit'])
            if v['fit']:
                self.assertEqual(r['key'],v['key']);self.assertEqual([[x['second_start'],x['first_mismatch']] for x in r['second_checks']],v['checks'])
        by={(r['q'],r['c'],r['r']):r for r in o['sigaba_inspired']['records']};self.assertEqual(len(by),6760)
        r=json.loads((ROOT/'results/SIGABA-INSPIRED-001.json').read_text())
        for row in r['actual']['records']:
            for a in row['raw_keys']:self.assertEqual(row['first_conflict']['position'],by[a['q'],row['cipher_offset'],a['r']]['first_conflict'])
        node=shutil.which('node') or '/opt/homebrew/bin/node'
        if not Path(node).is_file():self.skipTest('Node unavailable for independent replay')
        p=subprocess.run([node,str(ROOT/'experiments/greek_sigaba_oracle.mjs')],capture_output=True,text=True,timeout=30)
        self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(json.loads(p.stdout),o)

    def test_fixed_state_is_not_a_previous_additive_or_beaufort_cursor(self):
        m=sig.machine();states,_=sig.schedule(m,0,0)
        # Hold one state fixed to inspect its substitution, not a running message.
        permutation=sig.crypt(sig.AZ,m,[states[0]]*26,0)
        self.assertEqual(len(set(permutation)),26)
        for a in (sig.AZ,'KRYPTOSABCDEFGHIJLMNQUVWXZ'):
            for sign in (1,-1):
                shifts={(a.index(permutation[sig.AZ.index(a[i])])-sign*i)%26 for i in range(26)}
                self.assertGreater(len(shifts),1)
