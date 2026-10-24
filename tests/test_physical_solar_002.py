import importlib.util
import math
from pathlib import Path
import unittest
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('physical002', ROOT/'experiments/physical_solar_002.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class PhysicalSolarTests(unittest.TestCase):
    def test_julian_epoch_and_timezone(self):
        self.assertEqual(m.solar_usno(datetime(2000,1,1,12,tzinfo=timezone.utc))['jd'],2451545)
        with self.assertRaises(ValueError):
            m.solar_usno(datetime(2000,1,1))

    def test_enu_inverse_complete_declared_grid(self):
        for lat in (-60, 0, 38.951, 60):
            for dec in (-23.5, 0, 23.5):
                for hour in range(-180,181,10):
                    v = m.horizontal(lat,dec,hour)
                    self.assertAlmostEqual(sum(x*x for x in v['enu']),1,places=12)
                    self.assertAlmostEqual(m.required_declination(lat,v['azimuth'],v['altitude']),dec,places=10)

    def test_analytic_limits_and_solar_shadow_direction(self):
        # Equatorial equinox: east horizon, zenith transit, west horizon.
        self.assertAlmostEqual(m.horizontal(0,0,-90)['azimuth'],90)
        self.assertAlmostEqual(m.horizontal(0,0,90)['azimuth'],270)
        self.assertAlmostEqual(m.horizontal(0,0,0)['altitude'],90)
        # Direct source vector at ENE: ray points WSW, not ENE.
        a,h=map(math.radians,(67.5,10))
        v=(math.cos(h)*math.sin(a),math.cos(h)*math.cos(a),math.sin(h))
        result=m.ray_plane([v[0],v[1],1+v[2]],[0,0,1],0)
        x,y,_=result['intersection']
        bearing=math.degrees(math.atan2(x,y))%360
        self.assertAlmostEqual(bearing,247.5)
        self.assertNotAlmostEqual(bearing,67.5)

    def test_grid_roots_and_boundary_branches(self):
        for az in (0,67.5,90,180,247.5,270):
            for lat in (-38.951,0,38.951):
                row=m.envelope(lat,az,23.5,-.833)
                self.assertEqual(m.independent_grid_check(row,1000),1001)

    def test_lamp_height_order_and_countermodels(self):
        # Below-ground emitter, higher aperture, intermediate ground: no forward hit.
        self.assertEqual(m.ray_plane([0,0,-1],[1,1,2],0)['status'],'behind_aperture')
        # A higher receiver and a source above the aperture are different models.
        self.assertEqual(m.ray_plane([0,0,-1],[1,1,2],3)['status'],'forward')
        self.assertEqual(m.ray_plane([0,0,3],[1,1,2],0)['status'],'forward')
        self.assertEqual(m.ray_plane([0,0,2],[1,1,2],0)['status'],'parallel_disjoint')
        self.assertEqual(m.ray_plane([0,0,2],[1,1,2],2)['status'],'coplanar')
        self.assertEqual(m.ray_plane([1,1,2],[1,1,2],2)['status'],'degenerate_source_at_aperture')

    def test_fixed_date_approximations_and_calendar_domain(self):
        rows=m.date_samples()
        self.assertEqual(len(rows),39)
        self.assertEqual(sum(role.startswith('month_') for role,_ in rows),30)
        for _,instant in rows:
            a,b=m.solar_usno(instant),m.solar_noaa(instant)
            self.assertLessEqual(abs(a['declination']-b['declination']),.75)
            self.assertLessEqual(abs(a['equation_of_time_minutes']-b['equation_of_time_minutes']),2)

    def test_legacy_bounds_are_prior_coverage(self):
        self.assertAlmostEqual(m.envelope(38.95,67.5,23.44,0)['reachable_altitude_intervals'][0][1],9.548,delta=.01)
        self.assertAlmostEqual(m.envelope(38.95,247.5,23.44,0)['reachable_altitude_intervals'][0][1],60.22,delta=.02)

if __name__=='__main__':unittest.main()
