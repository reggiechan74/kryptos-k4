import sys;
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import json,numpy as np,pathlib
P=pathlib.Path(__file__).parent
r=json.loads((P/'route_results.json').read_text());route=json.loads((P/'route.geojson').read_text())['features'][0]['geometry']['coordinates']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.titleweight':'bold'})
fig=plt.figure(figsize=(16,10.1),facecolor='#f8fafc')
ax=fig.add_axes([.045,.28,.91,.58]);ax.set_facecolor('#eaf3f8')
cs=json.loads((P/'ne_10m_admin_0_countries.geojson').read_text())['features']
segs=[]
for f in cs:
 g=f['geometry'];polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
 for poly in polys:
  for idx,ring in enumerate(poly):
   ring=np.array(ring)
   if idx==0:ax.fill(ring[:,0],ring[:,1],color='#d9e2dc',zorder=1)
   else:ax.fill(ring[:,0],ring[:,1],color='#eaf3f8',zorder=1)
   segs.append(ring)
ax.add_collection(LineCollection(segs,colors='#a8b5ad',linewidths=.28,zorder=2))
for part in route:
 a=np.array(part);ax.plot(a[:,0],a[:,1],lw=2.5,color='#005f73',zorder=4)
for f in json.loads((P/'country_polygon_intersections.geojson').read_text())['features']:
 a=np.array(f['geometry']['coordinates']);ax.plot(a[:,0],a[:,1],lw=3.1,color='#c64c20',zorder=5)
# Locate route coordinate by unambiguous length order, without geographic interpolation across map edge.
R=r['parameters']['sphere_radius_km'];la,lo,az=np.radians([52.521146530576253,13.413309039143103,247.5])
u=np.array([np.cos(la)*np.cos(lo),np.cos(la)*np.sin(lo),np.sin(la)])
east=np.array([-np.sin(lo),np.cos(lo),0]);north=np.array([-np.sin(la)*np.cos(lo),-np.sin(la)*np.sin(lo),np.cos(la)]);v=north*np.cos(az)+east*np.sin(az)
def xy(d):
 p=np.cos(d/R)*u+np.sin(d/R)*v
 return np.degrees(np.arctan2(p[1],p[0])),np.degrees(np.arctan2(p[2],np.hypot(p[0],p[1])))
for d in [2700,7000,10500,14500,18000,23100,27100,30700,33300,36000,39500]:
 a=xy(d-90);b=xy(d+90)
 ax.annotate('',xy=b,xytext=a,arrowprops={'arrowstyle':'-|>','mutation_scale':15,'color':'#005f73','lw':1.6},zorder=5)
# Numbered regions; consistent numbering follows increasing distance from Berlin.
marks=[(1,650,(-8,58)),(2,9300,(-38,-7)),(3,11600,(-89,-23)),(4,17800,(-133,-40)),(5,21935,(166,-58)),(6,25200,(150,-31)),(7,27950,(146,1)),(8,29900,(128,19)),(9,33300,(104,45)),(10,35900,(81,61)),(11,38300,(42,67)),(12,39400,(22,39))]
for num,d,pt in marks:
 target=xy(d)
 ax.plot(*target,marker='o',markersize=3.5,color='#005f73',zorder=6)
 ax.annotate(str(num),xy=target,xytext=pt,ha='center',va='center',fontsize=10.5,fontweight='bold',color='white',bbox={'boxstyle':'circle,pad=.30','fc':'#ae4e26','ec':'white','lw':1},arrowprops={'arrowstyle':'-','color':'#8b5c46','lw':.8,'shrinkA':8,'shrinkB':4},zorder=8)
ax.scatter([13.413309],[52.521147],s=95,marker='*',color='#ecb33b',edgecolor='#3a332a',lw=.7,zorder=10)
ax.annotate('BERLIN',xy=(13.413309,52.521147),xytext=(22,51),color='#202b31',fontsize=9,fontweight='bold',zorder=11)
for label,x,y in [('ATLANTIC',-35,25),('SOUTH PACIFIC',-121,-7),('NORTH PACIFIC',-140,34),('INDIAN OCEAN',70,-30)]:
 ax.text(x,y,label,color='#6d929f',fontsize=10,ha='center',fontweight='medium',zorder=3)
ax.text(-177,-63,'← continues',fontsize=8.5,color='#005f73');ax.text(177,-63,'continues ←',fontsize=8.5,ha='right',color='#005f73')
ax.set_xlim(-180,180);ax.set_ylim(-65,76)
ax.set_xticks(np.arange(-180,181,60));ax.set_yticks([-60,-30,0,30,60]);ax.grid(color='#b4c7d1',alpha=.4,lw=.5)
ax.set_xticklabels(['180°','120°W','60°W','0°','60°E','120°E','180°'],fontsize=9,color='#65757d')
ax.set_yticklabels(['60°S','30°S','0°','30°N','60°N'],fontsize=9,color='#65757d')
for s in ax.spines.values():s.set_color('#bacad1')
fig.text(.045,.951,'Where the WSW line crosses countries',fontsize=25,fontweight='bold',color='#18353f')
fig.text(.045,.912,'Great circle from the Alexanderplatz World Clock • initial true bearing 247.5°',fontsize=13.2,color='#48616b')
fig.text(.045,.882,'Orange: within mapped country polygons (including inland waters). Teal: outside those polygons.',fontsize=11,color='#48616b')
entries=[('1','EUROPE OUTBOUND','Germany → Belgium → France'),('2','AMAZON / BRAZIL','Marajó Island → mainland Brazil'),('3','ANDES / SOUTH AMERICA','Bolivia → Argentina → Chile'),('4','SOUTH PACIFIC','Open ocean; no Antarctic crossing'),('5','NEW ZEALAND','South Island → Tasman Sea'),('6','AUSTRALIA','Eastern mainland → Gulf of Carpentaria'),('7','INDONESIA','Western New Guinea and other islands'),('8','PHILIPPINES','Multiple islands, then South China Sea'),('9','CHINA','Southeast coast → western China'),('10','KAZAKHSTAN','Steppe and Kazakhstan–Russia border'),('11','RUSSIA / BELARUS','Russia → Belarus'),('12','EUROPE RETURN','Lithuania → Kaliningrad → Poland → Berlin')]
for i,(num,title,body) in enumerate(entries):
 col=i//4;row=i%4;x=.045+col*.31;y=.232-row*.043
 fig.text(x,y,num,ha='center',va='center',fontsize=10,color='white',fontweight='bold',bbox={'boxstyle':'circle,pad=.28','fc':'#ae4e26','ec':'none'})
 fig.text(x+.021,y+.006,title,fontsize=9.5,fontweight='bold',color='#233f48')
 fig.text(x+.021,y-.012,body,fontsize=9,color='#4d626b')
fig.text(.045,.032,'Conditional map result: spherical Earth, not a rhumb line. Boundary source: Natural Earth 1:10m country polygons, current not historical.',fontsize=8.5,color='#60717a')
fig.text(.045,.015,'No nearby city or monument points are plotted. Orange marks a dataset-polygon intersection, not a survey-level or building-level touch.',fontsize=8.5,color='#60717a')
fig.savefig(P/'Berlin-WSW-country-polygon-intersections.png',dpi=170,facecolor=fig.get_facecolor())
fig.savefig(P/'Berlin-WSW-country-polygon-intersections.svg',facecolor=fig.get_facecolor())
print(P/'Berlin-WSW-country-polygon-intersections.png')
