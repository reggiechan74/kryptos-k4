import contextlib,io,json,math
with contextlib.redirect_stdout(io.StringIO()):from compute_route import *
features=[]
for f in load('ne_10m_admin_0_countries'):
 g=shape(f['geometry']);g=g if g.is_valid else make_valid(g)
 for line in flatten(route.intersection(g)):
  a=proximity(*line.coords[0])['along_km'];b=proximity(*line.coords[-1])['along_km']
  if abs(a-b)>C/2:
   if a==0:a=C
   if b==0:b=C
  coords=list(line.coords)
  if b<a:a,b=b,a;coords.reverse()
  if b-a<=.0001:continue
  features.append({'type':'Feature','properties':{'country':f['properties']['ADMIN'],'iso':f['properties']['ADM0_A3'],'start_km':round(a,3),'end_km':round(b,3),'entry_lon':coords[0][0],'entry_lat':coords[0][1],'exit_lon':coords[-1][0],'exit_lat':coords[-1][1],'relation':'modeled route intersects generalized country polygon; includes inland waters','boundary_source':'https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-0-countries/','bearing_true_degrees':AZ,'model':'sphere','radius_km':R},'geometry':{'type':'LineString','coordinates':coords}})
features.sort(key=lambda f:f['properties']['start_km'])
for i,f in enumerate(features):f['properties']['interval_id']=i+1
assert len(features)==45
(P/'country_polygon_intersections.geojson').write_text(json.dumps({'type':'FeatureCollection','features':features}))
print(len(features),'country polygon intervals')
