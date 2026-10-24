from verify_footprints import *
out=[];features=[]
source='https://gdi.berlin.de/services/wfs/welterbe'
data=json.loads((P/'berlin_heritage_official.geojson').read_text())
for f in data['features']:
 props=f['properties']
 if props['id'] not in ['DE_896_boundaries','DE_896_buffer','DE_532_boundaries','DE_532_buffer']:continue
 row={'geojson':f['geometry'],'osm_type':'official','osm_id':f['id'],'display_name':props['nam']}
 a,g=analyze(row,props['nam']+' / '+props['id']);a.pop('osm_type');a['geometry_id']=a.pop('osm_id');a['source_url']=source;a['authority']='Landesdenkmalamt Berlin';a['source_properties']=props;a['accuracy_note']='Official heritage boundary; spherical 247.5° nominal route. Numerical precision is not survey accuracy. Potsdam/Berlin 532 layer covers BERLIN components only.' if '532' in props['id'] else 'Official heritage boundary; spherical 247.5° nominal route. Numerical precision is not survey accuracy.';g['properties']=a
 out.append(a);features.append(g)
for f in json.loads((P/'paris_unesco_official.geojson').read_text())['features']:
 props=f['properties']
 if props['nom']!='RIVES DE LA SEINE':continue
 a,g=analyze({'geojson':f['geometry'],'osm_type':'official','osm_id':'Paris-RIVES-DE-LA-SEINE-'+props['type'],'display_name':props['nom']},props['nom']+' / '+props['type']);a.pop('osm_type');a['geometry_id']=a.pop('osm_id');a['source_url']='https://opendata.paris.fr/explore/dataset/plu-annexes-biens-inscrits-au-patrimoine-mondial/';a['authority']='Ville de Paris';a['source_properties']=props;a['accuracy_note']='Official July 2024 heritage property (PB) / buffer (ZT); nominal spherical 247.5° route. Numerical precision is not survey accuracy.';g['properties']=a;out.append(a);features.append(g)
for a in out:print(a['label'],a['result'],round(a['minimum_gap_m'],2),a['intervals'])
(P/'official_results.json').write_text(json.dumps(out,indent=2));(P/'verified_official_footprints.geojson').write_text(json.dumps({'type':'FeatureCollection','features':features}))
