import itertools,sys,unittest,random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import cover_phrase as p
import cover_extraction as c
import cover_extraction_reference as ref
class CoverPhraseTests(unittest.TestCase):
 def test_tokens_break_not_silently_deleted(self):
  t=p.parse_line("I/ppss can/md go/vb ./ ./. A/at X/nn had/vbd a/at well-known/jj book/nn")
  self.assertEqual(t,['I','CAN','GO',None,None,'A',None,'HAD','A',None,'BOOK']);self.assertEqual(list(p.windows(t)),[(0,2,('I','CAN')),(0,3,('I','CAN','GO')),(1,2,('CAN','GO')),(7,2,('HAD','A'))])
 def test_all_window_counts_and_word_limits(self):
  for n in range(9):self.assertEqual(len(list(p.windows(['WORD']*n))),sum(max(0,n-k+1) for k in range(2,6)))
 def test_all_split_counts_against_cut_enumeration(self):
  vocab={'A','I','AI','IA','AA','II'}
  for length in range(1,8):
   for letters in itertools.product('AI',repeat=length):
    text=''.join(letters);truth=0
    for n in range(2,6):
     for cuts in itertools.combinations(range(1,length),n-1):
      pts=(0,)+cuts+(length,)
      truth+=all(text[a:b] in vocab for a,b in zip(pts,pts[1:]))
    self.assertEqual(p.split_message(text,vocab)['total'],truth)
 def test_constructive_witness_and_global_selection(self):
  rng=random.Random(340024)
  for m in c.models():
   words=m.sample(rng)
   for N,phase in [(1,0),(2,0),(2,1)]:
    for k in range(1,5):
     y=c.extract(words,k,N,phase);lane=c.Lane(m,k,N,phase,'all');got=p.construct_cover(lane,y);self.assertIsNotNone(got);self.assertEqual(c.extract(got,k,N,phase),y);self.assertEqual(ref.count_message(m,y,k,N,phase),lane.count(y))
 def test_corpus_hash_gate(self):
  import tempfile
  with tempfile.NamedTemporaryFile() as f:
   f.write(b'not the frozen corpus');f.flush()
   with self.assertRaisesRegex(ValueError,'hash mismatch'):p.validate_brown(f.name)
