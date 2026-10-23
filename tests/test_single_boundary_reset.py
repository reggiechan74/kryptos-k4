from pathlib import Path
import json
import sys
import time
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments'))
from single_boundary_reset import (AZ,ALPHABETS,BOUNDARIES,case_id,canonical_phase,
    configurations,fit_recurrence_seeds,generator,internal_edges,known,
    parity_conflict,phase_constraints,phases,recency_oracle,recurrence_crypt,split_transform)


class SingleBoundaryResetTests(unittest.TestCase):
    def test_boundary_definition_and_same_state(self):
        cfg=(AZ,AZ)
        self.assertEqual(split_transform('DB',cfg,None),'DA')
        self.assertEqual(split_transform('DB',cfg,1),'DB')
        self.assertEqual(generator('DB',cfg,1),'DB')
        self.assertEqual(recency_oracle('DB',cfg,1),'DB')
        self.assertEqual(len(BOUNDARIES),97)
        self.assertEqual(BOUNDARIES[-1],96)

    def test_reset_oracles_with_actual_crib_structure(self):
        k=known(json.loads((ROOT/'data/k4.json').read_text()))
        p=list((AZ*4)[:97])
        for i,c in k.items():p[i]=c
        p=''.join(p)
        for cfg in configurations():
            for b in (None,1,21,63,74,96):
                c=generator(p,cfg,b)
                self.assertEqual(recency_oracle(c,cfg,b),p)
                self.assertEqual(split_transform(c,cfg,b,True),p)

    def test_nonunit_seed_filter_matches_direct_truth(self):
        p=(AZ*4)[:97]
        for a in (0,2,13,25):
            for b in (None,21,63):
                params=(a,4,16,7);c=recurrence_crypt(p,AZ,params,b)
                train={i:p[i] for i in range(21,34)}
                fitted=fit_recurrence_seeds(c,train,AZ,params[:3],b)
                truth=[seed for seed in range(26) if all(recurrence_crypt(c,AZ,(a,4,16,seed),b,True)[i]==x for i,x in train.items())]
                self.assertEqual(fitted,truth)
                self.assertIn(7,fitted)

    def test_parity_certificate_does_not_cross_a_removed_edge(self):
        edges=[dict(source=22,target=23,key=11,cipher=11,required=25),
               dict(source=23,target=24,key=25,cipher=17,required=2)]
        self.assertIsNotNone(parity_conflict(edges,None))
        self.assertIsNone(parity_conflict(edges,23))
        self.assertIsNone(parity_conflict(edges,24))

    def test_phase_aliases_and_key_negation(self):
        for period in range(1,13):
            self.assertEqual(phases(period,None),phases(period,period))
        self.assertEqual(canonical_phase((4,2,4,1)),(0,1,0,2))
        p=(AZ*4)[:97];period=8;b=21;key=list(range(8));schedule=phases(period,b)
        plus=''.join(AZ[(AZ.index(x)+key[schedule[i]])%26] for i,x in enumerate(p))
        minus=''.join(AZ[(AZ.index(x)-(-key[schedule[i]])%26)%26] for i,x in enumerate(p))
        self.assertEqual(plus,minus)


if __name__=='__main__':unittest.main()
