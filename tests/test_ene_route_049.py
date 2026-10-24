import gzip,hashlib,json,random,sys,unittest,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import ene_route_049 as e
import finite_hand_operators as f
class ENERoute049Tests(unittest.TestCase):
 def test_complete_catalogue_aliases_and_bijections(self):
  raw=gzip.decompress((ROOT/'results/ENE-ROUTE-049-CATALOGUE.json.gz').read_bytes());r=json.loads((ROOT/'results/ENE-ROUTE-049-ORIGINAL.json').read_text());self.assertEqual(hashlib.sha256(raw).hexdigest(),r['catalogue_uncompressed_sha256']);catalog=json.loads(raw);self.assertEqual(len(catalog),34569);aliases=[]
  for row in catalog:self.assertEqual(sorted(row['permutation']),list(range(97)));aliases.extend(map(tuple,row['aliases']))
  self.assertEqual(len(aliases),56454);self.assertEqual(len(set(aliases)),56454);self.assertEqual({a[1] for a in aliases},set(range(1,98)));self.assertEqual({a[2] for a in aliases},set(range(97)))
 def test_pathological_width_reference_and_inverse_no_dropped_cells(self):
  for w in (1,2,3,31,48,49,96,97):
   for start in (0,48,96):
    for kind in e.KINDS:
     p=e.route(w,start,kind);self.assertEqual(p,e.reference(w,start,kind));self.assertEqual(f.invperm(f.invperm(p)),p)
 def test_packed_whole_family_matching_is_exact(self):
  rng=random.Random(49099)
  for n in range(25):
   for _ in range(40):
    x=bytes(rng.randrange(26) for _ in range(n));y=bytes(rng.randrange(26) for _ in range(n));self.assertEqual(f.packed_matches(int.from_bytes(x,'big'),int.from_bytes(y,'big'),n),sum(a==b for a,b in zip(x,y)))
  p=bytes(range(97));sigs=[''.join(e.decode(chr(65+x)*97,p,v) for x in range(26)) for v in e.variants()];self.assertEqual(len(set(sigs)),19)
 def test_controls_limits_and_full_replay(self):
  r=json.loads((ROOT/'results/ENE-ROUTE-049-CONTROLLED.json').read_text());v=json.loads((ROOT/'results/ENE-ROUTE-049-CONTROLLED-REPLAY.json').read_text())
  for row in (r,v):row.pop('started_at_utc');row.pop('finished_at_utc')
  self.assertEqual(r,v);self.assertEqual(r['actual']['operator_evaluations'],656811);self.assertEqual(r['actual']['exact_model_hits'],0);self.assertEqual(r['controls']['complete_independent_coordinate_route_checks'],28227);self.assertEqual(r['controls']['all_width_inverse_arithmetic_plants'],11058);self.assertTrue(all(p['planted_full_plaintext_present'] for p in r['full_selector_plants']));self.assertEqual(len(r['nulls']),31)
  for name,h in r['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),h)

 def test_true_plant_is_in_actual_returned_selector_hits_and_old_history_retained(self):
  r=json.loads((ROOT/'results/ENE-ROUTE-049-CONTROLLED.json').read_text());old=json.loads((ROOT/'results/ENE-ROUTE-049-ORIGINAL.json').read_text());self.assertEqual(r['actual'],old['actual']);self.assertEqual(r['nulls'],old['nulls']);self.assertEqual(r['catalogue_uncompressed_sha256'],old['catalogue_uncompressed_sha256'])
  for plant in r['full_selector_plants']:
   self.assertTrue(plant['actual_returned_hit_verified']);hit=plant['recovered_hit'];self.assertEqual(hit['route_sha256'],plant['planted_route_sha256']);self.assertEqual(hit['variant'],plant['planted_variant']);self.assertEqual(len(hit['plaintext']),97)
  for name,h in old['source_sha256'].items():self.assertEqual(hashlib.sha256(subprocess.check_output(['git','show','1cef25a:'+name],cwd=ROOT)).hexdigest(),h)
