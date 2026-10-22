from pathlib import Path
import hashlib
import json
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments'))
from strategy_followup import configurations, crib_map, rank_oracle


class StrategyFollowupArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base=ROOT/'results/strategy-followup-runs'
        pointer=json.loads((base/'latest.json').read_text())
        cls.run_dir=base/pointer['run_id']
        cls.manifest=json.loads((cls.run_dir/'manifest.json').read_text())
        cls.result=json.loads((cls.run_dir/'STRATEGY-FOLLOWUP-001.json').read_text())

    def test_complete_receipt_and_committed_input_hashes(self):
        m,d=self.manifest,self.result
        self.assertEqual(m['status'],'completed')
        self.assertTrue(all(j['status']=='completed' for j in m['jobs']))
        b=(self.run_dir/'STRATEGY-FOLLOWUP-001.json').read_bytes()
        self.assertEqual(m['artifacts']['STRATEGY-FOLLOWUP-001.json']['sha256'],hashlib.sha256(b).hexdigest())
        self.assertEqual(m['artifacts']['STRATEGY-FOLLOWUP-001.json']['bytes'],len(b))
        subprocess.run(['git','merge-base','--is-ancestor',d['spec_commit'],d['code_commit']],cwd=ROOT,check=True)
        for name,expected in d['file_sha256'].items():
            committed=subprocess.check_output(['git','show',d['code_commit']+':'+name],cwd=ROOT)
            self.assertEqual(hashlib.sha256(committed).hexdigest(),expected)

    def test_fixed_outputs_independent_decoder_and_boundaries(self):
        data=json.loads((ROOT/'data/k4.json').read_text())
        known=crib_map(data)
        d=self.result
        for cfg,record in zip(configurations(),d['actual_K4']):
            plain=rank_oracle(data['ciphertext'],cfg,True)
            self.assertEqual(plain,record['plaintext'])
            self.assertEqual(record['matches'],sum(plain[i]==p for i,p in known.items()))
            self.assertEqual(record['matches'],0)
            self.assertEqual(record['fitted_symbols'],0)
            self.assertEqual(len(record['states']),97)
        h=d['blind_harness']
        self.assertEqual(len(h['plants']),32)
        self.assertEqual(len(h['histogram_decoys']),199)
        self.assertEqual(h['summary']['correct_unique'],32)
        self.assertEqual(d['clock']['K4_application_status'],'underidentified_no_letter_operator')
        self.assertEqual(d['calibration']['planted_ambiguous'],15)
        self.assertEqual(d['calibration']['null_compatible'],6)


if __name__=='__main__':unittest.main()
