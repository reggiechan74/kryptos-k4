"""Documentation-only checks for canonical external coverage and selection rules."""
from pathlib import Path
import json
import re
import unittest
ROOT = Path(__file__).resolve().parents[1]

class ExternalPriorArtRegisterTests(unittest.TestCase):
    def test_stable_records_have_required_fields(self):
        text = (ROOT/'research/EXTERNAL-PRIOR-ART.md').read_text()
        blocks = re.split(r'^### (EXT-\d{3}) — ', text, flags=re.M)
        ids = blocks[1::2]
        # The original survey's stable IDs remain; the live register may grow.
        self.assertTrue({f"EXT-{i:03d}" for i in range(1,30)} <= set(ids))
        index_ids = re.findall(r"^\| \[(EXT-\d{3})\]\(#ext-\d{3}\) \|", text, re.M)
        self.assertEqual(len(index_ids), len(set(index_ids)))
        self.assertEqual(set(index_ids), set(ids))
        self.assertEqual(len(ids), len(set(ids)))
        for ident, body in zip(ids, blocks[2::2]):
            for field in ('Researcher / project','Exact inspected scope','Method','Reported outcome','Evidence inspected','Local overlap / selection consequence','Limits and unresolved evidence','Primary sources'):
                self.assertIn('**'+field+':**', body, (ident, field))
            self.assertIn('https://', body)
    def test_source_pins_and_no_fake_reproduction(self):
        data = json.loads((ROOT/'sources/external-prior-art-pins-20261031.json').read_text())
        self.assertEqual('2026-10-31', data['reviewed_on'])
        self.assertEqual(15, len(data['repositories']))
        for row in data['repositories']:
            self.assertRegex(row['commit'], r'^[0-9a-f]{40}$')
        text = (ROOT/'research/EXTERNAL-PRIOR-ART.md').read_text()
        self.assertIn('No external experiment was reproduced', text)
        self.assertNotIn('/workspace/', text)
    def test_navigation_and_agent_gate(self):
        for file in ('README.md','AGENTS.md','research/HYPOTHESES.md'):
            self.assertIn('EXTERNAL-PRIOR-ART.md', (ROOT/file).read_text())
        agents = (ROOT/'AGENTS.md').read_text()
        for phrase in ('Required public prior-art gate','unfinished searches','Unknown external scope','after every'):
            if phrase == 'after every':
                self.assertIn('every experiment run', agents)
            else:
                self.assertIn(phrase, agents)
    def test_current_queue_is_not_new_execution_authority(self):
        text = (ROOT/'research/HYPOTHESES.md').read_text()
        archive = (ROOT/'research/HYPOTHESIS-HISTORY.md').read_text()
        self.assertIn('At that survey closeout, no proposed new execution-ready hypothesis cleared', archive)
        self.assertIn('execution was separately authorized at 15:03 UTC', archive)
        self.assertIn('15:03 UTC on 31 October 2026', text)
        self.assertIn('Each target requires its own frozen protocol', archive)
        self.assertIn('exact prior-art, protocol or control gates', text)
        self.assertIn('no cipher is currently cleared to run', text)
        self.assertIn('superseded ten-item', archive)
        self.assertIn('Historical ranked queue and current eligibility', archive)

if __name__ == '__main__':
    unittest.main()
