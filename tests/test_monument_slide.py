import collections,itertools,json,math,random,sys,unittest
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import monument_slide as s

def tiny():return {'width':3,'cipher_rows':['ABC','B?A'],'models':{'a':['AAB','BBA'],'b':[' B?','AAB']},'observed_anchor':{'fixed_cipher_raw_indices_for_conditional_null':[[0,1]]}}
class MonumentSlideTests(unittest.TestCase):
 def test_complete_source_and_observed_registration(self):
  m=s.Model();self.assertEqual((m.w,m.h),(33,28));self.assertEqual(len(m.frames),134);self.assertEqual(sum(f['active'] for f in m.frames),130)
  C=[''.join(s.SYMBOLS[x] for x in m.base[r*33:(r+1)*33]) for r in range(28)];T=[''.join(s.SYMBOLS[x] for x in m.targets['OBSERVED_RENDER33'][r*33:(r+1)*33]) for r in range(28)]
  self.assertEqual(''.join(row[1] for row in C[:5]),'MYVGT');self.assertEqual(''.join(row[1] for row in T[:5]),'AABCD');self.assertEqual(C[0][0],'E')
  k4=[p for p in m.cmeta if p['k4_position'] is not None];self.assertEqual([p['k4_position'] for p in k4],list(range(1,98)));self.assertEqual(''.join(p['character'] for p in k4),json.loads((ROOT/'data/k4.json').read_text())['ciphertext'])
 def test_independent_coordinate_and_pixel_oracle_every_tiny_shift(self):
  m=s.Model(tiny());records=m.actual()
  for f,r in zip(m.frames,records):
   target=m.targets[f['model']];pairs=[]
   for row in range(m.h):
    for j in range(m.w):
     common_front=m.w-1-j;folded=m.w-1-common_front;x=folded+f['shift']
     if 0<=x<m.w:pairs.append((row*m.w+x,row*m.w+j))
   pairs.sort();self.assertEqual(pairs,f['pairs']);match=area=0
   for i,j in pairs:
    a,b=m.base[i],target[j];match+=a==b and a<26
    A,B=m.masks[a],m.masks[b]
    for bit in range(35):area+=bool(A>>bit&1) and bool(B>>bit&1)
   self.assertEqual(r['label_matches'],match);self.assertEqual(r['common_pixel_area'],area)
 def test_exact_expectation_against_exhaustive_conditional_nulls(self):
  m=s.Model(tiny())
  for scheme in ('shuffle','rotation'):
   variants=[]
   for positions in m.free:
    values=tuple(m.base[i] for i in positions)
    variants.append(sorted(set(itertools.permutations(values))) if scheme=='shuffle' else [values[k:]+values[:k] for k in range(len(values))])
   results=[]
   for rows in itertools.product(*variants):
    source=m.base[:]
    for positions,values in zip(m.free,rows):
     for i,v in zip(positions,values):source[i]=v
    results.append(m.scores(source))
   for i,frame in enumerate(m.frames):
    self.assertEqual(Fraction(sum(row[i]//s.SCALE for row in results),len(results)),Fraction(frame['expected_rational'][0]));self.assertEqual(Fraction(sum(row[i]%s.SCALE for row in results),len(results)),Fraction(frame['expected_rational'][1]))
 def test_null_family_seed_replay_and_fixed_structure(self):
  m=s.Model(tiny());actual=m.actual()
  for scheme in ('shuffle','rotation'):
   rng=random.Random(7)
   for _ in range(20):
    values=m.surrogate(rng,scheme)
    for i,x in enumerate(m.base):
     if i in m.fixed or x>=26:self.assertEqual(values[i],x)
    for row in m.free:self.assertEqual(collections.Counter(values[i] for i in row),collections.Counter(m.base[i] for i in row))
   a=s.nulls(m,actual,scheme,n=19,seed=7);b=s.nulls(m,actual,scheme,n=19,seed=7);a.pop('seconds');b.pop('seconds');self.assertEqual(a,b)
   for f in a['per_frame']:
    for p in f['endpoints'].values():
     if p:self.assertGreaterEqual(p['family_max_plus_one_p'],p['raw_plus_one_p']);self.assertGreaterEqual(p['four_report_adjusted_p'],p['family_max_plus_one_p']);self.assertGreaterEqual(p['raw_plus_one_p'],1/20)
 def test_double_reflection_same_facing_and_partial_overlap(self):
  masks=s.glyph_masks()
  for mask in masks:self.assertEqual(s.mirror(s.mirror(mask)),mask)
  F=masks[s.SYMBOLS.index('F')];E=masks[s.SYMBOLS.index('E')];self.assertNotEqual(s.mirror(F),F);self.assertGreater(s.pop(F&E),0);self.assertNotEqual(F,E);self.assertEqual(F&F,F)
 def test_planted_translation_and_no_wrap_endpoints(self):
  m=s.Model({'width':3,'cipher_rows':['AAA','BBB'],'models':{'same':['AAA','BBB']}});r={x['shift']:x for x in m.actual()};self.assertEqual(r[0]['label_matches'],6);self.assertEqual(r[1]['label_matches'],4)
  for shift in (-3,3):self.assertEqual(r[shift]['geometric_overlap_cells'],0);self.assertEqual(r[shift]['common_pixel_area'],0);self.assertIsNone(r[shift]['common_over_union'])
