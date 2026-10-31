# Study 058 — transposition before periodic arithmetic

## Result

**UNSAT_COMPLETE within the frozen reverse-stage domain.** Both production and independent reference returned zero compatible key cylinders, operators and plaintexts for K4. The reference exhausted **22,901,760 route/period/convention descriptions**. This is an exact bounded exclusion, not a solution or a rejection of all composite ciphers.

The order is now columnar transposition first, then periodic arithmetic at the ciphertext output index. Study 057 attached the key phase before transposition. Some operators overlap those earlier tests, especially constant keys; the search total is not a novelty count. A ciphertext-free certificate demonstrates an explicit reverse-order operator outside the 057 domain.

## Frozen scope

Fill the 97-letter plaintext left to right into an unpadded ragged rectangle, width 6–9, then emit physical columns top to bottom in any permutation. If r(j) is the original plaintext position emitted at output j, use C_j = B[(s index_A(P_r(j)) + K_(j mod p)) mod 26]. A and B independently use ordinary A–Z or KRYPTOSABCDEFGHIJLMNQUVWXZ; s is +1 or −1; the arbitrary numeric key has nominal period 2–8 and zero output phase. The 24 cribs remain at their original plaintext positions.

No padding, corruption, shifted cribs, reverse column reads, other alphabets, longer keys, autokey or extra layers were added. Variant Beaufort and arbitrary key phase do not add independent coverage. Period aliases and the zero-key identity overlap across alphabet conventions remain explicit.

## Why key cylinders were necessary

Independent ciphertext-free geometry censuses proved that some routes leave key residues unobserved. Across all 2,862,720 route/period descriptions, the counts with 0, 1, 2, 3 and 4 free residues are respectively 2,736,856; 83,912; 29,472; 10,680; and 1,800. Width 6/period 8 and width 7/period 7 always leave 3–4 free residues; width 8/period 6 always leaves 1–3.

Each compatible route is therefore represented by its exact key cylinder: fixed key entries plus independent free entries. Four free entries represent 26^4 = 456,976 possible plaintexts even with that route known. The implementation retains this family instead of inserting preferred English letters. Cylinder volumes can overlap across nominal periods and conventions, so they are never added as an exact distinct-plaintext or operator count.

Exact projected classification is still possible: an empty complete cylinder set is excluded; any free cylinder proves multiple plaintexts; if every cylinder is fixed, decrypt and compare the full plaintexts. When free families exist, report conservative lower/upper bounds rather than a fabricated exact union count.

## Pre-freeze correction, preserved openly

The initial draft proposed a uniqueness-rate gate conditional on the generating key period being fully observed. Independent review found this insufficient: a period-2 seed may also belong to a period-8 cylinder with free entries. The stronger alias-aware census showed that even the proposed conditional denominator was wrong.

This was corrected **before any held-out fixture generation or target run**. The original draft is retained in the archive. Parent review selected an exact feasibility/ambiguity objective: complete cylinder agreement, all plants, exact empty/singleton/multiple classification and random-fit calibration. Unique recovery is descriptive across all fixtures, not a positive pass gate. No threshold was relaxed after seeing blind results.

## Validation and blind results

- Independent tiny brute-force checks: 768 complete cases, 49,780 cylinders and 103,156 expanded re-encryptions. Production and reference agree with complete key enumeration, including ambiguity and overlapping aliases.
- Two separately retained sets of 16 full-alphabet development controls validate signs, alphabet roles, free cylinders and identity aliases. The final production witness-hardening rerun also passes; original pre-hardening evidence is retained.
- Final freeze SHA256: 0be0fee99fbbaeb8f46aaff77b9baa32964502b1ad4f55fa8518e2cbe2a318c6. All 34 frozen file hashes independently verified.
- Fresh unfiltered blind fixtures: 224 uniform positives, 224 literal-clue positives, 16 alias cases and 56 independent random-ciphertext controls.
- All 520 runs completed with exact independent cylinder-set and projected-classification agreement.
- All 464 planted keys belonged to a returned cylinder. All 68 plants with free generating residues were correctly classified as multiple plaintexts.
- Descriptive unique plaintext counts: 156/224 uniform positives and 150/224 literal-clue positives. These are synthetic model-identifiability results, not natural-English recovery probabilities.
- Ninety plants whose generating keys were fully covered still had multiple plaintexts. Eighty-nine had verified longer-period free-slot aliases; one had another compatible explanation. These outcomes were retained, not discarded or relabeled as failed plants.
- No compatible cylinder in 56 independent random-ciphertext controls. This finite observation is not a global error guarantee.
- Independent audit replayed fixture generation and verified 893 compatible cylinders, 1,312 representative re-encryptions, all count bounds and 11,908,915,200 total reference trials.

Both blind result files were sealed at 2026-10-31T12:21:03.520988 UTC before answer analysis. Production inclusive CPU was 3.492710351 seconds; reference was 695.957593901 seconds. This is not presented as a new benchmark competition or a general speedup claim.

## Target and resource evidence

After independent benchmark audit and parent approval at 12:22 UTC, one production and one reference run evaluated K4. Both returned an empty complete family set. Target inclusive CPU was 0.015614601 seconds for production and 1.588732901 seconds for the reference. Additive target freeze SHA256: 074213b711fc5737ffff49ed268e8aa39b215a6a3f2b720bce3531a16e8d24a0. Canonical ciphertext SHA256: eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab.

Sequential worker and child processes each had a 1 GiB address-space cap. The benchmark's maximum conservative combined RSS was 20,742,144 bytes. The resource ledger includes a conservative 600 CPU-second preparation reserve and rounded analysis/audit/packaging charges, alongside measured batch CPU. The 8 CPU-hour / 8 GiB study cap was not approached. No paid checker, Site change, language scorer or corpus expansion was used.

## Next action and limits

Close Q-02 only for these exact widths, periods, alphabets, arithmetic and stage order. Reconcile the canonical hypothesis ledger and experiment log before selecting Q-03, the separately specified autokey-plus-columnar family. Do not reopen direct English-running-key decoding from 055 or infer that all transposition/substitution combinations are excluded. A future compatible cylinder would still require explicit ambiguity reporting and independent evidence before any solution claim.
