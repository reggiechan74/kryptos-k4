import itertools,random,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import sigaba_joint_toy as t
from sigaba_sparse_ownership import ReservedPredicates
from sigaba_byte_mask_predicates import ByteMaskPredicates,periodic_low
import audit_sigaba_unknown_anchor_dynamic_controls as dynamic
class ByteMaskTests(unittest.TestCase):
    def test_all_small_masks_and_translation_preimages(self):
        rng=random.Random(2026102424)
        for q in (2,3):
            m=t.Model(t.fixture(q,3));fast=ByteMaskPredicates(m,t.Budget(20),0);old=ReservedPredicates(m,t.Budget(20),0)
            subsets=range(256) if q==2 else [0,(1<<27)-1]+[1<<i for i in range(27)]+[rng.getrandbits(27) for _ in range(256)]
            for delta in itertools.product(range(q),repeat=3):
                for subset in subsets:
                    self.assertEqual(fast.translate(subset,delta),old.translate(subset,delta))
                    expected=0
                    for i in range(q**3):
                        state=t.unpack(i,q,3);j=0
                        for x,d in zip(state,delta):j=j*q+(x+d)%q
                        if subset>>j&1:expected|=1<<i
                    self.assertEqual(fast.translate(subset,delta),expected)
    def test_periodic_formula_and_real_boundary_bits(self):
        for q in (2,3,5):
            n=q**3;full=(1<<n)-1
            for j in range(3):
                stride=q**(2-j);period=q*stride
                for d in range(1,q):self.assertEqual(periodic_low(n,period,d*stride),(full//((1<<period)-1))*((1<<(d*stride))-1))
        n=26**5
        for j in range(5):
            stride=26**(4-j);period=26*stride
            for d in (1,25):
                shift=d*stride;raw=periodic_low(n,period,shift).to_bytes((n+7)//8,'little')
                for k in (0,1,n//period-1):
                    for value in (0,shift-1,shift,period-1):
                        i=k*period+value
                        if 0<=i<n:self.assertEqual((raw[i//8]>>(i%8))&1,int(i%period<shift))
    def test_dynamic_collector_complete_truth(self):
        r=dynamic.run();self.assertEqual(r['complete_raw_truth_streams'],12);self.assertEqual(r['varying_fixture_count'],4);self.assertEqual(r['independent_controller_traces'],124);self.assertEqual(r['implicit_explicit_varying_input_graphs'],124)
