# SILK-PERIODIC-001: fixed table, hypothetical periods 1–12

All 12 registered periods are contradicted. No keywords were enumerated and no
full K4 plaintext was generated. This excludes only direct, position-preserving
use of the pinned photographed chart with a key repeating every 1–12 letters.
It says nothing about other tables, nonperiodic/OTP keys, longer periods, masks,
routes, transposition, or additional layers. Historical creator use is unestablished.
[Source review](../docs/silk-chart-source-and-scope.md).

## Exact proof

Unique required keys for the 24 confirmed plaintext/ciphertext pairs are:

- positions 22–34: `JICEHTUFLMSXZ`
- positions 64–74: `TCUFDISXLFX`

The first segment has 13 distinct keys in 13 consecutive positions. For every
period p from 1 through 12, positions 22 and 22+p have the same repeating-key
phase yet require different keys. Shifting the global phase origin cannot change
this equality. All witnesses are below; the raw artifact also records every phase
constraint and conflict from both cribs.

| Period | Positions (one-based) | Required keys |
| --- | --- | --- |
| 1 | 22, 23 | J, I |
| 2 | 22, 24 | J, C |
| 3 | 22, 25 | J, E |
| 4 | 22, 26 | J, H |
| 5 | 22, 27 | J, T |
| 6 | 22, 28 | J, U |
| 7 | 22, 29 | J, F |
| 8 | 22, 30 | J, L |
| 9 | 22, 31 | J, M |
| 10 | 22, 32 | J, S |
| 11 | 22, 33 | J, X |
| 12 | 22, 34 | J, Z |

This deduction and the independent 24-cell verification were known before the
specification. The run reproduces a sourced constraint; it is not a blind discovery.

## Reproduction and checks

Specification commit: `bb0cfb9c0cd9c75b13782c1cc11cf34535e0fdd9`
(2026-10-18 15:28:30 UTC). Implementation commit:
`f82749aa22e14c063d8fc3c02ff4e6f2a381c616` (15:32:17 UTC), directly
following the specification. The run began at 15:32:21.428512 UTC.

```sh
python3 experiments/silk_periodic.py --spec-commit bb0cfb9c0cd9c75b13782c1cc11cf34535e0fdd9 --code-commit f82749aa22e14c063d8fc3c02ff4e6f2a381c616
python3 -m unittest discover -s tests -v
```

One process, registered cap 5 seconds, recorded action time 0.003 seconds;
no randomness or third-party executable code. Controls check 26 row permutations,
26 column permutations, 676 reciprocal cells and 676 roundtrips, the corrected
modern example, all 24 independently checked cells, 39 exhaustive toy-key
roundtrips, 117 shifted positive and 117 shifted negative cases. A single observation
with 11 free phases remains compatible, guarding against false rejection.
All **118 tests pass in 8.744 seconds**, preserving the previous 112 tests.
A fresh audit replay matches every proof-bearing field, and the raw artifact's
SHA256 matches its manifest. Input hashes are included in run metadata.

[Raw snapshot](../results/silk-periodic-runs/20261018T153221Z-b7f6cad7292747f6ba81099de8a671e1/SILK-PERIODIC-001.json),
[manifest](../results/silk-periodic-runs/20261018T153221Z-b7f6cad7292747f6ba81099de8a671e1/manifest.json),
[validation and chronology](../results/SILK-PERIODIC-VALIDATION.json).
The source receipt explicitly distinguishes 24-cell pixel verification from full
computational table checks. Stop at this proof. No period extension, alternate
schedule or keyword search is justified by this negative alone.
