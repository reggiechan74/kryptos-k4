"""Static M21 evidence checks only: no scientific imports or replay."""
from pathlib import Path
import gzip,hashlib,json,re,subprocess,unittest
R=Path(__file__).resolve().parents[1];D=R/'research/m21-framing-capacity-v1'
class M21Artifacts(unittest.TestCase):
 def test_payload_pins_and_lossless_rows(self):
  m=json.loads((D/'SHA256SUMS.json').read_text());self.assertEqual(len(m),24)
  for n,h in m.items():self.assertEqual(hashlib.sha256((D/n).read_bytes()).hexdigest(),h,n)
  with gzip.open(D/'results/cases.jsonl.gz','rb') as f:data=f.read()
  self.assertEqual(hashlib.sha256(data).hexdigest(),'8a1810a8f6aa7cf4b7fab9bc8b94b4ba46548805dab19faba0833b2abdca9b0c');self.assertEqual(len(data.splitlines()),24624)
 def test_retained_summary_counts_and_limits(self):
  s=json.loads((D/'results/summary.json').read_text());self.assertEqual(s['matrix_cases_completed'],24624);self.assertEqual(s['control_checks_completed'],132);self.assertEqual(s['mismatches'],0);self.assertEqual(s['false_pruning'],0);self.assertEqual(s['bit_filter_exclusions_beyond_exact_length_nonzero_guarantee'],1930);self.assertEqual(s['bit_filter_exclusions_beyond_exact_length_weak'],8453);self.assertGreater(s['total_dp_cpu_seconds'],s['total_oracle_cpu_seconds']);self.assertIn('cached oracle',(D/'README.md').read_text());self.assertIn('not a fourth K4 target',(D/'README.md').read_text())
 def test_current_method_status_not_fourth_target(self):
  d=R/'research/next-100-hypotheses-20261101';j=json.loads((d/'CURRENT-CATALOG.json').read_text());u=next(x for x in j['records'] if x['id']=='N100-099');self.assertEqual(u['status'],'synthetic_method_validated_limited_utility');self.assertEqual(u['recorded_runs'],1);self.assertEqual(u['target_admission'],'target_model_absent_not_admitted');self.assertEqual(sum(x.get('status')=='target_tested_narrow_negative' for x in j['records']),3)
 def test_historical_family_bodies_and_catalog_unchanged(self):
  old=subprocess.check_output(['git','show','1cecf32112d18193da720894191201fa1d4a91d9:research/HYPOTHESES.md'],cwd=R,text=True);new=(R/'research/HYPOTHESES.md').read_text();pat=r'^### (H-[^\n]+)\n(.*?)(?=^### H-|<!-- CURRENT-REGISTER:END -->)';a=dict(re.findall(pat,old,re.M|re.S));b=dict(re.findall(pat,new,re.M|re.S));self.assertEqual(len(a),72);self.assertEqual({k:b[k] for k in a},a);self.assertEqual(len(b),len(re.findall(r'^### H-',new,re.M)));self.assertEqual(hashlib.sha256((R/'research/next-100-hypotheses-20261101/catalog.json').read_bytes()).hexdigest(),'1b58132bd63c42618c5d1c20bff280c01ea6ffa89d44582c4dfe21a154801862')
