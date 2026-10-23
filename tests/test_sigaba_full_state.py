import hashlib,json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import sigaba_csp889 as sig
import sigaba_state_inference as st
import exclusion_scope_audit as audit

class SigabaFullStateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.prepared=sig.prepare()
    def test_complete_small_rings_keep_ambiguity(self):
        import itertools
        for n in (2,3,4,6):
            t=st.toy_tables(n);g={'layout':1,'states':[(0,0,0,0,0)]*5};p={0:0,1:1,2:0,3:1,4:0};seed=(0,)*5;c=[st.enc_letter(x,i,seed,g,t,n) for i,x in p.items()]
            joined={s for s in st.join_states(p,c,g,t,n) if all(st.enc_letter(x,i,s,g,t,n)==c[i] for i,x in p.items())}
            self.assertEqual(joined,st.direct_fixed(p,c,g,t,n));self.assertIn(seed,joined);self.assertGreater(len(joined),1)
    def test_unknown_prefix_state_uses_continuous_schedule(self):
        d,t,groups=self.prepared;g=groups[25];seed=(1,4,9,16,25);k=sig.key(g['layout'],0,*g['aliases'][0]);k['cipherposition']=''.join(sig.AZ[x] for x in seed)
        p=(sig.AZ*4)[:97];c=sig.Machine(k,d,t).crypt(p)
        for i in (0,21,22,23,63,73,96):self.assertEqual(st.enc_letter(sig.AZ.index(p[i]),i,seed,g,t),sig.AZ.index(c[i]))
        pp={i:sig.AZ.index(p[i]) for i in (21,22,23)};self.assertIn(seed,set(st.join_states(pp,[sig.AZ.index(x) for x in c],g,t)))
    def test_incomplete_budget_never_claims_negative(self):
        r=st.selector('A'*97,self.prepared,budget=-1)
        self.assertFalse(r['completed']);self.assertEqual(r['schedules_completed'],0);self.assertIsNotNone(r['reason']);self.assertEqual(r['raw_state_descriptions_covered'],0)
    def test_full_actual_replay_and_accounting(self):
        r=json.loads((ROOT/'results/SIGABA-CSP889-STATE-002.json').read_text())['actual'];cipher=json.loads((ROOT/'data/k4.json').read_text())['ciphertext']
        self.assertEqual(st.selector(cipher,self.prepared),r);self.assertTrue(r['completed']);self.assertEqual(r['schedules_completed'],520)
        self.assertEqual(r['raw_state_descriptions_covered'],520*26**5);self.assertEqual(r['three_letter_joined_starts'],350311)
        self.assertEqual(r['first_stage_survivors'],[]);self.assertEqual(r['full_survivors'],[])
        self.assertEqual(sum(sum(x['first_conflict_histogram'].values()) for x in r['records']),350311)
        self.assertEqual(r['left_pairs_evaluated'],520*26**2);self.assertEqual(r['right_triples_evaluated'],520*26**3)
    def test_complete_control_receipts_and_source_hashes(self):
        r=json.loads((ROOT/'results/SIGABA-CSP889-STATE-002-controls.json').read_text())['controls']
        self.assertEqual(len(r['complete_toy_comparisons']),16);self.assertTrue(any(p['complete_set_size']>1 for p in r['complete_toy_comparisons']))
        self.assertTrue(all(p['truth_included'] for p in r['literal_crib_plants']))
        self.assertEqual([p['selector_schedules'] for p in r['literal_crib_plants']],[520,520,1,1])
        self.assertEqual(r['direct_26_power_5_comparison']['raw_starts'],26**5);self.assertTrue(r['direct_26_power_5_comparison']['sets_equal'])
        for name in ('SIGABA-CSP889-STATE-002-controls.json','SIGABA-CSP889-STATE-002.json','PHYSICAL-ADDENDUM-LOCAL-REVIEW-001.json'):
            record=json.loads((ROOT/'results'/name).read_text())
            for path,h in record['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),h)
    def test_visual_receipt_staging_and_dated_source_conflicts(self):
        r=json.loads((ROOT/'results/PHYSICAL-ADDENDUM-LOCAL-REVIEW-001.json').read_text());self.assertEqual(r['local_visual_inspections'],11);self.assertEqual(len(r['images']),11)
        self.assertFalse(r['entire_worker_survey_independently_repeated']);self.assertEqual(r['final_reported_worker_screening_images'],252)
        note=(ROOT/'research/evidence/2026-10-23-lodestone-compass/PHYSICAL-ADDENDUM-LOCAL-REVIEW.md').read_text()
        for value in ('static','three-inch','handwritten','typed','5 November 1990','not a measured lamp height'):self.assertIn(value,note)
        self.assertFalse(r['third_party_image_binaries_committed'])
    def test_current_registry_and_audit_are_separate_from_prior_snapshots(self):
        saved=json.loads((ROOT/'results/EXCLUSION-SCOPE-AUDIT-002.json').read_text());self.assertEqual(audit.run(),saved)
        reg=json.loads((ROOT/'results/HYPOTHESIS-REGISTER-006.json').read_text())
        for p,h in reg['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),h)
        self.assertEqual(len(saved['canonical_entries']),57)
        sigaba=next(x for x in saved['canonical_entries'] if x['id']=='H-SIGABA');self.assertIn('6,178,315,520',sigaba['exact_tested_scope'])
