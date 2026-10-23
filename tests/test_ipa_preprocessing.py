import copy
import itertools
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments'))
from exact_linear import ring_vectors
from ipa_preprocessing import (normalize,long_vowel_tokens,input_audit,ORDINARY,SPECIAL,NEW_SPECIAL,WINDOWS,AZ,KR,
    constraints,select,recover_key,injective_first,encoded_plain,crypt,second_stage,phase_conflicts)

class IPAPreprocessingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.data=json.loads((ROOT/'data/ipa-cambridge-us-v1.json').read_text())

    def test_source_normalization_and_codepoint_not_byte_counts(self):
        a=input_audit(self.data)
        self.assertEqual(a['R1_lengths'],[10,9]);self.assertEqual(a['R2_lengths'],[13,11])
        self.assertEqual(normalize('/ˌiːst.nɔːrθˈiːst/'),WINDOWS[0][1])
        self.assertEqual(normalize(' /bɝːˈlɪn/ '),'bɝːlɪn')
        self.assertEqual(long_vowel_tokens('iːstnɔːrθiːst'),['iː','s','t','n','ɔː','r','θ','iː','s','t'])
        self.assertNotEqual(len(WINDOWS[0][1]),len(WINDOWS[0][1].encode('utf-8')))
        for s in ['ːi','iːː']:
            with self.assertRaises(ValueError):long_vowel_tokens(s)
        with self.assertRaises(ValueError):normalize('/iːst')

    def test_length_and_unicode_mutations_fail_frozen_input(self):
        d=copy.deepcopy(self.data);d['entries']['east']='/ist/'
        with self.assertRaises(AssertionError):input_audit(d)
        d=copy.deepcopy(self.data);d['entries']['northeast']=d['entries']['northeast'].replace('θ','T')
        with self.assertRaises(AssertionError):input_audit(d)
        for _,w in WINDOWS:
            self.assertEqual(json.loads(json.dumps(w,ensure_ascii=True)),w)
        with self.assertRaises(ValueError):encoded_plain('ə',AZ,{})

    def test_complete_small_alias_sets_against_independent_fits(self):
        aliases=dict(zip(SPECIAL+NEW_SPECIAL,'ADEFGH'));mapping={**ORDINARY,**aliases}
        tokens=['i']*97
        for start,w in WINDOWS:tokens[start:start+len(w)]=w
        latin=''.join(mapping[s] for s in tokens)
        from exact_linear import solve_ring
        for m in (2,10,12):
            cipher=crypt(latin,AZ,[(3+7*j)%26 for j in range(m)],'add')
            matrix,rhs,_=constraints(cipher,AZ,'add',m)
            solved=set(ring_vectors(solve_ring(matrix,rhs,26,3)))
            brute={x for x in itertools.product(range(26),repeat=3) if recover_key(cipher,AZ,'add',m,x) is not None}
            self.assertEqual(solved,brute)
            self.assertIn(tuple(AZ.index(aliases[s]) for s in SPECIAL),solved)

    def test_second_window_new_aliases_are_not_predictions(self):
        aliases=dict(zip(SPECIAL+NEW_SPECIAL,'ADEFGH'));mapping={**ORDINARY,**aliases}
        tokens=['i']*97
        for start,w in WINDOWS:tokens[start:start+len(w)]=w
        latin=''.join(mapping[s] for s in tokens);key=[3,10,17,24,5,12,19,0,7,14,21,2]
        cipher=crypt(latin,AZ,key,'add')
        stage=second_stage(cipher,AZ,'add',key,tuple(AZ.index(aliases[s]) for s in SPECIAL))
        self.assertTrue(stage['compatible'])
        self.assertEqual([x['position'] for x in stage['predicted_existing_symbol_positions']],[64,66,67,69,70,71,73,74])
        self.assertEqual(stage['new_alias_fit_positions'],[65,68,72])
        self.assertEqual(set(stage['new_aliases_fitted_not_predicted']),set(NEW_SPECIAL))
        self.assertFalse(injective_first((0,0,4),AZ))
        self.assertFalse(injective_first((AZ.index('I'),3,4),AZ))

    def test_first_crib_negative_and_phase_staging(self):
        r=json.loads((ROOT/'results/IPA-PREPROCESSING-001.json').read_text())
        self.assertEqual(r['mapping_independent_periods']['rejected'],[1,2,3,4,5,6,7,9,10])
        self.assertEqual(r['mapping_independent_periods']['not_contradicted'],[8,11,12])
        for m in (8,11,12):
            d=r['mapping_independent_periods']['pair_diagnostics'][str(m)]
            self.assertEqual((d['repeated_IPA_pairs'],d['repeated_ciphertext_pairs']),(0,0))
        self.assertEqual((r['ordinary_anchor_rejected_structures'],r['non_anchor_modular_rejected_structures']),(47,1))
        self.assertEqual(r['relaxed_training_survivor_structures'],0)
        self.assertEqual(r['actual_alias_assignments_enumerated'],0)
        extra=[row for row in r['rows'] if not row['fixed_ordinary_anchor_conflicts']]
        self.assertEqual([(x['alphabet'],x['equation'],x['period']) for x in extra],[('AZ','add',10)])
        self.assertEqual(extra[0]['modular_constraints'][0]['rhs'],13)
        self.assertEqual((-extra[0]['modular_constraints'][1]['rhs'])%26,11)
        for row in r['rows']:
            self.assertFalse(row['second_window_evaluated'])
            self.assertEqual(row['relaxed_alias_assignment_count'],0)
            for conflict in row['fixed_ordinary_anchor_conflicts']:
                self.assertTrue(all(22<=i<=34 for i in conflict['positions']))
            equations=row['modular_constraints']
            for field in row['relaxed_solution_space']['fields']:
                if field['consistent']:continue
                q=field['prime'];cert=field['contradiction'];weights=cert['equation_weights']
                self.assertTrue(all(sum(w*e['coefficients'][i] for w,e in zip(weights,equations))%q==0 for i in range(3)))
                self.assertEqual(sum(w*e['rhs'] for w,e in zip(weights,equations))%q,cert['rhs'])
                self.assertNotEqual(cert['rhs'],0)
        import hashlib
        for path,digest in r['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),digest)

    def test_control_receipt_truth_inclusion_and_ambiguity(self):
        r=json.loads((ROOT/'results/IPA-PREPROCESSING-001-controls.json').read_text())
        self.assertEqual(r['plant_count'],48)
        self.assertTrue(all(x['full_selector_models']==48 and x['true_aliases_and_key_retained'] and x['roundtrip'] and x['mutation_target_rejected'] for x in r['plants']))
        self.assertTrue(any(x['compatible_second_stage_assignments']>1 for x in r['plants']))
        self.assertEqual(len(r['complete_small_ring_comparisons']),9)
        self.assertTrue(all(x['complete_sets_equal'] for x in r['complete_small_ring_comparisons']))

if __name__=='__main__':unittest.main()
