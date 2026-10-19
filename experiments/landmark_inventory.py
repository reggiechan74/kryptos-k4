"""Independent fixed heritage-inventory acquisition; does not compute axis scores."""
import concurrent.futures
import gzip
import hashlib
from html import unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import time
import urllib.request
from landmark_geometry import ORIGIN,utm,bbox,area,contained,inside,support,segdist,segments
ROOT=Path(__file__).resolve().parents[1]

def save(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def digest(b):return hashlib.sha256(b).hexdigest()
class Text(HTMLParser):
    def __init__(self):super().__init__();self.parts=[]
    def handle_data(self,s):self.parts.append(s)
def clean(s):
    p=Text();p.feed(s);return ' '.join(' '.join(p.parts).split())
def date_rows(page):
    tables=re.findall(r'<table\b[^>]*>.*?</table>',page,re.S|re.I)
    main=next((t for t in tables if 'Obj.-Dok.-Nr.' in clean(t)),None)
    if main is None:return [],{},[]
    fields={};raw=[]
    for tr in re.findall(r'<tr\b[^>]*>.*?</tr>',main,re.S|re.I):
        cells=[clean(v) for v in re.findall(r'<t[dh]\b[^>]*>(.*?)</t[dh]>',tr,re.S|re.I)]
        if len(cells)>=2:
            label=cells[0].strip();value=' '.join(cells[1:]);fields.setdefault(label,[]).append(value)
            if label in ('Datierung','Fertigstellung'):raw.append({'label':label,'value':value,'raw_html':tr})
    dates=[]
    for row in raw:
        value=row['value'];years=re.findall(r'(?<!\d)(?:1\d{3}|20\d{2})(?!\d)',value)
        rem=re.sub(r'(?<!\d)(?:1\d{3}|20\d{2})(?!\d)','',value)
        if years and not re.sub(r'[\s,;:/\-–—.]','',rem):dates.append(max(map(int,years)))
    return dates,fields,raw

def regional_sites(region):
    groups={};origin=utm(*ORIGIN);excluded=[]
    for f in region['features']:
        prop=f['properties'];typ=prop['typ'];id0=prop['id'].split(',')[0][:8]
        if typ not in ('Baudenkmal','Gesamtanlage','Gartendenkmal'):continue
        geom=f['geometry'];polys=geom['coordinates'] if geom['type']=='MultiPolygon' else [geom['coordinates']]
        for rs in polys:
            if any(len(r)<4 or r[0]!=r[-1] for r in rs):raise ValueError('unclosed source ring '+id0)
        g=groups.setdefault(id0,{'ids':[id0],'types':set(),'polygons':[],'source_features':[],'links':{}});g['types'].add(typ);g['polygons'].extend(polys);g['source_features'].append(f['id']);g['links'][id0]=prop['link']
    candidates=[]
    for id0,g in groups.items():
        bb=bbox(g['polygons']);dx=max(bb[0]-origin[0],0,origin[0]-bb[2]);dy=max(bb[1]-origin[1],0,origin[1]-bb[3])
        if dx*dx+dy*dy>5010**2:continue
        if inside(origin,g['polygons']):excluded.append({'id':id0,'reason':'containsclockorigin'});continue
        # Conservative native disk filter; final radial clipping follows before sampling.
        if min(segdist(origin,a,b) for a,b in segments(g['polygons']))>5010:continue
        g['bbox']=bb;g['area_m2']=area(g['polygons']);candidates.append(g)
    n=len(candidates);parents=list(range(n))
    def find(i):
        while parents[i]!=i:parents[i]=parents[parents[i]];i=parents[i]
        return i
    containment_pairs=[]
    for i,a in enumerate(candidates):
        for j in range(i):
            b=candidates[j];large,small=(a,b) if a['area_m2']>=b['area_m2'] else (b,a);u,v=large['bbox'],small['bbox']
            if u[0]>v[0]+1e-7 or u[1]>v[1]+1e-7 or u[2]<v[2]-1e-7 or u[3]<v[3]-1e-7:continue
            if contained(small['polygons'],large['polygons']):
                parents[find(i)]=find(j);containment_pairs.append([a['ids'][0],b['ids'][0]])
    clusters={}
    for i,g in enumerate(candidates):
        key=find(i);c=clusters.setdefault(key,{'ids':[],'types':set(),'polygons':[],'links':{},'source_features':[]})
        for k in ('ids','polygons','source_features'):c[k].extend(g[k])
        c['types'].update(g['types']);c['links'].update(g['links'])
    for g in clusters.values():
        g['ids'].sort();g['types']=sorted(g['types']);g['canonical_id']=','.join(g['ids']);g['selection_hash']=digest(g['canonical_id'].encode())
    selected=[];tested=0
    for g in sorted(clusters.values(),key=lambda x:x['selection_hash']):
        intervals,_=support(g['polygons'],5);tested+=1
        if not intervals:continue
        # Do not retain or inspect orientation scores in inventory phase.
        selected.append(g)
        if len(selected)==200:break
    return selected,{'regional_features':len(region['features']),'rootgroups_before_disk':len(groups),'native_disk_candidates':n,'containment_pairs':containment_pairs,'canonicalclusters_before_precise_disk':len(clusters),'precise_disk_tests_before_sample_complete':tested,'selected':len(selected),'excluded_origin_sites':excluded}

def fetch_record(item):
    id0,url=item;started=time.monotonic()
    try:
        with urllib.request.urlopen(url,timeout=15) as response:b=response.read()
        page=b.decode('utf-8',errors='replace');dates,fields,raw=date_rows(page)
        title=re.findall(r'<h2\b[^>]*>(.*?)</h2>',page,re.S|re.I)
        return {'id':id0,'url':url,'status':'ok','full_response_sha256':digest(b),'full_response_bytes':len(b),'primary_date_rows':raw,'accepted_latest_years':dates,'category':fields.get('Sachbegriff',[]),'title':clean(title[0]) if title else '', 'elapsed_seconds':round(time.monotonic()-started,3)}
    except Exception as e:return {'id':id0,'url':url,'status':'error','error':type(e).__name__+': '+str(e),'elapsed_seconds':round(time.monotonic()-started,3)}

def main():
    begun=time.monotonic();raw=Path('/tmp/align-denkmale-region.geojson').read_bytes();region=json.loads(raw)
    assert region['numberMatched']==region['numberReturned']==len(region['features']) and not any(l.get('rel')=='next' for l in region.get('links',[]))
    assert region['crs']['properties']['name'].endswith('25833')
    sites,receipt=regional_sites(region);print('inventory selected',len(sites),'in',round(time.monotonic()-begun,2),'s',flush=True)
    first=[(g['ids'][0],g['links'][g['ids'][0]]) for g in sites];rest=[(id0,g['links'][id0]) for g in sites for id0 in g['ids'][1:]];items=list(dict(first+rest).items())[:250]
    records=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for r in pool.map(fetch_record,items):records.append(r)
    byid={r['id']:r for r in records}
    for g in sites:
        g['metadata_ids_fetched']=[i for i in g['ids'] if i in byid]
        years=[y for i in g['ids'] if i in byid for y in byid[i].get('accepted_latest_years',[])]
        g['accepted_primary_years']=years
        g['stratum']='H1' if any(y<=1989 for y in years) else 'POST' if years and all(y>1989 for y in years) else 'U'
        categories=[v for i in g['ids'] if i in byid for v in byid[i].get('category',[])]
        g['official_subject_categories']=categories
        types=set(g['types'])
        g['count_class']='mixed_complex' if len(types)>1 else 'garden_grounds' if 'Gartendenkmal' in types else 'institutional_complex' if 'Gesamtanlage' in types else 'compact_monument' if any(re.search(r'Denkmal|Standbild|Skulptur|Brunnen',c) for c in categories) else 'built_footprint'
    dest=ROOT/'data/landmark-axis';sources=ROOT/'sources/landmark-axis'
    dest.mkdir(exist_ok=True);sources.mkdir(exist_ok=True)
    (sources/'official-region.geojson.gz').write_bytes(gzip.compress(raw,mtime=0))
    for f in ('capabilities.xml','schema'):
        b=Path('/tmp/align-denkmale-'+f).read_bytes();(sources/('official-'+f+'.gz')).write_bytes(gzip.compress(b,mtime=0))
    payload=json.dumps({'sites':sites},ensure_ascii=False,separators=(',',':')).encode();(dest/'inventory.json.gz').write_bytes(gzip.compress(payload,mtime=0))
    (sources/'record-excerpts.json.gz').write_bytes(gzip.compress(json.dumps(records,ensure_ascii=False,separators=(',',':')).encode(),mtime=0))
    receipt.update({'region_url':Path('/tmp/align-denkmale-region-url.txt').read_text(),'region_timestamp':region.get('timeStamp'),'region_sha256':digest(raw),'metadata_pages_requested':len(items),'metadata_ok':sum(r['status']=='ok' for r in records),'chronology_counts':{k:sum(s['stratum']==k for s in sites) for k in ['H0','H1','U','POST']},'H0_verified_historical_outlines':0,'sample_selection':'SHA256(sortedrootIDs)first200preciselydiskeligiblecanonicalsites; no angledependentselection','elapsed_seconds':round(time.monotonic()-begun,3),'source_date_rule':'strict literal primary Fertigstellung/Datierung completed date; no Entwurf-only existence','raw_page_policy':'Retain fullresponsehash/URL/bytes and exact primarydate HTMLrows; full navigational/contact pagebody notpublished','source_receipts_sha256':{p.name:digest(p.read_bytes()) for p in sources.iterdir() if p.is_file()},'inventory_gzip_sha256':digest((dest/'inventory.json.gz').read_bytes())})
    save(sources/'inventory-receipt.json',receipt);print(json.dumps({k:receipt[k] for k in ['selected','metadata_pages_requested','metadata_ok','chronology_counts','elapsed_seconds']}),flush=True)
if __name__=='__main__':main()
