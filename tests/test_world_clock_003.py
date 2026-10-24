import importlib.util
import json
from fractions import Fraction
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('clock003',ROOT/'experiments/world_clock_003.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class WorldClock003Tests(unittest.TestCase):
    def test_complete_tiny_compatible_sets_and_plants(self):
        result=m.controls()
        self.assertEqual(result['complete_tiny_ring_solution_set_comparisons'],36)
        self.assertEqual(result['planted_true_layouts_retained'],36)
        self.assertTrue(result['mutations_and_unknown_vs_empty_checks_passed'])

    def test_original_evidence_replay_without_overwrite(self):
        import hashlib
        before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in m.INPUT.parent.iterdir() if p.is_file()}
        result=m.replay_old_pilot();self.assertTrue(result['all_original_result_fields_equal'])
        self.assertEqual(result['result']['coordinate_label_roundtrips'],41)
        self.assertEqual(result['result']['mechanical_integer_phase_roundtrips'],1152)
        after={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in m.INPUT.parent.iterdir() if p.is_file()}
        self.assertEqual(before,after)

    def test_single_phase_recovery_and_wrong_direction_mutation(self):
        sectors=[0,1,2];hours=[Fraction(13,2),Fraction(15,2),Fraction(17,2)]
        self.assertEqual(m.phase_fit(sectors,hours,24),Fraction(13,2))
        self.assertIsNone(m.phase_fit([0,23,22],hours,24))
        self.assertIsNone(m.phase_fit(sectors,[6,8,9],24))
        self.assertIsNone(m.phase_fit([],[],24))

    def test_complete_partial_unknown_and_rank_override(self):
        def slot(upper,complete,rank=None):
            d={'s':0,'upper':upper,'lower':[],'upper_complete':complete,'lower_complete':False}
            if rank:d['upper_rank_override']=rank
            return d
        self.assertIsNone(m.pair_conflict(slot([],False),slot(['A'],True)))
        self.assertIsNotNone(m.pair_conflict(slot([],True),slot(['A'],True)))
        self.assertIsNone(m.pair_conflict(slot(['B'],False,[2]),slot(['A','B'],True)))
        self.assertIsNotNone(m.pair_conflict(slot(['B'],False,[2]),slot(['A'],True)))
        with self.assertRaises(ValueError):m.band_map(slot(['B'],True,[2]),'upper')

    def test_common_rotation_is_a_gauge_not_new_evidence(self):
        for rotation in range(24):
            for phase in (Fraction(0),Fraction(1,3)):
                for s in range(24):
                    self.assertEqual((s+phase)%24,((s+rotation)%24+(phase-rotation)%24)%24)

    def test_original_registration_receipt_and_complete_set(self):
        import hashlib
        root=ROOT/'results/world-clock-003'
        run=json.loads((root/'latest.json').read_text())['run_id']
        manifest=json.loads((root/run/'manifest.json').read_text())
        raw=(root/run/'registration-analysis.json').read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),manifest['artifacts']['registration-analysis.json']['sha256'])
        d=json.loads(raw)
        self.assertEqual(hashlib.sha256(m.INPUT.read_bytes()).hexdigest(),d['input_sha256'])
        self.assertEqual(hashlib.sha256((ROOT/'experiments/world_clock_003.py').read_bytes()).hexdigest(),d['source_sha256'])
        self.assertEqual((d['raw_gauge_fixed_offset_pairs'],d['compatible_registration_count']),(576,240))
        self.assertEqual(d['forced_pair_counts'],{'within_segment':272})
        self.assertEqual(d['cross_segment_pair_count'],548)
        self.assertEqual(d['k4_trials'],0)
        data=json.loads(m.INPUT.read_text())
        accepted=m.oracle_layouts(data['segments'],24)
        ids=[x['id'] for x in data['segments']]
        self.assertEqual(accepted,{tuple(row[k] for k in ids) for row in d['compatible_registrations']})

if __name__=='__main__':unittest.main()
