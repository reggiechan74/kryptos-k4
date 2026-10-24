"""Static corrected-version archive checks; no handed-off JavaScript execution."""
import hashlib,json,zipfile
from pathlib import Path
from verify_projection_site_handoff import safe_members
ROOT=Path(__file__).resolve().parents[1];ARCHIVE=ROOT/'docs/site-source/projection-v17-20261024';OLD=ROOT/'docs/site-source/projection-20261024/snapshot'
def verify():
 data={};summary={}
 for filename,count in [('from-v16.zip',7),('full-feature.zip',31)]:
  p=ARCHIVE/filename
  with zipfile.ZipFile(p) as z:
   names=safe_members(z);m=json.loads(z.read('HANDOFF_MANIFEST.json'));paths={r['path'] for r in m['files']}
   if len(paths)!=count or names!=paths|{'HANDOFF_MANIFEST.json'} or m['version']!=17 or m['sourceCommit']!='2cb85a7714e12a627495f42dd3a7581c09b0b809':raise ValueError('incorrect version or manifest domain')
   data[filename]={r['path']:z.read(r['path']) for r in m['files']}
   for r in m['files']:
    raw=data[filename][r['path']]
    if len(raw)!=r['bytes'] or hashlib.sha256(raw).hexdigest()!=r['sha256']:raise ValueError('member integrity mismatch')
   if filename=='from-v16.zip':
    for n in names:
     if (ARCHIVE/'snapshot'/n).read_bytes()!=z.read(n):raise ValueError('delta snapshot changed')
   summary[filename]=dict(sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size,manifest_files=count,original_members=len(names))
 full,delta=data['full-feature.zip'],data['from-v16.zip']
 for path,raw in full.items():
  expected=delta[path] if path in delta else (OLD/path).read_bytes()
  if raw!=expected:raise ValueError('full feature differs from preserved baseline plus delta')
 expected={'PROJECTION_CONCURRENCE_QA.md','candidate/projection-test/module.mjs','candidate/qa/projection-mobile.html','dist/RELEASE_MANIFEST.json','dist/projection-test/module.mjs','dist/qa/projection-mobile.html','tests/projection-concurrence.test.mjs'}
 if set(delta)!=expected:raise ValueError('unexpected changed file')
 for side in ['candidate','dist']:
  html=delta[side+'/qa/projection-mobile.html'];module=delta[side+'/projection-test/module.mjs']
  if any(x not in html for x in [b'<meta charset="utf-8">',b'&middot;',b'&times;']):raise ValueError('encoding fix absent')
  if b'residual computed' not in module:raise ValueError('residual wording fix absent')
 if delta['candidate/projection-test/module.mjs']!=delta['dist/projection-test/module.mjs'] or delta['candidate/qa/projection-mobile.html']!=delta['dist/qa/projection-mobile.html']:raise ValueError('candidate/dist mismatch')
 for p in ['core.mjs','fixtures.mjs','synthetic.mjs','view.mjs','photo-provenance.json','loc-highsmith-site.jpg']:
  if full['candidate/projection-test/'+p]!=(OLD/'candidate/projection-test'/p).read_bytes():raise ValueError('scientific inputs/core changed')
 for n,path in [('projection-reference-results.json','PROJECTION-CONCURRENCE-029-SYNTHETIC.json'),('projection-local-reference.json','PROJECTION-CONCURRENCE-029-LOCAL-CONTROLS.json')]:
  if full['tests/'+n]!=(ROOT/'results'/path).read_bytes():raise ValueError('reference payload drift')
 return dict(archives=summary,changed_paths=sorted(delta),source_commit='2cb85a7714e12a627495f42dd3a7581c09b0b809',full_feature_equals_v16_plus_delta=True,numeric_core_fixtures_and_export_code_unchanged=True,encoding_and_residual_wording_verified=True,reference_payloads_unchanged=True,handed_off_JavaScript_executed=False,site_deployed_here=False)
if __name__=='__main__':print(json.dumps(verify(),indent=2))
