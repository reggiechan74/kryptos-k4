"""SPLIT-COORDINATE-001: fixed coordinate-stream permutations, no fitted keys."""
from collections import Counter
import hashlib
import itertools
import json
import random
from continuation_io import registered_run, deadline_check

SPEC = 'research/specifications/SPLIT-COORDINATE-001.json'
ALPHABETS = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'KRYPTOSABCDEFGHIJLMNQUVWXZ')
SEED = 20261027


def configurations():
    for alphabet, columns, row_width, row_inverse, column_inverse in itertools.product(ALPHABETS, (13, 2), (7, 21), (False, True), (False, True)):
        yield dict(alphabet=alphabet, grid_rows=26 // columns, grid_columns=columns,
                   row_width=row_width, column_width=21 if row_width == 7 else 7,
                   row_inverse=row_inverse, column_inverse=column_inverse)


def route_order(n, width, inverse=False):
    if n < 1 or width < 1:
        raise ValueError('positive stream size and route width required')
    order = [i for c in range(width) for i in range(c, n, width)]
    if inverse:
        reverse = [0] * n
        for i, source in enumerate(order):
            reverse[source] = i
        order = reverse
    return order


def component_orders(n, cfg, inverse=False):
    return (route_order(n, cfg['row_width'], cfg['row_inverse'] != inverse),
            route_order(n, cfg['column_width'], cfg['column_inverse'] != inverse))


def transform(text, cfg, inverse=False):
    alphabet, columns = cfg['alphabet'], cfg['grid_columns']
    if len(set(alphabet)) != 26 or set(alphabet) != set(ALPHABETS[0]) or any(c not in alphabet for c in text):
        raise ValueError('literal ASCII letters and complete fixed alphabet required')
    if cfg['grid_rows'] * columns != 26:
        raise ValueError('grid must cover all26letters')
    indices = [alphabet.index(c) for c in text]
    rows, cols = component_orders(len(text), cfg, inverse)
    return ''.join(alphabet[(indices[rows[i]] // columns) * columns + indices[cols[i]] % columns]
                   for i in range(len(text)))


def matrix_route(values, width, inverse=False):
    """Independent ragged-cell oracle using explicit row storage/scatter."""
    cells = [list(values[i:i + width]) for i in range(0, len(values), width)]
    if not inverse:
        return [row[c] for c in range(width) for row in cells if c < len(row)]
    stream = iter(values)
    for c in range(width):
        for row in cells:
            if c < len(row):
                row[c] = next(stream)
    return [v for row in cells for v in row]


def oracle(text, cfg, inverse=False):
    grid = [list(cfg['alphabet'][i:i + cfg['grid_columns']]) for i in range(0, 26, cfg['grid_columns'])]
    mapping = {c: (r, k) for r, row in enumerate(grid) for k, c in enumerate(row)}
    rows = matrix_route([mapping[c][0] for c in text], cfg['row_width'], cfg['row_inverse'] != inverse)
    columns = matrix_route([mapping[c][1] for c in text], cfg['column_width'], cfg['column_inverse'] != inverse)
    return ''.join(grid[r][c] for r, c in zip(rows, columns))


def function_signature(cfg, n=97):
    """Exact canonical truth table per output over its one/two source variables.

    Sort input positions and transpose truth table when necessary. When the two
    positions coincide only the reachable diagonal entries describe the function.
    """
    rows, columns = component_orders(n, cfg, inverse=True)
    alphabet, width = cfg['alphabet'], cfg['grid_columns']
    index = {c: i for i, c in enumerate(alphabet)}
    regular = bytes(ord(alphabet[(index[a] // width) * width + index[b] % width]) - 65
                    for a in ALPHABETS[0] for b in ALPHABETS[0])
    reversed_table = bytes(ord(alphabet[(index[b] // width) * width + index[a] % width]) - 65
                           for a in ALPHABETS[0] for b in ALPHABETS[0])
    diagonal = bytes(range(26))
    parts = []
    for row, col in zip(rows, columns):
        if row == col:
            parts.append(bytes((1, row)) + diagonal)
        else:
            parts.append(bytes((2, min(row, col), max(row, col))) + (regular if row < col else reversed_table))
    return b''.join(parts)


def catalogue():
    seen, groups, records = {}, {}, []
    for number, cfg in enumerate(configurations()):
        case_id = 'SC-%03d' % number
        signature = function_signature(cfg)
        canonical = seen.setdefault(signature, case_id)
        groups.setdefault(canonical, []).append(case_id)
        records.append(dict(cfg, case_id=case_id, canonical_case_id=canonical,
                            function_signature_sha256=hashlib.sha256(signature).hexdigest()))
    return records, groups


def known_positions(data):
    return {c['start'] - 1 + j: p for c in data['cribs'] for j, p in enumerate(c['plaintext'])}


def assess(cipher, known, cfg):
    plain = transform(cipher, cfg, inverse=True)
    if transform(plain, cfg) != cipher:
        raise AssertionError('full inverse/regeneration failure')
    matched = [i + 1 for i, p in sorted(known.items()) if plain[i] == p]
    return dict(cfg, plaintext=plain, matched_positions_one_based=matched,
                matched_crib_letters=len(matched), east_matches=sum(22 <= i <= 34 for i in matched),
                berlin_matches=sum(64 <= i <= 74 for i in matched),
                all24_match=len(matched) == 24, full97_regeneration=len(cipher) == 97,
                free_parameters=0, evidence_class='crib_fit_only' if len(matched) == 24 else 'rejected_model_output')


def controls():
    rng = random.Random(SEED)
    counts = dict(planted_roundtrips=0, planted_crib_recoveries=0, mutated_rejections=0,
                  oracle_comparisons=0, source_pair_grid_checks=0, ragged_route_checks=0,
                  equivalence_checks=0)
    for n in (1, 2, 7, 21, 26, 97):
        for width in (7, 21):
            values = list(range(n))
            for inverse in (False, True):
                order = route_order(n, width, inverse)
                assert sorted(order) == values
                assert [values[i] for i in order] == matrix_route(values, width, inverse)
                inverse_order = route_order(n, width, not inverse)
                assert [order[i] for i in inverse_order] == values
                counts['ragged_route_checks'] += 1
    for cfg in configurations():
        alphabet, width = cfg['alphabet'], cfg['grid_columns']
        for a in alphabet:
            for b in alphabet:
                row, col = alphabet.index(a) // width, alphabet.index(b) % width
                joined = alphabet[row * width + col]
                assert divmod(alphabet.index(joined), width) == (row, col)
                counts['source_pair_grid_checks'] += 1
        plain = list(''.join(rng.choice(ALPHABETS[0]) for _ in range(97)))
        plain[21:34] = 'EASTNORTHEAST'
        plain[63:74] = 'BERLINCLOCK'
        plain = ''.join(plain)
        cipher = transform(plain, cfg)
        assert oracle(plain, cfg) == cipher
        assert oracle(cipher, cfg, True) == plain
        assert transform(cipher, cfg, True) == plain
        counts['planted_roundtrips'] += 1
        counts['oracle_comparisons'] += 2
        known = {i: plain[i] for i in list(range(21, 34)) + list(range(63, 74))}
        assert assess(cipher, known, cfg)['all24_match']
        counts['planted_crib_recoveries'] += 1
        changed = dict(known)
        changed[21] = ALPHABETS[0][(ALPHABETS[0].index(changed[21]) + 1) % 26]
        assert not assess(cipher, changed, cfg)['all24_match']
        counts['mutated_rejections'] += 1
    cases = list(configurations())
    assert function_signature(cases[0]) == function_signature(dict(cases[0]))
    counts['equivalence_checks'] += 1
    changed = dict(cases[0], row_inverse=not cases[0]['row_inverse'])
    assert function_signature(cases[0]) != function_signature(changed)
    counts['equivalence_checks'] += 1
    # If both streams have the same route, all grid/alphabet choices implement
    # the same whole-letter permutation; the canonical signature must agree.
    one = dict(cases[0], column_width=7, column_inverse=False)
    other = dict(one, alphabet=ALPHABETS[1], grid_rows=13, grid_columns=2)
    assert function_signature(one) == function_signature(other)
    counts['equivalence_checks'] += 1
    return counts


def scan(cipher, known, cases, groups, deadline, retain=False):
    canonical = []
    for cfg in cases:
        if cfg['case_id'] == cfg['canonical_case_id']:
            deadline_check(deadline)
            canonical.append(assess(cipher, known, cfg))
    summary = dict(distinct_models=len(canonical), formal_models=len(cases),
                   max_matches=max(r['matched_crib_letters'] for r in canonical),
                   candidates=sum(r['all24_match'] for r in canonical),
                   per_model_matches=[r['matched_crib_letters'] for r in canonical])
    return summary, canonical if retain else []


def run(data, deadline):
    passed = controls()
    cases, groups = catalogue()
    observed, records = scan(data['ciphertext'], known_positions(data), cases, groups, deadline, True)
    rng = random.Random(SEED)
    nulls = []
    for _ in range(199):
        shuffled = list(data['ciphertext'])
        rng.shuffle(shuffled)
        summary, _ = scan(''.join(shuffled), known_positions(data), cases, groups, deadline)
        nulls.append(summary)
    exceed = sum(n['max_matches'] >= observed['max_matches'] for n in nulls)
    return dict(controls=passed, catalogue=cases, equivalence_classes=groups,
                observed=observed, records=records, nulls=nulls, seed=SEED,
                rng='random.Random MT19937; fresh original ciphertext each shuffle',
                formal_model_evaluations=6400, distinct_model_evaluations=observed['distinct_models'] * 200,
                exceedances=exceed, plus_one_conditional_tail=(exceed + 1) / 200,
                interpretation='32formal fixed coordinate-route models, deduplicated by exact functional truth tables. Widths7/21postselected; familywise conditional shuffle maxima cover this correlated family only. No fitting or score-based expansion; regeneration alone is invertibility, not independent decoding.')


if __name__ == '__main__':
    runid, result = registered_run('SPLIT-COORDINATE-001', SPEC, 'experiments/split_coordinate.py',
                                 ['tests/test_split_coordinate.py'], 30, run)
    print(json.dumps(dict(run_id=runid, observed=result['observed'], controls=result['controls'],
                          exceedances=result['exceedances'], plus_one_conditional_tail=result['plus_one_conditional_tail'],
                          distinct_model_evaluations=result['distinct_model_evaluations'],
                          elapsed_seconds=result['elapsed_seconds']), indent=2))
