"""Static target evidence assertions; no decoding, source imports or replay."""
from pathlib import Path
import json,hashlib,unittest
R=Path(__file__).resolve().parents[1];D=R/'research/c20-successor-queue-v1/target'
class C20Target(unittest.TestCase):
 def test_exact_package(self):
  for name,row in json.loads((D/'MANIFEST.json').read_text())['files'].items():
   b=(D/name).read_bytes();self.assertEqual(len(b),row['bytes']);self.assertEqual(hashlib.sha256(b).hexdigest(),row['sha256'])
 def test_stored_masks_and_scope(self):
  x=json.loads((D/'TARGET-RESULT.json').read_text());self.assertEqual(x['conclusion'],'EXACT_SEVEN_PHASE_MODEL_NEGATIVE');self.assertEqual(x['compatible_phases'],[]);self.assertEqual(x['candidate_count'],7);self.assertEqual([z['clue_matches'] for z in x['records']],[2,1,1,1,0,0,0])
  for row in x['records']:self.assertEqual(sum(row['clue_mask']),row['clue_matches']);self.assertEqual(len(row['plaintext']),97);self.assertTrue(row['reference_agreement']);self.assertTrue(row['full_reencryption']);self.assertFalse(row['compatible'])
 def test_current_frontier_closed(self):
  x=json.loads((R/'research/specifications/FRONTIER-CURRENT-20261101-C20-CLOSED.json').read_text());self.assertEqual(x['expected_register_entries'],70);g=next(z for z in x['gates'] if z['id']=='F-C20-CLOSED');self.assertFalse(g['ready_for_new_K4_evaluation']);self.assertIsNone(g['safe_replay_argv'])
