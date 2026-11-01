"""Static P1 packet/ledger checks only; no source collection or instruction coding."""
from pathlib import Path
import hashlib,json,re,subprocess,unittest
R=Path(__file__).resolve().parents[1];D=R/'research/puzzle-instruction-discovery-v1';P=D/'p1-evidence-v1'
class PuzzleP1(unittest.TestCase):
 def test_sealed_six_files_and_payloads(self):
  self.assertEqual(hashlib.sha256((P/'PACKET-MANIFEST.json').read_bytes()).hexdigest(),'2d0260e4c00c7f2383448c50d51ad8301f30231dd0f678ba8e5e86e9603e62bc');m=json.loads((P/'PACKET-MANIFEST.json').read_text());self.assertEqual(len(m['files']),5)
  for x in m['files']:b=(P/x['path']).read_bytes();self.assertEqual(len(b),x['bytes']);self.assertEqual(hashlib.sha256(b).hexdigest(),x['sha256'])
 def test_inventory_and_canonical_pins(self):
  r=json.loads((P/'SOURCE-RECEIPTS.json').read_text());ids=[x['id'] for x in r['source_statuses']];self.assertEqual(len(ids),16);self.assertEqual(len(set(ids)),16);self.assertEqual(set(ids),set(re.findall(r'^### (P1-S\d+) —',(P/'INVENTORY.md').read_text(),re.M)))
  for x in json.loads((P/'CANONICAL-PINS.json').read_text())['files']:
   b=subprocess.check_output(['git','show','e2f4a1e24acdc8bcd319f01b68fd51afbc924ce3:'+x['path']],cwd=R);self.assertEqual(hashlib.sha256(b).hexdigest(),x['sha256']);self.assertEqual(len(b),x['utf8_bytes'])
 def test_current_acceptance_does_not_authorize_p2(self):
  old=json.loads((D/'STATUS.json').read_text());self.assertTrue(all(x['status']=='pending' for x in old['checks']));s=json.loads((D/'CURRENT-STATUS.json').read_text());self.assertEqual(s['checks'][0]['status'],'accepted_bounded_source_inventory');self.assertTrue(all(x['status']=='pending' for x in s['checks'][1:]));self.assertFalse(s['next_stage_started']);self.assertFalse(s['experiment_executed']);self.assertFalse(s['target_admitted']);self.assertEqual(s['run_receipts'],[])
 def test_73_family_bodies_original_catalog_plan_preserved(self):
  a=subprocess.check_output(['git','show','e2f4a1e24acdc8bcd319f01b68fd51afbc924ce3:research/HYPOTHESES.md'],cwd=R,text=True);b=(R/'research/HYPOTHESES.md').read_text();pat=r'^### (H-[^\n]+)\n(.*?)(?=^### H-|<!-- CURRENT-REGISTER:END -->)';aa=dict(re.findall(pat,a,re.M|re.S));bb=dict(re.findall(pat,b,re.M|re.S));self.assertEqual(len(aa),73);self.assertEqual(aa,bb)
  for n,h in json.loads((D/'SHA256SUMS.json').read_text()).items():self.assertEqual(hashlib.sha256((D/n).read_bytes()).hexdigest(),h)
  self.assertEqual(hashlib.sha256((R/'research/next-100-hypotheses-20261101/catalog.json').read_bytes()).hexdigest(),'1b58132bd63c42618c5d1c20bff280c01ea6ffa89d44582c4dfe21a154801862')
