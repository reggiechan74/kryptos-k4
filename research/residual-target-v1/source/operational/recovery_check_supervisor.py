"""Exactly two repair-only metadata slots. Never imports science or reads K4."""
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

ROOT=Path('/workspace/shared/k4-canonical-residual-recovered-target-v1')
CHECKS=Path('/workspace/shared/k4-residual-recovery-assessment-v1/checks')
MIB=1024*1024


def require(ok,message):
    if not ok:raise ValueError(message)


def load(name,path,pin):
    b=bounded_bytes(path,1024*1024);require(path.is_file() and not path.is_symlink() and len(b)<=MIB and hashlib.sha256(b).hexdigest()==pin,'bounded source identity')
    spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);sys.modules[name]=module
    exec(compile(b,str(path),'exec',dont_inherit=True,optimize=sys.flags.optimize),module.__dict__);return module


def bounded_bytes(path,limit):
    require(path.is_file() and not path.is_symlink() and path.stat().st_size<=limit,'bounded regular metadata input')
    with path.open('rb') as handle:data=handle.read(limit+1)
    require(len(data)<=limit,'metadata input grew')
    return data


def artifact_inventory(common,directory,complete):
    caps={'ATTEMPT.json':65536,'stdout.txt':MIB,'stderr.txt':MIB,'result.json':2*MIB}
    present={p.name for p in directory.iterdir()}
    require(present<=set(caps)|{'resource.json'},'only fixed check inventory paths')
    if complete:require(set(caps)<=present,'complete check artifacts')
    return [{'name':name,'bytes':(directory/name).stat().st_size,'sha256':common.sha(directory/name,cap)} for name,cap in caps.items() if name in present]


def authenticate_normal(common,freeze_pin):
    accepted=common.read_json(CHECKS/'normal-acceptance.json',65536)
    require(type(accepted) is dict and set(accepted)=={'schema','status','freeze_sha256','receipt_sha256','external_completion_sha256','review_sha256'} and accepted['schema']=='k4-recovery-check-normal-acceptance-v1' and accepted['status']=='ACCEPTED' and accepted['freeze_sha256']==freeze_pin and accepted['receipt_sha256']==common.sha(CHECKS/'normal'/'resource.json') and common.digest_string(accepted['external_completion_sha256']) and common.digest_string(accepted['review_sha256']),'independent normal receipt acceptance')
    prior=common.read_json(CHECKS/'normal'/'resource.json')
    require(prior['schema']=='k4-recovery-check-receipt-v1' and prior['mode']=='normal' and prior['freeze_sha256']==freeze_pin and prior['status']=='PASS' and prior['completed'] is True and prior['nominal_consumed']==12 and prior['inventory']==artifact_inventory(common,CHECKS/'normal',True),'immutable normal receipt and artifact inventory')
    require(prior['execution']['child_reaped'] is True and prior['execution']['exit_code']==0 and prior['execution']['failures']==[] and prior['result_sha256']==common.sha(CHECKS/'normal'/'result.json'),'normal guarded completion')
    ext=common.read_json(CHECKS/'normal-external-completion.json',65536,accepted['external_completion_sha256'])
    require(type(ext) is dict and set(ext)=={'schema','mode','freeze_sha256','receipt_sha256','completed','exit_code','tool_evidence'} and ext['schema']=='k4-recovery-check-external-completion-v1' and ext['mode']=='normal' and ext['freeze_sha256']==freeze_pin and ext['receipt_sha256']==accepted['receipt_sha256'] and ext['completed'] is True and type(ext['exit_code']) is int and ext['exit_code']==0 and type(ext['tool_evidence']) is str and 1<=len(ext['tool_evidence'])<=1000,'actual external normal completion')
    return common.sha(CHECKS/'normal-acceptance.json',65536)


def main():
    parser=argparse.ArgumentParser()
    for name in ('mode','freeze-sha256','approval-sha256'):parser.add_argument('--'+name,required=True)
    args=parser.parse_args();require(args.mode in ('normal','optimized'),'fixed mode')
    parent=os.getppid();require(parent>=1 and ctypes.CDLL(None).prctl(1,signal.SIGKILL,0,0,0)==0 and os.getppid()==parent,'supervisor parent-death guard before any source/authority read')
    resource.setrlimit(resource.RLIMIT_CPU,(3,8));resource.setrlimit(resource.RLIMIT_AS,(512*MIB,512*MIB))
    raw=bounded_bytes(ROOT/'FREEZE.json',2*1024*1024);require(len(raw)<=2*MIB and hashlib.sha256(raw).hexdigest()==args.freeze_sha256,'source freeze pin');freeze=json.loads(raw)
    common=load('k4_recovery_check_common',ROOT/'common.py',freeze['files'][str(ROOT/'common.py')]);common.freeze_context(args.freeze_sha256)
    catalog=common.read_json(ROOT/'RECOVERY-CHECK-COMMANDS.json',MIB,freeze['files'][str(ROOT/'RECOVERY-CHECK-COMMANDS.json')]);spec=catalog['jobs'][args.mode]
    require(sys.flags.isolated==1 and sys.dont_write_bytecode is True and sys.flags.optimize==0 and sys.orig_argv==common.expand(spec['launch_command'],args.freeze_sha256,args.approval_sha256) and Path.cwd()==ROOT,'exact metadata launcher')
    approval=common.read_json(CHECKS/'approval.json',65536,args.approval_sha256)
    require(approval=={'schema':'k4-recovery-check-approval-v1','status':'APPROVED_REPAIR_METADATA_ONLY','freeze_sha256':args.freeze_sha256,'jobs':['normal','optimized'],'commands_sha256':freeze['files'][str(ROOT/'RECOVERY-CHECK-COMMANDS.json')],'no_science':True},'parent repair-check authority')
    directory=CHECKS/args.mode;require(not directory.exists() and not directory.is_symlink(),'one use; never retry')
    if args.mode=='optimized':
        normal_commitment=authenticate_normal(common,args.freeze_sha256)
    else:require(not (CHECKS/'optimized').exists(),'normal precedes optimized')
    directory.mkdir();common.write_new(directory/'ATTEMPT.json',dict(schema='k4-recovery-check-attempt-v1',mode=args.mode,freeze_sha256=args.freeze_sha256,approval_sha256=args.approval_sha256,nominal_consumed=12))
    bounded=common.load_pinned('k4_recovery_metadata_collector',ROOT/'bounded_stage.py',freeze['files'][str(ROOT/'bounded_stage.py')])
    execution=None;status='INCOMPLETE';reason=None
    try:
        command=common.expand(spec['command'],args.freeze_sha256,args.approval_sha256)
        execution=bounded.run_bounded(command,str(ROOT),directory/'stdout.txt',directory/'stderr.txt',spec['limits'])
        require(execution['child_reaped'] is True and execution['exit_code']==0 and execution['failures']==[],'complete bounded check')
        report=common.read_json(directory/'result.json')
        require(report==dict(schema='k4-recovery-metadata-check-v1',mode=args.mode,freeze_sha256=args.freeze_sha256,approval_sha256=args.approval_sha256,status='PASS',case_count=16,cases=catalog['cases'],forbidden_effects={k:0 for k in ('science_imports','case_reads','child_launches','entropy_calls')},science_executed=False,target_input_read=False),'exact finite metadata report')
        if args.mode=='optimized':
            first=common.read_json(CHECKS/'normal'/'result.json');require({k:v for k,v in first.items() if k!='mode'}=={k:v for k,v in report.items() if k!='mode'},'normal/optimized checks agree')
        common.freeze_context(args.freeze_sha256)
        require(common.sha(CHECKS/'approval.json',65536)==args.approval_sha256,'repair approval changed during invocation')
        if args.mode=='optimized':require(authenticate_normal(common,args.freeze_sha256)==normal_commitment,'normal artifacts changed during optimized check')
        status='PASS'
    except BaseException as error:reason=type(error).__name__+': '+str(error)[:500]
    inventory=[]
    try:inventory=artifact_inventory(common,directory,status=='PASS')
    except BaseException as error:status='INCOMPLETE';reason='inventory: '+type(error).__name__+': '+str(error)[:300]
    if execution is not None:
        own=resource.getrusage(resource.RUSAGE_SELF);execution['supervisor_exclusive_cpu_sample']=own.ru_utime+own.ru_stime;execution['supervisor_peak_rss_kib']=own.ru_maxrss
        if execution['supervisor_exclusive_cpu_sample']>4:status='INCOMPLETE';reason='supervisor final exclusive CPU sample exceeds4'
    receipt=dict(schema='k4-recovery-check-receipt-v1',mode=args.mode,freeze_sha256=args.freeze_sha256,approval_sha256=args.approval_sha256,status=status,completed=status=='PASS',nominal_consumed=12,execution=execution,inventory=inventory,reason=reason,supervisor_final_write_tail_measured=False)
    if (directory/'result.json').is_file():receipt['result_sha256']=common.sha(directory/'result.json')
    common.write_new(directory/'resource.json',receipt)
    return 0 if status=='PASS' else 1


if __name__=='__main__':sys.exit(main())
