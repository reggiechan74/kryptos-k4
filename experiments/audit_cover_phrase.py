"""Post-outcome independent full-position validation of every unique positive."""
import argparse,datetime,gzip,hashlib,json,time,zipfile
from pathlib import Path
import cover_extraction as c
import cover_extraction_reference as ref
import cover_phrase as p
ROOT=Path(__file__).resolve().parents[1]
def audit(brown_path,summary_path):
 p.validate_brown(brown_path);start=p.utc();clock=time.monotonic();summary=json.loads(Path(summary_path).read_text());models={m.name:m for m in c.models()};seen=set();cache={};checked=0;rows=0;complete=True
 with zipfile.ZipFile(brown_path) as z,gzip.open(Path(summary_path).with_name('COVER-PHRASE-034-original-windows.jsonl.gz'),'rt') as stream:
  for line in stream:
   row=json.loads(line);r=row['source'];rows+=1
   if r['file'] not in cache:cache[r['file']]=z.read(r['file']).decode('ascii').splitlines()
   tokens=p.parse_line(cache[r['file']][r['line_zero_based']]);words=tokens[r['start_token_zero_based']:r['start_token_zero_based']+r['output_words']];assert all(words);text=''.join(words);assert hashlib.sha256(text.encode()).hexdigest()==r['joined_sha256']
   for i,expected in row['cover_counts'].items():
    key=(r['joined_sha256'],int(i))
    if key in seen:continue
    lane=summary['lanes'][int(i)];actual=ref.count_message(models[lane['model']],text,lane['k'],lane['N'],lane['phase'],15 if lane['stratum']=='15' else None);assert actual==expected,(r,i,actual,expected);seen.add(key);checked+=1
   if time.monotonic()-clock>60 or p.rss_bytes()>512*1024**2:complete=False;break
 return dict(kind='Post-outcome independent full-position audit of all recorded unique corpus positives',started_at_utc=start,finished_at_utc=p.utc(),elapsed_seconds=time.monotonic()-clock,peak_rss_bytes=p.rss_bytes(),complete=complete,matched_occurrence_records_processed=rows,unique_message_lane_counts_verified=checked,all_matched_occurrences=summary['corpus']['counts']['matched_window_occurrences'],claim='Complete recorded positive soundness plus independent tiny exhaustive language controls; not a separate exhaustive corpus false-negative implementation',new_K4_trials=0)
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--brown-zip',required=True);a.add_argument('--summary',required=True);a.add_argument('--output',required=True);args=a.parse_args();r=audit(args.brown_zip,args.summary);Path(args.output).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
