import bisect,csv,datetime,gzip,hashlib,io,json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import monument_slide_2d as m
class TwoDimensionalArtifactTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  root=ROOT/'results/fold-slide-2d-001-runs';cls.directory=root/'20261023T234752Z-ddb7425463b745a4b3d70b1b669dd641';cls.summary=json.loads((cls.directory/'summary.json').read_text());cls.actual=json.loads((cls.directory/'actual.json').read_text());cls.records=cls.actual['records']
 def test_immutable_original_hashes_chronology_and_full_oracle(self):
  manifest=json.loads((self.directory/'manifest.json').read_text());self.assertEqual(manifest['status'],'completed');self.assertEqual(manifest['execution_kind'],'original');self.assertLess(datetime.datetime.fromisoformat(manifest['started_at_utc']),datetime.datetime.fromisoformat(manifest['finished_at_utc']))
  for job in manifest['jobs']:self.assertEqual(job['status'],'completed');self.assertLessEqual(datetime.datetime.fromisoformat(job['started_at_utc'].replace('Z','+00:00')),datetime.datetime.fromisoformat(job['finished_at_utc'].replace('Z','+00:00')))
  for name,meta in manifest['artifacts'].items():
   raw=(self.directory/name).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),meta['sha256']);self.assertEqual(len(raw),meta['bytes'])
  for name,h in self.summary['file_sha256'].items():
   raw=subprocess.check_output(['git','show',self.summary['code_commit']+':'+name],cwd=ROOT);self.assertEqual(hashlib.sha256(raw).hexdigest(),h)
  subprocess.check_call(['git','merge-base','--is-ancestor',self.summary['spec_commit'],self.summary['code_commit']],cwd=ROOT)
  pre=json.loads((ROOT/'results/FOLD-SLIDE-2D-PRE-EVALUATION-CONTROLS.json').read_text())
  for name,h in pre['implementation_sha256'].items():
   raw=subprocess.check_output(['git','show',self.summary['code_commit']+':'+name],cwd=ROOT);self.assertEqual(hashlib.sha256(raw).hexdigest(),h)
  oracle=json.loads((self.directory/'independent.json').read_text())['records'];self.assertEqual(len(oracle),7638);self.assertEqual(sum(bool(r['geometric_overlap_cells']) for r in self.records),7150)
  for a,b in zip(self.records,oracle):
   for key,value in b.items():self.assertEqual(a[key],value,(a['id'],key))
  import ast
  original=subprocess.check_output(['git','show',self.summary['code_commit']+':experiments/monument_slide_2d.py'],cwd=ROOT).decode();current=(ROOT/'experiments/monument_slide_2d.py').read_text()
  def algorithms(text):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name!='run'}
  self.assertEqual(algorithms(original),algorithms(current))
  engine=m.Engine();values=engine.score(engine.base.base)
  for e,name in enumerate(m.NAMES):self.assertEqual(values[e],[r[name] for r in self.records])
 def test_complete_positions_masks_and_changing_denominators(self):
  grouped=collections_default();labels=collections_default()
  with gzip.open(self.directory/'label-matches.csv.gz','rt') as f:
   for r in csv.DictReader(f):
    key=f"{r['model']}:{r['dy']}:{r['dx']}";labels[key][0]+=1;self.assertEqual(int(r['cipher_row'])-int(r['tableau_row']),int(r['dy']));self.assertEqual(int(r['cipher_grid_column'])-int(r['tableau_grid_column']),int(r['dx']))
  font=dict(zip(m.old.SYMBOLS,m.old.glyph_masks()));data=json.loads((ROOT/'data/monument-slide-input-v2.json').read_text());center=lambda rows:[(' '*((33-len(row))//2)+row).ljust(33) for row in rows];C=center(data['cipher_rows']);T={name:center(rows) for name,rows in data['models'].items()}
  with gzip.open(self.directory/'aperture-intersections.csv.gz','rt') as f:
   for r in csv.DictReader(f):
    cr,cc,tr,tc=map(int,(r['cipher_row'],r['cipher_grid_column'],r['tableau_row'],r['tableau_grid_column']));self.assertEqual(cr-tr,int(r['dy']));self.assertEqual(cc-tc,int(r['dx']));self.assertEqual(C[cr-1][cc-1],r['cipher_character']);self.assertEqual(T[r['model']][tr-1][tc-1],r['tableau_character'])
    key=f"{r['model']}:{r['dy']}:{r['dx']}";mask=int(r['common_mask']);self.assertEqual(mask,font[r['cipher_character']]&font[r['tableau_character']]);self.assertEqual(m.old.pop(mask),int(r['common_pixels']));grouped[key][0]+=1;grouped[key][1]+=int(r['common_pixels']);grouped[key][2]+=int(r['full_nonempty_mask_coincidence'])
  self.assertEqual(sum(v[0] for v in labels.values()),57674);self.assertEqual(sum(v[0] for v in grouped.values()),1506846)
  for r in self.records:
   self.assertEqual(r['geometric_overlap_cells'],(33-abs(r['dx']))*(28-abs(r['dy'])));self.assertEqual(labels[r['id']][0],r['label_matches']);self.assertEqual(grouped[r['id']],[r['nonempty_common_aperture_pairs'],r['common_pixel_area'],r['full_mask_coincidences']])
 def test_whole_family_exact_tails_and_original_seed_prefix(self):
  e=m.Engine();D=e.D
  for scheme,expected in [('shuffle',[1494,1299]),('rotation',[1526,1217])]:
   report=json.loads((self.directory/f'null-{scheme}.json').read_text());self.assertEqual(report['draws'],1999);self.assertEqual(report['active_frames'],7150);self.assertEqual([x['exceedances'] for x in report['family_endpoints']],expected)
   prefix=m.calibrate(e,self.records,scheme,3,report['seed']);self.assertEqual({n:v[:3] for n,v in report['null_maxima'].items()},prefix['null_maxima'])
   for endpoint,name in enumerate(m.NAMES):
    ordered=sorted(m.exact_key(x['difference_numerator'],x['weight']) for x in report['null_maxima'][name]);tail=report['family_endpoints'][endpoint];key=m.exact_key(tail['actual_maximum']['difference_numerator'],tail['actual_maximum']['weight']);self.assertEqual(1999-bisect.bisect_left(ordered,key),tail['exceedances']);self.assertEqual(tail['plus_one_p'],(tail['exceedances']+1)/2000)
    for actual,saved in zip(self.records,report['per_frame']):
     p=saved['endpoints'][name]
     if not actual['geometric_overlap_cells']:self.assertIsNone(p);continue
     N=actual['expected_numerators'][endpoint];key=m.exact_key(actual[name]*D-N,max(N,D));self.assertEqual(p['family_max_plus_one_p'],(2000-bisect.bisect_left(ordered,key))/2000);self.assertEqual(p['four_report_adjusted_p'],1);self.assertGreaterEqual(p['family_max_plus_one_p'],p['raw_plus_one_p'])
 def test_export_current_register_and_scoped_SIGABA_correction(self):
  rows=list(csv.DictReader(io.StringIO((ROOT/'results/FOLD-SLIDE-2D-001-frames.csv').read_text())));self.assertEqual(len(rows),7638)
  for a,b in zip(self.records,rows):self.assertEqual(a['matched_letters'],b['matched_letters']);self.assertEqual(a['label_matches'],int(b['label_matches']));self.assertEqual(a['geometric_overlap_cells'],int(b['geometric_overlap_cells']))
  import audit_monument_slide_2d_controls as supplement
  retained=json.loads((ROOT/'results/FOLD-SLIDE-2D-CONTROL-SUPPLEMENT-001.json').read_text());self.assertEqual(supplement.audit()['results'],retained['results']);self.assertEqual(retained['truth_in_label_statistic_maximum'],18);self.assertEqual(retained['truth_in_area_statistic_maximum'],18)
  import frontier_assessment as f,exclusion_scope_audit as a
  entries=f.canonical((ROOT/'research/HYPOTHESES.md').read_text());sig=entries['H-SIGABA']['Untested scope'];self.assertIn('12 and 14 controllers',sig);self.assertNotIn('fail before completing a controller',sig);self.assertIn('7,638',entries['H-GLYPH-VIEW']['Tested scope']);self.assertEqual(f.assess(),json.loads((ROOT/'results/FRONTIER-035.json').read_text()));self.assertEqual(a.run(),json.loads((ROOT/'results/EXCLUSION-SCOPE-AUDIT-035.json').read_text()))
def collections_default():
 import collections
 return collections.defaultdict(lambda:[0,0,0])
