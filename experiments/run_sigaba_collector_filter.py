"""Run the separately frozen supplied-anchor filter diagnostic, local only."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
import sigaba_collector_filter as f
ROOT=Path(__file__).resolve().parents[1]
PIN=['experiments/run_sigaba_collector_filter.py','experiments/sigaba_collector_filter.py','experiments/sigaba_real_adapter.py','experiments/sigaba_csp889.py','experiments/sigaba_joint_toy.py','experiments/sigaba_first_observation.py','data/sigaba-csp889-v1.json','research/SIGABA-COLLECTOR-FILTER-SPEC.md']
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--case',type=int,choices=(0,1));ap.add_argument('--output',required=True);ap.add_argument('--all',action='store_true');a=ap.parse_args()
 if a.all:
  directory=Path(a.output);directory.mkdir(exist_ok=True,parents=True)
  for n in (0,1):
   out=directory/f'case-{n}.json'
   try:subprocess.run([sys.executable,__file__,'--case',str(n),'--output',str(out)],timeout=65,check=True)
   except subprocess.TimeoutExpired:out.write_text(json.dumps(dict(id='CSP889-FILTER-019',case=n,completed=False,reason='watchdog_unresolved',K4_evaluations=0,full_domain_gate_passed=False))+'\n')
   r=json.loads(out.read_text());print(n,r.get('completed'),r.get('summary'),r.get('budget'),flush=True)
 else:
  result=f.run_panel(a.case);result['source_sha256']={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in PIN};Path(a.output).write_text(json.dumps(result,indent=2)+'\n')
