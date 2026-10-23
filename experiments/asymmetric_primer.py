"""Six fixed asymmetric plaintext-autokey models; no fitting or key search."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import platform
import random
import subprocess
import time

from check_controls import run as check_controls
from run_bounded import validated_baseline, inputs_hashes
from run_io import RunSnapshot, specification, json_bytes

ROOT = Path(__file__).resolve().parents[1]
SPEC = 'research/specifications/ASYMMETRIC-PRIMER-001.json'
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
KR = 'KRYPTOSABCDEFGHIJLMNQUVWXZ'
PRIMER = 'PALIMPSEST'
SEED = 20261024


def configurations():
    for roles in itertools.product(('AZ', 'KR'), repeat=3):
        if len(set(roles)) > 1:
            yield dict(zip(('Ap', 'Ac', 'Ak'), roles))


def alphabets(cfg):
    return tuple({'AZ': AZ, 'KR': KR}[cfg[role]] for role in ('Ap', 'Ac', 'Ak'))


def encrypt(plain, cfg, primer=PRIMER):
    ap, ac, ak = alphabets(cfg)
    return ''.join(ac[(ap.index(p) + ak.index(primer[i] if i < len(primer)
                                              else plain[i - len(primer)])) % 26]
                   for i, p in enumerate(plain))


def decrypt(cipher, cfg, primer=PRIMER):
    ap, ac, ak = alphabets(cfg)
    plain = []
    for i, c in enumerate(cipher):
        key = primer[i] if i < len(primer) else plain[i - len(primer)]
        plain.append(ap[(ac.index(c) - ak.index(key)) % 26])
    return ''.join(plain)


def numeric_oracle(cipher, cfg):
    # A separately indexed circular feedback buffer; no string lag lookup.
    ap, ac, ak = [[ord(c) - 65 for c in a] for a in alphabets(cfg)]
    ci = {c: i for i, c in enumerate(ac)}
    ki = {c: i for i, c in enumerate(ak)}
    ring = [ord(c) - 65 for c in PRIMER]
    out = []
    for i, c in enumerate(cipher):
        slot = i % len(ring)
        value = ap[(ci[ord(c) - 65] - ki[ring[slot]]) % 26]
        ring[slot] = value
        out.append(chr(value + 65))
    return ''.join(out)


def known_positions(data):
    return {c['start'] - 1 + j: letter for c in data['cribs']
            for j, letter in enumerate(c['plaintext'])}


def assess(cipher, known, cfg):
    plain = decrypt(cipher, cfg)
    if encrypt(plain, cfg) != cipher:
        raise AssertionError('full regeneration failed')
    matches = [i + 1 for i, p in sorted(known.items()) if plain[i] == p]
    return dict(cfg, plaintext=plain, matched_positions_one_based=matches,
                matched_crib_letters=len(matches),
                east_matches=sum(22 <= i <= 34 for i in matches),
                berlin_matches=sum(64 <= i <= 74 for i in matches),
                all24_match=len(matches) == 24, full97_regeneration=len(cipher) == 97,
                free_parameters=0,
                evidence_class='crib_fit_only' if len(matches) == 24 else 'rejected_model_output')


def controls():
    counts = dict(symbol_roundtrips=0, planted_full_recoveries=0,
                  planted_crib_recoveries=0, mutated_crib_rejections=0,
                  random_oracle_comparisons=0)
    rng = random.Random(SEED)
    for cfg in configurations():
        ap, ac, ak = alphabets(cfg)
        assert all(len(set(a)) == 26 for a in (ap, ac, ak))
        for p in AZ:
            for key in AZ:
                cipher = encrypt(p, cfg, primer=key)
                assert decrypt(cipher, cfg, primer=key) == p
                counts['symbol_roundtrips'] += 1
        plain = list(''.join(rng.choice(AZ) for _ in range(97)))
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
        mutated[21] = AZ[(AZ.index(mutated[21]) + 1) % 26]
        assert not assess(cipher, mutated, cfg)['all24_match']
        counts['mutated_crib_rejections'] += 1
        for _ in range(8):
            random_cipher = ''.join(rng.choice(AZ) for _ in range(97))
            decoded = decrypt(random_cipher, cfg)
            assert numeric_oracle(random_cipher, cfg) == decoded
            assert encrypt(decoded, cfg) == random_cipher
            counts['random_oracle_comparisons'] += 1
    return counts


def scan(cipher, known, deadline):
    records = []
    for cfg in configurations():
        if time.monotonic() > deadline:
            raise TimeoutError('15-second asymmetric pilot budget exceeded')
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
        raise ValueError('spec differs from declared commit')
    names = [SPEC, 'data/k4.json', 'data/controls.json', 'experiments/asymmetric_primer.py',
             'tests/test_asymmetric_primer.py', 'experiments/run_io.py', 'experiments/run_bounded.py',
             'experiments/check_baseline.py', 'experiments/check_controls.py', 'experiments/ciphers.py']
    for name in names:
        if subprocess.check_output(['git', 'show', code_commit + ':' + name], cwd=ROOT) != (ROOT / name).read_bytes():
            raise ValueError('consulted file uncommitted: ' + name)
    with RunSnapshot('results/asymmetric-primer-runs', 'ASYMMETRIC-PRIMER-001', spec) as snapshot:
        started = time.monotonic()
        deadline = started + 15
        snapshot.manifest['jobs'].append(dict(experiment='ASYMMETRIC-PRIMER-001', status='running', deadline_seconds=15))
        data = validated_baseline(ROOT / 'data/k4.json')
        check_controls()
        passed = controls()
        known = known_positions(data)
        observed = scan(data['ciphertext'], known, deadline)
        rng = random.Random(SEED)
        nulls = []
        for draw in range(199):
            cipher = list(data['ciphertext'])
            rng.shuffle(cipher)
            records = scan(''.join(cipher), known, deadline)
            nulls.append(dict(max_matches=max(r['matched_crib_letters'] for r in records),
                              candidates=sum(r['all24_match'] for r in records),
                              per_model_matches=[r['matched_crib_letters'] for r in records]))
        best = max(r['matched_crib_letters'] for r in observed)
        exceed = sum(r['max_matches'] >= best for r in nulls)
        result = dict(id='ASYMMETRIC-PRIMER-001', status='completed', spec_commit=args.spec_commit,
                      code_commit=code_commit, command='python3 experiments/asymmetric_primer.py --spec-commit ' + args.spec_commit,
                      python=platform.python_version(), platform=platform.platform(),
                      normalization='97 literal uppercase letters, fixed one-based crib intervals; internal zero-based',
                      primer=PRIMER, lag=10, equation='addition', free_parameters_per_model=0,
                      controls=passed, observed=observed, nulls=nulls, seed=SEED,
                      rng='random.Random MT19937; each shuffle starts with original ciphertext',
                      best_matches=best, exceedances=exceed, plus_one_conditional_tail=(exceed + 1) / 200,
                      model_evaluations=1200, elapsed_seconds=time.monotonic() - started,
                      file_sha256=inputs_hashes(names),
                      interpretation='All outputs are deterministic fixed-model results. Regeneration alone is an invertibility control; only all24 known letters qualify as a crib fit. Null maximum covers these six correlated models only; exploratory, resolution1/200, no intent or solution inference.')
        snapshot.write('ASYMMETRIC-PRIMER-001.json', json_bytes(result))
        snapshot.manifest['jobs'][-1]['status'] = 'completed'
        def final_check():
            if time.monotonic() > deadline:
                raise TimeoutError('budget exceeded during publication')
        snapshot.final_check = final_check
    print(json.dumps(dict(run_id=snapshot.run_id, best_matches=best,
                          candidates=sum(r['all24_match'] for r in observed),
                          per_model_matches=[r['matched_crib_letters'] for r in observed],
                          exceedances=exceed, plus_one_conditional_tail=(exceed + 1) / 200,
                          controls=passed, elapsed_seconds=result['elapsed_seconds']), indent=2))


if __name__ == '__main__':
    main()
