"""Static sealed package/ledger checks only, never a source or certificate replay."""
import hashlib,json,re,tarfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'research/residual-target-v1'
class ResidualTargetArtifacts(unittest.TestCase):
 def test_reviewed_package_identity(self):
  m=json.loads((D/'PACKAGE-MANIFEST.json').read_text());self.assertEqual(len(m['files']),96)
  for name,row in m['files'].items():
   b=(D/name).read_bytes();self.assertEqual(len(b),row['bytes']);self.assertEqual(hashlib.sha256(b).hexdigest(),row['sha256'])
   if not name.endswith('.gz'):self.assertFalse(re.search(rb'page_[a-f0-9]{20,}|Responsibilities Page|/root/[A-Za-z_]|https://chatgpt.com/space/',b),name)
 def test_one_unique_certificate_stream(self):
  p=json.loads((D/'CERTIFICATE-ARCHIVE-MANIFEST.json').read_text());a=D/p['archive'];self.assertEqual(hashlib.sha256(a.read_bytes()).hexdigest(),p['archive_sha256']);self.assertEqual(len(p['original_mode_specific_provenance']),2);count=0
  with tarfile.open(a,'r|gz') as t:
   for m in t:
    count+=1;self.assertTrue(m.isfile());self.assertEqual(m.name,p['member']['name']);self.assertEqual(m.size,p['member']['bytes']);h=hashlib.sha256();f=t.extractfile(m)
    for b in iter(lambda:f.read(65536),b''):h.update(b)
    self.assertEqual(h.hexdigest(),p['member']['sha256'])
  self.assertEqual(count,1)
 def test_retained_empty_reports_and_spent_state(self):
  for mode in ('normal','optimized'):
   o=json.loads((D/f'evidence/K4-{mode}/result.json').read_text());self.assertEqual(o['status'],'VERIFIED_EMPTY');self.assertEqual(o['producer']['status'],'EMPTY');self.assertEqual(o['verification']['status'],'VERIFIED_EMPTY');self.assertEqual(o['verification']['stats']['supports'],4495);s=o['semantic_summary'];self.assertEqual(s['joint_predictions'],0);self.assertEqual(s['masks'],[[] for _ in range(91)]);self.assertFalse(s['interpretation']['first_six_claimed'])
  state=json.loads((D/'evidence/accounting/SEALED-STATE.json').read_text());self.assertIsNone(state['in_flight']);self.assertEqual(len(state['completed']),3);self.assertEqual(state['allocation_charged'],172)
 def test_existing_family_only_and_closed_frontier(self):
  s=(ROOT/'research/HYPOTHESES.md').read_text();records=dict(re.findall(r'^### (H-[^\n]+)\n(.*?)(?=^### H-|<!-- CURRENT-REGISTER:END -->)',s,re.M|re.S));self.assertEqual(len(records),69);self.assertIn('- Status: narrow negative',records['H-CANONICAL-RESIDUAL-FEEDBACK']);self.assertIn('R = E minus (B union C)',records['H-CANONICAL-RESIDUAL-FEEDBACK'])
  f=json.loads((ROOT/'research/specifications/FRONTIER-CURRENT-20261101-RESIDUAL-CLOSED.json').read_text());g=next(x for x in f['gates'] if x['id']=='F-CANONICAL-RESIDUAL-CLOSED');self.assertFalse(g['ready_for_new_K4_evaluation']);self.assertIsNone(g['safe_replay_argv'])
