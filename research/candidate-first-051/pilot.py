#!/usr/bin/env python3
"""Candidate-first pilot 051. Standard-library implementation, no network.

This module never contains or retrieves K4. See PROTOCOL.md for the frozen test.
Keys have AZ residue labels even when a tableau uses the keyed alphabet.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import math
import os
import platform
import random
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KR = "".join(dict.fromkeys("KRYPTOS" + AZ))
ALPHABETS = {"AZ": AZ, "KR": KR}
LENGTH = 97
CRIBS = ((21, "EASTNORTHEAST"), (63, "BERLINCLOCK"))
KNOWN = frozenset(i for start, word in CRIBS for i in range(start, start + len(word)))
UNKNOWN = tuple(i for i in range(LENGTH) if i not in KNOWN)
N = len(UNKNOWN)
UMASK = sum(1 << i for i in UNKNOWN)
PERIODS = tuple(range(1, 33))
STRUCTURES = ("periodic", "plaintext_autokey", "ciphertext_autokey")
OPERATIONS = ("vigenere", "beaufort", "variant_beaufort")
LOG26 = math.log2(26)
LOG25 = math.log2(25)
CHOICE_BITS = math.log2(32) + math.log2(12 * 3 * 32)
BASELINE_BITS = N * LOG26
GROUPS = {r: tuple(tuple(i for i in UNKNOWN if i % r == j) for j in range(r)) for r in PERIODS}
TAIL_N = {r: sum(i >= r for i in UNKNOWN) for r in PERIODS}
ROOT = Path(__file__).resolve().parent


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def load_json(path):
    return json.loads(Path(path).read_text())


def letters(text):
    return "".join(c for c in text.upper() if c in AZ)


def validate_ciphertext(text):
    if len(text) != LENGTH or any(c not in AZ for c in text):
        raise ValueError("Ciphertext must already be exactly 97 A-Z letters")
    return text


def validate_bank(records):
    if len(records) != 32:
        raise ValueError("Exactly 32 candidates required")
    seen_ids, seen_text = set(), set()
    groups = {"thematic": 0, "neutral": 0}
    for item in records:
        if not isinstance(item.get("id"), str) or not item["id"] or item["id"] in seen_ids:
            raise ValueError("Candidate IDs must be unique nonempty strings")
        seen_ids.add(item["id"])
        text = validate_ciphertext(item["text"])
        if text in seen_text:
            raise ValueError("Duplicate plaintext candidate")
        seen_text.add(text)
        if item.get("group") not in groups:
            raise ValueError("Candidate group must be thematic or neutral")
        groups[item["group"]] += 1
        for start, word in CRIBS:
            if text[start:start + len(word)] != word:
                raise ValueError(f"Wrong crib placement in {item['id']}")
    if groups != {"thematic": 16, "neutral": 16}:
        raise ValueError("Require exactly 16 thematic and 16 neutral candidates")
    return sorted(records, key=lambda x: x["id"])


@dataclass(frozen=True)
class Tableau:
    plain_alphabet: str
    cipher_alphabet: str
    operation: str

    @property
    def id(self):
        return f"{self.plain_alphabet}-{self.cipher_alphabet}-{self.operation}"


TABLEAUX = tuple(Tableau(p, c, op) for p in ALPHABETS for c in ALPHABETS for op in OPERATIONS)
TABLEAU_BY_ID = {t.id: t for t in TABLEAUX}


def encode(text, alphabet):
    lookup = {c: i for i, c in enumerate(ALPHABETS[alphabet])}
    return tuple(lookup[c] for c in text)


def decode(values, alphabet):
    a = ALPHABETS[alphabet]
    return "".join(a[v % 26] for v in values)


def forward(p, q, operation):
    if operation == "vigenere":
        return (p + q) % 26
    if operation == "beaufort":
        return (q - p) % 26
    if operation == "variant_beaufort":
        return (p - q) % 26
    raise ValueError(operation)


def backward(c, q, operation):
    if operation == "vigenere":
        return (c - q) % 26
    if operation == "beaufort":
        return (q - c) % 26
    if operation == "variant_beaufort":
        return (c + q) % 26
    raise ValueError(operation)


def induced(p, c, operation):
    if operation == "vigenere":
        return tuple((b - a) % 26 for a, b in zip(p, c))
    if operation == "beaufort":
        return tuple((b + a) % 26 for a, b in zip(p, c))
    if operation == "variant_beaufort":
        return tuple((a - b) % 26 for a, b in zip(p, c))
    raise ValueError(operation)


def encrypt_key(plaintext, key, tableau):
    p = encode(plaintext, tableau.plain_alphabet)
    if len(p) != len(key):
        raise ValueError("Full keystream length must equal plaintext length")
    return decode((forward(a, q, tableau.operation) for a, q in zip(p, key)), tableau.cipher_alphabet)


def decrypt_key(ciphertext, key, tableau):
    c = encode(ciphertext, tableau.cipher_alphabet)
    if len(c) != len(key):
        raise ValueError("Full keystream length must equal ciphertext length")
    return decode((backward(b, q, tableau.operation) for b, q in zip(c, key)), tableau.plain_alphabet)


def encrypt_structured(plaintext, seed, tableau, structure):
    if not seed:
        raise ValueError("Seed must not be empty")
    p = encode(plaintext, tableau.plain_alphabet)
    c, key = [], []
    r = len(seed)
    for i, a in enumerate(p):
        if structure == "periodic":
            q = seed[i % r]
        elif i < r:
            q = seed[i]
        elif structure == "plaintext_autokey":
            q = p[i - r]
        elif structure == "ciphertext_autokey":
            q = c[i - r]
        else:
            raise ValueError(structure)
        key.append(q)
        c.append(forward(a, q, tableau.operation))
    return decode(c, tableau.cipher_alphabet), tuple(key)


def decrypt_structured(ciphertext, seed, tableau, structure):
    if not seed:
        raise ValueError("Seed must not be empty")
    c = encode(ciphertext, tableau.cipher_alphabet)
    p = []
    r = len(seed)
    for i, b in enumerate(c):
        if structure == "periodic":
            q = seed[i % r]
        elif i < r:
            q = seed[i]
        elif structure == "plaintext_autokey":
            q = p[i - r]
        elif structure == "ciphertext_autokey":
            q = c[i - r]
        else:
            raise ValueError(structure)
        p.append(backward(b, q, tableau.operation))
    return decode(p, tableau.plain_alphabet)


def residual_bits(n, e):
    if not 0 <= e <= n:
        raise ValueError((n, e))
    return math.log2(n + 1) + math.log2(math.comb(n, e)) + e * LOG25


def description_score(r, n, e):
    return BASELINE_BITS - CHOICE_BITS - r * LOG26 - residual_bits(n, e)


PERIOD_SCORES = {r: tuple(description_score(r, N, e) for e in range(N + 1)) for r in PERIODS}
AUTO_SCORES = {r: tuple(description_score(r, TAIL_N[r], e) for e in range(TAIL_N[r] + 1)) for r in PERIODS}


def mode(values):
    counts = [0] * 26
    for v in values:
        counts[v] += 1
    return max(range(26), key=lambda v: (counts[v], -v))


def periodic_errors(q, r):
    errors = 0
    for positions in GROUPS[r]:
        counts = {}
        best = 0
        for i in positions:
            v = q[i]
            count = counts.get(v, 0) + 1
            counts[v] = count
            if count > best:
                best = count
        errors += len(positions) - best
    return errors


def bitmasks(values, positions=range(LENGTH)):
    masks = [0] * 26
    for i in positions:
        masks[values[i]] |= 1 << i
    return tuple(masks)


def reference_description(q, p, c, structure, r):
    """Unoptimized score and explicit description; used for audits and test oracle."""
    if structure == "periodic":
        seed = tuple(mode(q[i] for i in GROUPS[r][j]) for j in range(r))
        template = tuple(seed[i % r] for i in range(LENGTH))
        scored_positions = UNKNOWN
    else:
        seed = tuple(q[:r])
        source = p if structure == "plaintext_autokey" else c
        template = tuple(q[i] if i < r else source[i - r] for i in range(LENGTH))
        scored_positions = tuple(i for i in UNKNOWN if i >= r)
    residuals = [i for i in range(LENGTH) if q[i] != template[i]]
    scored_residuals = [i for i in scored_positions if q[i] != template[i]]
    n, e = len(scored_positions), len(scored_residuals)
    return {
        "structure": structure,
        "r": r,
        "score_bits": description_score(r, n, e),
        "literal_baseline_bits": BASELINE_BITS,
        "choice_bits": CHOICE_BITS,
        "seed_bits": r * LOG26,
        "residual_bits": residual_bits(n, e),
        "n_scored": n,
        "mismatch_count_scored": e,
        "seed_AZ": decode(seed, "AZ"),
        "full_key_AZ": decode(q, "AZ"),
        "template_key_AZ": decode(template, "AZ"),
        "residual_positions_1based": [i + 1 for i in residuals],
        "scored_residual_positions_1based": [i + 1 for i in scored_residuals],
        "crib_residual_positions_1based": [i + 1 for i in residuals if i in KNOWN],
        "exact_full_fit": not residuals,
    }


class Scorer:
    def __init__(self, bank):
        self.bank = validate_bank(bank)
        self.plain = [{a: encode(rec["text"], a) for a in ALPHABETS} for rec in self.bank]
        self.plain_masks = [{a: bitmasks(self.plain[j][a]) for a in ALPHABETS} for j in range(32)]

    def score(self, ciphertext, details=False):
        """Exact maximum over the frozen bank/model family. No pruning/crib exclusions."""
        validate_ciphertext(ciphertext)
        cipher = {a: encode(ciphertext, a) for a in ALPHABETS}
        cipher_masks = {a: bitmasks(cipher[a]) for a in ALPHABETS}
        candidate_best = []
        global_best = float("-inf")
        for j, record in enumerate(self.bank):
            best = None
            tied_descriptions = []
            for t in TABLEAUX:
                p, c = self.plain[j][t.plain_alphabet], cipher[t.cipher_alphabet]
                q = induced(p, c, t.operation)
                q_masks = bitmasks(q, UNKNOWN)
                for r in PERIODS:
                    e = periodic_errors(q, r)
                    score = PERIOD_SCORES[r][e]
                    item = (score, t.id, "periodic", r)
                    if best is None or item[0] > best[0]:
                        tied_descriptions = [item]
                    elif item[0] == best[0]:
                        tied_descriptions.append(item)
                    if best is None or self._better(item, best):
                        best = item
                for structure, source_masks in (
                    ("plaintext_autokey", self.plain_masks[j][t.plain_alphabet]),
                    ("ciphertext_autokey", cipher_masks[t.cipher_alphabet]),
                ):
                    for r in PERIODS:
                        matches = sum((a & (b << r)).bit_count() for a, b in zip(q_masks, source_masks))
                        e = TAIL_N[r] - matches
                        score = AUTO_SCORES[r][e]
                        item = (score, t.id, structure, r)
                        if item[0] > best[0]:
                            tied_descriptions = [item]
                        elif item[0] == best[0]:
                            tied_descriptions.append(item)
                        if self._better(item, best):
                            best = item
            entry = {"candidate_id": record["id"], "group": record["group"], "score_bits": best[0],
                     "tableau_id": best[1], "structure": best[2], "r": best[3],
                     "equal_score_top_descriptions": [{"tableau_id": x[1], "structure": x[2], "r": x[3]}
                                                        for x in sorted(tied_descriptions, key=lambda x:x[1:])]}
            candidate_best.append(entry)
            global_best = max(global_best, best[0])
        candidate_best.sort(key=lambda x: (-x["score_bits"], x["candidate_id"], x["tableau_id"], x["structure"], x["r"]))
        if not details:
            return global_best
        for entry in candidate_best:
            record = next(x for x in self.bank if x["id"] == entry["candidate_id"])
            t = TABLEAU_BY_ID[entry["tableau_id"]]
            p, c = encode(record["text"], t.plain_alphabet), cipher[t.cipher_alphabet]
            q = induced(p, c, t.operation)
            diagnostic = reference_description(q, p, c, entry["structure"], entry["r"])
            if abs(diagnostic["score_bits"] - entry["score_bits"]) > 1e-10:
                raise AssertionError("Optimized/reference score mismatch")
            entry.update(diagnostic)
            entry["plaintext"] = record["text"]
        tied = [x["candidate_id"] for x in candidate_best if abs(x["score_bits"] - global_best) < 1e-10]
        return {"maximum_score_bits": global_best, "ranked_candidates": candidate_best,
                "tied_top_candidate_ids": tied,
                "different_plaintext_margin_bits": candidate_best[0]["score_bits"] - candidate_best[1]["score_bits"]}

    @staticmethod
    def _better(a, b):
        return a[0] > b[0] or (a[0] == b[0] and a[1:] < b[1:])


def exact_diagnostics(bank, ciphertext):
    """Every bank/tableau full-stream inverse check and exact mechanism diagnostic."""
    results = []
    for rec in validate_bank(bank):
        for t in TABLEAUX:
            p, c = encode(rec["text"], t.plain_alphabet), encode(ciphertext, t.cipher_alphabet)
            q = induced(p, c, t.operation)
            if encrypt_key(rec["text"], q, t) != ciphertext:
                raise AssertionError("Full re-encryption failed")
            if decrypt_key(ciphertext, q, t) != rec["text"]:
                raise AssertionError("Full inverse failed")
            periods = [r for r in range(1, LENGTH + 1) if all(q[i] == q[i % r] for i in range(LENGTH))]
            pa = [r for r in PERIODS if all(q[i] == p[i - r] for i in range(r, LENGTH))]
            ca = [r for r in PERIODS if all(q[i] == c[i - r] for i in range(r, LENGTH))]
            excluded_periods = [r for r in PERIODS if any(q[i] != q[j] for i in KNOWN for j in KNOWN if i % r == j % r)]
            excluded_pa = [r for r in PERIODS if any(q[i] != p[i - r] for i in KNOWN if i >= r and i - r in KNOWN)]
            # At a known plaintext output, the inferred key is fixed; all ciphertext inputs are observed.
            excluded_ca = [r for r in PERIODS if any(q[i] != c[i - r] for i in KNOWN if i >= r)]
            results.append({"candidate_id": rec["id"], "tableau_id": t.id,
                            "minimum_exact_period": min(periods),
                            "registered_exact_periods": [r for r in periods if r <= 32],
                            "exact_plaintext_autokey_lengths": pa,
                            "exact_ciphertext_autokey_lengths": ca,
                            "crib_excluded_periods": excluded_periods,
                            "crib_excluded_plaintext_autokey_lengths": excluded_pa,
                            "crib_excluded_ciphertext_autokey_lengths": excluded_ca,
                            "full_reencryption": True, "full_inverse": True})
    return results


def conditioned_null(ciphertext, rng):
    out = list(ciphertext)
    unknown_values = [out[i] for i in UNKNOWN]
    rng.shuffle(unknown_values)
    for i, value in zip(UNKNOWN, unknown_values):
        out[i] = value
    return "".join(out)


def rng_for(label):
    seed = int.from_bytes(hashlib.sha256(("candidate-first-051-v1|" + label).encode()).digest(), "big")
    return random.Random(seed)


def pvalue(value, calibration):
    return (1 + sum(x >= value for x in calibration)) / (len(calibration) + 1)


def flag(value, p, alpha=0.05):
    return value >= 16.0 and p <= alpha


WORKER_SCORER = None


def init_worker(bank):
    global WORKER_SCORER
    WORKER_SCORER = Scorer(bank)


def score_worker(ciphertext):
    return WORKER_SCORER.score(ciphertext)


def run_nulls(bank, ciphertext, count, label, executor=None):
    rng = rng_for(label)
    ciphertexts = [conditioned_null(ciphertext, rng) for _ in range(count)]
    if executor is None:
        scorer = Scorer(bank)
        maxima = [scorer.score(c) for c in ciphertexts]
    else:
        maxima = list(executor.map(score_worker, ciphertexts, chunksize=2))
    return {"label": label, "count": count,
            "ciphertext_sha256": [hashlib.sha256(c.encode()).hexdigest() for c in ciphertexts],
            "maximum_scores_bits": maxima}


def environment_record():
    return {"python": sys.version, "platform": platform.platform(), "cpu_count": os.cpu_count(),
            "utc": datetime.now(timezone.utc).isoformat()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate-bank")
    validate.add_argument("bank")
    benchmark = sub.add_parser("benchmark")
    benchmark.add_argument("bank")
    benchmark.add_argument("--iterations", type=int, default=1)
    args = parser.parse_args()
    if args.command == "validate-bank":
        bank = validate_bank(load_json(args.bank))
        print(json.dumps({"validated": len(bank), "sha256": sha256_file(args.bank)}, indent=2))
    elif args.command == "benchmark":
        bank = validate_bank(load_json(args.bank))
        rng = rng_for("benchmark-random-cipher-not-k4")
        ciphertext = "".join(rng.choice(AZ) for _ in range(LENGTH))
        scorer = Scorer(bank)
        start = time.monotonic()
        for _ in range(args.iterations):
            result = scorer.score(ciphertext)
        print(json.dumps({"iterations": args.iterations, "seconds": time.monotonic()-start,
                          "maximum": result, "environment": environment_record()}, indent=2))


if __name__ == "__main__":
    main()
