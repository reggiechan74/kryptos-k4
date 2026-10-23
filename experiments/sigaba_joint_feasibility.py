"""Exact static-index quotient and synthetic-only controller resource assessment."""
import argparse,hashlib,importlib.util,itertools,json,time
from collections import Counter
from pathlib import Path
import sigaba_csp889 as sig
import sigaba_state_inference as state
ROOT=sig.ROOT

def run():
    d,t,groups=sig.prepare();start=time.monotonic();classes=Counter();connected=Counter();mask_hist=Counter();collector=Counter(d['collector'])
    for pos in itertools.product(range(10),repeat=5):
        if time.monotonic()-start>30:raise TimeoutError('index quotient incomplete: budget-unresolved')
        mapping=[]
        for x in range(10):
            for j in range(5):x=t['index'][j][0][0][pos[j]][x]
            mapping.append(d['magnets'][x])
        assert sorted(Counter(mapping).values())==[2]*5
        classes[tuple(mapping)]+=1;connected[tuple(mapping[1:])]+=1
    assert len(classes)==len(connected)
    digest=hashlib.sha256()
    for h,multiplicity in sorted(classes.items()):
        digest.update(json.dumps([h,multiplicity],separators=(',',':')).encode()+b'\n')
        capacities=[sum(collector[i] for i in range(10) if h[i]==j) for j in range(5)]
        masks=[mask for mask in range(1,31) if sum(capacities[j] for j in range(5) if mask>>j&1)>=4]
        assert all(1<=mask.bit_count()<=4 for mask in masks) if hasattr(int,'bit_count') else True
        mask_hist[len(masks)]+=1
    quotient_seconds=time.monotonic()-start
    counter=[0,0,0];seen=set()
    for _ in range(26**3):
        seen.add(tuple(counter))
        if counter[0]==14:
            if counter[1]==14:counter[2]=(counter[2]-1)%26
            counter[1]=(counter[1]-1)%26
        counter[0]=(counter[0]-1)%26
    assert len(seen)==26**3 and counter==[0,0,0]
    bench=[]
    p=list((sig.AZ*4)[:97]);p[21:34]='EASTNORTHEAST';p[63:74]='BERLINCLOCK';p=''.join(p);known={i:sig.AZ.index(x) for i,x in enumerate('EASTNORTHEAST',21)}
    start=time.monotonic()
    for group in groups[:10]:
        seed=(3,5,7,11,13);k=sig.key(group['layout'],0,*group['aliases'][0]);k['cipherposition']=''.join(sig.AZ[x] for x in seed)
        cipher=sig.Machine(k,d,t).crypt(p);clock=time.monotonic();joined=list(state.join_states(known,[sig.AZ.index(x) for x in cipher],group,t));elapsed=time.monotonic()-clock
        assert seed in joined;bench.append(dict(seconds=elapsed,joined_states=len(joined),truth_retained=True))
        if time.monotonic()-start>30:raise TimeoutError('synthetic benchmark budget-unresolved')
    product=2*26**5*len(classes);per=sum(x['seconds'] for x in bench)/len(bench)
    return dict(id='SIGABA-JOINT-FEASIBILITY-003',K4_evaluations=0,index_position_tuples=10**5,distinct_magnet_functions=len(classes),connected_digit_functions=len(connected),class_multiplicities={str(k):v for k,v in Counter(classes.values()).items()},classes_sha256=digest.hexdigest(),allowed_mask_relaxation_class_counts={str(k):v for k,v in mask_hist.items()},quotient_seconds=quotient_seconds,control_start_tuples=26**5,moving_control_cycle_states=len(seen),two_layout_quotient_controller_descriptions=product,raw_full_machine_start_descriptions=str(2*(26**5)**2*10**5),synthetic_benchmarks=bench,empirical_join_seconds_per_schedule=per,naive_projected_seconds=product*per,projection_is_lower_bound=False,installed_constraint_backends={name:importlib.util.find_spec(name) is not None for name in ('z3','ortools')},status='not_implemented_budget_unresolved',interpretation='Static-index aliases are exactly collapsed, but remaining joint controller inference is not implemented. This timing projection is not an impossibility proof or a K4 exclusion. Arbitrary feasible masks relax rather than implement authentic control dynamics.',source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),ROOT/'research/SIGABA-JOINT-FEASIBILITY-SPEC.md',ROOT/'experiments/sigaba_csp889.py',ROOT/'experiments/sigaba_state_inference.py')})
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();Path(a.output).write_text(json.dumps(run(),indent=2)+'\n')
