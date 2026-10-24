from verify_footprints import *
base='https://services6.arcgis.com/eMd5K6XXEvJETxfQ/arcgis/rest/services/prd_whc_sites_dossiers_elements_v2_view/FeatureServer'
out=[];features=[]
for layer in [1,2]:
 for f in json.loads((P/f'unesco_layer{layer}_official.geojson').read_text())['features']:
  props=f['properties'];label=props['property_name_en']+(' / property' if layer==1 else ' / buffer')
  a,g=analyze({'geojson':f['geometry'],'osm_type':'official','osm_id':str(f['id']),'display_name':props['property_name_en']},label)
  a.pop('osm_type');a['geometry_id']=a.pop('osm_id');a['source_url']=base+f'/{layer}/'+str(f['id']);a['authority']='UNESCO World Heritage Centre';a['source_layer']=layer;a['source_properties']={k:props.get(k)for k in ['property_id','dossier','dossier_id','element_id','element_name_en','element_precision_publish','EditDate_1']};a['accuracy_note']='Official UNESCO published polygon; numeric precision is not survey accuracy. Conditional on spherical Earth and nominal initial true247.5° bearing.';g['properties']=a
  out.append(a);features.append(g);print(label,a['result'],round(a['minimum_gap_m'],2),a['intervals'])
(P/'unesco_results.json').write_text(json.dumps(out,indent=2));(P/'verified_unesco_footprints.geojson').write_text(json.dumps({'type':'FeatureCollection','features':features}))
