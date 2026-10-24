"""Reproducible spherical great-circle inventory. Source polygons are generalized 1:10m.
Cities: all records in Natural Earth 10m populated_places with POP_MAX >= 100000,
within 50 km point-to-great-circle distance. UNESCO reference points: same 50 km.
Point proximity is never interpreted as physical intersection.
"""
import sys

import math,json,csv,pathlib,numpy as np
from shapely.geometry import shape,LineString,MultiLineString,mapping
from shapely import make_valid
P=pathlib.Path(__file__).parent
R=6371.0088; C=2*math.pi*R
LAT=52.521146530576253; LON=13.4133090391431029; AZ=247.5
la,lo,az=np.radians([LAT,LON,AZ])
u=np.array([np.cos(la)*np.cos(lo),np.cos(la)*np.sin(lo),np.sin(la)])
east=np.array([-np.sin(lo),np.cos(lo),0]); north=np.array([-np.sin(la)*np.cos(lo),-np.sin(la)*np.sin(lo),np.cos(la)])
v=north*np.cos(az)+east*np.sin(az)
n=np.cross(u,v); n/=np.linalg.norm(n)
def coord(t):
 p=np.cos(t)[...,None]*u+np.sin(t)[...,None]*v if isinstance(t,np.ndarray) else np.cos(t)*u+np.sin(t)*v
 return np.degrees(np.arctan2(p[...,1],p[...,0])),np.degrees(np.arctan2(p[...,2],np.hypot(p[...,0],p[...,1])))
def proximity(lon,lat):
 la,lo=np.radians([lat,lon]); p=np.array([np.cos(la)*np.cos(lo),np.cos(la)*np.sin(lo),np.sin(la)])
 off=float(np.arcsin(np.clip(np.dot(p,n),-1,1))*R)
 ang=float(np.arctan2(np.dot(p,v),np.dot(p,u))%(2*np.pi))
 along=ang*R
 if abs(along-C)<1e-7: along=0
 ll=coord(ang)
 return {'along_km':round(along,3),'off_line_km':round(abs(off),3),'point_lon':lon,'point_lat':lat,'nearest_route_lon':float(ll[0]),'nearest_route_lat':float(ll[1])}
def load(name): return json.loads((P/(name+'.geojson')).read_text())['features']
ts=np.linspace(0,2*np.pi,80001); xs,ys=coord(ts)
coords=np.column_stack([xs,ys]); breaks=list(np.where(np.abs(np.diff(xs))>180)[0])
parts=[]; start=0
# Insert exact antimeridian point, preserving both sides.
for k in breaks:
 t0,t1=ts[k],ts[k+1]
 for _ in range(50):
  mid=(t0+t1)/2; xm,_=coord(mid)
  if (xm>0)==(xs[k]>0):t0=mid
  else:t1=mid
 _,ym=coord((t0+t1)/2)
 side=180 if xs[k]>0 else -180
 parts.append(np.vstack([coords[start:k+1],[side,ym]]).tolist());start=k+1
 coords[start]=[-side,ym]
parts.append(coords[start:].tolist())
route=MultiLineString(parts)
geo={'type':'FeatureCollection','features':[{'type':'Feature','properties':{'name':'Berlin clock WSW initial-bearing great circle','initial_true_bearing':AZ,'origin_lat':LAT,'origin_lon':LON,'model':'sphere','radius_km':R,'length_km':C,'point_spacing_km':C/80000},'geometry':mapping(route)}]}
(P/'route.geojson').write_text(json.dumps(geo))

def flatten(g):
 if g.is_empty:return []
 if g.geom_type=='LineString': return [g]
 if hasattr(g,'geoms'):return [x for s in g.geoms for x in flatten(s)]
 return []
def intervals(g):
 if not g.is_valid:g=make_valid(g)
 ins=[]
 for line in flatten(route.intersection(g)):
  a=proximity(*line.coords[0])['along_km'];b=proximity(*line.coords[-1])['along_km']
  if abs(a-b)>C/2:
   # Last coordinate is Berlin on the final route portion.
   if a==0:a=C
   if b==0:b=C
  a,b=sorted([a,b])
  if b-a>0.0001:
   c1=coord(a/R);c2=coord(b/R)
   ins.append({'start_km':round(a,3),'end_km':round(b,3),'length_km':round(b-a,3),'entry_lon':float(c1[0]),'entry_lat':float(c1[1]),'exit_lon':float(c2[0]),'exit_lat':float(c2[1])})
 return sorted(ins,key=lambda x:x['start_km'])

countries=[]
for f in load('ne_10m_admin_0_countries'):
 for x in intervals(shape(f['geometry'])):
  x.update(name=f['properties']['ADMIN'],iso=f['properties']['ADM0_A3']);countries.append(x)
countries.sort(key=lambda x:x['start_km'])
near_cities=[]; all_near_cities=[]
for f in load('ne_10m_populated_places'):
 pr=proximity(*f['geometry']['coordinates']);p=f['properties']
 if pr['off_line_km']<=50:
  pr.update(name=p['NAME'],country=p['ADM0NAME'],pop_max=p['POP_MAX'],wikidataid=p['WIKIDATAID']);all_near_cities.append(pr)
  if p['POP_MAX']>=100000:near_cities.append(pr)
near_cities.sort(key=lambda x:x['along_km']);all_near_cities.sort(key=lambda x:x['along_km'])
regions=[];marine=[]
for filename,dest in [('ne_10m_geography_regions_polys',regions),('ne_10m_geography_marine_polys',marine)]:
 for f in load(filename):
  p={k.lower():v for k,v in f['properties'].items()}
  for x in intervals(shape(f['geometry'])):
   x.update(name=p['name'],kind=p['featurecla'],scalerank=p['scalerank']);dest.append(x)
 dest.sort(key=lambda x:x['start_km'])
points=[]
for f in load('ne_10m_geography_regions_points'):
 pr=proximity(*f['geometry']['coordinates']);p=f['properties']
 if pr['off_line_km']<=50:
  pr.update(name=p['name'],kind=p['featurecla']);points.append(pr)
points.sort(key=lambda x:x['along_km'])

result={'parameters':{'origin_lat':LAT,'origin_lon':LON,'initial_true_bearing':AZ,'sphere_radius_km':R,'total_length_km':C,'latitude_extreme_degrees':math.degrees(math.acos(abs(n[2]))),'nearby_threshold_km':50,'city_dataset_threshold_POP_MAX':100000},'countries':countries,'cities_within_50km_POP_MAX_100000':near_cities,'all_NE_cities_within_50km':all_near_cities,'NE_generalized_region_intervals':regions,'NE_generalized_marine_region_intervals':marine,'NE_feature_points_within_50km':points,'misses':{k:proximity(lo,la) for k,lo,la in [('Washington, DC',-77.0369,38.9072),('Chesapeake Bay representative point',-76.1,37.8),('Kryptos representative point',-77.146,38.952),('Stonehenge',-1.8262,51.1789)]}}
(P/'route_results.json').write_text(json.dumps(result,indent=2))
for name,rows in [('country_crossings',countries),('cities_within_50km',near_cities),('all_cities_within_50km',all_near_cities),('generalized_land_regions',regions),('generalized_marine_regions',marine),('physical_feature_points_within_50km',points)]:
 if rows:
  with (P/(name+'.csv')).open('w') as f:
   wr=csv.DictWriter(f,fieldnames=rows[0].keys());wr.writeheader();wr.writerows(rows)
print('COUNTRIES')
for x in countries:print(f"{x['start_km']:9.1f}–{x['end_km']:9.1f} {x['name']:30s} {x['entry_lat']:8.3f},{x['entry_lon']:8.3f} to {x['exit_lat']:8.3f},{x['exit_lon']:8.3f}")
print('CITIES >=100K /50KM')
for x in near_cities:print(f"{x['along_km']:9.1f} {x['off_line_km']:5.1f} {x['name']:30s} {x['country']}")
print('REGIONS')
for x in regions:print(f"{x['start_km']:9.1f}–{x['end_km']:9.1f} {str(x['name']):30s} {x['kind']}")
print('MARINE')
for x in marine:print(f"{x['start_km']:9.1f}–{x['end_km']:9.1f} {str(x['name']):30s} {x['kind']}")
print('FEATURES',points)
print('MISSES',result['misses'])
