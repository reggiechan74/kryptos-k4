# Study 058 — columnar transposition before periodic arithmetic

## Decision, scope and prior work

Q-02 follows the reconciled study 057 result. The user authorized continuation through the ranked queue on 31 October 2026. This protocol changes stage order, not key bounds or route geometry. No K4 target evaluation is permitted until the synthetic benchmark, independent audit and parent review pass.

Fill the 97-letter plaintext row-wise into an unpadded ragged rectangle of width 6, 7, 8 or 9. Read physical columns top to bottom in any column permutation. Let r(j) be the original plaintext index emitted at output position j. Encrypt C_j = B[(s index_A(P_r(j)) + K_(j mod p)) mod 26], where A and B independently are ordinary A–Z or KRYPTOSABCDEFGHIJLMNQUVWXZ, s is +1 or −1, and the arbitrary numeric key has nominal period p in 2–8. The key phase is zero at ciphertext output position zero. Shorter-period and constant seeds remain included.

No reversed column read, padding, noise, shifted cribs, other alphabets, longer keys, feedback or extra layer is included. The 24 clues stay attached to original plaintext indices 21:34 and 63:74, zero-based. Every candidate must reproduce their exact letters.

The full reference domain is 408,960 routes × 7 periods × 8 conventions = 22,901,760 route/period/convention descriptions. This is not a distinct-key count and is not all new coverage: constant-key operators and some other alignments overlap earlier studies. A pre-target mathematical certificate must demonstrate at least one operator outside 057. Variant Beaufort, arbitrary key phase and nominal-period aliases add no independent convention. The eight alphabet/sign families have 207 unique single-letter maps; the only cross-convention overlap is zero-shift identity for AZ/AZ/+ and KR/KR/+.

## Structural identifiability and exact representation

Before any target or held-out ciphertext, two independent geometry censuses counted unobserved key residues over all routes and periods. The histogram for free residue counts 0,1,2,3,4 is respectively 2,736,856; 83,912; 29,472; 10,680; 1,800. Width 6/period 8 and width 7/period 7 always leave 3–4 free residues. Width 8/period 6 always leaves 1–3. Thus a universal high unique-recovery rate is an inappropriate gate, even when the correct route is known.

Each returned compatible family is an exact key cylinder: convention, width, nominal period, complete column order, and key slots either fixed in 0–25 or free (-1). A cylinder with f free slots represents exactly 26^f distinct seeds and, within that route/convention, 26^f distinct plaintexts. Every residue occurs in the 97-position output, so any free slot changes a noncrib plaintext letter. A family with a free slot therefore proves multiple plaintexts. If all returned cylinders have no free slots, decrypt and deduplicate the full plaintexts to classify unique versus multiple exactly. An empty complete family set is an exact bounded exclusion.

Different cylinders can overlap through period or alphabet aliases. Never sum their volumes as a distinct union count. For a nonempty set, max(26^f) is a lower bound; the sum is only an upper bound. Retain the full compressed family set. Report exact canonical operator counts only when every cylinder is fixed, using the full route and physical-letter map at every output position. Do not invent preferred English values for free keys. The objective is exact feasibility/exclusion and ambiguity diagnosis, not guaranteed plaintext recovery.

## Implementations and tiny controls

Production uses prefix column placement: as a physical column is assigned to the next output segment, each of its clues constrains a key residue at that output position. Contradictory partial assignments are pruned. Every compatible complete route emits its exact key cylinder.

An independently written reference constructs each ragged row matrix and output route explicitly, checks all periods/conventions, and derives the entire cylinder. It must not reuse production propagation. In a four-symbol domain, compare both engines' complete cylinder sets and all expanded concrete keys/plaintexts against a separate brute-force oracle, including missing-residue cases. Re-encrypt every tiny concrete witness and independently classify projected ambiguity. Full-alphabet development controls must include all role/sign combinations, fixed and free cylinders, and the zero-key identity overlap. No target data is used in development.

## Pre-freeze correction and blind gates

An initial draft proposed a conditional 95%/90% uniqueness gate among plants with no free generating-key slots. Independent review showed this was unsound: for example, width 6 with a period-2 key is also compatible with nominal period 8, whose geometry leaves free slots. The draft is preserved as superseded before any blind generation. Parent review at 12:05 UTC explicitly selected exact feasibility/cylinder correctness, all plants, exact projected classification and random-fit calibration, with uniqueness descriptive across all fixtures. No gate was changed after observing blind outcomes.

## Blind fixtures and frozen gates

Freeze protocol, source, compiled binaries, fixture generator, preflight audits and resource rules before held-out generation. Fresh entropy is secrets.token_hex(32), recorded in a separate seed file. Public solver inputs contain only opaque ID, ciphertext and clues. Generating convention, route, key and plaintext are withheld until both result files are sealed.

Use 520 unfiltered inputs: 224 uniform plaintext positives (all 8 conventions × 4 widths × 7 nominal periods), 224 literal-crib positives with the same cells and otherwise uniform text, 16 constant/repeated-key alias cases, and 56 independent uniform-ciphertext controls (28 uniform independent clues, 28 literal clues). No rejection or resampling by solvability, uniqueness or speed. The fixture generator records the generating route's free residue count from geometry alone. These synthetic texts do not test natural-language ranking.

Required gates:

1. Tiny exhaustive concrete-key and compressed-cylinder sets agree for both engines, including exact ambiguity checks and alias behavior.
2. Every one of 520 blind runs completes within resource limits, and both independent complete cylinder sets agree exactly. No compatible family may be silently truncated.
3. All 464 in-family planted keys belong to a returned generating-route cylinder. Every free-residue plant must be classified as multiple plaintexts, not failed recovery.
4. Classify every complete family union exactly as empty, singleton plaintext, or multiple plaintexts. Report uniqueness rates descriptively across all fixtures, stratified by generating geometry and nominal-period aliases. There is no positive unique-recovery-rate gate. A fully observed generating period may fit a longer nominal-period cylinder with free slots or another compatible route. Independent tiny exhaustive union enumeration and independent full-size projection checks must verify this classification. Do not filter fixtures to manufacture a high recovery rate.
5. At most 1 of 56 independent uniform-ciphertext controls has a compatible cylinder. Preserve all control outcomes. This is an operational gate, not a project-wide error probability.
6. Independent post-benchmark audit verifies all freeze/input/output hashes, fixture generation, complete family sets, exact projection classifications, free-slot bounds, re-encryption representatives, numerical gates and resource receipts.

If all gates pass, request parent approval for one unchanged-domain K4 run and one independent reference run. If compatible cylinders are found, report compatibility and exact ambiguity without claiming a solution. If no cylinders exist, report exact exclusion only of this domain. Failed or incomplete gates stop target evaluation; any corrective post-unblinding change requires a preserved failure record, reviewed repair and fresh held-out namespace. Do not weaken gates after seeing results.

## Resource and end-of-run policy

Overall cap: 8 CPU hours and 8 GiB per study. Sequential parent worker and one child each have 1 GiB address-space caps. Each engine has internal 60 CPU seconds, hard 65 CPU seconds, and 90 wall seconds per input. The shared ledger reserves 600 CPU seconds for all preparation, compilation and tiny checks; each batch records total parent/child CPU and peak RSS in a finally block, including failed or terminated children. Stop before another case if fewer than 180 CPU seconds remain. Charge independent audits, analysis and final validation conservatively as explicit additional entries.

No paid services, public checker submissions, dependency installation or Site changes. At every run's end, retain failed and partial evidence. At study closeout, reconcile canonical HYPOTHESES.md and EXPERIMENTS.md, reviewed classifications and generated navigation before selecting Q-03. Publication is separately verified; never infer scientific status from a commit timestamp.
