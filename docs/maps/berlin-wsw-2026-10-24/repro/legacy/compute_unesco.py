import contextlib,io,json,csv
with contextlib.redirect_stdout(io.StringIO()):from compute_route import *
records=json.loads((P/'unesco_world_heritage.json').read_text())
out=[];npoints=0;missing=[]
for site in records:
 components=json.loads(site['components_list']) if site.get('components_list') else []
 valid=[x for x in components if x.get('latitude') is not None and x.get('longitude') is not None]
 if not valid:
  geo=site.get('coordinates')
  if geo:
   geom=geo.get('geometry',geo)
   pts=geom['coordinates'] if geom['type']=='MultiPoint' else [geom['coordinates']]
   valid=[{'latitude':y,'longitude':x,'name':site['name_en'],'ref':site['id_no']} for x,y in pts]
 if not valid:missing.append(site['name_en'])
 for x in valid:
  npoints+=1;v=proximity(float(x['longitude']),float(x['latitude']))
  if v['off_line_km']<=50:
   v.update(name=site['name_en'],component_name=x.get('name'),component_ref=x.get('ref'),id=site['id_no'],inscribed=site['date_inscribed'],url='https://whc.unesco.org/en/list/'+site['id_no']+'/',category=site['category'])
   out.append(v)
out.sort(key=lambda x:x['along_km'])
summary={'site_records':len(records),'reference_points_tested':npoints,'sites_missing_coordinates':missing,'points_within_50km':out,'threshold_km':50,'warning':'Distances refer to UNESCO reference points, not site footprints. Serial properties can have multiple component points. Current 2026 list; inscriptions may postdate 1990.'}
(P/'unesco_within_50km.json').write_text(json.dumps(summary,indent=2))
with (P/'unesco_within_50km.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=out[0].keys());w.writeheader();w.writerows(out)
print('records',len(records),'points',npoints,'within',len(out),'unique sites',len(set(x['id'] for x in out)))
for x in out:print(f"{x['along_km']:8.1f} {x['off_line_km']:5.1f} {x['name']} | {x['component_name']} | {x['inscribed']}")
