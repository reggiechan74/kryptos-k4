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
