"""Post-outcome reviewer controls: active cache failure, wrong DST and invalid.Zflags."""
import datetime,hashlib,io,json
from pathlib import Path
import zoneinfo
import sigaba_support_signature_041 as cachemod
import sigaba_unknown_anchor_collector as prior
from sigaba_byte_mask_predicates import ByteMaskPredicates
import clock_civil_042 as clock
import compress_transport_043 as codec
ROOT=Path(__file__).resolve().parents[1]
def active_cache_control():
 progress={}
 class ActiveBudget(cachemod.toy.Budget):
  def check(self,force=False):
   if progress.get('stage')=='connected_support' and progress.get('layer') is not None:raise cachemod.toy.Limit('deliberate_active_root_interruption')
   super().check(force)
 model=cachemod.toy.Model(cachemod.toy.fixture(3,3));cache=cachemod.SupportCache();observations=[(i,0,0) for i in range(2,6)];digits=model.digits((0,0,0),6);budget=ActiveBudget(10)
 try:cache.evaluate(model,observations,digits,budget,ByteMaskPredicates(model,budget,0),progress=progress)
 except cachemod.toy.Limit as exc:assert str(exc)=='deliberate_active_root_interruption'
 else:raise AssertionError('No active interruption')
 assert progress['layers_built']==4 and progress['stage']=='connected_support' and not cache.cache and cache.bytes==0
 after_interruption=dict(progress);budget=cachemod.toy.Budget(10);pred=ByteMaskPredicates(model,budget,0);a,r=cache.evaluate(model,observations,digits,budget,pred);b,s=cache.evaluate(model,observations,digits,budget,pred);expected,_=prior.root_support(model,observations,digits,budget,pred);assert a==b==expected and not r['support_cache_hit'] and s['support_cache_hit']
 return dict(active_stage=after_interruption,partial_entry_absent=True,recomputed_exact_roots_equal=True,subsequent_cache_hit=True)
def wrong_shared_dst_control():
 saved=json.loads((ROOT/'results/CLOCK-CIVIL-042-ORIGINAL.json').read_text());zones={k:zoneinfo.ZoneInfo.from_file(io.BytesIO(bytes.fromhex(v)),key=k) for k,v in saved['tzif_hex'].items()};b=clock.boundaries();start=clock.datetime.datetime(1989,1,1,tzinfo=clock.UTC);wrong=0;records=0
 for i in range(8760):
  t=start+clock.datetime.timedelta(hours=i);common=60 if b['both_start']<=t<b['Berlin_end'] else 0;wrong_berlin=60+common;wrong_london=common;actual=[int(t.astimezone(zones[k]).utcoffset().total_seconds()/60) for k in ('Europe/Berlin','Europe/London')];wrong+=(wrong_berlin-wrong_london)!=(actual[0]-actual[1]);records+=1
 assert wrong==840 and wrong==saved['analysis']['uniform_DST_wrong_reference_disagreements']
 return dict(explicit_deliberately_wrong_model='Apply EU March–September DST schedule equally toBerlin andLondon',hourly_comparisons=records,difference_disagreements=wrong,derived_from_maxcounts=False)
def invalid_flags_control():
 raw=bytes.fromhex('1f9d904100');badflags=(0x80,0x88,0x91,0x9f,0xb0,0xd0);checks=0
 for flag in badflags:
  invalid=raw[:2]+bytes([flag])+raw[3:];assert invalid[:2]==b'\x1f\x9d' and not codec.header(invalid)
  for name,b,r in codec.versions():
   text=codec.encode(invalid,codec.ALPHABETS[name],b,r);decoded=codec.decode(text,codec.ALPHABETS[name],b,r);assert decoded==invalid and not codec.header(decoded);checks+=1
 assert not codec.header(raw[:2]) and codec.header(raw)
 return dict(valid_magic_invalid_flag_transport_checks=checks,invalid_flags=list(badflags),valid_control=True,truncated_header_rejected=True)
def run():
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();values=dict(active_cache=active_cache_control(),explicit_wrong_DST=wrong_shared_dst_control(),valid_magic_invalid_flags=invalid_flags_control())
 return dict(id='REVIEW-CONTROLS-046',started_at_utc=start,finished_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),chronology='Post-outcome independent review supplement; no original source/model/receipt changed or large experiment rerun',controls=values,source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ('experiments/review_controls_046.py','experiments/sigaba_support_signature_041.py','experiments/clock_civil_042.py','experiments/compress_transport_043.py')},new_K4_trials=0)
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();r=run();Path(a.output).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r['controls']))
