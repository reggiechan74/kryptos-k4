"""Static pending coverage-plan checks, never experiment or target execution."""
from pathlib import Path
import hashlib,json,re,subprocess,unittest
R=Path(__file__).resolve().parents[1];D=R/'research/puzzle-instruction-discovery-v1'
class PuzzleInstructionPlan(unittest.TestCase):
 def test_public_plan_pins_pending_checks(self):
  for n,h in json.loads((D/'SHA256SUMS.json').read_text()).items():self.assertEqual(hashlib.sha256((D/n).read_bytes()).hexdigest(),h)
  s=json.loads((D/'STATUS.json').read_text());self.assertFalse(s['experiment_executed']);self.assertFalse(s['target_admitted']);self.assertEqual(s['run_receipts'],[]);self.assertEqual([x['id'] for x in s['checks']],['P1','P2','P3','P4','P5','P6']);self.assertTrue(all(x['status']=='pending' for x in s['checks']))
 def test_historical72_exact_and_only_pending_addition(self):
  old=subprocess.check_output(['git','show','21e5a3e2ad834cfc545d5616716da0c157ffc28a:research/HYPOTHESES.md'],cwd=R,text=True);new=(R/'research/HYPOTHESES.md').read_text();p=r'^### (H-[^\n]+)\n(.*?)(?=^### H-|<!-- CURRENT-REGISTER:END -->)';a=dict(re.findall(p,old,re.M|re.S));b=dict(re.findall(p,new,re.M|re.S));self.assertEqual(len(a),72);self.assertEqual({k:b[k] for k in a},a);self.assertEqual(set(b)-set(a),{'H-PUZZLE-INSTRUCTION-DISCOVERY'});self.assertIn('- Status: specified but not run',b['H-PUZZLE-INSTRUCTION-DISCOVERY']);self.assertEqual(new.count('## Next-action queue'),1)
 def test_prior_scopes_and_gates_explicit(self):
  s=(D/'README.md').read_text()
  for x in ('FACE-ROW-001','ENE-ROUTE-049','HAND-GRAMMAR-050','K3-CLOCK-ROUTES-001','FOLD-SLIDE-2D-001','810-cell','Post-decode branch','No supported recipe','Zero recipes','No target command'):self.assertIn(x,s)
  self.assertEqual(hashlib.sha256((R/'research/next-100-hypotheses-20261101/catalog.json').read_bytes()).hexdigest(),'1b58132bd63c42618c5d1c20bff280c01ea6ffa89d44582c4dfe21a154801862')
 def test_current_inventory_pending_and_old_snapshot_frozen(self):
  d=R/'research/specifications';old=json.loads((d/'FRONTIER-CURRENT-20261101-E02-CLOSED.json').read_text());new=json.loads((d/'FRONTIER-CURRENT-20261101-PUZZLE-PLAN.json').read_text());self.assertEqual(old['expected_register_entries'],72);self.assertEqual(new['expected_register_entries'],73);g=next(x for x in new['gates'] if x['id']=='F-PUZZLE-INSTRUCTION-PLAN');self.assertFalse(g['ready_for_new_K4_evaluation']);self.assertIsNone(g['safe_replay_argv'])
