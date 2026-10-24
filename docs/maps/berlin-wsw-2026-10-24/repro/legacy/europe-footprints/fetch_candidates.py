import urllib.request, urllib.parse, json, pathlib, time
p=pathlib.Path(__file__).parent
queries={'museum_island':'Museumsinsel Berlin','potsdam_heritage':'Palaces and Parks of Potsdam and Berlin','versailles_palace':'Château de Versailles','versailles_park':'Parc du Château de Versailles','chartres_cathedral':'Cathédrale Notre-Dame de Chartres','red_square':'Красная площадь Москва','novodevichy':'Новодевичий монастырь Москва','vilnius_old_town':'Vilnius Old Town','paris_city':'Paris France','moscow_city':'Moscow Russia'}
for name,q in queries.items():
 f=p/(name+'_nominatim.json')
 if f.exists():continue
 u='https://nominatim.openstreetmap.org/search?'+urllib.parse.urlencode({'q':q,'format':'jsonv2','polygon_geojson':1,'limit':3})
 try:
  r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Geographic-footprint-verification/1.0'}),timeout=40);b=r.read();f.write_bytes(b)
  vals=json.loads(b);print(name,[(x['osm_type'],x['osm_id'],x['display_name'],x.get('geojson',{}).get('type')) for x in vals],flush=True)
 except Exception as e:print(name,type(e).__name__,str(e),flush=True)
 time.sleep(1.1)
