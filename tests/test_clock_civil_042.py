import datetime,hashlib,io,json,sys,unittest,zoneinfo
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import clock_civil_042 as c
class ClockCivil042Tests(unittest.TestCase):
 def test_full_year_independent_calendar_and_timezone_tables(self):
  r=json.loads((ROOT/'results/CLOCK-CIVIL-042-ORIGINAL.json').read_text());z={k:zoneinfo.ZoneInfo.from_file(io.BytesIO(bytes.fromhex(v)),key=k) for k,v in r['tzif_hex'].items()};self.assertEqual(json.loads(json.dumps(c.analyze(z))),r['analysis']);self.assertEqual(r['analysis']['civil_difference_hour_counts'],{'0':840,'60':7920});self.assertFalse(r['analysis']['any_constant_difference_fits_whole_year']);self.assertEqual(r['analysis']['independent_offset_comparisons'],17538)
  for p,h in r['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),h)
 def test_transition_boundaries_not_selected_for_K4(self):
  b=c.boundaries();self.assertEqual(b['both_start'].isoformat(),'1989-03-26T01:00:00+00:00');self.assertEqual(b['Berlin_end'].isoformat(),'1989-09-24T01:00:00+00:00');self.assertEqual(b['London_end'].isoformat(),'1989-10-29T01:00:00+00:00')
  for key in ('Europe/Berlin','Europe/London'):
   self.assertEqual(c.reference(datetime.datetime(1989,1,1,tzinfo=c.UTC),key),60 if key.endswith('Berlin') else 0)
 def test_fixed_standard_time_positive_and_common_DST_negative(self):
  r=json.loads((ROOT/'results/CLOCK-CIVIL-042-ORIGINAL.json').read_text());passed=0
  for hour in range(8760):
   phase=(hour*60)%1440;berlin=(phase+60)%1440;london=phase;passed+=((berlin-london)%1440==60)
  self.assertEqual(passed,r['analysis']['positive_fixed_standard_time_model_hours']);self.assertEqual(8760-r['analysis']['constant_integer_sector_fit_hours']['1'],840);self.assertEqual(r['K4_trials'],0);self.assertFalse(r['actual_clock_layout_assumed'])
