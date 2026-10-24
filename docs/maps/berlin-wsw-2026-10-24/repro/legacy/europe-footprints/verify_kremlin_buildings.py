from verify_footprints import *
from shapely.ops import polygonize,unary_union
from shapely.geometry import Polygon
import xml.etree.ElementTree as E
root=E.parse(P/'kremlin_bbox_small.osm').getroot()
nodes={x.attrib['id']:(float(x.attrib['lon']),float(x.attrib['lat'])) for x in root.findall('node')}
ways={x.attrib['id']:x for x in root.findall('way')}
rels={x.attrib['id']:x for x in root.findall('relation')}
def coords(w):return [nodes[x.attrib['ref']] for x in w.findall('nd')]
def geom(elem):
 if elem.tag=='way':return Polygon(coords(elem))
 outer=[];inner=[]
 for mem in elem.findall('member'):
  if mem.attrib['role'] not in ['outer','inner','outline','']:continue
  if mem.attrib['type']!='way':continue
  line=LineString(coords(ways[mem.attrib['ref']]))
  (inner if mem.attrib['role']=='inner' else outer).append(line)
 if not outer:raise ValueError('no outer')
 g=unary_union(list(polygonize(outer)))
 if inner:g=g.difference(unary_union(list(polygonize(inner))))
 return g
out=[];features=[];skipped=[]
for elem in [*root.findall('way'),*root.findall('relation')]:
 tags={t.attrib['k']:t.attrib['v'] for t in elem.findall('tag')}
 if 'building' not in tags:continue
 if elem.tag=='way' and (len(elem.findall('nd'))<4 or elem.findall('nd')[0].attrib['ref']!=elem.findall('nd')[-1].attrib['ref']):continue
 try:g=geom(elem)
 except Exception as e:skipped.append((elem.tag,elem.attrib['id'],tags.get('name'),str(e)));continue
 if g.is_empty:continue
 row={'osm_type':elem.tag,'osm_id':int(elem.attrib['id']),'display_name':tags.get('name:en',tags.get('name','Unnamed '+tags['building'])),'geojson':mapping(g)}
 a,feat=analyze(row,row['display_name']);a['source_tags']=tags;a['osm_version']=elem.attrib.get('version');a['osm_timestamp']=elem.attrib.get('timestamp');feat['properties']=a
 if a['result']!='miss' or 'name' in tags:
  out.append(a);features.append(feat);print(row['display_name'],elem.tag,elem.attrib['id'],a['result'],round(a['minimum_gap_m'],2),[(round(z['entry_km'],6),round(z['exit_km'],6),round(z['length_m'],1),round(z['sampled_max_interior_clearance_m'],1))for z in a['intervals']])
(P/'kremlin_buildings_results.json').write_text(json.dumps(out,indent=2));(P/'kremlin_buildings.geojson').write_text(json.dumps({'type':'FeatureCollection','features':features}));(P/'kremlin_buildings_skipped.json').write_text(json.dumps(skipped,indent=2));print('SKIPPED',skipped)
