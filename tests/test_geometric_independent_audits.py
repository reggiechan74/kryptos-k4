import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments'))
from geometric_followup_checks import compare,verify_imports

class GeometricIndependentAuditTests(unittest.TestCase):
    def test_original_members_remain_exact(self):
        self.assertEqual(verify_imports(),11)

    def test_full_replay_cross_comparison(self):
        result=compare()
        self.assertEqual(result,json.loads((ROOT/'results/GEOMETRIC-FOLLOWUP-COMPARISON.json').read_text()))
        self.assertEqual(result['pilot_a_conflict_and_fit_records_equal'],24)
        self.assertEqual(result['pilot_b_full_plaintext_outputs_equal'],3640)
        self.assertEqual(result['new_K4_models_or_root_searches'],0)

    def test_raw_number_attack_scope_and_exact_ambiguities(self):
        r=json.loads((ROOT/'results/GEOMETRIC-FOLLOWUP-COMPARISON.json').read_text())
        cases=r['raw_number_security_lookup_comparisons']
        self.assertEqual([(x['root_digit_radix'],x['pairs'],x['distinct_codes']) for x in cases],[(10,260,259),(12,312,311),(16,416,415),(60,1560,1558)])
        self.assertTrue(all(x['full_lookup_equal'] for x in cases))
        self.assertEqual(cases[-1]['collision_classes'],[
            {'code':'8','candidates':[{'letter':'C','base':2},{'letter':'O','base':8}]},
            {'code':'27','candidates':[{'letter':'C','base':3},{'letter':'O','base':27}]}])

    def test_ambiguity_and_independent_controls_preserved(self):
        r=json.loads((ROOT/'independent/2026-10-22/geometric-pilot-oracle/result.json').read_text())
        self.assertEqual(r['controls']['rotor_all_family_roundtrips'],3640)
        self.assertTrue(any(x['exact_survivor_count']==2 for x in r['controls']['rotor_full_selection_controls']))
        self.assertEqual(r['pilot2']['first_crib_survivors'],[])
        self.assertEqual(r['pilot2']['exact_crib_survivors'],[])

if __name__=='__main__':unittest.main()
