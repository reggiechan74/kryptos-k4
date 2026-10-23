"""Profile frozen synthetic fixtures without changing their resource budgets."""
import argparse,cProfile,hashlib,json,pstats,subprocess,sys
from pathlib import Path
import run_sigaba_sparse_ownership as baseline
ROOT=baseline.ROOT

def run(n):
 profile=cProfile.Profile();profile.enable()
 try:result=baseline.run(n)
 finally:profile.disable()
 stats=pstats.Stats(profile);rows=[]
 for (path,line,name),(primitive,total,selftime,cumulative,callers) in stats.stats.items():
  try:path=str(Path(path).relative_to(ROOT))
  except ValueError:path=Path(path).name
  rows.append(dict(file=path,line=line,function=name,primitive_calls=primitive,total_calls=total,self_seconds=selftime,cumulative_seconds=cumulative))
 rows.sort(key=lambda r:(-r['self_seconds'],r['file'],r['line'],r['function']))
 return dict(id='CSP889-DOMAIN-016-profile',profiler='stdlib cProfile; instrumentation overhead included',source_baseline_commit='552cbdae9d253c1f4cfd62edc5fd08427f87aefa',case=n,result=result,profile_total_seconds=stats.total_tt,function_table=rows,source_sha256={'experiments/profile_sigaba_sparse.py':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'research/SIGABA-DOMAIN-IDENTITY-SPEC.md':hashlib.sha256((ROOT/'research/SIGABA-DOMAIN-IDENTITY-SPEC.md').read_bytes()).hexdigest()},K4_evaluations=0)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--case',type=int,choices=(0,1));ap.add_argument('--output',required=True);ap.add_argument('--all',action='store_true');a=ap.parse_args()
 if a.all:
  directory=Path(a.output);directory.mkdir(exist_ok=True,parents=True)
  for n in (0,1):subprocess.run([sys.executable,__file__,'--case',str(n),'--output',str(directory/f'case-{n}.json')],timeout=65,check=True)
 else:Path(a.output).write_text(json.dumps(run(a.case),indent=2)+'\n')
