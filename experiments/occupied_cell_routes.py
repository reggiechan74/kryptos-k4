"""Fixed carved-text mask, eight routes and eighteen literal phased keys."""
from collections import Counter
import gzip
import itertools
import json
import random
from continuation_io import ROOT, registered_run, deadline_check
from ciphers import vigenere, permute

SPEC = 'research/specifications/OCCUPIED-CELL-ROUTES-001.json'
A = 'KRYPTOSABCDEFGHIJLMNQUVWXZ'
KEYS = ('PALIMPSEST', 'ABSCISSA')
SEED = 20261030
PRIOR = 'results/k3-clock-routes-001-runs/20261022T193238Z-99bf9337176c469e9d7742f2a21f2aca/K3-CLOCK-ROUTES-001.json'


def mask():
    return [(0, c) for c in range(27, 31)] + [(r, c) for r in range(1, 4) for c in range(31)]


def inverse_permutation(pi):
    if sorted(pi) != list(range(len(pi))):
        raise ValueError('complete position permutation required')
    inverse = [None] * len(pi)
    for j, i in enumerate(pi):
        inverse[i] = j
    return inverse


def route_catalogue():
    lookup, result, seen = {cell: i for i, cell in enumerate(mask())}, [], {}
    for horizontal, vertical, inverse in itertools.product((1, -1), (1, -1), (False, True)):
        columns = range(31) if horizontal == 1 else range(30, -1, -1)
        rows = range(4) if vertical == 1 else range(3, -1, -1)
        pi = [lookup[r, c] for c in columns for r in rows if (r, c) in lookup]
        if inverse:
            pi = inverse_permutation(pi)
        route_id = 'OCC-%02d' % len(result)
        canonical = seen.setdefault(tuple(pi), route_id)
        result.append(dict(route_id=route_id, canonical_route_id=canonical, horizontal=horizontal,
                           vertical=vertical, inverse=inverse, permutation=pi))
    return result


def cell_oracle(values, horizontal, vertical, inverse=False):
    matrix = [[None] * 31 for _ in range(4)]
    occupied = {(0, c) for c in range(27, 31)} | {(r, c) for r in range(1, 4) for c in range(31)}
    natural = [(r, c) for r in range(4) for c in range(31) if (r, c) in occupied]
    columnwise = [(r, c) for c in (range(31) if horizontal == 1 else range(30, -1, -1))
                  for r in (range(4) if vertical == 1 else range(3, -1, -1)) if (r, c) in occupied]
    fill, read = (columnwise, natural) if inverse else (natural, columnwise)
    for (r, c), value in zip(fill, values):
        matrix[r][c] = value
    return [matrix[r][c] for r, c in read]


def canonical(labels):
    seen = {}
    return tuple(seen.setdefault(x, len(seen)) for x in labels)


def model_signature(pi, period, order):
    phase = [i % period for i in pi] if order == 'sub_then_route' else [j % period for j in range(97)]
    return tuple(pi), canonical(phase)


def phased_key(word, phase):
    return word[phase:] + word[:phase]


def transform(text, route, word, phase, order, decrypt=False):
    key = phased_key(word, phase)
    if decrypt:
        if order == 'sub_then_route':
            return vigenere(permute(text, route, inverse=True), key, A, decrypt=True)
        return permute(vigenere(text, key, A, decrypt=True), route, inverse=True)
    if order == 'sub_then_route':
        return permute(vigenere(text, key, A), route)
    return vigenere(permute(text, route), key, A)


def explicit_encode(plain, pi, word, phase, order):
    return ''.join(A[(A.index(plain[i]) + A.index(word[((i if order == 'sub_then_route' else j) + phase) % len(word)])) % 26]
                   for j, i in enumerate(pi))


def preflight():
    data = json.loads((ROOT / 'data/k4.json').read_text())
    rows = json.loads((ROOT / 'data/controls.json').read_text())['transcription_panels']['lower_rows']
    start = next(i for i, row in enumerate(rows) if row.endswith('OBKR'))
    assert len(rows[start]) == 31 and rows[start][27:31] == 'OBKR'
    assert [len(row) for row in rows[start + 1:]] == [31, 31, 31]
    assert rows[start][27:31] + ''.join(rows[start + 1:]) == data['ciphertext']
    prior = json.loads(gzip.decompress((ROOT / 'results/ROUTE-001.json.gz').read_bytes()))
    newer = json.loads((ROOT / PRIOR).read_text())
    prior_models = {}
    for route in prior['route_catalogue']:
        for period, order in itertools.product((8, 10), ('sub_then_route', 'route_then_sub')):
            covered = not any(x['route'] == route['id'] and x['period'] == period and x['alphabet'] == 'KRYPTOS'
                              and x['equation'] == 'plus' and x['order'] == order for x in prior['survivors'])
            if covered:
                prior_models.setdefault(model_signature(route['permutation'], period, order), []).append(
                    dict(result='results/ROUTE-001.json.gz', route_id=route['id'], period=period,
                         order=order, alphabet=A, equation='plus', key_domain='all26^period periodic keys'))
    newer_routes = {r['route_id']: r['permutation'] for r in newer['preflight']['routes']}
    for family in ('F1', 'F3'):
        for record in newer['records'][family]:
            if not record['compatible']:
                pi = newer_routes[record['route_id']]
                prior_models.setdefault(model_signature(pi, record['period'], record['order']), []).append(
                    dict(result=PRIOR, case_id=record['case_id'], route_id=record['route_id'], period=record['period'],
                         order=record['order'], alphabet=A, equation='plus', key_domain='all26^period periodic keys'))
    catalogue, cases, seen = route_catalogue(), [], {}
    for route in catalogue:
        for word in KEYS:
            for phase, order in itertools.product(range(len(word)), ('sub_then_route', 'route_then_sub')):
                case_id = 'OCC-K-%03d' % len(cases)
                pi = route['permutation']
                shifts = tuple(A.index(word[((i if order == 'sub_then_route' else j) + phase) % len(word)])
                               for j, i in enumerate(pi))
                exact_signature = (tuple(pi), shifts)
                covered = prior_models.get(model_signature(pi, len(word), order), [])
                case = dict(case_id=case_id, route_id=route['route_id'], word=word, phase=phase, order=order,
                            prior_equivalents=covered)
                if covered:
                    case['status'] = 'skipped_prior_stronger_periodic_model'
                elif exact_signature in seen:
                    case.update(status='skipped_new_exact_equivalent', canonical_case_id=seen[exact_signature])
                else:
                    case['status'] = 'new_to_test'
                    seen[exact_signature] = case_id
                cases.append(case)
    assert len(catalogue) == 8 and len({tuple(r['permutation']) for r in catalogue}) == 8
    assert len(cases) == 288 and sum(c['status'] == 'new_to_test' for c in cases) == 288
    return dict(fixture_mask_verified=True, first_row_one_based_columns=[28, 31], remaining_row_lengths=[31, 31, 31],
                occupied_cells_zero_based=mask(), routes=catalogue, cases=cases,
                raw_routes=8, distinct_routes=8, prior_stronger_skips=0, exact_unique_new_cases=288,
                prior_route_catalogues=dict(original=66, newer=len(newer_routes)),
                coverage_scope='Exact route, period, alphabet, addition equation, both layer orders and unrestricted periodic-key domain checked before scoring.')


def known_positions(data):
    return {c['start'] - 1 + j: p for c in data['cribs'] for j, p in enumerate(c['plaintext'])}


def assess(cipher, known, case, pi):
    plain = transform(cipher, pi, case['word'], case['phase'], case['order'], True)
    assert transform(plain, pi, case['word'], case['phase'], case['order']) == cipher
    matched = [i + 1 for i, p in sorted(known.items()) if plain[i] == p]
    return dict(case, plaintext=plain, matched_positions_one_based=matched, matched_crib_letters=len(matched),
                east_matches=sum(22 <= i <= 34 for i in matched), berlin_matches=sum(64 <= i <= 74 for i in matched),
                all24_match=len(matched) == 24, full97_regeneration=len(cipher) == 97, fitted_parameters=0,
                evidence_class='crib_fit_only' if len(matched) == 24 else 'rejected_model_output')


def controls(pre):
    counts = dict(route_unique_index_oracles=0, single_symbol_roundtrips=0,
                  planted_full_recoveries=0, planted_crib_recoveries=0,
                  explicit_encoder_comparisons=0, altered_crib_rejections=0)
    rng = random.Random(SEED)
    for p in A:
        for k in A:
            cipher = vigenere(p, k, A)
            assert vigenere(cipher, k, A, True) == p
            counts['single_symbol_roundtrips'] += 1
    lookup = {r['route_id']: r for r in pre['routes']}
    for route in pre['routes']:
        labels = list(range(97))
        assert cell_oracle(labels, route['horizontal'], route['vertical'], route['inverse']) == route['permutation']
        restored = cell_oracle(route['permutation'], route['horizontal'], route['vertical'], not route['inverse'])
        assert restored == labels
        counts['route_unique_index_oracles'] += 1
    for case in pre['cases']:
        if case['status'] != 'new_to_test':
            continue
        pi = lookup[case['route_id']]['permutation']
        plain = list(''.join(rng.choice(A) for _ in range(97)))
        plain[21:34], plain[63:74] = 'EASTNORTHEAST', 'BERLINCLOCK'
        plain = ''.join(plain)
        known = {i: plain[i] for i in list(range(21, 34)) + list(range(63, 74))}
        cipher = transform(plain, pi, case['word'], case['phase'], case['order'])
        assert explicit_encode(plain, pi, case['word'], case['phase'], case['order']) == cipher
        counts['explicit_encoder_comparisons'] += 1
        assert transform(cipher, pi, case['word'], case['phase'], case['order'], True) == plain
        counts['planted_full_recoveries'] += 1
        assert assess(cipher, known, case, pi)['all24_match']
        counts['planted_crib_recoveries'] += 1
        changed = dict(known)
        changed[21] = A[(A.index(changed[21]) + 1) % 26]
        assert not assess(cipher, changed, case, pi)['all24_match']
        counts['altered_crib_rejections'] += 1
    return counts


def scan(cipher, known, pre, deadline, retain=True):
    routes = {r['route_id']: r['permutation'] for r in pre['routes']}
    records, scores = [], []
    for case in pre['cases']:
        if case['status'] != 'new_to_test':
            continue
        deadline_check(deadline)
        r = assess(cipher, known, case, routes[case['route_id']])
        scores.append(r['matched_crib_letters'])
        if retain:
            records.append(r)
    return dict(models=len(scores), compatible=sum(x == 24 for x in scores), max_matches=max(scores), per_model_matches=scores), records


def run(data, deadline):
    pre = preflight()
    passed = controls(pre)
    known = known_positions(data)
    observed, records = scan(data['ciphertext'], known, pre, deadline)
    nulls = dict(status='not_needed_all_fixed_models_contradicted', draws=[])
    if observed['compatible']:
        rng, draws = random.Random(20261031), []
        for _ in range(199):
            shuffled = list(data['ciphertext'])
            rng.shuffle(shuffled)
            summary, _ = scan(''.join(shuffled), known, pre, deadline, False)
            draws.append(summary['max_matches'])
        exceed = sum(score >= observed['max_matches'] for score in draws)
        nulls = dict(status='completed', draws=draws, seed=20261031, exceedances=exceed, plus_one_conditional_tail=(exceed + 1) / 200)
    return dict(preflight=pre, controls=passed, observed=observed, records=records, nulls=nulls,
                actual_model_evaluations=288, control_seed=SEED,
                interpretation='Carved textual occupancy only, not surveyed geometry. Eighteen phased literal keys enumerated; no fitting. Re-encryption tests invertibility only. No null simulation if all24crib gate fails for every branch. Rejected outputs are not decoded plaintext.')


if __name__ == '__main__':
    runid, result = registered_run('OCCUPIED-CELL-ROUTES-001', SPEC, 'experiments/occupied_cell_routes.py',
                                 ['tests/test_occupied_cell_routes.py', 'results/ROUTE-001.json.gz', PRIOR,
                                  'research/BOUNDED-SPEC.md'], 15, run)
    print(json.dumps(dict(run_id=runid, models=result['observed']['models'], compatible=result['observed']['compatible'],
                          max_matches=result['observed']['max_matches'], controls=result['controls'],
                          null_status=result['nulls']['status'], elapsed_seconds=result['elapsed_seconds']), indent=2))
