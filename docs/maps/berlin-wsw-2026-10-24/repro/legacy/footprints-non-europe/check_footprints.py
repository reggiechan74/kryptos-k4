import sys

import numpy as np,json,pathlib,math,hashlib,csv
from shapely.geometry import shape,Polygon,LineString,mapping
from shapely import make_valid,get_coordinates,segmentize
from scipy.optimize import minimize_scalar
P=pathlib.Path(__file__).parent
R=6371.0088;la,lo,az=np.radians([52.521146530576253,13.4133090391431029,247.5])
u=np.array([np.cos(la)*np.cos(lo),np.cos(la)*np.sin(lo),np.sin(la)])
v=np.array([-np.sin(la)*np.cos(lo),-np.sin(la)*np.sin(lo),np.cos(la)])*np.cos(az)+np.array([-np.sin(lo),np.cos(lo),0])*np.sin(az)
n=np.cross(u,v)
route=shape(json.load(open(P.parent/'route.geojson'))['features'][0]['geometry'])
def coords(t):
 p=np.cos(t)[...,None]*u+np.sin(t)[...,None]*v if isinstance(t,np.ndarray) else np.cos(t)*u+np.sin(t)*v
 return np.column_stack([np.degrees(np.arctan2(p[...,1],p[...,0])),np.degrees(np.arcsin(p[...,2]))]) if isinstance(t,np.ndarray) else [float(np.degrees(np.arctan2(p[1],p[0]))),float(np.degrees(np.arcsin(p[2])))]
def info(c):
 ar=np.asarray(c);lo,la=np.radians(ar[...,0]),np.radians(ar[...,1]);v0=np.stack([np.cos(la)*np.cos(lo),np.cos(la)*np.sin(lo),np.sin(la)],axis=-1)
 return np.arcsin(np.clip(v0@n,-1,1))*R,np.mod(np.arctan2(v0@v,v0@u),2*np.pi)*R

def lines(g):
 if g.is_empty:return []
 if g.geom_type=='LineString':return [g]
 if hasattr(g,'geoms'):return [x for a in g.geoms for x in lines(a)]
 return []
def rings(g):
 if g.geom_type=='Polygon':return [g.exterior,*g.interiors]
 if hasattr(g,'geoms'):return [r for part in g.geoms for r in rings(part)]
 return []
def precise_boundary_near(g):
 best=1e9;foot=None;segments=[]
 for r in rings(g):
  a=np.asarray(segmentize(r,0.001).coords);off,_=info(a);i=int(np.argmin(abs(off)))
  if abs(off[i])<best:best=float(abs(off[i]));foot=a[i]
  segments.append((a,off))
 for a,off in segments:
  ix=np.where(np.minimum(abs(off[:-1]),abs(off[1:]))<best+0.12)[0]
  for i in ix:
   aa,bb=a[i],a[i+1];res=minimize_scalar(lambda t: abs(float(info(aa+t*(bb-aa))[0])),bounds=(0,1),method='bounded',options={'xatol':1e-12})
   if res.fun<best:best=float(res.fun);foot=aa+res.x*(bb-aa)
 return best,foot.tolist(),coords(float(info(foot)[1])/R)
def analyze(f):
 g=shape(f['geometry']);was_valid=g.is_valid
 if not was_valid:g=make_valid(g)
 # 20m local refinement around feature extent; full-route model remains same exact spherical great circle.
 along=np.asarray(info(get_coordinates(g))[1]);amin,amax=min(along)-100,max(along)+100
 ts=np.arange(amin,amax+0.02,0.02)/R
 fine=LineString(coords(ts))
 ins=fine.intersection(g);ints=[]
 for l in lines(ins):
  a,b=info(np.array([l.coords[0],l.coords[-1]]))[1];ints.append({'entry_km':float(min(a,b)),'exit_km':float(max(a,b)),'length_km':float(abs(a-b)),'entry_lonlat':list(l.coords[0]),'exit_lonlat':list(l.coords[-1])})
 c=get_coordinates(segmentize(g.boundary,0.001));off,along=info(c);i=int(np.argmin(abs(off)))
 # In degree-linear polygon edges signed distance extrema are sampled at <=111m, not point proximity to arbitrary centroid.
 dist,foot,near=precise_boundary_near(g) if ins.is_empty else (0,c[i].tolist(),coords(along[i]/R))
 result=dict(f['properties'],intersects=not ins.is_empty,intersection_length_km=sum(x['length_km'] for x in ints),intervals=ints,minimum_boundary_distance_km=dist,closest_boundary_lonlat=foot,nearest_route_lonlat=near,geometry_was_valid=was_valid,source_precision='Not stated; no survey-accuracy claim',sampling_note='20m route vertices; degree-linear boundary edges subdivided <=0.001 degree, then candidate-edge minima optimized; distances rounded to 0.1km for communication')
 return result,{'type':'Feature','properties':dict(f['properties'],result='intersects' if not ins.is_empty else 'misses',minimum_distance_km=dist),'geometry':mapping(g)},{'type':'Feature','properties':dict(f['properties'],kind='intersection_segment'),'geometry':mapping(ins)}

features=[]
for name in ['gondwana_official.geojson','bounty_reserve.geojson','cebu_boundary.geojson','santa_ana_church.geojson','main_range_park.geojson']:
 if (P/name).exists():
  j=json.load(open(P/name))
  for f in j['features']:
   if name=='gondwana_official.geojson':
    f['properties']={'name':'Gondwana Rainforests of Australia — '+f['properties']['STATE']+' declared property','source_url':(P/(name+'.url')).read_text(),'source_objectid':f['properties']['OBJECTID'],'source_file':name,'boundary_kind':'World Heritage declared property (not buffer)'}
   elif name=='bounty_reserve.geojson':
    f['properties']={'name':f['properties']['Name'],'source_url':(P/(name+'.url')).read_text(),'source_objectid':f['properties']['OBJECTID'],'source_file':name,'boundary_kind':'Marine reserve water boundary, not island land or automatically UNESCO boundary'}
   elif name=='main_range_park.geojson':
    f['properties']={'name':f['properties']['estatename'],'source_objectid':f['properties']['objectid'],'source_url':(P/(name+'.url')).read_text(),'source_file':name,'boundary_kind':'Park boundary, distinct from UNESCO property','source_warning':'Derived from Queensland cadastral database. Not definitive absolute reserve boundary.'}
   features.append(f)
j=json.load(open(P/'san_agustin_osm.json'));ns={x['id']:[x['lon'],x['lat']] for x in j['elements'] if x['type']=='node'}
for w in j['elements']:
 if w['type']=='way':
  features.append({'type':'Feature','properties':{'name':'San Agustin Church, Manila — building footprint','boundary_kind':'OSM church building, not whole UNESCO property','source_url':'https://www.openstreetmap.org/way/'+str(w['id']),'source_file':'san_agustin_osm.json','osm_version':w['version'],'osm_timestamp':w['timestamp']},'geometry':mapping(Polygon([ns[i] for i in w['nodes']]))})
res=[];foots=[];segments=[]
for f in features:
 r,a,b=analyze(f);res.append(r);foots.append(a)
 if r['intersects']:segments.append(b)
 print(r['name'],r['intersects'],'length=',round(r['intersection_length_km'],3),'distance=',round(r['minimum_boundary_distance_km'],3));print(r['intervals'])
(P/'footprint_results.json').write_text(json.dumps(res,indent=2))
(P/'verified_footprints.geojson').write_text(json.dumps({'type':'FeatureCollection','features':foots}))
(P/'verified_intersection_segments.geojson').write_text(json.dumps({'type':'FeatureCollection','features':segments}))
