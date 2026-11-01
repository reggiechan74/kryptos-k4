"""Static retained E02 target evidence only; no cipher import/replay."""
import hashlib,json,unittest,zipfile
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'research/e02-reference-cursor-v1/target-v1'
class E02Target(unittest.TestCase):
 def test_package_and_member_hashes(self):
  for n,h in json.loads((D/'MANIFEST.json').read_text()).items():self.assertEqual(hashlib.sha256((D/n).read_bytes()).hexdigest(),h)
  with zipfile.ZipFile(D/'e02-target-evidence.zip') as z:
   m=json.loads((D/'EVIDENCE-INDEX.json').read_text())['archive_members'];self.assertEqual(set(z.namelist()),set(m))
   for n,h in m.items():self.assertEqual(hashlib.sha256(z.read(n)).hexdigest(),h)
 def test_stored_fixed_candidate(self):
  with zipfile.ZipFile(D/'e02-target-evidence.zip') as z:o=json.loads(z.read('target/result/REPORT.json'))
  self.assertEqual(o['candidate_count'],1);self.assertEqual(o['outcome'],'EXACT_INCOMPATIBLE');self.assertEqual(len(o['candidates']),1);c=o['candidates'][0];self.assertEqual(c['clue_mask'],[False]*24);self.assertEqual(c['clue_matches'],0);self.assertEqual(c['plaintext'],c['reference_plaintext']);self.assertEqual(len(c['plaintext']),97);self.assertEqual(c['production_reencrypted_ciphertext'],c['reference_reencrypted_ciphertext']);self.assertTrue(c['production_full_reencryption']);self.assertTrue(c['reference_full_reencryption'])
  for k in ('production_final_state','reference_final_state','production_reencryption_final_state','reference_reencryption_final_state'):self.assertEqual(c[k],756)
 def test_current_closed_gate(self):
  j=json.loads((R/'research/specifications/FRONTIER-CURRENT-20261101-E02-CLOSED.json').read_text());self.assertEqual(j['expected_register_entries'],72);g=next(x for x in j['gates'] if x['id']=='F-E02-CLOSED');self.assertFalse(g['ready_for_new_K4_evaluation']);self.assertIsNone(g['safe_replay_argv'])
