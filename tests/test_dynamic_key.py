import itertools
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'experiments'))
from dynamic_key import ALPHABETS, analyze, configurations, groups_score, phase_offsets, synthetic_controls, transform


class DynamicKeyTests(unittest.TestCase):
    def test_all_planted_models_and_mutations(self):
        self.assertEqual(synthetic_controls(), dict(roundtrips=288, planted_compatible=288,
                                                   mutated_constraints_rejected=288))

    def test_modal_score_is_exhaustive_key_optimum(self):
        groups = {0: [0, 1, 1], 1: [1, 0], 2: [0, 0]}
        brute = max(sum(value == key[phase] for phase, values in groups.items() for value in values)
                    for key in itertools.product(range(2), repeat=3))
        self.assertEqual(groups_score(groups), brute)

    def test_cursor_updates_after_current_letter(self):
        cfg = dict(family='ciphertext_step', alphabet=ALPHABETS[0], sigma=1, period=5, variant='AEIOU')
        self.assertEqual(phase_offsets('ABECID', cfg), [(0, 0), (2, 0), (3, 0), (0, 0), (1, 0), (3, 0)])
        # Independent manually computed encryption: A + key0 = B; no trigger;
        # A + key1 = E triggers a skipped phase2; A + key3 = C.
        self.assertEqual(transform('AAA', [1, 4, 9, 2, 3], cfg), 'BEC')
        self.assertEqual(transform('BEC', [1, 4, 9, 2, 3], cfg, True), 'AAA')

    def test_progressive_known_answer_and_zero_step(self):
        cfg = dict(family='progressive', alphabet=ALPHABETS[0], sigma=1, period=2, variant=3)
        self.assertEqual(transform('AAAAAA', [1, 2], cfg), 'BCE FHI'.replace(' ', ''))
        cfg['variant'] = 0
        self.assertEqual(transform('AAAAAA', [1, 2], cfg), 'BCBCBC')
        self.assertEqual(phase_offsets('XXXXXX', cfg), [(i % 2, 0) for i in range(6)])

    def test_free_phases_are_not_candidates(self):
        cfg = dict(family='progressive', alphabet=ALPHABETS[0], sigma=1, period=12, variant=0)
        r = analyze('A' * 97, {21: 'A'}, cfg)
        self.assertTrue(r['compatible'])
        self.assertEqual(r['free_phases'], 11)
        self.assertFalse(r['candidate_gate'])

    def test_parameter_budget(self):
        cases = list(configurations())
        self.assertEqual(len(cases), 1344)
        self.assertEqual(sum(c['family'] == 'progressive' for c in cases), 1248)
        for alphabet in ALPHABETS:
            self.assertEqual(len(set(alphabet)), 26)


if __name__ == '__main__':
    unittest.main()
