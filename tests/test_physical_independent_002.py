import json
import math
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'independent/2026-10-24/physical-item2'

class IndependentPhysicalTests(unittest.TestCase):
    def test_solar_cone_boundary_against_independent_ray_ellipse(self):
        data=json.loads((BASE/'physical-constraints.json').read_text())
        rho=math.radians(data['constants']['sun_full_angular_diameter_arcsec']/7200)
        for row in data['solar_blur_per_metre_height']:
            h=math.radians(row['elevation_deg'])
            q=math.sin(h)**2-math.sin(rho)**2
            center=math.sin(h)*math.cos(h)/q
            major_radius=math.sin(rho)*math.cos(rho)/q
            minor_radius=math.sin(rho)/math.sqrt(q)
            self.assertAlmostEqual(major_radius*2,row['exact_major_m'],places=12)
            self.assertAlmostEqual(minor_radius*2,row['exact_minor_m'],places=12)
            for deg in range(360):
                t=math.radians(deg)
                # Independent cone ray: central axis plus orthogonal tangents.
                x=math.cos(rho)*math.cos(h)-math.sin(rho)*math.cos(t)*math.sin(h)
                y=math.sin(rho)*math.sin(t)
                z=math.cos(rho)*math.sin(h)+math.sin(rho)*math.cos(t)*math.cos(h)
                self.assertGreater(z,0)
                self.assertAlmostEqual(((x/z-center)/major_radius)**2+(y/z/minor_radius)**2,1,places=10)

    def test_channel_thresholds_and_interval_overlap(self):
        rows=json.loads((BASE/'physical-constraints.json').read_text())['hypothetical_straight_channel_clipping']
        self.assertEqual(len(rows),9)
        for row in rows:
            w,t,theta=row['width_mm'],row['thickness_mm'],math.radians(row['zero_overlap_threshold_deg'])
            self.assertAlmostEqual(t*math.tan(theta),w,places=12)
            for fraction in (0,.5,1,1.1):
                displacement=w*fraction
                # Intersection of independently shifted front/back intervals.
                length=max(0,min(w,w+displacement)-max(0,displacement))
                self.assertAlmostEqual(length,max(0,w-abs(displacement)))

    def test_receipt_and_provenance(self):
        import hashlib
        receipt=json.loads((BASE/'LOCAL-REPLAY-RECEIPT.json').read_text())
        self.assertEqual(receipt['status'],'passed')
        for name,expected in receipt['local_outputs'].items():
            self.assertEqual(hashlib.sha256((BASE/name).read_bytes()).hexdigest(),expected)
        self.assertIsNone(receipt['original_worker_run_start_utc'])
        self.assertIsNone(receipt['original_worker_run_end_utc'])

if __name__=='__main__':unittest.main()
