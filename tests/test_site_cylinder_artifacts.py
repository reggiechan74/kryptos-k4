import csv,gzip,hashlib,json,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import compare_site_cylinder037 as comparison
class SiteCylinderArtifactTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.s=json.loads((ROOT/'results/SITE-CYLINDER-037-SUMMARY.json').read_text())
 def test_frozen_inputs_and_original_numeric_archive(self):
  for path,sha in self.s['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),sha)
  p=ROOT/'results/SITE-CYLINDER-037-ORIGINAL.json.gz';self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),self.s['original_archive']['sha256']);h=hashlib.sha256()
  with gzip.open(p,'rb') as f:
   for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
  self.assertEqual(h.hexdigest(),self.s['original_archive']['raw_sha256']);self.assertFalse(self.s['Site_source_archived']);self.assertFalse(self.s['source_files_modified']);self.assertEqual(self.s['actual_K4_evaluations'],0)
 def test_complete_source_default_neighborhood_agreement(self):
  n=self.s['neighborhood'];self.assertEqual((n['states'],n['complete97'],n['invalid97'],n['same_default_key'],n['distinct_complete_keys']),(729,441,288,186,11));self.assertEqual(n['same_default_cells_and_admission'],186);self.assertEqual(n['full_stability_selected'],11);self.assertEqual(n['unselected_complete_states'],430);self.assertEqual(self.s['fixture_comparison']['samples_compared'],71198);self.assertLess(self.s['fixture_comparison']['maximum_coordinate_error'],1e-9)
 def test_every_default_margin_and_scale_conversion(self):
  with (ROOT/'results/SITE-CYLINDER-037-DEFAULT-MARGINS.csv').open() as f:rows=list(csv.DictReader(f))
  self.assertEqual(len(rows),97);base=self.s['default']['result'];tight=[]
  for i,row in enumerate(rows):
   value=float(row['margin_pitch']);self.assertEqual(int(row['sample']),i+1);self.assertEqual(row['key_letter'],base['letters'][i]);self.assertEqual(value,base['margins'][i]);self.assertAlmostEqual(float(row['U100_margin_mm']),value*25);self.assertAlmostEqual(float(row['R250_margin_mm']),value*78.125);self.assertAlmostEqual(float(row['U100_guard_excess_mm']),(value-.01)*25)
   if abs(value-self.s['default_min_margin_fraction'])<1e-12:tight.append(i+1)
  self.assertEqual(tight,[25,56,87]);self.assertAlmostEqual(self.s['default_min_margin_fraction'],.01784193946678414)
 def test_all_frozen_stability_records_preserve_floor_and_admission(self):
  r=json.load(gzip.open(ROOT/'results/SITE-CYLINDER-037-ORIGINAL.json.gz','rt'));n=r['stages']['replay_neighborhood'];byid={x['id']:x['result'] for x in n['neighbors']};cases=r['stages']['stability']['records'];self.assertEqual(len(cases),22)
  for case in cases:
   self.assertEqual(len(case['records']),162);self.assertFalse(case['assembly_cell_stable']);self.assertFalse(case['assembly_key_stable']);base=byid[case['neighbor_id']]
   for rec in case['records']:
    value=rec['result'];self.assertEqual(len(value['margins']),97);floor=sum(a!=b for a,b in zip(base['cell_path'],value['cell_path']));admission=sum(a!=b for a,b in zip(base['statuses'],value['statuses']));self.assertEqual((floor,admission),(rec['floor_cell_changes'],rec['admission_changes']));self.assertEqual(rec['same_cells_and_admission'],floor==0 and admission==0);self.assertEqual(rec['same_key'],value['key']==base['key'])
 def test_pupil_subset_success_is_not_full_manual_pass(self):
  a=self.s['stability_counts'];self.assertEqual(a['U100']['tiny_pupil_passes'],10);self.assertEqual(a['R250']['tiny_pupil_passes'],11)
  for x in a.values():self.assertEqual(x['cases'],11);self.assertEqual(x['assembly_cell_passes'],0);self.assertEqual(x['assembly_key_passes'],0);self.assertEqual(x['human_scale_pupil_passes'],0)
  defaults=[x for x in self.s['stability_cases'] if x['neighbor_id']==364];self.assertEqual(len(defaults),2);self.assertFalse(defaults[0]['pupil']['0.05']['cell_stable']);self.assertTrue(defaults[1]['pupil']['0.05']['cell_stable'])
 def test_full_replay_and_honest_resource_scope(self):
  c=json.loads((ROOT/'results/SITE-CYLINDER-037-PY312-COMPARISON.json').read_text());self.assertTrue(c['complete']);self.assertLess(c['maximum_absolute_float_difference'],1e-9);self.assertEqual(c['floats_compared'],494004)
  r=json.loads((ROOT/'results/SITE-CYLINDER-037-RESOURCE-REPLAY.json').read_text());self.assertTrue(r['geometry_domain_unchanged']);self.assertTrue(r['no_data_truncation']);self.assertLess(r['maximum_resident_bytes'],r['cap_bytes']);self.assertIn('not measured',r['original_resource_limit'])
 def test_comparator_checks_float_and_discrete_values(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);a=root/'a.json';b=root/'b.json';work=root/'floats';a.write_text(json.dumps({'x':.123,'status':'valid','started_at_utc':'old'}));b.write_text(json.dumps({'x':.123+1e-11,'status':'valid','started_at_utc':'new'}));first=comparison.fingerprint(a,work);second=comparison.fingerprint(b,work,True);self.assertEqual(first['discrete_structure_sha256'],second['discrete_structure_sha256']);self.assertGreater(second['maximum_absolute_difference'],0)
   b.write_text(json.dumps({'x':.123+1e-8,'status':'valid'}))
   with self.assertRaises(AssertionError):comparison.fingerprint(b,work,True)
   b.write_text(json.dumps({'x':.123,'status':'invalid'}));self.assertNotEqual(first['discrete_structure_sha256'],comparison.fingerprint(b,work,True)['discrete_structure_sha256'])
