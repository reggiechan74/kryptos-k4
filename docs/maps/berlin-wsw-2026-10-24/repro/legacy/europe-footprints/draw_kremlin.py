import os;os.environ['MPLCONFIGDIR']='/tmp/europe-mpl'
from verify_footprints import *
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as PatchPolygon
from shapely.ops import nearest_points
LON0=37.6175;LAT0=55.7515
k=R*1000*math.pi/180

def xy(lon,lat,z=None):return ((np.asarray(lon)-LON0)*k*math.cos(math.radians(LAT0)),(np.asarray(lat)-LAT0)*k)
def draw_poly(ax,g,fc,ec,lw=1,alpha=1,z=2):
 for sub in ([g] if g.geom_type=='Polygon' else g.geoms):
  ax.add_patch(PatchPolygon(np.asarray(sub.exterior.coords),closed=True,facecolor=fc,edgecolor=ec,lw=lw,alpha=alpha,zorder=z))
  for ring in sub.interiors:ax.add_patch(PatchPolygon(np.asarray(ring.coords),closed=True,facecolor='#f7f9fb',edgecolor=ec,lw=.6,zorder=z))
kremlin=json.loads((P/'moscow_kremlin_nominatim.json').read_text())[0];square=json.loads((P/'red_square_nominatim.json').read_text())[0]
gk=transform(xy,shape(kremlin['geojson']));gs=transform(xy,shape(square['geojson']))
fig=plt.figure(figsize=(14,10),facecolor='white');ax=fig.add_axes([.055,.19,.66,.67]);side=fig.add_axes([.745,.20,.235,.64]);side.axis('off')
ax.set_facecolor('#f7f9fb');draw_poly(ax,gk,'#c6e9d5','#21825a',1.8);draw_poly(ax,gs,'#f8e1ad','#bb8928',1.5)
for f in json.loads((P/'kremlin_buildings.geojson').read_text())['features']:
 g=transform(xy,shape(f['geometry']));draw_poly(ax,g,'#dae0e4','#89949d',.45,z=3)
route=LineString([unproject(s) for s in np.linspace(38421.0,38423.1,600)]);line=transform(xy,route)
x,y=line.xy;ax.plot(x,y,color='#cf3554',lw=2.7,zorder=7)
cut=line.intersection(gk)
for seg in flatten(cut):
 x,y=seg.xy;ax.plot(x,y,color='#087c4c',lw=5,zorder=8)
for vals in [(38421.838361, 'Entry'),(38422.289440,'Exit')]:
 xx,yy=xy(*unproject(vals[0]));ax.scatter(xx,yy,s=40,c='#087c4c',edgecolor='white',zorder=9);ax.text(xx,yy-28,vals[1],fontsize=10,ha='center',va='top',color='#087c4c',fontweight='bold')
a,b=nearest_points(gs,line);ax.plot([a.x,b.x],[a.y,b.y],ls=(0,(3,3)),color='#a57416',lw=1.5,zorder=7);ax.text(a.x+30,(a.y+b.y)/2,'267 m\nminimum gap',fontsize=10,color='#886415',ha='left',va='center',bbox={'facecolor':'white','edgecolor':'none','alpha':.9,'pad':4})
ax.text(*xy(37.6167,55.75325),'KREMLIN GROUNDS',fontsize=13,fontweight='bold',ha='center',color='#125f3e',zorder=10)
ax.text(*xy(37.62135,55.7540),'RED SQUARE',fontsize=11,fontweight='bold',ha='center',rotation=-50,color='#886415',zorder=10)
ax.annotate('Grand Kremlin Palace\n13 m mapped miss',xy=xy(37.6162,55.74975),xytext=xy(37.6155,55.75145),fontsize=10,ha='center',arrowprops={'arrowstyle':'-','color':'#475561'},bbox={'facecolor':'white','edgecolor':'none','alpha':.92,'pad':3},zorder=12)
ax.annotate('Armoury\n26 m mapped clip*',xy=xy(37.6131,55.74935),xytext=xy(37.61175,55.7508),fontsize=10,ha='center',arrowprops={'arrowstyle':'-','color':'#475561'},bbox={'facecolor':'white','edgecolor':'none','alpha':.92,'pad':3},zorder=12)
ax.set_xlim(-490,525);ax.set_ylim(-430,500);ax.set_aspect('equal');ax.set_xticks([]);ax.set_yticks([])
for s in ax.spines.values():s.set_visible(False)
# North and a local metric scale.
ax.annotate('N',xy=(450,420),xytext=(450,330),ha='center',fontsize=11,fontweight='bold',arrowprops={'arrowstyle':'-|>','color':'#263743','lw':1.5})
ax.plot([-430,-230],[-375,-375],color='#263743',lw=3);ax.plot([-430,-430],[-382,-368],color='#263743',lw=1);ax.plot([-230,-230],[-382,-368],color='#263743',lw=1);ax.text(-330,-355,'200 m',ha='center',fontsize=10,color='#263743')
fig.text(.055,.945,'Kremlin grounds: crossed. Red Square: nearby.',fontsize=23,fontweight='bold',color='#152d3d')
fig.text(.055,.905,'Berlin → full great circle • nominal initial true bearing 247.5° • spherical Earth',fontsize=12,color='#546674')
side.text(0,.99,'WHAT THE LINE TOUCHES',fontsize=12,fontweight='bold',color='#152d3d',va='top')
side.text(0,.89,'Kremlin grounds\n451 m inside the mapped boundary',fontsize=13,fontweight='bold',color='#087c4c',va='top',linespacing=1.6)
side.text(0,.73,'Red Square\nNot intersected; ~267 m away',fontsize=13,fontweight='bold',color='#a57416',va='top',linespacing=1.6)
side.text(0,.56,'Green: route inside Kremlin grounds\nRose: the same route outside\nGrey: mapped building footprints',fontsize=11,color='#475561',va='top',linespacing=1.7)
side.text(0,.38,'* Small building clips are sensitive\nto mapping and model assumptions.\nThey are not survey-grade claims.',fontsize=11,color='#475561',va='top',linespacing=1.6)
side.text(0,.19,'Bearing matters:\n247.51° misses Kremlin grounds.\nThis map uses exactly 247.50°.',fontsize=11,fontweight='bold',color='#475561',va='top',linespacing=1.6)
fig.text(.055,.125,'Model: sphere R = 6,371.0088 km; origin 52.5211465306°N, 13.4133090391°E. Not a WGS84 ellipsoidal geodesic.',fontsize=10,color='#546674')
fig.text(.055,.091,'Sources: © OpenStreetMap contributors (ODbL), retrieved 24 Oct 2026. Kremlin relation 1360641; Red Square relation 1577673.',fontsize=10,color='#546674')
fig.text(.055,.058,'The green outline is Kremlin grounds, not the combined UNESCO property boundary. Local north-up metric display; no basemap imagery.',fontsize=10,color='#546674')
fig.savefig(P/'Kremlin-ground-intersection.png',dpi=180,bbox_inches='tight',facecolor='white');fig.savefig(P/'Kremlin-ground-intersection.svg',bbox_inches='tight',facecolor='white');print(P/'Kremlin-ground-intersection.png')
