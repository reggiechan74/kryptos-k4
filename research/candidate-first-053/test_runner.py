import unittest,tempfile
from pathlib import Path
from unittest.mock import patch
import reference as p
import run_experiment as r

class RunnerTests(unittest.TestCase):
    def test_audit_hash_binding(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'code.py').write_text('unchanged')
            audit={'passed':True,'audited_sha256':{'code.py':p.sha256_file(root/'code.py')}}
            r.verify_audit_bindings(audit,root,['code.py'])
            (root/'code.py').write_text('changed')
            with self.assertRaises(ValueError):r.verify_audit_bindings(audit,root,['code.py'])
            with self.assertRaises(ValueError):r.verify_audit_bindings({'passed':True},root,['code.py'])
    def test_detection_and_tail_include_ties(self):
        self.assertEqual(r.tail_p(2,[1,2,2,3]),.8)
        w={'score_bits':32,'full_key_cross_entropy':3.6}
        self.assertTrue(r.detection(w,.05,3.6));self.assertFalse(r.detection(w,.051,3.6));self.assertFalse(r.detection(w,.05,3.59))
        w['score_bits']=31.999;self.assertFalse(r.detection(w,0,4))
    def test_gate_counts_and_each_condition(self):
        rows=[]
        for kind,n in [('published_prose',36),('hard_style',24),('novel_prose',12),('uniform_key',24),('letter_permuted',24),('plaintext_absent',12),('word_order_stress',12)]:
            for j in range(n):rows.append({'kind':kind,'successful_recovery':kind in ('published_prose','hard_style','novel_prose'),
                       'flagged':kind in ('published_prose','hard_style','novel_prose'),'planted_tableau_id':p.TABLEAUX[j%12].id,
                       'validation_count':10,'validation_flags':0,'all_candidate_model_crypto_passed':True})
        self.assertTrue(r.control_gate(rows)['passed'])
        for row in rows[:5]:row['successful_recovery']=False
        self.assertFalse(r.control_gate(rows)['checks']['published_recovery'])
        rows[72]['flagged']=True;rows[73]['flagged']=True;rows[74]['flagged']=True
        self.assertFalse(r.control_gate(rows)['checks']['negative_flags'])
        rows[0]['validation_flags']=73
        self.assertFalse(r.control_gate(rows)['checks']['validation_flags'])
        self.assertFalse(r.control_gate(rows[:-1])['checks']['complete_counts'])
    def test_target_denied_without_freeze(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(r,'ROOT',Path(tmp)):
                with self.assertRaises(FileNotFoundError):r.require_target_gate()
    def test_absent_recovery_requires_candidate_not_englishness(self):
        # Isolate orchestration with literal synthetic fake maxima, no actual corpus/bank.
        class Scorer:
            bank=[{'id':'other','text':'A'*97,'group':'synthetic'}]
            def score(self,cipher,details=False):
                row={'candidate_id':'other','tableau_id':p.TABLEAUX[0].id,'score_bits':40 if cipher=='A'*97 else 0,
                     'key':'B'*97,'full_key_cross_entropy':2.,'margin_bits':10,'unique_top_plaintext':True,
                     'full_reencryption':True,'full_inverse':True,'ties':[]}
                if details:row['ranking']=[dict(row)]
                return row
        class Executor:
            def map(self,fn,values):return map(fn,values)
        spec={'id':'fake','kind':'plaintext_absent','ciphertext':'A'*97,'plaintext_id':'missing','tableau_id':p.TABLEAUX[0].id,
              'key':'B'*97,'source_document':'synthetic','calibration_rng_label':'cal','validation_rng_label':'val'}
        with patch.object(p,'conditional_nulls',lambda c,n,l:['C'*97]*n):
            receipt=r.evaluate_control(spec,Scorer(),3.,Executor(),{'calibration_nulls_per_control':99,'validation_nulls_per_control':10,'control_alpha':.05})
        self.assertTrue(receipt['summary']['flagged']);self.assertFalse(receipt['summary']['successful_recovery'])
        self.assertTrue(receipt['summary']['exact_key_recovered'])

if __name__=='__main__':unittest.main()
