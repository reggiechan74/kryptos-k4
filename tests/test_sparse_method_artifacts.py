"""Static artifact verification only: no solver, target or benchmark execution."""
import gzip,hashlib,json,re,unittest,zipfile
from pathlib import Path
D=Path(__file__).resolve().parents[1]/'research/method-pilots/sparse-law-v1'
class SparseMethodArtifacts(unittest.TestCase):
 def test_archive_and_provenance(self):
  receipt=json.loads((D/'ARCHIVE-RECEIPT.json').read_text());p=D/receipt['archive']
  self.assertEqual(receipt['sha256'],hashlib.sha256(p.read_bytes()).hexdigest());self.assertEqual(receipt['bytes'],p.stat().st_size)
  with zipfile.ZipFile(p) as z:
   manifest=json.loads(z.read('PUBLIC-PROVENANCE.json'));self.assertEqual(manifest,json.loads((D/'PUBLIC-PROVENANCE.json').read_text()))
   self.assertEqual(len(z.namelist()),len(manifest['files'])+1)
   for row in manifest['files']:
    b=z.read(row['path']);self.assertEqual(row['bytes'],len(b));self.assertEqual(row['public_sha256'],hashlib.sha256(b).hexdigest())
    if row['byte_identical']:self.assertEqual(row['original_sha256'],row['public_sha256'])
    else:self.assertTrue(row['path'].endswith('.md'));self.assertTrue(row['reason'])
 def test_public_privacy(self):
  with zipfile.ZipFile(D/'synthetic-pilot-and-future-design-evidence.zip') as z:
   for name in z.namelist():
    b=z.read(name)
    if name.endswith('.gz'):b=gzip.decompress(b)
    self.assertFalse(re.search(rb'page_[a-f0-9]{20,}|Responsibilities Page|/root/[A-Za-z_]|https://[^\s"<>]*(?:chatgpt\.com|notion\.so)',b,re.I),name)
 def test_public_reports_equal_sanitized_archive(self):
  with zipfile.ZipFile(D/'synthetic-pilot-and-future-design-evidence.zip') as z:
   for public,source in [('RESULTS.md','sparse-law-blind40/BLIND-REPORT.md'),('FUTURE-QUOTIENT-DESIGN.md','k4-function-quotient-audit/REPORT.md'),('FUTURE-PARITY-FIRST-DESIGN.md','k4-parity-first-v2-design/REPORT.md')]:self.assertEqual((D/public).read_bytes(),z.read(source))
 def test_scope_and_workload_disclosures(self):
  s=(D/'README.md').read_text()
  for token in ['1,510','1,876','219','33/40','49.322','66.554','factorized','first six','misspecified']:self.assertIn(token,s)
  for p in D.glob('FUTURE-*.md'):self.assertIn('Future design / toy mathematical checks only',p.read_text())
