"""Preserve published map payload bytes while validating integration navigation."""
import hashlib,json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];ARCHIVE=ROOT/'docs/maps/berlin-wsw-2026-10-24';ORIGINAL='2be4e0585e76aa98a1487c962d0adcc44bfa84fa'
class MapArchiveIntegrationTests(unittest.TestCase):
 def test_all_original_published_payload_bytes_are_preserved(self):
  original=json.loads(subprocess.check_output(['git','show',ORIGINAL+':docs/maps/berlin-wsw-2026-10-24/manifest.json'],cwd=ROOT));self.assertEqual(len(original['files']),88)
  for row in original['files']:
   raw=(ARCHIVE/row['path']).read_bytes();self.assertEqual(len(raw),row['bytes']);self.assertEqual(hashlib.sha256(raw).hexdigest(),row['sha256'])
  current=json.loads((ARCHIVE/'manifest.json').read_text());self.assertEqual(len(current['files']),100);extra={x['path'] for x in current['files']}-{x['path'] for x in original['files']};self.assertEqual(extra,set(current['repository_integration']['added_navigation_only']));self.assertTrue(all(Path(p).name=='README.md' for p in extra))
 def test_read_only_integrity_validator(self):
  r=json.loads(subprocess.check_output([sys.executable,str(ARCHIVE/'repro/validate_bundle.py')],cwd=ARCHIVE));self.assertTrue(r['passed']);self.assertEqual(r['payload_files'],100);self.assertEqual(len(r['required_maps']),4);self.assertEqual(sorted(r['table_rows'].values()),[45,104,147])
 def test_read_only_spherical_route_validator(self):
  r=json.loads(subprocess.check_output([sys.executable,str(ARCHIVE/'repro/validate_spherical_route.py')],cwd=ARCHIVE));self.assertTrue(r['passed']);self.assertLess(r['saved_route']['max_vertex_cross_track_error_km'],1e-6);self.assertIn('not WGS84',r['model'])
