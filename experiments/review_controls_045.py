"""Late explicit review controls; preserves038's original source/run chronology."""
import datetime,hashlib,itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run():
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();rows=[]
 for q in (2,3):
  for n in range(1,5):
   C=tuple(i%q for i in range(n));known={0:0,n-1:(n-1)%q};changed=dict(known);changed[0]=(known[0]+1)%q;old=set();new=set();contradict=set()
   for key in itertools.product(range(q),repeat=n):
    P=tuple((a-b)%q for a,b in zip(C,key))
    if all(P[i]==v for i,v in known.items()):old.add(key)
    if all(P[i]==v for i,v in changed.items()):new.add(key)
    if P[0]==known[0] and P[0]==changed[0]:contradict.add(key)
   expected=q**(n-len(known));assert len(old)==len(new)==expected and not(old&new) and not contradict
   rows.append(dict(q=q,length=n,known=known,changed_known=changed,original_keys=len(old),new_keys=len(new),equal_cardinality=True,disjoint_key_sets=True,old_keys_all_fail_changed_crib=True,new_free_keys_remain_admitted=True,contradictory_duplicate_crib_keys=len(contradict)))
 return dict(id='REVIEW-CONTROLS-045',started_at_utc=start,finished_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),chronology='After-outcome reviewer supplement;038original omitted its specified explicit changed-crib control. Original source/receipt preserved.',changed_crib_complete_systems=len(rows),records=rows,source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ('experiments/review_controls_045.py','experiments/cover_selector_038.py','research/COVER-SELECTOR-038-SPEC.md','results/COVER-SELECTOR-038-ORIGINAL.json')},new_K4_trials=0)
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();r=run();Path(a.output).write_text(json.dumps(r,indent=2)+'\n');print(r['changed_crib_complete_systems'])
