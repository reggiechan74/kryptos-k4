"""Four frozen synthetic comparisons. Watchdog/timeout are unresolved, never empty."""
import argparse,datetime,hashlib,json,subprocess,sys
from pathlib import Path
from unittest.mock import patch
import sigaba_joint_toy as toy
import sigaba_real_adapter as real
import sigaba_unknown_anchor_collector as uncached
import sigaba_support_signature_041 as cached
from sigaba_byte_mask_predicates import ByteMaskPredicates
ROOT=Path(__file__).resolve().parents[1]
PIN=('research/SIGABA-SUPPORT-SIGNATURE-041-SPEC.md','experiments/sigaba_support_signature_041.py','experiments/run_sigaba_support_signature_041.py','experiments/sigaba_unknown_anchor_collector.py','experiments/sigaba_byte_mask_predicates.py','data/sigaba-csp889-v1.json')
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def hashes():return {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in PIN}
def child(backend,case):
 start=utc();budget=toy.Budget(60);fixture=real.fixture(case);model=real.RealModel(budget=budget);prior=json.loads((ROOT/f'results/sigaba-real-adapter/case-{case}.json').read_text())['fixture'];prior['observations']=[tuple(x) for x in prior['observations']];assert prior==fixture
 assert model.stream(fixture['plaintext'],fixture['key'])==fixture['ciphertext']==real.physical(fixture['plaintext'],fixture['key'])
 module=uncached if backend=='uncached' else cached
 with patch.object(module,'ReservedPredicates',ByteMaskPredicates):value=module.solve(model,fixture['observations'],budget)
 return dict(id='SIGABA-SUPPORT-SIGNATURE-041',backend=backend,case=case,started_at_utc=start,finished_at_utc=utc(),fixture=fixture,solver=value,source_sha256=hashes(),independent_full_real_compatible_set_validation=False,real_sized_gate_passed=False,K4_evaluations=0,historical_wiring_limit='Pinned simulator wiring, not authenticated hardware or creator initialization')
def main():
 p=argparse.ArgumentParser();p.add_argument('--child',choices=('uncached','cached'));p.add_argument('--case',type=int,choices=(0,1));p.add_argument('--output');a=p.parse_args()
 if a.child:Path(a.output).write_text(json.dumps(child(a.child,a.case),indent=2)+'\n');return
 controls=json.loads((ROOT/'results/SIGABA-SUPPORT-SIGNATURE-041-CONTROLS.json').read_text());assert controls['complete']
 vectors=[]
 for v in real.sig.data()['vectors']:
  assert real.sig.Machine(v).crypt(v['input'])==v['output']==real.physical(v['input'],v);vectors.append(v['n'])
 rows=[];start=utc()
 for case in (0,1):
  for backend in ('uncached','cached'):
   target=ROOT/f'results/SIGABA-SUPPORT-SIGNATURE-041-{backend}-case{case}.json';beg=utc()
   try:
    subprocess.run([sys.executable,__file__,'--child',backend,'--case',str(case),'--output',str(target)],check=True,timeout=65);value=json.loads(target.read_text())
   except (subprocess.TimeoutExpired,subprocess.CalledProcessError) as e:
    value=dict(id='SIGABA-SUPPORT-SIGNATURE-041',backend=backend,case=case,started_at_utc=beg,finished_at_utc=utc(),source_sha256=hashes(),solver=dict(completed=False,reason='watchdog_or_process_unresolved',internal_coverage_unknown=True),failure=str(e),real_sized_gate_passed=False,K4_evaluations=0);target.write_text(json.dumps(value,indent=2)+'\n')
   s=value['solver'];row=dict(backend=backend,case=case,complete=s['completed'],reason=s.get('reason'),controllers_completed=s.get('control_starts_completed'),requested=s.get('control_starts_requested'),budget=s.get('budget'),support_cache=s.get('support_cache'),receipt=str(target.relative_to(ROOT)));rows.append(row);print(json.dumps(row),flush=True)
 out=dict(id='SIGABA-SUPPORT-SIGNATURE-041-SUMMARY',started_at_utc=start,finished_at_utc=utc(),published_simulator_vectors=vectors,comparisons=rows,source_sha256=hashes(),real_sized_gate_passed=False,K4_evaluations=0);(ROOT/'results/SIGABA-SUPPORT-SIGNATURE-041-SUMMARY.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
