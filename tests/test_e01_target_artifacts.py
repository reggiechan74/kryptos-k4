"""Static E01 result/provenance checks; no cipher imports or target replay."""
from pathlib import Path
import hashlib,json,unittest,zipfile
R=Path(__file__).resolve().parents[1];D=R/'research/e01-conditional-alphabet-v1/target-v1'
class E01Target(unittest.TestCase):
 def test_exact_public_files_and_archive_members(self):
  for name,row in json.loads((D/'MANIFEST.json').read_text())['files'].items():
   b=(D/name).read_bytes();self.assertEqual(len(b),row['bytes']);self.assertEqual(hashlib.sha256(b).hexdigest(),row['sha256'])
  with zipfile.ZipFile(D/'e01-target-evidence.zip') as z:
   m=json.loads(z.read('e01-target/PUBLIC-MEMBER-MANIFEST.json'));self.assertEqual(set(z.namelist()),{'e01-target/'+n for n in m}|{'e01-target/PUBLIC-MEMBER-MANIFEST.json'})
   for name,row in m.items():
    b=z.read('e01-target/'+name);self.assertEqual(len(b),row['bytes']);self.assertEqual(hashlib.sha256(b).hexdigest(),row['sha256'])
 def test_stored_single_candidate_negative(self):
  with zipfile.ZipFile(D/'e01-target-evidence.zip') as z:o=json.loads(z.read('e01-target/results/REPORT.json'))
  self.assertEqual(o['status'],'COMPLETE_ONE_CANDIDATE');self.assertEqual(o['outcome'],'EXACT_INCOMPATIBLE');self.assertEqual(o['candidate_count'],1);self.assertEqual(len(o['candidates']),1);c=o['candidates'][0];self.assertEqual(c['clue_mask'],[False]*24);self.assertEqual(c['clue_matches'],0);self.assertEqual(c['plaintext'],c['reference_plaintext']);self.assertEqual(len(c['plaintext']),97);self.assertTrue(c['production_full_reencryption']);self.assertTrue(c['reference_full_reencryption']);self.assertTrue(c['reference_agreement'])
 def test_current_inventory_and_gate(self):
  x=json.loads((R/'research/specifications/FRONTIER-CURRENT-20261101-E01-CLOSED.json').read_text());self.assertEqual(x['expected_register_entries'],71);g=next(z for z in x['gates'] if z['id']=='F-E01-CLOSED');self.assertFalse(g['ready_for_new_K4_evaluation']);self.assertIsNone(g['safe_replay_argv'])
