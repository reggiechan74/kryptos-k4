"""Static archive verification only: parse patch/data; never execute handed-off JS."""
import hashlib,json,re
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parents[1];ARCHIVE=ROOT/'docs/site-source/manual-overlay-v15'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def patch_members(raw):
 new={};paths=[];blobs={}
 for block in raw.decode().split('diff --git ')[1:]:
  header=block.splitlines()[0];m=re.fullmatch(r'a/(\S+) b/(\S+)',header)
  if not m or m[1]!=m[2]:raise ValueError('unsupported/renamed patch path')
  path=PurePosixPath(m[1])
  if path.is_absolute() or '..' in path.parts:raise ValueError('unsafe patch path')
  paths.append(str(path));prefix=block.split('@@',1)[0]
  if 'new file mode' in prefix:
   if 'new file mode 100644' not in prefix:raise ValueError('unsupported new file mode')
   body=''.join(line[1:]+'\n' for line in block.splitlines() if line.startswith('+') and not line.startswith('+++')).encode();new[str(path)]=body
   index=re.search(r'index 0+\.\.([0-9a-f]+)',prefix)
   if not index:raise ValueError('missing new-file blob ID')
   blob=hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()
   if not blob.startswith(index[1]):raise ValueError('new file does not match patch blob')
   blobs[str(path)]=blob
 if len(paths)!=len(set(paths)):raise ValueError('duplicate patch paths')
 return paths,new,blobs

def verify():
 raw=(ARCHIVE/'site-source.patch').read_bytes();paths,new,blobs=patch_members(raw);copies={}
 for name in ('core.mjs','data.mjs','module.mjs','view.mjs'):
  if new['candidate/fold-overlay/'+name]!=new['dist/fold-overlay/'+name]:raise ValueError('candidate/dist drift')
  copies['source/'+name]=new['dist/fold-overlay/'+name]
 copies.update({'ORIGINAL-HANDOFF.md':new['FOLD_OVERLAY_HANDOFF.md'],'original-tests/fold-overlay.test.mjs':new['tests/fold-overlay.test.mjs'],'original-tests/fold-offline-records.json':new['tests/fold-offline-records.json'],'qa/fold-overlay.html':new['qa/fold-overlay.html']})
 for path,content in copies.items():
  if (ARCHIVE/path).read_bytes()!=content:raise ValueError('archive copy differs '+path)
 text=copies['source/data.mjs'].decode();prefix='export const FOLD_DATA='
 if not text.startswith(prefix) or not text.rstrip().endswith(';'):raise ValueError('unexpected data serialization')
 data=json.loads(text[len(prefix):].rstrip()[:-1])
 if data['input']!=json.loads((ROOT/'data/monument-slide-input-v2.json').read_text()):raise ValueError('changed input')
 if data['glyphs']!=json.loads((ROOT/'data/fold-aperture-surrogate-v1.json').read_text())['glyph_rows']:raise ValueError('changed masks')
 if data['sourceArtifactSHA256']!=sha((ROOT/'research/figures/fold-slide-020.html').read_bytes()):raise ValueError('changed source HTML')
 release=raw.decode().split('diff --git a/dist/RELEASE_MANIFEST.json b/dist/RELEASE_MANIFEST.json',1)[1].split('diff --git ',1)[0]
 declared=dict(re.findall(r'^\+\s+"path": "([^"]+)",\n\+\s+"sha256": "([a-f0-9]{64})"',release,re.M))
 if len(declared)!=7 or any(sha(new['dist/'+p])!=h for p,h in declared.items()):raise ValueError('release manifest new-module hash mismatch')
 records=json.loads(copies['original-tests/fold-offline-records.json']);native={r['id']:r for r in json.loads((ROOT/'results/FOLD-SLIDE-020-actual.json').read_text())['records']}
 if len(records)!=134:raise ValueError('incomplete column oracle')
 for r in records:
  expected=native[r['model']+':'+str(r['shift'])]
  if any(expected[k]!=v for k,v in r.items()):raise ValueError('column oracle mismatch')
 return dict(patch_bytes=len(raw),patch_sha256=sha(raw),patch_paths=paths,new_git_blobs=blobs,new_release_hashes=declared,archived_member_sha256={k:sha(v) for k,v in copies.items()},input_identical=True,glyphs_identical=True,offline_column_records_equal=134,source_artifact_sha256=data['sourceArtifactSHA256'],research_source_commit=data['researchSourceCommit'],handed_off_JavaScript_executed=False,rows_statistically_scanned=False)
if __name__=='__main__':print(json.dumps(verify(),indent=2))
