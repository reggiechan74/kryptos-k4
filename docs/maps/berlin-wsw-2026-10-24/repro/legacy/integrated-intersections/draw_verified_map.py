import sys;
import pathlib,json,math,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, FormatStrFormatter
from matplotlib.collections import LineCollection
from shapely.geometry import shape
P=pathlib.Path(__file__).parent;ROOT=P.parent
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
GREEN='#147d64';AMBER='#bd7d13';GREY='#85929a';LINE='#c44726';BG='#f8fafc'
eu=json.loads((ROOT/'europe-footprints/EUROPE_FINAL_FOOTPRINTS.geojson').read_text())['features']
non=json.loads((ROOT/'footprints-non-europe/verified_footprints.geojson').read_text())['features']
uc=json.loads((ROOT/'unesco-boundary-pass/layer1_route_hit_polygons.json').read_text())['features']
ub=json.loads((ROOT/'unesco-boundary-pass/layer2_route_hit_polygons.json').read_text())['features']
lakes=json.loads((ROOT/'ne_10m_lakes.geojson').read_text())['features']
cs=json.loads((ROOT/'ne_10m_admin_0_countries.geojson').read_text())['features']
route=json.loads((ROOT/'route.geojson').read_text())['features'][0]['geometry']['coordinates']
R=6371.0088;la,lo,az=np.radians([52.521146530576253,13.413309039143103,247.5]);u=np.array([np.cos(la)*np.cos(lo),np.cos(la)*np.sin(lo),np.sin(la)]);v=np.array([-np.sin(la)*np.cos(lo),-np.sin(la)*np.sin(lo),np.cos(la)])*np.cos(az)+np.array([-np.sin(lo),np.cos(lo),0])*np.sin(az)
def xy(d):
 p=np.cos(np.asarray(d)/R)[...,None]*u+np.sin(np.asarray(d)/R)[...,None]*v
 return np.degrees(np.arctan2(p[...,0:1]*0+p[...,1:2],p[...,0:1]))[...,0],np.degrees(np.arctan2(p[...,2],np.hypot(p[...,0],p[...,1])))
def find(arr,key,value):return next(f for f in arr if value in str(f['properties'].get(key,'')))
def poly(ax,f,color=GREEN,alpha=.20,lw=1.1):
 g=shape(f['geometry'])
 def draw(q):
  if q.geom_type=='Polygon':
   a=np.asarray(q.exterior.coords);ax.fill(a[:,0],a[:,1],fc=color,ec=color,lw=lw,alpha=alpha,zorder=2)
   for z in q.interiors:
    a=np.asarray(z.coords);ax.fill(a[:,0],a[:,1],fc='white',ec=color,lw=lw*.6,zorder=2)
  elif hasattr(q,'geoms'):
   for z in q.geoms:draw(z)
 draw(g)
def route_local(ax,center_km,span_km=25):
 ds=np.linspace(max(0,center_km-span_km),min(40030.228884,center_km+span_km),max(100,int(span_km*2/.01)))
 x,y=xy(ds)
 cuts=np.where(np.abs(np.diff(x))>180)[0]+1
 for indices in np.split(np.arange(len(x)),cuts):
  ax.plot(x[indices],y[indices],color=LINE,lw=2.2,zorder=8)
def panel(ax,title,desc,source,bbox,center,features):
 ax.set_facecolor('white')
 for f,color in features:poly(ax,f,color)
 route_local(ax,center,300 if center in [21165,33370] else 45)
 ax.set_xlim(bbox[:2]);ax.set_ylim(bbox[2:]);ax.set_aspect(1/math.cos(math.radians(sum(bbox[2:])/2)))
 ax.set_title(title,loc='left',fontsize=12.6,fontweight='bold',pad=26,color='#173f48')
 ax.text(0,1.035,desc,transform=ax.transAxes,fontsize=9.7,color='#384e57',va='bottom')
 ax.text(0,-.15,source,transform=ax.transAxes,fontsize=8.5,color='#687880')
 ax.tick_params(labelsize=7,colors='#70818a');ax.grid(alpha=.18,lw=.5)
 ax.xaxis.set_major_locator(MaxNLocator(nbins=4));ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
 if bbox[1]-bbox[0]<.03:ax.xaxis.set_major_formatter(FormatStrFormatter('%.3f'))
 for s in ax.spines.values():s.set_color('#b8c6cb')
fig=plt.figure(figsize=(16,19),facecolor=BG)
fig.text(.045,.967,'Mapped intersections — not nearby points',fontsize=25,fontweight='bold',color='#18353f')
fig.text(.045,.943,'Selected footprint checks along the full WSW great circle from the Berlin World Clock',fontsize=13,color='#48616b')
fig.text(.045,.923,'SPHERICAL MODEL, initial true bearing 247.5°. Changing to WGS84 makes the Kremlin crossing a ≈1.3 km miss.',fontsize=11.1,color='#8a3d22',bbox={'boxstyle':'round,pad=.45','fc':'#fff0db','ec':'none'})
ax=fig.add_axes([.045,.70,.91,.20]);ax.set_facecolor('#eaf3f8')
segs=[]
for f in cs:
 g=f['geometry'];polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
 for p in polys:
  a=np.asarray(p[0]);ax.fill(a[:,0],a[:,1],fc='#dce5df',ec='none',zorder=1);segs.append(a)
ax.add_collection(LineCollection(segs,colors='#aebbb4',lw=.22,zorder=2))
for p in route:
 a=np.asarray(p);ax.plot(a[:,0],a[:,1],color=LINE,lw=1.9,zorder=3)
marks=[('1',214,(-5,61)),('2',21165,(165,-58)),('3',24320,(157,-19)),('4',29598,(132,18)),('5',33370,(104,45)),('6',38422,(45,67))]
for label,d,off in marks:
 pt=xy(d);ax.scatter(*pt,s=20,color=GREEN,zorder=6)
 ax.annotate(label,xy=pt,xytext=off,ha='center',va='center',color='white',fontweight='bold',fontsize=10,bbox={'boxstyle':'circle,pad=.28','fc':GREEN,'ec':'white','lw':.7},arrowprops={'arrowstyle':'-','color':GREEN,'lw':.7},zorder=7)
ax.scatter(13.413309,52.521147,s=70,marker='*',color='#e6ac2c',ec='#4b4e38',lw=.5,zorder=8)
ax.set_xlim(-180,180);ax.set_ylim(-63,76);ax.set_xticks([-180,-120,-60,0,60,120,180]);ax.set_yticks([-60,0,60]);ax.tick_params(labelsize=8,colors='#73838b');ax.grid(alpha=.18,lw=.5)
for s in ax.spines.values():s.set_color('#bacad1')
fig.text(.045,.68,'Numbers locate the six crossing examples below. Buffers and tested misses are shown separately in the lower panels.',fontsize=10.3,color='#4f6570')
axes=[]
for row in range(3):
 for col in range(3):axes.append(fig.add_axes([.045+col*.313,.49-row*.205,.275,.143]))
upper=uc[0]
panel(axes[0],'1  Upper Harz heritage property','Two narrow intersections: ≈20 m + 28 m; first shown.','UNESCO core-property polygon; no specific canal hit inferred.',(10.5425,10.5503,51.7485,51.7535),213.56,[(upper,GREEN)])
bounty=find(non,'name','Bounty Islands Marine Reserve')
panel(axes[1],'2  Bounty Islands marine reserve','≈35.0 km through protected WATER, not island land.','New Zealand Department of Conservation reserve boundary.',(178.50,179.65,-48.02,-47.23),21165,[(bounty,GREEN)])
npf=find(non,'name','Main Range National Park');gq=find(non,'name','QLD declared');gn=find(non,'name','NSW declared')
panel(axes[2],'3  Main Range National Park','Four park crossings total ≈1.83 km; first shown.','Queensland park / Australian declared WH boundaries.',(152.365,152.46,-28.30,-28.205),24320,[(npf,GREEN),(gq,GREY),(gn,GREY)])
axes[2].text(.03,.03,'Gondwana World Heritage core:\nmissed by ≈240 m',transform=axes[2].transAxes,fontsize=8,color='#4e626a',bbox={'fc':'white','ec':'none','alpha':.8})
cebu=find(non,'name','Cebu City');g=shape(cebu['geometry']);a,b,c,d=g.bounds
panel(axes[3],'4  Cebu City municipality','≈21.7 km inside the administrative boundary.','OpenStreetMap boundary; not continuous built-up area.',(a-.015,c+.015,b-.015,d+.015),29598,[(cebu,GREEN)])
qing=next(f for f in lakes if f['properties'].get('name_en')=='Qinghai');g=shape(qing['geometry']);a,b,c,d=g.bounds
panel(axes[4],'5  Qinghai Lake','≈102 km inside the mapped lake polygon.','Natural Earth 1:10m; generalized water extent.',(a-.2,c+.2,b-.1,d+.1),33370,[(qing,GREEN)])
krem=find(eu,'label','moscow_kremlin');red=find(eu,'label','red_square')
ks=[(red,GREY),(krem,GREEN)]+[(f,GREEN) for f in eu if f['properties'].get('label') in ['Armoury','Armoury Tower','First Unnamed Tower','Unnamed wall']]
panel(axes[5],'6  Kremlin grounds (sphere only)','≈451 m crossing; Red Square missed by ≈267 m.','OSM footprints. Narrow building/tower clips are model-sensitive.',(37.609,37.628,55.744,55.756),38422,ks)
axes[5].text(.03,.03,'WGS84 near-return:\nmisses grounds by ≈1.3 km',transform=axes[5].transAxes,fontsize=8,color='#8a3d22',bbox={'fc':'#fff0db','ec':'none','alpha':.94})
mi=find(eu,'label','Museumsinsel / DE_896_boundaries');mib=find(eu,'label','Pufferzone Museumsinsel');g=shape(mi['geometry']);a,b,c,d=g.bounds
panel(axes[6],'A  Museum Island: buffer only','Core property missed ≈139 m; buffer crossed ≈53 m.','Official Berlin heritage boundary; a buffer is NOT the property.',(a-.0015,c+.003,b-.0015,d+.0015),1,[(mib,AMBER),(mi,GREY)])
vcore=next(f for f in eu if f['properties'].get('label')=='Palace and Park of Versailles / property');vbuff=next(f for f in eu if f['properties'].get('label')=='Palace and Park of Versailles / buffer');g=shape(vbuff['geometry']);a,b,c,d=g.bounds
panel(axes[7],'B  Versailles: buffer only','Core property missed ≈890 m; buffer crossed 4.55 km.','UNESCO core vs buffer. Palace building is farther away.',(a-.008,c+.008,b-.008,d+.008),899,[(vbuff,AMBER),(vcore,GREY)])
legend=axes[8];legend.axis('off')
legend.text(0,1.14,'How to read the evidence',fontsize=13,fontweight='bold',color='#173f48',transform=legend.transAxes)
for y,color,txt in [(.93,GREEN,'Crossed mapped area / footprint'),(.77,AMBER,'Buffer zone only — not core property'),(.61,GREY,'Tested footprint not crossed'),(.45,LINE,'The nominal spherical route')]:
 legend.plot([0,.10],[y,y],color=color,lw=6 if color!=LINE else 2,transform=legend.transAxes);legend.text(.15,y,txt,va='center',fontsize=10,transform=legend.transAxes,color='#3d555f')
legend.text(0,.24,'Not an inventory of every physical object.\nFull tested geometry list and source URLs\nare in the accompanying CSV.\n\nUNESCO core polygons cover 519 property\nname groups; missing polygons stay untested.',fontsize=9.5,va='top',linespacing=1.4,transform=legend.transAxes,color='#536b75')
fig.text(.045,.038,'Conditional results: exact nominal bearing + spherical Earth + published geometry. GIS and OSM accuracy is not survey accuracy.',fontsize=10,color='#425d68')
fig.text(.045,.022,'Sources: UNESCO GIS; Berlin monument office; DOC NZ; Queensland/DCCEEW; © OpenStreetMap contributors; Natural Earth. Checked 24 Oct 2026.',fontsize=8.8,color='#687a83')
fig.savefig(P/'Berlin-WSW-Mapped-footprint-crossings-and-misses.png',dpi=175,facecolor=BG)
print(P/'Berlin-WSW-Mapped-footprint-crossings-and-misses.png')
