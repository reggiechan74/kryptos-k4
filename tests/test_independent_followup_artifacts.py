from pathlib import Path
import hashlib
import json
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'independent/2026-10-22'
sys.path.insert(0,str(ROOT/'experiments'))
from strategy_followup import rank_oracle,configurations


class IndependentFollowupTests(unittest.TestCase):
    def test_received_member_integrity_and_no_photographs(self):
        d=json.loads((BASE/'TRANSFER-RECEIPT.json').read_text())
        self.assertEqual(len(d['received_files']),40)
        for name,record in d['received_files'].items():
            b=(BASE/name).read_bytes()
            self.assertEqual(len(b),record['bytes'])
            self.assertEqual(hashlib.sha256(b).hexdigest(),record['sha256'])
        for p in BASE.rglob('*'):
            self.assertNotIn(p.suffix.lower(),{'.jpg','.jpeg','.png','.webp','.pdf','.zip','.gz'})

    def test_independent_state_full_outputs_match_local_rank_oracle(self):
        d=json.loads((BASE/'evolving-alphabet/k4_results.json').read_text())
        for cfg,row in zip(configurations(),d['models']):
            self.assertEqual(rank_oracle(d['ciphertext'],cfg,True),row['full_plaintext'])
            self.assertEqual(row['matched_known'],0)
            self.assertEqual(row['first_contradiction']['position_1based'],22)
        trace=json.loads((BASE/'evolving-alphabet/k4_full_trace.json').read_text())
        self.assertEqual(len(trace),388)
        for row in trace:
            if row['position_1based']==22:
                self.assertEqual(row['state_before'][:3],'WBF')
                self.assertEqual(row['rank_0based'],2)

    def test_closed_world_classifier_controls_and_clock_limits_retained(self):
        c=json.loads((BASE/'calibration/classification_results.json').read_text())
        self.assertEqual(c['metrics']['test']['n'],144)
        self.assertEqual(round(c['metrics']['test']['accuracy']*144),125)
        self.assertEqual(c['controls']['IID_UNIFORM']['forced_label_counts'],[4,0,44])
        self.assertEqual(c['K4']['forced_label'],'EVOLVING_ALPHABET')
        h=json.loads((BASE/'historical-clock/pilot_results.json').read_text())
        self.assertEqual(h['label_observations'],41)
        self.assertEqual(h['disconnected_segments'],3)
        self.assertEqual(h['k4_trials_executed'],0)
        self.assertEqual(h['mechanical_integer_phase_roundtrips'],1152)
        r=json.loads((ROOT/'results/independent-followup-review/LOCAL-REPLAY-001.json').read_text())
        self.assertTrue(r['classification_results_equal'])
        self.assertFalse(r['synthesis_enumeration_replayed'])


    def test_supplied_synthesis_descriptions_and_plaintexts_not_conflated(self):
        r=json.loads((ROOT/'results/independent-followup-review/SYNTHESIS-LOCAL-EQUATION-AUDIT-001.json').read_text())
        self.assertFalse(r['full_parameter_enumeration_repeated'])
        self.assertEqual(r['additional_novel_K4_searches'],0)
        self.assertEqual(r['targets'][0]['parameter_candidates'],0)
        self.assertEqual([x['parameter_candidates'] for x in r['targets'][1:]],[39,3,2,3,13,1])
        self.assertEqual([x['distinct_full_plaintexts'] for x in r['targets'][1:]],[26,2,2,2,13,1])
        for x in r['targets'][1:]:
            self.assertTrue(all(y['position_1based']==1 for y in x['ambiguous_positions']))


if __name__=='__main__':unittest.main()
