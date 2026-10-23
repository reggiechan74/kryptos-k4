import hashlib,itertools,json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import fractionated_morse_constraints as fm
import exclusion_scope_audit as scope

def read(name):return json.loads((ROOT/'results'/name).read_text())
class ArbitraryMorseTests(unittest.TestCase):
    def test_complete_small_mapping_counts_and_mutations(self):
        for q in (2,3,4):
            for domains in itertools.product(range(1<<q),repeat=2):
                ds=list(domains)+[(1<<q)-1]*(q-2);expected=[list(p) for p in itertools.permutations(range(q)) if all(ds[i]>>p[i]&1 for i in range(q))];r=fm.completions(ds,q)
                self.assertTrue(r['completed']);self.assertEqual(int(r['count']),len(expected))
                if expected:self.assertIn(r['witness'],expected)
        self.assertFalse(fm.completions([3,3],2,cap=0)['completed'])
        self.assertEqual(fm.completions([1,1],2)['count'],'0')
    def test_partial_boundaries_and_independent_substring_oracle(self):
        for offset in range(3):
            for word in ('EAST','NORTHEAST','BERLIN','CLOCK'):
                for mask in (0,(1<<(len(word)-1))-1):
                    raw=fm.pattern(word,mask);cipher='ABCDEFGHIJKLMNOPQRSTUVWXYZ'*3
                    r=fm.window(cipher,offset,raw);expected=fm.direct_oracle(cipher,offset,raw)
                    self.assertEqual(r,expected if all(expected) else None)
        with self.assertRaises(ValueError):fm.window('A',1,'....')
    def test_saved_plants_include_true_complete_selector_context(self):
        r=read('MASK-FM-ARBITRARY-007-controls.json')['controls'];self.assertEqual(fm.controls(),r);self.assertEqual(len(r['literal_crib_plants']),6);self.assertEqual(len(r['complete_small_permutation_comparisons']),100)
        self.assertEqual(r['direct_substring_checks'],102)
        for p in r['literal_crib_plants']:
            self.assertTrue(p['complete_first_selector_truth_retained']);self.assertEqual(p['complete_first_selector_contexts'],348160);self.assertTrue(p['full_roundtrip'])
            for window in p['windows']:self.assertTrue(window['true_key_retained']);self.assertGreater(int(window['local_key_count']),0)
    def test_actual_first_stage_exclusion_replays_without_berlin(self):
        r=read('MASK-FM-ARBITRARY-007.json')['actual'];fresh=fm.actual()
        for record in (r['first'],fresh['first']):record.pop('seconds')
        self.assertEqual(fresh,r);self.assertEqual(r['first']['raw_contexts'],348160);self.assertEqual(r['first']['unique_domain_records'],0)
        self.assertEqual(r['first']['rejection_tally'],{'repeated_cipher_empty_domain':348160});self.assertIsNone(r['second']);self.assertFalse(r['second_stage_evaluated'])
    def test_independent_certificates_and_complete_digest(self):
        raw=subprocess.check_output(['/opt/homebrew/bin/node',str(ROOT/'experiments/fractionated_morse_oracle.mjs')]);r=json.loads(raw);self.assertEqual(r,read('MASK-FM-ARBITRARY-007-independent.json'));self.assertEqual(sum(r['rejection_counts'].values()),348160);self.assertEqual(r['compatible_contexts'],0)
        cipher=json.loads((ROOT/'data/k4.json').read_text())['ciphertext']
        for example in r['examples'].values():
            c=example['certificate'];raw=fm.pattern('EASTNORTHEAST',example['mask']);a,b=c['first'],c['second']
            for point in (a,b):
                pos=example['offset']+point['index'];self.assertEqual(pos%3,c['coordinate']);self.assertEqual(cipher[pos//3],c['cipher']);self.assertEqual(raw[point['index']],point['symbol'])
            self.assertNotEqual(a['symbol'],b['symbol'])
    def test_shared_map_across_windows_retains_true_key(self):
        alphabet='KRYPTOSABCDEFGHIJLMNQUVWXZ';message='A'*21+' EASTNORTHEAST '+'B'*29+' BERLINCLOCK '+'C'*23;encoded=fm.old.morse_encode(message,alphabet);cipher=encoded['ciphertext'];raw1=fm.pattern('EASTNORTHEAST',0);s=21*len(fm.MORSE['A'])+20+2
        d=fm.window(cipher,s,raw1);raw2=fm.pattern('BERLINCLOCK',0);t=s+len(raw1)+2+29*len(fm.MORSE['B'])+28+2;combined=fm.window(cipher,t,raw2,d)
        true=[fm.TRIPLES.index(x) for c in fm.AZ for x,v in fm.old.triple_table(alphabet).items() if v==c]
        self.assertTrue(all(combined[i]>>true[i]&1 for i in range(26)));self.assertGreater(int(fm.completions(combined)['count']),0)
    def test_source_hashes_and_current_scope_receipt(self):
        for n in ('MASK-FM-ARBITRARY-007-controls.json','MASK-FM-ARBITRARY-007.json'):
            for p,h in read(n)['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),h)
        saved=read('EXCLUSION-SCOPE-AUDIT-005.json');self.assertEqual(scope.run(),saved)
        records={x['id']:x for x in saved['canonical_entries']};self.assertEqual(len(records),60);self.assertEqual(records['H-MASK-FM']['status'],'analytical exclusion')
