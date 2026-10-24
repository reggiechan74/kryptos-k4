import math,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'experiments'))
import projection_concurrence as p
import projection_concurrence_reference as r
class ProjectionTests(unittest.TestCase):
 def setUp(self):self.f=p.fixtures()
 def test_exact_finite_reference(self):
  for name,truth in [('finite',[120,-80]),('distant_finite',[8000,-5000])]:
   f=self.f[name];out=p.fit(f['pairs'],1000,800,f['training']);ref=r.finite_least_squares([f['pairs'][i] for i in f['training']])
   for a,b,c in zip(out['source_image_finite'],ref,truth):self.assertAlmostEqual(a,c,places=6);self.assertAlmostEqual(a,b,places=6)
   q=r.intersection(f['pairs'][0],f['pairs'][3]);self.assertAlmostEqual(q[0]/q[2],truth[0]);self.assertAlmostEqual(q[1]/q[2],truth[1])
 def test_infinite_reference(self):
  f=self.f['infinity'];out=p.fit(f['pairs'],1000,800,f['training']);s=out['source_image_homogeneous'];self.assertLess(abs(s[2]),1e-12);self.assertAlmostEqual(s[1]/s[0],.3)
  q=r.intersection(f['pairs'][0],f['pairs'][3]);self.assertAlmostEqual(q[2],0);self.assertAlmostEqual(q[1]/q[0],.3)
 def test_noiseless_heldout_and_noise(self):
  for name in ('finite','distant_finite','infinity','noisy_finite'):
   f=self.f[name];o=p.diagnose(f['pairs'],1000,800,f['training'],32);self.assertTrue(o['conditional_line_gate_pass'],(name,o['heldout_combined_rms']));self.assertFalse(o['real_data_admission'])
 def test_mutation_and_mixed(self):
  for name in ('heldout_mutation','mixed_sources'):
   f=self.f[name];o=p.diagnose(f['pairs'],1000,800,f['training'],32);self.assertFalse(o['conditional_line_gate_pass']);self.assertGreater(o['heldout_combined_rms'],4)
 def test_degenerate(self):
  f=self.f['coincident_lines'];o=p.fit(f['pairs'],1000,800,f['training']);self.assertIn('nonunique_or_ill_conditioned_source',o['warnings'])
  with self.assertRaisesRegex(ValueError,'collapsed'):p.fit(self.f['collapsed']['pairs'],1000,800,f['training'])
 def test_source_coincident(self):
  pair=dict(aperture=[120,-80],receiver=[150,100],sigma_px=1);s=p.normalize([120,-80],1000,800);self.assertIsNone(p.residual(pair,s,1000,800)['signed_miss_px'])
 def test_covariance_gradient(self):
  coords=[.2,-.3,.8,.4];s=[.5,-.7,.2];x,y,u,v=coords;exact=[-s[1]+v*s[2],s[0]-u*s[2],s[1]-y*s[2],-s[0]+x*s[2]]
  for a,b in zip(exact,r.numerical_gradient(coords,s)):self.assertAlmostEqual(a,b,places=9)
 def test_homography_preserves_incidence(self):
  f=self.f['finite'];h=[[1.1,.15,30],[-.1,.9,40],[.0002,-.0001,1]]
  def transform(v):
   q=[sum(a*b for a,b in zip(row,v+[1])) for row in h];return [q[0]/q[2],q[1]/q[2]]
  pairs=[dict(z,aperture=transform(z['aperture']),receiver=transform(z['receiver'])) for z in f['pairs']];o=p.fit(pairs,1000,800,f['training']);truth=transform([120,-80])
  for a,b in zip(o['source_image_finite'],truth):self.assertAlmostEqual(a,b,places=7)
  for z in pairs:self.assertLess(abs(p.residual(z,o['source_normalized_homogeneous'],1000,800)['signed_miss_px']),1e-7)
 def test_coordinate_scale(self):
  f=self.f['finite'];pairs=[dict(z,aperture=[2*x for x in z['aperture']],receiver=[2*x for x in z['receiver']],sigma_px=2*z['sigma_px']) for z in f['pairs']];o=p.fit(pairs,2000,1600,f['training'])
  self.assertAlmostEqual(o['source_image_finite'][0],240);self.assertAlmostEqual(o['source_image_finite'][1],-160)
 def test_no_full_point_prediction(self):
  f=self.f['finite'];o=p.fit(f['pairs'],1000,800,f['training']);z=f['pairs'][2];a=z['aperture'];s=[120,-80]
  for t in (1.01,2,10):
   changed=dict(z,receiver=[s[j]+t*(a[j]-s[j]) for j in (0,1)]);self.assertLess(abs(p.residual(changed,o['source_normalized_homogeneous'],1000,800)['signed_miss_px']),1e-8)
 def test_eigen_residual(self):
  m=[[4.,1.,2.],[1.,3.,.5],[2.,.5,5.]]
  for val,v in p.eigensystem(m):
   for a,b in zip([p.dot(row,v) for row in m],[val*x for x in v]):self.assertAlmostEqual(a,b,places=10)
 def test_two_line_and_near_parallel_warning(self):
  f=self.f['finite'];self.assertTrue(p.fit(f['pairs'],1000,800,[0,3])['warnings'])
  pairs=[dict(aperture=[100.,1e-10*i],receiver=[200.,2e-10*i],sigma_px=.25) for i in range(12)];self.assertIn('nonunique_or_ill_conditioned_source',p.fit(pairs,1000,800,f['training'])['warnings'])
if __name__=='__main__':unittest.main()

# Parallel distinct lines have rank two and a unique projective infinity source;
# near-coincident lines, rather than parallelism itself, are the degeneracy above.
