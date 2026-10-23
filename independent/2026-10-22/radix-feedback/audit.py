#!/usr/bin/env python3
"""Reproduce the frozen-glyph K4 radix-feedback admissibility audit. Stdlib only."""

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
GEOMETRY_SHA = "6a5c6eae644dedf88afb68df911f0c3161a969af3815972aa5694479155aa010"
SPEC_SHA = "caa60d80cf41e7b0a498eeaff62a14b84ef250c44756762fcf84878cfb2c6e5f"
AMENDMENT_SHA = "01982c71b729ec5673c9ba52a63a6e699e3955a05af3c8ee25ead8265795683d"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_verified():
    for name, expected in [
        ("modeled-uppercase-geometry-001-core.json", GEOMETRY_SHA),
        ("SPECIFICATION.json", SPEC_SHA),
        ("SCHEMA_AMENDMENT.json", AMENDMENT_SHA),
    ]:
        assert sha(HERE / name) == expected, "Frozen input changed: " + name
    geometry = json.loads((HERE / "modeled-uppercase-geometry-001-core.json").read_text())
    spec = json.loads((HERE / "SPECIFICATION.json").read_text())
    order = geometry["feature_order"]
    assert len(order) == len(set(order)) == 35
    assert order[0] == "ARC_BOTTOM_HALF"
    assert set(geometry["glyphs"]) == set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    vectors = {}
    for letter, glyph in geometry["glyphs"].items():
        assert set(glyph) <= set(order)
        v = [0] * 35
        for feature in glyph:
            v[order.index(feature)] += 1
        independently_built = [glyph.count(feature) for feature in order]
        assert v == independently_built
        assert set(v) <= {0, 1}
        vectors[letter] = v
    return geometry, spec, vectors


def code_exact(v, base):
    assert isinstance(base, int) and base >= 2
    return sum(bit * base ** j for j, bit in enumerate(v))


def code_mod(v, base, modulus=26):
    # Horner uses a different evaluation order from code_exact and the reference.
    value = 0
    for bit in reversed(v):
        value = (value * base + bit) % modulus
    return value


def inferred_keys(plaintext, ciphertext, alphabet, equation):
    sign = -1 if equation == "additive" else 1
    return [(alphabet.index(c) + sign * alphabet.index(p)) % 26
            for p, c in zip(plaintext, ciphertext)]


def transition_rows(plaintext, ciphertext, alphabet, equation, source, vectors, start=1):
    assert len(plaintext) == len(ciphertext)
    keys = inferred_keys(plaintext, ciphertext, alphabet, equation)
    glyphs = plaintext if source == "plaintext" else ciphertext
    rows = []
    for i in range(len(keys) - 1):
        v = vectors[glyphs[i]]
        rows.append({
            "position": start + i, "next_position": start + i + 1,
            "source_glyph": glyphs[i], "key": keys[i], "next_key": keys[i + 1],
            "code_parities": sorted({v[0] % 2, sum(v) % 2}),
            "code_residues_mod26": sorted({code_mod(v, b) for b in range(2, 28)}),
        })
    return keys, rows


def accepts(params, rows, modulus):
    a, c, d = params
    field = "code_parities" if modulus == 2 else "code_residues_mod26"
    return all(any((a * row["key"] + c + d * q - row["next_key"]) % modulus == 0
                   for q in row[field]) for row in rows)


def survivors(rows, modulus):
    return [t for t in itertools.product(range(modulus), repeat=3)
            if accepts(t, rows, modulus)]


def minimum_certificate(rows):
    candidates = list(itertools.product(range(2), repeat=3))
    for size in range(1, len(rows) + 1):
        for subset in itertools.combinations(rows, size):
            if not any(accepts(p, subset, 2) for p in candidates):
                return list(subset)
    return []


def independent_certificate_verification(certificate):
    # Verify by direct parity equations rather than reusing accepts().
    exclusions = []
    for a in (0, 1):
        for c in (0, 1):
            for d in (0, 1):
                bad = []
                for row in certificate:
                    allowed = {(a * (row["key"] & 1) + c + d * q) & 1
                               for q in row["code_parities"]}
                    if (row["next_key"] & 1) not in allowed:
                        bad.append(row["position"])
                assert bad, "Reported certificate does not exclude every parity triple"
                exclusions.append({"a_c_d_mod2": [a, c, d], "violated_positions": bad})
    return exclusions


def reference_encrypt(plaintext, alphabet, equation, source, params, initial, bases, geometry):
    # Independent sparse-primitive polynomial evaluation, direct powers mod 26.
    index = {letter: i for i, letter in enumerate(alphabet)}
    feature_index = {feature: i for i, feature in enumerate(geometry["feature_order"])}
    a, c, d = params
    key = initial
    ciphertext, trace = [], []
    for i, p in enumerate(plaintext):
        p_num = index[p]
        c_num = (p_num + key) % 26 if equation == "additive" else (key - p_num) % 26
        c_glyph = alphabet[c_num]
        trace.append(key)
        ciphertext.append(c_glyph)
        glyph = p if source == "plaintext" else c_glyph
        q = sum(pow(bases[i], feature_index[component], 26)
                for component in geometry["glyphs"][glyph]) % 26
        key = (a * key + c + d * q) % 26
    trace.append(key)
    return "".join(ciphertext), trace


def decrypt(ciphertext, alphabet, equation, source, params, initial, bases, vectors):
    key = initial
    plaintext, trace = [], []
    a, c, d = params
    for i, c_glyph in enumerate(ciphertext):
        c_num = alphabet.index(c_glyph)
        p_num = (c_num - key) % 26 if equation == "additive" else (key - c_num) % 26
        p = alphabet[p_num]
        trace.append(key)
        plaintext.append(p)
        glyph = p if source == "plaintext" else c_glyph
        key = (a * key + c + d * code_mod(vectors[glyph], bases[i])) % 26
    trace.append(key)
    return "".join(plaintext), trace


def sqrt_two_fractional_digits(radix, length):
    # Exact digits from floor(sqrt(2) * radix**length), without floats.
    integer = math.isqrt(2 * radix ** (2 * length)) - radix ** length
    digits = [0] * length
    for i in reversed(range(length)):
        integer, digits[i] = divmod(integer, radix)
    assert integer == 0
    return digits


def run_controls(geometry, spec, vectors):
    evaluation_checks = 0
    eval_bases = [2, 3, 4, 11, 13, 17, 26, 27, 61, 10 ** 80, 10 ** 80 + 1]
    always_even = []
    for letter, v in vectors.items():
        if v[0] == 0 and sum(v) % 2 == 0:
            always_even.append(letter)
        for base in eval_bases:
            exact = code_exact(v, base)
            assert exact % 26 == code_mod(v, base)
            predicted = v[0] % 2 if base % 2 == 0 else sum(v) % 2
            assert exact % 2 == predicted
            assert code_mod(v, base) == code_mod(v, base + 26)
            evaluation_checks += 1
    assert set("ELQS") <= set(always_even)
    # Nonqualifying counterexamples test BOTH requirements of the even-code lemma.
    counterexamples = []
    for letter, base in [("J", 2), ("A", 3), ("U", 2), ("U", 3)]:
        v = vectors[letter]
        assert code_exact(v, base) % 2 == 1
        counterexamples.append({"glyph": letter, "base": base,
                                "bit0": v[0], "components": sum(v), "code_parity": 1})

    plaintext = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" * 2
    n = len(plaintext)
    schedules = {"constant_2": [2] * n, "constant_3": [3] * n,
                 "constant_26": [26] * n, "constant_27": [27] * n,
                 "constant_61": [61] * n, "alternating_2_3": [2 + i % 2 for i in range(n)],
                 "cycle_2_through_61": [2 + i % 60 for i in range(n)],
                 "huge_alternating_parities": [10 ** 80 + i for i in range(n)]}
    for radix in [10, 12, 16, 60]:
        schedules["sqrt2_radix_%d_digits_plus2" % radix] = [
            d + 2 for d in sqrt_two_fractional_digits(radix, n)]
    params_list = list(itertools.product(range(2), repeat=3))
    params_list += [(i, (7 * i + 3) % 26, (11 * i + 5) % 26) for i in range(26)]
    roundtrips, parity_retained, exact_retained = 0, 0, 0
    exhaustive_positive_checks = []
    for alphabet_name, alphabet in spec["alphabets"].items():
        for equation in ["additive", "beaufort"]:
            for source in ["ciphertext", "plaintext"]:
                for schedule_name, bases in schedules.items():
                    for test_i, params in enumerate(params_list):
                        initial = (17 * test_i + 9) % 26
                        ct, reference_trace = reference_encrypt(
                            plaintext, alphabet, equation, source, params, initial, bases, geometry)
                        actual_plain, actual_trace = decrypt(
                            ct, alphabet, equation, source, params, initial, bases, vectors)
                        assert actual_plain == plaintext and actual_trace == reference_trace
                        inferred, rows = transition_rows(
                            plaintext, ct, alphabet, equation, source, vectors)
                        assert inferred == reference_trace[:-1]
                        # First character MUST use the supplied key, not an advanced state.
                        expected_first = ((alphabet.index(plaintext[0]) + initial) % 26
                                          if equation == "additive" else
                                          (initial - alphabet.index(plaintext[0])) % 26)
                        assert ct[0] == alphabet[expected_first]
                        reduced = tuple(x % 2 for x in params)
                        assert reduced in survivors(rows, 2)
                        assert accepts(params, rows, 26)
                        roundtrips += 1
                        parity_retained += 1
                        exact_retained += 1
                # One full 26^3 solve per family checks the exact enumerator on positive data.
                planted = (5, 7, 11)
                bases = schedules["sqrt2_radix_60_digits_plus2"]
                short_plain = plaintext[:13]
                ct, _ = reference_encrypt(short_plain, alphabet, equation, source,
                                          planted, 3, bases, geometry)
                _, rows = transition_rows(short_plain, ct, alphabet, equation, source, vectors)
                retained = survivors(rows, 26)
                assert planted in retained
                exhaustive_positive_checks.append({"alphabet": alphabet_name, "equation": equation,
                                                     "source": source, "survivor_count": len(retained),
                                                     "planted": list(planted)})

    # A deliberately wrong pre-update encryption must differ on a pinned test.
    alphabet = spec["alphabets"]["AZ"]
    p, initial, params, base = "E", 3, (5, 7, 11), 2
    correct, trace = reference_encrypt(p, alphabet, "additive", "plaintext", params,
                                       initial, [base], geometry)
    wrong_advanced = (params[0] * initial + params[1] +
                      params[2] * code_mod(vectors[p], base)) % 26
    wrong = alphabet[(alphabet.index(p) + wrong_advanced) % 26]
    assert correct == "H" and wrong != correct and trace[0] == initial
    return {"status": "PASS", "vector_reconstruction_letters": len(vectors),
            "polynomial_parity_periodicity_checks": evaluation_checks,
            "always_even_glyphs": "".join(sorted(always_even)),
            "odd_code_counterexamples": counterexamples,
            "roundtrip_cases": roundtrips, "letters_per_roundtrip": n,
            "parity_solver_plants_retained": parity_retained,
            "mod26_plants_retained": exact_retained,
            "full_mod26_positive_solves": exhaustive_positive_checks,
            "base_schedule_names": list(schedules), "parameter_triples_per_schedule": len(params_list),
            "alignment_mutation": {"correct_first_ciphertext": correct,
                                    "wrong_preupdate_ciphertext": wrong,
                                    "initial_key": initial, "wrong_advanced_key": wrong_advanced,
                                    "mutation_detected": True}}


def main():
    if not __debug__:
        raise RuntimeError("Run without -O or PYTHONOPTIMIZE; the audit requires assertions.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="results.replay.json")
    args = parser.parse_args()
    geometry, spec, vectors = load_verified()
    full_ct = spec["ciphertext"]
    start, end = spec["plaintext_training_crib"]["positions_1_based_inclusive"]
    plaintext = spec["plaintext_training_crib"]["text"]
    ciphertext = full_ct[start - 1:end]
    assert len(full_ct) == 97 and len(plaintext) == len(ciphertext) == 13
    assert ciphertext == "FLRVQQPRNGKSS"
    controls = run_controls(geometry, spec, vectors)
    families = []
    for alphabet_name, alphabet in spec["alphabets"].items():
        assert len(alphabet) == len(set(alphabet)) == 26
        for equation in ["additive", "beaufort"]:
            for source in ["ciphertext", "plaintext"]:
                keys, rows = transition_rows(plaintext, ciphertext, alphabet, equation, source, vectors, start)
                parity = survivors(rows, 2)
                exact = survivors(rows, 26)
                certificate = minimum_certificate(rows) if not parity else []
                verification = independent_certificate_verification(certificate) if certificate else []
                assert not parity and not exact and len(certificate) == 2
                families.append({"alphabet": alphabet_name, "equation": equation, "source": source,
                                 "key_sequence": keys, "transition_count": len(rows),
                                 "parity_survivors": parity, "mod26_survivor_count": len(exact),
                                 "minimum_certificate": certificate,
                                 "certificate_all_parity_triples_check": verification,
                                 "all_training_transitions": rows})

    auxiliary = []
    allowed_bases = spec["auxiliary_closure_check"]["allowed_bases"]
    for alphabet_name, alphabet in spec["alphabets"].items():
        positions = []
        for offset, (p, c) in enumerate(zip(plaintext, ciphertext)):
            target = alphabet.index(c)
            bases = [b for b in allowed_bases if code_mod(vectors[p], b) == target]
            positions.append({"position": start + offset, "plaintext": p, "ciphertext": c,
                              "target_index": target, "compatible_bases": bases,
                              "attainable_code_residues": sorted({code_mod(vectors[p], b)
                                                                   for b in allowed_bases})})
        auxiliary.append({"alphabet": alphabet_name,
                          "possible": all(row["compatible_bases"] for row in positions),
                          "impossible_positions": [row["position"] for row in positions
                                                   if not row["compatible_bases"]],
                          "positions": positions})
    result = {"audit_id": spec["audit_id"], "geometry_sha256": GEOMETRY_SHA,
              "specification_sha256": SPEC_SHA, "schema_amendment_sha256": AMENDMENT_SHA,
              "training": {"positions": [start, end], "plaintext": plaintext, "ciphertext": ciphertext},
              "controls": controls, "families": families,
              "primary_result": "All eight specified families excluded modulo 2 for every independent integer-base schedule b_i>=2.",
              "heldout_evaluated": False, "root_or_digit_search_performed": False,
              "auxiliary_direct_map": auxiliary,
              "limits": "Only frozen-glyph first-order affine feature feedback, these two equations, two alphabets and two source choices. No claim about other geometries, feature orders, states, feedback laws or all root-driven ciphers."}
    output = Path(args.output)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS: 8/8 families excluded modulo 2 and modulo 26; %d synthetic roundtrips passed." %
          controls["roundtrip_cases"])
    print("Heldout untouched; no root/digit search. Results:", output.resolve())
    print("SHA256:", sha(output))


if __name__ == "__main__":
    main()
