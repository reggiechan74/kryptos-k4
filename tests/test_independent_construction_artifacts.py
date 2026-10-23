from pathlib import Path
import hashlib
import json
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'independent/2026-10-22'
# Admit the seven original standard-library-only offline unit controls to the
# core suite. No source retrieval or cache access occurs in those tests.
sys.path.insert(0,str(BASE/'construction'))
from test_audit_construction import ConventionTests


class IndependentConstructionArtifacts(unittest.TestCase):
    def test_transfer_and_received_manifest(self):
        r=json.loads((BASE/'CONSTRUCTION-TRANSFER-RECEIPT.json').read_text())
        self.assertEqual(len(r['received_files']),9)
        for name,row in r['received_files'].items():
            b=(BASE/name).read_bytes()
            self.assertEqual(len(b),row['bytes'])
            self.assertEqual(hashlib.sha256(b).hexdigest(),row['sha256'])
        manifest=json.loads((BASE/'construction/MANIFEST.json').read_text())
        for row in manifest['files']:
            self.assertEqual(hashlib.sha256((BASE/'construction'/row['path']).read_bytes()).hexdigest(),row['sha256'])
        self.assertFalse(any(p.name=='.audit_cache' for p in BASE.rglob('*')))

    def test_replay_checks_source_coordinates_and_existing_local_pair(self):
        r=ROOT/'results/independent-followup-review'
        fresh=json.loads((r/'CONSTRUCTION-FRESH-REPLAY-001.json').read_text())
        offline=json.loads((r/'CONSTRUCTION-OFFLINE-REPLAY-001.json').read_text())
        original=json.loads((BASE/'construction/construction_audit_results.json').read_text())
        self.assertEqual(fresh['checks'],offline['checks'])
        self.assertEqual(fresh['checks'],original['checks'])
        self.assertEqual(fresh['source_receipts'],original['source_receipts'])
        c=fresh['checks']['cyrillic_projector']
        old_dir=ROOT/'results/cp-convention-runs'
        latest=json.loads((old_dir/'latest.json').read_text())
        old=json.loads((old_dir/latest['run_id']/'CP-CONVENTION-REPLAY-001.json').read_text())
        self.assertEqual(c['cipher_sha256_utf8'],old['ciphertext_sha256'])
        self.assertEqual(c['published_plain_sha256_utf8'],old['plaintext_sha256'])
        self.assertEqual(c['semantic_boundary_coordinates']['778'],{'row_1_based':22,'column_1_based_including_MEDUSA':33})
        self.assertNotEqual(c['panel_boundary_after_symbol'],777)
        self.assertEqual(fresh['checks']['kryptos_k1_k2']['unique_deleted_intended_cipher_position_1_based'],362)

    def test_canonical_and_proposed_scope_not_expanded(self):
        r=ROOT/'results/independent-followup-review'
        d=json.loads((r/'CONSTRUCTION-FRESH-REPLAY-001.json').read_text())
        c=d['checks']['k4_reference_only']
        baseline=json.loads((ROOT/'data/k4.json').read_text())
        self.assertEqual(c['sha256_utf8'],hashlib.sha256(baseline['ciphertext'].encode()).hexdigest())
        self.assertEqual(c['mutations_applied'],0)
        self.assertEqual(c['candidate_plaintexts_generated'],0)
        local=json.loads((r/'CONSTRUCTION-LOCAL-REPLAY-001.json').read_text())
        self.assertEqual(local['sensitivity_variants_executed'],0)
        self.assertEqual(len(local['corrupted_inputs_rejected']),2)


if __name__=='__main__':unittest.main()
