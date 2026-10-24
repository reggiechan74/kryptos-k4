import gzip,hashlib,json,random,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import hand_grammar_050 as h
import finite_hand_operators as f
class FixedKeyGrammar050Tests(unittest.TestCase):
 def test_primitives_and_small_complete_action_reference(self):
  prim=[dict(op=o,aliases=[d]) for d,o in f.primitives()];r=h.controls(prim);self.assertEqual(r['complete_small_alphabet_input_composition_checks'],6080);self.assertEqual(r['all_primitive_input_symbol_checks'],988);self.assertEqual({len(d['key']) for d,_ in f.primitives() if d['kind']=='columnar'},{7,8,10});self.assertEqual(len(prim),38);self.assertTrue(all(x['forward_exact'] for x in r['historical_known_answers']))
 def test_every_descriptor_retained_with_exact_canonical_operator(self):
  raw=gzip.decompress((ROOT/'results/HAND-GRAMMAR-050-CATALOGUE.json.gz').read_bytes());rows=json.loads(raw);r=json.loads((ROOT/'results/HAND-GRAMMAR-050-ORIGINAL.json').read_text());self.assertEqual(hashlib.sha256(raw).hexdigest(),r['catalogue_uncompressed_sha256']);self.assertEqual(len(rows),27323);words=[];sigs=[];rng=random.Random(50099);sample=bytes(rng.randrange(26) for _ in range(97))
  for row in rows:
   rawsig=bytes.fromhex(row['signature_hex']);self.assertEqual(len(rawsig),195);p=rawsig[:97];s=1 if rawsig[97]==1 else -1;b=rawsig[98:];self.assertEqual(sorted(p),list(range(97)));op=(p,s,b);self.assertEqual(f.apply(f.apply(sample,op),f.invert(op)),sample);sigs.append(rawsig);words.extend(map(tuple,row['aliases']))
  self.assertEqual(len(set(sigs)),27323);self.assertEqual(len(words),56355);self.assertEqual(len(set(words)),56355);self.assertEqual({len(w) for w in words},{0,1,2,3});self.assertTrue(all(all(0<=i<38 for i in w) for w in words))
  allsig=set(sigs)
  for rawsig in sigs:
   op=(rawsig[:97],1 if rawsig[97]==1 else -1,rawsig[98:]);self.assertIn(f.signature(f.invert(op)),allsig)
 def test_composition_output_index_convention(self):
  vector=bytes(range(26))*3+bytes(range(19));atoms=f.primitives()
  for i,j in ((0,11),(4,36),(25,37),(38-1,38-2)):
   first,second=atoms[i][1],atoms[j][1];self.assertEqual(f.apply(vector,f.compose(first,second)),h.reference(h.reference(vector,atoms[i][0]),atoms[j][0]))
 def test_actual_scoped_negative_and_whole_selector_plants_replay(self):
  r=json.loads((ROOT/'results/HAND-GRAMMAR-050-ORIGINAL.json').read_text());v=json.loads((ROOT/'results/HAND-GRAMMAR-050-REPLAY.json').read_text())
  for row in (r,v):row.pop('started_at_utc');row.pop('finished_at_utc')
  self.assertEqual(r,v);self.assertEqual(r['actual']['exact_operator_hits'],0);self.assertEqual(r['unique_operators'],27323);self.assertEqual(len(r['full_selector_plants']),43);self.assertTrue(all(x['full_selector_true_plaintext_recovered'] for x in r['full_selector_plants']));self.assertEqual(len(r['nulls']),31);self.assertFalse(r['unrestricted_keys_tested']);self.assertEqual(r['columnar_widths'],[7,10,8])
  for name,hsh in r['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),hsh)
