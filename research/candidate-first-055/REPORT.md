# Candidate 055 — forced-fragment language screen

**Result: NO DIRECT-ENGLISH-KEY CONTINUATION UNDER THIS SCREEN.**

Calibration passed all **17/17 frozen admission checks**. None of K4’s 12 forced fragment pairs survived the unchanged screen. The best score was **−7.992897 bits/letter**, **3.607249 bits/letter below** the frozen threshold of **−4.385648**. One primary target computation and one independently implemented repeat agree. **Study 055 stops here; no decoder or new hypothesis was run.**

This is a bounded research-priority decision, **not proof that English running keys are impossible** and not a decipherment. No repository publication or Site change was performed for 055.

## What was fixed and when

- Final reviewed protocol: `PROTOCOL.md`, SHA-256 `793e4aea979227eb6b1bc12f2a490712b2db8f26c276c01c69878c1773a71f0d`.
- The unchanged 053 order-4 model was reused: 1,600,000 training letters from eight works by Austen, Chesterton, Edgeworth and Melville; smoothing `[0.5, 5, 10, 20]`. Its binary SHA-256 is `cf21822e9078c9a9d810cbd5ea57db4f4fd440db793c7f5dd4c3cecf49f1212b`.
- `freeze.json` pins 314 source, fixture, code and provenance files. It was issued before any new 055 language score. Target fragments were already known in this research project: this is **frozen before this new evaluation**, not blind preregistration before seeing K4.
- Development alone determined the threshold. `threshold.json` was saved before held-out test scores. No model, source role, fixture, criterion or threshold changed after scoring began.
- After calibration and two independent calibration replays passed, the parent authorized the target at **2026-10-31 01:53:35 UTC**. An additive `target_stage_freeze.json` pinned target orchestration and reference-report semantics before the first target score; the original frozen mathematical code remained unchanged.
- The public 053/054 receipts were fetched at repository commit `5b6cd7ac47d35a7afdd26a9d0109d95a726b2067` and verified byte-for-byte against local originals. All 658 snapshotted original 053/054 files remain unchanged.

## Statistic and scope

`S = [L(key[21:34]) + L(key[63:74])] / 24`, where each fragment starts with a unigram and its context grows to order four. Context resets between fragments. Higher values are more English-like under this model. A tableau survives if `S >= tau`; a ciphertext case survives if its maximum across all 12 tableaux does.

Only the literal cribs EASTNORTHEAST and BERLINCLOCK, with their fixed positions, enter the calculation. The 29 missing letters, 73 unknown plaintext positions, word segmentation and long-range coherence are not scored. All two plaintext alphabets × two ciphertext alphabets × three operations are retained. Key residues are spelled in the plaintext-axis alphabet and then scored as literal A–Z letters.

## Sources and leakage audit

The source plan retains 88 pinned documents: eight training documents, 44 development documents and 36 test documents. A further Austen work is excluded by author policy. Every pinned raw/body/normalized/offset checksum matches the committed 054 receipt. There are no exact normalized document duplicates, cross-role source-group intersections, or surviving sampled-window duplicates against training or another role.

| Source groups | Fiction | Nonfiction / public essay | Archaic / verse |
|---|---:|---:|---:|
| Development | 6 | 22 | 2 |
| Test | 9 | 13 | 3 |

Each role has 100 distinct nonoverlapping positive 97-letter windows per stratum. Another 200 windows per role support letter-scrambled references; another 200 test bases support descriptive word-order/deletion stresses. All **1,200 natural reference bases** are distinct, nonoverlapping in their source documents, within protected work segments, and absent as exact 97-letter strings from every full training document. There are **648 protected compilation boundaries**. Descriptive transformed 300-letter source regions are not asserted independent of every neighboring base.

Before any score, independent review corrected sampling role-priority order (fixture bytes unchanged) and caught a Blake Songs-of-Experience / Book-of-Thel boundary defect. Eight explicit Blake boundaries were added, the original deterministic sampler was rerun, and earlier unscored artifacts were retained under `prefreeze/`. No target score motivated a source change.

Attribution qualifications remain: Bryant is a retelling/compilation source, not verified sole authorship; inaugural groupings are conservative speaker/surname groups, not verified ghostwriters. Machiavelli and identified translator W. K. Marriott remain one test group. Modern electronic transcriptions do not certify exact historical editions. Sources were previously present in 053/054, not newly unseen project-wide controls.

## Calibration

The fifth-smallest development true-key scores were −3.837552 (archaic), −4.385648 (fiction) and −3.616541 (nonfiction); the minimum set `tau`. Development true-key survivors were 100/100, 96/100 and 100/100 respectively. Development uniform and letter-scrambled cases each had 0/200 survivors.

| Held-out admission measure | Observed | Required |
|---|---:|---:|
| Archaic / verse true keys | 96/100 | ≥90/100 |
| Fiction true keys | 98/100 | ≥90/100 |
| Nonfiction true keys | 100/100 | ≥90/100 |
| Worst eligible author/source-group retention | 90.91% | ≥80% |
| Archaic author-bootstrap lower sensitivity limit | 93.94% | ≥80% |
| Fiction author-bootstrap lower sensitivity limit | 94.95% | ≥80% |
| Nonfiction author-bootstrap lower sensitivity limit | 100% | ≥80% |
| Uniform-case acceptance | 0/200; one-sided exact 95% upper bound 1.4867% | Upper bound ≤15% |
| Letter-scrambled acceptance, equal-group weighted | 0% | ≤20% |
| Letter-scrambled author-bootstrap upper sensitivity limit | 0% | ≤30% |
| Proper-name subset | 18/20 | ≥18/20 |
| Historical-spelling subset | 18/20 | ≥18/20 |

Arithmetic, provenance, normalization and leakage gates also pass. All group counts, 10,000-resample bootstrap draws and leave-one-group-out rates are retained in `results/calibration_gate.json`. The bootstrap is a descriptive group-sensitivity calculation, not a reliable population confidence interval, especially with only three archaic test groups. Zero scrambled successes makes its empirical bootstrap degenerate at zero; it does not establish a zero population acceptance probability.

True generating-key retention, not merely rescue by the 12-way maximum, governs positives. Each of the 300 test keys generates 12 correlated synthetic ciphertext cases; these are not 3,600 independent English keys. All 12 generating conventions had the same case-survival counts as true-key retention in each stratum.

Both authentic subsets are the first qualifying windows in frozen fixture-ID order and are entirely archaic/verse. They overlap in four windows; the same two windows (TA070 and TA071) fail both subsets. Only **10/20 name tokens and 5/20 spelling tokens intersect the scored fragments**. Therefore this gate is window-level coverage, not robust measurement of every name/spelling within the 24 letters. Authentic compressed-writing genre coverage is absent.

## All 12 target scores

Units are bits per letter. Every margin is `score − tau`; a nonnegative margin is required.

| Plain axis | Cipher axis | Operation | Score | Margin | Survives |
|---|---|---|---:|---:|---|
| AZ | AZ | vigenere | -10.070060 | -5.684412 | No |
| AZ | AZ | beaufort | -9.214748 | -4.829100 | No |
| AZ | AZ | variant_beaufort | -11.098894 | -6.713246 | No |
| AZ | KR | vigenere | -9.367219 | -4.981571 | No |
| AZ | KR | beaufort | -9.021259 | -4.635611 | No |
| AZ | KR | variant_beaufort | -7.992897 | -3.607249 | No |
| KR | AZ | vigenere | -9.146598 | -4.760949 | No |
| KR | AZ | beaufort | -11.875352 | -7.489704 | No |
| KR | AZ | variant_beaufort | -9.128420 | -4.742771 | No |
| KR | KR | vigenere | -8.414196 | -4.028548 | No |
| KR | KR | beaufort | -9.791700 | -5.406052 | No |
| KR | KR | variant_beaufort | -10.713467 | -6.327819 | No |

The best convention is **AZ plaintext / KR ciphertext / variant Beaufort**. All recovered fragments exactly match the committed 054 pairs; the full pairs are retained with every score in `results/target_result.json`.

## Reference comparisons — not English probabilities

- The target maximum is below **all 100 true-key scores in each of the three held-out strata** (also below every individual test source-group reference score). This compares the target maximum with the explicitly labeled true-key score distribution.
- Separately, it is below **all 100 positive case-max scores per stratum under every one of the 12 generating conventions**. All convention-specific comparisons are retained; none was selected after looking at the target.
- Among 200 independent uniform ciphertext cases, **86 case maxima are at least the target maximum**, and 114 are below it. The prescribed uniform-reference upper-tail rank is **(1 + 86) / 201 = 0.432835821**. This is a reference rank, **not** the probability that English is impossible or that K4 is solved.
- Every individual target-tableau score also has separately labeled true-key stratum/source-group, generating-convention case-max, and uniform-case-max comparisons in the result JSON.

## What the descriptive stresses show

| Altered/reference construction | True-fragment survivors | Case-max survivors |
|---|---:|---:|
| One seeded adjacent-letter transposition | 290/300 | 290/300 |
| Word-order scrambling | 100/100 | 100/100 |
| Independently paired English-source fragments | 99/100 | 99/100 |
| Deterministic function-word deletion | 100/100 | 100/100 |

These are not mandatory negative truths. Their high acceptance is an important limitation: this local character model does **not** establish semantics, sentence order, common source provenance, a feasible 29-letter bridge or full 97-letter English coherence. No global confirmatory p-value follows from this adaptively motivated study.

## Verification and compute

- Independent pre-calibration verifier: 8,112 exhaustive residue/tableau checks; 456 generated-fragment recovery checks; 38 fixed non-target score fixtures; 26 malformed-input checks.
- All 18,279 conditional-probability rows normalize (maximum error 2.22×10⁻¹⁶). All 475,254 table entries reconstruct exactly from the unchanged count tables and smoothing rule.
- Two separately reviewed calibration replays validate 8,600 ciphertext cases and 103,200 tableau scores. Largest primary/independent discrepancy: 5.33×10⁻¹⁵ bits/letter, below 10⁻¹⁰.
- Target independent repeat: PASS; 12 scores, every fragment/margin/rank checked; maximum score discrepancy 3.55e-15 bits/letter.
- Charged experimental CPU: **120.880 seconds**, including 100 seconds of conservative development/provenance allowance, against a 3,600-second cap. Peak observed RSS: **0.617 GiB**, below 8 GiB. The ledger retains exact process receipts plus clearly labeled conservative debits.
- No post-score correctness repair, threshold change, source replacement or failed scoring run occurred. All pre-score corrections and the unavailable optional `/usr/bin/time` command are recorded in `PRE_SCORE_CHANGE_LOG.json`; that command failed before any fixture or score process began.

## Artifact map

| Artifact | Purpose |
|---|---|
| `PROTOCOL.md`, `IMPLEMENTATION_SPEC.json` | Final reviewed protocol and exact executable criteria |
| `freeze.json`, `threshold.json` | Pre-score input/code freeze and pre-test threshold freeze |
| `target_authorization.json`, `target_stage_freeze.json` | Parent admission and additive pre-target orchestration freeze |
| `source/source_manifest.json` | Every source path/hash/group/role and protected work segment |
| `fixtures/` | All positive, random, scrambled and descriptive fixtures; offsets, seeds and allocations |
| `stress_manifest.json`, `stress_review_ledger.json` | Authentic names/spellings and full ordered annotation decisions |
| `results/*cases*.jsonl`, `results/*scrambled*.jsonl`, `results/uniform*.jsonl` | All 12 scores for every calibration case |
| `results/calibration_gate.json` | All 17 gates, counts, groups, bootstrap and leave-one-group-out results |
| `results/target_result.json`, `results/independent_target.json` | All target scores, fragments, margins and source-stratified ranks |
| `results/independent_verification.json`, `results/independent_analysis.json`, `results/external_audit/` | Independent verification and review receipts |
| `results/compute_budget.json`, `results/execution/` | Aggregate resource cap and process receipts |
| `results/final_integrity.json`, `CHECKSUMS.json` | Frozen/original-file integrity and final artifact inventory |
| `prefreeze/` | Retained unscored preparation versions and correction receipts |

Execution commands are retained in the resource ledger. Replay requires the unchanged sibling `candidate-first-053` model/count tables and pinned `candidate-first-054` raw assets at their recorded paths; these dependencies and public acquisition URLs are hash-identified in the manifests. Existing score runners refuse receipt overwrite. A later independent reproduction must use a separate output location and must not silently modify these historical receipts.

## Key hashes

| File | SHA-256 |
|---|---|
| `freeze.json` | `489d519d2d507d3104433f2e8ca55fa5fd96e3f066233ea39a4f60a8e9fcf324` |
| `threshold.json` | `e87318170f134d2679463a0f6a9401f16ff274d453850246e476870e4e606b1f` |
| `target_stage_freeze.json` | `ed1108abce0a19af37eaf153550b59fffd7779b996c275a479bac0de28994540` |
| `source/source_manifest.json` | `84fa8cfb35520789025b2379584c40fd611772d8d78b1b8a3f6f7481f8ece452` |
| `stress_manifest.json` | `0d9d5afb077fa544856d3958c872163dc356c26a3baf597a70774a680b440d94` |
| `core.py` | `09fc5ab385bf1dc1699279d5b94fb09ebdda2ac7ad7c77dae8df741ac6912c33` |
| `run_calibration.py` | `860b266f04c99335128109cf3c304390a65822b97f23d7206ceef4d8e430c7f7` |
| `results/calibration_gate.json` | `7ada4636932f3c3ed508a6b62cbeed723ec637cfd8c05273aae26b8325c96bc8` |
| `results/target_result.json` | `d8a1525fc76722fa8592d74e242fca6a6c4d02c3655b930c4c6f007ab0d1d03d` |
| `results/independent_target.json` | `6e6122e32a90ca4ee90ba35b9e95d60a992a354c90f3855fa684344bbd787eb4` |

**Stopping decision:** no direct-English-key continuation under this screen. Broader running-key families, other models or ciphers are neither proved impossible nor authorized for a new search by this result.
