import filecmp,itertools,json,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import sigaba_joint_toy as s
import sigaba_joint_toy_oracle as o
class CoupledToyTests(unittest.TestCase):
    def test_complete_small_relation_equals_raw_truth_bytes(self):
        for q in (2,3):
            f=s.fixture(q,3);p=f['plant'];cipher=o.simulate(f,f['plaintext'],p['control'],p['index'],p['cipher']);obs=[(i,f['plaintext'][i],cipher[i]) for i in (2,3,6,9)];b=s.Budget(30);r=s.solve(f,obs,b)
            with tempfile.TemporaryDirectory() as td:
                a=Path(td)/'a';z=Path(td)/'z';a_count=s.write_keys(r,f,a,b);truth=o.truth(f,obs,z,b.check,s.Limit)
                self.assertTrue(filecmp.cmp(a,z,shallow=False));self.assertEqual(a_count['count'],int(truth['raw_key_count']))
    def test_empty_and_inconsistent_sets_are_exact(self):
        f=s.fixture(2,3);self.assertEqual(int(s.solve(f,[])['exact_raw_key_count']),2**6*36)
        r=s.solve(f,[(2,0,0),(2,0,1)]);self.assertTrue(r['completed']);self.assertEqual(r['exact_raw_key_count'],'0')
    def test_merging_preserves_joint_correlations(self):
        nodes={};s.merge(nodes,(0,0,0),1,1);s.merge(nodes,(0,0,0),2,2)
        self.assertEqual(len(nodes),2);self.assertEqual(nodes[((0,0,0),1)],1);self.assertEqual(nodes[((0,0,0),2)],2)
        s.merge(nodes,(0,0,0),1,4);self.assertEqual(nodes[((0,0,0),1)],5)
    def test_predicates_match_every_seed_without_sampling(self):
        f=s.fixture(4,3);m=s.Model(f);b=s.Budget(30);pred=s.Predicates(m,b,cap=0);delta=(1,2,3)
        for p,c in ((0,1),(2,3)):
            got=set(s.bits(pred.get(delta,p,c)));expected=set()
            for i,seed in enumerate(itertools.product(range(4),repeat=3)):
                x=p
                for j in range(3):x=o.wire(f['cipher'][j],(seed[j]+delta[j])%4,x)
                if x==c:expected.add(i)
            self.assertEqual(got,expected)
        self.assertEqual(pred.cache_bytes,0)
    def test_reachable_index_aliases_and_continuous_control(self):
        f=s.fixture(5,3);m=s.Model(f);self.assertEqual(sum(map(len,m.aliases)),36)
        for ctl in [(0,1,2),(4,3,2)]:
            digits=m.digits(ctl,97)
            for h,aliases in enumerate(m.aliases):
                delta=[0]*3;observed=[]
                for row in digits:
                    observed.append(tuple(delta));mask=next(mask for mask,domain in m.mask_groups(row) if domain>>h&1)
                    delta=[(x-((mask>>j)&1))%5 for j,x in enumerate(delta)]
                self.assertEqual(observed,o.schedule(f,ctl,aliases[0],97))
    def test_budget_never_becomes_a_false_negative(self):
        r=s.solve(s.fixture(3,3),[],s.Budget(seconds=-1));self.assertFalse(r['completed']);self.assertIsNone(r['exact_raw_key_count']);self.assertEqual(r['control_starts_completed'],0)
