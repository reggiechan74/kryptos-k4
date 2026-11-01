"""Static E02 evidence only; no scientific imports, generators or replay."""
from pathlib import Path
import hashlib,json,re,subprocess,unittest,zipfile
R=Path(__file__).resolve().parents[1];D=R/'research/e02-reference-cursor-v1'
class E02Artifacts(unittest.TestCase):
 def test_public_and_archive_pins(self):
  for n,h in json.loads((D/'MANIFEST.json').read_text()).items():self.assertEqual(hashlib.sha256((D/n).read_bytes()).hexdigest(),h)
  with zipfile.ZipFile(D/'e02-synthetic-evidence.zip') as z:
   m=json.loads((D/'EVIDENCE-INDEX.json').read_text())['archive_members'];self.assertEqual(set(z.namelist()),set(m))
   for n,h in m.items():self.assertEqual(hashlib.sha256(z.read(n)).hexdigest(),h)
 def test_stored_finite_counts_and_amendment(self):
  with zipfile.ZipFile(D/'e02-synthetic-evidence.zip') as z:o=json.loads(z.read('synthetic/result/REPORT.json'))
  self.assertEqual(o['scope'],'DISCLOSED_SYNTHETIC_ONLY_NO_K4');self.assertEqual(o['toy_message_cases'],22230);self.assertEqual(o['real_reference_one_step_cells'],20020);self.assertEqual(o['full_size_disclosed_plants'],48);self.assertEqual(o['null_plaintext_mismatches'],{'reversed-reference':48,'AZ-only-reference':47,'wrong-start-one':15});a=json.loads((D/'GATE-AMENDMENT.json').read_text());self.assertEqual(a['original_gate'],'blind synthetic plants');self.assertFalse(a['blind_recovery_claim']);self.assertTrue(a['preserve_original_catalog_history'])
 def test_effective_status_target_not_admitted(self):
  j=json.loads((R/'research/next-100-hypotheses-20261101/CURRENT-CATALOG.json').read_text());e=next(x for x in j['records'] if x['id']=='N100-045');self.assertEqual(e['status'],'synthetic_validated_target_not_admitted');self.assertEqual(e['recorded_runs'],1);self.assertEqual(e['target_admission'],'not_admitted')
 def test_all71_family_bodies_unchanged(self):
  old=subprocess.check_output(['git','show','5a5008e036d081836f02cc288731a78ac6c03286:research/HYPOTHESES.md'],cwd=R,text=True);new=(R/'research/HYPOTHESES.md').read_text();pat=r'^### (H-[^\n]+)\n(.*?)(?=^### H-|<!-- CURRENT-REGISTER:END -->)';a=dict(re.findall(pat,old,re.M|re.S));b=dict(re.findall(pat,new,re.M|re.S));self.assertEqual(len(a),71);self.assertEqual(a,b)
