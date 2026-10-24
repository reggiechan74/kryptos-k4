import json,sys,unittest,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import verify_projection_v17_handoff as v
class CorrectedProjectionArchiveTests(unittest.TestCase):
 def test_exact_delta_and_full_feature_integrity(self):
  r=json.loads((ROOT/'results/SITE-PROJECTION-V17-SOURCE-HANDOFF.json').read_text());self.assertEqual(v.verify(),r['static_checks']);self.assertTrue(r['static_checks']['full_feature_equals_v16_plus_delta']);self.assertEqual(len(r['static_checks']['changed_paths']),7);self.assertFalse(r['JavaScript_executed_here']);self.assertEqual(r['owner_reported_tests'],107)
 def test_original_version16_archive_remains_immutable(self):
  paths=subprocess.check_output(['git','ls-tree','-r','--name-only','d157fa4d1aa7113ac6a313828826e8708d8e1094','--','docs/site-source/projection-20261024'],cwd=ROOT,text=True).splitlines()
  for path in paths:self.assertEqual((ROOT/path).read_bytes(),subprocess.check_output(['git','show','d157fa4d1aa7113ac6a313828826e8708d8e1094:'+path],cwd=ROOT),path)
