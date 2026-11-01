"""Read-only C02 publication metadata; no derivation import or execution."""
from pathlib import Path
import hashlib,json,subprocess,re,unittest
R=Path(__file__).resolve().parents[1];D=R/'research/c02-huffman-framing-audit-v1'
class C02Audit(unittest.TestCase):
 def test_exact_public_pins_and_single_admin_derivative(self):
  for n,h in json.loads((D/'SHA256SUMS.json').read_text()).items():self.assertEqual(hashlib.sha256((D/n).read_bytes()).hexdigest(),h,n)
  m=json.loads((D/'PUBLICATION-PROVENANCE.json').read_text());old=json.loads((D/'ORIGINAL-SHA256SUMS.json').read_text());self.assertEqual(len(m['files']),6);self.assertEqual([x['path'] for x in m['files'] if x['original_sha256']!=x['public_sha256']],['REPORT.md'])
  for x in m['files']:self.assertEqual(x['original_sha256'],old[x['path']]);self.assertEqual(x['public_sha256'],hashlib.sha256((D/x['path']).read_bytes()).hexdigest())
 def test_unrun_status_and_no_capacity_count(self):
  s=json.loads((D/'STATUS.json').read_text());self.assertFalse(s['experiment_executed']);self.assertFalse(s['target_read_or_transformed']);self.assertEqual(s['budget_requested'],0);j=json.loads((R/'research/next-100-hypotheses-20261101/CURRENT-CATALOG.json').read_text());u=next(x for x in j['records'] if x['id']=='N100-047');self.assertEqual(u['recorded_runs'],0);self.assertEqual(u['target_admission'],'not_admitted');self.assertEqual(u['status'],'source_proof_audited_operational_gates_pending');self.assertIn('Do not run a standalone M21',(D/'README.md').read_text());self.assertIn('not excluded',(D/'README.md').read_text())
 def test_72_families_and_m21_freeze_preserved(self):
  old=subprocess.check_output(['git','show','439415d9c30bd395369f76c3341a22db9d6714ef:research/HYPOTHESES.md'],cwd=R,text=True);new=(R/'research/HYPOTHESES.md').read_text();pat=r'^### (H-[^\n]+)\n(.*?)(?=^### H-|<!-- CURRENT-REGISTER:END -->)';a=dict(re.findall(pat,old,re.M|re.S));b=dict(re.findall(pat,new,re.M|re.S));self.assertEqual(len(a),72);self.assertEqual({k:b[k] for k in a},a);self.assertEqual(len(b),len(re.findall(r'^### H-',new,re.M)))
  p=R/'research/m21-framing-capacity-v1';m=json.loads((p/'SHA256SUMS.json').read_text())
  for n,h in m.items():self.assertEqual(hashlib.sha256((p/n).read_bytes()).hexdigest(),h)
