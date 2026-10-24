import gzip,hashlib,json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
BASE=ROOT/'results/one-edit-028'
def folder():return BASE/json.loads((BASE/'latest.json').read_text())['run_id']

class OneEditArtifactTests(unittest.TestCase):
 def test_original_snapshot_and_source_hashes(self):
  p=folder();m=json.loads((p/'manifest.json').read_text());self.assertEqual(m['status'],'completed');self.assertEqual(m['execution_kind'],'original')
  for name,row in m['artifacts'].items():self.assertEqual(hashlib.sha256((p/name).read_bytes()).hexdigest(),row['sha256'])
  source=json.loads((p/'inputs.json').read_text());self.assertTrue(source['canonical_file_unchanged'])
  for name,h in source['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),h)
  spec=m['specification'];raw=subprocess.check_output(['git','show',spec['commit']+':research/ONE-EDIT-028-SPEC.md'],cwd=ROOT);self.assertEqual(hashlib.sha256(raw).hexdigest(),spec['sha256'])
 def test_raw_descriptions_unique_strings_and_constraint_counts(self):
  d=json.loads((folder()/'actual-summary.json').read_text());self.assertEqual((d['raw_edits'],d['unique_latent_strings'],d['unique_constraint_instances']),(5071,4968,6317));self.assertEqual((d['gross_alignment_descriptions'],d['admissible_alignment_descriptions'],d['inadmissible_alignment_descriptions']),(10142,9546,596));self.assertEqual(d['logical_periodic_checks'],458208);self.assertEqual(d['complete_periodic_records'],0)
  self.assertEqual(d['by_alignment']['ENGLISH_FIXED']['permutation_compatible'],191);self.assertEqual(d['by_alignment']['OBSERVED_CELL_TRANSPORT']['permutation_compatible'],169)
  self.assertEqual(d['by_alignment']['ENGLISH_FIXED']['strip_certificate_reject'],5071)
 def test_full_control_solutions_lossless_storage_and_truth_inclusion(self):
  p=folder();d=json.loads((p/'controls-summary.json').read_text());self.assertEqual(d['status'],'passed');self.assertEqual(d['plants'],24);self.assertEqual(d['planted_periodic_complete_records'],137600);self.assertTrue(any(n>3000 for n in d['planted_plaintext_class_counts']));self.assertEqual(d['independent_fixed_table_checks'],144)
  self.assertLess(d['storage']['saved_bytes'],64*1024**2);self.assertGreater(d['storage']['uncompressed_bytes'],64*1024**2)
  total=0
  with gzip.open(p/d['storage']['artifact'],'rb') as stream:
   while True:
    chunk=stream.read(1024*1024)
    if not chunk:break
    total+=len(chunk)
  self.assertEqual(total,d['storage']['uncompressed_bytes']);self.assertEqual(d['conventions']['offline_original_convention_tests'],7)
 def test_whole_family_nulls_and_first_fit_non_evidence(self):
  d=json.loads((folder()/'nulls.json').read_text());self.assertEqual(len(d['draws']),99);self.assertEqual((d['permutation_events'],d['periodic_first_events'],d['periodic_complete_events']),(99,99,0))
  self.assertTrue(all(r['by_alignment']['ENGLISH_FIXED']['admissible']==5071 and r['by_alignment']['OBSERVED_CELL_TRANSPORT']['admissible']==4475 for r in d['draws']))
 def test_post_outcome_independent_full_sets_and_exact_union(self):
  # Isolate complete decoded artifacts from cumulative RSS of unrelated tests.
  fresh=json.loads(subprocess.check_output([sys.executable,str(ROOT/'experiments/audit_one_edit.py')],cwd=ROOT));saved=json.loads((ROOT/'results/ONE-EDIT-028-INDEPENDENT-AUDIT.json').read_text())
  for key in ('complete_instance_model_sets_equal','permutation_union','independent_certificate_replay','permutation_compatible_by_alignment_and_operation','unique_first_fit_records'):self.assertEqual(fresh[key],saved[key])
  u=fresh['permutation_union'];self.assertEqual((u['unique_plaintext_constraint_classes'],u['primary_plaintext_constraint_classes'],u['pairwise_disjointness_checks']),(27,25,351));self.assertTrue(u['all_pairs_disjoint']);self.assertGreater(int(u['exact_distinct_plaintexts_primary_english_fixed']),10**84);self.assertEqual(fresh['independent_certificate_replay']['strip_rejected_instances'],6317)
 def test_incomplete_pre_scoring_attempt_is_not_a_cipher_negative(self):
  p=BASE/'20261024T025915Z-631d1a506e55420792c3f2bfd4729e95/manifest.json';d=json.loads(p.read_text());self.assertEqual(d['status'],'incomplete');self.assertEqual(d['error_type'],'TypeError');self.assertEqual(d['artifacts'],{})
 def test_canonical_bytes_unchanged_from_pre_study_main(self):
  raw=subprocess.check_output(['git','show','f6c5d2637fe0ab529c2019a2317d8e9375462da2:data/k4.json'],cwd=ROOT);self.assertEqual(raw,(ROOT/'data/k4.json').read_bytes())
