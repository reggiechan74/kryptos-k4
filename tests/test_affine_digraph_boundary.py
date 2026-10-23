import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments'))
from affine_digraph_boundary import verify

class AffineDigraphBoundaryTests(unittest.TestCase):
    def test_all_four_canonical_parity_certificates(self):
        actual=verify();stored=json.loads((ROOT/'results/AFFINE-DIGRAPH-PARITY-001.json').read_text())
        self.assertEqual(actual,stored)
        self.assertEqual(actual['analytic_exclusions'],4)
        self.assertEqual(actual['matrices_or_keys_searched'],0)
        self.assertEqual([(x['alphabet'],x['pair_origin_one_based']) for x in actual['certificates']],[('AZ',1),('AZ',2),('KRYPTOS',1),('KRYPTOS',2)])
        for x in actual['certificates']:self.assertNotEqual(*x['opposed_output_parities'])
        self.assertEqual(actual['controls'],{'fixed_affine_positive_cases':16,'parity_mutation_negatives':16})

if __name__=='__main__':unittest.main()
