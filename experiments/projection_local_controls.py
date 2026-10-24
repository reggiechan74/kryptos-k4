"""Supplementary predeclared nearby mismatch sensitivity; no real photograph input."""
import datetime,hashlib,json,math,platform,resource,subprocess,sys,time
from pathlib import Path
import projection_concurrence as p
ROOT=Path(__file__).resolve().parents[1]
def run():
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();clock=time.monotonic();f=p.fixtures()['finite'];out=[]
 for offset in (.25,.5,1.,2.,5.):
  for sign in (-1,1):
   pairs=[]
   for i,z in enumerate(f['pairs']):
    a,g=z['aperture'],z['receiver'];dx,dy=g[0]-a[0],g[1]-a[1];n=math.hypot(dx,dy)
    q=g[:] if i in f['training'] else [g[0]-sign*offset*dy/n,g[1]+sign*offset*dx/n];pairs.append(dict(z,receiver=q))
    if i not in f['training']:
     # Independent raw pixel determinant/line distance, not native normalized incidence.
     sx,sy=120.,-80.;aa=a[1]-sy;bb=sx-a[0];cc=a[0]*sy-a[1]*sx;miss=(aa*q[0]+bb*q[1]+cc)/math.hypot(aa,bb)
     assert abs(abs(miss)-offset)<1e-8
   result=p.diagnose(pairs,1000,800,f['training']);out.append(dict(kind='nearby_heldout_mismatch',offset_px=offset,sign=sign,pairs=pairs,result=result))
 pairs=[dict(z,receiver=[x+2 for x in z['receiver']]) for z in f['pairs']];out.append(dict(kind='correlated_all_receivers_translation',offset_vector_px=[2,2],pairs=pairs,result=p.diagnose(pairs,1000,800,f['training'])))
 peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024);elapsed=time.monotonic()-clock
 assert elapsed<=60 and peak<=256*1024**2
 paths=['experiments/projection_local_controls.py','experiments/projection_concurrence.py','research/PROJECTION-CONCURRENCE-029-LOCAL-CONTROLS-SPEC.md']
 return dict(kind='Supplementary synthetic local mismatch sensitivity, not field false-match calibration',started_at_utc=start,finished_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=elapsed,peak_rss_bytes=peak,implementation_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),source_sha256={x:hashlib.sha256((ROOT/x).read_bytes()).hexdigest() for x in paths},records=out,real_pairs=0,real_fits=0,K4_trials=0,original_thresholds_changed=False)
if __name__=='__main__':
 import argparse
 a=argparse.ArgumentParser();a.add_argument('--output',required=True);args=a.parse_args();d=run();Path(args.output).write_text(json.dumps(d,indent=2,allow_nan=False)+'\n');print(json.dumps([{k:r[k] for k in ('kind','offset_px','sign') if k in r}|dict(gate=r['result']['conditional_line_gate_pass'],rms=r['result']['heldout_combined_rms']) for r in d['records']]))
