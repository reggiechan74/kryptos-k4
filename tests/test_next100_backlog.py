"""Static draft-catalog and integration checks; no cipher/benchmark execution."""
from pathlib import Path
import hashlib,json,re,unittest
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'research/next-100-hypotheses-20261101'
class Next100Backlog(unittest.TestCase):
 def test_exact100_unrun_drafts(self):
  c=json.loads((D/'catalog.json').read_text());rows=c['records'];self.assertEqual(len(rows),100);self.assertEqual(len({x['id'] for x in rows}),100);self.assertEqual(sum(x['type']=='mechanism' for x in rows),78);self.assertEqual(sum(x['type']=='method' for x in rows),22);self.assertEqual(sum(x['status']=='specification_blocked' for x in rows),6)
  for x in rows:self.assertIn(x['status'],('proposed_unrun','specification_blocked'));self.assertEqual(x['target_admission'],'not_admitted');self.assertEqual(x['novelty_status'],'exact_scope_review_pending')
 def test_original_specifications_and_declared_derivatives(self):
  changes={x['path']:x for x in json.loads((D/'PUBLICATION-PROVENANCE.json').read_text())['derivatives']}
  for row in json.loads((D/'MANIFEST.json').read_text())['files']:
   expected=row['sha256']
   if row['path'] in changes:self.assertEqual(expected,changes[row['path']]['original_sha256']);expected=changes[row['path']]['public_sha256']
   self.assertEqual(hashlib.sha256((D/row['path']).read_bytes()).hexdigest(),expected,row['path'])
 def test_no_duplicate_queue_or_fake_completed_count(self):
  h=(ROOT/'research/HYPOTHESES.md').read_text();self.assertEqual(h.count('## Next-action queue'),1);self.assertIn('78 mechanism proposals and 22 falsifiable method experiments',h);self.assertIn('not replace the canonical execution queue',h);self.assertIn('N100-',(D/'README.md').read_text())
  ids=re.findall(r'^### (H-[^\n]+)$',h,re.M);self.assertEqual(len(ids),69);self.assertEqual(len(set(ids)),69)
 def test_new_external_evidence_tiers(self):
  e=(ROOT/'research/EXTERNAL-PRIOR-ART.md').read_text()
  for id in ('EXT-052','EXT-053'):self.assertEqual(len(re.findall(r'^### '+id+r' — ',e,re.M)),1)
  self.assertIn('No author count is imported as independently verified completed negatives',e);self.assertIn('Documentation review only',e)
 def test_current_machine_status_overrides(self):
  original=json.loads((D/'catalog.json').read_text());effective=json.loads((D/'CURRENT-CATALOG.json').read_text());overrides=json.loads((D/'CURRENT-STATUS.json').read_text());by={x['id']:x for x in effective['records']};old={x['id']:x for x in original['records']};self.assertEqual(set(by),set(old));self.assertEqual(effective['original_catalog_sha256'],hashlib.sha256((D/'catalog.json').read_bytes()).hexdigest())
  updates={x['id']:x for x in overrides['overrides']}
  for ident,row in by.items():self.assertEqual(row['specification'],old[ident]['specification']);self.assertEqual(row['status'],updates[ident]['status'] if ident in updates else old[ident]['status']);self.assertEqual(row['target_admission'],'not_admitted')
  self.assertEqual(by['N100-036']['status'],'blocked_prior_art_overlap_unresolved');self.assertFalse(by['N100-036']['synthetic_ready']);self.assertIn('blocked_prior_art_overlap_unresolved',(D/'CURRENT-INDEX.md').read_text())
