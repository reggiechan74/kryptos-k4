# Autonomous multi-step key generators: exact first-crib exclusion

22 October 2026. **All 20 frozen structures are impossible on EASTNORTHEAST.**
No K4 candidate, Berlin validation or positive decoding emerges. No order, reset,
alphabet, edit, ciphertext feedback or route was added after the result. The
separately discussed tree/Morse idea is outside this experiment.

## What was tested

For AZ or KRYPTOS coordinates, use C_i=P_i+K_i modulo 26 and, from i=r onward,

`K_i = b + sum(a_j*K_(i-j), j=1..r) mod 26`.

Orders are r=2..6; b is fixed zero or fitted. The initial r key symbols are arbitrary
and the same coefficients apply to all 97 positions. This gives 20 formal
structures, including known/degenerate overlap, not 20 globally novel methods.
Only the 13 key values derived from EASTNORTHEAST at one-based positions 22–34
fit coefficients. BERLINCLOCK at 64–74 is reserved for joint forecast validation.
The intended forecast spans the 29-symbol gap at 35–63 and all 11 Berlin symbols;
no per-position witness selection is allowed.

Specification commit: `5615caf91915b75251156d6da826bdae0500d349`.
Implementation committed before evaluation: `4354cc26f354ffb7955c6b6304428d8a3c1ce966`.
Run: `20261022T215356Z-4769d0b137d348e99db42ee5918dc799`, Python 3.9.6,
0.087 seconds under the frozen 120-second, single-process budget. No enumeration
cap was reached. Independent parity witnesses were disclosed after the
specification but before implementation; their verification is not blind discovery.

## Exact ranks: why seven equations need not give a fit

Coefficient equations are solved over F2 and F13, retaining exact affine bases,
particular solutions and inconsistency witnesses. CRT requires solutions in both
fields. Both coordinate alphabets have the following ranks, shown as coefficient
rank / augmented rank:

| Order | Constant | Equations | Variables | F2 ranks | F13 ranks | Modulo-26 coefficient solutions |
| --- | --- | ---: | ---: | --- | --- | ---: |
| 2 | Zero | 11 | 2 | 2 / 3 | 2 / 3 | 0 |
| 2 | Fitted | 11 | 3 | 3 / 4 | 3 / 4 | 0 |
| 3 | Zero | 10 | 3 | 3 / 4 | 3 / 4 | 0 |
| 3 | Fitted | 10 | 4 | 4 / 5 | 4 / 5 | 0 |
| 4 | Zero | 9 | 4 | 4 / 5 | 4 / 5 | 0 |
| 4 | Fitted | 9 | 5 | 5 / 6 | 5 / 6 | 0 |
| 5 | Zero | 8 | 5 | 5 / 6 | 5 / 6 | 0 |
| 5 | Fitted | 8 | 6 | 6 / 7 | 6 / 7 | 0 |
| 6 | Zero | 7 | 6 | 5 / 6 | 6 / 7 | 0 |
| 6 | Fitted | 7 | 7 | 6 / 7 | 7 / 7 | 0 |

Affine order six is the useful caution. Modulo 13 it has a unique fitted
coefficient vector and zero spare training equations. Modulo 2 its matrix is
singular and the right-hand side is inconsistent. The mod-13 fit has no CRT mate;
it must not be lifted arbitrarily or treated as predictive progress. Exact
Gaussian row-combination certificates are saved for every inconsistent component.

## A small parity certificate explains all 20 negatives

The AZ first-crib key parities are:

`1,1,1,0,1,0,0,0,0,0,0,0,1`.

Predecessor windows at positions 27–32 and 28–33 are both six zeros, but require
K33 even and K34 odd. The KRYPTOS key parities are:

`1,0,1,0,1,1,0,1,1,0,1,0,0`.

Windows 24–29 and 27–32 both have parity state `101101`, but require K30 odd and
K33 even. A fixed affine rule cannot send an identical predecessor parity state
to different next parities. Shorter lag windows are suffixes of the same states,
and homogeneous models are subsets of the affine model. Neither an unknown
initial seed nor unknown earlier plaintext can repair this internal contradiction.

This is a bounded exclusion of the declared modular linear/affine generators.
It is not an exclusion of arbitrary full-symbol lookup functions, other
alphabets, nonlinear methods, message resets or every possible key generator.
Repeated-EAST/pair equations were not counted as extra evidence: these certificates
are consequences of the same first 13 known letters.

## Prefixes, multiplicity and prediction were not silently assumed

Because there are no coefficient solutions, the actual full-plaintext multiplicity
is exactly zero. Reachable-prefix sets, common forecast letters and forced
held-out positions are **not applicable**, not inferred by vacuous agreement over
an empty solution set. No actual prefix or coefficient vector was enumerated and
no Berlin forecast comparison was needed. Berlin values were not used to fit the
first-crib matrices. There are no budget-unresolved structures.

The implementation nevertheless exercises the required singular-case machinery
on controls. Given fixed coefficients, a linear-affine map propagates every
possible initial seed to the beginning of the known state. Its reachable seeds
are solved by CRT, without backward inversion. The complete affine seed spaces
and their images in the unknown 21-symbol prefix are retained. Predictions use
one complete coefficient tuple through the whole gap and Berlin block.

For compatible controls, full-stream counting groups identical fixed tails and
counts unions of affine prefix product spaces by signed intersections. It does
not sum overlapping parameter descriptions. Full finite-set comparisons verify
those counts. Resource caps would leave an exact symbolic coefficient set or
prefix set and an explicit unresolved count; they would not sample representatives.
No such cap was invoked on K4.

## Controls and lower-order aliases

All 80 literal-crib plants retain the true coefficient and reachable seed, reproduce
the complete 97-letter message, and forecast the entire known continuation exactly
under that tuple. They span both alphabets, all five orders, both constant modes,
and final coefficients 1, 2, 13 and 0. Sixty plants have multiple reachable prefixes
under their planted coefficient tuple; counts range from 1 to 208. These are
symbolic truth-inclusion and forecast controls, not a claim of unique model recovery.

Twelve independent complete parameter/seed enumerations over moduli 2, 3 and 6
agree with the staged solver on both parameter sets and distinct full streams.
Additional controls verify nonunit equations modulo 26, inconsistent prefix states,
exact affine-space intersections/unions and 29-gap/11-Berlin indexing.

Two alias distinctions are explicit:

- A fitted constant of zero overlaps the homogeneous structure.
- A zero last coefficient lowers the recurrence's active lag but can leave extra
  startup freedom. With order two, coefficients (1,0), b=0 and a known constant
  tail of 8, there are 26 reachable seeds; only one obeys the global order-one
  startup equation. Calling all 26 globally lower-order would be wrong.

Fixed coefficients and a fixed seed always give one full decryption. Ambiguity
comes from fitting or unobserved initial states, not a multivalued decoder. No
English score or statistical significance is claimed. No matched K4 significance
simulation is needed for this exact rejection.

## Prior art and independent replay

The pinned [Barney linear-relation source](https://github.com/barneyjm/kryptos-k4/blob/2db2722cc3f18c52d4d8369d7adc5a1db7e859d7/scripts/linear.py)
was read statically, not executed. Homogeneous order two expands into the five
features P0, C−1, P−1, C−2, P−2, which its grammar contains. Generic affine order
two adds a sixth feature; orders three through six require absent lags. Degenerate
subcases can still overlap. This is static containment, not proof of an external
completed run or worldwide novelty. The existing fixed mod-16 Gromark lag-5/6
stream with unknown alphabets is a different model. The byte pin and detailed
scope are in the [prior-art receipt](../sources/autonomous-recurrence-prior-art.json).

The independent JavaScript oracle was supplied as text after its filesystem was
unavailable. The message escaped HTML operators; one transport decoding produced
exactly 12,929 bytes and the declared source SHA-256. No algorithm or whitespace
repair was applied. Its inspected source then reproduced exactly the declared
16,388-byte JSON output and SHA-256 under Node.js v23.9.0. All 20 ranks/counts
agree, with zero Berlin evaluations and 231 independent numerical controls passing.
That numerical-control count is separate from the local regression-test count.

Its unused generic positive branch is illustrative: it lacks complete plaintext
counting and postpones prefix reachability until after Berlin. It is not adopted
as a production survivor solver. Actual K4 rejects before that branch, so its
negative proof does not depend on those limitations. Original source/output and
transport details are preserved in the [independent package](../independent/2026-10-22/autonomous-recurrence/README.md).

## Reproduction and stopping point

[Specification](specifications/AUTONOMOUS-RECURRENCE-001.json),
[production audit](../experiments/autonomous_recurrence.py),
[exact algebra helper](../experiments/exact_linear.py),
[full immutable result](../results/autonomous-recurrence-runs/20261022T215356Z-4769d0b137d348e99db42ee5918dc799/AUTONOMOUS-RECURRENCE-001.json),
[manifest](../results/autonomous-recurrence-runs/20261022T215356Z-4769d0b137d348e99db42ee5918dc799/manifest.json).

```sh
python3 experiments/autonomous_recurrence.py --spec-commit 5615caf91915b75251156d6da826bdae0500d349
python3 -m unittest discover -s tests -v
```

The audit stops at the frozen order-six boundary. No higher order, reset, new
alphabet or tree layer is started. Main, the Site and persistent authentication
remain unchanged. The user's privately inspected Morse image was kept outside
the repository and is not an input to this experiment.

Integration validation: **242 local regression tests passed in 9.439 seconds**.
The independent oracle's 231 numerical controls are recorded separately.
