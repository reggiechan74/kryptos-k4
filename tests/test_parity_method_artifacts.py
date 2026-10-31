"""Static validation of published evidence only; never executes solvers."""
import hashlib,json,re,tarfile,unittest
from pathlib import Path
D=Path(__file__).resolve().parents[1]/'research/method-pilots/parity-first-v2'
class ParityMethodArtifacts(unittest.TestCase):
 def test_archive_provenance(self):
  receipt=json.loads((D/'ARCHIVE-RECEIPT.json').read_text());a=D/receipt['archive'];self.assertEqual(hashlib.sha256(a.read_bytes()).hexdigest(),receipt['sha256']);self.assertEqual(a.stat().st_size,receipt['bytes'])
  with tarfile.open(a) as t:
   files={m.name.removeprefix('./'):t.extractfile(m).read() for m in t.getmembers() if m.isfile()}
   # The archive uses a single named root directory.
   if 'PROVENANCE.json' not in files:files={k.split('/',1)[1]:v for k,v in files.items()}
   p=json.loads(files['PROVENANCE.json']);self.assertEqual(p,json.loads((D/'PROVENANCE.json').read_text()));self.assertEqual(len(p['entries']),679)
   for e in p['entries']:
    self.assertEqual(hashlib.sha256(files[e['public_path']]).hexdigest(),e['public_sha256'])
    if e['action'] in ('exact_copy','relocated_exact_copy'):self.assertEqual(e['original_sha256'],e['public_sha256'])
   for k,v in files.items():self.assertFalse(re.search(rb'page_[a-f0-9]{20,}|Responsibilities Page|/workspace/|/root/[A-Za-z_]',v),k)
 def test_retained_summary(self):
  a=json.loads((D/'validation-analysis.json').read_text());s=a['summary'];self.assertEqual((s['cases'],s['stages'],s['parity_faster'],s['parity_slower']),(40,240,38,2));self.assertEqual((s['in_family_cases'],s['in_family_forced'],s['in_family_false_forced'],s['in_family_all_unknown_forced']),(32,2103,0,27));self.assertTrue(s['exact_masks_agree_all_repeats'])
  for method in ('crt','parity'):self.assertAlmostEqual(sum(c['methods'][method]['median_cpu'] for c in a['cases']),s['methods'][method]['sum_case_median_cpu'])
 def test_resource_no_double_count(self):
  a=json.loads((D/'RESOURCE-SUMMARY.json').read_text());self.assertAlmostEqual(sum(r['cpu'] for r in a['receipts']),a['cpu_seconds']);self.assertAlmostEqual(a['cpu_seconds'],148.455768)
 def test_limits(self):
  s=(D/'README.md').read_text()
  for text in ('not 40 independent random draws','First six','26.6%','13.6%','46.9%','same','not a K4 result','from validation/'):self.assertIn(text.lower(),s.lower())
