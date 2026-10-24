from verify_footprints import *
import csv,hashlib,xml.etree.ElementTree as E
features=[]
for fn in ['verified_footprints.geojson','verified_official_footprints.geojson','verified_unesco_footprints.geojson']:
 for f in json.loads((P/fn).read_text())['features']:
  a=f['properties'];oid=a.get('osm_id');label=a['label']
  if oid in [71525,1641193,618277004]:continue # duplicate Paris levels and wrong-named Glienicke park
  if label.startswith('RIVES DE LA SEINE'):continue # use matching UNESCO geometry once; City source retained raw
  f['properties']['source_result_file']=fn
  if a.get('osm_type'):
   if label=='moscow_kremlin':scope='OSM Kremlin walled grounds, not entire UNESCO property'
   elif label=='red_square':scope='OSM pedestrian-square area, not entire UNESCO property'
   elif label=='novodevichy':scope='OSM monastery grounds, not official UNESCO boundary'
   elif label=='moscow_city':scope='OSM administrative federal-city boundary (admin_level4)' if oid==102269 else 'OSM city-place polygon; not administrative boundary or every building'
   elif label=='paris_city':scope='OSM municipality boundary (admin_level8)'
   elif label=='museum_buildings':scope='OSM individual building footprint, not whole Museum Island UNESCO site'
   elif label in ['versailles_palace','chartres_cathedral']:scope='OSM individual building footprint'
   elif label=='versailles_gardens':scope='OSM park grounds, not full UNESCO property'
   else:scope='OSM individual park/island area, not complete serial UNESCO property'
  else:
   if a.get('source_layer')==1:scope='UNESCO published property polygon'
   elif a.get('source_layer')==2:scope='UNESCO published buffer polygon, NOT property'
   elif 'DE_532_' in label:scope='Berlin government polygon of BERLIN-ONLY components '+('buffer; NOT property' if 'buffer' in label else 'property; incomplete Potsdam coverage')
   else:scope='Berlin government UNESCO '+('buffer polygon, NOT property' if 'buffer' in label else 'property polygon')
  a['geometry_scope']=scope;a['model']='Sphere R6371.0088km; origin52.521146530576253N,13.4133090391431029E; initial true247.5deg; closed full great circle'
  a['conditionality']='All intersections conditional on exact nominal247.5-degree spherical model and source geometry, not survey-grade physical touches. WGS84 westward near-return misses Kremlin grounds by~1.344km.'
  features.append(f)
# Add only named local building results requested by parent, preserving marginal classifications.
for f in json.loads((P/'kremlin_buildings.geojson').read_text())['features']:
 a=f['properties']
 if a['osm_id'] not in [225033,1359335,1360631,1360642]:continue
 a['geometry_scope']='OSM individual building footprint';a['classification_note']='Narrow building clip or close miss: model/map-sensitive; no physical-survey conclusion';a['source_result_file']='kremlin_buildings.geojson';a['model']='Closed spherical great circle; initial247.5deg; R6371.0088km';features.append(f)
meta={}
for fn in ['relation_1360641.osm','relation_1577673.osm','relation_1149002.osm','osm_relations_metadata.xml','osm_ways_metadata.xml','relation_7392626.osm']:
 for x in E.parse(P/fn).getroot():
  if x.tag in ['way','relation']:meta[(x.tag,int(x.attrib['id']))]={'version':x.attrib.get('version'),'timestamp':x.attrib.get('timestamp')}
for f in features:
 a=f['properties'];m=meta.get((a.get('osm_type'),a.get('osm_id')))
 if m:a['osm_version']=m['version'];a['osm_timestamp']=m['timestamp']
(P/'EUROPE_FINAL_FOOTPRINTS.geojson').write_text(json.dumps({'type':'FeatureCollection','features':features}))
(P/'EUROPE_FINAL_RESULTS.json').write_text(json.dumps([f['properties'] for f in features],indent=2))
lines=[]
with (P/'EUROPE_FINAL_RESULTS.csv').open('w') as o:
 fields=['name','geometry_scope','result','minimum_gap_m','entry_km','exit_km','inside_length_m','interior_clearance_m','source_url','geometry_id','osm_version','osm_timestamp','caveat']
 w=csv.DictWriter(o,fieldnames=fields);w.writeheader()
 for f in features:
  a=f['properties']
  for interval in a['intervals'] or [{}]:
   name=a['name'] if a.get('osm_id') else a['label']
   w.writerow({'name':name,'geometry_scope':a['geometry_scope'],'result':a['result'],'minimum_gap_m':round(a['minimum_gap_m'],3),'entry_km':interval.get('entry_km'),'exit_km':interval.get('exit_km'),'inside_length_m':interval.get('length_m'),'interior_clearance_m':interval.get('sampled_max_interior_clearance_m'),'source_url':a['source_url'],'geometry_id':str(a.get('osm_type',''))+'/'+str(a.get('osm_id',a.get('geometry_id'))),'osm_version':a.get('osm_version'),'osm_timestamp':a.get('osm_timestamp'),'caveat':a.get('conditionality',a.get('classification_note'))})
   if interval:
    coords=[unproject(float(s)) for s in np.linspace(interval['entry_km'],interval['exit_km'],max(2,int(interval['length_m']/10)+2))]
    props={**a,**interval};props.pop('intervals',None);lines.append({'type':'Feature','properties':props,'geometry':{'type':'LineString','coordinates':coords}})
(P/'EUROPE_FINAL_INTERSECTION_SEGMENTS.geojson').write_text(json.dumps({'type':'FeatureCollection','features':lines}))
raw=[]
for f in sorted(P.iterdir()):
 if f.name.endswith(('_nominatim.json','.osm','metadata.xml','_official.geojson')) or f.name in ['berlin_wfs_capabilities.xml']:
  b=f.read_bytes();raw.append({'file':f.name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
manifest={'retrieved_utc_date':'2026-10-24','model':features[0]['properties']['model'],'sources':{'osm':'https://www.openstreetmap.org/copyright','osm_queries':'fetch_candidates.py, fetch_additional.py, raw OSM XML object ids; Nominatim polygons requested with polygon_geojson=1','berlin':'https://gdi.berlin.de/services/wfs/welterbe?service=WFS&version=2.0.0&request=GetFeature&typeNames=welterbe:welterbe&count=500&outputFormat=application/json&srsName=EPSG:4326','paris':'https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/plu-annexes-biens-inscrits-au-patrimoine-mondial/exports/geojson','unesco':'unesco_layer1_query_url.txt and unesco_layer2_query_url.txt'},'coverage_limitations':['Not an exhaustive global landmark inventory','Full Potsdam/Berlin UNESCO property polygon unavailable in queried UNESCO current service; Berlin-only official components and six major individual OSM parks checked','Kremlin/RedSquare and Novodevichy official UNESCO core unavailable in queried current service; OSM site footprints used, not UNESCO core inferred','Vilnius municipal ArcGIS publicly discoverable endpoint returned403; no bypass; independent UNESCO published boundary used successfully','Museum Island official property misses139m while buffer intersects53m; buffer is NOT property','Narrow Kremlin building clips highly sensitive to geometry and nominal bearing'],'files':raw}
(P/'EUROPE_SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2))
print('FINAL',len(features),'footprints',len(lines),'intersectionsegments')
