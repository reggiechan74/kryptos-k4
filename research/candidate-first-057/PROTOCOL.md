# Study 057 — alphabet-role and arithmetic extensions of 056

Status: protocol preparation; no target evaluation authorized until benchmark and independent audit gates pass and the parent reviews them.

## Prior evidence and exact scope

This is queue Q-01 of the canonical ledger at e589286feedd6c3b52959418acd848f0a54a62b5. Study 056 exhausted ordinary A–Z Vigenère followed by unpadded ragged columnar transposition. The present extension holds its length, key-period and route bounds fixed and varies explicit alphabet roles and sign. This is new bounded coverage, not a new cryptanalytic algorithm or claim of historical attribution. Earlier ROUTE-001 covered restricted routes; 050 fixed-key grammar does not cover the full route/key domain here.

Let A and B independently be the ordinary alphabet AZ or KRYPTOSABCDEFGHIJLMNQUVWXZ. Let s be +1 or -1. For plaintext position i, compute D_i = B[(s*index_A(P_i)+K_(i mod p)) mod26]. Fill rows left to right with D and emit physical columns in an arbitrary permutation, reading each top down, with no padding. Width w is6,7,8,9; nominal period p is2,3,4,5,6,7,8; the numeric seed is arbitrary in0..25, including shorter-period aliases. Alignment is zero. No added reverse, offset, padding, noise or stage-order variants.

All eight (A,B,s) conventions are evaluated to retain the 056 baseline as a regression. Only seven conventions add domain coverage. Variant Beaufort is key negation of the + convention, and arbitrary key phase permutes an arbitrary seed: neither adds coverage. The independent one-letter map certificate identifies207 distinct maps among208 descriptions; the sole duplicate is zero-key AZ/AZ/+ versus KR/KR/+ identity. Canonical operator identity is the full output-to-input97-position route plus the complete26-letter permutation at each plaintext position. Count plaintexts separately. Do not report a convention label, nominal period or key spelling as a distinct operator.

The exhaustive reference tests408,960 column orders for each period/convention:22,901,760 route/period/convention descriptions per full input, including2,862,720 baseline descriptions. The seven nonbaseline convention loops contain20,039,040 descriptions, not necessarily that many distinct new operators or keys. The route fixes all key residues because the13-letter contiguous crib covers every allowed period; missing residues must be represented explicitly, never filled from language preference.

## Implementations

Production reuses study056's frozen solver source byte-for-byte (SHA256625739e4d4e5a4e0052de4069563319b1a0c13e7b1c82cb0cf2751c09f657573), modeS (shared placement constraint propagation, no learned conflicts). Convert ciphertext to B indices, crib plaintext to s*A indices, then convert output u to A[s*u mod26]. An independently written C++ route enumeration uses the physical-letter equations directly. Full raw solution-set and canonical operator/plaintext-set agreement is required, plus independent exact re-encryption.

## Controls and blinding

Before heldout generation, freeze all code, this protocol, fixture specification and seeds policy by SHA256. No post-unblinding tuning. Fresh root entropy comes from secrets.token_hex(32), recorded in a separate answer/seed file. Inputs have opaque IDs and only ciphertext/clues. The solver and reference receive no planted convention, route, period or key. This is procedural synthetic blinding, not a claim that public K4 clues are unknown.

Heldout520:224 uniform plaintext positives (all8 conventions×4widths×7periods),224 positives with the literal24 crib letters (same cells),16 alias diagnostics (each convention at constant nominal period6/width7 and primitive-period2 repeated to nominal8/width8),56 independent uniform ciphertext controls (28 uniform clue strings;28 literal clue strings). All plaintexts length97; mask zero-based21:34 and63:74. No sample rejection by uniqueness, score, solvability or speed. Positive keys are unfiltered IID numeric symbols of the nominal period, so rare shorter-period aliases are retained. The period-two alias stratum uses distinct first two symbols. Aliases may be compatible under multiple descriptions. No English scorer or corpus is used.

Tiny tests must independently enumerate all keys/routes for a small alphabet and compare complete solutions of all conventions, and verify alphabet adapters and alias canonicalization. Development examples can be used only before final freeze and never substituted for blind evidence.

## Frozen gates and stopping

1. All tiny complete solution sets agree with an independent brute-force implementation; exact re-encryption and canonical alias tests pass.
2. Every heldout run completes within resource bounds. Any timeout/exception invalidates the target gate until a documented pre-specified recovery is reviewed; no silent omission.
3. Full independently reconstructed raw and canonical operator/plaintext solution sets agree for every heldout input.
4. Every declared in-family plant is present, including alias cases.
5. At least95% of224 uniform positives and at least90% of224 literal-clue positives have exactly one plaintext. Report both counts and uncertainty; these are recovery gates, not historical likelihoods.
6. At most1 of56 independent uniform-ciphertext controls has any compatible plaintext. Preserve every control result; this is not a project-wide error probability.
7. Independent audit verifies frozen hashes, resource receipts, baseline coverage and all gate calculations.

Pass permits one parent-reviewed exact K4 evaluation and one independent reference evaluation. Failure means stop this target branch and record the specific failing gate, without broadening families or weakening thresholds. A coding/resource defect discovered after heldout unblinding requires preserved original receipts, explicit review and a fresh seed namespace before claiming blind success.

## Resource limits and receipts

Overall study budget at most8CPU hours and8GiB, including validation, reference and audits. Production worker address space capped1GiB; each child solver1GiB, hard20CPU seconds and30wall seconds, internal15CPU seconds. Independent reference capped1GiB with explicit per-input CPU budget60seconds and90wall timeout. Worker+one child conservative sum remains2GiB; jobs sequential. Reserve600CPU seconds for preparation, compiler and tiny checks; each batch charges full parent and child rusage in a finally receipt even on failure, and stops before the next case if the remaining study allowance is below180CPU seconds. Parent CPU and terminated-child charges must be included. No paid APIs, checker submissions, new packages or external services. Record command/compiler/environment, input/output/code hashes, CPU time and maximum RSS for all executions. A resource failure is inconclusive, not an exclusion.

## Interpretation and end-of-run workflow

Complete absence of solutions excludes only the exact fixed domain above. Compatible solutions are not historical identifications. Re-encryption is necessary but insufficient; never select a preferred sentence from a large family without independent evidence. Do not equate new algebraic conventions with new observed K4 facts.

Reconcile research/HYPOTHESES.md, research/EXPERIMENTS.md and reviewed classifications, regenerate navigation and verify documentation before selecting Q-02. Preserve original artifacts, corrections and audits. Q-02 is a separately frozen reverse-stage model, not an automatic parameter expansion inside057.
