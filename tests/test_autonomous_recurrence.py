from pathlib import Path
import itertools
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments'))
from exact_linear import (solve_field,solve_ring,contains,field_vectors,ring_vectors,
                          canonical_affine,affine_key,affine_intersection,union_cardinality)
from autonomous_recurrence import keys,companion_keys,reachable_prefix,controls,analyze


class ExactAutonomousTests(unittest.TestCase):
    def test_field_inconsistency_certificate(self):
        a=[[1,1],[1,1]];b=[0,1];r=solve_field(a,b,2)
        self.assertEqual((r['rank'],r['augmented_rank']),(1,2))
        self.assertFalse(r['consistent'])
        w=r['contradiction']['equation_weights']
        self.assertTrue(all(sum(w[j]*a[j][i] for j in range(2))%2==0 for i in range(2)))
        self.assertEqual(sum(x*y for x,y in zip(w,b))%2,1)

    def test_field_basis_retains_all_singular_solutions(self):
        r=solve_field([[1,1,0]],[1],13)
        true={v for v in itertools.product(range(13),repeat=3) if (v[0]+v[1])%13==1}
        self.assertEqual(set(field_vectors(r)),true)
        self.assertEqual(r['cardinality'],169)
        self.assertTrue(all(contains(solve_ring([[1,1,0]],[1],26),[x%26 for x in v])
                            for v in [(1,0,3),(0,1,4),(14,13,2)]))

    def test_nonunit_mod26_and_square_free_oracle(self):
        self.assertEqual(set(ring_vectors(solve_ring([[2]],[0],26))),{(0,),(13,)})
        self.assertEqual(solve_ring([[2]],[1],26)['cardinality'],0)
        self.assertEqual(solve_ring([[13]],[0],26)['cardinality'],13)
        for q in (2,3,6,26):
            a=[[2,1],[0,2]];b=[1,2]
            exact={v for v in itertools.product(range(q),repeat=2) if all(sum(x*y for x,y in zip(row,v))%q==rhs%q for row,rhs in zip(a,b))}
            self.assertEqual(set(ring_vectors(solve_ring(a,b,q))),exact)

    def test_affine_union_exact_not_sum_and_canonical_gauge(self):
        spaces=[]
        for basis in ([[1,0]],[[0,1]],[[1,1]]):
            spaces.append([canonical_affine([0,0],basis,p) for p in (2,3)])
        count,_=union_cardinality(spaces)
        self.assertEqual(count,16)
        self.assertEqual(affine_key(canonical_affine([1,0],[[1,0]],3)),affine_key(canonical_affine([0,0],[[1,0]],3)))
        a=canonical_affine([0,1],[[1,0]],3);b=canonical_affine([1,0],[[0,1]],3)
        intersection=affine_intersection(a,b)
        self.assertEqual(intersection['point'],[1,1])
        self.assertEqual(intersection['cardinality'],1)

    def test_prefix_reachability_and_startup_alias(self):
        bad=reachable_prefix([1,0,0,0,0],[0,0],0,start=3,length=12)
        self.assertFalse(bad['reachable'])
        good=reachable_prefix([8]*13,[1,0],0)
        self.assertEqual(good['seed_cardinality'],26)
        self.assertEqual(good['same_rule_reduced_startup_seed_count'],1)
        self.assertFalse(good['all_reachable_seeds_globally_reduce'])

    def test_end_state_forecast_and_independent_companion(self):
        stream=companion_keys([1,7,3],[2,5,13],9,97)
        self.assertEqual(keys([1,7,3],[2,5,13],9,97),stream)
        forecast=keys(stream[21:34],[2,5,13],9,76)
        self.assertEqual(forecast,stream[21:])
        self.assertEqual(forecast[13:42],stream[34:63])
        self.assertEqual(forecast[42:53],stream[63:74])

    def test_all_literal_plants_and_independent_complete_small_rings(self):
        c=controls()
        self.assertEqual(c['literal_plant_count'],80)
        self.assertEqual(c['small_ring_count'],12)
        self.assertTrue(c['unreachable_internal_fit_rejected'])
        self.assertGreater(c['ambiguous_planted_prefixes'],0)
        self.assertTrue(all(x['exact_sets_equal'] for x in c['complete_small_ring_comparisons']))


if __name__=='__main__':unittest.main()
