"""Validate the existing ledger's current section, not a second status database."""
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]

class HypothesisRegisterTests(unittest.TestCase):
    def sections(self):
        text=(ROOT/'research/HYPOTHESES.md').read_text()
        current=text.split('<!-- CURRENT-REGISTER:START -->')[1].split('<!-- CURRENT-REGISTER:END -->')[0]
        sections=re.findall(r'^### (H-[A-Z0-9-]+)\n(.*?)(?=^### H-|\Z)',current,re.M|re.S)
        return text,current,sections

    def test_unique_ids_fields_status_and_legacy_retention(self):
        text,current,sections=self.sections()
        ids=[i for i,_ in sections]
        self.assertEqual(len(ids),63)
        self.assertEqual(len(ids),len(set(ids)))
        referenced=set(re.findall(r'\bH-[A-Z][A-Z0-9-]*',current))-{'H-PHONETIC-RESP'}
        self.assertTrue(referenced<=set(ids),referenced-set(ids))
        historical=text.split('<!-- CURRENT-REGISTER:END -->')[1]
        old=set(re.findall(r'\bH-[A-Z][A-Z0-9-]*',historical))-{'H-PHONETIC-RESP'}
        self.assertTrue(old<=set(ids),old-set(ids))
        statuses={'untested','evidence-blocked','specified but not run','narrow negative','analytical exclusion','non-identifiable'}
        for i,body in sections:
            with self.subTest(id=i):
                fields=dict(re.findall(r'^- ([A-Za-z ]+): (.+)$',body,re.M))
                self.assertEqual(set(fields),{'Status','Mechanism','Evidence','Tested scope','Untested scope','Missing inputs','Next discriminating test','Dependencies','Results'})
                self.assertIn(fields['Status'],statuses)
                self.assertTrue(all(v.strip() for v in fields.values()))
                self.assertIn(f'| [{i}](#{i.lower()}) | {fields["Status"]} |',current)

    def test_reference_paths_and_specific_scope_boundaries(self):
        _,current,sections=self.sections();records=dict(sections)
        for target in re.findall(r'\]\(([^)]+)\)',current):
            if target.startswith('#') or '://' in target:continue
            self.assertTrue((ROOT/'research'/target.split('#')[0]).exists(),target)
        for i in ('H-COMPASS-REVERSE','H-COMPASS-FRAMES','H-SHADOW-TIME','H-CELESTIAL-ALTITUDE','H-CLOCK-HISTORICAL'):
            self.assertIn('- Status: evidence-blocked',records[i])
        self.assertIn('- Status: narrow negative',records['H-GREEK-PHONETIC'])
        self.assertIn('- Status: narrow negative',records['H-SIGABA'])
        self.assertIn('104',records['H-TREE-STATEFUL'])
        self.assertIn('not ordinary positional base 5',records['H-LAMP-MENGENLEHRE'])
        self.assertIn('non-identifiable',records['H-OTP'])
        self.assertIn('- Status: analytical exclusion',records['H-AFFINE-DIGRAPH'])

    def test_working_queue_and_agent_closeout_contract(self):
        text=(ROOT/'research/HYPOTHESES.md').read_text()
        top=text.split('<!-- CURRENT-REGISTER:START -->')[0]
        self.assertIn('canonical reference for deciding what to test next',top)
        for number in range(1,6):
            self.assertRegex(top,rf'\| {number} / Q-0{number} \|')
        self.assertIn('Queue rank is a recommendation, not authorization',top)
        self.assertIn('Required end-of-run reconciliation',top)
        agents=(ROOT/'AGENTS.md').read_text()
        self.assertIn('research/HYPOTHESES.md',agents)
        self.assertIn('every experiment run',agents)
        self.assertIn('interrupted and inconclusive runs',agents)
        self.assertIn('before choosing or starting work',agents)
        self.assertIn('before declaring completion or deciding what runs next',agents)
        self.assertIn('python3 experiments/build_research_navigation.py',agents)
        self.assertIn('research/HYPOTHESES.md',(ROOT/'README.md').read_text().split('## Start here')[0])

    def test_recent_studies_reconciled_with_explicit_curation(self):
        import json,hashlib
        log=(ROOT/'research/EXPERIMENTS.md').read_text()
        curated=json.loads((ROOT/'docs/tracking/curated-records.json').read_text())['records']
        for number in range(51,57):
            titles=re.findall(rf'^## (CANDIDATE-FIRST-{number:03d} .+)$',log,re.M)
            self.assertEqual(len(titles),1)
            ident='LOG-'+hashlib.sha256(titles[0].encode()).hexdigest()[:10].upper()
            self.assertEqual(curated[ident]['title'],titles[0])
            self.assertTrue(curated[ident]['categories'])
            self.assertTrue(curated[ident]['outcome'])
            self.assertTrue((ROOT/f'research/candidate-first-{number:03d}/README.md').is_file())
