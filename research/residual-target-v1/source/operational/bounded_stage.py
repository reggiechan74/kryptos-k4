"""Byte-preserved bounded collector/guard/reaper from validated stage.
No CLI, input access, launch or write occurs at import. Only the separately
approved fixed-job supervisor may call run_bounded after durable reservation.
"""
import ctypes
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import selectors
import signal
import sys
import time
MIB = 1024 * 1024
LOG_MAX = MIB
JSON_MAX = 2 * MIB
CHUNK = 16384
VERSION = 'k4-residual-bounded-stage-v1'

def require(condition, message):
    if not condition:
        raise ValueError(message)


def numeric(value):
    return ((type(value) is int and value >= 0) or
            (type(value) is float and math.isfinite(value) and value >= 0))


def integer(value, maximum=None):
    return type(value) is int and value >= 0 and (maximum is None or value <= maximum)


def digest_string(value):
    return type(value) is str and len(value) == 64 and all(c in '0123456789abcdef' for c in value)


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False) + '\n').encode()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def read_json(path, limit=JSON_MAX):
    path = Path(path)
    require(path.is_file() and not path.is_symlink(), 'regular JSON file required')
    require(path.stat().st_size <= limit, 'JSON file byte limit')
    with path.open('rb') as handle:
        data = handle.read(limit + 1)
    require(len(data) <= limit, 'JSON file grew beyond byte limit')
    return json.loads(data, object_pairs_hook=unique_object,
        parse_constant=lambda _x: (_ for _ in ()).throw(ValueError('nonfinite JSON number')))


def sha(path, limit=None):
    path = Path(path)
    require(path.is_file() and not path.is_symlink(), 'regular hash input required')
    size = path.stat().st_size
    if limit is not None:
        require(size <= limit, 'hash input byte limit')
    digest = hashlib.sha256()
    total = 0
    with path.open('rb') as handle:
        while True:
            data = handle.read(MIB)
            if not data:
                break
            total += len(data)
            if limit is not None:
                require(total <= limit, 'hash input grew beyond limit')
            digest.update(data)
    require(total == size, 'hash input size changed')
    return digest.hexdigest()


def fsync_dir(path):
    fd = os.open(str(path), os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def write_new(path, value):
    path = Path(path)
    data = canonical(value)
    require(len(data) <= JSON_MAX, 'JSON output byte limit')
    with path.open('xb') as handle:
        require(handle.write(data) == len(data), 'short JSON write')
        handle.flush()
        os.fsync(handle.fileno())
    fsync_dir(path.parent)


def atomic(path, value):
    """Only fixed state/resource JSON uses .tmp; partial bytes are preserved."""
    path = Path(path)
    temporary = path.with_name(path.name + '.tmp')
    data = canonical(value)
    require(len(data) <= JSON_MAX, 'JSON output byte limit')
    with temporary.open('xb') as handle:
        require(handle.write(data) == len(data), 'short JSON write')
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)
    fsync_dir(path.parent)


def death_guard(expected=None):
    parent = os.getppid() if expected is None else expected
    require(type(parent) is int and parent >= 1, 'expected positive parent PID')
    if os.getppid() != parent:
        os.kill(os.getpid(), signal.SIGKILL)
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.prctl(1, signal.SIGKILL, 0, 0, 0) != 0:
        raise OSError(ctypes.get_errno(), 'PR_SET_PDEATHSIG')
    if os.getppid() != parent:
        os.kill(os.getpid(), signal.SIGKILL)


def check_limits(limits):
    keys = {'worker_cpu_soft', 'worker_cpu_hard', 'supervisor_cpu_soft',
            'supervisor_cpu_hard', 'worker_address_space_bytes',
            'supervisor_address_space_bytes', 'wall_seconds', 'log_max_bytes'}
    require(type(limits) is dict and set(limits) == keys, 'exact launch limit schema')
    require(all(integer(value) and value > 0 for value in limits.values()), 'positive integer launch caps')
    require(limits['worker_cpu_soft'] <= limits['worker_cpu_hard'], 'worker CPU ordering')
    require(limits['supervisor_cpu_soft'] <= limits['supervisor_cpu_hard'], 'supervisor CPU ordering')
    require(limits['log_max_bytes'] == LOG_MAX, 'fixed one-MiB log cap')


def reserve_log_bytes(used, amount, maximum=LOG_MAX):
    require(integer(used, maximum) and integer(amount) and integer(maximum), 'log counter types')
    if amount > maximum - used:
        return None
    return used + amount


class BoundedCapture:
    """Actual collector debit/write policy; injected callbacks enable no-child mocks."""
    def __init__(self, write_callback, kill_callback, maximum=LOG_MAX):
        require(integer(maximum, LOG_MAX) and maximum > 0, 'bounded capture limit')
        require(callable(write_callback) and callable(kill_callback), 'capture callbacks')
        self.maximum, self.write_callback, self.kill_callback = maximum, write_callback, kill_callback
        self.written, self.read_bytes = [0,0], [0,0]
        self.overflow = False

    def feed(self, index, data):
        require(type(index) is int and index in (0,1), 'capture stream index')
        require(type(data) is bytes and 0 < len(data) <= CHUNK, 'bounded nonempty pipe chunk')
        self.read_bytes[index] += len(data)
        if self.overflow:
            return False
        following = reserve_log_bytes(self.written[index],len(data),self.maximum)
        if following is None:
            self.overflow = True
            self.kill_callback()
            return False
        self.written[index] = following
        require(self.write_callback(index,data) == len(data), 'short log write')
        return True


def reap_after_disarm(wait_ready, disarm, release_pid_guard, wait_usage):
    """Ordered unreaped exit -> alarm disarm -> guard release -> wait4.

    Callbacks are real OS operations in run_bounded and no-child stubs in mocks.
    An interrupted wait is the only retried operation; no child is relaunched.
    """
    for callback in (wait_ready,disarm,release_pid_guard,wait_usage):
        require(callable(callback), 'reaping callback')
    while True:
        try:
            wait_ready()
            break
        except InterruptedError:
            continue
    disarm()
    release_pid_guard()
    return wait_usage()


def run_bounded(command, cwd, stdout_path, stderr_path, limits):
    """Launch exactly one child; collect two bounded pipes in this supervisor.

    Process launch is reachable only through explicit callers, never import.
    The caller must durably reserve the invocation before calling this function.
    No process/thread is created to collect logs. waitid/WNOWAIT preserves the
    child's PID until alarm disarming and wait4; kill never targets a reaped PID.
    """
    check_limits(limits)
    require(type(command) is list and command and all(type(x) is str and len(x) <= 4096 for x in command), 'bounded argv')
    require(len(command) <= 64 and Path(command[0]).is_absolute(), 'absolute bounded command')
    cwd = Path(cwd)
    require(cwd.is_absolute() and cwd.is_dir() and not cwd.is_symlink(), 'canonical cwd')
    paths = [Path(stdout_path), Path(stderr_path)]
    require(all(p.is_absolute() and p.parent.is_dir() and not p.parent.is_symlink() for p in paths), 'log paths')
    require(paths[0] != paths[1], 'distinct logs')
    death_guard()
    max_cpu = max(limits['worker_cpu_hard'], limits['supervisor_cpu_hard'])
    max_memory = max(limits['worker_address_space_bytes'], limits['supervisor_address_space_bytes'])
    resource.setrlimit(resource.RLIMIT_CPU, (limits['supervisor_cpu_soft'], max_cpu))
    resource.setrlimit(resource.RLIMIT_AS, (limits['supervisor_address_space_bytes'], max_memory))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_FSIZE, (32*MIB, 32*MIB))
    logfds = [os.open(str(p), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600) for p in paths]
    pipes = [os.pipe(), os.pipe()]
    started = time.monotonic()
    supervisor_pid = os.getpid()
    child = os.fork()
    if child == 0:
        try:
            for index, (readfd, writefd) in enumerate(pipes):
                os.close(readfd)
                os.dup2(writefd, index+1)
                os.close(writefd)
            for fd in logfds:
                os.close(fd)
            death_guard(supervisor_pid)
            os.setsid()
            signal.signal(signal.SIGXCPU, signal.SIG_DFL)
            signal.signal(signal.SIGALRM, signal.SIG_DFL)
            resource.setrlimit(resource.RLIMIT_CPU, (limits['worker_cpu_soft'], limits['worker_cpu_hard']))
            memory = limits['worker_address_space_bytes']
            resource.setrlimit(resource.RLIMIT_AS, (memory, memory))
            os.chdir(str(cwd))
            os.execve(command[0], command, {'PATH':'/usr/bin:/bin', 'LANG':'C.UTF-8'})
        except BaseException as error:
            os.write(2, canonical({'schema':'bounded-child-setup-error-v2',
                'type':type(error).__name__, 'message':str(error)[:400]})[:1024])
            os._exit(125)
    for _readfd, writefd in pipes:
        os.close(writefd)
    resource.setrlimit(resource.RLIMIT_CPU, (limits['supervisor_cpu_soft'], limits['supervisor_cpu_hard']))
    memory = limits['supervisor_address_space_bytes']
    resource.setrlimit(resource.RLIMIT_AS, (memory, memory))
    selector = selectors.DefaultSelector()
    for index, (readfd, _writefd) in enumerate(pipes):
        os.set_blocking(readfd, False)
        selector.register(readfd, selectors.EVENT_READ, index)
    timed_out = False
    collector_error = None
    child_unreaped = True
    child_exited = False
    deadline = started + limits['wall_seconds']

    def kill_unreaped():
        if not child_unreaped:
            return
        try:
            os.killpg(child, signal.SIGKILL)
        except ProcessLookupError:
            try:
                os.kill(child, signal.SIGKILL)
            except ProcessLookupError:
                pass

    def timeout(_signum, _frame):
        nonlocal timed_out
        if child_unreaped:
            timed_out = True
            kill_unreaped()

    capture = BoundedCapture(lambda index,data: os.write(logfds[index],data), kill_unreaped)
    signal.signal(signal.SIGALRM, timeout)
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        timeout(signal.SIGALRM, None)
    else:
        signal.setitimer(signal.ITIMER_REAL, remaining)
    try:
        while not child_exited or selector.get_map():
            if not child_exited:
                try:
                    found = os.waitid(os.P_PID, child, os.WEXITED | os.WNOHANG | os.WNOWAIT)
                    child_exited = found is not None
                except InterruptedError:
                    pass
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                timeout(signal.SIGALRM, None)
                break  # No pipe drain is permitted beyond the frozen deadline.
            events = selector.select(min(0.05, remaining)) if selector.get_map() else []
            if not events and not selector.get_map() and not child_exited:
                time.sleep(min(0.01, remaining))
            for key, _mask in events:
                fd, index = key.fd, key.data
                try:
                    data = os.read(fd, CHUNK)
                except BlockingIOError:
                    continue
                if not data:
                    selector.unregister(fd)
                    os.close(fd)
                    continue
                capture.feed(index,data)
    except BaseException as error:
        collector_error = type(error).__name__ + ':' + str(error)[:300]
        kill_unreaped()
    finally:
        for key in list(selector.get_map().values()):
            selector.unregister(key.fd)
            os.close(key.fd)
        selector.close()
    # If an exceptional collector exit ended early, kill and then await an
    # unreaped exit. All time after the deadline is cleanup, never a PASS.
    if collector_error is not None or timed_out or capture.overflow:
        kill_unreaped()
    def release_pid_guard():
        nonlocal child_unreaped
        child_unreaped = False
    _, wait_status, usage = reap_after_disarm(
        lambda: os.waitid(os.P_PID,child,os.WEXITED|os.WNOWAIT),
        lambda: signal.setitimer(signal.ITIMER_REAL,0), release_pid_guard,
        lambda: os.wait4(child,0))
    for fd in logfds:
        os.fsync(fd)
        os.close(fd)
    for parent in {p.parent for p in paths}:
        fsync_dir(parent)
    log_records=[dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p,LOG_MAX)) for p in paths]
    wall = time.monotonic() - started
    own = resource.getrusage(resource.RUSAGE_SELF)
    child_cpu = usage.ru_utime + usage.ru_stime
    own_cpu = own.ru_utime + own.ru_stime
    failures = []
    if timed_out or wall > limits['wall_seconds']:
        failures.append('wall_timeout_or_overshoot')
    if capture.overflow:
        failures.append('log_overflow')
    if collector_error is not None:
        failures.append('collector_error:' + collector_error)
    exit_code = os.waitstatus_to_exitcode(wait_status)
    if exit_code != 0:
        failures.append('child_exit_' + str(exit_code))
    if not numeric(child_cpu) or child_cpu > limits['worker_cpu_hard']:
        failures.append('worker_cpu_invalid_or_overshoot')
    if not numeric(own_cpu) or own_cpu > limits['supervisor_cpu_hard']:
        failures.append('supervisor_cpu_invalid_or_overshoot')
    return dict(schema=VERSION, command=command, cwd=str(cwd), limits=dict(limits),
        supervisor_pid=supervisor_pid, child_pid=child, child_reaped=True,
        parent_death_guard=True, exit_code=exit_code, wall_timeout=timed_out,
        log_overflow=capture.overflow, collector_error=collector_error,
        wall_seconds=wall, child_user_cpu_seconds=usage.ru_utime,
        child_system_cpu_seconds=usage.ru_stime, child_cpu_seconds=child_cpu,
        supervisor_exclusive_cpu_sample=own_cpu,
        supervisor_cpu_allocation_charged=limits['supervisor_cpu_hard'],
        supervisor_final_write_tail_measured=False,
        child_peak_rss_kib=usage.ru_maxrss, supervisor_peak_rss_kib=own.ru_maxrss,
        log_bytes_reserved=capture.written, log_bytes_read=capture.read_bytes,
        logs=log_records,
        failures=failures)

