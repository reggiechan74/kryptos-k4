import hashlib,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import candidate_first_048 as c
class CandidateFirst048Tests(unittest.TestCase):
 def test_complete_tiny_source_plaintext_key_relations(self):
  r=c.controls();self.assertEqual(r['complete_tiny_source_key_plaintext_relations'],3612);self.assertGreater(r['complete_admitted_pairs'],0)
 def test_actual_preflight_not_free_key_or_generated_message_evidence(self):
  r=json.loads((ROOT/'results/CANDIDATE-FIRST-048-ORIGINAL.json').read_text());self.assertEqual(r['actual']['model_descriptions'],582);self.assertEqual(r['actual']['structurally_compatible_models'],42);self.assertEqual(r['actual']['distinct_compatible_full_plaintexts'],0);self.assertEqual(r['candidate_bank_generated'],0);self.assertFalse(r['unrestricted_candidate_first_exhausted']);self.assertEqual(len(r['plants']),24);self.assertTrue(all(p['true_key_recovered'] and p['all97_ciphertext_regenerated'] for p in r['plants']));self.assertEqual(len(r['nulls']),31);self.assertTrue(all(x['complete'] and x['distinct_compatible_full_plaintexts']==0 for x in r['nulls']))
 def test_frozen_inputs_and_exact_cross_version_replay(self):
  r=json.loads((ROOT/'results/CANDIDATE-FIRST-048-ORIGINAL.json').read_text());v=json.loads((ROOT/'results/CANDIDATE-FIRST-048-REPLAY.json').read_text())
  for row in (r,v):row.pop('started_at_utc');row.pop('finished_at_utc')
  self.assertEqual(r,v)
  for name,h in r['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),h)
