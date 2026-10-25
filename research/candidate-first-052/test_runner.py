"""Import, stage-integrity, control-schedule and null-pipeline tests using only synthetic banks."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import concurrent.futures
import import_bank
import native
import reference as p
import run_experiment as runner
from test_native import synthetic_bank,random_cipher


class RunnerTests(unittest.TestCase):
    def fixture(self,root):
        (root/'authors').mkdir()
        for group in p.GROUPS_BANK:
            records=[{'id':r['id'],'spaced_prose':r['text'],'normalized':r['text'],
                      'revision_history':[],'theme':'synthetic test fixture','authoring_method':'synthetic test only'}
                     for r in synthetic_bank() if r['group']==group]
            p.write_json(root/'authors'/f'{group}.json',records)
        p.write_json(root/'prior051_bank.json',synthetic_bank(32,seed=131))
        heldout=synthetic_bank(4,seed=132)[0];heldout['group']='heldout'
        p.write_json(root/'heldout.json',heldout)
        (root/'running_key.txt').write_bytes((runner.ROOT/'running_key.txt').read_bytes())
        (root/'config.json').write_bytes((runner.ROOT/'config.json').read_bytes())
        with mock.patch.object(import_bank,'ROOT',root):bank,receipt=import_bank.import_records()
        p.write_json(root/'bank.json',bank);p.write_json(root/'bank_import.json',receipt)
        return bank,receipt

    def test_import_preserves_bytes_aliases_prose_sources_and_exclusions(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);bank,receipt=self.fixture(root)
            before={f:f.read_bytes() for f in (root/'authors').glob('*.json')}
            with mock.patch.object(import_bank,'ROOT',root):again,again_receipt=import_bank.import_records()
            self.assertEqual(bank,again);self.assertEqual(receipt,again_receipt)
            self.assertEqual(len(bank),1024);self.assertEqual(len({r['text'] for r in bank}),1024)
            for r in bank:
                self.assertEqual(r['id'],r['group']+':'+r['original_id'])
                self.assertEqual(r['source_sha256'],p.sha256_file(root/r['source_file']))
            self.assertEqual(before,{f:f.read_bytes() for f in before})
            # Cross-author duplicate must fail rather than be silently dropped.
            a=p.load_json(root/'authors/a_themes.json');b=p.load_json(root/'authors/b_neutral.json')
            b[0]['normalized']=a[0]['normalized'];b[0]['spaced_prose']=a[0]['spaced_prose']
            p.write_json(root/'authors/b_neutral.json',b)
            with mock.patch.object(import_bank,'ROOT',root):
                with self.assertRaisesRegex(ValueError,'Duplicate normalized'):import_bank.import_records()

    def test_prior_bank_exclusion_and_length_crib_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);self.fixture(root)
            records=p.load_json(root/'authors/a_themes.json')
            excluded=p.load_json(root/'prior051_bank.json')[0]['text']
            records[0]['normalized']=excluded;records[0]['spaced_prose']=excluded
            p.write_json(root/'authors/a_themes.json',records)
            with mock.patch.object(import_bank,'ROOT',root):
                with self.assertRaisesRegex(ValueError,'Prior051/heldout'):import_bank.import_records()
            records[0]['normalized']='A'*97;records[0]['spaced_prose']='A'*97
            p.write_json(root/'authors/a_themes.json',records)
            with mock.patch.object(import_bank,'ROOT',root):
                with self.assertRaisesRegex(ValueError,'crib position'):import_bank.import_records()

    def test_controls_reproduce_and_cover_balanced_spread(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);bank,_=self.fixture(root)
            with mock.patch.object(runner,'ROOT',root):
                controls=runner.build_controls();self.assertEqual(controls,runner.build_controls())
            self.assertEqual(len(controls),84)
            inscope=[c for c in controls if c['kind'] in ('simple','structured_hard')]
            self.assertEqual(len(inscope),60);self.assertEqual(len({c['plaintext_id'] for c in inscope}),60)
            self.assertEqual({g:sum(c['plaintext_group']==g for c in inscope) for g in p.GROUPS_BANK},{g:15 for g in p.GROUPS_BANK})
            for c in controls:
                t=p.TABLEAU_BY_ID[c['tableau_id']];key=p.encode(c['full_key_AZ'],'AZ')
                self.assertEqual(p.encrypt_key(c['plaintext'],key,t),c['ciphertext'])
                self.assertEqual(p.decrypt_key(c['ciphertext'],key,t),c['plaintext'])
            rows=[{'kind':c['kind'],'planted_structure':c['structure'],'successful_recovery':True,
                   'validation_flags':0,'validation_count':10 if c['kind']!='running_key' else 0,
                   'flagged':c['kind'] in ('simple','structured_hard')} for c in controls]
            self.assertTrue(runner.control_gate(rows)['passed'])
            self.assertFalse(runner.control_gate(rows[:-1])['passed'])
            rows[0]['validation_flags']=31;self.assertFalse(runner.control_gate(rows)['passed'])

    def test_audit_binds_every_required_source_and_binary(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);hashes={}
            for name in runner.AUDITED_SOURCE_NAMES:
                (root/name).write_text('synthetic audited source '+name);hashes[name]=p.sha256_file(root/name)
            audit={'passed':True,'audited_sha256':hashes};runner.verify_audited_sources(audit,root)
            with self.assertRaises(ValueError):runner.verify_audited_sources({'passed':True},root)
            (root/'scorer.so').write_text('post-audit mutation')
            with self.assertRaises(ValueError):runner.verify_audited_sources(audit,root)

    def test_run_nulls_uses_same_full_native_scorer_and_rng(self):
        bank=synthetic_bank(8);scorer=native.NativeScorer(bank,8);cipher=random_cipher(43210)
        result=runner.run_nulls(scorer,cipher,7,'synthetic-runner-null')
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            parallel=runner.run_nulls(scorer,cipher,7,'synthetic-runner-null',executor)
        self.assertEqual(result,parallel)
        rng=p.rng_for('synthetic-runner-null')
        nulls=[p.conditioned_null(cipher,rng) for _ in range(7)]
        self.assertEqual(result['ciphertext_sha256'],[hashlib.sha256(v.encode()).hexdigest() for v in nulls])
        self.assertEqual(result['maximum_scores_bits'],[p.Scorer(bank,8).score(v) for v in nulls])

    def test_wrong_canonical_target_refused_before_scoring(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);self.fixture(root);(root/'results').mkdir()
            p.write_json(root/'results/pretarget_gate.json',{'passed':True,'freeze_sha256':'test-only'})
            (root/'wrong.txt').write_text('A'*97)
            with mock.patch.object(runner,'ROOT',root),mock.patch.object(runner,'verify_freeze',return_value='test-only'):
                with mock.patch.object(native.NativeScorer,'score',side_effect=AssertionError('Must not score wrong target')):
                    with self.assertRaisesRegex(ValueError,'Canonical target SHA256 mismatch'):
                        runner.run_target(root/'wrong.txt',1)


if __name__=='__main__':unittest.main(verbosity=2)
