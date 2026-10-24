import urllib.request,urllib.parse,pathlib,json,concurrent.futures
P=pathlib.Path(__file__).parent
jobs={
'gondwana_official.geojson':('https://gis.environment.gov.au/gispubmap/rest/services/ogc_services/World_Heritage_Areas/MapServer/0/query',{'where':"NAME = 'Gondwana Rainforests of Australia'",'outFields':'*','outSR':'4326','f':'geojson'}),
'bounty_reserve_metadata.json':('https://services1.arcgis.com/3JjYDyG3oajxU6HO/ArcGIS/rest/services/DOC_Marine_Reserves/FeatureServer/0',{'f':'pjson'}),
'santa_ana_osm.json':('https://overpass-api.de/api/interpreter',{'data':'[out:json][timeout:30];(way[building](-16.585,-60.690,-16.582,-60.684);nwr["amenity"="place_of_worship"](-16.585,-60.690,-16.582,-60.684););out meta geom;'}),
'cebu_boundary_osm.json':('https://overpass-api.de/api/interpreter',{'data':'[out:json][timeout:30];rel["boundary"="administrative"]["name"="Cebu City"](10.2,123.7,10.6,124.0);out meta geom;'})}
def fetch(n,job):
 url=job[0]+'?'+urllib.parse.urlencode(job[1]);(P/(n+'.url')).write_text(url)
 try:
  d=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Research geometry verification contact none'}),timeout=45).read();(P/n).write_bytes(d);print(n,len(d),flush=True)
 except Exception as e:print(n,str(e),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(lambda x:fetch(*x),jobs.items()))
