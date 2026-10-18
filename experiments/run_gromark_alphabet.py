"""One source-pinned tuple; full alphabet feasibility is not plaintext recovery."""
import argparse
import json
import time

from bounded_models import deadline_check
from gromark_alphabet import expand, solve, verify, decrypt, encrypt
from gromark_alphabet_controls import controls
from run_bounded import ROOT, execute, inputs_hashes, validated_baseline
from run_io import specification
from structural_checks import known_pairs

SPEC = 'research/specifications/GROMARK-ALPHABET-001.json'
FIXTURE = 'data/gromark-one-survivor.json'


def audit(data, spec, fixture, limit=10):
    started = time.monotonic()
    deadline_check(started, limit)
    assert (fixture['base'], fixture['primer'], fixture['lags']) == (spec['model']['base'], spec['model']['primer'], spec['model']['lags'])
    stream = expand(fixture['base'], fixture['primer'], fixture['lags'], 97)
    pairs = known_pairs(data)
    edges = [(p, c, stream[i]) for i, c, p in pairs]
    result = solve(spec['model']['alphabet_symbols'], edges,
                   max_states=spec['resource_limits']['model_search_states'], limit=limit - (time.monotonic() - started))
    result.update({'experiment': 'GROMARK-ALPHABET-001', 'selected_tuple': fixture,
                   'stream': stream, 'known_edges': [{'position_one_based': i + 1,
                        'plain': p, 'cipher': c, 'key': stream[i]} for i, c, p in pairs],
                   'K4_tuples_tested': 1, 'additional_tuple_search': False,
                   'filters': [], 'full_K4_plaintext_emitted': False,
                   'historical_alphabets_recovered': False, 'K4_solution_claimed': False})
    if result['feasibility'] == 'satisfiable':
        w = result['witness']
        assert verify(spec['model']['alphabet_symbols'], edges, w['plain_alphabet'], w['cipher_alphabet'])
        plain = decrypt(data['ciphertext'], stream, w['plain_alphabet'], w['cipher_alphabet'])
        assert all(plain[i] == p for i, _, p in pairs)
        assert encrypt(plain, stream, w['plain_alphabet'], w['cipher_alphabet']) == data['ciphertext']
        result['verification'] = {'full_bijections': True, 'all_24_cribs': True,
                                  'exact_97_character_regeneration': True,
                                  'interpretation': 'one arbitrary complete alphabet witness, no recovered meaningful plaintext'}
    deadline_check(started, limit)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--spec-commit', required=True)
    parser.add_argument('--code-commit', required=True)
    parser.add_argument('--output-dir', default='results/gromark-alphabet-runs')
    args = parser.parse_args()
    if len(args.code_commit) != 40 or any(c not in '0123456789abcdef' for c in args.code_commit):
        raise ValueError('full implementation commit required')
    spec = json.loads((ROOT / SPEC).read_text())
    fixture = json.loads((ROOT / FIXTURE).read_text())
    provenance = specification(args.spec_commit, SPEC)
    provenance['implementation_commit'] = args.code_commit
    holder = {}
    def preflight():
        holder['data'] = validated_baseline(ROOT / 'data/k4.json')
    def action(limit):
        started = time.monotonic()
        checked = controls(spec, limit)
        deadline_check(started, limit)
        result = audit(holder['data'], spec, fixture, limit - (time.monotonic() - started))
        result['controls'] = checked
        deadline_check(started, limit)
        return result
    files = [SPEC, FIXTURE, 'data/k4.json', 'experiments/gromark_alphabet.py',
             'experiments/gromark_alphabet_controls.py', 'experiments/run_gromark_alphabet.py',
             'experiments/run_bounded.py', 'experiments/run_io.py', 'experiments/bounded_models.py',
             'experiments/check_baseline.py', 'experiments/structural_checks.py']
    command = 'python3 experiments/run_gromark_alphabet.py --spec-commit ' + args.spec_commit + ' --code-commit ' + args.code_commit
    run_id = execute(args.output_dir, 'GROMARK-ALPHABET-001', provenance,
                     [('GROMARK-ALPHABET-001', action, 10)], inputs_hashes(files), command, preflight)
    print('completed GROMARK-ALPHABET-001', run_id)


if __name__ == '__main__':
    main()
