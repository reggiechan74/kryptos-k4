import hashlib,json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import summarize_sigaba_joint_toy as summary
class CoupledArtifactTests(unittest.TestCase):
    def test_all_complete_tiny_sets_are_byte_identical(self):
        for i in range(10):
            r=json.loads((ROOT/f'results/sigaba-joint-toy/case-{i:02d}.json').read_text());self.assertTrue(r['solver']['completed']);self.assertTrue(r['verification_completed']);self.assertTrue(r['full_sets_byte_equal'])
            self.assertEqual(r['expanded']['sha256'],r['independent_truth']['sha256']);self.assertEqual(r['expanded']['count'],int(r['solver']['exact_raw_key_count']))
            self.assertEqual(r['solver']['exact_raw_key_count'],r['independent_truth']['raw_key_count']);self.assertEqual(r['solver']['K4_evaluations'],0)
    def test_frozen_scaling_verification_limit_is_not_a_pass(self):
        r=json.loads((ROOT/'results/sigaba-joint-toy/case-10.json').read_text());self.assertTrue(r['solver']['completed']);self.assertFalse(r['verification_completed']);self.assertEqual(r['verification_reason'],'output_budget_unresolved');self.assertEqual(r['solver']['exact_raw_key_count'],'12582912')
        r=json.loads((ROOT/'results/sigaba-joint-toy/case-11.json').read_text());self.assertTrue(r['verification_completed']);self.assertEqual(r['solver']['exact_raw_key_count'],'1');self.assertEqual(r['returned_raw_keys_independently_checked'],1);self.assertNotIn('full_sets_byte_equal',r)
    def test_summary_preserves_completeness_and_resource_classifications(self):
        saved=json.loads((ROOT/'results/SIGABA-JOINT-TOY-012.json').read_text());self.assertEqual(summary.summary(),saved);self.assertEqual(saved['independent_complete_set_comparisons_passed'],10);self.assertFalse(saved['real_sized_gate_passed']);self.assertFalse(saved['all_declared_scaling_verifications_passed']);self.assertEqual(saved['K4_evaluations'],0)
        for row in saved['records']:
            if not row['inference_completed']:self.assertIsNone(row['exact_raw_key_count'])
            self.assertLessEqual(row['controller_starts_completed'],row['controller_starts_requested'])
    def test_every_original_receipt_pins_the_executed_source(self):
        for path in sorted((ROOT/'results/sigaba-joint-toy').glob('case-*.json')):
            r=json.loads(path.read_text());self.assertEqual(r['K4_evaluations'],0)
            for p,h in r.get('source_sha256',{}).items():self.assertEqual(hashlib.sha256(subprocess.check_output(['git','show','9840d8af781dc7291683267106f49223959117e7:'+p],cwd=ROOT)).hexdigest(),h)
            self.assertNotIn('data/k4.json',r.get('source_sha256',{}))

    def test_current_scope_and_frontier_retain_the_real_adapter_gate(self):
        import exclusion_scope_audit as audit
        import frontier_assessment as frontier
        saved=json.loads((ROOT/'results/EXCLUSION-SCOPE-AUDIT-008.json').read_text());self.assertEqual(audit.run(),saved)
        entries={r['id']:r for r in saved['canonical_entries']};self.assertIn('Real-sized',entries['H-SIGABA']['unexcluded_scope']);self.assertIn('synthetic',entries['H-SIGABA']['exact_tested_scope'])
        current=json.loads((ROOT/'results/FRONTIER-012.json').read_text());self.assertEqual(frontier.assess(),current);self.assertEqual(current['ready_new_K4_experiments'],0)
