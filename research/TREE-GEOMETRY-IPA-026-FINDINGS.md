# Item 6: dynamic trees, nonlinear geometry and pronunciation-derived keys

**No first-crib survivor among 448 fixed descriptions.** This is a bounded negative for our rules, not a general tree, geometry or phonetic exclusion. No plaintext candidate or recovered method is claimed. The three constructions were frozen at `e35121c31d34c62c8f836d9169214f79d53de8b5` before K4 scoring.

## New coverage and what it means

| Family | Frozen mechanism | Descriptions | Outcome |
| --- | --- | ---: | --- |
| T | Balanced letter-bearing search tree; output current preorder rank; bottom-up splay the accessed node after output. Initial AZ or geometry-code order, 26 cyclic label seeds, AZ/KRYPTOS output | 104 | All first-crib failures |
| G | Full 35-bit geometry state, one-bit rotation plus XOR/addition feedback, P or C source, 26 geometry seeds, two alphabets/equations | 208 | All first-crib failures |
| I | Two source-fixed public IPA phrases converted to UTF-8 key bytes, every cyclic byte phase, two alphabets/equations | 136 | All first-crib failures; modern serialization diagnostic, not historical evidence |

All 448 full-message decryptions are distinct on actual K4. Model descriptions are not independent statistical hypotheses or a search of arbitrary initial states/functions. No Berlin-stage fit survives; no partial-English score or attractive fragment is selected.

### T changes topology, not only labels

Each of the 26 nodes carries one letter. At a fixed state, current preorder is a permutation, so ciphertext rank identifies one node uniquely. Both directions then splay that same node, proving causal inverse by induction. No raw bit-stream framing is needed. Initial order and splaying are completely specified; they are not inferred from K4. Every plaintext access can change tree shape, unlike the old fixed geometry/Morse subtree cycles.

The old arbitrary-label relaxation remains valid for **its fixed topology and update**, not this splay mechanism. New coverage is only two balanced initial orders and their 26 cyclic labels, not arbitrary topology/permutation, arbitrary learned trees or every dynamic-tree rule. Geometry codes supply one of the two initial orders; no claim is made that numerical rank itself has new geometrical content.

### G retains nonlinear full-state information

With M=2^35−1, use k=S mod26 and then S'=(rotl35(S,1)+(S XOR code(T))) AND M, after the letter. The output uses addition or true Beaufort; T is globally P or C. Noninvertible state updates are permitted because both causal directions recover identical P/C and advance from the same initial state.

The independently checked structural witness is code(C): states 0 and 26 have the same output key residue 0 but next residues 8 and 18. Thus the full update does not reduce to a function of only the modulo-26 key and current glyph, as the old first-order affine proof requires. This is an algebraic witness over the state domain, **not a claim that both witness states occur in the 26 seeded K4 trajectories**. Bit-list rotation and ripple-carry addition independently validate the implementation. Other nonlinear operators, seed states, glyph conventions and timing remain outside coverage. No claim of secure cipher design or global novelty follows.

### I avoids a false spelling inverse, but is historically weak

Use the existing Cambridge-US normalized strings `iːstnɔːrθiːst` and `bɝːlɪnklɑːk` as fixed running material only. Their UTF-8 byte lengths and primitive residue periods are 18 and 16. Every phase is tested; phase is never fitted separately at each crib. These periods lie outside the repository's prior unrestricted period 1–12 direct baseline. Their exact streams and numerical conversion are retained.

English plaintext remains English, one key byte per letter, continuously from position 1. No claim of an IPA-to-English inverse, general IPA A–Z codec or unchanged phonetic offsets is needed. The key phrases are the already public clues, not independently recovered secret material. Existing dictionary notation is a reproducible modern proxy, not a documented Sanborn source.

**Historical limitation:** UTF-8 was devised in September 1992, after Kryptos's 1990 dedication; [RFC 3629, introduction](https://www.rfc-editor.org/rfc/rfc3629) explicitly records that history. This was frozen as a modern numerical-serialization hypothesis, and its result is only an engineering diagnostic. It is not a credible source-backed 1990 mechanism or meaningful historical exclusion of pronunciation ciphers. No alternative serializer was introduced after failure. Requests for new Cambridge keyword entries returned403 and were not retried through another route; existing verified source strings were used instead. See [previous source verification/inversion limits](IPA-CODECS-INTEGRATION.md).

## Controls, failed attempt and independent checks

The first control attempt failed before K4 evaluation: a recursive reference used a different rotation grouping from the specified bottom-up splay. For AZ seed 0 on the alphabet message, native output was `ECEDGFGKJLKNMNRQSRUTUXWXZZ`, the mismatched reference `ECEEGGGKJLLNNNRQSSUUUXXXZZ`. Its incomplete manifest and empty artifact set are retained. The corrected reference uses nested trees and functional path rebuilding for the exact bottom-up rule; no model parameter or rule changed.

The completed run has 1,792 fixed-model/reference message roundtrips, 24,336 permutation checks at tree states, 104 topology-change witnesses and 104 wrong-timing mutations detected. All 24 literal-crib plants are retained by the full 448-description selector, and complete candidate sets agree with the independent reference. Each plant has one compatible setting/plaintext in these particular fixtures; that is not a uniqueness theorem.

After original scoring, a separate direct-reference replay agrees on every actual model record, not merely counts. An additional 1,040 geometry carry/boundary checks pass. References share the pinned input dictionaries and author; this is separate implementation, not external blinded verification.

All 199 histogram-preserving nulls rerun the complete family (seed 260024), with zero first-crib or complete fits. This is a descriptive control; no positive significance claim is made for a negative actual result and no posterior probability or correction for all earlier research is asserted. Public Berlin is a second-stage constraint, not untouched validation.

## Receipts and reproduction

Original completed run UTC: controls `2026-10-24T02:05:03.782641+00:00`–`02:05:12.193005+00:00`; actual `02:05:12.193900+00:00`–`02:05:12.247353+00:00`; nulls end `02:05:23.118605+00:00`. The manifest supplies the enclosing start/end and hashes. Independent replay has separate timestamps. Budgets were not approached: controls 8.41 seconds, actual 0.054 seconds, null panel 10.87 seconds; checks occur at roundtrip/plant/batch boundaries, not a hard real-time interrupt inside an individual decoder.

[Original and failed run receipts](../results/tree-geometry-ipa-026/README.md), [post-outcome independent audit](../results/TREE-GEOMETRY-IPA-026-INDEPENDENT-VALIDATION.json), [protocol](TREE-GEOMETRY-IPA-026-SPEC.md), [native code](../experiments/tree_geometry_ipa.py), [reference](../experiments/tree_geometry_ipa_reference.py).

```sh
python3 experiments/run_tree_geometry_ipa.py --spec-commit e35121c31d34c62c8f836d9169214f79d53de8b5
python3 experiments/audit_tree_geometry_ipa.py
python3 -m unittest discover -s tests -p test_tree_geometry_ipa.py
```

The runner writes a fresh uniquely named directory and preserves earlier runs. The independent audit prints a fresh replay to stdout. Do not overwrite original receipt files. No new alphabet, topology sweep, operator or pronunciation was tried after negatives. Broader physical geometry and general IPA global-alignment/inversion questions remain unresolved. No Site change; stop before item 7. K4 remains unsolved.

Final aggregate validation: **538 tests pass on Python 3.9 and 3.12**. [Separate UTC regression receipt and log hashes](../results/TREE-GEOMETRY-IPA-026-VALIDATION.json). No new documentation-link failures; 13 historical exceptions remain in one preserved independent source. No configured CI workflow; no live Site change.
