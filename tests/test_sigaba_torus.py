import filecmp,itertools,json,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import sigaba_joint_toy as b
import sigaba_joint_toy_oracle as physical
import sigaba_compact_oracle as compact
from sigaba_torus import TorusPredicates
class TorusTests(unittest.TestCase):
    def test_translation_equals_direct_physical_positions(self):
        f=b.fixture(3,3);m=b.Model(f);guard=b.Budget(30);t=TorusPredicates(m,guard)
        for delta in itertools.product(range(3),repeat=3):
            for p,c in itertools.product(range(3),repeat=2):
                expected=0
                for number,seed in enumerate(itertools.product(range(3),repeat=3)):
                    x=p
                    for j in range(3):x=physical.wire(f['cipher'][j],(seed[j]+delta[j])%3,x)
                    if x==c:expected|=1<<number
                self.assertEqual(t.get(delta,p,c),expected)
        self.assertLessEqual(t.builds,9)
    def test_coupled_relations_unchanged_with_every_cache_policy(self):
        f=b.fixture(5,3);p=f['plant'];cipher=physical.simulate(f,f['plaintext'],p['control'],p['index'],p['cipher']);obs=[(i,f['plaintext'][i],cipher[i]) for i in (2,3,6,9)];old=b.solve(f,obs)
        for cap in (0,1024,64<<20):
            new=b.solve(f,obs,cache_cap=cap,predicate_factory=TorusPredicates);self.assertEqual(b.relation_masks(old),b.relation_masks(new));self.assertEqual(old['exact_raw_key_count'],new['exact_raw_key_count'])
    def test_compact_independent_truth_reconstructs_whole_key_set(self):
        for q in (2,3):
            f=b.fixture(q,3);p=f['plant'];cipher=physical.simulate(f,f['plaintext'],p['control'],p['index'],p['cipher']);obs=[(i,f['plaintext'][i],cipher[i]) for i in (2,3,6,9)];guard=b.Budget(30);r=b.solve(f,obs,predicate_factory=TorusPredicates);model=b.Model(f);domains=b.relation_masks(r)
            with tempfile.TemporaryDirectory() as td:
                a=Path(td)/'a';z=Path(td)/'z';production=compact.emit_rows(f,lambda ctl,ix:domains.get((ctl,model.class_of[ix]),0),a,guard.check,b.Limit);independent=compact.truth_rows(f,obs,z,guard.check,b.Limit)
                self.assertTrue(filecmp.cmp(a,z,shallow=False));self.assertEqual(production['raw_key_count'],independent['raw_key_count'])
        with self.assertRaises(ValueError):compact.compact_domains(b.fixture(5,3),[],lambda:None)
    def test_fixed_width_wrap_and_inverse(self):
        t=TorusPredicates(b.Model(b.fixture(2,3)),b.Budget(),cap=0)
        for value in range(256):
            for delta in itertools.product(range(2),repeat=3):self.assertEqual(t.translate(t.translate(value,delta),tuple(-x for x in delta)),value)
        with self.assertRaises(ValueError):t.translate(1<<8,(0,0,0))
        with self.assertRaises(ValueError):t.translate(-1,(0,0,0))
        self.assertEqual(t.cache_bytes,0)
