import hashlib
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class IndependentIPAIntegrationTests(unittest.TestCase):
    def test_original_member_hashes(self):
        for name in ('ipa-unanchored','pronunciation-codecs'):
            root=ROOT/'independent/2026-10-23'/name
            if (root/'SHA256SUMS').exists():
                entries={line.split('  ',1)[1]:line.split('  ',1)[0] for line in (root/'SHA256SUMS').read_text().splitlines()}
            else:entries=json.loads((root/'sha256.json').read_text())
            for path,sha in entries.items():self.assertEqual(hashlib.sha256((root/path).read_bytes()).hexdigest(),sha)

    def test_all_independent_counts_certificates_and_prediction_domains(self):
        local=json.loads((ROOT/'results/IPA-FREE-MAP-001.json').read_text())['rows']
        native=json.loads((ROOT/'independent/2026-10-23/ipa-unanchored/results.json').read_text())
        by={(r['alphabet'],r['period']):r for r in native['structures']}
        types=[]
        for r in local:
            n=by[r['alphabet'],r['period']]
            self.assertEqual(r['training_count']['gauge_fixed_count'],n['first_8_glyph_count']['gauge_orbits'])
            self.assertEqual(n['full_count']['gauge_orbits'],0)
            self.assertIsNotNone(n['primary_certificate']);types.append(n['primary_certificate']['type'])
            if r['second_block_evaluated']:
                domain={p['position']:p for p in n['Berlin_first_stage_status']}
                for p in r['first_stage_existing_glyph_predictions']:
                    self.assertEqual(p['possible_cipher_values'],domain[p['position']]['exact_allowed_c_values_before_any_Berlin_data'])
                    self.assertEqual(p['forced_under_all_training_injections'],domain[p['position']]['fully_forced_before_Berlin'])
        self.assertEqual(types.count('nonzero_cycle'),21)
        self.assertEqual(types.count('forced_glyph_collision'),3)
        self.assertEqual(native['validation']['tiny_rings']['count'],225)
        self.assertEqual(native['validation']['synthetic']['count'],24)

    def test_codec_lengths_and_border_boundary(self):
        d=json.loads((ROOT/'independent/2026-10-23/pronunciation-codecs/results.json').read_text())
        expected=[[(14,10),(12,9)],[(12,9),(10,9)],[(11,9),(9,8),(10,9)]]
        self.assertEqual(len(d['codecs']),3)
        for codec,e in zip(d['codecs'],expected):
            self.assertEqual([(s['normalized']['codepoints'],s['token_count']) for s in codec['streams']],e)
            self.assertTrue(all(s['source_EAST_token_prefix_suffix'] for s in codec['streams'] if s['block'][0]=='EAST'))
        c=d['border_certificate']['ciphertext']
        self.assertEqual([i for i in range(1,len(c)) if c[:i]==c[-i:]],[])
        self.assertEqual(d['border_certificate']['proper_border_lengths'],[])
