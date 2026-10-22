#!/usr/bin/env python3
"""Independent, fixed-scope K4 same-state/same-key single-boundary audit.
Run: python audit.py --output results.json
Python standard library only. Boundary b is after one-based position b;
b=0 means the no-reset baseline. No cipher parameters are fitted per block.
"""
import argparse
import hashlib
import itertools
import json
import random
from pathlib import Path

C = 'OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR'
ALPHABETS = {'AZ': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'K': 'KRYPTOSABCDEFGHIJLMNQUVWXZ'}
CRIBS = [(22, 'EASTNORTHEAST'), (64, 'BERLINCLOCK')]
KNOWN = {start - 1 + j: p for start, text in CRIBS for j, p in enumerate(text)}
BOUNDARIES = list(range(len(C)))
assert len(C) == 97 and len(KNOWN) == 24
assert all(len(set(a)) == len(a) == 26 for a in ALPHABETS.values())


def mtf_decode(cipher, ref, initial, boundary):
    state = list(initial)
    out = []
    for i, char in enumerate(cipher):
        if boundary and i == boundary:
            state = list(initial)
        rank = state.index(char)
        out.append(ref[rank])
        state.pop(rank)
        state.insert(0, char)
    return ''.join(out)


def mtf_rank_oracle(cipher, ref, initial, boundary):
    # Independent representation: symbol->rank instead of an ordered alphabet.
    ranks = {x: i for i, x in enumerate(initial)}
    out = []
    for i, char in enumerate(cipher):
        if boundary and i == boundary:
            ranks = {x: j for j, x in enumerate(initial)}
        old_rank = ranks[char]
        out.append(ref[old_rank])
        for symbol in ranks:
            if ranks[symbol] < old_rank:
                ranks[symbol] += 1
        ranks[char] = 0
    return ''.join(out)


def mtf_encode(plain, ref, initial, boundary):
    state = initial
    out = ''
    for i, char in enumerate(plain):
        if boundary and i == boundary:
            state = initial
        emitted = state[ref.index(char)]
        out += emitted
        state = emitted + state.replace(emitted, '')
    return out


def rec_encode(plain, q, params, boundary):
    a, b, d, initial = params
    current = initial
    out = []
    for i, value in enumerate(plain):
        if i and i != boundary:
            current = (a * current + b + d * out[-1]) % q
        elif i == boundary:
            current = initial
        out.append((value + current) % q)
    return out


def rec_decode(cipher, q, params, boundary):
    # A separate key-array calculation provides the decoder.
    a, b, d, initial = params
    keys = [initial]
    for i in range(1, len(cipher)):
        keys.append(initial if i == boundary else (a * keys[-1] + b + d * cipher[i - 1]) % q)
    return [(value - key) % q for value, key in zip(cipher, keys)]


def recurrence_equations(cipher, known, q, boundary):
    key = {i: (cipher[i] - value) % q for i, value in known.items()}
    return [(i, key[i - 1], cipher[i - 1], key[i])
            for i in sorted(key) if i - 1 in key and i != boundary]


def filter_triples(equations, q):
    # Exhaustive ring arithmetic, no inversion or field assumption.
    return [(a, b, d) for a, b, d in itertools.product(range(q), repeat=3)
            if all((a * u + b + d * v - w) % q == 0 for i, u, v, w in equations)]


def staged_recurrence_solver(cipher, known, q, boundary):
    triples = filter_triples(recurrence_equations(cipher, known, q, boundary), q)
    solutions = []
    for a, b, d in triples:
        for initial in range(q):
            params = (a, b, d, initial)
            decoded = rec_decode(cipher, q, params, boundary)
            if all(decoded[i] == p for i, p in known.items()):
                solutions.append(params)
    return triples, solutions


def brute_recurrence_oracle(cipher, known, q, boundary):
    # Does not construct key equations, use staged filtering, or call the decoder.
    answer = []
    for params in itertools.product(range(q), repeat=4):
        multiplier, offset, feedback, start = params
        key = start
        good = True
        for j in range(len(cipher)):
            if j > 0:
                key = start if j == boundary else (multiplier * key + offset + feedback * cipher[j - 1]) % q
            if j in known and (cipher[j] - key) % q != known[j]:
                good = False
                break
        if good:
            answer.append(params)
    return answer


def periodic_solution(cipher, known, q, period, boundary):
    assigned = {}
    first = {}
    for i, p in sorted(known.items()):
        phase = ((i - boundary) if boundary and i >= boundary else i) % period
        value = (cipher[i] - p) % q
        if phase in assigned and value != assigned[phase]:
            return {'solution_count': 0, 'conflict': [first[phase] + 1, i + 1],
                    'values': [assigned[phase], value], 'phase': phase}
        assigned[phase] = value
        first.setdefault(phase, i)
    return {'solution_count': q ** (period - len(assigned)), 'assigned': assigned}


def periodic_encode(plain, key, q, boundary):
    return [(value + key[(i - boundary if boundary and i >= boundary else i) % len(key)]) % q
            for i, value in enumerate(plain)]


def parity_certificate(equations):
    for n in range(1, len(equations) + 1):
        for subset in itertools.combinations(equations, n):
            if not filter_triples(subset, 2):
                return [{'transition': [i, i + 1], 'previous_key': u,
                         'previous_cipher': v, 'next_key': w,
                         'parity_predictors': [u % 2, v % 2], 'parity_target': w % 2}
                        for i, u, v, w in subset]
    return None


def controls():
    rng = random.Random(20261022)
    counts = {'mtf_roundtrips_and_rank_oracle': 0, 'recurrence_planted_controls': 0,
              'recurrence_toy_full_enumeration': 0, 'periodic_planted_controls': 0,
              'periodic_toy_full_enumeration': 0, 'mutation_controls': 0}
    plain = ''.join(rng.choice(ALPHABETS['AZ']) for _ in C)
    for ref, initial in itertools.product(ALPHABETS.values(), repeat=2):
        for boundary in BOUNDARIES:
            encrypted = mtf_encode(plain, ref, initial, boundary)
            assert mtf_decode(encrypted, ref, initial, boundary) == plain
            assert mtf_rank_oracle(encrypted, ref, initial, boundary) == plain
            bad = ('Z' if plain[0] != 'Z' else 'Y') + plain[1:]
            assert mtf_decode(encrypted, ref, initial, boundary) != bad
            counts['mtf_roundtrips_and_rank_oracle'] += 1
            counts['mutation_controls'] += 1
    selected_boundaries = [0, 1, 22, 23, 26, 33, 50, 64, 68, 74, 96]
    parameters = [(11, 23, 24, 7), (2, 6, 12, 0), (13, 0, 13, 25), (0, 9, 0, 13)]
    for alphabet in ALPHABETS.values():
        values = [alphabet.index(x) for x in plain]
        known = {i: values[i] for i in KNOWN}
        for params, boundary in itertools.product(parameters, selected_boundaries):
            encrypted = rec_encode(values, 26, params, boundary)
            assert rec_decode(encrypted, 26, params, boundary) == values
            triples, solutions = staged_recurrence_solver(encrypted, known, 26, boundary)
            assert params in solutions and params[:3] in triples
            counts['recurrence_planted_controls'] += 1
        for period, boundary in itertools.product([8, 10], selected_boundaries):
            key = [rng.randrange(26) for _ in range(period)]
            encrypted = periodic_encode(values, key, 26, boundary)
            solved = periodic_solution(encrypted, known, 26, period, boundary)
            assert solved['solution_count'] == 1
            assert all(solved['assigned'][i] == key[i] for i in range(period))
            counts['periodic_planted_controls'] += 1
    # Rings 4 and 6 exercise zero divisors. Full 4-parameter oracle is independent.
    for q in [2, 3, 4, 6]:
        values = [rng.randrange(q) for _ in range(10)]
        known = {i: values[i] for i in [1, 2, 3, 6, 7, 8]}
        for boundary in range(len(values)):
            params = tuple(rng.randrange(q) for _ in range(4))
            cipher = rec_encode(values, q, params, boundary)
            _, staged = staged_recurrence_solver(cipher, known, q, boundary)
            brute = brute_recurrence_oracle(cipher, known, q, boundary)
            assert set(staged) == set(brute) and params in brute
            counts['recurrence_toy_full_enumeration'] += 1
    for q, period in itertools.product([2, 3], [2, 3]):
        cipher = [rng.randrange(q) for _ in range(9)]
        known = {i: rng.randrange(q) for i in [1, 2, 3, 6, 7]}
        for boundary in range(len(cipher)):
            count = 0
            for key in itertools.product(range(q), repeat=period):
                if all((cipher[i] - key[(i - boundary if boundary and i >= boundary else i) % period]) % q == p
                       for i, p in known.items()):
                    count += 1
            assert periodic_solution(cipher, known, q, period, boundary)['solution_count'] == count
            counts['periodic_toy_full_enumeration'] += 1
    return counts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='results.json')
    args = parser.parse_args()
    result = {'ciphertext': C, 'ciphertext_sha256': hashlib.sha256(C.encode()).hexdigest(),
              'alphabets': ALPHABETS, 'cribs': [{'start': s, 'text': p} for s, p in CRIBS],
              'boundary_definition': 'b=0: no reset; b in 1..96: reset before one-based position b+1',
              'mtf': [], 'recurrence': [], 'periodic': [], 'island_certificates': {}}
    result['controls'] = controls()
    print('Controls passed:', result['controls'], flush=True)
    repeat_certificates = []
    for i in sorted(KNOWN):
        if i and C[i] == C[i - 1]:
            repeat_certificates.append({'ciphertext_positions': [i, i + 1], 'ciphertext_symbol': C[i],
                                        'known_plaintext_position': i + 1, 'known_plaintext': KNOWN[i],
                                        'forced_without_reset': {name: a[0] for name, a in ALPHABETS.items()},
                                        'reset_boundary_required': i})
    result['mtf_adjacent_repeat_certificates'] = repeat_certificates
    # Analytical consequence requested after preregistration, not another search:
    # at position 27, either Q is at front after emitting Q at 26, or state=S0.
    fixed_mtf_position27 = []
    for (rname, ref), (sname, initial) in itertools.product(ALPHABETS.items(), repeat=2):
        possible = [ref[0], ref[initial.index(C[26])]]
        assert C[25:27] == 'QQ' and KNOWN[26] == 'O' and 'O' not in possible
        fixed_mtf_position27.append({'reference': rname, 'initial': sname,
                                     'without_reset_before27': possible[0],
                                     'with_reset_before27': possible[1],
                                     'required_plaintext': 'O'})
    result['analytic_consequence_fixed_mtf_arbitrary_same_state_resets'] = fixed_mtf_position27
    for (rname, ref), (sname, initial) in itertools.product(ALPHABETS.items(), repeat=2):
        for boundary in BOUNDARIES:
            decoded = mtf_decode(C, ref, initial, boundary)
            assert decoded == mtf_rank_oracle(C, ref, initial, boundary)
            mismatches = [i + 1 for i, p in sorted(KNOWN.items()) if decoded[i] != p]
            result['mtf'].append({'reference': rname, 'initial': sname, 'boundary': boundary,
                                  'survives': not mismatches, 'crib_mismatch_positions': mismatches})
    for name, alphabet in ALPHABETS.items():
        cipher = [alphabet.index(x) for x in C]
        known = {i: alphabet.index(p) for i, p in KNOWN.items()}
        island = []
        for start, text in CRIBS:
            island_known = {i: known[i] for i in range(start - 1, start - 1 + len(text))}
            equations = recurrence_equations(cipher, island_known, 26, 0)
            keys = {i: (cipher[i] - p) % 26 for i, p in island_known.items()}
            conflicts = {}
            for period in [8, 10]:
                conflicts[period] = [{'positions': [i + 1, i + period + 1], 'key_values': [keys[i], keys[i + period]]}
                                     for i in keys if i + period in keys and keys[i] != keys[i + period]]
            island.append({'start': start, 'end': start + len(text) - 1,
                           'derived_key': list(keys.values()), 'recurrence_parity_certificate': parity_certificate(equations),
                           'periodic_conflicts': conflicts})
        result['island_certificates'][name] = island
        for boundary in BOUNDARIES:
            equations = recurrence_equations(cipher, known, 26, boundary)
            parity_candidates = filter_triples(equations, 2)
            triples, solutions = staged_recurrence_solver(cipher, known, 26, boundary)
            assert not parity_candidates and not triples and not solutions
            result['recurrence'].append({'alphabet': name, 'boundary': boundary,
                                         'internal_equation_count': len(equations),
                                         'mod2_candidate_triples': len(parity_candidates),
                                         'mod26_candidate_triples': len(triples), 'parameter_solutions': len(solutions),
                                         'distinct_plaintext_classes': 0,
                                         'forced_positions': None})
            for period in [8, 10]:
                solved = periodic_solution(cipher, known, 26, period, boundary)
                assert solved['solution_count'] == 0
                result['periodic'].append({'alphabet': name, 'period': period, 'boundary': boundary, **solved})
    result['summary'] = {
        'mtf_settings_tested': len(result['mtf']), 'mtf_survivors': sum(x['survives'] for x in result['mtf']),
        'recurrence_alphabet_boundary_settings': len(result['recurrence']),
        'recurrence_triples_enumerated': 2 * len(BOUNDARIES) * 26 ** 3,
        'recurrence_parameter_boundary_domain_size': 2 * len(BOUNDARIES) * 26 ** 4,
        'recurrence_surviving_parameter_settings': sum(x['parameter_solutions'] for x in result['recurrence']),
        'periodic_alphabet_period_boundary_settings': len(result['periodic']),
        'periodic_surviving_settings': sum(x['solution_count'] > 0 for x in result['periodic']),
        'plaintext_classes': 0, 'forced_positions': None,
        'scope_note': 'Exact exclusion only of the preregistered models, not all reset models or K4 generally.'}
    Path(args.output).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result['summary'], indent=2), flush=True)
    print('Wrote', args.output, flush=True)


if __name__ == '__main__':
    main()
