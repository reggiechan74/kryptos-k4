from pathlib import Path
import sys,unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
from masking_pilots import *

class MaskingPilotTests(unittest.TestCase):
    def test_hand_vectors_and_all12_planted_scanner_cases(self):
        c=autokey_controls();self.assertEqual(c['actual_scanner_planted_recoveries'],12);self.assertEqual(c['altered_crib_rejections'],12)
    def test_ACA_example_full_morse_controls_and_two_plants(self):
        c=morse_controls();self.assertTrue(c['ACA_example_pass']);self.assertEqual(c['actual_scanner_planted_recoveries'],2)
    def test_plain_and_cipher_feedback_differ_past_primer(self):
        self.assertEqual(autokey('ATTACKATDAWN','ABCDEFGHIJKLMNOPQRSTUVWXYZ','KEY','plaintext'),'KXRAVDAVNAPQ')
        self.assertEqual(autokey('ATTACKATDAWN','ABCDEFGHIJKLMNOPQRSTUVWXYZ','KEY','ciphertext'),'KXRKZBKSEKOR')
    def test_all26_Morse_patterns_and_independent_short_vectors(self):
        expected=['.-','-...','-.-.','-..','.','..-.','--.','....','..','.---','-.-','.-..','--','-.','---','.--.','--.-','.-.','...','-','..-','...-','.--','-..-','-.--','--..']
        self.assertEqual(list(read_spec(FM_SPEC)['Morse'].values()),expected)
        for plain,cipher in [('A','F'),('E','I'),('T','R'),('I','C')]:self.assertEqual(morse_encode(plain,'ABCDEFGHIJKLMNOPQRSTUVWXYZ')['ciphertext'],cipher)
    def test_no_silent_repairs(self):
        for message in ['e','E  E',' E','E ','E.','']:
            with self.assertRaises(ValueError):morse_encode(message,'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        for stream in ['x..','...xxx...','......','.xxxxx','..']:
            with self.assertRaises(MorseParseError):parse_morse_stream(stream)
    def test_final_positions_are_letters_not_ternary_or_spaced_indices(self):
        message=fm_planted_message();plain=message.replace(' ','');self.assertEqual(plain[21:34],'EASTNORTHEAST');self.assertNotEqual(message[21:34],'EASTNORTHEAST')
        for alphabet in read_spec(FM_SPEC)['alphabets']:
            cipher=morse_encode(message,alphabet)['ciphertext'];self.assertEqual(len(cipher),97)
            result=fractionated_morse_scan(synthetic_data(cipher,plain));self.assertTrue(next(r for r in result['records'] if r['alphabet']==alphabet)['accepted'])
    def test_no_unknown_autokey_symbols_or_feedback(self):
        for text,primer,feedback in [('abc','KEY','plaintext'),('ABC','','plaintext'),('ABC','KEY','unknown')]:
            with self.assertRaises(ValueError):autokey(text,'ABCDEFGHIJKLMNOPQRSTUVWXYZ',primer,feedback)
    def test_initial_deadlines(self):
        data={'ciphertext':'A'*97,'cribs':[]}
        with self.assertRaises(TimeoutError):autokey_scan(data,-1)
        with self.assertRaises(TimeoutError):fractionated_morse_scan(data,-1)

if __name__=='__main__':unittest.main()
