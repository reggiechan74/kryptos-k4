import contextlib,io,json,hashlib,math,numpy as np
with contextlib.redirect_stdout(io.StringIO()):from compute_route import *
# Independent forward spherical-navigation formula, 17 points around the world.
errors=[]
for d in np.linspace(0,C,17):
 a=d/R
 lat=math.asin(math.sin(la)*math.cos(a)+math.cos(la)*math.sin(a)*math.cos(az))
 lon=lo+math.atan2(math.sin(az)*math.sin(a)*math.cos(la),math.cos(a)-math.sin(la)*math.sin(lat))
 expected=np.array([(math.degrees(lon)+180)%360-180,math.degrees(lat)]);actual=np.array(coord(a))
 diff=actual-expected;diff[0]=(diff[0]+180)%360-180;errors.append(float(np.max(np.abs(diff))))
# A numeric tangent at origin independently verifies the initial bearing.
p0=np.array(coord(0));p1=np.array(coord(1e-7));dl=np.radians(p1[0]-p0[0]);a0=np.radians(p0[1]);a1=np.radians(p1[1])
bearing=math.degrees(math.atan2(math.sin(dl)*math.cos(a1),math.cos(a0)*math.sin(a1)-math.sin(a0)*math.cos(a1)*math.cos(dl)))%360
max_t=math.atan2(v[2],u[2])%(2*math.pi);min_t=(max_t+math.pi)%(2*math.pi)
meta={'max_forward_formula_coordinate_error_degrees':max(errors),'numeric_initial_bearing_degrees':bearing,'closed_endpoint_coordinate_error_degrees':float(np.max(np.abs(np.array(coord(0))-np.array(coord(2*np.pi))))),'route_vertices':sum(len(x) for x in parts),'country_land_segment_count':len(countries),'unique_country_count':len(set(x['name'] for x in countries)),'southern_vertex':{'distance_km':min_t*R,'lonlat':list(map(float,coord(min_t)))},'northern_vertex':{'distance_km':max_t*R,'lonlat':list(map(float,coord(max_t)))},'antipode':{'distance_km':C/2,'lonlat':list(map(float,coord(np.pi)))}}
assert max(errors)<1e-9
assert abs(bearing-AZ)<1e-5
assert meta['closed_endpoint_coordinate_error_degrees']<1e-9
(P/'validation.json').write_text(json.dumps(meta,indent=2));print(json.dumps(meta,indent=2))
urls={f.name:'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/'+f.name for f in P.glob('ne_*.geojson')}
urls['unesco_world_heritage.json']='https://data.unesco.org/api/explore/v2.1/catalog/datasets/whc001/exports/json'
manifest={'retrieved_date_utc':'2026-10-24','origin_source':'https://denkmaldatenbank.berlin.de/daobj_karte.php?obj_dok_nr=09020854','country_documentation':'https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-0-countries/','cities_documentation':'https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-populated-places/','UNESCO_documentation':'https://data.unesco.org/explore/dataset/whc001/','sources':[{'file':fn,'url':url,'sha256':hashlib.sha256((P/fn).read_bytes()).hexdigest(),'bytes':(P/fn).stat().st_size} for fn,url in urls.items()]}
(P/'source_manifest.json').write_text(json.dumps(manifest,indent=2))
