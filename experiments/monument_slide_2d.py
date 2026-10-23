"""Frozen item-1 2D overlay; exact carry-free integer correlation, not a cipher."""
import argparse,array,bisect,collections,csv,datetime,functools,gzip,hashlib,io,itertools,json,math,random,resource,subprocess,sys,time
from fractions import Fraction
from pathlib import Path
import monument_slide as old
from run_io import RunSnapshot,json_bytes
ROOT=old.ROOT;SPEC=ROOT/'research/specifications/FOLD-SLIDE-2D-001.json';NAMES=('label_matches','common_pixel_area')
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z')
def budget(start,seconds):
 if time.monotonic()-start>seconds:raise TimeoutError('frozen job budget unresolved')
 rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
 if rss>1<<30:raise MemoryError('frozen RSS budget unresolved')
def exact_key(n,m):return ((n>0)-(n<0),Fraction(n*n,m) if n>=0 else -Fraction(n*n,m))
def stat_display(n,m,D):return n/math.sqrt(D*m)
def greater(n,m,bn,bm):
 if (n>=0)!=(bn>=0):return n>=0
 left=n*n*bm;right=bn*bn*m
 return left>right if n>=0 else left<right

class Engine:
 def __init__(self,data=None,glyphs=None):
  self.base=old.Model() if data is None else old.Model(data,glyphs);b=self.base;self.w=b.w;self.h=b.h;self.stride=2*self.w-1;self.digits=(self.h-1)*self.stride+self.w;self.coefficients=2*self.digits-1;self.D=math.lcm(*[len(x) for x in b.free if x]) if any(b.free) else 1
  assert 35*self.w*self.h<1<<16 and 35*self.w*self.h*self.D<1<<64
  self.pix=[[p for p in range(35) if mask>>p&1] for mask in b.masks];self.free=set(itertools.chain.from_iterable(b.free));self.frames=[];self.indices=[]
  for model in b.targets:
   for dy in range(-self.h,self.h+1):
    for dx in range(-self.w,self.w+1):
     self.frames.append(dict(id=f'{model}:{dy}:{dx}',model=model,dy=dy,dx=dx,geometric_overlap_cells=(self.w-abs(dx))*(self.h-abs(dy))))
     self.indices.append((self.h-1-dy)*self.stride+self.w-1-dx if abs(dy)<self.h and abs(dx)<self.w else None)
  self.active=[i for i,k in enumerate(self.indices) if k is not None]
  self.target={name:self.pack(target,16,False) for name,target in b.targets.items()}
  weighted=self.pack(b.base,64,True,expected=True);self.expected=self.correlate(weighted,{name:self.pack(t,64,False) for name,t in b.targets.items()},64)
  self.weights=[[max(n,self.D) for n in row] for row in self.expected]
 def pack(self,source,bits,reverse,expected=False):
  step=bits//8;buffers=[bytearray(step*self.digits) for _ in range(61)];row_weights=[]
  if expected:
   for row,hist in enumerate(self.base.hist):
    n=len(self.base.free[row]);factor=self.D//n if n else 0
    letters=[hist[a]*factor for a in range(26)];pixels=[sum(count for a,count in hist.items() if self.base.masks[a]>>p&1)*factor for p in range(35)];row_weights.append(letters+pixels)
  for i,a in enumerate(source):
   r,c=divmod(i,self.w);position=r*self.stride+c;position=self.digits-1-position if reverse else position;offset=step*position
   if expected and i in self.free:
    for plane,weight in enumerate(row_weights[r]):
     if weight:buffers[plane][offset:offset+step]=weight.to_bytes(step,'little')
   else:
    planes=([a] if a<26 else [])+[26+p for p in self.pix[a]]
    for plane in planes:
     if expected:buffers[plane][offset:offset+step]=self.D.to_bytes(step,'little')
     else:buffers[plane][offset]=1
  return [int.from_bytes(b,'little') for b in buffers]
 def correlate(self,source,targets,bits):
  values=[[],[]];typecode='H' if bits==16 else 'Q';step=bits//8
  for model,target in targets.items():
   decoded=[]
   for start,end in ((0,26),(26,61)):
    product=sum(source[i]*target[i] for i in range(start,end));a=array.array(typecode);assert a.itemsize==step;a.frombytes(product.to_bytes(self.coefficients*step,'little'))
    if sys.byteorder!='little':a.byteswap()
    decoded.append(a)
   # Frame order: model, row, column. Empty frames are explicit zeros.
   size=(2*self.h+1)*(2*self.w+1);offset=len(values[0])
   for i in range(offset,offset+size):
    index=self.indices[i]
    for e in range(2):values[e].append(decoded[e][index] if index is not None else 0)
  return values
 def score(self,source):return self.correlate(self.pack(source,16,True),self.target,16)
 def best(self,values,e):
  best=None;bn=bm=0
  for i in self.active:
   n=values[i]*self.D-self.expected[e][i];m=self.weights[e][i]
   if best is None or greater(n,m,bn,bm):best=i;bn=n;bm=m
  return dict(frame=self.frames[best]['id'],difference_numerator=bn,weight=bm,display_stat=stat_display(bn,bm,self.D))

def gzip_csv(header):
 buffer=io.BytesIO();gz=gzip.GzipFile(fileobj=buffer,mode='wb',mtime=0);text=io.TextIOWrapper(gz,encoding='utf-8',newline='');writer=csv.writer(text,lineterminator='\n');writer.writerow(header)
 return buffer,gz,text,writer
def finish_csv(parts):
 buffer,gz,text,writer=parts;text.flush();text.detach();gz.close();return buffer.getvalue()

def actual(engine,output=True,seconds=120):
 start=time.monotonic();b=engine.base;values=engine.score(b.base);records=[];matches_count=aperture_count=0
 match_csv=gzip_csv(['model','dy','dx','letter','cipher_row','cipher_grid_column','cipher_raw_column','cipher_glyph_position','cipher_letter_position','k4_position','tableau_row','tableau_grid_column','tableau_raw_column','tableau_glyph_position','tableau_letter_position']) if output else None
 aperture_csv=gzip_csv(['model','dy','dx','cipher_row','cipher_grid_column','tableau_row','tableau_grid_column','cipher_character','tableau_character','common_mask','common_pixels','full_nonempty_mask_coincidence']) if output else None
 for k,frame in enumerate(engine.frames):
  budget(start,seconds);model,dy,dx=frame['model'],frame['dy'],frame['dx'];target=b.targets[model];eligible=nonempty=full=union=area=0;letters=[];positions=[];k4=[]
  for r in range(max(0,dy),min(engine.h,engine.h+dy)):
   for c in range(max(0,dx),min(engine.w,engine.w+dx)):
    i=r*engine.w+c;j=(r-dy)*engine.w+c-dx;a,t=b.base[i],target[j];A,B=b.masks[a],b.masks[t];common=A&B;pixels=old.pop(common);area+=pixels;union+=old.pop(A|B);eligible+=a<26 and t<26;nonempty+=bool(common);same=bool(common) and A==B;full+=same
    if common:
     aperture_count+=1
     if output:aperture_csv[3].writerow([model,dy,dx,r+1,c+1,r-dy+1,c-dx+1,old.SYMBOLS[a],old.SYMBOLS[t],str(common),pixels,int(same)])
    if a==t and a<26:
     cm,tm=b.cmeta[i],b.tmeta[model][j];letter=old.AZ[a];letters.append(letter);positions.append([r+1,c+1,cm['raw_row_character'],r-dy+1,c-dx+1,tm['raw_row_character'],letter]);matches_count+=1
     if cm['k4_position'] is not None:k4.append(cm['k4_position'])
     if output:match_csv[3].writerow([model,dy,dx,letter,cm['row'],cm['column'],cm['raw_row_character'],cm['glyph_position'],cm['letter_position'],cm['k4_position'],tm['row'],tm['column'],tm['raw_row_character'],tm['glyph_position'],tm['letter_position']])
  if len(letters)!=values[0][k] or area!=values[1][k]:raise AssertionError('packed/direct disagreement')
  record=dict(**frame,comparable_letter_pairs=eligible,label_matches=len(letters),common_pixel_area=area,nonempty_common_aperture_pairs=nonempty,full_mask_coincidences=full,union_pixel_area=union,label_match_fraction=len(letters)/eligible if eligible else None,common_over_union=area/union if union else None,matched_letters=''.join(letters),label_positions=positions,k4_positions=k4,expected_numerators=[engine.expected[e][k] for e in range(2)])
  records.append(record)
 files={'label-matches.csv.gz':finish_csv(match_csv),'aperture-intersections.csv.gz':finish_csv(aperture_csv)} if output else {}
 return dict(records=records,common_expectation_denominator=engine.D,label_position_rows=matches_count,aperture_position_rows=aperture_count,active_frames=len(engine.active),raw_frames=len(records),physical_calibration=False),files

def calibrate(engine,records,scheme,draws,seed,seconds=300):
 start=time.monotonic();rng=random.Random(seed);truth=[[r[name] for r in records] for name in NAMES];exceed=[[0]*len(records) for _ in range(2)];maxima=[[],[]]
 for trial in range(draws):
  budget(start,seconds);source=engine.base.surrogate(rng,scheme);values=engine.score(source)
  for e in range(2):
   maxima[e].append(engine.best(values[e],e))
   for i in engine.active:exceed[e][i]+=values[e][i]>=truth[e][i]
 actual_max=[engine.best(v,e) for e,v in enumerate(truth)];tails=[];per_frame=[];sorted_keys=[sorted(exact_key(x['difference_numerator'],x['weight']) for x in row) for row in maxima]
 for e,name in enumerate(NAMES):
  maximum=actual_max[e];threshold=exact_key(maximum['difference_numerator'],maximum['weight']);count=draws-bisect.bisect_left(sorted_keys[e],threshold);tails.append(dict(endpoint=name,actual_maximum=maximum,exceedances=count,plus_one_p=(count+1)/(draws+1),four_report_adjusted_p=min(1,4*(count+1)/(draws+1))))
 for i,frame in enumerate(engine.frames):
  endpoints={}
  for e,name in enumerate(NAMES):
   if i not in engine.active:endpoints[name]=None;continue
   n=truth[e][i]*engine.D-engine.expected[e][i];threshold=exact_key(n,engine.weights[e][i]);count=draws-bisect.bisect_left(sorted_keys[e],threshold)
   endpoints[name]=dict(raw_plus_one_p=(exceed[e][i]+1)/(draws+1),family_max_plus_one_p=(count+1)/(draws+1),four_report_adjusted_p=min(1,4*(count+1)/(draws+1)))
  per_frame.append(dict(id=frame['id'],endpoints=endpoints))
 return dict(scheme=scheme,seed=seed,draws=draws,raw_frames=len(records),active_frames=len(engine.active),common_expectation_denominator=engine.D,family_endpoints=tails,per_frame=per_frame,null_maxima=dict(zip(NAMES,maxima)),seconds=time.monotonic()-start,scope='Entire two-dimensional/two-registration selector; conditional row structure and fixed anchor, not English/artist intent or a cipher posterior.')


def toy_data(rows,models,fixed=()):return dict(width=max(len(x) for x in rows),cipher_rows=rows,models=models,observed_anchor={'fixed_cipher_raw_indices_for_conditional_null':list(fixed)})
def controls():
 start=time.monotonic();checks=0;plants=[];rows=['ABCDE','FGHIJ','KLMNO','PQRST'];models={'FORWARD':rows,'REVERSED':[r[::-1] for r in rows]}
 for model in models:
  for dy in (-1,0,1):
   for dx in (-1,0,1):
    source=[''.join(models[model][r-dy][c-dx] if 0<=r-dy<4 and 0<=c-dx<5 else 'Z' for c in range(5)) for r in range(4)];engine=Engine(toy_data(source,models));result,_=actual(engine,False);records=result['records'];values=[r['label_matches'] for r in records];best=max(values);winners=[r['id'] for r in records if r['label_matches']==best];truth=f'{model}:{dy}:{dx}';assert truth in winners;plants.append(dict(truth=truth,winners=winners));checks+=1
 # Exact mean over every raw permutation/rotation, including duplicate values.
 rows=['ABC','?CA'];models={'FIRST':['BAC','A? '],'SECOND':['CAB',' CA']};engine=Engine(toy_data(rows,models,[(0,0)]));score_count=0
 for scheme in ('shuffle','rotation'):
  free=engine.base.free;options=[]
  for positions in free:
   values=[engine.base.base[i] for i in positions];options.append(list(itertools.permutations(values)) if scheme=='shuffle' else [values[k:]+values[:k] for k in range(len(values))])
  totals=[[0]*len(engine.frames) for _ in range(2)];n=0
  for choices in itertools.product(*options):
   source=engine.base.base[:]
   for positions,values in zip(free,choices):
    for i,v in zip(positions,values):source[i]=v
   values=engine.score(source);n+=1
   for e in range(2):totals[e]=[a+b for a,b in zip(totals[e],values[e])]
   cdata=toy_data([''.join(old.SYMBOLS[source[r*3+c]] for c in range(3)) for r in range(2)],models);direct,_=actual(Engine(cdata),False)
   for e,name in enumerate(NAMES):assert values[e]==[r[name] for r in direct['records']]
   checks+=1
  for e in range(2):
   for i in range(len(engine.frames)):assert Fraction(totals[e][i],n)==Fraction(engine.expected[e][i],engine.D)
  checks+=1
 # Ambiguity is retained, not converted to a unique planted recovery claim.
 same=Engine(toy_data(['AAA','AAA'],{'ONE':['AAA','AAA'],'TWO':['AAA','AAA']}));vals=same.score(same.base.base)[0];ties=[same.frames[i]['id'] for i,x in enumerate(vals) if x==max(vals)];assert len(ties)==2;checks+=1
 for n in range(-3,4):
  for m in range(1,4):
   for bn in range(-3,4):
    for bm in range(1,4):assert greater(n,m,bn,bm)==(exact_key(n,m)>exact_key(bn,bm));checks+=1
 # Independent forward/pixel oracle on two synthetic geometries only.
 for data in (toy_data(['ABC','?CA'],{'ONE':['BAC','A? '],'TWO':['CAB',' CA']},[(0,0)]),toy_data(['ABCDE','FGH','IJKL','M'],{'ONE':['ABCDE',' FGH','IJK','LMNOP']})):
  native,_=actual(Engine(data),False);independent=oracle(data)
  assert len(native['records'])==len(independent['records'])
  for a,b in zip(native['records'],independent['records']):
   for key,value in b.items():assert a[key]==value,(a['id'],key)
  checks+=1
 return dict(checks=checks,failures=[],plants=plants,ambiguous_tie_fixture=ties,seconds=time.monotonic()-start,actual_new_rankings_examined=False)


def oracle(data=None,glyphs=None):
 args=['/opt/homebrew/bin/node',str(ROOT/'experiments/monument_slide_2d_oracle.mjs')]
 if data is None:args+=['--actual'];raw=subprocess.check_output(args,timeout=120)
 else:args+=['--stdin'];raw=subprocess.check_output(args,input=json.dumps(dict(input=data,glyphs=glyphs or json.loads((ROOT/'data/fold-aperture-surrogate-v1.json').read_text())['glyph_rows'])).encode(),timeout=60)
 return json.loads(raw)

def run(spec_commit):
 spec=json.loads(SPEC.read_text());committed=subprocess.check_output(['git','show',spec_commit+':research/specifications/FOLD-SLIDE-2D-001.json'],cwd=ROOT)
 if committed!=SPEC.read_bytes():raise ValueError('specification differs from frozen commit')
 for p,digest in spec['source_sha256'].items():
  if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=digest:raise ValueError('changed pinned input '+p)
 code_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();paths=list(spec['source_sha256'])+['research/specifications/FOLD-SLIDE-2D-001.json','experiments/monument_slide_2d.py','experiments/monument_slide_2d_oracle.mjs','experiments/run_io.py'];hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}
 for p in ('experiments/monument_slide_2d.py','experiments/monument_slide_2d_oracle.mjs'):
  if subprocess.check_output(['git','show',code_commit+':'+p],cwd=ROOT)!=(ROOT/p).read_bytes():raise ValueError('implementation not committed')
 root=ROOT/'results/fold-slide-2d-001-runs';registration=dict(commit=spec_commit,file='research/specifications/FOLD-SLIDE-2D-001.json',sha256=hashes['research/specifications/FOLD-SLIDE-2D-001.json'])
 with RunSnapshot(root,'FOLD-SLIDE-2D-001',registration,execution_kind='original') as snapshot:
  def job(name,action,limit):
   row=dict(experiment=name,status='running',started_at_utc=utc(),deadline_seconds=limit);snapshot.manifest['jobs'].append(row);start=time.monotonic()
   try:answer=action();budget(start,limit);row['status']='completed';return answer
   except BaseException:row['status']='incomplete';raise
   finally:row['finished_at_utc']=utc()
  result=job('synthetic-controls',controls,60);snapshot.write('controls.json',json_bytes(result))
  def prepare_actual():
   engine=Engine();result,files=actual(engine);return engine,result,files
  engine,actual_result,files=job('prepare-and-actual-all-frames',prepare_actual,120)
  if len(actual_result['records'])!=spec['raw_frames'] or len(engine.active)!=spec['active_frames']:raise AssertionError('wrong domain')
  old_records={r['id']:r for r in json.loads((ROOT/'results/FOLD-SLIDE-020-actual.json').read_text())['records']}
  for r in actual_result['records']:
   if r['dy']!=0:continue
   previous=old_records[f"{r['model']}:{r['dx']}"]
   for field in ('label_matches','common_pixel_area','nonempty_common_aperture_pairs','full_mask_coincidences','union_pixel_area','comparable_letter_pairs','matched_letters'):assert r[field]==previous[field]
   for e in range(2):assert Fraction(r['expected_numerators'][e],engine.D)==Fraction(previous['expected_rational'][e])
  snapshot.write('actual.json',json_bytes(actual_result))
  for path,raw in files.items():snapshot.write(path,raw)
  independent=job('independent-cell-pixel-oracle',oracle,120)
  for a,b in zip(actual_result['records'],independent['records']):
   for key,value in b.items():assert a[key]==value,(a['id'],key)
  assert len(independent['records'])==len(actual_result['records']);snapshot.write('independent.json',json_bytes(independent))
  summaries=[]
  for null in spec['nulls']:
   report=job('whole-search-null-'+null['scheme'],lambda null=null:calibrate(engine,actual_result['records'],null['scheme'],null['draws'],null['seed']),300);snapshot.write('null-'+null['scheme']+'.json',json_bytes(report));summaries.append(dict(scheme=null['scheme'],family_endpoints=report['family_endpoints']))
  summary=dict(id=spec['id'],status='completed',spec_commit=spec_commit,code_commit=code_commit,file_sha256=hashes,raw_frames=len(engine.frames),active_frames=len(engine.active),prior_row_zero_frames=134,new_nonzero_row_frames=7504,common_expectation_denominator=engine.D,physical_calibration=False,null_reports=summaries,label_position_rows=actual_result['label_position_rows'],aperture_position_rows=actual_result['aperture_position_rows'],independent_frames_verified=len(independent['records']),new_cipher_or_plaintext_candidate=False,started_at_utc=snapshot.manifest['started_at_utc'],finished_at_utc=utc(),timing_note='Summary end follows computation; manifest end includes publication of staged artifacts.')
  snapshot.write('summary.json',json_bytes(summary));run_id=snapshot.run_id
 return run_id

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--controls',action='store_true');parser.add_argument('--run',action='store_true');parser.add_argument('--spec-commit');args=parser.parse_args()
 if args.controls:print(json.dumps(controls(),indent=2))
 elif args.run and args.spec_commit:print(run(args.spec_commit))
 else:parser.error('choose --controls or --run --spec-commit FULL_SHA')
