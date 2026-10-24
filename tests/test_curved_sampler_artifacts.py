import collections,gzip,hashlib,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import curved_sampler as c
class CurvedArtifactTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.s=json.loads((ROOT/'results/CURVED-SAMPLER-036-SUMMARY.json').read_text())
 def test_source_hashes_and_lossless_archives(self):
  for path,sha in self.s['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),sha)
  for path,metadata in self.s['archives'].items():self.assertEqual(hashlib.sha256((ROOT/'results'/path).read_bytes()).hexdigest(),metadata['sha256'])
  raw=gzip.decompress((ROOT/'results/CURVED-SAMPLER-036-ORIGINAL.json.gz').read_bytes());self.assertEqual(hashlib.sha256(raw).hexdigest(),self.s['archives']['CURVED-SAMPLER-036-ORIGINAL.json.gz']['raw_sha256'])
 def test_full_optical_and_cell_panel_independent_audits(self):
  r=json.loads((ROOT/'results/CURVED-SAMPLER-036-RAY-VALIDATION.json').read_text());self.assertEqual(r['rays'],54320);self.assertTrue(r['all_statuses_equal']);self.assertLess(r['maximum_absolute_coordinate_error'],1e-9)
  a=json.loads((ROOT/'results/CURVED-SAMPLER-036-INDEPENDENT-CELL-AUDIT.json').read_text());self.assertTrue(a['complete']);self.assertEqual((a['poses_checked'],a['samples_checked']),(45252,4389444));self.assertEqual((a['complete97_poses'],a['utility_gate_poses']),(54,4))
 def test_saved_pose_domain_and_alias_accounting(self):
  counts=collections.Counter();keys=set();paths=set()
  for line in gzip.open(ROOT/'results/CURVED-SAMPLER-036-poses.jsonl.gz','rt'):
   x=json.loads(line);counts['rows']+=1;self.assertEqual(len(x['statuses']),97);self.assertEqual(len(x['cells']),97)
   if x['complete']:counts['complete']+=1;self.assertEqual(x['statuses'],'V'*97);self.assertEqual(len(x['key']),97);keys.add(x['key']);paths.add(json.dumps(x['cells']))
   else:self.assertIsNone(x['key'])
  self.assertEqual((counts['rows'],counts['complete'],len(keys),len(paths)),(45252,54,54,54));self.assertEqual(self.s['sweep']['counts']['complete_ground_footprints'],419);self.assertEqual(self.s['sweep']['counts']['incomplete_ground_footprints'],141)
 def test_scope_of_stability_failures_and_all_records(self):
  r=json.load(gzip.open(ROOT/'results/CURVED-SAMPLER-036-ORIGINAL.json.gz','rt'));s=r['stages']['stability'];self.assertEqual(s['selected'],4)
  for case in s['records']:
   self.assertEqual(len(case['records']),340);self.assertFalse(case['assembly_cell_stable']);self.assertFalse(case['assembly_key_stable']);self.assertTrue(case['first_counterexample'])
   for pupil in case['pupil'].values():self.assertEqual(pupil['records'],9);self.assertFalse(pupil['all_cells_stable']);self.assertFalse(pupil['all_keys_stable'])
  self.assertEqual(r['actual_K4_evaluations'],0);self.assertFalse(r['physical_replica']);self.assertEqual(len(r['stages']['sweep']['utility_rows']),4)
 def test_synthetic_panel_recovery_and_whole_family_nulls(self):
  r=json.load(gzip.open(ROOT/'results/CURVED-SAMPLER-036-ORIGINAL.json.gz','rt'));panel=r['stages']['sweep']['key_panel'];recovery=r['stages']['recovery'];self.assertEqual(len(panel),4);self.assertTrue(recovery['complete']);self.assertEqual(len(recovery['plants']),4)
  for plant in recovery['plants']:
   known={int(i)-1:v for i,v in plant['known_one_based'].items()};value=c.recover_keys(plant['ciphertext'],known,panel);self.assertEqual(value,plant['result']);self.assertEqual(len(value['first13_key_classes']),2);self.assertEqual(len(value['full24_candidates']),1);self.assertEqual(value['full24_candidates'][0]['plaintext'],plant['plaintext']);self.assertEqual(c.encrypt(plant['plaintext'],plant['planted_key']),plant['ciphertext'])
  self.assertEqual(len(recovery['nulls']),31);self.assertTrue(all(len(x['records'])==4 for x in recovery['nulls']));self.assertEqual(max(x['whole_family_maximum'] for x in recovery['nulls']),5);self.assertEqual(sum(x['full24_key_classes'] for x in recovery['nulls']),0)
 def test_nominal_and_failure_site_fixtures_are_research_model(self):
  f=json.loads((ROOT/'results/CURVED-SAMPLER-036-SITE-FIXTURES.json').read_text());rows=f['tableau_rows'];nominal=f['nominal'];new=c.sample(nominal['params'],rows);self.assertEqual(new['key'],nominal['key']);self.assertTrue(new['complete']);failure=f['assembly_failure'];self.assertNotEqual(c.sample(failure['params'],rows,failure['eye_offset'],failure['fixed_reticle'])['key'],nominal['key']);p=f['pupil_failure'];self.assertNotEqual(c.sample(p['params'],rows,p['eye_offset'],True)['key'],nominal['key'])
  comparison=json.loads((ROOT/'results/CURVED-SAMPLER-036-SITE-CONTRACT-COMPARISON.json').read_text());self.assertFalse(comparison['Site_tests_independently_rerun']);self.assertFalse(comparison['handoff_inventory_only']['archived_in_repository']);self.assertIn('vertical',comparison['site_geometry']['tableau']);self.assertIn('horizontal',comparison['research_geometry']['tableau'])
 def test_full_cross_version_discrete_replay_and_coordinate_tolerance(self):
  r=json.loads((ROOT/'results/CURVED-SAMPLER-036-PY312-COMPARISON.json').read_text());self.assertTrue(r['complete']);self.assertTrue(r['discrete_decisions_keys_and_recovery_equal']);self.assertEqual(r['pose_records_compared'],45252);self.assertLess(r['metrics']['maximum_absolute_float_difference'],1e-9)
  for path,sha in [('results/CURVED-SAMPLER-036-PY312-REPLAY.json.gz',r['archive_sha256']),('results/CURVED-SAMPLER-036-PY312-poses.jsonl.gz',r['pose_archive_sha256'])]:self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),sha)
  self.assertEqual(sum(1 for _ in gzip.open(ROOT/'results/CURVED-SAMPLER-036-PY312-poses.jsonl.gz','rt')),45252)
