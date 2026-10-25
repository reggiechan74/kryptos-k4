#!/usr/bin/env python3
"""Read-only compact-archive verification and isolated deterministic replication.

This post-experiment utility is NOT a new scorer/model. Frozen files stay untouched.
It copies byte-verified audited source into temporary scratch space to accommodate
explicit environment/path binding of the production loader. No network required.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from tempfile import TemporaryDirectory
import argparse,hashlib,json,shutil,subprocess,sys,zipfile,collections
ROOT=Path(__file__).resolve().parent
RUNTIME=('reference.py','native.py','native053.c','run_experiment.py','prepare_data.py','prepare_source_plan.py',
         'test_reference.py','test_native.py','test_runner.py','config.json')
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read(path):return json.loads(Path(path).read_text())
def write(path,value):Path(path).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')

def verify_payload():
    manifest=read(ROOT/'ARCHIVE_MANIFEST.json');checked=0
    for name,entry in manifest['files'].items():
        f=ROOT/name
        if not f.is_file() or f.stat().st_size!=entry['bytes'] or sha(f)!=entry['sha256']:raise ValueError('Archive payload mismatch: '+name)
        checked+=1
    omitted=read(ROOT/'OMITTED_FILES_INVENTORY.json');allowed={**omitted['control_receipts'],**omitted['frozen_files']}
    frozen=read(ROOT/'freeze.json')['files'];included=missing=0
    for name,digest in frozen.items():
        f=ROOT/name
        if f.exists():
            if sha(f)!=digest:raise ValueError('Frozen input mismatch: '+name)
            included+=1
        elif name in allowed and allowed[name]['sha256']==digest:missing+=1
        else:raise ValueError('Unaccounted missing frozen file: '+name)
    accounting=read(ROOT/'FROZEN_INPUT_ACCOUNTING.json')
    if accounting['included_count']!=included or accounting['omitted_count']!=missing:raise ValueError('Wrong frozen accounting')
    audits={}
    for name in ('implementation_audit.json','results/pretarget_gate_audit.json','results/target_audit.json'):
        cert=read(ROOT/name);present=absent=0
        if cert['passed'] is not True:raise ValueError('Failed audit certificate')
        for path,digest in cert['audited_sha256'].items():
            f=ROOT/path
            if f.is_file():
                if sha(f)!=digest:raise ValueError('Audit-bound file mismatch: '+path)
                present+=1
            elif path in allowed and allowed[path]['sha256']==digest:absent+=1
            else:raise ValueError('Unaccounted audit evidence: '+path)
        audits[name]={'present_hashes_checked':present,'omitted_hashes_accounted_not_physically_verified':absent}
    return {'payload_hashes_checked':checked,'frozen_inputs_present_verified':included,'frozen_inputs_omitted_accounted':missing,'audit_accounting':audits}

def prepare_runtime(scratch):
    for name in RUNTIME:shutil.copyfile(ROOT/name,scratch/name)
    # No freeze or old build receipt is copied; original archived files are untouched.
    sys.path.insert(0,str(scratch))
    import reference as p,native,run_experiment as r
    binary=native.build_native()
    return p,native,r,{'rebuilt_binary_sha256':sha(binary),'original_binary_sha256':sha(ROOT/'native053.so'),'binary_identical':sha(binary)==sha(ROOT/'native053.so')}

def verify_windows_and_training(scratch,p):
    plan=read(ROOT/'CONTROL_SOURCE_PLAN.json');extracted=0
    for corpus in ('gutenberg','inaugural'):
        with zipfile.ZipFile(ROOT/f'data/raw/{corpus}.zip') as z:
            for item in z.infolist():
                name=Path(item.filename)
                if name.is_absolute() or '..' in name.parts:raise ValueError('Unsafe ZIP entry')
                if item.is_dir():continue
                target=scratch/'data/documents'/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(z.read(item));extracted+=1
    for doc in plan['documents']:
        if sha(scratch/doc['raw_path'])!=doc['raw_sha256']:raise ValueError('Source document mismatch')
    for name in ('CONTROL_SOURCE_PLAN.json','windows.json'):shutil.copyfile(ROOT/name,scratch/name)
    (scratch/'controls').mkdir(exist_ok=True)
    shutil.copyfile(ROOT/'controls/novel_key_documents.json',scratch/'controls/novel_key_documents.json')
    import prepare_data
    receipt=prepare_data.train_model()
    for name,digest in read(ROOT/'model/training_receipt.json')['files'].items():
        if sha(scratch/name)!=digest:raise ValueError('Recreated model/count mismatch: '+name)
    if sha(scratch/'model/training_receipt.json')!=sha(ROOT/'model/training_receipt.json'):raise ValueError('Training/calibration receipt mismatch')
    return {'published_documents_recreated':len(plan['documents']),'archive_members_extracted':extracted,'training_letters':receipt['training_letters'],
            'all_count_log_and_calibration_receipt_hashes_exact':True,'calibration_count':receipt['calibration_count']}

def check_null_rows(cipher,rows,label,p,model,bank):
    expected=p.conditional_nulls(cipher,len(rows),label)
    for c,row in zip(expected,rows):
        if row['ciphertext']!=c or row['ciphertext_sha256']!=hashlib.sha256(c.encode()).hexdigest():raise ValueError('Null input mismatch')
        rec=bank[row['candidate_id']];t=p.TABLEAU_BY_ID[row['tableau_id']];key=p.derive_key(rec['text'],c,t)
        if key!=row['key'] or model.score_key(key)!=row['score_bits'] or model.full_cross_entropy(key)!=row['full_key_cross_entropy']:raise ValueError('Null winner score/key mismatch')
    return len(rows)

def validate(scratch,p,native,r):
    tests=subprocess.run([sys.executable,'-m','unittest','-v','test_reference','test_native','test_runner'],cwd=scratch,text=True,capture_output=True)
    if tests.returncode:raise RuntimeError(tests.stdout+tests.stderr)
    bank=p.validate_bank(read(ROOT/'bank.json'));byid={x['id']:x for x in bank};model=p.LanguageModel.load(ROOT/'model/log_tables.bin')
    target=read(ROOT/'results/target_result.json');observed=target['observed'];reference=p.reference_scores(bank,target['ciphertext'],model)
    saved={(x['candidate_id'],x['tableau_id']):x for x in observed['ranking']}
    if len(saved)!=12288 or len(observed['ranked_candidates'])!=1024:raise ValueError('Incomplete target hypotheses')
    for row in reference:
        old=saved[(row['candidate_id'],row['tableau_id'])]
        if any(old[k]!=v for k,v in row.items()):raise ValueError('Target reference mismatch')
    for row in observed['ranked_candidates']:
        if row['spaced_prose']!=byid[row['candidate_id']]['spaced_prose']:raise ValueError('Target prose mismatch')
    target_null_count=check_null_rows(target['ciphertext'],target['nulls'],'K4|conditional-null',p,model,byid)
    specs={x['id']:x for x in read(ROOT/'controls.json')};compact=read(ROOT/'results/control_null_receipts.json');nullcount=0
    summaries={x['id']:x for x in read(ROOT/'results/control_results.json')['controls']}
    ceiling=read(ROOT/'model/training_receipt.json')['full_key_cross_entropy_ceiling']
    for entry in compact['controls']:
        spec=specs[entry['id']];cal=entry['calibration_nulls'];val=entry['validation_nulls'];summary=summaries[entry['id']]
        nullcount+=check_null_rows(spec['ciphertext'],cal,spec['calibration_rng_label'],p,model,byid)
        nullcount+=check_null_rows(spec['ciphertext'],val,spec['validation_rng_label'],p,model,byid)
        maxima=[x['score_bits'] for x in cal]
        if summary['conditional_p']!=r.tail_p(summary['observed_score_bits'],maxima):raise ValueError('Control p mismatch')
        for row in val:
            pv=r.tail_p(row['score_bits'],maxima)
            if row['conditional_p']!=pv or row['flagged']!=r.detection(row,pv,ceiling):raise ValueError('Validation p/flag mismatch')
    gate=r.control_gate(list(summaries.values()));savedgate=read(ROOT/'results/control_gate.json')
    if any(savedgate[k]!=v for k,v in gate.items()):raise ValueError('Control gate mismatch')
    if target['global_p']!=r.tail_p(observed['score_bits'],[x['score_bits'] for x in target['nulls']]):raise ValueError('Target p mismatch')
    # Replicate one entire original control receipt, including full-bank null maxima,
    # and compare its exact serialized hash to the omitted original inventory.
    scorer=native.NativeScorer(bank,model);spec=specs['C001'];c=r.configuration()
    with ThreadPoolExecutor(max_workers=c['workers']) as executor:receipt=r.evaluate_control(spec,scorer,ceiling,executor,c)
    path=scratch/'C001.json';p.write_json(path,receipt)
    expected=read(ROOT/'OMITTED_FILES_INVENTORY.json')['control_receipts']['results/controls/C001.json']['sha256']
    if sha(path)!=expected:raise ValueError('Exact first-control reproduction mismatch')
    return {'synthetic_tests_passed':22,'tests_output':tests.stdout+tests.stderr,'target_reference_hypotheses_verified':len(reference),
            'target_candidate_prose_verified':1024,'target_null_inputs_and_winner_stats_verified':target_null_count,
            'control_null_inputs_and_winner_stats_verified':nullcount,'control_gates_recomputed':True,
            'full_control_receipts_regenerated_byte_exact':1,'regenerated_control_id':'C001',
            'scope_note':'Only C001 full control/maxima replayed here. Other null inputs/winner statistics and saved p/gates checked, NOT every full-bank null maximum independently recomputed.'}

def recreate_controls(output,p,native,r):
    output=Path(output).resolve()
    if output.exists() and any(output.iterdir()):raise ValueError('Controls output must be a new/empty directory')
    output.mkdir(parents=True,exist_ok=True)
    bank=read(ROOT/'bank.json');model=p.LanguageModel.load(ROOT/'model/log_tables.bin');scorer=native.NativeScorer(bank,model)
    ceiling=read(ROOT/'model/training_receipt.json')['full_key_cross_entropy_ceiling'];c=r.configuration();inventory=read(ROOT/'OMITTED_FILES_INVENTORY.json')['control_receipts'];count=0
    with ThreadPoolExecutor(max_workers=c['workers']) as executor:
        for spec in read(ROOT/'controls.json'):
            result=r.evaluate_control(spec,scorer,ceiling,executor,c);path=output/(spec['id']+'.json');p.write_json(path,result)
            if sha(path)!=inventory['results/controls/'+spec['id']+'.json']['sha256']:raise ValueError('Regenerated receipt hash mismatch: '+spec['id'])
            count+=1;print(f'Exact control receipt regenerated {count}/144: {spec["id"]}',flush=True)
    return {'controls_regenerated_byte_exact':count,'output':str(output)}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--validate',action='store_true');parser.add_argument('--verify-training',action='store_true');parser.add_argument('--controls-output');parser.add_argument('--validation-output');args=parser.parse_args()
    if not any((args.validate,args.verify_training,args.controls_output)):parser.error('Choose a verification or regeneration action')
    result={'archive_accounting':verify_payload()}
    with TemporaryDirectory(prefix='candidate-first-053-replay-') as tmp:
        scratch=Path(tmp);p,native,r,build=prepare_runtime(scratch);result['isolated_build']=build
        if args.validate:result['validation']=validate(scratch,p,native,r)
        if args.verify_training:result['training_reproduction']=verify_windows_and_training(scratch,p)
        if args.controls_output:result['control_reproduction']=recreate_controls(args.controls_output,p,native,r)
    result['passed']=True
    if args.validation_output:write(args.validation_output,result)
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
