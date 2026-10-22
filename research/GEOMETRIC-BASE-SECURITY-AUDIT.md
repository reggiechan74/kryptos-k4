# Changing-base geometric codes — finite raw-number security audit

22 October 2026. Under the specified raw-token model, a secret root-digit schedule
usually fails to hide either the letter or its weight base. This is a finite
encoding/security audit, not a K4 solution test, root search or general theorem
about every changing-base cipher.

## Exact model and threat assumptions

Use the unchanged public binary vectors and feature order from
[MODELED-UPPERCASE-GEOMETRY-001](../data/alphabet-skeleton-v1.json), SHA-256
`6a5c6eae644dedf88afb68df911f0c3161a969af3815972aa5694479155aa010`.
At a letter position a root digit d chooses the integer weight base b=d+2.
Emit the exact number `N=sum(v_letter[i]*b**i)`, with i=0–34.

This audit assumes the attacker knows that geometry/order and the digit radix,
and sees each exact integer with its token boundary. No extra secret arithmetic,
packing, framing, permutation or cipher layer is present. The audited root-digit
radices are 10, 12, 16 and 60; their weight-base ranges are respectively 2–11,
2–13, 2–17 and 2–61. No root, degree, digit sequence, starting offset or root
parameter is guessed. Root digits need not be uniform or independent.

## Exhaustive finite lookup result

| Root-digit radix | Weight bases | Letter/base pairs | Distinct numbers | Ambiguous numbers |
| ---: | --- | ---: | ---: | --- |
| 10 | 2–11 | 260 | 259 | 8 |
| 12 | 2–13 | 312 | 311 | 8 |
| 16 | 2–17 | 416 | 415 | 8 |
| 60 | 2–61 | 1,560 | 1,558 | 8 and 27 |

Every number outside those collision classes identifies both its letter and base
within the stated range, without knowing the root. The complete ambiguities are:

- `8 = code(C,2) = code(O,8)`.
- `27 = code(C,3) = code(O,27)`; base 27 occurs only in the largest audited range.

Here C occupies only component 3, so its code is b^3; O occupies only component 1,
so its code is b. There are no same-base letter collisions. All 1,560 pairs and
every inverse candidate are preserved in the largest complete lookup. These
finite counts are not percentages of arbitrary messages: message frequencies,
root-digit distributions and contextual disambiguation were not modeled.

The exact arithmetic is arbitrary-precision Python integer arithmetic. Values
are serialized as decimal strings. Direct polynomial evaluation, Horner's rule
and radix decoding agree for every enumerated pair. The separately implemented
repository codec independently rebuilds and matches every lookup in all four
ranges. Bases outside those ranges and changed glyphs are not covered.

## Artifacts, replay and limitations

The original source, full lookup, compact report and frozen core are preserved
unchanged in `independent/2026-10-22/geometric-base-security/`. The received ZIP
had SHA-256 `90651d68c4e1a0740b8a67085c795e2085780fc0a92b9b7997da6ff0078291fe`.
The [transfer/replay receipt](../results/GEOMETRIC-FOLLOWUP-LOCAL-REPLAY.json)
records all member hashes; both supplied JSON artifacts replay exactly. The complete regression suite passes
261 tests in 9.635 seconds.

```sh
python3 independent/2026-10-22/geometric-base-security/geometric-base-schedule-audit.py \
  --output /tmp/geometric-base-security-replay.json
python3 experiments/geometric_followup_checks.py
```

The [local comparison](../results/GEOMETRIC-FOLLOWUP-COMPARISON.json) includes
complete lookup equality and all collision classes. The independent K4 pilot
oracle was replayed separately, including all-family round trips and ambiguous
planted recovery; see [pilot findings](GEOMETRIC-PILOT-FINDINGS.md).

This result identifies a weakness in emitting these exact raw numeric tokens.
It neither recovers a secret root nor evaluates a later cryptographic transform.
A proposed modular arithmetic use on K4 requires its own frozen admissibility
specification. No root, offset, extra transform or new K4 family was searched in
this audit, and canonical ciphertext and public cribs remain unchanged.

## Later arithmetic follow-up — 22 October 2026

The separately frozen [radix-feedback audit](RADIX-FEEDBACK-FINDINGS.md) now
completes the pending modular-arithmetic admissibility step described above.
All eight named first-order affine feature-feedback families fail inside the
first crib, even under arbitrary independent integer bases. This is a separate
exact-proof result and leaves the raw-token security audit's assumptions and
scope unchanged. No root or root-offset search was performed.
