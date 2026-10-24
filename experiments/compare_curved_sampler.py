"""Post-outcome portable complete cross-version comparison; no new parameter search."""
import argparse,datetime,gzip,hashlib,itertools,json,math
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--original',required=True);ap.add_argument('--replay',required=True);ap.add_argument('--original-poses',required=True);ap.add_argument('--replay-poses',required=True);ap.add_argument('--destination',required=True);args=ap.parse_args();R=Path(args.destination);(R/'results').mkdir(exist_ok=True,parents=True)
def read_json(path):
 return json.loads(gzip.decompress(Path(path).read_bytes())) if str(path).endswith('.gz') else json.loads(Path(path).read_bytes())
original=read_json(args.original);replay=read_json(args.replay);metrics={'floats_compared':0,'maximum_absolute_float_difference':0,'different_floats':0}
skip={'elapsed_seconds','peak_rss_bytes','pose_records_sha256','pose_records_bytes'}
def compare(a,b,path=''):
 if isinstance(a,dict):
  assert set(a)==set(b),(path,'keys')
  for k in a:
   if k in skip or k.endswith('_utc'):continue
   compare(a[k],b[k],path+'/'+k)
 elif isinstance(a,list):
  assert len(a)==len(b),(path,'length')
  for i,(x,y) in enumerate(zip(a,b)):compare(x,y,path+'/'+str(i))
 elif isinstance(a,float) or isinstance(b,float):
  difference=abs(a-b);assert difference<=1e-9,(path,a,b);metrics['floats_compared']+=1;metrics['maximum_absolute_float_difference']=max(metrics['maximum_absolute_float_difference'],difference);metrics['different_floats']+=int(difference!=0)
 else:assert a==b,(path,a,b)
compare(original,replay)
count=0
with gzip.open(args.original_poses,'rt') as fa,gzip.open(args.replay_poses,'rt') as fb:
 for a,b in itertools.zip_longest(fa,fb):
  assert a is not None and b is not None,'unequal pose record counts'
  compare(json.loads(a),json.loads(b),'pose/'+str(count));count+=1
assert count==original['stages']['sweep']['counts']['table_poses']
raw=json.dumps(replay,indent=2).encode()+b'\n';archive=R/'results/CURVED-SAMPLER-036-PY312-REPLAY.json.gz';archive.write_bytes(gzip.compress(raw,mtime=0));poses=R/'results/CURVED-SAMPLER-036-PY312-poses.jsonl.gz';poses.write_bytes(Path(args.replay_poses).read_bytes())
out=dict(kind='Complete cross-version synthetic study and all saved pose records, discrete exact and float absolute tolerance1e-9',recorded_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),complete=True,pose_records_compared=count,original_started_at_utc=original['started_at_utc'],replay_started_at_utc=replay['started_at_utc'],metrics=metrics,excluded_metadata=sorted(skip)+['*_utc'],discrete_decisions_keys_and_recovery_equal=True,archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),pose_archive_sha256=hashlib.sha256(poses.read_bytes()).hexdigest(),actual_K4_evaluations=0)
(R/'results/CURVED-SAMPLER-036-PY312-COMPARISON.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
