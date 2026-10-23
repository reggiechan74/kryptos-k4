"""Complete predicate identity controls, separate from coupled benchmarks."""
import argparse,hashlib,itertools,json,time
from pathlib import Path
import sigaba_joint_toy as b
import sigaba_joint_toy_oracle as physical
from sigaba_torus import TorusPredicates

def check():
    start=time.monotonic();budget=b.Budget(120);rows=[];direct_checks=0;predicates=0
    for q,r in [(2,3),(3,3),(4,3),(5,3),(2,5),(3,5)]:
        f=b.fixture(q,r);m=b.Model(f);old=b.Predicates(m,budget);new=TorusPredicates(m,budget)
        for delta in itertools.product(range(q),repeat=r):
            for p,c in itertools.product(range(q),repeat=2):
                budget.check(force=True);expected=0
                for number,seed in enumerate(itertools.product(range(q),repeat=r)):
                    x=p
                    for j in range(r):x=physical.wire(f['cipher'][j],(seed[j]+delta[j])%q,x)
                    if x==c:expected|=1<<number
                    direct_checks+=1
                    if direct_checks>2000000:raise b.Limit('identity_control_cap_unresolved')
                assert new.get(delta,p,c)==expected==old.get(delta,p,c);predicates+=1
        rows.append(dict(q=q,rotors=r,complete_offsets=q**r,complete_symbol_pairs=q*q,base_builds=new.builds,all_predicates_equal=True))
    f=b.fixture(2,3);t=TorusPredicates(b.Model(f),budget,cap=0);subset_checks=0
    for subset in range(1<<(2**3)):
        for delta in itertools.product(range(2),repeat=3):
            expected=0
            for actual in b.bits(subset):
                coordinates=b.unpack(actual,2,3);initial=tuple((x-d)%2 for x,d in zip(coordinates,delta));number=0
                for x in initial:number=number*2+x
                expected|=1<<number
            assert t.translate(subset,delta)==expected
            assert t.translate(t.translate(subset,delta),tuple(-x for x in delta))==subset;subset_checks+=1
    return dict(completed=True,rows=rows,predicates_compared=predicates,direct_seed_checks=direct_checks,all_subset_and_inverse_checks=subset_checks,budget=budget.receipt(),K4_evaluations=0)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();r=check();r['source_sha256']={str(p.relative_to(b.ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),b.ROOT/'experiments/sigaba_torus.py',b.ROOT/'experiments/sigaba_joint_toy.py',b.ROOT/'experiments/sigaba_joint_toy_oracle.py',b.ROOT/'research/SIGABA-TORUS-SPEC.md',b.ROOT/'data/sigaba-joint-toy-v1.json')};Path(a.output).write_text(json.dumps(r,indent=2)+'\n')
