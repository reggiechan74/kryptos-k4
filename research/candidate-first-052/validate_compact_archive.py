#!/usr/bin/env python3
"""Validate compact052 ZIP; omitted raw control payloads are explicitly NOT present."""
import collections
import hashlib
import json
import pathlib
import random
import stat
import subprocess
import sys
import tempfile
import zipfile


def sha(data):return hashlib.sha256(data).hexdigest()


def check_null_hashes(cipher,record):
    seed=int.from_bytes(hashlib.sha256(('candidate-first-052-v1|'+record['label']).encode()).digest(),'big')
    rng=random.Random(seed)
    positions=[i for i in range(97) if not(21<=i<34 or 63<=i<74)]
    assert record['count']==len(record['ciphertext_sha256'])==len(record['maximum_scores_bits'])
    for expected in record['ciphertext_sha256']:
        values=[cipher[i] for i in positions];rng.shuffle(values);out=list(cipher)
        for i,value in zip(positions,values):out[i]=value
        assert sha(''.join(out).encode())==expected
    return record['count']


def main(path):
    archive=pathlib.Path(path)
    report={'archive':str(archive.resolve()),'archive_bytes':archive.stat().st_size,'archive_sha256':sha(archive.read_bytes()),
            'archive_type':'compact reproducibility package, not byte-complete raw archive'}
    with zipfile.ZipFile(archive) as z:
        names=z.namelist();assert len(names)==len(set(names));assert z.testzip() is None
        prefix='candidate-first-052/'
        for info in z.infolist():
            pp=pathlib.PurePosixPath(info.filename)
            assert info.filename.startswith(prefix) and not pp.is_absolute() and '..' not in pp.parts
            assert not stat.S_ISLNK(info.external_attr>>16)
            assert not any(part in {'__pycache__','.git','.aws','.codex','.agents','memories','sessions'} for part in pp.parts)
            assert not info.filename.endswith(('.pyc','.pyo','.log','.zip'))
        read=lambda f:z.read(prefix+f)
        data=lambda f:json.loads(read(f))
        manifest=data('ARCHIVE_MANIFEST.json')
        assert set(names)=={prefix+f for f in manifest['files']}|{prefix+'ARCHIVE_MANIFEST.json'}
        for f,item in manifest['files'].items():
            payload=read(f);assert len(payload)==item['bytes'] and sha(payload)==item['sha256'],f
        json_n=jsonl_n=0
        for name in names:
            if name.endswith('.json'):json.loads(z.read(name));json_n+=1
            elif name.endswith('.jsonl'):
                for line in z.read(name).decode().splitlines():
                    if line:json.loads(line);jsonl_n+=1
        frozen=data('freeze.json')
        for f,digest in frozen['files'].items():assert sha(read(f))==digest,f
        for auditfile in ('implementation_code_audit.json','implementation_audit.json'):
            audit=data(auditfile);assert audit['passed']
            for f,digest in audit['audited_sha256'].items():assert sha(read(f))==digest,f
        pre=data('results/pretarget_gate_audit.json');assert pre['passed'] and pre['target_stage_eligible']
        assert pre['freeze_sha256']==sha(read('freeze.json'))
        assert pre['pretarget_gate_sha256']==sha(read('results/pretarget_gate.json'))
        assert pre['control_summary_sha256']==sha(read('results/control_summary.json'))
        ta=data('results/target_audit.json');assert ta['audit_passed'] and not ta['scientific_target_gate_passed']
        for f,digest in ta['bound_file_sha256'].items():assert sha(read(f))==digest,f
        inventory=data('FULL_CONTROL_RECEIPT_INVENTORY.json')
        assert inventory['omitted_file_count']==len(inventory['files'])==84
        assert inventory['control_audit_sha256']==sha(read('results/pretarget_gate_audit.json'))
        assert inventory['freeze_sha256']==sha(read('freeze.json'))
        assert inventory['omitted_total_bytes']==sum(item['bytes'] for item in inventory['files'].values())
        assert set(inventory['files'])==set(pre['control_receipt_sha256'])
        for f,item in inventory['files'].items():
            assert prefix+f not in names and item['included_in_compact_archive'] is False
            assert item['sha256']==pre['control_receipt_sha256'][f]
        bank=data('bank.json');assert len(bank)==1024 and len({r['text'] for r in bank})==1024
        lookup={r['id']:r for r in bank};assert len(lookup)==1024
        groups=('a_themes','b_neutral','c_berlin','d_messages')
        assert collections.Counter(r['group'] for r in bank)=={g:256 for g in groups}
        sources={}
        for group in groups:
            filename=f'authors/{group}.json';records=data(filename);assert len(records)==256
            for r in records:
                alias=group+':'+r['id'];assert alias in lookup
                row=lookup[alias];assert row['original_id']==r['id'] and row['text']==r['normalized']
                assert row['spaced_prose']==r['spaced_prose'] and row['source_sha256']==sha(read(filename))
                assert ''.join(c for c in r['spaced_prose'].upper() if 'A'<=c<='Z')==r['normalized']
                text=r['normalized'];assert len(text)==97 and text[21:34]=='EASTNORTHEAST' and text[63:74]=='BERLINCLOCK'
        excluded={r['text'] for r in data('prior051_bank.json')}|{data('heldout.json')['text']}
        assert not({r['text'] for r in bank}&excluded)
        markdown=data('message_markdown_validation.json')
        assert markdown['count']==1024 and markdown['unique_normalized']==1024 and markdown['all_constraints_valid']
        assert markdown['markdown_sha256']==sha(read('Kryptos-K4-1024-Candidate-Messages.md'))
        for f,digest in markdown['source_sha256'].items():assert sha(read('authors/'+f))==digest
        control_defs={c['id']:c for c in data('controls.json')};assert len(control_defs)==84
        compact=data('results/control_results_compact.json')['controls'];assert len(compact)==84
        control_nulls=0;counts=collections.Counter();validation_n=validation_flags=absent_flags=0
        simple_by_structure=collections.Counter()
        for row in compact:
            cid=row['control_id'];definition=control_defs[cid];inv=inventory['files'][row['source_receipt']]
            assert inv['sha256']==row['source_receipt_sha256'] and inv['bytes']==row['source_receipt_bytes']
            assert row['original_candidate_ranking_count']==1024 and row['original_exact_diagnostic_count']==12288
            top,second=row['top_two_candidates'];assert row['maximum_score_bits']==top['score_bits']
            assert row['different_plaintext_margin_bits']==top['score_bits']-second['score_bits']
            for candidate in row['top_two_candidates']:
                assert lookup[candidate['candidate_id']]['text']==candidate['plaintext']
            cal=row['calibration']['maximum_scores_bits'];assert len(cal)==99
            value=row['maximum_score_bits'];pv=(1+sum(v>=value for v in cal))/100
            flagged=value>=16 and pv<=.05
            summary=row['summary'];assert summary['p_value']==pv and summary['flagged']==flagged
            correct=row['tied_top_candidate_ids']==[definition['plaintext_id']]
            success=correct and flagged and top['exact_full_fit']
            assert summary['successful_recovery']==success and summary['unique_correct_candidate']==correct
            flags=[v>=16 and (1+sum(x>=v for x in cal))/100<=.05 for v in row['validation']['maximum_scores_bits']]
            assert flags==summary['validation_flag_vector'] and sum(flags)==summary['validation_flags']
            kind=definition['kind'];counts[kind]+=success
            if kind in ('simple','structured_hard'):
                validation_n+=len(flags);validation_flags+=sum(flags)
            if kind=='simple':simple_by_structure[definition['structure']]+=success
            if kind=='bank_absent':absent_flags+=flagged
            control_nulls+=check_null_hashes(definition['ciphertext'],row['calibration'])
            control_nulls+=check_null_hashes(definition['ciphertext'],row['validation'])
        assert control_nulls==9036 and counts['simple']==36 and counts['structured_hard']==24
        assert all(v==12 for v in simple_by_structure.values()) and validation_n==600 and validation_flags==0 and absent_flags==0
        target=data('results/target.json');ranked=target['scores']['ranked_candidates'];assert len(ranked)==1024
        assert {r['candidate_id'] for r in ranked}==set(lookup)
        for row in ranked:assert row['plaintext']==lookup[row['candidate_id']]['text'] and row['spaced_prose']==lookup[row['candidate_id']]['spaced_prose']
        nulls=target['conditional_nulls']['maximum_scores_bits'];assert len(nulls)==1999
        value=target['scores']['maximum_score_bits'];assert value==ranked[0]['score_bits']
        assert (1+sum(v>=value for v in nulls))/2000==target['global_p_value']==.519
        assert sum(v==value for v in nulls)==62
        assert target['scores']['different_plaintext_margin_bits']==ranked[0]['score_bits']-ranked[1]['score_bits']
        assert not target['expansion_gate']['passed'] and not any(target['expansion_gate']['checks'].values())
        diag=target['exact_diagnostics'];assert len(diag)==12288
        assert all(d['full_inverse'] and d['full_reencryption'] for d in diag)
        assert not any(d['registered_exact_periods'] or d['exact_plaintext_autokey_lengths'] or d['exact_ciphertext_autokey_lengths'] for d in diag)
        canonical=read('target.txt').decode().strip()
        assert len(canonical)==97 and sha(canonical.encode())=='eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab'
        target_nulls=check_null_hashes(canonical,target['conditional_nulls']);assert target_nulls==1999
        report.update({'zip_crc_pass':True,'safe_unique_paths':True,'packaged_file_count':len(names),
                       'packaged_payload_hashes_verified':len(manifest['files']),'frozen_source_hashes_verified':len(frozen['files']),
                       'json_files_parsed':json_n,'jsonl_records_parsed':jsonl_n,'candidate_aliases_prose_exclusions_verified':1024,
                       'compact_control_records_verified':84,'control_null_hashes_regenerated_without_scoring':control_nulls,
                       'target_null_hashes_regenerated_without_scoring':target_nulls,'full_target_rankings_retained':1024,
                       'full_target_exact_diagnostics_retained':12288,'omitted_control_receipt_count':84,
                       'omitted_control_receipt_bytes':inventory['omitted_total_bytes'],'omitted_inventory_matches_independent_audit':True,
                       'omitted_control_payload_bytes_verified_from_archive':False,'gate_and_target_arithmetic_verified':True,
                       'all_audit_bindings_present_or_explicitly_inventoried':True})
        with tempfile.TemporaryDirectory(prefix='candidate-first-052-compact-') as directory:
            z.extractall(directory);cwd=pathlib.Path(directory)/'candidate-first-052'
            tests=subprocess.run([sys.executable,'-m','unittest','-v','test_native','test_runner'],cwd=cwd,text=True,capture_output=True)
            assert tests.returncode==0 and 'Ran 14 tests' in tests.stderr,tests.stdout+tests.stderr
            frozen_check=subprocess.run([sys.executable,'run_experiment.py','verify-freeze'],cwd=cwd,text=True,capture_output=True)
            assert frozen_check.returncode==0 and frozen_check.stdout.strip()==sha(read('freeze.json')),frozen_check.stdout+frozen_check.stderr
            report['fresh_extraction_synthetic_tests']='14/14 passed'
            report['fresh_extraction_source_freeze_verification']='passed; does not verify omitted control payloads'
    report['passed']=True
    print(json.dumps(report,indent=2,sort_keys=True))


if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('usage: python validate_compact_archive.py compact.zip')
    main(sys.argv[1])
