import argparse,contextlib,io,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import run_bounded as runner
from run_io import RunSnapshot
from build_research_navigation import iso
class RunTimingTests(unittest.TestCase):
 def test_validation_only_jobs_have_ordered_run_and_job_boundaries(self):
  with tempfile.TemporaryDirectory() as tmp:
   ident=runner.execute(tmp,'synthetic timing validation',{},[('SYNTHETIC',lambda cap:{'value':1},5)],{},'unit validation',lambda:None,execution_kind='validation');manifest=json.loads((Path(tmp)/ident/'manifest.json').read_text());job=manifest['jobs'][0]
   self.assertEqual(manifest['execution_kind'],'validation');self.assertEqual(job['status'],'completed')
   times=[manifest['started_at_utc'],job['started_at_utc'],job['finished_at_utc'],manifest['finished_at_utc']];self.assertTrue(all(iso(t) for t in times));self.assertEqual(times,sorted(times))
 def test_failed_job_still_records_end_and_does_not_publish_results(self):
  with tempfile.TemporaryDirectory() as tmp:
   def fail(cap):raise ValueError('synthetic failure')
   with self.assertRaises(ValueError):runner.execute(tmp,'validation',{},[('FAIL',fail,5)],{},'unit validation',lambda:None,execution_kind='validation')
   pointer=json.loads((Path(tmp)/'latest.json').read_text());m=json.loads((Path(tmp)/pointer['manifest']).read_text());self.assertEqual(m['status'],'incomplete');self.assertEqual(m['jobs'][0]['status'],'incomplete');self.assertTrue(iso(m['jobs'][0]['finished_at_utc']));self.assertEqual(m['artifacts'],{})
 def test_purpose_is_explicit_and_replay_entrypoints_do_not_claim_original(self):
  with tempfile.TemporaryDirectory() as tmp:
   self.assertEqual(RunSnapshot(tmp,'test',{}).manifest['execution_kind'],'unspecified')
   with self.assertRaises(ValueError):RunSnapshot(tmp,'test',{},execution_kind='invented')
  args=argparse.Namespace(spec_commit='0'*40,spec_file='research/BOUNDED-SPEC.md',output_dir='/tmp/unused-timing-test')
  for entry in (runner.main,runner.statistics_main):
   with patch.object(runner,'arguments',return_value=args),patch.object(runner,'specification',return_value={}),patch.object(runner,'execute',return_value='not-executed') as execute,contextlib.redirect_stdout(io.StringIO()):entry()
   self.assertEqual(execute.call_args.kwargs['execution_kind'],'replay')
