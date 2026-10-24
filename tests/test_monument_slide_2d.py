import csv,gzip,io,json,random,sys,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import monument_slide_2d as m
class TwoDimensionalOverlayTests(unittest.TestCase):
 def test_frozen_domain_and_sources_before_evaluation(self):
  import hashlib
  spec=json.loads(m.SPEC.read_text());self.assertEqual(spec['raw_frames'],2*67*57);self.assertEqual(spec['active_frames'],2*65*55);self.assertEqual(spec['new_nonzero_row_frames'],7504)
  for p,h in spec['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),h)
 def test_planted_full_selector_and_exact_small_system_controls(self):
  r=m.controls();self.assertFalse(r['failures']);self.assertEqual(len(r['plants']),18);self.assertTrue(all(p['truth'] in p['winners'] for p in r['plants']));self.assertEqual(len(r['ambiguous_tie_fixture']),2);self.assertFalse(r['actual_new_rankings_examined'])
 def test_lossless_full_position_outputs_and_boundaries(self):
  data=m.toy_data(['ABC','?CA'],{'ONE':['BAC','A? '],'TWO':['CAB',' CA']},[(0,0)]);e=m.Engine(data);r,files=m.actual(e);again,files2=m.actual(e);self.assertEqual(files,files2)
  labels=list(csv.DictReader(io.StringIO(gzip.decompress(files['label-matches.csv.gz']).decode())));optics=list(csv.DictReader(io.StringIO(gzip.decompress(files['aperture-intersections.csv.gz']).decode())));self.assertEqual(len(labels),r['label_position_rows']);self.assertEqual(len(optics),r['aperture_position_rows'])
  for row in optics:self.assertEqual(m.old.pop(int(row['common_mask'])),int(row['common_pixels']))
  for frame in r['records']:
   self.assertEqual(frame['geometric_overlap_cells'],(3-abs(frame['dx']))*(2-abs(frame['dy'])))
   if abs(frame['dx'])==3 or abs(frame['dy'])==2:self.assertIsNone(frame['common_over_union']);self.assertFalse(frame['label_positions'])
 def test_whole_selector_null_replay_invariants_and_exact_maxima(self):
  data=m.toy_data(['ABC','?CA'],{'ONE':['BAC','A? '],'TWO':['CAB',' CA']},[(0,0)]);e=m.Engine(data);r,_=m.actual(e,False)
  for scheme in ('shuffle','rotation'):
   result=m.calibrate(e,r['records'],scheme,7,17);repeat=m.calibrate(e,r['records'],scheme,7,17);self.assertEqual(result['null_maxima'],repeat['null_maxima']);rng=random.Random(17)
   for draw in range(7):
    source=e.base.surrogate(rng,scheme)
    for i in e.base.fixed:self.assertEqual(source[i],e.base.base[i])
    for row,positions in enumerate(e.base.free):self.assertEqual(sorted(source[i] for i in positions),sorted(e.base.base[i] for i in positions))
    rows=[''.join(m.old.SYMBOLS[source[rr*3+c]] for c in range(3)) for rr in range(2)];independent=m.oracle(m.toy_data(rows,data['models']))['records']
    for endpoint,name in enumerate(m.NAMES):
     keys=[(m.exact_key(independent[i][name]*e.D-e.expected[endpoint][i],e.weights[endpoint][i]),i) for i in e.active];best=max(k for k,i in keys);saved=result['null_maxima'][name][draw];self.assertEqual(m.exact_key(saved['difference_numerator'],saved['weight']),best)
   for frame in result['per_frame']:
    for p in frame['endpoints'].values():
     if p is not None:self.assertGreaterEqual(p['family_max_plus_one_p'],p['raw_plus_one_p']);self.assertGreaterEqual(p['four_report_adjusted_p'],p['family_max_plus_one_p'])
 def test_no_carry_full_masks_and_wrong_packed_result_rejected(self):
  data=m.toy_data(['AAA','AAA'],{'ONE':['AAA','AAA']});e=m.Engine(data,{'glyph_rows':{'A':['11111']*7}});scores=e.score(e.base.base);i=next(i for i,f in enumerate(e.frames) if f['dx']==f['dy']==0);self.assertEqual(scores[0][i],6);self.assertEqual(scores[1][i],210)
  with patch.object(e,'score',return_value=[[0]*len(e.frames),[0]*len(e.frames)]),self.assertRaises(AssertionError):m.actual(e,False)
  with self.assertRaises(TimeoutError):m.budget(0,-1)

 def test_future_replays_are_labelled_separately_from_original_run(self):
  import inspect,subprocess
  self.assertEqual(inspect.signature(m.run).parameters['execution_kind'].default,'replay')
  help_text=subprocess.check_output([sys.executable,str(ROOT/'experiments/monument_slide_2d.py'),'--help']).decode();self.assertIn('--execution-kind {original,replay}',help_text)
