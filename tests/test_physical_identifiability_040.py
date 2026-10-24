import hashlib,json,sys,unittest
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import physical_identifiability_040 as p
class PhysicalIdentifiability040Tests(unittest.TestCase):
 def test_three_distinct_physical_realizations_have_identical_image_pairs(self):
  rows=p.fixtures();self.assertEqual(len(rows),12)
  for row in rows:
   P=tuple(map(F,row['receiver']));self.assertEqual(P[2],10)
   for r in row['realizations']:
    A=tuple(map(F,r['aperture']));self.assertEqual(p.project(A),tuple(map(F,row['image_aperture'])));self.assertLess(A[2],P[2]);self.assertGreater(A[2],0)
    if r['type']=='finite_point_source':L=tuple(map(F,r['source']));self.assertEqual(p.cross(p.sub(A,L),p.sub(P,L)),(0,0,0))
 def test_controls_do_not_claim_real_fit_source_type_or_depth(self):
  r=json.loads((ROOT/'results/PHYSICAL-IDENTIFIABILITY-040-ORIGINAL.json').read_text());self.assertEqual(r['certified_real_pairs'],0);self.assertEqual(r['K4_trials'],0);self.assertFalse(r['physical_monument_fit']);self.assertIsNotNone(r['fit']['source_image_finite']);self.assertLess(r['maximum_heldout_incidence_miss_px'],1e-9);self.assertGreater(abs(r['local_wrong_match_miss_px']),70)
  for path,sha in r['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),sha)
 def test_scale_similarity_and_wrong_radius_control(self):
  r=p.run();self.assertEqual(r['scale_rays'],291);self.assertEqual(r['wrong_radius_negative_changes'],194)
  for s in r['scale_checks']:self.assertTrue(s['dimensionless_cells_equal']);self.assertLess(s['maximum_absolute_point_error'],1e-9)
