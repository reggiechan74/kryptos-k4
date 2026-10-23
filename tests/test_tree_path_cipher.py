import unittest
import json
from pathlib import Path
import hashlib
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

    def test_actual_and_control_receipts(self):
        root=Path(__file__).resolve().parents[1]
        r=json.loads((root/'results/TREE-PATH-CIPHER-001.json').read_text())
        self.assertEqual((r['raw_models'],r['distinct_full_decryptions'],r['first_survivors'],r['all_survivors']),(104,104,0,0))
        self.assertTrue(all(x['regenerates'] for x in r['results']))
        self.assertEqual(r['protocol_sha256'],hashlib.sha256((root/'research/TREE-PATH-CIPHER-SPEC.md').read_bytes()).hexdigest())
        self.assertEqual(r['source_sha256'],hashlib.sha256((root/'experiments/tree_path_cipher.py').read_bytes()).hexdigest())
        controls=json.loads((root/'results/TREE-PATH-CIPHER-001-controls.json').read_text())['controls']
        self.assertEqual(controls['selector_decodes'],10816)
        self.assertEqual(controls['timing_mutants_detected'],104)
        self.assertEqual(len(controls['planted_selectors']),104)
        self.assertTrue(all(len(p['compatible_models'])==1 for p in controls['planted_selectors']))
