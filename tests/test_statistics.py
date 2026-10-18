from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments'))
from statistical_diagnostics import collisions,wilson

class StatisticTests(unittest.TestCase):
    def test_duplicate_excess_definition(self):
        # Four identical lag-1 AA pairs: excess=3, not 6 unordered collisions.
        self.assertEqual(collisions('AAAAA',1),3)
        self.assertEqual(collisions('ABCDE',1),0)
        self.assertEqual(collisions('ABABAB',2),2)
    def test_zero_count_uncertainty_is_nonzero(self):
        low,high=wilson(0,5000)
        self.assertAlmostEqual(low,0)
        self.assertGreater(high,0)
    def test_invalid_width(self):
        for w in [0,-1,3]:
            with self.assertRaises(ValueError):collisions('ABC',w)

if __name__=='__main__':unittest.main()
