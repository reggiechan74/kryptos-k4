"""Fresh synthetic tests only; no K4 data loaded or key arithmetic performed."""
import copy
import hashlib
import tempfile
import unittest
from pathlib import Path
import checker as c

class Tests(unittest.TestCase):
 def fixture(self):
  context={'q':3,'coordinates':[0,2,4], 'equation':'C=P+K', 'alphabet':'ABC', 'normalization':'identity','alignment':'same'}
  index={'context':context,'records':[{'id':'synthetic','receipt_pointer':'/rows/0','status':'completed_exact_negative','key_domain':'unrestricted_mod_q','partition':[0,0,1]}]}
  request={'context':copy.deepcopy(context),'partition':[8,8,8],'domain':{'kind':'unrestricted_mod_q'}}
  return index,request
 def test_containment(self):
  self.assertTrue(c.contains([0,1,2],[0,0,0]));self.assertFalse(c.contains([0,0,0],[0,1,2]))
  self.assertFalse(c.contains([0,0,1],[0,1,1]));self.assertTrue(c.contains([9,9,4],[3,3,7]))
 def test_decision(self):
  i,r=self.fixture();self.assertEqual(c.check_request(i,r)['decision'],'inherited_negative')
  r['partition']=[0,1,2];self.assertEqual(c.check_request(i,r)['decision'],'no_certificate')
 def test_ineligible(self):
  for status in ['positive','skipped','threshold_skipped','heuristic','unknown','incomplete']:
   i,r=self.fixture();i['records'][0]['status']=status
   self.assertEqual(c.check_request(i,r)['decision'],'no_certificate')
 def test_restricted_old(self):
  i,r=self.fixture();i['records'][0]['key_domain']='restricted';self.assertEqual(c.check_request(i,r)['decision'],'no_certificate')
 def test_context(self):
  for key in self.fixture()[0]['context']:
   i,r=self.fixture();r['context'][key]='changed'
   with self.assertRaises(ValueError):c.check_request(i,r)
 def test_labels(self):
  for labels in [[],[0,True,0],[0,1.0,0],[0,-1,0],[0],[0,0,0,0],['0',0,0]]:
   i,r=self.fixture();r['partition']=labels
   with self.assertRaises(ValueError):c.check_request(i,r)
 def test_domains(self):
  i,r=self.fixture();r['domain']={'kind':'per_class_values','allowed_values':[[0,2]]}
  self.assertEqual(c.check_request(i,r)['decision'],'inherited_negative')
  for domain in [{'kind':'claimed_subset'}, {'kind':'per_class_values','allowed_values':[[True]]}, {'kind':'per_class_values','allowed_values':[[3]]}, {'kind':'per_class_values','allowed_values':[[]]}, {'kind':'per_class_values','allowed_values':[[0,0]]}]:
   r['domain']=domain
   with self.assertRaises(ValueError):c.check_request(i,r)
 def test_hash(self):
  with tempfile.TemporaryDirectory() as d:
   Path(d,'receipt').write_bytes(b'synthetic'); h=hashlib.sha256(b'synthetic').hexdigest()
   self.assertEqual(c.checked_bytes(d,'receipt',h),b'synthetic')
   Path(d,'receipt').write_bytes(b'corrupted')
   with self.assertRaises(ValueError):c.checked_bytes(d,'receipt',h)
 def test_json(self):
  for text in ['{"q":2,"q":3}', '{"v":NaN}', '{"v":Infinity}']:
   with self.assertRaises(ValueError):c.load_json(text)
 def test_no_free_key_veto(self):
  i,r=self.fixture();i['records'][0].update(partition=[0,1,2],status='ineligible')
  self.assertEqual(c.check_request(i,r)['decision'],'no_certificate')
if __name__=='__main__':unittest.main()
