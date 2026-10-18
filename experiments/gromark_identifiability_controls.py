"""Independent complete-permutation truth tables for difference queries."""
import itertools
import time

from bounded_models import deadline_check
from gromark_identifiability import difference


def all_pairs(alphabet, edges):
    result = []
    for pa in itertools.permutations(alphabet):
        for ca in itertools.permutations(alphabet):
            p, c = ''.join(pa), ''.join(ca)
            valid = all((c.index(b) - p.index(a)) % len(alphabet) == k for a, b, k in edges)
            result.append((p, c, valid))
    return result


def oracle_query(alphabet, edges, reference, cipher, key, pairs):
    ref = reference['plain_alphabet'][(reference['cipher_alphabet'].index(cipher) - key) % len(alphabet)]
    expected = False
    checks = 0
    valid_witnesses = set()
    for p, c, valid in pairs:
        checks += 1
        if valid and p[(c.index(cipher) - key) % len(alphabet)] != ref:
            expected = True
            valid_witnesses.add((p, c))
    result = difference(alphabet, edges, reference, cipher, key)
    assert result['classification'] == ('variable' if expected else 'forced')
    if expected:
        w = result['counterexample']
        assert (w['plain_alphabet'], w['cipher_alphabet']) in valid_witnesses
    else:
        assert result['certificate']['proof_complete']
    return result, checks


def controls(prior_spec, limit=5):
    started = time.monotonic()
    check = lambda: deadline_check(started, limit)
    check()
    bases = base_checks = queries = query_checks = 0
    sat_bases = unsat_bases = forced = variable = 0
    graphs = []
    for topology in prior_spec['controls']['toy_oracle']['modulus3_topologies']:
        for offsets in itertools.product(range(3), repeat=len(topology)):
            graphs.append(('ABC', [(a, b, k) for (a, b), k in zip(topology, offsets)]))
    graphs.extend(('ABCD', f['edges']) for f in prior_spec['controls']['toy_oracle']['modulus4_fixtures'])
    for alphabet, edges in graphs:
        check()
        pairs = all_pairs(alphabet, edges)
        bases += 1
        base_checks += len(pairs)
        valid = [(p, c) for p, c, ok in pairs if ok]
        if not valid:
            unsat_bases += 1
            continue
        sat_bases += 1
        reference = dict(zip(('plain_alphabet', 'cipher_alphabet'), valid[0]))
        for cipher, key in itertools.product(alphabet, range(len(alphabet))):
            check()
            r, checked = oracle_query(alphabet, edges, reference, cipher, key, pairs)
            queries += 1
            query_checks += checked
            forced += r['classification'] == 'forced'
            variable += r['classification'] == 'variable'
    assert (bases, base_checks, sat_bases, unsat_bases, queries, query_checks) == (231, 9396, 56, 175, 511, 27036)
    reference = {'plain_alphabet': 'AB', 'cipher_alphabet': 'AB'}
    extra = [([('A', 'A', 0)], 'B', 0), ([], 'A', 0), ([], 'A', 0), ([], 'B', 0)]
    extra_records = []
    for edges, cipher, key in extra:
        check()
        r, count = oracle_query('AB', edges, reference, cipher, key, all_pairs('AB', edges))
        queries += 1
        query_checks += count
        forced += r['classification'] == 'forced'
        variable += r['classification'] == 'variable'
        extra_records.append({'classification': r['classification'], 'method': r['method']})
    assert extra_records[0]['method'] == 'exhausted_difference_CSP'
    assert all(r['classification'] == 'variable' for r in extra_records[1:])
    joint = all_pairs('AB', [])
    assert not any(p[c.index('A')] == p[c.index('B')] == 'A' for p, c, _ in joint)
    assert (queries, query_checks) == (515, 27052)
    check()
    return {'base_graphs': bases, 'base_permutation_pairs': base_checks,
            'satisfiable_bases': sat_bases, 'unsatisfiable_bases': unsat_bases,
            'toy_difference_queries': queries, 'query_permutation_pairs': query_checks,
            'toy_forced': forced, 'toy_variable': variable,
            'single_unused_symbols_global_proof_verified': True,
            'joint_constraint_pairs_checked': len(joint),
            'marginal_variability_does_not_imply_joint_freedom': True,
            'supplied_witness_pool_disabled': True, 'randomness': 'none'}
