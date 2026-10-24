import hashlib,json,itertools,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import strip_source_gates as s

class ConditionalStripTests(unittest.TestCase):
 def test_every_registration_and_infinite_width_local_witness(self):
  d=s.actual();self.assertEqual((d['raw_width_origin_descriptions'],d['rejected']),(465,464));self.assertEqual(len(d['necessary_only_unrejected']),1);self.assertEqual(d['necessary_only_unrejected'][0]['width'],1)
  self.assertEqual([r['position'] for r in d['all_width_at_least_two_witness']],[32,33,34]);self.assertFalse(d['non_plaintext_row']['necessary_condition_pass']);self.assertEqual(d['actual_key_enumerations'],0);self.assertFalse(d['berlin_evaluated'])
  obs=d['all_width_at_least_two_witness']
  for width in (2,3,25,30,31,97,1000):
   for phase in range(width):self.assertFalse(s.classify(obs,width,phase)['necessary_condition_pass'])
 def test_complete_binary_observation_patterns_match_interval_partition(self):
  # Exhaust every length-eight fixed/changed pattern independently of cipher strings.
  for bits in itertools.product((False,True),repeat=8):
   obs=[dict(position=i+1,fixed=b) for i,b in enumerate(bits)]
   for width in range(1,9):
    for origin in range(width):self.assertEqual(s.classify(obs,width,origin)['necessary_condition_pass'],s.reference_pass(obs,width,origin))
 def test_inverse_and_nonzero_shift_support_do_not_need_table_guess(self):
  strips=[s.AZ,s.AZ[::-1],s.AZ[7:]+s.AZ[:7]];rows={-1:0,0:4,1:0,2:13,3:1}
  for plain in ('','A','TESTMESSAGE'):
   cipher=s.crypt(plain,strips,2,rows);self.assertEqual(s.crypt(cipher,strips,2,rows,True),plain)
  for w in (s.AZ,s.AZ[::-1]):
   for d in range(26):
    got=''.join(w[(w.index(c)+d)%26] for c in s.AZ);self.assertEqual(sum(a==b for a,b in zip(s.AZ,got)),26 if d==0 else 0)
 def test_invalid_historical_transcription_is_rejected_not_repaired(self):
  for w in ('A'*26,s.AZ[:-1],s.AZ[:-1]+'A'):
   with self.assertRaises(ValueError):s.validate_strips([w])
 def test_original_conditional_receipts_and_pins(self):
  root=ROOT/'results/strip-source-gates-027';p=root/json.loads((root/'latest.json').read_text())['run_id'];m=json.loads((p/'manifest.json').read_text());self.assertEqual(m['status'],'completed')
  for name,r in m['artifacts'].items():self.assertEqual(hashlib.sha256((p/name).read_bytes()).hexdigest(),r['sha256'])
  for path,h in json.loads((p/'inputs.json').read_text()).items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),h)
  spec=m['specification'];raw=subprocess.check_output(['git','show',spec['commit']+':research/STRIP-SOURCE-GATES-027-SPEC.md'],cwd=ROOT);self.assertEqual(hashlib.sha256(raw).hexdigest(),spec['sha256'])
  d=json.loads((p/'controls.json').read_text());self.assertEqual(len(d['literal_plants']),24);self.assertTrue(all(r['full_roundtrip'] and r['necessary_condition_pass'] for r in d['literal_plants']))

 def test_untransmitted_row_choice_is_preserved_as_a_relation(self):
  from strip_row_candidates import candidates
  strips=[s.AZ,s.AZ[::-1],s.AZ[3:]+s.AZ[:3]]
  for plain in ('A','ABC'):
   for d in (1,13,25):
    cipher=s.crypt(plain,strips,0,{0:d});rows=candidates(cipher,strips)
    self.assertEqual(len(rows),25);self.assertEqual(len({r['plaintext'] for r in rows}),25)
    self.assertIn(dict(displacement=d,plaintext=plain),rows)
    self.assertFalse(any(any(p==c for p,c in zip(r['plaintext'],cipher)) for r in rows))
   self.assertEqual(len(candidates(plain,strips,True)),26)

 def test_transcription_gate_keeps_doubled_cycles_but_rejects_unknowns(self):
  from strip_inventory_admission import cycle_from_literal,inspect_inventory
  self.assertEqual(cycle_from_literal(s.AZ+' '+s.AZ),s.AZ)
  for raw in (s.AZ+'?',s.AZ+s.AZ[::-1],s.AZ[:-1]+'A',s.AZ.lower()):
   with self.assertRaises(ValueError):cycle_from_literal(raw)
  d=inspect_inventory([dict(id='test',literal=s.AZ*2)],'SYNTHETIC-CONTROL','synthetic-control')
  self.assertTrue(d['valid_permutations']);self.assertIn('Not established',d['source_authentication'])
  with self.assertRaises(ValueError):inspect_inventory([dict(id='a',literal=s.AZ),dict(id='a',literal=s.AZ)],'test','test')
