import json,pathlib,urllib.request,urllib.parse,time
P=pathlib.Path(__file__).parent;ROOT=P.parent
BASE='https://services6.arcgis.com/eMd5K6XXEvJETxfQ/arcgis/rest/services/prd_whc_sites_dossiers_elements_v2_view/FeatureServer'
route=json.loads((ROOT/'route.geojson').read_text())['features'][0]['geometry']['coordinates']
# Read-only spatial query of the entire defined route, no point-distance prefilter.
geometry={'paths':[[[round(x,9),round(y,9)] for x,y in part] for part in route],'spatialReference':{'wkid':4326}}
def query(layer,params,name):
 q={'f':'json',**params};data=urllib.parse.urlencode(q).encode();u=f'{BASE}/{layer}/query'
 req=urllib.request.Request(u,data=data,headers={'Content-Type':'application/x-www-form-urlencoded'},method='POST')
 started=time.time();raw=urllib.request.urlopen(req,timeout=180).read();(P/(name+'.json')).write_bytes(raw)
 o=json.loads(raw)
 if 'error'in o:raise RuntimeError(o['error'])
 print(name,'request_bytes',len(data),'response_bytes',len(raw),'seconds',round(time.time()-started,2),'keys',list(o.keys()),flush=True)
 return o
for layer in [1,2]:
 ids=query(layer,{'geometry':json.dumps(geometry,separators=(',',':')),'geometryType':'esriGeometryPolyline','inSR':'4326','spatialRel':'esriSpatialRelIntersects','returnIdsOnly':'true','returnGeometry':'false','where':'1=1'},f'layer{layer}_route_hit_ids')
 print('ids',ids.get('objectIds'),flush=True)
 ids=ids.get('objectIds') or []
 if ids:
  # Only route-intersecting polygons are fetched, explicitly bounded by IDs.
  q=query(layer,{'objectIds':','.join(map(str,ids)),'outFields':'OBJECTID,property_id,dossier_id,dossier,property_name_en,property_inscribed,element_id,element_name_en,element_precision_publish,element_state_name_en,element_state,element_CoreArea,element_BufferArea,EditDate','outSR':'4326','returnGeometry':'true','f':'geojson','resultRecordCount':'2000'},f'layer{layer}_route_hit_polygons')
  print('features',len(q.get('features',[])),flush=True)
  for f in q.get('features',[]):print(f.get('properties') or f.get('attributes'),flush=True)
 # Coverage metadata only: property-name groups and count, not unbounded polygons.
 cov=query(layer,{'where':'1=1','groupByFieldsForStatistics':'property_name_en','outStatistics':json.dumps([{'statisticType':'count','onStatisticField':'OBJECTID','outStatisticFieldName':'polygon_count'}]),'returnGeometry':'false','resultRecordCount':'2000'},f'layer{layer}_coverage_counts')
 print('coverage_properties',len(cov.get('features',[])),'exceeded',cov.get('exceededTransferLimit'),flush=True)
