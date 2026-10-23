from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments'))
from cp_convention_replay import N,C,KEY,crypt,oracle_inverse,normalize


class CPConventionTests(unittest.TestCase):
    def test_literal_alphabets_and_table_cells(self):
        self.assertEqual(len(N),32)
        self.assertEqual(set(N),set(C))
        self.assertNotIn('Ё',N)
        self.assertEqual(KEY,'МЕДУЗА')
        self.assertEqual(crypt('ВЫ'),'ЛТ')
        # All six published key rows, all32input symbols, independent inverse.
        for phase in range(6):
            p='А'*phase+N
            c=crypt(p)
            self.assertEqual(oracle_inverse(c,False),p)

    def test_boundary_and_phase_equivalence(self):
        p=(N*36)[:1133]
        for reset in (False,True):
            c=crypt(p,reset)
            self.assertEqual(crypt(c,reset,True),p)
            self.assertEqual(oracle_inverse(c,reset),p)
        a,b=crypt(p),crypt(p,True)
        self.assertEqual(a[:777],b[:777])
        self.assertTrue(all(x!=y for x,y in zip(a[777:],b[777:])))
        self.assertTrue(all((i-777)%6==(i+3)%6 for i in range(777,1133)))

    def test_no_linguistic_repairs_or_latin_key(self):
        self.assertEqual(normalize('ВЫСОЧАЙЪИМ MEDUSA ПОВЕД{-}НИЯ'),'ВЫСОЧАЙЪИМПОВЕДНИЯ')


if __name__=='__main__':unittest.main()
