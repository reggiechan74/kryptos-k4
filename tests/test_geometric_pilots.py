import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments'))
from geometric_pilots import (frozen_codes, rotl35, bitlist_rotation, WIDTH, MASK,
    model_domain, feedback_encrypt, feedback_decrypt, literal_plaintext,
    periodic_select, periodic_transform, primitive_period, AZ, TRAIN, BERLIN)

class GeometricPilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.codes=frozen_codes()

    def test_rotation_boundaries_and_high_bits(self):
        for value in [0,MASK,1,1<<34]+[1<<i for i in range(35)]:
            for r in range(35):
                self.assertEqual(rotl35(value,r),bitlist_rotation(value,r))
                self.assertEqual(rotl35(rotl35(value,r),(35-r)%35),value)
        self.assertEqual(rotl35(1<<34,1),1)
        for args in [(-1,0),(1<<35,0),(1,35),(True,0),(1,False)]:
            with self.assertRaises(ValueError):rotl35(*args)

    def test_full_frozen_parameter_domain(self):
        d=model_domain()
        self.assertEqual(len(d),3640);self.assertEqual(len(set(d)),3640)
        self.assertEqual({m[2] for m in d},set(range(35)))
        self.assertEqual({m[3] for m in d},set(AZ))

    def test_independent_encoder_and_decoder_selected_boundaries(self):
        p=literal_plaintext()
        for name in ('AZ','KRYPTOS'):
            for source in ('P','C'):
                for r in (0,1,17,34):
                    for seed in ('A','M','Z'):
                        model=(name,source,r,seed)
                        self.assertEqual(feedback_decrypt(feedback_encrypt(p,model,self.codes),model,self.codes),p)
        self.assertTrue(all(p[i]==v for i,v in {**TRAIN,**BERLIN}.items()))

    def test_unrestricted_periodic_fit_and_equivalence(self):
        p=literal_plaintext();a=''.join(sorted(AZ,key=self.codes.get))
        for m in range(1,13):
            for equation in ('plus','beaufort'):
                key=[(i*5+3)%26 for i in range(m)]
                cipher=periodic_transform(p,a,key,equation)
                selected=periodic_select(cipher,self.codes)
                true=[r for r in selected['all24_survivors'] if r['period']==m and r['equation']==equation]
                self.assertEqual(len(true),1);self.assertEqual(true[0]['key'],key)
                self.assertEqual(true[0]['free_key_slots'],[])
        self.assertEqual(primitive_period([7]*12),1)
        self.assertEqual(periodic_transform(p,a,[7]*12,'plus'),periodic_transform(p,a,[7],'plus'))

    def test_complete_selector_control_receipt(self):
        receipt=json.loads((ROOT/'results/GEOMETRIC-PILOT-001-controls.json').read_text())
        self.assertEqual(len(receipt['feedback_plants']),48)
        self.assertEqual(len(receipt['periodic_plants']),24)
        self.assertTrue(all(r['truth_included'] and r['roundtrip'] and r['mutation_target_rejected'] for r in receipt['feedback_plants']+receipt['periodic_plants']))
        self.assertTrue(any(r['distinct_compatible_plaintexts']>1 for r in receipt['feedback_plants']))

if __name__=='__main__':unittest.main()
