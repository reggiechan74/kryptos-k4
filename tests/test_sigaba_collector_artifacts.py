import hashlib,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import sigaba_collector_filter as f
import sigaba_real_adapter as real
import sigaba_joint_toy as toy
import sigaba_csp889 as sig
class CollectorArtifactTests(unittest.TestCase):
 def test_panel_sizes_full_map_audits_and_necessary_scope(self):
  totals=dict(pairs=0,rejected=0,false_positive=0,false_negative=0,trials=0)
  for n in (0,1):
   r=json.loads((ROOT/f'results/sigaba-collector-filter/case-{n}.json').read_text());self.assertTrue(r['completed']);self.assertEqual(r['K4_evaluations'],0);self.assertFalse(r['full_domain_gate_passed']);self.assertEqual(r['selected_anchor_count'],[2,3][n]);self.assertEqual(len(r['anchor_attempts']),[16,7][n]);self.assertEqual(len(r['controller_panel']),4)
   for p in r['pairs']:
    self.assertEqual(p['reachable_map_trials'],66058);self.assertTrue(p['physical_audit_was_actually_executed']);self.assertFalse(p['false_negative']);self.assertTrue(not p['first_window_feasible_classes'] or p['filter']['passes']);totals['pairs']+=1;totals['trials']+=p['reachable_map_trials'];totals['rejected']+=not p['filter']['passes'];totals['false_positive']+=p['false_positive']
   for path,h in r['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),h)
  self.assertEqual(totals,dict(pairs=20,rejected=12,false_positive=6,false_negative=0,trials=1321160))
 def test_retained_connected_graphs_and_continuous_key_checks(self):
  for n in (0,1):
   r=json.loads((ROOT/f'results/sigaba-collector-filter/case-{n}.json').read_text());model=real.RealModel(quotient=False);first=r['fixture']['observations'][:13]
   for item in r['graphs']:
    encoded=item['graph'];self.assertEqual(hashlib.sha256(json.dumps(encoded,separators=(',',':')).encode()).hexdigest(),item['sha256']);rebuilt=f.encode_graph(f.build(model,item['anchor'],first,toy.Budget(10)));self.assertEqual(rebuilt,encoded)
   positives=[]
   for pair in r['pairs']:
    for c in pair['candidate_checks']:
     if c['second_block_passes']:
      positives.append(c);self.assertTrue(c['equals_generated_plaintext']);self.assertEqual(sig.Machine(c['representative_key']).crypt(c['plaintext']),r['fixture']['ciphertext']);self.assertEqual(c['gap_steps_executed'],[0,29][n]);self.assertEqual(c['raw_aliases'],[3,1][n])
   self.assertEqual(len(positives),1)
 def test_latest_local_register_and_separate_full_gate(self):
  import exclusion_scope_audit as a,frontier_assessment as p
  self.assertEqual(a.run()['fresh_analytical_replay'],json.loads((ROOT/'results/EXCLUSION-SCOPE-AUDIT-015.json').read_text())['fresh_analytical_replay']);self.assertEqual(json.loads((ROOT/'results/FRONTIER-019.json').read_text())['ready_new_K4_experiments'],0)
  r=json.loads((ROOT/'results/CSP889-FILTER-019.json').read_text());self.assertFalse(r['full_domain_gate_passed']);self.assertEqual(r['new_full_domain_controller_coverage'],0);self.assertEqual(r['summary']['false_negatives'],0)
