import gzip,json,math,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import site_cylinder_validation as s
class SiteCylinderValidationTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.source=json.load(gzip.open(ROOT/'results/SITE-CYLINDER-037-SOURCE-SNAPSHOT.json.gz','rt'));cls.rows=cls.source['tableau_rows']
 def test_source_default_and_all_invalid_fixtures(self):
  for case in self.source['cases']:
   actual=s.generate(case['state'],self.rows);self.assertEqual(actual['key'],case['result']['key']);self.assertEqual(actual['validCount'],case['result']['validCount'])
   for a,b in zip(actual['samples'],case['result']['samples']):
    self.assertEqual(a['status'],b['status'])
    for k in ('eye','reticle','hit','normal','eyeToMirror','reflectedTrace','tableauPoint'):
     if k in a and k in b:
      for x,y in zip(a[k],b[k]):self.assertAlmostEqual(x,y,delta=1e-9)
    if a['status']=='valid':self.assertEqual(a['cell'],b['cell']);self.assertEqual(a['source']['column'],b['source']['column']);self.assertEqual(a['key'],b['key'])
 def test_normal_incidence_reciprocity_and_fixed_pupil(self):
  p=s.sample(s.DEFAULTS,20,self.rows);self.assertAlmostEqual(p['hit'][0],0);self.assertAlmostEqual(p['hit'][2],.8);self.assertAlmostEqual(p['hit'][1],1.56);self.assertAlmostEqual(p['tableauPoint'][1],1.6575)
  reverse=s.reflected(tuple(-v for v in p['reflectedTrace']),p['normal'])
  for a,b in zip(reverse,tuple(-v for v in p['eyeToMirror'])):self.assertAlmostEqual(a,b,delta=1e-9)
  q=s.sample(s.DEFAULTS,20,self.rows,{'eyeX':.001});self.assertEqual(q['reticle'],p['reticle']);self.assertNotEqual(q['eye'],p['eye'])
 def test_source_ranges_and_low_level_failures(self):
  for value in (float('nan'),float('inf'),0,9):
   with self.assertRaises(ValueError):s.validate(dict(s.DEFAULTS,radius=value))
  for override in ({'selected':1.5},{'tableauDistance':4},{'sampleOverrides':{1:'A'}},{'obstruction':'false'}):
   with self.assertRaises(ValueError):s.validate(dict(s.DEFAULTS,**override))
  for case in self.source['low_level']:self.assertEqual(s.hit(case['eye'],case['direction'],case['radius'])['status'],case['result']['status'])
 def test_zero_board_transform_and_rigid_frame(self):
  a=s.generate(s.DEFAULTS,self.rows);b=s.generate(s.DEFAULTS,self.rows,dict(boardPitchDeg=0,boardYawDeg=0,boardRollDeg=0));self.assertEqual(a,b)
  for angles in ((.1,.1,.1),(0,.1,0),(.1,0,0),(0,0,.1)):
   right,up,normal=[s.rotate(v,angles) for v in ((1,0,0),(0,1,0),(0,0,1))]
   for v in (right,up,normal):self.assertAlmostEqual(s.dot(v,v),1)
   self.assertAlmostEqual(s.dot(right,up),0);self.assertAlmostEqual(s.dot(right,normal),0);self.assertAlmostEqual(s.dot(up,normal),0)
 def test_frozen_neighborhood_global_and_codec(self):
  rows=list(s.neighborhood());self.assertEqual(len(rows),729);self.assertEqual(len({tuple(x[1][k] for k in s.PARAMS) for x in rows}),729);self.assertEqual(sum(x[1]==s.DEFAULTS for x in rows),1)
  for _,state in rows:s.validate(state)
  default=s.generate(s.DEFAULTS,self.rows);cipher=s.addition(self.source['synthetic']['message'],default['key']);self.assertEqual(cipher,self.source['synthetic']['cipher']);self.assertEqual(s.addition(cipher,default['key'],True),self.source['synthetic']['message'])
 def test_card_touch_and_explicit_transcript_registration(self):
  self.assertTrue(s.blocked((0,1,4),(0,1,.8)));self.assertFalse(s.blocked((2,1,4),(2,1,.8)));self.assertEqual(len(self.rows),28);self.assertFalse(self.rows[0].startswith(' '));self.assertEqual(self.rows[14].count('L'),2)
