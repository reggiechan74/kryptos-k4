# Fresh bounded stateful hypotheses

Research date 31 October 2026. Proposal only: no solver, synthetic benchmark or K4 target evaluation has been run for these constructions. These are speculative mechanisms we are defining, not attributed Sanborn procedures or newly invented cryptographic primitives. Novelty means no matching K4 test located in the inspected local/external records and targeted searches, not worldwide novelty.

## A Ciphertext driven exchange alphabet

Let R be a fixed reference alphabet and S a mutable 26-letter permutation. Choose R and S0 independently from ordinary AZ and KRYPTOSABCDEFGHIJLMNQUVWXZ. Choose one initial pointer q0 in 0..25. No arbitrary alphabet, keyword, reset, padding or second layer.

For each plaintext letter P_i:
1. j = index_R(P_i).
2. Emit C_i = S_i[j].
3. Exchange S_i[j] and S_i[q_i].
4. q_(i+1) = (q_i + index_R(C_i) + 1) mod 26.

Decrypt by j = index_Si(C_i), P_i = R[j], followed by the same exchange and pointer advance. Unique decryption follows by induction: every S is a permutation and both sides know the emitted C and old state. The old state, not the post-exchange state, selects j. There are 104 raw initial configurations; aliases must be deduplicated before reporting distinct operators.

Why different: the tested local move-to-front construction extracts one ciphertext symbol and inserts it at the beginning, preserving all other relative order. Here a moving pointer exchanges exactly two locations. With AZ state, q=1, P=D, the exchange produces ADCBEF..., whereas move-to-front produces DABCEF... and a rotation produces DEFG...ABC. This is not a scalar affine/cursor shift. The tested tree model applies fixed subtree cycles selected by a plaintext path, with no ciphertext-driven moving pointer. CONDI's fixed alphabet with additive state is likewise not this mutation. Chaocipher and modern RC4/Chameleon are related design traditions, but their specific update/output rules are different; do not claim a new cryptographic invention.

Plausibility: an operator can carry it out with 26 labelled tiles and one marker, changing one small part of the alphabet per letter. There is no independent evidence Sanborn used it. It is worth a small falsification pilot because the rule is compact, one-symbol-in/one-symbol-out and the whole bounded family has only104 descriptions, not because of thematic word matches.

First proposed test: independent encrypt/decrypt/state-trace implementations; full 26-symbol one-step bijection checks; complete tiny-alphabet truth comparisons; blind97-letter plants and matched decoys with24fixed crib positions. Then, only if authorized, decode K4 once per deduplicated initial configuration and demand all24letters and exact97-character regeneration. A failure excludes only this104-description grammar. Do not change exchange targets or pointer arithmetic after a failure. A surviving plaintext needs independent verification and null comparison; re-encryption alone is not proof of correctness.

## B Ciphertext indexed prefix reversal alphabet

Use R and S0 as above. Choose a single constant input shift k in0..25. For each letter:
1. j = (index_R(P_i)+k) mod26.
2. Emit C_i=S_i[j].
3. Set l=1+index_R(C_i), using the FIXED reference alphabet, not C's current mutable location.
4. Reverse the first l entries of S_i; leave the remainder unchanged.

Decrypt j=index_Si(C_i), P_i=R[(j-k) mod26], then compute the same fixed-letter l and reverse the prefix. Again104 raw configurations and exact deterministic decryption. They do not produce104 independent state histories: k does not affect the ciphertext-driven state sequence, so there are four state traces and26 final reference offsets per trace. A crib can derive k, after which all remaining cribs test it. State can be reconstructed from the ciphertext and declared initial alphabet; no guessed plaintext is needed to choose the reversal.

Why different: prefix reversal changes the relative order of multiple symbols. For l=4, AZ becomes DCBAEF..., not MTF DABCEF... or a cyclic rotation. Different prefix reversals do not commute, so the history is an ordered permutation state rather than only a cumulative offset. This is also distinct from A's two-location exchange and moving pointer. It is a new proposed K4 update rule, not evidence of a historical named cipher.

Important rejected variant: choosing l from the CURRENT position of C would always put C at the front. That would give the same repeated-ciphertext obstruction as the tested MTF system. The proposal instead uses the immutable letter value, an independently specified distinction. It must not later switch to another function after a negative outcome.

Plausibility: reverse a segment of a strip of letter tiles after each emitted letter. Hand executable, compact and length preserving; the association with K4 remains speculative. Proposed benchmark/target gates match A. No periods, free starts at a crib, unknown alphabet or unrestricted reversal schedule is admitted.

## Prior art actually checked

- Current local ledger and external register at commit c860d9a47455478f2b64b595be7d404cbf57533d, especially local STRATEGY-RESET-2026-10-22.md, STRATEGY-FOLLOWUP-FINDINGS.md, SINGLE-BOUNDARY-RESET-FINDINGS.md and TREE-PATH-CIPHER-SPEC.md. Local MTF and tree-path mechanisms already tested; not proposed anew.
- Scott Dunphy NOTES at a75178587efe9401ebf2a4edf3828472dd6fb2a2: CONDI, linear chained feedback and fixed Chaocipher. https://github.com/scott-dunphy/kryptos-k4/blob/a75178587efe9401ebf2a4edf3828472dd6fb2a2/NOTES.md
- ActiveTK summary at992c9668b9f0783221cb570abbff969e59cbf27c: fixed/arbitrary-alphabet linear selfkey and Chaocipher; its equation-based feedback does not mutate an entire permutation by these rules. https://github.com/ActiveTK/dekrypt/blob/992c9668b9f0783221cb570abbff969e59cbf27c/notes/00_SUMMARY.md
- Targeted web searches: Kryptos K4 ciphertext feedback alphabet swap move-to-front; Kryptos K4 RC4 alphabet card shuffle; Kryptos prefix reversal alphabet; Kryptos mutating cipher; Kryptos Chameleon; Kryptos alphabet swap. No matching K4 test found. Some results concern alphabet swaps performed by an optimizer, which are not an encryption state update.
- Modern primary comparison: LC4 paper discusses RC4, Chameleon and Chaocipher differences. https://eprint.iacr.org/2017/339.pdf . The2017paper is design context only and cannot be historical evidence for a1990sculpture. Its known algorithms should not be presented as newly invented or blindly transplanted to K4.
- A1999 sci.crypt conversation discusses RC4-style swapping and Kryptos in different messages, not a receipt of either specific proposal tested on K4: https://groups.google.com/g/sci.crypt/c/Fnv1wyvbnxc/m/YoZobcuHdNYJ . This prevents mistaking co-occurrence for a prior run.

## Admission and priority

Treat A and B as two precise specifications within one evolving-alphabet research family, not two unrelated new cipher families. A is slightly more economical mechanically (one exchange and one marker move). B is simpler to reconstruct from ciphertext and provides a different permutation update. Both have low K4-specific evidential prior, but are cheap, explicitly specified and falsifiable. They should be called new-to-our-reviewed-K4-record candidate mechanisms, not likely solutions. Before execution freeze exact rules, count aliases, compare against the inspected transducers, and pass independent controls. User has requested ideation, not execution.
