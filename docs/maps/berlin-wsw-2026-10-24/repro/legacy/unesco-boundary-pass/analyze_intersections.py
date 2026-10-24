import contextlib,io,json,numpy as np,math
with contextlib.redirect_stdout(io.StringIO()):
 from sys import path
 path.insert(0,str(__import__('pathlib').Path(__file__).parent.parent))
 from compute_route import *
ROOT=P;P=ROOT/'unesco-boundary-pass'
from shapely.geometry import Point
from shapely.ops import transform
results=[];seg_features=[]
for layer in [1,2]:
 data=json.loads((P/f'layer{layer}_route_hit_polygons.json').read_text())
 for f in data['features']:
  prop=f['properties'];g=shape(f['geometry']);valid=g.is_valid
  if not valid:g=make_valid(g)
  minx,miny,maxx,maxy=g.bounds
  # Densify only the route section near this feature's bounding box to 10m spacing.
  ix=np.flatnonzero((xs>=minx-.05)&(xs<=maxx+.05)&(ys>=miny-.05)&(ys<=maxy+.05))
  if len(ix)==0:raise RuntimeError('No route vertex in feature bounding box')
  starts=[];split=np.where(np.diff(ix)>1)[0]
  groups=np.split(ix,split+1)
  local=[]
  for group in groups:
   t0=max(0,ts[max(0,group[0]-2)]);t1=min(2*np.pi,ts[min(len(ts)-1,group[-1]+2)])
   dense=np.linspace(t0,t1,max(2,int(math.ceil((t1-t0)*R/.01))+1))
   xx,yy=coord(dense);local.append(LineString(np.column_stack([xx,yy])))
  routefine=MultiLineString(local);inside=routefine.intersection(g);ints=[]
  for line in flatten(inside):
   def exact_along(xy):
    lon,lat=np.radians(xy);q=np.array([np.cos(lat)*np.cos(lon),np.cos(lat)*np.sin(lon),np.sin(lat)])
    return float(np.arctan2(np.dot(q,v),np.dot(q,u))%(2*np.pi))*R
   a=exact_along(line.coords[0]);b=exact_along(line.coords[-1]);a,b=sorted([a,b])
   if b-a<.000001:continue
   ent=list(map(float,coord(a/R)));ex=list(map(float,coord(b/R)))
   mid=line.interpolate(.5,normalized=True);lat0=mid.y
   gmet=transform(lambda x,y,z=None:(np.asarray(x)*111195.0802335329*np.cos(np.radians(lat0)),np.asarray(y)*111195.0802335329),g)
   pm=Point(mid.x*111195.0802335329*np.cos(np.radians(lat0)),mid.y*111195.0802335329)
   ints.append({'entry_km':a,'exit_km':b,'length_km':round(b-a,6),'entry_lonlat':ent,'exit_lonlat':ex,'midpoint_boundary_clearance_m_approx':gmet.boundary.distance(pm)})
   sp={**prop,'source_layer':layer,'boundary_kind':'UNESCO core property' if layer==1 else 'UNESCO buffer zone (not property)','source_url':f'https://services6.arcgis.com/eMd5K6XXEvJETxfQ/arcgis/rest/services/prd_whc_sites_dossiers_elements_v2_view/FeatureServer/{layer}/{prop["OBJECTID"]}','entry_km':a,'exit_km':b,'length_km':round(b-a,6)}
   seg_features.append({'type':'Feature','properties':sp,'geometry':mapping(line)})
  ints.sort(key=lambda x:x['entry_km'])
  r={'property_name':prop['property_name_en'],'element_name':prop['element_name_en'],'property_id':prop['property_id'],'object_id':prop['OBJECTID'],'source_layer':layer,'boundary_kind':'UNESCO core property' if layer==1 else 'UNESCO buffer zone (not property)','source_url':f'https://services6.arcgis.com/eMd5K6XXEvJETxfQ/arcgis/rest/services/prd_whc_sites_dossiers_elements_v2_view/FeatureServer/{layer}/{prop["OBJECTID"]}','geometry_was_valid':valid,'intervals':ints,'total_length_km':sum(x['length_km'] for x in ints),'source_precision_publish_flag':prop['element_precision_publish'],'route_vertex_spacing_km':.01,'caveat':'Conditional on spherical Earth and exact initial bearing247.5. Official published GIS polygon, not survey-level proof of physical structure. Buffer != property.'}
  results.append(r)
  print(r['boundary_kind'],r['property_name'],r['element_name'],'intervals',len(ints),'total_km',r['total_length_km'])
  for x in ints:print(x)
(P/'official_unesco_intersection_results.json').write_text(json.dumps(results,indent=2))
(P/'official_unesco_intersection_segments.geojson').write_text(json.dumps({'type':'FeatureCollection','features':seg_features}))
# Count unique published names, rows, and dates without fetching unrelated geometries.
coverage={}
for layer in [1,2]:
 rows=json.loads((P/f'layer{layer}_coverage_counts.json').read_text())['features'];meta=json.loads((P/f'metadata_{layer}.json').read_text())
 coverage[str(layer)]={'property_name_groups':len(rows),'published_polygon_features':sum(x['attributes']['polygon_count'] for x in rows),'editingInfo':meta.get('editingInfo'),'precision_flag_field':next(x for x in meta['fields'] if x['name']=='element_precision_publish'),'exceededTransferLimit':json.loads((P/f'layer{layer}_coverage_counts.json').read_text()).get('exceededTransferLimit',False)}
(P/'coverage_summary.json').write_text(json.dumps(coverage,indent=2));print('COVERAGE',json.dumps(coverage,indent=2))
