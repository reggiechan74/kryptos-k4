# Geometric alphabet pilots — bounded findings

22 October 2026. No candidate survives either frozen pilot. This is a negative
result for two specified mechanisms, not a rejection of geometric representations
or every cipher using letter shapes.

## Representation result

The [representation](ALPHABET-GEOMETRY-REPRESENTATION.md) succeeds: all 26 letters
have different 35-feature binary arrays and exact positional integer codes, with
325 pair certificates and full lookup round trips. Ordinary sums collide, and
reducing full binary codes modulo 26 gives only 14 distinct values. The full
codes are useful identifiers; uniqueness does not provide encryption or secrecy.

The user's clarified weights 1, 3, 9, 27 are base 3. The same binary arrays also
have unique, exactly reversible base-3 codes; decimal strings preserve integers
that exceed JavaScript's safe Number range. Generic base-3 decoding allows digits
0–2, but codebook decoding rejects digit 2 because this version's features are
binary. No glyph convention, feature order or bit-state recurrence was changed.

For any two distinct binary vectors and any integer base b >= 2, their highest
differing position i determines their numeric order: b^i is greater than the sum
of every possible lower binary weight, (b^i-1)/(b-1). Thus all such bases give the
same code-ranked alphabet. The theorem is about ordering, not modular residues or
rotation/XOR dynamics. Pilot A applies equally to base-3-ranked letters; Pilot B
was tested only with the frozen 35-bit binary codes.

## Chronology and fixed scope

Representation source SHA-256:
`6a5c6eae644dedf88afb68df911f0c3161a969af3815972aa5694479155aa010`.
The [specification](ALPHABET-GEOMETRY-PILOT-SPEC.md) and source were committed at
`934a2ef` before K4 evaluation. The implementation and complete planted control
receipt were committed at `012ee53` before K4 evaluation. Independent review
approved the scope; its preliminary numerical results were disclosed before our
K4 run, so this is an implementation cross-check, not a blinded independent
hypothesis discovery. No feature or parameter was retuned in response.

The canonical fixture and all 24 public crib letters were preserved. Positions
22–34 EASTNORTHEAST fit models; positions 64–74 BERLINCLOCK check those same
models without refitting. Berlin is public, historically used evidence rather
than an untouched out-of-sample secret. All repeated-letter constraints reuse
these observations and add no independent evidence.

## A — code-ranked periodic arithmetic

Alphabet: `OCSQVXWAGZITYDPBRKLFENMHJU`. There are 24 formal structures: periods
1–12, each with C=P+K or C=K-P in this alphabet. Eighteen are explicitly marked
baseline rechecks of already excluded alphabet-independent periods; six are new
checks at periods 8, 11 and 12. Key phase is redundant for unrestricted keys;
C=P-K is already included by key negation. No key-word search was performed.

Twenty-three structures contradict the training island. Only C=K-P at period 12
fits it. Its 12 key slots are all fixed by the 13 letters, with one repeated-slot
training check and no free entries. The zero-based key values are
`[15,24,3,4,1,18,2,24,4,13,25,18]`; its primitive period is 12. Its unchanged key
predicts `ZBVJDFKRUCA` at positions 64–74, matching just one of eleven letters.
There are zero all-24 survivors. This one training fit is a rejected crib fit,
not a candidate. No duplicate passing output or smaller-period key alters that.

## B — binary rotation and feedback

Exactly 3,640 descriptions: 26 full-code seeds × 35 rotations × P/C feedback ×
AZ/KRYPTOS coordinates. Every fixed model starts at position 1, uses the full
35-bit rotation/XOR state and outputs its residue modulo 26. There are no resets,
fitted masks, independent block keys or extra operators.

All 3,640 full plaintext outputs are distinct. Zero match the complete first
crib; therefore no model reaches the Berlin evaluation stage. There are zero
all-24 survivors, no unresolved parameter or plaintext classes and no timeout.
No partial-English ranking, null p-value or significance claim is made. The
negative concerns this exact state rule and dictionary, not all feature ciphers.

## Controls and reproducibility

The [control receipt](../results/GEOMETRIC-PILOT-001-controls.json) records:

- 48 literal-crib feedback plants through the complete 3,640-description selector;
  all true models included and all fixed-model full round trips exact.
- One planted feedback case has two compatible seed/plaintext solutions; it is
  correctly retained as ambiguous. The other 47 have one. True inclusion is not
  confused with unique identification.
- 24 periodic plants through the complete 24-structure selector, including
  smaller-period aliases, exact encryption/decryption and mutation rejection.
- 1,365 rotation comparisons against a separately written bit-list oracle,
  including bit 34, zero rotation, wraparound and inverse rotation.
- 72 altered-ciphertext controls reject their fixed planted target; 36 nonzero
  rotation plants reject the nearby rotate-after-XOR mechanism. At rotation zero
  the two operation orders are identical and are marked not applicable.

Commands, from repository root:

```sh
python3 experiments/alphabet_geometry.py --write
python3 experiments/geometric_pilots.py controls
python3 experiments/geometric_pilots.py actual
python3 -m unittest discover -s tests -v
```

Everything uses Python's standard library and exact integers. Full actual records
include every description, its training outcome, full output and contradiction
certificate where applicable; they are in
[GEOMETRIC-PILOT-001.json](../results/GEOMETRIC-PILOT-001.json). Selection ran in
about 0.061 seconds for B and below 0.001 seconds for A; controls took 2.874 seconds.
Both finite runtime and retained-data budgets were met. The full regression suite
passes all 257 tests in 9.523 seconds. No larger search or
alternative ordering follows these failures. The next decision requires a new,
independently motivated mechanism; this batch stops here.

## Independent replay — 22 October 2026

The separately authored oracle is preserved unchanged under
`independent/2026-10-22/geometric-pilot-oracle/`. Its source SHA-256 is
`9ee330efcd2d93b633ae61264a334484a645bde793157f430c9f8b8a2c8edd88`;
replay reproduces result SHA-256
`0ea8a0ec15ddc26f2b06ee18c7410f45fcc9aa4ec15a157e5404bcba966f4e86` exactly.
The local comparison matches all 24 periodic conflict/fit records and every one
of the 3,640 full feedback plaintext outputs, not only the headline survivor
counts. The canonical source fixture is identical.

The oracle separately passes all 3,640 fixed-model round trips, 2,205 rotation
comparisons, six periodic full-selector plants, twelve feedback full-selector
plants and 156 alphabet-origin gauge comparisons. One feedback plant has two
compatible plaintext/seed solutions; all are retained. These are control scopes,
not additional novel K4 search counts or independent statistical evidence.
Original sources/results remain byte-exact; local replay evidence is stored in
[GEOMETRIC-FOLLOWUP-COMPARISON.json](../results/GEOMETRIC-FOLLOWUP-COMPARISON.json).
The separate [raw-number security audit](GEOMETRIC-BASE-SECURITY-AUDIT.md) does not
change this pilot's frozen binary-state model or initiate a root search.

## Requested probability follow-up — 22 October 2026

The subsequent [calibration](PERIODIC-CRIB-CALIBRATION.md) refits all 24 periodic
models on each of 19,999 histogram-preserving shuffles. It reproduces 1,731
first-crib exceedances, plus-one Monte Carlo p=0.0866. This is a separately frozen
post-discovery calibration requested by the user, not a change to the original
pilot or a posterior probability of correctness. The period-12 fit has only one
closure beyond twelve fitted key values and still fails Berlin. No rotor-family
or global research-wide probability is inferred.
