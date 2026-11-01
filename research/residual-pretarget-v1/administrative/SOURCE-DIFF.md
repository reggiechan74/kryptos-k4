# Public administrative derivative — NON_RELAUNCH_READY

> Historical evidence only; not executable authority or a current target result. Original document `execution-original/SOURCE-DIFF.md`, SHA256 `f146ad3b77597b2f10322bd9bb200ce8ae712c352a0a67ba1fd1dee7b1e64ec3`, 212384 bytes. Only declared administrative sanitization was applied; see PROVENANCE.json. Original embedded hashes remain original commitments, not hashes of these public bytes. Current prefix status is separate in STATUS.json.

---

# Source-only adapter delta

No source import, test, mock, control or target execution occurred. Existing scientific files are unchanged. Authentication hardening was explicitly approved before freeze; it makes no claim that any historical cache was wrong.
## Scope map
- bounded_stage: retain all 17 operational definitions byte-identically; change namespace/version and remove generic CLI.
- worker: frozen role-authorized raw converter, independent conversion/known control gate, unchanged preflight/producer/reference calls, exact EMPTY pairing, complete relation/interpretation then postseal.
- supervisor: fixed seven jobs/four distinct grant stages, inherited finite counters/caps/pair exclusions, exact role/report/receipt schemas, durable one-use reservations, inclusive OS resources, failure-preserving prefix and finite inventory.
- common: inert fixed identities/source graph, role capabilities, parent-only authority/external receipts, strict capped JSON and finite disk whitelist.
- sealer: one approved metadata-only snapshot after accepted six-slot prefix; no science/raw input/semantic replay, own external completion explicitly pending.
- mocks: exact 159 finite operational assertions in 14 categories; no actual science or case file.
- input_check: separately authored by parent; untouched by adapter author.
## Exact approved loader delta
`common.load_pinned`, `worker.load` (bootstrap), `supervisor._load` (bootstrap), `seal_results.bootstrap`, and mock bootstrap/operational in-memory loading authenticate capped source bytes and compile those bytes with `dont_inherit=True, optimize=sys.flags.optimize`; module identity, __file__, registration and scientific APIs/paths stay fixed. No loader.exec_module/cache route is called. Source cap1 MiB, interpreter hash cap64 MiB.
## Accounting and stops
Runtime nominal456 (124 mocks+160 controls+160 target+12 seal) plus144 preparation/review; no reserve reuse. `launch_attempted=False, execution=null` proves no child; `True,null` is uncertain, never zero-use evidence. All failed authorized attempts retain marker/reserve and stop successors. Exact report postseal failures preserve diagnostic bytes but invalidate all scientific claims. Catastrophic termination can leave only reservation/partial files; parent must preserve a failure inventory, not retry or success-seal. Main update28c60816 remains DENIED pending explicit user branch permission; no alternate publication path.

Exact invocation guards now require integer optimize0/1 and `sys.orig_argv` equality to the whole expanded frozen argv, in addition to parsed argument binding. The two added finite command-category mutations reject -OO and hidden -S; invocation counts remain2+2+2+1.

## Exact text diff: bounded_stage.py
```diff
--- local-provenance/residual-fixed-data-reevaluation-v1/bounded_stage.py
+++ source/operational/bounded_stage.py
@@ -1,8 +1,6 @@
-"""Bounded two-process launcher; source-only until independently frozen.
-
-Derived from audited bounded_checked.py and the full31 supervisor. No module
-import launches, consumes approval, creates files or reads experiment input.
-CLI: receipt cpu_soft memory_MiB wall_seconds stdout_path stderr_path command...
+"""Byte-preserved bounded collector/guard/reaper from validated stage.
+No CLI, input access, launch or write occurs at import. Only the separately
+approved fixed-job supervisor may call run_bounded after durable reservation.
 """
 import ctypes
 import hashlib
@@ -15,13 +13,11 @@
 import signal
 import sys
 import time
-
 MIB = 1024 * 1024
 LOG_MAX = MIB
 JSON_MAX = 2 * MIB
 CHUNK = 16384
-VERSION = 'fixed-data-post-failure-bounded-stage-v1'
-
+VERSION = 'k4-residual-bounded-stage-v1'
 
 def require(condition, message):
     if not condition:
@@ -190,173 +186,6 @@
     disarm()
     release_pid_guard()
     return wait_usage()
-
-
-def expand_freeze_tokens(command, freeze_pin):
-    require(digest_string(freeze_pin), 'mock freeze pin')
-    require(type(command) is list and 1 <= len(command) <= 80
-        and all(type(token) is str and len(token) <= 4096 for token in command), 'mock command template')
-    require(all('${' not in token or token == '${FREEZE_PIN}' for token in command), 'only whole freeze-pin substitution')
-    return [freeze_pin if token == '${FREEZE_PIN}' else token for token in command]
-
-
-def mock_limits():
-    return dict(worker_cpu_soft=30,worker_cpu_hard=31,
-        supervisor_cpu_soft=30,supervisor_cpu_hard=31,
-        worker_address_space_bytes=512*MIB,supervisor_address_space_bytes=512*MIB,
-        wall_seconds=120,log_max_bytes=LOG_MAX)
-
-
-def validate_mock_spec(freeze, freeze_pin, mode, args, command, root):
-    """Pure exact argv/path gate, exercised by no-child source mocks."""
-    root=Path(root)
-    require(mode in ('normal','optimized') and type(freeze) is dict, 'mock mode/freeze')
-    require(type(freeze.get('mock_jobs')) is dict
-        and list(freeze['mock_jobs']) == ['normal','optimized'], 'exact two ordered mock slots')
-    spec=freeze['mock_jobs'][mode]
-    require(type(spec) is dict and set(spec)=={'launch_command','receipt','stdout','stderr',
-        'output','cwd','script','command','expected_counts'}, 'exact mock job schema')
-    directory=root/'mocks'/mode
-    for name,basename in (('receipt','resource.json'),('stdout','stdout.txt'),
-                          ('stderr','stderr.txt'),('output','result.json')):
-        require(spec[name]==str(directory/basename), 'fixed mock '+name+' path')
-    require(spec['cwd']==str(root) and spec['script']==str(root/'protocol_mock_tests.py'), 'fixed mock source/cwd')
-    python=freeze.get('python')
-    require(type(python) is dict and set(python)=={'executable','sha256','version'}, 'mock interpreter schema')
-    expected=[python['executable'],'-I','-B']+(['-O'] if mode=='optimized' else [])+[
-        spec['script'],'--freeze-sha256','${FREEZE_PIN}','--output',spec['output']]
-    require(spec['command']==expected, 'fixed mock command template')
-    expected_launch=[python['executable'],'-I','-B',str(root/'bounded_stage.py'),
-        spec['receipt'],'30','512','120',spec['stdout'],spec['stderr']]+expected
-    require(spec['launch_command']==expected_launch, 'fixed mock launcher template')
-    require(command==expand_freeze_tokens(expected,freeze_pin), 'exact approved mock child argv')
-    actual_launch=[str(Path(sys.executable).resolve()),'-I','-B',str(root/'bounded_stage.py')]+list(args)
-    require(actual_launch==expand_freeze_tokens(expected_launch,freeze_pin), 'exact approved mock launcher argv')
-    require(type(spec['expected_counts']) is dict and bool(spec['expected_counts'])
-        and all(type(key) is str and integer(value) for key,value in spec['expected_counts'].items()), 'frozen exact mock counts')
-    return spec
-
-
-def validate_mock_report(report,spec,mode,freeze_pin):
-    require(mode in ('normal','optimized'), 'fixed mock report mode')
-    require(type(report) is dict and set(report)=={'schema','mode','freeze_sha256','status',
-        'counts','resources','failure','scope'}, 'exact mock result schema')
-    require(report['schema']=='fixed-data-post-failure-mock-report-v1' and report['mode']==mode
-        and report['freeze_sha256']==freeze_pin and report['status']=='PASS'
-        and report['failure'] is None, 'completed frozen mock result')
-    require(type(report['counts']) is dict and set(report['counts'])==set(spec['expected_counts'])
-        and all(integer(value) for value in report['counts'].values())
-        and report['counts']==spec['expected_counts'], 'exact completed mock counts')
-    resources=report['resources']
-    zero_fields={'actual_inner_children','real_solver_calls','seed_draws','generator_expansions','truth_bytes_read'}
-    require(type(resources) is dict and set(resources)==zero_fields|{'worker_cpu_seconds','worker_wall_seconds'}, 'mock resource schema')
-    require(all(type(resources[name]) is int and resources[name]==0 for name in zero_fields), 'no forbidden mock work')
-    require(numeric(resources['worker_cpu_seconds']) and resources['worker_cpu_seconds']<=31
-        and numeric(resources['worker_wall_seconds']) and resources['worker_wall_seconds']<=120, 'mock reported limits')
-    require(report['scope']=='fixed disclosed operational mocks; zero seed/case draws, real solvers, actual inner child launches or truth reads', 'mock scope identity')
-    return True
-
-
-def validate_mock_receipt(receipt,spec,mode,freeze_pin,approval_pin):
-    require(mode in ('normal','optimized') and Path(spec['receipt']).parent.name==mode,
-        'fixed mock receipt mode')
-    execution_keys={'schema','command','cwd','limits','supervisor_pid','child_pid','child_reaped',
-        'parent_death_guard','exit_code','wall_timeout','log_overflow','collector_error','wall_seconds',
-        'child_user_cpu_seconds','child_system_cpu_seconds','child_cpu_seconds','supervisor_exclusive_cpu_sample',
-        'supervisor_cpu_allocation_charged','supervisor_final_write_tail_measured',
-        'child_peak_rss_kib','supervisor_peak_rss_kib','log_bytes_reserved','log_bytes_read','logs','failures'}
-    require(type(receipt) is dict and set(receipt)==execution_keys|{'status','one_use_marker_sha256','mock_completion'}, 'exact mock resource receipt')
-    require(receipt['schema']==VERSION and receipt['status']=='COMPLETED'
-        and receipt['command']==expand_freeze_tokens(spec['command'],freeze_pin)
-        and receipt['cwd']==spec['cwd'] and receipt['limits']==mock_limits(), 'mock receipt invocation/limits')
-    require(type(receipt['exit_code']) is int and receipt['exit_code']==0
-        and receipt['child_reaped'] is True and receipt['parent_death_guard'] is True
-        and receipt['wall_timeout'] is False and receipt['log_overflow'] is False
-        and receipt['collector_error'] is None and receipt['failures']==[], 'mock receipt completed without failure')
-    require(numeric(receipt['wall_seconds']) and receipt['wall_seconds']<=120, 'mock receipt wall')
-    for key in ('child_user_cpu_seconds','child_system_cpu_seconds','child_cpu_seconds','supervisor_exclusive_cpu_sample'):
-        require(numeric(receipt[key]), 'finite mock CPU component')
-    require(abs(receipt['child_user_cpu_seconds']+receipt['child_system_cpu_seconds']-receipt['child_cpu_seconds'])<=1e-8
-        and receipt['child_cpu_seconds']<=31 and receipt['supervisor_exclusive_cpu_sample']<=31, 'mock CPU allowance')
-    require(type(receipt['supervisor_cpu_allocation_charged']) is int
-        and receipt['supervisor_cpu_allocation_charged']==31
-        and receipt['supervisor_final_write_tail_measured'] is False, 'mock supervisor charge/tail')
-    require(all(type(receipt[name]) is int and receipt[name]>=1 for name in ('supervisor_pid','child_pid'))
-        and receipt['supervisor_pid']!=receipt['child_pid'], 'mock process identity')
-    require(all(integer(receipt[name]) for name in ('child_peak_rss_kib','supervisor_peak_rss_kib')), 'mock RSS')
-    for key in ('log_bytes_reserved','log_bytes_read'):
-        require(type(receipt[key]) is list and len(receipt[key])==2
-            and all(integer(value,LOG_MAX) for value in receipt[key]), 'mock bounded log counts')
-    require(receipt['log_bytes_reserved']==receipt['log_bytes_read'], 'mock complete log capture')
-    require(type(receipt['logs']) is list and len(receipt['logs'])==2, 'two mock log records')
-    for index,name in enumerate(('stdout','stderr')):
-        item=receipt['logs'][index]
-        require(type(item) is dict and set(item)=={'path','bytes','sha256'} and item['path']==spec[name]
-            and integer(item['bytes'],LOG_MAX) and item['bytes']==receipt['log_bytes_reserved'][index]
-            and digest_string(item['sha256']), 'mock log identity')
-    marker={'schema':'bounded-stage-one-use-v2','command':receipt['command'],
-        'receipt':spec['receipt'],'stdout':spec['stdout'],'stderr':spec['stderr']}
-    require(receipt['one_use_marker_sha256']==hashlib.sha256(canonical(marker)).hexdigest(), 'mock one-use marker commitment')
-    completion=receipt['mock_completion']
-    require(type(completion) is dict and set(completion)=={'freeze_sha256','pre_mock_approval_sha256','result'}, 'mock completion schema')
-    require(completion['freeze_sha256']==freeze_pin and completion['pre_mock_approval_sha256']==approval_pin, 'mock approval/freeze commitment')
-    item=completion['result']
-    require(type(item) is dict and set(item)=={'path','bytes','sha256'} and item['path']==spec['output']
-        and integer(item['bytes'],65536) and digest_string(item['sha256']), 'mock result commitment')
-    return True
-
-
-def mock_context(root,args,command,mode):
-    """Read-only permission/source guard; returns before any marker or fork."""
-    root=Path(root);freeze_path=root/'FREEZE.json';approval_path=root/'PRE-MOCK-APPROVAL.json'
-    freeze_pin=sha(freeze_path,JSON_MAX);freeze=read_json(freeze_path)
-    approval=read_json(approval_path)
-    require(type(approval) is dict and set(approval)=={'schema','status','freeze_sha256'}
-        and approval['schema']=='fixed-data-post-failure-pre-mock-approval-v1'
-        and approval['status']=='APPROVED_FOR_TWO_FROZEN_MOCKS'
-        and approval['freeze_sha256']==freeze_pin, 'independent two-mock approval gate closed')
-    approval_pin=sha(approval_path,JSON_MAX)
-    require(type(freeze) is dict and set(freeze)=={'schema','files','python','jobs','limits','mock_jobs',
-        'public_paths','analysis_manifest_sha256','resource_allocation_sha256',
-        'origin_manifest_sha256','generation_origin_freeze_sha256'}
-        and freeze.get('schema')=='fixed-data-post-failure-reevaluation-v1-freeze', 'mock source freeze schema')
-    spec=validate_mock_spec(freeze,freeze_pin,mode,args,command,root)
-    other_mode='optimized' if mode=='normal' else 'normal'
-    other=freeze['mock_jobs'][other_mode]
-    validate_mock_spec(freeze,freeze_pin,other_mode,
-        expand_freeze_tokens(other['launch_command'],freeze_pin)[4:],
-        expand_freeze_tokens(other['command'],freeze_pin),root)
-    require(spec['expected_counts']==other['expected_counts'], 'same finite mock count dictionary in both modes')
-    require(freeze['python']=={'executable':str(Path(sys.executable).resolve()),
-        'sha256':sha(Path(sys.executable).resolve(),64*MIB),'version':sys.version}, 'mock interpreter source pin')
-    require(type(freeze.get('files')) is dict and 8<=len(freeze['files'])<=64, 'mock frozen source list')
-    ancestors={
-        'source/scientific/residual_decoder.py':'be050003b9a73c14a7f7dda44afeb160e0e847045d57ddfa4b9527bdc68f7d67',
-        'source/scientific/affine_filter.py':'1e19e9ad872d517487cfe7968a9f4b906756007d5e710be216807620f078c90d',
-        'source/scientific/reference_v3.py':'0730f8b0a26109919ba6eb558be18063d137ced233b397cd188dc261a13fe8f9',
-        'local-provenance/residual-fresh-validation-v2/generator.py':'4bf7b8198603f255692b90b5d5ab479ac0c4fa74ab8c2fa9871f6f54668edfa9',
-        'local-provenance/residual-fixed-data-reevaluation-v1-public/ORIGIN-MANIFEST.json':'002541c7d8c9786d21f1b5a3fb3293efc83709ee32d1cb72ba751eb7383ca80b',
-        'local-provenance/residual-fixed-data-reevaluation-v1-public/ORIGIN-RUN-INVENTORY.json':'a86c20e9c142e00f8f9165fe83184517b7d8324039d7cc86ced3f79aeb642f70'}
-    for name,pin in freeze['files'].items():
-        require(type(name) is str and Path(name).is_absolute()
-            and (Path(name).parent==root or ancestors.get(name)==pin) and digest_string(pin)
-            and sha(name,64*MIB)==pin, 'mock frozen source mismatch')
-    for filename in ('bounded_stage.py','protocol_mock_tests.py'):
-        require(str(root/filename) in freeze['files'], 'mock launcher/test source must be frozen')
-    if mode=='optimized':
-        previous=freeze['mock_jobs']['normal'];receipt=read_json(previous['receipt'])
-        validate_mock_receipt(receipt,previous,'normal',freeze_pin,approval_pin)
-        marker_path=Path(previous['receipt']).with_name(Path(previous['receipt']).name+'.started.json')
-        require(sha(marker_path,JSON_MAX)==receipt['one_use_marker_sha256'], 'normal one-use marker changed')
-        for item in receipt['logs']+[receipt['mock_completion']['result']]:
-            cap=65536 if item['path']==previous['output'] else LOG_MAX
-            path=Path(item['path'])
-            require(path.stat().st_size==item['bytes'] and sha(path,cap)==item['sha256'], 'normal sealed artifact changed')
-        validate_mock_report(read_json(previous['output'],65536),previous,'normal',freeze_pin)
-        # A missing/failed resource receipt is an outstanding one-use reservation,
-        # never permission to launch optimized. External tool completion is also
-        # required by the parent's operating gate; this local receipt cannot prove it.
-    return freeze,spec,freeze_pin,approval_pin
 
 
 def run_bounded(command, cwd, stdout_path, stderr_path, limits):
@@ -530,82 +359,3 @@
         logs=log_records,
         failures=failures)
 
-
-def main(argv=None):
-    args = list(sys.argv[1:] if argv is None else argv)
-    require(len(args) >= 7, 'receipt cpu MiB wall stdout stderr command required')
-    receipt_text, cpu_text, memory_text, wall_text, stdout_text, stderr_text, *command = args
-    require(all(text.isdigit() and str(int(text)) == text for text in (cpu_text,memory_text,wall_text)), 'canonical integer limits')
-    cpu, memory_mib, wall = int(cpu_text), int(memory_text), int(wall_text)
-    require((cpu,memory_mib,wall) in ((30,512,120),(5,512,120),(180,768,600)), 'only frozen generic stage envelopes')
-    death_guard()
-    resource.setrlimit(resource.RLIMIT_CPU,(cpu,cpu+1))
-    resource.setrlimit(resource.RLIMIT_AS,(memory_mib*MIB,memory_mib*MIB))
-    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
-    resource.setrlimit(resource.RLIMIT_FSIZE,(32*MIB,32*MIB))
-    require(len(command)<=64 and all(type(value) is str and len(value)<=4096 for value in command),'bounded stage argv')
-    require(sys.flags.isolated==1 and sys.dont_write_bytecode is True and sys.flags.optimize==0,
-        'launcher itself must use normal isolated no-bytecode Python')
-    root = Path(__file__).resolve().parent
-    require(command[0] == str(Path(sys.executable).resolve()) and command[1:3] == ['-I','-B'], 'isolated pinned Python command')
-    script_index = 4 if len(command) > 3 and command[3] == '-O' else 3
-    require(len(command) > script_index, 'stage script required')
-    script = Path(command[script_index])
-    require(script.parent == root and script.name in ('protocol_mock_tests.py','bind_ancestry.py','seal_results.py','analyze.py'), 'fixed stage script')
-    require(script.is_file() and not script.is_symlink(), 'regular stage source')
-    require(script_index == 3 or script.name == 'protocol_mock_tests.py', 'only mock optimized stage')
-    expected_cpu = {'protocol_mock_tests.py':30,'bind_ancestry.py':30,'seal_results.py':5,'analyze.py':180}[script.name]
-    require(cpu == expected_cpu, 'stage envelope identity')
-    receipt, stdout, stderr = map(Path, (receipt_text,stdout_text,stderr_text))
-    require(all(p.is_absolute() and p.parent.is_dir() and not p.parent.is_symlink() for p in (receipt,stdout,stderr)), 'absolute stage paths')
-    require(len({receipt,stdout,stderr}) == 3, 'distinct stage paths')
-    mock=None
-    if script.name=='protocol_mock_tests.py':
-        mode='optimized' if script_index==4 else 'normal'
-        mock=mock_context(root,args,command,mode)
-        require(not any(receipt.parent.iterdir()), 'fresh fixed mock slot directory required')
-    marker = receipt.with_name(receipt.name + '.started.json')
-    require(not receipt.exists() and not stdout.exists() and not stderr.exists(), 'new stage output paths required')
-    write_new(marker, dict(schema='bounded-stage-one-use-v2', command=command,
-        receipt=str(receipt),stdout=str(stdout),stderr=str(stderr)))
-    marker_pin=sha(marker,JSON_MAX)
-    limits = dict(worker_cpu_soft=cpu,worker_cpu_hard=cpu+1,
-        supervisor_cpu_soft=cpu,supervisor_cpu_hard=cpu+1,
-        worker_address_space_bytes=memory_mib*MIB,supervisor_address_space_bytes=memory_mib*MIB,
-        wall_seconds=wall,log_max_bytes=LOG_MAX)
-    result = run_bounded(command, root, stdout, stderr, limits)
-    result['one_use_marker_sha256'] = marker_pin
-    if mock is not None:
-        freeze,spec,freeze_pin,approval_pin=mock
-        result['mock_completion']=None
-        try:
-            require(sha(root/'FREEZE.json',JSON_MAX)==freeze_pin
-                and sha(root/'PRE-MOCK-APPROVAL.json',JSON_MAX)==approval_pin, 'post-mock freeze/approval changed')
-            for name,pin in freeze['files'].items():require(sha(name,64*MIB)==pin, 'post-mock source changed')
-            output=Path(spec['output'])
-            validate_mock_report(read_json(output,65536),spec,mode,freeze_pin)
-            result['mock_completion']={'freeze_sha256':freeze_pin,'pre_mock_approval_sha256':approval_pin,
-                'result':{'path':str(output),'bytes':output.stat().st_size,'sha256':sha(output,65536)}}
-        except (OSError,ValueError,TypeError,KeyError,MemoryError) as error:
-            result['failures'].append('mock_completion:'+type(error).__name__+':'+str(error)[:300])
-    own=resource.getrusage(resource.RUSAGE_SELF)
-    result['supervisor_exclusive_cpu_sample']=own.ru_utime+own.ru_stime
-    result['supervisor_peak_rss_kib']=own.ru_maxrss
-    if not numeric(result['supervisor_exclusive_cpu_sample']) or result['supervisor_exclusive_cpu_sample']>cpu+1:
-        result['failures'].append('supervisor_closeout_cpu_invalid_or_overshoot')
-    result['status'] = 'COMPLETED' if not result['failures'] else 'INCOMPLETE_OR_FAILED'
-    if mock is not None and not result['failures']:
-        validate_mock_receipt(result,spec,mode,freeze_pin,approval_pin)
-    write_new(receipt, result)
-    return 0 if not result['failures'] else 1
-
-
-if __name__ == '__main__':
-    try:
-        sys.exit(main())
-    except BaseException as error:
-        if isinstance(error, SystemExit):
-            raise
-        os.write(2, canonical({'schema':'bounded-stage-error-v2','type':type(error).__name__,
-            'message':str(error)[:400]})[:1024])
-        sys.exit(1)
```

## Exact text diff: worker.py
```diff
--- local-provenance/residual-fixed-data-reevaluation-v1/worker.py
+++ source/operational/worker.py
@@ -1,34 +1,31 @@
-"""One blind fixed-model slot. Source-only until independent freeze and approvals.
-
-No truth path, seed, generator or post-fit eligibility reaches this worker.
+"""One frozen raw-format control or K4 slot; inert on import/help.
+No target source input, matrices, imports of scientific modules, or output
+construction occurs before exact stage authority, bounds and source pins.
 """
 import argparse
-import copy
 import ctypes
 import hashlib
 import importlib.util
 import json
-import math
 import os
 from pathlib import Path
 import resource
 import signal
 import sys
 import time
-
-ROOT=Path('local-provenance/residual-fixed-data-reevaluation-v1')
+ROOT=Path('original-execution-namespace')
 ENGINE=Path('source/scientific/residual_decoder.py')
 AFFINE=ENGINE.with_name('affine_filter.py')
 REFERENCE=Path('source/scientific/reference_v3.py')
+PREFLIGHT=Path('source/scientific/preflight_blind.py')
+CHECKER=Path('source/scientific/checker_blind.py')
 ENGINE_PIN='be050003b9a73c14a7f7dda44afeb160e0e847045d57ddfa4b9527bdc68f7d67'
 AFFINE_PIN='1e19e9ad872d517487cfe7968a9f4b906756007d5e710be216807620f078c90d'
 REFERENCE_PIN='0730f8b0a26109919ba6eb558be18063d137ced233b397cd188dc261a13fe8f9'
 MIB=1024*1024
 REPORT_MAX=2*MIB
 HASH_MAX=64*MIB
-REPORT_SCHEMA='fixed-data-post-failure-slot-report-v1'
-SOURCE_PATHS=(ENGINE,AFFINE,REFERENCE,ROOT/'preflight_blind.py',ROOT/'checker_blind.py')
-
+REPORT_SCHEMA='k4-residual-slot-report-v1'
 
 def require(condition,message):
     if not condition: raise ValueError(message)
@@ -66,37 +63,21 @@
     return (json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
 
 
-def expanded_command(template,input_pin):
-    require(type(input_pin) is str and len(input_pin)==64 and all(c in '0123456789abcdef' for c in input_pin),
-            'exact input digest')
-    require(type(template) is list and all(type(part) is str and 0<len(part)<=4096 for part in template),
-            'command template strings')
-    require(template.count('${INPUT_PIN}')==1,'one whole-token input substitution')
-    for part in template:
-        require('${' not in part or part=='${INPUT_PIN}','only whole-token input substitution')
-    return [input_pin if part=='${INPUT_PIN}' else part for part in template]
-
-
 def load(name,path,pin):
     path=Path(path)
-    require(path.is_file() and not path.is_symlink() and sha(path)==pin,'pinned isolated module: '+str(path))
+    require(path.is_file() and not path.is_symlink() and path.stat().st_size<=MIB,'bounded pinned isolated source')
+    with path.open('rb') as handle:source=handle.read(MIB+1)
+    require(len(source)<=MIB and hashlib.sha256(source).hexdigest()==pin,'pinned isolated module: '+str(path))
     spec=importlib.util.spec_from_file_location(name,path)
+    require(spec is not None and spec.loader is not None,'isolated module loader')
     module=importlib.util.module_from_spec(spec);sys.modules[name]=module
-    spec.loader.exec_module(module)
+    exec(compile(source,str(path),'exec',dont_inherit=True,optimize=sys.flags.optimize),module.__dict__)
     return module
-
-
-def require_worker_bounds():
-    require(resource.getrlimit(resource.RLIMIT_CPU)==(60,75),'worker CPU wrapper')
-    require(resource.getrlimit(resource.RLIMIT_AS)==(1024*MIB,1024*MIB),'worker address-space wrapper')
-    guard=ctypes.c_int()
-    require(ctypes.CDLL(None).prctl(2,ctypes.byref(guard),0,0,0)==0 and guard.value==signal.SIGKILL,
-            'parent-death guard required')
 
 
 def normalized_producer(result):
     """Only these two typed path rules remove time; every logical counter remains."""
-    require(type(result) is dict and result.get('status')=='EXACT','complete producer required')
+    require(type(result) is dict and result.get('status') in ('EXACT','EMPTY'),'complete producer required')
     out=dict(result)
     require(type(result.get('resources')) is dict and 'wall_seconds' in result['resources'],'root time field')
     out['resources']={k:v for k,v in result['resources'].items() if k!='wall_seconds'}
@@ -134,113 +115,153 @@
     finally:os.close(fd)
 
 
-def literal_control(case_id):
-    require(case_id in ('G0','G1'),'literal gate id')
-    return dict(id=case_id,contexts=[[0]*6],observed=[] if case_id=='G0' else [[0,0]],
-                sparsity=3,allowed_features=list(range(31)))
-
-
-def main():
-    parser=argparse.ArgumentParser()
-    for flag in ('job','input','input-sha256','output'):parser.add_argument('--'+flag,required=True)
-    args=parser.parse_args()
-    require_worker_bounds()
-    freeze_path=ROOT/'FREEZE.json';freeze=read_json(freeze_path,MIB);freeze_pin=sha(freeze_path)
-    require(freeze.get('schema')=='fixed-data-post-failure-reevaluation-v1-freeze','freeze schema')
-    files=freeze.get('files')
-    require(type(files) is dict and all(type(p) is str and type(v) is str for p,v in files.items()),'source manifest')
-    for path,pin in files.items():
-        candidate=Path(path)
-        require(candidate.is_absolute() and candidate.is_file() and not candidate.is_symlink() and sha(candidate)==pin,'frozen source changed')
-    require(files.get(str(ENGINE))==ENGINE_PIN and files.get(str(AFFINE))==AFFINE_PIN
-            and files.get(str(REFERENCE))==REFERENCE_PIN,'immutable scientific pins')
-    require(str(Path(__file__).resolve()) in files,'worker frozen')
-    spec=freeze['jobs'].get(args.job);require(type(spec) is dict,'scheduled worker only')
-    expected=expanded_command(spec['command'],args.input_sha256)
-    actual=[str(Path(sys.executable).resolve()),'-I','-B']+(['-O'] if sys.flags.optimize else [])+[str(Path(__file__).resolve())]+sys.argv[1:]
-    require(actual==expected,'exact frozen worker command')
-    require(spec['report_identity']['python_optimized'] is bool(sys.flags.optimize),'worker mode')
-    common=load('fresh_custody_common',ROOT/'custody_common.py',files[str(ROOT/'custody_common.py')])
-    common.verify_freeze(freeze_path,freeze_pin)
-    public=common.read_public(args.input,args.input_sha256)
-    run_path=Path(freeze['public_paths']['run_approval'])
-    run=read_json(run_path,65536)
-    require(type(run) is dict and set(run)==common.RUN_APPROVAL_KEYS,'exact public run approval')
-    custody_path=Path(freeze['public_paths']['custody'])
-    custody=common.read_json(custody_path,65536,run['custody_sha256'])
-    common.validate_custody(custody,freeze,freeze_pin,args.input_sha256)
-    common.validate_run_approval(run,freeze,freeze_pin,args.input_sha256,run['custody_sha256'])
-    require(run['draw_approval_sha256']==custody['draw_approval_sha256'],'one-draw custody binding')
-    require(run['public_input_path']==str(Path(args.input).resolve()),'public input path')
-    case_id=spec['report_identity']['case_id'];output=Path(args.output)
-    require(output==ROOT/'runs'/args.job/'result.json','fixed report path')
-    require(type(case_id) is str,'case id')
-    if case_id in ('G0','G1'):control=literal_control(case_id)
+def bootstrap(freeze_pin):
+    require(type(freeze_pin) is str and len(freeze_pin)==64,'freeze pin syntax')
+    path=ROOT/'FREEZE.json'
+    require(sha(path,REPORT_MAX)==freeze_pin,'external source freeze pin')
+    frozen=read_json(path,REPORT_MAX)
+    common_path=ROOT/'common.py'
+    require(type(frozen) is dict and type(frozen.get('files')) is dict and str(common_path) in frozen['files'],'operational bootstrap source pin')
+    common=load('k4_target_common_worker',common_path,frozen['files'][str(common_path)])
+    return common,common.freeze_context(freeze_pin)
+
+
+def convert_raw(raw,internal_id):
+    """Primary raw-letter converter; no scientific module or input-file access.
+
+    Called only by an approved actual worker or disclosed literal operational
+    mock. Independent implementation lives in input_check.py, not here.
+    """
+    require(internal_id in ('v000','v001','v002'),'fixed structural role ID')
+    text=raw['ciphertext']
+    ranks=[ord(letter)-ord('A') for letter in text]
+    require(len(ranks)==97 and all(type(v) is int and 0<=v<26 for v in ranks),'raw rank domain')
+    contexts=[]
+    for i in range(6,97):
+        contexts.append([ranks[i-j] for j in range(1,7)])
+    observations=[]
+    for crib in raw['cribs']:
+        first=crib['start']-1
+        for offset,letter in enumerate(crib['plaintext']):
+            i=first+offset
+            observations.append([i-6,(ranks[i]-(ord(letter)-ord('A')))%26])
+    require([row for row,_value in observations]==list(range(15,28))+list(range(57,68)),'fixed public row mapping')
+    return dict(id=internal_id,contexts=contexts,observed=observations,sparsity=3,allowed_features=list(range(31)))
+
+
+def require_status_pair(producer_status,reference_status):
+    require((producer_status,reference_status) in (('EXACT','VERIFIED_EXACT'),('EMPTY','VERIFIED_EMPTY')),'complete matching producer/reference statuses')
+    return True
+
+
+def empty_invariants(result,verified):
+    require(result['status']=='EMPTY' and verified['status']=='VERIFIED_EMPTY','EMPTY exact pairing')
+    require(result['pieces']==[] and result['masks']==[[] for _ in range(91)] and result['witnesses']==[{} for _ in range(91)] and result['provenance']==[{} for _ in range(91)] and result['feasibility_witness'] is None,'complete empty relation shape')
+    require(all(type(verified[name]) is int and verified[name]==0 for name in ('pieces_checked','canonical_functions','original_lifts','joint_predictions')),'zero EMPTY reference counts')
+    return True
+
+
+def semantic_summary(result,verified,interpretation):
+    require_status_pair(result['status'],verified['status'])
+    if result['status']=='EMPTY':empty_invariants(result,verified)
     else:
-        matches=[c for c in public['cases'] if c['id']==case_id]
-        require(len(matches)==1,'exact public case')
-        control=dict(matches[0]['instance'],id=case_id)
-    report=dict(schema=REPORT_SCHEMA,slot=args.job,case_id=case_id,python_optimized=bool(sys.flags.optimize),
-        origin_manifest_sha256=freeze['origin_manifest_sha256'],
-        freeze_sha256=freeze_pin,input_sha256=args.input_sha256,source_sha256=files,
-        status='INCOMPLETE_OR_FAILED',preflight=None,producer=None,verification=None,
-        semantic_summary=None,resources=None,reason=None)
+        require(all(type(verified[name]) is int and verified[name]>0 for name in ('pieces_checked','canonical_functions','original_lifts','joint_predictions')),'nonempty reference counts')
+        require(type(result['feasibility_witness']) is dict,'common admitted feasibility witness')
+    require(type(interpretation) is dict and set(interpretation)=={'classification','plaintext_masks','example_plaintext_tail','first_six_claimed'} and interpretation['first_six_claimed'] is False,'interpretation contract/no first-six claim')
+    return dict(producer_nontime_sha256=producer_digest(result),masks=result['masks'],
+        pieces=verified['pieces_checked'],canonical_functions=verified['canonical_functions'],
+        original_lifts=verified['original_lifts'],joint_predictions=verified['joint_predictions'],
+        feasibility_witness=result['feasibility_witness'],interpretation=interpretation)
+
+
+def main(argv=None):
+    parser=argparse.ArgumentParser(description='One frozen raw-format job; no implicit runs.')
+    for flag in ('job','freeze-sha256','approval-sha256','output'):parser.add_argument('--'+flag,required=True)
+    args=parser.parse_args(argv)
+    common,freeze=bootstrap(args.freeze_sha256)
+    stage,kind,key,inner,optimized=common.job_identity(args.job)
+    require(kind=='science','worker science jobs only')
+    common.require_child_bounds(stage)
+    actual=list(sys.argv[1:] if argv is None else argv)
+    spec=common.validate_child_command(freeze,args.job,args.freeze_sha256,args.approval_sha256,actual)
+    require(args.output==spec['output'],'fixed output path')
+    approval=common.read_authority(stage,freeze,args.freeze_sha256,args.approval_sha256)
+    raw=common.read_authorized_raw(freeze,approval,args.job)
+    input_spec=freeze['inputs'][key]
+    check=common.load_pinned('k4_target_independent_input',ROOT/'input_check.py',freeze['files'][str(ROOT/'input_check.py')])
+    instance=convert_raw(raw,inner)
+    independently=check.convert_raw_independent(raw,inner)
+    require(instance==independently,'independent raw conversion mismatch')
+    expected=None
+    if stage=='controls':
+        expected=common.read_json(input_spec['expected_path'],common.RAW_MAX,input_spec['expected_sha256'])
+        require(expected['raw_sha256']==input_spec['sha256'],'expected fixture raw binding')
+        for converted in (instance,independently):
+            require(converted['contexts']==expected['expected_contexts'] and
+                converted['observed']==expected['expected_observed'],'pre-science known raw conversion gate')
+    report=dict(schema=REPORT_SCHEMA,slot=args.job,stage=stage,input_role=key,case_id=inner,
+        python_optimized=optimized,freeze_sha256=args.freeze_sha256,input_sha256=input_spec['sha256'],
+        approval_sha256=args.approval_sha256,source_sha256=freeze['files'],status='INCOMPLETE_OR_FAILED',
+        preflight=None,producer=None,verification=None,semantic_summary=None,control_check=None,
+        resources=None,reason=None)
     wall_start=time.monotonic();cpu_start=time.process_time()
     producer_counters=None;reference_counters=None
     producer_attempted=False;reference_attempted=False
     try:
-        reference=load('fresh_reference_v3',REFERENCE,REFERENCE_PIN)
-        preflight=load('fresh_preflight_blind',ROOT/'preflight_blind.py',files[str(ROOT/'preflight_blind.py')])
-        checker=load('fresh_checker_blind',ROOT/'checker_blind.py',files[str(ROOT/'checker_blind.py')])
+        reference=common.load_pinned('k4_target_reference',REFERENCE,REFERENCE_PIN)
+        preflight=common.load_pinned('k4_target_preflight',PREFLIGHT,freeze['files'][str(PREFLIGHT)])
+        checker=common.load_pinned('k4_target_certificate_checker',CHECKER,freeze['files'][str(CHECKER)])
         evidence=preflight.EvidenceBudget()
-        pf=preflight.run(control,output.parent/'case.cert.jsonl',args.input_sha256,REFERENCE_PIN,
-                         freeze_pin,reference,checker,evidence)
+        pf=preflight.run(instance,Path(args.output).parent/'case.cert.jsonl',input_spec['sha256'],
+            REFERENCE_PIN,args.freeze_sha256,reference,checker,evidence)
         report['preflight']=pf
         if pf['status']=='GATE_REJECTED_LOWER_BOUND':
-            require(pf['certificate']['complete'] and pf['exact_W'] is None
-                    and type(pf['lower_bound']) is int and pf['lower_bound']>1000000,'complete resource gate')
+            require(stage=='target','an actual interface control may not resource-gate')
+            require(pf['certificate']['complete'] is True and pf['exact_W'] is None and type(pf['lower_bound']) is int and pf['lower_bound']>1000000,'complete resource gate')
             report['status']='CERTIFIED_RESOURCE_GATE'
         else:
-            require(case_id not in ('G0','G1'),'predetermined resource control failed to gate')
-            require(pf['status']=='WORKLOAD_ADMITTED' and pf['checked_supports']==4495
-                    and type(pf['exact_W']) is int and 0<=pf['exact_W']<=1000000
-                    and pf['certificate']['complete'],'precheck incomplete')
-            load('affine_filter',AFFINE,AFFINE_PIN)
-            engine=load('fresh_residual_decoder',ENGINE,ENGINE_PIN)
-            observed=dict(control['observed'])
+            require(pf['status']=='WORKLOAD_ADMITTED' and pf['checked_supports']==4495 and type(pf['exact_W']) is int and 0<=pf['exact_W']<=1000000 and pf['certificate']['complete'] is True,'complete preflight required')
+            common.load_pinned('affine_filter',AFFINE,AFFINE_PIN)
+            engine=common.load_pinned('k4_target_decoder',ENGINE,ENGINE_PIN)
+            observed=dict(instance['observed'])
             producer_attempted=True
-            result=engine.decode(control['contexts'],observed,3,list(range(31)),
+            result=engine.decode(instance['contexts'],observed,3,list(range(31)),
                 budget=engine.Budget(max_steps=2000000,max_pieces=40000,max_core_work=200000000,
                     max_core_solves=1000000,max_core_terms=100000,max_seconds=30.0))
-            report['producer']={k:result[k] for k in ('status','resources','stats')}
-            producer_counters={k:v for k,v in result['resources'].items() if k!='wall_seconds'}
-            require(result['status']=='EXACT','supported producer not EXACT')
+            report['producer']={name:result[name] for name in ('status','resources','stats')}
+            producer_counters={name:value for name,value in result['resources'].items() if name!='wall_seconds'}
+            require(result['status'] in ('EXACT','EMPTY'),'producer did not complete')
             budget=reference.BudgetV3(max_fiber_points=1000000,max_lift_trials=4000000,
                 max_solve_calls=100000,max_certificate_checks=200000,max_row_operations=5000000,
                 max_work_units=500000000,max_witness_checks=1000000,max_output_records=5000000,max_seconds=45.0)
             reference_attempted=True
-            verified=reference.verify_result_v3(control['contexts'],observed,result,3,list(range(31)),
+            verified=reference.verify_result_v3(instance['contexts'],observed,result,3,list(range(31)),
                 budget=budget,expected_source_sha256=ENGINE_PIN)
             report['verification']=verified
-            reference_counters={k:v for k,v in verified['resources'].items() if k!='wall_seconds'}
-            require(verified['status']=='VERIFIED_EXACT' and verified['resources']['fiber_points']==pf['exact_W'],
-                    'complete independent verification required')
-            report['semantic_summary']=dict(producer_nontime_sha256=producer_digest(result),masks=result['masks'],
-                pieces=verified['pieces_checked'],canonical_functions=verified['canonical_functions'],
-                original_lifts=verified['original_lifts'],joint_predictions=verified['joint_predictions'],
-                feasibility_witness=result['feasibility_witness'])
-            report['status']='VERIFIED_EXACT'
-        for path,pin in files.items():require(sha(path)==pin,'post-run source changed')
-        require(sha(args.input,262144)==args.input_sha256,'post-run public input changed')
+            reference_counters={name:value for name,value in verified['resources'].items() if name!='wall_seconds'}
+            require_status_pair(result['status'],verified['status'])
+            require(verified['resources']['fiber_points']==pf['exact_W'],'complete reference charged fiber count')
+            interpretation=check.interpret_verified(raw,instance,result,verified)
+            report['semantic_summary']=semantic_summary(result,verified,interpretation)
+            if expected is not None:
+                require(check.verify_control_expectations(raw,instance,result,verified,interpretation,expected,pf) is True,'actual control expectations failed')
+                report['control_check']=dict(status='PASS',expected_sha256=input_spec['expected_sha256'])
+            report['status']=verified['status']
+        common.freeze_context(args.freeze_sha256)
+        require(common.sha(input_spec['path'],common.RAW_MAX)==input_spec['sha256'],'post-run raw input changed')
+        require(common.sha(ROOT/'approvals'/(stage+'.json'),65536)==args.approval_sha256,'post-run authority changed')
+        if expected is not None:require(common.sha(input_spec['expected_path'],common.RAW_MAX)==input_spec['expected_sha256'],'post-run control expectation changed')
     except BaseException as error:
-        report['status']='INCOMPLETE_OR_FAILED';report['semantic_summary']=None
+        report['status']='INCOMPLETE_OR_FAILED';report['semantic_summary']=None;report['control_check']=None
         report['producer']=None;report['verification']=None
         report['reason']=type(error).__name__+': '+str(error)[:500]
-    report['resources']=dict(worker_wall_seconds=time.monotonic()-wall_start,
-                             worker_cpu_seconds=time.process_time()-cpu_start,
-                             producer_counters=producer_counters,reference_counters=reference_counters,
-                             producer_attempted=producer_attempted,reference_attempted=reference_attempted)
-    write_report(output,report)
-    return 0 if report['status'] in ('VERIFIED_EXACT','CERTIFIED_RESOURCE_GATE') else 1
-
-if __name__=='__main__':sys.exit(main())
+    report['resources']=dict(worker_wall_seconds=time.monotonic()-wall_start,worker_cpu_seconds=time.process_time()-cpu_start,
+        producer_counters=producer_counters,reference_counters=reference_counters,
+        producer_attempted=producer_attempted,reference_attempted=reference_attempted)
+    write_report(args.output,report)
+    return 0 if report['status'] in ('VERIFIED_EXACT','VERIFIED_EMPTY','CERTIFIED_RESOURCE_GATE') else 1
+
+
+if __name__=='__main__':
+    sys.exit(main())
+
```

## Exact text diff: supervisor.py
```diff
--- local-provenance/residual-fixed-data-reevaluation-v1/supervisor.py
+++ source/operational/supervisor.py
@@ -1,7 +1,7 @@
-"""One-use blind-cohort supervisor and read-only terminal authenticator.
-
-SOURCE ONLY until independent freeze confirmation and separate parent authority.
-No import-time launch, seed, input/custody read, state mutation or solver import.
+"""Seven fixed one-use jobs with distinct authority stages; inert at import.
+Only metadata/source authentication precedes parent stage authorization. No raw
+input is opened by a mock, sealer, help, import, or generic source verification.
+The bounded process collector remains byte-identical to the validated study.
 """
 import argparse
 import ctypes
@@ -14,50 +14,58 @@
 import resource
 import signal
 import sys
-
-ROOT = Path('local-provenance/residual-fixed-data-reevaluation-v1')
-MIB = 1024*1024
-REPORT_MAX = 2*MIB
-LOG_MAX = MIB
-CERT_MAX = 32*MIB
-CERT_TOTAL = 28*CERT_MAX
-STAGE_MAX = 1280*MIB
-NONCOHORT_RESERVE = 64*MIB
-SCHEMA = 'fixed-data-post-failure-supervisor-v1'
-FREEZE_SCHEMA = 'fixed-data-post-failure-reevaluation-v1-freeze'
-CASES = ('G0','G1') + tuple('v%03d' % index for index in range(12))
-JOBS = tuple(case+'-'+mode for case in CASES for mode in ('normal','optimized'))
-ACCEPTED = ('VERIFIED_EXACT','CERTIFIED_RESOURCE_GATE')
-ARTIFACT_CAPS = {'stdout.txt':LOG_MAX,'stderr.txt':LOG_MAX,
-                 'result.json':REPORT_MAX,'case.cert.jsonl':CERT_MAX}
-REPORT_KEYS = {'schema','slot','case_id','python_optimized','freeze_sha256','origin_manifest_sha256',
-    'input_sha256','source_sha256','status','preflight','producer','verification',
-    'semantic_summary','resources','reason'}
+ROOT=Path('original-execution-namespace')
+MIB=1024*1024
+REPORT_MAX=2*MIB
+LOG_MAX=MIB
+CERT_MAX=32*MIB
+STAGE_MAX=256*MIB
+SCHEMA='k4-residual-target-supervisor-v1'
+JOBS=('mock-normal','mock-optimized','CTRL-positive-normal','CTRL-empty-normal','K4-normal','K4-optimized','seal')
+ACCEPTED=('PASS','VERIFIED_EXACT','VERIFIED_EMPTY','CERTIFIED_RESOURCE_GATE','SEALED_METADATA')
+REPORT_KEYS={'schema','slot','stage','input_role','case_id','python_optimized','freeze_sha256','input_sha256','approval_sha256','source_sha256','status','preflight','producer','verification','semantic_summary','control_check','resources','reason'}
+ARTIFACT_CAPS={'stdout.txt':LOG_MAX,'stderr.txt':LOG_MAX,'result.json':REPORT_MAX,'case.cert.jsonl':CERT_MAX}
+
+
 PREFLIGHT_COUNTERS = {'fiber_points','lift_trials','solve_calls','certificate_checks',
     'row_operations','work_units','witness_checks','output_records',
     'generated_row_operations','replayed_row_operations','supports',
     'generation_beta_candidates','audit_beta_candidates',
     'generation_parity_row_tests','audit_parity_row_tests'}
+
+
 REFERENCE_COUNTERS = PREFLIGHT_COUNTERS - {'supports','generation_beta_candidates',
     'audit_beta_candidates','generation_parity_row_tests','audit_parity_row_tests'}
+
+
 PRODUCER_COUNTERS = {'steps','core_work','core_solves','core_terms'}
+
+
 PRODUCER_CAPS = {'steps':2000000,'core_work':200000000,'core_solves':1000000,'core_terms':100000}
+
+
 REFERENCE_CAPS = {'fiber_points':1000000,'lift_trials':4000000,'solve_calls':100000,
     'certificate_checks':200000,'row_operations':5000000,'work_units':500000000,
     'witness_checks':1000000,'output_records':5000000,
     'generated_row_operations':5000000,'replayed_row_operations':5000000}
+
+
 PREFLIGHT_CAPS = {'fiber_points':0,'lift_trials':0,'witness_checks':0,
     'supports':4495,'generation_beta_candidates':35264,'audit_beta_candidates':35264,
     'generation_parity_row_tests':846336,'audit_parity_row_tests':846336,
     'solve_calls':4495,'certificate_checks':8990,'row_operations':1500000,
     'work_units':50000000,'output_records':2000000,
     'generated_row_operations':1500000,'replayed_row_operations':1500000}
+
+
 EXECUTION_KEYS = {'schema','command','cwd','limits','supervisor_pid','child_pid',
     'child_reaped','parent_death_guard','exit_code','wall_timeout','log_overflow',
     'collector_error','wall_seconds','child_user_cpu_seconds','child_system_cpu_seconds',
     'child_cpu_seconds','supervisor_exclusive_cpu_sample','supervisor_cpu_allocation_charged',
     'supervisor_final_write_tail_measured','child_peak_rss_kib','supervisor_peak_rss_kib',
     'log_bytes_reserved','log_bytes_read','logs','failures'}
+
+
 PAIR_EXCLUSIONS = (('slot',),('python_optimized',),
     ('preflight','resources','wall_seconds'),('producer','resources','wall_seconds'),
     ('verification','resources','wall_seconds'),('resources','worker_wall_seconds'),
@@ -119,80 +127,16 @@
         parse_constant=lambda _x: (_ for _ in ()).throw(ValueError('nonfinite JSON')))
 
 
-def limits():
-    return dict(worker_cpu_soft=60,worker_cpu_hard=75,supervisor_cpu_soft=4,
-        supervisor_cpu_hard=5,worker_address_space_bytes=1024*MIB,
-        supervisor_address_space_bytes=256*MIB,wall_seconds=150,log_max_bytes=LOG_MAX,
-        worker_cpu_allocation=2100,supervisor_cpu_allocation=140,
-        certificate_file_max_bytes=CERT_MAX,certificate_stage_max_bytes=CERT_TOTAL,
-        certificate_stage_max_files=28,report_max_bytes=REPORT_MAX,
-        stage_max_bytes=STAGE_MAX,noncohort_storage_reserved_bytes=NONCOHORT_RESERVE,
-        pair_exclusions=[list(path) for path in PAIR_EXCLUSIONS])
-
-
-def launch_limits():
-    return {key:limits()[key] for key in ('worker_cpu_soft','worker_cpu_hard',
-        'supervisor_cpu_soft','supervisor_cpu_hard','worker_address_space_bytes',
-        'supervisor_address_space_bytes','wall_seconds','log_max_bytes')}
-
-
-def prepare_supervisor_bounds():
-    """Called before argument/source/inventory reads, never at import."""
-    parent=os.getppid()
-    require(type(parent) is int and parent>=1,'positive expected parent PID')
-    libc=ctypes.CDLL(None,use_errno=True)
-    if libc.prctl(1,signal.SIGKILL,0,0,0)!=0:
-        raise OSError(ctypes.get_errno(),'PR_SET_PDEATHSIG')
-    if os.getppid()!=parent:os.kill(os.getpid(),signal.SIGKILL)
-    resource.setrlimit(resource.RLIMIT_CPU,(4,75))
-    resource.setrlimit(resource.RLIMIT_AS,(256*MIB,1024*MIB))
-    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
-    resource.setrlimit(resource.RLIMIT_FSIZE,(CERT_MAX,CERT_MAX))
-
-
-def _load(name,path):
+def _load(name,path,pin):
+    path=Path(path)
+    require(digest_string(pin) and path.is_file() and not path.is_symlink() and path.stat().st_size<=MIB,'bounded pinned bootstrap source')
+    with path.open('rb') as handle:source=handle.read(MIB+1)
+    require(len(source)<=MIB and hashlib.sha256(source).hexdigest()==pin,'authenticated bootstrap bytes')
     spec=importlib.util.spec_from_file_location(name,path)
     require(spec is not None and spec.loader is not None,'explicit module loader')
     module=importlib.util.module_from_spec(spec);sys.modules[name]=module
-    spec.loader.exec_module(module)
+    exec(compile(source,str(path),'exec',dont_inherit=True,optimize=sys.flags.optimize),module.__dict__)
     return module
-
-
-def context(freeze_path,freeze_pin):
-    require(digest_string(freeze_pin),'freeze digest')
-    freeze_path=Path(freeze_path)
-    require(freeze_path==ROOT/'FREEZE.json' and sha(freeze_path,REPORT_MAX)==freeze_pin,'fixed freeze identity')
-    preliminary=read_json(freeze_path)
-    require(type(preliminary) is dict and type(preliminary.get('files')) is dict,'source map required')
-    helper_path=ROOT/'custody_common.py'
-    require(preliminary['files'].get(str(helper_path))==sha(helper_path,REPORT_MAX),'custody helper source pin')
-    common=_load('fresh_residual_supervisor_custody',helper_path)
-    freeze=common.verify_freeze(freeze_path,freeze_pin)
-    require(freeze['schema']==FREEZE_SCHEMA and freeze['limits']==limits(),'frozen supervisor limits')
-    require(list(freeze['jobs'])==list(JOBS),'exact frozen28-slot schedule')
-    require(freeze['files'].get(str(ROOT/'supervisor.py'))==sha(ROOT/'supervisor.py',REPORT_MAX),'supervisor pinned')
-    for slot in JOBS:
-        spec=freeze['jobs'][slot]
-        require(type(spec) is dict and set(spec)=={'script','cwd','command','report_identity'},'job specification schema')
-        case=slot.rsplit('-',1)[0]
-        require(spec['script']==str(ROOT/'worker.py') and spec['cwd']==str(ROOT),'fixed worker source/cwd')
-        identity={'schema':'fixed-data-post-failure-slot-report-v1','slot':slot,'case_id':case,
-                  'python_optimized':slot.endswith('-optimized')}
-        require(spec['report_identity']==identity and type(spec['report_identity'].get('python_optimized')) is bool,'frozen report identity')
-        expected=[freeze['python']['executable'],'-I','-B']
-        if slot.endswith('-optimized'):expected.append('-O')
-        expected += [str(ROOT/'worker.py'),'--job',slot,'--input',freeze['public_paths']['input'],
-            '--input-sha256','${INPUT_PIN}','--output',str(ROOT/'runs'/slot/'result.json')]
-        require(spec['command']==expected,'frozen exact worker argv/template')
-    return common,freeze
-
-
-def expanded_command(spec,input_pin):
-    require(digest_string(input_pin),'input pin')
-    command=spec['command']
-    require(type(command) is list and command.count('${INPUT_PIN}')==1,'one whole-token input substitution')
-    require(all(type(x) is str and ('${' not in x or x=='${INPUT_PIN}') for x in command),'only input pin substitution')
-    return [input_pin if x=='${INPUT_PIN}' else x for x in command]
 
 
 def counter_map(value,names):
@@ -241,87 +185,6 @@
     return value['status']
 
 
-def validate_report(report,spec,freeze,freeze_pin,input_pin):
-    require(type(report) is dict and set(report)==REPORT_KEYS,'exact report schema')
-    require(type(report['python_optimized']) is bool,'strict report mode boolean')
-    require(all(report[key]==value for key,value in spec['report_identity'].items()),'report identity/mode')
-    require(report['freeze_sha256']==freeze_pin and report['input_sha256']==input_pin
-            and report['source_sha256']==freeze['files']
-            and report['origin_manifest_sha256']==freeze['origin_manifest_sha256'],
-            'report new source/original input/origin identity')
-    require(type(report['resources']) is dict and set(report['resources'])=={'worker_wall_seconds','worker_cpu_seconds',
-        'producer_counters','reference_counters','producer_attempted','reference_attempted'} and numeric(report['resources']['worker_wall_seconds'])
-        and numeric(report['resources']['worker_cpu_seconds']),'report resource fields')
-    require(type(report['resources']['producer_attempted']) is bool
-        and type(report['resources']['reference_attempted']) is bool,'strict attempt flags')
-    require(not report['resources']['reference_attempted'] or report['resources']['producer_attempted'],'reference follows producer')
-    bounded_counters(report['resources']['producer_counters'],PRODUCER_CAPS,True)
-    bounded_counters(report['resources']['reference_counters'],REFERENCE_CAPS,True)
-    for name in ('producer','reference'):
-        require(report['resources'][name+'_attempted'] or report['resources'][name+'_counters'] is None,'uncalled stage cannot claim counters')
-    if report['status']=='INCOMPLETE_OR_FAILED':
-        require(all(report[field] is None for field in ('producer','verification','semantic_summary')),'no incomplete semantic claims')
-        if report['preflight'] is not None:
-            require(type(report['preflight']) is dict and type(report['preflight'].get('resources')) is dict,'incomplete preflight resource shape')
-            counter_map(report['preflight']['resources'],PREFLIGHT_COUNTERS)
-            bounded_counters({key:report['preflight']['resources'][key] for key in PREFLIGHT_COUNTERS},PREFLIGHT_CAPS)
-        require(type(report['reason']) is str and 0<len(report['reason'])<=2000,'failure reason')
-        return report['status']
-    require(report['status'] in ACCEPTED and report['reason'] is None,'accepted report status')
-    preflight_status=checked_preflight(report['preflight'])
-    if report['case_id'] in ('G0','G1'):
-        require(report['status']=='CERTIFIED_RESOURCE_GATE','disclosed controls must gate')
-    if report['status']=='CERTIFIED_RESOURCE_GATE':
-        require(preflight_status=='GATE_REJECTED_LOWER_BOUND','gate status linkage')
-        require(all(report[key] is None for key in ('producer','verification','semantic_summary')),'gate has no semantic claim')
-        require(report['resources']['producer_counters'] is None and report['resources']['reference_counters'] is None,'gate has no semantic calls')
-        require(report['resources']['producer_attempted'] is False and report['resources']['reference_attempted'] is False,'gate cannot attempt semantics')
-        return report['status']
-    require(preflight_status=='WORKLOAD_ADMITTED','semantic result needs full admission')
-    require(report['resources']['producer_attempted'] is True and report['resources']['reference_attempted'] is True,'completed semantic calls required')
-    producer=report['producer']
-    require(type(producer) is dict and set(producer)=={'status','resources','stats'}
-            and producer['status']=='EXACT','exact producer summary')
-    counter_map(producer['resources'],PRODUCER_COUNTERS)
-    completion_wall(producer['resources']['wall_seconds'],30)
-    bounded_counters({key:producer['resources'][key] for key in PRODUCER_COUNTERS},PRODUCER_CAPS)
-    require(report['resources']['producer_counters']=={key:producer['resources'][key] for key in PRODUCER_COUNTERS},'producer diagnostic counters match subset')
-    require(type(producer['stats']) is dict and set(producer['stats'])=={'containers','beta_candidates',
-        'incompatible_beta','excluded_B','eligible_pieces','empty_pieces','feasible_pieces'}
-        and all(integer(v) for v in producer['stats'].values()),'producer integer stats')
-    verify=report['verification']
-    require(type(verify) is dict and set(verify)=={'version','source_sha256','request_sha256','status',
-        'resources','pieces_checked','canonical_functions','original_lifts','joint_predictions','stats'},'exact verifier schema')
-    require(verify['version']=='independent-residual-reference-3' and verify['status']=='VERIFIED_EXACT','complete verifier required')
-    require(verify['source_sha256']==freeze['files']['source/scientific/reference_v3.py']
-            and digest_string(verify['request_sha256']),'verifier identity')
-    counter_map(verify['resources'],REFERENCE_COUNTERS)
-    completion_wall(verify['resources']['wall_seconds'],45)
-    bounded_counters({key:verify['resources'][key] for key in REFERENCE_COUNTERS},REFERENCE_CAPS)
-    require(report['resources']['reference_counters']=={key:verify['resources'][key] for key in REFERENCE_COUNTERS},'reference diagnostic counters match subset')
-    require(verify['resources']['row_operations']==verify['resources']['generated_row_operations']+
-        verify['resources']['replayed_row_operations'],'completed reference row-operation subtotals')
-    require(verify['resources']['fiber_points']==report['preflight']['exact_W'],'full verifier exact workload equality')
-    for key in ('pieces_checked','canonical_functions','original_lifts','joint_predictions'):
-        require(integer(verify[key]) and verify[key]>0,'nonempty complete reference count')
-    require(type(verify['stats']) is dict and set(verify['stats'])=={'supports','beta_candidates',
-        'eligible_beta','retained_points','legacy_ambient_points_equivalent'}
-        and all(integer(v) for v in verify['stats'].values()),'reference integer stats')
-    summary=report['semantic_summary']
-    require(type(summary) is dict and set(summary)=={'producer_nontime_sha256','masks','pieces',
-        'canonical_functions','original_lifts','joint_predictions','feasibility_witness'},'exact semantic summary')
-    require(digest_string(summary['producer_nontime_sha256']),'full producer semantic hash')
-    require(type(summary['masks']) is list and len(summary['masks'])==91,'91 verified masks')
-    for mask in summary['masks']:
-        require(type(mask) is list and 1<=len(mask)<=26 and all(integer(v,25) for v in mask)
-                and mask==sorted(set(mask)),'canonical complete scalar mask')
-    for summary_key,verify_key in (('pieces','pieces_checked'),('canonical_functions','canonical_functions'),
-                                  ('original_lifts','original_lifts'),('joint_predictions','joint_predictions')):
-        require(integer(summary[summary_key]) and summary[summary_key]==verify[verify_key],'semantic/reference count linkage')
-    require(type(summary['feasibility_witness']) is dict,'verified nonempty witness retained')
-    return report['status']
-
-
 def pair_projection(report):
     """Exactly frozen field exclusions; all other semantics and counters remain."""
     require(type(report) is dict and set(report)==REPORT_KEYS,'pair report schema')
@@ -349,32 +212,6 @@
     return True
 
 
-def artifact_inventory(jobdir,completed=False):
-    jobdir=Path(jobdir)
-    require(jobdir.is_dir() and not jobdir.is_symlink(),'regular slot directory')
-    entries=[]
-    for path in sorted(jobdir.iterdir()):
-        if path.name in ('resource.json','resource.json.tmp'):
-            require(path.is_file() and not path.is_symlink() and path.stat().st_size<=REPORT_MAX,'bounded resource receipt/partial')
-            if completed:require(path.name=='resource.json','no completed resource partial')
-            continue
-        require(path.name in ARTIFACT_CAPS,'unexpected slot artifact: '+path.name)
-        cap=ARTIFACT_CAPS[path.name]
-        require(path.is_file() and not path.is_symlink() and path.stat().st_size<=cap,'bounded regular slot artifact')
-        entries.append(dict(name=path.name,bytes=path.stat().st_size,sha256=sha(path,cap),
-            classification='certificate_evidence' if path.name=='case.cert.jsonl' else
-                'result' if path.name=='result.json' else 'diagnostic_nonresult'))
-    if completed:
-        require({item['name'] for item in entries}==set(ARTIFACT_CAPS),'complete artifact set')
-    return entries
-
-
-def compare_certificate_claim(report,inventory):
-    actual={item['name']:item for item in inventory}.get('case.cert.jsonl')
-    claim=report['preflight']['certificate']
-    require(actual is not None and claim['bytes']==actual['bytes'] and claim['sha256']==actual['sha256'],'certificate bytes differ from report')
-
-
 def diagnostic_inventory(jobdir):
     """Preserve bounded failed-file metadata; never certify this as complete."""
     entries=[];complete=True
@@ -392,285 +229,414 @@
     return sorted(entries,key=lambda item:item['name']),complete
 
 
-def validate_execution(value,command,cwd):
-    require(type(value) is dict and set(value)==EXECUTION_KEYS
-            and value.get('schema')=='fixed-data-post-failure-bounded-stage-v1','bounded execution schema')
-    require(value.get('command')==command and value.get('cwd')==cwd and value.get('limits')==launch_limits(),'execution invocation/limits')
-    require(type(value.get('exit_code')) is int and value['exit_code']==0,'successful child exit')
-    require(value.get('child_reaped') is True and value.get('parent_death_guard') is True,'child reaped and guarded')
-    require(value.get('wall_timeout') is False and value.get('log_overflow') is False
-            and value.get('collector_error') is None and value.get('failures')==[],'bounded execution failure')
-    require(numeric(value.get('wall_seconds')) and value['wall_seconds']<=150,'finite bounded wall')
-    for key in ('child_user_cpu_seconds','child_system_cpu_seconds','child_cpu_seconds','supervisor_exclusive_cpu_sample'):
-        require(numeric(value.get(key)),'finite CPU component')
-    require(abs(value['child_user_cpu_seconds']+value['child_system_cpu_seconds']-value['child_cpu_seconds'])<=1e-8,'CPU component sum')
-    require(value['child_cpu_seconds']<=75 and value['supervisor_exclusive_cpu_sample']<=5,'nominal CPU ceiling exceeded')
-    require(type(value.get('supervisor_cpu_allocation_charged')) is int
-            and value['supervisor_cpu_allocation_charged']==5
-            and value.get('supervisor_final_write_tail_measured') is False,'supervisor charge/tail distinction')
-    require(all(type(value.get(k)) is int and value[k]>=1 for k in ('supervisor_pid','child_pid'))
-            and value['supervisor_pid']!=value['child_pid'],'distinct positive process IDs')
-    require(all(integer(value.get(k)) for k in ('child_peak_rss_kib','supervisor_peak_rss_kib')),'RSS fields')
-    for key in ('log_bytes_reserved','log_bytes_read'):
-        require(type(value.get(key)) is list and len(value[key])==2 and all(integer(v) for v in value[key]),'log counters')
-    require(all(value['log_bytes_reserved'][i]==value['log_bytes_read'][i]<=LOG_MAX for i in (0,1)),'successful bounded log totals')
-    require(type(value.get('logs')) is list and len(value['logs'])==2,'two log records')
+def prepare_supervisor_bounds():
+    """Constant prelaunch envelope before parsing, source or authority reads.
+
+    CPU soft 4 seconds and memory soft 256 MiB match the smallest supervisor;
+    hard headroom only permits the frozen child fork. After argument parsing
+    these soft limits become the exact job values, and run_bounded lowers the
+    parent hard limits immediately after its one fork.
+    """
+    parent=os.getppid();require(type(parent) is int and parent>=1,'positive parent PID')
+    libc=ctypes.CDLL(None,use_errno=True)
+    if libc.prctl(1,signal.SIGKILL,0,0,0)!=0:raise OSError(ctypes.get_errno(),'PR_SET_PDEATHSIG')
+    if os.getppid()!=parent:os.kill(os.getpid(),signal.SIGKILL)
+    resource.setrlimit(resource.RLIMIT_CPU,(4,75))
+    resource.setrlimit(resource.RLIMIT_AS,(256*MIB,1024*MIB))
+    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
+    resource.setrlimit(resource.RLIMIT_FSIZE,(CERT_MAX,CERT_MAX))
+
+
+def bootstrap(freeze_pin):
+    require(digest_string(freeze_pin) and sha(ROOT/'FREEZE.json',REPORT_MAX)==freeze_pin,'external source freeze pin')
+    freeze=read_json(ROOT/'FREEZE.json')
+    path=ROOT/'common.py'
+    require(type(freeze) is dict and type(freeze.get('files')) is dict and freeze['files'].get(str(path))==sha(path,MIB),'bootstrap common source pin')
+    common=_load('k4_target_common_supervisor',path,freeze['files'][str(path)])
+    return common,common.freeze_context(freeze_pin)
+
+
+def validate_report(report,spec,freeze,freeze_pin,approval_pin):
+    """Strict metadata check of a complete, independently checked relation.
+
+    It does not replace the immutable reference. EMPTY requires the reference's
+    actual VERIFIED_EMPTY and zero relation; a resource gate is not EMPTY.
+    """
+    job=Path(spec['directory']).name
+    require(type(report) is dict and set(report)==REPORT_KEYS,'exact report schema')
+    require(report['schema']=='k4-residual-slot-report-v1' and report['slot']==job and
+        report['stage']==spec['stage'] and report['input_role']==spec['input_key'] and
+        report['case_id']==spec['internal_id'] and type(report['python_optimized']) is bool and
+        report['python_optimized']==spec['optimized'],'report exact role/mode')
+    require(report['freeze_sha256']==freeze_pin and report['approval_sha256']==approval_pin and
+        report['input_sha256']==freeze['inputs'][spec['input_key']]['sha256'] and
+        report['source_sha256']==freeze['files'],'report source/input/approval binding')
+    resources=report['resources']
+    require(type(resources) is dict and set(resources)=={'worker_wall_seconds','worker_cpu_seconds',
+        'producer_counters','reference_counters','producer_attempted','reference_attempted'},'report resource schema')
+    completion_wall(resources['worker_wall_seconds'],150)
+    require(numeric(resources['worker_cpu_seconds']) and resources['worker_cpu_seconds']<=75,'worker subset CPU')
+    require(type(resources['producer_attempted']) is bool and type(resources['reference_attempted']) is bool and
+        (not resources['reference_attempted'] or resources['producer_attempted']),'attempt order')
+    bounded_counters(resources['producer_counters'],PRODUCER_CAPS,True)
+    bounded_counters(resources['reference_counters'],REFERENCE_CAPS,True)
+    for name in ('producer','reference'):
+        require(resources[name+'_attempted'] or resources[name+'_counters'] is None,'no uncalled stage counters')
+    if report['status']=='INCOMPLETE_OR_FAILED':
+        require(all(report[k] is None for k in ('producer','verification','semantic_summary','control_check')),'no incomplete result claims')
+        require(type(report['reason']) is str and 0<len(report['reason'])<=2000,'bounded failure reason')
+        return report['status']
+    require(report['status'] in ('VERIFIED_EXACT','VERIFIED_EMPTY','CERTIFIED_RESOURCE_GATE') and report['reason'] is None,'completed report status')
+    pf_status=checked_preflight(report['preflight'])
+    if report['status']=='CERTIFIED_RESOURCE_GATE':
+        require(spec['stage']=='target' and pf_status=='GATE_REJECTED_LOWER_BOUND','target-only certified resource gate')
+        require(all(report[k] is None for k in ('producer','verification','semantic_summary','control_check')),'gate has no semantic claims')
+        require(resources['producer_attempted'] is False and resources['reference_attempted'] is False and resources['producer_counters'] is None and resources['reference_counters'] is None,'gate cannot call semantics')
+        return report['status']
+    require(pf_status=='WORKLOAD_ADMITTED' and resources['producer_attempted'] and resources['reference_attempted'],'full preflight/producer/reference required')
+    producer=report['producer'];verify=report['verification']
+    require(type(producer) is dict and set(producer)=={'status','resources','stats'},'producer summary schema')
+    wanted='EXACT' if report['status']=='VERIFIED_EXACT' else 'EMPTY'
+    require(producer['status']==wanted,'matching producer status')
+    counter_map(producer['resources'],PRODUCER_COUNTERS);completion_wall(producer['resources']['wall_seconds'],30)
+    bounded_counters({k:producer['resources'][k] for k in PRODUCER_COUNTERS},PRODUCER_CAPS)
+    require(resources['producer_counters']=={k:producer['resources'][k] for k in PRODUCER_COUNTERS},'producer counter linkage')
+    require(type(producer['stats']) is dict and set(producer['stats'])=={'containers','beta_candidates','incompatible_beta','excluded_B','eligible_pieces','empty_pieces','feasible_pieces'} and all(integer(v) for v in producer['stats'].values()),'producer exact integer stats')
+    require(type(verify) is dict and set(verify)=={'version','source_sha256','request_sha256','status','resources','pieces_checked','canonical_functions','original_lifts','joint_predictions','stats'},'exact reference schema')
+    require(verify['version']=='independent-residual-reference-3' and verify['status']==report['status'] and
+        verify['source_sha256']==freeze['files']['source/scientific/reference_v3.py'] and digest_string(verify['request_sha256']),'complete reference identity/status')
+    counter_map(verify['resources'],REFERENCE_COUNTERS);completion_wall(verify['resources']['wall_seconds'],45)
+    bounded_counters({k:verify['resources'][k] for k in REFERENCE_COUNTERS},REFERENCE_CAPS)
+    require(resources['reference_counters']=={k:verify['resources'][k] for k in REFERENCE_COUNTERS},'reference counter linkage')
+    require(verify['resources']['row_operations']==verify['resources']['generated_row_operations']+verify['resources']['replayed_row_operations'] and verify['resources']['fiber_points']==report['preflight']['exact_W'],'complete reference workload and row totals')
+    require(type(verify['stats']) is dict and set(verify['stats'])=={'supports','beta_candidates','eligible_beta','retained_points','legacy_ambient_points_equivalent'} and all(integer(v) for v in verify['stats'].values()),'reference exact integer stats')
+    empty=wanted=='EMPTY'
+    for key in ('pieces_checked','canonical_functions','original_lifts','joint_predictions'):
+        require(integer(verify[key]) and (verify[key]==0 if empty else verify[key]>0),'nonvacuous exact relation counts')
+    summary=report['semantic_summary']
+    require(type(summary) is dict and set(summary)=={'producer_nontime_sha256','masks','pieces','canonical_functions','original_lifts','joint_predictions','feasibility_witness','interpretation'} and digest_string(summary['producer_nontime_sha256']),'full producer summary commitment')
+    require(type(summary['masks']) is list and len(summary['masks'])==91,'91 scalar masks')
+    for mask in summary['masks']:
+        require(type(mask) is list and (len(mask)==0 if empty else 1<=len(mask)<=26) and all(integer(v,25) for v in mask) and mask==sorted(set(mask)),'canonical complete scalar masks')
+    for a,b in (('pieces','pieces_checked'),('canonical_functions','canonical_functions'),('original_lifts','original_lifts'),('joint_predictions','joint_predictions')):
+        require(integer(summary[a]) and summary[a]==verify[b],'reference/summary counts')
+    require(summary['feasibility_witness'] is None if empty else type(summary['feasibility_witness']) is dict,'no vacuous witness')
+    interpretation=summary['interpretation']
+    require(type(interpretation) is dict and set(interpretation)=={'classification','plaintext_masks','example_plaintext_tail','first_six_claimed'} and interpretation['first_six_claimed'] is False,'no first-six/score interpretation fields')
+    plain=interpretation['plaintext_masks']
+    require(type(plain) is list and len(plain)==91,'91 plaintext masks')
+    for original,mask in zip(summary['masks'],plain):
+        require(type(mask) is list and len(mask)==len(original) and all(type(v) is str and len(v)==1 and 'A'<=v<='Z' for v in mask) and mask==sorted(set(mask)),'canonical plaintext mask shape')
+    tail=interpretation['example_plaintext_tail']
+    if empty:
+        require(interpretation['classification']=='EMPTY' and tail is None,'empty is not a candidate or uniqueness')
+    else:
+        require(type(tail) is str and len(tail)==91 and all(v in mask for v,mask in zip(tail,plain)),'one independently verified common-law example')
+        singleton=verify['joint_predictions']==1
+        require(singleton==all(len(mask)==1 for mask in plain),'joint cardinality/marginal nonvacuity agreement')
+        require(interpretation['classification']==('CONDITIONAL_SINGLETON_TAIL' if singleton else 'NONEMPTY_AMBIGUOUS'),'complete relation classification')
+    if spec['stage']=='controls':
+        require(report['status']==spec['expected_status'] and report['control_check']=={'status':'PASS','expected_sha256':freeze['inputs'][spec['input_key']]['expected_sha256']},'actual control exact expectation gate')
+    else:require(report['control_check'] is None,'no target fixture bypass')
+    return report['status']
+
+
+def validate_mock_report(report,spec,freeze,freeze_pin,approval_pin):
+    require(type(report) is dict and set(report)=={'schema','job','freeze_sha256','approval_sha256','python_optimized','status','counts','actual_forbidden_calls','reason'},'exact mock report schema')
+    require(report['schema']=='k4-residual-operational-mock-report-v1' and report['job']==Path(spec['directory']).name and report['freeze_sha256']==freeze_pin and report['approval_sha256']==approval_pin and type(report['python_optimized']) is bool and report['python_optimized']==spec['optimized'],'mock identity')
+    require(report['status']=='PASS' and report['reason'] is None and report['counts']==freeze['mock_counts'],'finite mock completion/counts')
+    require(report['actual_forbidden_calls']=={k:0 for k in ('science_imports','science_calls','case_reads','child_launches','entropy_calls')},'no actual forbidden mock effects')
+    return 'PASS'
+
+
+def validate_seal_report(report,spec,freeze,freeze_pin,approval_pin):
+    keys={'schema','job','freeze_sha256','approval_sha256','status','prior_completed_jobs','artifacts','state_sha256','source_sha256','input_sha256','allocation_charged_before_seal','worker_cpu_seconds_before_seal','seal_own_completion_pending','reason'}
+    require(type(report) is dict and set(report)==keys and report['schema']=='k4-residual-metadata-seal-v1','metadata seal schema')
+    require(report['job']=='seal' and report['freeze_sha256']==freeze_pin and report['approval_sha256']==approval_pin and report['status']=='SEALED_METADATA' and report['reason'] is None,'metadata seal identity/status')
+    require(report['prior_completed_jobs']==list(JOBS[:6]) and report['seal_own_completion_pending'] is True,'six prior finalized slots; own outer receipt pending')
+    require(report['source_sha256']==freeze['files'] and report['input_sha256']=={k:v['sha256'] for k,v in freeze['inputs'].items()} and digest_string(report['state_sha256']),'seal metadata pins only')
+    require(report['allocation_charged_before_seal']==444 and numeric(report['worker_cpu_seconds_before_seal']),'seal allocation before own 12-second slot')
+    wanted={'FREEZE.json','PUBLICATION-CHECKPOINT.json','runs/state.json','runs/IN_FLIGHT.lock'}
+    wanted|={'approvals/'+name+'.json' for name in ('mocks','controls','target','seal')}
+    wanted|={'acceptance/'+name+'.json' for name in ('MOCKS','CONTROLS','TARGET')}
+    for job in JOBS[:6]:
+        wanted.add('external/'+job+'.json')
+        names={'stdout.txt','stderr.txt','result.json','resource.json'}
+        if job in JOBS[2:6]:names.add('case.cert.jsonl')
+        wanted|={'runs/'+job+'/'+name for name in names}
+    require(type(report['artifacts']) is dict and set(report['artifacts'])==wanted,'complete finite seal inventory')
+    for path,record in report['artifacts'].items():
+        require(type(path) is str and type(record) is dict and set(record)=={'bytes','sha256'} and integer(record['bytes'],CERT_MAX) and digest_string(record['sha256']),'seal artifact record')
+    require(report['state_sha256']==report['artifacts']['runs/state.json']['sha256'],'seal state binding')
+    return 'SEALED_METADATA'
+
+
+def validate_execution(value,command,cwd,limits):
+    require(type(value) is dict and set(value)==EXECUTION_KEYS and value['schema']=='k4-residual-bounded-stage-v1','bounded execution schema')
+    require(value['command']==command and value['cwd']==cwd and value['limits']==limits,'execution invocation/limits')
+    require(type(value['exit_code']) is int and value['exit_code']==0 and value['child_reaped'] is True and value['parent_death_guard'] is True,'clean guarded reaped child')
+    require(value['wall_timeout'] is False and value['log_overflow'] is False and value['collector_error'] is None and value['failures']==[],'no execution failures')
+    completion_wall(value['wall_seconds'],limits['wall_seconds'])
+    for k in ('child_user_cpu_seconds','child_system_cpu_seconds','child_cpu_seconds','supervisor_exclusive_cpu_sample'):require(numeric(value[k]),'finite CPU components')
+    require(abs(value['child_user_cpu_seconds']+value['child_system_cpu_seconds']-value['child_cpu_seconds'])<=1e-8,'CPU sum')
+    require(value['child_cpu_seconds']<=limits['worker_cpu_hard'] and value['supervisor_exclusive_cpu_sample']<=limits['supervisor_cpu_hard'],'CPU ceilings')
+    require(type(value['supervisor_cpu_allocation_charged']) is int and value['supervisor_cpu_allocation_charged']==limits['supervisor_cpu_hard'] and value['supervisor_final_write_tail_measured'] is False,'charged supervisor tail not claimed measured')
+    require(all(type(value[k]) is int and value[k]>=1 for k in ('supervisor_pid','child_pid')) and value['supervisor_pid']!=value['child_pid'],'distinct positive PIDs')
+    require(all(integer(value[k]) for k in ('child_peak_rss_kib','supervisor_peak_rss_kib')),'RSS counts')
+    for k in ('log_bytes_reserved','log_bytes_read'):
+        require(type(value[k]) is list and len(value[k])==2 and all(integer(v) for v in value[k]),'log integer counts')
+    require(all(value['log_bytes_reserved'][i]==value['log_bytes_read'][i]<=LOG_MAX for i in (0,1)),'bounded exact log predebit')
+    require(type(value['logs']) is list and len(value['logs'])==2,'two logs')
     jobdir=Path(command[-1]).parent
     for i,name in enumerate(('stdout.txt','stderr.txt')):
         item=value['logs'][i]
-        require(type(item) is dict and set(item)=={'path','bytes','sha256'}
-            and item['path']==str(jobdir/name) and integer(item['bytes'],LOG_MAX)
-            and item['bytes']==value['log_bytes_reserved'][i] and digest_string(item['sha256']),'execution log identity')
-
-
-def validate_receipt(receipt,spec,slot,freeze,freeze_pin,input_pin,approval_pin):
-    required={'schema','slot','case_id','freeze_sha256','input_sha256','run_approval_sha256',
-        'status','execution','inventory','certificate_bytes','certificate_files','artifact_bytes',
-        'mode_pair_checked','failures'}
-    require(type(receipt) is dict and set(receipt)==required,'exact receipt schema')
-    require(receipt['schema']==SCHEMA and receipt['slot']==slot and receipt['case_id']==slot.rsplit('-',1)[0],'receipt identity')
-    require(receipt['freeze_sha256']==freeze_pin and receipt['input_sha256']==input_pin
-            and receipt['run_approval_sha256']==approval_pin,'receipt source/input/approval')
-    require(receipt['status'] in ACCEPTED and receipt['failures']==[],'accepted receipt only')
-    require(type(receipt['mode_pair_checked']) is bool
-            and receipt['mode_pair_checked']==slot.endswith('-optimized'),'pair-check receipt')
-    validate_execution(receipt['execution'],expanded_command(spec,input_pin),spec['cwd'])
-    inventory=receipt['inventory']
-    require(type(inventory) is list and len(inventory)==4,'exact four worker artifacts')
+        require(type(item) is dict and set(item)=={'path','bytes','sha256'} and item['path']==str(jobdir/name) and integer(item['bytes'],LOG_MAX) and item['bytes']==value['log_bytes_reserved'][i] and digest_string(item['sha256']),'exact bounded log record')
+    return True
+
+
+def allocation(job):
+    require(job in JOBS,'fixed allocation job')
+    return 62 if job.startswith('mock-') else 12 if job=='seal' else 80
+
+
+def validate_state_shape(state,freeze_pin,allow_in_flight=False):
+    keys={'schema','freeze_sha256','completed','in_flight','stopped','canceled','worker_cpu_actual','allocation_charged','certificate_bytes','certificate_files','artifact_bytes'}
+    require(type(state) is dict and set(state)==keys and state['schema']==SCHEMA and state['freeze_sha256']==freeze_pin,'state schema/source identity')
+    require(type(state['completed']) is list and len(state['completed'])<=7,'finite completed prefix')
+    for index,record in enumerate(state['completed']):
+        require(type(record) is dict and set(record)=={'job','status','resource_sha256','approval_sha256'} and record['job']==JOBS[index] and record['status'] in ACCEPTED and digest_string(record['resource_sha256']) and digest_string(record['approval_sha256']),'accepted exact prefix record')
+    require(state['stopped'] is False and state['canceled']==[],'stopped state cannot continue')
+    require(numeric(state['worker_cpu_actual']) and integer(state['allocation_charged'],456) and state['allocation_charged']==sum(allocation(r['job']) for r in state['completed']),'allocation exact prefix')
+    require(integer(state['certificate_bytes'],4*CERT_MAX) and integer(state['certificate_files'],4) and integer(state['artifact_bytes'],STAGE_MAX),'state finite evidence totals')
+    if not allow_in_flight:require(state['in_flight'] is None,'no unresolved reserved invocation')
+    elif state['in_flight'] is not None:
+        item=state['in_flight']
+        require(type(item) is dict and set(item)=={'job','allocation_reserved','certificate_bytes_reserved','artifact_bytes_reserved','command','approval_sha256'} and len(state['completed'])<7 and item['job']==JOBS[len(state['completed'])] and item['allocation_reserved']==allocation(item['job']) and digest_string(item['approval_sha256']),'one fixed in-flight reservation')
+        require(item['certificate_bytes_reserved']==(CERT_MAX if item['job'] in JOBS[2:6] else 0) and item['artifact_bytes_reserved']==(38*MIB if item['job'] in JOBS[2:6] else 6*MIB),'fixed evidence reservation')
+        require(type(item['command']) is list and 1<=len(item['command'])<=64 and all(type(v) is str and 0<len(v)<=4096 for v in item['command']),'finite reserved command')
+    return True
+
+
+def require_next_job(state,job):
+    require(state['stopped'] is False and state['in_flight'] is None and state['canceled']==[] and len(state['completed'])<7 and job==JOBS[len(state['completed'])],'only next unused job; no retry')
+    return True
+
+
+def retain_failed_reservation(state,job):
+    """An authorized attempt cannot become reusable when no child was started."""
+    require(job in JOBS and type(state['in_flight']) is dict and state['in_flight'].get('job')==job,'failed attempt retains its own reserve')
+    state['stopped']=True;state['canceled']=list(JOBS[JOBS.index(job)+1:])
+    return state
+
+
+def artifact_inventory(jobdir,kind,completed=False):
+    jobdir=Path(jobdir);require(jobdir.is_dir() and not jobdir.is_symlink(),'regular job directory')
+    wanted=set(ARTIFACT_CAPS) if kind=='science' else set(ARTIFACT_CAPS)-{'case.cert.jsonl'}
+    entries=[]
+    for path in sorted(jobdir.iterdir()):
+        if path.name in ('resource.json','resource.json.tmp'):
+            require(path.is_file() and not path.is_symlink() and path.stat().st_size<=REPORT_MAX,'bounded receipt/partial')
+            if completed:require(path.name=='resource.json','no completed receipt partial')
+            continue
+        require(path.name in wanted,'unexpected job artifact')
+        cap=ARTIFACT_CAPS[path.name]
+        require(path.is_file() and not path.is_symlink() and path.stat().st_size<=cap,'bounded regular artifact')
+        entries.append(dict(name=path.name,bytes=path.stat().st_size,sha256=sha(path,cap),classification='certificate_evidence' if path.name=='case.cert.jsonl' else 'result' if path.name=='result.json' else 'diagnostic_nonresult'))
+    if completed:require({v['name'] for v in entries}==wanted,'complete artifact set')
+    return entries
+
+
+def validate_receipt(receipt,spec,freeze,freeze_pin,approval_pin,common):
+    keys={'schema','job','stage','freeze_sha256','approval_sha256','status','launch_attempted','execution','inventory','certificate_bytes','certificate_files','artifact_bytes','mode_pair_checked','failures'}
+    job=Path(spec['directory']).name
+    require(type(receipt) is dict and set(receipt)==keys and receipt['schema']==SCHEMA and receipt['job']==job and receipt['stage']==spec['stage'] and receipt['freeze_sha256']==freeze_pin and receipt['approval_sha256']==approval_pin,'receipt identity/schema')
+    require(receipt['status'] in ACCEPTED and receipt['failures']==[] and receipt['launch_attempted'] is True and type(receipt['mode_pair_checked']) is bool and receipt['mode_pair_checked']==(job=='K4-optimized'),'accepted receipt/pair status')
+    if spec['kind']=='mock':require(receipt['status']=='PASS','mock receipt status')
+    elif spec['kind']=='seal':require(receipt['status']=='SEALED_METADATA','seal receipt status')
+    elif spec['stage']=='controls':require(receipt['status']==spec['expected_status'],'control receipt status')
+    else:require(receipt['status'] in ('VERIFIED_EXACT','VERIFIED_EMPTY','CERTIFIED_RESOURCE_GATE'),'target receipt status')
+    validate_execution(receipt['execution'],common.expand(spec['command'],freeze_pin,approval_pin),str(ROOT),spec['limits'])
+    inventory=receipt['inventory'];wanted=set(ARTIFACT_CAPS) if spec['kind']=='science' else set(ARTIFACT_CAPS)-{'case.cert.jsonl'}
+    require(type(inventory) is list and len(inventory)==len(wanted),'complete receipt inventory')
     seen=set()
     for item in inventory:
-        require(type(item) is dict and set(item)=={'name','bytes','sha256','classification'},'artifact record schema')
-        name=item['name'];require(type(name) is str and name in ARTIFACT_CAPS and name not in seen,'artifact name uniqueness')
-        seen.add(name)
-        require(integer(item['bytes'],ARTIFACT_CAPS[name]) and digest_string(item['sha256']),'artifact bytes/hash')
-        wanted='certificate_evidence' if name=='case.cert.jsonl' else 'result' if name=='result.json' else 'diagnostic_nonresult'
-        require(item['classification']==wanted,'artifact class')
-    require(seen==set(ARTIFACT_CAPS),'artifact inventory coverage')
-    certificate=next(item for item in inventory if item['name']=='case.cert.jsonl')
-    require(type(receipt['certificate_files']) is int and receipt['certificate_files']==1
-            and receipt['certificate_bytes']==certificate['bytes'],'certificate receipt totals')
-    require(type(receipt['artifact_bytes']) is int and receipt['artifact_bytes']==sum(item['bytes'] for item in inventory),'artifact receipt totals')
-    by_name={item['name']:item for item in inventory}
-    for item in receipt['execution']['logs']:
-        actual=by_name[Path(item['path']).name]
-        require(item['bytes']==actual['bytes'] and item['sha256']==actual['sha256'],'execution/inventory log identity')
-
-
-def validate_state_shape(state,freeze_pin,input_pin,approval_pin,require_terminal=False):
-    keys={'schema','freeze_sha256','input_sha256','run_approval_sha256','completed','paired_cases',
-        'in_flight','stopped','canceled','worker_cpu_actual','supervisor_allocation_charged',
-        'certificate_bytes','certificate_files','artifact_bytes'}
-    require(type(state) is dict and set(state)==keys and state['schema']==SCHEMA,'exact state schema')
-    require(state['freeze_sha256']==freeze_pin and state['input_sha256']==input_pin
-            and state['run_approval_sha256']==approval_pin,'state identity')
-    require(type(state['completed']) is list and len(state['completed'])<=28,'completed list')
-    require(all(type(r) is dict and set(r)=={'slot','status','resource_sha256'}
-        and r['status'] in ACCEPTED and digest_string(r['resource_sha256']) for r in state['completed']),'completed records')
-    require([r['slot'] for r in state['completed']]==list(JOBS[:len(state['completed'])]),'completed exact prefix')
-    require(state['in_flight'] is None and state['stopped'] is False and state['canceled']==[],'stopped/uncertain state')
-    require(state['paired_cases']==list(CASES[:len(state['completed'])//2]),'completed mode pairs')
-    require(numeric(state['worker_cpu_actual']) and state['worker_cpu_actual']<=2100,'state worker CPU')
-    require(type(state['supervisor_allocation_charged']) is int and state['supervisor_allocation_charged']==5*len(state['completed']),'state supervisor allocation')
-    require(integer(state['certificate_bytes'],CERT_TOTAL) and type(state['certificate_files']) is int
-        and state['certificate_files']==len(state['completed']),'state certificate totals')
-    require(integer(state['artifact_bytes'],STAGE_MAX-NONCOHORT_RESERVE),'state artifact bytes')
-    if require_terminal:require(len(state['completed'])==28,'all28 terminal slots required')
-
-
-def inspect_completed(state,freeze,freeze_pin,input_pin,approval_pin,runs,allow_lock=False):
-    """Rehash complete recorded slot tree, without certificate replay or truth."""
-    validate_state_shape(state,freeze_pin,input_pin,approval_pin)
-    runs=Path(runs)
-    allowed={'state.json'}|{record['slot'] for record in state['completed']}
-    if allow_lock:allowed.add('IN_FLIGHT.lock')
-    require({path.name for path in runs.iterdir()}==allowed,'exact root runtime inventory')
-    total_cpu=0.0;total_certificate=0;total_artifacts=0;reports={};artifacts={}
+        require(type(item) is dict and set(item)=={'name','bytes','sha256','classification'},'inventory record schema')
+        name=item['name'];require(name in wanted and name not in seen and integer(item['bytes'],ARTIFACT_CAPS[name]) and digest_string(item['sha256']),'bounded unique artifact')
+        seen.add(name);require(item['classification']==('certificate_evidence' if name=='case.cert.jsonl' else 'result' if name=='result.json' else 'diagnostic_nonresult'),'artifact class')
+    require(seen==wanted,'full artifact inventory')
+    cert=[v for v in inventory if v['name']=='case.cert.jsonl']
+    require(type(receipt['certificate_files']) is int and receipt['certificate_files']==len(cert) and type(receipt['certificate_bytes']) is int and receipt['certificate_bytes']==sum(v['bytes'] for v in cert) and type(receipt['artifact_bytes']) is int and receipt['artifact_bytes']==sum(v['bytes'] for v in inventory),'receipt evidence totals')
+    byname={v['name']:v for v in inventory}
+    for log in receipt['execution']['logs']:
+        item=byname[Path(log['path']).name]
+        require(log['bytes']==item['bytes'] and log['sha256']==item['sha256'],'collector/inventory log pins')
+    return True
+
+
+def report_status(report,spec,freeze,freeze_pin,approval_pin):
+    if spec['kind']=='science':return validate_report(report,spec,freeze,freeze_pin,approval_pin)
+    if spec['kind']=='mock':return validate_mock_report(report,spec,freeze,freeze_pin,approval_pin)
+    return validate_seal_report(report,spec,freeze,freeze_pin,approval_pin)
+
+
+def inspect_completed(state,freeze,freeze_pin,common,validate_reports=True,allow_in_flight=False):
+    """Read-only prior prefix. Metadata sealer selects no report parsing."""
+    validate_state_shape(state,freeze_pin,allow_in_flight)
+    if state['in_flight'] is not None:
+        pending=state['in_flight'];spec=freeze['jobs'][pending['job']]
+        require(pending['command']==common.expand(spec['command'],freeze_pin,pending['approval_sha256']),'in-flight exact frozen command')
+    reports={};artifacts={};cpu=0.0;certbytes=0;certfiles=0;artifactbytes=0
     for record in state['completed']:
-        slot=record['slot'];jobdir=runs/slot;receipt_path=jobdir/'resource.json'
-        require(sha(receipt_path,REPORT_MAX)==record['resource_sha256'],'immutable receipt changed')
-        receipt=read_json(receipt_path)
-        spec=freeze['jobs'][slot]
-        validate_receipt(receipt,spec,slot,freeze,freeze_pin,input_pin,approval_pin)
+        job=record['job'];spec=freeze['jobs'][job];directory=Path(spec['directory'])
+        pin=record['resource_sha256'];approval_pin=record['approval_sha256']
+        require(sha(directory/'resource.json',REPORT_MAX)==pin,'immutable prior receipt')
+        receipt=read_json(directory/'resource.json')
+        validate_receipt(receipt,spec,freeze,freeze_pin,approval_pin,common)
+        common.read_authority(spec['stage'],freeze,freeze_pin,approval_pin)
         require(receipt['status']==record['status'],'state/receipt status')
-        inventory=artifact_inventory(jobdir,True)
-        require(inventory==receipt['inventory'],'filesystem receipt inventory mismatch')
-        report=read_json(jobdir/'result.json')
-        require(validate_report(report,spec,freeze,freeze_pin,input_pin)==receipt['status'],'report/receipt status')
-        compare_certificate_claim(report,inventory)
-        reports[slot]=report
-        if slot.endswith('-optimized'):
-            compare_pair(reports[slot[:-9]+'normal'],report)
-        total_cpu+=receipt['execution']['child_cpu_seconds']
-        total_certificate+=receipt['certificate_bytes']
-        total_artifacts+=receipt['artifact_bytes']+receipt_path.stat().st_size
-        for item in inventory:
-            artifacts[slot+'/'+item['name']]={'bytes':item['bytes'],'sha256':item['sha256']}
-        artifacts[slot+'/resource.json']={'bytes':receipt_path.stat().st_size,'sha256':record['resource_sha256']}
-    require(abs(total_cpu-state['worker_cpu_actual'])<=1e-8,'state actual CPU reconciliation')
-    require(total_certificate==state['certificate_bytes'] and total_artifacts==state['artifact_bytes'],'state byte reconciliation')
-    state_path=runs/'state.json'
-    artifacts['state.json']={'bytes':state_path.stat().st_size,'sha256':sha(state_path,REPORT_MAX)}
-    require(sum(item['bytes'] for item in artifacts.values())<=STAGE_MAX-NONCOHORT_RESERVE,'runtime stage bytes')
+        inventory=artifact_inventory(directory,spec['kind'],True)
+        require(inventory==receipt['inventory'],'immutable prior artifacts')
+        external_pin=common.external_completion(job,freeze_pin,pin)
+        artifacts['external/'+job+'.json']={'bytes':(ROOT/'external'/(job+'.json')).stat().st_size,'sha256':external_pin}
+        if validate_reports:
+            report=read_json(directory/'result.json');require(report_status(report,spec,freeze,freeze_pin,approval_pin)==receipt['status'],'report/receipt status')
+            if spec['kind']=='science':
+                actual=next(item for item in inventory if item['name']=='case.cert.jsonl');claim=report['preflight']['certificate']
+                require(claim['bytes']==actual['bytes'] and claim['sha256']==actual['sha256'],'certificate/report binding')
+            reports[job]=report
+            if job=='K4-optimized':compare_pair(reports['K4-normal'],report)
+        cpu+=receipt['execution']['child_cpu_seconds'];certbytes+=receipt['certificate_bytes'];certfiles+=receipt['certificate_files']
+        artifactbytes+=receipt['artifact_bytes']+(directory/'resource.json').stat().st_size
+        for item in inventory:artifacts['runs/'+job+'/'+item['name']]={'bytes':item['bytes'],'sha256':item['sha256']}
+        artifacts['runs/'+job+'/resource.json']={'bytes':(directory/'resource.json').stat().st_size,'sha256':pin}
+    require(abs(cpu-state['worker_cpu_actual'])<=1e-8 and certbytes==state['certificate_bytes'] and certfiles==state['certificate_files'] and artifactbytes==state['artifact_bytes'],'state resource/byte reconciliation')
     return artifacts,reports
 
 
-def snapshot_terminal(results,input_path,input_pin,freeze_path,freeze_pin,custody_path,custody_pin,
-                      receipts_manifest_path,receipts_manifest_pin):
-    """Read-only complete terminal seal input. No seed/truth read or solver call."""
-    common,freeze=context(freeze_path,freeze_pin)
-    paths=freeze['public_paths'];results=Path(results)
-    require(str(results)==paths['results'] and str(input_path)==paths['input']
-            and str(custody_path)==paths['custody'],'terminal frozen public paths')
-    require(sha(input_path,262144)==input_pin and sha(custody_path,REPORT_MAX)==custody_pin,'terminal input/custody pins')
-    custody=read_json(custody_path)
-    require(custody.get('public_sha256')==input_pin and custody.get('freeze_sha256')==freeze_pin,'custody input/source binding')
-    approval_path=Path(paths['run_approval']);approval_pin=sha(approval_path,REPORT_MAX)
-    approval=read_json(approval_path)
-    common.validate_run_approval(approval,freeze,freeze_pin,input_pin,custody_pin)
-    require(approval['draw_approval_sha256']==custody.get('draw_approval_sha256'),'custody consumed-draw identity')
-    manifest_path=Path(receipts_manifest_path)
-    require(manifest_path.is_absolute() and manifest_path.resolve()==manifest_path,'canonical absolute receipt manifest path')
-    require(results not in manifest_path.parents and manifest_path!=results,'receipt manifest outside result inventory')
-    require(sha(manifest_path,REPORT_MAX)==receipts_manifest_pin,'external receipt manifest hash')
-    manifest=read_json(manifest_path)
-    require(type(manifest) is dict and set(manifest)=={'schema','freeze_sha256','input_sha256',
-        'run_approval_sha256','state_sha256','receipts'} and manifest['schema']=='fixed-data-post-failure-receipts-manifest-v1','receipt manifest schema')
-    require(manifest['freeze_sha256']==freeze_pin and manifest['input_sha256']==input_pin
-            and manifest['run_approval_sha256']==approval_pin,'receipt manifest bindings')
-    state_path=results/'state.json'
-    require(sha(state_path,REPORT_MAX)==manifest['state_sha256'],'externally pinned state')
-    state=read_json(state_path)
-    validate_state_shape(state,freeze_pin,input_pin,approval_pin,True)
-    require(type(manifest['receipts']) is dict and manifest['receipts']==
-        {record['slot']:record['resource_sha256'] for record in state['completed']},'external exact receipt set')
-    artifacts,_reports=inspect_completed(state,freeze,freeze_pin,input_pin,approval_pin,results)
-    return dict(schema='fixed-data-post-failure-terminal-snapshot-v1',freeze_sha256=freeze_pin,
-        input_sha256=input_pin,custody_sha256=custody_pin,run_approval_sha256=approval_pin,
-        receipts_manifest_path=str(manifest_path),receipts_manifest_sha256=receipts_manifest_pin,artifacts=artifacts,
-        worker_cpu_seconds=state['worker_cpu_actual'],supervisor_allocation_seconds=state['supervisor_allocation_charged'],
-        certificate_bytes=state['certificate_bytes'],certificate_files=state['certificate_files'])
-
-
 def main(argv=None):
+    parser=argparse.ArgumentParser(description='One explicitly granted frozen job; no implicit runs.')
+    for name in ('job','freeze-sha256','approval-sha256'):parser.add_argument('--'+name,required=True)
+    args=parser.parse_args(argv)  # --help exits before guards, files or processes.
+    require(args.job in JOBS,'fixed job only')
     prepare_supervisor_bounds()
-    parser=argparse.ArgumentParser()
-    for name in ('job','approval','approval-sha256','input','input-sha256','freeze-sha256'):
-        parser.add_argument('--'+name,required=True)
-    args=parser.parse_args(argv)
-    require(args.job in JOBS,'fixed slot only')
-    common,freeze=context(ROOT/'FREEZE.json',args.freeze_sha256)
-    paths=freeze['public_paths'];runs=Path(paths['results'])
-    require(args.input==paths['input'] and args.approval==paths['run_approval'],'frozen public invocation paths')
-    require(sha(args.input,262144)==args.input_sha256 and sha(args.approval,REPORT_MAX)==args.approval_sha256,'input/run approval seals')
-    approval=read_json(args.approval);custody_pin=sha(paths['custody'],REPORT_MAX)
-    common.validate_run_approval(approval,freeze,args.freeze_sha256,args.input_sha256,custody_pin)
-    custody=read_json(paths['custody'])
-    require(custody.get('public_sha256')==args.input_sha256 and custody.get('freeze_sha256')==args.freeze_sha256
-            and custody.get('draw_approval_sha256')==approval['draw_approval_sha256'],'public custody linkage')
-    bounded=common.load_pinned('fresh_residual_bounded_supervisor',ROOT/'bounded_stage.py',freeze)
-    bounded.death_guard()
-    runs.mkdir(exist_ok=True)
-    require(not runs.is_symlink(),'regular runs root')
+    if args.job.startswith('mock-'):
+        resource.setrlimit(resource.RLIMIT_CPU,(30,75));resource.setrlimit(resource.RLIMIT_AS,(512*MIB,1024*MIB))
+    elif args.job=='seal':
+        resource.setrlimit(resource.RLIMIT_CPU,(5,75));resource.setrlimit(resource.RLIMIT_AS,(512*MIB,1024*MIB))
+    common,freeze=bootstrap(args.freeze_sha256);spec=freeze['jobs'][args.job]
+    actual=list(sys.argv[1:] if argv is None else argv)
+    require(sys.flags.isolated==1 and sys.dont_write_bytecode is True and sys.flags.optimize==0 and
+        sys.orig_argv==common.expand(spec['launch_command'],args.freeze_sha256,args.approval_sha256) and
+        common.actual_command(ROOT/'supervisor.py',actual)==common.expand(spec['launch_command'],args.freeze_sha256,args.approval_sha256) and Path.cwd()==ROOT,'exact isolated supervisor command')
+    common.read_authority(spec['stage'],freeze,args.freeze_sha256,args.approval_sha256)
+    bounded=common.load_pinned('k4_target_bounded_supervisor',ROOT/'bounded_stage.py',freeze['files'][str(ROOT/'bounded_stage.py')])
+    runs=ROOT/'runs';runs.mkdir(exist_ok=True);require(not runs.is_symlink(),'regular runs root')
     lock=runs/'IN_FLIGHT.lock';state_path=runs/'state.json'
-    bounded.write_new(lock,dict(schema='fixed-data-post-failure-slot-lock-v1',slot=args.job,
-        freeze_sha256=args.freeze_sha256,run_approval_sha256=args.approval_sha256))
+    require(not lock.exists() and not lock.is_symlink(),'one-use unresolved lock blocks every successor')
+    reports={}
     if state_path.exists():
         state=read_json(state_path)
-        inspect_completed(state,freeze,args.freeze_sha256,args.input_sha256,args.approval_sha256,runs,True)
+        _artifacts,reports=inspect_completed(state,freeze,args.freeze_sha256,common)
+        require({p.name for p in runs.iterdir()}=={'state.json'}|{r['job'] for r in state['completed']},'exact immutable completed directory prefix')
     else:
-        require(args.job==JOBS[0] and {p.name for p in runs.iterdir()}=={'IN_FLIGHT.lock'},'fresh first-slot directory')
-        state=dict(schema=SCHEMA,freeze_sha256=args.freeze_sha256,input_sha256=args.input_sha256,
-            run_approval_sha256=args.approval_sha256,completed=[],paired_cases=[],in_flight=None,
-            stopped=False,canceled=[],worker_cpu_actual=0.0,supervisor_allocation_charged=0,
-            certificate_bytes=0,certificate_files=0,artifact_bytes=0)
-    require(len(state['completed'])<28 and args.job==JOBS[len(state['completed'])],'only next unconsumed slot')
-    require(state['worker_cpu_actual']+75<=2100 and state['supervisor_allocation_charged']+5<=140,'CPU reservation unavailable')
-    require(state['certificate_bytes']+CERT_MAX<=CERT_TOTAL and state['certificate_files']<28,'certificate reservation unavailable')
-    require(state['artifact_bytes']+40*MIB+REPORT_MAX<=STAGE_MAX-NONCOHORT_RESERVE,'stage byte reservation unavailable')
-    jobdir=runs/args.job;jobdir.mkdir()
-    spec=freeze['jobs'][args.job];command=expanded_command(spec,args.input_sha256)
-    state['in_flight']=dict(slot=args.job,worker_cpu_reserved=75,supervisor_cpu_reserved=5,
-        certificate_bytes_reserved=CERT_MAX,artifact_bytes_reserved=40*MIB,command=command)
-    bounded.atomic(state_path,state)
-    execution=bounded.run_bounded(command,spec['cwd'],jobdir/'stdout.txt',jobdir/'stderr.txt',launch_limits())
-    failures=list(execution['failures']);report=None;status='INCOMPLETE_OR_FAILED';pair_checked=False
+        require(args.job==JOBS[0] and list(runs.iterdir())==[],'fresh first-job namespace')
+        state=dict(schema=SCHEMA,freeze_sha256=args.freeze_sha256,completed=[],in_flight=None,stopped=False,canceled=[],worker_cpu_actual=0.0,allocation_charged=0,certificate_bytes=0,certificate_files=0,artifact_bytes=0)
+    require_next_job(state,args.job)
+    reserve_bytes=38*MIB if spec['kind']=='science' else 6*MIB
+    command=common.expand(spec['command'],args.freeze_sha256,args.approval_sha256)
+    reservation=dict(job=args.job,allocation_reserved=allocation(args.job),certificate_bytes_reserved=CERT_MAX if spec['kind']=='science' else 0,artifact_bytes_reserved=reserve_bytes,command=command,approval_sha256=args.approval_sha256)
+    # Marker itself carries the full reserve if a later state write is interrupted.
+    bounded.write_new(lock,dict(schema='k4-residual-one-use-lock-v1',freeze_sha256=args.freeze_sha256,reservation=reservation))
+    state['in_flight']=reservation;bounded.atomic(state_path,state)
+    reserved_state_pin=sha(state_path,REPORT_MAX);lock_pin=sha(lock,REPORT_MAX)
+    jobdir=Path(spec['directory']);jobdir.mkdir();bounded.fsync_dir(runs)
+    execution=None;report=None;inventory=[];failures=[];status='INCOMPLETE_OR_FAILED';pair_checked=False;launch_attempted=False
     try:
+        require(state['allocation_charged']+allocation(args.job)<=456,'runtime allocation unavailable')
+        if spec['kind']=='science':
+            require(state['certificate_files']<4 and state['certificate_bytes']+CERT_MAX<=4*CERT_MAX,'four certificate reservations')
+            # Only after durable consumption: a bad/missing authorized raw file
+            # is an INCOMPLETE attempt with no child, never a reusable slot.
+            item=freeze['inputs'][spec['input_key']]
+            require(common.sha(item['path'],common.RAW_MAX)==item['sha256'],'active raw source pin')
+            if spec['stage']=='controls':require(common.sha(item['expected_path'],common.RAW_MAX)==item['expected_sha256'],'active expected fixture pin')
+        require(common.disk_bytes(freeze)+reserve_bytes+REPORT_MAX<=STAGE_MAX,'stage disk reservation unavailable')
+        launch_attempted=True
+        execution=bounded.run_bounded(command,str(ROOT),jobdir/'stdout.txt',jobdir/'stderr.txt',spec['limits'])
+        failures.extend(execution['failures'])
+        validate_execution(execution,command,str(ROOT),spec['limits'])
         report=read_json(jobdir/'result.json')
-        status=validate_report(report,spec,freeze,args.freeze_sha256,args.input_sha256)
-        if status=='INCOMPLETE_OR_FAILED':failures.append('worker_incomplete:'+report['reason'][:200])
-    except (OSError,ValueError,TypeError,KeyError,MemoryError) as error:
-        failures.append('worker_report:'+type(error).__name__+':'+str(error)[:200])
-    inventory=[]
-    try:
-        inventory=artifact_inventory(jobdir,status in ACCEPTED)
-        if status in ACCEPTED:compare_certificate_claim(report,inventory)
-    except (OSError,ValueError,TypeError,KeyError,MemoryError) as error:
-        failures.append('artifact_inventory:'+type(error).__name__+':'+str(error)[:200])
+        status=report_status(report,spec,freeze,args.freeze_sha256,args.approval_sha256)
+        require(status in ACCEPTED,'worker incomplete or invalid')
+        inventory=artifact_inventory(jobdir,spec['kind'],True)
+        if spec['kind']=='science':
+            cert=next(v for v in inventory if v['name']=='case.cert.jsonl');claim=report['preflight']['certificate']
+            require(cert['bytes']==claim['bytes'] and cert['sha256']==claim['sha256'],'complete certificate bytes match report')
+            require(report['resources']['worker_cpu_seconds']<=execution['child_cpu_seconds']+0.001,'inner worker timer is a subset of inclusive OS CPU')
+        if args.job=='K4-optimized':
+            compare_pair(reports['K4-normal'],report);pair_checked=True
+        if args.job=='mock-optimized':
+            previous=reports['mock-normal']
+            require(previous['counts']==report['counts'] and previous['actual_forbidden_calls']==report['actual_forbidden_calls'],'mock mode obligation agreement')
+        common.freeze_context(args.freeze_sha256)
+        common.read_authority(spec['stage'],freeze,args.freeze_sha256,args.approval_sha256)
+        require(sha(state_path,REPORT_MAX)==reserved_state_pin and sha(lock,REPORT_MAX)==lock_pin,'reserved state/one-use marker changed')
+        # Reauthenticate every consumed receipt/outer completion and artifact;
+        # an earlier result cannot change while a successor executes.
+        inspect_completed(state,freeze,args.freeze_sha256,common,True,True)
+        if spec['kind']=='science':
+            item=freeze['inputs'][spec['input_key']]
+            require(common.sha(item['path'],common.RAW_MAX)==item['sha256'],'post-run active input seal')
+            if spec['stage']=='controls':require(common.sha(item['expected_path'],common.RAW_MAX)==item['expected_sha256'],'post-run active control expectation seal')
+        require(common.disk_bytes(freeze)+REPORT_MAX<=STAGE_MAX,'post-run disk closeout reserve')
+    except BaseException as error:
+        failures.append(type(error).__name__+':'+str(error)[:400]);status='INCOMPLETE_OR_FAILED'
+        retain_failed_reservation(state,args.job)
+        if not launch_attempted:
+            # No fork needs inherited headroom on this failed prelaunch path.
+            resource.setrlimit(resource.RLIMIT_CPU,(spec['limits']['supervisor_cpu_soft'],spec['limits']['supervisor_cpu_hard']))
+            memory=spec['limits']['supervisor_address_space_bytes']
+            resource.setrlimit(resource.RLIMIT_AS,(memory,memory))
         try:
-            inventory,diagnostic_complete=diagnostic_inventory(jobdir)
-            if not diagnostic_complete:failures.append('diagnostic_inventory_incomplete_retained_reserve')
-        except (OSError,ValueError,TypeError,MemoryError) as diagnostic_error:
-            failures.append('diagnostic_inventory_unavailable:'+str(diagnostic_error)[:200])
-    if not failures and args.job.endswith('-optimized'):
-        try:
-            previous=state['completed'][-1]
-            previous_dir=runs/previous['slot']
-            require(sha(previous_dir/'resource.json',REPORT_MAX)==previous['resource_sha256'],'normal receipt changed during optimized slot')
-            previous_receipt=read_json(previous_dir/'resource.json')
-            normal_claim=next(item for item in previous_receipt['inventory'] if item['name']=='result.json')
-            require(sha(previous_dir/'result.json',REPORT_MAX)==normal_claim['sha256'],'normal result changed during optimized slot')
-            normal=read_json(previous_dir/'result.json')
-            compare_pair(normal,report);pair_checked=True
-        except (OSError,ValueError,TypeError,KeyError,MemoryError) as error:
-            failures.append('mode_pair:'+str(error)[:200])
-    try:
-        common.verify_freeze(ROOT/'FREEZE.json',args.freeze_sha256)
-        require(sha(args.input,262144)==args.input_sha256 and sha(args.approval,REPORT_MAX)==args.approval_sha256
-            and sha(paths['custody'],REPORT_MAX)==custody_pin,'post-run public pin change')
-    except (OSError,ValueError,TypeError,KeyError,MemoryError) as error:
-        failures.append('post_run_source_input:'+str(error)[:200])
-    own=resource.getrusage(resource.RUSAGE_SELF)
-    execution['supervisor_exclusive_cpu_sample']=own.ru_utime+own.ru_stime
-    execution['supervisor_peak_rss_kib']=own.ru_maxrss
-    if not numeric(execution['supervisor_exclusive_cpu_sample']) or execution['supervisor_exclusive_cpu_sample']>5:
-        failures.append('supervisor_closeout_cpu_invalid_or_overshoot')
+            inventory,complete=diagnostic_inventory(jobdir)
+            if not complete:failures.append('partial_inventory_incomplete_reserve_retained')
+        except BaseException as diagnostic:
+            failures.append('partial_inventory_unavailable:'+type(diagnostic).__name__+':'+str(diagnostic)[:200])
+    if execution is not None:
+        own=resource.getrusage(resource.RUSAGE_SELF)
+        execution['supervisor_exclusive_cpu_sample']=own.ru_utime+own.ru_stime
+        execution['supervisor_peak_rss_kib']=own.ru_maxrss
+        if not numeric(execution['supervisor_exclusive_cpu_sample']) or execution['supervisor_exclusive_cpu_sample']>spec['limits']['supervisor_cpu_hard']:failures.append('supervisor_closeout_cpu_invalid_or_overshoot')
     if failures:status='INCOMPLETE_OR_FAILED'
-    cert_items=[item for item in inventory if item['name']=='case.cert.jsonl']
-    cert_bytes=sum(item['bytes'] for item in cert_items)
-    receipt=dict(schema=SCHEMA,slot=args.job,case_id=args.job.rsplit('-',1)[0],
-        freeze_sha256=args.freeze_sha256,input_sha256=args.input_sha256,
-        run_approval_sha256=args.approval_sha256,status=status,execution=execution,
-        inventory=inventory,certificate_bytes=cert_bytes,certificate_files=len(cert_items),
-        artifact_bytes=sum(item['bytes'] for item in inventory),mode_pair_checked=pair_checked,failures=failures)
-    if not failures:validate_receipt(receipt,spec,args.job,freeze,args.freeze_sha256,args.input_sha256,args.approval_sha256)
+    cert=[v for v in inventory if v['name']=='case.cert.jsonl']
+    receipt=dict(schema=SCHEMA,job=args.job,stage=spec['stage'],freeze_sha256=args.freeze_sha256,
+        approval_sha256=args.approval_sha256,status=status,launch_attempted=launch_attempted,execution=execution,inventory=inventory,
+        certificate_bytes=sum(v['bytes'] for v in cert),certificate_files=len(cert),
+        artifact_bytes=sum(v['bytes'] for v in inventory),mode_pair_checked=pair_checked,failures=failures)
+    if not failures:validate_receipt(receipt,spec,freeze,args.freeze_sha256,args.approval_sha256,common)
     receipt_path=jobdir/'resource.json'
     if receipt_path.exists() or receipt_path.with_name('resource.json.tmp').exists():
-        state['stopped']=True;state['canceled']=list(JOBS[len(state['completed'])+1:])
-        bounded.atomic(state_path,state)
-        raise ValueError('worker wrote a supervisor-only receipt path; preserved without replacement')
+        retain_failed_reservation(state,args.job);bounded.atomic(state_path,state)
+        raise ValueError('worker touched supervisor-only receipt path; preserve it and reserve')
     bounded.atomic(receipt_path,receipt)
-    state['worker_cpu_actual']+=execution['child_cpu_seconds']
-    state['supervisor_allocation_charged']+=5
-    state['certificate_bytes']+=cert_bytes;state['certificate_files']+=len(cert_items)
+    if execution is not None and numeric(execution.get('child_cpu_seconds')):state['worker_cpu_actual']+=execution['child_cpu_seconds']
+    state['allocation_charged']+=allocation(args.job)
+    state['certificate_bytes']+=receipt['certificate_bytes'];state['certificate_files']+=receipt['certificate_files']
     state['artifact_bytes']+=receipt['artifact_bytes']+receipt_path.stat().st_size
-    state['completed'].append(dict(slot=args.job,status=status,resource_sha256=sha(receipt_path,REPORT_MAX)))
-    if not failures:
-        state['in_flight']=None
-        if pair_checked:state['paired_cases'].append(receipt['case_id'])
+    state['completed'].append(dict(job=args.job,status=status,resource_sha256=sha(receipt_path,REPORT_MAX),approval_sha256=args.approval_sha256))
+    if not failures:state['in_flight']=None
     else:
-        # Conservatively retain reservation even when OS use is known; no retry.
-        state['stopped']=True;state['canceled']=list(JOBS[len(state['completed']):])
+        # Final failure receipt and partials are immutable; reserve/marker remain.
+        # No subsequent command may consume this failed slot or its successor.
+        retain_failed_reservation(state,args.job)
     bounded.atomic(state_path,state)
-    if not failures:
-        lock.unlink();bounded.fsync_dir(runs)
+    if not failures:lock.unlink();bounded.fsync_dir(runs)
     return 0 if not failures else 1
 
 
 if __name__=='__main__':
-    try:
-        sys.exit(main())
+    try:sys.exit(main())
     except BaseException as error:
         if isinstance(error,SystemExit):raise
-        os.write(2,canonical({'schema':'fixed-data-post-failure-supervisor-error-v1',
-            'type':type(error).__name__,'message':str(error)[:400]})[:1024])
+        os.write(2,canonical({'schema':'k4-residual-supervisor-error-v1','type':type(error).__name__,'message':str(error)[:400]})[:1024])
         sys.exit(1)
```

## New operational source: common.py
```diff
--- /dev/null
+++ source/operational/common.py
@@ -0,0 +1,359 @@
+"""Target-stage operational identities and permission guards; inert at import.
+
+No raw source input is read by source verification. Raw input is a separately
+authorized capability of one exact scheduled science job, never a source file.
+All approval, acceptance and external-completion objects are parent-owned and
+are deliberately not created by this module or any worker.
+"""
+import ctypes
+import hashlib
+import importlib.util
+import json
+import math
+import os
+from pathlib import Path
+import resource
+import signal
+import sys
+
+ROOT = Path('original-execution-namespace')
+MIB = 1024 * 1024
+JSON_MAX = 2 * MIB
+RAW_MAX = 262144
+LOG_MAX = MIB
+CERT_MAX = 32 * MIB
+STAGE_MAX = 256 * MIB
+FREEZE_SCHEMA = 'k4-residual-target-source-freeze-v1'
+JOBS = ('mock-normal','mock-optimized','CTRL-positive-normal','CTRL-empty-normal',
+        'K4-normal','K4-optimized','seal')
+STAGE_JOBS = {'mocks':JOBS[:2], 'controls':JOBS[2:4], 'target':JOBS[4:6], 'seal':JOBS[6:]}
+INPUT_ROLES = {'positive':'v000','empty':'v001','K4':'v002'}
+SCIENCE = {
+    'source/scientific/residual_decoder.py':'be050003b9a73c14a7f7dda44afeb160e0e847045d57ddfa4b9527bdc68f7d67',
+    'source/scientific/affine_filter.py':'1e19e9ad872d517487cfe7968a9f4b906756007d5e710be216807620f078c90d',
+    'source/scientific/reference_v3.py':'0730f8b0a26109919ba6eb558be18063d137ced233b397cd188dc261a13fe8f9',
+    'source/scientific/preflight_blind.py':'7f1929c0bd3c29a4e972f814e1fa1ade045a33e4b1cfc629e0b696c7b71dfe43',
+    'source/scientific/checker_blind.py':'065e3c29d2705c706b44a553bd9013b10c84751251145a4a683b940962ecc5c6',
+    'source/scientific/CAPS.json':'912461b0b97d4ad9738b830cf6130788e9295f9a92901a5af1664e9f3875a9d4'}
+TARGET_PATH = 'https://github.com/reggiechan74/kryptos-k4/blob/7b9075daa6aee50187b18794b1d3c97e6d840249/data/k4.json'
+TARGET_PIN = '08a1a84bd0dddf2449a2c7f67ee770d093ed47f6ad9a795630b77a2c8062f241'
+LOCAL_SOURCES = ('common.py','bounded_stage.py','worker.py','supervisor.py',
+                 'protocol_mock_tests.py','seal_results.py','input_check.py')
+
+
+def require(condition,message):
+    if not condition:
+        raise ValueError(message)
+
+
+def integer(value,maximum=None):
+    return type(value) is int and value >= 0 and (maximum is None or value <= maximum)
+
+
+def numeric(value):
+    return (type(value) is int and value >= 0) or (type(value) is float and math.isfinite(value) and value >= 0)
+
+
+def digest_string(value):
+    return type(value) is str and len(value)==64 and all(c in '0123456789abcdef' for c in value)
+
+
+def canonical(value):
+    return (json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
+
+
+def unique_object(pairs):
+    out={}
+    for key,value in pairs:
+        require(key not in out,'duplicate JSON key')
+        out[key]=value
+    return out
+
+
+def sha(path,limit=JSON_MAX):
+    path=Path(path)
+    require(path.is_file() and not path.is_symlink(),'bounded regular hash input')
+    size=path.stat().st_size
+    require(integer(size,limit),'bounded hash size')
+    h=hashlib.sha256();total=0
+    with path.open('rb') as f:
+        while True:
+            data=f.read(min(MIB,limit+1))
+            if not data:break
+            require(len(data)<=limit-total,'hash input grew beyond cap')
+            total+=len(data);h.update(data)
+    require(total==size,'hash input size changed')
+    return h.hexdigest()
+
+
+def read_json(path,limit=JSON_MAX,pin=None):
+    path=Path(path)
+    require(path.is_file() and not path.is_symlink() and path.stat().st_size<=limit,'bounded regular JSON input')
+    with path.open('rb') as f:data=f.read(limit+1)
+    require(len(data)<=limit,'JSON input grew beyond cap')
+    if pin is not None:
+        require(digest_string(pin) and hashlib.sha256(data).hexdigest()==pin,'JSON input hash mismatch')
+    return json.loads(data,object_pairs_hook=unique_object,
+        parse_constant=lambda _x:(_ for _ in ()).throw(ValueError('nonfinite JSON')))
+
+
+def fsync_dir(path):
+    fd=os.open(str(path),os.O_RDONLY|os.O_DIRECTORY)
+    try:os.fsync(fd)
+    finally:os.close(fd)
+
+
+def write_new(path,value,limit=JSON_MAX):
+    path=Path(path);data=canonical(value)
+    require(len(data)<=limit,'JSON output cap')
+    require(path.parent.is_dir() and not path.parent.is_symlink(),'regular existing output parent')
+    with path.open('xb') as f:
+        require(f.write(data)==len(data),'short JSON write');f.flush();os.fsync(f.fileno())
+    fsync_dir(path.parent)
+
+
+def atomic(path,value):
+    path=Path(path);temporary=path.with_name(path.name+'.tmp')
+    write_new(temporary,value)
+    os.replace(temporary,path);fsync_dir(path.parent)
+
+
+def load_pinned(name,path,pin):
+    path=Path(path)
+    require(digest_string(pin) and path.is_file() and not path.is_symlink() and path.stat().st_size<=MIB,'bounded pinned module source')
+    with path.open('rb') as handle:source=handle.read(MIB+1)
+    require(len(source)<=MIB and hashlib.sha256(source).hexdigest()==pin,'pinned module source changed')
+    spec=importlib.util.spec_from_file_location(name,path)
+    require(spec is not None and spec.loader is not None,'module loader unavailable')
+    module=importlib.util.module_from_spec(spec);sys.modules[name]=module
+    # Execute these authenticated bytes, never an importlib bytecode cache.
+    exec(compile(source,str(path),'exec',dont_inherit=True,optimize=sys.flags.optimize),module.__dict__)
+    return module
+
+
+def stage_limits(stage):
+    require(stage in STAGE_JOBS,'known stage')
+    if stage in ('controls','target'):
+        return dict(worker_cpu_soft=60,worker_cpu_hard=75,supervisor_cpu_soft=4,
+            supervisor_cpu_hard=5,worker_address_space_bytes=1024*MIB,
+            supervisor_address_space_bytes=256*MIB,wall_seconds=150,log_max_bytes=LOG_MAX)
+    cpu=30 if stage=='mocks' else 5
+    return dict(worker_cpu_soft=cpu,worker_cpu_hard=cpu+1,supervisor_cpu_soft=cpu,
+        supervisor_cpu_hard=cpu+1,worker_address_space_bytes=512*MIB,
+        supervisor_address_space_bytes=512*MIB,wall_seconds=120,log_max_bytes=LOG_MAX)
+
+
+def job_identity(job):
+    require(job in JOBS,'only fixed job')
+    stage=next(stage for stage,jobs in STAGE_JOBS.items() if job in jobs)
+    kind='mock' if stage=='mocks' else 'seal' if stage=='seal' else 'science'
+    key='positive' if job=='CTRL-positive-normal' else 'empty' if job=='CTRL-empty-normal' else 'K4' if stage=='target' else None
+    return stage,kind,key,None if key is None else INPUT_ROLES[key],job.endswith('-optimized')
+
+
+def expand(command,freeze_pin,approval_pin):
+    require(digest_string(freeze_pin) and digest_string(approval_pin),'command commitment pins')
+    require(type(command) is list and 1<=len(command)<=64 and all(type(v) is str and 0<len(v)<=4096 for v in command),'finite argv')
+    mapping={'${FREEZE_PIN}':freeze_pin,'${APPROVAL_PIN}':approval_pin}
+    require(command.count('${FREEZE_PIN}')==1 and command.count('${APPROVAL_PIN}')==1,'exact whole-token pins')
+    require(all('${' not in v or v in mapping for v in command),'only declared whole-token pins')
+    return [mapping.get(v,v) for v in command]
+
+
+def expected_job(freeze,job):
+    stage,kind,key,inner,optimized=job_identity(job)
+    script=ROOT/('protocol_mock_tests.py' if kind=='mock' else 'seal_results.py' if kind=='seal' else 'worker.py')
+    directory=ROOT/'runs'/job;output=directory/'result.json'
+    flags=[freeze['python']['executable'],'-I','-B']+(['-O'] if optimized else [])
+    args=['--job',job,'--freeze-sha256','${FREEZE_PIN}','--approval-sha256','${APPROVAL_PIN}']
+    child=flags+[str(script)]+args+['--output',str(output)]
+    launch=[freeze['python']['executable'],'-I','-B',str(ROOT/'supervisor.py')]+args
+    status='PASS' if kind=='mock' else 'SEALED_METADATA' if kind=='seal' else 'VERIFIED_EXACT' if key=='positive' else 'VERIFIED_EMPTY' if key=='empty' else 'TARGET_CLASSIFIED'
+    return dict(stage=stage,kind=kind,input_key=key,internal_id=inner,optimized=optimized,
+        script=str(script),command=child,launch_command=launch,directory=str(directory),
+        output=str(output),limits=stage_limits(stage),expected_status=status)
+
+
+def validate_input_specs(inputs):
+    require(type(inputs) is dict and set(inputs)==set(INPUT_ROLES),'exact three input identities')
+    for role,inner in INPUT_ROLES.items():
+        item=inputs[role]
+        require(type(item) is dict and set(item)=={'path','sha256','internal_id','expected_path','expected_sha256'},'input metadata schema')
+        require(item['internal_id']==inner and digest_string(item['sha256']),'input identity/pin')
+        if role=='K4':
+            require(item['path']==TARGET_PATH and item['sha256']==TARGET_PIN and item['expected_path'] is None and item['expected_sha256'] is None,'one fixed K4 source only')
+        else:
+            require(item['path']==str(ROOT/'fixtures'/(role+'.json')) and item['expected_path']==str(ROOT/'fixtures'/(role+'-expected.json')) and digest_string(item['expected_sha256']),'fixed disclosed fixture paths')
+
+
+def verify_freeze_object(freeze):
+    keys={'schema','files','python','inputs','jobs','mock_counts','resource_allocation_sha256','protocol_sha256','design_review_sha256'}
+    require(type(freeze) is dict and set(freeze)==keys and freeze['schema']==FREEZE_SCHEMA,'exact freeze schema')
+    p=freeze['python']
+    require(type(p) is dict and set(p)=={'executable','sha256','version'} and Path(p['executable']).is_absolute() and digest_string(p['sha256']) and type(p['version']) is str,'interpreter metadata')
+    require(freeze['protocol_sha256']=='02db816f0510497952a057c246c3297847bb31dfa2c7046caf9483c95c65b170' and freeze['design_review_sha256']=='e3dd87e44a1db6d30be4fca25acea77343ec0772af1d912628ad94dc1bf275ef','reviewed protocol ancestry')
+    require(digest_string(freeze['resource_allocation_sha256']),'resource decision pin')
+    validate_input_specs(freeze['inputs'])
+    forbidden={v['path'] for v in freeze['inputs'].values()}|{v['expected_path'] for v in freeze['inputs'].values() if v['expected_path'] is not None}
+    files=freeze['files']
+    require(type(files) is dict and 12<=len(files)<=64,'finite frozen source graph')
+    for path,pin in files.items():
+        require(type(path) is str and Path(path).is_absolute() and path not in forbidden and digest_string(pin),'raw input excluded from source graph')
+        local=Path(path).parent==ROOT and Path(path).name not in {'FREEZE.json','PUBLICATION-CHECKPOINT.json'}
+        require(local or SCIENCE.get(path)==pin,'frozen source namespace')
+    require(all(files.get(path)==pin for path,pin in SCIENCE.items()),'immutable scientific paths/pins')
+    require(all(str(ROOT/name) in files for name in LOCAL_SOURCES),'all operational sources frozen')
+    require(files.get(str(ROOT/'RESOURCE-ALLOCATION.json'))==freeze['resource_allocation_sha256'],'resource file binding')
+    require(type(freeze['mock_counts']) is dict and bool(freeze['mock_counts']) and all(type(k) is str and integer(v) for k,v in freeze['mock_counts'].items()),'finite mock count dictionary')
+    require(type(freeze['jobs']) is dict and set(freeze['jobs'])==set(JOBS),'exact seven jobs')
+    for job in JOBS:require(freeze['jobs'][job]==expected_job(freeze,job),'exact frozen job specification: '+job)
+    return freeze
+
+
+def freeze_context(freeze_pin):
+    require(digest_string(freeze_pin),'source freeze hash')
+    freeze=read_json(ROOT/'FREEZE.json',JSON_MAX,freeze_pin)
+    verify_freeze_object(freeze)
+    require(freeze['python']=={'executable':str(Path(sys.executable).resolve()),'sha256':sha(Path(sys.executable).resolve(),64*MIB),'version':sys.version},'exact isolated interpreter')
+    # Deliberately never open/hash any FREEZE.inputs member here.
+    for path,pin in freeze['files'].items():require(sha(path,MIB)==pin,'frozen source bytes changed: '+path)
+    return freeze
+
+
+def validate_approval_object(approval,freeze,freeze_pin,stage):
+    keys={'schema','status','stage','freeze_sha256','jobs','input_sha256','source_review_sha256','prerequisite_acceptance_sha256','publication_checkpoint_sha256'}
+    require(stage in STAGE_JOBS and type(approval) is dict and set(approval)==keys,'exact approval schema')
+    require(approval['schema']=='k4-residual-stage-approval-v1' and approval['status']=='APPROVED_FOR_'+stage.upper() and approval['stage']==stage and approval['freeze_sha256']==freeze_pin,'stage approval identity')
+    require(approval['jobs']==list(STAGE_JOBS[stage]) and digest_string(approval['source_review_sha256']),'explicit exact-stage grant/review')
+    roles=('positive','empty') if stage=='controls' else ('K4',) if stage=='target' else ()
+    require(approval['input_sha256']=={r:freeze['inputs'][r]['sha256'] for r in roles},'exact stage input capability')
+    require(approval['prerequisite_acceptance_sha256'] is None if stage=='mocks' else digest_string(approval['prerequisite_acceptance_sha256']),'stage prerequisite commitment')
+    require(digest_string(approval['publication_checkpoint_sha256']) if stage=='target' else approval['publication_checkpoint_sha256'] is None,'target-only publication commitment')
+    return approval
+
+
+def validate_external_object(value,job,freeze_pin,receipt_pin):
+    require(type(value) is dict and set(value)=={'schema','job','freeze_sha256','receipt_sha256','exit_code','completed','tool_evidence'},'external completion schema')
+    require(value['schema']=='k4-residual-external-completion-v1' and value['job']==job and value['freeze_sha256']==freeze_pin and value['receipt_sha256']==receipt_pin,'external completion binding')
+    require(type(value['exit_code']) is int and value['exit_code']==0 and value['completed'] is True and type(value['tool_evidence']) is str and 0<len(value['tool_evidence'])<=1000,'external clean completion')
+    return True
+
+
+def external_completion(job,freeze_pin,receipt_pin):
+    path=ROOT/'external'/(job+'.json')
+    value=read_json(path,65536)
+    validate_external_object(value,job,freeze_pin,receipt_pin)
+    return sha(path,65536)
+
+
+def validate_acceptance_object(value,stage,freeze_pin):
+    require(stage in ('mocks','controls','target'),'acceptable predecessor stage')
+    require(type(value) is dict and set(value)=={'schema','status','stage','freeze_sha256','jobs','receipts','review_sha256'},'acceptance schema')
+    jobs=list(STAGE_JOBS[stage])
+    require(value['schema']=='k4-residual-stage-acceptance-v1' and value['status']=='ACCEPTED_COMPLETE' and value['stage']==stage and value['freeze_sha256']==freeze_pin and value['jobs']==jobs and digest_string(value['review_sha256']),'independent accepted stage')
+    require(type(value['receipts']) is dict and set(value['receipts'])==set(jobs),'accepted exact receipt set')
+    for record in value['receipts'].values():
+        require(type(record) is dict and set(record)=={'receipt_sha256','external_sha256'} and all(digest_string(v) for v in record.values()),'accepted receipt/external pins')
+    return True
+
+
+def read_authority(stage,freeze,freeze_pin,approval_pin):
+    require(digest_string(approval_pin),'explicit approval pin')
+    path=ROOT/'approvals'/(stage+'.json')
+    approval=read_json(path,65536,approval_pin)
+    validate_approval_object(approval,freeze,freeze_pin,stage)
+    if stage!='mocks':
+        previous={'controls':'mocks','target':'controls','seal':'target'}[stage]
+        accepted=read_json(ROOT/'acceptance'/(previous.upper()+'.json'),65536,approval['prerequisite_acceptance_sha256'])
+        validate_acceptance_object(accepted,previous,freeze_pin)
+        for job,record in accepted['receipts'].items():
+            require(sha(ROOT/'runs'/job/'resource.json')==record['receipt_sha256'],'accepted resource receipt changed')
+            require(external_completion(job,freeze_pin,record['receipt_sha256'])==record['external_sha256'],'accepted external completion changed')
+    if stage=='target':
+        checkpoint=read_json(ROOT/'PUBLICATION-CHECKPOINT.json',65536,approval['publication_checkpoint_sha256'])
+        require(type(checkpoint) is dict and set(checkpoint)=={'schema','status','freeze_sha256','remote_commit','permission_record_sha256','ledger_sha256','responsibilities_sequence','main_denial_resolved'},'publication checkpoint schema')
+        require(checkpoint['schema']=='k4-residual-publication-checkpoint-v1' and checkpoint['status']=='RECONCILED_AND_PUBLISHED' and checkpoint['freeze_sha256']==freeze_pin and checkpoint['main_denial_resolved'] is True,'publication gate closed')
+        require(type(checkpoint['remote_commit']) is str and len(checkpoint['remote_commit'])==40 and all(c in '0123456789abcdef' for c in checkpoint['remote_commit']),'verified publication commit')
+        require(digest_string(checkpoint['permission_record_sha256']) and type(checkpoint['ledger_sha256']) is dict and set(checkpoint['ledger_sha256'])=={'HYPOTHESES.md','EXPERIMENTS.md','EXTERNAL-PRIOR-ART.md','tracker.json'} and all(digest_string(v) for v in checkpoint['ledger_sha256'].values()) and integer(checkpoint['responsibilities_sequence']) and checkpoint['responsibilities_sequence']>=53,'publication permission/ledger evidence')
+    return approval
+
+
+def validate_raw(raw,input_key):
+    require(input_key in INPUT_ROLES,'scheduled raw identity')
+    require(type(raw) is dict and set(raw)=={'ciphertext','length','indexing','cribs'},'raw source exact schema')
+    require(type(raw['length']) is int and raw['length']==97 and raw['indexing']=='one-based inclusive','97-symbol indexing')
+    ct=raw['ciphertext']
+    require(type(ct) is str and len(ct)==97 and all('A'<=c<='Z' for c in ct),'strict AZ ciphertext')
+    require(type(raw['cribs']) is list and len(raw['cribs'])==2,'two crib blocks')
+    for crib,(start,end) in zip(raw['cribs'],((22,34),(64,74))):
+        require(type(crib) is dict and set(crib)=={'start','end','plaintext'} and type(crib['start']) is int and type(crib['end']) is int and crib['start']==start and crib['end']==end,'fixed crib ranges')
+        require(type(crib['plaintext']) is str and len(crib['plaintext'])==end-start+1 and all('A'<=c<='Z' for c in crib['plaintext']),'AZ crib lengths')
+    if input_key=='K4':require([c['plaintext'] for c in raw['cribs']]==['EASTNORTHEAST','BERLINCLOCK'],'official K4 clues only')
+    return raw
+
+
+def read_authorized_raw(freeze,approval,job):
+    stage,kind,key,inner,_optimized=job_identity(job)
+    require(kind=='science' and approval['stage']==stage and job in approval['jobs'] and approval['input_sha256'].get(key)==freeze['inputs'][key]['sha256'],'raw input capability absent')
+    spec=freeze['inputs'][key]
+    raw=read_json(spec['path'],RAW_MAX,spec['sha256'])
+    validate_raw(raw,key)
+    return raw
+
+
+def require_child_bounds(stage):
+    limits=stage_limits(stage)
+    require(resource.getrlimit(resource.RLIMIT_CPU)==(limits['worker_cpu_soft'],limits['worker_cpu_hard']),'worker CPU guard')
+    memory=limits['worker_address_space_bytes']
+    require(resource.getrlimit(resource.RLIMIT_AS)==(memory,memory),'worker memory guard')
+    guard=ctypes.c_int()
+    require(ctypes.CDLL(None).prctl(2,ctypes.byref(guard),0,0,0)==0 and guard.value==signal.SIGKILL,'worker parent-death guard')
+
+
+def actual_command(script,args,optimized=False):
+    return [str(Path(sys.executable).resolve()),'-I','-B']+(['-O'] if optimized else [])+[str(script)]+list(args)
+
+
+def validate_child_command(freeze,job,freeze_pin,approval_pin,args):
+    spec=freeze['jobs'][job]
+    require(sys.flags.isolated==1 and sys.dont_write_bytecode is True and sys.flags.optimize==int(spec['optimized']),'isolated child interpreter flags')
+    require(sys.orig_argv==expand(spec['command'],freeze_pin,approval_pin),'exact original interpreter/worker argv')
+    require(actual_command(spec['script'],args,spec['optimized'])==expand(spec['command'],freeze_pin,approval_pin),'exact scheduled worker argv')
+    require(str(Path.cwd())==str(ROOT),'exact working directory')
+    return spec
+
+
+def disk_bytes(freeze):
+    """Bounded metadata-only inventory; never opens raw source inputs."""
+    allowed={Path(path).relative_to(ROOT).as_posix():MIB for path in freeze['files'] if Path(path).parent==ROOT}
+    allowed.update({'FREEZE.json':JSON_MAX,'PUBLICATION-CHECKPOINT.json':65536,
+        'runs/state.json':JSON_MAX,'runs/state.json.tmp':JSON_MAX,'runs/IN_FLIGHT.lock':JSON_MAX})
+    for spec in freeze['inputs'].values():
+        for key in ('path','expected_path'):
+            if spec[key] is not None and ROOT in Path(spec[key]).parents:
+                allowed[Path(spec[key]).relative_to(ROOT).as_posix()]=RAW_MAX
+    for stage in STAGE_JOBS:allowed['approvals/'+stage+'.json']=65536
+    for stage in ('MOCKS','CONTROLS','TARGET'):allowed['acceptance/'+stage+'.json']=65536
+    for job in JOBS:
+        allowed['external/'+job+'.json']=65536
+        for name,cap in (('stdout.txt',LOG_MAX),('stderr.txt',LOG_MAX),('result.json',JSON_MAX),('resource.json',JSON_MAX),('resource.json.tmp',JSON_MAX)):
+            allowed['runs/'+job+'/'+name]=cap
+        if job in JOBS[2:6]:allowed['runs/'+job+'/case.cert.jsonl']=CERT_MAX
+    allowed_dirs={'.'}
+    for name in allowed:
+        parent=Path(name).parent
+        while parent!=Path('.'):
+            allowed_dirs.add(parent.as_posix());parent=parent.parent
+    total=0;files=0;directories=0
+    for base,dirs,names in os.walk(ROOT,followlinks=False):
+        directories+=1;require(directories<=64,'stage directory bound')
+        require(Path(base).relative_to(ROOT).as_posix() in allowed_dirs,'frozen finite directory inventory')
+        for name in dirs:require(not (Path(base)/name).is_symlink(),'stage symlink directory')
+        for name in names:
+            p=Path(base)/name;files+=1
+            require(files<=256 and p.is_file() and not p.is_symlink(),'stage finite regular inventory')
+            relative=p.relative_to(ROOT).as_posix()
+            require(relative in allowed,'unexpected stage path')
+            size=p.stat().st_size;require(size<=allowed[relative],'stage per-path file cap')
+            require(size<=STAGE_MAX-total,'stage byte ceiling');total+=size
+    return total
```

## New operational source: seal_results.py
```diff
--- /dev/null
+++ source/operational/seal_results.py
@@ -0,0 +1,88 @@
+"""One explicitly granted metadata seal; no raw input or scientific imports.
+
+The accepted six-job prefix must be complete with no scientific reserve before
+the supervisor reserves this own metadata invocation. This report does not
+claim its own external completion; that immutable receipt remains parent-owned.
+"""
+import argparse
+import hashlib
+import importlib.util
+import json
+from pathlib import Path
+import sys
+
+ROOT=Path('original-execution-namespace')
+MIB=1024*1024
+
+
+def require(condition,message):
+    if not condition:raise ValueError(message)
+
+
+def bootstrap(pin):
+    path=ROOT/'FREEZE.json'
+    require(type(pin) is str and len(pin)==64 and path.is_file() and not path.is_symlink() and path.stat().st_size<=2*MIB,'bounded external freeze identity')
+    with path.open('rb') as f:data=f.read(2*MIB+1)
+    require(len(data)<=2*MIB and hashlib.sha256(data).hexdigest()==pin,'source freeze bytes')
+    def unique(pairs):
+        out={}
+        for key,value in pairs:require(key not in out,'duplicate JSON key');out[key]=value
+        return out
+    frozen=json.loads(data,object_pairs_hook=unique,parse_constant=lambda _x:(_ for _ in ()).throw(ValueError('nonfinite JSON')))
+    path=ROOT/'common.py'
+    require(path.is_file() and not path.is_symlink() and path.stat().st_size<=MIB,'bounded common source')
+    with path.open('rb') as f:source=f.read(MIB+1)
+    require(len(source)<=MIB and frozen['files'][str(path)]==hashlib.sha256(source).hexdigest(),'common source commitment')
+    spec=importlib.util.spec_from_file_location('k4_target_common_sealer',path)
+    require(spec is not None and spec.loader is not None,'common source loader')
+    common=importlib.util.module_from_spec(spec);sys.modules[spec.name]=common
+    exec(compile(source,str(path),'exec',dont_inherit=True,optimize=sys.flags.optimize),common.__dict__)
+    return common,common.freeze_context(pin)
+
+
+def snapshot(common,supervisor,freeze,freeze_pin,approval_pin):
+    state_path=ROOT/'runs'/'state.json';state=common.read_json(state_path)
+    supervisor.validate_state_shape(state,freeze_pin,True)
+    require([r['job'] for r in state['completed']]==list(common.JOBS[:6]),'exact six-job completed prefix')
+    require(state['in_flight'] is not None and state['in_flight']['job']=='seal' and state['in_flight']['allocation_reserved']==12 and state['in_flight']['approval_sha256']==approval_pin,'only own metadata reserve')
+    marker=common.read_json(ROOT/'runs'/'IN_FLIGHT.lock')
+    require(marker=={'schema':'k4-residual-one-use-lock-v1','freeze_sha256':freeze_pin,'reservation':state['in_flight']},'retained own marker/reservation binding')
+    require(state['completed'][5]['status']==state['completed'][4]['status'] and state['completed'][5]['status'] in ('VERIFIED_EXACT','VERIFIED_EMPTY','CERTIFIED_RESOURCE_GATE'),'matching accepted scientific pair')
+    artifacts,_=supervisor.inspect_completed(state,freeze,freeze_pin,common,False,True)
+    # Reports and certificates are streamed to hashes, never parsed/evaluated.
+    for name in ('FREEZE.json','PUBLICATION-CHECKPOINT.json','runs/state.json','runs/IN_FLIGHT.lock'):
+        path=ROOT/name;artifacts[name]={'bytes':path.stat().st_size,'sha256':common.sha(path,2*MIB)}
+    for kind,names in (('approvals',('mocks','controls','target','seal')),('acceptance',('MOCKS','CONTROLS','TARGET'))):
+        for name in names:
+            path=ROOT/kind/(name+'.json');artifacts[kind+'/'+name+'.json']={'bytes':path.stat().st_size,'sha256':common.sha(path,65536)}
+    return dict(schema='k4-residual-metadata-seal-v1',job='seal',freeze_sha256=freeze_pin,
+        approval_sha256=approval_pin,status='SEALED_METADATA',prior_completed_jobs=list(common.JOBS[:6]),
+        artifacts=artifacts,state_sha256=artifacts['runs/state.json']['sha256'],source_sha256=freeze['files'],
+        input_sha256={k:v['sha256'] for k,v in freeze['inputs'].items()},
+        allocation_charged_before_seal=state['allocation_charged'],worker_cpu_seconds_before_seal=state['worker_cpu_actual'],
+        seal_own_completion_pending=True,reason=None)
+
+
+def main(argv=None):
+    parser=argparse.ArgumentParser(description='One metadata-only seal; no science replay.')
+    for name in ('job','freeze-sha256','approval-sha256','output'):parser.add_argument('--'+name,required=True)
+    args=parser.parse_args(argv)
+    require(args.job=='seal','only fixed metadata job')
+    common,freeze=bootstrap(args.freeze_sha256)
+    common.require_child_bounds('seal')
+    actual=list(sys.argv[1:] if argv is None else argv)
+    spec=common.validate_child_command(freeze,args.job,args.freeze_sha256,args.approval_sha256,actual)
+    require(args.output==spec['output'],'fixed metadata output')
+    common.read_authority('seal',freeze,args.freeze_sha256,args.approval_sha256)
+    supervisor=common.load_pinned('k4_target_metadata_supervisor',ROOT/'supervisor.py',freeze['files'][str(ROOT/'supervisor.py')])
+    report=snapshot(common,supervisor,freeze,args.freeze_sha256,args.approval_sha256)
+    supervisor.validate_seal_report(report,spec,freeze,args.freeze_sha256,args.approval_sha256)
+    common.freeze_context(args.freeze_sha256)
+    common.read_authority('seal',freeze,args.freeze_sha256,args.approval_sha256)
+    require(snapshot(common,supervisor,freeze,args.freeze_sha256,args.approval_sha256)==report,'metadata postseal changed')
+    common.write_new(args.output,report)
+    return 0
+
+
+if __name__=='__main__':
+    sys.exit(main())
```

## New operational source: protocol_mock_tests.py
```diff
--- /dev/null
+++ source/operational/protocol_mock_tests.py
@@ -0,0 +1,1072 @@
+"""Two finite operational-only invocations; no scientific call or real case read.
+
+SOURCE ONLY until separately approved. The fixtures below are literal interface
+stubs, not target data, a decoder benchmark or fresh synthetic validation. This
+module is inert at import and --help; it never grants authority or launches a
+process. Counts are frozen before either invocation; failures forbid retries.
+"""
+import argparse
+import builtins
+import contextlib
+import copy
+import ctypes
+import hashlib
+import importlib.machinery
+import importlib.util
+import io
+import json
+import math
+import os
+from pathlib import Path
+import resource
+import selectors
+import signal
+import subprocess
+import sys
+import time
+import types
+
+ROOT = Path('original-execution-namespace')
+MIB = 1024 * 1024
+REPORT_SCHEMA = 'k4-residual-operational-mock-report-v1'
+EXPECTED_COUNTS = {
+    'inert_boundaries': 15,
+    'raw_schema': 14,
+    'mapping': 7,
+    'status_relation': 16,
+    'freeze_authority': 24,
+    'command_mode': 10,
+    'digest': 6,
+    'collector_reaper': 12,
+    'state_execution': 18,
+    'file_boundaries': 8,
+    'mode_pair': 8,
+    'worker_fail_closed': 4,
+    'supervisor_reports': 13,
+    'byte_loader': 4,
+}
+EXPECTED_CASES = {
+    'inert_boundaries': (
+        'import:common.py', 'import:bounded_stage.py', 'import:worker.py',
+        'import:supervisor.py', 'import:protocol_mock_tests.py',
+        'import:seal_results.py', 'import:input_check.py',
+        'help:worker.py', 'unsupported-status:worker.py',
+        'help:supervisor.py', 'unsupported-status:supervisor.py',
+        'help:protocol_mock_tests.py', 'unsupported-status:protocol_mock_tests.py',
+        'help:seal_results.py', 'unsupported-status:seal_results.py'),
+    'raw_schema': (
+        'valid-literal', 'raw-mutation-0', 'raw-mutation-1', 'raw-mutation-2',
+        'raw-mutation-3', 'raw-mutation-4', 'raw-mutation-5', 'raw-mutation-6',
+        'raw-mutation-7', 'raw-mutation-8', 'raw-mutation-9', 'raw-extra-field',
+        'raw-duplicate-key', 'control-cannot-claim-target'),
+    'mapping': (
+        'independent-converters-agree', 'hand-newest-first', 'hand-final-context',
+        'hand-clue-offsets-sign', 'reversed-lags', 'off-by-one-row', 'wrong-sign'),
+    'status_relation': (
+        'matching-EXACT', 'matching-EMPTY', 'rejected-pair-EXACT-VERIFIED_EMPTY',
+        'rejected-pair-EMPTY-VERIFIED_EXACT', 'rejected-pair-INCOMPLETE-VERIFIED_EXACT',
+        'rejected-pair-EMPTY-FORMAT_ONLY', 'singleton-common-law',
+        'aliases-not-function-uniqueness', 'multiple-joints', 'no-common-witness',
+        'singleton-joint-inconsistency', 'empty-zero-relation',
+        'empty-not-vacuous-singleton', 'empty-partial-masks-rejected',
+        'no-first-six-claim', 'no-score-ranking-field'),
+    'freeze_authority': (
+        'valid-freeze-metadata', 'no-input-in-source-positive-path',
+        'no-input-in-source-positive-expected_path', 'no-input-in-source-empty-path',
+        'no-input-in-source-empty-expected_path', 'no-input-in-source-K4-path',
+        'role-inner-id-binding', 'fixed-target-pin', 'valid-mock-approval',
+        'approval-old-freeze', 'approval-wrong-stage', 'approval-extra-job',
+        'approval-case-capability', 'approval-missing-review',
+        'mock-no-raw-capability-CTRL-positive-normal', 'mock-no-raw-capability-K4-normal',
+        'missing-approval', 'valid-external-completion', 'external-uncertain-rejected',
+        'source-auth-traps-all-real-cases', 'source-byte-pin-mismatch', 'control-grant-cannot-read-K4',
+        'target-grant-cannot-read-control', 'control-path-never-opens-target'),
+    'command_mode': (
+        'fixed-expanded-command', 'partial-token', 'duplicate-freeze',
+        'unknown-token', 'missing-approval', 'extra-argv', 'wrong-output', 'wrong-mode',
+        'double-optimized-rejected', 'unexpected-interpreter-flag-rejected'),
+    'digest': (
+        'root-time-only-exclusion', 'piece-time-only-exclusion',
+        'logical-counter-retained', 'relation-bytes-retained',
+        'stream-cap-predebit', 'incomplete-digest-disallowed'),
+    'collector_reaper': (
+        'integer-not-bool', 'finite-not-nan', 'finite-not-infinity',
+        'exact-log-cap', 'log-overflow-no-debit', 'log-bool-rejected',
+        'collector-exact-boundary', 'collector-overflow-stops-write',
+        'collector-after-overflow-discard', 'collector-chunk-bound',
+        'reap-disarm-release-order', 'reap-retries-only-interrupted-wait'),
+    'state_execution': (
+        'clean-initial-state', 'first-only-job', 'out-of-order-no-launch',
+        'retained-reserve-blocks-successor', 'stopped-blocks-successor',
+        'old-state-freeze', 'complete-execution-receipt',
+        'execution-unreaped', 'execution-unguarded', 'execution-wall-overshoot',
+        'execution-cpu-overshoot', 'execution-log-overflow', 'execution-child-failed',
+        'execution-collector-error', 'execution-bool-receipt-count',
+        'execution-arbitrary-command', 'missing-output-retained-reserve-stops',
+        'prelaunch-failure-retains-full-reserve'),
+    'file_boundaries': (
+        'bounded-json-correct-pin', 'reader-duplicate-key', 'reader-nan',
+        'reader-infinity', 'reader-symlink', 'reader-input-pin-mismatch',
+        'reader-growth-overflow', 'exclusive-marker-no-retry'),
+    'mode_pair': (
+        'same-pair', 'only-frozen-times-excluded', 'reject-pair-producer-counter',
+        'reject-pair-preflight-counter', 'reject-pair-reference-counter',
+        'reject-pair-full-relation-digest', 'reject-pair-joint-count', 'reject-pair-source-role'),
+    'worker_fail_closed': (
+        'worker-path-missing-approval', 'worker-path-reference-mismatch',
+        'worker-path-postseal-mismatch', 'worker-path-control-gate'),
+    'supervisor_reports': (
+        'report-complete-EXACT', 'report-complete-EMPTY', 'report-resource-gate-no-result',
+        'report-incomplete-no-result', 'reject-report-EXACT-crossed-verifier',
+        'reject-report-EMPTY-crossed-verifier', 'reject-report-EMPTY-partial-inventory',
+        'reject-report-W-zero-alone', 'reject-report-incomplete-partial-claim',
+        'reject-report-gate-partial-claim', 'reject-report-bool-cap-counter',
+        'reject-report-extra-resource-field', 'reject-report-over-cap-wall'),
+    'byte_loader': (
+        'authenticated-literal-module-identity', 'wrong-hash-before-compile',
+        'source-cap-before-compile', 'loader-exec-module-never-used'),
+}
+FORBIDDEN_COUNTER_KEYS = ('science_imports', 'science_calls', 'case_reads',
+                          'child_launches', 'entropy_calls')
+
+
+def require(condition, message):
+    if not condition:
+        raise ValueError(message)
+
+
+def _unique(pairs):
+    result = {}
+    for key, value in pairs:
+        require(key not in result, 'duplicate bootstrap key')
+        result[key] = value
+    return result
+
+
+def _bytes(path, limit):
+    path = Path(path)
+    require(path.is_file() and not path.is_symlink() and path.stat().st_size <= limit,
+            'bounded regular operational source')
+    with path.open('rb') as handle:
+        data = handle.read(limit + 1)
+    require(len(data) <= limit, 'operational source grew beyond cap')
+    return data
+
+
+def bootstrap(pin):
+    require(type(pin) is str and len(pin) == 64 and
+            all(c in '0123456789abcdef' for c in pin), 'freeze commitment')
+    raw = _bytes(ROOT / 'FREEZE.json', 2 * MIB)
+    require(hashlib.sha256(raw).hexdigest() == pin, 'freeze bytes changed')
+    preliminary = json.loads(raw, object_pairs_hook=_unique,
+        parse_constant=lambda _x: (_ for _ in ()).throw(ValueError('nonfinite JSON')))
+    source = ROOT / 'common.py'
+    content = _bytes(source, MIB)
+    require(hashlib.sha256(content).hexdigest() == preliminary['files'][str(source)],
+            'operational bootstrap pin')
+    common = memory_module('k4_target_mock_common', source, content)
+    return common, common.freeze_context(pin)
+
+
+def memory_module(name, path, source):
+    """Execute only caller-authenticated operational source, never a pyc cache."""
+    spec = importlib.machinery.ModuleSpec(name, loader=None, origin=str(path))
+    spec.has_location = True
+    module = importlib.util.module_from_spec(spec)
+    module.__file__ = str(path)
+    sys.modules[name] = module
+    exec(compile(source, str(path), 'exec', dont_inherit=True, optimize=sys.flags.optimize), module.__dict__)
+    return module
+
+
+@contextlib.contextmanager
+def patched(obj, name, value):
+    previous = getattr(obj, name)
+    setattr(obj, name, value)
+    try:
+        yield
+    finally:
+        setattr(obj, name, previous)
+
+
+class Suite:
+    def __init__(self):
+        require(set(EXPECTED_CASES) == set(EXPECTED_COUNTS) and all(
+            len(names) == EXPECTED_COUNTS[group] and len(set(names)) == len(names)
+            for group, names in EXPECTED_CASES.items()), 'literal manifest/count agreement')
+        self.counts = {key: 0 for key in EXPECTED_COUNTS}
+        self.names = {key: set() for key in EXPECTED_COUNTS}
+
+    def case(self, group, name, function, rejects=False):
+        require(group in self.counts and name in EXPECTED_CASES[group] and name not in self.names[group],
+                'finite unique declared mock assertion')
+        self.names[group].add(name)
+        if rejects:
+            try:
+                function()
+            except (ValueError, FileNotFoundError, FileExistsError):
+                pass
+            else:
+                raise ValueError('mock failed to reject: ' + name)
+        else:
+            require(function() is True, 'mock assertion failed: ' + name)
+        self.counts[group] += 1
+
+
+def changed(value, path, replacement):
+    result = copy.deepcopy(value)
+    cursor = result
+    for item in path[:-1]:
+        cursor = cursor[item]
+    cursor[path[-1]] = replacement
+    return result
+
+
+def call_true(function, *args):
+    function(*args)
+    return True
+
+
+@contextlib.contextmanager
+def source_only_guard(counts):
+    """Install before the first operational module executes in a mock process.
+
+    Only byte reads of frozen-source candidates, interpreter and the mock grant
+    can pass. The later authenticated source graph further narrows these paths.
+    Real inputs/expected arrays, pyc caches, entropy and processes are blocked.
+    """
+    science_paths = {
+        'source/scientific/residual_decoder.py',
+        'source/scientific/affine_filter.py',
+        'source/scientific/reference_v3.py',
+        'source/scientific/preflight_blind.py',
+        'source/scientific/checker_blind.py',
+        'source/scientific/CAPS.json'}
+    case_paths = {'https://github.com/reggiechan74/kryptos-k4/blob/7b9075daa6aee50187b18794b1d3c97e6d840249/data/k4.json'} | {
+        str(ROOT / 'fixtures' / (name + '.json')) for name in
+        ('positive', 'positive-expected', 'empty', 'empty-expected')}
+    interpreter = str(Path(sys.executable).resolve())
+    original_io = io.open
+    original_builtin = builtins.open
+    original_import = builtins.__import__
+    def checked_open(original, path, mode='r', *args, **kwargs):
+        require(isinstance(path, (str, bytes, os.PathLike)), 'source-only pathname')
+        text = os.fsdecode(path)
+        if text in case_paths:
+            counts['case_reads'] += 1
+            raise ValueError('setup attempted real case input')
+        candidate = Path(text)
+        allowed = (text in science_paths or text == interpreter or
+                   text == str(ROOT / 'approvals' / 'mocks.json') or
+                   candidate.parent == ROOT and candidate.suffix in ('.py', '.json', '.md')
+                   and candidate.name != 'PUBLICATION-CHECKPOINT.json')
+        require(allowed and mode in ('r', 'rb'), 'mock setup permits authenticated source metadata reads only')
+        return original(path, mode, *args, **kwargs)
+    def no_process(*_a, **_k):
+        counts['child_launches'] += 1
+        raise ValueError('mock setup forbids process launch')
+    def no_entropy(*_a, **_k):
+        counts['entropy_calls'] += 1
+        raise ValueError('mock setup forbids entropy')
+    def no_dynamic_module(*_a, **_k):
+        counts['science_imports'] += 1
+        raise ValueError('only authenticated operational in-memory modules are allowed')
+    def no_effect(*_a, **_k):
+        raise ValueError('mock setup forbids direct filesystem or resource mutation')
+    def guarded_import(name, *args, **kwargs):
+        if name.split('.')[0] in ('residual_decoder', 'affine_filter', 'reference_v3',
+                                 'preflight_blind', 'checker_blind'):
+            counts['science_imports'] += 1
+            raise ValueError('mock setup forbids scientific import')
+        return original_import(name, *args, **kwargs)
+    absent = object()
+    prior = {}
+    for name in ('random', 'secrets'):
+        prior[name] = sys.modules.get(name, absent)
+        stub = types.ModuleType(name)
+        stub.__getattr__ = no_entropy
+        sys.modules[name] = stub
+    try:
+        with contextlib.ExitStack() as stack:
+            replacements = [(io, 'open', lambda path, mode='r', *a, **k: checked_open(original_io, path, mode, *a, **k)),
+                (builtins, 'open', lambda path, mode='r', *a, **k: checked_open(original_builtin, path, mode, *a, **k)),
+                (os, 'fork', no_process), (os, 'execve', no_process),
+                (subprocess, 'Popen', no_process), (os, 'urandom', no_entropy),
+                (os, 'open', no_effect), (os, 'mkdir', no_effect), (os, 'unlink', no_effect),
+                (os, 'remove', no_effect), (os, 'replace', no_effect), (os, 'write', no_effect),
+                (importlib.util, 'spec_from_file_location', no_dynamic_module),
+                (builtins, '__import__', guarded_import)]
+            if hasattr(os, 'getrandom'):
+                replacements.append((os, 'getrandom', no_entropy))
+            for obj, name, replacement in replacements:
+                stack.enter_context(patched(obj, name, replacement))
+            yield
+    finally:
+        for name, value in prior.items():
+            if value is absent:
+                sys.modules.pop(name, None)
+            else:
+                sys.modules[name] = value
+
+
+@contextlib.contextmanager
+def forbidden_io(common, worker, forbidden, counts):
+    """No actual filesystem data I/O, scientific loader, child or entropy in tests.
+
+    The case-path set contains all three raw files and both expected arrays.
+    Source authentication is tested with its metadata reader/hash replaced by
+    a finite fixture. Any accidental source-graph traversal into a case path
+    fails before a real open; no deliberately successful probe is made.
+    """
+    def denied_file(path, *_args, **_kwargs):
+        if isinstance(path, (str, bytes, os.PathLike)) and os.fsdecode(path) in forbidden:
+            counts['case_reads'] += 1
+        raise ValueError('mock forbids data-file I/O')
+
+    def denied_process(*_args, **_kwargs):
+        counts['child_launches'] += 1
+        raise ValueError('mock forbids process launch')
+
+    def denied_entropy(*_args, **_kwargs):
+        counts['entropy_calls'] += 1
+        raise ValueError('mock forbids entropy')
+
+    def denied_science(*_args, **_kwargs):
+        counts['science_calls'] += 1
+        raise ValueError('mock forbids dynamic scientific/operational loading in body')
+
+    def denied_effect(*_args, **_kwargs):
+        raise ValueError('mock forbids filesystem/resource/signal mutation')
+
+    original_import = builtins.__import__
+    scientific = {'residual_decoder', 'affine_filter', 'reference_v3',
+                  'preflight_blind', 'checker_blind'}
+
+    def guarded_import(name, *args, **kwargs):
+        if name.split('.')[0] in scientific or 'k4_target_decoder' in name or 'k4_target_reference' in name:
+            counts['science_imports'] += 1
+            raise ValueError('mock forbids scientific import')
+        return original_import(name, *args, **kwargs)
+
+    with contextlib.ExitStack() as stack:
+        for obj, name, replacement in (
+                (builtins, 'open', denied_file), (io, 'open', denied_file),
+                (os, 'open', denied_file), (os, 'fork', denied_process),
+                (os, 'execve', denied_process), (subprocess, 'Popen', denied_process),
+                (os, 'mkdir', denied_effect), (os, 'unlink', denied_effect),
+                (os, 'remove', denied_effect), (os, 'replace', denied_effect),
+                (os, 'write', denied_effect), (resource, 'setrlimit', denied_effect),
+                (signal, 'setitimer', denied_effect), (ctypes, 'CDLL', denied_effect),
+                (os, 'urandom', denied_entropy),
+                (common, 'load_pinned', denied_science), (worker, 'load', denied_science),
+                (builtins, '__import__', guarded_import)):
+            stack.enter_context(patched(obj, name, replacement))
+        yield
+
+
+def raw_literal():
+    # This is not any disclosed pilot or K4 input. Hand-check: first preceding
+    # six letters ABCDEF -> [5,4,3,2,1,0]; current letters after the prefix are
+    # A, plaintext B, hence signed C-P=25 at each frozen observation row.
+    return {'ciphertext': 'ABCDEF' + 'A' * 91, 'length': 97,
+            'indexing': 'one-based inclusive',
+            'cribs': [{'start': 22, 'end': 34, 'plaintext': 'B' * 13},
+                      {'start': 64, 'end': 74, 'plaintext': 'B' * 11}]}
+
+
+def relation_literal(empty=False):
+    result = {'status': 'EMPTY' if empty else 'EXACT',
+        'resources': {'wall_seconds': 1.0, 'steps': 3},
+        'pieces': [] if empty else [{'core': {'resources': {'wall_seconds': 0.5, 'work': 2}}}],
+        'masks': [[] if empty else [2] for _ in range(91)],
+        'witnesses': [{} for _ in range(91)], 'provenance': [{} for _ in range(91)],
+        'feasibility_witness': None if empty else {'piece': 'literal-stub', 'theta': [[28, 1], [29, 1]]}}
+    verified = {'status': 'VERIFIED_EMPTY' if empty else 'VERIFIED_EXACT',
+        'pieces_checked': 0 if empty else 1, 'canonical_functions': 0 if empty else 1,
+        'original_lifts': 0 if empty else 1, 'joint_predictions': 0 if empty else 1}
+    raw = {'ciphertext': 'A' * 97, 'length': 97, 'indexing': 'one-based inclusive',
+        'cribs': [{'start': 22, 'end': 34, 'plaintext': 'Y' * 13},
+                  {'start': 64, 'end': 74, 'plaintext': 'Y' * 11}]}
+    return raw, result, verified
+
+
+def inert_cases(suite, sources, modules):
+    def imported(name):
+        namespace = {'__name__': 'k4_inert_probe_' + name, '__file__': str(ROOT / name)}
+        exec(compile(sources[name], str(ROOT / name), 'exec', dont_inherit=True, optimize=sys.flags.optimize), namespace)
+        return True
+
+    for name in ('common.py', 'bounded_stage.py', 'worker.py', 'supervisor.py',
+                 'protocol_mock_tests.py', 'seal_results.py', 'input_check.py'):
+        suite.case('inert_boundaries', 'import:' + name, lambda name=name: imported(name))
+
+    def parse_only(module, option, expected):
+        output = io.StringIO()
+        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
+            try:
+                module.main([option])
+            except SystemExit as error:
+                return type(error.code) is int and error.code == expected
+        return False
+
+    for name in ('worker.py', 'supervisor.py', 'protocol_mock_tests.py', 'seal_results.py'):
+        suite.case('inert_boundaries', 'help:' + name,
+                   lambda name=name: parse_only(modules[name], '--help', 0))
+        suite.case('inert_boundaries', 'unsupported-status:' + name,
+                   lambda name=name: parse_only(modules[name], '--status', 2))
+
+
+def raw_and_mapping_cases(suite, common, worker, independent):
+    raw = raw_literal()
+    suite.case('raw_schema', 'valid-literal', lambda: call_true(common.validate_raw, raw, 'positive'))
+    mutations = [
+        (('length',), True), (('length',), 96), (('indexing',), 'zero-based'),
+        (('ciphertext',), 'A' * 96), (('ciphertext',), 'A' * 96 + 'a'),
+        (('cribs', 0, 'start'), 21), (('cribs', 0, 'end'), 33),
+        (('cribs', 1, 'plaintext'), 'A' * 10), (('cribs', 0, 'start'), True),
+        (('cribs', 0, 'plaintext'), 'A' * 12 + '?')]
+    for index, (path, value) in enumerate(mutations):
+        suite.case('raw_schema', 'raw-mutation-' + str(index),
+            lambda path=path, value=value: common.validate_raw(changed(raw, path, value), 'positive'), True)
+    extra = copy.deepcopy(raw); extra['score'] = 1
+    suite.case('raw_schema', 'raw-extra-field', lambda: common.validate_raw(extra, 'positive'), True)
+    suite.case('raw_schema', 'raw-duplicate-key', lambda: common.unique_object([('a', 1), ('a', 2)]), True)
+    suite.case('raw_schema', 'control-cannot-claim-target', lambda: common.validate_raw(raw, 'K4'), True)
+
+    primary = worker.convert_raw(raw, 'v000')
+    secondary = independent.convert_raw_independent(raw, 'v000')
+    expected_rows = list(range(15, 28)) + list(range(57, 68))
+    suite.case('mapping', 'independent-converters-agree', lambda: primary == secondary)
+    suite.case('mapping', 'hand-newest-first', lambda: primary['contexts'][0] == [5, 4, 3, 2, 1, 0])
+    suite.case('mapping', 'hand-final-context', lambda: primary['contexts'][90] == [0, 0, 0, 0, 0, 0])
+    suite.case('mapping', 'hand-clue-offsets-sign', lambda: primary['observed'] == [[r, 25] for r in expected_rows])
+    for label, mutant in (
+            ('reversed-lags', changed(primary, ('contexts', 0), [0, 1, 2, 3, 4, 5])),
+            ('off-by-one-row', changed(primary, ('observed', 0, 0), 16)),
+            ('wrong-sign', changed(primary, ('observed', 0, 1), 1))):
+        suite.case('mapping', label, lambda mutant=mutant: require(mutant == secondary, 'mapping mismatch'), True)
+
+
+def relation_cases(suite, worker, independent):
+    for producer, verifier in (('EXACT', 'VERIFIED_EXACT'), ('EMPTY', 'VERIFIED_EMPTY')):
+        suite.case('status_relation', 'matching-' + producer,
+                   lambda producer=producer, verifier=verifier: worker.require_status_pair(producer, verifier))
+    for producer, verifier in (('EXACT', 'VERIFIED_EMPTY'), ('EMPTY', 'VERIFIED_EXACT'),
+                              ('INCOMPLETE', 'VERIFIED_EXACT'), ('EMPTY', 'FORMAT_ONLY')):
+        suite.case('status_relation', 'rejected-pair-' + producer + '-' + verifier,
+                   lambda producer=producer, verifier=verifier: worker.require_status_pair(producer, verifier), True)
+    raw, result, verified = relation_literal()
+    instance = worker.convert_raw(raw, 'v000')
+    interpretation = independent.interpret_verified(raw, instance, result, verified)
+    suite.case('status_relation', 'singleton-common-law', lambda:
+        interpretation == {'classification': 'CONDITIONAL_SINGLETON_TAIL',
+            'plaintext_masks': [['Y'] for _ in range(91)], 'example_plaintext_tail': 'Y' * 91,
+            'first_six_claimed': False})
+    alias = dict(verified, canonical_functions=2, original_lifts=2)
+    suite.case('status_relation', 'aliases-not-function-uniqueness', lambda:
+        independent.interpret_verified(raw, instance, result, alias)['classification'] == 'CONDITIONAL_SINGLETON_TAIL')
+    ambiguous = dict(result, masks=[[2, 3] for _ in range(91)])
+    suite.case('status_relation', 'multiple-joints', lambda:
+        independent.interpret_verified(raw, instance, ambiguous, dict(verified, joint_predictions=2))['classification'] == 'NONEMPTY_AMBIGUOUS')
+    suite.case('status_relation', 'no-common-witness', lambda:
+        independent.interpret_verified(raw, instance, dict(result, feasibility_witness=None), verified), True)
+    suite.case('status_relation', 'singleton-joint-inconsistency', lambda:
+        independent.interpret_verified(raw, instance, ambiguous, verified), True)
+    emptyraw, empty, emptyverified = relation_literal(True)
+    emptyinstance = worker.convert_raw(emptyraw, 'v000')
+    emptyinterpretation = independent.interpret_verified(emptyraw, emptyinstance, empty, emptyverified)
+    suite.case('status_relation', 'empty-zero-relation', lambda:
+        worker.semantic_summary(empty, emptyverified, emptyinterpretation)['interpretation']['example_plaintext_tail'] is None)
+    suite.case('status_relation', 'empty-not-vacuous-singleton', lambda:
+        worker.empty_invariants(empty, dict(emptyverified, joint_predictions=1)), True)
+    suite.case('status_relation', 'empty-partial-masks-rejected', lambda:
+        worker.empty_invariants(dict(empty, masks=[]), emptyverified), True)
+    suite.case('status_relation', 'no-first-six-claim', lambda:
+        worker.semantic_summary(result, verified, dict(interpretation, first_six_claimed=True)), True)
+    suite.case('status_relation', 'no-score-ranking-field', lambda:
+        worker.semantic_summary(result, verified, dict(interpretation, score=1)), True)
+
+
+def authority_cases(suite, common, freeze, freeze_pin, approval):
+    suite.case('freeze_authority', 'valid-freeze-metadata', lambda: call_true(common.verify_freeze_object, freeze))
+    for role, field in (('positive', 'path'), ('positive', 'expected_path'), ('empty', 'path'),
+                        ('empty', 'expected_path'), ('K4', 'path')):
+        mutant = copy.deepcopy(freeze)
+        mutant['files'][freeze['inputs'][role][field]] = '0' * 64
+        suite.case('freeze_authority', 'no-input-in-source-' + role + '-' + field,
+                   lambda mutant=mutant: common.verify_freeze_object(mutant), True)
+    suite.case('freeze_authority', 'role-inner-id-binding', lambda:
+        common.verify_freeze_object(changed(freeze, ('inputs', 'positive', 'internal_id'), 'v002')), True)
+    suite.case('freeze_authority', 'fixed-target-pin', lambda:
+        common.verify_freeze_object(changed(freeze, ('inputs', 'K4', 'sha256'), '0' * 64)), True)
+    suite.case('freeze_authority', 'valid-mock-approval', lambda:
+        call_true(common.validate_approval_object, approval, freeze, freeze_pin, 'mocks'))
+    for label, path, value in (
+            ('old-freeze', ('freeze_sha256',), '0' * 64),
+            ('wrong-stage', ('stage',), 'target'),
+            ('extra-job', ('jobs',), ['mock-normal', 'mock-optimized', 'K4-normal']),
+            ('case-capability', ('input_sha256',), {'K4': freeze['inputs']['K4']['sha256']}),
+            ('missing-review', ('source_review_sha256',), None)):
+        suite.case('freeze_authority', 'approval-' + label, lambda path=path, value=value:
+            common.validate_approval_object(changed(approval, path, value), freeze, freeze_pin, 'mocks'), True)
+    for job in ('CTRL-positive-normal', 'K4-normal'):
+        suite.case('freeze_authority', 'mock-no-raw-capability-' + job,
+                   lambda job=job: common.read_authorized_raw(freeze, approval, job), True)
+    def missing():
+        with patched(common, 'read_json', lambda *_a, **_k: (_ for _ in ()).throw(FileNotFoundError('absent grant'))):
+            common.read_authority('mocks', freeze, freeze_pin, '1' * 64)
+    suite.case('freeze_authority', 'missing-approval', missing, True)
+    external = {'schema': 'k4-residual-external-completion-v1', 'job': 'mock-normal',
+        'freeze_sha256': freeze_pin, 'receipt_sha256': '2' * 64, 'exit_code': 0,
+        'completed': True, 'tool_evidence': 'explicit external completion stub'}
+    suite.case('freeze_authority', 'valid-external-completion', lambda:
+        common.validate_external_object(external, 'mock-normal', freeze_pin, '2' * 64))
+    suite.case('freeze_authority', 'external-uncertain-rejected', lambda:
+        common.validate_external_object(dict(external, completed=False), 'mock-normal', freeze_pin, '2' * 64), True)
+    def source_without_case_reads(corrupt=False):
+        def metadata_read(path, _limit=None, _pin=None):
+            require(str(path) == str(ROOT / 'FREEZE.json'), 'only freeze metadata reader')
+            return freeze
+        def metadata_hash(path, _limit=None):
+            value = str(path)
+            require(value not in {v['path'] for v in freeze['inputs'].values()} and
+                    value not in {v['expected_path'] for v in freeze['inputs'].values()},
+                    'source verification attempted actual case path')
+            if value == freeze['python']['executable']:
+                return freeze['python']['sha256']
+            require(value in freeze['files'], 'only frozen metadata source')
+            if corrupt and value == str(ROOT / 'common.py'):
+                return '0' * 64
+            return freeze['files'][value]
+        with patched(common, 'read_json', metadata_read), patched(common, 'sha', metadata_hash):
+            return common.freeze_context(freeze_pin) == freeze
+    suite.case('freeze_authority', 'source-auth-traps-all-real-cases', source_without_case_reads)
+    suite.case('freeze_authority', 'source-byte-pin-mismatch', lambda: source_without_case_reads(True), True)
+    control_grant = {'stage': 'controls', 'jobs': list(common.STAGE_JOBS['controls']),
+        'input_sha256': {role: freeze['inputs'][role]['sha256'] for role in ('positive', 'empty')}}
+    target_grant = {'stage': 'target', 'jobs': list(common.STAGE_JOBS['target']),
+        'input_sha256': {'K4': freeze['inputs']['K4']['sha256']}}
+    suite.case('freeze_authority', 'control-grant-cannot-read-K4', lambda:
+        common.read_authorized_raw(freeze, control_grant, 'K4-normal'), True)
+    suite.case('freeze_authority', 'target-grant-cannot-read-control', lambda:
+        common.read_authorized_raw(freeze, target_grant, 'CTRL-positive-normal'), True)
+    def control_path_only():
+        paths = []
+        def raw_reader(path, _limit, pin):
+            paths.append(str(path))
+            require(str(path) == freeze['inputs']['positive']['path'] and
+                    str(path) != freeze['inputs']['K4']['path'] and
+                    pin == freeze['inputs']['positive']['sha256'], 'control-only raw path/hash')
+            return raw_literal()
+        with patched(common, 'read_json', raw_reader):
+            value = common.read_authorized_raw(freeze, control_grant, 'CTRL-positive-normal')
+        return value == raw_literal() and paths == [freeze['inputs']['positive']['path']]
+    suite.case('freeze_authority', 'control-path-never-opens-target', control_path_only)
+
+
+def command_cases(suite, common, freeze, freeze_pin, approval_pin, job):
+    spec = freeze['jobs'][job]
+    expanded = common.expand(spec['command'], freeze_pin, approval_pin)
+    suite.case('command_mode', 'fixed-expanded-command', lambda:
+        expanded.count(freeze_pin) == 1 and expanded.count(approval_pin) == 1 and
+        expanded[-1] == spec['output'] and expanded.count('-O') == int(spec['optimized']))
+    for label, command in (
+            ('partial-token', ['x${FREEZE_PIN}', '${APPROVAL_PIN}']),
+            ('duplicate-freeze', ['${FREEZE_PIN}', '${FREEZE_PIN}', '${APPROVAL_PIN}']),
+            ('unknown-token', ['${FREEZE_PIN}', '${APPROVAL_PIN}', '${INPUT}']),
+            ('missing-approval', ['${FREEZE_PIN}'])):
+        suite.case('command_mode', label, lambda command=command:
+                   common.expand(command, freeze_pin, approval_pin), True)
+    for label, args in (('extra-argv', expanded[expanded.index(spec['script']) + 1:] + ['--retry']),
+                        ('wrong-output', expanded[expanded.index(spec['script']) + 1:-1] + ['/tmp/result.json'])):
+        suite.case('command_mode', label, lambda args=args:
+            common.validate_child_command(freeze, job, freeze_pin, approval_pin, args), True)
+    opposite = 'mock-normal' if job == 'mock-optimized' else 'mock-optimized'
+    other = common.expand(freeze['jobs'][opposite]['command'], freeze_pin, approval_pin)
+    suite.case('command_mode', 'wrong-mode', lambda:
+        common.validate_child_command(freeze, opposite, freeze_pin, approval_pin,
+            other[other.index(freeze['jobs'][opposite]['script']) + 1:]), True)
+    def double_optimized():
+        selected = freeze['jobs']['mock-optimized']
+        command = common.expand(selected['command'], freeze_pin, approval_pin)
+        args = command[command.index(selected['script']) + 1:]
+        with patched(sys, 'flags', types.SimpleNamespace(isolated=1, optimize=2)):
+            common.validate_child_command(freeze, 'mock-optimized', freeze_pin, approval_pin, args)
+    suite.case('command_mode', 'double-optimized-rejected', double_optimized, True)
+    def unexpected_interpreter_flag():
+        index = expanded.index(spec['script'])
+        mutant = expanded[:index] + ['-S'] + expanded[index:]
+        with patched(sys, 'orig_argv', mutant):
+            common.validate_child_command(freeze, job, freeze_pin, approval_pin, expanded[index + 1:])
+    suite.case('command_mode', 'unexpected-interpreter-flag-rejected', unexpected_interpreter_flag, True)
+
+
+def digest_cases(suite, worker):
+    _raw, result, _verified = relation_literal()
+    digest = worker.producer_digest(result)
+    suite.case('digest', 'root-time-only-exclusion', lambda:
+        worker.producer_digest(changed(result, ('resources', 'wall_seconds'), 9.0)) == digest)
+    suite.case('digest', 'piece-time-only-exclusion', lambda:
+        worker.producer_digest(changed(result, ('pieces', 0, 'core', 'resources', 'wall_seconds'), 9.0)) == digest)
+    suite.case('digest', 'logical-counter-retained', lambda:
+        worker.producer_digest(changed(result, ('resources', 'steps'), 4)) != digest)
+    suite.case('digest', 'relation-bytes-retained', lambda:
+        worker.producer_digest(changed(result, ('masks', 0), [3])) != digest)
+    def overflow():
+        with patched(worker, 'HASH_MAX', 4):
+            worker.producer_digest(result)
+    suite.case('digest', 'stream-cap-predebit', overflow, True)
+    suite.case('digest', 'incomplete-digest-disallowed', lambda:
+        worker.producer_digest(dict(result, status='INCOMPLETE')), True)
+
+
+def collector_cases(suite, bounded, common):
+    suite.case('collector_reaper', 'integer-not-bool', lambda: not common.integer(True))
+    suite.case('collector_reaper', 'finite-not-nan', lambda: not common.numeric(float('nan')))
+    suite.case('collector_reaper', 'finite-not-infinity', lambda: not common.numeric(float('inf')))
+    suite.case('collector_reaper', 'exact-log-cap', lambda: bounded.reserve_log_bytes(3, 1, 4) == 4)
+    suite.case('collector_reaper', 'log-overflow-no-debit', lambda: bounded.reserve_log_bytes(3, 2, 4) is None)
+    suite.case('collector_reaper', 'log-bool-rejected', lambda: bounded.reserve_log_bytes(True, 1, 4), True)
+    writes = []; kills = []
+    capture = bounded.BoundedCapture(lambda stream, data: (writes.append((stream, data)), len(data))[1],
+                                    lambda: kills.append('kill'), 4)
+    suite.case('collector_reaper', 'collector-exact-boundary', lambda:
+        capture.feed(0, b'abcd') is True and capture.written == [4, 0] and writes == [(0, b'abcd')])
+    suite.case('collector_reaper', 'collector-overflow-stops-write', lambda:
+        capture.feed(0, b'x') is False and capture.overflow is True and
+        capture.written == [4, 0] and len(writes) == 1 and kills == ['kill'])
+    suite.case('collector_reaper', 'collector-after-overflow-discard', lambda:
+        capture.feed(1, b'z') is False and capture.written == [4, 0] and len(writes) == 1)
+    suite.case('collector_reaper', 'collector-chunk-bound', lambda: capture.feed(0, b'x' * 16385), True)
+    events = []
+    suite.case('collector_reaper', 'reap-disarm-release-order', lambda:
+        bounded.reap_after_disarm(lambda: events.append('ready'), lambda: events.append('disarm'),
+            lambda: events.append('release'), lambda: (events.append('wait4'), 'usage')[1]) == 'usage' and
+        events == ['ready', 'disarm', 'release', 'wait4'])
+    retried = []
+    def ready():
+        retried.append('ready')
+        if len(retried) == 1:
+            raise InterruptedError()
+    suite.case('collector_reaper', 'reap-retries-only-interrupted-wait', lambda:
+        bounded.reap_after_disarm(ready, lambda: retried.append('disarm'),
+            lambda: retried.append('release'), lambda: (retried.append('wait4'), True)[1]) is True and
+        retried == ['ready', 'ready', 'disarm', 'release', 'wait4'])
+
+
+def state_cases(suite, supervisor, common, freeze, freeze_pin, approval_pin):
+    # Pure metadata guards only: no actual marker, process or receipt is created.
+    state = {'schema': 'k4-residual-target-supervisor-v1', 'freeze_sha256': freeze_pin,
+        'completed': [], 'in_flight': None, 'stopped': False, 'canceled': [],
+        'worker_cpu_actual': 0, 'allocation_charged': 0,
+        'certificate_bytes': 0, 'certificate_files': 0, 'artifact_bytes': 0}
+    suite.case('state_execution', 'clean-initial-state', lambda:
+        call_true(supervisor.validate_state_shape, state, freeze_pin))
+    suite.case('state_execution', 'first-only-job', lambda:
+        call_true(supervisor.require_next_job, state, 'mock-normal'))
+    suite.case('state_execution', 'out-of-order-no-launch', lambda:
+        supervisor.require_next_job(state, 'K4-normal'), True)
+    suite.case('state_execution', 'retained-reserve-blocks-successor', lambda:
+        supervisor.validate_state_shape(dict(state, in_flight={'job': 'mock-normal'}), freeze_pin), True)
+    suite.case('state_execution', 'stopped-blocks-successor', lambda:
+        supervisor.require_next_job(dict(state, stopped=True), 'mock-normal'), True)
+    suite.case('state_execution', 'old-state-freeze', lambda:
+        supervisor.validate_state_shape(dict(state, freeze_sha256='0' * 64), freeze_pin), True)
+    limits = common.stage_limits('mocks')
+    spec = freeze['jobs']['mock-normal']
+    command = common.expand(spec['command'], freeze_pin, approval_pin)
+    execution = {'schema': 'k4-residual-bounded-stage-v1', 'command': command,
+        'cwd': str(ROOT), 'limits': limits, 'supervisor_pid': 101, 'child_pid': 102,
+        'child_reaped': True, 'parent_death_guard': True, 'exit_code': 0,
+        'wall_timeout': False, 'log_overflow': False, 'collector_error': None,
+        'wall_seconds': 1.0, 'child_user_cpu_seconds': 0.5, 'child_system_cpu_seconds': 0.25,
+        'child_cpu_seconds': 0.75, 'supervisor_exclusive_cpu_sample': 0.25,
+        'supervisor_cpu_allocation_charged': 31, 'supervisor_final_write_tail_measured': False,
+        'child_peak_rss_kib': 100, 'supervisor_peak_rss_kib': 100,
+        'log_bytes_reserved': [0, 0], 'log_bytes_read': [0, 0],
+        'logs': [{'path': str(Path(spec['directory']) / name), 'bytes': 0, 'sha256': '0' * 64}
+                 for name in ('stdout.txt', 'stderr.txt')], 'failures': []}
+    suite.case('state_execution', 'complete-execution-receipt', lambda:
+        call_true(supervisor.validate_execution, execution, command, str(ROOT), limits))
+    for label, path, value in (
+            ('unreaped', ('child_reaped',), False), ('unguarded', ('parent_death_guard',), False),
+            ('wall-overshoot', ('wall_seconds',), 121), ('cpu-overshoot', ('child_cpu_seconds',), 32),
+            ('log-overflow', ('log_overflow',), True), ('child-failed', ('exit_code',), 1),
+            ('collector-error', ('collector_error',), 'failure'),
+            ('bool-receipt-count', ('log_bytes_read', 0), True),
+            ('arbitrary-command', ('command',), command + ['--retry'])):
+        suite.case('state_execution', 'execution-' + label, lambda path=path, value=value:
+            supervisor.validate_execution(changed(execution, path, value), command, str(ROOT), limits), True)
+    def missing_output_retained():
+        reserved = dict(state, in_flight={'job': 'mock-normal'})
+        with patched(common, 'read_json', lambda *_a: (_ for _ in ()).throw(FileNotFoundError('missing result'))):
+            try:
+                common.read_json('memory-only missing result')
+            except FileNotFoundError:
+                supervisor.require_next_job(reserved, 'mock-normal')
+                return False
+        return False
+    suite.case('state_execution', 'missing-output-retained-reserve-stops', missing_output_retained, True)
+    def prelaunch_failure():
+        reservation = {'job': 'mock-normal', 'allocation_reserved': 62,
+            'certificate_bytes_reserved': 0, 'artifact_bytes_reserved': 6 * MIB,
+            'command': command, 'approval_sha256': approval_pin}
+        failed = dict(copy.deepcopy(state), in_flight=copy.deepcopy(reservation))
+        try:
+            raise ValueError('literal prelaunch hash/read/disk failure')
+        except ValueError:
+            preserved = supervisor.retain_failed_reservation(failed, 'mock-normal')
+        require(preserved is failed and failed['in_flight'] == reservation and failed['stopped'] is True
+                and failed['canceled'] == list(common.JOBS[1:]) and failed['completed'] == []
+                and failed['allocation_charged'] == 0, 'full failed prelaunch reservation survives')
+        try:
+            supervisor.require_next_job(failed, 'mock-normal')
+        except ValueError:
+            return True
+        return False
+    suite.case('state_execution', 'prelaunch-failure-retains-full-reserve', prelaunch_failure)
+
+
+def file_cases(suite, common):
+    class MemoryPath:
+        def __init__(self, data, symlink=False, reported_size=None):
+            self.data, self.link, self.reported_size = data, symlink, reported_size
+            self.parent = self
+        def is_file(self): return True
+        def is_dir(self): return True
+        def is_symlink(self): return self.link
+        def stat(self):
+            return types.SimpleNamespace(st_size=len(self.data) if self.reported_size is None else self.reported_size)
+        def open(self, mode):
+            if mode == 'xb':
+                raise FileExistsError('one-use destination already exists')
+            require(mode == 'rb', 'read-only in-memory fixture')
+            return io.BytesIO(self.data)
+    def read(data, limit=100, pin=None, symlink=False, size=None):
+        fixture = MemoryPath(data, symlink, size)
+        with patched(common, 'Path', lambda _path: fixture):
+            return common.read_json('memory-only', limit, pin)
+    suite.case('file_boundaries', 'bounded-json-correct-pin', lambda:
+        read(b'{"a":1}', pin=hashlib.sha256(b'{"a":1}').hexdigest()) == {'a': 1})
+    suite.case('file_boundaries', 'reader-duplicate-key', lambda: read(b'{"a":1,"a":2}'), True)
+    suite.case('file_boundaries', 'reader-nan', lambda: read(b'{"a":NaN}'), True)
+    suite.case('file_boundaries', 'reader-infinity', lambda: read(b'{"a":Infinity}'), True)
+    suite.case('file_boundaries', 'reader-symlink', lambda: read(b'{}', symlink=True), True)
+    suite.case('file_boundaries', 'reader-input-pin-mismatch', lambda: read(b'{}', pin='0' * 64), True)
+    suite.case('file_boundaries', 'reader-growth-overflow', lambda: read(b'{}    ', limit=2, size=2), True)
+    def existing():
+        fixture = MemoryPath(b'{}')
+        with patched(common, 'Path', lambda _path: fixture):
+            common.write_new('memory-only', {})
+    suite.case('file_boundaries', 'exclusive-marker-no-retry', existing, True)
+
+
+def pair_cases(suite, supervisor):
+    normal = {key: None for key in supervisor.REPORT_KEYS}
+    normal.update(slot='K4-normal', case_id='v002', python_optimized=False,
+        status='VERIFIED_EMPTY', preflight={'resources': {'wall_seconds': 1.0, 'supports': 4495}},
+        producer={'resources': {'wall_seconds': 1.0, 'steps': 1}},
+        verification={'resources': {'wall_seconds': 1.0, 'fiber_points': 0}},
+        resources={'worker_wall_seconds': 1.0, 'worker_cpu_seconds': 0.5},
+        semantic_summary={'producer_nontime_sha256': '0' * 64, 'joint_predictions': 0})
+    optimized = dict(copy.deepcopy(normal), slot='K4-optimized', python_optimized=True)
+    suite.case('mode_pair', 'same-pair', lambda: supervisor.compare_pair(normal, optimized))
+    timed = copy.deepcopy(optimized)
+    for path in (('preflight', 'resources', 'wall_seconds'), ('producer', 'resources', 'wall_seconds'),
+                 ('verification', 'resources', 'wall_seconds'), ('resources', 'worker_wall_seconds'),
+                 ('resources', 'worker_cpu_seconds')):
+        timed = changed(timed, path, 2.0)
+    suite.case('mode_pair', 'only-frozen-times-excluded', lambda: supervisor.compare_pair(normal, timed))
+    for label, path, value in (
+            ('producer-counter', ('producer', 'resources', 'steps'), 2),
+            ('preflight-counter', ('preflight', 'resources', 'supports'), 4494),
+            ('reference-counter', ('verification', 'resources', 'fiber_points'), 1),
+            ('full-relation-digest', ('semantic_summary', 'producer_nontime_sha256'), '1' * 64),
+            ('joint-count', ('semantic_summary', 'joint_predictions'), 1),
+            ('source-role', ('case_id',), 'v000')):
+        suite.case('mode_pair', 'reject-pair-' + label, lambda path=path, value=value:
+            supervisor.compare_pair(normal, changed(optimized, path, value)), True)
+
+
+def worker_path_cases(suite, common, worker, independent, freeze, freeze_pin, approval_pin):
+    """Only literal stubs enter the actual adapter orchestration, never science.
+
+    Grants/files are in-memory replacements, not active authority objects. The
+    missing-approval case must exit before a raw read. All other failures clear
+    the worker's producer/reference/semantic fields before its captured report.
+    """
+    def one(mode):
+        job = 'CTRL-positive-normal'
+        spec = freeze['jobs'][job]
+        raw, result, verified = relation_literal()
+        result['stats'] = {}
+        result['resources'] = {'steps': 3, 'core_work': 2, 'core_solves': 1,
+                               'core_terms': 2, 'wall_seconds': 0.0}
+        verified['resources'] = {'fiber_points': 1, 'wall_seconds': 0.0}
+        instance = worker.convert_raw(raw, 'v000')
+        expected = {'raw_sha256': freeze['inputs']['positive']['sha256'],
+                    'expected_contexts': instance['contexts'], 'expected_observed': instance['observed']}
+        preflight = {'status': 'WORKLOAD_ADMITTED', 'checked_supports': 4495,
+                     'exact_W': 1, 'lower_bound': 1,
+                     'certificate': {'complete': True}}
+        writes = []; calls = {'raw': 0, 'preflight': 0, 'producer': 0, 'reference': 0}
+        def read_raw(*_a):
+            calls['raw'] += 1
+            return raw
+        def pf(*_a):
+            calls['preflight'] += 1
+            if mode == 'control-gate':
+                return {'status': 'GATE_REJECTED_LOWER_BOUND', 'lower_bound': 1000001,
+                        'exact_W': None, 'certificate': {'complete': True}}
+            return preflight
+        def produce(*_a, **_k):
+            calls['producer'] += 1
+            return result
+        def verify(*_a, **_k):
+            calls['reference'] += 1
+            return dict(verified, status='VERIFIED_EMPTY') if mode == 'reference-mismatch' else verified
+        check = types.SimpleNamespace(convert_raw_independent=independent.convert_raw_independent,
+            interpret_verified=independent.interpret_verified, verify_control_expectations=lambda *_a: True)
+        modules = {str(ROOT / 'input_check.py'): check,
+            str(worker.REFERENCE): types.SimpleNamespace(BudgetV3=lambda **_k: object(), verify_result_v3=verify),
+            str(worker.PREFLIGHT): types.SimpleNamespace(EvidenceBudget=lambda: object(), run=pf),
+            str(worker.CHECKER): object(), str(worker.AFFINE): object(),
+            str(worker.ENGINE): types.SimpleNamespace(Budget=lambda **_k: object(), decode=produce)}
+        def grant(*_a):
+            if mode == 'missing-approval':
+                raise FileNotFoundError('explicit authority absent')
+            return {'stage': 'controls'}
+        def postfreeze(*_a):
+            if mode == 'postseal-mismatch':
+                raise ValueError('changed post-run source bytes')
+            return freeze
+        def expected_read(path, _limit, pin):
+            require(str(path) == freeze['inputs']['positive']['expected_path'] and
+                    str(path) != freeze['inputs']['K4']['path'] and
+                    pin == freeze['inputs']['positive']['expected_sha256'], 'control-only expected path/hash')
+            return expected
+        args = ['--job', job, '--freeze-sha256', freeze_pin,
+                '--approval-sha256', approval_pin, '--output', spec['output']]
+        with contextlib.ExitStack() as stack:
+            for obj, name, replacement in (
+                    (worker, 'bootstrap', lambda _p: (common, freeze)),
+                    (common, 'require_child_bounds', lambda _s: None),
+                    (common, 'validate_child_command', lambda *_a: spec),
+                    (common, 'read_authority', grant), (common, 'read_authorized_raw', read_raw),
+                    (common, 'read_json', expected_read),
+                    (common, 'load_pinned', lambda _n, path, _p: modules[str(path)]),
+                    (common, 'freeze_context', postfreeze),
+                    (worker, 'write_report', lambda _p, report: writes.append(copy.deepcopy(report)))):
+                stack.enter_context(patched(obj, name, replacement))
+            try:
+                status = worker.main(args)
+            except FileNotFoundError:
+                return mode == 'missing-approval' and calls == {'raw': 0, 'preflight': 0, 'producer': 0, 'reference': 0} and writes == []
+        require(len(writes) == 1, 'one captured failure report')
+        report = writes[0]
+        return status == 1 and report['status'] == 'INCOMPLETE_OR_FAILED' and all(
+            report[name] is None for name in ('producer', 'verification', 'semantic_summary', 'control_check')) and (
+            calls['producer'] == calls['reference'] == 0 if mode == 'control-gate' else calls['reference'] == 1)
+    for mode in ('missing-approval', 'reference-mismatch', 'postseal-mismatch', 'control-gate'):
+        suite.case('worker_fail_closed', 'worker-path-' + mode, lambda mode=mode: one(mode))
+
+
+def report_cases(suite, supervisor, freeze, freeze_pin, approval_pin):
+    """Fabricated metadata shapes only, not certificates or scientific claims."""
+    def complete(job, empty):
+        spec = freeze['jobs'][job]
+        pf_counts = {name: 0 for name in supervisor.PREFLIGHT_COUNTERS}
+        pf_counts.update(wall_seconds=0.0, supports=4495, solve_calls=4495, certificate_checks=8990)
+        producer_counts = {name: 0 for name in supervisor.PRODUCER_COUNTERS}
+        reference_counts = {name: 0 for name in supervisor.REFERENCE_COUNTERS}
+        reference_counts['fiber_points'] = 0 if empty else 1
+        n = 0 if empty else 1
+        return {'schema': 'k4-residual-slot-report-v1', 'slot': job,
+            'stage': spec['stage'], 'input_role': spec['input_key'], 'case_id': spec['internal_id'],
+            'python_optimized': spec['optimized'], 'freeze_sha256': freeze_pin,
+            'input_sha256': freeze['inputs'][spec['input_key']]['sha256'],
+            'approval_sha256': approval_pin, 'source_sha256': freeze['files'],
+            'status': 'VERIFIED_EMPTY' if empty else 'VERIFIED_EXACT',
+            'preflight': {'status': 'WORKLOAD_ADMITTED', 'checked_supports': 4495,
+                'lower_bound': n, 'exact_W': n, 'resources': pf_counts,
+                'certificate': {'name': 'case.cert.jsonl', 'bytes': 1, 'sha256': '0' * 64, 'complete': True}},
+            'producer': {'status': 'EMPTY' if empty else 'EXACT',
+                'resources': dict(producer_counts, wall_seconds=0.0),
+                'stats': {name: 0 for name in ('containers', 'beta_candidates', 'incompatible_beta',
+                    'excluded_B', 'eligible_pieces', 'empty_pieces', 'feasible_pieces')}},
+            'verification': {'version': 'independent-residual-reference-3',
+                'source_sha256': freeze['files']['source/scientific/reference_v3.py'],
+                'request_sha256': '0' * 64, 'status': 'VERIFIED_EMPTY' if empty else 'VERIFIED_EXACT',
+                'resources': dict(reference_counts, wall_seconds=0.0), 'pieces_checked': n,
+                'canonical_functions': n, 'original_lifts': n, 'joint_predictions': n,
+                'stats': {name: 0 for name in ('supports', 'beta_candidates', 'eligible_beta',
+                    'retained_points', 'legacy_ambient_points_equivalent')}},
+            'semantic_summary': {'producer_nontime_sha256': '0' * 64,
+                'masks': [[] if empty else [2] for _ in range(91)],
+                'pieces': n, 'canonical_functions': n, 'original_lifts': n, 'joint_predictions': n,
+                'feasibility_witness': None if empty else {'piece': 'stub', 'theta': [[28, 1], [29, 1]]},
+                'interpretation': {'classification': 'EMPTY' if empty else 'CONDITIONAL_SINGLETON_TAIL',
+                    'plaintext_masks': [[] if empty else ['Y'] for _ in range(91)],
+                    'example_plaintext_tail': None if empty else 'Y' * 91, 'first_six_claimed': False}},
+            'control_check': {'status': 'PASS', 'expected_sha256': freeze['inputs'][spec['input_key']]['expected_sha256']}
+                if spec['stage'] == 'controls' else None,
+            'resources': {'worker_wall_seconds': 0.0, 'worker_cpu_seconds': 0.0,
+                'producer_counters': producer_counts, 'reference_counters': reference_counts,
+                'producer_attempted': True, 'reference_attempted': True}, 'reason': None}
+    exact = complete('CTRL-positive-normal', False)
+    empty = complete('CTRL-empty-normal', True)
+    def checked(report):
+        return supervisor.validate_report(report, freeze['jobs'][report['slot']], freeze,
+                                           freeze_pin, approval_pin)
+    suite.case('supervisor_reports', 'report-complete-EXACT', lambda: checked(exact) == 'VERIFIED_EXACT')
+    suite.case('supervisor_reports', 'report-complete-EMPTY', lambda: checked(empty) == 'VERIFIED_EMPTY')
+    gate = complete('K4-normal', False)
+    gate.update(status='CERTIFIED_RESOURCE_GATE', producer=None, verification=None,
+                semantic_summary=None, control_check=None)
+    gate['preflight'].update(status='GATE_REJECTED_LOWER_BOUND', checked_supports=1,
+                            lower_bound=1000001, exact_W=None)
+    gate['preflight']['resources'].update(supports=1, solve_calls=1, certificate_checks=2)
+    gate['resources'].update(producer_counters=None, reference_counters=None,
+                             producer_attempted=False, reference_attempted=False)
+    suite.case('supervisor_reports', 'report-resource-gate-no-result', lambda: checked(gate) == 'CERTIFIED_RESOURCE_GATE')
+    incomplete = dict(copy.deepcopy(exact), status='INCOMPLETE_OR_FAILED', producer=None,
+        verification=None, semantic_summary=None, control_check=None, reason='literal failed stage')
+    suite.case('supervisor_reports', 'report-incomplete-no-result', lambda: checked(incomplete) == 'INCOMPLETE_OR_FAILED')
+    rejects = (
+        ('EXACT-crossed-verifier', changed(exact, ('verification', 'status'), 'VERIFIED_EMPTY')),
+        ('EMPTY-crossed-verifier', changed(empty, ('verification', 'status'), 'VERIFIED_EXACT')),
+        ('EMPTY-partial-inventory', changed(empty, ('semantic_summary', 'masks'), [])),
+        ('W-zero-alone', dict(empty, producer=None, verification=None, semantic_summary=None)),
+        ('incomplete-partial-claim', dict(incomplete, semantic_summary=exact['semantic_summary'])),
+        ('gate-partial-claim', dict(gate, semantic_summary=exact['semantic_summary'])),
+        ('bool-cap-counter', changed(exact, ('preflight', 'resources', 'supports'), True)),
+        ('extra-resource-field', changed(exact, ('producer', 'resources'), dict(exact['producer']['resources'], score=1))),
+        ('over-cap-wall', changed(exact, ('preflight', 'resources', 'wall_seconds'), 61.0)))
+    for label, report in rejects:
+        suite.case('supervisor_reports', 'reject-report-' + label, lambda report=report: checked(report), True)
+
+
+def loader_cases(suite, common, authenticated_loader):
+    """Real loader helper, in-memory literal bytes, no imported test module file."""
+    literal = b'VALUE = 7\n'
+    class MemoryPath:
+        def __init__(self, oversized=False): self.oversized = oversized
+        def __str__(self): return '/memory-only/frozen-literal.py'
+        def is_file(self): return True
+        def is_symlink(self): return False
+        def stat(self): return types.SimpleNamespace(st_size=MIB + 1 if self.oversized else len(literal))
+        def open(self, mode):
+            require(mode == 'rb', 'literal-loader read mode')
+            return io.BytesIO(literal)
+    def one(mode):
+        path = MemoryPath(mode == 'oversized')
+        name = 'k4_mock_authenticated_literal_' + mode
+        events = {'compile': 0, 'exec_module': 0}
+        original_compile = builtins.compile
+        class CacheTrap:
+            def create_module(self, _spec): return None
+            def exec_module(self, _module):
+                events['exec_module'] += 1
+                raise ValueError('cache execution forbidden')
+        def spec_for(module_name, module_path):
+            require(module_name == name and str(module_path) == str(path), 'fixed literal module identity')
+            spec = importlib.machinery.ModuleSpec(module_name, CacheTrap(), origin=str(module_path))
+            spec.has_location = True
+            return spec
+        def compile_counted(source, filename, mode_value, **kwargs):
+            events['compile'] += 1
+            require(source == literal and filename == str(path) and mode_value == 'exec'
+                    and kwargs == {'dont_inherit': True, 'optimize': sys.flags.optimize},
+                    'authenticated compiler byte/flag identity')
+            return original_compile(source, filename, mode_value, **kwargs)
+        try:
+            with patched(common, 'Path', lambda _p: path), \
+                 patched(importlib.util, 'spec_from_file_location', spec_for), \
+                 patched(builtins, 'compile', compile_counted):
+                pin = '0' * 64 if mode == 'wrong-hash' else hashlib.sha256(literal).hexdigest()
+                try:
+                    module = authenticated_loader(name, path, pin)
+                except ValueError:
+                    return mode in ('wrong-hash', 'oversized') and events == {'compile': 0, 'exec_module': 0} and name not in sys.modules
+            return mode in ('valid', 'no-cache') and module.VALUE == 7 and module.__name__ == name and \
+                module.__file__ == str(path) and module.__spec__.name == name and \
+                sys.modules.get(name) is module and events == {'compile': 1, 'exec_module': 0}
+        finally:
+            sys.modules.pop(name, None)
+    for label, mode in (
+            ('authenticated-literal-module-identity', 'valid'), ('wrong-hash-before-compile', 'wrong-hash'),
+            ('source-cap-before-compile', 'oversized'), ('loader-exec-module-never-used', 'no-cache')):
+        suite.case('byte_loader', label, lambda mode=mode: one(mode))
+
+
+def authorized_run(args, actual, counts):
+    common, freeze = bootstrap(args.freeze_sha256)
+    require(args.job in ('mock-normal', 'mock-optimized'), 'exact mock job only')
+    common.require_child_bounds('mocks')
+    spec = common.validate_child_command(freeze, args.job, args.freeze_sha256, args.approval_sha256, actual)
+    require(args.output == spec['output'] and freeze['mock_counts'] == EXPECTED_COUNTS,
+            'frozen output and exact finite mock counts')
+    approval = common.read_authority('mocks', freeze, args.freeze_sha256, args.approval_sha256)
+    modules = {'common.py': common, 'protocol_mock_tests.py': sys.modules[__name__]}
+    sources = {}
+    for name in common.LOCAL_SOURCES:
+        content = _bytes(ROOT / name, MIB)
+        require(hashlib.sha256(content).hexdigest() == freeze['files'][str(ROOT / name)],
+                'inert-probe source hash')
+        sources[name] = content
+    for name in ('worker.py', 'input_check.py', 'bounded_stage.py', 'supervisor.py', 'seal_results.py'):
+        modules[name] = memory_module('k4_mock_operational_' + name[:-3], ROOT / name, sources[name])
+    forbidden = {item['path'] for item in freeze['inputs'].values()} | {
+        item['expected_path'] for item in freeze['inputs'].values() if item['expected_path'] is not None}
+    suite = Suite()
+    authenticated_loader = common.load_pinned
+    report = {'schema': REPORT_SCHEMA, 'job': args.job, 'freeze_sha256': args.freeze_sha256,
+        'approval_sha256': args.approval_sha256, 'python_optimized': spec['optimized'],
+        'status': 'INCOMPLETE_OR_FAILED', 'counts': suite.counts,
+        'actual_forbidden_calls': counts, 'reason': None}
+    try:
+        with forbidden_io(common, modules['worker.py'], forbidden, counts):
+            inert_cases(suite, sources, modules)
+            raw_and_mapping_cases(suite, common, modules['worker.py'], modules['input_check.py'])
+            relation_cases(suite, modules['worker.py'], modules['input_check.py'])
+            authority_cases(suite, common, freeze, args.freeze_sha256, approval)
+            command_cases(suite, common, freeze, args.freeze_sha256, args.approval_sha256, args.job)
+            digest_cases(suite, modules['worker.py'])
+            collector_cases(suite, modules['bounded_stage.py'], common)
+            state_cases(suite, modules['supervisor.py'], common, freeze,
+                        args.freeze_sha256, args.approval_sha256)
+            file_cases(suite, common)
+            pair_cases(suite, modules['supervisor.py'])
+            worker_path_cases(suite, common, modules['worker.py'], modules['input_check.py'],
+                              freeze, args.freeze_sha256, args.approval_sha256)
+            report_cases(suite, modules['supervisor.py'], freeze, args.freeze_sha256, args.approval_sha256)
+            loader_cases(suite, common, authenticated_loader)
+        require(suite.counts == EXPECTED_COUNTS and all(suite.names[group] == set(names)
+                for group, names in EXPECTED_CASES.items()) and all(value == 0 for value in counts.values()),
+                'complete finite counts and zero forbidden actual calls')
+        common.freeze_context(args.freeze_sha256)
+        require(common.sha(ROOT / 'approvals' / 'mocks.json', 65536) == args.approval_sha256,
+                'post-mock approval unchanged')
+        report['status'] = 'PASS'
+    except BaseException as error:
+        report['reason'] = type(error).__name__ + ': ' + str(error)[:500]
+    return common, report
+
+
+def main(argv=None):
+    parser = argparse.ArgumentParser(description='Finite operational stubs only; no implicit invocation.')
+    for flag in ('job', 'freeze-sha256', 'approval-sha256', 'output'):
+        parser.add_argument('--' + flag, required=True)
+    args = parser.parse_args(argv)
+    counts = {key: 0 for key in FORBIDDEN_COUNTER_KEYS}
+    actual = list(sys.argv[1:] if argv is None else argv)
+    with source_only_guard(counts):
+        common, report = authorized_run(args, actual, counts)
+    # The only mock-worker write is the fixed result after all guards restore;
+    # stdout/stderr and the one-use reservation belong to the outer supervisor.
+    common.write_new(args.output, report)
+    return 0 if report['status'] == 'PASS' else 1
+
+
+if __name__ == '__main__':
+    sys.exit(main())
```
