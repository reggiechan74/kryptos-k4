# Fresh hypothesis candidate — plaintext driven 26 by 24 accumulator

Status: speculative, not run. No matching K4 implementation or test was found in this bounded register, source and targeted-web review. This is not a claim of global invention or evidence that Sanborn used it.

## Plain language

Instead of reading a precomputed clock schedule, let each encrypted letter turn a 26-position alphabet wheel. Each full turn advances a 24-position counter. The counter's **old** setting contributes to the letter being emitted. Thus the message itself drives the clock, and whole-turn information persists rather than being discarded by mod-26 arithmetic.

The World Clock's 24-sided display provides only thematic motivation for 24. Berlin's official description confirms 24 segments and a moving hour ring. The proposed 26-to-24 gearing is invented for this hypothesis; it is NOT a measured feature of the actual clock.

## Exact model

Use one fixed alphabet A, either ordinary A–Z or KRYPTOSABCDEFGHIJLMNQUVWXZ. Convert plaintext and ciphertext to its 0–25 indices. No mixed alphabets, transposition, padding, spelling changes, or additional layer in the initial pilot.

State is a in {0,...,25} and h in {0,...,23}. Secret key K has nominal period p in 1,...,6, entries 0–25. Phase zero at plaintext/ciphertext position zero; cyclic phase aliases are not new models.

For plaintext index x at position i:

1. t = a + x + K[i mod p].
2. a_new = t mod 26.
3. y = (a_new + h) mod 26. Emit A[y]. **Use old h here.**
4. h_new = (h + floor(t/26)) mod 24.
5. Replace (a,h) by (a_new,h_new).

Decryption is unique from the current state and key: x = (y - h - a - K[i mod p]) mod 26, then recompute t and the same state update. There are 624 initial states. A fixed state and key letter induce a bijection on the 26 plaintext letters. Carry can be 0, 1 or 2.

## Honest normal form and difference from prior work

Let T=26h+a in Z624. The state update is simply T_new = T + x + K[i mod p] (mod 624). The output reads the new low base-26 digit and the old high digit. Thus this is a **scalar modular accumulator with a nonlinear digit readout**, not a claim to have invented a new kind of physical gearing.

The substantive hypothesis is retention and re-use of the integer quotient in a second modulus. Without that state, cyclic-tableau walks collapse to already-tried mod-26 feedback.

Closest inspected work:

- zeyeteam odometer k_i = a[i mod p] + b[floor(i/p) mod q] is position driven, not input driven. Its Alberti stepping is likewise autonomous. https://github.com/zeyeteam-debug/kryptos-k4-eliminations/blob/00696f393c861db2dcfaf3adfef29823c601cf7a/README.md
- Scott carry.py models directly derived periodic key values in {K_r,K_r+1}. It does not retain the carry in a mod-24 state. https://github.com/scott-dunphy/kryptos-k4/blob/a75178587efe9401ebf2a4edf3828472dd6fb2a2/novel/carry.py
- Scott run_chain.py models fixed low-order linear combinations of earlier plaintext/ciphertext indices, linear position drift and a constant, all mod26. The persistent high digit here is not such an asserted linear term; a full equivalence audit remains part of admission. https://github.com/scott-dunphy/kryptos-k4/blob/a75178587efe9401ebf2a4edf3828472dd6fb2a2/novel/run_chain.py
- Scott run_digitcode.py explicitly has no carry and operates on fixed mixed-radix encodings per letter, not a message-driven cross-letter accumulator. https://github.com/scott-dunphy/kryptos-k4/blob/a75178587efe9401ebf2a4edf3828472dd6fb2a2/run_digitcode.py
- Local affine/radix feedback and autonomous recurrence exclusions must not automatically be applied to a hidden mod624 state with nonlinear readout. This is a distinction to prove during preflight, not a blanket novelty assertion.

## Hand derived nonlinearity witness

For zero initial state and constant key zero, let u=[25,1,0] and v=[1,0,0]. The proposed equations give E(u)=[25,0,1] and E(v)=[1,1,1]. Yet E(u+v mod26)=E([0,1,0])=[0,1,1], whereas E(u)+E(v) mod26=[0,1,2]. Thus this member is not a fixed linear/affine mod26 feedback map, even though its internal accumulator updates linearly in Z624. This is a hand-derived algebra example, not an executed cryptanalysis run or proof against every nonlinear prior family.

## Cheap first experiment

First validate encryption/decryption and an independent small-alphabet analogue exhaustively; check aliases against simple Vigenere, cumulative mod26 feedback and autonomous odometers. Then use blind synthetic 97-letter positives and matched nulls with the 24-position crib mask.

There is an efficient exact crib filter without searching all 26^p seeds. For each p<=6 and each of 624 possible states entering the 13-letter crib, the first encounter of a key residue forces K_r = (C_i-h-a-P_i) mod26. Repeated residues must agree as the state is advanced. A 13-letter crib visits every residue for these periods. Repeat at the 11-letter crib using its global phase, intersect complete key seeds, then replay every surviving seed from all 624 message-start states to test the full 97-letter forward map. Do not reset state at either crib; separate local start states are only a lossless first-stage superset.

This proposed filter is a mathematical design, not a run receipt. No K4 fit or rejection has been computed here.

## Advance and stop criteria

- Advance only if the two independently implemented solvers agree on complete tiny and blind result sets, retain all planted keys up to equivalence, and meet predeclared resource/false-fit criteria.
- A complete empty K4 result would exclude only these two alphabets, p1–6, this exact old-counter readout, and no extra layers.
- A survivor must independently re-encrypt all97 letters and have projected plaintext ambiguity measured. English appearance alone is not evidence.
- Do not change readout timing, add signs, increase state dimensions or add a route after failure without a new explicit hypothesis and prior-art review.

## Source and search provenance

Official artifact motivation: https://www.berlin.de/sehenswuerdigkeiten/3561749-3558930-weltzeituhr.html — confirms 24 segments, moving hour ring, and drive mechanism. Does not support the invented cipher operation.

Reviewed current local HYPOTHESES.md and EXTERNAL-PRIOR-ART.md at c860d9a, downloaded Scott NOTES, zeyeteam README, actual Scott carry.py/run_chain.py/run_clock16.py; targeted web queries included Kryptos K4 carry clock feedback; Kryptos odometer plaintext; Kryptos geared24/26; Kryptos cumulative carry; Kryptos carry feedback; Kryptos data-dependent carry. Search results included old odometer/carry, generic rotor and self-key discussions; no matching full state/output algorithm was located.

No experiment, external code execution or repository change performed.
