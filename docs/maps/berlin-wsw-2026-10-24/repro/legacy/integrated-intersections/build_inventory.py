import sys,contextlib,io,json,math,pathlib,numpy as np
sys.path.insert(0,str(pathlib.Path(__file__).parent.parent))
with contextlib.redirect_stdout(io.StringIO()):from compute_route import *
from scipy.optimize import minimize_scalar
ROOT=P;OUT=ROOT/'integrated-intersections'
MODEL='Spherical great circle; R=6371.0088 km; origin52.521146530576253,13.413309039143103; initial true bearing247.5 deg. Not a WGS84 geodesic or rhumb line.'
CAUTION='Mapped/model-conditional relation, not survey-grade physical touch. Real boundary accuracy and exact bearing matter.'
COVERAGE='UNESCO core:2265 polygon features/519 property-name groups; buffer:1146/347. Unpublished polygons untested. Current data checked2026-10-24; not historical1989.'
rows=[];features=[]
def near_boundary(g):
 parts=[]
 def visit(q):
  if q.geom_type=='Polygon':
   parts.append(np.asarray(q.exterior.coords));parts.extend(np.asarray(z.coords) for z in q.interiors)
  elif hasattr(q,'geoms'):
   for z in q.geoms:visit(z)
 visit(g)
 aa=np.vstack([a[:-1] for a in parts]);bb=np.vstack([a[1:] for a in parts])
 def score(x):
  lo,la=np.radians(x).T;q=np.column_stack([np.cos(la)*np.cos(lo),np.cos(la)*np.sin(lo),np.sin(la)])
  return np.abs(q@n)
 scores=np.minimum.reduce([score(aa),score(bb),score((aa+bb)/2)])
 best=(1,None)
 for k in np.argsort(scores)[:min(40,len(scores))]:
  a,b=aa[k],bb[k]
  opt=minimize_scalar(lambda t:float(score(np.asarray([a+t*(b-a)]))[0]),bounds=(0,1),method='bounded',options={'xatol':1e-13})
  for t in [0,opt.x,1]:
   q=a+t*(b-a);s=float(score(np.asarray([q]))[0])
   if s<best[0]:best=(s,q)
 return proximity(*best[1])
def row(category,name,bkind,geomtype,relation,ints,gap,source,evidence,scope,caveat,geom=None,near=None,source_id='',extra=None):
 ints=sorted(ints,key=lambda a:a['entry_km'])
 if ints:along=ints[0]['entry_km'];end=ints[-1]['exit_km'];length=sum(x.get('length_km',x.get('length_m',0)/1000) for x in ints)
 else:along=(near or {}).get('along_km');end=None;length=None
 rr={'category':category,'name':name,'boundary_kind':bkind,'source_geometry_type':geomtype,'relationship':relation,'along_km':along,'last_exit_km':end,'intersection_length_km':length,'minimum_gap_km':gap,'interval_count':len(ints),'intervals':ints,'source_url':source,'source_feature_id':source_id,'evidence_type':evidence,'source_scope':scope,'accuracy_and_semantic_caveat':caveat,'model':MODEL,'retrieved_date':'2026-10-24','UNESCO_polygon_coverage':COVERAGE,'extra_source_metadata':extra or {}}
 rows.append(rr)
 if geom is not None:features.append({'type':'Feature','properties':rr.copy(),'geometry':geom})

r=json.loads((ROOT/'route_results.json').read_text())
countrygeoms=json.loads((ROOT/'country_polygon_intersections.geojson').read_text())['features']
for i,x in enumerate(r['countries']):
 ints=[{'entry_km':x['start_km'],'exit_km':x['end_km'],'length_km':x['length_km'],'entry_lonlat':[x['entry_lon'],x['entry_lat']],'exit_lonlat':[x['exit_lon'],x['exit_lat']]}]
 row('country',x['name'],'Country polygon (includes inland waters)','Polygon/MultiPolygon','intersects mapped country polygon',ints,0,'https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-0-countries/','Generalized Natural Earth 1:10m geometry','All258 country polygons tested',CAUTION+' Current de facto boundaries; not dry-land-only or1989.',source_id=x['iso']+':interval'+str(i+1))
w=json.loads((ROOT/'waterways.json').read_text())
for i,x in enumerate(w['all_named_base_river_crossings']):
 ints=[{'entry_km':x['along_km'],'exit_km':x['along_km'],'entry_lonlat':[x['point_lon'],x['point_lat']],'exit_lonlat':[x['point_lon'],x['point_lat']]}]
 row('river centerline',x['name'],'Named river centerline (not channel banks)','LineString/MultiLineString','crosses mapped river centerline',ints,0,'https://www.naturalearthdata.com/downloads/10m-physical-vectors/10m-rivers-lake-centerlines/','Generalized Natural Earth base river geometry','All named River-class features in1455-feature base dataset tested; no supplementary layers',CAUTION+' Does not establish channel width or riverbank coordinates.',source_id=x['name']+':crossing'+str(i+1),extra={'scalerank':x['scalerank']})
for i,x in enumerate(w['lake_and_reservoir_crossings']):
 ints=[{'entry_km':x['start_km'],'exit_km':x['end_km'],'length_km':x['length_km'],'entry_lonlat':[x['entry_lon'],x['entry_lat']],'exit_lonlat':[x['exit_lon'],x['exit_lat']]}]
 row('lake or reservoir',x['name'] or 'Unnamed lake polygon',x['kind']+' water polygon','Polygon/MultiPolygon','intersects mapped water polygon',ints,0,'https://www.naturalearthdata.com/downloads/10m-physical-vectors/10m-lakes/','Generalized Natural Earth 1:10m geometry','All1355 base lake/reservoir features tested',CAUTION+' Water extent is generalized and not a current water-level survey.',source_id='lake_interval_'+str(i+1),extra={'dataset_year_field':x['year'],'scalerank':x['scalerank']})

# Definitive regional geometries only; do not double count intermediate datasets.
for f in json.loads((ROOT/'europe-footprints/EUROPE_FINAL_FOOTPRINTS.geojson').read_text())['features']:
 x=f['properties'];geom=f['geometry'];g=shape(geom);hit=x['result']!='miss';ints=x['intervals'];src=x['source_url'];kind=x.get('geometry_scope','Mapped footprint');isbuffer='buffer' in kind.lower() or 'buffer' in x['label'].lower() or 'puffer' in x['label'].lower()
 category='heritage buffer' if isbuffer else ('building footprint' if 'building' in kind.lower() else ('administrative area' if 'administrative' in kind.lower() else 'site/property footprint'))
 near=near_boundary(g) if not hit else None
 evidence='Community-mapped OpenStreetMap boundary' if 'openstreetmap' in src else 'Official published heritage GIS boundary'
 name=x.get('label') if len(x.get('name',''))>100 else x.get('name',x['label'])
 if x.get('label') in ['moscow_city','moscow_kremlin','red_square','paris_city']:
  name={'moscow_city':'Moscow administrative area','moscow_kremlin':'Moscow Kremlin grounds','red_square':'Red Square','paris_city':'Paris municipal boundary'}[x['label']]
 relation=('intersects buffer zone only (not property)' if isbuffer else 'intersects mapped footprint') if hit else 'misses tested footprint'
 row(category,name,kind,geom['type'],relation,ints,x['minimum_gap_m']/1000,src,evidence,'Targeted European candidate footprint checks; not exhaustive buildings/sites',x.get('accuracy_note','')+' '+x.get('conditionality',CAUTION),geom=geom,near=near,source_id=str(x.get('geometry_id') or str(x.get('osm_type',''))+'/'+str(x.get('osm_id',''))),extra={'source_label':x['label'],'osm_version':x.get('osm_version'),'osm_timestamp':x.get('osm_timestamp'),'source_properties':x.get('source_properties'),'gap_independent_check_delta_m':None if hit else round(near['off_line_km']*1000-x['minimum_gap_m'],4)})
non=json.loads((ROOT/'footprints-non-europe/footprint_results.json').read_text());nongeo=json.loads((ROOT/'footprints-non-europe/verified_footprints.geojson').read_text())['features']
for x,f in zip(non,nongeo):
 assert x['name']==f['properties']['name']
 hit=x['intersects'];geom=f['geometry'];kind=x['boundary_kind'];ints=[]
 for a in x['intervals']:
  # source uses entry/exit field names retained below after inspection if needed
  b=dict(a)
  if 'start_km'in b:b['entry_km']=b.pop('start_km')
  if 'end_km'in b:b['exit_km']=b.pop('end_km')
  ints.append(b)
 near=None
 if not hit:
  q=x.get('closest_boundary_lonlat');near=proximity(*q) if q else near_boundary(shape(geom))
 src=x['source_url'];evidence='Community-mapped OpenStreetMap boundary' if 'openstreetmap' in src else 'Official published agency GIS boundary'
 category='marine reserve' if 'Marine reserve' in kind else ('administrative area' if 'Administrative' in kind else ('building footprint' if 'building' in kind.lower() else 'site/property footprint'))
 row(category,x['name'],kind,geom['type'],'intersects mapped footprint' if hit else 'misses tested footprint',ints,0 if hit else x['minimum_boundary_distance_km'],src,evidence,'Nine targeted non-European footprint checks; not exhaustive sites',CAUTION+' '+x['source_precision']+' '+kind,geom=geom,near=near,source_id=str(x.get('source_objectid',x.get('osm_id',''))),extra={'geometry_was_valid':x['geometry_was_valid'],'sampling_note':x['sampling_note']})

known={x['source_url'] for x in rows}
unesco=json.loads((ROOT/'unesco-boundary-pass/official_unesco_intersection_results.json').read_text())
for x in unesco:
 if x['source_url'] in known:continue
 layer=x['source_layer'];raw=json.loads((ROOT/f'unesco-boundary-pass/layer{layer}_route_hit_polygons.json').read_text())['features'];f=next(z for z in raw if z['properties']['OBJECTID']==x['object_id'])
 row('UNESCO core property' if layer==1 else 'heritage buffer',x['element_name'],x['boundary_kind'],f['geometry']['type'],'intersects UNESCO core-property polygon' if layer==1 else 'intersects buffer zone only (not property)',x['intervals'],0,x['source_url'],'Official published UNESCO GIS boundary','Whole defined great circle queried directly against ALL published core/buffer polygons, no nearby-point prefilter',x['caveat']+' Source precision flag has no documented domain; no accuracy inferred from it.',geom=f['geometry'],source_id=str(x['object_id']),extra={'property_name':x['property_name'],'property_id':x['property_id'],'precision_publish_flag':x['source_precision_publish_flag']})
rows.sort(key=lambda x:(x['along_km'] is None,x['along_km'] or 0,x['category'],x['name']))
for i,x in enumerate(rows):x['row_id']=i+1
summary={'rows':len(rows),'category_counts':{k:sum(x['category']==k for x in rows) for k in sorted(set(x['category'] for x in rows))},'relation_counts':{k:sum(x['relationship']==k for x in rows) for k in sorted(set(x['relationship'] for x in rows))},'model':MODEL,'coverage':COVERAGE,'scope':'Complete within specified Natural Earth base and published UNESCO layers plus targeted regional checks; not every physical object on Earth. Rows may overlap; do not sum across categories. Point-proximity inventory is separate and unchanged.','major_model_warning':'The spherical route crosses mapped Kremlin grounds; a same-initial-bearing WGS84 near-return misses by approximately1.344 km. Narrow building clips are not robust physical-touch claims.'}
(OUT/'inventory.json').write_text(json.dumps({'summary':summary,'rows':rows},indent=2))
(OUT/'verified_footprints_overlay.geojson').write_text(json.dumps({'type':'FeatureCollection','features':features}))
print(json.dumps(summary,indent=2));print('footprints',len(features))
