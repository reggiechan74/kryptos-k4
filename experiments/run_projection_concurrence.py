"""Run frozen synthetic diagnostic, never a monument/K4 fit."""
import argparse,datetime,hashlib,json,os,platform,resource,subprocess,sys,time
from pathlib import Path
import projection_concurrence as p
ROOT=Path(__file__).resolve().parents[1]
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def run():
 start=utc();clock=time.monotonic();fixtures=p.fixtures();records={}
 for name,f in fixtures.items():
  records[name]={}
  for factor in (.5,1.,2.):
   pairs=[dict(z,sigma_px=z['sigma_px']*factor) for z in f['pairs']]
   try:records[name][str(factor)]=p.diagnose(pairs,f['width'],f['height'],f['training'])
   except ValueError as e:records[name][str(factor)]={'status':'inadmissible_geometry','reason':str(e)}
  if time.monotonic()-clock>60:raise RuntimeError('frozen 60 second budget exceeded')
 peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
 if peak>256*1024**2:raise RuntimeError('frozen 256 MiB budget exceeded')
 source_paths=[ROOT/'experiments'/x for x in ['projection_concurrence.py','projection_concurrence_reference.py','run_projection_concurrence.py']]+[ROOT/'tests/test_projection_concurrence.py',ROOT/'research/PROJECTION-CONCURRENCE-029-SPEC.md']
 return dict(kind='synthetic image-line concurrence diagnostic, not monument result',started_at_utc=start,finished_at_utc=utc(),elapsed_seconds=time.monotonic()-clock,peak_rss_bytes=peak,python=platform.python_version(),implementation_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),source_sha256={str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in source_paths},budget_seconds=60,budget_rss_bytes=256*1024**2,real_certified_pairs=0,real_fits_executed=0,K4_trials=0,site_changed=False,records=records,fixtures=fixtures,conditioning_warning_threshold=1e-7,noise_sensitivity_factors=[.5,1.,2.],perturbations_per_configuration=256,source_fit_uncertainty_note='Conditional Gaussian perturbation sensitivity; endpoint picks and systematics not empirically established for monument')
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args();out=run();Path(args.output).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n');print(json.dumps({k:out[k] for k in ['started_at_utc','finished_at_utc','elapsed_seconds','peak_rss_bytes','real_certified_pairs']}))
