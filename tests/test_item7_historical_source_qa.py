import hashlib,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import item7_historical_source_qa as qa

class HistoricalSourceQATests(unittest.TestCase):
 def test_partial_strip_figure_without_invented_permutation_repair(self):
  d=qa.m138_figure();self.assertEqual(d['verified_permutations'],24);self.assertFalse(d['complete_inventory_admitted']);self.assertEqual(d['computed_ciphertext'],'VMIZKKJGFCDWVMKHYYXIATMCC');self.assertEqual(d['source_occurrence_from_figure'],24)
  self.assertEqual(d['unresolved_strip_literal'].count('O'),2);self.assertNotIn('Q',d['unresolved_strip_literal']);self.assertEqual(len(d['trace']),25)
 def test_historical_wheatstone_preserves_source_conflict_and_occlusion(self):
  d=qa.partial_wheatstone();self.assertEqual(d['computed_ciphertext'],'XZAABGQAM');self.assertEqual(d['preserved_conflicting_forward_string'],'XZZZBGQAM');self.assertIn('?',d['preserved_partial_inner']);self.assertFalse(d['occluded_slot_used']);self.assertFalse(d['inferred_completion_visually_authenticated']);self.assertTrue(d['production_engine_matches_with_explicit_inferred_completion'])
 def test_original_script_arithmetic_replay_is_explicit_about_binary_metadata(self):
  d=qa.replay_original();self.assertTrue(d['arithmetic_receipt_equal']);self.assertFalse(d['source_pdf_binary_rehashed_locally']);self.assertTrue(d['original_source_unchanged']);self.assertEqual(len(d['adapter_changes']),3)
 def test_first_crib_source_conditioned_proof_and_public_second_witness(self):
  d=qa.source_conditioned_certificate();self.assertTrue(d['first_crib_sufficient']);self.assertEqual(d['first_witness']['position'],33);self.assertEqual(d['additional_public_fixed_point']['position'],74);self.assertEqual(d['inventory_enumerations'],0);self.assertFalse(d['full_M138A_inventory_authenticated'])
 def test_supplied_artifacts_are_pinned_without_missing_binary_claim(self):
  manifest=json.loads((qa.SOURCE/'RECEIPT.json').read_text())
  for name,row in manifest['files'].items():self.assertEqual(hashlib.sha256((qa.SOURCE/name).read_bytes()).hexdigest(),row['sha256'])
  saved=json.loads((ROOT/'results/ITEM7-HISTORICAL-SOURCE-QA-027.json').read_text())
  self.assertEqual(saved['m138'],qa.m138_figure());self.assertEqual(saved['wheatstone'],qa.partial_wheatstone());self.assertEqual(saved['original_script_replay'],qa.replay_original())
 def test_primary_visual_review_is_scoped_and_no_private_images_committed(self):
  d=json.loads((ROOT/'results/ITEM7-LOCAL-SOURCE-REVIEW.json').read_text());self.assertTrue(d['srh366']['locally_downloaded']);self.assertEqual(d['srh366']['physical_pages_visually_inspected'],[101,102]);self.assertEqual(d['srh366']['sha256'],'d2165cd0558a4697ed99954da6184a11cc1ee7d82f46c4dfda82f19f2b8f8d73');self.assertFalse(d['nsa_a67592']['local_visual_inspection']);self.assertTrue(d['srh366']['private_original_not_committed'])
