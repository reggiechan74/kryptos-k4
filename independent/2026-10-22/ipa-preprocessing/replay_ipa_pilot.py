#!/usr/bin/env python3
"""Independent scratch replay of the frozen IPA feasibility pilots; stdlib only."""
import json
from pathlib import Path
from itertools import combinations
ROOT = Path(__file__).resolve().parent
BASE = json.loads((ROOT / "ipa-feasibility-001.json").read_text())
SPEC = json.loads((ROOT / "ipa-feasibility-001b-spec.json").read_text())
EXPECTED = json.loads((ROOT / "ipa-feasibility-001b-results.json").read_text())
STRINGS = BASE["representations"][1]["strings"]
CIPHERTEXT = BASE["baseline"]["ciphertext"]
STARTS = BASE["crib_offsets_zero_based"]
FIXED = SPEC["fixed_ascii_identity"]

def records(ciphertexts):
    return [(start + j, ch, c[j]) for start, s, c in zip(STARTS, STRINGS, ciphertexts)
            for j, ch in enumerate(s)]

def anchor_conflicts(rows, alphabet, family, period):
    first, conflicts = {}, []
    sign = 1 if family == "true Beaufort" else -1
    for i, ch, cipher in rows:
        if ch not in FIXED:
            continue
        p, c = alphabet.index(FIXED[ch]), alphabet.index(cipher)
        k, phase = (c + sign * p) % 26, i % period
        row = {"i": i, "position": i + 1, "symbol": ch,
               "cipher": cipher, "P": p, "C": c, "K": k}
        if phase in first and first[phase]["K"] != k:
            conflicts.append({"phase": phase, "first": first[phase], "second": row})
        elif phase not in first:
            first[phase] = row
    return conflicts

def periodic_conflicts(rows, period):
    same_source, same_cipher = [], []
    for a, b in combinations(rows, 2):
        if (b[0] - a[0]) % period:
            continue
        if a[1] == b[1] and a[2] != b[2]:
            same_source.append((a, b))
        if a[1] != b[1] and a[2] == b[2]:
            same_cipher.append((a, b))
    return same_source, same_cipher

def main():
    assert len(CIPHERTEXT) == 97
    slices = [CIPHERTEXT[start:start + len(s)] for start, s in zip(STARTS, STRINGS)]
    assert slices == ["FLRVQQPRNGKSS", "NYPVTTMZFPK"]
    assert [len(s) for s in STRINGS] == [13, 11]
    assert [len(t) for t in BASE["representations"][0]["tokens"]] == [10, 9]
    assert [len(s.encode("utf-8")) for s in STRINGS] == [18, 16]
    assert [len(json.dumps(s, ensure_ascii=True)[1:-1]) for s in STRINGS] == [38, 36]
    for s in STRINGS:
        assert json.loads(json.dumps(s, ensure_ascii=True)) == s

    # This established ASCII codec is a contrast/control, not another pronunciation.
    xsampa = {"ː": ":", "ɔ": "O", "θ": "T", "ɝ": "3`", "ɪ": "I", "ɑ": "A"}
    serialized = ["".join(xsampa.get(c, c) for c in s) for s in STRINGS]
    assert serialized == ["i:stnO:rTi:st", "b3`:lInklA:k"]
    assert list(map(len, serialized)) == [13, 12]
    # Exact reverse on the observed source-symbol subset; longest codes first.
    inverse = {v: k for k, v in xsampa.items()}
    def reverse_xsampa(s):
        out, i = [], 0
        while i < len(s):
            code = next((x for x in sorted(inverse, key=len, reverse=True)
                         if s.startswith(x, i)), s[i])
            out.append(inverse.get(code, code))
            i += len(code)
        return "".join(out)
    assert [reverse_xsampa(s) for s in serialized] == STRINGS

    rows = records(slices)
    for expected in BASE["results"]["periodic_constraints"]:
        a, b = periodic_conflicts(rows, expected["period"])
        assert len(a) == expected["deterministic_contradictions"]
        assert len(b) == expected["injectivity_contradictions"]
    for expected in EXPECTED["certificates"]:
        conflicts = anchor_conflicts(rows, expected["alphabet"],
                                     expected["family"], expected["period"])
        assert conflicts
        assert len(conflicts) == expected["contradiction_count"]
        assert conflicts[0] == expected["first_certificate"]

    # Synthetic cipher controls use a fixed arbitrary mapping only to test code.
    # This mapping is never fitted to K4 and is not claimed as a historical codec.
    remaining = [c for c in SPEC["alphabets"][0] if c not in FIXED.values()]
    mapping = dict(FIXED, **dict(zip(SPEC["special_glyphs"], remaining)))
    controls = 0
    for alphabet in SPEC["alphabets"]:
        for family in [f["name"] for f in SPEC["families"]]:
            for period in SPEC["periods"]:
                key = [(j * 7 + 3) % 26 for j in range(period)]
                output, recovered = [], []
                for start, s in zip(STARTS, STRINGS):
                    encrypted, decrypted = [], []
                    for j, ch in enumerate(s):
                        p, k = alphabet.index(mapping[ch]), key[(start+j) % period]
                        c = (k-p) % 26 if family == "true Beaufort" else (p+k) % 26
                        q = (k-c) % 26 if family == "true Beaufort" else (c-k) % 26
                        encrypted.append(alphabet[c])
                        decrypted.append(alphabet[q])
                    output.append("".join(encrypted))
                    recovered.append("".join(decrypted))
                assert recovered == ["".join(mapping[c] for c in s) for s in STRINGS]
                assert not anchor_conflicts(records(output), alphabet, family, period)
                # Position22 and position34 share phase for period12; corrupt the
                # second ordinary anchor to verify rejection without a special map.
                if period == 12:
                    bad = output[:]
                    bad[0] = bad[0][:-1] + alphabet[(alphabet.index(bad[0][-1])+1) % 26]
                    assert anchor_conflicts(records(bad), alphabet, family, period)
                controls += 1
    print(json.dumps({"status": "pass", "k4_structures_rejected": 48,
                      "k4_special_assignments_enumerated": 0,
                      "synthetic_cipher_roundtrips": controls,
                      "mutation_negative_controls": 4,
                      "ascii_storage_roundtrips": 2,
                      "xsampa_subset_roundtrips": 2,
                      "xsampa_lengths": list(map(len, serialized))}, indent=2))

if __name__ == "__main__":
    main()

