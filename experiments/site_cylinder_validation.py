"""Independent closest-approach/complex-reflection replay of exact Site v1 model.
No Site imports, horizontal-table substitution or K4 cryptanalysis.
"""
import itertools,math
ALPHABET='KRYPTOSABCDEFGHIJLMNQUVWXZ'
DEFAULTS=dict(version=1,radius=.8,eyeDistance=4,tableauDistance=6,shiftX=.037,shiftY=.043,reticleWidth=.225,selected=1,obstruction=False,view='mirror',screenYaw=0)
PARAMS=('radius','eyeDistance','tableauDistance','shiftX','shiftY','reticleWidth')
RANGES={'radius':(.25,1.4),'eyeDistance':(2.5,7),'tableauDistance':(4,10),'shiftX':(-4,4),'shiftY':(-3,3),'reticleWidth':(.1,.9),'selected':(1,97),'screenYaw':(-70,70)}
def validate(raw):
 if not isinstance(raw,dict) or set(raw)!=set(DEFAULTS):raise ValueError('Exact global state fields required')
 for k,(lo,hi) in RANGES.items():
  if type(raw[k]) not in (int,float) or not math.isfinite(raw[k]) or not lo<=raw[k]<=hi:raise ValueError('Invalid '+k)
 if type(raw['version']) not in (int,float) or raw['version']!=1 or raw['selected']!=int(raw['selected']) or type(raw['obstruction']) is not bool or raw['view'] not in ('mirror','screen'):raise ValueError('Invalid mode/version')
 if raw['tableauDistance']<=raw['eyeDistance']+.2:raise ValueError('Tableau too close')
 return dict(raw)
def plus(a,b,t=1):return tuple(x+t*y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def unit(d):
 length=math.hypot(*d)
 if not math.isfinite(length) or length<1e-12:raise ValueError('Zero direction')
 return tuple(x/length for x in d)
def hit(eye,d,radius,height=3):
 d=unit(d);speed=math.hypot(d[0],d[2])
 if speed**2<1e-14:return dict(status='miss-cylinder')
 ux,uz=d[0]/speed,d[2]/speed;along=-(eye[0]*ux+eye[2]*uz);perp=eye[0]*uz-eye[2]*ux;chord2=radius**2-perp**2;disc=4*speed**2*chord2
 if disc<0:return dict(status='miss-cylinder')
 if disc<1e-12:return dict(status='grazing-cylinder')
 half=math.sqrt(chord2);distances=[t/speed for t in (along-half,along+half) if t/speed>1e-9]
 if not distances:return dict(status='mirror-behind-eye')
 distance=min(distances);point=plus(eye,d,distance)
 if point[1]<=1e-9 or point[1]>=height-1e-9:return dict(status='outside-mirror-height',point=point)
 norm=unit((point[0],0,point[2]));return dict(status='hit',point=point,normal=norm,direction=d,distance=distance)
def reflected(d,n):
 # Complex reflection about a tangent, independent of source vector expression.
 normal=complex(n[0],n[2]);value=-(normal*normal)*complex(d[0],d[2]).conjugate();return (value.real,d[1],value.imag)
def blocked(a,b):
 intervals=[(1e-8,1-1e-8)]
 for i,(lo,hi) in enumerate(zip((-.18,0,2),(.18,3,2.2))):
  delta=b[i]-a[i]
  if abs(delta)<1e-14:
   if not lo<=a[i]<=hi:return False
  else:intervals.append(tuple(sorted(((lo-a[i])/delta,(hi-a[i])/delta))))
 return max(x[0] for x in intervals)<=min(x[1] for x in intervals)
def rotate(v,angles):
 x,y,z=v;pitch,yaw,roll=map(math.radians,angles);y,z=y*math.cos(pitch)-z*math.sin(pitch),y*math.sin(pitch)+z*math.cos(pitch);x,z=x*math.cos(yaw)+z*math.sin(yaw),-x*math.sin(yaw)+z*math.cos(yaw);x,y=x*math.cos(roll)-y*math.sin(roll),x*math.sin(roll)+y*math.cos(roll);return (x,y,z)
def sample(state,index,rows,nuisance=None):
 s=validate(state);n=nuisance or {};position=index-1+27;row,col=divmod(position,31);eye=(n.get('eyeX',0),1.5+n.get('eyeY',0),s['eyeDistance']);q=((col-15)*s['reticleWidth']/31,1.5+n.get('reticleY',0)+(1.5-row)*.075*(1+n.get('verticalPitchFraction',0)),2+n.get('reticleZ',0));h=hit(eye,plus(q,eye,-1),s['radius']);out=dict(index=index,row=row,column=col,eye=eye,reticle=q,status=h['status'],key=None)
 if h['status']!='hit':return out
 out.update(hit=h['point'],normal=h['normal'],eyeToMirror=h['direction']);r=reflected(h['direction'],h['normal']);out['reflectedTrace']=r
 angles=(n.get('boardPitchDeg',0),n.get('boardYawDeg',0),n.get('boardRollDeg',0));right=rotate((1,0,0),angles);up=rotate((0,1,0),angles);normal=rotate((0,0,1),angles);centre=(s['shiftX'],1.5+s['shiftY'],s['tableauDistance']);denominator=dot(r,normal)
 t=dot(plus(centre,h['point'],-1),normal)/denominator if denominator else float('inf')
 if not math.isfinite(t) or t<=1e-9:return dict(out,status='miss-tableau-plane')
 point=plus(h['point'],r,t);out['tableauPoint']=point
 if s['obstruction'] and (blocked(eye,h['point']) or blocked(h['point'],point)):return dict(out,status='blocked-by-hypothetical-card')
 local=plus(point,centre,-1);u=(dot(local,right)+4.125)/.25;v=(3.5-dot(local,up))/.25;ci,ri=math.floor(u),math.floor(v);out.update(cell=dict(row=ri+1,column=ci+1),coordinates=(u,v))
 if ci<0 or ci>=33 or ri<0 or ri>=28:return dict(out,status='outside-tableau')
 margin=min(u-ci,1-u+ci,v-ri,1-v+ri);out['margin']=margin
 if margin<=.01:return dict(out,status='cell-boundary-ambiguous')
 j=ci-(33-len(rows[ri]))//2
 if not 0<=j<len(rows[ri]) or rows[ri][j] not in ALPHABET:return dict(out,status='blank-tableau-cell')
 return dict(out,status='valid',key=rows[ri][j],source=dict(row=ri+1,column=j+1,modelColumn=ci+1))
def generate(state,rows,nuisance=None):
 records=[sample(state,i,rows,nuisance) for i in range(1,98)];valid=sum(x['status']=='valid' for x in records);key=''.join(x['key'] for x in records) if valid==97 else None
 return dict(samples=records,validCount=valid,invalidCount=97-valid,key=key,minimum_margin=min((x['margin'] for x in records if 'margin' in x),default=None),cell_path=[x.get('cell') for x in records],distinct_cells=len({(x['cell']['row'],x['cell']['column']) for x in records if x['status']=='valid'}))
def neighborhood():
 values=((.796,.8,.804),(3.99,4,4.01),(5.99,6,6.01),(.032,.037,.042),(.038,.043,.048),(.22275,.225,.22725))
 for index,combo in enumerate(itertools.product(*values)):yield index,dict(DEFAULTS,**dict(zip(PARAMS,combo)))
def choose(rows):
 complete=[x for x in rows if x['result']['validCount']==97];baseline=next(x for x in rows if all(x['state'][k]==DEFAULTS[k] for k in PARAMS));path=baseline['result']['cell_path'];order=lambda x:(-round(x['result']['minimum_margin'],9),tuple(round(x['state'][k],12) for k in PARAMS));same=sorted((x for x in complete if x['result']['cell_path']==path),key=order)[:5];different=sorted((x for x in complete if x['result']['cell_path']!=path),key=order)[:5];selected={x['id']:x for x in [baseline]+same+different}
 return list(selected.values())
def addition(text,key,inverse=False):
 if len(text)!=len(key) or any(x not in ALPHABET for x in text+key):raise ValueError('Equal letter strings required')
 return ''.join(ALPHABET[(ALPHABET.index(x)+(-1 if inverse else 1)*ALPHABET.index(k))%26] for x,k in zip(text,key))
