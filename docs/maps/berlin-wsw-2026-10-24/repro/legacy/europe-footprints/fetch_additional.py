import urllib.request,urllib.parse,json,pathlib,time
p=pathlib.Path(__file__).parent
base='https://nominatim.openstreetmap.org/'
queries={'museum_buildings':('lookup',{'osm_ids':'R3619,R4211594,W313670733,W313670734,W313659704,W18578139,R7392625'}),'versailles_gardens':('lookup',{'osm_ids':'R6697690'}),'potsdam_neuergarten':('search',{'q':'Neuer Garten Potsdam','limit':2}),'potsdam_sanssouci':('search',{'q':'Park Sanssouci Potsdam','limit':2}),'potsdam_babelsberg':('search',{'q':'Park Babelsberg Potsdam','limit':2}),'potsdam_glienicke':('search',{'q':'Park Glienicke Berlin','limit':2}),'potsdam_sacrow':('search',{'q':'Schlosspark Sacrow','limit':2}),'potsdam_peacock':('search',{'q':'Pfaueninsel Berlin','limit':2})}
for name,(endpoint,params) in queries.items():
 f=p/(name+'_nominatim.json')
 if f.exists():continue
 params.update(format='jsonv2',polygon_geojson=1)
 u=base+endpoint+'?'+urllib.parse.urlencode(params)
 try:
  r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Geographic-footprint-verification/1.0'}),timeout=40);b=r.read();f.write_bytes(b)
  print(name,[(x['osm_type'],x['osm_id'],x['display_name'],x['geojson']['type']) for x in json.loads(b)],flush=True)
 except Exception as e:print(name,type(e).__name__,str(e),flush=True)
 time.sleep(1.1)
