# One shared-state reset: bounded negative result

22 October 2026. A single reset does not rescue the registered constructions.
There is no K4 lead. This rejects the exact models below, not all message-based
initialization or all ciphers. No second reset, edit or new state rule was searched.

## Frozen scope and results

A boundary b is a zero-based index: reset immediately before index b, hence before
one-based position b+1. The domain is no reset, or b=1..96. Both blocks use the
same original state, seed, key and rule; there are no independently chosen block
parameters. No sentence boundary or carved row is privileged.

| Family | Raw domain and exact accounting | Result |
| --- | --- | --- |
| Move-to-front | Four AZ/KRYPTOS reference/initial pairs × 97 schedules = 388 cases: 4 covered baselines and 384 new boundary cases | All 388 contradict EASTNORTHEAST; 0 training-compatible descriptions, 0 compatible plaintexts |
| Affine ciphertext feedback | Two alphabets × 97 schedules, each with one shared four-symbol tuple | All 194 structures impossible; 0 training-compatible parameter tuples and 0 plaintexts. The 88,653,344-description upper bound was not simulated as distinct trials |
| Periodic arithmetic, periods 1–12 | 6,984 raw alphabet/equation/period/boundary descriptions collapse to 3,476 canonical models | All reject within EASTNORTHEAST. Of the canonical models, 48 are covered baselines and 3,428 are new reset schedules |

The local run completed in 2.465 seconds within the 120-second single-process
budget. Specification commit: `f67e282fa3309d1fab21027cbc2f206ebf20763c`.
Implementation committed before evaluation: `5c22acab1866680d01e2dc1387e38be8630bd016`.
The supplied parity witnesses were known before the specification; the MTF local
certificate was supplied after specification but before implementation/evaluation.
Their verification is not a blind discovery. The complete finite domains remained
unchanged after results.

The later Cyrillic Projector phase change supplied only weak motivation. Its date
and reset/phase ambiguity do not establish K4's method. In particular, a semantic
boundary in that published pair was not a physical panel or printed-line boundary.

## Move-to-front: why a reset cannot repair the crib

The immutable reference R and initial permutation S0 each range over AZ and
KRYPTOS. Encryption emits S[index_R(P)] and then moves that ciphertext symbol to
the front. At a reset, restore the same S0. The reference R never changes.

The consecutive ciphertext QQ at positions 26–27 places Q at rank 0 after position
26. Without a reset immediately before 27, the next plaintext must be R[0], A or
K. The confirmed plaintext at 27 is O, requiring a reset there. Likewise SS at
33–34 requires another reset immediately before 34 to avoid A/K when T is needed.
One reset cannot occupy both boundaries. This alone excludes the registered family
using the first crib. Direct enumeration and an independent prefix-recency decoder
agree on all 388 full outputs. Each already differs at the first known position,
22; all 388 outputs are distinct for this fixed ciphertext, but none is compatible.

The independent reviewer supplied a stronger analytical corollary for the same
four mappings. If a reset does occur immediately before 27, Q instead decodes
through S0/R to Q, U, J or Q for AZ/AZ, AZ/KRYPTOS, KRYPTOS/AZ and
KRYPTOS/KRYPTOS. None is O. Thus arbitrary reset timing cannot repair these exact
four mappings either. This is a local invariant with two state cases, not a
multi-reset sweep or an exclusion of arbitrary alphabets, state rules or composites.

## Affine feedback: internal contradictions survive any one cut

Use C_i=P_i+K_i modulo 26, K_0=k, and away from the boundary:

`K_i = a*K_(i-1) + c + d*C_(i-1) mod 26`.

At the boundary set K_i=k. Here c denotes the constant coefficient called b in the
earlier recurrence, avoiding confusion with the boundary variable. Each alphabet
is fixed to AZ or KRYPTOS; a,c,d,k range independently over 0..25 and remain shared.

Cribs fix K_i=C_i−P_i. Two transitions with the same previous-key/ciphertext
parities must have the same target-key parity. The following witnesses violate
that requirement independently within each island. Entries are
(previous key, previous ciphertext, target key), with one-based positions:

| Alphabet / island | Transition and values | Contradictory transition and values |
| --- | --- | --- |
| AZ / EASTNORTHEAST | 22→23: (1,5,11) | 24→25: (25,17,2) |
| AZ / BERLINCLOCK | 64→65: (12,13,20) | 67→68: (10,21,11) |
| KRYPTOS / EASTNORTHEAST | 22→23: (1,12,10) | 26→27: (1,20,15) |
| KRYPTOS / BERLINCLOCK | 65→66: (17,2,2) | 67→68: (5,22,15) |

One boundary skips only its incoming transition. It leaves at least one complete
crib island untouched, so at least one certificate survives. The unknown earlier
plaintext and seed cannot remove an internal contradiction. This uses arithmetic
modulo 2 and remains valid modulo 26 without any field or invertibility assumption.

To measure first-crib fitting separately, the local implementation also checked
all 26^3 coefficient triples per alphabet. Any triple with more than one violated
internal training transition is already impossible with one reset; a single
violation can be removed only at its target. None passed even this necessary
filter. Consequently no seed enumeration was required and there were no first-crib
fits from which to make Berlin predictions. The raw upper bound contains 913,952
previous no-reset descriptions and additional degenerate/overlapping descriptions;
it is not a count of newly simulated unique hypotheses. With zero solutions,
parameter and distinct-plaintext multiplicities are both exactly zero.

## Periodic-key coverage and deduplication

The audit uses the existing two alphabets and three equations C=P+K, C=P−K and
C=K−P, with one unrestricted shared key of period 1..12 and phase-zero restart.
No dictionary list or additional period was introduced. The prior ROUTE-001 identity
model already covers the no-reset versions over periods 1..96. The older identical
resets at both positions 22 and 64 are a different schedule and were not recycled
as evidence for a single unknown boundary.

With an unrestricted key, plus and minus are the same family under key negation.
Full 97-position phase signatures are also canonicalized under phase relabeling.
A reset at a multiple of the period is exactly the no-reset schedule. These
identities collapse the 6,984 raw descriptions to 3,476 canonical models, including
48 covered baselines. Those baselines account for 1,842 raw aliases; there are
3,428 genuinely different reset schedules within this fixed audit. No literal key
or broad new keyspace was brute-forced.

Required key values are grouped by phase. Every canonical model already has a
contradiction inside EASTNORTHEAST, so no unknown phase is filled and no Berlin
letter is used to rescue or fit a key. Exact key/full-plaintext solution counts
are zero. Independently, periods 8 and 10 in the additive model each contradict
both islands separately; one restart cannot repair two untouched-island conflicts.
The independent audit confirms that subset, not the entire local period-1..12
scope. Other periods and other coordinate alphabets remain outside this new test.

## Controls, prediction and identifiability

The local MTF selector searches all 388 descriptions on every control. Thirty-two
synthetic messages use the actual EASTNORTHEAST and BERLINCLOCK strings at their
fixed indices, with random filler, four true boundary placements and all four
initial pairs. All generating descriptions and complete true plaintexts are
retained. Sixteen plants have a unique compatible plaintext; sixteen remain
ambiguous. A boundary after the last crib is intentionally included: agreement at
known letters need not identify later state or the complete message. Unforced
noncrib positions and complete compatible-set counts are retained rather than
filled by English or a chosen representative. This is programmatic label blinding,
not investigator blinding or a natural-English benchmark.

Eight nearby cyclic-rotation controls and 32 histogram-preserving planted-cipher
shuffles yield no compatible MTF case. These are descriptive finite controls,
not a K4 p-value or universal false-positive bound. The same 24 constraints and
full selector are applied throughout. The batch also passes:

- 104 MTF one-step checks and independent full-message reset oracles;
- 32 recurrence fixed-parameter plants with literal crib structure, including
  nonunit multipliers and stationary states;
- 776 checks of stationary-state boundary aliases, plus explicit seed ambiguity
  for multipliers 0 and 2;
- 216 periodic planted inverses and 216 mutated-crib rejections.

First-crib fitting and second-crib evaluation are separate in the saved records.
For a selected fully specified MTF description, the second crib would be predicted;
for an unresolved key family, only previously fixed phases would be individual
predictions, while new phases would spend free parameters. Here no actual family
survives the first crib, so forced held-out positions are **not applicable**.
Empty maps/lists in the local records denote that inapplicability, not consensus
over an empty set or evidence for any letters. All public clues were historically
known before design; the split is not independent historical validation. Boundary
selection is charged to the full finite family.

## Independent replay and reproducibility

The separately supplied independent archive was downloaded through the supported
Library flow, checked against its 16,158-byte size and SHA-256
`85fed390a386e07f3d14f6537b2fe6911d9aab60c63c673b07feb0437262d779`,
and safely extracted. All member manifests match. Its standard-library code was
read before execution in an isolated scratch copy. Replay reproduces every result
exactly; original artifacts are preserved separately.

The independent audit checks 388 MTF settings, 194 affine structures and 388
period-8/10 additive structures. Its 3,409,744 coefficient checks and modulo-2
cross-checks are corroboration, not extra novel model counts. Its controls include
388 MTF roundtrips/mutations, 88 recurrence plants, 40 complete small-ring solver
comparisons and 44 periodic plants with 36 toy key comparisons. Those controls use
known-position masks on generated messages and are not a claim of full-family blind
unique recovery; the local literal-crib controls above supply that separate test.

[Local specification](specifications/SINGLE-BOUNDARY-RESET-001.json),
[implementation](../experiments/single_boundary_reset.py),
[complete local result](../results/single-boundary-reset-runs/20261022T212416Z-f634e152375e406d971f9edc1dc91096/SINGLE-BOUNDARY-RESET-001.json),
[immutable manifest](../results/single-boundary-reset-runs/20261022T212416Z-f634e152375e406d971f9edc1dc91096/manifest.json),
[independent report](../independent/2026-10-22/single-boundary-reset/REPORT.md),
[transfer receipt](../independent/2026-10-22/single-boundary-reset/TRANSFER-RECEIPT.json),
[independent local replay](../results/SINGLE-RESET-INDEPENDENT-LOCAL-REPLAY-001.json).

```sh
python3 experiments/single_boundary_reset.py --spec-commit f67e282fa3309d1fab21027cbc2f206ebf20763c
python3 -m unittest discover -s tests -v
```

Python 3.9.6; local run 2.465 seconds. Full regression: **231 tests passed in
9.367 seconds**. Inputs, code/spec commits, versions, control data, all raw aliases,
complete rejected MTF outputs and exact certificates are saved. No source images,
private material or credentials are added. Canonical K4 and controls remain intact.

This bounded test is complete. It supplies precise exclusions, not a positive
mechanism. No further reset, new alphabet, independent block key or edit arm is
started automatically. Main, the Site and persistent authentication are unchanged.
