"""Bounded exact audit; retain every lag, including zero-information cases."""
import argparse
from collections import Counter
import json
import time

from autokey_constraints import analyze, COEFFICIENTS
from autokey_constraint_controls import controls
from bounded_models import deadline_check
from run_bounded import ROOT, execute, inputs_hashes, validated_baseline
from run_io import specification
from structural_checks import known_pairs

SPEC = 'research/specifications/AUTOKEY-CONSTRAINT-001.json'


def audit(data, spec, limit=10):
    started = time.monotonic()
    deadline_check(started, limit)
    known = {i: p for i, _, p in known_pairs(data)}
    records = []
    groups = []
    for label, alphabet in spec['alphabets'].items():
        for feedback in spec['feedback']:
            for equation in spec['equations']:
                assert COEFFICIENTS[equation] == (spec['equations'][equation]['sigma'], spec['equations'][equation]['tau'])
                group = {'alphabet': label, 'feedback': feedback, 'equation': equation,
                         'contradicted_lags': [], 'compatible_underdetermined_lags': [],
                         'vacuous_lags': [], 'untested_lags': []}
                for lag in range(spec['lags']['minimum'], spec['lags']['maximum'] + 1):
                    deadline_check(started, limit)
                    result = analyze(data['ciphertext'], known, alphabet, equation, feedback, lag)
                    if result['classification'] == 'compatible_fully_constrained':
                        raise RuntimeError('unexpected fully constrained compatible case: independent audit required')
                    if result['classification'] == 'contradicted':
                        group['contradicted_lags'].append(lag)
                    else:
                        group['compatible_underdetermined_lags'].append(lag)
                    if result['vacuous_consistency_test']:
                        group['vacuous_lags'].append(lag)
                    records.append({'alphabet': label, 'feedback': feedback, 'equation': equation,
                                    'lag': lag, **result})
                groups.append(group)
    assert len(records) == spec['case_count'] == 1152
    counts = Counter(r['classification'] for r in records)
    deadline_check(started, limit)
    return {'experiment': 'AUTOKEY-CONSTRAINT-001', 'tested_cases': len(records),
            'classification_counts': dict(counts), 'untested_cases': 0,
            'vacuous_cases': sum(r['vacuous_consistency_test'] for r in records),
            'compatible_with_positive_consistency_checks': sum(
                r['classification'].startswith('compatible') and r['independent_consistency_checks'] > 0 for r in records),
            'groups': groups, 'records': records, 'K4_primer_enumerations': 0,
            'full_K4_plaintexts_emitted': 0, 'scoring': 'none',
            'scope': 'Forward same-alphabet direct plaintext/ciphertext feedback, independent arbitrary L-symbol primer, three stated equations, lags1-96. No other autokey or composite-family claim.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--spec-commit', required=True)
    parser.add_argument('--code-commit', required=True)
    parser.add_argument('--output-dir', default='results/autokey-constraint-runs')
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
        checked = controls(list(spec['alphabets'].values()), limit)
        deadline_check(started, limit)
        result = audit(holder['data'], spec, limit)
        result['controls'] = checked
        deadline_check(started, limit)
        return result
    files = [SPEC, 'data/k4.json', 'experiments/autokey_constraints.py',
             'experiments/autokey_constraint_controls.py', 'experiments/run_autokey_constraints.py',
             'experiments/run_bounded.py', 'experiments/run_io.py', 'experiments/bounded_models.py',
             'experiments/structural_checks.py', 'experiments/check_baseline.py']
    command = 'python3 experiments/run_autokey_constraints.py --spec-commit ' + args.spec_commit + ' --code-commit ' + args.code_commit
    run_id = execute(args.output_dir, 'AUTOKEY-CONSTRAINT-001', provenance,
                     [('AUTOKEY-CONSTRAINT-001', action, 10)], inputs_hashes(files), command, preflight)
    print('completed AUTOKEY-CONSTRAINT-001', run_id)


if __name__ == '__main__':
    main()
