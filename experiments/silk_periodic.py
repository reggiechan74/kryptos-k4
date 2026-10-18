"""Fixed photographed chart plus hypothetical periodic-key constraints only."""
import argparse
import itertools
import json
import time

from bounded_models import deadline_check
from run_bounded import ROOT, execute, inputs_hashes, validated_baseline
from run_io import specification
from structural_checks import known_pairs

SPEC = 'research/specifications/SILK-PERIODIC-001.json'
CHART = 'data/silk-red-black-chart.json'
RECEIPT = 'sources/silk-chart-verification.json'


def validate_chart(chart):
    alphabet, keys, columns = chart['plaintext_order'], chart['key_order'], chart['columns']
    if not alphabet or len(set(alphabet)) != len(alphabet) or keys != alphabet or set(columns) != set(keys):
        raise ValueError('explicit matching unique row/key orders required')
    m = len(alphabet)
    for col in columns.values():
        if len(col) != m or set(col) != set(alphabet):
            raise ValueError('column is not a full permutation')
    for i in range(m):
        if set(columns[k][i] for k in keys) != set(alphabet):
            raise ValueError('row does not give a unique key for every output')
    fixed = []
    for key, col in columns.items():
        for i, p in enumerate(alphabet):
            if col[alphabet.index(col[i])] != p:
                raise ValueError('column is not reciprocal')
            if col[i] == p:
                fixed.append({'key': key, 'plain_and_cipher': p})
    return {'column_permutations': m, 'row_permutations': m, 'reciprocal_cell_checks': m * m,
            'fixed_points': fixed, 'pixel_retranscription_of_all_cells_claimed': False}


def transform(text, key, chart):
    alphabet = chart['plaintext_order']
    if not key or any(k not in chart['key_order'] for k in key) or any(c not in alphabet for c in text):
        raise ValueError('literal alphabet letters and nonempty key required')
    return ''.join(chart['columns'][key[i % len(key)]][alphabet.index(p)] for i, p in enumerate(text))


def required_key(plain, cipher, chart):
    alphabet = chart['plaintext_order']
    if plain not in alphabet or cipher not in alphabet or len(plain) != 1 or len(cipher) != 1:
        raise ValueError('literal single letters required')
    candidates = [k for k in chart['key_order'] if chart['columns'][k][alphabet.index(plain)] == cipher]
    if len(candidates) != 1:
        raise ValueError('required key is not unique')
    return candidates[0]


def compatibility(requirements, period):
    if type(period) is not int or period < 1:
        raise ValueError('positive integer period required')
    positions = [r['position_one_based'] for r in requirements]
    if any(type(p) is not int or p < 1 for p in positions) or len(set(positions)) != len(positions):
        raise ValueError('unique positive one-based positions required')
    phases, conflicts = {}, []
    for r in sorted(requirements, key=lambda r: r['position_one_based']):
        p, key = r['position_one_based'], r['required_key']
        if not isinstance(key, str) or len(key) != 1:
            raise ValueError('single required key symbols required')
        phase = (p - 1) % period
        if phase not in phases:
            phases[phase] = {'phase_zero_based': phase, 'positions_one_based': [], 'required_keys': []}
        group = phases[phase]
        if group['required_keys'] and group['required_keys'][0] != key:
            conflicts.append({'positions_one_based': [group['positions_one_based'][0], p],
                              'required_keys': [group['required_keys'][0], key], 'phase_zero_based': phase})
        group['positions_one_based'].append(p)
        group['required_keys'].append(key)
    return {'period': period, 'compatible': not conflicts,
            'independent_phase_comparisons': len(requirements) - len(phases),
            'observed_phases': len(phases), 'unassigned_key_phases': period - len(phases),
            'phase_constraints': [phases[i] for i in sorted(phases)],
            'first_conflict': conflicts[0] if conflicts else None, 'conflicts': conflicts}


def controls(chart, receipt):
    structural = validate_chart(chart)
    alphabet = chart['plaintext_order']
    roundtrips = 0
    for key in chart['key_order']:
        cipher = transform(alphabet, key, chart)
        assert transform(cipher, key, chart) == alphabet
        roundtrips += len(alphabet)
    example = receipt['modern_worked_example']
    actual = transform(example['plaintext_letters'], example['repeated_key'], chart)
    assert actual == example['pixel_supported_output'] == 'ZEAAIZXQOTFL'
    assert actual != example['source_printed_output']
    assert transform(actual, example['repeated_key'], chart) == example['plaintext_letters']
    assert chart['columns']['I'][alphabet.index('K')] == 'Z'
    for cell in receipt['decisive_cells']:
        assert chart['columns'][cell['key']][alphabet.index(cell['plain'])] == cell['cipher']
        assert required_key(cell['plain'], cell['cipher'], chart) == cell['key']
    assert required_key('S', 'S', chart) == required_key('K', 'K', chart) == 'X'
    toy = {'plaintext_order': 'ABC', 'key_order': 'ABC', 'columns': {'A': 'ACB', 'B': 'BAC', 'C': 'CBA'}}
    validate_chart(toy)
    plain = 'ABCABCABC'
    toy_roundtrips = positives = negatives = 0
    for period in (1, 2, 3):
        for symbols in itertools.product('ABC', repeat=period):
            key = ''.join(symbols)
            independent = ''.join('ABC'[('ABC'.index(key[i % period]) - 'ABC'.index(p)) % 3]
                                  for i, p in enumerate(plain))
            assert transform(plain, key, toy) == independent
            assert transform(independent, key, toy) == plain
            toy_roundtrips += 1
            changed = list(independent)
            changed_key = ('ABC'.index(key[0]) + 1) % 3
            changed[period] = 'ABC'[(changed_key - 'ABC'.index(plain[period])) % 3]
            for offset in (0, 1, 7):
                good = [{'position_one_based': i + 1 + offset, 'required_key': required_key(p, c, toy)}
                        for i, (p, c) in enumerate(zip(plain, independent))]
                bad = [{'position_one_based': i + 1 + offset, 'required_key': required_key(p, c, toy)}
                       for i, (p, c) in enumerate(zip(plain, changed))]
                assert compatibility(good, period)['compatible']
                assert not compatibility(bad, period)['compatible']
                positives += 1
                negatives += 1
    vacuous = compatibility([{'position_one_based': 100, 'required_key': 'A'}], 12)
    assert vacuous['compatible'] and vacuous['independent_phase_comparisons'] == 0
    assert (roundtrips, toy_roundtrips, positives, negatives) == (676, 39, 117, 117)
    return {'chart_structure': structural, 'table_cell_roundtrips': roundtrips,
            'modern_worked_example_computed': actual, 'source_example_typo_not_adopted': True,
            'independent_decisive_cells_matched': 24, 'toy_roundtrips': toy_roundtrips,
            'shifted_positive_checks': positives, 'shifted_negative_checks': negatives,
            'vacuous_case_preserved': True, 'randomness': 'none'}


def audit(data, chart):
    required = [{'position_one_based': i + 1, 'plain': p, 'cipher': c, 'required_key': required_key(p, c, chart)}
                for i, c, p in known_pairs(data)]
    segments = [''.join(r['required_key'] for r in required if crib['start'] <= r['position_one_based'] <= crib['end'])
                for crib in data['cribs']]
    first = [r for r in required if 22 <= r['position_one_based'] <= 34]
    distinct = len(first) == len({r['required_key'] for r in first}) == 13
    records = [compatibility(required, period) for period in range(1, 13)]
    short = []
    if distinct:
        for period in range(1, 13):
            short.append({'period': period, 'positions_one_based': [22, 22 + period],
                          'required_keys': [first[0]['required_key'], first[period]['required_key']],
                          'same_phase_for_any_global_origin': True})
    return {'experiment': 'SILK-PERIODIC-001', 'required_key_lookups': required,
            'required_key_segments': segments, 'first_segment13distinct': distinct,
            'period_records': records, 'periods_tested': 12,
            'compatible_periods': [r['period'] for r in records if r['compatible']],
            'contradicted_periods': [r['period'] for r in records if not r['compatible']],
            'short_proof_witnesses': short, 'K4_keyword_enumerations': 0,
            'full_K4_plaintexts_emitted': False,
            'scope': 'Only the frozen photographed chart plus hypothetical direct periodic key1-12. Not nonperiodic/OTP, other tables or added layers; no creator-use or historical repeated-schedule claim.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--spec-commit', required=True)
    parser.add_argument('--code-commit', required=True)
    parser.add_argument('--output-dir', default='results/silk-periodic-runs')
    args = parser.parse_args()
    if len(args.code_commit) != 40 or any(c not in '0123456789abcdef' for c in args.code_commit):
        raise ValueError('full implementation commit required')
    chart = json.loads((ROOT / CHART).read_text())
    receipt = json.loads((ROOT / RECEIPT).read_text())
    provenance = specification(args.spec_commit, SPEC)
    provenance['implementation_commit'] = args.code_commit
    holder = {}
    def preflight():
        holder['data'] = validated_baseline(ROOT / 'data/k4.json')
    def action(limit):
        started = time.monotonic()
        checked = controls(chart, receipt)
        deadline_check(started, limit)
        result = audit(holder['data'], chart)
        result['controls'] = checked
        deadline_check(started, limit)
        return result
    files = [SPEC, CHART, RECEIPT, 'data/k4.json', 'experiments/silk_periodic.py',
             'experiments/structural_checks.py', 'experiments/run_bounded.py', 'experiments/run_io.py',
             'experiments/bounded_models.py', 'experiments/check_baseline.py']
    command = 'python3 experiments/silk_periodic.py --spec-commit ' + args.spec_commit + ' --code-commit ' + args.code_commit
    run_id = execute(args.output_dir, 'SILK-PERIODIC-001', provenance,
                     [('SILK-PERIODIC-001', action, 5)], inputs_hashes(files), command, preflight)
    print('completed SILK-PERIODIC-001', run_id)


if __name__ == '__main__':
    main()
