# Independent K4 single-boundary reset audit

2026-10-22 UTC. Negative result within an explicitly bounded model family. No positive decoding or worldwide novelty claim.

## Bottom line

A same-state/same-key reset at one of K4's 96 internal boundaries does not rescue either preregistered model. The key result is not merely a failed search: short contradictions wholly inside the published crib islands prove the exclusions. Period-8 and period-10 repeating additive keys with one restart of the same key are also ruled out independently by the two islands.

The related Cyrillic Projector restart is motivation to test a boundary, not evidence that K4 uses a restart. This audit does not independently revalidate that published pair or its restart position.

## Inputs and exact scope

Ciphertext, 97 characters:

OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR

Known plaintext: positions 22–34 EASTNORTHEAST; positions 64–74 BERLINCLOCK. Positions here are one-based. AZ is ABCDEFGHIJKLMNOPQRSTUVWXYZ; K is KRYPTOSABCDEFGHIJLMNQUVWXZ. A boundary b is immediately after position b; b=0 identifies the no-reset baseline. Resets restore the same initial state/key and skip the usual recurrence transition at that boundary.

The preregistration was written before evaluation. No independently chosen block keys, extra resets, ciphertext edits, crib changes, extra alphabets, or alternative update rules were searched.

## 1. Move-to-front: a local impossibility

The immutable reference alphabet R and mutable initial alphabet S0 each range over AZ and K, giving four models. Encryption emits C_i = S_i[index_R(P_i)] and then moves C_i to the front, preserving all other order.

After emitting Q at position 26, Q is at rank 0. If there is no reset immediately before position 27, the second Q at 27 therefore decodes to R[0], either A or K. The published plaintext there is O. Consequently a single-reset model must reset after position 26.

Likewise the adjacent S symbols at 33–34 force plaintext 34 to R[0] unless reset occurs after position 33. The published plaintext there is T. One reset cannot occur at both boundaries. Thus the first crib alone rules out any single-reset version with either reference alphabet, even if S0 were arbitrary. The second crib additionally has TT at 68–69, requiring plaintext 69=N rather than A/K if no reset intervenes.

Direct enumeration and an independent rank-map oracle agree: zero of 388 settings survive (4 baseline settings plus 384 single-boundary settings).

### Stronger analytical consequence for the fixed four models

This was derived after preregistration, not searched as another model. At position 27 there are only two possible state cases, regardless of earlier reset timing:

- No reset immediately before 27: Q is at rank 0, giving A or K.
- Reset immediately before 27: the state is exactly S0. The resulting plaintext for R/S0 = AZ/AZ, AZ/K, K/AZ, K/K is respectively Q, U, J, Q.

None is O. Therefore even an arbitrary schedule of resets to the same S0 cannot rescue these fixed four models. This conclusion does not extend to arbitrary reference alphabets or different state-update rules.

## 2. Ciphertext-feedback affine recurrence: parity certificates

The model is C_i=P_i+K_i mod26, with K_1=k and K_i=a*K_(i−1)+b+d*C_(i−1) mod26 except that the one reset restores k and skips that transition. One shared tuple (a,b,d,k), each coordinate 0..25, applies to both blocks.

The cribs determine K_i=C_i−P_i mod26. Two equations with identical (K_previous,C_previous) parity must have identical target-key parity. Each island independently violates this necessary condition in both coordinate alphabets.

AZ, first island:

- Transition 22→23: (K22,C22)=(1,5), target K23=11. Thus a+b+d is odd.
- Transition 24→25: (K24,C24)=(25,17), target K25=2. Thus a+b+d is even.

AZ, second island:

- Transition 64→65: (K64,C64)=(12,13), target K65=20. Thus b+d is even.
- Transition 67→68: (K67,C67)=(10,21), target K68=11. Thus b+d is odd.

K alphabet, first island:

- Transition 22→23: (K22,C22)=(1,12), target K23=10. Thus a+b is even.
- Transition 26→27: (K26,C26)=(1,20), target K27=15. Thus a+b is odd.

K alphabet, second island:

- Transition 65→66: (K65,C65)=(17,2), target K66=2. Thus a+b is even.
- Transition 67→68: (K67,C67)=(5,22), target K68=15. Thus a+b is odd.

A reset can skip only one transition. The first- and second-island certificates use disjoint transitions, so at least one contradiction survives every possible single reset. In particular, a reset between the islands leaves both certificates intact. These certificates do not depend on k, on the unknown intervening plaintext, or on treating mod26 as a field.

All 194 alphabet/boundary cases (2 alphabets ×97 baseline/boundary settings) were checked. For each, all 26^3 parameter triples (a,b,d) were enumerated against the internal equations. None survived. An independent mod2 enumeration likewise found zero parity triples for every case. Therefore no initial key k can complete a solution.

This represents an exact exclusion of 88,653,344 parameter/alphabet/boundary settings: 913,952 no-reset baseline settings plus 87,739,392 single-boundary settings. Runtime optimization enumerated 3,409,744 triples rather than pointlessly simulating all 88,653,344 complete tuples after their internal equations had already contradicted them.

## 3. Periodic additive keys of lengths 8 and 10

For an unbroken periodic additive key of period p, derived K_i and K_(i+p) must agree regardless of the island's starting phase. They do not:

- AZ, period 8: positions 22/30 have values 1/6; positions 64/72 have 12/17.
- AZ, period 10: positions 22/32 have values 1/10; positions 64/74 have 12/0.
- K, period 8: positions 22/30 have values 1/5; positions 64/72 have 11/7.
- K, period 10: positions 22/32 have values 1/19; positions 64/74 have 11/0.

Each island independently rejects each proposed period. A single restart can interrupt at most one island, leaving the other contradiction untouched. The result covers period dividing 8 or 10, including shorter periods that divide them. An equality-constraint solver independently checked all 388 alphabet/period/boundary settings and found zero consistent keys.

This does not rule out all periodic-key lengths, nonperiodic keys, position-dependent substitutions, or reset mechanisms outside the frozen scope.

## Controls and independent checks

The reproducible script uses only the Python standard library and includes:

- 388 generated MTF encrypt/decrypt round trips, one for each fixed model/boundary setting, cross-checked with a separate symbol-to-rank oracle.
- 388 mutated-plaintext negative controls for those MTF outputs.
- 88 planted recurrence controls spanning both coordinate alphabets, 11 boundary placements, and four parameter tuples, including noninvertible multipliers 0, 2, and 13. Every planted tuple was recovered, without demanding uniqueness where it is not justified.
- 40 exact cross-checks between the staged recurrence solver and an independently written full four-parameter simulator over moduli 2, 3, 4, and 6. Composite moduli exercise zero divisors.
- 44 planted period-8/10 controls plus 36 exact small-domain comparisons against full key enumeration.
- Independent mod2 enumeration for every actual affine-recurrence boundary case.
- All actual MTF results checked by both alphabet-list and rank-map implementations.

Planted controls assert that the true tuple is retained, not that its boundary, seed, or plaintext is uniquely recoverable. An absorbing recurrence can erase the initial seed before the first observed crib; different seeds can then agree at every known position while disagreeing elsewhere. A nominal reset may also be observationally redundant, so its location can be ambiguous. The controls do not force unique seed recovery or unique boundary identification.

No surviving parameter solution exists in the actual tested models, hence there are zero surviving plaintext classes. Forced plaintext positions are reported as not applicable, not manufactured by vacuous consensus over an empty solution set.

## Reproduction

Run from this directory:

    python audit.py --output results.json

PREREGISTRATION.md records the frozen scope. audit.py contains the algorithms and controls. results.json provides all per-boundary outcomes, key arrays, local certificates, counts, and the fixed-four MTF analytical consequence. This REPORT.md summarizes the conclusions. The ciphertext hash and file hashes permit transfer verification.
