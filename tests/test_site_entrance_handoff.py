import hashlib,json,shutil,subprocess,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class EntranceHandoffTests(unittest.TestCase):
    def test_byte_exact_archive_and_source_provenance(self):
        r=json.loads((ROOT/'results/SITE-ENTRANCE-V14-SOURCE-HANDOFF.json').read_text())
        self.assertEqual(r['published_version_supplied'],14)
        self.assertEqual(r['supplied_source_commit'],'d4155931cd760d4222c9f66916551110eb40053b')
        for path,sha in r['preserved_files_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),sha)
        self.assertFalse(r['redeployed_here']);self.assertFalse(r['private_photographs_included'])
        self.assertFalse(r['child_reported_validation']['independently_repeated_here'])
    def test_isolated_drawing_and_controls(self):
        node=shutil.which('node') or '/opt/homebrew/bin/node'
        if not Path(node).is_file():self.skipTest('Node unavailable')
        r=subprocess.run([node,'--test',str(ROOT/'docs/site-source/entrance-v14/review.test.mjs')],capture_output=True,text=True,timeout=30)
        self.assertEqual(r.returncode,0,r.stdout+r.stderr);self.assertIn('pass 3',r.stdout)
