"""Replay received code in fresh scratch copies; never rewrite original evidence."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import time

ROOT=Path(__file__).resolve().parents[1]
VENDOR=ROOT/'independent/2026-10-22'


def verify_received():
    receipt=json.loads((VENDOR/'TRANSFER-RECEIPT.json').read_text())
    for name,record in receipt['received_files'].items():
        b=(VENDOR/name).read_bytes()
        assert len(b)==record['bytes'] and hashlib.sha256(b).hexdigest()==record['sha256'],name
    return receipt


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',required=True)
    p.add_argument('--python',default='python3')
    p.add_argument('--node',required=True)
    p.add_argument('--calibration-python',required=True)
    args=p.parse_args()
    receipt=verify_received()
    out=Path(args.output).resolve()
    if out.exists():raise FileExistsError('use a new scratch output; never overwrite prior evidence')
    out.mkdir(parents=True)
    start=time.monotonic();commands=[]
    env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
    def execute(command,cwd,log):
        remaining=120-(time.monotonic()-start)
        if remaining<=0:raise TimeoutError('total replay120second budget')
        r=subprocess.run(command,cwd=cwd,env=env,capture_output=True,text=True,timeout=remaining)
        (out/log).write_text(r.stdout+r.stderr)
        commands.append({'argv':command,'cwd_label':cwd.name,'returncode':r.returncode})
        if r.returncode:raise RuntimeError('replay command failed; see scratch log '+log)
    for label in ('evolving-alphabet','historical-clock','calibration'):
        shutil.copytree(VENDOR/label,out/label)
    state=out/'evolving-alphabet';clock=out/'historical-clock';cal=out/'calibration'
    execute([args.python,'generate_controls.py'],state,'state-generate.log')
    execute([args.python,'blind_selector.py'],state,'state-selector.log')
    execute([args.python,'audit.py'],state,'state-audit.log')
    execute([args.node,'recency_gap_oracle.js'],state,'state-js.log')
    js=json.loads((out/'state-js.log').read_text())
    assert js==json.loads((VENDOR/'evolving-alphabet/recency_gap_oracle.json').read_text())
    state_results=['blind_cases.json','sealed_truth.json','blind_predictions.json','controls_summary.json',
                   'primitive_summary.json','one_step_cases.json','k4_results.json','k4_full_trace.json']
    for name in state_results:
        assert json.loads((state/name).read_text())==json.loads((VENDOR/'evolving-alphabet'/name).read_text()),name
    execute([args.python,'pilot.py'],clock,'clock.log')
    assert json.loads((clock/'pilot_results.json').read_text())==json.loads((VENDOR/'historical-clock/pilot_results.json').read_text())
    # Deliberately replay classification only. No repeated913952-description synthesis.
    execute([args.calibration_python,'-c','import run_calibration as m; m.classification()'],cal,'classification.log')
    cal_names=['classification_results.json','generated_examples.json','label_null_accuracy.json']
    for name in cal_names:
        assert json.loads((cal/name).read_text())==json.loads((VENDOR/'calibration'/name).read_text()),name
    execute([args.calibration_python,'-m','pip','freeze'],cal,'calibration-environment.txt')
    # Roundtrip every supplied dataset row using fixed recorded parameters, not a solver.
    execute([args.calibration_python,'-c',
             "import json,numpy as np,run_calibration as m; d=json.loads((m.ROOT/'generated_examples.json').read_text()); n=0; "
             "exec('for rows in d[\"data\"].values():\\n for row in rows:\\n  assert np.array_equal(m.decrypt(m.encode(row[\"ciphertext\"]),row[\"label\"],row[\"key\"]),m.encode(row[\"plaintext\"])); n+=1'); "
             "assert n==288; print(n)"],cal,'classification-roundtrips.log')
    clf=json.loads((cal/'classification_results.json').read_text())
    result=dict(id='INDEPENDENT-FOLLOWUP-LOCAL-REPLAY-001',status='completed',
                code_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                python=platform.python_version(),platform=platform.platform(),
                adapter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                transfer_receipt_sha256=hashlib.sha256((VENDOR/'TRANSFER-RECEIPT.json').read_bytes()).hexdigest(),
                commands=commands,received_member_count=len(receipt['received_files']),
                state_deterministic_results_equal=True,javascript_models_and_all388ranks_equal=True,
                clock_results_equal=True,classification_results_equal=True,classification_roundtrips=288,
                classifier_test_correct=125,classifier_test_n=144,
                uniform_controls_same_forced_K4_label=44,uniform_control_n=48,
                classification_versions=clf['versions'],
                calibration_environment=(out/'calibration-environment.txt').read_text().splitlines(),
                synthesis_enumeration_replayed=False,
                synthesis_reason='Preserve independent enumeration evidence; exact K4 contradiction certificates locally checked separately. No duplicate search.',
                construction_artifact_status='not yet received at replay',
                elapsed_seconds=time.monotonic()-start)
    (out/'LOCAL-REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
