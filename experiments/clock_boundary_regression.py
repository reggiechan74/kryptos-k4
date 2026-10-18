"""CLOCK-BOUNDARY-REG-001: verify known certificates, never scan keywords."""
import argparse
import json
import time

from bounded_models import crypt, required_key, deadline_check
from ciphers import alphabet_check
from reset_boundary_proof import analyze
from run_bounded import ROOT, execute, inputs_hashes, validated_baseline
from run_io import specification

SPEC = 'research/specifications/CLOCK-BOUNDARY-REG-001.json'


def phases(length, starts, period=11):
    if (not isinstance(starts, tuple) or not starts or starts[0] != 1
            or any(type(i) is not int for i in starts)
            or list(starts) != sorted(set(starts)) or starts[-1] > length
            or type(period) is not int or period < 1):
        raise ValueError('explicit sorted one-based starts and positive period required')
    result = []
    phase = 0
    for position in range(1, length + 1):
        if position in starts:
            phase = 0
        result.append(phase)
        phase = (phase + 1) % period
    return result


def transform(text, key, alphabet, equation, starts, decrypt=False):
    alphabet_check(alphabet)
    if not key or any(c not in alphabet for c in text + key):
        raise ValueError('explicit uppercase text and key required')
    schedule = phases(len(text), starts, len(key))
    return ''.join(crypt(letter, [alphabet.index(key[phase])], alphabet, equation, decrypt)
                   for letter, phase in zip(text, schedule))


def controls(spec, limit=10):
    started = time.monotonic()
    check = lambda: deadline_check(started, limit)
    check()
    assert spec['keywords'] == ['KRASNOJARSK', 'BERLINCLOCK', 'WELTZEITUHR']
    assert all(len(key) == 11 for key in spec['keywords'])
    assert len(spec['keywords']) * len(spec['segment_starts_one_based']) * len(spec['alphabets']) * 3 == 72
    primitive = 0
    equations = ('plus', 'minus', 'beaufort')
    for alphabet in spec['alphabets']:
        for equation in equations:
            for p in range(26):
                for k in range(26):
                    check()
                    expected = ((p + k) if equation == 'plus' else
                                (p - k) if equation == 'minus' else (k - p)) % 26
                    cipher = crypt(alphabet[p], [k], alphabet, equation)
                    assert cipher == alphabet[expected]
                    assert crypt(cipher, [k], alphabet, equation, True) == alphabet[p]
                    assert required_key(alphabet[p], cipher, alphabet, equation) == k
                    primitive += 1
    arrays = []
    comparisons = 0
    for given in spec['segment_starts_one_based']:
        starts = tuple(given)
        actual = phases(97, starts)
        independent = [(position - max(s for s in starts if s <= position)) % 11
                       for position in range(1, 98)]
        assert actual == independent
        assert actual[21] == actual[32]
        if 22 in starts and 64 in starts:
            assert actual[21] == actual[63] == 0
            assert actual[24] == actual[66] == 3
        arrays.append({'starts_one_based': given, 'phases': actual})
        comparisons += len(actual)
    plain = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ' * 4)[:97]
    key = 'ABCDEFGHIJK'
    roundtrips = negatives = 0
    for given in spec['segment_starts_one_based']:
        starts = tuple(given)
        for alphabet in spec['alphabets']:
            for equation in equations:
                check()
                # Independent formula and schedule expression, no transform call.
                reference = []
                for position, letter in enumerate(plain, 1):
                    offset = (position - max(s for s in starts if s <= position)) % 11
                    p, k = alphabet.index(letter), alphabet.index(key[offset])
                    value = p + k if equation == 'plus' else p - k if equation == 'minus' else k - p
                    reference.append(alphabet[value % 26])
                expected = ''.join(reference)
                cipher = transform(plain, key, alphabet, equation, starts)
                assert cipher == expected
                recovered = transform(cipher, key, alphabet, equation, starts, True)
                assert recovered == plain
                assert transform(recovered, key, alphabet, equation, starts) == cipher
                roundtrips += 1
                # The same-phase equality is true before, false after mutation.
                k22 = required_key(plain[21], cipher[21], alphabet, equation)
                assert k22 == required_key(plain[32], cipher[32], alphabet, equation)
                changed = alphabet[(alphabet.index(cipher[32]) + 1) % 26]
                assert k22 != required_key(plain[32], changed, alphabet, equation)
                negatives += 1
    assert (primitive, comparisons, roundtrips, negatives) == (4056, 388, 24, 24)
    check()
    return {'primitive_cases': primitive, 'phase_arrays': arrays,
            'independent_phase_comparisons': comparisons,
            'synthetic_97letter_roundtrips': roundtrips,
            'altered_position33_negative_fixtures': negatives,
            'random_seed': None, 'deterministic': True}


def verify_certificates(data, spec):
    result = analyze(data)
    witness = result['identical_reset_bijection_witness']
    assert witness['positions_one_based'] == [25, 67]
    assert witness['zero_based_offsets_after_resets'] == [3, 3]
    assert witness['ciphertext'] == ['V', 'V'] and witness['plaintext'] == ['T', 'L']
    assert witness['contradiction']
    for record in result['arithmetic_witnesses']:
        section = 'period11' if record['purpose'] == 'within_segment_period_11' else 'shared_reset'
        label = 'AZ' if record['alphabet'] == spec['alphabets'][0] else 'KRYPTOS'
        expected = spec['certificates'][section]['expected_required_key_pairs'][label][record['equation']]
        assert record['required_key_values'] == expected and record['contradiction']
    assert len(result['arithmetic_witnesses']) == 12
    result.update({'experiment': 'CLOCK-BOUNDARY-REG-001', 'certificate_count': 13,
                   'formal_cases_subsumed_analytically': 72,
                   'classification': spec['classification'],
                   'witnesses_known_before_specification': True,
                   'scope': 'Declared unchanged-alignment arithmetic period11 cases; identical-reset bijections only where both starts22/64 apply. No transposition, feedback, different keys or broader family conclusion.'})
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--spec-commit', required=True)
    parser.add_argument('--code-commit', required=True)
    parser.add_argument('--output-dir', default='results/clock-boundary-runs')
    args = parser.parse_args()
    if len(args.code_commit) != 40 or any(c not in '0123456789abcdef' for c in args.code_commit):
        raise ValueError('full implementation commit required')
    spec = json.loads((ROOT / SPEC).read_text())
    provenance = specification(args.spec_commit, SPEC)
    provenance['implementation_commit'] = args.code_commit
    holder = {}
    def preflight():
        holder['data'] = validated_baseline(ROOT / 'data/k4.json')
    def action(limit):
        started = time.monotonic()
        checked = controls(spec, limit)
        deadline_check(started, limit)
        result = verify_certificates(holder['data'], spec)
        result['controls'] = checked
        deadline_check(started, limit)
        return result
    files = [SPEC, 'data/k4.json', 'experiments/clock_boundary_regression.py',
             'experiments/reset_boundary_proof.py', 'experiments/bounded_models.py',
             'experiments/ciphers.py', 'experiments/structural_checks.py',
             'experiments/run_bounded.py', 'experiments/run_io.py', 'experiments/check_baseline.py']
    command = 'python3 experiments/clock_boundary_regression.py --spec-commit ' + args.spec_commit + ' --code-commit ' + args.code_commit
    run_id = execute(args.output_dir, 'CLOCK-BOUNDARY-REG-001', provenance,
                     [('CLOCK-BOUNDARY-REG-001', action, 10)], inputs_hashes(files), command, preflight)
    print('completed CLOCK-BOUNDARY-REG-001', run_id)


if __name__ == '__main__':
    main()
