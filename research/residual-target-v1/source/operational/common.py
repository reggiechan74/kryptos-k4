"""Target-stage operational identities and permission guards; inert at import.

No raw source input is read by source verification. Raw input is a separately
authorized capability of one exact scheduled science job, never a source file.
All approval, acceptance and external-completion objects are parent-owned and
are deliberately not created by this module or any worker.
"""
import ctypes
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import resource
import signal
import sys

ROOT = Path('/workspace/shared/k4-canonical-residual-recovered-target-v1')
MIB = 1024 * 1024
JSON_MAX = 2 * MIB
RAW_MAX = 262144
LOG_MAX = MIB
CERT_MAX = 32 * MIB
STAGE_MAX = 128 * MIB
HISTORICAL_DISK_RESERVATION = 128 * MIB
FREEZE_SCHEMA = 'k4-residual-recovery-source-freeze-v1'
JOBS = ('K4-normal','K4-optimized','seal')
STAGE_JOBS = {'target':JOBS[:2], 'seal':JOBS[2:]}
INPUT_ROLES = {'K4':'v002'}
SCIENCE = {
    '/workspace/shared/k4-canonical-residual-recovered-target-v1/scientific/residual_decoder.py':'be050003b9a73c14a7f7dda44afeb160e0e847045d57ddfa4b9527bdc68f7d67',
    '/workspace/shared/k4-canonical-residual-recovered-target-v1/scientific/affine_filter.py':'1e19e9ad872d517487cfe7968a9f4b906756007d5e710be216807620f078c90d',
    '/workspace/shared/k4-canonical-residual-recovered-target-v1/scientific/reference_v3.py':'0730f8b0a26109919ba6eb558be18063d137ced233b397cd188dc261a13fe8f9',
    '/workspace/shared/k4-canonical-residual-recovered-target-v1/scientific/preflight_blind.py':'7f1929c0bd3c29a4e972f814e1fa1ade045a33e4b1cfc629e0b696c7b71dfe43',
    '/workspace/shared/k4-canonical-residual-recovered-target-v1/scientific/checker_blind.py':'065e3c29d2705c706b44a553bd9013b10c84751251145a4a683b940962ecc5c6',
    '/workspace/shared/k4-canonical-residual-recovered-target-v1/scientific/CAPS.json':'912461b0b97d4ad9738b830cf6130788e9295f9a92901a5af1664e9f3875a9d4'}
TARGET_PATH = str(ROOT/'data'/'k4.json')
TARGET_PIN = '08a1a84bd0dddf2449a2c7f67ee770d093ed47f6ad9a795630b77a2c8062f241'
LOCAL_SOURCES = ('common.py','bounded_stage.py','worker.py','supervisor.py',
                 'seal_results.py','input_check.py')


def require(condition,message):
    if not condition:
        raise ValueError(message)


def integer(value,maximum=None):
    return type(value) is int and value >= 0 and (maximum is None or value <= maximum)


def numeric(value):
    return (type(value) is int and value >= 0) or (type(value) is float and math.isfinite(value) and value >= 0)


def digest_string(value):
    return type(value) is str and len(value)==64 and all(c in '0123456789abcdef' for c in value)


def canonical(value):
    return (json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()


def unique_object(pairs):
    out={}
    for key,value in pairs:
        require(key not in out,'duplicate JSON key')
        out[key]=value
    return out


def sha(path,limit=JSON_MAX):
    path=Path(path)
    require(path.is_file() and not path.is_symlink(),'bounded regular hash input')
    size=path.stat().st_size
    require(integer(size,limit),'bounded hash size')
    h=hashlib.sha256();total=0
    with path.open('rb') as f:
        while True:
            data=f.read(min(MIB,limit+1))
            if not data:break
            require(len(data)<=limit-total,'hash input grew beyond cap')
            total+=len(data);h.update(data)
    require(total==size,'hash input size changed')
    return h.hexdigest()


def read_json(path,limit=JSON_MAX,pin=None):
    path=Path(path)
    require(path.is_file() and not path.is_symlink() and path.stat().st_size<=limit,'bounded regular JSON input')
    with path.open('rb') as f:data=f.read(limit+1)
    require(len(data)<=limit,'JSON input grew beyond cap')
    if pin is not None:
        require(digest_string(pin) and hashlib.sha256(data).hexdigest()==pin,'JSON input hash mismatch')
    return json.loads(data,object_pairs_hook=unique_object,
        parse_constant=lambda _x:(_ for _ in ()).throw(ValueError('nonfinite JSON')))


def fsync_dir(path):
    fd=os.open(str(path),os.O_RDONLY|os.O_DIRECTORY)
    try:os.fsync(fd)
    finally:os.close(fd)


def write_new(path,value,limit=JSON_MAX):
    path=Path(path);data=canonical(value)
    require(len(data)<=limit,'JSON output cap')
    require(path.parent.is_dir() and not path.parent.is_symlink(),'regular existing output parent')
    with path.open('xb') as f:
        require(f.write(data)==len(data),'short JSON write');f.flush();os.fsync(f.fileno())
    fsync_dir(path.parent)


def atomic(path,value):
    path=Path(path);temporary=path.with_name(path.name+'.tmp')
    write_new(temporary,value)
    os.replace(temporary,path);fsync_dir(path.parent)


def load_pinned(name,path,pin):
    path=Path(path)
    require(digest_string(pin) and path.is_file() and not path.is_symlink() and path.stat().st_size<=MIB,'bounded pinned module source')
    with path.open('rb') as handle:source=handle.read(MIB+1)
    require(len(source)<=MIB and hashlib.sha256(source).hexdigest()==pin,'pinned module source changed')
    spec=importlib.util.spec_from_file_location(name,path)
    require(spec is not None and spec.loader is not None,'module loader unavailable')
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module
    # Execute these authenticated bytes, never an importlib bytecode cache.
    exec(compile(source,str(path),'exec',dont_inherit=True,optimize=sys.flags.optimize),module.__dict__)
    return module


def stage_limits(stage):
    require(stage in STAGE_JOBS,'known stage')
    if stage in ('controls','target'):
        return dict(worker_cpu_soft=60,worker_cpu_hard=75,supervisor_cpu_soft=4,
            supervisor_cpu_hard=5,worker_address_space_bytes=1024*MIB,
            supervisor_address_space_bytes=256*MIB,wall_seconds=150,log_max_bytes=LOG_MAX)
    cpu=30 if stage=='mocks' else 5
    return dict(worker_cpu_soft=cpu,worker_cpu_hard=cpu+1,supervisor_cpu_soft=cpu,
        supervisor_cpu_hard=cpu+1,worker_address_space_bytes=512*MIB,
        supervisor_address_space_bytes=512*MIB,wall_seconds=120,log_max_bytes=LOG_MAX)


def job_identity(job):
    require(job in JOBS,'only fixed recovery job')
    stage='seal' if job=='seal' else 'target'
    kind='seal' if stage=='seal' else 'science'
    key='K4' if stage=='target' else None
    return stage,kind,key,None if key is None else 'v002',job.endswith('-optimized')


def expand(command,freeze_pin,approval_pin):
    require(digest_string(freeze_pin) and digest_string(approval_pin),'command commitment pins')
    require(type(command) is list and 1<=len(command)<=64 and all(type(v) is str and 0<len(v)<=4096 for v in command),'finite argv')
    mapping={'${FREEZE_PIN}':freeze_pin,'${APPROVAL_PIN}':approval_pin}
    require(command.count('${FREEZE_PIN}')==1 and command.count('${APPROVAL_PIN}')==1,'exact whole-token pins')
    require(all('${' not in v or v in mapping for v in command),'only declared whole-token pins')
    return [mapping.get(v,v) for v in command]


def expected_job(freeze,job):
    stage,kind,key,inner,optimized=job_identity(job)
    script=ROOT/('protocol_mock_tests.py' if kind=='mock' else 'seal_results.py' if kind=='seal' else 'worker.py')
    directory=ROOT/'runs'/job;output=directory/'result.json'
    flags=[freeze['python']['executable'],'-I','-B']+(['-O'] if optimized else [])
    args=['--job',job,'--freeze-sha256','${FREEZE_PIN}','--approval-sha256','${APPROVAL_PIN}']
    child=flags+[str(script)]+args+['--output',str(output)]
    launch=[freeze['python']['executable'],'-I','-B',str(ROOT/'supervisor.py')]+args
    status='PASS' if kind=='mock' else 'SEALED_METADATA' if kind=='seal' else 'VERIFIED_EXACT' if key=='positive' else 'VERIFIED_EMPTY' if key=='empty' else 'TARGET_CLASSIFIED'
    return dict(stage=stage,kind=kind,input_key=key,internal_id=inner,optimized=optimized,
        script=str(script),command=child,launch_command=launch,directory=str(directory),
        output=str(output),limits=stage_limits(stage),expected_status=status)


def validate_input_specs(inputs):
    require(type(inputs) is dict and set(inputs)==set(INPUT_ROLES),'one unchanged K4 identity')
    for role,inner in INPUT_ROLES.items():
        item=inputs[role]
        require(type(item) is dict and set(item)=={'path','sha256','internal_id','expected_path','expected_sha256'},'input metadata schema')
        require(item['internal_id']==inner and digest_string(item['sha256']),'input identity/pin')
        if role=='K4':
            require(item['path']==TARGET_PATH and item['sha256']==TARGET_PIN and item['expected_path'] is None and item['expected_sha256'] is None,'one fixed K4 source only')
        else:
            require(item['path']==str(ROOT/'fixtures'/(role+'.json')) and item['expected_path']==str(ROOT/'fixtures'/(role+'-expected.json')) and digest_string(item['expected_sha256']),'fixed disclosed fixture paths')


def verify_freeze_object(freeze):
    keys={'schema','files','python','inputs','jobs','mock_counts','resource_allocation_sha256','protocol_sha256','design_review_sha256','historical_evidence_sha256','recovery_design_review_sha256'}
    require(type(freeze) is dict and set(freeze)==keys and freeze['schema']==FREEZE_SCHEMA,'exact freeze schema')
    p=freeze['python']
    require(type(p) is dict and set(p)=={'executable','sha256','version'} and Path(p['executable']).is_absolute() and digest_string(p['sha256']) and type(p['version']) is str,'interpreter metadata')
    require(freeze['protocol_sha256']=='02db816f0510497952a057c246c3297847bb31dfa2c7046caf9483c95c65b170' and freeze['design_review_sha256']=='e3dd87e44a1db6d30be4fca25acea77343ec0772af1d912628ad94dc1bf275ef','reviewed protocol ancestry')
    require(digest_string(freeze['resource_allocation_sha256']) and digest_string(freeze['historical_evidence_sha256']) and freeze['recovery_design_review_sha256']=='668cddf83ba4fcaf1fbce1cd83ad93e399698022a0e146af3242a7120439fe75','recovery ancestry pins')
    validate_input_specs(freeze['inputs'])
    forbidden={v['path'] for v in freeze['inputs'].values()}|{v['expected_path'] for v in freeze['inputs'].values() if v['expected_path'] is not None}
    files=freeze['files']
    require(type(files) is dict and 12<=len(files)<=64,'finite frozen source graph')
    for path,pin in files.items():
        require(type(path) is str and Path(path).is_absolute() and path not in forbidden and digest_string(pin),'raw input excluded from source graph')
        local=Path(path).parent==ROOT and Path(path).name not in {'FREEZE.json','PUBLICATION-CHECKPOINT.json','HISTORICAL-BRIDGE.json'}
        require(local or SCIENCE.get(path)==pin,'frozen source namespace')
    require(all(files.get(path)==pin for path,pin in SCIENCE.items()),'immutable scientific paths/pins')
    require(all(str(ROOT/name) in files for name in LOCAL_SOURCES),'all operational sources frozen')
    require(files.get(str(ROOT/'RESOURCE-ALLOCATION.json'))==freeze['resource_allocation_sha256'],'resource file binding')
    require(files.get(str(ROOT/'HISTORICAL-EVIDENCE.json'))==freeze['historical_evidence_sha256'],'historical evidence binding')
    require(type(freeze['mock_counts']) is dict and bool(freeze['mock_counts']) and all(type(k) is str and integer(v) for k,v in freeze['mock_counts'].items()),'finite mock count dictionary')
    require(type(freeze['jobs']) is dict and set(freeze['jobs'])==set(JOBS),'exact three new jobs')
    for job in JOBS:require(freeze['jobs'][job]==expected_job(freeze,job),'exact frozen job specification: '+job)
    return freeze


def freeze_context(freeze_pin):
    require(digest_string(freeze_pin),'source freeze hash')
    freeze=read_json(ROOT/'FREEZE.json',JSON_MAX,freeze_pin)
    verify_freeze_object(freeze)
    require(freeze['python']=={'executable':str(Path(sys.executable).resolve()),'sha256':sha(Path(sys.executable).resolve(),64*MIB),'version':sys.version},'exact isolated interpreter')
    # Deliberately never open/hash any FREEZE.inputs member here.
    for path,pin in freeze['files'].items():require(sha(path,MIB)==pin,'frozen source bytes changed: '+path)
    return freeze


def validate_approval_object(approval,freeze,freeze_pin,stage):
    keys={'schema','status','stage','freeze_sha256','jobs','input_sha256','source_review_sha256','prerequisite_acceptance_sha256','publication_checkpoint_sha256'}
    require(stage in STAGE_JOBS and type(approval) is dict and set(approval)==keys,'exact approval schema')
    require(approval['schema']=='k4-residual-recovery-stage-approval-v1' and approval['status']=='APPROVED_FOR_'+stage.upper() and approval['stage']==stage and approval['freeze_sha256']==freeze_pin,'stage approval identity')
    require(approval['jobs']==list(STAGE_JOBS[stage]) and digest_string(approval['source_review_sha256']),'explicit exact-stage grant/review')
    roles=('positive','empty') if stage=='controls' else ('K4',) if stage=='target' else ()
    require(approval['input_sha256']=={r:freeze['inputs'][r]['sha256'] for r in roles},'exact stage input capability')
    require(approval['prerequisite_acceptance_sha256'] is None if stage=='mocks' else digest_string(approval['prerequisite_acceptance_sha256']),'stage prerequisite commitment')
    require(digest_string(approval['publication_checkpoint_sha256']) if stage=='target' else approval['publication_checkpoint_sha256'] is None,'target-only publication commitment')
    return approval


def validate_external_object(value,job,freeze_pin,receipt_pin):
    require(type(value) is dict and set(value)=={'schema','job','freeze_sha256','receipt_sha256','exit_code','completed','tool_evidence'},'external completion schema')
    require(value['schema']=='k4-residual-recovery-external-completion-v1' and value['job']==job and value['freeze_sha256']==freeze_pin and value['receipt_sha256']==receipt_pin,'external completion binding')
    require(type(value['exit_code']) is int and value['exit_code']==0 and value['completed'] is True and type(value['tool_evidence']) is str and 0<len(value['tool_evidence'])<=1000,'external clean completion')
    return True


def external_completion(job,freeze_pin,receipt_pin):
    path=ROOT/'external'/(job+'.json')
    value=read_json(path,65536)
    validate_external_object(value,job,freeze_pin,receipt_pin)
    return sha(path,65536)


def validate_acceptance_object(value,stage,freeze_pin):
    require(stage=='target','only local target predecessor stage')
    require(type(value) is dict and set(value)=={'schema','status','stage','freeze_sha256','jobs','receipts','review_sha256'},'acceptance schema')
    jobs=list(STAGE_JOBS[stage])
    require(value['schema']=='k4-residual-recovery-stage-acceptance-v1' and value['status']=='ACCEPTED_COMPLETE' and value['stage']==stage and value['freeze_sha256']==freeze_pin and value['jobs']==jobs and digest_string(value['review_sha256']),'independent accepted stage')
    require(type(value['receipts']) is dict and set(value['receipts'])==set(jobs),'accepted exact receipt set')
    for record in value['receipts'].values():
        require(type(record) is dict and set(record)=={'receipt_sha256','external_sha256'} and all(digest_string(v) for v in record.values()),'accepted receipt/external pins')
    return True


def validate_historical_bridge(value,freeze,freeze_pin):
    keys={'schema','status','freeze_sha256','historical_evidence_sha256','published_commit','published_tree','historical_runtime_nominal','historical_overhead_committed','target_history','parent_attestation_record'}
    require(type(value) is dict and set(value)==keys,'fresh historical bridge schema')
    require(value['schema']=='k4-recovery-historical-acceptance-v1' and value['status']=='ACCEPTED_PUBLISHED_HISTORY' and value['freeze_sha256']==freeze_pin and value['historical_evidence_sha256']==freeze['historical_evidence_sha256'],'fresh bridge ancestry')
    require(value['published_commit']=='3e128d9a617af377516a0b9878a942b29bf2e3b8' and value['published_tree']=='6503bb9ed6d1fc260ecd7af8fdc38174269974a2','published checkpoint identity')
    require(type(value['historical_runtime_nominal']) is int and value['historical_runtime_nominal']==284 and type(value['historical_overhead_committed']) is int and value['historical_overhead_committed']==144,'historical consumption never reset')
    require(value['target_history']=='NO_TARGET_ATTEMPT_IN_KNOWN_HISTORY' and type(value['parent_attestation_record']) is str and 1<=len(value['parent_attestation_record'])<=1000,'parent-held known-history attestation')
    return True


def read_authority(stage,freeze,freeze_pin,approval_pin):
    require(digest_string(approval_pin),'explicit approval pin')
    approval=read_json(ROOT/'approvals'/(stage+'.json'),65536,approval_pin)
    validate_approval_object(approval,freeze,freeze_pin,stage)
    if stage=='target':
        bridge=read_json(ROOT/'HISTORICAL-BRIDGE.json',65536,approval['prerequisite_acceptance_sha256'])
        validate_historical_bridge(bridge,freeze,freeze_pin)
        checkpoint=read_json(ROOT/'PUBLICATION-CHECKPOINT.json',65536,approval['publication_checkpoint_sha256'])
        keys={'schema','status','freeze_sha256','remote_commit','permission_record_sha256','ledger_sha256','responsibilities_sequence','main_denial_resolved'}
        require(type(checkpoint) is dict and set(checkpoint)==keys,'fresh publication checkpoint schema')
        require(checkpoint['schema']=='k4-recovery-publication-checkpoint-v1' and checkpoint['status']=='RECONCILED_AND_PUBLISHED' and checkpoint['freeze_sha256']==freeze_pin and checkpoint['remote_commit']=='3e128d9a617af377516a0b9878a942b29bf2e3b8' and checkpoint['main_denial_resolved'] is True,'publication gate closed')
        require(digest_string(checkpoint['permission_record_sha256']) and type(checkpoint['ledger_sha256']) is dict and set(checkpoint['ledger_sha256'])=={'HYPOTHESES.md','EXPERIMENTS.md','EXTERNAL-PRIOR-ART.md','tracker.json'} and all(digest_string(v) for v in checkpoint['ledger_sha256'].values()) and integer(checkpoint['responsibilities_sequence']) and checkpoint['responsibilities_sequence']>=66,'publication evidence')
        historical=read_json(ROOT/'HISTORICAL-EVIDENCE.json',JSON_MAX,freeze['historical_evidence_sha256'])
        require(checkpoint['ledger_sha256']==historical['published_ledger_sha256'] and checkpoint['remote_commit']==historical['published_commit']==bridge['published_commit'] and historical['published_tree']==bridge['published_tree'],'exact frozen published ledger/commit/tree ancestry')
    else:
        require(stage=='seal','known recovery stage')
        accepted=read_json(ROOT/'acceptance'/'TARGET.json',65536,approval['prerequisite_acceptance_sha256'])
        validate_acceptance_object(accepted,'target',freeze_pin)
        for job,record in accepted['receipts'].items():
            require(sha(ROOT/'runs'/job/'resource.json')==record['receipt_sha256'],'accepted local receipt changed')
            require(external_completion(job,freeze_pin,record['receipt_sha256'])==record['external_sha256'],'accepted local external completion changed')
    return approval


def validate_attempt_object(value,job,freeze_pin,approval_pin):
    keys={'schema','status','job','freeze_sha256','approval_sha256','durable_parent_record','durable_parent_record_sha256','predecessor_receipt_sha256','predecessor_review_sha256'}
    require(type(value) is dict and set(value)==keys and job in JOBS,'parent attempt schema')
    require(value['schema']=='k4-recovery-parent-attempt-v1' and value['status']=='CONSUMED_FOR_ONE_ATTEMPT' and value['job']==job and value['freeze_sha256']==freeze_pin and value['approval_sha256']==approval_pin,'parent attempt binding')
    require(type(value['durable_parent_record']) is str and 1<=len(value['durable_parent_record'])<=1000 and digest_string(value['durable_parent_record_sha256']) and hashlib.sha256(value['durable_parent_record'].encode()).hexdigest()==value['durable_parent_record_sha256'],'exact parent conversation record bytes/hash required; external persistence is parent-owned')
    durable=json.loads(value['durable_parent_record'],object_pairs_hook=unique_object)
    require(durable=={'schema':'k4-durable-attempt-start-v1','run_id':'k4-canonical-residual-recovered-target-v1','job':job,'phase':'ATTEMPT_START_CONSUMED','freeze_sha256':freeze_pin,'approval_sha256':approval_pin} and canonical(durable).decode()==value['durable_parent_record'],'exact canonical durable record binds run/job/freeze/grant')
    if job=='K4-normal':
        require(value['predecessor_receipt_sha256'] is None and value['predecessor_review_sha256'] is None,'normal has historical predecessor only')
    else:
        require(digest_string(value['predecessor_receipt_sha256']) and digest_string(value['predecessor_review_sha256']),'independently accepted preceding local job')
    return True


def require_attempt(job,freeze_pin,approval_pin):
    path=ROOT/'parent-attempts'/(job+'.json')
    value=read_json(path,65536)
    validate_attempt_object(value,job,freeze_pin,approval_pin)
    if job!='K4-normal':
        previous='K4-normal' if job=='K4-optimized' else 'K4-optimized'
        require(sha(ROOT/'runs'/previous/'resource.json')==value['predecessor_receipt_sha256'],'durable predecessor receipt binding')
    return sha(path,65536)


def validate_raw(raw,input_key):
    require(input_key in INPUT_ROLES,'scheduled raw identity')
    require(type(raw) is dict and set(raw)=={'ciphertext','length','indexing','cribs'},'raw source exact schema')
    require(type(raw['length']) is int and raw['length']==97 and raw['indexing']=='one-based inclusive','97-symbol indexing')
    ct=raw['ciphertext']
    require(type(ct) is str and len(ct)==97 and all('A'<=c<='Z' for c in ct),'strict AZ ciphertext')
    require(type(raw['cribs']) is list and len(raw['cribs'])==2,'two crib blocks')
    for crib,(start,end) in zip(raw['cribs'],((22,34),(64,74))):
        require(type(crib) is dict and set(crib)=={'start','end','plaintext'} and type(crib['start']) is int and type(crib['end']) is int and crib['start']==start and crib['end']==end,'fixed crib ranges')
        require(type(crib['plaintext']) is str and len(crib['plaintext'])==end-start+1 and all('A'<=c<='Z' for c in crib['plaintext']),'AZ crib lengths')
    if input_key=='K4':require([c['plaintext'] for c in raw['cribs']]==['EASTNORTHEAST','BERLINCLOCK'],'official K4 clues only')
    return raw


def read_authorized_raw(freeze,approval,job):
    stage,kind,key,inner,_optimized=job_identity(job)
    require(kind=='science' and approval['stage']==stage and job in approval['jobs'] and approval['input_sha256'].get(key)==freeze['inputs'][key]['sha256'],'raw input capability absent')
    spec=freeze['inputs'][key]
    raw=read_json(spec['path'],RAW_MAX,spec['sha256'])
    validate_raw(raw,key)
    return raw


def require_child_bounds(stage):
    limits=stage_limits(stage)
    require(resource.getrlimit(resource.RLIMIT_CPU)==(limits['worker_cpu_soft'],limits['worker_cpu_hard']),'worker CPU guard')
    memory=limits['worker_address_space_bytes']
    require(resource.getrlimit(resource.RLIMIT_AS)==(memory,memory),'worker memory guard')
    guard=ctypes.c_int()
    require(ctypes.CDLL(None).prctl(2,ctypes.byref(guard),0,0,0)==0 and guard.value==signal.SIGKILL,'worker parent-death guard')


def actual_command(script,args,optimized=False):
    return [str(Path(sys.executable).resolve()),'-I','-B']+(['-O'] if optimized else [])+[str(script)]+list(args)


def validate_child_command(freeze,job,freeze_pin,approval_pin,args):
    spec=freeze['jobs'][job]
    require(sys.flags.isolated==1 and sys.dont_write_bytecode is True and sys.flags.optimize==int(spec['optimized']),'isolated child interpreter flags')
    require(sys.orig_argv==expand(spec['command'],freeze_pin,approval_pin),'exact original interpreter/worker argv')
    require(actual_command(spec['script'],args,spec['optimized'])==expand(spec['command'],freeze_pin,approval_pin),'exact scheduled worker argv')
    require(str(Path.cwd())==str(ROOT),'exact working directory')
    return spec


def disk_bytes(freeze):
    """Bounded metadata-only inventory; never opens raw source inputs."""
    allowed={Path(path).relative_to(ROOT).as_posix():MIB for path in freeze['files']}
    allowed.update({'FREEZE.json':JSON_MAX,'PUBLICATION-CHECKPOINT.json':65536,
        'HISTORICAL-BRIDGE.json':65536,'runs/state.json':JSON_MAX,'runs/state.json.tmp':JSON_MAX,'runs/IN_FLIGHT.lock':JSON_MAX})
    for spec in freeze['inputs'].values():
        for key in ('path','expected_path'):
            if spec[key] is not None and ROOT in Path(spec[key]).parents:
                allowed[Path(spec[key]).relative_to(ROOT).as_posix()]=RAW_MAX
    for stage in STAGE_JOBS:allowed['approvals/'+stage+'.json']=65536
    for stage in ('TARGET',):allowed['acceptance/'+stage+'.json']=65536
    for job in JOBS:
        allowed['external/'+job+'.json']=65536
        allowed['parent-attempts/'+job+'.json']=65536
        for name,cap in (('stdout.txt',LOG_MAX),('stderr.txt',LOG_MAX),('result.json',JSON_MAX),('resource.json',JSON_MAX),('resource.json.tmp',JSON_MAX)):
            allowed['runs/'+job+'/'+name]=cap
        if job in JOBS[:2]:allowed['runs/'+job+'/case.cert.jsonl']=CERT_MAX
    allowed_dirs={'.'}
    for name in allowed:
        parent=Path(name).parent
        while parent!=Path('.'):
            allowed_dirs.add(parent.as_posix());parent=parent.parent
    total=0;files=0;directories=0
    for base,dirs,names in os.walk(ROOT,followlinks=False):
        directories+=1;require(directories<=64,'stage directory bound')
        require(Path(base).relative_to(ROOT).as_posix() in allowed_dirs,'frozen finite directory inventory')
        for name in dirs:require(not (Path(base)/name).is_symlink(),'stage symlink directory')
        for name in names:
            p=Path(base)/name;files+=1
            require(files<=256 and p.is_file() and not p.is_symlink(),'stage finite regular inventory')
            relative=p.relative_to(ROOT).as_posix()
            require(relative in allowed,'unexpected stage path')
            size=p.stat().st_size;require(size<=allowed[relative],'stage per-path file cap')
            require(size<=STAGE_MAX-total,'stage byte ceiling');total+=size
    return total
