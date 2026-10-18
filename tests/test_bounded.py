import json
from pathlib import Path
import random
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments'))
from bounded_models import *


class BoundedTests(unittest.TestCase):
    def test_twenty_planted_route_and_running_cases(self):
        self.assertEqual(synthetic_controls()['given_parameter_route_constraint_checks'],20)
        self.assertEqual(synthetic_controls()['running_key_roundtrips'],20)

    def test_all_routes_bijective_and_inverse(self):
        catalogue=routes()
        self.assertEqual(len({tuple(x['permutation']) for x in catalogue}),len(catalogue))
        for entry in catalogue:
            p=entry['permutation'];self.assertEqual(sorted(p),list(range(97)))
            self.assertIn(tuple(inverse_permutation(p)),{tuple(x['permutation']) for x in catalogue})

    def test_every_modular_equation(self):
        for name,a in ALPHABETS:
            for eq in EQUATIONS:
                for p in a:
                    for key in range(26):
                        c=crypt(p,[key],a,eq)
                        self.assertEqual(crypt(c,[key],a,eq,True),p)
                        self.assertEqual(required_key(p,c,a,eq),key)

    def test_trifid_independent_coordinate_example(self):
        cube=ascii_uppercase+'?'
        # A=(0,0,0), B=(0,0,1), ?=(2,2,2); concatenated axes => C C F.
        self.assertEqual(trifid('AB?',cube,3),'CCF')
        self.assertEqual(trifid('CCF',cube,3,True),'AB?')

    def test_trifid_all_symbols_and_ragged_blocks(self):
        rng=random.Random(SEED)
        for _,a in ALPHABETS:
            cube=a+'?'
            for period in TRIFID_PERIODS:
                for text in [cube, ''.join(rng.choice(cube) for _ in range(97)), '?', 'A??A']:
                    self.assertEqual(trifid(trifid(text,cube,period),cube,period,True),text)

    def test_literal_window_counts_and_version(self):
        controls=json.loads((ROOT/'data/controls.json').read_text())
        streams=running_streams(controls)
        self.assertEqual([len(s) for _,s in streams],[370,336,769,370,336,769])
        self.assertEqual(sum((len(s)-96)*2*2*3 for _,s in streams),28488)

    def test_constraints_detect_corruption(self):
        data={'ciphertext':'A'*97,'cribs':[{'start':22,'end':34,'plaintext':'EASTNORTHEAST'},{'start':64,'end':74,'plaintext':'BERLINCLOCK'}]}
        self.assertIsNone(constrain(data['ciphertext'],known_pairs(data),list(range(97)),1,ascii_uppercase,'plus','identity'))


if __name__=='__main__':unittest.main()
