"""Exact optical ambiguity witnesses and ideal mirror scale invariance; no real data fit."""
from fractions import Fraction as F
import datetime,gzip,hashlib,json,math,time
from pathlib import Path
import projection_concurrence as pc
import site_cylinder_validation as m
ROOT=Path(__file__).resolve().parents[1]
def project(x):return (x[0]/x[2],x[1]/x[2])
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def fixtures():
 rows=[]
 for i,(x,y) in enumerate(( (x,y) for y in (-2,1,3) for x in (-3,-1,2,4))):
  P=(F(x),F(y),F(10));k=F(6+i%3,5);g=project(P);a=tuple(k*v for v in g);realizations=[]
  for depth in (-10,-20):
   L=(F(0),F(0),F(depth));t=k*L[2]/(P[2]*(1-k)+k*L[2]);assert 0<t<1
   A=tuple((1-t)*l+t*p for l,p in zip(L,P));assert 0<A[2]<P[2];assert project(A)==a and cross(sub(A,L),sub(P,L))==(0,0,0)
   realizations.append(dict(type='finite_point_source',source=[str(v) for v in L],aperture=[str(v) for v in A],source_to_receiver_aperture_fraction=str(t)))
  A=(P[0],P[1],P[2]/k);assert project(A)==a and sub(P,A)[:2]==(0,0) and P[2]>A[2]
  realizations.append(dict(type='parallel_positive_Z_rays',aperture=[str(v) for v in A],physical_source_at_infinity=True))
  assert a!=g and pc.cross([*a,F(1)],[*g,F(1)])[2]==0
  rows.append(dict(index=i,receiver=[str(v) for v in P],image_aperture=[str(v) for v in a],image_receiver=[str(v) for v in g],realizations=realizations))
 return rows

def run():
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();clock=time.monotonic();exact=fixtures();pairs=[dict(aperture=[500+500*float(F(v)) for v in x['image_aperture']],receiver=[500+500*float(F(v)) for v in x['image_receiver']],sigma_px=1) for x in exact];fit=pc.fit(pairs,1000,1000,list(range(8)));res=[pc.residual(x,fit['source_normalized_homogeneous'],1000,1000) for x in pairs];assert not fit['warnings'] and max(abs(x['signed_miss_px']) for x in res)<1e-9
 wrong=[dict(x) for x in pairs];wrong[8]=dict(wrong[8],receiver=pairs[9]['receiver']);bad=pc.residual(wrong[8],fit['source_normalized_homogeneous'],1000,1000);assert abs(bad['signed_miss_px'])>1
 with gzip.open(ROOT/'results/SITE-CYLINDER-037-SOURCE-SNAPSHOT.json.gz','rt') as f:source=json.load(f)
 nominal=m.generate(m.DEFAULTS,source['tableau_rows']);assert nominal['validCount']==97;scales=[];negative=0
 for s in (.1,1,10):
  maxerr=0;coordinates=[];wrong_radius_changes=0
  for row in nominal['samples']:
   eye=tuple(s*v for v in row['eye']);h=m.hit(eye,row['eyeToMirror'],s*m.DEFAULTS['radius'],height=3*s);assert h['status']=='hit';point=h['point'];maxerr=max(maxerr,max(abs(x-s*y) for x,y in zip(point,row['hit'])));normal=h['normal'];r=tuple(d-2*sum(x*y for x,y in zip(row['eyeToMirror'],normal))*n for d,n in zip(row['eyeToMirror'],normal));t=(m.DEFAULTS['tableauDistance']*s-point[2])/r[2];assert t>0;board=tuple(a+t*b for a,b in zip(point,r));maxerr=max(maxerr,max(abs(x-s*y) for x,y in zip(board,row['tableauPoint'])));u=(board[0]-m.DEFAULTS['shiftX']*s+4.125*s)/(.25*s);v=(3.5*s-(board[1]-(1.5+m.DEFAULTS['shiftY'])*s))/(.25*s);assert math.floor(u)+1==row['cell']['column'] and math.floor(v)+1==row['cell']['row'];assert abs(u-row['coordinates'][0])<1e-10 and abs(v-row['coordinates'][1])<1e-10;coordinates.append([u,v])
   w=m.hit(eye,row['eyeToMirror'],m.DEFAULTS['radius'],height=3*s)
   if w['status']!='hit' or max(abs(x-y) for x,y in zip(w.get('point',(0,0,0)),point))>1e-6:wrong_radius_changes+=1
  if s!=1:assert wrong_radius_changes>0
  negative+=wrong_radius_changes;scales.append(dict(scale=s,checked_rays=97,maximum_absolute_point_error=maxerr,dimensionless_cells_equal=True,unscaled_radius_negative_changes=wrong_radius_changes))
 return dict(id='PHYSICAL-IDENTIFIABILITY-040',started_at_utc=start,finished_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-clock,exact_rational_image_pairs=exact,physical_realizations_per_image_pair=3,fit=fit,maximum_heldout_incidence_miss_px=max(abs(x['signed_miss_px']) for x in res[8:]),local_wrong_match_miss_px=bad['signed_miss_px'],scale_checks=scales,scale_rays=291,wrong_radius_negative_changes=negative,source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ('research/PHYSICAL-IDENTIFIABILITY-040-SPEC.md','experiments/physical_identifiability_040.py','results/SITE-CYLINDER-037-SOURCE-SNAPSHOT.json.gz')},certified_real_pairs=0,physical_monument_fit=False,K4_trials=0,Site_changed=False,puzzle_solved=False)
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();r=run();Path(a.output).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ('started_at_utc','finished_at_utc','maximum_heldout_incidence_miss_px','local_wrong_match_miss_px','scale_rays','wrong_radius_negative_changes')}))
