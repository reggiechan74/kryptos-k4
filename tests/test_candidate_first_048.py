import hashlib,json,sys,unittest,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import candidate_first_048 as c
class CandidateFirst048Tests(unittest.TestCase):
 def test_complete_tiny_source_plaintext_key_relations(self):
  r=c.controls();self.assertEqual(r['complete_tiny_source_key_plaintext_relations'],3612);self.assertGreater(r['complete_admitted_pairs'],0)
 def test_actual_preflight_not_free_key_or_generated_message_evidence(self):
  r=json.loads((ROOT/'results/CANDIDATE-FIRST-048-ORIGINAL.json').read_text());self.assertEqual(r['actual']['model_descriptions'],582);self.assertEqual(r['actual']['structurally_compatible_models'],42);self.assertEqual(r['actual']['distinct_compatible_full_plaintexts'],0);self.assertEqual(r['candidate_bank_generated'],0);self.assertFalse(r['unrestricted_candidate_first_exhausted']);self.assertEqual(len(r['plants']),24);self.assertTrue(all(p['true_key_recovered'] and p['all97_ciphertext_regenerated'] for p in r['plants']));self.assertEqual(len(r['nulls']),31);self.assertTrue(all(x['complete'] and x['distinct_compatible_full_plaintexts']==0 for x in r['nulls']))
 def test_frozen_inputs_and_exact_cross_version_replay(self):
  r=json.loads((ROOT/'results/CANDIDATE-FIRST-048-CONTROLLED.json').read_text());v=json.loads((ROOT/'results/CANDIDATE-FIRST-048-CONTROLLED-REPLAY.json').read_text())
  for row in (r,v):row.pop('started_at_utc');row.pop('finished_at_utc')
  self.assertEqual(r,v)
  for name,h in r['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),h)

 def test_full_source_lookup_plants_and_prior044_crosscheck(self):
  r=json.loads((ROOT/'results/CANDIDATE-FIRST-048-CONTROLLED.json').read_text());old=json.loads((ROOT/'results/CANDIDATE-FIRST-048-ORIGINAL.json').read_text())
  self.assertEqual(r['actual'],old['actual']);self.assertEqual(r['nulls'],old['nulls']);self.assertEqual(r['source'],old['source'])
  self.assertEqual(len(r['plants']),24)
  for plant in r['plants']:
   self.assertTrue(plant['actual_compatible_source_called']);self.assertTrue(plant['all_source_aliases_retained']);self.assertEqual(plant['source_coordinate_recovered'],['brown/ca01',0]);self.assertGreater(plant['admissible_source_occurrences'],0)
   if plant['model']['mode']=='ciphertext':self.assertEqual(plant['admissible_source_occurrences'],4743928);self.assertGreater(plant['admissible_distinct_keys'],1)
  cross=r['structural_crosscheck_044'];self.assertEqual(cross['comparable_models'],576);self.assertEqual(cross['explicit_periodic_sign_relabel_aliases'],64);self.assertEqual(cross['compatible_models'],36);self.assertTrue(cross['all_structural_viability_and_compatible_free_counts_equal'])
 def test_exact_compact_source_positions_and_old_control_receipt_history(self):
  coords=c.SourceCoordinates(('first','second'));coords.append(0,0);coords.append(1,2**32-1);coords.append(0,19);self.assertEqual(list(coords),[['first',0],['second',2**32-1],['first',19]]);self.assertEqual(len(coords),3)
  with self.assertRaises(ValueError):coords.append(0,2**32)
  old=json.loads((ROOT/'results/CANDIDATE-FIRST-048-ORIGINAL.json').read_text())
  for name,h in old['source_sha256'].items():self.assertEqual(hashlib.sha256(subprocess.check_output(['git','show','1cef25a:'+name],cwd=ROOT)).hexdigest(),h)
