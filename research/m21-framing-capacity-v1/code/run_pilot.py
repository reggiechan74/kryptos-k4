"""Finite synthetic M21 differential pilot. Source prepared before execution grant.

No execution occurs on import. The main matrix has exactly 24,624 cases.
This runner does not grant itself permission; an external grant/supervisor is required.
"""
import argparse
from functools import lru_cache
from itertools import product
import json
import math
from pathlib import Path
import resource
import sys
import time

# Load authenticated source bytes directly: never consult local bytecode caches.
import hashlib
import types

def authenticated_source(name):
    here = Path(__file__).resolve().parent
    frozen = json.loads((here / 'SOURCE-SHA256.json').read_text())
    source = (here / (name + '.py')).read_bytes()
    if hashlib.sha256(source).hexdigest() != frozen[name + '.py']:
        raise RuntimeError('source hash mismatch: ' + name)
    module = types.ModuleType(name)
    module.__file__ = str(here / (name + '.py'))
    exec(compile(source, module.__file__, 'exec'), module.__dict__)
    return module

oracle = authenticated_source('oracle')
p = authenticated_source('production')

EXPECTED_CASES = 24624
EXPECTED_CONTROLS = 132


def cases():
    manifest = json.loads((Path(__file__).resolve().parent / 'cases.json').read_text())
    if len(manifest) != EXPECTED_CASES:
        raise ValueError('frozen manifest does not contain 24624 cases')
    expected_manifest = []
    for codec in range(1, 13):
        for n in range(7):
            for mode in (('all',) if n == 0 else ('all', 'first_min', 'first_max')):
                for header in ('', '1', '11'):
                    for base in (2, 3, 26):
                        for width in range(1, 7):
                            for transport in ('minimal', 'fixed'):
                                expected_manifest.append({
                                    'case_id': f'M21-{len(expected_manifest) + 1:05d}',
                                    'codec': codec, 'n': n, 'mode': mode, 'header': header,
                                    'base': base, 'width': width, 'transport': transport})
    if manifest != expected_manifest:
        raise ValueError('manifest differs from exact frozen Cartesian product or IDs')
    keys = ('codec', 'n', 'mode', 'header', 'base', 'width', 'transport')
    seen = set()
    ids = set()
    for entry in manifest:
        signature = tuple(entry[key] for key in keys)
        if signature in seen or entry['case_id'] in ids:
            raise ValueError('duplicate frozen case')
        seen.add(signature)
        ids.add(entry['case_id'])
        yield entry['case_id'], signature


def baseline(lengths, lo, hi, nonzero_prefix=False, envelope=False):
    """Safe length-only necessary test; never infer nonzero from payload data."""
    if not lengths:
        return False
    candidates = range(min(lengths), max(lengths) + 1) if envelope else lengths
    for length in candidates:
        lower = (1 << (length - 1)) if nonzero_prefix and length > 0 else 0
        upper = (1 << length) - 1
        if max(lo, lower) <= min(hi, upper):
            return True
    return False


def oracle_transport(transport):
    return 'canonical' if transport == 'minimal' else transport


@lru_cache(None)
def group_info(codec, n, mode, header):
    records = oracle.records(codec, n, mode, header)
    lengths = sorted({len(bits) for _, bits, _ in records})
    raw_inputs = len(oracle.alphabet(codec)) ** (n if mode == 'all' or n == 0 else n - 1)
    # Uniform-domain source entropy is a diagnostic, never a rejection bound.
    entropy = math.log2(raw_inputs)
    return {
        'oracle_records': len(records),
        'raw_domain_inputs': raw_inputs,
        'oracle_lengths': lengths,
        'source_entropy_bits_uniform_domain': entropy,
        'mean_emitted_bits_valid_inputs': (
            sum(len(bits) for _, bits, _ in records) / len(records) if records else None),
        'entropy_is_exclusion_bound': False,
    }


class TableModel:
    deterministic = True
    def __init__(self, mapping, trailer=''):
        self.mapping = mapping
        self.alphabet = ''.join(mapping)
        self.start = 0
        self.trailer = trailer
    def step(self, state, letter):
        return 0, self.mapping[letter]
    def finish(self, state):
        return self.trailer


def direct_bits(model, text):
    """Used only for frozen fixture handchecks, not the differential oracle."""
    q = model.start
    out = ''
    for letter in text:
        q, word = model.step(q, letter)
        out += word
    tail = model.finish(q)
    return None if tail is None else out + tail


def controls(record, guard):
    """Ten mandatory control categories, with exact independent expectations."""
    def check(name, condition, **details):
        guard()
        record({'id': name, 'pass': bool(condition), **details})
        if not condition:
            raise AssertionError('control failed: ' + name)

    # Hardcoded whole-message examples precede differential comparisons.
    fixtures = [
        (1, 'ABBA', '0110'), (2, 'ABC', '01011'),
        (3, 'ABCD', '101001100100'), (4, 'ABCD', '0001100101'),
        (5, 'ABCD', '1101100111011'), (6, 'ABBC', '010011'),
        (7, 'BBBBA', '1101100'), (8, 'ABBAA', '101100'),
        (9, 'AAAABBB', '0110001110'), (10, 'BACA', '10101110'),
        (11, 'BAB', '1010'), (12, 'BBAABA', '100001'),
    ]
    for codec, text, expected in fixtures:
        actual = direct_bits(p.Model(codec), text)
        reference = oracle.encode(codec, text)
        check(f'fixture_{codec:02d}', actual == reference == expected,
              expected=expected, production=actual, oracle=reference)

    # 1 / 2: boundary values, zero convention, long leading-zero streams.
    for value in (0, 2, 3, 8, 9):
        for zeros in (0, 1, 4):
            bits = '0' * zeros + format(value, 'b')
            model = TableModel({'A': bits})
            for width in (1, 2):
                for transport in ('minimal', 'fixed'):
                    digits = oracle.digit_count(value, 3)
                    expected = int(digits == width if transport == 'minimal' else digits <= width)
                    got = p.count(model, 1, 'all', '', 3, width, transport)['count']
                    check(f'boundary_{value}_{zeros}_{width}_{transport}', got == expected,
                          count=got, expected=expected)
    empty = TableModel({'A': ''})
    for n in (0, 1):
        for width in (1, 2):
            for transport in ('minimal', 'fixed'):
                expected = int(width == 1 or transport == 'fixed')
                got = p.count(empty, n, 'all', '', 3, width, transport)['count']
                check(f'empty_{n}_{width}_{transport}', got == expected, count=got, expected=expected)

    # 3: explicit header mutations and terminal framing, each against its own oracle.
    for header in ('', '1', '11'):
        for width in (1, 2, 3):
            for codec in (1, 11):
                got = p.count(p.Model(codec), 3, 'all', header, 3, width, 'minimal')['count']
                expected = oracle.count(codec, 3, 'all', header, 3, width, 'canonical')
                check(f'header_trailer_{codec}_{header or "empty"}_{width}', got == expected,
                      count=got, expected=expected)
    class NoParity(p.Model):
        def finish(self, state):
            return ''
    class DoubleParity(p.Model):
        def finish(self, state):
            return str(int(state)) * 2
    for label, model, copies in (('missing', NoParity(11), 0), ('doubled', DoubleParity(11), 2)):
        for width in (1, 2, 3):
            values = []
            for letters in product('AB', repeat=3):
                text = ''.join(letters)
                bits = oracle.encode(1, text) + str(text.count('B') % 2) * copies
                values.append(int(bits, 2))
            expected = sum(oracle.digit_count(v, 3) == width for v in values)
            got = p.count(model, 3, 'all', '', 3, width, 'minimal')['count']
            check(f'parity_{label}_{width}', got == expected, count=got, expected=expected)

    # 4: incomplete phrases must reject without padding.
    for text in ('B', 'BB'):
        got = p.count_interval(p.Model(12), list(text), '', 0, 1023)['count']
        check('incomplete_' + text, got == 0 and oracle.encode(12, text) is None, count=got)

    # 5: exact input counts are not distinct output-integer counts.
    collision = TableModel({'A': '0', 'B': '00'})
    got = p.count_interval(collision, ['AB', 'AB'], '', 0, 0)['count']
    values = [int(''.join({'A': '0', 'B': '00'}[a] for a in letters), 2)
              for letters in product('AB', repeat=2)]
    check('colliding_encoder', got == len(values) == 4 and len(set(values)) == 1,
          plaintext_count=got, distinct_integer_count=len(set(values)), invertible=False)

    # 6: modulo transport is deliberately outside interval API.
    refused = False
    try:
        p.interval(3, 2, 'clipped')
    except NotImplementedError:
        refused = True
    check('clipped_unsupported', refused and (9 % 9 == 0) and oracle.digit_count(9, 3) == 3,
          interval_api_refused=refused, ordinary_value=9, clipped_value=0)

    # 7 / 8: position restrictions, subset/interval monotonicity and additivity.
    def domain_count(ds, lo, hi):
        got = p.count_interval(p.Model(2), ds, '1', lo, hi)['count']
        records = oracle.records_domains(2, ds, '1')
        expected = sum(lo <= value <= hi for _, _, value in records)
        check('domain_count_' + '_'.join(ds) + f'_{lo}_{hi}', got == expected,
              count=got, expected=expected)
        return got
    full = ['ABC'] * 3
    full_count = domain_count(full, 8, 63)
    expanded = domain_count(full, 0, 511)
    check('interval_expansion', expanded >= full_count,
          narrow_count=full_count, expanded_count=expanded)
    for position in range(3):
        restricted = list(full)
        restricted[position] = 'B'
        restricted_count = domain_count(restricted, 8, 63)
        check(f'domain_restriction_{position}', restricted_count <= full_count,
              restricted_count=restricted_count, full_count=full_count)
        pieces = []
        for symbol in 'ABC':
            ds = list(full)
            ds[position] = symbol
            pieces.append(domain_count(ds, 8, 63))
        check(f'domain_partition_{position}', sum(pieces) == full_count,
              parts=pieces, full_count=full_count)

    # 9: hand witnesses, both against independently enumerated exact values.
    first = p.count_interval(p.Model(1), ['AB', 'AB'], '11', 3, 8)
    first_values = [value for _, _, value in oracle.records(1, 2, 'all', '11')]
    check('witness_header', first['count'] == 0 and all(v > 8 for v in first_values)
          and baseline(first['lengths'], 3, 8, nonzero_prefix=True),
          values=first_values, count=first['count'], strong_length_baseline=True)
    second_model = TableModel({'A': '00', 'B': '11'})
    second = p.count_interval(second_model, ['B', 'AB'], '', 3, 8)
    second_values = [int('11' + tail, 2) for tail in ('00', '11')]
    check('witness_position', second['count'] == 0 and second_values == [12, 15]
          and baseline(second['lengths'], 3, 8), values=second_values, count=second['count'])

    # 10: duplicate nondeterministic paths must be explicitly refused.
    class DuplicatePaths:
        deterministic = False
        alphabet = 'A'
        start = 0
        def step(self, state, letter):
            return [(0, '0'), (0, '0')]
        def finish(self, state):
            return ''
    refused = False
    try:
        p.count_interval(DuplicatePaths(), ['A'], '', 0, 1)
    except (TypeError, NotImplementedError):
        refused = True
    check('nondeterministic_duplicate_paths_refused', refused)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--results', type=Path,
                        default=Path(__file__).resolve().parent / 'results')
    parser.add_argument('--cpu-seconds', type=float, default=180.0)
    args = parser.parse_args()
    if args.cpu_seconds <= 0:
        parser.error('positive CPU limit required')
    # Supervisor creates the directory; never overwrite scientific receipts.
    args.results.mkdir(parents=True, exist_ok=True)
    for filename in ('summary.json', 'controls.json', 'cases.jsonl'):
        if (args.results / filename).exists():
            parser.error('refusing existing scientific receipt: ' + filename)
    started = time.process_time()
    wall_started = time.monotonic()
    summary = {
        'status': 'running', 'expected_matrix_cases': EXPECTED_CASES,
        'expected_control_checks': EXPECTED_CONTROLS,
        'matrix_cases_completed': 0, 'control_checks_completed': 0,
        'mismatches': 0, 'false_pruning': 0,
        'bit_filter_exclusions_beyond_exact_length_weak': 0,
        'bit_filter_exclusions_beyond_exact_length_nonzero_guarantee': 0,
        'all_methods_same_decision': 0, 'dp_cpu_exceeds_cached_oracle_cpu': 0,
        'total_dp_cpu_seconds': 0.0, 'total_oracle_cpu_seconds': 0.0,
        'total_dp_states': 0, 'total_dp_transitions': 0,
        'total_dp_bit_work': 0, 'maximum_count_bit_length': 0,
        'source_note': 'Classical finite-state DP; synthetic validation only; no target inference.',
        'timing_note': 'Oracle caches whole-string encoding and digit histograms. Per-case timing includes cache hits; not an uncached algorithmic speed comparison.',
        'budget_cpu_seconds': args.cpu_seconds,
    }
    control_rows = []
    def guard():
        if time.process_time() - started >= args.cpu_seconds:
            raise TimeoutError('pilot CPU guard reached; unfinished cases remain unknown')
    def save_summary():
        summary['cpu_seconds'] = time.process_time() - started
        summary['wall_seconds'] = time.monotonic() - wall_started
        summary['peak_rss_kib_linux'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        (args.results / 'summary.json').write_text(json.dumps(summary, indent=2, sort_keys=True) + '\n')
        (args.results / 'controls.json').write_text(json.dumps(control_rows, indent=2, sort_keys=True) + '\n')
    def record_control(row):
        row['control_index'] = len(control_rows)
        control_rows.append(row)
        summary['control_checks_completed'] += 1
        if not row['pass']:
            summary['mismatches'] += 1
        # Flush controls on failure as well as at completion.
        if not row['pass']:
            save_summary()
    try:
        frozen_cases = list(cases())
        controls(record_control, guard)
        if summary['control_checks_completed'] != EXPECTED_CONTROLS:
            raise AssertionError('control count differs from frozen 132')
        save_summary()
        models = {codec: p.Model(codec) for codec in range(1, 13)}
        with (args.results / 'cases.jsonl').open('x') as output:
            for index, (case_id, case) in enumerate(frozen_cases):
                guard()
                codec, n, mode, header, base, width, transport = case
                before = time.process_time()
                actual = p.count(models[codec], n, mode, header, base, width, transport)
                dp_time = time.process_time() - before
                before = time.process_time()
                expected = oracle.count(codec, n, mode, header, base, width, oracle_transport(transport))
                info = group_info(codec, n, mode, header)
                oracle_time = time.process_time() - before
                lo, hi = p.interval(base, width, transport)
                weak = baseline(actual['lengths'], lo, hi)
                strong = baseline(actual['lengths'], lo, hi, nonzero_prefix=header.startswith('1'))
                envelope = baseline(actual['lengths'], lo, hi, envelope=True)
                same = actual['count'] == expected
                lengths_same = actual['lengths'] == info['oracle_lengths']
                witness_valid = actual['witness'] is None if expected == 0 else any(
                    text == actual['witness'] and lo <= value <= hi
                    for text, _, value in oracle.records(codec, n, mode, header))
                baseline_sound = not expected or (weak and strong and envelope)
                row = {
                    'case_id': case_id, 'case_index': index, 'codec': codec, 'n': n, 'mode': mode,
                    'header': header, 'base': base, 'width': width, 'transport': transport,
                    'production': actual, 'oracle_count': expected,
                    'count_match': same, 'length_set_match': lengths_same,
                    'witness_valid': witness_valid, 'baselines_sound': bool(baseline_sound),
                    'length_baseline_weak_feasible': weak,
                    'length_baseline_nonzero_guarantee_feasible': strong,
                    'minmax_length_envelope_feasible': envelope,
                    'dp_cpu_seconds': dp_time, 'cached_oracle_cpu_seconds': oracle_time,
                    **info,
                }
                output.write(json.dumps(row, sort_keys=True) + '\n')
                summary['matrix_cases_completed'] += 1
                summary['total_dp_cpu_seconds'] += dp_time
                summary['total_oracle_cpu_seconds'] += oracle_time
                summary['total_dp_states'] += actual['states']
                summary['total_dp_transitions'] += actual['transitions']
                summary['total_dp_bit_work'] += actual['bit_work']
                summary['maximum_count_bit_length'] = max(summary['maximum_count_bit_length'], actual['max_count_bits'])
                summary['dp_cpu_exceeds_cached_oracle_cpu'] += dp_time > oracle_time
                summary['bit_filter_exclusions_beyond_exact_length_weak'] += expected == 0 and weak
                summary['bit_filter_exclusions_beyond_exact_length_nonzero_guarantee'] += expected == 0 and strong
                summary['all_methods_same_decision'] += (bool(expected) == weak == strong == envelope)
                if not (same and lengths_same and witness_valid and baseline_sound):
                    summary['mismatches'] += 1
                    summary['false_pruning'] += actual['count'] == 0 and expected > 0
                    summary['failed_case_id'] = case_id
                    output.flush()
                    raise AssertionError('differential case mismatch at ' + str(index))
        if summary['matrix_cases_completed'] != EXPECTED_CASES:
            raise AssertionError('case count differs from frozen 24624')
        summary['status'] = 'pass'
        returncode = 0
    except BaseException as exc:
        summary['status'] = 'timeout_unknown' if isinstance(exc, TimeoutError) else 'failed'
        summary['error'] = type(exc).__name__ + ': ' + str(exc)
        returncode = 2
    finally:
        save_summary()
    print(json.dumps(summary, sort_keys=True), flush=True)
    return returncode


if __name__ == '__main__':
    sys.exit(main())
