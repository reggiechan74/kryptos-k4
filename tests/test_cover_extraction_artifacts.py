import collections,gzip,hashlib,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import cover_extraction as c
class CoverArtifactTests(unittest.TestCase):
 def test_original_input_hashes_and_counts(self):
  r=json.loads((ROOT/'results/COVER-EXTRACTION-033-ORIGINAL.json').read_text());self.assertEqual(r['actual_K4_cipher_trials'],0)
  for path,sha in r['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),sha)
  by={x['id']:x for x in r['models']};self.assertEqual(by['A30-ENE']['distribution']['total'],158540149214580072342);self.assertEqual(by['R26-ENE']['distribution']['total'],27493275220775879424);self.assertEqual(by['A30-ENE']['distribution']['counts']['15'],3787080);self.assertNotIn('15',by['R26-ENE']['distribution']['counts']);self.assertEqual(r['strict_NATO_unanchored_counts'],{})
 def test_complete_corpus_and_independent_positive_audit(self):
  r=json.loads((ROOT/'results/COVER-PHRASE-034-original-summary.json').read_text());a=json.loads((ROOT/'results/COVER-PHRASE-034-INDEPENDENT-AUDIT.json').read_text());self.assertTrue(r['corpus']['complete']);self.assertEqual(len(r['corpus']['member_hashes']),500);self.assertEqual(r['corpus']['counts']['all_windows_2_to_5'],2673853);self.assertTrue(a['complete']);self.assertEqual(a['unique_message_lane_counts_verified'],7266)
  for path,sha in r['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),sha)
 def test_all_matched_records_union_and_lane_counts(self):
  r=json.loads((ROOT/'results/COVER-PHRASE-034-original-summary.json').read_text());path=ROOT/'results/COVER-PHRASE-034-original-windows.jsonl.gz';self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),r['corpus']['output_sha256']);counts=collections.Counter();seen=set();n=0
  with gzip.open(path,'rt') as f:
   for line in f:
    x=json.loads(line);n+=1;seen.add(x['source']['joined_sha256']);mask=0
    for i,value in x['cover_counts'].items():self.assertGreater(value,0);mask|=1<<int(i);counts[r['lanes'][int(i)]['id']]+=1
    self.assertEqual(mask,int(x['model_bitmask']))
  self.assertEqual(n,6358);self.assertEqual(len(seen),3139);self.assertEqual(dict(counts),r['corpus']['matched_occurrences_by_lane']);s=json.loads((ROOT/'results/COVER-PHRASE-034-MESSAGE-SPLITS.json').read_text());self.assertEqual(s['unique_spaced_phrases'],3147)
 def test_null_controls_whole_family_and_global_word_phase(self):
  r=json.loads((ROOT/'results/COVER-PHRASE-034-original-summary.json').read_text());d=json.load(gzip.open(ROOT/'results/COVER-PHRASE-034-original-controls.json.gz','rt'));known=c.source_known(json.loads((ROOT/'data/k4.json').read_text()));events=0;branchA=0
  for draw in d['draws']:
   event=False
   for row in draw['records']:
    cover=row['cover'];self.assertEqual(len(cover),97);self.assertTrue(all(cover[i]==v for i,v in known.items()));self.assertEqual(c.extract(row['coverwords'],row['k'],row['N'],row['phase']),row['output'])
    if row['stratum']=='15':self.assertEqual(len(row['coverwords']),15)
    event|=row['branch_A_member'] or row['branch_B']['total']>0
   events+=event;branchA+=any(x['branch_A_member'] for x in draw['records']);self.assertEqual(event,draw['any_family_match'])
  self.assertEqual(len(d['draws']),31);self.assertEqual(events,24);self.assertEqual(branchA,0)
 def test_original_initials_and_exact15_corpus_results_are_separate(self):
  r=json.loads((ROOT/'results/COVER-PHRASE-034-original-summary.json').read_text());lanes={x['id']:x for x in r['lanes']};counts=r['corpus']['matched_occurrences_by_lane'];self.assertEqual(sum(v for k,v in counts.items() if lanes[k]['N']==1 and lanes[k]['k']==1),0);self.assertEqual(sum(v for k,v in counts.items() if lanes[k]['N']==1 and lanes[k]['stratum']=='15'),0);self.assertEqual(sum(v for k,v in counts.items() if lanes[k]['N']==1),1)
 def test_same_initial_same_length_alias_is_not_unique_message(self):
  middle=['NOVEMBER','FOXTROT','FOXTROT','FOXTROT'];suffix=['NOVEMBER','NOVEMBER','FOXTROT'];words=['ECHO','BRAVO','BERLIN','SIERRA','EAST','NORTH','EAST']+middle+['BERLIN','CLOCK']+suffix;other=['EAST']+words[1:];self.assertEqual(len(''.join(words)),97);self.assertNotEqual(words,other);self.assertEqual(c.extract(words),c.extract(other))
