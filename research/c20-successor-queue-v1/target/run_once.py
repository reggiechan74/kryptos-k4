"""One-shot bounded supervisor. Metadata validation and exactly one target child."""
import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT.parent / 'k4-c20-target-v1-run'
APPROVAL = ROOT.parent / 'k4-c20-target-v1-approval.json'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_new(path, payload):
    with path.open('x') as f:
        json.dump(payload, f, sort_keys=True, indent=2)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())


def check_sources(expected):
    require(sha(ROOT / 'FREEZE.json') == expected, 'freeze mismatch')
    freeze = json.loads((ROOT / 'FREEZE.json').read_text())
    require(set(freeze['files']) == {'c20.py', 'reference.py', 'target.py', 'run_once.py', 'PROTOCOL.md'}, 'source inventory')
    for name, pin in freeze['files'].items():
        require(sha(ROOT / name) == pin, 'source changed: '+name)
    require(sha(Path(sys.executable).resolve()) == freeze['interpreter_sha256'], 'interpreter mismatch')
    require(sha(Path(freeze['timeout_binary'])) == freeze['timeout_sha256'], 'outer timeout mismatch')
    require(sha(Path(freeze['input_path'])) == freeze['input_sha256'], 'canonical input changed')
    return freeze


def main():
    # This supervisor never executes experiment functions itself.
    signal.signal(signal.SIGXCPU, signal.SIG_DFL)
    # Hard10 permits the forked child to install its8-second hard limit;
    # the supervisor itself is terminated by the default SIGXCPU at soft2.
    resource.setrlimit(resource.RLIMIT_CPU, (2, 10))
    resource.setrlimit(resource.RLIMIT_AS, (128*1024*1024, 128*1024*1024))
    resource.setrlimit(resource.RLIMIT_FSIZE, (1024*1024, 1024*1024))
    parser = argparse.ArgumentParser()
    parser.add_argument('--freeze-sha256', required=True)
    parser.add_argument('--approval-sha256', required=True)
    args = parser.parse_args()
    began = time.monotonic()
    cpu_start = resource.getrusage(resource.RUSAGE_SELF)
    f = check_sources(args.freeze_sha256)
    require(sha(APPROVAL) == args.approval_sha256, 'approval hash mismatch')
    approved_bytes = APPROVAL.read_bytes()
    approval = json.loads(approved_bytes)
    require(approval['status'] == 'APPROVED_TARGET_ONLY' and approval['job'] == 'C20-target-once'
            and approval['freeze_sha256'] == args.freeze_sha256, 'wrong approval')
    require(f['child_cpu_seconds'] == 8 and f['supervisor_cpu_seconds'] == 2
            and f['memory_bytes'] == 134217728 and f['external_wall_seconds'] == 30,
            'caps mismatch')
    OUTPUT.mkdir(exist_ok=True)
    require(not any(OUTPUT.iterdir()), 'output directory must be empty')
    write_new(OUTPUT / 'ATTEMPT.json', {'status': 'CONSUMED_FOR_ONE_ATTEMPT',
              'freeze_sha256': args.freeze_sha256, 'approval_sha256': args.approval_sha256})
    parent = os.getpid()

    def child_limits():
        # Linux parent-death guard closes an orphan gap before the child exec.
        libc = ctypes.CDLL(None, use_errno=True)
        if libc.prctl(1, signal.SIGKILL, 0, 0, 0) != 0 or os.getppid() != parent:
            os._exit(125)
        resource.setrlimit(resource.RLIMIT_CPU, (8, 8))
        resource.setrlimit(resource.RLIMIT_AS, (128*1024*1024, 128*1024*1024))
        resource.setrlimit(resource.RLIMIT_FSIZE, (1024*1024, 1024*1024))

    command = [sys.executable, '-I', '-B', str(ROOT / 'target.py'), '--freeze-sha256', args.freeze_sha256]
    status = 'INCOMPLETE'
    error = None
    returncode = None
    result = None
    timed_out = False
    child = None
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    try:
        with (OUTPUT / 'stdout.json').open('xb') as out, (OUTPUT / 'stderr.log').open('xb') as err:
            child = subprocess.Popen(command, cwd=str(ROOT), stdout=out, stderr=err,
                                     preexec_fn=child_limits, start_new_session=True,
                                     env={'PATH': '/usr/bin:/bin', 'LANG': 'C.UTF-8'})
            try:
                returncode = child.wait(timeout=max(0.1, 25-(time.monotonic()-began)))
            except subprocess.TimeoutExpired:
                timed_out = True
                os.killpg(child.pid, signal.SIGKILL)
                returncode = child.wait()
        require(not timed_out and returncode == 0, 'child failure or timeout')
        require((OUTPUT / 'stderr.log').stat().st_size == 0, 'unexpected stderr')
        result = json.loads((OUTPUT / 'stdout.json').read_text())
        require(result['status'] == 'COMPLETE_SEVEN_DECODERS' and result['freeze_sha256'] == args.freeze_sha256,
                'result status/binding')
        require(result['candidate_count'] == 7 and result['clue_positions'] == 24
                and len(result['records']) == 7
                and [r['phase'] for r in result['records']] == list(range(7))
                and all(r['reference_agreement'] and r['full_reencryption'] for r in result['records']),
                'result expected counts/controls')
        require(result['input_sha256'] == f['input_sha256'], 'result input binding')
        for row in result['records']:
            require(type(row['phase']) is int and type(row['plaintext']) is str
                    and len(row['plaintext']) == 97
                    and all('A' <= ch <= 'Z' for ch in row['plaintext']), 'result plaintext framing')
            mask = row['clue_mask']
            require(type(mask) is list and len(mask) == 24
                    and all(type(x) is bool for x in mask), 'result mask framing')
            require(type(row['clue_matches']) is int and row['clue_matches'] == sum(mask)
                    and type(row['compatible']) is bool and row['compatible'] == all(mask)
                    and row['reference_agreement'] is True and row['full_reencryption'] is True,
                    'result row consistency')
        hits = [row['phase'] for row in result['records'] if row['compatible']]
        require(result['compatible_phases'] == hits
                and all(type(p) is int for p in result['compatible_phases'])
                and result['conclusion'] == ('COMPATIBLE_CANDIDATE_NOT_SOLUTION' if hits else
                                              'EXACT_SEVEN_PHASE_MODEL_NEGATIVE'), 'result conclusion')
        check_sources(args.freeze_sha256)
        require(APPROVAL.read_bytes() == approved_bytes, 'approval changed')
        status = 'COMPLETE_TARGET_CHECK'
    except Exception as exc:
        error = type(exc).__name__ + ': ' + str(exc)
        if child is not None and child.poll() is None:
            os.killpg(child.pid, signal.SIGKILL)
            returncode = child.wait()
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    artifact_inventory = {p.name: {'bytes': p.stat().st_size, 'sha256': sha(p)} for p in OUTPUT.iterdir() if p.is_file()}
    self_end = resource.getrusage(resource.RUSAGE_SELF)
    child_cpu = after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime
    supervisor_total_sample = self_end.ru_utime+self_end.ru_stime
    final_wall_sample = time.monotonic()-began
    if child_cpu > 8 or supervisor_total_sample > 2 or final_wall_sample >= 30:
        status = 'INCOMPLETE'
        error = 'final resource usage exceeded declared bound'
    receipt = {'schema': 'c20-one-shot-receipt-v1', 'status': status, 'error': error,
               'freeze_sha256': args.freeze_sha256, 'approval_sha256': args.approval_sha256,
               'command': command, 'actual_child_returncode': returncode, 'child_reaped': child is not None and child.poll() is not None,
               'wall_seconds': final_wall_sample, 'timed_out': timed_out,
               'child_cpu_seconds': child_cpu,
               'supervisor_cpu_seconds_sample': supervisor_total_sample,
               'supervisor_sample_scope': 'cumulative process CPU including startup and artifact hashing, before receipt serialization/write/final print',
               'unmeasured_tail': 'receipt serialization/fsync/hash/final print and outer timeout/tool overhead are not claimed measured',
               'external_wall_contract': f['command_template'],
               'child_maxrss_kib': after.ru_maxrss, 'nominal_cpu_consumed': 10,
               'target_child_started': child is not None, 'complete_target_result': status == 'COMPLETE_TARGET_CHECK', 'retry_authorized': False,
               'artifacts': artifact_inventory}
    require(sum(x['bytes'] for x in receipt['artifacts'].values()) < 1024*1024-65536, 'output budget')
    write_new(OUTPUT / 'RECEIPT.json', receipt)
    print(json.dumps({'status': status, 'receipt_sha256': sha(OUTPUT / 'RECEIPT.json')}, sort_keys=True))
    return 0 if status == 'COMPLETE_TARGET_CHECK' else 1


if __name__ == '__main__':
    raise SystemExit(main())
