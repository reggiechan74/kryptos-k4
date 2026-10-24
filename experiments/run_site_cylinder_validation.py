"""Frozen exact-Site replay and scale-labeled finite stability; no actual K4."""
import argparse,collections,datetime,gzip,hashlib,itertools,json,math,random,resource,sys,time
from pathlib import Path
import site_cylinder_validation as m
ROOT=Path(__file__).resolve().parents[1]
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def rss():return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
def save(path,d):Path(path).write_text(json.dumps(d,indent=2)+'\n')
def check(clock):
 if time.monotonic()-clock>120 or rss()>512*1024**2:raise TimeoutError('frozen120second/512MiB cap')
def compact(g):
 return dict(validCount=g['validCount'],invalidCount=g['invalidCount'],key=g['key'],minimum_margin=g['minimum_margin'],distinct_cells=g['distinct_cells'],cell_path=[[x['cell']['row'],x['cell']['column']] if x.get('cell') else None for x in g['samples']],admitted_cell_path=[[x['cell']['row'],x['cell']['column']] if x['status']=='valid' else None for x in g['samples']],statuses=[x['status'] for x in g['samples']],margins=[x.get('margin') for x in g['samples']],letters=[x['key'] for x in g['samples']])
def compare(source,result):
 assert source['validCount']==result['validCount'] and source['key']==result['key'];error=0
 for expected,actual in zip(source['samples'],result['samples']):
  assert expected['status']==actual['status'],('status',expected['index'],expected['status'],actual['status'])
  if actual['status']=='valid':
   assert expected['cell']==actual['cell'] and expected['key']==actual['key']
   for k in ('row','column','modelColumn'):assert expected['source'][k]==actual['source'][k]
  for field in ('eye','reticle','hit','normal','eyeToMirror','reflectedTrace','tableauPoint'):
   if expected.get(field) is not None and actual.get(field) is not None:error=max(error,max(abs(x-y) for x,y in zip(expected[field],actual[field])))
 assert error<=1e-9,error
 return error

def replay(source):
 start=utc();clock=time.monotonic();rows=source['tableau_rows'];error=0;fixtures=[]
 for case in source['cases']:
  value=m.generate(case['state'],rows);error=max(error,compare(case['result'],value));fixtures.append(dict(id=case['id'],state=case['state'],result=compact(value)))
 for case in source['low_level']:assert m.hit(case['eye'],case['direction'],case['radius'])['status']==case['result']['status']
 neighbors=[]
 for (index,state),case in zip(m.neighborhood(),source['neighborhood']):
  assert index==case['id'] and state==case['state'];value=m.generate(state,rows);error=max(error,compare(case['result'],value));neighbors.append(dict(id=index,state=state,result=compact(value)));check(clock)
 assert len(neighbors)==729
 baseline=next(x for x in neighbors if x['state']==m.DEFAULTS);nominal=baseline['result'];counts=collections.Counter();completekeys=set()
 for row in neighbors:
  result=row['result'];counts['complete97']+=result['validCount']==97;counts['same_default_cellpath_and_admission']+=result['cell_path']==nominal['cell_path'] and result['statuses']==nominal['statuses'];counts['same_default_key']+=result['key']==nominal['key']
  if result['key']:completekeys.add(result['key'])
 key=nominal['key'];synthetic=source['synthetic'];assert m.addition(synthetic['message'],key)==synthetic['cipher'];assert m.addition(synthetic['cipher'],key,True)==synthetic['roundtrip']
 return dict(started_at_utc=start,finished_at_utc=utc(),elapsed_seconds=time.monotonic()-clock,complete=True,source_fixtures=fixtures,fixture_samples_compared=485,neighborhood_samples_compared=729*97,maximum_coordinate_difference=error,neighbors=neighbors,counts=dict(counts),distinct_complete_keys=len(completekeys),default_id=baseline['id'],default=baseline,synthetic_default_roundtrip=True),m.choose(neighbors)

def stability(rows,selected):
 start=utc();clock=time.monotonic();rng=random.Random(370024);out=[]
 for chosen in selected:
  state=chosen['state'];base=compact(m.generate(state,rows))
  for label,scale in (('U100',100),('R250',312.5)):
   delta=(state['radius']*.005,1/scale,1/scale,.5/scale,.5/scale,state['reticleWidth']*.01);records=[];example=None
   def evaluate(name,s,nuisance=None):
    nonlocal example
    generated=m.generate(s,rows,nuisance);g=compact(generated);floor=sum(a!=b for a,b in zip(base['cell_path'],g['cell_path']));admission=sum(a!=b for a,b in zip(base['statuses'],g['statuses']));same=floor==0 and admission==0;row=dict(id=name,state=s,nuisance=nuisance or {},result=g,same_cells_and_admission=same,same_key=g['key']==base['key'],floor_cell_changes=floor,admission_changes=admission,valid_letter_changes=sum(a!=b and a is not None and b is not None for a,b in zip(base['letters'],g['letters'])))
    if example is None and not same:example=dict(id=name,state=s,nuisance=nuisance or {},sample=generated)
    records.append(row);check(clock)
   for i,signs in enumerate(itertools.product((-1,1),repeat=6)):evaluate('corner-%02d'%i,dict(state,**{k:state[k]+v*d for k,v,d in zip(m.PARAMS,signs,delta)}))
   for i in range(64):evaluate('interior-%02d'%i,dict(state,**{k:state[k]+rng.uniform(-d,d) for k,d in zip(m.PARAMS,delta)}))
   for field,amount in (('eyeX',1/scale),('eyeY',1/scale),('reticleY',.5/scale),('reticleZ',.5/scale),('verticalPitchFraction',.01),('boardPitchDeg',.1),('boardYawDeg',.1),('boardRollDeg',.1)):
    for sign in (-1,1):evaluate(field+':'+str(sign),state,{field:sign*amount})
   assert len(records)==144;assembly=records[:];pupils={}
   for radius in (.05,1.5):
    begin=len(records);evaluate('pupil-%s-centre'%radius,state)
    for i in range(8):
     angle=i*math.pi/4;evaluate('pupil-%s-rim-%d'%(radius,i),state,dict(eyeX=radius/scale*math.cos(angle),eyeY=radius/scale*math.sin(angle)))
    panel=records[begin:];pupils[str(radius)]=dict(cell_stable=all(x['same_cells_and_admission'] for x in panel),key_stable=all(x['same_key'] for x in panel),minimum_margin=min(x['result']['minimum_margin'] for x in panel if x['result']['minimum_margin'] is not None),records=9)
   out.append(dict(neighbor_id=chosen['id'],state=state,scale=label,mm_per_unit=scale,nominal_minimum_margin=base['minimum_margin'],nominal_margin_mm=base['minimum_margin']*.25*scale,assembly_cell_stable=all(x['same_cells_and_admission'] for x in assembly),assembly_key_stable=all(x['same_key'] for x in assembly),primary_corner_cell_stable=all(x['same_cells_and_admission'] for x in assembly[:64]),nuisance_cell_stable=all(x['same_cells_and_admission'] for x in assembly[128:]),pupil=pupils,records=records,first_counterexample=example))
 return dict(started_at_utc=start,finished_at_utc=utc(),elapsed_seconds=time.monotonic()-clock,complete=True,selected_ids=[x['id'] for x in selected],selected_states=len(selected),state_scale_cases=len(out),records=out)

def run(snapshot,output):
 start=utc();source=json.load(gzip.open(snapshot,'rt'));out=dict(id='SITE-CYLINDER-037',started_at_utc=start,source_snapshot_sha256=hashlib.sha256(Path(snapshot).read_bytes()).hexdigest(),source_head=source['source_head'],source_core_sha256=source['source_sha256'],source_sha256={q:hashlib.sha256((ROOT/q).read_bytes()).hexdigest() for q in ('research/SITE-CYLINDER-037-SPEC.md','experiments/site_cylinder_validation.py','experiments/run_site_cylinder_validation.py')},actual_K4_evaluations=0,Site_files_modified=False,Site_source_archived=False,stages={});save(output,out)
 try:
  replayed,selected=replay(source);out['stages']['replay_neighborhood']=replayed;save(output,out);print('neighborhood',replayed['counts'],'keys',replayed['distinct_complete_keys'],'selected',len(selected),flush=True)
  out['stages']['stability']=stability(source['tableau_rows'],selected);out['complete']=True;print('stability',out['stages']['stability']['state_scale_cases'],flush=True)
 except (AssertionError,TimeoutError) as exc:out['complete']=False;out['blocker']=repr(exc);save(output,out);raise
 finally:out.update(finished_at_utc=utc(),peak_rss_bytes=rss());save(output,out)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--snapshot',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();run(a.snapshot,a.output)
