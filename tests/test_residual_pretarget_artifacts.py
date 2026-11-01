"""Static reviewed-byte, family-retention and UNRUN checks; no scientific imports."""
import hashlib,json,re,tarfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'research/residual-pretarget-v1'
class ResidualPretargetArtifacts(unittest.TestCase):
 def test_reviewed_package_unchanged(self):
  manifest=json.loads((D/'REVIEWED-PACKAGE-MANIFEST.json').read_text());self.assertEqual(manifest['file_count'],72)
  derivatives={x['path']:x for x in json.loads((D/'REPOSITORY-DERIVATIVES.json').read_text())['files']}
  for original in manifest['files']:
   row=dict(original)
   if row['path'] in derivatives:
    d=derivatives[row['path']];self.assertEqual(row['sha256'],d['original_sha256']);row.update(bytes=d['public_bytes'],sha256=d['public_sha256'])
   b=(D/row['path']).read_bytes();self.assertEqual(len(b),row['bytes']);self.assertEqual(hashlib.sha256(b).hexdigest(),row['sha256'])
   if not row['path'].endswith('.gz'):self.assertFalse(re.search(rb'page_[a-f0-9]{20,}|Responsibilities Page|/root/[A-Za-z_]|https://chatgpt.com/space/',b),row['path'])
 def test_control_archive_stream(self):
  p=json.loads((D/'CERTIFICATE-PROVENANCE.json').read_text());seen=set();rows={x['member']:x for x in p['members']}
  with tarfile.open(D/p['archive']['path'],'r|gz') as t:
   for m in t:
    self.assertTrue(m.isfile());self.assertIn(m.name,rows);self.assertNotIn(m.name,seen);seen.add(m.name);h=hashlib.sha256();f=t.extractfile(m)
    for b in iter(lambda:f.read(65536),b''):h.update(b)
    self.assertEqual(h.hexdigest(),rows[m.name]['original_sha256']);self.assertEqual(m.size,rows[m.name]['original_bytes'])
  self.assertEqual(len(seen),2)
 def test_original68_and_one_pending_family(self):
  s=(ROOT/'research/HYPOTHESES.md').read_text();records=dict(re.findall(r'^### (H-[^\n]+)\n(.*?)(?=^### H-|<!-- CURRENT-REGISTER:END -->)',s,re.M|re.S));pins=json.loads((D/'ORIGINAL-68-FAMILY-PINS.json').read_text())['records'];self.assertEqual(len(pins),68)
  for row in pins:self.assertEqual(hashlib.sha256(records[row['id']].encode()).hexdigest(),row['sha256'])
  historical=__import__('subprocess').check_output(['git','show','3e128d9a617af377516a0b9878a942b29bf2e3b8:research/HYPOTHESES.md'],cwd=ROOT).decode();self.assertEqual(set(re.findall(r'^### (H-[^\n]+)$',historical,re.M))-{r['id'] for r in pins},{'H-CANONICAL-RESIDUAL-FEEDBACK'});self.assertIn('- Status: specified but not run',historical.split('### H-CANONICAL-RESIDUAL-FEEDBACK\n')[1].split('### H-')[0])
 def test_unrun_and_current_frontier(self):
  s=json.loads((D/'STATUS.json').read_text());self.assertEqual(s['target_status'],'UNRUN');self.assertFalse(s['target_execution_authorized']);self.assertEqual(s['sealer_status'],'UNRUN_UNAUTHORIZED')
  f=json.loads((ROOT/'research/specifications/FRONTIER-CURRENT-20261101-PRETARGET.json').read_text());self.assertEqual(f['expected_register_entries'],69);g=next(x for x in f['gates'] if x['id']=='F-CANONICAL-RESIDUAL-PRETARGET');self.assertFalse(g['ready_for_new_K4_evaluation']);self.assertIsNone(g['safe_replay_argv'])
