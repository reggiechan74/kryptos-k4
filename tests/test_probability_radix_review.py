from fractions import Fraction
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments'))
from probability_radix_review import exact_checks,verify_members,CAL,RAD
from alphabet_geometry import load_schema,codebook,encode_array

class ProbabilityRadixReviewTests(unittest.TestCase):
    def test_imported_originals_and_replay_status(self):
        self.assertEqual(verify_members(),19)
        r=json.loads((ROOT/'results/GEOMETRIC-PROBABILITY-RADIX-LOCAL-REPLAY.json').read_text())
        self.assertTrue(r['calibration']['numeric_and_trace_fields_exactly_equal'])
        self.assertLessEqual(set(r['calibration']['differing_metadata_fields']),{'python_version'})
        self.assertTrue(r['radix_primary_byte_equal'] and r['radix_independent_byte_equal'])
        self.assertFalse(r['original_files_modified'])

    def test_first_crib_fit_has_only_one_period12_closure(self):
        positions=list(range(21,34));groups={}
        for i in positions:groups.setdefault(i%12,[]).append(i+1)
        self.assertEqual(len(groups),12)
        self.assertEqual([v for v in groups.values() if len(v)>1],[[22,34]])
        r=json.loads((CAL/'result.json').read_text())
        self.assertEqual(Fraction(r['exact_period12_histogram_null']['beaufort']['probability_fraction']),Fraction(382,97*96))
        self.assertEqual(r['observed_survivors'][0]['second_window'],'ZBVJDFKRUCA')
        self.assertFalse(r['observed_survivors'][0]['second_check_pass'])

    def test_matched_null_refitting_counts_and_scope(self):
        p=json.loads((CAL/'preregistration.json').read_text());r=json.loads((CAL/'result.json').read_text())
        self.assertEqual(p['N'],19999)
        self.assertEqual(len(r['per_model_pass_counts']),24)
        self.assertEqual({(x['family'],x['period']) for x in r['per_model_pass_counts']},{(f,m) for f in ('add','beaufort') for m in range(1,13)})
        self.assertEqual(r['family_null_count_distribution'],{'0':18268,'1':1728,'2':3})
        self.assertEqual(r['family_plus_one_monte_carlo_p'],1732/20000)
        self.assertEqual(r['controls']['pairwise_comparisons'],24*19999)
        self.assertFalse(p['second_check']['used_in_null_statistic'])

    def test_independent_local_closure_and_all_eight_certificates(self):
        expected=json.loads((ROOT/'results/GEOMETRIC-PROBABILITY-RADIX-LOCAL-REPLAY.json').read_text())['checks']
        self.assertEqual(exact_checks(),expected)
        self.assertEqual(expected['radix_families_excluded'],8)
        self.assertEqual(expected['root_searches_added'],0)
        self.assertEqual({(x['alphabet'],x['source'],tuple(x['positions'])) for x in expected['first_crib_only_certificates']},
            {('AZ','plaintext',(22,24)),('AZ','ciphertext',(23,26)),('KRYPTOS','plaintext',(22,29)),('KRYPTOS','ciphertext',(23,33))})

    def test_parity_proof_requires_both_geometric_conditions(self):
        v=codebook(load_schema())
        for c in 'ELQST':
            self.assertEqual(v[c][0],0);self.assertEqual(sum(v[c])%2,0)
            for b in (2,3,26,27,61,10**80,10**80+1):self.assertEqual(encode_array(v[c],b)%2,0)
        self.assertEqual(sum(v['J'])%2,0)
        self.assertEqual(encode_array(v['J'],2)%2,1)
        self.assertEqual(v['A'][0],0)
        self.assertEqual(encode_array(v['A'],3)%2,1)

    def test_positive_controls_and_auxiliary_are_separate(self):
        r=json.loads((RAD/'results.json').read_text())
        self.assertEqual(r['controls']['roundtrip_cases'],3264)
        self.assertEqual(r['controls']['parity_solver_plants_retained'],3264)
        self.assertEqual(r['controls']['mod26_plants_retained'],3264)
        mutation=r['controls']['alignment_mutation']
        self.assertEqual((mutation['correct_first_ciphertext'],mutation['wrong_preupdate_ciphertext']),('H','O'))
        self.assertFalse(r['heldout_evaluated'] or r['root_or_digit_search_performed'])
        self.assertEqual(len(r['auxiliary_direct_map']),2)
        self.assertTrue(all(x['impossible_positions'][0]==22 for x in r['auxiliary_direct_map']))

if __name__=='__main__':unittest.main()
