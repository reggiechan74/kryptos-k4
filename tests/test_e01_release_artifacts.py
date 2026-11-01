"""Stored E01 metadata and byte checks only, never source imports/replays."""
import hashlib,json,re,subprocess,unittest,zipfile
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'research/e01-conditional-alphabet-v1'
class E01Artifacts(unittest.TestCase):
 def test_exact_public_package(self):
  for name,row in json.loads((D/'MANIFEST.json').read_text())['files'].items():
   b=(D/name).read_bytes();self.assertEqual(len(b),row['bytes']);self.assertEqual(hashlib.sha256(b).hexdigest(),row['sha256'])
 def test_archive_manifest_and_stored_counts(self):
  with zipfile.ZipFile(D/'e01-synthetic-evidence.zip') as z:
   m=json.loads(z.read('e01/PUBLIC-MEMBER-MANIFEST.json'));self.assertEqual(set(z.namelist()),{'e01/'+n for n in m}|{'e01/PUBLIC-MEMBER-MANIFEST.json'})
   for name,row in m.items():
    b=z.read('e01/'+name);self.assertEqual(len(b),row['bytes']);self.assertEqual(hashlib.sha256(b).hexdigest(),row['sha256'])
   o=json.loads(z.read('e01/synthetic-results/REPORT.json'));self.assertEqual(o['status'],'PASS');self.assertFalse(o['target_used']);self.assertEqual(o['checks'],dict(malformed_assertion_cases=4,malformed_cipher_cases=24,real_row_cells=676,tiny_cases=235872));self.assertEqual(sum(x['cases'] for x in o['synthetic'].values()),320);self.assertEqual(o['synthetic']['positive']['compatible'],64)
   for name,v in o['synthetic'].items():
    if name!='positive':self.assertEqual(v['compatible'],0)
 def test_current_e01_target_gate(self):
  c=json.loads((R/'research/next-100-hypotheses-20261101/CURRENT-CATALOG.json').read_text());e=next(x for x in c['records'] if x['id']=='N100-044');self.assertEqual(e['status'],'target_tested_narrow_negative');self.assertEqual(e['target_admission'],'completed_fixed_scope_no_retry');self.assertEqual(e['recorded_runs'],2)
 def test_all70_family_bodies_unchanged(self):
  old=subprocess.check_output(['git','show','4764b4f0439c62d9f1db5abe902e116abb08d91a:research/HYPOTHESES.md'],cwd=R,text=True);new=(R/'research/HYPOTHESES.md').read_text();pattern=r'^### (H-[^\n]+)\n(.*?)(?=^### H-|<!-- CURRENT-REGISTER:END -->)';a=dict(re.findall(pattern,old,re.M|re.S));b=dict(re.findall(pattern,new,re.M|re.S));self.assertEqual(len(a),70);self.assertEqual({k:b[k] for k in a},a);self.assertIn('H-CONDITIONAL-ALPHABET-BANK',set(b)-set(a))
