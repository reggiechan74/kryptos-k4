#!/usr/bin/env python3
"""Exact audit of C(letter, base) = sum(feature[i] * base**i).

This is a finite codebook attack, not a root-digit generator or a K4 test.
The feature order and glyphs are frozen by the model's SHA-256 checksum.
All arithmetic is Python arbitrary-precision integer arithmetic. Decimal
code values in the JSON artifact are strings to prevent consumer rounding.
"""

import argparse
from collections import Counter, defaultdict
import hashlib
import itertools
import json
from pathlib import Path


EXPECTED_SHA256 = "6a5c6eae644dedf88afb68df911f0c3161a969af3815972aa5694479155aa010"
DEFAULT_MODEL = Path(__file__).with_name("modeled-uppercase-geometry-001-core.json")
DEFAULT_RESULT = Path(__file__).with_suffix(".json")


def load_vectors(path):
    data = path.read_bytes()
    actual = hashlib.sha256(data).hexdigest()
    if actual != EXPECTED_SHA256:
        raise ValueError(f"Model checksum mismatch: {actual}")
    model = json.loads(data)
    order = model["feature_order"]
    assert len(order) == len(set(order)) == 35
    assert set(model["glyphs"]) == set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    vectors = {}
    for letter, features in sorted(model["glyphs"].items()):
        counts = Counter(features)
        assert set(counts) <= set(order)
        vector = tuple(counts[feature] for feature in order)
        assert set(vector) <= {0, 1}
        assert any(vector[1:]), "Strict monotonicity requires a positive exponent."
        vectors[letter] = vector
    assert len(set(vectors.values())) == 26
    return model, vectors, actual


def encode(vector, base):
    # Independent evaluations cross-check feature/exponent order.
    direct = sum(value * base**index for index, value in enumerate(vector))
    horner = 0
    for value in reversed(vector):
        horner = horner * base + value
    assert direct == horner
    decoded = []
    remaining = direct
    for _ in vector:
        remaining, digit = divmod(remaining, base)
        decoded.append(digit)
    assert remaining == 0 and tuple(decoded) == vector
    return direct


def audit(vectors, digit_radix):
    candidates = defaultdict(list)
    bases = range(2, digit_radix + 2)
    for base in bases:
        at_base = set()
        for letter, vector in vectors.items():
            code = encode(vector, base)
            assert code not in at_base, "A fixed-base letter collision is invalid."
            at_base.add(code)
            candidates[code].append({"letter": letter, "base": base})
    classes = []
    pair_counts = Counter()
    for code, entries in sorted(candidates.items()):
        if len(entries) < 2:
            continue
        classes.append({"code": str(code), "candidates": entries})
        for left, right in itertools.combinations(entries, 2):
            pair_counts["all"] += 1
            pair_counts["same_letter" if left["letter"] == right["letter"] else "different_letters"] += 1
            pair_counts["same_base" if left["base"] == right["base"] else "different_bases"] += 1
    ambiguous_codes = [
        entries for entries in candidates.values()
        if len({entry["letter"] for entry in entries}) > 1
    ]
    return {
        "root_digit_radix": digit_radix,
        "digit_to_weight_base": "base = digit + 2",
        "weight_bases_inclusive": [2, digit_radix + 1],
        "letter_base_pairs": 26 * digit_radix,
        "distinct_numeric_codes": len(candidates),
        "collision_classes": classes,
        "collision_class_count": len(classes),
        "colliding_unordered_pair_counts": {
            key: pair_counts[key]
            for key in ("all", "same_letter", "different_letters", "same_base", "different_bases")
        },
        "letter_ambiguous_numeric_codes": len(ambiguous_codes),
        "letter_base_pairs_with_ambiguous_letter": sum(map(len, ambiguous_codes)),
        "letter_base_pairs_uniquely_recoverable": sum(
            len(entries) for entries in candidates.values() if len(entries) == 1
        ),
        "max_candidate_letters_per_code": max(
            len({entry["letter"] for entry in entries}) for entries in candidates.values()
        ),
        "max_candidate_pairs_per_code": max(map(len, candidates.values())),
        "lookup": [
            {"code": str(code), "candidates": entries}
            for code, entries in sorted(candidates.items())
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--output", type=Path, default=DEFAULT_RESULT)
    args = parser.parse_args()
    model, vectors, actual = load_vectors(args.model)
    cases = [audit(vectors, radix) for radix in (10, 12, 16, 60)]
    result = {
        "audit_schema": "GEOMETRIC-BASE-SCHEDULE-AUDIT-001",
        "model_schema": model["schema_id"],
        "model_sha256": actual,
        "formula": "C(letter, base) = sum(v_letter[i] * base**i), i = 0..34",
        "arithmetic": "Exact arbitrary-precision integers; code values serialized as decimal strings.",
        "assumptions": [
            "The public, frozen model and feature order are known.",
            "Each observed token is the exact weighted-sum integer with known boundaries.",
            "Each position's base is its root digit plus 2; no later secret transformation is applied.",
            "Only digit radices 10, 12, 16, and 60 are audited; root parameters and digits are not needed.",
        ],
        "finding": "Inspect the enumerated collision classes for each range. Every code not in a collision class identifies both letter and base uniquely.",
        "scope_warning": "Finite-model result, not a proof of uniqueness for arbitrary bases or changed glyphs, and not a K4 result.",
        "cases": cases,
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    summary_result = {
        **result,
        "cases": [
            {key: value for key, value in case.items() if key != "lookup"}
            for case in cases
        ],
    }
    summary_path = args.output.with_name(args.output.stem + ".summary.json")
    summary_path.write_text(json.dumps(summary_result, indent=2) + "\n")
    for case in cases:
        summary = {key: value for key, value in case.items() if key != "lookup"}
        print(json.dumps(summary, sort_keys=True))
    print(f"Saved {args.output}")
    print(f"Saved {summary_path}")


if __name__ == "__main__":
    main()
