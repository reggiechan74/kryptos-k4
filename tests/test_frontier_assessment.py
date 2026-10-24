import copy,json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import frontier_assessment as frontier
import exclusion_scope_audit as audit

class FrontierAssessmentTests(unittest.TestCase):
    def test_all_current_entries_are_reviewed_without_new_search(self):
        saved=json.loads((ROOT/'results/FRONTIER-021.json').read_text());self.assertEqual(frontier.assess(),saved)
        self.assertEqual(saved['registered_entries'],60);self.assertEqual(len({r['id'] for r in saved['entries']}),60)
        self.assertEqual(saved['new_K4_evaluations'],0);self.assertEqual(saved['replay_commands_executed'],0);self.assertEqual(saved['ready_new_K4_experiments'],0);self.assertFalse(saved['puzzle_solved'])
        self.assertTrue(all(not r['ready_for_new_K4_evaluation'] for r in saved['entries']));self.assertEqual(len(saved['frontier_gates']),9)
    def test_a_new_gate_requires_actual_review_not_a_ready_flag(self):
        original=json.loads(frontier.SPEC.read_text());entries=frontier.canonical((ROOT/'research/HYPOTHESES.md').read_text())
        for mutation in ('ready','missing','unknown','executable','duplicate'):
            spec=copy.deepcopy(original)
            if mutation=='ready':spec['gates'][0]['ready_for_new_K4_evaluation']=True
            elif mutation=='missing':spec['gates'][0]['available'].append('research/nonexistent-unadmitted-input.json')
            elif mutation=='unknown':spec['gates'][0]['hypotheses'].append('H-INVENTED')
            elif mutation=='executable':spec['gates'][0]['safe_replay_argv']=['sh','-c','exit 0']
            else:spec['gates'].append(copy.deepcopy(spec['gates'][0]))
            with self.assertRaises(ValueError):frontier.assess(spec,entries)
    def test_register_parser_rejects_duplicate_or_incomplete_entries(self):
        text=(ROOT/'research/HYPOTHESES.md').read_text();self.assertEqual(len(frontier.canonical(text)),60)
        with self.assertRaises(ValueError):frontier.canonical(text.replace('### H-COMPASS-FRAMES','### H-COMPASS-REVERSE',1))
        with self.assertRaises(ValueError):frontier.canonical(text.replace('- Status: evidence-blocked','- Unknown: evidence-blocked',1))
    def test_cli_only_reproduces_readiness_and_current_scope_is_pinned(self):
        raw=subprocess.check_output([sys.executable,str(ROOT/'experiments/frontier_assessment.py')]);self.assertEqual(json.loads(raw),frontier.assess())
        saved=json.loads((ROOT/'results/EXCLUSION-SCOPE-AUDIT-007.json').read_text());self.assertEqual(audit.run()['fresh_analytical_replay'],saved['fresh_analytical_replay'])
        records={r['id']:r for r in saved['canonical_entries']};self.assertIn('already tested',records['H-AFFINE-DIGRAPH']['unexcluded_scope']);self.assertIn('completed',records['H-SIGABA-INSPIRED']['unexcluded_scope']);self.assertIn('72',records['H-AUTOKEY-EXACT']['unexcluded_scope'])

    def test_original_frontier_snapshot_keeps_its_historical_sources(self):
        import hashlib
        old=json.loads((ROOT/'results/FRONTIER-011.json').read_text())
        for p,h in old['source_sha256'].items():
            raw=subprocess.check_output(['git','show','2b612dfcf8b0e7fc4aed345ce97168d3b5b14512:'+p],cwd=ROOT)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),h)

    def test_previous_frontier_snapshot_keeps_original_sources(self):
        import hashlib
        old=json.loads((ROOT/'results/FRONTIER-012.json').read_text())
        for p,h in old['source_sha256'].items():
            raw=subprocess.check_output(['git','show','9840d8af781dc7291683267106f49223959117e7:'+p],cwd=ROOT)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),h)

    def test_torus_frontier_snapshot_keeps_its_original_sources(self):
        import hashlib
        old=json.loads((ROOT/'results/FRONTIER-013.json').read_text())
        for p,h in old['source_sha256'].items():
            raw=subprocess.check_output(['git','show','a1cf4c00b9553f888d74b3e88b2c711517f79d56:'+p],cwd=ROOT)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),h)

    def test_authentic_frontier_snapshot_keeps_original_sources(self):
        import hashlib
        old=json.loads((ROOT/'results/FRONTIER-014.json').read_text())
        for p,h in old['source_sha256'].items():
            raw=subprocess.check_output(['git','show','5273af698c956b6781ea4a9087808e92bb971833:'+p],cwd=ROOT)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),h)

    def test_sparse_frontier_snapshot_keeps_original_sources(self):
        import hashlib
        old=json.loads((ROOT/'results/FRONTIER-015.json').read_text())
        for p,h in old['source_sha256'].items():
            raw=subprocess.check_output(['git','show','552cbdae9d253c1f4cfd62edc5fd08427f87aefa:'+p],cwd=ROOT)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),h)

    def test_domain_frontier_snapshot_keeps_original_sources(self):
        import hashlib
        old=json.loads((ROOT/'results/FRONTIER-016.json').read_text())
        for p,h in old['source_sha256'].items():
            raw=subprocess.check_output(['git','show','03f77ff6707de30821904d614185ff992f1098ae:'+p],cwd=ROOT)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),h)

    def test_anchor_frontier_snapshot_keeps_original_sources(self):
        import hashlib
        old=json.loads((ROOT/'results/FRONTIER-017.json').read_text())
        for p,h in old['source_sha256'].items():
            raw=subprocess.check_output(['git','show','c481ba3:'+p],cwd=ROOT)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),h)

    def test_compact_frontier_snapshot_keeps_original_sources(self):
        import hashlib
        old=json.loads((ROOT/'results/FRONTIER-018.json').read_text())
        for p,h in old['source_sha256'].items():
            raw=subprocess.check_output(['git','show','f86889d99e09d22c193275da1ba146a7f46a1849:'+p],cwd=ROOT)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),h)

    def test_collector_frontier_snapshot_retains_historical_sources(self):
        import hashlib
        old=json.loads((ROOT/'results/FRONTIER-019.json').read_text())
        for p,h in old['source_sha256'].items():
            raw=subprocess.check_output(['git','show','6f269e11bec1a7b2f87e67f014b7b139708d0c61:'+p],cwd=ROOT)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),h)

    def test_overlay_frontier_snapshot_retains_historical_sources(self):
        import hashlib
        old=json.loads((ROOT/'results/FRONTIER-020.json').read_text())
        for p,h in old['source_sha256'].items():
            raw=subprocess.check_output(['git','show','a0d825e7424e5090501421720dd9b100775cdb8c:'+p],cwd=ROOT)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),h)
