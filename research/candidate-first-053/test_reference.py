import unittest,math,tempfile
from pathlib import Path
from collections import Counter
import reference as p
import prepare_data as d

class ReferenceTests(unittest.TestCase):
    def test_crypto_all_tableaux_and_key_label(self):
        rng=p.rng_for('synthetic-crypto')
        for t in p.TABLEAUX:
            plain=''.join(rng.choice(p.AZ) for _ in range(97));key=''.join(rng.choice(p.AZ) for _ in range(97))
            cipher=p.encrypt_key(plain,key,t)
            self.assertEqual(p.derive_key(plain,cipher,t),key)
            self.assertEqual(p.decrypt_key(cipher,key,t),plain)
        self.assertEqual(p.KR,'KRYPTOSABCDEFGHIJLMNQUVWXZ')
    def test_counts_boundaries_and_probability(self):
        m,c=p.LanguageModel.train([b'ABCA',b'BDA'])
        self.assertEqual(sum(c[0]),7);self.assertEqual(sum(c[1]),5);self.assertEqual(sum(c[2]),3);self.assertEqual(sum(c[3]),1)
        self.assertEqual(c[1][p.AZ.index('A')*26+p.AZ.index('B')],1)
        self.assertEqual(c[3][((0*26+1)*26+2)*26+0],1)
        for row in m.log_tables:
            for start in range(0,len(row),26):self.assertAlmostEqual(sum(2**x for x in row[start:start+26]),1.,places=12)
        self.assertAlmostEqual(2**m.log_tables[0][0],(3+.5)/(7+13),places=15)
        self.assertAlmostEqual(2**m.log_tables[1][1],(1+5*(2.5/20))/(1+5),places=15)
    def test_crib_context_excluded(self):
        m,_=p.LanguageModel.train([b'THISISASY NTHETICTRAININGDOCUMENT'.replace(b' ',b'')*10])
        key='A'*97;altered=list(key)
        for i in p.KNOWN:altered[i]='Z'
        altered=''.join(altered)
        self.assertEqual(m.score_key(key),m.score_key(altered));self.assertNotEqual(m.full_cross_entropy(key),m.full_cross_entropy(altered))
        vals=p.encode(key,'AZ');direct=sum(m.log_probability(vals,a,b) for a,b in p.BLOCKS)
        self.assertAlmostEqual(m.score_key(key),p.BASELINE+direct-math.log2(1024)-math.log2(12),places=10)
    def test_uniform_model_and_serialization(self):
        m,_=p.LanguageModel.train([])
        self.assertAlmostEqual(m.score_key('A'*97),-math.log2(1024)-math.log2(12),places=10)
        self.assertAlmostEqual(m.full_cross_entropy('Z'*97),math.log2(26),places=12)
        with tempfile.TemporaryDirectory() as t:
            f=Path(t)/'model';m.save(f);other=p.LanguageModel.load(f)
            self.assertEqual([list(r) for r in m.log_tables],[list(r) for r in other.log_tables])
    def test_conditional_nulls(self):
        cipher=(p.AZ*4)[:97];a=p.conditional_nulls(cipher,30,'synthetic-null');b=p.conditional_nulls(cipher,30,'synthetic-null')
        self.assertEqual(a,b)
        for row in a:
            self.assertEqual([row[i] for i in p.KNOWN],[cipher[i] for i in p.KNOWN])
            self.assertEqual(Counter(row[i] for i in p.UNKNOWN),Counter(cipher[i] for i in p.UNKNOWN))
        self.assertNotEqual(a,p.conditional_nulls(cipher,30,'independent'))
    def test_grid_short_boundary(self):
        for n in [97,98,200,286,409,600,1000,5000]:
            grid=d.window_grid(n,'synthetic-grid'+str(n));self.assertTrue(grid)
            self.assertTrue(all(0<=x<=n-97 for x in grid));s=sorted(grid)
            self.assertTrue(all(b-a==512 for a,b in zip(s,s[1:])))
        self.assertEqual(d.window_grid(96,'synthetic'),[])
    def test_overlap_exact48(self):
        doc={'role':'heldout','document_id':'one'};other={'role':'training','document_id':'two','norm':b'Z'+b'A'*48+b'Z'}
        self.assertIsNotNone(d.overlap_reason(b'A'*97,doc,[other]));other['norm']=b'Z'+b'A'*47+b'Z'
        self.assertIsNone(d.overlap_reason(b'A'*97,doc,[other]));other['role']='heldout';other['norm']=b'A'*97
        self.assertIsNone(d.overlap_reason(b'A'*97,doc,[other]))

if __name__=='__main__':unittest.main()
