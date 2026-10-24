"""Supplementary after-benchmark controls: changing collector inputs, complete truth."""
import hashlib,itertools,json,tempfile
from pathlib import Path
from unittest.mock import patch
import sigaba_joint_toy as t
import sigaba_joint_toy_oracle as oracle
import sigaba_compressed_ownership as baseline
import sigaba_unknown_anchor_collector as n
import sigaba_unknown_anchor_controls as original
from sigaba_compact_domain import legacy
from sigaba_byte_mask_predicates import ByteMaskPredicates

def independent_digits(f,control,length):
    pos=list(control);out=[]
    for _ in range(length):
        hits=[]
        for x in f['pulses']:
            for j in range(f['r']-1,-1,-1):x=oracle.wire(f['control'][j],pos[j],x,True)
            hits.append(f['collector'][x])
        out.append(tuple(sorted(set(hits))));oracle.tick_control(pos,f['q'],f['notch'])
    return out

def run():
    budget=t.Budget(60,256<<20);records=[];traces=0;graphs=0
    for q,pulses in ((2,[0]),(3,[0]),(3,[0,1])):
        for variant in (0,1):
            f=t.fixture(q,3,variant,mask='short');f['pulses']=pulses
            for control in itertools.product(range(q),repeat=3):
                m=t.Model(f);a=m.digits(control,97);assert a==independent_digits(f,control,97);traces+=1
                plant=f['plant'];c=oracle.simulate(f,f['plaintext'],plant['control'],plant['index'],plant['cipher']);obs=[(i,f['plaintext'][i],c[i]) for i in range(2,6)]
                roots,_=n.root_support(m,obs,a,budget,ByteMaskPredicates(m,budget,0));expected=original.explicit_roots(f,obs,control)
                assert {t.unpack(i,q,3) for i in t.bits(roots)}==expected;graphs+=1
            for mask in ('short','long'):
                f=t.fixture(q,3,variant,mask=mask);f['pulses']=pulses;plant=f['plant'];c=oracle.simulate(f,f['plaintext'],plant['control'],plant['index'],plant['cipher']);obs=[(i,f['plaintext'][i],c[i]) for i in f['observed_positions']]
                normal=baseline.solve(t.Model(f),obs,budget)
                with patch.object(n,'ReservedPredicates',ByteMaskPredicates),patch.object(baseline,'ReservedPredicates',ByteMaskPredicates):
                    fast=baseline.solve(t.Model(f),obs,budget);integrated=n.solve(t.Model(f),obs,budget)
                assert all(r['completed'] for r in (normal,fast,integrated));assert original.relation(normal)==original.relation(fast)==original.relation(integrated)
                with tempfile.TemporaryDirectory(prefix='k4-dynamic-truth-') as td:
                    a=Path(td)/'solver';b=Path(td)/'physical';x=t.write_keys(legacy(integrated),f,a,budget);y=oracle.truth(f,obs,b,budget.check,t.Limit);assert a.read_bytes()==b.read_bytes()
                varying=max(len(set(t.Model(f).digits(control,97))) for control in itertools.product(range(q),repeat=3))
                records.append(dict(q=q,pulses=pulses,variant=variant,mask=mask,complete_raw_count=integrated['exact_raw_key_count'],stream_sha256=x['sha256'],baseline_integrated_byte_backend_sets_equal=True,max_distinct_collector_sets=varying))
    assert any(r['max_distinct_collector_sets']>1 for r in records)
    return dict(varying_fixture_count=sum(r['max_distinct_collector_sets']>1 for r in records),id='COUPLED-024-DYNAMIC-CONTROLS',completed=True,fixtures=records,independent_controller_traces=traces,implicit_explicit_varying_input_graphs=graphs,complete_raw_truth_streams=len(records),budget=budget.receipt(),K4_evaluations=0,chronology='Supplement after original resource benchmarks; no production model/benchmark fixture changed')
