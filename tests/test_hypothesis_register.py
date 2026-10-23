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
        self.assertEqual(len(ids),55)
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
                self.assertIn(f'| [{i}](#{i.lower()}) |',current)

    def test_reference_paths_and_specific_scope_boundaries(self):
        _,current,sections=self.sections();records=dict(sections)
        for target in re.findall(r'\]\(([^)]+)\)',current):
            if target.startswith('#') or '://' in target:continue
            self.assertTrue((ROOT/'research'/target.split('#')[0]).exists(),target)
        for i in ('H-COMPASS-REVERSE','H-COMPASS-FRAMES','H-SHADOW-TIME','H-CELESTIAL-ALTITUDE','H-CLOCK-HISTORICAL','H-GREEK-PHONETIC'):
            self.assertIn('- Status: evidence-blocked',records[i])
        self.assertIn('104',records['H-TREE-STATEFUL'])
        self.assertIn('not ordinary positional base 5',records['H-LAMP-MENGENLEHRE'])
        self.assertIn('non-identifiable',records['H-OTP'])
        self.assertIn('- Status: analytical exclusion',records['H-AFFINE-DIGRAPH'])
