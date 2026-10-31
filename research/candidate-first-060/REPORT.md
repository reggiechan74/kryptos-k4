# Study 060 findings

## Question and frozen mechanism

Could K4 use either of two compact, continuously evolving alphabets? ModelA emits through a mutable alphabet, exchanges the used position with a pointer, and advances the pointer from the emitted ciphertext's fixed-reference index. ModelB emits through a mutable alphabet with one constant input offset and reverses a prefix selected by the ciphertext's fixed-reference index. In particular, the prefix length is not taken from the changing alphabet, which would be a different construction.

Reference and starting mutable alphabets are each ordinary AZ or KRYPTOS. The only additional setting is one of 26 starting pointers forA or 26 constant offsets forB. There is no keyword search, free alphabet, reset, extra layer, padding or post-hoc exception. Both mechanisms have exact inverses because the decoder reconstructs the same state update from the ciphertext and current permutation.

## Prior-art decision

The dated proposal and independent review compare actual state operations with the local move-to-front and tree-path models and public Scott Dunphy and ActiveTK implementations. Alphabet swaps made by an optimizer are not encryption-time state updates. RC4, Chameleon, LC4 and Chaocipher are related existing design traditions; this study claims only a new-to-the-reviewed-K4-record test of these exact bounded rules. There is no historical evidence that these were Sanborn's procedures.

## Validation and held-out results

An independent reference was written before its author inspected production. The tiny three-symbol analogue covered every length-five ciphertext and every three-position clue assignment, compared against a forward-generated truth table. All 6,561 complete sets agreed;5,832 forward/inverse cases also agreed. Full-alphabet first-step bijections passed.

The 208 descriptions were initially not assumed to be different functions. A complete certificate provides a short plaintext separating every pair; production independently replays all 21,528 witnesses. That proves distinctness without claiming that sample agreement would prove equivalence.

The frozen 480-case benchmark was generated once from fresh recorded entropy. Both solver output files were sealed before answers were inspected. The 416 plants comprise every configuration under one uniform and one literal-clue random plaintext. Literal clues occupy the public mask, but the rest is uniform text; this is not a language-model test. All 416 plants were recovered uniquely, all 480 complete sets agreed, and none of 64 random controls had a compatible plaintext. Independent audit replayed generation and all complete sets and re-encrypted every returned candidate.

## K4 outcome

After parent stage approval, one production and one independent reference evaluation used the unchanged frozen engines. The canonical ciphertext SHA256 is `eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab`. Both engines completed the208-function union and returned zero compatible descriptions or plaintexts. There were no partial-English candidates, free keys or surviving parameter cylinders to rank.

This is an exact exclusion only of the stated 208 functions, not a broad exclusion of evolving-alphabet ciphers. No target-dependent rule modification or additional target run was performed.

## What was learned and what follows

The useful reusable result is a small finite-transducer validation harness with complete tiny solution sets and pairwise separating-witness certificates. These are established verification ideas, not a claimed new cryptographic invention. Production was fast; no stochastic search, neural scoring or larger infrastructure is justified by a measured bottleneck here.

Close this bounded study. Reconcile the local and external ledgers before advancing to the separately specified sum-locked block-rotation proposal. That next model retains its own novelty, route-overlap, validation and target-admission gates; this negative does not authorize changing either completed update rule.
