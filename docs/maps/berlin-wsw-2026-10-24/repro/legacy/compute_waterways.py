import contextlib,io,json
with contextlib.redirect_stdout(io.StringIO()):from compute_route import *
def points(g):
 if g.is_empty:return []
 if g.geom_type=='Point':return [g]
 if hasattr(g,'geoms'):return [x for y in g.geoms for x in points(y)]
 return []
rivers=[]
for f in load('ne_10m_rivers_lake_centerlines'):
 p=f['properties'];g=shape(f['geometry'])
 if p['name'] and p['featurecla']=='River':
  for pt in points(route.intersection(g)):
   v=proximity(pt.x,pt.y);v.update(name=p.get('name_en') or p['name'],scalerank=p['scalerank']);rivers.append(v)
rivers.sort(key=lambda x:x['along_km'])
lakes=[]
for f in load('ne_10m_lakes'):
 p=f['properties'];g=shape(f['geometry'])
 for x in intervals(g):
  x.update(name=p.get('name_en') or p['name'],kind=p['featurecla'],scalerank=p['scalerank'],year=p['year']);lakes.append(x)
lakes.sort(key=lambda x:x['start_km'])
out={'all_named_base_river_crossings':rivers,'major_river_crossings_scalerank_at_most_3':[x for x in rivers if x['scalerank']<=3],'lake_and_reservoir_crossings':lakes,'caveat':'Intersections with generalized Natural Earth line/polygon data, not survey-grade boundaries. Waterways not exhaustive beyond base datasets; no supplementary datasets included. Modern geometry, not 1989.'}
(P/'waterways.json').write_text(json.dumps(out,indent=2))
print('RIVERS')
for x in rivers:print(x['along_km'],x['name'],x['scalerank'])
print('LAKES')
for x in lakes:print(x['start_km'],x['end_km'],x['name'],x['kind'],x['scalerank'],x['year'])
