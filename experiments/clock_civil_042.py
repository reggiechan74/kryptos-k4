"""A common moving phase cannot supply date-varying inter-city differences."""
import calendar,collections,datetime,hashlib,io,json,time,zoneinfo
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];UTC=datetime.timezone.utc

def sunday(year,month,minimum=None):
 days=[d for week in calendar.monthcalendar(year,month) for d in [week[calendar.SUNDAY]] if d and (minimum is None or d>=minimum)]
 return max(days) if minimum is None else min(days)
def boundaries():return {k:datetime.datetime(1989,month,sunday(1989,month,minimum),1,tzinfo=UTC) for k,month,minimum in (('both_start',3,None),('Berlin_end',9,None),('London_end',10,23))}
def reference(t,key):
 b=boundaries();base=60 if key=='Europe/Berlin' else 0;end=b['Berlin_end' if key=='Europe/Berlin' else 'London_end'];return base+(60 if b['both_start']<=t<end else 0)
def analyze(zones):
 start=datetime.datetime(1989,1,1,tzinfo=UTC);counts=collections.Counter();states=collections.Counter();intervals=[];previous=None;comparisons=0
 for i in range(8760):
  t=start+datetime.timedelta(hours=i);offsets={k:int(t.astimezone(z).utcoffset().total_seconds()//60) for k,z in zones.items()}
  for k,v in offsets.items():assert v==reference(t,k);comparisons+=1
  difference=offsets['Europe/Berlin']-offsets['Europe/London'];counts[difference]+=1;states[tuple(offsets[k] for k in ('Europe/Berlin','Europe/London'))]+=1
  if difference!=previous:
   if intervals:intervals[-1]['end_exclusive_utc']=t.isoformat()
   intervals.append(dict(start_utc=t.isoformat(),difference_minutes=difference));previous=difference
 intervals[-1]['end_exclusive_utc']='1990-01-01T00:00:00+00:00'
 for t in boundaries().values():
  for delta in (-1,0,1):
   for k,z in zones.items():assert int((t+datetime.timedelta(seconds=delta)).astimezone(z).utcoffset().total_seconds()//60)==reference(t+datetime.timedelta(seconds=delta),k);comparisons+=1
 return dict(hourly_instants=8760,independent_offset_comparisons=comparisons,civil_difference_hour_counts=dict(sorted(counts.items())),civil_offset_state_hour_counts={str(k):v for k,v in sorted(states.items())},difference_intervals=intervals,constant_integer_sector_fit_hours={str(d):counts[d*60] for d in range(24)},any_constant_difference_fits_whole_year=len(counts)==1,positive_fixed_standard_time_model_hours=8760,uniform_DST_wrong_reference_disagreements=8760-max(counts.values()),source_condition='IANA/OS1989implementation history, not certified historical clock readings')
def run(replay=None):
 start=datetime.datetime.now(UTC).isoformat();clock=time.monotonic();pins=json.loads((ROOT/'sources/CLOCK-CIVIL-042.json').read_text());raw={}
 if replay:raw={k:bytes.fromhex(v) for k,v in json.loads(Path(replay).read_text())['tzif_hex'].items()}
 else:
  for k,m in pins['tzif_sources'].items():raw[k]=Path(m['path']).read_bytes()
 for k,b in raw.items():assert hashlib.sha256(b).hexdigest()==pins['tzif_sources'][k]['sha256']
 zones={k:zoneinfo.ZoneInfo.from_file(io.BytesIO(b),key=k) for k,b in raw.items()};r=analyze(zones)
 return dict(id='CLOCK-CIVIL-042',started_at_utc=start,finished_at_utc=datetime.datetime.now(UTC).isoformat(),elapsed_seconds=time.monotonic()-clock,analysis=r,transition_calendar={k:v.isoformat() for k,v in boundaries().items()},source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ('research/CLOCK-CIVIL-042-SPEC.md','sources/CLOCK-CIVIL-042.json','experiments/clock_civil_042.py')},tzif_hex={k:v.hex() for k,v in raw.items()},tzif_fixture_scope='Small IANA-derived factual timezone tables for byte-identical independent replay; no source code or web pages',actual_clock_layout_assumed=False,K4_trials=0,Site_changed=False,puzzle_solved=False)
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--replay-from');a=p.parse_args();r=run(a.replay_from);Path(a.output).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ('started_at_utc','finished_at_utc','analysis')}))
