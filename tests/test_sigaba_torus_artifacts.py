import hashlib,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import summarize_sigaba_torus as summarize
class TorusArtifactTests(unittest.TestCase):
    def test_complete_identity_control_receipt(self):
        r=json.loads((ROOT/'results/SIGABA-TORUS-013-controls.json').read_text());self.assertTrue(r['completed']);self.assertEqual(r['predicates_compared'],6739);self.assertEqual(r['direct_seed_checks'],998515);self.assertEqual(r['all_subset_and_inverse_checks'],2048)
        for p,h in r['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),h)
    def test_no_fixture_or_branch_model_was_eased(self):
        for i in range(13):
            new=json.loads((ROOT/f'results/sigaba-torus/case-{i:02d}.json').read_text());old=json.loads((ROOT/f'results/sigaba-joint-toy/case-{i:02d}.json').read_text())
            self.assertEqual(new['fixture'],old['fixture']);self.assertEqual(new['synthetic_ciphertext'],old['synthetic_ciphertext']);self.assertEqual(new['observations'],old['observations']);self.assertEqual(new['K4_evaluations'],0)
            if new['solver']['completed'] and old['solver']['completed']:
                for field in ('exact_raw_key_count','branches_visited','index_mask_partitions','max_live_branches','index_aliases','index_maps'):self.assertEqual(new['solver'][field],old['solver'][field])
            if new['solver']['completed']:self.assertTrue(new['baseline_comparison']['canonical_sets_byte_equal'])
    def test_nontruncated_large_compact_truth(self):
        r=json.loads((ROOT/'results/sigaba-torus/case-10.json').read_text());self.assertTrue(r['verification_completed']);self.assertTrue(r['full_sets_canonical_byte_equal']);self.assertEqual(r['independent_compact_truth']['raw_key_count'],'12582912');self.assertEqual(r['canonical_complete']['sha256'],r['independent_compact_truth']['sha256']);self.assertEqual(r['independent_compact_truth']['rows'],49152);self.assertEqual(r['independent_compact_truth']['direct_cipher_seed_checks'],102400)
        self.assertLess(r['independent_compact_truth']['bytes'],256<<20)
    def test_all_executed_inputs_are_pinned(self):
        for i in range(13):
            r=json.loads((ROOT/f'results/sigaba-torus/case-{i:02d}.json').read_text())
            for p,h in r['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),h)
    def test_comparison_summary_and_current_registry(self):
        saved=json.loads((ROOT/'results/SIGABA-TORUS-013.json').read_text());self.assertEqual(summarize.summarize(),saved);self.assertEqual(saved['independent_complete_raw_set_comparisons'],10);self.assertEqual(saved['independent_complete_canonical_set_comparisons'],1);self.assertFalse(saved['real_sized_gate_passed']);self.assertEqual(saved['K4_evaluations'],0)
        import exclusion_scope_audit as audit
        import frontier_assessment as frontier
        r=json.loads((ROOT/'results/EXCLUSION-SCOPE-AUDIT-009.json').read_text());self.assertEqual(audit.run(),r)
        self.assertEqual(frontier.assess(),json.loads((ROOT/'results/FRONTIER-013.json').read_text()))
