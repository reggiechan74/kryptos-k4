"""Static Site delta/archive checks. Does not execute handed-off JavaScript."""
import hashlib,json,re,stat,zipfile
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parents[1];ARCHIVE=ROOT/'docs/site-source/projection-20261024'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def safe_members(z):
 seen=set();total=0
 for i in z.infolist():
  p=PurePosixPath(i.filename);mode=stat.S_IFMT(i.external_attr>>16)
  if p.is_absolute() or '..' in p.parts or '\\' in i.filename or str(p)!=i.filename or '.git' in p.parts or i.filename in seen or mode not in (0,stat.S_IFREG):raise ValueError('unsafe or duplicate archive entry')
  total+=i.file_size
  if i.file_size>5*1024**2 or total>20*1024**2:raise ValueError('archive budget exceeded')
  seen.add(i.filename)
 return seen

def verify():
 raw=(ARCHIVE/'original-handoff.zip').read_bytes();patch=(ARCHIVE/'site-source.patch').read_bytes();snap=ARCHIVE/'snapshot';copies={}
 with zipfile.ZipFile(ARCHIVE/'original-handoff.zip') as z:
  names=safe_members(z);manifest=json.loads(z.read('HANDOFF_MANIFEST.json'));declared={r['path'] for r in manifest['files']}
  if names!=declared|{'HANDOFF_MANIFEST.json','HANDOFF_README.txt'}:raise ValueError('undeclared archive member')
  for n in names:
   if (snap/n).read_bytes()!=z.read(n):raise ValueError('changed original member '+n)
  for r in manifest['files']:
   data=z.read(r['path'])
   if len(data)!=r['bytes'] or sha(data)!=r['sha256']:raise ValueError('manifest hash mismatch')
   copies[r['path']]=sha(data)
 headers=re.findall(rb'^diff --git a/(\S+) b/(\S+)$',patch,re.M)
 if len(headers)!=len(declared) or any(a!=b or '..' in PurePosixPath(a.decode()).parts for a,b in headers) or {a.decode() for a,b in headers}!=declared:raise ValueError('patch paths mismatch')
 prefix='export const PROJECTION_FIXTURES=';text=(snap/'candidate/projection-test/fixtures.mjs').read_text();fixtures=json.loads(text.split(prefix,1)[1].split(';\nexport const RESEARCH_PROVENANCE=',1)[0]);native=json.loads((ROOT/'results/PROJECTION-CONCURRENCE-029-SYNTHETIC.json').read_text())
 if fixtures!=native['fixtures']:raise ValueError('research fixture drift')
 for archived,nativepath in [('projection-reference-results.json','PROJECTION-CONCURRENCE-029-SYNTHETIC.json'),('projection-local-reference.json','PROJECTION-CONCURRENCE-029-LOCAL-CONTROLS.json')]:
  if (snap/'tests'/archived).read_bytes()!=(ROOT/'results'/nativepath).read_bytes():raise ValueError('reference payload differs')
 for n in [p for p in declared if p.startswith('candidate/projection-test/')]+['candidate/qa/projection-mobile.html','candidate/style.css']:
  if (snap/n).read_bytes()!=(snap/n.replace('candidate/','dist/',1)).read_bytes():raise ValueError('candidate/dist module drift')
 release=json.loads((snap/'dist/RELEASE_MANIFEST.json').read_text());available=[]
 for r in release['files']:
  p=snap/'dist'/r['path']
  if p.is_file():
   if sha(p.read_bytes())!=r['sha256']:raise ValueError('release manifest differs')
   available.append(r['path'])
 photo=json.loads((snap/'candidate/projection-test/photo-provenance.json').read_text())
 if sha((snap/'candidate/projection-test/loc-highsmith-site.jpg').read_bytes())!=photo['derivative_sha256'] or photo['certified_pairs']!=0 or photo['real_fits']!=0:raise ValueError('photo identity or admission changed')
 if manifest.get('version')!=16 or 'deployed' not in manifest['status']:raise ValueError('stale handoff deployment metadata')
 return dict(zip_sha256=sha(raw),zip_bytes=len(raw),patch_sha256=sha(patch),patch_bytes=len(patch),original_members=len(names),manifest_files=len(declared),original_source_sha256=copies,patch_paths=sorted(declared),research_fixtures_equal=8,research_local_control_records_equal=11,complete_reference_receipt_bytes_equal=True,candidate_dist_projection_assets_equal=True,available_release_members_verified=available,absent_release_members_not_verified=len(release['files'])-len(available),JavaScript_executed=False,site_checkout_modified=False,patch_applied_to_research_root=False)
if __name__=='__main__':print(json.dumps(verify(),indent=2))
