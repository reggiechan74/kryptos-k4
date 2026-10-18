# Identical clue-boundary reset: exact model boundary

Prepared 18 October 2026 from the independent reviewer's supplied witnesses.
The frozen verification specification is `research/specifications/CLOCK-BOUNDARY-REG-001.json`,
committed at 4e2d002925bfc7f3b332f94cd4472617919f52fa before verification.
Witnesses were supplied and draft code existed beforehand; this is verification
of known deductions, not new discovery or a blind preregistered negative search.
No keyword scan is needed.

## Assumptions and witness

Assume unchanged plaintext/ciphertext positions and resets immediately before
one-based positions 22 and 64. Both resets restart the **identical sequence of
positionwise bijections**. Thus at relative offset j, both segments apply the
same injective function f_j, independent of text content.

At zero-based relative offset 3, one-based positions 25 and 67 have confirmed
plaintext T and L, respectively. Both ciphertext letters are V. This requires
f_3(T) = V = f_3(L), contradicting injectivity since T differs from L. Key length,
literal keyword spelling and alphabet ordering cannot remove this contradiction.

This excludes only the declared identical-reset positionwise-bijective model.
It does not exclude transposition, content-dependent stateful feedback, different
keys/sequences at the two boundaries, changed alignment or unspecified composites.
Those are not implemented as rescue variants. The BERLINCLOCK crib is unchanged.

## Two supplementary arithmetic witnesses

For the three equations C=P+K, C=P−K, C=K−P modulo 26, the implied values are
respectively C−P, P−C, C+P. Under each of the two fixed alphabets A–Z and KRYPTOS:

- At the first reset offset, position 22 E→F and position 64 B→N require
  different key values. They cannot share the identical restarted key sequence.
- Within the first segment, position 22 E→F and position 33 S→S are separated
  by 11 and require different key values. A period-11 arithmetic key already
  fails inside that segment; resetting at positions 22/64 cannot repair it.

The latter is redundant with earlier ROUTE-001 period-11 arithmetic exclusion,
not a new keyword discovery. The weaker arbitrary-bijective period-11 equality
test is a different model and is not contradicted by that earlier result.

`experiments/reset_boundary_proof.py` pins only these witnesses and performs no
keyword, phase, length, alphabet or reset-position search. Prepared tests pin the
indexing, compare arithmetic formulae to an independent 26-value **synthetic
regression truth table**, and check a compatible artificial same-input fixture.
The truth table is a control, not a K4 candidate-key search. The registered run and permanent receipt follow the specification and
implementation commits. The fixed 72 formal cases are three 11-letter keywords
(KRASNOJARSK, BERLINCLOCK, WELTZEITUHR), four schedules [1], [1,22], [1,64],
[1,22,64], two alphabets and three equations. All are subsumed analytically by
the period-11 certificate; zero candidate-search trials are performed. The
general identical-reset bijection certificate applies when starts 22 and 64
both reset to the same sequence. No optional phase-fitting exercise is run.

## Completed verification

CLOCK-BOUNDARY-REG-001 verified all 13 certificates and all declared controls:
4,056 primitive cases, 388 independent phase comparisons, 24 synthetic 97-letter
round trips/regenerations, and 24 altered-position-33 negatives. It completed in
0.018 s under the 10 s cap, one process, Python standard library. Zero candidate
search trials; 72 formal cases analytically subsumed. This confirms the supplied
known deductions, not new discovery, a K4 solution, or elimination of composites.

[Immutable manifest](../results/clock-boundary-runs/20261018T124241Z-f156ac09cb06401b8bfbcc8e48b8383d/manifest.json)
and [all certificates/control arrays](../results/clock-boundary-runs/20261018T124241Z-f156ac09cb06401b8bfbcc8e48b8383d/CLOCK-BOUNDARY-REG-001.json).
Implementation commit: 000b8c3a4e480fd773f131cf85eef6bc30d47206.
The specification commit precedes implementation, which precedes the actual run;
witnesses and draft proof code were known before the specification. All output
and consulted input/code hashes were checked against the local files afterward.
Full regression suite: 90 tests pass in 7.382 s; earlier result files preserved.
