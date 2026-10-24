import io,csv,hashlib,json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import monument_slide as s
class SlideArtifacts(unittest.TestCase):
 def test_all_frames_independent_pixel_oracle_and_source_pins(self):
  saved=json.loads((ROOT/'results/FOLD-SLIDE-020-actual.json').read_text());self.assertEqual(len(saved['records']),134);self.assertFalse(saved['physical_calibration'])
  for p,h in saved['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),h)
  node='/opt/homebrew/bin/node';oracle=json.loads(subprocess.check_output([node,str(ROOT/'experiments/monument_slide_oracle.mjs')]))
  for a,b in zip(saved['records'],oracle):
   for k,v in b.items():self.assertEqual(a[k],v,(a['id'],k))
  subprocess.check_call([node,str(ROOT/'experiments/monument_slide_visual_check.mjs')])
  zero=next(r for r in saved['records'] if r['id']=='OBSERVED_RENDER33:0');self.assertEqual((zero['label_matches'],zero['comparable_letter_pairs'],zero['common_pixel_area']),(35,856,7614));self.assertEqual([x['cipher']['k4_position'] for x in zero['k4_matches']],[14,44,72,95])
 def test_null_accounting_full_selector_and_seed_prefix(self):
  m=s.Model();records=m.actual()
  for scheme,expected in [('shuffle',[925,1126]),('rotation',[921,907])]:
   r=json.loads((ROOT/f'results/FOLD-SLIDE-020-null-{scheme}.json').read_text());self.assertEqual(r['controls'],1999);self.assertEqual(r['active_family'],130);self.assertEqual([x['exceedances'] for x in r['family_endpoints']],expected)
   fresh=s.nulls(m,records,scheme,n=5)
   for key in ('label_matches','common_pixel_area'):self.assertEqual(fresh['null_family_maxima'][key],r['null_family_maxima'][key][:5])
   for frame in r['per_frame']:
    for v in frame['endpoints'].values():
     if v is not None:self.assertLessEqual(v['raw_plus_one_p'],v['family_max_plus_one_p']);self.assertLessEqual(v['family_max_plus_one_p'],v['four_report_adjusted_p'])
   for p,h in r['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),h)
 def test_csv_complete_sequence_and_current_scope_receipts(self):
  actual=json.loads((ROOT/'results/FOLD-SLIDE-020-actual.json').read_text())['records'];rows=list(csv.DictReader(io.StringIO((ROOT/'results/FOLD-SLIDE-020-frames.csv').read_text())));self.assertEqual(len(rows),134)
  for a,b in zip(actual,rows):
   for k in ('shift','label_matches','geometric_overlap_cells','common_pixel_area'):self.assertEqual(a[k],int(b[k]))
  import frontier_assessment as f,exclusion_scope_audit as e
  self.assertEqual(f.assess(),json.loads((ROOT/'results/FRONTIER-023.json').read_text()));self.assertEqual(e.run(),json.loads((ROOT/'results/EXCLUSION-SCOPE-AUDIT-023.json').read_text()))
