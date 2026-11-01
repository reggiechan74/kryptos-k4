"""Static stored-evidence checks only; never import scientific source."""
import hashlib,json,re,subprocess,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'research/c20-successor-queue-v1'
class C20Release(unittest.TestCase):
 def test_package_bytes(self):
  for name,row in json.loads((D/'MANIFEST.json').read_text())['files'].items():
   b=(D/name).read_bytes();self.assertEqual(len(b),row['bytes']);self.assertEqual(hashlib.sha256(b).hexdigest(),row['sha256'])
 def test_stored_finite_synthetic_result(self):
  x=json.loads((D/'SYNTHETIC-RESULT.json').read_text());self.assertEqual(x['status'],'PASS_SYNTHETIC_ONLY');self.assertEqual(x['target_admission'],'NOT_ADMITTED');self.assertTrue(x['no_target_inputs']);self.assertEqual(sum(z['cases'] for z in x['per_alphabet']),17349);self.assertEqual(x['plant_phase_pairs'],91);self.assertEqual(x['plants'],13);self.assertEqual(x['malformed_rejections'],16);self.assertEqual(x['phase_rejections'],12)
 def test_effective_status_not_target_result(self):
  d=R/'research/next-100-hypotheses-20261101';rows={x['id']:x for x in json.loads((d/'CURRENT-CATALOG.json').read_text())['records']};self.assertEqual(rows['N100-065']['status'],'target_tested_narrow_negative');self.assertEqual(rows['N100-065']['recorded_runs'],2);self.assertEqual(rows['N100-065']['target_admission'],'completed_fixed_scope_no_retry');self.assertEqual(rows['N100-036']['status'],'blocked_prior_art_overlap_unresolved')
 def test_all_historical_family_bodies_unchanged(self):
  old=subprocess.check_output(['git','show','608fc123567b77ba48616c9c2191825d08964ea7:research/HYPOTHESES.md'],cwd=R,text=True);new=(R/'research/HYPOTHESES.md').read_text();pattern=r'^### (H-[^\n]+)\n(.*?)(?=^### H-|<!-- CURRENT-REGISTER:END -->)';before=dict(re.findall(pattern,old,re.M|re.S));after=dict(re.findall(pattern,new,re.M|re.S));self.assertEqual(len(before),69)
  for ident,body in before.items():self.assertEqual(after[ident],body,ident)
  self.assertEqual(set(after)-set(before),{'H-SUCCESSOR-QUEUE-COMPOSITE'})
