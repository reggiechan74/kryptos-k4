"""Image-line concurrence only. No physical emitter reconstruction or cipher input."""
import math, random

EPS=1e-12

def cross(a,b):
 return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def unit(v):
 n=math.sqrt(dot(v,v))
 if n<EPS:raise ValueError('zero vector')
 v=[x/n for x in v]
 k=max(range(len(v)),key=lambda i:abs(v[i]))
 return v if v[k]>=0 else [-x for x in v]
def eigensystem(matrix):
 """Symmetric Jacobi rotations; returned eigenvectors are matrix columns."""
 a=[list(row) for row in matrix];v=[[float(i==j) for j in range(3)] for i in range(3)]
 for _ in range(100):
  p,q=max(((0,1),(0,2),(1,2)),key=lambda ij:abs(a[ij[0]][ij[1]]))
  if abs(a[p][q])<=1e-15*max(1,sum(abs(a[i][i]) for i in range(3))):break
  tau=(a[q][q]-a[p][p])/(2*a[p][q]);t=(1 if tau>=0 else -1)/(abs(tau)+math.sqrt(1+tau*tau));c=1/math.sqrt(1+t*t);s=t*c
  app,aqq,apq=a[p][p],a[q][q],a[p][q]
  a[p][p]=app-t*apq;a[q][q]=aqq+t*apq;a[p][q]=a[q][p]=0.0
  for k in range(3):
   if k not in (p,q):
    akp,akq=a[k][p],a[k][q];a[k][p]=a[p][k]=c*akp-s*akq;a[k][q]=a[q][k]=s*akp+c*akq
   vp,vq=v[k][p],v[k][q];v[k][p]=c*vp-s*vq;v[k][q]=s*vp+c*vq
 return sorted([(a[i][i],unit([v[k][i] for k in range(3)])) for i in range(3)],key=lambda x:x[0])

def normalize(p,width,height):return [(p[0]-width/2)/max(width,height),(p[1]-height/2)/max(width,height),1.0]
def image_source(s,width,height):
 scale=max(width,height)
 return unit([s[0]*scale+s[2]*width/2,s[1]*scale+s[2]*height/2,s[2]])
def line(a,g):
 l=cross(a,g);n=math.hypot(l[0],l[1])
 if n<EPS:raise ValueError('collapsed aperture/receiver segment')
 return [x/n for x in l]
def fit(pairs,width,height,training):
 if width<=0 or height<=0:raise ValueError('positive image dimensions required')
 if len(set(training))!=len(training) or len(training)<2:raise ValueError('at least two distinct training indices')
 lines=[line(normalize(pairs[i]['aperture'],width,height),normalize(pairs[i]['receiver'],width,height)) for i in training]
 scatter=[[sum(l[i]*l[j] for l in lines) for j in range(3)] for i in range(3)]
 e=eigensystem(scatter);values=[x[0] for x in e];s=e[0][1]
 relative_gap=(values[1]-values[0])/max(EPS,values[2]);warnings=[]
 if relative_gap<1e-7:warnings.append('nonunique_or_ill_conditioned_source')
 if len(training)<3:warnings.append('two_lines_determine_intersection_without_redundancy')
 px=image_source(s,width,height)
 return dict(source_normalized_homogeneous=s,source_image_homogeneous=px,source_image_finite=None if abs(px[2])<EPS else [px[0]/px[2],px[1]/px[2]],eigenvalues=values,relative_eigen_gap=relative_gap,warnings=warnings,training_indices=training)

def residual(pair,s,width,height,sigma_factor=1.0):
 a=normalize(pair['aperture'],width,height);g=normalize(pair['receiver'],width,height);l=cross(a,g);f=dot(l,s)
 grad=[-s[1]+g[1]*s[2],s[0]-g[0]*s[2],s[1]-a[1]*s[2],-s[0]+a[0]*s[2]]
 sigma=pair['sigma_px']*sigma_factor/max(width,height)
 if sigma<=0:raise ValueError('positive pick sigma required')
 variance=sigma*sigma*dot(grad,grad)
 pred=cross(a,s);n=math.hypot(pred[0],pred[1])
 if n<EPS:return dict(status='source_coincident_with_aperture_or_degenerate',signed_miss_px=None,endpoint_standardized=None,endpoint_sigma_miss_px=None)
 signed=dot(pred,g)/n*max(width,height)
 # pred is - (source cross aperture); determinant has opposite sign, irrelevant to variance.
 sigma_miss=math.sqrt(variance)/n*max(width,height)
 return dict(status='ok',signed_miss_px=signed,endpoint_standardized=None if variance<EPS**2 else f/math.sqrt(variance),endpoint_sigma_miss_px=sigma_miss)

def diagnose(pairs,width,height,training,perturbations=256,seed=290024):
 base=fit(pairs,width,height,training);s=base['source_normalized_homogeneous'];rows=[residual(p,s,width,height) for p in pairs];rng=random.Random(seed)
 samples=[[] for _ in pairs];failed=0
 for _ in range(perturbations):
  changed=[dict(p,aperture=[x+rng.gauss(0,p['sigma_px']) for x in p['aperture']],receiver=[x+rng.gauss(0,p['sigma_px']) for x in p['receiver']]) for p in pairs]
  try:
   fit_s=fit(changed,width,height,training)['source_normalized_homogeneous']
   # Fixed sign in normalized homogeneous coordinates prevents arbitrary projective flips.
   if dot(fit_s,s)<0:fit_s=[-x for x in fit_s]
   for i,p in enumerate(pairs):
    z=residual(p,fit_s,width,height)['signed_miss_px']
    if z is not None:samples[i].append(z)
  except ValueError:failed+=1
 for i,row in enumerate(rows):
  vals=samples[i];sd=math.sqrt(sum((x-sum(vals)/len(vals))**2 for x in vals)/(len(vals)-1)) if len(vals)>1 else None
  row.update(index=i,role='training' if i in training else 'heldout',source_fit_sigma_miss_px=sd)
  total=None if sd is None or row['endpoint_sigma_miss_px'] is None else math.hypot(sd,row['endpoint_sigma_miss_px'])
  row['combined_standardized']=None if not total else row['signed_miss_px']/total
 held=[r['combined_standardized'] for r in rows if r['role']=='heldout'];valid=bool(held) and all(x is not None for x in held)
 rms=math.sqrt(sum(x*x for x in held)/len(held)) if valid else None;mx=max(map(abs,held)) if valid else None
 return dict(fit=base,residuals=rows,heldout_combined_rms=rms,heldout_combined_max=mx,conditional_line_gate_pass=valid and not base['warnings'] and rms<=2 and mx<=4,perturbations=perturbations,failed_perturbations=failed,real_data_admission=False,interpretation='Synthetic/conditional line incidence only; no full ground-point prediction, physical source, date or K4 result')

def fixtures():
 apertures=[[x,y] for y in (200.,400.,600.) for x in (200.,400.,600.,800.)];training=[0,1,3,4,6,7,9,10];rng=random.Random(290024)
 out={}
 for name,source in [('finite',[120.,-80.]),('distant_finite',[8000.,-5000.]),('infinity',None)]:
  pairs=[]
  for i,a in enumerate(apertures):
   g=[a[0]+80+10*i,a[1]+.3*(80+10*i)] if source is None else [source[j]+(1.2+.1*(i%3))*(a[j]-source[j]) for j in (0,1)]
   pairs.append(dict(aperture=a[:],receiver=g,sigma_px=.25))
  out[name]=dict(width=1000,height=800,training=training,pairs=pairs)
 exact=out['finite'];out['noisy_finite']=dict(exact,pairs=[dict(p,aperture=[x+rng.gauss(0,.25) for x in p['aperture']],receiver=[x+rng.gauss(0,.25) for x in p['receiver']]) for p in exact['pairs']])
 negative=[]
 for i,p in enumerate(exact['pairs']):
  a,g=p['aperture'],p['receiver'];dx,dy=g[0]-a[0],g[1]-a[1];n=math.hypot(dx,dy);sign=1 if i%2 else -1
  negative.append(dict(p,receiver=g[:] if i in training else [g[0]-sign*60*dy/n,g[1]+sign*60*dx/n]))
 out['heldout_mutation']=dict(exact,pairs=negative)
 mixed=[]
 for i,p in enumerate(exact['pairs']):
  s=[120.,-80.] if i%2 else [900.,100.];a=p['aperture'];mixed.append(dict(p,receiver=[s[j]+(1.2+.1*(i%3))*(a[j]-s[j]) for j in (0,1)]))
 out['mixed_sources']=dict(exact,pairs=mixed)
 out['coincident_lines']=dict(exact,pairs=[dict(aperture=[100.+50*i,400.],receiver=[200.+50*i,400.],sigma_px=.25) for i in range(12)])
 out['collapsed']=dict(exact,pairs=[dict(p,receiver=p['aperture'][:]) for p in exact['pairs']])
 return out
