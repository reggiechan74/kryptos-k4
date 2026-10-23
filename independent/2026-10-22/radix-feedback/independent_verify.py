#!/usr/bin/env python3
"""Independent, read-only verifier for K4-FROZEN-GLYPH-AFFINE-FEEDBACK-001.

Usage: python independent_verify.py [audit-directory] [geometry-file]
Uses Python's standard library only. Does not read primary audit code or evaluate
the heldout or auxiliary direct-map experiment. Prints JSON; writes no files.
"""
import hashlib
import itertools
import json
import sys
from pathlib import Path


def pinned_json(path, expected):
    raw = path.read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    assert actual == expected, (str(path), actual, expected)
    return json.loads(raw)


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent
    if len(sys.argv) > 2:
        geometry_path = Path(sys.argv[2])
    else:
        geometry_path = root / 'modeled-uppercase-geometry-001-core.json'
        if not geometry_path.exists():
            geometry_path = root.parent / geometry_path.name
    spec = pinned_json(root / 'SPECIFICATION.json',
        'caa60d80cf41e7b0a498eeaff62a14b84ef250c44756762fcf84878cfb2c6e5f')
    geometry = pinned_json(geometry_path,
        '6a5c6eae644dedf88afb68df911f0c3161a969af3815972aa5694479155aa010')
    amendment = pinned_json(root / 'SCHEMA_AMENDMENT.json',
        '01982c71b729ec5673c9ba52a63a6e699e3955a05af3c8ee25ead8265795683d')
    assert amendment['original_spec_sha256'] == hashlib.sha256(
        (root / 'SPECIFICATION.json').read_bytes()).hexdigest()

    order = geometry['feature_order']
    glyphs = geometry['glyphs']
    assert len(order) == len(set(order)) == 35
    assert order == sorted(geometry['primitives'])
    assert set(glyphs) == set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    assert all(set(parts) <= set(order) for parts in glyphs.values())
    # Dense reconstruction and independent sparse-index reconstruction.
    vectors = {t: [parts.count(f) for f in order] for t, parts in glyphs.items()}
    powers = {t: [order.index(f) for f in parts] for t, parts in glyphs.items()}
    for t, vector in vectors.items():
        assert set(vector) <= {0, 1}
        assert vector == [int(j in powers[t]) for j in range(35)]

    def code_mod(t, b, modulus):
        return sum(pow(b, j, modulus) for j in powers[t]) % modulus

    bases = list(range(2, 62)) + [10**50 + 2, 10**50 + 3]
    for t, vector in vectors.items():
        for b in bases:
            direct = sum(b**j for j in powers[t])
            horner = 0
            for digit in reversed(vector):
                horner = horner * b + digit
            assert direct == horner
            assert direct % 26 == code_mod(t, b, 26)
            expected_parity = vector[0] if b % 2 == 0 else sum(vector) % 2
            assert direct % 2 == expected_parity

    residues = {t: {code_mod(t, b, 26) for b in range(2, 28)} for t in glyphs}
    parities = {t: {v[0] % 2, sum(v) % 2} for t, v in vectors.items()}
    triples2 = list(itertools.product(range(2), repeat=3))

    def allowable_parity_triples(keys, source):
        return [{(a, c, d) for a, c, d in triples2
                 if any((a * keys[i] + c + d * r - keys[i+1]) % 2 == 0
                        for r in parities[t])}
                for i, t in enumerate(source[:-1])]

    def mod26_survivors(keys, source):
        found = []
        for a, c, d in itertools.product(range(26), repeat=3):
            if all((keys[i+1] - a * keys[i] - c) % 26
                   in {(d * r) % 26 for r in residues[t]}
                   for i, t in enumerate(source[:-1])):
                found.append((a, c, d))
        return found

    lo, hi = spec['plaintext_training_crib']['positions_1_based_inclusive']
    plaintext = spec['plaintext_training_crib']['text']
    ciphertext = spec['ciphertext'][lo-1:hi]
    assert len(spec['ciphertext']) == 97
    assert len(plaintext) == len(ciphertext) == hi-lo+1 == 13
    assert (lo, hi, plaintext, ciphertext) == (22, 34, 'EASTNORTHEAST', 'FLRVQQPRNGKSS')
    expected_cores = {('AZ', 'P'): (22, 24), ('AZ', 'C'): (23, 26),
                      ('KRYPTOS', 'P'): (22, 29), ('KRYPTOS', 'C'): (23, 33)}
    expected_core_counts = {('AZ', 'P'): 5, ('AZ', 'C'): 7,
                            ('KRYPTOS', 'P'): 4, ('KRYPTOS', 'C'): 5}
    output = {'training': {'positions': [lo, hi], 'plaintext': plaintext,
                           'ciphertext': ciphertext}, 'families': [],
              'positive_controls': [], 'heldout_evaluated': False,
              'auxiliary_direct_map_evaluated': False}
    for name, alphabet in spec['alphabets'].items():
        assert len(alphabet) == len(set(alphabet)) == 26
        paired_keys = []
        for equation in ['additive', 'Beaufort']:
            sign = -1 if equation == 'additive' else 1
            keys = [(alphabet.index(c) + sign * alphabet.index(p)) % 26
                    for p, c in zip(plaintext, ciphertext)]
            paired_keys.append(keys)
            for source_name, source in [('P', plaintext), ('C', ciphertext)]:
                allowed = allowable_parity_triples(keys, source)
                assert not set(triples2).intersection(*allowed)
                minimum_cores = []
                for size in range(1, len(allowed)+1):
                    minimum_cores = [inds for inds in itertools.combinations(range(len(allowed)), size)
                                     if not set(triples2).intersection(*(allowed[i] for i in inds))]
                    if minimum_cores:
                        break
                core = minimum_cores[0]
                assert tuple(lo+i for i in core) == expected_cores[name, source_name]
                assert len(minimum_cores) == expected_core_counts[name, source_name]
                survivors26 = mod26_survivors(keys, source)
                assert not survivors26
                certificates = [{'position': lo+i, 'glyph': source[i],
                                 'key_parity': keys[i] % 2, 'next_key_parity': keys[i+1] % 2,
                                 'possible_code_parities': sorted(parities[source[i]])}
                                for i in core]
                eliminated = [{'coefficient_parities': abc,
                               'first_rejecting_position': next(lo+i for i in core if abc not in allowed[i])}
                              for abc in triples2]
                output['families'].append({'alphabet': name, 'equation': equation,
                    'source': source_name, 'keys': keys, 'key_parity': ''.join(str(k % 2) for k in keys),
                    'minimum_core': certificates, 'minimum_core_count': len(minimum_cores),
                    'eliminations': eliminated, 'mod26_triples_examined': 26**3,
                    'mod26_survivors': len(survivors26)})
        assert paired_keys[0] != paired_keys[1]
        assert all((a-b) % 2 == 0 for a, b in zip(*paired_keys))

    # Positive controls use the same arbitrary-base freedom, but freshly generate
    # ciphertext and keys. In particular C is generated before a C-source update.
    a, c, d, initial_key = 17, 9, 23, 21
    schedule = [2, 3, 11, 13, 17, 61, 10**50+2, 10**50+3, 7, 26, 27, 60, 6]
    for name, alphabet in spec['alphabets'].items():
        for equation in ['additive', 'Beaufort']:
            for source_name in ['P', 'C']:
                key = initial_key
                planted_keys, generated = [], []
                for i, p in enumerate(plaintext):
                    planted_keys.append(key)
                    pi = alphabet.index(p)
                    ci = (pi+key) % 26 if equation == 'additive' else (key-pi) % 26
                    ch = alphabet[ci]
                    generated.append(ch)
                    glyph = p if source_name == 'P' else ch
                    key = (a*key + c + d*code_mod(glyph, schedule[i], 26)) % 26
                recovered = [(alphabet.index(ch) + (-1 if equation == 'additive' else 1)
                              * alphabet.index(p)) % 26 for p, ch in zip(plaintext, generated)]
                source = plaintext if source_name == 'P' else ''.join(generated)
                assert recovered == planted_keys
                assert (a, c, d) in mod26_survivors(planted_keys, source)
                assert (a % 2, c % 2, d % 2) in set(triples2).intersection(
                    *allowable_parity_triples(planted_keys, source))
                output['positive_controls'].append({'alphabet': name, 'equation': equation,
                    'source': source_name, 'planted_coefficients': [a, c, d],
                    'initial_key': initial_key, 'retained': True, 'full_key_recovery_exact': True})
    output['geometry_controls'] = {'glyphs': 26, 'dimensions': 35,
        'bases_checked_per_glyph': len(bases), 'exact_horner_modular_parity_agree': True}
    output['result'] = 'All eight specified families are impossible; heldout not evaluated.'
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
