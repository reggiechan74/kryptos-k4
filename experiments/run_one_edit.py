"""Immutable original/replay item8 receipts, with lossless bounded serialization."""
import argparse,gzip,hashlib,json,random,subprocess,tempfile,time
from datetime import datetime,timezone
from pathlib import Path
from one_edit_controls import controls
from one_edit_models import select,budget
from run_io import RunSnapshot,specification,json_bytes
ROOT=Path(__file__).resolve().parents[1]

def stamp():return datetime.now(timezone.utc).isoformat()
def compressed(run,name,value):
 total=0
 with tempfile.TemporaryFile() as raw:
  with gzip.GzipFile(fileobj=raw,mode='wb',mtime=0) as stream:
   for chunk in json.JSONEncoder(indent=2).iterencode(value):
    data=chunk.encode();total+=len(data);stream.write(data)
   stream.write(b'\n');total+=1
  saved=raw.tell()
  if saved>64*1024**2:raise MemoryError('saved stage payload exceeds64MiB; unresolved')
  raw.seek(0);run.write(name,raw.read())
 return dict(artifact=name,uncompressed_bytes=total,saved_bytes=saved,lossless=True)

def main():
 p=argparse.ArgumentParser();p.add_argument('--spec-commit',required=True);p.add_argument('--execution-kind',choices=['original','replay'],default='replay');args=p.parse_args();spec=ROOT/'research/ONE-EDIT-028-SPEC.md';canonical=ROOT/'data/k4.json';pinned=hashlib.sha256(canonical.read_bytes()).hexdigest();observed=json.loads(canonical.read_text())['ciphertext']
 with RunSnapshot(ROOT/'results/one-edit-028','Item8 complete one-edit counterfactual sensitivity',specification(args.spec_commit,spec),execution_kind=args.execution_kind) as run:
  run.write('README.md',b'# Item8 original/replay run\n\nManifest and stage summaries record UTC chronology. Gzip JSON is lossless, with uncompressed byte counts. The canonical observation is never edited. All compatible arbitrary-permutation classes are underidentified, not K4 leads.\n')
  started=stamp();clock=time.monotonic();out=controls();budget(clock,180);storage=compressed(run,'controls.json.gz',out);budget(clock,180)
  summary=dict(started_at_utc=started,finished_at_utc=stamp(),**{k:v for k,v in out.items() if k!='plants'},plants=len(out['plants']),planted_periodic_complete_records=sum(len(r['full_periodic_compatible_records']) for r in out['plants']),planted_plaintext_class_counts=[r['distinct_periodic_plaintexts'] for r in out['plants']],storage=storage);run.write('controls-summary.json',json_bytes(summary));print('controls completed',flush=True)
  started=stamp();clock=time.monotonic();out=select(observed,start=clock,seconds=120);storage=compressed(run,'actual.json.gz',out);budget(clock,120)
  summary=dict(started_at_utc=started,finished_at_utc=stamp(),**out['summary'],complete_periodic_records=len(out['complete_periodic_fits']),distinct_periodic_full_plaintexts=out['distinct_periodic_full_plaintexts'],compatible_permutation_classes=len(out['permutation_classes']),storage=storage);run.write('actual-summary.json',json_bytes(summary));print('actual completed',flush=True)
  started=stamp();clock=time.monotonic();rng=random.Random(280024);nulls=[]
  for j in range(99):
   xs=list(observed);rng.shuffle(xs);row=select(''.join(xs),False,start=clock,seconds=300);nulls.append(dict(draw=j,permutation_compatible_raw=row['permutation_compatible_raw_alignment_cases'],periodic_first_raw=row['periodic_first_raw_cases'],periodic_all_raw=row['periodic_all_raw_cases'],unique_instances=row['unique_constraint_instances'],by_alignment=row['by_alignment']));budget(clock,300)
  null_summary=dict(started_at_utc=started,finished_at_utc=stamp(),seed=280024,draws=nulls,permutation_events=sum(r['permutation_compatible_raw']>0 for r in nulls),periodic_first_events=sum(r['periodic_first_raw']>0 for r in nulls),periodic_complete_events=sum(r['periodic_all_raw']>0 for r in nulls),interpretation='Full edit/alignment/family exact-fit controls, no partial-score or positive significance claim. Unrestricted permutation compatibility is capacity, not a lead.');run.write('nulls.json',json_bytes(null_summary));print('nulls completed',flush=True)
  assert hashlib.sha256(canonical.read_bytes()).hexdigest()==pinned
  paths=[spec,canonical,Path(__file__)]+[ROOT/'experiments'/n for n in ('one_edit_channel.py','one_edit_models.py','one_edit_reference.py','one_edit_controls.py')]
  run.write('inputs.json',json_bytes(dict(implementation_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),canonical_file_unchanged=True,source_sha256={str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in paths})));print(run.final,flush=True)
if __name__=='__main__':main()
