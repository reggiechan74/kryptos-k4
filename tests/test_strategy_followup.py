from pathlib import Path
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'experiments'))
from strategy_followup import (AZ, KR, assess, configurations, construction_audit,
                               crib_map, equivalence_audit, gauge_id, rank_oracle,
                               summarize_toy, toy_encode, transform, clock_audit)
import itertools


class StrategyFollowupTests(unittest.TestCase):
    def test_rule_timing_and_nonrotation(self):
        # First D outputs D; MTF state now DABCE..., so next plain B outputs A.
        self.assertEqual(transform('DB', (AZ, AZ))[0], 'DA')
        self.assertEqual(transform('DB', (AZ, AZ), rotate=True)[0], 'DE')
        self.assertEqual(transform('DA', (AZ, AZ), inverse=True)[0], 'DB')
        self.assertEqual(rank_oracle('DA', (AZ, AZ), True), 'DB')

    def test_exact_domain_and_affine_superset_witness(self):
        self.assertEqual(configurations(), [(AZ,AZ),(AZ,KR),(KR,AZ),(KR,KR)])
        r=equivalence_audit()
        self.assertEqual(r['raw_prior_role_sign_shift_cases'],208)
        self.assertTrue(all(x['outside_prior_affine_superset'] for x in r['records']))

    def test_planted_actual_crib_structure_without_reading_K4_scores(self):
        known=crib_map(json.loads((ROOT/'data/k4.json').read_text()))
        p=list(AZ*4)
        for i,c in known.items():p[i]=c
        p=''.join(p[:97])
        for cfg in configurations():
            c,states=transform(p,cfg,trace=True)
            self.assertEqual(rank_oracle(c,cfg,True),p)
            self.assertEqual(rank_oracle(p,cfg,False),c)
            self.assertEqual(len(states),97)
            self.assertTrue(assess(c,known,cfg)['all24'])

    def test_known_source_controls_and_separate_clock_gate(self):
        c=construction_audit()
        self.assertTrue(c['K1']['exact63_cipher_match'])
        self.assertEqual(c['K1']['normal_key_differences_one_based'],[57])
        self.assertTrue(c['K2']['exact_deletion_reproduction'])
        self.assertEqual(c['K2']['deleted_suffix'],'IDBYROWS')
        self.assertEqual(c['K2']['restored_suffix'],'XLAYERTWO')
        clock=clock_audit()
        self.assertEqual(clock['predicted'],[13,14,15,16])
        self.assertEqual(clock['K4_application_status'],'underidentified_no_letter_operator')

    def test_toy_gauge_and_independent_counting(self):
        alph=[''.join(p) for p in itertools.permutations('ABCD')]
        pairs=list(itertools.product(alph,repeat=2))
        p='ABCDBADCBACD'; r='ABCD'; s='CADB'
        c=toy_encode(p,r,s)
        for i in range(4):
            self.assertEqual(toy_encode(p,r[i:]+r[:i],s[i:]+s[:i]),c)
            self.assertEqual(gauge_id(r,s),gauge_id(r[i:]+r[:i],s[i:]+s[:i]))
        result=summarize_toy(c,p,pairs)
        self.assertIn(p,result['compatible_plaintexts'])
        self.assertEqual(result['raw_compatible'],4*result['gauge_classes'])
        self.assertEqual(result['forced_correct'],len(result['forced_nonfit']))

    def test_invalid_input_rejected(self):
        for bad in ('A?','a','A B'):
            with self.assertRaises(ValueError):transform(bad,(AZ,AZ))


if __name__ == '__main__':unittest.main()
