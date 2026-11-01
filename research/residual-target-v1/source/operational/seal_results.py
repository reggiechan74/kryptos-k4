"""One explicitly granted metadata seal; no raw input or scientific imports.

The accepted two-target-job prefix must be complete with no scientific reserve before
the supervisor reserves this own metadata invocation. This report does not
claim its own external completion; that immutable receipt remains parent-owned.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT=Path('/workspace/shared/k4-canonical-residual-recovered-target-v1')
MIB=1024*1024


def require(condition,message):
    if not condition:raise ValueError(message)


def bootstrap(pin):
    path=ROOT/'FREEZE.json'
    require(type(pin) is str and len(pin)==64 and path.is_file() and not path.is_symlink() and path.stat().st_size<=2*MIB,'bounded external freeze identity')
    with path.open('rb') as f:data=f.read(2*MIB+1)
    require(len(data)<=2*MIB and hashlib.sha256(data).hexdigest()==pin,'source freeze bytes')
    def unique(pairs):
        out={}
        for key,value in pairs:require(key not in out,'duplicate JSON key');out[key]=value
        return out
    frozen=json.loads(data,object_pairs_hook=unique,parse_constant=lambda _x:(_ for _ in ()).throw(ValueError('nonfinite JSON')))
    path=ROOT/'common.py'
    require(path.is_file() and not path.is_symlink() and path.stat().st_size<=MIB,'bounded common source')
    with path.open('rb') as f:source=f.read(MIB+1)
    require(len(source)<=MIB and frozen['files'][str(path)]==hashlib.sha256(source).hexdigest(),'common source commitment')
    spec=importlib.util.spec_from_file_location('k4_target_common_sealer',path)
    require(spec is not None and spec.loader is not None,'common source loader')
    common=importlib.util.module_from_spec(spec);sys.modules[spec.name]=common
    exec(compile(source,str(path),'exec',dont_inherit=True,optimize=sys.flags.optimize),common.__dict__)
    return common,common.freeze_context(pin)


def snapshot(common,supervisor,freeze,freeze_pin,approval_pin):
    state_path=ROOT/'runs'/'state.json';state=common.read_json(state_path)
    supervisor.validate_state_shape(state,freeze_pin,True)
    require([r['job'] for r in state['completed']]==list(common.JOBS[:2]),'exact two-target-job completed prefix')
    require(state['in_flight'] is not None and state['in_flight']['job']=='seal' and state['in_flight']['allocation_reserved']==12 and state['in_flight']['approval_sha256']==approval_pin,'only own metadata reserve')
    marker=common.read_json(ROOT/'runs'/'IN_FLIGHT.lock')
    require(marker=={'schema':'k4-residual-one-use-lock-v1','freeze_sha256':freeze_pin,'reservation':state['in_flight']},'retained own marker/reservation binding')
    require(state['completed'][1]['status']==state['completed'][0]['status'] and state['completed'][1]['status'] in ('VERIFIED_EXACT','VERIFIED_EMPTY','CERTIFIED_RESOURCE_GATE'),'matching accepted scientific pair')
    artifacts,_=supervisor.inspect_completed(state,freeze,freeze_pin,common,False,True)
    # Reports and certificates are streamed to hashes, never parsed/evaluated.
    for name in ('FREEZE.json','PUBLICATION-CHECKPOINT.json','HISTORICAL-BRIDGE.json','HISTORICAL-EVIDENCE.json','runs/state.json','runs/IN_FLIGHT.lock'):
        path=ROOT/name;artifacts[name]={'bytes':path.stat().st_size,'sha256':common.sha(path,2*MIB)}
    for kind,names in (('approvals',('target','seal')),('acceptance',('TARGET',)),('parent-attempts',common.JOBS)):
        for name in names:
            path=ROOT/kind/(name+'.json');artifacts[kind+'/'+name+'.json']={'bytes':path.stat().st_size,'sha256':common.sha(path,65536)}
    return dict(schema='k4-residual-recovery-metadata-seal-v1',job='seal',freeze_sha256=freeze_pin,
        approval_sha256=approval_pin,status='SEALED_METADATA',prior_completed_jobs=list(common.JOBS[:2]),
        artifacts=artifacts,state_sha256=artifacts['runs/state.json']['sha256'],source_sha256=freeze['files'],
        input_sha256={k:v['sha256'] for k,v in freeze['inputs'].items()},
        allocation_charged_before_seal=state['allocation_charged'],worker_cpu_seconds_before_seal=state['worker_cpu_actual'],
        seal_own_completion_pending=True,reason=None)


def main(argv=None):
    parser=argparse.ArgumentParser(description='One metadata-only seal; no science replay.')
    for name in ('job','freeze-sha256','approval-sha256','output'):parser.add_argument('--'+name,required=True)
    args=parser.parse_args(argv)
    require(args.job=='seal','only fixed metadata job')
    common,freeze=bootstrap(args.freeze_sha256)
    common.require_child_bounds('seal')
    actual=list(sys.argv[1:] if argv is None else argv)
    spec=common.validate_child_command(freeze,args.job,args.freeze_sha256,args.approval_sha256,actual)
    require(args.output==spec['output'],'fixed metadata output')
    common.read_authority('seal',freeze,args.freeze_sha256,args.approval_sha256)
    attempt_pin=common.require_attempt('seal',args.freeze_sha256,args.approval_sha256)
    supervisor=common.load_pinned('k4_target_metadata_supervisor',ROOT/'supervisor.py',freeze['files'][str(ROOT/'supervisor.py')])
    report=snapshot(common,supervisor,freeze,args.freeze_sha256,args.approval_sha256)
    supervisor.validate_seal_report(report,spec,freeze,args.freeze_sha256,args.approval_sha256)
    common.freeze_context(args.freeze_sha256)
    common.read_authority('seal',freeze,args.freeze_sha256,args.approval_sha256)
    require(common.require_attempt('seal',args.freeze_sha256,args.approval_sha256)==attempt_pin,'seal attempt changed')
    require(snapshot(common,supervisor,freeze,args.freeze_sha256,args.approval_sha256)==report,'metadata postseal changed')
    common.write_new(args.output,report)
    return 0


if __name__=='__main__':
    sys.exit(main())
