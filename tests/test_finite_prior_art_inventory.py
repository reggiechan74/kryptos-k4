"""Static checks for the frozen 71-hit discovery review, not live repo counts."""
import json
import re
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'research/finite-prior-art-20261031'

class FinitePriorArtInventoryTests(unittest.TestCase):
    def test_every_discovery_hit_once_and_exact_dispositions(self):
        data = json.loads((EVIDENCE/'coverage-disposition-20261031.json').read_text())
        rows = data['records']
        self.assertEqual(list(range(71)), sorted(r['discovery_index'] for r in rows))
        self.assertEqual(71, len({r['repo'] for r in rows}))
        self.assertEqual(dict(Counter(r['classification'] for r in rows)), data['summary']['disposition_counts'])
        self.assertEqual({'implemented_k4':33,'documentation_only':8,'unsupported_solution_claim':13,'fork_duplicate':11,'irrelevant':4,'unavailable':2}, data['summary']['disposition_counts'])
        self.assertFalse(any(r['independent_reproduction'] for r in rows))

    def test_source_depth_is_not_completed_program_count(self):
        rows=json.loads((EVIDENCE/'coverage-disposition-20261031.json').read_text())['records']
        self.assertEqual(60,len({r['unique_project'] for r in rows}))
        self.assertEqual(54,len({r['unique_project'] for r in rows if r['classification'] not in {'irrelevant','unavailable'}}))
        self.assertEqual(59,sum(r['documentation_inspected'] or r['source_inspected'] for r in rows))
        self.assertEqual(39,sum(r['source_inspected'] for r in rows))
        self.assertEqual(6,sum(r['named_result_inspected'] for r in rows))
        self.assertTrue(next(r for r in rows if r['repo']=='akaalias/k4')['discovery_member'])
        self.assertNotIn('jcolinpatrick/kryptos',{r['repo'] for r in rows})
        for r in rows:
            if r['classification']=='unavailable':
                self.assertFalse(r['pin'])
            else:
                self.assertRegex(r['pin'],r'^[0-9a-f]{40}$')

    def test_additions_link_to_canonical_records(self):
        rows=json.loads((EVIDENCE/'register-additions.json').read_text())
        text=(ROOT/'research/EXTERNAL-PRIOR-ART.md').read_text()
        self.assertEqual([f'EXT-{i:03d}' for i in range(31,48)],[r['id'] for r in rows])
        for row in rows:
            self.assertIn('### '+row['id']+' — '+row['title'],text)
            self.assertTrue(row['limits'] and row['evidence'])
            for source in row['sources']:
                self.assertIn(source,text)
                self.assertTrue(source.startswith('https://github.com/'))

    def test_public_package_has_no_source_cache_or_private_paths(self):
        for path in EVIDENCE.iterdir():
            self.assertTrue(path.is_file())
            self.assertIn(path.suffix,{'.md','.json'})
            text=path.read_text()
            for private in ('/workspace/','/tmp/','Responsibilities Page','source_content','raw_source'):
                self.assertNotIn(private,text,path.name)
