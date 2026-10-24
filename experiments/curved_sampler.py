"""Invented ideal cylindrical mirror sampler. No monument reflectance or K4 fit."""
import math
ALPHABET='KRYPTOSABCDEFGHIJLMNQUVWXZ'
EPS=1e-10
RIM=1e-9

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def add(a,b,t=1):return tuple(x+t*y for x,y in zip(a,b))
def norm(v):
 n=math.sqrt(dot(v,v))
 if n<EPS:raise ValueError('zero direction')
 return tuple(x/n for x in v)
def reflect(d,n):return add(d,n,-2*dot(d,n))
def basis(angle):
 a=math.radians(angle);return (0,math.cos(a),-math.sin(a)),(1,0,0),(0,math.sin(a),math.cos(a))
def reticle():
 return [dict(index=0,row=r,column=c,u=(c-15)/15,v=(1.5-r)/15) for r in range(4) for c in (range(27,31) if r==0 else range(31))]
RETICLE=reticle()
for _i,_point in enumerate(RETICLE):_point['index']=_i+1

def first_hit(eye,d):
 # Opaque closed cylinder; first hit may be a cap rather than a mirror side.
 a=d[0]**2+d[1]**2;b=2*(eye[0]*d[0]+eye[1]*d[1]);c=eye[0]**2+eye[1]**2-1;candidates=[]
 if a>EPS:
  delta=b*b-4*a*c
  if delta>=0:
   root=math.sqrt(delta)
   for t in ((-b-root)/(2*a),(-b+root)/(2*a)):
    z=eye[2]+t*d[2]
    if t>EPS and -RIM<=z<=2+RIM:candidates.append((t,'side'))
 if abs(d[2])>EPS:
  for z in (0,2):
   t=(z-eye[2])/d[2];x,y,_=add(eye,d,t)
   if t>EPS and x*x+y*y<=1+RIM:candidates.append((t,'cap'))
 if not candidates:return dict(status='miss')
 t,kind=min(candidates);hit=add(eye,d,t)
 if min(abs(hit[2]),abs(hit[2]-2))<=RIM and abs(hit[0]**2+hit[1]**2-1)<=RIM:return dict(status='rim',hit=hit)
 if kind=='cap':return dict(status='cap',hit=hit)
 n=norm((hit[0],hit[1],0))
 if abs(dot(d,n))<1e-4:return dict(status='grazing',hit=hit)
 return dict(status='side',hit=hit,normal=n,distance=t)

def ground_ray(eye,d):
 d=norm(d);out=first_hit(eye,d)
 if out['status']!='side':return out
 hit=out['hit'];r=reflect(d,out['normal']);out.update(incoming=d,reflected=r)
 if r[2]>=-1e-8:return dict(out,status='ground_miss')
 t=-hit[2]/r[2]
 if t<=EPS:return dict(out,status='ground_behind')
 point=add(hit,r,t)
 if point[0]**2+point[1]**2<=1+RIM:return dict(out,status='inside_cylinder')
 # A convex-cylinder outgoing ray has r·n>0, hence cannot re-enter it.
 if dot(r,out['normal'])<=0:return dict(out,status='occluded')
 return dict(out,status='ground',point=point,ground_distance=t)

def trace(params,u,v,eye_offset=(0,0,0),fixed_reticle=False):
 if not all(math.isfinite(params[k]) for k in ('D','H','s','aim_deg')) or params['D']<=1 or params['H']<=0 or params['s']<=0:return dict(status='invalid_parameters')
 f,right,up=basis(params['aim_deg']);base=(0,-params['D'],params['H']);eye=add(base,eye_offset)
 direction=add(add(f,right,params['s']*u),up,params['s']*v)
 if fixed_reticle:
  target=add(base,direction,.5);direction=add(target,eye,-1)
 return ground_ray(eye,direction)

def table_cell(point,params,rows):
 if not all(math.isfinite(params[k]) for k in ('tx','ty','rotation_deg','pitch')) or params['pitch']<=0 or not all(math.isfinite(x) for x in point):return dict(status='invalid_parameters')
 t=math.radians(params['rotation_deg']);cs,sn=math.cos(t),math.sin(t);dx,dy=point[0]-params['tx'],point[1]-params['ty'];x=(cs*dx+sn*dy)/params['pitch']+15;y=13.5-(-sn*dx+cs*dy)/params['pitch'];col,row=math.floor(x+.5),math.floor(y+.5);margin=min(.5-abs(x-col),.5-abs(y-row));base=dict(row=row,column=col,column_coordinate=x,row_coordinate=y,margin=margin)
 if not 0<=row<len(rows) or not 0<=col<len(rows[row]):return dict(base,status='outside')
 ch=rows[row][col]
 if ch not in ALPHABET:return dict(base,status='blank',letter=ch)
 if margin<=.02:return dict(base,status='boundary',letter=ch)
 return dict(base,status='valid',letter=ch)

def sample(params,rows,eye_offset=(0,0,0),fixed_reticle=False,ground=None):
 records=[]
 for i,pt in enumerate(RETICLE):
  ray=ground[i] if ground is not None else trace(params,pt['u'],pt['v'],eye_offset,fixed_reticle)
  record=dict(index=i+1,reticle_row=pt['row'],reticle_column=pt['column'],ray=ray)
  if ray['status']=='ground':record.update(table_cell(ray['point'],params,rows))
  else:record['status']=ray['status']
  records.append(record)
 key=''.join(x['letter'] for x in records) if all(x['status']=='valid' for x in records) else None
 cells={(x['row'],x['column']) for x in records if x['status']=='valid'}
 return dict(params=params,key=key,complete=key is not None,distinct_cells=len(cells),distinct_letters=len(set(key)) if key else 0,minimum_margin=min((x['margin'] for x in records if 'margin' in x),default=None),records=records)

def encrypt(plain,key,decrypt=False):
 if len(plain)!=len(key) or any(c not in ALPHABET for c in plain+key):raise ValueError('Equal-length ordinary letters/key required')
 return ''.join(ALPHABET[(ALPHABET.index(a)+(-1 if decrypt else 1)*ALPHABET.index(b))%26] for a,b in zip(plain,key))

def recover_keys(cipher,known,panel):
 first={i:v for i,v in known.items() if 21<=i<=33};partial=[];complete=[]
 for key,owners in panel.items():
  plain=encrypt(cipher,key,True)
  if all(plain[i]==v for i,v in first.items()):partial.append(key)
  if all(plain[i]==v for i,v in known.items()):
   assert encrypt(plain,key)==cipher;complete.append(dict(key=key,owners=owners,plaintext=plain,full_reencryption=True))
 return dict(first13_key_classes=partial,full24_candidates=complete)
