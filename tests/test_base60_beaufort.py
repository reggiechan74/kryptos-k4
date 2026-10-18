import itertools
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'experiments'))
from base60_beaufort import stream,solve,component_options,graph_model,parity_proof,parity_rows

class Base60BeaufortTests(unittest.TestCase):
    def test_exhaustive_small_oracles(self):
        for n in (2,3):
            vertices=list('ABC'[:n]); candidates=[(a,b) for j,a in enumerate(vertices) for b in vertices[j:]]
            for mask in range(1<<len(candidates)):
                pairs=[p for i,p in enumerate(candidates) if mask>>i&1]
                for labels in itertools.product(range(n),repeat=len(pairs)):
                    expected=any(all((v[vertices.index(a)]+v[vertices.index(b)])%n==d for (a,b),d in zip(pairs,labels)) for v in itertools.permutations(range(n)))
                    result=solve(vertices,pairs,labels,n,seconds=1)
                    self.assertEqual(result['status']=='complete_global_alphabet_feasible',expected,(n,pairs,labels,result))
    def test_noninvertible_two_and_cycles(self):
        for n in (4,6,26):
            c=graph_model(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:n]),[('A','A')])[0]
            for d in range(n):
                opts,_=component_options(c,[d],n)
                self.assertEqual(len(opts),0 if d%2 else 2)
        self.assertEqual(solve(list('ABCD'),[('A','B'),('B','C'),('C','D'),('D','A')],[1,2,3,1],4)['status'],'local_sum_or_injectivity_contradiction')
        self.assertEqual(solve(list('ABCD'),[('A','A'),('B','B'),('C','C')],[0,0,0],4)['status'],'local_compatible_global_contradiction')
        self.assertEqual(solve(list('ABCD'),[('A','B'),('C','D')],[0,0],4)['status'],'local_compatible_global_contradiction')
        self.assertEqual(solve(list('ABCD'),[('A','B')],[1],4,max_states=0)['status'],'unresolved_resource_cap')
    def test_synthetic_true_beaufort(self):
        vertices=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'); alphabet={c:(7*i+3)%26 for i,c in enumerate(vertices)};inv={v:k for k,v in alphabet.items()}
        for lag in (2,3,4):
            for rule in (0,1):
                d=stream([17,42,5,59][:lag],rule);pairs=[];labels=[]
                for i in list(range(21,34))+list(range(63,74)):
                    p=vertices[(i*5+1)%26]; c=inv[(d[i]-alphabet[p])%26];pairs.append((p,c));labels.append(d[i]%26)
                self.assertEqual(solve(vertices,pairs,labels,seconds=1)['status'],'complete_global_alphabet_feasible')
    def test_recurrence_parity_and_equivalence(self):
        for lag in (2,3,4):
            for rule in (0,1):
                for p in itertools.product((0,1,58,59),repeat=lag):
                    self.assertEqual([v%2 for v in stream(p,rule)],stream([v%2 for v in p],rule,2))
        for p in itertools.product(range(4),repeat=2):self.assertEqual(stream(p,0),stream(p,1))
    def test_parity_balance(self):
        vertices=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ');pairs=[(vertices[i],vertices[i+1]) for i in range(20)]
        self.assertFalse(parity_proof(vertices,pairs,[0]*20)['compatible'])
        self.assertTrue(parity_proof(vertices,pairs,[1]*20)['compatible'])

    def test_independent_binary_row_certificate(self):
        expected={(2,0):['11','01','11','01'],(2,1):['11','01','11','01'],(3,0):['011','110','001','100'],(3,1):['111','101','100','010'],(4,0):['0010','1011','0010','1001'],(4,1):['0010','0110','0010','0001']}
        for key,rows in expected.items():self.assertEqual(parity_rows(*key),rows)
