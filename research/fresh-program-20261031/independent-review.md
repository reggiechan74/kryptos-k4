# Independent review of fresh K4 hypotheses

31 October 2026. Research and mathematical specification review only. No K4 candidate was evaluated, no new cipher experiment was run, and no repository was changed.

## Decision

Five concrete pilots, in four broad mechanism families, pass the present proposal-level review. Their forward and inverse operations are well defined, their first domains can be bounded, and no matching exact K4 test was found in the inspected local/external records and targeted searches. This is not a global novelty claim, cryptographic invention claim, likelihood estimate or statement that any model fits K4. The alphabet-exchange and prefix-reversal pilots belong to one evolving-alphabet family and should not be inflated into two independent discoveries.

Novelty is about the operator and state update, not a new name. Conversely, a broad label such as “stateful substitution” or “transposition” does not establish that every materially different operation in that class has already been tested. These proposals remain speculative; creator-use evidence is not claimed.

The current comparison baseline is our canonical ledger and external register at commit c860d9a47455478f2b64b595be7d404cbf57533d. Primary relevant public source files and the local finite-model reports were read; external programs were not executed.

## 1 Ciphertext driven exchange alphabet

**Rank:** first cheap pilot. Author specification: `stateful-models.md`.

Let immutable reference alphabet R and initial mutable alphabet S independently be AZ or KRYPTOS; q starts at any of 26 positions. For each plaintext letter P, let j be its index in R, emit C=S[j], exchange S[j] and S[q], then set q=(q+index_R(C)+1) mod26. Decryption finds j=index_S(C), emits P=R[j], then makes the same exchange and pointer update. Update is after output, without resets.

**Bound:** 4 alphabet pairs ×26 initial pointers, 104 descriptions. There are no free per-letter choices or arbitrary unknown alphabets.

**Why different:** our move-to-front preserves the relative order of every unaffected letter. Exchange changes two entries. With state ABCDEF, accessed D and pointer0, exchange gives DBCAEF; MTF gives DABCEF; cyclic rotation gives DEFABC. Neither a fixed cyclic CONDI alphabet nor a fixed position transposition represents this update. Its permutation-state resemblance to RC4 does not make it RC4: output is the plaintext-selected entry, and the pointer is driven by the emitted ciphertext rather than the standard RC4 generator.

**First falsification:** freeze the 104 descriptions and independent inversion/state-trace controls; test all 24 cribs and exact roundtrip for every surviving description. Retain canonical duplicates, identity updates and first contradiction, rather than enlarging the model after failure.

**Caveats:** some descriptions or special messages can be equivalent; deduplicate complete operators where provable and report surviving plaintexts separately. Same mechanism family as item4. General evolving-alphabet ciphers are old; only this exact K4 proposal is provisionally unmatched.

## 2 Ciphertext steers the next message position

**Rank:** second. Author specification: `/workspace/shared/k4-fresh-structural-models.md`.

Maintain an ordered circular list of all97 plaintext slots. Start at a selected slot and orientation. Remove the current slot, encrypt its plaintext letter with an emission-indexed periodic additive key, and output C_t. The next cursor starts at the next surviving slot in the declared orientation and advances 1+index_A(C_t) among surviving slots. Stop when the list is empty. Use one fixed alphabet A, AZ or KRYPTOS, for letter arithmetic and step values.

The decoder reads the observed C sequence, reconstructs exactly the same deletion route, subtracts K_(t mod p), and puts the recovered letter in the selected plaintext slot. This is bijective for each fixed key and starting configuration.

**Bound:** 97 starts ×2 orientations ×2 alphabets ×periods1–8. The observed ciphertext determines 388 routes; there are3,104 route/period structural descriptions, not3,104 complete encryption keys. Key slots not constrained by cribs must remain symbolic and yield explicit ambiguity.

**Why different:** Scott's C7 uses fixed Josephus step counts; zeyeteam's safe-dial uses repeating or artifact-derived step sequences. Here the emitted data drives the next position, so two messages encrypted under the same key can use different permutations. Feedback is into position selection, not merely the additive key.

**First falsification:** check full inverse/visited-once properties on independent fixtures. Before a K4 search, compare any induced target route with the prior fixed-route libraries; if an identical route/key domain was already completely tested, that cell adds no new target coverage. Then perform exact key-residue consistency, not a language-scored route search.

**Caveats:** define deletion successor, counting convention and final empty-list handling exactly. Pure-transposition exclusions do not apply to the whole additive-key construction, but its zero-key cases may be analytically redundant. No direction flips, alternative step formula or free movement schedule should be appended after failure.

## 3 Block sums determine their own rotations

**Rank:** third. Author specification: `/workspace/shared/k4-fresh-structural-models.md`.

First X_i=(index_A(P_i)+K_(i mod p)) mod26. Split X into fixed-width blocks, with a ragged final block and no padding. For each actual block length n, let r=(sum of its integer values) mod n and rotate the block RIGHT by r. Output the resulting letters C.

Rotation preserves the integer sum. Thus decryption obtains the same r from each ciphertext block, rotates LEFT by r, and subtracts the periodic key. No transmitted metadata or guessed boundaries are needed.

**Bound:** widths3–12, periods1–8, AZ/KRYPTOS:160 structural descriptions. Key values are inferred from cribs after deterministic unrotation; the contiguous13-letter crib covers every residue for these periods. Phase is fixed at plaintext index0.

**Why different:** the rotation is data-dependent rather than fixed, periodic or freely fitted per block. Same key and different messages can produce different route maps. This is not merely enlarging a prior fixed-rotation library. However an individual target-induced permutation can coincide with an old route and must be deduplicated before claiming additional target coverage.

**First falsification:** prove/check sum invariance and independent roundtrips, then unrotate and solve exact periodic crib equalities. Freeze right rotation and the bounds; do not add opposite direction or another checksum after failure.

**Caveats:** constant blocks, zero rotations, length-one tails and periodic-key aliases are degenerate cases to retain and deduplicate. A result counts structural descriptions and distinct plaintexts, not a huge imagined brute-force key space. No arbitrary per-block rotation parameters are allowed.

## 4 Ciphertext selected prefix reversal

**Rank:** alternative small pilot within item1's evolving-alphabet family. Author specification: `stateful-models.md`.

Choose R,S0 independently AZ/KRYPTOS and constant k in0–25. Emit C_i=S_i[(index_R(P_i)+k) mod26]. Then reverse the first l=1+index_R(C_i) entries of S. Decode P_i=R[(index_S(C_i)-k) mod26], then make the same reversal. Prefix length is the ciphertext letter's index in immutable R, NOT its position in mutable S.

**Bound:**104 descriptions. For a fixed R,S0 the observed ciphertext determines a single state trace independent of k, so only four traces and constant-offset checks are required. Do not imply104 independent state histories.

**Why different:** prefix reversal changes the relative order of a whole segment, unlike MTF, exchange or cyclic rotation. Making prefix length depend on mutable position would create a repeated-ciphertext invariant resembling MTF and was rejected during model design; that is not the admitted operation.

**First falsification:** independent prefix-reversal and inverse controls, exact constant-offset consistency across all cribs, followed by full roundtrip for survivors.

**Caveats:** reversal lengths1/2 and some messages overlap simpler actions. This should be presented as a second specific update rule, not another broad cipher family. It is not a claimed newly invented mathematical operation.

## 5 Data driven carry between 26 and 24 states

**Rank:** more demanding, but a distinct state/readout model. Author specification: `artifact-geared-accumulator.md`.

State (a,h) has a∈0..25 and h∈0..23. For plaintext ordinal x and periodic key digit k, compute t=a+x+k; a'=t mod26; emit y=(a'+h) mod26 using OLD h; then h'=(h+floor(t/26)) mod24. Decode x=(y-h-a-k) mod26, then recompute t, a' and h'. Carry is0,1 or2; no arbitrary carries may be fitted.

Equivalent normal form: T=26h+a modulo624; update T'=T+x+k mod624, with output equal to the new low digit plus the OLD high digit modulo26. This normalization makes the mechanism transparent; it does not reduce the readout to the previously tested mod26 affine recurrence.

**Bound:** AZ/KRYPTOS, all624 initial states, periodic keys1–6, fixed update timing and direction. A lossless first screen can enumerate624 entering states for each contiguous crib, derive key residues and check repetitions; intersect absolute-phase-compatible seeds between the islands, then require full prefix reachability/global replay. A crib-local compatible state alone is not sufficient.

**Why different:** prior odometers and clock-hand keys advance by position, while this high state advances when the data-dependent low wheel overflows. Scott's carry screen admits instantaneous key±1, not a persistent24-state high digit; local H-RADIX/H-AUTONOMOUS results concern fixed affine mod26 feature/lag recurrences.

A hand-derived nonlinearity witness at zero initial state and key is E([25,1,0])=[25,0,1], E([1,0,0])=[1,1,1], but E([0,1,0])=[0,1,1], which differs from the sum of the first two output vectors modulo26. Since E(0)=0, it is not an affine mod26 map in this setting. This is a mathematical example, not a K4 experiment.

**Caveats:** using24 and26 is artifact-inspired speculation, not a claim about the Berlin clock's actual gearing or creator intent. Ciphertext alone does not fix the state without a key/start, so reachability and projected ambiguity matter. Do not replace24 by a sweep of convenient moduli if this frozen model fails.

## Sources and checked distinctions

- Current external register: https://github.com/reggiechan74/kryptos-k4/blob/c860d9a47455478f2b64b595be7d404cbf57533d/research/EXTERNAL-PRIOR-ART.md
- Local MTF rule: https://github.com/reggiechan74/kryptos-k4/blob/c860d9a47455478f2b64b595be7d404cbf57533d/research/STRATEGY-RESET-2026-10-22.md
- Local tree/splay scope: https://github.com/reggiechan74/kryptos-k4/blob/c860d9a47455478f2b64b595be7d404cbf57533d/research/HYPOTHESES.md#h-tree-stateful
- Local radix/affine scope: https://github.com/reggiechan74/kryptos-k4/blob/c860d9a47455478f2b64b595be7d404cbf57533d/research/RADIX-FEEDBACK-FINDINGS.md
- Scott fixed Josephus C7, carry, chain and block families: https://github.com/scott-dunphy/kryptos-k4/blob/a75178587efe9401ebf2a4edf3828472dd6fb2a2/NOTES.md
- Zeyeteam odometer, periodic safe-dial and artifact-step Josephus: https://github.com/zeyeteam-debug/kryptos-k4-eliminations/blob/00696f393c861db2dcfaf3adfef29823c601cf7a/README.md
- ActiveTK affine state/feedback family summary: https://github.com/ActiveTK/dekrypt/blob/992c9668b9f0783221cb570abbff969e59cbf27c/notes/00_SUMMARY.md

Targeted independent web searches covered dynamic alphabet swap/MTF, prefix reversal, ciphertext-driven Josephus, block-sum/checksum rotation and24-state carry wheels. They found related general cryptography and previously catalogued K4 schemes, but no matching exact admitted K4 operation. Absence from those searches remains limited evidence, not proof of universal novelty. Historical dynamic-alphabet/reset speculation also exists at https://pcsxcetrasupport3.wordpress.com/2016/08/04/my-first-deep-look-at-kryptos-k4/ and must not be conflated with these exact state updates.

## Shared admission gates

1. Freeze a complete reversible algorithm, bounds and parameter canonicalization before target evaluation.
2. Demonstrate exact roundtrip and state traces independently, including repeated letters, boundary cases and nearby wrong-update controls.
3. Show structural non-equivalence to closest prior mechanisms and remove previously covered target-induced permutations/cells before claiming new coverage.
4. Use exact cribs at original plaintext coordinates, then complete97-letter regeneration. Never reset at a crib island or select free states independently without checking global reachability.
5. Report compatible, excluded in bounded domain, not found, ambiguous and inconclusive separately. An English-looking candidate or exact roundtrip is not evidence of historical correctness by itself.
6. If the declared bounded model fails, record the result and stop that model. No automatic extra layer, new modulus, opposite direction or broader key space.
