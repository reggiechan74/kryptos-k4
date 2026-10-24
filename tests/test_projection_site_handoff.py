import io,json,shutil,stat,sys,tempfile,unittest,zipfile
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import verify_projection_site_handoff as v
class ProjectionSiteHandoffTests(unittest.TestCase):
 def test_static_archive_source_and_reference_integrity(self):
  r=json.loads((ROOT/'results/SITE-PROJECTION-20261024-SOURCE-HANDOFF.json').read_text());self.assertEqual(v.verify(),r['static_checks']);self.assertEqual(r['static_checks']['original_members'],33);self.assertEqual(r['static_checks']['manifest_files'],31);self.assertEqual(r['static_checks']['research_fixtures_equal'],8);self.assertEqual(r['static_checks']['research_local_control_records_equal'],11);self.assertFalse(r['static_checks']['JavaScript_executed'])
 def test_archive_path_type_and_duplicate_guards(self):
  for name,mode,duplicate in [('../escape',stat.S_IFREG|0o644,False),('/absolute',stat.S_IFREG|0o644,False),('a\\b',stat.S_IFREG|0o644,False),('a//b',stat.S_IFREG|0o644,False),('.git/config',stat.S_IFREG|0o644,False),('link',stat.S_IFLNK|0o777,False),('same',stat.S_IFREG|0o644,True)]:
   with self.subTest(name=name):
    data=io.BytesIO()
    with zipfile.ZipFile(data,'w') as z:
     info=zipfile.ZipInfo(name);info.external_attr=mode<<16;z.writestr(info,b'content')
     if duplicate:
      import warnings
      with warnings.catch_warnings():warnings.simplefilter('ignore');z.writestr(info,b'content')
    data.seek(0)
    with zipfile.ZipFile(data) as z,self.assertRaises(ValueError):v.safe_members(z)
 def test_changed_snapshot_is_rejected_without_repair(self):
  with tempfile.TemporaryDirectory() as d:
   dest=Path(d)/'archive';shutil.copytree(v.ARCHIVE,dest);p=dest/'snapshot/candidate/projection-test/core.mjs';p.write_bytes(p.read_bytes()+b'\n// altered\n')
   with patch.object(v,'ARCHIVE',dest),self.assertRaisesRegex(ValueError,'changed original'):v.verify()
 def test_owner_publication_QA_and_local_static_scope_are_distinct(self):
  r=json.loads((ROOT/'results/SITE-PROJECTION-20261024-SOURCE-HANDOFF.json').read_text());self.assertEqual(r['source_commit'],'543634f866b74a778b7f1b4de58a4815237dcb2f');self.assertEqual(r['deployment']['version'],16);self.assertEqual(r['deployment']['public_access_revision'],2);self.assertIn('locked',r['deployment']['rendered_browser_QA']);self.assertEqual(r['owner_reported_tests'],105);self.assertFalse(r['full_site_suite_rerun']);self.assertFalse(r['deployment']['site_deployed_here']);self.assertTrue(r['exact_git_diff_matches_patch']);self.assertTrue(r['all_manifest_bytes_match_source_commit'])
