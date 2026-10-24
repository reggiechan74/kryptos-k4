import hashlib,json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import build_research_navigation as nav
import check_documentation as links
class NavigationTests(unittest.TestCase):
 def test_generated_tracker_matches_canonical_sources(self):
  saved=json.loads((ROOT/'docs/tracking/tracker.json').read_text());self.assertEqual(nav.gather(),saved);self.assertEqual(len(saved['hypotheses']),61);self.assertEqual(len({h['id'] for h in saved['hypotheses']}),61)
  for h in saved['hypotheses']:
   for key in ('Status','Mechanism','Evidence','Tested scope','Untested scope','Missing inputs','Next discriminating test','Dependencies','Results'):self.assertTrue(h[key])
  self.assertTrue(any('FOLD-SLIDE-020' in e['experiment_ids'] for e in saved['experiments']))
 def test_times_are_explicit_roles_not_inferred_commit_dates(self):
  saved=json.loads((ROOT/'docs/tracking/tracker.json').read_text())
  for r in saved['receipts']:
   d=json.loads((ROOT/r['path']).read_text())
   for t in r['timestamps']:self.assertIn(t['field'],nav.TIME_FIELDS);self.assertEqual(t['utc'],nav.iso(d[t['field']]));self.assertTrue(t['utc'].endswith('Z'))
  fold=next(e for e in saved['experiments'] if 'FOLD-SLIDE-020' in e['experiment_ids']);self.assertFalse(any(t['role'] in ('start','end') for t in fold['timestamps']))
  self.assertIsNone(nav.iso('2026-10-23'));self.assertIsNone(nav.iso('2026-10-23T12:00:00'));self.assertEqual(nav.iso('2026-10-23T08:00:00-04:00'),'2026-10-23T12:00:00Z')
 def test_all_folder_guides_and_relative_targets(self):
  files=nav.tracked();dirs={Path(p).parent for p in files if not p.startswith('.')}
  for p in list(dirs):dirs.update(p.parents)
  for d in dirs:
   if str(d)=='.':continue
   self.assertTrue((ROOT/d/'README.md').is_file(),str(d))
  report=links.audit();self.assertFalse(report['broken_markdown_fragments']);actual=report['broken'];allowed=json.loads((ROOT/'docs/tracking/preserved-link-exceptions.json').read_text());self.assertEqual({(x['source'],x['target']) for x in actual},{(x['source'],x['target']) for x in allowed})
  for x in allowed:self.assertTrue((ROOT/x['current_repository_target']).is_file())
 def test_original_root_documentation_retained_without_fabricated_history(self):
  original=subprocess.check_output(['git','show','6f269e11bec1a7b2f87e67f014b7b139708d0c61:README.md'],cwd=ROOT);self.assertEqual(original,(ROOT/'docs/history/README-before-navigation.txt').read_bytes())
  old=subprocess.check_output(['git','show','6f269e11bec1a7b2f87e67f014b7b139708d0c61:independent/2026-10-22/evolving-alphabet/PINNED-SPEC.md'],cwd=ROOT);self.assertEqual(old,(ROOT/'independent/2026-10-22/evolving-alphabet/PINNED-SPEC.md').read_bytes())

 def test_categories_outcomes_are_explicit_reviewed_data(self):
  import copy,tempfile
  from unittest.mock import patch
  saved=json.loads(nav.CURATION.read_text());records=nav.gather()['experiments'];self.assertEqual({e['record_id'] for e in records},set(saved['records']))
  for e in records:self.assertEqual(e['categories'],saved['records'][e['record_id']]['categories']);self.assertEqual(e['outcome'],saved['records'][e['record_id']]['outcome']);self.assertNotIn('category_hint',e)
  with tempfile.TemporaryDirectory() as tmp:
   invalid=copy.deepcopy(saved);invalid['records'].pop(records[0]['record_id']);p=Path(tmp)/'curation.json';p.write_text(json.dumps(invalid))
   with patch.object(nav,'CURATION',p),self.assertRaisesRegex(ValueError,'review required'):nav.gather()
 def test_heading_dates_are_day_precision_and_never_created_midnight_timestamps(self):
  date=nav.entry_date('23 October 2026 — a review','No execution time recorded',None);self.assertEqual(date,dict(date='2026-10-23',precision='day',source='heading',not_a_run_timestamp=True))
  self.assertIsNone(nav.entry_date('REGISTRY-20261023','No date recorded',None))
  records=nav.gather()['experiments'];dated=next(e for e in records if e['record_id']=='LOG-F2014ABCF5');self.assertEqual(dated['date_only']['date'],'2026-10-23');self.assertFalse(dated['timestamps'])
