import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import verify_manual_overlay_handoff as v
class ManualOverlayArchiveTests(unittest.TestCase):
 def test_static_archive_copies_and_full_column_oracle(self):
  r=json.loads((ROOT/'results/SITE-MANUAL-FOLD-V15-SOURCE-HANDOFF.json').read_text());self.assertEqual(v.verify(),r['static_checks']);self.assertEqual(r['static_checks']['offline_column_records_equal'],134);self.assertEqual(len(r['static_checks']['patch_paths']),25);self.assertEqual(len(r['static_checks']['new_git_blobs']),18);self.assertFalse(r['static_checks']['handed_off_JavaScript_executed'])
 def test_paths_modes_and_corrupted_member_bytes_are_rejected(self):
  raw=(v.ARCHIVE/'site-source.patch').read_bytes()
  for changed in (raw.replace(b'a/FOLD_OVERLAY_HANDOFF.md b/FOLD_OVERLAY_HANDOFF.md',b'a/../escape b/../escape',1),raw.replace(b'new file mode 100644',b'new file mode 120000',1),raw.replace(b'+# Manual fold overlay',b'+# Altered fold overlay',1)):
   with self.assertRaises(ValueError):v.patch_members(changed)
 def test_owner_live_status_and_QA_attribution_remain_distinct(self):
  r=json.loads((ROOT/'results/SITE-MANUAL-FOLD-V15-SOURCE-HANDOFF.json').read_text());self.assertEqual(r['deployment']['status'],'live');self.assertEqual(r['deployment']['version'],15);self.assertIsNone(r['deployment']['exact_published_at_utc']);self.assertEqual(r['owner_reported_validation']['site_tests_passed'],87);self.assertIn('locked',r['owner_reported_validation']['rendered_browser_QA']);self.assertFalse(r['local_verification']['full_site_suite_rerun']);self.assertFalse(r['local_verification']['site_deployed_here']);self.assertTrue(r['local_verification']['read_only_source_commit_check']['canonical_full_git_diff_equals_patch']);self.assertFalse(r['owner_reported_validation']['row_statistical_scan_performed'])
