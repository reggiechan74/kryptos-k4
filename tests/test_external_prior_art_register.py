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
        self.assertEqual(29, len(ids))
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
        self.assertIn('At that survey closeout, no proposed new execution-ready hypothesis cleared', text)
        self.assertIn('execution was separately authorized at 15:03 UTC', text)
        self.assertIn('Each target requires its own frozen protocol', text)
        self.assertIn('superseded ten-item', text)
        self.assertIn('Historical ranked queue and current eligibility', text)

if __name__ == '__main__':
    unittest.main()
