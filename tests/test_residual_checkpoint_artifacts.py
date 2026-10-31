"""Static archive and derivative provenance; no scientific execution/import."""
import hashlib,json,re,tarfile,unittest
from pathlib import Path
D=Path(__file__).resolve().parents[1]/'research/method-pilots/canonical-residual-checkpoint'
class ResidualCheckpointArtifacts(unittest.TestCase):
 def test_archive_and_manifest(self):
  r=json.loads((D/'ORIGINAL-ARCHIVE-RECEIPT.json').read_text());a=D/r['archive_name'];self.assertEqual(a.stat().st_size,r['archive_bytes']);self.assertEqual(hashlib.sha256(a.read_bytes()).hexdigest(),r['archive_sha256']);manifest=json.loads((D/'MANIFEST.json').read_text());want={e['path']:e for e in manifest['files']}
  with tarfile.open(a) as t:
   members=[m for m in t.getmembers() if m.isfile()];self.assertEqual(len(members),1675)
   for m in members:
    name=m.name.split('/',1)[1];b=t.extractfile(m).read()
    if name in want:self.assertEqual(hashlib.sha256(b).hexdigest(),want[name]['sha256']);self.assertEqual(len(b),want[name]['bytes'])
    self.assertFalse(re.search(rb'page_[a-f0-9]{20,}|Responsibilities Page|https://chatgpt.com/space/|/workspace/shared/|/root/[A-Za-z_]',b),name)
 def test_payload_map_and_core_pins(self):
  p=json.loads((D/'PROVENANCE.json').read_text());self.assertEqual(len(p['entries']),1665)
  exact=sum(e['source_sha256']==e['public_sha256'] for e in p['entries']);self.assertEqual(exact,1124)
  roots={e['source_root'] for e in p['entries']};self.assertEqual(len(roots),15)
  for bad in ('residual-validation-custody','residual-validation-run-records'):self.assertNotIn(bad,roots)
  rows={e['public_path']:e for e in p['entries']}
  for path in ('canonical-residual-dev/residual_decoder.py','canonical-residual-reference-v2/reference.py','canonical-residual-reference-v3/reference_v3.py'):
   matches=[e for e in p['entries'] if e['source_root']==path.split('/')[0] and e['source_relative_path']==path.split('/',1)[1]]
   self.assertEqual(len(matches),1);self.assertEqual(matches[0]['source_sha256'],matches[0]['public_sha256'])
 def test_outer_report_provenance(self):
  p=json.loads((D/'TOPLEVEL-PROVENANCE.json').read_text());self.assertEqual(hashlib.sha256((D/'RESULTS.md').read_bytes()).hexdigest(),p['navigation_copy_sha256'])
  with tarfile.open(D/'canonical-residual-method-development.tar.gz') as t:
   b=t.extractfile('canonical-residual-method-development/RESULTS.md').read();self.assertEqual(hashlib.sha256(b).hexdigest(),p['source_report_sha256'])
 def test_failure_and_development_distinct(self):
  s=(D/'README.md').read_text()
  for x in ('Permanently INCOMPLETE','23 accepted','72 jobs','47.947867','82-second','1,393','3,060,421','2,000,000','42 disclosed','25 exact nonempty / 17 empty','not frozen-original','No failed-cohort seed','design review'):self.assertIn(x,s)
