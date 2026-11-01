"""One frozen raw-format control or K4 slot; inert on import/help.
No target source input, matrices, imports of scientific modules, or output
construction occurs before exact stage authority, bounds and source pins.
"""
import argparse
import ctypes
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import signal
import sys
import time
ROOT=Path('/workspace/shared/k4-canonical-residual-recovered-target-v1')
ENGINE=Path('/workspace/shared/k4-canonical-residual-recovered-target-v1/scientific/residual_decoder.py')
AFFINE=ENGINE.with_name('affine_filter.py')
REFERENCE=Path('/workspace/shared/k4-canonical-residual-recovered-target-v1/scientific/reference_v3.py')
PREFLIGHT=Path('/workspace/shared/k4-canonical-residual-recovered-target-v1/scientific/preflight_blind.py')
CHECKER=Path('/workspace/shared/k4-canonical-residual-recovered-target-v1/scientific/checker_blind.py')
ENGINE_PIN='be050003b9a73c14a7f7dda44afeb160e0e847045d57ddfa4b9527bdc68f7d67'
AFFINE_PIN='1e19e9ad872d517487cfe7968a9f4b906756007d5e710be216807620f078c90d'
REFERENCE_PIN='0730f8b0a26109919ba6eb558be18063d137ced233b397cd188dc261a13fe8f9'
MIB=1024*1024
REPORT_MAX=2*MIB
HASH_MAX=64*MIB
REPORT_SCHEMA='k4-residual-slot-report-v1'

def require(condition,message):
    if not condition: raise ValueError(message)


def sha(path,limit=MIB):
    path=Path(path)
    require(path.is_file() and not path.is_symlink() and path.stat().st_size<=limit,'bounded hash input')
    h=hashlib.sha256()
    total=0
    with path.open('rb') as f:
        for block in iter(lambda:f.read(min(MIB,limit+1)),b''):
            require(len(block)<=limit-total,'hash input grew past cap')
            total+=len(block);h.update(block)
    return h.hexdigest()


def unique(pairs):
    out={}
    for key,value in pairs:
        require(key not in out,'duplicate JSON key');out[key]=value
    return out


def read_json(path,limit):
    path=Path(path)
    require(path.is_file() and not path.is_symlink() and path.stat().st_size<=limit,'bounded regular JSON file')
    with path.open('rb') as f:raw=f.read(limit+1)
    require(len(raw)<=limit,'JSON grew beyond cap')
    return json.loads(raw,object_pairs_hook=unique,
        parse_constant=lambda _s:(_ for _ in ()).throw(ValueError('nonfinite JSON')))


def canonical(value):
    return (json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()


def load(name,path,pin):
    path=Path(path)
    require(path.is_file() and not path.is_symlink() and path.stat().st_size<=MIB,'bounded pinned isolated source')
    with path.open('rb') as handle:source=handle.read(MIB+1)
    require(len(source)<=MIB and hashlib.sha256(source).hexdigest()==pin,'pinned isolated module: '+str(path))
    spec=importlib.util.spec_from_file_location(name,path)
    require(spec is not None and spec.loader is not None,'isolated module loader')
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module
    exec(compile(source,str(path),'exec',dont_inherit=True,optimize=sys.flags.optimize),module.__dict__)
    return module


def normalized_producer(result):
    """Only these two typed path rules remove time; every logical counter remains."""
    require(type(result) is dict and result.get('status') in ('EXACT','EMPTY'),'complete producer required')
    out=dict(result)
    require(type(result.get('resources')) is dict and 'wall_seconds' in result['resources'],'root time field')
    out['resources']={k:v for k,v in result['resources'].items() if k!='wall_seconds'}
    require(type(result.get('pieces')) is list,'complete pieces')
    pieces=[]
    for piece in result['pieces']:
        p=dict(piece);core=dict(piece['core'])
        require(type(core.get('resources')) is dict and 'wall_seconds' in core['resources'],'piece time field')
        core['resources']={k:v for k,v in core['resources'].items() if k!='wall_seconds'}
        p['core']=core;pieces.append(p)
    out['pieces']=pieces
    return out


def producer_digest(result):
    # Stream the full representation, not masks/counts; never retain a second
    # unbounded JSON string or write a semantic relation to disk.
    h=hashlib.sha256();total=0
    encoder=json.JSONEncoder(sort_keys=True,separators=(',',':'),allow_nan=False)
    for token in encoder.iterencode(normalized_producer(result)):
        data=token.encode('utf8')
        require(len(data)<=HASH_MAX-total,'semantic digest serialization cap')
        total+=len(data);h.update(data)
    require(total<HASH_MAX,'semantic digest newline cap');h.update(b'\n')
    return h.hexdigest()


def write_report(path,report):
    data=canonical(report)
    require(len(data)<=REPORT_MAX,'report byte cap')
    with Path(path).open('xb') as f:
        require(f.write(data)==len(data),'short report write');f.flush();os.fsync(f.fileno())
    fd=os.open(Path(path).parent,os.O_RDONLY|os.O_DIRECTORY)
    try:os.fsync(fd)
    finally:os.close(fd)


def bootstrap(freeze_pin):
    require(type(freeze_pin) is str and len(freeze_pin)==64,'freeze pin syntax')
    path=ROOT/'FREEZE.json'
    require(sha(path,REPORT_MAX)==freeze_pin,'external source freeze pin')
    frozen=read_json(path,REPORT_MAX)
    common_path=ROOT/'common.py'
    require(type(frozen) is dict and type(frozen.get('files')) is dict and str(common_path) in frozen['files'],'operational bootstrap source pin')
    common=load('k4_target_common_worker',common_path,frozen['files'][str(common_path)])
    return common,common.freeze_context(freeze_pin)


def convert_raw(raw,internal_id):
    """Primary raw-letter converter; no scientific module or input-file access.

    Called only by an approved actual worker or disclosed literal operational
    mock. Independent implementation lives in input_check.py, not here.
    """
    require(internal_id in ('v000','v001','v002'),'fixed structural role ID')
    text=raw['ciphertext']
    ranks=[ord(letter)-ord('A') for letter in text]
    require(len(ranks)==97 and all(type(v) is int and 0<=v<26 for v in ranks),'raw rank domain')
    contexts=[]
    for i in range(6,97):
        contexts.append([ranks[i-j] for j in range(1,7)])
    observations=[]
    for crib in raw['cribs']:
        first=crib['start']-1
        for offset,letter in enumerate(crib['plaintext']):
            i=first+offset
            observations.append([i-6,(ranks[i]-(ord(letter)-ord('A')))%26])
    require([row for row,_value in observations]==list(range(15,28))+list(range(57,68)),'fixed public row mapping')
    return dict(id=internal_id,contexts=contexts,observed=observations,sparsity=3,allowed_features=list(range(31)))


def require_status_pair(producer_status,reference_status):
    require((producer_status,reference_status) in (('EXACT','VERIFIED_EXACT'),('EMPTY','VERIFIED_EMPTY')),'complete matching producer/reference statuses')
    return True


def empty_invariants(result,verified):
    require(result['status']=='EMPTY' and verified['status']=='VERIFIED_EMPTY','EMPTY exact pairing')
    require(result['pieces']==[] and result['masks']==[[] for _ in range(91)] and result['witnesses']==[{} for _ in range(91)] and result['provenance']==[{} for _ in range(91)] and result['feasibility_witness'] is None,'complete empty relation shape')
    require(all(type(verified[name]) is int and verified[name]==0 for name in ('pieces_checked','canonical_functions','original_lifts','joint_predictions')),'zero EMPTY reference counts')
    return True


def semantic_summary(result,verified,interpretation):
    require_status_pair(result['status'],verified['status'])
    if result['status']=='EMPTY':empty_invariants(result,verified)
    else:
        require(all(type(verified[name]) is int and verified[name]>0 for name in ('pieces_checked','canonical_functions','original_lifts','joint_predictions')),'nonempty reference counts')
        require(type(result['feasibility_witness']) is dict,'common admitted feasibility witness')
    require(type(interpretation) is dict and set(interpretation)=={'classification','plaintext_masks','example_plaintext_tail','first_six_claimed'} and interpretation['first_six_claimed'] is False,'interpretation contract/no first-six claim')
    return dict(producer_nontime_sha256=producer_digest(result),masks=result['masks'],
        pieces=verified['pieces_checked'],canonical_functions=verified['canonical_functions'],
        original_lifts=verified['original_lifts'],joint_predictions=verified['joint_predictions'],
        feasibility_witness=result['feasibility_witness'],interpretation=interpretation)


def main(argv=None):
    parser=argparse.ArgumentParser(description='One frozen raw-format job; no implicit runs.')
    for flag in ('job','freeze-sha256','approval-sha256','output'):parser.add_argument('--'+flag,required=True)
    args=parser.parse_args(argv)
    common,freeze=bootstrap(args.freeze_sha256)
    stage,kind,key,inner,optimized=common.job_identity(args.job)
    require(kind=='science','worker science jobs only')
    common.require_child_bounds(stage)
    actual=list(sys.argv[1:] if argv is None else argv)
    spec=common.validate_child_command(freeze,args.job,args.freeze_sha256,args.approval_sha256,actual)
    require(args.output==spec['output'],'fixed output path')
    approval=common.read_authority(stage,freeze,args.freeze_sha256,args.approval_sha256)
    attempt_pin=common.require_attempt(args.job,args.freeze_sha256,args.approval_sha256)
    raw=common.read_authorized_raw(freeze,approval,args.job)
    input_spec=freeze['inputs'][key]
    check=common.load_pinned('k4_target_independent_input',ROOT/'input_check.py',freeze['files'][str(ROOT/'input_check.py')])
    instance=convert_raw(raw,inner)
    independently=check.convert_raw_independent(raw,inner)
    require(instance==independently,'independent raw conversion mismatch')
    expected=None
    if stage=='controls':
        expected=common.read_json(input_spec['expected_path'],common.RAW_MAX,input_spec['expected_sha256'])
        require(expected['raw_sha256']==input_spec['sha256'],'expected fixture raw binding')
        for converted in (instance,independently):
            require(converted['contexts']==expected['expected_contexts'] and
                converted['observed']==expected['expected_observed'],'pre-science known raw conversion gate')
    report=dict(schema=REPORT_SCHEMA,slot=args.job,stage=stage,input_role=key,case_id=inner,
        python_optimized=optimized,freeze_sha256=args.freeze_sha256,input_sha256=input_spec['sha256'],
        approval_sha256=args.approval_sha256,source_sha256=freeze['files'],status='INCOMPLETE_OR_FAILED',
        preflight=None,producer=None,verification=None,semantic_summary=None,control_check=None,
        resources=None,reason=None)
    wall_start=time.monotonic();cpu_start=time.process_time()
    producer_counters=None;reference_counters=None
    producer_attempted=False;reference_attempted=False
    try:
        reference=common.load_pinned('k4_target_reference',REFERENCE,REFERENCE_PIN)
        preflight=common.load_pinned('k4_target_preflight',PREFLIGHT,freeze['files'][str(PREFLIGHT)])
        checker=common.load_pinned('k4_target_certificate_checker',CHECKER,freeze['files'][str(CHECKER)])
        evidence=preflight.EvidenceBudget()
        pf=preflight.run(instance,Path(args.output).parent/'case.cert.jsonl',input_spec['sha256'],
            REFERENCE_PIN,args.freeze_sha256,reference,checker,evidence)
        report['preflight']=pf
        if pf['status']=='GATE_REJECTED_LOWER_BOUND':
            require(stage=='target','an actual interface control may not resource-gate')
            require(pf['certificate']['complete'] is True and pf['exact_W'] is None and type(pf['lower_bound']) is int and pf['lower_bound']>1000000,'complete resource gate')
            report['status']='CERTIFIED_RESOURCE_GATE'
        else:
            require(pf['status']=='WORKLOAD_ADMITTED' and pf['checked_supports']==4495 and type(pf['exact_W']) is int and 0<=pf['exact_W']<=1000000 and pf['certificate']['complete'] is True,'complete preflight required')
            common.load_pinned('affine_filter',AFFINE,AFFINE_PIN)
            engine=common.load_pinned('k4_target_decoder',ENGINE,ENGINE_PIN)
            observed=dict(instance['observed'])
            producer_attempted=True
            result=engine.decode(instance['contexts'],observed,3,list(range(31)),
                budget=engine.Budget(max_steps=2000000,max_pieces=40000,max_core_work=200000000,
                    max_core_solves=1000000,max_core_terms=100000,max_seconds=30.0))
            report['producer']={name:result[name] for name in ('status','resources','stats')}
            producer_counters={name:value for name,value in result['resources'].items() if name!='wall_seconds'}
            require(result['status'] in ('EXACT','EMPTY'),'producer did not complete')
            budget=reference.BudgetV3(max_fiber_points=1000000,max_lift_trials=4000000,
                max_solve_calls=100000,max_certificate_checks=200000,max_row_operations=5000000,
                max_work_units=500000000,max_witness_checks=1000000,max_output_records=5000000,max_seconds=45.0)
            reference_attempted=True
            verified=reference.verify_result_v3(instance['contexts'],observed,result,3,list(range(31)),
                budget=budget,expected_source_sha256=ENGINE_PIN)
            report['verification']=verified
            reference_counters={name:value for name,value in verified['resources'].items() if name!='wall_seconds'}
            require_status_pair(result['status'],verified['status'])
            require(verified['resources']['fiber_points']==pf['exact_W'],'complete reference charged fiber count')
            interpretation=check.interpret_verified(raw,instance,result,verified)
            report['semantic_summary']=semantic_summary(result,verified,interpretation)
            if expected is not None:
                require(check.verify_control_expectations(raw,instance,result,verified,interpretation,expected,pf) is True,'actual control expectations failed')
                report['control_check']=dict(status='PASS',expected_sha256=input_spec['expected_sha256'])
            report['status']=verified['status']
        common.freeze_context(args.freeze_sha256)
        require(common.require_attempt(args.job,args.freeze_sha256,args.approval_sha256)==attempt_pin,'parent attempt changed')
        require(common.sha(input_spec['path'],common.RAW_MAX)==input_spec['sha256'],'post-run raw input changed')
        require(common.sha(ROOT/'approvals'/(stage+'.json'),65536)==args.approval_sha256,'post-run authority changed')
        if expected is not None:require(common.sha(input_spec['expected_path'],common.RAW_MAX)==input_spec['expected_sha256'],'post-run control expectation changed')
    except BaseException as error:
        report['status']='INCOMPLETE_OR_FAILED';report['semantic_summary']=None;report['control_check']=None
        report['producer']=None;report['verification']=None
        report['reason']=type(error).__name__+': '+str(error)[:500]
    report['resources']=dict(worker_wall_seconds=time.monotonic()-wall_start,worker_cpu_seconds=time.process_time()-cpu_start,
        producer_counters=producer_counters,reference_counters=reference_counters,
        producer_attempted=producer_attempted,reference_attempted=reference_attempted)
    write_report(args.output,report)
    return 0 if report['status'] in ('VERIFIED_EXACT','VERIFIED_EMPTY','CERTIFIED_RESOURCE_GATE') else 1


if __name__=='__main__':
    sys.exit(main())

