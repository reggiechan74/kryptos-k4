#!/usr/bin/env python3
"""Replayable null calibration of the frozen 24-model periodic crib search.

Python standard library only. No fitting or changing geometry. All key entries
are re-estimated from the first crib in every null replicate.
"""
import collections
import fractions
import hashlib
import json
import math
import platform
import random
from pathlib import Path

import oracle

ROOT = Path(__file__).resolve().parent


def fit_keys(cipher_indices, plain_indices, start, family, period):
    key = [None] * period
    sign = -1 if family == 'add' else 1
    for j, plain in enumerate(plain_indices):
        pos = start + j
        value = (cipher_indices[pos] + sign * plain) % 26
        residue = pos % period
        if key[residue] is not None and value != key[residue]:
            return None
        key[residue] = value
    assert all(k is not None for k in key)
    return key


def independent_pairwise_pass(cipher_indices, plain_indices, start, family, period):
    # Check all same-residue ciphertext differences against plaintext differences,
    # with no key table, fitting step, or fit_keys call.
    for left in range(len(plain_indices)):
        for right in range(left + period, len(plain_indices), period):
            observed = (cipher_indices[start+right] - cipher_indices[start+left]) % 26
            delta = (plain_indices[right] - plain_indices[left]) % 26
            expected = delta if family == 'add' else (-delta) % 26
            if observed != expected:
                return False
    return True


def scan(cipher_indices, plain_indices, start, models):
    return {(family, period): fit_keys(cipher_indices, plain_indices, start, family, period)
            for family, period in models}


def wilson(k, n, z=1.959963984540054):
    p = k / n
    denominator = 1 + z*z/n
    center = (p + z*z/(2*n)) / denominator
    margin = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / denominator
    return [center-margin, center+margin]


def main():
    plan = json.loads((ROOT/'preregistration.json').read_text())
    code, alphabet = oracle.read_geometry(ROOT/'geometry-core.json')
    assert alphabet == plan['fixed_alphabet']
    source = json.loads((ROOT/'k4.json').read_text())
    ciphertext = source['ciphertext']
    index = {ch:i for i, ch in enumerate(alphabet)}
    original = [index[ch] for ch in ciphertext]
    start = plan['training_crib']['start_one_based'] - 1
    plain_indices = [index[ch] for ch in plan['training_crib']['plaintext']]
    models = [(family, period) for family in ('add','beaufort') for period in range(1,13)]
    observed = scan(original, plain_indices, start, models)
    actual_survivors = []
    for (family, period), key in observed.items():
        assert (key is not None) == independent_pairwise_pass(original, plain_indices, start, family, period)
        if key is not None:
            plaintext = oracle.periodic_crypt(ciphertext, alphabet, key, family, True)
            actual_survivors.append({'family':family,'period':period,'key':key,
                                     'training_window':plaintext[21:34],
                                     'second_window':plaintext[63:74],
                                     'second_check_pass':plaintext[63:74]=='BERLINCLOCK'})
    assert len(actual_survivors) == plan['observed_statistic'] == 1
    assert actual_survivors[0]['family']=='beaufort' and actual_survivors[0]['period']==12
    assert actual_survivors[0]['key']==[15,24,3,4,1,18,2,24,4,13,25,18]
    assert actual_survivors[0]['second_window']=='ZBVJDFKRUCA'

    # Positive controls: one planted 97-letter plaintext per member of the family.
    # Recover the entire key, training crib, Berlin crib, and complete plaintext.
    planted_plaintext = oracle.synthetic_plaintext()
    plants = []
    for family, period in models:
        key = [(7*j+3) % 26 for j in range(period)]
        planted_ciphertext = oracle.periodic_crypt(planted_plaintext, alphabet, key, family)
        planted_indices = [index[ch] for ch in planted_ciphertext]
        recovered = scan(planted_indices, plain_indices, start, models)[(family,period)]
        assert recovered == key
        full_plaintext = oracle.periodic_crypt(planted_ciphertext, alphabet, recovered, family, True)
        assert full_plaintext == planted_plaintext
        assert full_plaintext[21:34]=='EASTNORTHEAST' and full_plaintext[63:74]=='BERLINCLOCK'
        plants.append({'family':family,'period':period,'status':'pass'})

    counts = collections.Counter(original)
    expected_delta = (plain_indices[-1] - plain_indices[0]) % 26
    assert expected_delta == 17
    exact = {}
    for family, delta in (('add',expected_delta),('beaufort',(-expected_delta)%26)):
        numerator = sum(counts[x] * (counts[(x+delta)%26] - (delta == 0)) for x in range(26))
        denominator = len(original)*(len(original)-1)
        probability = fractions.Fraction(numerator, denominator)
        exact[family] = {'ciphertext_delta_mod26':delta,'favorable_ordered_position_pairs':numerator,
                         'all_ordered_distinct_position_pairs':denominator,
                         'probability_fraction':str(probability),'probability':float(probability)}
        # Independently enumerate physical source positions to verify histogram algebra.
        assert sum((original[j]-original[i])%26 == delta for i in range(97) for j in range(97) if i != j) == numerator
    assert expected_delta != (-expected_delta)%26

    seed_hex = hashlib.sha256(plan['experiment_id'].encode('utf-8')).hexdigest()
    seed = int(seed_hex, 16)
    rng = random.Random(seed)
    distribution = collections.Counter()
    per_model = collections.Counter()
    pairwise_comparisons = 0
    oracle_comparisons = 0
    trace_hash = hashlib.sha256()
    for trial in range(plan['N']):
        null = original.copy()
        rng.shuffle(null)
        fits = scan(null, plain_indices, start, models)
        passing = [(family,period) for (family,period),key in fits.items() if key is not None]
        distribution[len(passing)] += 1
        per_model.update(passing)
        trace_hash.update(bytes(null))
        trace_hash.update(bytes([len(passing)]))
        # Every null/model is cross-checked against independently expressed constraints.
        for (family,period), key in fits.items():
            assert (key is not None) == independent_pairwise_pass(null, plain_indices, start, family, period)
            pairwise_comparisons += 1
        # Also cross-check the original audit's independently developed oracle.
        if trial < 200 or trial % 1000 == 0:
            null_text = ''.join(alphabet[i] for i in null)
            for row in oracle.periodic_scan(null_text, alphabet):
                key = fits[(row['family'],row['period'])]
                assert row['first_crib_pass'] == (key is not None)
                if key is not None:
                    assert row['key'] == key
                oracle_comparisons += 1
    n = plan['N']
    exceedances = sum(count for value,count in distribution.items() if value>=plan['observed_statistic'])
    result = {
        'experiment_id':plan['experiment_id'],
        'python_version':platform.python_version(),
        'seed_sha256':seed_hex,
        'seed_integer_decimal':str(seed),
        'N':n,
        'rank_alphabet':alphabet,
        'observed_survivors':actual_survivors,
        'exact_period12_histogram_null':exact,
        'exact_union_of_both_period12_models':exact['add']['probability']+exact['beaufort']['probability'],
        'iid_uniform_single_period12_probability':1/26,
        'iid_uniform_per_model_probability':{str(p):26**(-(13-p)) for p in range(1,13)},
        'family_null_count_distribution':{str(k):v for k,v in sorted(distribution.items())},
        'per_model_pass_counts':[{'family':f,'period':p,'count':per_model[(f,p)],'frequency':per_model[(f,p)]/n} for f,p in models],
        'family_exceedances':exceedances,
        'family_empirical_tail_frequency':exceedances/n,
        'family_plus_one_monte_carlo_p':(exceedances+1)/(n+1),
        'family_tail_95pct_wilson_interval':wilson(exceedances,n),
        'null_draw_and_count_trace_sha256':trace_hash.hexdigest(),
        'controls':{'all_passed':True,'synthetic_plants':plants,'pairwise_comparisons':pairwise_comparisons,
                    'original_oracle_model_comparisons':oracle_comparisons,
                    'exact_pair_enumeration':'both equations passed'},
        'scope_caveat':plan['scope'],
        'null_caveat':'Shuffling is a specified exchangeability null, not a physical model of the unknown Kryptos encryption. The interval describes Monte Carlo uncertainty, not uncertainty over null choice.'
    }
    (ROOT/'result.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['N','family_null_count_distribution','family_exceedances','family_empirical_tail_frequency','family_plus_one_monte_carlo_p','family_tail_95pct_wilson_interval','exact_union_of_both_period12_models','controls']}, indent=2))


if __name__ == '__main__':
    main()
