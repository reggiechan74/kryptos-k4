"""Write bounded result artifacts and exact code/input metadata, offline."""
import gzip
import hashlib
import json
from pathlib import Path
import platform
import time
from bounded_models import ROOT, synthetic_controls, route_scan, running_scan, trifid_scan


def main():
    inputs=['data/k4.json','data/controls.json','experiments/run_bounded.py',
            'experiments/bounded_models.py','experiments/ciphers.py','experiments/structural_checks.py']
    hashes={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in inputs}
    data=json.loads((ROOT/'data/k4.json').read_text())
    controls=json.loads((ROOT/'data/controls.json').read_text())
    synthetic=synthetic_controls()
    tasks=[('ROUTE-001',lambda:route_scan(data)),('RUNKEY-001',lambda:running_scan(data,controls)),('TRIFID-001',lambda:trifid_scan(data))]
    for name,action in tasks:
        started=time.monotonic();result=action()
        result['run_metadata']={'status':'completed','date_utc':'2026-10-18','python':platform.python_version(),
            'command':'python3 experiments/run_bounded.py','elapsed_seconds':round(time.monotonic()-started,3),
            'file_sha256':hashes,'synthetic_controls':synthetic}
        encoded=(json.dumps(result,separators=(',',':'))+'\n').encode()
        if name=='ROUTE-001':
            (ROOT/'results/ROUTE-001.json.gz').write_bytes(gzip.compress(encoded,mtime=0))
            summary={k:v for k,v in result.items() if k not in ['route_catalogue','survivors']}
            summary['compatible_periods']=sorted({r['period'] for r in result['survivors']})
            summary['compatible_route_ids']=sorted({r['route'] for r in result['survivors']})
            summary['detail_artifact']='ROUTE-001.json.gz'
            summary['detail_uncompressed_sha256']=hashlib.sha256(encoded).hexdigest()
            (ROOT/'results/ROUTE-001-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
        else:(ROOT/('results/'+name+'.json')).write_bytes(encoded)
        print(name,'models',result['tested_models'],'survivors',len(result['survivors']),'seconds',result['run_metadata']['elapsed_seconds'])


if __name__=='__main__':main()
