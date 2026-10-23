import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import unittest
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/site-source/confirmed-clues-v13'

class SiteSourceHandoffTests(unittest.TestCase):
    def test_source_delta_and_extracted_component_hashes(self):
        r=json.loads((ROOT/'results/SITE-CONFIRMED-CLUES-SOURCE-HANDOFF.json').read_text())
        patch=BASE/'kryptos-confirmed-k4-clues.patch'
        self.assertEqual(len(patch.read_bytes()),99546)
        self.assertEqual(hashlib.sha256(patch.read_bytes()).hexdigest(),r['patch_sha256'])
        self.assertEqual(hashlib.sha256((BASE/'source/k4-clues.mjs').read_bytes()).hexdigest(),r['extracted_module_sha256'])
        self.assertEqual(r['published_version_supplied'],13)
        self.assertEqual(r['canonical_display'],{'positions':97,'known':24,'unknown':73,'leading_padding_cells':27})
        self.assertFalse(r['child_reported_validation']['independently_repeated_here'])

    def test_isolated_component_against_canonical_cribs(self):
        node=shutil.which('node')
        if node is None and Path('/opt/homebrew/bin/node').is_file():node='/opt/homebrew/bin/node'
        if node is None:self.skipTest('Node unavailable; isolated Site component tests not repeated')
        result=subprocess.run([node,'--test',str(BASE/'review.test.mjs')],capture_output=True,text=True,timeout=30)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertIn('pass 4',result.stdout)

if __name__=='__main__':unittest.main()
