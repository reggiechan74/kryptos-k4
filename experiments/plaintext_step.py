"""PLAINTEXT-STEP-001: twelve fixed plaintext-driven extra-step models."""
import argparse
import hashlib
import itertools
from pathlib import Path
import json
import platform
import random
import subprocess
import time

from check_controls import run as check_controls
from run_bounded import validated_baseline, inputs_hashes
from run_io import RunSnapshot, specification, json_bytes

ROOT = Path(__file__).resolve().parents[1]
SPEC = 'research/specifications/PLAINTEXT-STEP-001.json'
ALPHABETS = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'KRYPTOSABCDEFGHIJLMNQUVWXZ')
WORDS = ('KRYPTOS', 'PALIMPSEST', 'ABSCISSA')
TRIGGERS = ('AEIOU', 'BCDFGHJKLMNPQRSTVWXYZ')
SEED = 20261025


def configurations():
    for word, alphabet, trigger in itertools.product(WORDS, ALPHABETS, TRIGGERS):
        yield dict(word=word, alphabet=alphabet, trigger=trigger)


def encrypt(plain, cfg, start=0):
    alphabet, word, trigger = cfg['alphabet'], cfg['word'], cfg['trigger']
    cursor = start
    out = []
    for p in plain:
        out.append(alphabet[(alphabet.index(p) + alphabet.index(word[cursor % len(word)])) % 26])
        cursor += 1 + (p in trigger)
    return ''.join(out)


def decrypt(cipher, cfg, start=0):
    alphabet, word, trigger = cfg['alphabet'], cfg['word'], cfg['trigger']
    cursor = start
    plain = []
    for c in cipher:
        p = alphabet[(alphabet.index(c) - alphabet.index(word[cursor % len(word)])) % 26]
        plain.append(p)
        cursor += 1 + (p in trigger)
    return ''.join(plain)


def numeric_oracle(cipher, cfg):
    order = [ord(c) - 65 for c in cfg['alphabet']]
    index = {c: i for i, c in enumerate(order)}
    word = [index[ord(c) - 65] for c in cfg['word']]
    trigger = {ord(c) - 65 for c in cfg['trigger']}
    position = 0
    out = []
    for c in cipher:
        p = order[(index[ord(c) - 65] - word[position]) % 26]
        out.append(chr(p + 65))
        position = (position + (2 if p in trigger else 1)) % len(word)
    return ''.join(out)


def known_positions(data):
    return {c['start'] - 1 + j: p for c in data['cribs'] for j, p in enumerate(c['plaintext'])}


def assess(cipher, known, cfg):
    plain = decrypt(cipher, cfg)
    if encrypt(plain, cfg) != cipher:
        raise AssertionError('full regeneration failed')
    matched = [i + 1 for i, p in sorted(known.items()) if plain[i] == p]
    return dict(cfg, plaintext=plain, matched_positions_one_based=matched,
                matched_crib_letters=len(matched), east_matches=sum(22 <= i <= 34 for i in matched),
                berlin_matches=sum(64 <= i <= 74 for i in matched),
                all24_match=len(matched) == 24, full97_regeneration=len(cipher) == 97,
                free_parameters=0, initial_cursor=0,
                evidence_class='crib_fit_only' if len(matched) == 24 else 'rejected_model_output')


def controls():
    rng = random.Random(SEED)
    counts = dict(symbol_phase_roundtrips=0, planted_full_recoveries=0,
                  planted_crib_recoveries=0, mutated_crib_rejections=0, numeric_oracle_comparisons=0)
    for cfg in configurations():
        for start in range(len(cfg['word'])):
            for p in ALPHABETS[0]:
                expected = cfg['alphabet'][(cfg['alphabet'].index(p)
                                           + cfg['alphabet'].index(cfg['word'][start])) % 26]
                assert encrypt(p, cfg, start) == expected
                assert decrypt(expected, cfg, start) == p
                counts['symbol_phase_roundtrips'] += 1
        plain = list(''.join(rng.choice(ALPHABETS[0]) for _ in range(97)))
        plain[21:34] = 'EASTNORTHEAST'
        plain[63:74] = 'BERLINCLOCK'
        plain = ''.join(plain)
        known = {i: plain[i] for i in list(range(21, 34)) + list(range(63, 74))}
        cipher = encrypt(plain, cfg)
        assert decrypt(cipher, cfg) == plain
        assert numeric_oracle(cipher, cfg) == plain
        counts['planted_full_recoveries'] += 1
        assert assess(cipher, known, cfg)['all24_match']
        counts['planted_crib_recoveries'] += 1
        mutated = dict(known)
        mutated[21] = ALPHABETS[0][(ALPHABETS[0].index(mutated[21]) + 1) % 26]
        assert not assess(cipher, mutated, cfg)['all24_match']
        counts['mutated_crib_rejections'] += 1
        for _ in range(8):
            cipher = ''.join(rng.choice(ALPHABETS[0]) for _ in range(97))
            decoded = decrypt(cipher, cfg)
            assert numeric_oracle(cipher, cfg) == decoded
            assert encrypt(decoded, cfg) == cipher
            counts['numeric_oracle_comparisons'] += 1
    return counts


def scan(cipher, known, deadline):
    records = []
    for cfg in configurations():
        if time.monotonic() > deadline:
            raise TimeoutError('15-second plaintext-step budget exceeded')
        records.append(assess(cipher, known, cfg))
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--spec-commit', required=True)
    args = parser.parse_args()
    spec = specification(args.spec_commit, SPEC)
    code_commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    subprocess.run(['git', 'merge-base', '--is-ancestor', args.spec_commit, code_commit], cwd=ROOT, check=True)
    committed_spec = subprocess.check_output(['git', 'show', args.spec_commit + ':' + SPEC], cwd=ROOT)
    if hashlib.sha256(committed_spec).hexdigest() != spec['sha256']:
        raise ValueError('specification changed')
    names = [SPEC, 'data/k4.json', 'data/controls.json', 'experiments/plaintext_step.py',
             'tests/test_plaintext_step.py', 'experiments/run_io.py', 'experiments/run_bounded.py',
             'experiments/check_baseline.py', 'experiments/check_controls.py', 'experiments/ciphers.py']
    for name in names:
        if subprocess.check_output(['git', 'show', code_commit + ':' + name], cwd=ROOT) != (ROOT / name).read_bytes():
            raise ValueError('consulted file uncommitted: ' + name)
    with RunSnapshot('results/plaintext-step-runs', 'PLAINTEXT-STEP-001', spec) as snapshot:
        started = time.monotonic()
        deadline = started + 15
        snapshot.manifest['jobs'].append(dict(experiment='PLAINTEXT-STEP-001', status='running', deadline_seconds=15))
        data = validated_baseline(ROOT / 'data/k4.json')
        check_controls()
        passed = controls()
        known = known_positions(data)
        observed = scan(data['ciphertext'], known, deadline)
        nulls = []
        rng = random.Random(SEED)
        for _ in range(199):
            cipher = list(data['ciphertext'])
            rng.shuffle(cipher)
            records = scan(''.join(cipher), known, deadline)
            nulls.append(dict(max_matches=max(r['matched_crib_letters'] for r in records),
                              candidates=sum(r['all24_match'] for r in records),
                              per_model_matches=[r['matched_crib_letters'] for r in records]))
        best = max(r['matched_crib_letters'] for r in observed)
        exceed = sum(r['max_matches'] >= best for r in nulls)
        result = dict(id='PLAINTEXT-STEP-001', status='completed', spec_commit=args.spec_commit,
                      code_commit=code_commit, command='python3 experiments/plaintext_step.py --spec-commit ' + args.spec_commit,
                      python=platform.python_version(), platform=platform.platform(), controls=passed,
                      normalization='97 literal uppercase letters; fixed one-based crib intervals, internal zero-based',
                      observed=observed, free_parameters_per_model=0, initial_cursor=0,
                      nulls=nulls, seed=SEED, rng='random.Random MT19937; fresh original list each draw',
                      best_matches=best, exceedances=exceed, plus_one_conditional_tail=(exceed + 1) / 200,
                      model_evaluations=2400, elapsed_seconds=time.monotonic() - started,
                      file_sha256=inputs_hashes(names),
                      interpretation='Fixed-model outputs, no fits or solution claims on partial scores. Regeneration tests invertibility only. Null maxima cover this12model family, correlated, exploratory and resolution1/200; no correction across other experiments or historical-intent interpretation.')
        snapshot.write('PLAINTEXT-STEP-001.json', json_bytes(result))
        snapshot.manifest['jobs'][-1]['status'] = 'completed'
        def final_check():
            if time.monotonic() > deadline:
                raise TimeoutError('publication budget exceeded')
        snapshot.final_check = final_check
    print(json.dumps(dict(run_id=snapshot.run_id, per_model_matches=[r['matched_crib_letters'] for r in observed],
                          best_matches=best, candidates=sum(r['all24_match'] for r in observed),
                          exceedances=exceed, plus_one_conditional_tail=(exceed + 1) / 200,
                          controls=passed, elapsed_seconds=result['elapsed_seconds']), indent=2))


if __name__ == '__main__':
    main()
