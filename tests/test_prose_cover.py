import collections,itertools,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import prose_cover as p

def brute(v,n,known,pos=0,words=()):
 if pos==n:yield words;return
 for w in v:
  if pos+len(w)<=n and all(not(pos<=i<pos+len(w)) or w[i-pos]==c for i,c in known.items()):yield from brute(v,n,known,pos+len(w),words+(w,))

def direct(cipher,primer,alphabet,equation):
 sig,tau=p.ak.COEFFICIENTS[equation];out=[];lag=len(primer);m=len(alphabet)
 for i,ch in enumerate(cipher):
  key=alphabet.index(primer[i]) if i<lag else alphabet.index(out[i-lag]);out.append(alphabet[sig*(alphabet.index(ch)-tau*key)%m])
 return ''.join(out)
class ProseCoverTests(unittest.TestCase):
 def test_complete_mask_paths_and_all_selectors(self):
  v={'A','B','AA','AB','BA','ABA'}
  for n in range(1,8):
   for known in ({},{0:'A'},{n-1:'B'},{0:'B',n-1:'A'}):
    words=list(brute(v,n,known));h=p.mask_hist(n,known,v)
    for k in range(1,5):
     for N,phase in ((1,0),(2,0),(2,1)):
      valid=[w for w in words if all(len(x)>=k for j,x in enumerate(w) if j%N==phase)];d=p.distribution(h,k,N,phase);self.assertEqual(d['total'],len(valid));self.assertEqual(d['coverwords'],dict(collections.Counter(map(len,valid))));self.assertEqual(d['output_lengths'],dict(collections.Counter(sum(j%N==phase for j in range(len(w))) for w in valid)))
 def test_complete_root_spaces_independent_literal_primers(self):
  alphabet='ABC'
  for equation in p.ak.COEFFICIENTS:
   for lag in (2,3):
    for cipher in ('ABCAABBC','CCCCABAB'):
     for known in ({},{0:'A'},{0:'A',3:'B'},{0:'A',2:'B',5:'C'}):
      expected={direct(cipher,''.join(key),alphabet,equation) for key in itertools.product(alphabet,repeat=lag)};expected={plain for plain in expected if all(plain[i]==v for i,v in known.items())};actual=list(p.plaintexts(cipher,known,alphabet,equation,lag));self.assertEqual(set(actual),expected);self.assertEqual(len(actual),len(expected))
      for plain in actual:
       primer=p.primer_for(cipher,plain,alphabet,equation,lag);self.assertEqual(direct(cipher,primer,alphabet,equation),plain)
 def test_word_crossings_and_compounds_are_not_forced(self):
  v={'EAST','NORTH','NORTHEAST','THE','ART','HEART','A','I'};text='EASTNORTHEAST';lex=p.Lexicon(v);d=p.distribution(lex.hist(text));self.assertEqual(d['coverwords'],{2:1,3:1});self.assertTrue(p.Lexicon({'HEART'}).accepts('HEART'));self.assertEqual(p.mask_hist(5,{2:'A',3:'R'}, {'HEART'})[0],{5:1})
 def test_selected_short_words_and_phase_continuity(self):
  h=p.Lexicon({'A','LONG','WORD'}).hist('ALONGWORD');self.assertEqual(p.distribution(h,4,1,0)['total'],0);self.assertEqual(p.distribution(h,4,2,1)['total'],1);self.assertEqual(p.distribution(h,4,2,0)['total'],0)
 def test_frozen_actual_root_domain_is_three_free(self):
  data=json.loads((ROOT/'data/k4.json').read_text());known={c['start']-1+j:ch for c in data['cribs'] for j,ch in enumerate(c['plaintext'])}
  for a in p.ALPHABETS.values():
   for e in p.ak.COEFFICIENTS:self.assertEqual(len(p.roots(data['ciphertext'],known,a,e,27)[3]),3)
 def test_literal_lexicon_extraction_and_witness(self):
  lex=p.Lexicon({'A','AA','B','AB','BA'});
  for text in ('ABA','AAAB','BBB','C'):
   words=list(brute(lex.words,len(text),dict(enumerate(text))));self.assertEqual(lex.accepts(text),bool(words));self.assertEqual(p.distribution(lex.hist(text))['total'],len(words))
   if words:self.assertIn(tuple(lex.witness(text)),words)
