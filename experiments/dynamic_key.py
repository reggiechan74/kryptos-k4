"""DYNAMIC-KEY-001: exact finite constraints, never a plaintext search."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import platform
import random
import subprocess
import time

from run_bounded import validated_baseline, inputs_hashes
from check_controls import run as check_controls
from run_io import RunSnapshot, specification, json_bytes

ROOT = Path(__file__).resolve().parents[1]
SPEC = 'research/specifications/DYNAMIC-KEY-001.json'
ALPHABETS = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'KRYPTOSABCDEFGHIJLMNQUVWXZ')
TRIGGERS = ('AEIOU', 'BCDFGHJKLMNPQRSTVWXYZ')
SEED = 20261022


def configurations():
    for family in ('progressive', 'ciphertext_step'):
        for alphabet in ALPHABETS:
            for sigma in (1, -1):
                for period in range(1, 13):
                    for variant in (range(26) if family == 'progressive' else TRIGGERS):
                        yield dict(family=family, alphabet=alphabet, sigma=sigma,
                                   period=period, variant=variant)


def phase_offsets(ciphertext, cfg):
    p = cfg['period']
    if cfg['family'] == 'progressive':
        return [(i % p, cfg['variant'] * (i // p) % 26)
                for i in range(len(ciphertext))]
    # Prefix sums depend exclusively on ciphertext, not the unknown plaintext/key.
    prefix = 0
    result = []
    for i, c in enumerate(ciphertext):
        result.append(((i + prefix) % p, 0))
        prefix += c in cfg['variant']
    return result


def known_positions(data):
    return {crib['start'] - 1 + j: c for crib in data['cribs']
            for j, c in enumerate(crib['plaintext'])}


def groups_score(groups):
    return sum(max(Counter(values).values()) for values in groups.values())


def analyze(ciphertext, known, cfg):
    alphabet = cfg['alphabet']
    index = {c: i for i, c in enumerate(alphabet)}
    schedule = phase_offsets(ciphertext, cfg)
    groups, anchors, train = {}, {}, {}
    first_conflict = None
    for i, plain in sorted(known.items()):
        phase, offset = schedule[i]
        key = (index[ciphertext[i]] - cfg['sigma'] * index[plain] - offset) % 26
        groups.setdefault(phase, []).append(key)
        if phase in anchors and anchors[phase][1] != key and first_conflict is None:
            first_conflict = dict(positions_one_based=[anchors[phase][0] + 1, i + 1],
                                  phase=phase, required_keys=[anchors[phase][1], key])
        anchors.setdefault(phase, (i, key))
        if 21 <= i < 34:
            train.setdefault(phase, []).append(key)
    training_compatible = all(len(set(v)) == 1 for v in train.values())
    heldout = []
    if training_compatible:
        for i, plain in sorted(known.items()):
            if 63 <= i < 74:
                phase, offset = schedule[i]
                match = None if phase not in train else (
                    (cfg['sigma'] * index[plain] + train[phase][0] + offset) % 26
                    == index[ciphertext[i]])
                heldout.append(dict(position_one_based=i + 1, matches=match))
    compatible = first_conflict is None
    record = dict(cfg, compatible=compatible, occupied_phases=len(groups),
                  free_phases=cfg['period'] - len(groups),
                  independent_equality_checks=len(known) - len(groups),
                  first_conflict=first_conflict, best_same_data_agreements=groups_score(groups),
                  training_compatible=training_compatible, heldout=heldout)
    record['candidate_gate'] = (compatible and record['free_phases'] == 0
                               and len(heldout) == 11
                               and all(v['matches'] is True for v in heldout))
    if record['candidate_gate']:
        key = [anchors[j][1] for j in range(cfg['period'])]
        plain = transform(ciphertext, key, cfg, decrypt=True)
        if not all(plain[i] == c for i, c in known.items()):
            raise AssertionError('full crib inverse failure')
        if transform(plain, key, cfg) != ciphertext:
            raise AssertionError('full regeneration failure')
        record.update(base_key=key, plaintext=plain, full_regeneration=True,
                      evidence_class='crib_fit_only')
    return record


def transform(text, key, cfg, decrypt=False):
    """Sequential invertible oracle; update state after output C is known."""
    if len(key) != cfg['period'] or any(not 0 <= k < 26 for k in key):
        raise ValueError('complete key required')
    alphabet, out = cfg['alphabet'], []
    cursor = cycle_shift = 0
    for symbol in text:
        value = alphabet.index(symbol)
        k = (key[cursor % len(key)] + cycle_shift) % 26
        result = (cfg['sigma'] * (value - k) if decrypt
                  else cfg['sigma'] * value + k) % 26
        output = alphabet[result]
        out.append(output)
        cipher = symbol if decrypt else output
        cursor += 1
        if cfg['family'] == 'ciphertext_step':
            cursor += cipher in cfg['variant']
        elif cursor % len(key) == 0:
            cycle_shift = (cycle_shift + cfg['variant']) % 26
    return ''.join(out)


def scan(ciphertext, known, deadline, retain=False):
    summaries = {f: dict(models=0, compatible=0, candidates=0, max_agreements=0,
                         training_survivors=0) for f in ('progressive', 'ciphertext_step')}
    records = []
    for cfg in configurations():
        if time.monotonic() > deadline:
            raise TimeoutError('DYNAMIC-KEY-001 60-second budget exhausted')
        r = analyze(ciphertext, known, cfg)
        s = summaries[cfg['family']]
        s['models'] += 1
        s['compatible'] += r['compatible']
        s['candidates'] += r['candidate_gate']
        s['training_survivors'] += r['training_compatible']
        s['max_agreements'] = max(s['max_agreements'], r['best_same_data_agreements'])
        if retain:
            records.append(r)
    return summaries, records


def synthetic_controls():
    rng = random.Random(SEED)
    counts = dict(roundtrips=0, planted_compatible=0, mutated_constraints_rejected=0)
    for family in ('progressive', 'ciphertext_step'):
        for alphabet in ALPHABETS:
            for sigma in (1, -1):
                for period in range(1, 13):
                    variants = (0, 1, 13, 25) if family == 'progressive' else TRIGGERS
                    for variant in variants:
                        cfg = dict(family=family, alphabet=alphabet, sigma=sigma,
                                   period=period, variant=variant)
                        key = [rng.randrange(26) for _ in range(period)]
                        plain = ''.join(rng.choice(alphabet) for _ in range(97))
                        cipher = transform(plain, key, cfg)
                        assert transform(cipher, key, cfg, True) == plain
                        counts['roundtrips'] += 1
                        known = {i: plain[i] for i in list(range(21, 34)) + list(range(63, 74))}
                        r = analyze(cipher, known, cfg)
                        assert r['compatible']
                        counts['planted_compatible'] += 1
                        schedule = phase_offsets(cipher, cfg)
                        seen = set()
                        for i in sorted(known):
                            phase = schedule[i][0]
                            if phase in seen:
                                changed = dict(known)
                                changed[i] = alphabet[(alphabet.index(plain[i]) + 1) % 26]
                                assert not analyze(cipher, changed, cfg)['compatible']
                                counts['mutated_constraints_rejected'] += 1
                                break
                            seen.add(phase)
                        else:
                            raise AssertionError('control needs a repeated phase')
    return counts


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--spec-commit', required=True)
    args = parser.parse_args()
    spec = specification(args.spec_commit, SPEC)
    committed = subprocess.check_output(['git', 'show', args.spec_commit + ':' + SPEC], cwd=ROOT)
    if hashlib.sha256(committed).hexdigest() != spec['sha256']:
        raise ValueError('specification differs from committed file')
    code_commit = git('rev-parse', 'HEAD')
    subprocess.run(['git', 'merge-base', '--is-ancestor', args.spec_commit, code_commit], cwd=ROOT, check=True)
    names = ['data/k4.json', SPEC, 'experiments/dynamic_key.py', 'tests/test_dynamic_key.py',
             'experiments/run_io.py', 'experiments/run_bounded.py', 'experiments/check_baseline.py',
             'experiments/check_controls.py', 'experiments/ciphers.py', 'data/controls.json']
    for name in names:
        if subprocess.check_output(['git', 'show', code_commit + ':' + name], cwd=ROOT) != (ROOT / name).read_bytes():
            raise ValueError('consulted input/code not committed: ' + name)
    with RunSnapshot('results/dynamic-key-runs', 'DYNAMIC-KEY-001', spec) as snapshot:
        started = time.monotonic()
        deadline = started + 60
        snapshot.manifest['jobs'].append(dict(experiment='DYNAMIC-KEY-001', status='running', deadline_seconds=60))
        data = validated_baseline(ROOT / 'data/k4.json')
        check_controls()
        controls = synthetic_controls()
        known = known_positions(data)
        observed, records = scan(data['ciphertext'], known, deadline, retain=True)
        nulls = []
        rng = random.Random(SEED)
        for draw in range(199):
            shuffled = list(data['ciphertext'])
            rng.shuffle(shuffled)
            summary, _ = scan(''.join(shuffled), known, deadline)
            nulls.append(summary)
        tails = {}
        for family, s in observed.items():
            exceed = sum(n[family]['max_agreements'] >= s['max_agreements'] for n in nulls)
            tails[family] = dict(exceedances=exceed, plus_one_conditional_tail=(exceed + 1) / 200)
        best = max(s['max_agreements'] for s in observed.values())
        exceed = sum(max(s['max_agreements'] for s in n.values()) >= best for n in nulls)
        tails['combined'] = dict(exceedances=exceed, plus_one_conditional_tail=(exceed + 1) / 200)
        result = dict(id='DYNAMIC-KEY-001', status='completed', spec_commit=args.spec_commit,
                      code_commit=code_commit, command='python3 experiments/dynamic_key.py --spec-commit ' + args.spec_commit,
                      python=platform.python_version(), platform=platform.platform(), seed=SEED,
                      rng='random.Random MT19937; fresh original ciphertext for each shuffle',
                      normalization='97 literal uppercase letters; one-based reported positions; internal zero-based',
                      controls=controls, observed=observed, records=records, nulls=nulls, tails=tails,
                      model_evaluations=sum(s['models'] for s in observed.values()) * 200,
                      elapsed_seconds=time.monotonic() - started, file_sha256=inputs_hashes(names),
                      interpretation='Exploratory conditional shuffle calibration, both full families searched in every draw; not a historical intent test. Heldout cribs were public before model design. Fits are not independent decoding.')
        if result['model_evaluations'] > 268800:
            raise RuntimeError('model cap exceeded')
        snapshot.write('DYNAMIC-KEY-001.json', json_bytes(result))
        snapshot.manifest['jobs'][-1]['status'] = 'completed'
        def final_check():
            if time.monotonic() > deadline:
                raise TimeoutError('budget exceeded during serialization')
        snapshot.final_check = final_check
    print(json.dumps(dict(run_id=snapshot.run_id, observed=observed, tails=tails,
                          controls=controls, elapsed_seconds=result['elapsed_seconds']), indent=2))


if __name__ == '__main__':
    main()
