"""Complete tiny truth and independent explicit state-graph controls."""
import itertools,json,tempfile,hashlib
from pathlib import Path
import sigaba_unknown_anchor_collector as new
import sigaba_compressed_ownership as old
from sigaba_compact_domain import legacy
import sigaba_joint_toy as toy
import sigaba_joint_toy_oracle as oracle


def relation(result):
    out={}
    for row in legacy(result)['relations']:
        for rel in row['relations']:
            for h in toy.bits(int(rel['index_classes'],16)):
                key=tuple(row['control']),h
                if key in out:raise AssertionError('duplicate owner')
                out[key]=(int(rel['cipher_starts'],16),tuple(rel['final_offsets']))
    return out


def explicit_roots(f,observations,control,max_passes=8):
    m=toy.Model(f);start,block=new.first_block(observations)
    allstates=list(itertools.product(range(m.q),repeat=m.r));layers=[]
    for t,pairs in block:
        valid=set()
        for state in allstates:
            good=True
            for p,c in pairs:
                for j,s in enumerate(state):p=oracle.wire(f['cipher'][j],s,p)
                if p!=c:good=False;break
            if good:valid.add(state)
        layers.append(valid)
    if not layers:return set(allstates)
    digits=m.digits(control,block[-1][0]+1);inputs=digits[start:start+len(block)-1];allowed={}
    for B in inputs:
        allowed[B]={sum(1<<j for j in {mapping[x] for x in B}) for mapping in m.maps}
    for _ in range(max_passes):
        previous=[set(x) for x in layers];old={B:set(ms) for B,ms in allowed.items()}
        for backward in (True,False):
            common={B:set(ms) for B,ms in allowed.items()}
            for i in (range(len(inputs)-1,-1,-1) if backward else range(len(inputs))):
                B=inputs[i];sources=set();targets=set();local=set()
                for u in layers[i]:
                    for mask in allowed[B]:
                        v=tuple((x-((mask>>j)&1))%m.q for j,x in enumerate(u))
                        if v in layers[i+1]:sources.add(u);targets.add(v);local.add(mask)
                common[B]&=local
                if backward:layers[i]&=sources
                else:layers[i+1]&=targets
            for B in allowed:allowed[B]&=common[B]
            if any(not ms for ms in allowed.values()):return set()
        if layers==previous and allowed==old:break
    return layers[0]


def run():
    results=[];graph_comparisons=0;truth_streams=0;budget=toy.Budget(60,256<<20)
    for q in (2,3):
        for variant in (0,1):
            f=toy.fixture(q,3,variant=variant,mask='short');plant=f['plant'];cipher=oracle.simulate(f,f['plaintext'],plant['control'],plant['index'],plant['cipher'])
            # Consecutive block at a delayed absolute time; multiple initial roots.
            observations=[(t,f['plaintext'][t],cipher[t]) for t in range(2,6)]
            for control in itertools.product(range(q),repeat=3):
                m=toy.Model(f);pred=new.ReservedPredicates(m,budget,0)
                got,receipt=new.root_support(m,observations,m.digits(control,6),budget,pred)
                expected=explicit_roots(f,observations,control)
                states={toy.unpack(i,q,3) for i in toy.bits(got)}
                assert states==expected;graph_comparisons+=1
            for mask in ('empty','short','long'):
                f=toy.fixture(q,3,variant=variant,mask=mask);plant=f['plant'];cipher=oracle.simulate(f,f['plaintext'],plant['control'],plant['index'],plant['cipher']);obs=[(i,f['plaintext'][i],cipher[i]) for i in f['observed_positions']]
                baseline=old.solve(toy.Model(f),obs,budget);integrated=new.solve(toy.Model(f),obs,budget)
                assert baseline['completed'] and integrated['completed']
                assert relation(baseline)==relation(integrated)
                with tempfile.TemporaryDirectory(prefix='k4-coupled-truth-') as td:
                    a=Path(td)/'solver';b=Path(td)/'oracle'
                    x=toy.write_keys(legacy(integrated),f,a,budget);y=oracle.truth(f,obs,b,budget.check,toy.Limit)
                    assert a.read_bytes()==b.read_bytes();truth_streams+=1
                plant_h=toy.Model(f).class_of[tuple(plant['index'])]
                seed=0
                for v in plant['cipher']:seed=seed*q+v
                assert relation(integrated)[tuple(plant['control']),plant_h][0]>>seed&1
                results.append(dict(q=q,variant=variant,mask=mask,complete_raw_key_count=integrated['exact_raw_key_count'],stream_sha256=x['sha256'],full_relations_equal=True,independent_full_raw_stream_equal=True,plant_included=True))
    # Conflicting observations must not become a spurious compatible anchor merge.
    f=toy.fixture(3,3);zero=new.solve(toy.Model(f),[(2,0,0),(2,0,1)],budget)
    assert zero['completed'] and zero['exact_raw_key_count']=='0'
    return dict(id='CSP889-COUPLED-024-CONTROLS',completed=True,implicit_vs_explicit_graph_comparisons=graph_comparisons,complete_raw_truth_streams=truth_streams,fixtures=results,contradiction_control_passed=True,budget=budget.receipt(),K4_evaluations=0)
