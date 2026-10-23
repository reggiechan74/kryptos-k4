"""Three frozen K3/clock-route periodic-key families with exact prior skips."""
from collections import Counter
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import random
from continuation_io import ROOT, registered_run, deadline_check
from bounded_models import routes as previous_routes
from ciphers import k3_permutation
from route_key_graph import solve_graph

SPEC = 'research/specifications/K3-CLOCK-ROUTES-001.json'
A = 'KRYPTOSABCDEFGHIJLMNQUVWXZ'
SEED = 20261028


def inverse_permutation(pi):
    if sorted(pi) != list(range(len(pi))):
        raise ValueError('complete position permutation required')
    inverse = [None] * len(pi)
    for j, i in enumerate(pi):
        inverse[i] = j
    return inverse


def up_order(length, width):
    return [r * width + c for c in range(width)
            for r in reversed(range((length + width - 1) // width)) if r * width + c < length]


def composite_route(length):
    first, second = up_order(length, 42), up_order(length, 14)
    return [first[i] for i in second]


def matrix_up(values, width):
    matrix = [list(values[i:i + width]) for i in range(0, len(values), width)]
    return [row[c] for c in range(width) for row in reversed(matrix) if c < len(row)]


def canonical(labels):
    classes = {}
    return tuple(classes.setdefault(value, len(classes)) for value in labels)


def signature(pi, period, order):
    labels = [i % period for i in pi] if order == 'sub_then_route' else [j % period for j in range(len(pi))]
    return tuple(pi), canonical(labels)


def clock_catalogue():
    result = []
    for start, direction, descending in itertools.product(range(24), (1, -1), (False, True)):
        columns = [(start + direction * q) % 24 for q in range(24)]
        row_order = range(4, -1, -1) if descending else range(5)
        pi = [24 * r + c for c in columns for r in row_order if 24 * r + c < 97]
        inverse_permutation(pi)
        result.append(dict(route_id='CLOCK-%03d' % len(result), start=start, direction=direction,
                           descending_rows=descending, permutation=pi))
    return result


def preflight():
    controls = json.loads((ROOT / 'data/controls.json').read_text())
    f = controls['k3']
    pi336 = composite_route(336)
    assert ''.join(f['plaintext'][i] for i in pi336) == f['ciphertext']
    assert pi336 == k3_permutation()
    assert matrix_up(matrix_up(list(range(336)), 42), 14) == pi336
    assert ''.join(f['ciphertext'][j] for j in inverse_permutation(pi336)) == f['plaintext']
    previous = json.loads(gzip.decompress((ROOT / 'results/ROUTE-001.json.gz').read_bytes()))
    assert previous['route_catalogue'] == previous_routes(), 'saved route catalogue drift'
    old = {}
    for route in previous['route_catalogue']:
        for period, order in itertools.product((8, 10), ('sub_then_route', 'route_then_sub')):
            survivors = [r for r in previous['survivors'] if r['route'] == route['id'] and r['period'] == period
                         and r['alphabet'] == 'KRYPTOS' and r['equation'] == 'plus'
                         and r['order'] == ('identity' if route['permutation'] == list(range(97)) else order)]
            old.setdefault(signature(route['permutation'], period, order), []).append(
                dict(route_id=route['id'], period=period, order=order,
                     previous_compatible=bool(survivors), previous_result='results/ROUTE-001.json.gz'))
    composite = dict(route_id='K3-COMPOSITE-97', permutation=composite_route(97))
    clocks = clock_catalogue()
    assert len({tuple(r['permutation']) for r in clocks}) == 96
    cases, seen = [], {}
    for family, route_list in (('F1', [composite]), ('F3', clocks)):
        for route in route_list:
            for period, order in itertools.product((8, 10), ('sub_then_route', 'route_then_sub')):
                sig = signature(route['permutation'], period, order)
                case_id = family + '-%03d' % sum(c['family'] == family for c in cases)
                record = dict(family=family, case_id=case_id, route_id=route['route_id'], period=period, order=order,
                              key_phase_partition=list(sig[1]))
                if sig in old:
                    record.update(status='skipped_prior_exact_equivalent', prior_equivalents=old[sig])
                    assert not any(r['previous_compatible'] for r in old[sig]), 'unexpected prior fit'
                elif sig in seen:
                    record.update(status='skipped_new_exact_equivalent', canonical_case_id=seen[sig])
                else:
                    seen[sig] = case_id
                    record['status'] = 'new_to_test'
                cases.append(record)
    assert sum(c['family'] == 'F1' and c['status'] == 'new_to_test' for c in cases) == 4
    assert sum(c['family'] == 'F3' and c['status'] == 'new_to_test' for c in cases) == 368
    assert sum(c['status'] == 'skipped_prior_exact_equivalent' for c in cases) == 16
    return dict(k3_all336_known_answer=True, k3_existing_position_permutation=True,
                independent_matrix_oracle=True, previous_catalogue_size=66,
                previous_result_sha256=hashlib.sha256((ROOT / 'results/ROUTE-001.json.gz').read_bytes()).hexdigest(),
                routes=[composite] + clocks, formal_single_cases=cases,
                skipped_prior_exact=16, new_single_cases=372)


def known_positions(data):
    return {c['start'] - 1 + j: p for c in data['cribs'] for j, p in enumerate(c['plaintext'])}


def single_transform(text, key, pi, order, decrypt=False):
    n = len(text)
    if decrypt:
        if order == 'sub_then_route':
            moved = ''.join(text[j] for j in inverse_permutation(pi))
            return ''.join(A[(A.index(p) - key[i % len(key)]) % 26] for i, p in enumerate(moved))
        shifted = ''.join(A[(A.index(c) - key[j % len(key)]) % 26] for j, c in enumerate(text))
        return ''.join(shifted[j] for j in inverse_permutation(pi))
    if order == 'sub_then_route':
        shifted = ''.join(A[(A.index(p) + key[i % len(key)]) % 26] for i, p in enumerate(text))
        return ''.join(shifted[i] for i in pi)
    return ''.join(A[(A.index(text[i]) + key[j % len(key)]) % 26] for j, i in enumerate(pi))


def analyze_single(cipher, known, pi, period, order):
    inverse = inverse_permutation(pi)
    requirements, groups, train, first = [], {}, {}, None
    for i, plain in sorted(known.items()):
        j = inverse[i]
        phase = (i if order == 'sub_then_route' else j) % period
        value = (A.index(cipher[j]) - A.index(plain)) % 26
        req = dict(plain_position_one_based=i + 1, cipher_position_one_based=j + 1, phase=phase, key_value=value)
        if phase in groups and groups[phase][0]['key_value'] != value and first is None:
            first = dict(phase=phase, conflicting_requirements=[groups[phase][0], req])
        groups.setdefault(phase, []).append(req)
        requirements.append(req)
        if 21 <= i < 34:
            train.setdefault(phase, []).append(req)
    train_ok = all(len({r['key_value'] for r in values}) == 1 for values in train.values())
    heldout = []
    for req in requirements:
        if 64 <= req['plain_position_one_based'] <= 74:
            phase = req['phase']
            predictable = train_ok and phase in train
            predicted = A[(A.index(cipher[req['cipher_position_one_based'] - 1]) - train[phase][0]['key_value']) % 26] if predictable else None
            heldout.append(dict(plain_position_one_based=req['plain_position_one_based'],
                                predictable_from_frozen_training=predictable, predicted=predicted,
                                matches=predicted == known[req['plain_position_one_based'] - 1] if predictable else None))
    free = period - len(groups)
    record = dict(compatible=first is None, primer_parameters=period, occupied_slots=len(groups), free_slots=free,
                  independent_equality_checks=len(known) - len(groups), requirements=requirements,
                  first_conflict=first, exact_key_assignments=0 if first else 26 ** free,
                  training_compatible=train_ok, training_occupied_slots=len(train),
                  training_free_slots=period - len(train), training_equality_checks=13 - len(train),
                  heldout=heldout, best_modal_agreements=sum(max(Counter(r['key_value'] for r in rows).values()) for rows in groups.values()))
    if first is None and free == 0:
        key = [groups[j][0]['key_value'] for j in range(period)]
        plain = single_transform(cipher, key, pi, order, True)
        assert all(plain[i] == p for i, p in known.items())
        assert single_transform(plain, key, pi, order) == cipher
        record.update(key=key, plaintext=plain, full97_regeneration=len(cipher) == 97, evidence_class='crib_fit_only')
    return record


def sandwich_transform(text, a, b, pi, decrypt=False):
    if decrypt:
        moved = ''.join(A[(A.index(c) - b[j % len(b)]) % 26] for j, c in enumerate(text))
        reordered = ''.join(moved[j] for j in inverse_permutation(pi))
        return ''.join(A[(A.index(p) - a[i % len(a)]) % 26] for i, p in enumerate(reordered))
    moved = ''.join(A[(A.index(p) + a[i % len(a)]) % 26] for i, p in enumerate(text))
    return ''.join(A[(A.index(moved[i]) + b[j % len(b)]) % 26] for j, i in enumerate(pi))


def sandwich_edges(cipher, known, pi, m, n):
    inverse = inverse_permutation(pi)
    return [dict(u=i % m, v=m + inverse[i] % n, delta=(A.index(cipher[inverse[i]]) - A.index(p)) % 26,
                 plain_position_one_based=i + 1, cipher_position_one_based=inverse[i] + 1)
            for i, p in sorted(known.items())]


def analyze_sandwich(cipher, known, pi, m, n):
    edges = sandwich_edges(cipher, known, pi, m, n)
    train_edges = [e for e in edges if 22 <= e['plain_position_one_based'] <= 34]
    heldout_edges = [e for e in edges if 64 <= e['plain_position_one_based'] <= 74]
    all_graph = solve_graph(m + n, edges)
    training = solve_graph(m + n, train_edges)
    full_edges = [dict(u=i % m, v=m + j % n, delta=0) for j, i in enumerate(pi)]
    full = solve_graph(m + n, full_edges)
    c_train, c_all, d = (g['component_count'] for g in (training, all_graph, full))
    predictions = []
    for edge in heldout_edges:
        connected = training['component_labels'][edge['u']] == training['component_labels'][edge['v']]
        predictable = training['compatible'] and connected
        delta = (training['representative_potentials'][edge['u']] - training['representative_potentials'][edge['v']]) % 26 if predictable else None
        predictions.append(dict(plain_position_one_based=edge['plain_position_one_based'],
                                endpoints_connected_in_training=connected, predictable_from_frozen_training=predictable,
                                predicted_delta=delta, matches=delta == edge['delta'] if predictable else None))
    compatible = all_graph['compatible']
    record = dict(period_pair=[m, n], key_vertices=m + n, edges=edges, training_edges=train_edges,
                  all_crib_graph=all_graph, training_graph=training, full_graph_component_count=d,
                  c_train=c_train, c_all24=c_all, d_full=d,
                  training_plaintext_relevant_offsets=c_train - d,
                  remaining_plaintext_relevant_offsets=c_all - d,
                  heldout=predictions, joint_independent_heldout_checks=len(heldout_edges) - (c_train - c_all),
                  compatible=compatible, exact_key_assignments=all_graph['exact_key_assignments'],
                  distinct_compatible_plaintexts=26 ** (c_all - d) if compatible else 0,
                  forced_plaintext_positions=[])
    if compatible:
        potential, component = all_graph['representative_potentials'], all_graph['component_labels']
        for j, i in enumerate(pi):
            u, v = i % m, m + j % n
            if component[u] == component[v]:
                delta = (potential[u] - potential[v]) % 26
                record['forced_plaintext_positions'].append(dict(position_one_based=i + 1, plaintext=A[(A.index(cipher[j]) - delta) % 26]))
        if c_all == d:
            a = potential[:m]
            b = [(-x) % 26 for x in potential[m:]]
            plain = sandwich_transform(cipher, a, b, pi, True)
            assert all(plain[i] == p for i, p in known.items())
            assert sandwich_transform(plain, a, b, pi) == cipher
            record.update(plaintext=plain, representative_gauge_keys=dict(a=a, b=b), full97_regeneration=len(cipher) == 97,
                          evidence_class='unique_under_model_crib_fit_only')
    return record


def controls(pre):
    rng = random.Random(SEED)
    counts = dict(single_planted_roundtrips=0, single_mutated_rejections=0,
                  sandwich_planted_roundtrips=0, sandwich_mutated_cycle_rejections=0,
                  exhaustive_graph_cases=0, toy_key_assignments=0, explicit_graph_controls=0)
    route_lookup = {r['route_id']: r['permutation'] for r in pre['routes']}
    known_indices = list(range(21, 34)) + list(range(63, 74))
    for case in pre['formal_single_cases']:
        if case['status'] != 'new_to_test':
            continue
        pi, m = route_lookup[case['route_id']], case['period']
        plain = list(''.join(rng.choice(A) for _ in range(97)))
        plain[21:34], plain[63:74] = 'EASTNORTHEAST', 'BERLINCLOCK'
        plain = ''.join(plain)
        key = [rng.randrange(26) for _ in range(m)]
        cipher = single_transform(plain, key, pi, case['order'])
        assert single_transform(cipher, key, pi, case['order'], True) == plain
        known = {i: plain[i] for i in known_indices}
        r = analyze_single(cipher, known, pi, m, case['order'])
        assert r['compatible']
        assert all(x['matches'] is True for x in r['heldout'] if x['predictable_from_frozen_training'])
        counts['single_planted_roundtrips'] += 1
        seen = set()
        for req in r['requirements']:
            if req['phase'] in seen:
                changed = dict(known)
                i = req['plain_position_one_based'] - 1
                changed[i] = A[(A.index(changed[i]) + 1) % 26]
                assert not analyze_single(cipher, changed, pi, m, case['order'])['compatible']
                counts['single_mutated_rejections'] += 1
                break
            seen.add(req['phase'])
    pi = route_lookup['K3-COMPOSITE-97']
    for m, n in ((8, 10), (10, 8)):
        a, b = [rng.randrange(26) for _ in range(m)], [rng.randrange(26) for _ in range(n)]
        plain = ''.join(rng.choice(A) for _ in range(97))
        cipher = sandwich_transform(plain, a, b, pi)
        assert sandwich_transform(cipher, a, b, pi, True) == plain
        known = {i: plain[i] for i in known_indices}
        r = analyze_sandwich(cipher, known, pi, m, n)
        assert r['compatible']
        assert all(x['matches'] for x in r['heldout'] if x['predictable_from_frozen_training'])
        counts['sandwich_planted_roundtrips'] += 1
        non_tree = next(i for i in range(24) if i not in r['all_crib_graph']['tree_edge_indices'])
        changed = dict(known)
        index = r['edges'][non_tree]['plain_position_one_based'] - 1
        changed[index] = A[(A.index(changed[index]) + 1) % 26]
        assert not analyze_sandwich(cipher, changed, pi, m, n)['compatible']
        counts['sandwich_mutated_cycle_rejections'] += 1
    # Independent complete toy assignment enumeration verifies gauges, isolated
    # vertices and distinct full-edge images, without relying on graph potentials.
    toy_pi, m, n, base = [5, 2, 4, 1, 3, 0], 3, 2, 3
    full_edges = [(i % m, m + j % n) for j, i in enumerate(toy_pi)]
    full_d = solve_graph(m + n, [dict(u=u, v=v, delta=0) for u, v in full_edges], base)['component_count']
    truth = [0, 1, 2, 2, 1]
    deltas = [(truth[u] + truth[v]) % base for u, v in full_edges]
    for selected in ([], [0], [0, 1], [0, 1, 2, 3], list(range(6))):
        edges = [dict(u=full_edges[k][0], v=full_edges[k][1], delta=deltas[k]) for k in selected]
        solved = solve_graph(m + n, edges, base)
        accepted, images = 0, set()
        for values in itertools.product(range(base), repeat=m + n):
            counts['toy_key_assignments'] += 1
            if all((values[e['u']] + values[e['v']]) % base == e['delta'] for e in edges):
                accepted += 1
                images.add(tuple((values[u] + values[v]) % base for u, v in full_edges))
        assert accepted == solved['exact_key_assignments']
        assert len(images) == base ** (solved['component_count'] - full_d)
        counts['exhaustive_graph_cases'] += 1
    assert solve_graph(4, [dict(u=0, v=2, delta=1)])['component_count'] == 3
    counts['explicit_graph_controls'] += 1
    assert not solve_graph(4, [dict(u=0, v=2, delta=1), dict(u=0, v=2, delta=2)])['compatible']
    counts['explicit_graph_controls'] += 1
    g = solve_graph(4, [dict(u=0, v=2, delta=1), dict(u=1, v=3, delta=2)])
    assert g['component_labels'][0] != g['component_labels'][3]
    joined = solve_graph(4, [dict(u=0, v=2, delta=1), dict(u=1, v=3, delta=2), dict(u=0, v=3, delta=7)])
    assert joined['compatible'] and joined['component_count'] == 1
    counts['explicit_graph_controls'] += 1
    # A global a+=q, b-=q gauge leaves every encrypted character unchanged.
    p = 'A' * 97
    assert sandwich_transform(p, [1] * 8, [2] * 10, pi) == sandwich_transform(p, [5] * 8, [24] * 10, pi)
    counts['explicit_graph_controls'] += 1
    return counts


def scan_single(cipher, known, pre, family, deadline, retain=True):
    lookup = {r['route_id']: r['permutation'] for r in pre['routes']}
    records, summary = [], dict(new_models=0, compatible=0, training_survivors=0, max_modal_agreements=0)
    for case in pre['formal_single_cases']:
        if case['family'] != family or case['status'] != 'new_to_test':
            continue
        deadline_check(deadline)
        r = analyze_single(cipher, known, lookup[case['route_id']], case['period'], case['order'])
        r.update(case)
        summary['new_models'] += 1
        summary['compatible'] += r['compatible']
        summary['training_survivors'] += r['training_compatible']
        summary['max_modal_agreements'] = max(summary['max_modal_agreements'], r['best_modal_agreements'])
        if retain:
            records.append(r)
    return summary, records


def run(data, deadline):
    pre = preflight()
    passed = controls(pre)
    known = known_positions(data)
    families, records = {}, {}
    for family in ('F1', 'F3'):
        families[family], records[family] = scan_single(data['ciphertext'], known, pre, family, deadline)
    pi = pre['routes'][0]['permutation']
    records['F2'] = []
    for m, n in ((8, 10), (10, 8)):
        deadline_check(deadline)
        records['F2'].append(analyze_sandwich(data['ciphertext'], known, pi, m, n))
    families['F2'] = dict(new_models=2, compatible=sum(r['compatible'] for r in records['F2']),
                          training_survivors=sum(r['training_graph']['compatible'] for r in records['F2']))
    # Nulls are conditional on compatibility, never run for wholly contradicted
    # families. Refit the complete applicable model family in every draw.
    nulls = {}
    for family in ('F1', 'F2', 'F3'):
        if families[family]['compatible'] == 0:
            nulls[family] = dict(status='not_needed_all_models_contradicted', draws=[])
            continue
        rng, draws = random.Random(20261029), []
        for _ in range(199):
            deadline_check(deadline)
            shuffled = list(data['ciphertext'])
            rng.shuffle(shuffled)
            shuffled = ''.join(shuffled)
            if family in ('F1', 'F3'):
                summary, _ = scan_single(shuffled, known, pre, family, deadline, False)
                draws.append(summary['max_modal_agreements'])
            else:
                draws.append(sum(analyze_sandwich(shuffled, known, pi, m, n)['compatible'] for m, n in ((8, 10), (10, 8))))
        observed = families[family]['max_modal_agreements'] if family in ('F1', 'F3') else families[family]['compatible']
        exceed = sum(value >= observed for value in draws)
        nulls[family] = dict(status='completed', seed=20261029, draws=draws, exceedances=exceed, plus_one_conditional_tail=(exceed + 1) / 200)
    return dict(preflight=pre, controls=passed, families=families, records=records, nulls=nulls,
                actual_new_models=374, raw_structures=390, skipped_prior_exact=16,
                interpretation='Exact bounded route/key constraints, not a solution. Fitting spends parameters; Berlin public before design. Graph gauge representatives describe only within-component differences. No null simulation needed for entirely contradicted families. No added scope.')


if __name__ == '__main__':
    runid, result = registered_run('K3-CLOCK-ROUTES-001', SPEC, 'experiments/k3_clock_routes.py',
                                 ['experiments/route_key_graph.py', 'tests/test_k3_clock_routes.py',
                                  'tests/test_route_key_graph.py', 'results/ROUTE-001.json.gz', 'research/BOUNDED-SPEC.md'], 30, run)
    print(json.dumps(dict(run_id=runid, families=result['families'], controls=result['controls'],
                          skipped_prior_exact=result['skipped_prior_exact'],
                          null_status={k: v['status'] for k, v in result['nulls'].items()},
                          elapsed_seconds=result['elapsed_seconds']), indent=2))
