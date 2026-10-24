import hashlib,itertools,json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import lamp_greek as g
import audit_lamp_greek as oracle

class LampGreekTests(unittest.TestCase):
 def test_display_weights_and_inverse_exhaustive(self):
  self.assertEqual(oracle.reference_values(),[[list(v) for v in r] for r in g.VALUES])
  for t,p in itertools.product(range(1440),(0,1)):
   bits=g.lamp_bits(t,p);self.assertEqual(g.lamp_inverse(bits),(t,p))
   self.assertEqual(g.ordinal(t,p)+g.ordinal(t,p,True),25*sum(bits))
  for bits in ((0,)*23,(2,)+(0,)*23,(0,0,1)+(0,)*21,(0,)+(1,)*8+(0,)*15):
   with self.assertRaises(ValueError):g.lamp_inverse(bits)
 def test_complete_prefix_framing_and_rank_bridge(self):
  for c in g.LATIN:self.assertEqual(g.unframe(g.frame(c)),c)
  self.assertEqual(g.frame('XYZ'),'ΩΑΩΒΩΓ')
  for rank in range(676):self.assertEqual(g.undigits(g.digits(rank,3),676),rank)
  for s in ('Ω','ΩΔ','ΩΩ'):
   with self.assertRaises(ValueError):g.unframe(s)
  with self.assertRaises(ValueError):g.undigits(g.digits(676,3),676)
 def test_all_role_equation_alphabet_roundtrips_with_expanded_prefix(self):
  plain=g.plant()
  for role,rev,name,eq in itertools.product(g.ROLES,(False,True),g.ALPHABETS,('plus','beaufort')):
   m=g.model(role,rev,1438,1,name,eq);c=g.crypt(plain,m)
   self.assertEqual(g.crypt(c,m,True),plain);self.assertEqual(c,g.crypt(plain,m,oracle=True))
   self.assertEqual(len(c),104 if role=='G' else 97)
  self.assertEqual(len(g.frame(plain[:21])),25)
 def test_constraint_compiler_equals_direct_plaintext_for_every_local_key(self):
  plain=g.plant()
  for role,name,eq in itertools.product(('L','B'),g.ALPHABETS,('plus','beaufort')):
   m=g.model(role,False,58,1,name,eq);cipher=g.crypt(plain,m);a=g.ALPHABETS[name]
   for i,allowed,n in g.first_constraints(cipher,role,a,eq):
    # Independent exhaustive decrypted local block for every possible key.
    for key in range(n):
     if role=='L':
      v=a.index(cipher[i]);p=(v-key if eq=='plus' else key-v)%26
      good=a[p]==plain[i]
     else:
      pos=i*2;cv=a.index(cipher[pos])*26+a.index(cipher[pos+1]);v=(cv-key if eq=='plus' else key-cv)%676
      out=a[v//26]+a[v%26]
      good=all(out[j]==plain[pos+j] for j in range(2) if 21<=pos+j<34)
     self.assertEqual(key in allowed,good)
 def test_original_receipts_controls_and_exact_counts(self):
  root=ROOT/'results/lamp-greek-025';p=root/json.loads((root/'latest.json').read_text())['run_id'];manifest=json.loads((p/'manifest.json').read_text())
  self.assertEqual(manifest['status'],'completed')
  for name,row in manifest['artifacts'].items():self.assertEqual(hashlib.sha256((p/name).read_bytes()).hexdigest(),row['sha256'])
  controls=json.loads((p/'controls.json').read_text());self.assertEqual(controls['raw_roundtrips'],69120);self.assertEqual(len(controls['literal_plants']),24)
  self.assertTrue(all(x['truth_retained'] for x in controls['literal_plants']));self.assertTrue(any(x['distinct_plaintexts']==2 for x in controls['literal_plants']))
  actual=json.loads((p/'actual.json').read_text());self.assertEqual(actual['first_survivors'],0)
  self.assertEqual(sum(x['raw_descriptions'] for x in actual['accounting'].values()),69120)
  self.assertEqual(actual['accounting']['G']['support_or_length_pruned'],23040)
  self.assertEqual(actual['accounting']['G']['first_constraints_tested'],0)
  nulls=json.loads((p/'nulls.json').read_text());self.assertEqual(len(nulls['rows']),199);self.assertEqual(nulls['all_events'],0)
 def test_actual_support_contradiction_independent_of_english_alignment(self):
  cipher=json.loads((ROOT/'data/k4.json').read_text())['ciphertext'];self.assertEqual(set(cipher),set(g.LATIN))
  for a in g.ALPHABETS.values():self.assertEqual(len(set(cipher)-set(a[:24])),2)
 def test_original_source_hashes_and_spec_chronology(self):
  root=ROOT/'results/lamp-greek-025';p=root/json.loads((root/'latest.json').read_text())['run_id'];sources=json.loads((p/'inputs.json').read_text())
  for path,h in sources.items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),h)
  spec=json.loads((p/'manifest.json').read_text())['specification'];raw=subprocess.check_output(['git','show',spec['commit']+':research/LAMP-GREEK-025-SPEC.md'],cwd=ROOT)
  self.assertEqual(hashlib.sha256(raw).hexdigest(),spec['sha256'])
 def test_independent_complete_selector_receipt(self):
  d=json.loads((ROOT/'results/LAMP-GREEK-025-INDEPENDENT-VALIDATION.json').read_text());self.assertEqual(d['complete_raw_selectors_compared'],25);self.assertEqual(d['actual_survivors'],0)
  self.assertTrue(all(r['complete_set_equal'] for r in d['plant_comparisons']))

 def test_finite_certificates_replay_without_zero_solution_predictions(self):
  from lamp_greek_certificates import certificates
  saved=json.loads((ROOT/'results/LAMP-GREEK-025-CERTIFICATES.json').read_text());saved.pop('created_at_utc')
  self.assertEqual(certificates(),saved)
  self.assertTrue(all(r['final_remaining']==0 for r in saved['first_stage_eliminations']))
