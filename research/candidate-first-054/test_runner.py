import unittest,tempfile
from pathlib import Path
from unittest.mock import patch
import search as s
import run_experiment as r
from test_search import PLAIN,key_for
class RunnerTests(unittest.TestCase):
    def test_audit_hash_binding(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'code').write_text('audited');audit={'passed':True,'audited_sha256':{'code':s.sha_file(root/'code')}}
            r.verify_audit(audit,root,['code']);(root/'code').write_text('changed')
            with self.assertRaises(ValueError):r.verify_audit(audit,root,['code'])
            with self.assertRaises(ValueError):r.verify_audit({'passed':True},root,['code'])
    def test_target_blocked_before_freeze(self):
        with tempfile.TemporaryDirectory() as d:
            with patch.object(r,'ROOT',Path(d)):
                with self.assertRaises(FileNotFoundError):r.require_target_gate()
    def test_positive_requires_exact_planted_coordinates_key_plaintext(self):
        t=s.TABLEAUX[0];key=key_for('runner');cipher=s.encrypt(PLAIN,key,t);doc=s.Document.from_bytes('source',key.encode());result=s.search_all(cipher,[doc])
        spec={'id':'fake','kind':'planted_positive','tableau_id':t.id,'source_document_id':'source','source_window_start':0,'key':key,'plaintext':PLAIN}
        self.assertTrue(r.summarize_control(spec,result)['passed'])
        for k,v in [('source_document_id','wrong'),('source_window_start',1),('key','A'*97),('plaintext','A'*97)]:
            altered={**spec,k:v};self.assertFalse(r.summarize_control(altered,result)['passed'])
    def test_absent_control_any_hit_fails_and_missing_coverage_fails(self):
        t=s.TABLEAUX[0];key=key_for('absent');cipher=s.encrypt(PLAIN,key,t);doc=s.Document.from_bytes('source',key.encode());result=s.search_all(cipher,[doc])
        spec={'id':'fake','kind':'random_absent','tableau_id':t.id}
        self.assertFalse(r.summarize_control(spec,result)['passed'])
        result=s.search_all(cipher,[s.Document.from_bytes('empty',b'Z'*97)])
        self.assertTrue(r.summarize_control(spec,result)['passed']);result['coverage']=[]
        self.assertFalse(r.summarize_control(spec,result)['passed'])
    def test_gate_exact_denominators_and_all_models(self):
        rows=[]
        for t in s.TABLEAUX:
            for j in range(3):rows.append({'kind':'planted_positive','passed':True,'planted_tableau_id':t.id,'reference_and_crypto_integrity_passed':True,'hit_count':1})
        for t in s.TABLEAUX:rows.append({'kind':'random_absent','passed':True,'planted_tableau_id':t.id,'reference_and_crypto_integrity_passed':True,'hit_count':0})
        self.assertTrue(r.control_gate(rows)['passed']);self.assertFalse(r.control_gate(rows[:-1])['passed'])
        rows[0]['passed']=False;self.assertFalse(r.control_gate(rows)['passed'])
    def test_reconstruction_failure_is_fatal(self):
        t=s.TABLEAUX[0];key=key_for('failure');cipher=s.encrypt(PLAIN,key,t);doc=s.Document.from_bytes('fixture',key.encode())
        with patch.object(s,'independent_reconstruction',return_value=('A'*97,'A'*97)):
            with self.assertRaises(AssertionError):s.search_all(cipher,[doc])
if __name__=='__main__':unittest.main()
