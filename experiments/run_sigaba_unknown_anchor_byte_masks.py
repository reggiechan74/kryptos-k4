"""Single bounded shared-byte-mask comparison; preserves original failed runs."""
import argparse,datetime,hashlib,json,subprocess,sys
from pathlib import Path
from unittest.mock import patch
import run_sigaba_unknown_anchor as original
import sigaba_unknown_anchor_controls as basic
import audit_sigaba_unknown_anchor_dynamic_controls as dynamic
from sigaba_byte_mask_predicates import ByteMaskPredicates
from run_io import RunSnapshot,specification,json_bytes,atomic_write
ROOT=Path(__file__).resolve().parents[1]
EXTRA=['experiments/sigaba_byte_mask_predicates.py','experiments/audit_sigaba_unknown_anchor_dynamic_controls.py','experiments/run_sigaba_unknown_anchor_byte_masks.py','research/SIGABA-UNKNOWN-ANCHOR-BYTE-MASK-SPEC.md']
def hashes():return {**original.hashes(),**{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in EXTRA}}
def main():
 p=argparse.ArgumentParser();p.add_argument('--child',choices=('baseline','integrated'));p.add_argument('--case',type=int,choices=(0,1));p.add_argument('--output',required=True);p.add_argument('--spec-commit');p.add_argument('--kind',choices=('original','replay'),default='replay');a=p.parse_args()
 if a.child:
  with patch.object(original.baseline,'ReservedPredicates',ByteMaskPredicates),patch.object(original.integrated,'ReservedPredicates',ByteMaskPredicates):r=original.child(a.child,a.case)
  r.update(id='CSP889-COUPLED-024B',predicate_backend='Exact byte-tiled masks; unchanged cache caps/policy',source_sha256=hashes());atomic_write(a.output,json_bytes(r));return
 if not a.spec_commit:p.error('--spec-commit required')
 with RunSnapshot(a.output,'CSP889-COUPLED-024B',specification(a.spec_commit,Path('research/SIGABA-UNKNOWN-ANCHOR-BYTE-MASK-SPEC.md')),execution_kind=a.kind) as snapshot:
  start=original.utc()
  with patch.object(original.baseline,'ReservedPredicates',ByteMaskPredicates),patch.object(original.integrated,'ReservedPredicates',ByteMaskPredicates):base=basic.run()
  extra=dynamic.run();snapshot.write('controls.json',json_bytes(dict(started_at_utc=start,finished_at_utc=original.utc(),original_fixed_controls=base,varying_input_supplement=extra,source_sha256=hashes())))
  summaries=[]
  for backend in ('baseline','integrated'):
   for case in (0,1):
    name=f'{backend}-case-{case}.json';path=snapshot.stage/name;start=original.utc()
    try:
     subprocess.run([sys.executable,__file__,'--child',backend,'--case',str(case),'--output',str(path)],check=True,timeout=65);value=json.loads(path.read_text())
    except subprocess.TimeoutExpired:value=dict(id='CSP889-COUPLED-024B',backend=backend,case=case,started_at_utc=start,finished_at_utc=original.utc(),completed=False,reason='watchdog_unresolved',exact_raw_key_count=None,source_sha256=hashes(),real_sized_gate_passed=False,K4_evaluations=0)
    except subprocess.CalledProcessError as error:value=dict(id='CSP889-COUPLED-024B',backend=backend,case=case,started_at_utc=start,finished_at_utc=original.utc(),completed=False,reason='process_error_unresolved',exit_code=error.returncode,exact_raw_key_count=None,source_sha256=hashes(),real_sized_gate_passed=False,K4_evaluations=0)
    snapshot.write(name,json_bytes(value));s=value.get('solver',value);item=dict(backend=backend,case=case,completed=s.get('completed'),reason=s.get('reason'),controllers_completed=s.get('control_starts_completed'),filters_completed=s.get('filters_completed'),filter_progress=s.get('filter_progress'),budget=s.get('budget'));summaries.append(item);print(json.dumps(item),flush=True)
  snapshot.write('summary.json',json_bytes(dict(id='CSP889-COUPLED-024B',cases=summaries,same_fixtures_caps_and_predicate_primitive=True,real_sized_gate_passed=False,K4_evaluations=0)))
 print(snapshot.final,flush=True)
if __name__=='__main__':main()
