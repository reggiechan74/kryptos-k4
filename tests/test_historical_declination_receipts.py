from pathlib import Path
import hashlib,json,unittest
ROOT=Path(__file__).resolve().parents[1]
class HistoricalDeclinationReceiptTests(unittest.TestCase):
    def test_official_receipts_dates_units_coordinates_and_hashes(self):
        m=json.loads((ROOT/'sources/igrf14-langley-20261023/manifest.json').read_text())
        self.assertEqual(len(m['receipts']),3)
        for row in m['receipts']:
            p=ROOT/row['path'];self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),row['sha256'])
            r=json.loads(p.read_text())['geomagnetic-field-model-result']
            self.assertEqual(r['model_revision'],'14');self.assertEqual(r['date']['value'],row['date'])
            self.assertEqual(r['field-value']['declination']['units'],'deg (east)')
            self.assertEqual(r['field-value']['declination']['value'],row['declination_degrees_east'])
            self.assertEqual(r['coordinates']['latitude']['value'],38.951)
            self.assertEqual(r['coordinates']['longitude']['value'],-77.146)
            self.assertEqual(r['coordinates']['altitude']['value'],0)
            self.assertTrue(row['url'].startswith('https://geomag.bgs.ac.uk/'))
    def test_conditional_conversion_sign_and_original_bundle_separation(self):
        m=json.loads((ROOT/'sources/igrf14-langley-20261023/manifest.json').read_text())
        self.assertEqual([r['declination_degrees_east'] for r in m['receipts']],[-9.540,-9.628,-9.716])
        self.assertAlmostEqual(m['conditional_conversion']['true_bearing_degrees'],237.872)
        self.assertFalse(m['conditional_conversion']['monument_bearing_measured'])
        self.assertFalse(m['original_research_bundle_modified'])
        original=json.loads((ROOT/'results/LODESTONE-COMPASS-EVIDENCE-INTEGRATION-001.json').read_text())
        self.assertEqual(len(original['member_sha256']),4)
        for path,sha in original['member_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),sha)
