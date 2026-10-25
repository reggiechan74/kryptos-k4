#!/usr/bin/env python3
"""Validate the 051 deliverable ZIP without changing its contents or rerunning null scores."""
import hashlib
import json
import math
import pathlib
import stat
import subprocess
import sys
import tempfile
import zipfile


def sha(data):return hashlib.sha256(data).hexdigest()


def main(path):
    archive=pathlib.Path(path)
    report={"archive":str(archive.resolve()),"archive_bytes":archive.stat().st_size,"archive_sha256":sha(archive.read_bytes())}
    with zipfile.ZipFile(archive) as z:
        names=z.namelist()
        assert len(names)==len(set(names)),"Duplicate ZIP paths"
        assert z.testzip() is None,"ZIP CRC failure"
        root="candidate-first-051/"
        for info in z.infolist():
            p=pathlib.PurePosixPath(info.filename)
            assert info.filename.startswith(root) and not p.is_absolute() and '..' not in p.parts
            assert not stat.S_ISLNK(info.external_attr>>16),"Symlinks forbidden"
            assert not any(part in {"__pycache__",".git",".aws",".codex",".agents","memories","sessions"} for part in p.parts)
            assert not info.filename.endswith((".pyc",".pyo",".log",".zip"))
        read=lambda relative:z.read(root+relative)
        data=lambda relative:json.loads(read(relative))
        manifest=data("ARCHIVE_MANIFEST.json")
        expected={root+name for name in manifest["files"]}|{root+"ARCHIVE_MANIFEST.json"}
        assert set(names)==expected,"Manifest inventory mismatch"
        for name,entry in manifest["files"].items():
            payload=read(name)
            assert len(payload)==entry["bytes"] and sha(payload)==entry["sha256"],name
        json_count=jsonl_count=0
        for name in names:
            if name.endswith('.json'):
                json.loads(z.read(name));json_count+=1
            elif name.endswith('.jsonl'):
                for line in z.read(name).decode().splitlines():
                    if line:json.loads(line);jsonl_count+=1
        frozen=data('freeze.json')
        for name,digest in frozen['files'].items():assert sha(read(name))==digest,name
        audit=data('implementation_audit.json')
        assert audit['passed']
        for name,digest in audit['audited_sha256'].items():assert sha(read(name))==digest,name
        preaudit=data('results/pretarget_gate_audit.json')
        assert preaudit['passed'] and preaudit['target_stage_eligible']
        for name,digest in preaudit['control_receipt_sha256'].items():assert sha(read(name))==digest,name
        ta=data('results/target_audit.json')
        assert ta['audit_passed'] and not ta['scientific_target_gate_passed'] and not ta['open_blockers']
        for name,digest in ta['bound_file_sha256'].items():assert sha(read(name))==digest,name
        bank=data('bank.json');assert len(bank)==32 and len({r['text'] for r in bank})==32
        source={}
        lines=['Candidate first Kryptos pilot 051','32 frozen authored messages, not proposed verified decryptions.','IDs below are the original candidate aliases. Fictional local details are unverified.','']
        for group in ('thematic','neutral'):
            for rec in sorted(data(f'authors/{group}.json'),key=lambda r:r['id']):
                assert rec['id'] not in source
                source[rec['id']]=rec
                lines += [f"{rec['id']} | {group}",rec['spaced_prose'],'']
        assert read('CANDIDATES.txt').decode()=='\n'.join(lines)+'\n'
        for rec in bank:
            assert source[rec['id']]['normalized']==rec['text']
            assert len(rec['text'])==97 and rec['text'][21:34]=='EASTNORTHEAST' and rec['text'][63:74]=='BERLINCLOCK'
        target=data('results/target.json');ranked=target['scores']['ranked_candidates']
        assert len(ranked)==32 and {r['candidate_id'] for r in ranked}==set(source)
        assert len(target['exact_diagnostics'])==384
        nulls=target['conditional_nulls']['maximum_scores_bits'];assert len(nulls)==1999
        score=target['scores']['maximum_score_bits']
        pv=(1+sum(v>=score for v in nulls))/2000
        assert pv==target['global_p_value']==.916
        assert not target['expansion_gate']['passed']
        assert abs(ranked[0]['score_bits']-ranked[1]['score_bits']-target['scores']['different_plaintext_margin_bits'])<1e-12
        canonical=read('target.txt').decode().strip()
        assert len(canonical)==97 and sha(canonical.encode())=='eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab'
        controls=data('controls.json');assert len(controls)==84
        control_nulls=0
        for control in controls:
            rec=data(f"results/controls/{control['id']}.json")
            assert rec['control']==control and len(rec['scores']['ranked_candidates'])==32
            assert len(rec['exact_diagnostics'])==384
            control_nulls+=len(rec['calibration']['maximum_scores_bits'])+len(rec['validation']['maximum_scores_bits'])
        assert control_nulls==9036
        report.update({"zip_crc_pass":True,"safe_unique_paths":True,"packaged_file_count":len(names),
                       "payload_hashes_verified":len(manifest['files']),"frozen_hashes_verified":len(frozen['files']),
                       "json_files_parsed":json_count,"jsonl_records_parsed":jsonl_count,"candidate_aliases_and_prose_verified":32,
                       "control_receipts_verified":84,"control_null_records":control_nulls,"target_null_records":1999,
                       "source_and_result_audit_hashes_verified":True,"target_statistics_verified":True})
        with tempfile.TemporaryDirectory(prefix='candidate-first-051-archive-') as directory:
            z.extractall(directory)
            cwd=pathlib.Path(directory)/'candidate-first-051'
            tests=subprocess.run([sys.executable,'-m','unittest','-v','test_pilot'],cwd=cwd,text=True,capture_output=True)
            assert tests.returncode==0,tests.stdout+tests.stderr
            assert 'Ran 14 tests' in tests.stderr
            frozen_run=subprocess.run([sys.executable,'run_experiment.py','verify-freeze'],cwd=cwd,text=True,capture_output=True)
            assert frozen_run.returncode==0,frozen_run.stdout+frozen_run.stderr
            assert frozen_run.stdout.strip()==sha(read('freeze.json'))
            report.update({"fresh_extraction_unit_tests":"14/14 passed","fresh_extraction_verify_freeze":"passed"})
    report['passed']=True
    print(json.dumps(report,indent=2,sort_keys=True))


if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('usage: python validate_archive.py deliverable.zip')
    main(sys.argv[1])
