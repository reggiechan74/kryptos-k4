"""Exact arbitrary-primer audit of 72 frozen mixed-alphabet PT-feedback cases."""
from collections import Counter
import itertools
import json
import random
from continuation_io import registered_run, deadline_check
from autokey_constraints import analyze as shared_analyze

SPEC = 'research/specifications/ASYMMETRIC-FEEDBACK-001.json'
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
KR = 'KRYPTOSABCDEFGHIJLMNQUVWXZ'
COEFFICIENTS = {'plus': (1, 1), 'minus': (1, -1), 'beaufort': (-1, 1)}
SEED = 20261023


def configurations():
    for roles in itertools.product((AZ, KR), repeat=3):
        if len(set(roles)) == 1:
            continue
        for equation in COEFFICIENTS:
            for lag in range(9, 13):
                yield dict(Ap=roles[0], Ac=roles[1], Ak=roles[2], equation=equation, lag=lag)


def validate(cipher, known, cfg):
    ap, ac, ak = (cfg[k] for k in ('Ap', 'Ac', 'Ak'))
    if len(ap) < 2 or any(len(a) != len(ap) or len(set(a)) != len(ap) or set(a) != set(ap) for a in (ap, ac, ak)):
        raise ValueError('role alphabets must permute the same distinct symbol set')
    if not cipher or any(c not in ac for c in cipher) or not 1 <= cfg['lag'] <= len(cipher):
        raise ValueError('invalid ciphertext or lag')
    if cfg['equation'] not in COEFFICIENTS or any(type(i) is not int or not 0 <= i < len(cipher) or p not in ap or len(p) != 1 for i, p in known.items()):
        raise ValueError('invalid equation or literal known map')


def transform(text, primer, cfg, decrypt=False):
    validate(text, {}, cfg)
    if len(primer) != cfg['lag'] or any(c not in cfg['Ak'] for c in primer):
        raise ValueError('complete literal primer of specified lag required')
    ap, ac, ak = (cfg[k] for k in ('Ap', 'Ac', 'Ak'))
    sigma, tau = COEFFICIENTS[cfg['equation']]
    m, out = len(ap), []
    for i, value in enumerate(text):
        key = primer[i] if i < len(primer) else (out[i - len(primer)] if decrypt else text[i - len(primer)])
        if decrypt:
            out.append(ap[sigma * (ac.index(value) - tau * ak.index(key)) % m])
        else:
            out.append(ac[(sigma * ap.index(value) + tau * ak.index(key)) % m])
    return ''.join(out)


def root_requirements(cipher, known, cfg):
    validate(cipher, known, cfg)
    ap, ac, ak = (cfg[k] for k in ('Ap', 'Ac', 'Ak'))
    pi, ci = ({c: i for i, c in enumerate(a)} for a in (ap, ac))
    sigma, tau = COEFFICIENTS[cfg['equation']]
    lag, m = cfg['lag'], len(ap)
    requirements = []
    for i, p in sorted(known.items()):
        value = pi[p]
        j = i
        while j >= lag:
            # Invert the symbol-to-symbol transition, reindexing the key symbol.
            value = pi[ak[tau * (ci[cipher[j]] - sigma * value) % m]]
            j -= lag
        requirements.append(dict(position_one_based=i + 1, lane=j, required_root=value,
                                 root_to_known_positions_one_based=list(range(j + 1, i + 2, lag))))
    return requirements


def decode_roots(cipher, roots, cfg):
    ap, ac, ak = (cfg[k] for k in ('Ap', 'Ac', 'Ak'))
    sigma, tau = COEFFICIENTS[cfg['equation']]
    out = [ap[roots[j]] for j in range(cfg['lag'])]
    for i in range(cfg['lag'], len(cipher)):
        out.append(ap[sigma * (ac.index(cipher[i]) - tau * ak.index(out[i - cfg['lag']])) % len(ap)])
    return ''.join(out)


def analyze(cipher, known, cfg, include_predictions=True):
    requirements = root_requirements(cipher, known, cfg)
    groups, anchors = {}, {}
    first = None
    for req in requirements:
        lane, value = req['lane'], req['required_root']
        groups.setdefault(lane, []).append(value)
        if lane in anchors and anchors[lane]['required_root'] != value and first is None:
            first = dict(known_positions_one_based=[anchors[lane]['position_one_based'], req['position_one_based']],
                         lane=lane, required_roots=[anchors[lane]['required_root'], value],
                         root_to_known_paths_one_based=[anchors[lane]['root_to_known_positions_one_based'], req['root_to_known_positions_one_based']])
        anchors.setdefault(lane, req)
    occupied = len(groups)
    free = cfg['lag'] - occupied
    compatible = first is None
    train = [v for v in requirements if 22 <= v['position_one_based'] <= 34]
    train_groups = {}
    for req in train:
        train_groups.setdefault(req['lane'], []).append(req['required_root'])
    train_ok = all(len(set(v)) == 1 for v in train_groups.values())
    record = dict(cfg, compatible=compatible,
                  classification='contradicted' if not compatible else 'compatible_fully_constrained' if free == 0 else 'compatible_but_underdetermined',
                  requirements=requirements, first_conflict=first, occupied_lanes=occupied, free_lanes=free,
                  primer_parameters_before_constraints=cfg['lag'], independent_equality_checks=len(known) - occupied,
                  exact_solution_count=0 if not compatible else len(cfg['Ap']) ** free,
                  best_same_data_agreements=sum(max(Counter(v).values()) for v in groups.values()),
                  training_compatible=train_ok, training_occupied_lanes=len(train_groups),
                  training_equality_checks=len(train) - len(train_groups), heldout=[])
    if include_predictions and train_ok and len(train_groups) == cfg['lag']:
        roots = {j: values[0] for j, values in train_groups.items()}
        predicted = decode_roots(cipher, roots, cfg)
        record['heldout'] = [dict(position_one_based=i + 1, predicted=predicted[i], matches=predicted[i] == p)
                             for i, p in sorted(known.items()) if 63 <= i < 74]
    record['candidate_gate'] = compatible and free == 0 and len(record['heldout']) == 11 and all(x['matches'] for x in record['heldout'])
    if record['candidate_gate']:
        roots = {lane: v['required_root'] for lane, v in anchors.items()}
        plain = decode_roots(cipher, roots, cfg)
        sigma, tau = COEFFICIENTS[cfg['equation']]
        ap, ac, ak = (cfg[k] for k in ('Ap', 'Ac', 'Ak'))
        primer = ''.join(ak[tau * (ac.index(cipher[i]) - sigma * ap.index(plain[i])) % len(ap)] for i in range(cfg['lag']))
        if transform(cipher, primer, cfg, True) != plain or transform(plain, primer, cfg) != cipher or any(plain[i] != p for i, p in known.items()):
            raise AssertionError('candidate failed independent sequential regeneration')
        record.update(plaintext=plain, primer=primer, full97_regeneration=len(cipher) == 97, evidence_class='crib_fit_only')
    return record


def known_positions(data):
    return {c['start'] - 1 + j: p for c in data['cribs'] for j, p in enumerate(c['plaintext'])}


def controls():
    rng = random.Random(SEED)
    counts = dict(planted_roundtrips=0, root_recoveries=0, mutated_rejections=0,
                  exhaustive_toy_cases=0, toy_primer_decryptions=0, same_alphabet_comparisons=0)
    for cfg in configurations():
        primer = ''.join(rng.choice(AZ) for _ in range(cfg['lag']))
        plain = ''.join(rng.choice(AZ) for _ in range(97))
        cipher = transform(plain, primer, cfg)
        assert transform(cipher, primer, cfg, True) == plain
        counts['planted_roundtrips'] += 1
        known = {i: plain[i] for i in list(range(21, 34)) + list(range(63, 74))}
        record = analyze(cipher, known, cfg)
        assert record['compatible'] and record['free_lanes'] == 0 and record['candidate_gate']
        assert all(r['required_root'] == cfg['Ap'].index(plain[r['lane']]) for r in record['requirements'])
        counts['root_recoveries'] += 1
        seen = set()
        for i in sorted(known):
            if i % cfg['lag'] in seen:
                changed = dict(known)
                changed[i] = AZ[(AZ.index(changed[i]) + 1) % 26]
                assert not analyze(cipher, changed, cfg)['compatible']
                counts['mutated_rejections'] += 1
                break
            seen.add(i % cfg['lag'])
    for roles in itertools.product(('ABCD', 'CADB'), repeat=3):
        if len(set(roles)) == 1:
            continue
        for equation in COEFFICIENTS:
            for lag in (1, 2):
                cfg = dict(zip(('Ap', 'Ac', 'Ak'), roles), equation=equation, lag=lag)
                cipher = 'ABCDACB'
                for known in ({}, {2: 'A'}, {0: 'C', 2: 'A', 3: 'B', 5: 'D', 6: 'C'}):
                    record = analyze(cipher, known, cfg, False)
                    matches = 0
                    best = 0
                    for primer_tuple in itertools.product('ABCD', repeat=lag):
                        plain = transform(cipher, ''.join(primer_tuple), cfg, True)
                        score = sum(plain[i] == p for i, p in known.items())
                        best = max(best, score)
                        matches += score == len(known)
                        counts['toy_primer_decryptions'] += 1
                    assert matches == record['exact_solution_count']
                    assert best == record['best_same_data_agreements']
                    counts['exhaustive_toy_cases'] += 1
    for alphabet in (AZ, KR):
        for equation in COEFFICIENTS:
            for lag in range(9, 13):
                cfg = dict(Ap=alphabet, Ac=alphabet, Ak=alphabet, equation=equation, lag=lag)
                cipher = ''.join(rng.choice(AZ) for _ in range(97))
                known = {i: rng.choice(AZ) for i in list(range(21, 34)) + list(range(63, 74))}
                old = shared_analyze(cipher, known, alphabet, equation, 'plaintext', lag)
                new = analyze(cipher, known, cfg)
                assert old['classification'] == new['classification']
                assert old['independent_consistency_checks'] == new['independent_equality_checks']
                counts['same_alphabet_comparisons'] += 1
    return counts


def scan(cipher, known, deadline, retain=False):
    records = []
    summary = dict(models=0, compatible=0, candidates=0, training_survivors=0, max_agreements=0)
    for cfg in configurations():
        deadline_check(deadline)
        record = analyze(cipher, known, cfg)
        summary['models'] += 1
        summary['compatible'] += record['compatible']
        summary['candidates'] += record['candidate_gate']
        summary['training_survivors'] += record['training_compatible']
        summary['max_agreements'] = max(summary['max_agreements'], record['best_same_data_agreements'])
        if retain:
            records.append(record)
    return summary, records


def run(data, deadline):
    passed = controls()
    known = known_positions(data)
    observed, records = scan(data['ciphertext'], known, deadline, True)
    rng = random.Random(SEED)
    nulls = []
    for _ in range(199):
        shuffled = list(data['ciphertext'])
        rng.shuffle(shuffled)
        summary, _ = scan(''.join(shuffled), known, deadline)
        nulls.append(summary)
    exceed = sum(n['max_agreements'] >= observed['max_agreements'] for n in nulls)
    return dict(controls=passed, observed=observed, records=records, nulls=nulls, seed=SEED,
                rng='random.Random MT19937, fresh original ciphertext each shuffle', model_evaluations=14400,
                exceedances=exceed, plus_one_conditional_tail=(exceed + 1) / 200,
                interpretation='Exact existential-primer constraints. First crib fits are evaluated on Berlin without refitting; both cribs public before design. Optimized-root null maximum covers72correlated configs only, exploratory and resolution1/200. No partial-fit or historical intent claim.')


if __name__ == '__main__':
    runid, result = registered_run('ASYMMETRIC-FEEDBACK-001', SPEC, 'experiments/asymmetric_feedback.py',
                                 ['tests/test_asymmetric_feedback.py', 'experiments/autokey_constraints.py'], 60, run)
    print(json.dumps(dict(run_id=runid, observed=result['observed'], controls=result['controls'],
                          exceedances=result['exceedances'], plus_one_conditional_tail=result['plus_one_conditional_tail'],
                          elapsed_seconds=result['elapsed_seconds']), indent=2))
