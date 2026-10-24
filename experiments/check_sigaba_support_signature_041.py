"""Independent complete compatible relations and cache invariance before benchmarking."""
import datetime,hashlib,itertools,json,tempfile
from pathlib import Path
import sigaba_support_signature_041 as new
import sigaba_unknown_anchor_collector as old
import sigaba_unknown_anchor_controls as control
import sigaba_joint_toy as toy
import sigaba_joint_toy_oracle as oracle
from sigaba_compact_domain import legacy
ROOT=Path(__file__).resolve().parents[1]
def dynamic_controls(budget):
 from sigaba_byte_mask_predicates import ByteMaskPredicates
 from unittest.mock import patch
 import audit_sigaba_unknown_anchor_dynamic_controls as dynamic
 roots=0;streams=0;varied=0
 for q,pulses in ((2,[0]),(3,[0]),(3,[0,1])):
  for variant in (0,1):
   f=toy.fixture(q,3,variant,mask='short');f['pulses']=pulses;m=toy.Model(f);cache=new.SupportCache();pred=ByteMaskPredicates(m,budget,0);plant=f['plant'];cipher=oracle.simulate(f,f['plaintext'],plant['control'],plant['index'],plant['cipher']);obs=[(i,f['plaintext'][i],cipher[i]) for i in range(2,6)]
   for controller in itertools.product(range(q),repeat=3):
    digits=m.digits(controller,97);assert digits==dynamic.independent_digits(f,controller,97);got,_=cache.evaluate(m,obs,digits,budget,pred);assert {toy.unpack(i,q,3) for i in toy.bits(got)}==control.explicit_roots(f,obs,controller);roots+=1
   for mask in ('short','long'):
    f=toy.fixture(q,3,variant,mask=mask);f['pulses']=pulses;plant=f['plant'];cipher=oracle.simulate(f,f['plaintext'],plant['control'],plant['index'],plant['cipher']);obs=[(i,f['plaintext'][i],cipher[i]) for i in f['observed_positions']]
    with patch.object(new,'ReservedPredicates',ByteMaskPredicates):value=new.solve(toy.Model(f),obs,budget)
    assert value['completed']
    with tempfile.TemporaryDirectory(prefix='sigaba-signature-varying-') as d:
     p=Path(d);toy.write_keys(legacy(value),f,p/'native',budget);oracle.truth(f,obs,p/'truth',budget.check,toy.Limit);assert (p/'native').read_bytes()==(p/'truth').read_bytes()
    streams+=1;varied+=max(len(set(toy.Model(f).digits(controller,97))) for controller in itertools.product(range(q),repeat=3))>1
 return dict(independent_controller_graphs=roots,full_raw_truth_streams=streams,varying_fixtures=varied)

def run():
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();rows=[];roots=0;hits=0;capcases=0;budget=toy.Budget(60,256<<20)
 for q in (2,3):
  for variant in (0,1):
   f=toy.fixture(q,3,variant=variant,mask='short');m=toy.Model(f);pred=old.ReservedPredicates(m,budget,0);cache=new.SupportCache();plant=f['plant'];cipher=oracle.simulate(f,f['plaintext'],plant['control'],plant['index'],plant['cipher']);observations=[(t,f['plaintext'][t],cipher[t]) for t in range(2,6)]
   for controller in itertools.product(range(q),repeat=3):
    digits=m.digits(controller,6);a,_=cache.evaluate(m,observations,digits,budget,pred);expected=control.explicit_roots(f,observations,controller);assert {toy.unpack(i,q,3) for i in toy.bits(a)}==expected;roots+=1
   hits+=cache.hits
   for mask in ('empty','short','long'):
    f=toy.fixture(q,3,variant=variant,mask=mask);plant=f['plant'];cipher=oracle.simulate(f,f['plaintext'],plant['control'],plant['index'],plant['cipher']);obs=[(i,f['plaintext'][i],cipher[i]) for i in f['observed_positions']];baseline=old.solve(toy.Model(f),obs,budget);assert baseline['completed'];expected=control.relation(baseline)
    for cap in (0,1,64<<20):
     value=new.solve(toy.Model(f),obs,budget,support_cache_cap=cap);assert value['completed'] and control.relation(value)==expected;capcases+=1
    with tempfile.TemporaryDirectory(prefix='sigaba-signature041-') as d:
     p=Path(d);a=toy.write_keys(legacy(value),f,p/'native',budget);b=oracle.truth(f,obs,p/'truth',budget.check,toy.Limit);assert (p/'native').read_bytes()==(p/'truth').read_bytes()
    rows.append(dict(q=q,variant=variant,mask=mask,full_raw_key_stream_sha256=a['sha256'],full_truth_equal=True,raw_count=value['exact_raw_key_count'],cache_metrics=value['support_cache']))
 supplement=dynamic_controls(budget)
 f=toy.fixture(3,3);z=new.solve(toy.Model(f),[(2,0,0),(2,0,1)],budget);assert z['completed'] and z['exact_raw_key_count']=='0'
 # Adversarial canonical signatures. These controllers are abstract necessary-filter inputs only.
 class Fake:
  def mask_groups(self,B):return [(1,1),(2,1)] if B!=(9,) else [(1,1)]
 m=Fake();cache=new.SupportCache();obs=[(i,0,0) for i in range(3)]
 a,_=cache.signature(m,obs,[(1,),(1,)],budget);b,_=cache.signature(m,obs,[(7,),(7,)],budget);c,_=cache.signature(m,obs,[(1,),(2,)],budget);d,_=cache.signature(m,obs,[(9,),(9,)],budget);assert a==b and a!=c and a!=d
 e,_=cache.signature(m,[(i,0,1) for i in range(3)],[(1,),(1,)],budget);assert e!=a
 try:cache.signature(Fake(),obs,[(1,),(1,)],budget)
 except ValueError:pass
 else:raise AssertionError('wrong model cache merge')
 return dict(id='SIGABA-SUPPORT-SIGNATURE-041-CONTROLS',started_at_utc=start,finished_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),complete=True,complete_independent_root_graphs=roots,root_cache_hits=hits,complete_raw_truth_streams=len(rows),complete_cap_invariance_cases=capcases,varying_input_supplement=supplement,rows=rows,contradiction_control=True,equality_partition_mask_observation_and_model_guards=True,budget=budget.receipt(),K4_evaluations=0)
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();r=run();Path(a.output).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='rows'}))
