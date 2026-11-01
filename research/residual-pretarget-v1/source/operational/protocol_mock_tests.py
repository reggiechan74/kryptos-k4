"""Two finite operational-only invocations; no scientific call or real case read.

SOURCE ONLY until separately approved. The fixtures below are literal interface
stubs, not target data, a decoder benchmark or fresh synthetic validation. This
module is inert at import and --help; it never grants authority or launches a
process. Counts are frozen before either invocation; failures forbid retries.
"""
import argparse
import builtins
import contextlib
import copy
import ctypes
import hashlib
import importlib.machinery
import importlib.util
import io
import json
import math
import os
from pathlib import Path
import resource
import selectors
import signal
import subprocess
import sys
import time
import types

ROOT = Path('/workspace/shared/k4-canonical-residual-target-v1')
MIB = 1024 * 1024
REPORT_SCHEMA = 'k4-residual-operational-mock-report-v1'
EXPECTED_COUNTS = {
    'inert_boundaries': 15,
    'raw_schema': 14,
    'mapping': 7,
    'status_relation': 16,
    'freeze_authority': 24,
    'command_mode': 10,
    'digest': 6,
    'collector_reaper': 12,
    'state_execution': 18,
    'file_boundaries': 8,
    'mode_pair': 8,
    'worker_fail_closed': 4,
    'supervisor_reports': 13,
    'byte_loader': 4,
}
EXPECTED_CASES = {
    'inert_boundaries': (
        'import:common.py', 'import:bounded_stage.py', 'import:worker.py',
        'import:supervisor.py', 'import:protocol_mock_tests.py',
        'import:seal_results.py', 'import:input_check.py',
        'help:worker.py', 'unsupported-status:worker.py',
        'help:supervisor.py', 'unsupported-status:supervisor.py',
        'help:protocol_mock_tests.py', 'unsupported-status:protocol_mock_tests.py',
        'help:seal_results.py', 'unsupported-status:seal_results.py'),
    'raw_schema': (
        'valid-literal', 'raw-mutation-0', 'raw-mutation-1', 'raw-mutation-2',
        'raw-mutation-3', 'raw-mutation-4', 'raw-mutation-5', 'raw-mutation-6',
        'raw-mutation-7', 'raw-mutation-8', 'raw-mutation-9', 'raw-extra-field',
        'raw-duplicate-key', 'control-cannot-claim-target'),
    'mapping': (
        'independent-converters-agree', 'hand-newest-first', 'hand-final-context',
        'hand-clue-offsets-sign', 'reversed-lags', 'off-by-one-row', 'wrong-sign'),
    'status_relation': (
        'matching-EXACT', 'matching-EMPTY', 'rejected-pair-EXACT-VERIFIED_EMPTY',
        'rejected-pair-EMPTY-VERIFIED_EXACT', 'rejected-pair-INCOMPLETE-VERIFIED_EXACT',
        'rejected-pair-EMPTY-FORMAT_ONLY', 'singleton-common-law',
        'aliases-not-function-uniqueness', 'multiple-joints', 'no-common-witness',
        'singleton-joint-inconsistency', 'empty-zero-relation',
        'empty-not-vacuous-singleton', 'empty-partial-masks-rejected',
        'no-first-six-claim', 'no-score-ranking-field'),
    'freeze_authority': (
        'valid-freeze-metadata', 'no-input-in-source-positive-path',
        'no-input-in-source-positive-expected_path', 'no-input-in-source-empty-path',
        'no-input-in-source-empty-expected_path', 'no-input-in-source-K4-path',
        'role-inner-id-binding', 'fixed-target-pin', 'valid-mock-approval',
        'approval-old-freeze', 'approval-wrong-stage', 'approval-extra-job',
        'approval-case-capability', 'approval-missing-review',
        'mock-no-raw-capability-CTRL-positive-normal', 'mock-no-raw-capability-K4-normal',
        'missing-approval', 'valid-external-completion', 'external-uncertain-rejected',
        'source-auth-traps-all-real-cases', 'source-byte-pin-mismatch', 'control-grant-cannot-read-K4',
        'target-grant-cannot-read-control', 'control-path-never-opens-target'),
    'command_mode': (
        'fixed-expanded-command', 'partial-token', 'duplicate-freeze',
        'unknown-token', 'missing-approval', 'extra-argv', 'wrong-output', 'wrong-mode',
        'double-optimized-rejected', 'unexpected-interpreter-flag-rejected'),
    'digest': (
        'root-time-only-exclusion', 'piece-time-only-exclusion',
        'logical-counter-retained', 'relation-bytes-retained',
        'stream-cap-predebit', 'incomplete-digest-disallowed'),
    'collector_reaper': (
        'integer-not-bool', 'finite-not-nan', 'finite-not-infinity',
        'exact-log-cap', 'log-overflow-no-debit', 'log-bool-rejected',
        'collector-exact-boundary', 'collector-overflow-stops-write',
        'collector-after-overflow-discard', 'collector-chunk-bound',
        'reap-disarm-release-order', 'reap-retries-only-interrupted-wait'),
    'state_execution': (
        'clean-initial-state', 'first-only-job', 'out-of-order-no-launch',
        'retained-reserve-blocks-successor', 'stopped-blocks-successor',
        'old-state-freeze', 'complete-execution-receipt',
        'execution-unreaped', 'execution-unguarded', 'execution-wall-overshoot',
        'execution-cpu-overshoot', 'execution-log-overflow', 'execution-child-failed',
        'execution-collector-error', 'execution-bool-receipt-count',
        'execution-arbitrary-command', 'missing-output-retained-reserve-stops',
        'prelaunch-failure-retains-full-reserve'),
    'file_boundaries': (
        'bounded-json-correct-pin', 'reader-duplicate-key', 'reader-nan',
        'reader-infinity', 'reader-symlink', 'reader-input-pin-mismatch',
        'reader-growth-overflow', 'exclusive-marker-no-retry'),
    'mode_pair': (
        'same-pair', 'only-frozen-times-excluded', 'reject-pair-producer-counter',
        'reject-pair-preflight-counter', 'reject-pair-reference-counter',
        'reject-pair-full-relation-digest', 'reject-pair-joint-count', 'reject-pair-source-role'),
    'worker_fail_closed': (
        'worker-path-missing-approval', 'worker-path-reference-mismatch',
        'worker-path-postseal-mismatch', 'worker-path-control-gate'),
    'supervisor_reports': (
        'report-complete-EXACT', 'report-complete-EMPTY', 'report-resource-gate-no-result',
        'report-incomplete-no-result', 'reject-report-EXACT-crossed-verifier',
        'reject-report-EMPTY-crossed-verifier', 'reject-report-EMPTY-partial-inventory',
        'reject-report-W-zero-alone', 'reject-report-incomplete-partial-claim',
        'reject-report-gate-partial-claim', 'reject-report-bool-cap-counter',
        'reject-report-extra-resource-field', 'reject-report-over-cap-wall'),
    'byte_loader': (
        'authenticated-literal-module-identity', 'wrong-hash-before-compile',
        'source-cap-before-compile', 'loader-exec-module-never-used'),
}
FORBIDDEN_COUNTER_KEYS = ('science_imports', 'science_calls', 'case_reads',
                          'child_launches', 'entropy_calls')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def _unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate bootstrap key')
        result[key] = value
    return result


def _bytes(path, limit):
    path = Path(path)
    require(path.is_file() and not path.is_symlink() and path.stat().st_size <= limit,
            'bounded regular operational source')
    with path.open('rb') as handle:
        data = handle.read(limit + 1)
    require(len(data) <= limit, 'operational source grew beyond cap')
    return data


def bootstrap(pin):
    require(type(pin) is str and len(pin) == 64 and
            all(c in '0123456789abcdef' for c in pin), 'freeze commitment')
    raw = _bytes(ROOT / 'FREEZE.json', 2 * MIB)
    require(hashlib.sha256(raw).hexdigest() == pin, 'freeze bytes changed')
    preliminary = json.loads(raw, object_pairs_hook=_unique,
        parse_constant=lambda _x: (_ for _ in ()).throw(ValueError('nonfinite JSON')))
    source = ROOT / 'common.py'
    content = _bytes(source, MIB)
    require(hashlib.sha256(content).hexdigest() == preliminary['files'][str(source)],
            'operational bootstrap pin')
    common = memory_module('k4_target_mock_common', source, content)
    return common, common.freeze_context(pin)


def memory_module(name, path, source):
    """Execute only caller-authenticated operational source, never a pyc cache."""
    spec = importlib.machinery.ModuleSpec(name, loader=None, origin=str(path))
    spec.has_location = True
    module = importlib.util.module_from_spec(spec)
    module.__file__ = str(path)
    sys.modules[name] = module
    exec(compile(source, str(path), 'exec', dont_inherit=True, optimize=sys.flags.optimize), module.__dict__)
    return module


@contextlib.contextmanager
def patched(obj, name, value):
    previous = getattr(obj, name)
    setattr(obj, name, value)
    try:
        yield
    finally:
        setattr(obj, name, previous)


class Suite:
    def __init__(self):
        require(set(EXPECTED_CASES) == set(EXPECTED_COUNTS) and all(
            len(names) == EXPECTED_COUNTS[group] and len(set(names)) == len(names)
            for group, names in EXPECTED_CASES.items()), 'literal manifest/count agreement')
        self.counts = {key: 0 for key in EXPECTED_COUNTS}
        self.names = {key: set() for key in EXPECTED_COUNTS}

    def case(self, group, name, function, rejects=False):
        require(group in self.counts and name in EXPECTED_CASES[group] and name not in self.names[group],
                'finite unique declared mock assertion')
        self.names[group].add(name)
        if rejects:
            try:
                function()
            except (ValueError, FileNotFoundError, FileExistsError):
                pass
            else:
                raise ValueError('mock failed to reject: ' + name)
        else:
            require(function() is True, 'mock assertion failed: ' + name)
        self.counts[group] += 1


def changed(value, path, replacement):
    result = copy.deepcopy(value)
    cursor = result
    for item in path[:-1]:
        cursor = cursor[item]
    cursor[path[-1]] = replacement
    return result


def call_true(function, *args):
    function(*args)
    return True


@contextlib.contextmanager
def source_only_guard(counts):
    """Install before the first operational module executes in a mock process.

    Only byte reads of frozen-source candidates, interpreter and the mock grant
    can pass. The later authenticated source graph further narrows these paths.
    Real inputs/expected arrays, pyc caches, entropy and processes are blocked.
    """
    science_paths = {
        '/workspace/shared/canonical-residual-dev/residual_decoder.py',
        '/workspace/shared/canonical-residual-dev/affine_filter.py',
        '/workspace/shared/canonical-residual-reference-v3/reference_v3.py',
        '/workspace/shared/residual-fixed-data-reevaluation-v1/preflight_blind.py',
        '/workspace/shared/residual-fixed-data-reevaluation-v1/checker_blind.py',
        '/workspace/shared/residual-fixed-data-reevaluation-v1/CAPS.json'}
    case_paths = {'/workspace/shared/k4-full31-publisher/data/k4.json'} | {
        str(ROOT / 'fixtures' / (name + '.json')) for name in
        ('positive', 'positive-expected', 'empty', 'empty-expected')}
    interpreter = str(Path(sys.executable).resolve())
    original_io = io.open
    original_builtin = builtins.open
    original_import = builtins.__import__
    def checked_open(original, path, mode='r', *args, **kwargs):
        require(isinstance(path, (str, bytes, os.PathLike)), 'source-only pathname')
        text = os.fsdecode(path)
        if text in case_paths:
            counts['case_reads'] += 1
            raise ValueError('setup attempted real case input')
        candidate = Path(text)
        allowed = (text in science_paths or text == interpreter or
                   text == str(ROOT / 'approvals' / 'mocks.json') or
                   candidate.parent == ROOT and candidate.suffix in ('.py', '.json', '.md')
                   and candidate.name != 'PUBLICATION-CHECKPOINT.json')
        require(allowed and mode in ('r', 'rb'), 'mock setup permits authenticated source metadata reads only')
        return original(path, mode, *args, **kwargs)
    def no_process(*_a, **_k):
        counts['child_launches'] += 1
        raise ValueError('mock setup forbids process launch')
    def no_entropy(*_a, **_k):
        counts['entropy_calls'] += 1
        raise ValueError('mock setup forbids entropy')
    def no_dynamic_module(*_a, **_k):
        counts['science_imports'] += 1
        raise ValueError('only authenticated operational in-memory modules are allowed')
    def no_effect(*_a, **_k):
        raise ValueError('mock setup forbids direct filesystem or resource mutation')
    def guarded_import(name, *args, **kwargs):
        if name.split('.')[0] in ('residual_decoder', 'affine_filter', 'reference_v3',
                                 'preflight_blind', 'checker_blind'):
            counts['science_imports'] += 1
            raise ValueError('mock setup forbids scientific import')
        return original_import(name, *args, **kwargs)
    absent = object()
    prior = {}
    for name in ('random', 'secrets'):
        prior[name] = sys.modules.get(name, absent)
        stub = types.ModuleType(name)
        stub.__getattr__ = no_entropy
        sys.modules[name] = stub
    try:
        with contextlib.ExitStack() as stack:
            replacements = [(io, 'open', lambda path, mode='r', *a, **k: checked_open(original_io, path, mode, *a, **k)),
                (builtins, 'open', lambda path, mode='r', *a, **k: checked_open(original_builtin, path, mode, *a, **k)),
                (os, 'fork', no_process), (os, 'execve', no_process),
                (subprocess, 'Popen', no_process), (os, 'urandom', no_entropy),
                (os, 'open', no_effect), (os, 'mkdir', no_effect), (os, 'unlink', no_effect),
                (os, 'remove', no_effect), (os, 'replace', no_effect), (os, 'write', no_effect),
                (importlib.util, 'spec_from_file_location', no_dynamic_module),
                (builtins, '__import__', guarded_import)]
            if hasattr(os, 'getrandom'):
                replacements.append((os, 'getrandom', no_entropy))
            for obj, name, replacement in replacements:
                stack.enter_context(patched(obj, name, replacement))
            yield
    finally:
        for name, value in prior.items():
            if value is absent:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = value


@contextlib.contextmanager
def forbidden_io(common, worker, forbidden, counts):
    """No actual filesystem data I/O, scientific loader, child or entropy in tests.

    The case-path set contains all three raw files and both expected arrays.
    Source authentication is tested with its metadata reader/hash replaced by
    a finite fixture. Any accidental source-graph traversal into a case path
    fails before a real open; no deliberately successful probe is made.
    """
    def denied_file(path, *_args, **_kwargs):
        if isinstance(path, (str, bytes, os.PathLike)) and os.fsdecode(path) in forbidden:
            counts['case_reads'] += 1
        raise ValueError('mock forbids data-file I/O')

    def denied_process(*_args, **_kwargs):
        counts['child_launches'] += 1
        raise ValueError('mock forbids process launch')

    def denied_entropy(*_args, **_kwargs):
        counts['entropy_calls'] += 1
        raise ValueError('mock forbids entropy')

    def denied_science(*_args, **_kwargs):
        counts['science_calls'] += 1
        raise ValueError('mock forbids dynamic scientific/operational loading in body')

    def denied_effect(*_args, **_kwargs):
        raise ValueError('mock forbids filesystem/resource/signal mutation')

    original_import = builtins.__import__
    scientific = {'residual_decoder', 'affine_filter', 'reference_v3',
                  'preflight_blind', 'checker_blind'}

    def guarded_import(name, *args, **kwargs):
        if name.split('.')[0] in scientific or 'k4_target_decoder' in name or 'k4_target_reference' in name:
            counts['science_imports'] += 1
            raise ValueError('mock forbids scientific import')
        return original_import(name, *args, **kwargs)

    with contextlib.ExitStack() as stack:
        for obj, name, replacement in (
                (builtins, 'open', denied_file), (io, 'open', denied_file),
                (os, 'open', denied_file), (os, 'fork', denied_process),
                (os, 'execve', denied_process), (subprocess, 'Popen', denied_process),
                (os, 'mkdir', denied_effect), (os, 'unlink', denied_effect),
                (os, 'remove', denied_effect), (os, 'replace', denied_effect),
                (os, 'write', denied_effect), (resource, 'setrlimit', denied_effect),
                (signal, 'setitimer', denied_effect), (ctypes, 'CDLL', denied_effect),
                (os, 'urandom', denied_entropy),
                (common, 'load_pinned', denied_science), (worker, 'load', denied_science),
                (builtins, '__import__', guarded_import)):
            stack.enter_context(patched(obj, name, replacement))
        yield


def raw_literal():
    # This is not any disclosed pilot or K4 input. Hand-check: first preceding
    # six letters ABCDEF -> [5,4,3,2,1,0]; current letters after the prefix are
    # A, plaintext B, hence signed C-P=25 at each frozen observation row.
    return {'ciphertext': 'ABCDEF' + 'A' * 91, 'length': 97,
            'indexing': 'one-based inclusive',
            'cribs': [{'start': 22, 'end': 34, 'plaintext': 'B' * 13},
                      {'start': 64, 'end': 74, 'plaintext': 'B' * 11}]}


def relation_literal(empty=False):
    result = {'status': 'EMPTY' if empty else 'EXACT',
        'resources': {'wall_seconds': 1.0, 'steps': 3},
        'pieces': [] if empty else [{'core': {'resources': {'wall_seconds': 0.5, 'work': 2}}}],
        'masks': [[] if empty else [2] for _ in range(91)],
        'witnesses': [{} for _ in range(91)], 'provenance': [{} for _ in range(91)],
        'feasibility_witness': None if empty else {'piece': 'literal-stub', 'theta': [[28, 1], [29, 1]]}}
    verified = {'status': 'VERIFIED_EMPTY' if empty else 'VERIFIED_EXACT',
        'pieces_checked': 0 if empty else 1, 'canonical_functions': 0 if empty else 1,
        'original_lifts': 0 if empty else 1, 'joint_predictions': 0 if empty else 1}
    raw = {'ciphertext': 'A' * 97, 'length': 97, 'indexing': 'one-based inclusive',
        'cribs': [{'start': 22, 'end': 34, 'plaintext': 'Y' * 13},
                  {'start': 64, 'end': 74, 'plaintext': 'Y' * 11}]}
    return raw, result, verified


def inert_cases(suite, sources, modules):
    def imported(name):
        namespace = {'__name__': 'k4_inert_probe_' + name, '__file__': str(ROOT / name)}
        exec(compile(sources[name], str(ROOT / name), 'exec', dont_inherit=True, optimize=sys.flags.optimize), namespace)
        return True

    for name in ('common.py', 'bounded_stage.py', 'worker.py', 'supervisor.py',
                 'protocol_mock_tests.py', 'seal_results.py', 'input_check.py'):
        suite.case('inert_boundaries', 'import:' + name, lambda name=name: imported(name))

    def parse_only(module, option, expected):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            try:
                module.main([option])
            except SystemExit as error:
                return type(error.code) is int and error.code == expected
        return False

    for name in ('worker.py', 'supervisor.py', 'protocol_mock_tests.py', 'seal_results.py'):
        suite.case('inert_boundaries', 'help:' + name,
                   lambda name=name: parse_only(modules[name], '--help', 0))
        suite.case('inert_boundaries', 'unsupported-status:' + name,
                   lambda name=name: parse_only(modules[name], '--status', 2))


def raw_and_mapping_cases(suite, common, worker, independent):
    raw = raw_literal()
    suite.case('raw_schema', 'valid-literal', lambda: call_true(common.validate_raw, raw, 'positive'))
    mutations = [
        (('length',), True), (('length',), 96), (('indexing',), 'zero-based'),
        (('ciphertext',), 'A' * 96), (('ciphertext',), 'A' * 96 + 'a'),
        (('cribs', 0, 'start'), 21), (('cribs', 0, 'end'), 33),
        (('cribs', 1, 'plaintext'), 'A' * 10), (('cribs', 0, 'start'), True),
        (('cribs', 0, 'plaintext'), 'A' * 12 + '?')]
    for index, (path, value) in enumerate(mutations):
        suite.case('raw_schema', 'raw-mutation-' + str(index),
            lambda path=path, value=value: common.validate_raw(changed(raw, path, value), 'positive'), True)
    extra = copy.deepcopy(raw); extra['score'] = 1
    suite.case('raw_schema', 'raw-extra-field', lambda: common.validate_raw(extra, 'positive'), True)
    suite.case('raw_schema', 'raw-duplicate-key', lambda: common.unique_object([('a', 1), ('a', 2)]), True)
    suite.case('raw_schema', 'control-cannot-claim-target', lambda: common.validate_raw(raw, 'K4'), True)

    primary = worker.convert_raw(raw, 'v000')
    secondary = independent.convert_raw_independent(raw, 'v000')
    expected_rows = list(range(15, 28)) + list(range(57, 68))
    suite.case('mapping', 'independent-converters-agree', lambda: primary == secondary)
    suite.case('mapping', 'hand-newest-first', lambda: primary['contexts'][0] == [5, 4, 3, 2, 1, 0])
    suite.case('mapping', 'hand-final-context', lambda: primary['contexts'][90] == [0, 0, 0, 0, 0, 0])
    suite.case('mapping', 'hand-clue-offsets-sign', lambda: primary['observed'] == [[r, 25] for r in expected_rows])
    for label, mutant in (
            ('reversed-lags', changed(primary, ('contexts', 0), [0, 1, 2, 3, 4, 5])),
            ('off-by-one-row', changed(primary, ('observed', 0, 0), 16)),
            ('wrong-sign', changed(primary, ('observed', 0, 1), 1))):
        suite.case('mapping', label, lambda mutant=mutant: require(mutant == secondary, 'mapping mismatch'), True)


def relation_cases(suite, worker, independent):
    for producer, verifier in (('EXACT', 'VERIFIED_EXACT'), ('EMPTY', 'VERIFIED_EMPTY')):
        suite.case('status_relation', 'matching-' + producer,
                   lambda producer=producer, verifier=verifier: worker.require_status_pair(producer, verifier))
    for producer, verifier in (('EXACT', 'VERIFIED_EMPTY'), ('EMPTY', 'VERIFIED_EXACT'),
                              ('INCOMPLETE', 'VERIFIED_EXACT'), ('EMPTY', 'FORMAT_ONLY')):
        suite.case('status_relation', 'rejected-pair-' + producer + '-' + verifier,
                   lambda producer=producer, verifier=verifier: worker.require_status_pair(producer, verifier), True)
    raw, result, verified = relation_literal()
    instance = worker.convert_raw(raw, 'v000')
    interpretation = independent.interpret_verified(raw, instance, result, verified)
    suite.case('status_relation', 'singleton-common-law', lambda:
        interpretation == {'classification': 'CONDITIONAL_SINGLETON_TAIL',
            'plaintext_masks': [['Y'] for _ in range(91)], 'example_plaintext_tail': 'Y' * 91,
            'first_six_claimed': False})
    alias = dict(verified, canonical_functions=2, original_lifts=2)
    suite.case('status_relation', 'aliases-not-function-uniqueness', lambda:
        independent.interpret_verified(raw, instance, result, alias)['classification'] == 'CONDITIONAL_SINGLETON_TAIL')
    ambiguous = dict(result, masks=[[2, 3] for _ in range(91)])
    suite.case('status_relation', 'multiple-joints', lambda:
        independent.interpret_verified(raw, instance, ambiguous, dict(verified, joint_predictions=2))['classification'] == 'NONEMPTY_AMBIGUOUS')
    suite.case('status_relation', 'no-common-witness', lambda:
        independent.interpret_verified(raw, instance, dict(result, feasibility_witness=None), verified), True)
    suite.case('status_relation', 'singleton-joint-inconsistency', lambda:
        independent.interpret_verified(raw, instance, ambiguous, verified), True)
    emptyraw, empty, emptyverified = relation_literal(True)
    emptyinstance = worker.convert_raw(emptyraw, 'v000')
    emptyinterpretation = independent.interpret_verified(emptyraw, emptyinstance, empty, emptyverified)
    suite.case('status_relation', 'empty-zero-relation', lambda:
        worker.semantic_summary(empty, emptyverified, emptyinterpretation)['interpretation']['example_plaintext_tail'] is None)
    suite.case('status_relation', 'empty-not-vacuous-singleton', lambda:
        worker.empty_invariants(empty, dict(emptyverified, joint_predictions=1)), True)
    suite.case('status_relation', 'empty-partial-masks-rejected', lambda:
        worker.empty_invariants(dict(empty, masks=[]), emptyverified), True)
    suite.case('status_relation', 'no-first-six-claim', lambda:
        worker.semantic_summary(result, verified, dict(interpretation, first_six_claimed=True)), True)
    suite.case('status_relation', 'no-score-ranking-field', lambda:
        worker.semantic_summary(result, verified, dict(interpretation, score=1)), True)


def authority_cases(suite, common, freeze, freeze_pin, approval):
    suite.case('freeze_authority', 'valid-freeze-metadata', lambda: call_true(common.verify_freeze_object, freeze))
    for role, field in (('positive', 'path'), ('positive', 'expected_path'), ('empty', 'path'),
                        ('empty', 'expected_path'), ('K4', 'path')):
        mutant = copy.deepcopy(freeze)
        mutant['files'][freeze['inputs'][role][field]] = '0' * 64
        suite.case('freeze_authority', 'no-input-in-source-' + role + '-' + field,
                   lambda mutant=mutant: common.verify_freeze_object(mutant), True)
    suite.case('freeze_authority', 'role-inner-id-binding', lambda:
        common.verify_freeze_object(changed(freeze, ('inputs', 'positive', 'internal_id'), 'v002')), True)
    suite.case('freeze_authority', 'fixed-target-pin', lambda:
        common.verify_freeze_object(changed(freeze, ('inputs', 'K4', 'sha256'), '0' * 64)), True)
    suite.case('freeze_authority', 'valid-mock-approval', lambda:
        call_true(common.validate_approval_object, approval, freeze, freeze_pin, 'mocks'))
    for label, path, value in (
            ('old-freeze', ('freeze_sha256',), '0' * 64),
            ('wrong-stage', ('stage',), 'target'),
            ('extra-job', ('jobs',), ['mock-normal', 'mock-optimized', 'K4-normal']),
            ('case-capability', ('input_sha256',), {'K4': freeze['inputs']['K4']['sha256']}),
            ('missing-review', ('source_review_sha256',), None)):
        suite.case('freeze_authority', 'approval-' + label, lambda path=path, value=value:
            common.validate_approval_object(changed(approval, path, value), freeze, freeze_pin, 'mocks'), True)
    for job in ('CTRL-positive-normal', 'K4-normal'):
        suite.case('freeze_authority', 'mock-no-raw-capability-' + job,
                   lambda job=job: common.read_authorized_raw(freeze, approval, job), True)
    def missing():
        with patched(common, 'read_json', lambda *_a, **_k: (_ for _ in ()).throw(FileNotFoundError('absent grant'))):
            common.read_authority('mocks', freeze, freeze_pin, '1' * 64)
    suite.case('freeze_authority', 'missing-approval', missing, True)
    external = {'schema': 'k4-residual-external-completion-v1', 'job': 'mock-normal',
        'freeze_sha256': freeze_pin, 'receipt_sha256': '2' * 64, 'exit_code': 0,
        'completed': True, 'tool_evidence': 'explicit external completion stub'}
    suite.case('freeze_authority', 'valid-external-completion', lambda:
        common.validate_external_object(external, 'mock-normal', freeze_pin, '2' * 64))
    suite.case('freeze_authority', 'external-uncertain-rejected', lambda:
        common.validate_external_object(dict(external, completed=False), 'mock-normal', freeze_pin, '2' * 64), True)
    def source_without_case_reads(corrupt=False):
        def metadata_read(path, _limit=None, _pin=None):
            require(str(path) == str(ROOT / 'FREEZE.json'), 'only freeze metadata reader')
            return freeze
        def metadata_hash(path, _limit=None):
            value = str(path)
            require(value not in {v['path'] for v in freeze['inputs'].values()} and
                    value not in {v['expected_path'] for v in freeze['inputs'].values()},
                    'source verification attempted actual case path')
            if value == freeze['python']['executable']:
                return freeze['python']['sha256']
            require(value in freeze['files'], 'only frozen metadata source')
            if corrupt and value == str(ROOT / 'common.py'):
                return '0' * 64
            return freeze['files'][value]
        with patched(common, 'read_json', metadata_read), patched(common, 'sha', metadata_hash):
            return common.freeze_context(freeze_pin) == freeze
    suite.case('freeze_authority', 'source-auth-traps-all-real-cases', source_without_case_reads)
    suite.case('freeze_authority', 'source-byte-pin-mismatch', lambda: source_without_case_reads(True), True)
    control_grant = {'stage': 'controls', 'jobs': list(common.STAGE_JOBS['controls']),
        'input_sha256': {role: freeze['inputs'][role]['sha256'] for role in ('positive', 'empty')}}
    target_grant = {'stage': 'target', 'jobs': list(common.STAGE_JOBS['target']),
        'input_sha256': {'K4': freeze['inputs']['K4']['sha256']}}
    suite.case('freeze_authority', 'control-grant-cannot-read-K4', lambda:
        common.read_authorized_raw(freeze, control_grant, 'K4-normal'), True)
    suite.case('freeze_authority', 'target-grant-cannot-read-control', lambda:
        common.read_authorized_raw(freeze, target_grant, 'CTRL-positive-normal'), True)
    def control_path_only():
        paths = []
        def raw_reader(path, _limit, pin):
            paths.append(str(path))
            require(str(path) == freeze['inputs']['positive']['path'] and
                    str(path) != freeze['inputs']['K4']['path'] and
                    pin == freeze['inputs']['positive']['sha256'], 'control-only raw path/hash')
            return raw_literal()
        with patched(common, 'read_json', raw_reader):
            value = common.read_authorized_raw(freeze, control_grant, 'CTRL-positive-normal')
        return value == raw_literal() and paths == [freeze['inputs']['positive']['path']]
    suite.case('freeze_authority', 'control-path-never-opens-target', control_path_only)


def command_cases(suite, common, freeze, freeze_pin, approval_pin, job):
    spec = freeze['jobs'][job]
    expanded = common.expand(spec['command'], freeze_pin, approval_pin)
    suite.case('command_mode', 'fixed-expanded-command', lambda:
        expanded.count(freeze_pin) == 1 and expanded.count(approval_pin) == 1 and
        expanded[-1] == spec['output'] and expanded.count('-O') == int(spec['optimized']))
    for label, command in (
            ('partial-token', ['x${FREEZE_PIN}', '${APPROVAL_PIN}']),
            ('duplicate-freeze', ['${FREEZE_PIN}', '${FREEZE_PIN}', '${APPROVAL_PIN}']),
            ('unknown-token', ['${FREEZE_PIN}', '${APPROVAL_PIN}', '${INPUT}']),
            ('missing-approval', ['${FREEZE_PIN}'])):
        suite.case('command_mode', label, lambda command=command:
                   common.expand(command, freeze_pin, approval_pin), True)
    for label, args in (('extra-argv', expanded[expanded.index(spec['script']) + 1:] + ['--retry']),
                        ('wrong-output', expanded[expanded.index(spec['script']) + 1:-1] + ['/tmp/result.json'])):
        suite.case('command_mode', label, lambda args=args:
            common.validate_child_command(freeze, job, freeze_pin, approval_pin, args), True)
    opposite = 'mock-normal' if job == 'mock-optimized' else 'mock-optimized'
    other = common.expand(freeze['jobs'][opposite]['command'], freeze_pin, approval_pin)
    suite.case('command_mode', 'wrong-mode', lambda:
        common.validate_child_command(freeze, opposite, freeze_pin, approval_pin,
            other[other.index(freeze['jobs'][opposite]['script']) + 1:]), True)
    def double_optimized():
        selected = freeze['jobs']['mock-optimized']
        command = common.expand(selected['command'], freeze_pin, approval_pin)
        args = command[command.index(selected['script']) + 1:]
        with patched(sys, 'flags', types.SimpleNamespace(isolated=1, optimize=2)):
            common.validate_child_command(freeze, 'mock-optimized', freeze_pin, approval_pin, args)
    suite.case('command_mode', 'double-optimized-rejected', double_optimized, True)
    def unexpected_interpreter_flag():
        index = expanded.index(spec['script'])
        mutant = expanded[:index] + ['-S'] + expanded[index:]
        with patched(sys, 'orig_argv', mutant):
            common.validate_child_command(freeze, job, freeze_pin, approval_pin, expanded[index + 1:])
    suite.case('command_mode', 'unexpected-interpreter-flag-rejected', unexpected_interpreter_flag, True)


def digest_cases(suite, worker):
    _raw, result, _verified = relation_literal()
    digest = worker.producer_digest(result)
    suite.case('digest', 'root-time-only-exclusion', lambda:
        worker.producer_digest(changed(result, ('resources', 'wall_seconds'), 9.0)) == digest)
    suite.case('digest', 'piece-time-only-exclusion', lambda:
        worker.producer_digest(changed(result, ('pieces', 0, 'core', 'resources', 'wall_seconds'), 9.0)) == digest)
    suite.case('digest', 'logical-counter-retained', lambda:
        worker.producer_digest(changed(result, ('resources', 'steps'), 4)) != digest)
    suite.case('digest', 'relation-bytes-retained', lambda:
        worker.producer_digest(changed(result, ('masks', 0), [3])) != digest)
    def overflow():
        with patched(worker, 'HASH_MAX', 4):
            worker.producer_digest(result)
    suite.case('digest', 'stream-cap-predebit', overflow, True)
    suite.case('digest', 'incomplete-digest-disallowed', lambda:
        worker.producer_digest(dict(result, status='INCOMPLETE')), True)


def collector_cases(suite, bounded, common):
    suite.case('collector_reaper', 'integer-not-bool', lambda: not common.integer(True))
    suite.case('collector_reaper', 'finite-not-nan', lambda: not common.numeric(float('nan')))
    suite.case('collector_reaper', 'finite-not-infinity', lambda: not common.numeric(float('inf')))
    suite.case('collector_reaper', 'exact-log-cap', lambda: bounded.reserve_log_bytes(3, 1, 4) == 4)
    suite.case('collector_reaper', 'log-overflow-no-debit', lambda: bounded.reserve_log_bytes(3, 2, 4) is None)
    suite.case('collector_reaper', 'log-bool-rejected', lambda: bounded.reserve_log_bytes(True, 1, 4), True)
    writes = []; kills = []
    capture = bounded.BoundedCapture(lambda stream, data: (writes.append((stream, data)), len(data))[1],
                                    lambda: kills.append('kill'), 4)
    suite.case('collector_reaper', 'collector-exact-boundary', lambda:
        capture.feed(0, b'abcd') is True and capture.written == [4, 0] and writes == [(0, b'abcd')])
    suite.case('collector_reaper', 'collector-overflow-stops-write', lambda:
        capture.feed(0, b'x') is False and capture.overflow is True and
        capture.written == [4, 0] and len(writes) == 1 and kills == ['kill'])
    suite.case('collector_reaper', 'collector-after-overflow-discard', lambda:
        capture.feed(1, b'z') is False and capture.written == [4, 0] and len(writes) == 1)
    suite.case('collector_reaper', 'collector-chunk-bound', lambda: capture.feed(0, b'x' * 16385), True)
    events = []
    suite.case('collector_reaper', 'reap-disarm-release-order', lambda:
        bounded.reap_after_disarm(lambda: events.append('ready'), lambda: events.append('disarm'),
            lambda: events.append('release'), lambda: (events.append('wait4'), 'usage')[1]) == 'usage' and
        events == ['ready', 'disarm', 'release', 'wait4'])
    retried = []
    def ready():
        retried.append('ready')
        if len(retried) == 1:
            raise InterruptedError()
    suite.case('collector_reaper', 'reap-retries-only-interrupted-wait', lambda:
        bounded.reap_after_disarm(ready, lambda: retried.append('disarm'),
            lambda: retried.append('release'), lambda: (retried.append('wait4'), True)[1]) is True and
        retried == ['ready', 'ready', 'disarm', 'release', 'wait4'])


def state_cases(suite, supervisor, common, freeze, freeze_pin, approval_pin):
    # Pure metadata guards only: no actual marker, process or receipt is created.
    state = {'schema': 'k4-residual-target-supervisor-v1', 'freeze_sha256': freeze_pin,
        'completed': [], 'in_flight': None, 'stopped': False, 'canceled': [],
        'worker_cpu_actual': 0, 'allocation_charged': 0,
        'certificate_bytes': 0, 'certificate_files': 0, 'artifact_bytes': 0}
    suite.case('state_execution', 'clean-initial-state', lambda:
        call_true(supervisor.validate_state_shape, state, freeze_pin))
    suite.case('state_execution', 'first-only-job', lambda:
        call_true(supervisor.require_next_job, state, 'mock-normal'))
    suite.case('state_execution', 'out-of-order-no-launch', lambda:
        supervisor.require_next_job(state, 'K4-normal'), True)
    suite.case('state_execution', 'retained-reserve-blocks-successor', lambda:
        supervisor.validate_state_shape(dict(state, in_flight={'job': 'mock-normal'}), freeze_pin), True)
    suite.case('state_execution', 'stopped-blocks-successor', lambda:
        supervisor.require_next_job(dict(state, stopped=True), 'mock-normal'), True)
    suite.case('state_execution', 'old-state-freeze', lambda:
        supervisor.validate_state_shape(dict(state, freeze_sha256='0' * 64), freeze_pin), True)
    limits = common.stage_limits('mocks')
    spec = freeze['jobs']['mock-normal']
    command = common.expand(spec['command'], freeze_pin, approval_pin)
    execution = {'schema': 'k4-residual-bounded-stage-v1', 'command': command,
        'cwd': str(ROOT), 'limits': limits, 'supervisor_pid': 101, 'child_pid': 102,
        'child_reaped': True, 'parent_death_guard': True, 'exit_code': 0,
        'wall_timeout': False, 'log_overflow': False, 'collector_error': None,
        'wall_seconds': 1.0, 'child_user_cpu_seconds': 0.5, 'child_system_cpu_seconds': 0.25,
        'child_cpu_seconds': 0.75, 'supervisor_exclusive_cpu_sample': 0.25,
        'supervisor_cpu_allocation_charged': 31, 'supervisor_final_write_tail_measured': False,
        'child_peak_rss_kib': 100, 'supervisor_peak_rss_kib': 100,
        'log_bytes_reserved': [0, 0], 'log_bytes_read': [0, 0],
        'logs': [{'path': str(Path(spec['directory']) / name), 'bytes': 0, 'sha256': '0' * 64}
                 for name in ('stdout.txt', 'stderr.txt')], 'failures': []}
    suite.case('state_execution', 'complete-execution-receipt', lambda:
        call_true(supervisor.validate_execution, execution, command, str(ROOT), limits))
    for label, path, value in (
            ('unreaped', ('child_reaped',), False), ('unguarded', ('parent_death_guard',), False),
            ('wall-overshoot', ('wall_seconds',), 121), ('cpu-overshoot', ('child_cpu_seconds',), 32),
            ('log-overflow', ('log_overflow',), True), ('child-failed', ('exit_code',), 1),
            ('collector-error', ('collector_error',), 'failure'),
            ('bool-receipt-count', ('log_bytes_read', 0), True),
            ('arbitrary-command', ('command',), command + ['--retry'])):
        suite.case('state_execution', 'execution-' + label, lambda path=path, value=value:
            supervisor.validate_execution(changed(execution, path, value), command, str(ROOT), limits), True)
    def missing_output_retained():
        reserved = dict(state, in_flight={'job': 'mock-normal'})
        with patched(common, 'read_json', lambda *_a: (_ for _ in ()).throw(FileNotFoundError('missing result'))):
            try:
                common.read_json('memory-only missing result')
            except FileNotFoundError:
                supervisor.require_next_job(reserved, 'mock-normal')
                return False
        return False
    suite.case('state_execution', 'missing-output-retained-reserve-stops', missing_output_retained, True)
    def prelaunch_failure():
        reservation = {'job': 'mock-normal', 'allocation_reserved': 62,
            'certificate_bytes_reserved': 0, 'artifact_bytes_reserved': 6 * MIB,
            'command': command, 'approval_sha256': approval_pin}
        failed = dict(copy.deepcopy(state), in_flight=copy.deepcopy(reservation))
        try:
            raise ValueError('literal prelaunch hash/read/disk failure')
        except ValueError:
            preserved = supervisor.retain_failed_reservation(failed, 'mock-normal')
        require(preserved is failed and failed['in_flight'] == reservation and failed['stopped'] is True
                and failed['canceled'] == list(common.JOBS[1:]) and failed['completed'] == []
                and failed['allocation_charged'] == 0, 'full failed prelaunch reservation survives')
        try:
            supervisor.require_next_job(failed, 'mock-normal')
        except ValueError:
            return True
        return False
    suite.case('state_execution', 'prelaunch-failure-retains-full-reserve', prelaunch_failure)


def file_cases(suite, common):
    class MemoryPath:
        def __init__(self, data, symlink=False, reported_size=None):
            self.data, self.link, self.reported_size = data, symlink, reported_size
            self.parent = self
        def is_file(self): return True
        def is_dir(self): return True
        def is_symlink(self): return self.link
        def stat(self):
            return types.SimpleNamespace(st_size=len(self.data) if self.reported_size is None else self.reported_size)
        def open(self, mode):
            if mode == 'xb':
                raise FileExistsError('one-use destination already exists')
            require(mode == 'rb', 'read-only in-memory fixture')
            return io.BytesIO(self.data)
    def read(data, limit=100, pin=None, symlink=False, size=None):
        fixture = MemoryPath(data, symlink, size)
        with patched(common, 'Path', lambda _path: fixture):
            return common.read_json('memory-only', limit, pin)
    suite.case('file_boundaries', 'bounded-json-correct-pin', lambda:
        read(b'{"a":1}', pin=hashlib.sha256(b'{"a":1}').hexdigest()) == {'a': 1})
    suite.case('file_boundaries', 'reader-duplicate-key', lambda: read(b'{"a":1,"a":2}'), True)
    suite.case('file_boundaries', 'reader-nan', lambda: read(b'{"a":NaN}'), True)
    suite.case('file_boundaries', 'reader-infinity', lambda: read(b'{"a":Infinity}'), True)
    suite.case('file_boundaries', 'reader-symlink', lambda: read(b'{}', symlink=True), True)
    suite.case('file_boundaries', 'reader-input-pin-mismatch', lambda: read(b'{}', pin='0' * 64), True)
    suite.case('file_boundaries', 'reader-growth-overflow', lambda: read(b'{}    ', limit=2, size=2), True)
    def existing():
        fixture = MemoryPath(b'{}')
        with patched(common, 'Path', lambda _path: fixture):
            common.write_new('memory-only', {})
    suite.case('file_boundaries', 'exclusive-marker-no-retry', existing, True)


def pair_cases(suite, supervisor):
    normal = {key: None for key in supervisor.REPORT_KEYS}
    normal.update(slot='K4-normal', case_id='v002', python_optimized=False,
        status='VERIFIED_EMPTY', preflight={'resources': {'wall_seconds': 1.0, 'supports': 4495}},
        producer={'resources': {'wall_seconds': 1.0, 'steps': 1}},
        verification={'resources': {'wall_seconds': 1.0, 'fiber_points': 0}},
        resources={'worker_wall_seconds': 1.0, 'worker_cpu_seconds': 0.5},
        semantic_summary={'producer_nontime_sha256': '0' * 64, 'joint_predictions': 0})
    optimized = dict(copy.deepcopy(normal), slot='K4-optimized', python_optimized=True)
    suite.case('mode_pair', 'same-pair', lambda: supervisor.compare_pair(normal, optimized))
    timed = copy.deepcopy(optimized)
    for path in (('preflight', 'resources', 'wall_seconds'), ('producer', 'resources', 'wall_seconds'),
                 ('verification', 'resources', 'wall_seconds'), ('resources', 'worker_wall_seconds'),
                 ('resources', 'worker_cpu_seconds')):
        timed = changed(timed, path, 2.0)
    suite.case('mode_pair', 'only-frozen-times-excluded', lambda: supervisor.compare_pair(normal, timed))
    for label, path, value in (
            ('producer-counter', ('producer', 'resources', 'steps'), 2),
            ('preflight-counter', ('preflight', 'resources', 'supports'), 4494),
            ('reference-counter', ('verification', 'resources', 'fiber_points'), 1),
            ('full-relation-digest', ('semantic_summary', 'producer_nontime_sha256'), '1' * 64),
            ('joint-count', ('semantic_summary', 'joint_predictions'), 1),
            ('source-role', ('case_id',), 'v000')):
        suite.case('mode_pair', 'reject-pair-' + label, lambda path=path, value=value:
            supervisor.compare_pair(normal, changed(optimized, path, value)), True)


def worker_path_cases(suite, common, worker, independent, freeze, freeze_pin, approval_pin):
    """Only literal stubs enter the actual adapter orchestration, never science.

    Grants/files are in-memory replacements, not active authority objects. The
    missing-approval case must exit before a raw read. All other failures clear
    the worker's producer/reference/semantic fields before its captured report.
    """
    def one(mode):
        job = 'CTRL-positive-normal'
        spec = freeze['jobs'][job]
        raw, result, verified = relation_literal()
        result['stats'] = {}
        result['resources'] = {'steps': 3, 'core_work': 2, 'core_solves': 1,
                               'core_terms': 2, 'wall_seconds': 0.0}
        verified['resources'] = {'fiber_points': 1, 'wall_seconds': 0.0}
        instance = worker.convert_raw(raw, 'v000')
        expected = {'raw_sha256': freeze['inputs']['positive']['sha256'],
                    'expected_contexts': instance['contexts'], 'expected_observed': instance['observed']}
        preflight = {'status': 'WORKLOAD_ADMITTED', 'checked_supports': 4495,
                     'exact_W': 1, 'lower_bound': 1,
                     'certificate': {'complete': True}}
        writes = []; calls = {'raw': 0, 'preflight': 0, 'producer': 0, 'reference': 0}
        def read_raw(*_a):
            calls['raw'] += 1
            return raw
        def pf(*_a):
            calls['preflight'] += 1
            if mode == 'control-gate':
                return {'status': 'GATE_REJECTED_LOWER_BOUND', 'lower_bound': 1000001,
                        'exact_W': None, 'certificate': {'complete': True}}
            return preflight
        def produce(*_a, **_k):
            calls['producer'] += 1
            return result
        def verify(*_a, **_k):
            calls['reference'] += 1
            return dict(verified, status='VERIFIED_EMPTY') if mode == 'reference-mismatch' else verified
        check = types.SimpleNamespace(convert_raw_independent=independent.convert_raw_independent,
            interpret_verified=independent.interpret_verified, verify_control_expectations=lambda *_a: True)
        modules = {str(ROOT / 'input_check.py'): check,
            str(worker.REFERENCE): types.SimpleNamespace(BudgetV3=lambda **_k: object(), verify_result_v3=verify),
            str(worker.PREFLIGHT): types.SimpleNamespace(EvidenceBudget=lambda: object(), run=pf),
            str(worker.CHECKER): object(), str(worker.AFFINE): object(),
            str(worker.ENGINE): types.SimpleNamespace(Budget=lambda **_k: object(), decode=produce)}
        def grant(*_a):
            if mode == 'missing-approval':
                raise FileNotFoundError('explicit authority absent')
            return {'stage': 'controls'}
        def postfreeze(*_a):
            if mode == 'postseal-mismatch':
                raise ValueError('changed post-run source bytes')
            return freeze
        def expected_read(path, _limit, pin):
            require(str(path) == freeze['inputs']['positive']['expected_path'] and
                    str(path) != freeze['inputs']['K4']['path'] and
                    pin == freeze['inputs']['positive']['expected_sha256'], 'control-only expected path/hash')
            return expected
        args = ['--job', job, '--freeze-sha256', freeze_pin,
                '--approval-sha256', approval_pin, '--output', spec['output']]
        with contextlib.ExitStack() as stack:
            for obj, name, replacement in (
                    (worker, 'bootstrap', lambda _p: (common, freeze)),
                    (common, 'require_child_bounds', lambda _s: None),
                    (common, 'validate_child_command', lambda *_a: spec),
                    (common, 'read_authority', grant), (common, 'read_authorized_raw', read_raw),
                    (common, 'read_json', expected_read),
                    (common, 'load_pinned', lambda _n, path, _p: modules[str(path)]),
                    (common, 'freeze_context', postfreeze),
                    (worker, 'write_report', lambda _p, report: writes.append(copy.deepcopy(report)))):
                stack.enter_context(patched(obj, name, replacement))
            try:
                status = worker.main(args)
            except FileNotFoundError:
                return mode == 'missing-approval' and calls == {'raw': 0, 'preflight': 0, 'producer': 0, 'reference': 0} and writes == []
        require(len(writes) == 1, 'one captured failure report')
        report = writes[0]
        return status == 1 and report['status'] == 'INCOMPLETE_OR_FAILED' and all(
            report[name] is None for name in ('producer', 'verification', 'semantic_summary', 'control_check')) and (
            calls['producer'] == calls['reference'] == 0 if mode == 'control-gate' else calls['reference'] == 1)
    for mode in ('missing-approval', 'reference-mismatch', 'postseal-mismatch', 'control-gate'):
        suite.case('worker_fail_closed', 'worker-path-' + mode, lambda mode=mode: one(mode))


def report_cases(suite, supervisor, freeze, freeze_pin, approval_pin):
    """Fabricated metadata shapes only, not certificates or scientific claims."""
    def complete(job, empty):
        spec = freeze['jobs'][job]
        pf_counts = {name: 0 for name in supervisor.PREFLIGHT_COUNTERS}
        pf_counts.update(wall_seconds=0.0, supports=4495, solve_calls=4495, certificate_checks=8990)
        producer_counts = {name: 0 for name in supervisor.PRODUCER_COUNTERS}
        reference_counts = {name: 0 for name in supervisor.REFERENCE_COUNTERS}
        reference_counts['fiber_points'] = 0 if empty else 1
        n = 0 if empty else 1
        return {'schema': 'k4-residual-slot-report-v1', 'slot': job,
            'stage': spec['stage'], 'input_role': spec['input_key'], 'case_id': spec['internal_id'],
            'python_optimized': spec['optimized'], 'freeze_sha256': freeze_pin,
            'input_sha256': freeze['inputs'][spec['input_key']]['sha256'],
            'approval_sha256': approval_pin, 'source_sha256': freeze['files'],
            'status': 'VERIFIED_EMPTY' if empty else 'VERIFIED_EXACT',
            'preflight': {'status': 'WORKLOAD_ADMITTED', 'checked_supports': 4495,
                'lower_bound': n, 'exact_W': n, 'resources': pf_counts,
                'certificate': {'name': 'case.cert.jsonl', 'bytes': 1, 'sha256': '0' * 64, 'complete': True}},
            'producer': {'status': 'EMPTY' if empty else 'EXACT',
                'resources': dict(producer_counts, wall_seconds=0.0),
                'stats': {name: 0 for name in ('containers', 'beta_candidates', 'incompatible_beta',
                    'excluded_B', 'eligible_pieces', 'empty_pieces', 'feasible_pieces')}},
            'verification': {'version': 'independent-residual-reference-3',
                'source_sha256': freeze['files']['/workspace/shared/canonical-residual-reference-v3/reference_v3.py'],
                'request_sha256': '0' * 64, 'status': 'VERIFIED_EMPTY' if empty else 'VERIFIED_EXACT',
                'resources': dict(reference_counts, wall_seconds=0.0), 'pieces_checked': n,
                'canonical_functions': n, 'original_lifts': n, 'joint_predictions': n,
                'stats': {name: 0 for name in ('supports', 'beta_candidates', 'eligible_beta',
                    'retained_points', 'legacy_ambient_points_equivalent')}},
            'semantic_summary': {'producer_nontime_sha256': '0' * 64,
                'masks': [[] if empty else [2] for _ in range(91)],
                'pieces': n, 'canonical_functions': n, 'original_lifts': n, 'joint_predictions': n,
                'feasibility_witness': None if empty else {'piece': 'stub', 'theta': [[28, 1], [29, 1]]},
                'interpretation': {'classification': 'EMPTY' if empty else 'CONDITIONAL_SINGLETON_TAIL',
                    'plaintext_masks': [[] if empty else ['Y'] for _ in range(91)],
                    'example_plaintext_tail': None if empty else 'Y' * 91, 'first_six_claimed': False}},
            'control_check': {'status': 'PASS', 'expected_sha256': freeze['inputs'][spec['input_key']]['expected_sha256']}
                if spec['stage'] == 'controls' else None,
            'resources': {'worker_wall_seconds': 0.0, 'worker_cpu_seconds': 0.0,
                'producer_counters': producer_counts, 'reference_counters': reference_counts,
                'producer_attempted': True, 'reference_attempted': True}, 'reason': None}
    exact = complete('CTRL-positive-normal', False)
    empty = complete('CTRL-empty-normal', True)
    def checked(report):
        return supervisor.validate_report(report, freeze['jobs'][report['slot']], freeze,
                                           freeze_pin, approval_pin)
    suite.case('supervisor_reports', 'report-complete-EXACT', lambda: checked(exact) == 'VERIFIED_EXACT')
    suite.case('supervisor_reports', 'report-complete-EMPTY', lambda: checked(empty) == 'VERIFIED_EMPTY')
    gate = complete('K4-normal', False)
    gate.update(status='CERTIFIED_RESOURCE_GATE', producer=None, verification=None,
                semantic_summary=None, control_check=None)
    gate['preflight'].update(status='GATE_REJECTED_LOWER_BOUND', checked_supports=1,
                            lower_bound=1000001, exact_W=None)
    gate['preflight']['resources'].update(supports=1, solve_calls=1, certificate_checks=2)
    gate['resources'].update(producer_counters=None, reference_counters=None,
                             producer_attempted=False, reference_attempted=False)
    suite.case('supervisor_reports', 'report-resource-gate-no-result', lambda: checked(gate) == 'CERTIFIED_RESOURCE_GATE')
    incomplete = dict(copy.deepcopy(exact), status='INCOMPLETE_OR_FAILED', producer=None,
        verification=None, semantic_summary=None, control_check=None, reason='literal failed stage')
    suite.case('supervisor_reports', 'report-incomplete-no-result', lambda: checked(incomplete) == 'INCOMPLETE_OR_FAILED')
    rejects = (
        ('EXACT-crossed-verifier', changed(exact, ('verification', 'status'), 'VERIFIED_EMPTY')),
        ('EMPTY-crossed-verifier', changed(empty, ('verification', 'status'), 'VERIFIED_EXACT')),
        ('EMPTY-partial-inventory', changed(empty, ('semantic_summary', 'masks'), [])),
        ('W-zero-alone', dict(empty, producer=None, verification=None, semantic_summary=None)),
        ('incomplete-partial-claim', dict(incomplete, semantic_summary=exact['semantic_summary'])),
        ('gate-partial-claim', dict(gate, semantic_summary=exact['semantic_summary'])),
        ('bool-cap-counter', changed(exact, ('preflight', 'resources', 'supports'), True)),
        ('extra-resource-field', changed(exact, ('producer', 'resources'), dict(exact['producer']['resources'], score=1))),
        ('over-cap-wall', changed(exact, ('preflight', 'resources', 'wall_seconds'), 61.0)))
    for label, report in rejects:
        suite.case('supervisor_reports', 'reject-report-' + label, lambda report=report: checked(report), True)


def loader_cases(suite, common, authenticated_loader):
    """Real loader helper, in-memory literal bytes, no imported test module file."""
    literal = b'VALUE = 7\n'
    class MemoryPath:
        def __init__(self, oversized=False): self.oversized = oversized
        def __str__(self): return '/memory-only/frozen-literal.py'
        def is_file(self): return True
        def is_symlink(self): return False
        def stat(self): return types.SimpleNamespace(st_size=MIB + 1 if self.oversized else len(literal))
        def open(self, mode):
            require(mode == 'rb', 'literal-loader read mode')
            return io.BytesIO(literal)
    def one(mode):
        path = MemoryPath(mode == 'oversized')
        name = 'k4_mock_authenticated_literal_' + mode
        events = {'compile': 0, 'exec_module': 0}
        original_compile = builtins.compile
        class CacheTrap:
            def create_module(self, _spec): return None
            def exec_module(self, _module):
                events['exec_module'] += 1
                raise ValueError('cache execution forbidden')
        def spec_for(module_name, module_path):
            require(module_name == name and str(module_path) == str(path), 'fixed literal module identity')
            spec = importlib.machinery.ModuleSpec(module_name, CacheTrap(), origin=str(module_path))
            spec.has_location = True
            return spec
        def compile_counted(source, filename, mode_value, **kwargs):
            events['compile'] += 1
            require(source == literal and filename == str(path) and mode_value == 'exec'
                    and kwargs == {'dont_inherit': True, 'optimize': sys.flags.optimize},
                    'authenticated compiler byte/flag identity')
            return original_compile(source, filename, mode_value, **kwargs)
        try:
            with patched(common, 'Path', lambda _p: path), \
                 patched(importlib.util, 'spec_from_file_location', spec_for), \
                 patched(builtins, 'compile', compile_counted):
                pin = '0' * 64 if mode == 'wrong-hash' else hashlib.sha256(literal).hexdigest()
                try:
                    module = authenticated_loader(name, path, pin)
                except ValueError:
                    return mode in ('wrong-hash', 'oversized') and events == {'compile': 0, 'exec_module': 0} and name not in sys.modules
            return mode in ('valid', 'no-cache') and module.VALUE == 7 and module.__name__ == name and \
                module.__file__ == str(path) and module.__spec__.name == name and \
                sys.modules.get(name) is module and events == {'compile': 1, 'exec_module': 0}
        finally:
            sys.modules.pop(name, None)
    for label, mode in (
            ('authenticated-literal-module-identity', 'valid'), ('wrong-hash-before-compile', 'wrong-hash'),
            ('source-cap-before-compile', 'oversized'), ('loader-exec-module-never-used', 'no-cache')):
        suite.case('byte_loader', label, lambda mode=mode: one(mode))


def authorized_run(args, actual, counts):
    common, freeze = bootstrap(args.freeze_sha256)
    require(args.job in ('mock-normal', 'mock-optimized'), 'exact mock job only')
    common.require_child_bounds('mocks')
    spec = common.validate_child_command(freeze, args.job, args.freeze_sha256, args.approval_sha256, actual)
    require(args.output == spec['output'] and freeze['mock_counts'] == EXPECTED_COUNTS,
            'frozen output and exact finite mock counts')
    approval = common.read_authority('mocks', freeze, args.freeze_sha256, args.approval_sha256)
    modules = {'common.py': common, 'protocol_mock_tests.py': sys.modules[__name__]}
    sources = {}
    for name in common.LOCAL_SOURCES:
        content = _bytes(ROOT / name, MIB)
        require(hashlib.sha256(content).hexdigest() == freeze['files'][str(ROOT / name)],
                'inert-probe source hash')
        sources[name] = content
    for name in ('worker.py', 'input_check.py', 'bounded_stage.py', 'supervisor.py', 'seal_results.py'):
        modules[name] = memory_module('k4_mock_operational_' + name[:-3], ROOT / name, sources[name])
    forbidden = {item['path'] for item in freeze['inputs'].values()} | {
        item['expected_path'] for item in freeze['inputs'].values() if item['expected_path'] is not None}
    suite = Suite()
    authenticated_loader = common.load_pinned
    report = {'schema': REPORT_SCHEMA, 'job': args.job, 'freeze_sha256': args.freeze_sha256,
        'approval_sha256': args.approval_sha256, 'python_optimized': spec['optimized'],
        'status': 'INCOMPLETE_OR_FAILED', 'counts': suite.counts,
        'actual_forbidden_calls': counts, 'reason': None}
    try:
        with forbidden_io(common, modules['worker.py'], forbidden, counts):
            inert_cases(suite, sources, modules)
            raw_and_mapping_cases(suite, common, modules['worker.py'], modules['input_check.py'])
            relation_cases(suite, modules['worker.py'], modules['input_check.py'])
            authority_cases(suite, common, freeze, args.freeze_sha256, approval)
            command_cases(suite, common, freeze, args.freeze_sha256, args.approval_sha256, args.job)
            digest_cases(suite, modules['worker.py'])
            collector_cases(suite, modules['bounded_stage.py'], common)
            state_cases(suite, modules['supervisor.py'], common, freeze,
                        args.freeze_sha256, args.approval_sha256)
            file_cases(suite, common)
            pair_cases(suite, modules['supervisor.py'])
            worker_path_cases(suite, common, modules['worker.py'], modules['input_check.py'],
                              freeze, args.freeze_sha256, args.approval_sha256)
            report_cases(suite, modules['supervisor.py'], freeze, args.freeze_sha256, args.approval_sha256)
            loader_cases(suite, common, authenticated_loader)
        require(suite.counts == EXPECTED_COUNTS and all(suite.names[group] == set(names)
                for group, names in EXPECTED_CASES.items()) and all(value == 0 for value in counts.values()),
                'complete finite counts and zero forbidden actual calls')
        common.freeze_context(args.freeze_sha256)
        require(common.sha(ROOT / 'approvals' / 'mocks.json', 65536) == args.approval_sha256,
                'post-mock approval unchanged')
        report['status'] = 'PASS'
    except BaseException as error:
        report['reason'] = type(error).__name__ + ': ' + str(error)[:500]
    return common, report


def main(argv=None):
    parser = argparse.ArgumentParser(description='Finite operational stubs only; no implicit invocation.')
    for flag in ('job', 'freeze-sha256', 'approval-sha256', 'output'):
        parser.add_argument('--' + flag, required=True)
    args = parser.parse_args(argv)
    counts = {key: 0 for key in FORBIDDEN_COUNTER_KEYS}
    actual = list(sys.argv[1:] if argv is None else argv)
    with source_only_guard(counts):
        common, report = authorized_run(args, actual, counts)
    # The only mock-worker write is the fixed result after all guards restore;
    # stdout/stderr and the one-use reservation belong to the outer supervisor.
    common.write_new(args.output, report)
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
