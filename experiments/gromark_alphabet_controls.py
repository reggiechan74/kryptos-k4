"""Small direct permutation oracle and planted synthetic alphabet controls."""
import itertools
import random
import time

from bounded_models import deadline_check
from gromark_alphabet import expand, solve, encrypt, decrypt


def oracle(alphabet, edges):
    # Directly enumerate independent full permutations; no component logic.
    count = pairs = 0
    for p in itertools.permutations(range(len(alphabet))):
        for c in itertools.permutations(range(len(alphabet))):
            pairs += 1
            count += all((c[alphabet.index(b)] - p[alphabet.index(a)]) % len(alphabet) == k
                         for a, b, k in edges)
    return count, pairs


def independently_verify(alphabet, edges, witness):
    pa, ca = witness['plain_alphabet'], witness['cipher_alphabet']
    assert sorted(pa) == sorted(alphabet) and sorted(ca) == sorted(alphabet)
    p = {letter: coordinate for coordinate, letter in enumerate(pa)}
    c = {letter: coordinate for coordinate, letter in enumerate(ca)}
    assert all((c[b] - p[a]) % len(alphabet) == k for a, b, k in edges)


def controls(spec, limit=10):
    started = time.monotonic()
    check = lambda: deadline_check(started, limit)
    check()
    for vector in spec['controls']['hand_streams']:
        expected = vector.get('first10', vector.get('first12'))
        assert expand(vector['base'], vector['primer'], vector['lags'], len(expected)) == expected
    graphs = pairs = sat = unsat = 0
    for topology in spec['controls']['toy_oracle']['modulus3_topologies']:
        for offsets in itertools.product(range(3), repeat=len(topology)):
            check()
            edges = [(a, b, k) for (a, b), k in zip(topology, offsets)]
            count, used = oracle('ABC', edges)
            result = solve('ABC', edges, limit=limit - (time.monotonic() - started))
            assert (result['feasibility'] == 'satisfiable') == (count > 0)
            assert result['feasibility'] != 'unresolved'
            if count:
                independently_verify('ABC', edges, result['witness'])
                sat += 1
            else:
                unsat += 1
            graphs += 1
            pairs += used
    for fixture in spec['controls']['toy_oracle']['modulus4_fixtures']:
        check()
        count, used = oracle('ABCD', fixture['edges'])
        result = solve('ABCD', fixture['edges'], limit=limit - (time.monotonic() - started))
        assert result['graph']['local_filter_passed']
        assert (result['feasibility'] == 'satisfiable') == (count > 0)
        assert bool(count) == fixture['name'].endswith('_sat')
        if count:
            independently_verify('ABCD', fixture['edges'], result['witness'])
            sat += 1
        else:
            assert result['exhausted']
            unsat += 1
        graphs += 1
        pairs += used
    assert (graphs, pairs) == (231, 9396)
    rng = random.Random(20261018)
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    stream = expand(spec['model']['base'], spec['model']['primer'], spec['model']['lags'], 97)
    positions = tuple(range(21, 34)) + tuple(range(63, 74))
    plants = []
    for trial in range(8):
        check()
        pa = ''.join(rng.sample(alphabet, 26))
        ca = ''.join(rng.sample(alphabet, 26))
        plain = ''.join(rng.sample(alphabet, 26)) + ''.join(rng.choice(alphabet) for _ in range(71))
        # Independently form ciphertext, not via the encoder under test.
        coord = {letter: value for value, letter in enumerate(pa)}
        cipher = ''.join(ca[(coord[letter] + k) % 26] for letter, k in zip(plain, stream))
        assert encrypt(plain, stream, pa, ca) == cipher
        assert decrypt(cipher, stream, pa, ca) == plain
        known = range(97) if trial < 4 else positions
        edges = [(plain[i], cipher[i], stream[i]) for i in known]
        result = solve(alphabet, edges, limit=limit - (time.monotonic() - started))
        assert result['feasibility'] == 'satisfiable'
        witness = result['witness']
        independently_verify(alphabet, edges, witness)
        recovered = decrypt(cipher, stream, witness['plain_alphabet'], witness['cipher_alphabet'])
        assert all(recovered[i] == plain[i] for i in known)
        if trial < 4:
            assert recovered == plain
        assert encrypt(recovered, stream, witness['plain_alphabet'], witness['cipher_alphabet']) == cipher
        plants.append({'known_positions': len(known), 'search_states': result['search_states'],
                       'full_regeneration': True, 'original_plaintext_required': trial < 4})
    check()
    return {'hand_streams': 2, 'exhaustive_toy_graphs': graphs, 'full_permutation_pairs': pairs,
            'toy_sat': sat, 'toy_unsat': unsat, 'cross_component_obstruction_verified': True,
            'synthetic_full_alphabet_plants': plants, 'seed': 20261018,
            'generator': 'Python random.Random MT19937', 'third_party_source_execution': False}
