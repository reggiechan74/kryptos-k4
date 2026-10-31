"""Portable regression replays of the independently frozen literal-check fixtures.
These are replay tests, NOT a new blinded validation dataset.
"""
import base64
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT=Path(__file__).resolve().parents[1]
TOOL=ROOT/'experiments/source_literal_check.py'
ARCHIVE=ROOT/'research/source-literal-checker-v1/source-literal-checker-v1-evidence.zip'
spec=importlib.util.spec_from_file_location('source_literal_check_under_test',TOOL)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

class SourceLiteralCheckTests(unittest.TestCase):
 def test_frozen_source_identical(self):
  with zipfile.ZipFile(ARCHIVE) as z:
   self.assertEqual(TOOL.read_bytes(),z.read('original/literal_check.py'))
   freeze=json.loads(z.read('original/FREEZE.json'))
   self.assertEqual(hashlib.sha256(z.read('original/FREEZE.json')).hexdigest(),'29e3912f38661c9304adf37586d22801b0c610bfd866abe899d976d982c263d8')
   for name,digest in freeze['files'].items():self.assertEqual(hashlib.sha256(z.read('original/'+name)).hexdigest(),digest)
 def test_archive_and_independent_fixture_freeze(self):
  with zipfile.ZipFile(ARCHIVE) as z:
   manifest=json.loads(z.read('ARCHIVE-MANIFEST.json'))
   for name,record in manifest.items():self.assertEqual(hashlib.sha256(z.read(name)).hexdigest(),record['sha256'])
   frozen=json.loads(z.read('independent/FROZEN-FIXTURES.json'))
   for name,digest in frozen.items():self.assertEqual(hashlib.sha256(z.read('independent/'+name)).hexdigest(),digest)
 def test_81_frozen_synthetic_cli_cases(self):
  with zipfile.ZipFile(ARCHIVE) as z:cases=json.loads(z.read('independent/fixtures.json'))
  self.assertEqual(len(cases),81)
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);src=p/'source.py';req=p/'request.json'
   for case in cases:
    with self.subTest(case=case['id']):
     source=base64.b64decode(case['source_b64']);src.write_bytes(source)
     request={'sha256':case.get('hash_override',hashlib.sha256(source).hexdigest()),'provenance':case.get('provenance','independent synthetic fixture; not historical provenance'),'assignment':case['assignment'],'key':case['key'],'expected':case['expected']}
     req.write_text(json.dumps(request));r=subprocess.run([sys.executable,str(TOOL),str(req),str(src)],capture_output=True,timeout=5,cwd=d)
     result=json.loads(r.stdout);self.assertEqual(result['status'],case['expected_status']);self.assertEqual(r.returncode,0 if case['expected_status']=='PASS' else 2)
     if result['status']=='PASS':self.assertEqual(result['actual'],case['expected']);self.assertIn('not validated',result['limitation'])
 def test_three_malformed_cli_requests(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);src=p/'source.py';src.write_text('X={}');req=p/'request.json'
   for raw in [b'{"sha256":"x","sha256":"y"}',b'{',b'\xff']:
    req.write_bytes(raw);r=subprocess.run([sys.executable,str(TOOL),str(req),str(src)],capture_output=True,timeout=5);self.assertEqual(r.returncode,2);self.assertEqual(json.loads(r.stdout)['status'],'FAIL')
 def test_motivating_pair_regression_without_external_source(self):
  source=b"ERRnums={'shifts_ST':tuple((ord(b)-ord(a))%26 for a,b in ('LQ','OU','EA','IE'))}\n"
  for pair,status in [('EA','PASS'),('AE','FAIL')]:
   request={'sha256':hashlib.sha256(source).hexdigest(),'provenance':'synthetic regression, not external source','assignment':'ERRnums','key':'shifts_ST','expected':['LQ','OU',pair,'IE']};self.assertEqual(module.verify(source,request)['status'],status)
 def test_nonsemantic_limitations_remain_explicit(self):
  source=b"tuple=lambda x:None\nPOOL={'key':tuple(evil(x) for x in ('EA','IE'))}\nPOOL.update({})\nalias=POOL\nalias['key']=None\n"
  request={'sha256':hashlib.sha256(source).hexdigest(),'provenance':'synthetic lexical scope test','assignment':'POOL','key':'key','expected':['EA','IE']}
  result=module.verify(source,request);self.assertEqual(result['status'],'PASS');self.assertIn('runtime behavior',result['limitation'])
 def test_all_selected_dictionary_keys_must_be_strings(self):
  source=b"POOL={'key':[x for x in ('EA',)],1:2}"
  request={'sha256':hashlib.sha256(source).hexdigest(),'provenance':'synthetic','assignment':'POOL','key':'key','expected':['EA']}
  self.assertEqual(module.verify(source,request)['reason'],'DYNAMIC_OR_UNPACKED_KEY')

if __name__=='__main__':unittest.main()
