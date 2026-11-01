"""Three new fixed one-use jobs after accepted historical prefix with distinct authority stages; inert at import.
Only metadata/source authentication precedes parent stage authorization. No raw
input is opened by a mock, sealer, help, import, or generic source verification.
The bounded process collector remains byte-identical to the validated study.
"""
import argparse
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
ROOT=Path('/workspace/shared/k4-canonical-residual-recovered-target-v1')
MIB=1024*1024
REPORT_MAX=2*MIB
LOG_MAX=MIB
CERT_MAX=32*MIB
STAGE_MAX=128*MIB
SCHEMA='k4-residual-recovered-target-supervisor-v1'
JOBS=('K4-normal','K4-optimized','seal')
ACCEPTED=('PASS','VERIFIED_EXACT','VERIFIED_EMPTY','CERTIFIED_RESOURCE_GATE','SEALED_METADATA')
REPORT_KEYS={'schema','slot','stage','input_role','case_id','python_optimized','freeze_sha256','input_sha256','approval_sha256','source_sha256','status','preflight','producer','verification','semantic_summary','control_check','resources','reason'}
ARTIFACT_CAPS={'stdout.txt':LOG_MAX,'stderr.txt':LOG_MAX,'result.json':REPORT_MAX,'case.cert.jsonl':CERT_MAX}


PREFLIGHT_COUNTERS = {'fiber_points','lift_trials','solve_calls','certificate_checks',
    'row_operations','work_units','witness_checks','output_records',
    'generated_row_operations','replayed_row_operations','supports',
    'generation_beta_candidates','audit_beta_candidates',
    'generation_parity_row_tests','audit_parity_row_tests'}


REFERENCE_COUNTERS = PREFLIGHT_COUNTERS - {'supports','generation_beta_candidates',
    'audit_beta_candidates','generation_parity_row_tests','audit_parity_row_tests'}


PRODUCER_COUNTERS = {'steps','core_work','core_solves','core_terms'}


PRODUCER_CAPS = {'steps':2000000,'core_work':200000000,'core_solves':1000000,'core_terms':100000}


REFERENCE_CAPS = {'fiber_points':1000000,'lift_trials':4000000,'solve_calls':100000,
    'certificate_checks':200000,'row_operations':5000000,'work_units':500000000,
    'witness_checks':1000000,'output_records':5000000,
    'generated_row_operations':5000000,'replayed_row_operations':5000000}


PREFLIGHT_CAPS = {'fiber_points':0,'lift_trials':0,'witness_checks':0,
    'supports':4495,'generation_beta_candidates':35264,'audit_beta_candidates':35264,
    'generation_parity_row_tests':846336,'audit_parity_row_tests':846336,
    'solve_calls':4495,'certificate_checks':8990,'row_operations':1500000,
    'work_units':50000000,'output_records':2000000,
    'generated_row_operations':1500000,'replayed_row_operations':1500000}


EXECUTION_KEYS = {'schema','command','cwd','limits','supervisor_pid','child_pid',
    'child_reaped','parent_death_guard','exit_code','wall_timeout','log_overflow',
    'collector_error','wall_seconds','child_user_cpu_seconds','child_system_cpu_seconds',
    'child_cpu_seconds','supervisor_exclusive_cpu_sample','supervisor_cpu_allocation_charged',
    'supervisor_final_write_tail_measured','child_peak_rss_kib','supervisor_peak_rss_kib',
    'log_bytes_reserved','log_bytes_read','logs','failures'}


PAIR_EXCLUSIONS = (('slot',),('python_optimized',),
    ('preflight','resources','wall_seconds'),('producer','resources','wall_seconds'),
    ('verification','resources','wall_seconds'),('resources','worker_wall_seconds'),
    ('resources','worker_cpu_seconds'))


def require(condition,message):
    if not condition:
        raise ValueError(message)


def integer(value,maximum=None):
    return type(value) is int and value>=0 and (maximum is None or value<=maximum)


def numeric(value):
    return ((type(value) is int and value>=0) or
            (type(value) is float and math.isfinite(value) and value>=0))


def digest_string(value):
    return type(value) is str and len(value)==64 and all(c in '0123456789abcdef' for c in value)


def canonical(value):
    return (json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()


def sha(path,limit=None):
    path=Path(path)
    require(path.is_file() and not path.is_symlink(),'regular hash input required')
    size=path.stat().st_size
    require(limit is None or size<=limit,'hash input exceeds cap')
    digest=hashlib.sha256();total=0
    with path.open('rb') as handle:
        while True:
            data=handle.read(MIB)
            if not data:break
            total+=len(data)
            require(limit is None or total<=limit,'hash input grew beyond cap')
            digest.update(data)
    require(total==size,'hash input changed size')
    return digest.hexdigest()


def _unique(pairs):
    out={}
    for key,value in pairs:
        require(key not in out,'duplicate JSON key');out[key]=value
    return out


def read_json(path,limit=REPORT_MAX):
    path=Path(path)
    require(path.is_file() and not path.is_symlink() and path.stat().st_size<=limit,'bounded regular JSON')
    with path.open('rb') as handle:data=handle.read(limit+1)
    require(len(data)<=limit,'JSON grew beyond cap')
    return json.loads(data,object_pairs_hook=_unique,
        parse_constant=lambda _x: (_ for _ in ()).throw(ValueError('nonfinite JSON')))


def _load(name,path,pin):
    path=Path(path)
    require(digest_string(pin) and path.is_file() and not path.is_symlink() and path.stat().st_size<=MIB,'bounded pinned bootstrap source')
    with path.open('rb') as handle:source=handle.read(MIB+1)
    require(len(source)<=MIB and hashlib.sha256(source).hexdigest()==pin,'authenticated bootstrap bytes')
    spec=importlib.util.spec_from_file_location(name,path)
    require(spec is not None and spec.loader is not None,'explicit module loader')
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module
    exec(compile(source,str(path),'exec',dont_inherit=True,optimize=sys.flags.optimize),module.__dict__)
    return module


def counter_map(value,names):
    require(type(value) is dict and set(value)==set(names)|{'wall_seconds'},'exact counter schema')
    require(all(integer(value[name]) for name in names),'nonnegative exact integer counters')
    require(numeric(value['wall_seconds']),'finite wall counter')


def completion_wall(value,maximum):
    """Conservative completed-receipt acceptance, not a physical wall guarantee."""
    require(type(maximum) is int and maximum>0 and numeric(value) and value<=maximum,
            'completed cooperative wall allowance exceeded')


def bounded_counters(value,caps,allow_none=False):
    if value is None and allow_none:return
    require(type(value) is dict and set(value)==set(caps),'exact non-time counters')
    require(all(integer(value[key],maximum) for key,maximum in caps.items()),'counter type/cap')


def checked_preflight(value):
    require(type(value) is dict and set(value)=={'status','checked_supports','lower_bound','exact_W','certificate','resources'},'completed preflight exact schema')
    require(integer(value['checked_supports'],4495) and integer(value['lower_bound']),'preflight prefix counters')
    claim=value['certificate']
    require(type(claim) is dict and set(claim)=={'name','bytes','sha256','complete'},'certificate claim schema')
    require(claim['name']=='case.cert.jsonl' and integer(claim['bytes'],CERT_MAX)
        and digest_string(claim['sha256']) and claim['complete'] is True,'completed certificate identity')
    counter_map(value['resources'],PREFLIGHT_COUNTERS)
    completion_wall(value['resources']['wall_seconds'],60)
    bounded_counters({key:value['resources'][key] for key in PREFLIGHT_COUNTERS},PREFLIGHT_CAPS)
    require(value['resources']['supports']==value['checked_supports'],'preflight support meter linkage')
    require(value['resources']['solve_calls']==value['checked_supports']
            and value['resources']['certificate_checks']==2*value['checked_supports'],'preflight solve/replay counts')
    require(value['resources']['generation_beta_candidates']==value['resources']['audit_beta_candidates']
            and value['resources']['generation_parity_row_tests']==value['resources']['audit_parity_row_tests'],
            'generation/audit traversal counts')
    require(value['resources']['row_operations']==value['resources']['generated_row_operations']+
            value['resources']['replayed_row_operations'],'row operation subtotals')
    require(value['resources']['fiber_points']==0 and value['resources']['lift_trials']==0
            and value['resources']['witness_checks']==0,'no preflight semantic work')
    if value['status']=='GATE_REJECTED_LOWER_BOUND':
        require(value['checked_supports']>0 and value['lower_bound']>1000000 and value['exact_W'] is None,'certified gate prefix')
    else:
        require(value['status']=='WORKLOAD_ADMITTED' and value['checked_supports']==4495
            and integer(value['exact_W'],1000000) and value['exact_W']==value['lower_bound'],'complete workload admission')
    return value['status']


def pair_projection(report):
    """Exactly frozen field exclusions; all other semantics and counters remain."""
    require(type(report) is dict and set(report)==REPORT_KEYS,'pair report schema')
    result=json.loads(canonical(report))
    for path in PAIR_EXCLUSIONS:
        container=result
        absent_parent=False
        for part in path[:-1]:
            if container is None:
                absent_parent=True;break
            require(type(container) is dict and part in container,'pair exclusion parent')
            container=container[part]
        if absent_parent or container is None:
            continue  # Producer/reference are null on a certified gate.
        require(type(container) is dict and path[-1] in container,'exact pair exclusion field')
        del container[path[-1]]
    return result


def compare_pair(normal,optimized):
    require(normal['slot'].endswith('-normal') and optimized['slot'].endswith('-optimized')
            and normal['case_id']==optimized['case_id'],'same ordered pair')
    require(normal['python_optimized'] is False and optimized['python_optimized'] is True,'strict mode booleans')
    require(pair_projection(normal)==pair_projection(optimized),'normal/optimized deterministic disagreement')
    return True


def diagnostic_inventory(jobdir):
    """Preserve bounded failed-file metadata; never certify this as complete."""
    entries=[];complete=True
    with os.scandir(jobdir) as iterator:
        for index,entry in enumerate(iterator):
            if index>=64:
                complete=False;break
            path=Path(entry.path)
            regular=entry.is_file(follow_symlinks=False)
            size=entry.stat(follow_symlinks=False).st_size if regular else 0
            pin=sha(path,CERT_MAX) if regular and size<=CERT_MAX else None
            entries.append(dict(name=entry.name,bytes=size,sha256=pin,
                classification='certificate_evidence' if entry.name=='case.cert.jsonl' else 'diagnostic_nonresult'))
            if not regular or size>CERT_MAX:complete=False
    return sorted(entries,key=lambda item:item['name']),complete


def prepare_supervisor_bounds():
    """Constant prelaunch envelope before parsing, source or authority reads.

    CPU soft 4 seconds and memory soft 256 MiB match the smallest supervisor;
    hard headroom only permits the frozen child fork. After argument parsing
    these soft limits become the exact job values, and run_bounded lowers the
    parent hard limits immediately after its one fork.
    """
    parent=os.getppid();require(type(parent) is int and parent>=1,'positive parent PID')
    libc=ctypes.CDLL(None,use_errno=True)
    if libc.prctl(1,signal.SIGKILL,0,0,0)!=0:raise OSError(ctypes.get_errno(),'PR_SET_PDEATHSIG')
    if os.getppid()!=parent:os.kill(os.getpid(),signal.SIGKILL)
    resource.setrlimit(resource.RLIMIT_CPU,(4,75))
    resource.setrlimit(resource.RLIMIT_AS,(256*MIB,1024*MIB))
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    resource.setrlimit(resource.RLIMIT_FSIZE,(CERT_MAX,CERT_MAX))


def bootstrap(freeze_pin):
    require(digest_string(freeze_pin) and sha(ROOT/'FREEZE.json',REPORT_MAX)==freeze_pin,'external source freeze pin')
    freeze=read_json(ROOT/'FREEZE.json')
    path=ROOT/'common.py'
    require(type(freeze) is dict and type(freeze.get('files')) is dict and freeze['files'].get(str(path))==sha(path,MIB),'bootstrap common source pin')
    common=_load('k4_target_common_supervisor',path,freeze['files'][str(path)])
    return common,common.freeze_context(freeze_pin)


def validate_report(report,spec,freeze,freeze_pin,approval_pin):
    """Strict metadata check of a complete, independently checked relation.

    It does not replace the immutable reference. EMPTY requires the reference's
    actual VERIFIED_EMPTY and zero relation; a resource gate is not EMPTY.
    """
    job=Path(spec['directory']).name
    require(type(report) is dict and set(report)==REPORT_KEYS,'exact report schema')
    require(report['schema']=='k4-residual-slot-report-v1' and report['slot']==job and
        report['stage']==spec['stage'] and report['input_role']==spec['input_key'] and
        report['case_id']==spec['internal_id'] and type(report['python_optimized']) is bool and
        report['python_optimized']==spec['optimized'],'report exact role/mode')
    require(report['freeze_sha256']==freeze_pin and report['approval_sha256']==approval_pin and
        report['input_sha256']==freeze['inputs'][spec['input_key']]['sha256'] and
        report['source_sha256']==freeze['files'],'report source/input/approval binding')
    resources=report['resources']
    require(type(resources) is dict and set(resources)=={'worker_wall_seconds','worker_cpu_seconds',
        'producer_counters','reference_counters','producer_attempted','reference_attempted'},'report resource schema')
    completion_wall(resources['worker_wall_seconds'],150)
    require(numeric(resources['worker_cpu_seconds']) and resources['worker_cpu_seconds']<=75,'worker subset CPU')
    require(type(resources['producer_attempted']) is bool and type(resources['reference_attempted']) is bool and
        (not resources['reference_attempted'] or resources['producer_attempted']),'attempt order')
    bounded_counters(resources['producer_counters'],PRODUCER_CAPS,True)
    bounded_counters(resources['reference_counters'],REFERENCE_CAPS,True)
    for name in ('producer','reference'):
        require(resources[name+'_attempted'] or resources[name+'_counters'] is None,'no uncalled stage counters')
    if report['status']=='INCOMPLETE_OR_FAILED':
        require(all(report[k] is None for k in ('producer','verification','semantic_summary','control_check')),'no incomplete result claims')
        require(type(report['reason']) is str and 0<len(report['reason'])<=2000,'bounded failure reason')
        return report['status']
    require(report['status'] in ('VERIFIED_EXACT','VERIFIED_EMPTY','CERTIFIED_RESOURCE_GATE') and report['reason'] is None,'completed report status')
    pf_status=checked_preflight(report['preflight'])
    if report['status']=='CERTIFIED_RESOURCE_GATE':
        require(spec['stage']=='target' and pf_status=='GATE_REJECTED_LOWER_BOUND','target-only certified resource gate')
        require(all(report[k] is None for k in ('producer','verification','semantic_summary','control_check')),'gate has no semantic claims')
        require(resources['producer_attempted'] is False and resources['reference_attempted'] is False and resources['producer_counters'] is None and resources['reference_counters'] is None,'gate cannot call semantics')
        return report['status']
    require(pf_status=='WORKLOAD_ADMITTED' and resources['producer_attempted'] and resources['reference_attempted'],'full preflight/producer/reference required')
    producer=report['producer'];verify=report['verification']
    require(type(producer) is dict and set(producer)=={'status','resources','stats'},'producer summary schema')
    wanted='EXACT' if report['status']=='VERIFIED_EXACT' else 'EMPTY'
    require(producer['status']==wanted,'matching producer status')
    counter_map(producer['resources'],PRODUCER_COUNTERS);completion_wall(producer['resources']['wall_seconds'],30)
    bounded_counters({k:producer['resources'][k] for k in PRODUCER_COUNTERS},PRODUCER_CAPS)
    require(resources['producer_counters']=={k:producer['resources'][k] for k in PRODUCER_COUNTERS},'producer counter linkage')
    require(type(producer['stats']) is dict and set(producer['stats'])=={'containers','beta_candidates','incompatible_beta','excluded_B','eligible_pieces','empty_pieces','feasible_pieces'} and all(integer(v) for v in producer['stats'].values()),'producer exact integer stats')
    require(type(verify) is dict and set(verify)=={'version','source_sha256','request_sha256','status','resources','pieces_checked','canonical_functions','original_lifts','joint_predictions','stats'},'exact reference schema')
    require(verify['version']=='independent-residual-reference-3' and verify['status']==report['status'] and
        verify['source_sha256']==freeze['files']['/workspace/shared/k4-canonical-residual-recovered-target-v1/scientific/reference_v3.py'] and digest_string(verify['request_sha256']),'complete reference identity/status')
    counter_map(verify['resources'],REFERENCE_COUNTERS);completion_wall(verify['resources']['wall_seconds'],45)
    bounded_counters({k:verify['resources'][k] for k in REFERENCE_COUNTERS},REFERENCE_CAPS)
    require(resources['reference_counters']=={k:verify['resources'][k] for k in REFERENCE_COUNTERS},'reference counter linkage')
    require(verify['resources']['row_operations']==verify['resources']['generated_row_operations']+verify['resources']['replayed_row_operations'] and verify['resources']['fiber_points']==report['preflight']['exact_W'],'complete reference workload and row totals')
    require(type(verify['stats']) is dict and set(verify['stats'])=={'supports','beta_candidates','eligible_beta','retained_points','legacy_ambient_points_equivalent'} and all(integer(v) for v in verify['stats'].values()),'reference exact integer stats')
    empty=wanted=='EMPTY'
    for key in ('pieces_checked','canonical_functions','original_lifts','joint_predictions'):
        require(integer(verify[key]) and (verify[key]==0 if empty else verify[key]>0),'nonvacuous exact relation counts')
    summary=report['semantic_summary']
    require(type(summary) is dict and set(summary)=={'producer_nontime_sha256','masks','pieces','canonical_functions','original_lifts','joint_predictions','feasibility_witness','interpretation'} and digest_string(summary['producer_nontime_sha256']),'full producer summary commitment')
    require(type(summary['masks']) is list and len(summary['masks'])==91,'91 scalar masks')
    for mask in summary['masks']:
        require(type(mask) is list and (len(mask)==0 if empty else 1<=len(mask)<=26) and all(integer(v,25) for v in mask) and mask==sorted(set(mask)),'canonical complete scalar masks')
    for a,b in (('pieces','pieces_checked'),('canonical_functions','canonical_functions'),('original_lifts','original_lifts'),('joint_predictions','joint_predictions')):
        require(integer(summary[a]) and summary[a]==verify[b],'reference/summary counts')
    require(summary['feasibility_witness'] is None if empty else type(summary['feasibility_witness']) is dict,'no vacuous witness')
    interpretation=summary['interpretation']
    require(type(interpretation) is dict and set(interpretation)=={'classification','plaintext_masks','example_plaintext_tail','first_six_claimed'} and interpretation['first_six_claimed'] is False,'no first-six/score interpretation fields')
    plain=interpretation['plaintext_masks']
    require(type(plain) is list and len(plain)==91,'91 plaintext masks')
    for original,mask in zip(summary['masks'],plain):
        require(type(mask) is list and len(mask)==len(original) and all(type(v) is str and len(v)==1 and 'A'<=v<='Z' for v in mask) and mask==sorted(set(mask)),'canonical plaintext mask shape')
    tail=interpretation['example_plaintext_tail']
    if empty:
        require(interpretation['classification']=='EMPTY' and tail is None,'empty is not a candidate or uniqueness')
    else:
        require(type(tail) is str and len(tail)==91 and all(v in mask for v,mask in zip(tail,plain)),'one independently verified common-law example')
        singleton=verify['joint_predictions']==1
        require(singleton==all(len(mask)==1 for mask in plain),'joint cardinality/marginal nonvacuity agreement')
        require(interpretation['classification']==('CONDITIONAL_SINGLETON_TAIL' if singleton else 'NONEMPTY_AMBIGUOUS'),'complete relation classification')
    if spec['stage']=='controls':
        require(report['status']==spec['expected_status'] and report['control_check']=={'status':'PASS','expected_sha256':freeze['inputs'][spec['input_key']]['expected_sha256']},'actual control exact expectation gate')
    else:require(report['control_check'] is None,'no target fixture bypass')
    return report['status']


def validate_mock_report(report,spec,freeze,freeze_pin,approval_pin):
    require(type(report) is dict and set(report)=={'schema','job','freeze_sha256','approval_sha256','python_optimized','status','counts','actual_forbidden_calls','reason'},'exact mock report schema')
    require(report['schema']=='k4-residual-operational-mock-report-v1' and report['job']==Path(spec['directory']).name and report['freeze_sha256']==freeze_pin and report['approval_sha256']==approval_pin and type(report['python_optimized']) is bool and report['python_optimized']==spec['optimized'],'mock identity')
    require(report['status']=='PASS' and report['reason'] is None and report['counts']==freeze['mock_counts'],'finite mock completion/counts')
    require(report['actual_forbidden_calls']=={k:0 for k in ('science_imports','science_calls','case_reads','child_launches','entropy_calls')},'no actual forbidden mock effects')
    return 'PASS'


def validate_seal_report(report,spec,freeze,freeze_pin,approval_pin):
    keys={'schema','job','freeze_sha256','approval_sha256','status','prior_completed_jobs','artifacts','state_sha256','source_sha256','input_sha256','allocation_charged_before_seal','worker_cpu_seconds_before_seal','seal_own_completion_pending','reason'}
    require(type(report) is dict and set(report)==keys and report['schema']=='k4-residual-recovery-metadata-seal-v1','metadata seal schema')
    require(report['job']=='seal' and report['freeze_sha256']==freeze_pin and report['approval_sha256']==approval_pin and report['status']=='SEALED_METADATA' and report['reason'] is None,'metadata seal identity/status')
    require(report['prior_completed_jobs']==list(JOBS[:2]) and report['seal_own_completion_pending'] is True,'two prior finalized target slots; own outer receipt pending')
    require(report['source_sha256']==freeze['files'] and report['input_sha256']=={k:v['sha256'] for k,v in freeze['inputs'].items()} and digest_string(report['state_sha256']),'seal metadata pins only')
    require(report['allocation_charged_before_seal']==160 and numeric(report['worker_cpu_seconds_before_seal']),'seal allocation before own 12-second slot')
    wanted={'FREEZE.json','PUBLICATION-CHECKPOINT.json','HISTORICAL-BRIDGE.json','HISTORICAL-EVIDENCE.json','runs/state.json','runs/IN_FLIGHT.lock'}
    wanted|={'approvals/'+name+'.json' for name in ('target','seal')}
    wanted|={'acceptance/'+name+'.json' for name in ('TARGET',)}
    wanted|={'parent-attempts/'+job+'.json' for job in JOBS}
    for job in JOBS[:2]:
        wanted.add('external/'+job+'.json')
        names={'stdout.txt','stderr.txt','result.json','resource.json'}
        if job in JOBS[:2]:names.add('case.cert.jsonl')
        wanted|={'runs/'+job+'/'+name for name in names}
    require(type(report['artifacts']) is dict and set(report['artifacts'])==wanted,'complete finite seal inventory')
    for path,record in report['artifacts'].items():
        require(type(path) is str and type(record) is dict and set(record)=={'bytes','sha256'} and integer(record['bytes'],CERT_MAX) and digest_string(record['sha256']),'seal artifact record')
    require(report['state_sha256']==report['artifacts']['runs/state.json']['sha256'],'seal state binding')
    return 'SEALED_METADATA'


def validate_execution(value,command,cwd,limits):
    require(type(value) is dict and set(value)==EXECUTION_KEYS and value['schema']=='k4-residual-bounded-stage-v1','bounded execution schema')
    require(value['command']==command and value['cwd']==cwd and value['limits']==limits,'execution invocation/limits')
    require(type(value['exit_code']) is int and value['exit_code']==0 and value['child_reaped'] is True and value['parent_death_guard'] is True,'clean guarded reaped child')
    require(value['wall_timeout'] is False and value['log_overflow'] is False and value['collector_error'] is None and value['failures']==[],'no execution failures')
    completion_wall(value['wall_seconds'],limits['wall_seconds'])
    for k in ('child_user_cpu_seconds','child_system_cpu_seconds','child_cpu_seconds','supervisor_exclusive_cpu_sample'):require(numeric(value[k]),'finite CPU components')
    require(abs(value['child_user_cpu_seconds']+value['child_system_cpu_seconds']-value['child_cpu_seconds'])<=1e-8,'CPU sum')
    require(value['child_cpu_seconds']<=limits['worker_cpu_hard'] and value['supervisor_exclusive_cpu_sample']<=limits['supervisor_cpu_hard'],'CPU ceilings')
    require(type(value['supervisor_cpu_allocation_charged']) is int and value['supervisor_cpu_allocation_charged']==limits['supervisor_cpu_hard'] and value['supervisor_final_write_tail_measured'] is False,'charged supervisor tail not claimed measured')
    require(all(type(value[k]) is int and value[k]>=1 for k in ('supervisor_pid','child_pid')) and value['supervisor_pid']!=value['child_pid'],'distinct positive PIDs')
    require(all(integer(value[k]) for k in ('child_peak_rss_kib','supervisor_peak_rss_kib')),'RSS counts')
    for k in ('log_bytes_reserved','log_bytes_read'):
        require(type(value[k]) is list and len(value[k])==2 and all(integer(v) for v in value[k]),'log integer counts')
    require(all(value['log_bytes_reserved'][i]==value['log_bytes_read'][i]<=LOG_MAX for i in (0,1)),'bounded exact log predebit')
    require(type(value['logs']) is list and len(value['logs'])==2,'two logs')
    jobdir=Path(command[-1]).parent
    for i,name in enumerate(('stdout.txt','stderr.txt')):
        item=value['logs'][i]
        require(type(item) is dict and set(item)=={'path','bytes','sha256'} and item['path']==str(jobdir/name) and integer(item['bytes'],LOG_MAX) and item['bytes']==value['log_bytes_reserved'][i] and digest_string(item['sha256']),'exact bounded log record')
    return True


def allocation(job):
    require(job in JOBS,'fixed allocation job')
    return 62 if job.startswith('mock-') else 12 if job=='seal' else 80


def validate_state_shape(state,freeze_pin,allow_in_flight=False):
    keys={'schema','freeze_sha256','completed','in_flight','stopped','canceled','worker_cpu_actual','allocation_charged','certificate_bytes','certificate_files','artifact_bytes'}
    require(type(state) is dict and set(state)==keys and state['schema']==SCHEMA and state['freeze_sha256']==freeze_pin,'state schema/source identity')
    require(type(state['completed']) is list and len(state['completed'])<=3,'finite completed prefix')
    for index,record in enumerate(state['completed']):
        require(type(record) is dict and set(record)=={'job','status','resource_sha256','approval_sha256'} and record['job']==JOBS[index] and record['status'] in ACCEPTED and digest_string(record['resource_sha256']) and digest_string(record['approval_sha256']),'accepted exact prefix record')
    require(state['stopped'] is False and state['canceled']==[],'stopped state cannot continue')
    require(numeric(state['worker_cpu_actual']) and integer(state['allocation_charged'],172) and state['allocation_charged']==sum(allocation(r['job']) for r in state['completed']),'allocation exact prefix')
    require(integer(state['certificate_bytes'],2*CERT_MAX) and integer(state['certificate_files'],2) and integer(state['artifact_bytes'],STAGE_MAX),'state finite evidence totals')
    if not allow_in_flight:require(state['in_flight'] is None,'no unresolved reserved invocation')
    elif state['in_flight'] is not None:
        item=state['in_flight']
        require(type(item) is dict and set(item)=={'job','allocation_reserved','certificate_bytes_reserved','artifact_bytes_reserved','command','approval_sha256'} and len(state['completed'])<3 and item['job']==JOBS[len(state['completed'])] and item['allocation_reserved']==allocation(item['job']) and digest_string(item['approval_sha256']),'one fixed in-flight reservation')
        require(item['certificate_bytes_reserved']==(CERT_MAX if item['job'] in JOBS[:2] else 0) and item['artifact_bytes_reserved']==(38*MIB if item['job'] in JOBS[:2] else 6*MIB),'fixed evidence reservation')
        require(type(item['command']) is list and 1<=len(item['command'])<=64 and all(type(v) is str and 0<len(v)<=4096 for v in item['command']),'finite reserved command')
    return True


def require_next_job(state,job):
    require(state['stopped'] is False and state['in_flight'] is None and state['canceled']==[] and len(state['completed'])<3 and job==JOBS[len(state['completed'])],'only next unused job; no retry')
    return True


def retain_failed_reservation(state,job):
    """An authorized attempt cannot become reusable when no child was started."""
    require(job in JOBS and type(state['in_flight']) is dict and state['in_flight'].get('job')==job,'failed attempt retains its own reserve')
    state['stopped']=True;state['canceled']=list(JOBS[JOBS.index(job)+1:])
    return state


def artifact_inventory(jobdir,kind,completed=False):
    jobdir=Path(jobdir);require(jobdir.is_dir() and not jobdir.is_symlink(),'regular job directory')
    wanted=set(ARTIFACT_CAPS) if kind=='science' else set(ARTIFACT_CAPS)-{'case.cert.jsonl'}
    entries=[]
    for path in sorted(jobdir.iterdir()):
        if path.name in ('resource.json','resource.json.tmp'):
            require(path.is_file() and not path.is_symlink() and path.stat().st_size<=REPORT_MAX,'bounded receipt/partial')
            if completed:require(path.name=='resource.json','no completed receipt partial')
            continue
        require(path.name in wanted,'unexpected job artifact')
        cap=ARTIFACT_CAPS[path.name]
        require(path.is_file() and not path.is_symlink() and path.stat().st_size<=cap,'bounded regular artifact')
        entries.append(dict(name=path.name,bytes=path.stat().st_size,sha256=sha(path,cap),classification='certificate_evidence' if path.name=='case.cert.jsonl' else 'result' if path.name=='result.json' else 'diagnostic_nonresult'))
    if completed:require({v['name'] for v in entries}==wanted,'complete artifact set')
    return entries


def validate_receipt(receipt,spec,freeze,freeze_pin,approval_pin,common):
    keys={'schema','job','stage','freeze_sha256','approval_sha256','status','launch_attempted','execution','inventory','certificate_bytes','certificate_files','artifact_bytes','mode_pair_checked','failures','parent_attempt_sha256'}
    job=Path(spec['directory']).name
    require(type(receipt) is dict and set(receipt)==keys and receipt['schema']==SCHEMA and receipt['job']==job and receipt['stage']==spec['stage'] and receipt['freeze_sha256']==freeze_pin and receipt['approval_sha256']==approval_pin,'receipt identity/schema')
    require(digest_string(receipt['parent_attempt_sha256']) and common.require_attempt(job,freeze_pin,approval_pin)==receipt['parent_attempt_sha256'],'parent durable attempt binding')
    require(receipt['status'] in ACCEPTED and receipt['failures']==[] and receipt['launch_attempted'] is True and type(receipt['mode_pair_checked']) is bool and receipt['mode_pair_checked']==(job=='K4-optimized'),'accepted receipt/pair status')
    if spec['kind']=='mock':require(receipt['status']=='PASS','mock receipt status')
    elif spec['kind']=='seal':require(receipt['status']=='SEALED_METADATA','seal receipt status')
    elif spec['stage']=='controls':require(receipt['status']==spec['expected_status'],'control receipt status')
    else:require(receipt['status'] in ('VERIFIED_EXACT','VERIFIED_EMPTY','CERTIFIED_RESOURCE_GATE'),'target receipt status')
    validate_execution(receipt['execution'],common.expand(spec['command'],freeze_pin,approval_pin),str(ROOT),spec['limits'])
    inventory=receipt['inventory'];wanted=set(ARTIFACT_CAPS) if spec['kind']=='science' else set(ARTIFACT_CAPS)-{'case.cert.jsonl'}
    require(type(inventory) is list and len(inventory)==len(wanted),'complete receipt inventory')
    seen=set()
    for item in inventory:
        require(type(item) is dict and set(item)=={'name','bytes','sha256','classification'},'inventory record schema')
        name=item['name'];require(name in wanted and name not in seen and integer(item['bytes'],ARTIFACT_CAPS[name]) and digest_string(item['sha256']),'bounded unique artifact')
        seen.add(name);require(item['classification']==('certificate_evidence' if name=='case.cert.jsonl' else 'result' if name=='result.json' else 'diagnostic_nonresult'),'artifact class')
    require(seen==wanted,'full artifact inventory')
    cert=[v for v in inventory if v['name']=='case.cert.jsonl']
    require(type(receipt['certificate_files']) is int and receipt['certificate_files']==len(cert) and type(receipt['certificate_bytes']) is int and receipt['certificate_bytes']==sum(v['bytes'] for v in cert) and type(receipt['artifact_bytes']) is int and receipt['artifact_bytes']==sum(v['bytes'] for v in inventory),'receipt evidence totals')
    byname={v['name']:v for v in inventory}
    for log in receipt['execution']['logs']:
        item=byname[Path(log['path']).name]
        require(log['bytes']==item['bytes'] and log['sha256']==item['sha256'],'collector/inventory log pins')
    return True


def report_status(report,spec,freeze,freeze_pin,approval_pin):
    if spec['kind']=='science':return validate_report(report,spec,freeze,freeze_pin,approval_pin)
    if spec['kind']=='mock':return validate_mock_report(report,spec,freeze,freeze_pin,approval_pin)
    return validate_seal_report(report,spec,freeze,freeze_pin,approval_pin)


def inspect_completed(state,freeze,freeze_pin,common,validate_reports=True,allow_in_flight=False):
    """Read-only prior prefix. Metadata sealer selects no report parsing."""
    validate_state_shape(state,freeze_pin,allow_in_flight)
    if state['in_flight'] is not None:
        pending=state['in_flight'];spec=freeze['jobs'][pending['job']]
        require(pending['command']==common.expand(spec['command'],freeze_pin,pending['approval_sha256']),'in-flight exact frozen command')
    reports={};artifacts={};cpu=0.0;certbytes=0;certfiles=0;artifactbytes=0
    for record in state['completed']:
        job=record['job'];spec=freeze['jobs'][job];directory=Path(spec['directory'])
        pin=record['resource_sha256'];approval_pin=record['approval_sha256']
        require(sha(directory/'resource.json',REPORT_MAX)==pin,'immutable prior receipt')
        receipt=read_json(directory/'resource.json')
        validate_receipt(receipt,spec,freeze,freeze_pin,approval_pin,common)
        common.read_authority(spec['stage'],freeze,freeze_pin,approval_pin)
        require(receipt['status']==record['status'],'state/receipt status')
        inventory=artifact_inventory(directory,spec['kind'],True)
        require(inventory==receipt['inventory'],'immutable prior artifacts')
        external_pin=common.external_completion(job,freeze_pin,pin)
        artifacts['external/'+job+'.json']={'bytes':(ROOT/'external'/(job+'.json')).stat().st_size,'sha256':external_pin}
        if validate_reports:
            report=read_json(directory/'result.json');require(report_status(report,spec,freeze,freeze_pin,approval_pin)==receipt['status'],'report/receipt status')
            if spec['kind']=='science':
                actual=next(item for item in inventory if item['name']=='case.cert.jsonl');claim=report['preflight']['certificate']
                require(claim['bytes']==actual['bytes'] and claim['sha256']==actual['sha256'],'certificate/report binding')
            reports[job]=report
            if job=='K4-optimized':compare_pair(reports['K4-normal'],report)
        cpu+=receipt['execution']['child_cpu_seconds'];certbytes+=receipt['certificate_bytes'];certfiles+=receipt['certificate_files']
        artifactbytes+=receipt['artifact_bytes']+(directory/'resource.json').stat().st_size
        for item in inventory:artifacts['runs/'+job+'/'+item['name']]={'bytes':item['bytes'],'sha256':item['sha256']}
        artifacts['runs/'+job+'/resource.json']={'bytes':(directory/'resource.json').stat().st_size,'sha256':pin}
    require(abs(cpu-state['worker_cpu_actual'])<=1e-8 and certbytes==state['certificate_bytes'] and certfiles==state['certificate_files'] and artifactbytes==state['artifact_bytes'],'state resource/byte reconciliation')
    return artifacts,reports


def main(argv=None):
    parser=argparse.ArgumentParser(description='One explicitly granted frozen job; no implicit runs.')
    for name in ('job','freeze-sha256','approval-sha256'):parser.add_argument('--'+name,required=True)
    args=parser.parse_args(argv)  # --help exits before guards, files or processes.
    require(args.job in JOBS,'fixed job only')
    prepare_supervisor_bounds()
    if args.job.startswith('mock-'):
        resource.setrlimit(resource.RLIMIT_CPU,(30,75));resource.setrlimit(resource.RLIMIT_AS,(512*MIB,1024*MIB))
    elif args.job=='seal':
        resource.setrlimit(resource.RLIMIT_CPU,(5,75));resource.setrlimit(resource.RLIMIT_AS,(512*MIB,1024*MIB))
    common,freeze=bootstrap(args.freeze_sha256);spec=freeze['jobs'][args.job]
    actual=list(sys.argv[1:] if argv is None else argv)
    require(sys.flags.isolated==1 and sys.dont_write_bytecode is True and sys.flags.optimize==0 and
        sys.orig_argv==common.expand(spec['launch_command'],args.freeze_sha256,args.approval_sha256) and
        common.actual_command(ROOT/'supervisor.py',actual)==common.expand(spec['launch_command'],args.freeze_sha256,args.approval_sha256) and Path.cwd()==ROOT,'exact isolated supervisor command')
    common.read_authority(spec['stage'],freeze,args.freeze_sha256,args.approval_sha256)
    parent_attempt_pin=common.require_attempt(args.job,args.freeze_sha256,args.approval_sha256)
    bounded=common.load_pinned('k4_target_bounded_supervisor',ROOT/'bounded_stage.py',freeze['files'][str(ROOT/'bounded_stage.py')])
    runs=ROOT/'runs';runs.mkdir(exist_ok=True);require(not runs.is_symlink(),'regular runs root')
    lock=runs/'IN_FLIGHT.lock';state_path=runs/'state.json'
    require(not lock.exists() and not lock.is_symlink(),'one-use unresolved lock blocks every successor')
    reports={}
    if state_path.exists():
        state=read_json(state_path)
        _artifacts,reports=inspect_completed(state,freeze,args.freeze_sha256,common)
        require({p.name for p in runs.iterdir()}=={'state.json'}|{r['job'] for r in state['completed']},'exact immutable completed directory prefix')
    else:
        require(args.job==JOBS[0] and list(runs.iterdir())==[],'fresh first-job namespace')
        state=dict(schema=SCHEMA,freeze_sha256=args.freeze_sha256,completed=[],in_flight=None,stopped=False,canceled=[],worker_cpu_actual=0.0,allocation_charged=0,certificate_bytes=0,certificate_files=0,artifact_bytes=0)
    require_next_job(state,args.job)
    reserve_bytes=38*MIB if spec['kind']=='science' else 6*MIB
    command=common.expand(spec['command'],args.freeze_sha256,args.approval_sha256)
    reservation=dict(job=args.job,allocation_reserved=allocation(args.job),certificate_bytes_reserved=CERT_MAX if spec['kind']=='science' else 0,artifact_bytes_reserved=reserve_bytes,command=command,approval_sha256=args.approval_sha256)
    # Marker itself carries the full reserve if a later state write is interrupted.
    bounded.write_new(lock,dict(schema='k4-residual-one-use-lock-v1',freeze_sha256=args.freeze_sha256,reservation=reservation))
    state['in_flight']=reservation;bounded.atomic(state_path,state)
    reserved_state_pin=sha(state_path,REPORT_MAX);lock_pin=sha(lock,REPORT_MAX)
    jobdir=Path(spec['directory']);jobdir.mkdir();bounded.fsync_dir(runs)
    execution=None;report=None;inventory=[];failures=[];status='INCOMPLETE_OR_FAILED';pair_checked=False;launch_attempted=False
    try:
        require(state['allocation_charged']+allocation(args.job)<=172,'runtime allocation unavailable')
        if spec['kind']=='science':
            require(state['certificate_files']<2 and state['certificate_bytes']+CERT_MAX<=2*CERT_MAX,'two new certificate reservations')
            # Only after durable consumption: a bad/missing authorized raw file
            # is an INCOMPLETE attempt with no child, never a reusable slot.
            item=freeze['inputs'][spec['input_key']]
            require(common.sha(item['path'],common.RAW_MAX)==item['sha256'],'active raw source pin')
            if spec['stage']=='controls':require(common.sha(item['expected_path'],common.RAW_MAX)==item['expected_sha256'],'active expected fixture pin')
        require(common.disk_bytes(freeze)+reserve_bytes+REPORT_MAX<=STAGE_MAX,'stage disk reservation unavailable')
        launch_attempted=True
        execution=bounded.run_bounded(command,str(ROOT),jobdir/'stdout.txt',jobdir/'stderr.txt',spec['limits'])
        failures.extend(execution['failures'])
        validate_execution(execution,command,str(ROOT),spec['limits'])
        report=read_json(jobdir/'result.json')
        status=report_status(report,spec,freeze,args.freeze_sha256,args.approval_sha256)
        require(status in ACCEPTED,'worker incomplete or invalid')
        inventory=artifact_inventory(jobdir,spec['kind'],True)
        if spec['kind']=='science':
            cert=next(v for v in inventory if v['name']=='case.cert.jsonl');claim=report['preflight']['certificate']
            require(cert['bytes']==claim['bytes'] and cert['sha256']==claim['sha256'],'complete certificate bytes match report')
            require(report['resources']['worker_cpu_seconds']<=execution['child_cpu_seconds']+0.001,'inner worker timer is a subset of inclusive OS CPU')
        if args.job=='K4-optimized':
            compare_pair(reports['K4-normal'],report);pair_checked=True
        if args.job=='mock-optimized':
            previous=reports['mock-normal']
            require(previous['counts']==report['counts'] and previous['actual_forbidden_calls']==report['actual_forbidden_calls'],'mock mode obligation agreement')
        common.freeze_context(args.freeze_sha256)
        common.read_authority(spec['stage'],freeze,args.freeze_sha256,args.approval_sha256)
        require(common.require_attempt(args.job,args.freeze_sha256,args.approval_sha256)==parent_attempt_pin,'parent attempt changed during invocation')
        require(sha(state_path,REPORT_MAX)==reserved_state_pin and sha(lock,REPORT_MAX)==lock_pin,'reserved state/one-use marker changed')
        # Reauthenticate every consumed receipt/outer completion and artifact;
        # an earlier result cannot change while a successor executes.
        inspect_completed(state,freeze,args.freeze_sha256,common,True,True)
        if spec['kind']=='science':
            item=freeze['inputs'][spec['input_key']]
            require(common.sha(item['path'],common.RAW_MAX)==item['sha256'],'post-run active input seal')
            if spec['stage']=='controls':require(common.sha(item['expected_path'],common.RAW_MAX)==item['expected_sha256'],'post-run active control expectation seal')
        require(common.disk_bytes(freeze)+REPORT_MAX<=STAGE_MAX,'post-run disk closeout reserve')
    except BaseException as error:
        failures.append(type(error).__name__+':'+str(error)[:400]);status='INCOMPLETE_OR_FAILED'
        retain_failed_reservation(state,args.job)
        if not launch_attempted:
            # No fork needs inherited headroom on this failed prelaunch path.
            resource.setrlimit(resource.RLIMIT_CPU,(spec['limits']['supervisor_cpu_soft'],spec['limits']['supervisor_cpu_hard']))
            memory=spec['limits']['supervisor_address_space_bytes']
            resource.setrlimit(resource.RLIMIT_AS,(memory,memory))
        try:
            inventory,complete=diagnostic_inventory(jobdir)
            if not complete:failures.append('partial_inventory_incomplete_reserve_retained')
        except BaseException as diagnostic:
            failures.append('partial_inventory_unavailable:'+type(diagnostic).__name__+':'+str(diagnostic)[:200])
    if execution is not None:
        own=resource.getrusage(resource.RUSAGE_SELF)
        execution['supervisor_exclusive_cpu_sample']=own.ru_utime+own.ru_stime
        execution['supervisor_peak_rss_kib']=own.ru_maxrss
        if not numeric(execution['supervisor_exclusive_cpu_sample']) or execution['supervisor_exclusive_cpu_sample']>spec['limits']['supervisor_cpu_hard']:failures.append('supervisor_closeout_cpu_invalid_or_overshoot')
    if failures:status='INCOMPLETE_OR_FAILED'
    cert=[v for v in inventory if v['name']=='case.cert.jsonl']
    receipt=dict(schema=SCHEMA,job=args.job,stage=spec['stage'],freeze_sha256=args.freeze_sha256,
        approval_sha256=args.approval_sha256,parent_attempt_sha256=parent_attempt_pin,status=status,launch_attempted=launch_attempted,execution=execution,inventory=inventory,
        certificate_bytes=sum(v['bytes'] for v in cert),certificate_files=len(cert),
        artifact_bytes=sum(v['bytes'] for v in inventory),mode_pair_checked=pair_checked,failures=failures)
    if not failures:validate_receipt(receipt,spec,freeze,args.freeze_sha256,args.approval_sha256,common)
    receipt_path=jobdir/'resource.json'
    if receipt_path.exists() or receipt_path.with_name('resource.json.tmp').exists():
        retain_failed_reservation(state,args.job);bounded.atomic(state_path,state)
        raise ValueError('worker touched supervisor-only receipt path; preserve it and reserve')
    bounded.atomic(receipt_path,receipt)
    if execution is not None and numeric(execution.get('child_cpu_seconds')):state['worker_cpu_actual']+=execution['child_cpu_seconds']
    state['allocation_charged']+=allocation(args.job)
    state['certificate_bytes']+=receipt['certificate_bytes'];state['certificate_files']+=receipt['certificate_files']
    state['artifact_bytes']+=receipt['artifact_bytes']+receipt_path.stat().st_size
    state['completed'].append(dict(job=args.job,status=status,resource_sha256=sha(receipt_path,REPORT_MAX),approval_sha256=args.approval_sha256))
    if not failures:state['in_flight']=None
    else:
        # Final failure receipt and partials are immutable; reserve/marker remain.
        # No subsequent command may consume this failed slot or its successor.
        retain_failed_reservation(state,args.job)
    bounded.atomic(state_path,state)
    if not failures:lock.unlink();bounded.fsync_dir(runs)
    return 0 if not failures else 1


if __name__=='__main__':
    try:sys.exit(main())
    except BaseException as error:
        if isinstance(error,SystemExit):raise
        os.write(2,canonical({'schema':'k4-residual-supervisor-error-v1','type':type(error).__name__,'message':str(error)[:400]})[:1024])
        sys.exit(1)
