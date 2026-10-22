# Bounded K4 radix-feedback audit

## Result

All eight specified first-order affine feature-feedback families are incompatible with the public `EASTNORTHEAST` crib at positions 22–34. This remains true when every position is allowed its own unrelated integer base `b_i >= 2`, a larger choice set than any particular digit stream from pi, e, or an nth root.

The rejection is an exact parity contradiction, not a low-scoring search result. Each family has a two-transition certificate. Exhaustive modulo-26 checks independently agree. No root or digit sequence was searched and the `BERLINCLOCK` holdout was not evaluated.

This is a negative result for the explicitly defined family below, not for all geometric or root-driven ciphers. The geometry is a provisional modeled skeleton, not a measurement of the monument, and the proof depends on its frozen primitive order. No historical or global novelty claim is made.

## Frozen test

The input is `MODELED-UPPERCASE-GEOMETRY-001`, SHA256:

`6a5c6eae644dedf88afb68df911f0c3161a969af3815972aa5694479155aa010`

For each letter `T`, construct its 35-dimensional binary vector from the frozen sparse component array and frozen feature order. Define:

`code_b(T) = sum(v(T)[j] * b**j, j=0..34)`.

There are eight families, the Cartesian product of:

- Alphabet: `ABCDEFGHIJKLMNOPQRSTUVWXYZ` or `KRYPTOSABCDEFGHIJLMNQUVWXZ`.
- Letter equation: additive `C_i = P_i + K_i (mod 26)`, or true Beaufort `C_i = K_i - P_i (mod 26)`.
- Feedback source: ciphertext glyph `C_i`, or plaintext glyph `P_i`.

In every family, update **after** letter `i`:

`K_(i+1) = a*K_i + c + d*code_(b_i)(T_i) (mod 26)`.

The coefficients `a,c,d` are arbitrary but fixed residues in `0..25`. The initial state is arbitrary. Each `b_i` is an independently chosen integer at least 2. There are no resets, routes, extra masks, or changing coefficients. Allowing an arbitrary key at the crib start only relaxes the original initial-state requirement, so a contradiction inside the crib is sufficient.

The operational specification was saved before family feasibility was computed. A candidate parity argument was already known to the investigator, so this is not a blind preregistration. Schema inspection found that the frozen core has no dense `vectors` field. A documented, pre-test schema amendment changed only the validation control to reconstruct vectors independently in two ways. Geometry, order, and mathematical family were not changed.

### Training data

Positions are one-based, with zero-based alphabet indices:

| Positions | Plaintext | Ciphertext |
|---|---|---|
| 22–34 | EASTNORTHEAST | FLRVQQPRNGKSS |

All 12 internal transitions are tested. The ciphertext supplied for this audit has 97 letters. Its supplied provenance is the pinned [data/k4.json source](https://github.com/reggiechan74/kryptos-k4/blob/0d138240fb248d0b74942efc86a51d895946921d/data/k4.json); this package uses the exact supplied bytes and does not depend on a live network fetch.

## Why arbitrary bases cannot rescue these families

For any integer base:

- If `b` is even, `code_b(T) mod 2 = v(T)[0] mod 2`.
- If `b` is odd, `code_b(T) mod 2 = sum(v(T)) mod 2`.

Thus a glyph with bit 0 absent and an even number of components always has an even code. The certificate glyphs have these exact polynomials:

| Glyph | Frozen polynomial |
|---|---|
| E | b^31 + b^28 + b^26 + b^24 |
| L | b^31 + b^24 |
| Q | b^13 + b |
| S | b^8 + b^2 |
| T | b^29 + b^28 |

For each of these glyphs, the recurrence therefore reduces to:

`K_(i+1) mod 2 = a*(K_i mod 2) + c (mod 2)`.

The base and coefficient `d` disappear. Two transitions with the same input-key parity cannot then require different output-key parities.

### Exact minimum contradiction certificates

Each row below contains an impossible pair of requirements. The full keys are included to make the alphabet and equation calculations independently checkable.

| Alphabet | Equation | Source | First transition (glyph; key → next key) | Second transition (glyph; key → next key) | Contradiction modulo 2 |
|---|---|---|---|---|---|
| AZ | Additive | Ciphertext | 23→24: L; 11→25 | 26→27: Q; 3→2 | a+c=1 and a+c=0 |
| AZ | Beaufort | Ciphertext | 23→24: L; 11→9 | 26→27: Q; 3→4 | a+c=1 and a+c=0 |
| AZ | Additive | Plaintext | 22→23: E; 1→11 | 24→25: S; 25→2 | a+c=1 and a+c=0 |
| AZ | Beaufort | Plaintext | 22→23: E; 9→11 | 24→25: S; 9→14 | a+c=1 and a+c=0 |
| KRYPTOS | Additive | Ciphertext | 23→24: L; 10→21 | 33→34: S; 0→2 | c=1 and c=0 |
| KRYPTOS | Beaufort | Ciphertext | 23→24: L; 24→7 | 33→34: S; 12→10 | c=1 and c=0 |
| KRYPTOS | Additive | Plaintext | 22→23: E; 1→10 | 29→30: T; 23→5 | a+c=0 and a+c=1 |
| KRYPTOS | Beaufort | Plaintext | 22→23: E; 23→24 | 29→30: T; 5→7 | a+c=0 and a+c=1 |

These are minimum-size certificates, selected by lexicographically earliest transition starts. A single transition cannot exclude every parameter choice: choose `a=d=0` and `c` equal to its target parity. The replay explicitly checks all eight parity triples against each certificate.

Additive and Beaufort give different full keys, but the same parity sequence because their key formulas are `C-P` and `C+P`, differing by `2P`. Hence each pair of equation choices shares its parity obstruction.

### Full inferred keys at positions 22–34

- AZ additive: `1,11,25,2,3,2,24,24,6,2,10,0,25`.
- AZ Beaufort: `9,11,9,14,3,4,6,10,20,10,10,10,11`.
- KRYPTOS additive: `1,10,21,18,1,15,2,23,5,2,19,0,2`.
- KRYPTOS Beaufort: `23,24,7,0,13,25,4,5,7,24,7,12,10`.

## Cross-checks and positive controls

1. Reconstructed all 26 vectors independently from the frozen component names; confirmed 35 unique ordered features and binary counts.
2. Compared exact big-integer polynomial evaluation with modular Horner evaluation and the parity theorem for every glyph at 11 small/large bases. All 286 checks passed, including bases near `10^80`.
3. Tested odd-code counterexamples rather than assuming every glyph is even. `J` has an even component count but bit 0 present, so its code at base 2 is odd. `A` lacks bit 0 but has an odd component count, so its code at base 3 is odd. `U` is odd at both parities.
4. Passed 3,264 encryption/decryption roundtrips, each 52 letters long: eight families × 12 schedules × 34 parameter triples. Encryption used sparse component powers; decryption used dense-vector Horner evaluation. Full key traces matched. The parameters include all eight parity triples.
5. Schedules include constants 2,3,26,27,61; alternating parity; a sweep through the allowed 2–61 range; huge integer bases; and exact `sqrt(2)` fractional digits in radices 10,12,16,60, mapped to bases by adding 2. No floating-point approximation is used for these root-digit controls.
6. The parity solver retained the planted parameter parity in all 3,264 positive cases. The exact modulo-26 constraints retained their planted full coefficients in all cases. A separate full `26^3` solve on one synthetic case per family retained `(a,c,d)=(5,7,11)`.
7. A pinned alignment mutation verifies that updating before a letter is detected: with AZ additive, plaintext E, initial key 3, coefficients `(5,7,11)`, and base 2, correct after-letter encryption emits H; the wrong pre-update version emits O.
8. Enumerated all 17,576 full coefficient triples for each actual family, allowing every attainable code residue independently at each transition. All eight have zero survivors. Bases 2–27 cover every residue class modulo 26, and integer polynomial evaluation depends only on the base modulo 26, so this is not a finite-base approximation.
9. A second implementation derived and checked the parity certificates independently, without inspecting `audit.py`. Its report and replay are included separately.

## Separate auxiliary direct-map check

This was specified in advance as a separate, simpler closure check, not a new feedback variant:

`ciphertext index = code_(b_i)(plaintext glyph) mod 26`, independently choosing `b_i` in 2–61.

It fails both alphabets already at position 22 (E→F). E's attainable residues are `{0,2,4,6,10,14,16,22}`. F has index 5 in AZ and index 12 in KRYPTOS, neither attainable.

- AZ impossible positions within the crib: 22,24,25,29,32,34.
- KRYPTOS impossible positions: 22,24,26,29,31.

The range 2–61 includes every residue class modulo 26, so the same polynomial-periodicity observation also rules out other integer bases for this exact standalone map. It says nothing about affine shifts, additional state, or other maps not tested here.

## What this means for the proposed base generators

Within the eight frozen families, trying digits of pi, e, or a secret nth root cannot help: even completely unconstrained integer-base schedules fail. All digit-plus-2 schedules in radices 10,12,16,60 are subsets of the allowed schedules.

A different feature order, measured glyph model, non-affine update, larger or multi-component state, altered letter equation, feedback timing, reset, route, or additional mask would be a different hypothesis. It is not covered by this negative result. No search over those alternatives was performed or implied.

## Files and replay

The package contains the frozen operational specification, schema amendment, original geometry bytes, `audit.py`, machine-readable results, independent review, and SHA256 manifest. See `README.md` for a Python 3, standard-library-only replay on macOS or another machine. No files on the user's Mac or repository were modified.
