"""Small synthetic/library and retained-artifact checks; never reruns target search."""
import hashlib,itertools,json,sys,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import recurrence_clock as clock
D=ROOT/'research/candidate-first-064'
class RecurrenceClockTests(unittest.TestCase):
 def test_cyclic_primitive_and_fixed_key_inverse(self):
  self.assertTrue(clock.primitive([0,1,0]));self.assertFalse(clock.primitive([0,1,0,1]))
  for p in range(2,9):
   self.assertFalse(clock.primitive([25]*p));k=list(range(p));text=[(7*i+3)%26 for i in range(97)]
   self.assertEqual(clock.decrypt(clock.encrypt(text,k),k),text)
 def test_complete_small_seed_and_projection_relation(self):
  for p in range(2,5):
   for c in itertools.product(range(2),repeat=3):
    for v in range(2):
     known=[[1,v]];truth=[(k,clock.decrypt(c,k,2)) for k in itertools.product(range(2),repeat=p) if clock.primitive(k) and clock.decrypt(c,k,2)[1]==v]
     r=clock.solve_case({'ciphertext':list(c),'known':known,'periods':[p],'modulus':2})
     self.assertEqual(r['relations'][0]['primitive_seed_count'],len(truth));self.assertEqual(r['relations'][0]['plaintext_count'],len({tuple(pt) for k,pt in truth}))
 def test_archive_hashes_and_frozen_code(self):
  m=json.loads((D/'EVIDENCE-MANIFEST.json').read_text());archive=D/'candidate-first-064-evidence.zip'
  self.assertEqual(hashlib.sha256(archive.read_bytes()).hexdigest(),m['archive_sha256'])
  with zipfile.ZipFile(archive) as z:
   self.assertEqual(json.loads(z.read('MANIFEST.json')),m['files'])
   for name,h in m['files'].items():self.assertEqual(hashlib.sha256(z.read(name)).hexdigest(),h,name)
   self.assertEqual(z.read('production/clock.py'),(ROOT/'experiments/recurrence_clock.py').read_bytes())
   for name in m['third_party_source_files_omitted']:self.assertNotIn('prior/'+name,z.namelist())
 def test_retained_controls_and_target_scope(self):
  with zipfile.ZipFile(D/'candidate-first-064-evidence.zip') as z:
   control=json.loads(z.read('independent/AUDIT-RESULT.json'));self.assertEqual(control['status'],'PASS');self.assertEqual(control['cases'],309);self.assertEqual(control['period_relations'],2163);self.assertEqual(control['counts']['plants_retained'],224)
   self.assertEqual(control['counts']['plant_unique']+control['counts']['plant_ambiguous'],224)
   target=json.loads(z.read('production/target-receipt.json'));self.assertEqual(target['periods'],[5]);self.assertFalse(target['other_periods_rerun']);self.assertEqual(target['status'],'UNSAT_COMPLETE')
   result=json.loads(z.read('production/target-output.json'));self.assertEqual(result['union_status'],'empty');self.assertEqual(len(result['relations']),1);self.assertEqual(result['relations'][0]['primitive_seed_count'],0)
   inherited=json.loads(z.read('prior/local-negative-transfers.json'));self.assertEqual({x['recurrence_period'] for x in inherited['transfers']},{2,3,4,6,7,8});self.assertTrue(all(x['prior_outcome']['minimum_substitutions']>0 for x in inherited['transfers']))
   p5=json.loads(z.read('prior/p5-all-containing-domains.json'));self.assertEqual(p5['summary']['count'],604);self.assertEqual(p5['summary']['exact_crib_equal'],0);self.assertEqual(p5['summary']['exact_full_equal'],0)
 def test_preserved_snapshot_and_updated_inventory(self):
  old=json.loads((ROOT/'research/specifications/FRONTIER-CURRENT-20261031-063.json').read_text());new=json.loads((ROOT/'research/specifications/FRONTIER-CURRENT-20261031-064.json').read_text());self.assertEqual(old['expected_register_entries'],67);self.assertEqual(new['expected_register_entries'],68)
  self.assertTrue(any(g['id']=='F-RECURRENCE-064' for g in new['gates']))
if __name__=='__main__':unittest.main()
