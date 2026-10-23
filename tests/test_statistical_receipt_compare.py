import copy,gzip,json,math,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
from statistical_receipt_compare import compare,close_float
class ReceiptRoundingTests(unittest.TestCase):
 def test_rational_moments_validate_unchanged_archived_receipt(self):
  old=json.loads(gzip.decompress((ROOT/'results/STAT-001.json.gz').read_bytes()))
  self.assertTrue(compare(old,old)['rational_mean_variance_reference'])
 def test_controls_do_not_hide_mutations(self):
  old=json.loads(gzip.decompress((ROOT/'results/STAT-001.json.gz').read_bytes()))
  for field in ('raw_draws','evaluation_maxima_z','calibration_means','calibration_sample_sd','maximum_over_48_widths'):
   mutated=copy.deepcopy(old)
   if field=='raw_draws':mutated[field][0][0]+=1
   elif field=='maximum_over_48_widths':mutated[field]['evaluation_exceedances']+=1
   else:mutated[field][0]+=1e-9
   with self.assertRaises(AssertionError):compare(mutated,old)
  for x in (math.inf,math.nan):
   with self.assertRaises(AssertionError):close_float(x,1.0)
  self.assertLessEqual(close_float(math.nextafter(1.0,2.0),1.0),1)
