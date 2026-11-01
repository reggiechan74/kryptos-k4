"""Sixteen metadata-only recovery cases; no scientific or raw-input capability."""
import argparse
import builtins
import ctypes
import hashlib
import importlib.util
import io
import json
import math
import os
from pathlib import Path
import resource
import signal
import sys
import types

ROOT=Path('/workspace/shared/k4-canonical-residual-recovered-target-v1')
CHECKS=Path('/workspace/shared/k4-residual-recovery-assessment-v1/checks')
NAMES=('bridge_accept','bridge_charge','bridge_origin','public_not_authority',
       'grant_scope','grant_raw_identity','fixed_input_role','fixed_commands',
       'fresh_local_state','no_fake_history','next_job_order','normal_prefix',
       'inflight_stop','failure_stop','durable_attempt','exact_mode')


def require(ok,message):
    if not ok:raise ValueError(message)


def reject(fn):
    try:fn()
    except (ValueError,KeyError,TypeError):return
    raise ValueError('required rejection did not occur')


def canonical(value):
    return (json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()


def bounded_bytes(path,limit):
    require(path.is_file() and not path.is_symlink() and path.stat().st_size<=limit,'bounded regular metadata input')
    with path.open('rb') as handle:data=handle.read(limit+1)
    require(len(data)<=limit,'metadata input grew')
    return data


def main():
    parser=argparse.ArgumentParser()
    for name in ('mode','freeze-sha256','approval-sha256','output'):parser.add_argument('--'+name,required=True)
    args=parser.parse_args();require(args.mode in ('normal','optimized'),'fixed check mode')
    require(sys.flags.isolated==1 and sys.dont_write_bytecode is True and sys.flags.optimize==int(args.mode=='optimized'),'exact check mode')
    freeze_bytes=bounded_bytes(ROOT/'FREEZE.json',2*1024*1024);require(hashlib.sha256(freeze_bytes).hexdigest()==args.freeze_sha256,'freeze pin')
    freeze=json.loads(freeze_bytes)
    spec=json.loads(bounded_bytes(ROOT/'RECOVERY-CHECK-COMMANDS.json',1024*1024))['jobs'][args.mode]
    expanded=[{'${FREEZE_PIN}':args.freeze_sha256,'${APPROVAL_PIN}':args.approval_sha256}.get(x,x) for x in spec['command']]
    require(sys.orig_argv==expanded and args.output==spec['output'] and Path.cwd()==ROOT,'exact frozen metadata command')
    require(resource.getrlimit(resource.RLIMIT_CPU)==(7,8) and resource.getrlimit(resource.RLIMIT_AS)==(512*1024*1024,512*1024*1024),'finite metadata worker caps')
    guard=ctypes.c_int();require(ctypes.CDLL(None).prctl(2,ctypes.byref(guard),0,0,0)==0 and guard.value==signal.SIGKILL,'worker parent death guard')
    approval_bytes=bounded_bytes(CHECKS/'approval.json',65536);require(hashlib.sha256(approval_bytes).hexdigest()==args.approval_sha256,'metadata approval pin')
    approval=json.loads(approval_bytes)
    require(approval=={'schema':'k4-recovery-check-approval-v1','status':'APPROVED_REPAIR_METADATA_ONLY','freeze_sha256':args.freeze_sha256,'jobs':['normal','optimized'],'commands_sha256':freeze['files'][str(ROOT/'RECOVERY-CHECK-COMMANDS.json')],'no_science':True},'only metadata permission')
    sources={}
    for name in ('common.py','supervisor.py'):
        path=ROOT/name;b=bounded_bytes(path,1024*1024);require(len(b)<=1024*1024 and hashlib.sha256(b).hexdigest()==freeze['files'][str(path)],'operational source pin');sources[name]=b
    # Preload only stdlib dependencies. All operational first imports occur below
    # the rejecting I/O, entropy, process and scientific-import guards.
    original_import=builtins.__import__;original_open=builtins.open;original_os_open=os.open
    original_read=Path.read_bytes;original_text=Path.read_text;original_path_open=Path.open;original_io_open=io.open;original_urandom=os.urandom;original_getrandom=getattr(os,'getrandom',None)
    original_fork=os.fork;original_execve=os.execve;original_system=os.system
    counters={k:0 for k in ('science_imports','case_reads','child_launches','entropy_calls')}
    def blocked(kind):
        def inner(*_a,**_kw):counters[kind]+=1;raise RuntimeError('forbidden metadata effect: '+kind)
        return inner
    def guarded_import(name,*a,**kw):
        if any(x in name for x in ('residual_decoder','affine_filter','reference_v3','preflight_blind','checker_blind','input_check')):
            return blocked('science_imports')()
        return original_import(name,*a,**kw)
    builtins.open=blocked('case_reads');os.open=blocked('case_reads');Path.read_bytes=blocked('case_reads');Path.read_text=blocked('case_reads')
    Path.open=blocked('case_reads');io.open=blocked('case_reads')
    if original_getrandom is not None:os.getrandom=blocked('entropy_calls')
    os.urandom=blocked('entropy_calls');os.fork=blocked('child_launches');os.execve=blocked('child_launches');os.system=blocked('child_launches');builtins.__import__=guarded_import
    stubs={}
    for mod,names in (('random',('random','randint','randrange','choice','choices','seed','Random','SystemRandom')),('secrets',('token_bytes','token_hex','token_urlsafe','randbelow','choice')),('subprocess',('Popen','run','call','check_call','check_output'))):
        stubs[mod]=sys.modules.get(mod);stub=types.ModuleType(mod)
        for name in names:setattr(stub,name,blocked('child_launches' if mod=='subprocess' else 'entropy_calls'))
        sys.modules[mod]=stub
    passed=[]
    try:
        modules={}
        for name,source in sources.items():
            path=ROOT/name;module_name='k4_recovery_check_'+path.stem
            specmod=importlib.util.spec_from_file_location(module_name,path);module=importlib.util.module_from_spec(specmod);sys.modules[module_name]=module
            exec(compile(source,str(path),'exec',dont_inherit=True,optimize=sys.flags.optimize),module.__dict__);modules[name]=module
        common=modules['common.py'];supervisor=modules['supervisor.py'];pin=args.freeze_sha256;ap='a'*64
        def run(name,fn):fn();passed.append(name)
        bridge=dict(schema='k4-recovery-historical-acceptance-v1',status='ACCEPTED_PUBLISHED_HISTORY',freeze_sha256=pin,historical_evidence_sha256=freeze['historical_evidence_sha256'],published_commit='3e128d9a617af377516a0b9878a942b29bf2e3b8',published_tree='6503bb9ed6d1fc260ecd7af8fdc38174269974a2',historical_runtime_nominal=284,historical_overhead_committed=144,target_history='NO_TARGET_ATTEMPT_IN_KNOWN_HISTORY',parent_attestation_record='literal nonscientific test only')
        run('bridge_accept',lambda:require(common.validate_historical_bridge(bridge,freeze,pin) is True,'valid bridge'))
        run('bridge_charge',lambda:reject(lambda:common.validate_historical_bridge(dict(bridge,historical_runtime_nominal=0),freeze,pin)))
        run('bridge_origin',lambda:reject(lambda:common.validate_historical_bridge(dict(bridge,published_commit='0'*40),freeze,pin)))
        run('public_not_authority',lambda:reject(lambda:common.validate_historical_bridge({'schema':'k4-pretarget-public-administrative-derivative-v1','payload':bridge},freeze,pin)))
        grant=dict(schema='k4-residual-recovery-stage-approval-v1',status='APPROVED_FOR_TARGET',stage='target',freeze_sha256=pin,jobs=['K4-normal','K4-optimized'],input_sha256={'K4':common.TARGET_PIN},source_review_sha256='b'*64,prerequisite_acceptance_sha256='c'*64,publication_checkpoint_sha256='d'*64)
        run('grant_scope',lambda:reject(lambda:common.validate_approval_object(dict(grant,jobs=['K4-normal','K4-optimized','seal']),freeze,pin,'target')))
        run('grant_raw_identity',lambda:reject(lambda:common.validate_approval_object(dict(grant,input_sha256={'K4':'0'*64}),freeze,pin,'target')))
        run('fixed_input_role',lambda:require(common.validate_input_specs(freeze['inputs']) is None and set(freeze['inputs'])=={'K4'},'one role metadata only'))
        run('fixed_commands',lambda:require(all(common.expected_job(freeze,j)==freeze['jobs'][j] for j in common.JOBS),'all new exact commands'))
        state=dict(schema=supervisor.SCHEMA,freeze_sha256=pin,completed=[],in_flight=None,stopped=False,canceled=[],worker_cpu_actual=0.0,allocation_charged=0,certificate_bytes=0,certificate_files=0,artifact_bytes=0)
        run('fresh_local_state',lambda:require(supervisor.validate_state_shape(state,pin) is True,'new state'))
        run('no_fake_history',lambda:reject(lambda:supervisor.validate_state_shape(dict(state,allocation_charged=284),pin)))
        def next_case():
            require(supervisor.require_next_job(state,'K4-normal') is True,'normal first');reject(lambda:supervisor.require_next_job(state,'K4-optimized'))
        run('next_job_order',next_case)
        completed=dict(state,completed=[dict(job='K4-normal',status='VERIFIED_EMPTY',resource_sha256='b'*64,approval_sha256=ap)],allocation_charged=80)
        def normal_case():
            require(supervisor.validate_state_shape(completed,pin) is True and supervisor.require_next_job(completed,'K4-optimized') is True,'only optimized after normal');reject(lambda:supervisor.require_next_job(completed,'K4-normal'))
            wanted={'FREEZE.json','PUBLICATION-CHECKPOINT.json','HISTORICAL-BRIDGE.json','HISTORICAL-EVIDENCE.json','runs/state.json','runs/IN_FLIGHT.lock','approvals/target.json','approvals/seal.json','acceptance/TARGET.json'}
            wanted|={'parent-attempts/'+j+'.json' for j in common.JOBS}
            for j in common.JOBS[:2]:
                wanted.add('external/'+j+'.json');wanted|={'runs/'+j+'/'+n for n in ('stdout.txt','stderr.txt','result.json','resource.json','case.cert.jsonl')}
            seal=dict(schema='k4-residual-recovery-metadata-seal-v1',job='seal',freeze_sha256=pin,approval_sha256=ap,status='SEALED_METADATA',prior_completed_jobs=['K4-normal','K4-optimized'],artifacts={k:{'bytes':0,'sha256':'b'*64} for k in wanted},state_sha256='b'*64,source_sha256=freeze['files'],input_sha256={'K4':common.TARGET_PIN},allocation_charged_before_seal=160,worker_cpu_seconds_before_seal=0,seal_own_completion_pending=True,reason=None)
            require(supervisor.validate_seal_report(seal,freeze['jobs']['seal'],freeze,pin,ap)=='SEALED_METADATA','new two-target seal schema')
            reject(lambda:supervisor.validate_seal_report(dict(seal,allocation_charged_before_seal=444),freeze['jobs']['seal'],freeze,pin,ap))
            reject(lambda:supervisor.validate_seal_report(dict(seal,prior_completed_jobs=list(common.JOBS)),freeze['jobs']['seal'],freeze,pin,ap))
        run('normal_prefix',normal_case)
        reservation=dict(job='K4-normal',allocation_reserved=80,certificate_bytes_reserved=32*1024*1024,artifact_bytes_reserved=38*1024*1024,command=['literal'],approval_sha256=ap)
        pending=dict(state,in_flight=reservation)
        run('inflight_stop',lambda:reject(lambda:supervisor.require_next_job(pending,'K4-normal')))
        def fail_case():
            failed=supervisor.retain_failed_reservation(dict(pending),'K4-normal');require(failed['in_flight']==reservation and failed['canceled']==['K4-optimized','seal'],'retain and cancel');reject(lambda:supervisor.require_next_job(failed,'K4-optimized'))
        run('failure_stop',fail_case)
        durable=canonical(dict(schema='k4-durable-attempt-start-v1',run_id='k4-canonical-residual-recovered-target-v1',job='K4-normal',phase='ATTEMPT_START_CONSUMED',freeze_sha256=pin,approval_sha256=ap)).decode()
        attempt=dict(schema='k4-recovery-parent-attempt-v1',status='CONSUMED_FOR_ONE_ATTEMPT',job='K4-normal',freeze_sha256=pin,approval_sha256=ap,durable_parent_record=durable,durable_parent_record_sha256=hashlib.sha256(durable.encode()).hexdigest(),predecessor_receipt_sha256=None,predecessor_review_sha256=None)
        def attempt_case():
            require(common.validate_attempt_object(attempt,'K4-normal',pin,ap) is True,'normal attempt')
            opt_text=canonical(dict(schema='k4-durable-attempt-start-v1',run_id='k4-canonical-residual-recovered-target-v1',job='K4-optimized',phase='ATTEMPT_START_CONSUMED',freeze_sha256=pin,approval_sha256=ap)).decode()
            opt=dict(attempt,job='K4-optimized',durable_parent_record=opt_text,durable_parent_record_sha256=hashlib.sha256(opt_text.encode()).hexdigest(),predecessor_receipt_sha256='b'*64,predecessor_review_sha256='c'*64)
            require(common.validate_attempt_object(opt,'K4-optimized',pin,ap) is True,'valid independently accepted optimized predecessor')
            reject(lambda:common.validate_attempt_object(dict(opt,predecessor_review_sha256=None),'K4-optimized',pin,ap));reject(lambda:common.validate_attempt_object(dict(attempt,durable_parent_record=''),'K4-normal',pin,ap))
        run('durable_attempt',attempt_case)
        def mode_case():
            old=common.sys;fake=types.SimpleNamespace(flags=types.SimpleNamespace(isolated=1,optimize=2),dont_write_bytecode=True)
            try:common.sys=fake;reject(lambda:common.validate_child_command(freeze,'K4-optimized',pin,ap,[]))
            finally:common.sys=old
        run('exact_mode',mode_case)
        require(tuple(passed)==NAMES and all(v==0 for v in counters.values()),'all exact cases and no forbidden effects')
    finally:
        builtins.__import__=original_import;builtins.open=original_open;os.open=original_os_open;Path.read_bytes=original_read;Path.read_text=original_text;Path.open=original_path_open;io.open=original_io_open;os.urandom=original_urandom;os.fork=original_fork;os.execve=original_execve;os.system=original_system
        if original_getrandom is not None:os.getrandom=original_getrandom
        for name,previous in stubs.items():
            if previous is None:sys.modules.pop(name,None)
            else:sys.modules[name]=previous
    report=dict(schema='k4-recovery-metadata-check-v1',mode=args.mode,freeze_sha256=pin,approval_sha256=args.approval_sha256,status='PASS',case_count=16,cases=passed,forbidden_effects=counters,science_executed=False,target_input_read=False)
    output=Path(args.output);require(output.parent==CHECKS/args.mode and not output.exists(),'fixed new output')
    with output.open('xb') as handle:handle.write(canonical(report));handle.flush();os.fsync(handle.fileno())
    return 0


if __name__=='__main__':sys.exit(main())
