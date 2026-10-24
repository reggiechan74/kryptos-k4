"""Independent complex-coordinate cell lookup for every saved pose; no new domain."""
import argparse,cmath,collections,datetime,gzip,hashlib,json,math,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run(source,poses,output):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();clock=time.monotonic();r=json.load(gzip.open(source,'rt'));rows=json.loads((ROOT/'data/monument-fold-transcript-v1.json').read_text())['tableau_rows'];footprints={x['id']:x for x in r['stages']['sweep']['footprints']};checked=0;samples=0;full=0;utility=0;keys=set();paths=set()
 with gzip.open(poses,'rt') as f:
  for line in f:
   saved=json.loads(line);params=saved['params'];gid=int(saved['id'].split('-')[0][1:]);pts=[x['point'] for x in footprints[gid]['rays']];rotation=cmath.exp(-1j*math.radians(params['rotation_deg']));centre=complex(params['tx'],params['ty']);statuses=[];cells=[];key=[]
   for point in pts:
    local=(complex(point[0],point[1])-centre)*rotation;column=15+local.real/params['pitch'];row=13.5-local.imag/params['pitch'];ci=math.floor(column+.5);ri=math.floor(row+.5);margin=min(.5-abs(column-ci),.5-abs(row-ri))
    if not 0<=ri<len(rows) or not 0<=ci<len(rows[ri]):status='O'
    elif rows[ri][ci] not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':status='_'
    elif margin<=.02:status='B'
    else:status='V'
    statuses.append(status);cells.append([ri,ci] if status=='V' else None)
    if status=='V':key.append(rows[ri][ci])
   assert ''.join(statuses)==saved['statuses'] and cells==saved['cells'];complete=all(x=='V' for x in statuses);assert complete==saved['complete'];distinct=len({tuple(x) for x in cells if x is not None});assert distinct==saved['distinct_cells']
   if complete:
    full+=1;value=''.join(key);assert value==saved['key'];keys.add(value);paths.add(json.dumps(cells));utility+=int(distinct>=80 and len(set(value))>=12)
   checked+=1;samples+=len(pts)
   if checked%256==0 and time.monotonic()-clock>120:raise TimeoutError('independent120second replay cap')
 assert checked==r['stages']['sweep']['counts']['table_poses']
 out=dict(kind='Post-outcome independent complex-coordinate cell/status replay of entire frozen saved pose panel',started_at_utc=start,finished_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-clock,complete=True,poses_checked=checked,samples_checked=samples,complete97_poses=full,utility_gate_poses=utility,distinct_complete_keys=len(keys),distinct_cellpaths=len(paths),source_pose_sha256=hashlib.sha256(Path(poses).read_bytes()).hexdigest(),new_K4_evaluations=0)
 Path(output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--source',required=True);ap.add_argument('--poses',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();run(a.source,a.poses,a.output)
