"""Publication integrity only: no source imports, proof replay or extraction."""
import hashlib,json,re,tarfile,unittest,zipfile
from pathlib import Path
D=Path(__file__).resolve().parents[1]/'research/method-pilots/fresh-residual-v2-incomplete'
class FreshResidualFailureArtifacts(unittest.TestCase):
 def test_archive_pins(self):
  for name,pin in json.loads((D/'ARCHIVE-RECEIPTS.json').read_text()).items():
   b=(D/name).read_bytes();self.assertEqual(len(b),pin['bytes']);self.assertEqual(hashlib.sha256(b).hexdigest(),pin['sha256'])
 def test_public_derivatives_and_scientific_invariance(self):
  rows=json.loads((D/'PUBLIC-PROVENANCE.json').read_text())['files']
  with zipfile.ZipFile(D/'noncertificate-evidence.zip') as z:
   self.assertEqual(set(z.namelist()),{x['path'] for x in rows if x['path']!='certificates.tar.gz'})
   for row in rows:
    b=(D/row['path']).read_bytes() if row['path']=='certificates.tar.gz' else z.read(row['path'])
    self.assertEqual(hashlib.sha256(b).hexdigest(),row['public_sha256']);self.assertEqual(len(b),row['public_bytes'])
    if row['path'].endswith('.py') or row['path'].startswith('runs/') or row['path']=='public/solver-input.json':self.assertEqual(row['original_sha256'],row['public_sha256'])
    if row['path']!='certificates.tar.gz':self.assertFalse(re.search(rb'page_[a-f0-9]{20,}|Responsibilities Page|/root/[A-Za-z_]|https://chatgpt.com/space/',b),row['path'])
 def test_certificate_stream_identity(self):
  rows=json.loads((D/'CERTIFICATE-PROVENANCE.json').read_text())['original_certificates'];wanted={r['member']:r for r in rows};seen=set();size=0
  with tarfile.open(D/'certificates.tar.gz','r|gz') as t:
   for m in t:
    self.assertTrue(m.isfile());self.assertIn(m.name,wanted);self.assertNotIn(m.name,seen);seen.add(m.name);size+=m.size;h=hashlib.sha256();f=t.extractfile(m)
    for b in iter(lambda:f.read(65536),b''):h.update(b)
    row=wanted[m.name];self.assertEqual(h.hexdigest(),row['sha256']);self.assertEqual(m.size,row['bytes'])
  self.assertEqual(len(seen),8);self.assertEqual(size,40699407)
 def test_failure_scope(self):
  s=(D/'README.md').read_text()
  for x in ('INCOMPLETE','Eight of 28','Twenty successors','4,153','not exact W','56.075505','design only','not a new fresh replication'):self.assertIn(x,s)
