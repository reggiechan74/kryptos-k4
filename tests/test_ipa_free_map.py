import itertools
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments'))
from ipa_free_map import model,count_injections,brute_gauge_count,falling,analyze,AZ,WINDOWS

class IPAFreeMapTests(unittest.TestCase):
    def test_cycle_and_injectivity_have_different_certificates(self):
        cycle=count_injections(model([(0,'a',0),(1,'a',1)],1,5))
        collision=count_injections(model([(0,'a',0),(1,'b',0)],1,5))
        self.assertEqual(cycle['status'],'impossible_cycle')
        self.assertEqual(collision['status'],'impossible_within_component_injectivity')
        self.assertEqual(collision['certificate']['glyphs'],['a','b'])
        self.assertEqual((cycle['gauge_fixed_count'],collision['gauge_fixed_count']),(0,0))

    def test_component_packing_and_symmetric_mask_multiplicity(self):
        m=model([(0,'a',0),(2,'b',1),(1,'c',0),(3,'d',2)],2,4)
        r=count_injections(m)
        self.assertEqual(r['status'],'impossible_component_packing')
        self.assertEqual(brute_gauge_count(m),0)
        m=model([(0,'a',0),(1,'b',0),(3,'c',2)],2,4)
        r=count_injections(m)
        self.assertEqual(r['gauge_fixed_count'],2)
        self.assertEqual(brute_gauge_count(m),2)
        self.assertEqual(r['ungauged_count'],8)
        groups=r['component_descriptions'][1]['translations_grouped_by_occupied_set']
        self.assertEqual(sorted(x['multiplicity'] for x in groups),[2,2])

    def test_singleton_count_and_gauge_factor_from_full_maps(self):
        m=model([(i,chr(97+i),i) for i in range(4)],4,7)
        r=count_injections(m)
        self.assertEqual(r['gauge_fixed_count'],falling(6,3))
        self.assertEqual(r['ungauged_count'],falling(7,4))
        raw=0
        for f in itertools.permutations(range(7),4):
            # Every phase appears once, so its q is uniquely determined.
            q=[(f[i]-i)%7 for i in range(4)]
            self.assertTrue(all((f[e['u']]-q[e['v']-4])%7==e['delta'] for e in m['edges']))
            raw+=1
        self.assertEqual(raw,r['ungauged_count'])

    def test_component_count_invariant_to_labels_order_and_coordinate_origin(self):
        obs=[(0,'a',0),(1,'b',0),(3,'c',2)]
        expected=count_injections(model(obs,2,4))['gauge_fixed_count']
        for values in [obs,list(reversed(obs)),[(i,{'a':'θ','b':'ː','c':'ɝ'}[g],v) for i,g,v in obs],[(i,g,(v+1)%4) for i,g,v in obs],[(i+1,g,v) for i,g,v in obs]]:
            self.assertEqual(count_injections(model(values,2,4))['gauge_fixed_count'],expected)

    def test_literal_plant_prediction_marginals_and_stage_degrees(self):
        glyphs=list(dict.fromkeys(''.join(w for _,w in WINDOWS)))
        f=dict(zip(glyphs,range(14)));tokens=['i']*97
        for start,w in WINDOWS:tokens[start:start+len(w)]=w
        key=[(7*j+3)%26 for j in range(12)]
        cipher=''.join(AZ[(f[s]+key[i%12])%26] for i,s in enumerate(tokens))
        r=analyze(cipher,'AZ',12)
        self.assertEqual(len(r['training']['glyphs']),8)
        self.assertEqual(len(r['full']['glyphs']),14)
        self.assertEqual(r['training_count']['gauge_fixed_count'],falling(24,6))
        self.assertEqual(r['second_stage_topology']['counts'],{'new_glyph_parameter':6,'component_offset_join':4,'closure_check':1})
        # Independent set-merging connectivity check, without graph potentials.
        groups=[{node} for node in range(len(r['full']['node_labels']))]
        for edge in r['full']['edges']:
            a=next(group for group in groups if edge['u'] in group)
            b=next(group for group in groups if edge['v'] in group)
            if a is not b:
                groups.remove(a);groups.remove(b);groups.append(a|b)
        self.assertEqual(len(groups),3)
        self.assertEqual(r['full']['graph']['component_count'],len(groups))
        self.assertEqual(r['second_stage_topology']['additional_joint_cycle_checks'],1)
        self.assertEqual([x['position'] for x in r['first_stage_existing_glyph_predictions']],[66,69,73])
        for row in r['first_stage_existing_glyph_predictions']:
            self.assertEqual(sum(row['counts_by_cipher_value']),r['training_count']['gauge_fixed_count'])
            self.assertTrue(row['actual_in_prediction_set'])
        self.assertEqual(r['training_descriptions_with_unfitted_new_glyphs'],r['training_count']['gauge_fixed_count']*falling(18,6))

    def test_control_receipt_counts_and_truth_inclusion(self):
        r=json.loads((ROOT/'results/IPA-FREE-MAP-001-controls.json').read_text())
        self.assertEqual(r['small_ring_count'],45)
        self.assertTrue(all(x['complete_enumeration_equal'] for x in r['complete_small_ring_comparisons']))
        self.assertEqual(r['plant_count'],24)
        self.assertTrue(all(x['true_description_retained'] and x['fixed_model_full_roundtrip'] and x['global_translation_gauges_checked']==26 for x in r['plants']))

    def test_actual_exact_counts_and_certificates(self):
        r=json.loads((ROOT/'results/IPA-FREE-MAP-001.json').read_text())
        expected={'AZ':{7:14,8:380,10:175560,11:3862320,12:96909120},
                  'KRYPTOS':{7:13,8:380,10:175560,11:3862320,12:96909120}}
        self.assertEqual(len(r['rows']),24)
        second=0
        for row in r['rows']:
            self.assertNotEqual(row['status'],'budget_unresolved')
            self.assertEqual(row['training_count']['gauge_fixed_count'],expected[row['alphabet']].get(row['period'],0))
            self.assertEqual(row['training_count']['ungauged_count'],26*row['training_count']['gauge_fixed_count'])
            models=[row['training']]
            if row['second_block_evaluated']:
                second+=1;models.append(row['full'])
                self.assertEqual(row['full_count']['gauge_fixed_count'],0)
                for pred in row['first_stage_existing_glyph_predictions']:
                    self.assertEqual(sum(pred['counts_by_cipher_value']),row['training_count']['gauge_fixed_count'])
            for m in models:
                g=m['graph']
                self.assertEqual(g['independent_cycle_checks'],len(m['edges'])-len(m['node_labels'])+g['component_count'])
                cert=g['first_conflict']
                if cert is None:continue
                edge=m['edges'][cert['closing_edge_index']]
                self.assertEqual(cert['required_delta'],edge['delta'])
                total=0;current=edge['u']
                for step in cert['tree_path']:
                    e=m['edges'][step['edge_index']]
                    self.assertEqual(step['source'],current);current=step['target']
                    delta=e['delta'] if (step['source'],step['target'])==(e['u'],e['v']) else -e['delta']
                    self.assertEqual(step['potential_difference_mod'],delta%26);total+=delta
                self.assertEqual(current,edge['v'])
                self.assertEqual(total%26,cert['implied_delta'])
                self.assertEqual((total-edge['delta'])%26,cert['residual'])
                self.assertNotEqual(cert['residual'],0)
        self.assertEqual(second,10)
        import hashlib
        for path,digest in r['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),digest)

    def test_budget_failure_is_unresolved_not_zero(self):
        m=model([(0,'a',0),(1,'b',0),(3,'c',2)],2,4)
        with self.assertRaises(TimeoutError):count_injections(m,max_states=0)

if __name__=='__main__':unittest.main()
