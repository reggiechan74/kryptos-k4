import copy,json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import frontier_assessment as frontier
import exclusion_scope_audit as audit

class FrontierAssessmentTests(unittest.TestCase):
    def test_all_current_entries_are_reviewed_without_new_search(self):
        # 046 is a preserved historical inventory, not the live scheduling queue.
        # Check the live projection against today's canonical ledger rather than
        # silently rewriting the old receipt when a family scope is reconciled.
        current=frontier.assess()
        entries=frontier.canonical((ROOT/'research/HYPOTHESES.md').read_text())
        self.assertEqual({r['id'] for r in current['entries']},set(entries))
        for row in current['entries']:
            fields=entries[row['id']]
            self.assertEqual(row['status'],fields['Status'])
            self.assertEqual(row['mechanism'],fields['Mechanism'])
            self.assertEqual(row['missing_inputs'],fields['Missing inputs'])
            self.assertEqual(row['next_discriminating_test'],fields['Next discriminating test'])
            self.assertEqual(row['unexcluded_scope'],fields['Untested scope'])
        self.assertEqual(current['new_K4_evaluations'],0)
        self.assertEqual(current['replay_commands_executed'],0)
        self.assertTrue(all(not r['ready_for_new_K4_evaluation'] for r in current['entries']))
        saved=json.loads((ROOT/'results/FRONTIER-046.json').read_text())
        import hashlib
        for path,digest in saved['source_sha256'].items():
            raw=subprocess.check_output(['git','show','f526743d049a9b57f75a1996319a6fe3ae16724d:'+path],cwd=ROOT)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),digest)
        historical_ref='f526743d049a9b57f75a1996319a6fe3ae16724d'
        old_text=subprocess.check_output(['git','show',historical_ref+':research/HYPOTHESES.md'],cwd=ROOT).decode()
        old_spec=json.loads(subprocess.check_output(['git','show',historical_ref+':research/specifications/FRONTIER-2026-10-23.json'],cwd=ROOT))
        reconstructed=frontier.assess(spec=old_spec,entries=frontier.canonical(old_text))
        # assess hashes current files; substitute only the individually verified
        # historical input hashes, then compare the full historical output.
        reconstructed['source_sha256']=saved['source_sha256']
        self.assertEqual(reconstructed,saved)
        self.assertEqual(saved['registered_entries'],63);self.assertEqual(len({r['id'] for r in saved['entries']}),63)
        self.assertEqual(saved['new_K4_evaluations'],0);self.assertEqual(saved['replay_commands_executed'],0);self.assertEqual(saved['ready_new_K4_experiments'],0);self.assertFalse(saved['puzzle_solved'])
        self.assertTrue(all(not r['ready_for_new_K4_evaluation'] for r in saved['entries']));self.assertEqual(len(saved['frontier_gates']),12)
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
        text=(ROOT/'research/HYPOTHESES.md').read_text();self.assertEqual(len(frontier.canonical(text)),63)
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

    def test_two_dimensional_frontier_snapshot_retains_historical_sources(self):
        import hashlib
        old=json.loads((ROOT/'results/FRONTIER-021.json').read_text())
        for p,h in old['source_sha256'].items():
            raw=subprocess.check_output(['git','show','91b49e233787e3bd449407247602a1b02a7ff9ae:'+p],cwd=ROOT)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),h)

    def test_physical_frontier_snapshot_retains_historical_sources(self):
        import hashlib
        old=json.loads((ROOT/'results/FRONTIER-022.json').read_text())
        for p,h in old['source_sha256'].items():
            raw=subprocess.check_output(['git','show','c76f108a8d32b9506bf857dac2333a6e47a5a01e:'+p],cwd=ROOT)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),h)

    def test_historical_clock_frontier_snapshot_retains_original_sources(self):
        import hashlib
        old=json.loads((ROOT/'results/FRONTIER-023.json').read_text())
        for p,h in old['source_sha256'].items():
            raw=subprocess.check_output(['git','show','48b87aa79696984f647d70818e862a61b19cd575:'+p],cwd=ROOT)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),h)

    def test_unknown_anchor_snapshot_retains_historical_sources(self):
        import hashlib
        old=json.loads((ROOT/'results/FRONTIER-024.json').read_text())
        for p,h in old['source_sha256'].items():
            raw=subprocess.check_output(['git','show','ccdc8bf32c1ac40fc439363eda15f793f7ed0b97:'+p],cwd=ROOT)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),h)

    def test_lamp_greek_snapshot_retains_historical_sources(self):
        import hashlib
        old=json.loads((ROOT/'results/FRONTIER-025.json').read_text())
        for p,h in old['source_sha256'].items():
            raw=subprocess.check_output(['git','show','9e775c4714b44d2e22b39cbcc7e4db999789d753:'+p],cwd=ROOT)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),h)

    def test_item6_snapshot_retains_historical_sources(self):
        import hashlib
        old=json.loads((ROOT/'results/FRONTIER-026.json').read_text())
        for p,h in old['source_sha256'].items():
            raw=subprocess.check_output(['git','show','8ba613df2549f3ab7b111923094397722d66586c:'+p],cwd=ROOT)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),h)

    def test_item7_snapshot_retains_historical_sources(self):
        import hashlib
        old=json.loads((ROOT/'results/FRONTIER-027.json').read_text())
        for p,h in old['source_sha256'].items():
            raw=subprocess.check_output(['git','show','f6c5d2637fe0ab529c2019a2317d8e9375462da2:'+p],cwd=ROOT)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),h)

    def test_one_edit_frontier_retains_historical_sources(self):
        import hashlib
        old=json.loads((ROOT/'results/FRONTIER-028.json').read_text())
        for path,sha in old['source_sha256'].items():
            raw=subprocess.check_output(['git','show','ff80821cd93d00f2c85dc4d39a71fd73b3f56cbf:'+path],cwd=ROOT)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),sha)

    def test_projection_frontier_retains_historical_sources(self):
        import hashlib
        old=json.loads((ROOT/'results/FRONTIER-029.json').read_text())
        for path,sha in old['source_sha256'].items():
            raw=subprocess.check_output(['git','show','dab2f73e6d1a3b06269ad3c9107768138fb77e13:'+path],cwd=ROOT)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),sha)

    def test_site_v16_frontier_retains_historical_sources(self):
        import hashlib
        old=json.loads((ROOT/'results/FRONTIER-030.json').read_text())
        for path,sha in old['source_sha256'].items():
            raw=subprocess.check_output(['git','show','d157fa4d1aa7113ac6a313828826e8708d8e1094:'+path],cwd=ROOT)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),sha)

    def test_site_v17_frontier_retains_historical_sources(self):
        import hashlib
        old=json.loads((ROOT/'results/FRONTIER-031.json').read_text())
        for path,sha in old['source_sha256'].items():
            raw=subprocess.check_output(['git','show','341d811ec894c375c18f160824ef47839d763313:'+path],cwd=ROOT)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),sha)

    def test_spelling_frontier_retains_historical_sources(self):
        import hashlib
        old=json.loads((ROOT/'results/FRONTIER-032.json').read_text())
        for path,sha in old['source_sha256'].items():
            raw=subprocess.check_output(['git','show','97f017a7ab27b11e4638d2ac9d94e881579f5a5a:'+path],cwd=ROOT)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),sha)

    def test_cover_frontier_retains_historical_sources(self):
        import hashlib
        old=json.loads((ROOT/'results/FRONTIER-034.json').read_text())
        for path,sha in old['source_sha256'].items():
            raw=subprocess.check_output(['git','show','9d6db4cc4384dcad9c3e67589b32f08a07e60db1:'+path],cwd=ROOT)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),sha)

    def test_prose_frontier_retains_historical_sources(self):
        import hashlib
        old=json.loads((ROOT/'results/FRONTIER-035.json').read_text())
        for path,sha in old['source_sha256'].items():
            raw=subprocess.check_output(['git','show','817566c6ef416b8c781e90dd6de51d59be9b53b2:'+path],cwd=ROOT)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),sha)

    def test_curved_frontier_retains_historical_sources(self):
        import hashlib
        old=json.loads((ROOT/'results/FRONTIER-036.json').read_text())
        for path,sha in old['source_sha256'].items():
            raw=subprocess.check_output(['git','show','e9307503418fb4f60d6f8f4acf296b7da33aeaa0:'+path],cwd=ROOT)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),sha)

    def test_previous037frontier_preserves_its_original_source_history(self):
        import hashlib
        old=json.loads((ROOT/'results/FRONTIER-037.json').read_text())
        for path,sha in old['source_sha256'].items():
            raw=subprocess.check_output(['git','show','5db5cb0f0a7d18a7a6d00c16dd0a2e3e7791e643:'+path],cwd=ROOT)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),sha)
