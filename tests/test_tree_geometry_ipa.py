import hashlib,json,itertools,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import tree_geometry_ipa as x
import tree_geometry_ipa_reference as ref

class ItemSixTests(unittest.TestCase):
 def test_complete_finite_domain_and_utf8_source_fixed(self):
  self.assertEqual(len(x.MODELS),448);self.assertEqual(len({json.dumps(m,sort_keys=True) for m in x.MODELS}),448)
  self.assertEqual(x.IPA,{'east-northeast':'iːstnɔːrθiːst','berlin-clock':'bɝːlɪnklɑːk'})
  for key,value in x.IPA.items():self.assertEqual(ref.utf8(value),list(x.KEYS[key]))
 def test_tree_topology_and_parent_invariants_against_nested_oracle(self):
  tree=x.Splay(x.AZ)
  def build(lo,hi):
   if lo>=hi:return None
   mid=(lo+hi)//2;return (mid,build(lo,mid),build(mid+1,hi))
  other=build(0,26);initial=tree.signature()
  for c in x.AZ+'QWERTYUIOPLKJHGFDSAZXCVBNM':
   node=tree.lookup[c];tree.access(node);other=ref.splay(other,node);self.assertEqual(tree.preorder(),ref.preorder(other));self.assertEqual(tree.root,node)
   for i in range(26):
    for child in (tree.left[i],tree.right[i]):
     if child!=-1:self.assertEqual(tree.parent[child],i)
  self.assertNotEqual(tree.signature(),initial)
 def test_arx_boundary_and_nonreducible_key_state_witness(self):
  for state,letter in itertools.product((0,1,26,x.MASK,x.MASK-1),x.AZ):self.assertEqual(ref.step(state,x.CODES[letter]),(x.rotl35(state,1)+(state^x.CODES[letter]))&x.MASK)
  self.assertEqual([ref.step(s,x.CODES['C'])%26 for s in (0,26)],[8,18])
 def test_continuous_roundtrip_reference_and_reject_bad_framing(self):
  for role in ('T','G','I'):
   models=[m for m in x.MODELS if m['role']==role]
   for m in (models[0],models[-1]):
    plain=x.literal_plant();cipher=x.crypt(plain,m);self.assertEqual(x.crypt(cipher,m,True),plain);self.assertEqual(ref.crypt(plain,m),cipher)
    with self.assertRaises(ValueError):x.crypt('HELLO WORLD',m)
 def test_original_immutable_receipts_all_plants_and_bounded_counts(self):
  root=ROOT/'results/tree-geometry-ipa-026';p=root/json.loads((root/'latest.json').read_text())['run_id'];manifest=json.loads((p/'manifest.json').read_text());self.assertEqual(manifest['status'],'completed')
  for name,row in manifest['artifacts'].items():self.assertEqual(hashlib.sha256((p/name).read_bytes()).hexdigest(),row['sha256'])
  d=json.loads((p/'controls.json').read_text());self.assertEqual(d['fixed_model_reference_roundtrips'],1792);self.assertEqual(len(d['plants']),24);self.assertTrue(all(r['truth_retained'] and r['independent_complete_set_equal'] for r in d['plants']))
  actual=json.loads((p/'actual.json').read_text());self.assertEqual(actual['role_counts'],{'T':104,'G':208,'I':136});self.assertEqual(len(actual['records']),448);self.assertEqual(actual['distinct_full_outputs'],448);self.assertEqual(actual['first_survivors'],[])
  nulls=json.loads((p/'nulls.json').read_text());self.assertEqual(len(nulls['draws']),199);self.assertEqual((nulls['first_events'],nulls['all_events']),(0,0))
 def test_failed_reference_control_is_not_a_cipher_negative(self):
  p=ROOT/'results/tree-geometry-ipa-026/20261024T020432Z-cc0db30d728d46d781efc6aacc03ae11/manifest.json';d=json.loads(p.read_text());self.assertEqual(d['status'],'incomplete');self.assertEqual(d['error_type'],'AssertionError');self.assertEqual(d['artifacts'],{})
 def test_pinned_original_sources_and_before_scoring_spec(self):
  root=ROOT/'results/tree-geometry-ipa-026';p=root/json.loads((root/'latest.json').read_text())['run_id'];d=json.loads((p/'inputs.json').read_text())
  for path,h in d.items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),h)
  spec=json.loads((p/'manifest.json').read_text())['specification'];raw=subprocess.check_output(['git','show',spec['commit']+':research/TREE-GEOMETRY-IPA-026-SPEC.md'],cwd=ROOT);self.assertEqual(hashlib.sha256(raw).hexdigest(),spec['sha256'])
 def test_independent_actual_and_period_overlap_receipt(self):
  d=json.loads((ROOT/'results/TREE-GEOMETRY-IPA-026-INDEPENDENT-VALIDATION.json').read_text());self.assertTrue(d['actual_complete_record_set_equal']);self.assertEqual(d['geometry_bit_carry_boundary_checks'],1040);self.assertEqual([r['primitive_period'] for r in d['ipa_periods']],[18,16])
