import hashlib,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class UnknownAnchorArtifacts(unittest.TestCase):
    def load(self,name):
        root=ROOT/'results'/name;folder=root/json.loads((root/'latest.json').read_text())['run_id'];manifest=json.loads((folder/'manifest.json').read_text())
        self.assertEqual(manifest['status'],'completed');self.assertEqual(manifest['execution_kind'],'original')
        for path,meta in manifest['artifacts'].items():self.assertEqual(hashlib.sha256((folder/path).read_bytes()).hexdigest(),meta['sha256'])
        return folder
    def test_original_and_corrected_failure_counts_are_not_global_negatives(self):
        for name in ('sigaba-unknown-anchor-024','sigaba-unknown-anchor-024b'):
            folder=self.load(name)
            for backend in ('baseline','integrated'):
                for case in (0,1):
                    d=json.loads((folder/f'{backend}-case-{case}.json').read_text());self.assertEqual(d['K4_evaluations'],0);self.assertFalse(d['real_sized_gate_passed'])
                    for path,digest in d['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),digest)
                    s=d.get('solver',d);self.assertFalse(s['completed']);self.assertIsNone(s['exact_raw_key_count'])
                    if 'solver' in d:
                        self.assertEqual(s['control_starts_requested'],26**5);self.assertEqual(s['found_raw_keys_lower_bound'],'0')
                        self.assertLess(s['budget']['peak_RSS_bytes'],1<<30)
                    else:self.assertEqual(s['reason'],'watchdog_unresolved');self.assertNotIn('control_starts_completed',s)
        folder=self.load('sigaba-unknown-anchor-024b')
        for case in (0,1):
            b=json.loads((folder/f'baseline-case-{case}.json').read_text())['solver'];i=json.loads((folder/f'integrated-case-{case}.json').read_text())['solver']
            self.assertEqual((b['control_starts_completed'],i['control_starts_completed']),(9,11))
            self.assertEqual((i['filters_started'],i['filters_completed']),(12,11))
            self.assertTrue(all(f['retained_roots']<=f['initial_roots'] and f['fixed_point'] for f in i['filter_receipts']))
            self.assertEqual(i['relations'],b['relations'])
    def test_complete_control_streams_and_failure_receipt_are_preserved(self):
        folder=self.load('sigaba-unknown-anchor-024b');d=json.loads((folder/'controls.json').read_text())
        self.assertEqual(d['original_fixed_controls']['complete_raw_truth_streams'],12)
        self.assertEqual(d['varying_input_supplement']['complete_raw_truth_streams'],12)
        self.assertEqual(d['varying_input_supplement']['varying_fixture_count'],4)
        p=ROOT/'results/sigaba-unknown-anchor-diagnostic';failure=json.loads((p/'initial-control-failure.json').read_text())
        raw=(ROOT/'experiments/sigaba_unknown_anchor_collector.py').read_text().replace('list(lastcontrol) if reason and lastcontrol is not None else None','list(lastcontrol) if reason else None')
        self.assertEqual(hashlib.sha256(raw.encode()).hexdigest(),failure['failing_source_sha256'])
        self.assertIn('sigaba_sparse_ownership.py',(p/'stack.txt').read_text())
