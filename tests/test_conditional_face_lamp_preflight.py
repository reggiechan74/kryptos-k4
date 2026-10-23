import hashlib,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments'))
from face_row_coverage import catalogue,occupied_cells,inverse_permutation

class ConditionalPreflightTests(unittest.TestCase):
    def test_evidence_is_preserved_byte_exact_without_source_images(self):
        r=json.loads((ROOT/'results/LODESTONE-COMPASS-EVIDENCE-INTEGRATION-001.json').read_text())
        self.assertEqual(r['archive_bytes'],50458)
        self.assertEqual(len(r['member_sha256']),4)
        for path,sha in r['member_sha256'].items():
            p=ROOT/path;self.assertEqual(p.suffix,'.md');self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),sha)
        self.assertFalse(r['original_sources_refetched_here'])
        reg=json.loads((ROOT/'results/HYPOTHESIS-REGISTER-002.json').read_text())
        for path,sha in reg['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),sha)

    def test_complete_coordinate_inverse_and_exact_model_coverage(self):
        cells=occupied_cells();labels=dict(zip(cells,range(97)))
        for row in catalogue():
            mapped={(3-r if row['vertical'] else r,30-c if row['horizontal'] else c):i for (r,c),i in labels.items()}
            direct=[mapped[cell] for cell in sorted(mapped)]
            if row['inverse']:
                reverse=[None]*97
                for j,i in enumerate(direct):reverse[i]=j
                direct=reverse
            self.assertEqual(row['permutation'],direct)
            inv=inverse_permutation(direct)
            self.assertEqual([direct[inv[i]] for i in range(97)],list(range(97)))
        d=json.loads((ROOT/'results/FACE-ROW-001-COVERAGE.json').read_text())
        self.assertEqual([d[k] for k in ('raw_descriptions','distinct_routes','canonical_models','covered_models','new_models')],[768,5,372,280,92])
        self.assertEqual(sum(len(r['aliases']) for r in d['records']),768)
        self.assertEqual(hashlib.sha256((ROOT/'results/ROUTE-001.json.gz').read_bytes()).hexdigest(),d['prior_result_sha256'])
        self.assertEqual(hashlib.sha256((ROOT/'experiments/face_row_coverage.py').read_bytes()).hexdigest(),d['source_sha256'])
        for r in d['records']:
            if r['prior_coverage']:continue
            self.assertTrue(all(a['horizontal'] and not a['vertical'] for a in r['aliases']))
            inv=inverse_permutation(r['permutation'])
            phases={(i if r['order']=='sub_then_route' else inv[i])%r['period'] for i in range(21,34)}
            self.assertEqual(phases,set(range(r['period'])))
