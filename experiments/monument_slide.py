"""Frozen double-reflection inscription slide; approximate square-aperture control."""
import collections,csv,hashlib,json,math,random,sys,time,resource
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SCALE=65536;AZ='ABCDEFGHIJKLMNOPQRSTUVWXYZ';SYMBOLS=AZ+'? ';BLANK=27

def pop(x):return x.bit_count() if hasattr(int,'bit_count') else bin(x).count('1')
def mirror(mask):
 out=0
 for y in range(7):
  for x in range(5):
   if mask>>(y*5+x)&1:out|=1<<(y*5+4-x)
 return out

def glyph_masks(data=None):
 data=json.loads((ROOT/'data/fold-aperture-surrogate-v1.json').read_text()) if data is None else data
 result=[]
 for ch in SYMBOLS:
  rows=data['glyph_rows'].get(ch,['00000']*7);result.append(sum((digit=='1')<<(y*5+x) for y,row in enumerate(rows) for x,digit in enumerate(row)))
 return result

def grid(rows,width,region,k4=None):
 flat=[];meta=[];glyphpos=0;letterpos=0;total=sum(len(row.replace(' ','')) for row in rows);suffix=total-len(k4) if k4 else None
 if k4:assert ''.join(rows).replace(' ','').endswith(k4)
 for r,row in enumerate(rows):
  if len(row)>width or any(ch not in SYMBOLS for ch in row):raise ValueError('invalid transcript row')
  pad=(width-len(row))//2
  for c in range(width):
   j=c-pad;raw=row[j] if 0<=j<len(row) else ' ';index=j+1 if 0<=j<len(row) else None
   if raw!=' ':glyphpos+=1
   if raw in AZ:letterpos+=1
   flat.append(SYMBOLS.index(raw));meta.append(dict(region=region,row=r+1,column=c+1,raw_row_character=index,character=raw,glyph_position=glyphpos if raw!=' ' else None,letter_position=letterpos if raw in AZ else None,k4_position=glyphpos-suffix if suffix is not None and raw!=' ' and glyphpos>suffix else None))
 return flat,meta

class Model:
 def __init__(self,data=None,glyph_data=None):
  default=data is None;self.data=json.loads((ROOT/'data/monument-slide-input-v2.json').read_text()) if default else data;self.w=self.data['width'];self.h=len(self.data['cipher_rows']);self.masks=glyph_masks(glyph_data);self.base,self.cmeta=grid(self.data['cipher_rows'],self.w,'C',json.loads((ROOT/'data/k4.json').read_text())['ciphertext'] if default else None)
  if self.w*self.h*35>=SCALE:raise ValueError('packed score overflow')
  self.fixed=set()
  for r,j in self.data.get('observed_anchor',{}).get('fixed_cipher_raw_indices_for_conditional_null',[]):
   self.fixed.add(r*self.w+(self.w-len(self.data['cipher_rows'][r]))//2+j)
  self.free=[[i for i in range(r*self.w,(r+1)*self.w) if self.base[i]<26 and i not in self.fixed] for r in range(self.h)];self.hist=[collections.Counter(self.base[i] for i in row) for row in self.free]
  self.tables=[[((a==b and a<26)*SCALE)+pop(self.masks[a]&self.masks[b]) for a in range(28)] for b in range(28)];self.frames=[];self.targets={};self.tmeta={}
  for name,rows in self.data['models'].items():
   if len(rows)!=self.h:raise ValueError('unequal row counts')
   target,meta=grid(rows,self.w,'T');self.targets[name]=target;self.tmeta[name]=meta
   for shift in range(-self.w,self.w+1):
    pairs=[(r*self.w+c,r*self.w+c-shift) for r in range(self.h) for c in range(self.w) if 0<=c-shift<self.w];lookup=[(i,self.tables[target[j]]) for i,j in pairs]
    expected=[Fraction(),Fraction()]
    for i,j in pairs:
     b=target[j];a=self.base[i];row=i//self.w
     if i in self.free[row]:
      hist=self.hist[row];n=len(self.free[row]);expected[0]+=Fraction(hist[b],n) if b<26 else 0;expected[1]+=Fraction(sum(count*pop(self.masks[x]&self.masks[b]) for x,count in hist.items()),n)
     else:expected[0]+=int(a==b and a<26);expected[1]+=pop(self.masks[a]&self.masks[b])
    self.frames.append(dict(id=name+':'+str(shift),model=name,shift=shift,pairs=pairs,lookup=lookup,geometric_overlap=len(pairs),expected=[float(x) for x in expected],expected_rational=[str(x) for x in expected],active=bool(pairs)))
 def scores(self,source):return [sum(row[source[i]] for i,row in frame['lookup']) for frame in self.frames]
 def actual(self):
  encoded=self.scores(self.base);records=[]
  for frame,score in zip(self.frames,encoded):
   matches=[];overlaps=[];eligible=0;nonempty=0;full=0;union=0;area=score%SCALE;target=self.targets[frame['model']]
   for i,j in frame['pairs']:
    a,b=self.base[i],target[j];A,B=self.masks[a],self.masks[b];common=A&B;union+=pop(A|B);eligible+=a<26 and b<26;nonempty+=bool(common);full+=bool(common) and A==B
    if a==b and a<26:matches.append(dict(cipher=self.cmeta[i],tableau=self.tmeta[frame['model']][j]))
    if common:overlaps.append(dict(cipher_cell=i,tableau_cell=j,common_mask=str(common),common_pixels=pop(common),cipher_character=SYMBOLS[a],tableau_character=SYMBOLS[b]))
   records.append(dict(id=frame['id'],model=frame['model'],shift=frame['shift'],geometric_overlap_cells=frame['geometric_overlap'],comparable_letter_pairs=eligible,label_matches=score//SCALE,full_mask_coincidences=full,nonempty_common_aperture_pairs=nonempty,common_pixel_area=area,union_pixel_area=union,common_over_union=area/union if union else None,label_match_fraction=(score//SCALE)/eligible if eligible else None,expected=frame['expected'],expected_rational=frame['expected_rational'],matched_letters=''.join(p['cipher']['character'] for p in matches),matches=matches,k4_matches=[p for p in matches if p['cipher']['k4_position'] is not None],aperture_intersections=overlaps))
  return records
 def surrogate(self,rng,scheme):
  out=self.base[:]
  for positions in self.free:
   values=[self.base[i] for i in positions]
   if scheme=='shuffle':rng.shuffle(values)
   elif scheme=='rotation':
    if values:k=rng.randrange(len(values));values=values[k:]+values[:k]
   else:raise ValueError('unknown conditional null')
   for i,value in zip(positions,values):out[i]=value
  return out

def stat(value,mean):return (value-mean)/math.sqrt(max(mean,1))
def nulls(model,records,scheme,n=1999,seed=None):
 import bisect
 seed=(202610231230 if scheme=='shuffle' else 202610231231) if seed is None else seed;rng=random.Random(seed);start=time.monotonic();maxima=[[],[]];exceed=[[0]*len(records) for _ in range(2)];active=[i for i,f in enumerate(model.frames) if f['active']]
 for trial in range(n):
  if time.monotonic()-start>120:raise TimeoutError('null budget unresolved')
  rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
  if rss>1<<30:raise MemoryError('null RSS budget unresolved')
  source=model.surrogate(rng,scheme);scores=model.scores(source);values=([s//SCALE for s in scores],[s%SCALE for s in scores])
  for endpoint,name in enumerate(('label_matches','common_pixel_area')):
   maxima[endpoint].append(max(stat(values[endpoint][i],records[i]['expected'][endpoint]) for i in active))
   for i in active:exceed[endpoint][i]+=values[endpoint][i]>=records[i][name]
 actual_max=[max(stat(r[name],r['expected'][e]) for i,r in enumerate(records) if i in active) for e,name in enumerate(('label_matches','common_pixel_area'))];tails=[];per_frame=[]
 for endpoint,name in enumerate(('label_matches','common_pixel_area')):
  sorted_max=sorted(maxima[endpoint]);k=n-bisect.bisect_left(sorted_max,actual_max[endpoint]);tails.append(dict(endpoint=name,actual_family_max=actual_max[endpoint],exceedances=k,plus_one_p=(k+1)/(n+1),four_report_adjusted_p=min(1,4*(k+1)/(n+1))))
 for i,r in enumerate(records):
  row=dict(id=r['id'],endpoints={})
  for e,name in enumerate(('label_matches','common_pixel_area')):
   if i not in active:row['endpoints'][name]=None;continue
   threshold=stat(r[name],r['expected'][e]);k=n-bisect.bisect_left(sorted(maxima[e]),threshold);row['endpoints'][name]=dict(raw_plus_one_p=(exceed[e][i]+1)/(n+1),family_max_plus_one_p=(k+1)/(n+1),four_report_adjusted_p=min(1,4*(k+1)/(n+1)))
  per_frame.append(row)
 return dict(scheme=scheme,seed=seed,controls=n,active_family=len(active),family_endpoints=tails,per_frame=per_frame,null_family_maxima=dict(label_matches=maxima[0],common_pixel_area=maxima[1]),seconds=time.monotonic()-start,scope='Conditional row structure and five supplied anchor letters; all shifts/models re-evaluated, not an English/null-intent or solution probability.')

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--actual',action='store_true');p.add_argument('--null',choices=('shuffle','rotation'));p.add_argument('--output',required=True);a=p.parse_args();m=Model()
 if a.actual:result=dict(id='FOLD-SLIDE-020',records=m.actual(),models=list(m.targets),transforms={'initial_tableau_view_mirror':True,'fold_mirror':True,'net_glyph_mirror':False},publication_baseline='6f269e11bec1a7b2f87e67f014b7b139708d0c61',physical_calibration=False)
 else:result=nulls(m,m.actual(),a.null)
 pins=['experiments/monument_slide.py','data/monument-slide-input-v2.json','data/fold-aperture-surrogate-v1.json','research/MONUMENT-SLIDE-OVERLAY-SPEC.md','research/MONUMENT-SLIDE-REGISTRATION-AMENDMENT.md'];result['source_sha256']={x:hashlib.sha256((ROOT/x).read_bytes()).hexdigest() for x in pins};Path(a.output).write_text(json.dumps(result,indent=2)+'\n')
