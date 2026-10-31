"""Guard the editorial migration: exact science fields and dated prose survive."""
import hashlib,json,re,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments'))
from frontier_assessment import canonical
from check_documentation import markdown_anchors

def sha(text):return hashlib.sha256(text.encode()).hexdigest()

class HypothesisReorganizationTests(unittest.TestCase):
 def setUp(self):
  self.text=(ROOT/'research/HYPOTHESES.md').read_text()
  self.history=(ROOT/'research/HYPOTHESIS-HISTORY.md').read_text()
  self.manifest=json.loads((ROOT/'docs/tracking/hypothesis-reorganization-20261031.json').read_text())
 def test_migration_inventory_and_current_order(self):
  records=canonical(self.text)
  self.assertTrue(set(self.manifest['family_ids'])<=set(records))
  self.assertEqual(list(records),sorted(records))
  # Field hashes are a one-time migration receipt, not a freeze on future science.
  self.assertEqual(set(self.manifest['unchanged_family_fields_sha256']),set(self.manifest['family_ids']))
  self.assertEqual(self.manifest['verification']['unchanged_fields_compared'],599)
  self.assertTrue(self.manifest['verification']['all_equal'])
  for digest in self.manifest['unchanged_family_fields_sha256'].values():
   self.assertRegex(digest,r'^[0-9a-f]{64}$')
 def test_pinned_migration_preserves_material_fields(self):
  # Pin the editorial snapshot, not mutable current science. The publication's
  # reachable Git blob avoids duplicating a full canonical ledger fixture.
  result=subprocess.run(['git','cat-file','blob',self.manifest['migrated_ledger_blob']],cwd=ROOT,capture_output=True)
  if result.returncode:self.skipTest('Migration blob absent from shallow checkout; fetch publication history to verify equivalence')
  records=canonical(result.stdout.decode())
  self.assertEqual(sorted(records),self.manifest['family_ids'])
  for ident,fields in records.items():
   retained={k:v for k,v in fields.items() if k not in self.manifest['changed_fields'].get(ident,[])}
   self.assertEqual(sha(json.dumps(retained,sort_keys=True)),self.manifest['unchanged_family_fields_sha256'][ident],ident)
 def test_dated_prose_preserved_byte_for_byte(self):
  opening=self.history.split('<!-- ARCHIVED-OPENING:START -->\n')[1].split('<!-- ARCHIVED-OPENING:END -->')[0]
  notes=self.history.split('<!-- ARCHIVED-NOTES:START -->')[1].split('<!-- ARCHIVED-NOTES:END -->')[0]
  self.assertEqual(sha(opening),self.manifest['archived_opening_sha256'])
  self.assertEqual(sha(notes),self.manifest['archived_notes_sha256'])
 def test_legacy_anchors_and_all_ledger_internal_links(self):
  valid=markdown_anchors(self.text)
  self.assertTrue(set(self.manifest['legacy_aliases'])<=valid)
  for path,text in [('HYPOTHESES.md',self.text),('HYPOTHESIS-HISTORY.md',self.history)]:
   for target in re.findall(r'\]\(([^)]+)\)',text):
    if target.startswith('#'):self.assertIn(target[1:],markdown_anchors(text),path+target)
  self.assertIn('h-enigma-direct-1',valid)
  self.assertIn('geographic-branches-and-extraction-gate',valid)
 def test_stale_completed_successors_are_not_current_actions(self):
  records=canonical(self.text)
  for ident in self.manifest['changed_fields']:
   next_action=records[ident]['Next discriminating test']
   self.assertNotRegex(next_action,r'(?i)select Q-0[789]|proposed/unrun')
  self.assertIn('four cells remain unresolved',(ROOT/'README.md').read_text())
  self.assertNotIn('Next is an independent 810-cell',(ROOT/'README.md').read_text())
 def test_explicit_html_anchor_parser(self):
  self.assertEqual(markdown_anchors('# Title\n# Title\n<a id="old-section"></a>\n<a name=\'other\'></a>'),{'title','title-1','old-section','other'})

if __name__=='__main__':unittest.main()
