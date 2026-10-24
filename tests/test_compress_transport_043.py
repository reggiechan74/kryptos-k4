import hashlib,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import compress_transport_043 as c
class CompressTransport043Tests(unittest.TestCase):
 def test_complete_actual_header_failure_and_original_scope(self):
  r=json.loads((ROOT/'results/COMPRESS-TRANSPORT-043-ORIGINAL.json').read_text());self.assertEqual(r['actual_K4_transport_descriptions'],8);self.assertEqual(r['actual']['header_survivors'],0);self.assertEqual(r['actual']['full_candidates'],0);self.assertTrue(all(x['decoded_bytes']==57 for x in r['actual']['records']));self.assertEqual(r['additional_cipher_layers_tested'],0)
  for path,sha in r['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),sha)
 def test_all_recorded_plants_have_independent_decoder_and_full_transport_replay(self):
  r=json.loads((ROOT/'results/COMPRESS-TRANSPORT-043-ORIGINAL.json').read_text());self.assertEqual(r['controls']['integer_reference_roundtrips'],2040);self.assertEqual(c.short_lzw(bytes.fromhex('1f9d904100')),b'A');self.assertEqual(len(r['controls']['plants']),4)
  for p in r['controls']['plants']:
   raw=bytes.fromhex(p['compressed_hex']);self.assertEqual(c.short_lzw(raw).decode(),p['plaintext']);self.assertEqual(len(p['records']),8)
   for v in p['records']:
    a=c.ALPHABETS[v['alphabet']];b=v['bijective'];rev=v['reversed_letters'];self.assertEqual(c.decode(v['ciphertext'],a,b,rev),raw);self.assertEqual(c.reference_decode(v['ciphertext'],a,b,rev),raw);self.assertEqual(c.encode(raw,a,b,rev),v['ciphertext']);self.assertIn(p['plaintext'],[x['plaintext'] for x in v['full_selector']['candidates']])
 def test_entire_null_selector_and_canonical_notation(self):
  import collections
  r=json.loads((ROOT/'results/COMPRESS-TRANSPORT-043-ORIGINAL.json').read_text());original=json.loads((ROOT/'data/k4.json').read_text())['ciphertext'];self.assertEqual(len(r['nulls']['records']),31)
  for row in r['nulls']['records']:self.assertEqual(collections.Counter(row['ciphertext']),collections.Counter(original));self.assertEqual(row['search']['transport_versions'],8);self.assertEqual(row['search']['full_candidates'],0)
  with self.assertRaises(ValueError):c.decode('AB',c.ALPHABETS['AZ'])
  with self.assertRaises(ValueError):c.encode(b'\0ABC',c.ALPHABETS['AZ'])
