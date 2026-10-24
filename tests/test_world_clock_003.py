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

if __name__=='__main__':unittest.main()
