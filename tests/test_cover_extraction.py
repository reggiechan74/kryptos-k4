import collections,json,random,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import cover_extraction as c
import cover_extraction_reference as ref
class CoverExtractionTests(unittest.TestCase):
 def test_tiny_complete_language_counts_and_independent_lattice(self):
  for runs in [(2,4,2),(3,4,2),(4,2,3)]:
   m=c.Model('tiny',['AA','AB','BA','BBA'],['AB'],['BA'],runs)
   for N,phase in [(1,0),(2,0),(2,1)]:
    for k in (1,2):
     truth=ref.brute_model(m,k,N,phase);lane=c.Lane(m,k,N,phase,'all');self.assertEqual(sum(truth.values()),m.distributions()['total'])
     for text,count in truth.items():self.assertEqual(lane.count(text),count);self.assertEqual(ref.count_message(m,text,k,N,phase),count)
     self.assertEqual(lane.count('ZZZZ'),0)
 def test_continuous_alternate_word_phase_and_too_short(self):
  self.assertEqual(c.extract(['EAST','NORTH','EAST','BERLIN','CLOCK'],1,2,0),'EEC');self.assertEqual(c.extract(['EAST','NORTH','EAST','BERLIN','CLOCK'],1,2,1),'NB')
  with self.assertRaises(ValueError):c.extract(['A','CLOCK'],2)
  self.assertEqual(c.extract(['A','CLOCK'],2,2,1),'L')
 def test_known_tokens_kth_letters_and_compound_ambiguity(self):
  a=['EAST','NORTH','EAST'];b=['BERLIN','CLOCK'];self.assertEqual([c.extract(a,k) for k in range(1,5)],['ENE','AOA','SRS','TTT']);self.assertEqual([c.extract(b,k) for k in range(1,5)],['BC','EL','RO','LC']);self.assertEqual(c.extract(['EAST','NORTHEAST']),'EN')
  self.assertEqual(set(c.decode_cover('EASTNORTHEAST',['EAST','NORTH','NORTHEAST'])),{('EAST','NORTH','EAST'),('EAST','NORTHEAST')})
 def test_integer_weighted_sampler_all_ticket_counts(self):
  class Ticket:
   def __init__(self,x):self.x=x
   def randrange(self,n):self.asserted=n;return self.x
  self.assertEqual(collections.Counter(c.weighted_choice(['A','B','C'],[2,3,1],Ticket(i)) for i in range(6)),dict(A=2,B=3,C=1))
 def test_model_masks_consume_real97_and_prefix_codes(self):
  rng=random.Random(330024);known=c.source_known(json.loads((ROOT/'data/k4.json').read_text()))
  for m in c.models():
   self.assertEqual(m.total,97);self.assertTrue(c.prefix_free(m.vocab));self.assertEqual(len(m.vocab),30 if m.name.startswith('A30') else 26)
   words=m.sample(rng);cover=''.join(words);self.assertEqual(len(cover),97);self.assertTrue(all(cover[i]==x for i,x in known.items()));self.assertEqual(c.decode_cover(cover,m.vocab),[tuple(words)])
   for lane in m.lanes():
    if lane.stratum=='15' and len(words)!=15:continue
    text=c.extract(words,lane.k,lane.N,lane.phase);self.assertGreater(lane.count(text),0);self.assertEqual(lane.count(text),ref.count_message(m,text,lane.k,lane.N,lane.phase))
