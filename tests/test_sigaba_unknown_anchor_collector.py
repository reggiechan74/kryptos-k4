import itertools,json,sys,types,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import sigaba_unknown_anchor_collector as n
import sigaba_unknown_anchor_controls as control
import sigaba_joint_toy as t
import sigaba_joint_toy_oracle as oracle
import sigaba_compressed_ownership as baseline

class UnknownAnchorCollectorTests(unittest.TestCase):
    def test_complete_tiny_truth_and_explicit_graphs(self):
        r=control.run()
        self.assertEqual(r['implicit_vs_explicit_graph_comparisons'],70)
        self.assertEqual(r['complete_raw_truth_streams'],12)
        self.assertTrue(all(f['plant_included'] and f['full_relations_equal'] for f in r['fixtures']))

    def test_disconnected_edge_support_is_rejected(self):
        q=3
        cf=[[[ (p+s)%q for p in range(q)] for s in range(q)]]
        cb=[[[ (p-s)%q for p in range(q)] for s in range(q)]]
        m=types.SimpleNamespace(q=q,r=1,cf=cf,cb=cb,maps=[(0,)],mask_groups=lambda B:[(1,1)])
        b=t.Budget(10);pred=n.ReservedPredicates(m,b,0)
        bad,_=n.root_support(m,[(0,0,0),(1,0,2),(2,0,0)],[(0,)]*3,b,pred)
        good,_=n.root_support(m,[(0,0,0),(1,0,2),(2,0,1)],[(0,)]*3,b,pred)
        self.assertEqual(bad,0);self.assertEqual(good,1)

    def test_signs_and_reverse_coordinate_movement(self):
        m=types.SimpleNamespace(r=3,rev=[[0,1,0]])
        self.assertEqual(n.step(m,7),(-1,1,-1))
        self.assertEqual(n.step(m,2),(0,1,0))
        f=t.fixture(3,3,mask='short');plant=f['plant'];c=oracle.simulate(f,f['plaintext'],plant['control'],plant['index'],plant['cipher']);obs=[(i,f['plaintext'][i],c[i]) for i in f['observed_positions']]
        expected=control.relation(baseline.solve(t.Model(f),obs,t.Budget(10)))
        for enabled in (False,True):self.assertEqual(control.relation(n.solve(t.Model(f),obs,t.Budget(10),filter_enabled=enabled)),expected)

    def test_bad_shared_prefix_and_removed_gap_change_complete_relations(self):
        f=t.fixture(3,3,mask='short');p=f['plant'];cipher=oracle.simulate(f,f['plaintext'],p['control'],p['index'],p['cipher']);obs=[(i,f['plaintext'][i],cipher[i]) for i in f['observed_positions']]
        expected=control.relation(n.solve(t.Model(f),obs,t.Budget(10)))
        original=n.prefix_delta
        with patch.object(n,'prefix_delta',side_effect=lambda m,d,h,a,b:original(m,d,0,a,b)):
            wrong=n.solve(t.Model(f),obs,t.Budget(10))
        self.assertNotEqual(control.relation(wrong),expected)
        broken=t.Model(f);digits=broken.digits
        def skipped(q,length):
            result=digits(q,length)
            if length>5:result[5]=()
            return result
        broken.digits=skipped
        self.assertNotEqual(control.relation(n.solve(broken,obs,t.Budget(10))),expected)

    def test_limit_is_unresolved_not_rejection_and_restricted_starts_blocked(self):
        f=t.fixture(2,3)
        result=n.solve(t.Model(f),[(2,0,0)],t.Budget(-1))
        self.assertFalse(result['completed']);self.assertIsNone(result['exact_raw_key_count'])
        with self.assertRaises(ValueError):n.solve(t.Model(f),[(2,0,0)],t.Budget(10),full_initial_domain=False)
