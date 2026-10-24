"""Frozen matched synthetic benchmark; local only, no K4 reader or publication."""
import argparse,datetime,hashlib,json,subprocess,sys,time
from pathlib import Path
import sigaba_joint_toy as toy
import sigaba_real_adapter as real
import sigaba_compressed_ownership as baseline
import sigaba_unknown_anchor_collector as integrated
import sigaba_unknown_anchor_controls as controls
from run_io import RunSnapshot,specification,json_bytes,atomic_write
ROOT=Path(__file__).resolve().parents[1]
PIN=['experiments/sigaba_unknown_anchor_collector.py','experiments/sigaba_unknown_anchor_controls.py','experiments/run_sigaba_unknown_anchor.py','experiments/sigaba_compressed_ownership.py','experiments/sigaba_compact_domain.py','experiments/sigaba_sparse_ownership.py','experiments/sigaba_torus.py','experiments/sigaba_first_observation.py','experiments/sigaba_real_adapter.py','experiments/sigaba_joint_toy.py','experiments/sigaba_joint_toy_oracle.py','experiments/sigaba_csp889.py','data/sigaba-csp889-v1.json','research/SIGABA-UNKNOWN-ANCHOR-COLLECTOR-SPEC.md']
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def hashes():return {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in PIN}
def child(backend,case):
 start=utc();budget=toy.Budget(60);fixture=real.fixture(case);model=real.RealModel(budget=budget)
 prior=json.loads((ROOT/f'results/sigaba-real-adapter/case-{case}.json').read_text())['fixture'];prior['observations']=[tuple(x) for x in prior['observations']];assert fixture==prior
 assert model.stream(fixture['plaintext'],fixture['key'])==fixture['ciphertext']
 assert real.physical(fixture['plaintext'],fixture['key'])==fixture['ciphertext']
 result=(baseline if backend=='baseline' else integrated).solve(model,fixture['observations'],budget)
 return dict(id='CSP889-COUPLED-024',backend=backend,case=case,started_at_utc=start,finished_at_utc=utc(),fixture=fixture,solver=result,source_sha256=hashes(),complete_unknown_cipher_start_domain=True,original_controller_start_domain=26**5,reachable_shared_index_maps=len(model.maps),raw_aliases=sum(map(len,model.aliases)),independent_full_real_compatible_set_validation=False,real_sized_gate_passed=False,K4_evaluations=0,historical_wiring_limit='Pinned simulator wirings and conventions, not authenticated surviving hardware or creator initialization')

def main():
 p=argparse.ArgumentParser();p.add_argument('--child',choices=('baseline','integrated'));p.add_argument('--case',type=int,choices=(0,1));p.add_argument('--output',required=True);p.add_argument('--spec-commit');p.add_argument('--kind',choices=('original','replay'),default='replay');a=p.parse_args()
 if a.child:
  value=child(a.child,a.case);atomic_write(a.output,json_bytes(value));return
 if not a.spec_commit:p.error('--spec-commit required')
 spec=specification(a.spec_commit,Path('research/SIGABA-UNKNOWN-ANCHOR-COLLECTOR-SPEC.md'))
 with RunSnapshot(a.output,'CSP889-COUPLED-024',spec,execution_kind=a.kind) as snapshot:
  started=utc();check=controls.run();assert check['completed']
  vectors=[]
  for vector in real.sig.data()['vectors']:
   assert real.sig.Machine(vector).crypt(vector['input'])==vector['output']
   assert real.physical(vector['input'],vector)==vector['output'];vectors.append(vector['n'])
  check.update(started_at_utc=started,finished_at_utc=utc(),published_simulator_vectors=vectors,source_sha256=hashes());snapshot.write('controls.json',json_bytes(check))
  summaries=[]
  for backend in ('baseline','integrated'):
   for case in (0,1):
    name=f'{backend}-case-{case}.json';path=snapshot.stage/name;start=utc()
    try:
     subprocess.run([sys.executable,__file__,'--child',backend,'--case',str(case),'--output',str(path)],check=True,timeout=65)
     value=json.loads(path.read_text())
    except subprocess.TimeoutExpired:
     value=dict(id='CSP889-COUPLED-024',backend=backend,case=case,started_at_utc=start,finished_at_utc=utc(),completed=False,reason='watchdog_unresolved',exact_raw_key_count=None,source_sha256=hashes(),real_sized_gate_passed=False,K4_evaluations=0)
    snapshot.write(name,json_bytes(value));solver=value.get('solver',value);summary=dict(backend=backend,case=case,completed=solver.get('completed'),reason=solver.get('reason'),controllers_completed=solver.get('control_starts_completed'),filters_completed=solver.get('filters_completed'),filter_progress=solver.get('filter_progress'),budget=solver.get('budget'));summaries.append(summary);print(json.dumps(summary),flush=True)
  snapshot.write('summary.json',json_bytes(dict(id='CSP889-COUPLED-024',cases=summaries,matched_fixtures_and_resource_caps=True,real_sized_gate_passed=False,K4_evaluations=0)))
 print(snapshot.final,flush=True)
if __name__=='__main__':main()
