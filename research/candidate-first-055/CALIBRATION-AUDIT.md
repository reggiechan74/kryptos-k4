# Study 055 calibration — independent audit

## Decision

**PASS: the unchanged frozen gate genuinely admits the target stage.** All 17 admission items passed and were independently replayed. The saved operational outcome is **CALIBRATION ADMITTED; PAUSED BEFORE TARGET**. No target ciphertext was loaded or scored by this audit, and the audited calibration implementation has no target loader. Target continuation remains a separate action for the parent; this report does not perform it.

No arithmetic/model error, frozen-artifact mismatch, unresolved calibration-gate failure, or budget blocker was found. A failed or unavailable mandatory gate would instead require **INCONCLUSIVE CALIBRATION** and no target evaluation—not a favorable-model interpretation or relaxed threshold.

## Per-stage audit

| Stage | Result | Evidence |
|---|---|---|
| Protocol and input freeze | PASS | Reviewed protocol SHA-256 matches; all 314 frozen files verified before and after replay. Freeze issued 2026-10-31 01:51:51.694 UTC, before new 055 scoring. |
| Unchanged 053 model | PASS | Exact published model digest; all 18,279 probability rows normalize within 2.22×10^-16. Primary separate verifier reconstructs all 475,254 entries from pinned counts with zero log-probability discrepancy and smoothing [0.5, 5, 10, 20]. |
| Arithmetic and labels | PASS | All 12 plaintext-axis/ciphertext-axis/operation conventions preserved. Independent forward-enumeration inverses cover all 8,112 single-letter plaintext/key/convention combinations. Key letters are spelled on the plaintext axis and scored as literal A–Z. |
| Fragment statistic | PASS | Exact key slices [21:34] and [63:74]; context reset separately at each 13/11-letter block; divide by 24. No missing-gap, surrounding-key, or full-key MDL contribution. |
| Source provenance and splits | PASS within declared source-group scope | Independently matched raw/normalized/offset hashes and normalization for all 88 retained documents. Four training-author groups excluded from evaluation, including additional Austen work. Development/test groups are disjoint. All Machiavelli/Marriott material remains in one test group; conservative inaugural speaker groups retained. |
| Sampling and leakage | PASS | 1,200 base windows independently checked against raw offsets and normalized source bodies; no overlaps, exact duplicate windows, training-body membership, or recorded-segment crossings. Exactly 100 positives per stratum per role. |
| Synthetic controls and multiplicity | PASS | Replayed both separately seeded 200-case uniform streams; each control jointly derives all 12 candidate tableaux. Replayed all 400 whole-key letter permutations and balanced generating-convention assignment. Twelve encryptions of one positive key are not counted as twelve independent keys. |
| Authentic annotations | PASS with narrow coverage | Independently reviewed all 40 selected tokens and the complete preceding decision prefixes (94 name windows, 71 spelling windows). Raw tokens and modern-form/referent rationales are valid under the written policy. |
| Threshold freeze | PASS | Threshold is the minimum of the three development fifth-smallest true-key scores, not case maxima. Created 01:52:02.883 UTC; test scoring starts 01:52:09.878 UTC. No test or target threshold selection. |
| Full non-target arithmetic replay | PASS | All 8,600 case rows / 103,200 tableau scores independently reproduced. Maximum difference 5.33×10^-15 bits/letter, below 10^-10 tolerance. |
| Calibration statistics and stopping | PASS | All 17 gate decisions identical. Equal-weight whole-source bootstrap, leave-one-source-out values, and all 10,000 bootstrap draws per analysis reproduced exactly. Exact binomial upper bound is applied only to the 200 independent uniform cases. |
| Resource budget | PASS | Primary receipt total 112.219510 CPU seconds plus this audit's exact outer-process 8.253494 seconds = 120.473004 seconds through calibration review, including conservative preparation/development charges. Largest recorded primary peak 662,740,992 bytes; this replay 300,433,408 bytes. Both far below 1 CPU hour / 8 GB. |

The separate primary arithmetic verifier also passes generated fragment recovery, changed-unobserved-letter invariance, arbitrary substring boundaries, explicit block-reset differentiation, and malformed-input rejection tests. My replay implements its own inverse/scorer/statistical calculations and imports neither the primary arithmetic nor its verifier.

## Admission results

Frozen threshold: **−4.385648037504633 bits/letter**, higher survives, ties retained.

Development fifth-smallest scores: archaic −3.837552139392521; fiction −4.385648037504633; nonfiction −3.616541467008892.

| Mandatory component | Observed | Required | Result |
|---|---:|---:|---|
| Archaic true-key retention | 96/100 | ≥90/100 | PASS |
| Fiction true-key retention | 98/100 | ≥90/100 | PASS |
| Nonfiction true-key retention | 100/100 | ≥90/100 | PASS |
| Each eligible source group | Minimum 90.91% | ≥80% for groups with ≥10 keys | PASS |
| Archaic cluster lower sensitivity | 93.94% | ≥80% | PASS |
| Fiction cluster lower sensitivity | 94.95% | ≥80% | PASS |
| Nonfiction cluster lower sensitivity | 100% | ≥80% | PASS |
| Uniform case acceptance | 0/200; upper bound 1.4867% | Upper bound ≤15% | PASS |
| Scrambled equal-group acceptance | 0% across 25 groups | ≤20% | PASS |
| Scrambled cluster upper sensitivity | 0% | ≤30% | PASS |
| Authentic names | 18/20 | ≥18/20 | PASS |
| Authentic historical spellings | 18/20 | ≥18/20 | PASS |
| Arithmetic/provenance/leakage verification | No unresolved failure | All pass | PASS |

The three within-stratum source-group items are separately represented in the 17-item machine gate. Nonfiction groups each contain 7–8 keys, so none meets the ≥10-key trigger; the stratum and cluster conditions still pass. The two authentic subsets share four windows, and both fail the same two fixtures, TA070 and TA071. They are correlated checks, not independent replications.

## Corrections resolved before scoring

- Fixed a development/test sampling-order inconsistency. The old unscored version was retained; this change initially left fixture data hashes unchanged.
- Added missing Blake title/editorial/section boundaries, including the Songs-to-Thel join, then regenerated all fixtures deterministically with the original algorithm. Old sources/fixtures retained. Final manifest records 648 conservative boundaries; no source bytes or source roles changed.
- Aligned stress manifest aliases with the calibration runner, strengthened the synthetic verifier to check the complete freeze rather than merely file existence, and clarified aggregate budget accounting before freeze.

None was a post-score model, threshold, source-choice, or gate revision.

## Interpretation limits that must remain in the result

- This is a bounded research-priority screen, not an English impossibility theorem or evidence that an English key has been found.
- Whole-source bootstrap values are descriptive sensitivity analyses. The archaic stratum has only two development and three test groups; resampling cannot create additional independent styles.
- All first-20 authentic name and spelling windows are archaic/verse because of fixed fixture-ID ordering. Only **10/20 name tokens** and **5/20 spelling tokens** intersect the actual 24 scored letters. Passing these window-level subsets does not establish general robustness to names/spellings inside the scored fragments.
- Compilation groups are not proof of globally unique authorship, and inaugural speaker separation is not verified ghostwriter separation. No unresolved explicit cross-role contributor overlap was found, but anonymous borrowing cannot be ruled out.
- Descriptive word-order-scrambled cases survive 100/100; independently paired-source fragments survive 99/100; function-word deletion survives 100/100; adjacent transposition survives 290/300. These correctly are not mandatory negative-truth controls. They illustrate local-score limitations, not full-key coherence, syntax, 29-letter bridging, or genuine compressed-writing coverage.
- Zero accepted uniform/scrambled references is not zero probability. Only the independent uniform reference gets the exact-binomial statement; no project-wide confirmatory p-value follows.
- The protocol was frozen before this **new** evaluation, not before the project ever saw the target. Target results remain uncomputed at this audit boundary.

## Artifacts and identities

Audit directory: `/workspace/shared/candidate-first-055-audit/`

- `AUDIT_REPORT.md` — this report.
- `replay_audit.py` — independent allowlisted replay code.
- `replay_receipt.json` — machine audit results and verified hashes.
- `execution_01.json` — exact outer-process CPU/RAM receipt; one successful replay, no failed replay attempts.
- `annotation_review.json` — score-free semantic annotation review made before freeze.
- `replay_01.log` — replay log.

Primary directory: `/workspace/shared/candidate-first-055/`

- `freeze.json`, `threshold.json`, `results/calibration_gate.json`.
- `results/independent_verification.json`, `results/independent_analysis.json`.
- `source/source_manifest.json`, `source/independent_source_verification.json`, `source/document_leakage_audit.json`.
- `stress_manifest.json`, `stress_review_ledger.json`, `fixtures/sampling_receipt.json`.
- `results/execution/` — measured and explicitly conservative study-budget receipts.

| Artifact | SHA-256 |
|---|---|
| Reviewed protocol | `793e4aea979227eb6b1bc12f2a490712b2db8f26c276c01c69878c1773a71f0d` |
| Fixed 053 model | `cf21822e9078c9a9d810cbd5ea57db4f4fd440db793c7f5dd4c3cecf49f1212b` |
| Input freeze | `489d519d2d507d3104433f2e8ca55fa5fd96e3f066233ea39a4f60a8e9fcf324` |
| Threshold | `e87318170f134d2679463a0f6a9401f16ff274d453850246e476870e4e606b1f` |
| Calibration result | `7ada4636932f3c3ed508a6b62cbeed723ec637cfd8c05273aae26b8325c96bc8` |
| Independent external replay code | `72ee626eeb91b7f400bf3141fde5f5a10b435c64e0dff97931c0365cfeafe407` |

Primary files, model bytes, scores, historical 053/054 artifacts, and GitHub state were not modified by this audit.
