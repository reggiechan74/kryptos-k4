import argparse,hashlib,json,time
from datetime import datetime,timezone
from pathlib import Path
from run_io import RunSnapshot,specification,json_bytes
from strip_source_gates import ROOT,controls,actual

def main():
 p=argparse.ArgumentParser();p.add_argument('--spec-commit',required=True);args=p.parse_args();spec=ROOT/'research/STRIP-SOURCE-GATES-027-SPEC.md'
 with RunSnapshot(ROOT/'results/strip-source-gates-027','Item7 conditional row invariant pending historical admission',specification(args.spec_commit,spec),execution_kind='original') as run:
  run.write('README.md',b'# Conditional cyclic-strip replay\n\nUTC chronology and hashes are in the manifest. Synthetic controls and conditional first-crib proof are separate. No historical inventory or K4 key enumeration.\n')
  for name,fn in [('controls',controls),('conditional',actual)]:
   start=datetime.now(timezone.utc).isoformat();clock=time.monotonic();out=fn();assert time.monotonic()-clock<60
   out.update(started_at_utc=start,finished_at_utc=datetime.now(timezone.utc).isoformat());run.write(name+'.json',json_bytes(out));print(name,'completed',flush=True)
  paths=(spec,Path(__file__),ROOT/'experiments/strip_source_gates.py',ROOT/'data/k4.json');run.write('inputs.json',json_bytes({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}));print(run.final,flush=True)
if __name__=='__main__':main()
