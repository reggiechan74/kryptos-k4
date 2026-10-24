"""Spherical cross-track coordinate calculation independent of parent route code."""
import sys;
import math,json,pathlib,numpy as np
from shapely.geometry import shape,LineString,Point,mapping
from shapely.ops import transform,unary_union
from shapely import make_valid,segmentize
P=pathlib.Path(__file__).parent
R=6371.0088; C=2*math.pi*R
lat=math.radians(52.521146530576253);lon=math.radians(13.4133090391431029);bearing=math.radians(247.5)
start=np.array([math.cos(lat)*math.cos(lon),math.cos(lat)*math.sin(lon),math.sin(lat)])
north=np.array([-math.sin(lat)*math.cos(lon),-math.sin(lat)*math.sin(lon),math.cos(lat)])
east=np.array([-math.sin(lon),math.cos(lon),0.])
tan=north*math.cos(bearing)+east*math.sin(bearing); normal=np.cross(start,tan)
def project(x,y,z=None):
 x,y=np.radians(x),np.radians(y)
 p=np.array([np.cos(y)*np.cos(x),np.cos(y)*np.sin(x),np.sin(y)])
 return np.arctan2(np.einsum('i,i...->...',tan,p),np.einsum('i,i...->...',start,p))%(2*np.pi)*R,np.arcsin(np.clip(np.einsum('i,i...->...',normal,p),-1,1))*R
def unproject(x):
 p=start*math.cos(x/R)+tan*math.sin(x/R)
 return [math.degrees(math.atan2(p[1],p[0])),math.degrees(math.atan2(p[2],math.hypot(p[0],p[1])))]
def flatten(g):
 if g.is_empty:return []
 if g.geom_type=='LineString':return [g]
 return [v for x in getattr(g,'geoms',[]) for v in flatten(x)]
def polygonal(g):
 if g.geom_type in ['Polygon','MultiPolygon']:return g
 return unary_union([polygonal(x) for x in getattr(g,'geoms',[]) if x.geom_type in ['Polygon','MultiPolygon','GeometryCollection']])
def analyze(row,label):
 g=shape(row['geojson']);g=polygonal(make_valid(g))
 # 0.00005 degrees maximum segment (~5.56 m), then orthogonal great-circle coordinates.
 q=transform(project,segmentize(g,0.00005))
 if q.bounds[2]-q.bounds[0]>C/2:raise ValueError('crosses origin: handle unwrap')
 q=polygonal(make_valid(q))
 cut=q.intersection(LineString([(q.bounds[0]-1,0),(q.bounds[2]+1,0)]))
 intervals=[]
 for line in flatten(cut):
  a,b=sorted([line.coords[0][0],line.coords[-1][0]])
  clear=max(q.boundary.distance(Point(a+(b-a)*f,0)) for f in np.linspace(.01,.99,101))
  intervals.append({'entry_km':a,'exit_km':b,'length_m':(b-a)*1000,'entry_lonlat':unproject(a),'exit_lonlat':unproject(b),'sampled_max_interior_clearance_m':clear*1000})
 sep=0 if intervals else q.distance(LineString([(q.bounds[0]-1,0),(q.bounds[2]+1,0)]))*1000
 result={'label':label,'osm_type':row['osm_type'],'osm_id':row['osm_id'],'name':row['display_name'],'geometry_type':g.geom_type,'result':'mapped_polygon_intersection' if intervals else 'miss','minimum_gap_m':sep,'intervals':intervals,'source_url':f"https://www.openstreetmap.org/{row['osm_type']}/{row['osm_id']}",'retrieved_utc_date':'2026-10-24','accuracy_note':'OSM positional accuracy unquantified; numerical precision is not survey accuracy. Boundary segments sampled at <=5.56m before spherical projection.'}
 return result,{'type':'Feature','properties':result,'geometry':mapping(g)}
if __name__=='__main__':
 out=[];features=[]
 for f in sorted(P.glob('*nominatim.json')):
  if f.stem.startswith('versailles_park_'):continue # wrong similarly named park in Plaisir; rejected
  for row in json.loads(f.read_text()):
   if row['geojson']['type'] not in ['Polygon','MultiPolygon']:continue
   a,g=analyze(row,f.stem.replace('_nominatim',''));out.append(a);features.append(g)
   print(a['label'],a['osm_type'],a['osm_id'],a['result'],'gap_m',round(a['minimum_gap_m'],2),[(round(x['entry_km'],3),round(x['exit_km'],3),round(x['length_m'],1),round(x['sampled_max_interior_clearance_m'],1))for x in a['intervals']])
 (P/'footprint_results.json').write_text(json.dumps(out,indent=2));(P/'verified_footprints.geojson').write_text(json.dumps({'type':'FeatureCollection','features':features}))
