"""Static package checks; do not execute mathematical or target experiments."""
import hashlib,json,re,unittest,zipfile
from pathlib import Path
D=Path(__file__).resolve().parents[1]/'research/method-pilots/filtered-affine-v1'
class FilteredAffineArtifacts(unittest.TestCase):
 def test_archive_and_public_map(self):
  receipt=json.loads((D/'ARCHIVE-RECEIPT.json').read_text());a=D/receipt['archive'];self.assertEqual(hashlib.sha256(a.read_bytes()).hexdigest(),receipt['sha256']);self.assertEqual(a.stat().st_size,receipt['bytes'])
  with zipfile.ZipFile(a) as z:
   m=json.loads(z.read('PUBLIC-PROVENANCE.json'));self.assertEqual(m,json.loads((D/'PUBLIC-PROVENANCE.json').read_text()));self.assertEqual(len(z.namelist()),len(m['files'])+1)
   self.assertEqual(len(m['omitted']),7)
   for e in m['files']:
    b=z.read(e['path']);self.assertEqual(len(b),e['bytes']);self.assertEqual(hashlib.sha256(b).hexdigest(),e['public_sha256'])
    if e['byte_identical']:self.assertEqual(e['original_sha256'],e['public_sha256'])
    if e['path'].endswith('.py'):self.assertTrue(e['byte_identical'])
   self.assertFalse(any('/private-sources/' in n for n in z.namelist()))
 def test_retained_audit_numbers(self):
  with zipfile.ZipFile(D/'proof-module-and-source-evidence.zip') as z:
   for name in ('result.json','result-optimized.json'):
    x=json.loads(z.read('filtered-affine-hardened-independent-review/'+name));self.assertEqual(x['status'],'PASS');self.assertEqual((x['valid_cases'],x['witnesses'],x['malformed_rejections'],x['budget_checks'],x['tamper_rejections']),(10931,95713,46,74,8));self.assertEqual(sum(x['coverage'].values()),10931)
 def test_privacy(self):
  with zipfile.ZipFile(D/'proof-module-and-source-evidence.zip') as z:
   for n in z.namelist():self.assertFalse(re.search(rb'page_[a-f0-9]{20,}|Responsibilities Page|/root/[A-Za-z_]|https://chatgpt.com/space/',z.read(n)),n)
 def test_scope_limits(self):
  s=(D/'README.md').read_text()
  for text in ('unsafe as a reusable API','INCOMPLETE','156','unresolved','not target exclusion','prime-field','seven third-party'):self.assertIn(text.lower(),s.lower())
