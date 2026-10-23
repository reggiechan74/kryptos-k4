import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments'))
from ipa_source_review import compare,xsampa_subset,inverse_subset

class IPASourceReviewTests(unittest.TestCase):
    def test_all_source_and_certificate_checks_match_receipt(self):
        r=json.loads((ROOT/'results/IPA-SOURCE-COMPARISON.json').read_text())
        self.assertEqual(compare(),r['checks'])
        self.assertEqual(r['checks']['verified_original_members'],7)
        self.assertEqual(r['checks']['native_full_window_anchor_certificates_verified'],48)
        self.assertEqual(r['checks']['local_first_window_ordinary_anchor_rejections'],47)

    def test_cross_window_and_marker_stages_are_distinct(self):
        r=compare()
        self.assertEqual(r['native_cross_window_certificate'],[{'alphabet':'AZ','equation':'add','period':10,'positions':[24,64],'key_values':[25,12]}])
        self.assertEqual(r['supplementary_first_window_marker_indices'],[13,11])
        self.assertEqual(r['local_first_window_relaxed_rejections'],48)

    def test_xsampa_subset_is_case_sensitive_and_not_AZ_transport(self):
        a,b=xsampa_subset('iːstnɔːrθiːst'),xsampa_subset('bɝːlɪnklɑːk')
        self.assertEqual((len(a),len(b)),(13,12))
        self.assertEqual(inverse_subset(a),'iːstnɔːrθiːst')
        self.assertEqual(inverse_subset(b),'bɝːlɪnklɑːk')
        self.assertEqual(xsampa_subset('i').upper(),xsampa_subset('ɪ').upper())
        self.assertEqual(xsampa_subset('t').upper(),xsampa_subset('θ').upper())
        self.assertIn(':',a);self.assertIn('`',b)
        with self.assertRaises(ValueError):xsampa_subset('ə')
        with self.assertRaises(ValueError):inverse_subset('?')

    def test_replayed_native_control_scopes_preserved(self):
        r=json.loads((ROOT/'results/IPA-SOURCE-COMPARISON.json').read_text())['native_replays']
        self.assertEqual(r['main_replay']['synthetic_cipher_roundtrips'],48)
        self.assertEqual(r['main_replay']['mutation_negative_controls'],4)
        self.assertEqual(r['main_replay']['ascii_storage_roundtrips'],2)
        self.assertEqual(r['main_replay']['xsampa_subset_roundtrips'],2)
        self.assertTrue(r['supplement_replay']['supplementary_post_audit_check'])

if __name__=='__main__':unittest.main()
