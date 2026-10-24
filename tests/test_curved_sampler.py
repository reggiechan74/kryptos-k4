import math,random,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import curved_sampler as c
import curved_sampler_reference as ref
class CurvedSamplerTests(unittest.TestCase):
 def test_analytic_central_and_reciprocity(self):
  eye=(0,-3,2);d=(0,math.cos(math.pi/6),-math.sin(math.pi/6));r=c.ground_ray(eye,d);self.assertEqual(r['status'],'ground');self.assertAlmostEqual(r['point'][1],1-2*math.sqrt(3));self.assertAlmostEqual(r['hit'][1],-1)
  back=tuple(-v for v in r['reflected']);hit=c.first_hit(r['point'],back);self.assertEqual(hit['status'],'side');reverse=c.reflect(back,hit['normal'])
  for a,b in zip(reverse,tuple(-v for v in r['incoming'])):self.assertAlmostEqual(a,b)
 def test_cap_miss_parallel_and_rim(self):
  self.assertEqual(c.ground_ray((0,-3,1),(1,0,0))['status'],'miss');self.assertEqual(c.ground_ray((0,-3,4),(0,3,-2))['status'],'cap');self.assertEqual(c.ground_ray((0,-3,1),(0,1,0))['status'],'ground_miss');self.assertEqual(c.ground_ray((0,-3,2),(0,1,-1))['status'],'rim')
 def test_independent_seeded_rays_and_reflection_law(self):
  rng=random.Random(360023);count=0
  for _ in range(200):
   eye=(rng.uniform(-.1,.1),-rng.uniform(2,4),rng.uniform(1.2,2.4));angle=rng.uniform(15,45);f,right,up=c.basis(angle);d=c.norm(c.add(c.add(f,right,rng.uniform(-.15,.15)),up,rng.uniform(-.03,.03)));a=c.ground_ray(eye,d);b=ref.trace(eye,d);self.assertEqual(a['status'],b['status'])
   if a['status']=='ground':
    count+=1
    for x,y in zip(a['point'],b['point']):self.assertAlmostEqual(x,y,places=9)
    self.assertAlmostEqual(c.dot(a['reflected'],a['reflected']),1);self.assertAlmostEqual(c.dot(a['incoming'],a['normal']),-c.dot(a['reflected'],a['normal']))
  self.assertGreater(count,20)
 def test_reticle_cells_and_near_boundary(self):
  self.assertEqual(len(c.RETICLE),97);self.assertEqual([(p['row'],p['column']) for p in c.RETICLE[:4]],[(0,i) for i in range(27,31)])
  rows=['A'*31 for _ in range(28)];params=dict(tx=0,ty=0,rotation_deg=0,pitch=1)
  self.assertEqual(c.table_cell((0,.5,0),params,rows)['status'],'valid');self.assertEqual(c.table_cell((.5,.5,0),params,rows)['status'],'boundary');self.assertEqual(c.table_cell((100,0,0),params,rows)['status'],'outside')
  rows[13]=' '*31;self.assertEqual(c.table_cell((0,.5,0),params,rows)['status'],'blank')
 def test_fixed_reticle_pupil_and_cipher_recovery(self):
  params=dict(D=3,H=2,s=.02,aim_deg=30,tx=0,ty=-2,rotation_deg=0,pitch=.1)
  a=c.trace(params,0,0);b=c.trace(params,0,0,(0,0,0),True);self.assertEqual(a['status'],b['status'])
  for x,y in zip(a['point'],b['point']):self.assertAlmostEqual(x,y,places=9)
  rng=random.Random(360025);plain=''.join(rng.choice(c.ALPHABET) for _ in range(97));key=c.ALPHABET*3+c.ALPHABET[:19];self.assertEqual(len(key),97);cipher=c.encrypt(plain,key);self.assertEqual(c.encrypt(cipher,key,True),plain)
  known={i:plain[i] for i in list(range(21,34))+list(range(63,74))};out=c.recover_keys(cipher,known,{key:['plant'],key[::-1]:['wrong']});self.assertTrue(any(row['key']==key for row in out['full24_candidates']))
