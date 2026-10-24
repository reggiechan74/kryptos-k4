import pathlib
exec((pathlib.Path(__file__).parent/'fetch.py').read_text().split('with concurrent.futures')[0].split('jobs={')[0])
jobs={
'bounty_reserve.geojson':('https://services1.arcgis.com/3JjYDyG3oajxU6HO/ArcGIS/rest/services/DOC_Marine_Reserves/FeatureServer/0/query',{'where':"Name LIKE '%Bounty%'",'outFields':'*','outSR':'4326','f':'geojson'}),
'santa_ana_osm.xml':('https://api.openstreetmap.org/api/0.6/map',{'bbox':'-60.690,-16.585,-60.684,-16.582'})}
def fetch(n,job):
 url=job[0]+'?'+urllib.parse.urlencode(job[1]);(P/(n+'.url')).write_text(url)
 try:
  d=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'RouteFootprintResearch/1.0'}),timeout=45).read();(P/n).write_bytes(d);print(n,len(d),flush=True)
 except Exception as e:print(n,str(e),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(lambda x:fetch(*x),jobs.items()))
