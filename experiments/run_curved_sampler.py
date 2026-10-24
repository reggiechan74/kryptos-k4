"""Frozen synthetic geometry feasibility sweep; never evaluates actual K4."""
import argparse,collections,datetime,gzip,hashlib,itertools,json,math,random,resource,sys,time
from pathlib import Path
import curved_sampler as c
import curved_sampler_reference as ref
ROOT=Path(__file__).resolve().parents[1]
ORDER=('D','H','s','aim_deg','tx','ty','rotation_deg','pitch')
STATUS={'valid':'V','boundary':'B','blank':'_','outside':'O'}
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def rss():return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
def check(clock):
 if time.monotonic()-clock>120 or rss()>512*1024**2:raise TimeoutError('frozen stage120seconds/512MiB cap')
def save(path,r):Path(path).write_text(json.dumps(r,indent=2)+'\n')
def cells(sample):return [[x['row'],x['column']] if x['status']=='valid' else None for x in sample['records']]
def packed(sample,ident):
 records=sample['records'];return dict(id=ident,params=sample['params'],complete=sample['complete'],key=sample['key'],distinct_cells=sample['distinct_cells'],distinct_letters=sample['distinct_letters'],minimum_margin=sample['minimum_margin'],status_counts=dict(collections.Counter(x['status'] for x in records)),statuses=''.join(STATUS.get(x['status'],'!') for x in records),cells=cells(sample))
def scalar_geometry():
 return itertools.product((2,2.5,3,3.5,4),(1.2,1.6,2,2.4),(15,20,25,30,35,40,45),(.02,.04,.06,.08))
def poses(params,ground):
 pts=[x['point'] for x in ground]
 for ri,angle in enumerate((0,90,180,270)):
  t=math.radians(angle);cs,sn=math.cos(t),math.sin(t);x=[cs*q[0]+sn*q[1] for q in pts];y=[-sn*q[0]+cs*q[1] for q in pts];cx,cy=(min(x)+max(x))/2,(min(y)+max(y))/2;minimum=max((max(x)-min(x))/29,(max(y)-min(y))/26)
  for pi,factor in enumerate((1,1.1,1.25)):
   pitch=minimum*factor
   for xi,ox in enumerate((-.25,0,.25)):
    for yi,oy in enumerate((-.25,0,.25)):
     xx,yy=cx+ox*pitch,cy+oy*pitch;yield (ri,pi,xi,yi),dict(params,tx=cs*xx-sn*yy,ty=sn*xx+cs*yy,rotation_deg=angle,pitch=pitch)
def compare_rays(params,ground):
 f,right,up=c.basis(params['aim_deg']);eye=(0,-params['D'],params['H']);max_error=0
 for pt,a in zip(c.RETICLE,ground):
  d=c.add(c.add(f,right,params['s']*pt['u']),up,params['s']*pt['v']);b=ref.trace(eye,d)
  if a['status']!=b['status']:raise AssertionError(('independent status',params,pt,a['status'],b['status']))
  if a['status']=='ground':
   error=max(abs(x-y) for x,y in zip(a['point'],b['point']));max_error=max(max_error,error)
   if error>1e-9:raise AssertionError('independent point mismatch')
 return max_error

def sweep(rows,path):
 clock=time.monotonic();start=utc();counts=collections.Counter();footprints=[];valid=[];panel={};max_error=0
 with gzip.open(path,'wt') as stream:
  for gi,(D,H,aim,s) in enumerate(scalar_geometry()):
   params=dict(D=D,H=H,aim_deg=aim,s=s);ground=[c.trace(params,x['u'],x['v']) for x in c.RETICLE];max_error=max(max_error,compare_rays(params,ground));counts['optical_settings']+=1;complete=all(x['status']=='ground' for x in ground)
   footprints.append(dict(id=gi,params=params,complete_ground_footprint=complete,status_counts=dict(collections.Counter(x['status'] for x in ground)),rays=ground))
   if not complete:counts['incomplete_ground_footprints']+=1;continue
   counts['complete_ground_footprints']+=1
   for index,full in poses(params,ground):
    ident='g%03d-r%d-p%d-x%d-y%d'%((gi,)+index);sample=c.sample(full,rows,ground=ground);row=packed(sample,ident);stream.write(json.dumps(row,separators=(',',':'))+'\n');counts['table_poses']+=1
    if row['complete']:
     counts['complete97_poses']+=1
     if row['distinct_cells']>=80 and row['distinct_letters']>=12:
      counts['utility_gate_poses']+=1;valid.append(row);panel.setdefault(row['key'],[]).append(ident)
    if counts['table_poses']%256==0:check(clock)
   check(clock)
  stream.flush()
 if Path(path).stat().st_size>64*1024**2:raise TimeoutError('saved compressed64MiB cap')
 return dict(started_at_utc=start,finished_at_utc=utc(),elapsed_seconds=time.monotonic()-clock,complete=True,counts=dict(counts),maximum_independent_ray_error=max_error,independent_rays_checked=len(c.RETICLE)*len(footprints),footprints=footprints,pose_records_sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest(),pose_records_bytes=Path(path).stat().st_size,utility_rows=valid,key_panel=panel)

def stability(rows,selected):
 clock=time.monotonic();start=utc();rng=random.Random(360024);out=[]
 for nominal in selected:
  params=nominal['params'];base=c.sample(params,rows);basecells=cells(base);deltas=(.004,.004,.01*params['s'],.1,.002,.002,.1,.005*params['pitch']);records=[];counterexample=None
  def evaluate(label,p,eye=(0,0,0),fixed=False):
   nonlocal counterexample
   value=c.sample(p,rows,eye,fixed);cs=cells(value);cell_ok=cs==basecells;key_ok=value['key']==base['key'];row=dict(id=label,complete=value['complete'],same_cells=cell_ok,same_key=key_ok,changed_cell_positions=[i+1 for i,(a,b) in enumerate(zip(basecells,cs)) if a!=b],minimum_margin=value['minimum_margin'])
   if counterexample is None and not cell_ok:counterexample=dict(id=label,params=p,eye_offset=eye,fixed_reticle=fixed,sample=value)
   records.append(row);check(clock)
  for index,signs in enumerate(itertools.product((-1,1),repeat=8)):
   perturbed={k:params[k]+v*d for k,v,d in zip(ORDER,signs,deltas)};evaluate('assembly-corner-%03d'%index,perturbed)
  for i in range(64):evaluate('assembly-interior-%02d'%i,{k:params[k]+rng.uniform(-d,d) for k,d in zip(ORDER,deltas)})
  for sign in (-1,1):evaluate('lateral-eye-%d'%sign,params,(sign*.004,0,0))
  assembly=len(records);pupils={};_,right,up=c.basis(params['aim_deg'])
  for radius_mm in (.05,1.5):
   before=len(records);evaluate('pupil-%s-centre'%radius_mm,params,(0,0,0),True)
   for i in range(8):
    a=i*math.pi/4;size=radius_mm/250;offset=c.add(tuple(size*math.cos(a)*x for x in right),up,size*math.sin(a));evaluate('pupil-%s-rim-%d'%(radius_mm,i),params,offset,True)
   subset=records[before:];pupils[str(radius_mm)]=dict(all_cells_stable=all(x['same_cells'] for x in subset),all_keys_stable=all(x['same_key'] for x in subset),records=9)
  out.append(dict(id=nominal['id'],params=params,assembly_cell_stable=all(x['same_cells'] for x in records[:assembly]),assembly_key_stable=all(x['same_key'] for x in records[:assembly]),pupil=pupils,records=records,first_counterexample=counterexample))
 return dict(started_at_utc=start,finished_at_utc=utc(),elapsed_seconds=time.monotonic()-clock,complete=True,selected=len(selected),records=out)

def recovery(panel):
 clock=time.monotonic();start=utc();rng=random.Random(360025);plants=[]
 for key in list(panel)[:6]:
  plain=''.join(rng.choice(c.ALPHABET) for _ in range(97));cipher=c.encrypt(plain,key);known={i:plain[i] for i in list(range(21,34))+list(range(63,74))};result=c.recover_keys(cipher,known,panel);assert any(x['key']==key and x['plaintext']==plain for x in result['full24_candidates']);plants.append(dict(planted_key=key,owners=panel[key],plaintext=plain,ciphertext=cipher,known_one_based={i+1:v for i,v in known.items()},result=result));check(clock)
 if not plants:return dict(started_at_utc=start,finished_at_utc=utc(),complete=False,status='evidence_gate_not_met_no_utility_key_panel',plants=[],nulls=[])
 rng=random.Random(360026);nulls=[]
 for draw in range(31):
  rows=[]
  for plant in plants:
   chars=list(plant['ciphertext']);rng.shuffle(chars);cipher=''.join(chars);known={int(i)-1:v for i,v in plant['known_one_based'].items()};scores=[sum(c.encrypt(cipher,key,True)[i]==value for i,value in known.items()) for key in panel];rows.append(dict(ciphertext=cipher,maximum_known_matches=max(scores),full24_key_classes=sum(x==24 for x in scores)))
  nulls.append(dict(draw=draw,records=rows,whole_family_maximum=max(x['maximum_known_matches'] for x in rows),full24_key_classes=sum(x['full24_key_classes'] for x in rows)));check(clock)
 return dict(started_at_utc=start,finished_at_utc=utc(),elapsed_seconds=time.monotonic()-clock,complete=True,plants=plants,nulls=nulls)

def run(output,prefix):
 source='data/monument-fold-transcript-v1.json';rows=json.loads((ROOT/source).read_text())['tableau_rows'];path=str(prefix)+'-poses.jsonl.gz';out=dict(id='CURVED-SAMPLER-036',started_at_utc=utc(),actual_K4_evaluations=0,physical_replica=False,source_sha256={q:hashlib.sha256((ROOT/q).read_bytes()).hexdigest() for q in (source,'data/curved-sampler-v1.json','research/CURVED-SAMPLER-036-SPEC.md','experiments/curved_sampler.py','experiments/curved_sampler_reference.py','experiments/run_curved_sampler.py')},stages={});save(output,out)
 try:
  sw=sweep(rows,path);out['stages']['sweep']=sw;save(output,out);print('sweep',sw['counts'],'keys',len(sw['key_panel']),flush=True)
  selected=sorted(sw['utility_rows'],key=lambda x:(-x['minimum_margin'],tuple(x['params'][k] for k in ORDER)))[:10];out['stages']['stability']=stability(rows,selected);save(output,out);print('stability tested',len(selected),flush=True)
  out['stages']['recovery']=recovery(sw['key_panel']);save(output,out);print('recovery',out['stages']['recovery']['complete'],flush=True)
  out['complete']=True
 except (TimeoutError,AssertionError) as exc:out['complete']=False;out['blocker']=repr(exc);save(output,out);raise
 finally:
  out.update(finished_at_utc=utc(),peak_rss_bytes=rss());save(output,out)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--prefix',required=True);a=ap.parse_args();run(a.output,a.prefix)
