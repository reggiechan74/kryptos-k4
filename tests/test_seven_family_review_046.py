import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class SevenFamilyReviewTests(unittest.TestCase):
 def test_all_branches_have_explicit_limits_and_evidence(self):
  r=json.loads((ROOT/'research/specifications/SEVEN-FAMILY-REVIEW-046.json').read_text())
  self.assertEqual(len(r['family_order']),7);self.assertEqual(len(r['subbranches']),34)
  self.assertEqual({x['family'] for x in r['subbranches']},set(range(1,8)))
  self.assertEqual(len({x['id'] for x in r['subbranches']}),34)
  self.assertFalse(r['broad_families_exhausted']);self.assertFalse(r['puzzle_solved']);self.assertTrue(r['new_results_local_only'])
  for b in r['subbranches']:
   self.assertFalse(b['whole_family_excluded'])
   for field in ('status','coverage','missing_input','next_discriminating_work'):self.assertTrue(b[field])
   self.assertTrue(b['evidence'])
   for path in b['evidence']:self.assertTrue((ROOT/path).is_file(),path)

 def test_clock_mapping_cardinality_has_the_correct_direction(self):
  injection={i:i for i in range(24)}
  self.assertEqual(len(set(injection.values())),24);self.assertTrue(set(injection.values())<set(range(26)))
  self.assertEqual(len({i%24 for i in range(26)}),24)
  r=json.loads((ROOT/'research/specifications/SEVEN-FAMILY-REVIEW-046.json').read_text());b=next(x for x in r['subbranches'] if x['id']=='F5-KEY')
  self.assertIn('can inject into 26',b['coverage']);self.assertIn('cannot bijectively cover',b['coverage'])
 def test_feasible_photo_attempt_is_recorded_without_claiming_physical_completion(self):
  r=json.loads((ROOT/'research/specifications/SEVEN-FAMILY-REVIEW-046.json').read_text());b=next(x for x in r['subbranches'] if x['family']==3 and x['branch']=='Actual curved copper transmission/projection')
  self.assertEqual(b['status'],'partially_tested');self.assertTrue(b['feasible_follow_up_status'].startswith('attempted:'));self.assertIn('zero certified',b['coverage'])
