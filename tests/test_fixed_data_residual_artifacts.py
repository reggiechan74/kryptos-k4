"""Static package checks only; no solver import, truth analysis or extraction."""
import hashlib,json,re,tarfile,unittest,zipfile,io
from pathlib import Path
D=Path(__file__).resolve().parents[1]/'research/method-pilots/fixed-data-residual-v1'
class PartStream(io.RawIOBase):
 def __init__(self):
  self.paths=iter(json.loads((D/'ARCHIVE-PARTS.json').read_text())['parts_in_order']);self.f=None
 def readable(self):return True
 def readinto(self,b):
  while True:
   if self.f is None:
    try:self.f=(D/next(self.paths)['path']).open('rb')
    except StopIteration:return 0
   n=self.f.readinto(b)
   if n:return n
   self.f.close();self.f=None
 def close(self):
  if self.f:self.f.close()
  super().close()
def original_digest():
 h=hashlib.sha256();n=0
 with io.BufferedReader(PartStream()) as f:
  for b in iter(lambda:f.read(65536),b''):h.update(b);n+=len(b)
 return n,h.hexdigest()
class FixedDataResidualArtifacts(unittest.TestCase):
 def test_archive_identity(self):
  for name,pin in json.loads((D/'ARCHIVE-RECEIPTS.json').read_text()).items():

   if name=='certificates.tar.gz':n,h=original_digest()
   else:b=(D/name).read_bytes();n,h=len(b),hashlib.sha256(b).hexdigest()
   self.assertEqual(n,pin['bytes']);self.assertEqual(h,pin['sha256'])
 def test_exact_reviewed_public_transfer(self):
  rows=json.loads((D/'PACKAGE-TRANSFER.json').read_text())['files'];self.assertEqual(len(rows),199)
  with zipfile.ZipFile(D/'noncertificate-evidence.zip') as z:
   self.assertEqual(set(z.namelist()),{x['path'] for x in rows if x['path']!='certificates.tar.gz'})
   for row in rows:
    if row['path']=='certificates.tar.gz':
     n,h=original_digest();self.assertEqual(n,row['bytes']);self.assertEqual(h,row['sha256']);continue
    b=z.read(row['path']);self.assertEqual(hashlib.sha256(b).hexdigest(),row['sha256']);self.assertEqual(len(b),row['bytes'])
    if row['path']!='certificates.tar.gz':self.assertFalse(re.search(rb'page_[a-f0-9]{20,}|Responsibilities Page|/root/[A-Za-z_]|https://chatgpt.com/space/',b),row['path'])
   mirrors={'README.md':'RESULTS.md','SOURCE-PROVENANCE.json':'SOURCE-PROVENANCE.json','CERTIFICATE-PROVENANCE.json':'CERTIFICATE-PROVENANCE.json','RELEASE-AND-SCOPE.json':'RELEASE-AND-SCOPE.json','closeout/ANALYSIS.json':'ANALYSIS.json','closeout/COMBINED-RESOURCE-ACCOUNTING.sanitized.json':'RESOURCE-ACCOUNTING.sanitized.json','reviews/final/REVIEW.sanitized.md':'FINAL-REVIEW.sanitized.md'}
   for source,target in mirrors.items():self.assertEqual(z.read(source),(D/target).read_bytes())
 def test_certificate_stream_identity(self):
  p=json.loads((D/'CERTIFICATE-PROVENANCE.json').read_text());wanted={r['member']:r for r in p['members']};seen=set();total=0
  with io.BufferedReader(PartStream()) as parts, tarfile.open(fileobj=parts,mode='r|gz') as t:
   for m in t:
    self.assertTrue(m.isfile());self.assertIn(m.name,wanted);self.assertNotIn(m.name,seen);seen.add(m.name);total+=m.size;h=hashlib.sha256();f=t.extractfile(m)
    for b in iter(lambda:f.read(65536),b''):h.update(b)
    self.assertEqual(h.hexdigest(),wanted[m.name]['sha256']);self.assertEqual(m.size,wanted[m.name]['bytes'])
  self.assertEqual(len(seen),28);self.assertEqual(total,241621080)
 def test_summary_keeps_scope(self):
  s=(D/'README.md').read_text()
  for x in ('not a fresh replication','791','not necessarily a singleton','50 canonical','13','294.313402','INCOMPLETE','No mocks, actual controls or K4 target arithmetic/run'):self.assertIn(x,s)
