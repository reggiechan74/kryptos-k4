"""Toy-only protocol controls; these maps are not historical hypotheses."""
from pathlib import Path
import random,sys,unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
from language_interfaces import *

class LanguageInterfaceTests(unittest.TestCase):
    def test_exact_symbol_and_sequence_roundtrip(self):
        mapping={'toy_1':'A','toy_2':'BC','toy_3':'BD'}
        rng=random.Random(20261018)
        for count in [0,1,2,27,97]:
            symbols=[rng.choice(list(mapping)) for _ in range(count)]
            self.assertEqual(inverse_symbols(forward_symbols(symbols,mapping),mapping),symbols)

    def test_symbol_and_sequence_ambiguity_are_distinct(self):
        collision={'toy_1':'A','toy_2':'A'}
        sequence_collision={'toy_1':'A','toy_2':'B','toy_3':'AB'}
        self.assertTrue(mapping_audit(collision)['symbol_collisions'])
        self.assertFalse(mapping_audit(sequence_collision)['symbol_collisions'])
        self.assertFalse(mapping_audit(sequence_collision)['uniquely_decodable_symbol_sequences'])
        with self.assertRaises(ValueError):inverse_symbols('AB',sequence_collision)

    def test_nonprefix_code_can_be_uniquely_decodable(self):
        self.assertTrue(unique_decodability(['A','AB']))
        self.assertEqual(inverse_symbols('AAB',{'toy_1':'A','toy_2':'AB'}),['toy_1','toy_2'])

    def test_deletion_and_unknowns_are_not_silently_repaired(self):
        self.assertEqual(mapping_audit({'toy_1':'A','toy_mark':''})['empty_output_symbols'],['toy_mark'])
        with self.assertRaises(ValueError):inverse_symbols('A',{'toy_1':'A','toy_mark':''})
        with self.assertRaises(ValueError):forward_symbols(['unknown'],{'toy_1':'A'})
        with self.assertRaises(ValueError):inverse_symbols('Z',{'toy_1':'A'})

    def test_lengths_and_framing_are_explicit(self):
        self.assertFalse(length_feasibility(97,[2]))
        self.assertTrue(length_feasibility(97,[2],1))
        self.assertTrue(length_feasibility(97,[1,2]))
        with self.assertRaises(ValueError):length_feasibility(97,[0,2])

    def test_only_final_english_positions_receive_cribs(self):
        text='A'*21+'EASTNORTHEAST'+'A'*29+'BERLINCLOCK'+'A'*23
        cribs=[{'start':22,'end':34,'text':'EASTNORTHEAST'},{'start':64,'end':74,'text':'BERLINCLOCK'}]
        self.assertEqual(len(text),97)
        self.assertTrue(final_crib_check(text,cribs)['passes'])
        self.assertFalse(final_crib_check(text+'A',cribs)['passes'])
        self.assertFalse(final_crib_check(text.lower(),cribs)['passes'])

    def test_inverse_budget_and_deadline_fail_explicitly(self):
        with self.assertRaises(TimeoutError):inverse_symbols('A',{'toy_1':'A'},limit=0)
        with self.assertRaises(ValueError):inverse_symbols('A',{'toy_1':'A'},max_decodes=0)
        with self.assertRaises(TimeoutError):unique_decodability(['A','AB'],limit=0)
        with self.assertRaises(ValueError):unique_decodability(['A','AB'],state_budget=0)

if __name__=='__main__':unittest.main()
