"""Offline source/selection verification. No web requests and no axis scoring."""
import gzip,hashlib,json
from collections import Counter
from pathlib import Path
from landmark_inventory import regional_sites,date_rows
ROOT=Path(__file__).resolve().parents[1]

def main():
    src=ROOT/'sources/landmark-axis';receipt=json.loads((src/'inventory-receipt.json').read_text());parts=json.loads((src/'region-parts.json').read_text())
    archive=b''
    for item in parts['parts']:
        b=(src/item['name']).read_bytes();assert hashlib.sha256(b).hexdigest()==item['sha256'];archive+=b
    assert hashlib.sha256(archive).hexdigest()==receipt['source_receipts_sha256']['official-region.geojson.gz']
    raw=gzip.decompress(archive);assert hashlib.sha256(raw).hexdigest()==receipt['region_sha256']
    inventory_path=ROOT/'data/landmark-axis/inventory.json.gz';assert hashlib.sha256(inventory_path.read_bytes()).hexdigest()==receipt['inventory_gzip_sha256']
    saved=json.loads(gzip.decompress(inventory_path.read_bytes()))['sites'];again,counts=regional_sites(json.loads(raw))
    assert [s['canonical_id'] for s in again]==[s['canonical_id'] for s in saved]
    assert all(a['polygons']==b['polygons'] and a['types']==b['types'] for a,b in zip(again,saved))
    records=json.loads(gzip.decompress((src/'record-excerpts.json.gz').read_bytes()));byid={r['id']:r for r in records}
    for record in records:
        if record['status']!='ok':continue
        table='<table><tr><td>Obj.-Dok.-Nr.</td><td>'+record['id']+'</td></tr>'+''.join(row['raw_html'] for row in record['primary_date_rows'])+'</table>'
        years,_,_=date_rows(table);assert years==record['accepted_latest_years']
    for s in saved:
        years=[y for i in s['ids'] if i in byid for y in byid[i].get('accepted_latest_years',[])]
        stratum='H1' if any(y<=1989 for y in years) else 'POST' if years and all(y>1989 for y in years) else 'U'
        assert stratum==s['stratum']
    result={'status':'passed','raw_region_features':counts['regional_features'],'same200canonical_sample_reproduced':True,'chronology_counts':dict(Counter(s['stratum'] for s in saved)),'date_rows_reparsed':len(records),'all_sourcepart_and_region_hashes_verified':True,'no_web_requests':True,'no_axis_scores_computed':True}
    (ROOT/'results/landmark-axis/OFFLINE-RECEIPT-CHECK.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
