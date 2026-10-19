import json,math,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'experiments'))
from landmark_geometry import *
from landmark_inventory import date_rows

class LandmarkAxisTests(unittest.TestCase):
    def test_official_server_reprojection_reference(self):
        x=json.loads((Path(__file__).resolve().parents[1]/'data/landmark-axis/geodetic-control.json').read_text())
        for p in x['pairs']:
            lon,lat=p['lon_lat_reference'];self.assertLess(math.dist(utm(lat,lon),p['utm33_source']),.02)
    def test_geodesic_independent_equator_and_meridian(self):
        self.assertAlmostEqual(inverse(0,0,0,1)[0],A*math.pi/180,places=5)
        # Simpson integration of the meridional curvature, separate from Vincenty.
        n=10000;h=(math.pi/2)/n
        def mer(p):return A*(1-E2)/(1-E2*math.sin(p)**2)**1.5
        reference=h/3*(mer(0)+mer(math.pi/2)+sum((4 if i%2 else 2)*mer(i*h) for i in range(1,n)))
        self.assertLess(abs(inverse(0,0,90,0)[0]-reference),.002)
        for angle in (0,12.3,67.5,179.99,247.5,359):
            p=direct(*ORIGIN,angle,5000);d,b=inverse(*ORIGIN,*p);self.assertLess(abs(d-5000),.001);self.assertLess(abs((b-angle+180)%360-180),1e-7)
    def test_utm_roundtrip_region(self):
        for p in [(52.47,13.33),ORIGIN,(52.57,13.49)]:self.assertLess(inverse(*p,*unutm(*utm(*p)))[0],.002)
    def test_holes_multiparts_and_nested_units(self):
        outer=[[-10,-10],[10,-10],[10,10],[-10,10],[-10,-10]];hole=[[-2,-2],[2,-2],[2,2],[-2,2],[-2,-2]]
        poly=[[outer,hole]];self.assertFalse(inside((0,0),poly));self.assertTrue(inside((5,0),poly));self.assertTrue(inside((2,0),poly))
        child=[[[[3,3],[4,3],[4,4],[3,4],[3,3]]]];self.assertTrue(contained(child,poly));self.assertFalse(contained([[[[-1,-1],[1,-1],[1,1],[-1,1],[-1,-1]]]],poly))
        self.assertTrue(contained(poly,poly))
    def test_support_disk_endpoint_tangent_and_centroid_outside(self):
        self.assertTrue(hit(segment_support((4990,-10),(4990,10)),90))
        self.assertFalse(segment_support((5001,-10),(5001,10)))
        self.assertTrue(hit(segment_support((5000,-10),(5000,10)),90))
        self.assertEqual(segment_support((-1,0),(1,0)),[[0.,360.]])
        self.assertTrue(hit(axis_intervals([[247,248]]),67.5))
    def test_angular_support_against_independent_ray_intersections(self):
        shapes=[[[[20,10],[30,10],[30,20],[20,20],[20,10]]],[[[-30,10],[-20,10],[-20,20],[-30,20],[-30,10]]],[[[4990,-30],[5010,-30],[5010,30],[4990,30],[4990,-30]]]]
        for rings in shapes:
            intervals=merge_intervals([iv for a,b in segments([rings]) for iv in segment_support(a,b)])
            for i in range(1440):
                az=i/4;ray=(5000*math.sin(math.radians(az)),5000*math.cos(math.radians(az)));expected=False
                for a,b in segments([rings]):
                    s=(b[0]-a[0],b[1]-a[1]);den=ray[0]*s[1]-ray[1]*s[0]
                    if abs(den)<1e-12:continue
                    t=(a[0]*s[1]-a[1]*s[0])/den;u=(a[0]*ray[1]-a[1]*ray[0])/den
                    if -1e-10<=t<=1+1e-10 and -1e-10<=u<=1+1e-10:expected=True
                self.assertEqual(hit(intervals,az),expected,(az,rings))
    def test_primary_date_parsing_doesnot_use_design_or_subobjects(self):
        page='<table><tr><td>Obj.-Dok.-Nr.</td><td>1</td></tr><tr><td>Entwurf</td><td>1880</td></tr><tr><td>Fertigstellung</td><td>1890-1892</td></tr></table><table><tr><td>Datierung</td><td>2000</td></tr></table>'
        dates,fields,raw=date_rows(page);self.assertEqual(dates,[1892]);self.assertEqual(len(raw),1)
        dates,_,_=date_rows(page.replace('1890-1892','um 1890'));self.assertEqual(dates,[])
    def test_descriptive_angular_measure_and_ties(self):
        from landmark_axis import continuous,stats
        x=continuous([[[0,90]],[[45,135]]],2)
        self.assertEqual(x['angular_measure_deg'],{0:45.0,1:90.0,2:45.0});self.assertEqual(x['equal_or_higher_angular_fraction'],.25);self.assertEqual(x['median_count'],1)
        s=stats([1,2,2,3],2);self.assertEqual(s['strict_rank_best_is1'],2);self.assertEqual(s['tied_orientations'],2);self.assertEqual(s['equal_or_higher_angular_fraction'],.75)
