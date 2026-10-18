import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'experiments'))
from phonetic_cl import controls,mask_text,mask_known,known_original,crypt,inferred,primitive

class PhoneticCLTests(unittest.TestCase):
    def test_fixed_mask_context_and_loss(self):
        self.assertEqual(mask_text('CLOCK','CL'),'KLOCK');self.assertEqual(mask_text('CK','CL'),'CK');self.assertEqual(mask_text('CYCLE','CL'),'CYKLE')
        self.assertEqual(mask_text('CL','CL'),mask_text('KL','CL'))
        self.assertEqual([i+1 for i,c in known_original().items() if c!=mask_known(known_original(),97,'CL')[i]],[70])
        for s in ('cl','C L','C-L',''):
            with self.assertRaises(ValueError):mask_text(s,'CL')
    def test_unknown_context_not_guessed(self):
        with self.assertRaises(ValueError):mask_known({2:'C'},97,'CL')
    def test_unobserved_key_phases_are_not_filled(self):
        r=inferred('A'*97,{21:'A'},'identity',5)
        self.assertEqual(r['status'],'underdetermined');self.assertEqual(r['free_phases'],4);self.assertNotIn('transformed',r)
    def test_key_aliases_canonicalized_without_discarding_models(self):
        self.assertEqual(primitive([1,2,1,2]),(1,2));self.assertEqual(primitive([1,2,3]),(1,2,3))
    def test_seeded_recovery_and_exhaustive_small_oracle(self):
        r=controls();self.assertEqual(r['status'],'passed');self.assertEqual(len(r['primary_seeded_recovery_cases']),4);self.assertEqual(r['supplementary_count'],288);self.assertEqual(r['small_alphabet_oracle_cases'],24)
