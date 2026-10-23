from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'experiments'))
from plaintext_step import ALPHABETS, configurations, controls, decrypt, encrypt


class PlaintextStepTests(unittest.TestCase):
    def test_all_symbol_phases_planted_cribs_and_oracles(self):
        self.assertEqual(controls(), dict(symbol_phase_roundtrips=2600, planted_full_recoveries=12,
                                         planted_crib_recoveries=12, mutated_crib_rejections=12,
                                         numeric_oracle_comparisons=96))

    def test_plaintext_updates_after_current_letter(self):
        cfg = dict(word='PALIMPSEST', alphabet=ALPHABETS[0], trigger='AEIOU')
        # Plain A triggers extra step to L; ciphertext P would not trigger.
        self.assertEqual(encrypt('AA', cfg), 'PL')
        self.assertEqual(decrypt('PL', cfg), 'AA')
        cfg['trigger'] = 'BCDFGHJKLMNPQRSTVWXYZ'
        self.assertEqual(encrypt('AA', cfg), 'PA')
        self.assertEqual(decrypt('PA', cfg), 'AA')

    def test_frozen_configuration_count_and_partition(self):
        cases = list(configurations())
        self.assertEqual(len(cases), 12)
        self.assertEqual(len({tuple(c.items()) for c in cases}), 12)
        triggers = {c['trigger'] for c in cases}
        vowels, consonants = (set('AEIOU'), set('BCDFGHJKLMNPQRSTVWXYZ'))
        self.assertEqual(triggers, {''.join(sorted(vowels)), 'BCDFGHJKLMNPQRSTVWXYZ'})
        self.assertFalse(vowels & consonants)
        self.assertEqual(vowels | consonants, set(ALPHABETS[0]))


if __name__ == '__main__':
    unittest.main()
