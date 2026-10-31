"""Static retained-evidence checks, not solver or holdout execution."""
import hashlib,json,re,unittest,zipfile
from pathlib import Path
D=Path(__file__).resolve().parents[1]/'research/method-pilots/projection-saturation-v3'
class SaturationMethodArtifacts(unittest.TestCase):
 def test_archive_provenance(self):
  r=json.loads((D/'ARCHIVE-RECEIPT.json').read_text());p=D/r['archive'];self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),r['sha256']);self.assertEqual(p.stat().st_size,r['bytes'])
  with zipfile.ZipFile(p) as z:
   m=json.loads(z.read('PUBLIC-PROVENANCE.json'));self.assertEqual(m,json.loads((D/'PUBLIC-PROVENANCE.json').read_text()));self.assertEqual(len(z.namelist()),1013)
   self.assertEqual(sum(not e['byte_identical'] for e in m['files']),4)
   for e in m['files']:
    data=z.read(e['path']);self.assertEqual(hashlib.sha256(data).hexdigest(),e['public_sha256']);self.assertEqual(len(data),e['bytes'])
    if e['byte_identical']:self.assertEqual(e['original_sha256'],e['public_sha256'])
    else:self.assertTrue(e['path'].endswith('.md'))
   self.assertEqual(hashlib.sha256(z.read(m['source_map_copy'])).hexdigest(),m['source_map_copy_sha256'])
 def test_private_metadata_absent(self):
  with zipfile.ZipFile(D/'completed-synthetic-evidence.zip') as z:
   for name in z.namelist():self.assertFalse(re.search(rb'page_[a-f0-9]{20,}|Responsibilities Page|/root/[A-Za-z_]|https://chatgpt.com/space/',z.read(name)),name)
 def test_summary_limits(self):
  s=(D/'README.md').read_text()
  for x in ('480','47,412','78','24.405472','13.323356','16.280120','9.048368','79.65%','35.40%','488.783194','default-off','no failed residual-cohort seed or truth'):self.assertIn(x,s)
 def test_reports_equal_archive(self):
  with zipfile.ZipFile(D/'completed-synthetic-evidence.zip') as z:
   for target,source in [('RESULTS.md','validation/REPORT.md'),('CONDITIONAL-MASKS.md','validation/CONDITIONAL-MASKS.md'),('INDEPENDENT-RELEASE-REVIEW.md','release-review/REPORT.md'),('RESOURCE-ACCOUNTING.json','validation/RESOURCE-ACCOUNTING.json')]:self.assertEqual((D/target).read_bytes(),z.read(source))
