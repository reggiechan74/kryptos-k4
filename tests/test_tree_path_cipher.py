import unittest
from experiments.tree_path_cipher import trees, crypt, oracle, framed_path_decode, AZ, update

class TreePathTests(unittest.TestCase):
    def test_all_models_inverse_and_oracle(self):
        for t in trees().values():
            for d in (1,-1):
                for s in range(26):
                    p=AZ+'ATTACKATDAWN';c=crypt(p,t,d,s)
                    self.assertEqual(crypt(c,t,d,s,True),p)
                    self.assertEqual(oracle(p,t,d,s),c)
                    self.assertEqual(oracle(c,t,d,s,True),p)
    def test_framing_and_invalid_input(self):
        for t in trees().values():
            self.assertEqual(framed_path_decode([t['paths'][c] for c in AZ],t),AZ)
            with self.assertRaises(ValueError):framed_path_decode(['invalid'],t)
            with self.assertRaises(ValueError):crypt('a',t,1,0)
        t=trees()['morse']
        self.assertEqual(framed_path_decode(['.','.'],t),'EE')
        self.assertEqual(framed_path_decode(['..'],t),'I')
    def test_updates_are_permutations_and_not_only_rotations(self):
        for t in trees().values():
            states=[]
            for c in AZ:
                state=list(AZ);update(state,t,c,1);self.assertEqual(set(state),set(AZ));states.append(''.join(state))
            self.assertTrue(any(s not in [AZ[k:]+AZ[:k] for k in range(26)] for s in states))
