"""Post-outcome arithmetic/resource replay; source vectors remain separate."""
from datetime import datetime,timezone
import hashlib,json,resource,sys,time
from pathlib import Path
from strip_source_gates import ROOT,controls,actual

def audit():
 start=datetime.now(timezone.utc).isoformat();clock=time.monotonic();r=ROOT/'results/strip-source-gates-027';p=r/json.loads((r/'latest.json').read_text())['run_id'];old=json.loads((p/'conditional.json').read_text());old.pop('started_at_utc');old.pop('finished_at_utc');assert actual()==old
 c=controls();oldc=json.loads((p/'controls.json').read_text())
 for key in ('elapsed_seconds','started_at_utc','finished_at_utc'):oldc.pop(key,None)
 fresh=dict(c);fresh.pop('elapsed_seconds');assert fresh==oldc
 rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024);assert rss<256*1024**2;assert time.monotonic()-clock<60
 return dict(kind='post_outcome_resource_and_exact_arithmetic_replay_not_historical_vector_validation',started_at_utc=start,finished_at_utc=datetime.now(timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-clock,peak_rss_bytes=rss,declared_cap_bytes=256*1024**2,original_receipts_reproduced=True,original_peak_rss_was_not_recorded=True,full_historical_inventory_admitted=False,source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),ROOT/'experiments/strip_source_gates.py')})
if __name__=='__main__':print(json.dumps(audit(),indent=2))
