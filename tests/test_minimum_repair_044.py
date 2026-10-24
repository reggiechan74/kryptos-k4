import hashlib,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import minimum_repair_044 as m
import autokey_constraints as ak
class MinimumRepair044Tests(unittest.TestCase):
 def test_complete_small_optimal_cipher_key_sets(self):
  r=m.controls();self.assertEqual(r['complete_tiny_optimal_relation_comparisons'],2752);self.assertEqual(r['complete_optimal_cipher_key_pairs'],9158)
 def test_all_real_witnesses_replay_with_separate_existing_autokey_code(self):
  r=json.loads((ROOT/'results/MINIMUM-REPAIR-044-ORIGINAL.json').read_text());data=json.loads((ROOT/'data/k4.json').read_text());known={x['start']-1+j:v for x in data['cribs'] for j,v in enumerate(x['plaintext'])};abc={'AZ':'ABCDEFGHIJKLMNOPQRSTUVWXYZ','KRYPTOS':'KRYPTOSABCDEFGHIJLMNQUVWXZ'};eq={v:k for k,v in ak.COEFFICIENTS.items()}
  self.assertEqual(len(r['rows']),1536)
  for row in r['rows']:
   w=row['witness'];a=abc[row['alphabet']];P=w['plaintext'];C=w['corrected_cipher'];key=w['key'];self.assertTrue(all(P[i]==v for i,v in known.items()));self.assertEqual(sum(x!=y for x,y in zip(C,data['ciphertext'])),row['minimum_substitutions'])
   if row['mode']!='periodic':
    self.assertEqual(ak.transform(P,key,a,eq[row['sigma'],row['tau']],row['mode']),C);self.assertEqual(ak.transform(C,key,a,eq[row['sigma'],row['tau']],row['mode'],True),P);original=ak.analyze(data['ciphertext'],known,a,eq[row['sigma'],row['tau']],row['mode'],row['lag_or_period']);self.assertEqual(original['classification']=='contradicted',row['minimum_substitutions']>0)
   else:self.assertEqual(''.join(a[(row['sigma']*a.index(p)+a.index(key[i%len(key)]))%26] for i,p in enumerate(P)),C)
   self.assertEqual(int(row['optimal_cipher_key_pairs']),int(row['optimal_corrected_ciphertexts'])*int(row['keys_per_corrected_ciphertext']))
 def test_saved_scope_lower_bounds_and_known_one_error_thresholds(self):
  r=json.loads((ROOT/'results/MINIMUM-REPAIR-044-ORIGINAL.json').read_text());self.assertEqual({k:v['short_1_to_12_minimum'] for k,v in r['summary'].items()},{'periodic':11,'plaintext':10,'ciphertext':20});self.assertEqual([x['position_one_based'] for x in r['direct_nonzero_strip_fixed_points']],[33,74]);self.assertEqual(r['arbitrary_permutation_required_letter_deficits'],{'E':1})
  for p,h in r['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),h)
  for mode,L,cost in (('plaintext',26,1),('plaintext',27,0),('ciphertext',73,1),('ciphertext',74,0)):
   row=next(x for x in r['rows'] if x['mode']==mode and x['alphabet']=='AZ' and x['sigma']==x['tau']==1 and x['lag_or_period']==L);self.assertEqual(row['minimum_substitutions'],cost)
