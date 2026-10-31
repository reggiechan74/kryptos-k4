# Study 056 — independent final audit of the resource-recovery benchmark

## Decision

**PASS for proposing one bounded S-based full-family target experiment, subject to the parent's explicit authorization. No target was run.** Numerical gates 1–4 and 6, complete-set correctness, blinding chronology and replacement resource compliance pass. **Learning-specific gate 5 fails.** There is no demonstrated benefit from learned-conflict machinery, nor material S-over-P benefit. The supported result is efficient ordinary/shared constraint propagation over the new bounded model family, not a new category of key elimination or proof of historical applicability.

The original held-out run remains preserved as numerical-only evidence with incomplete aggregate-memory certification. It is not silently merged with, substituted for or counted as an additional independent success in the replacement gates. The resource-only repair and fresh holdout were explicitly authorized by the parent. See `../ORIGINAL-RUN-AUDIT.md` for that run and its diagnosed watchdog defect.

## Frozen scope and chronology — PASS

- Protocol v2 remains `58cf2196845555b7355f7b6c7f59b11033c462832ad7c1e9ceff79a1ad61d6ea`: standard A–Z periodic Vigenère at plaintext indices, then row-filled unpadded top-to-bottom columnar transposition; unknown widths 6–9, periods 2–8 and every column order. No model expansion, language score, keyword restriction, target-derived key or actual target ciphertext.
- Replacement code freeze: `c9f6d54a3f9fccf48ba4e22cb54d69b974d1bc3f6215a26145aa6d0bc58f182e`. Independent no-cipher resource probes passed before fresh generation.
- Fresh namespace `study056-resource-recovery-v2`; generation at 02:47:44 UTC. Same 256 allocations/rules; fresh OS seed; no runtime/uniqueness filtering. Generator changes were namespace selection only. Solver source/binary, oracle, all numeric gates and W=S remained unchanged.
- Final manifest: `5eba2499c0a05408330e885c0ba163831c28632655eaf0aa1f787c81dd09d231`. All 40 public file hashes verified at 02:48:52 UTC with no held-out outputs present. Input commitment `18f2dcd6ca76c1b1882c6b908aa135776b55d736d7388962b71ac4d3d59c9780`.
- Replacement output seal: 02:55:36.655451 UTC; result-hash manifest `3ca7242d0b940359c4d984e0f88c270ddf443a4ccb8fb2dd24cc53b61dd987fd`. Answers were opened only after verifying the complete seal. Fresh generation replay reproduced inputs and answers byte-for-byte after unblinding. All 40 frozen public hashes remained unchanged afterward.
- Blinding is procedural in a shared workspace, not cryptographic isolation. The solving harness blocks private answer/seed opening and sees only opaque IDs, ciphertext and literal clues. Every case searches all 28 width/period cells. File names and IDs do not encode generating width/period.
- The superseded protocol-v1 corruption-control error was corrected before any held-out generation/score in the inspected records. Do not confuse that pre-score correction with the later resource-only recovery of the first protocol-v2 run.

## Correctness and exact completeness — PASS

The final, unchanged solver passed the declared exhaustive tiny suite plus a preregistered rectangular supplement: **288,363 fixtures, 1,153,452 solver calls and 2,277,336 witness re-encryptions**. Empty masks and unobserved key slots are included. The auditor independently checked **all 24,780 recorded learned clauses against all 697,472 concrete premise completions**, not merely final counts, and checked all 3,040 tiny cross-branch activation receipts. Zero unsound exclusions or complete-set discrepancies.

For the replacement holdout, a separately written direct row-matrix reference enumerated **732,856,320 route/period trials**, exactly 2,862,720 for each of 256 fixtures. It infers unrestricted keys from transported clues instead of enumerating 26^p keys. It uses no production placement helpers or learned cache. Every complete raw solution set matched E/P/S/L, including all nominal aliases. Canonical full dependency/shift operators, full plaintext sets, forced positions and set hashes matched independently. All **1,600** returned witness records re-encrypted exactly and satisfied all 24 clues.

Ragged starts include exact subset-sum length offsets, not just ranks. Pairwise placement consistency and nonoverlap imply a complete tiling, and the production crib mask observes every key residue. Tiny missing-residue cases correctly enumerate free coordinates. The entire union is completed before unique/ambiguous/UNSAT classification; no first-witness result is called recovery.

All methods returned 169 complete unique-plaintext cases, 8 complete ambiguous cases and 79 complete UNSAT cases. Across fixtures there were **400 raw descriptions, 241 canonical operators and 241 full plaintexts**; these are separate quantities. All 128 in-family planted operators and full plaintexts were recovered. Full-reference set digest: `75755ad053d495aa51661b8ef30eaf13f9eb78e0d8a92c7ed04968f312b8415f`.

All nine held-out learned clauses were independently proved sound and checked against exhaustive full-union solution sets. Two later cross-branch activations in one fixture were independently validated; this is far below the learning acceptance threshold.

## Exact preregistered gates

| Gate | Frozen requirement | Replacement result | Status |
|---|---|---|---|
| 1 Correctness | Zero tiny/full-set errors or unsound exclusions | Zero; independent sets/witnesses/clauses agree | PASS |
| 2 Completion | W completes 256; E ≥244 | E=P=S=L=256/256 | PASS |
| 3 Identifiability | U+J+L ≥80/84; literal ≥26/28 | 83/84; 28/28 | PASS |
| 4 Representation | E/W geometric-mean CPU ratio ≥2; bootstrap lower >1.25 | **17.327106×**, 95% **[17.132535,17.517474]** | PASS |
| 5 Learning | S/L ≥1.20; lower >1; ≥50 reused clauses in ≥10 fixtures | **1.002360×**, [0.988463,1.015533]; **2 clauses / 1 fixture** | FAIL |
| 6 Uniform calibration | At most 1 unique fit among 56 uniform-C controls | **0/56 SAT or unique** | PASS |

The auditor independently reproduced all reported counts, exact Clopper–Pearson intervals and deterministic paired bootstrap arithmetic (10,000 resamples, seed 56003110). Identifiability CI: 83/84 gives [0.935448,0.999699]; 28/28 literal gives [0.876564,1]. Primary unique counts: U 28/28, R 27/28, J 27/28, L 28/28. Alias diagnostics: 8/8 unique; constant-crib degeneracy: 2/8 unique. Ambiguous diagnostics remain in all correctness and timing results.

P achieves essentially the same gain: E/P 17.313936×. P/S is 1.000761×, 95% [0.987375,1.014648]. Therefore do not attribute all E-to-S improvement to the placement CSP rather than ordinary early key propagation.

## Uniform, mismatch and corruption strata — PASS

- **Uniform controls:** 0/56 SAT and unique; exact 95% rate interval [0,0.0637501]. Only these 56 enter gate 6. This is an engineering calibration policy, not a project-wide p-value or evidence of historical intent.
- **Outside-family generator diagnostics:** all 16 UNSAT; interval [0,0.205907]. This was determined by the full exact reference, not assumed from the generating class.
- **One-symbol corruption diagnostics:** 49 changed ciphertext positions mapped to noncrib plaintext positions. Every one retained its exact original operator and corresponding one-letter-modified plaintext, independently re-encrypted and recovered uniquely. The remaining 7 mapped to crib positions and were UNSAT. SAT/unique rate 49/56, interval [0.759267,0.948235]. These 49 valid modified-plaintext fits are **not false positives** and are not pooled with uniform controls.

## Resource correction and replacement verification — PASS

The original watchdog relied on an unavailable `/proc/.../children` API and returned zeros. The replacement instead uses an announced sole solver PID and known-PID `/proc/stat` observations. Both worker and its one persistent solver have hard/soft **1 GiB address-space limits**, giving a hard additive **2 GiB** pair bound independent of sampling. Twenty repetitions share these same two processes, with no relaunch or unbounded descendants.

The worker's CPU hard limit is 2 s after child spawn and before PID announcement; the solver's is 16 s. Exact completed-call accounting uses waited worker-and-descendant CPU plus parent monitoring CPU. Normal timings include worker startup/import, solver startup, all 28 cells, preprocessing, per-repeat canonical projection, output serialization and monitoring. The former inner metric is descriptive only. All methods receive identical timing boundaries and limits.

Independent no-cipher probes verified normal/reaped execution, an aggregate CPU failure while each component remained below the aggregate trigger individually, both half-memory limits, duplicate-announcement cleanup, and descendant peak-RSS propagation. Every abnormal process group was stopped; unobservable orphan CPU is conservatively charged from enforced hard bounds instead of called measured zero. Unconfirmed cleanup aborts the benchmark. No such failures occurred on the replacement holdout.

Independent replay of **all 1,024 method/fixture resource receipts** established:

- 1,024 complete batches; 20 repetitions each; zero resource failures or failure reserves.
- Maximum inclusive batch CPU **1.733977410 s**, below 20 s.
- Maximum conservative measured worker+solver peak upper bound **29,097,984 bytes (27.75 MiB)**, below 2 GiB.
- Every batch had positive RSS observations and known-live-child samples; minimum two live-child samples.
- Primary batch CPU sum **371.448938309 s**; full benchmark **372.289077402 s**. The remaining **0.840139093 s** of shared controller/output work is charged globally rather than hidden. No timeout censoring or survivor-only timing issue arises.
- Original and replacement work remain charged to one 28,800 CPU-second / 8 GiB study budget. The frozen cumulative pre-replacement charge is 1,043.315964 s; replacement benchmark plus the new post-seal auditor charge brings the established charge to 1,450.093309 s before the final independently recorded author/reporting allowance. This is far below the cap. The final worker cumulative ledger should be retained with this report. Original failed-resource certification is not retroactively declared repaired.

## Coverage and remaining interpretation limits

The ciphertext-free novelty certificate was independently replayed exactly: 27,323 prior 050 affine operators have 7,985 dependency-permutation components; only 14 of the 408,960 proposed routes overlap that projection. Thus at least **408,946 routes, with every allowed key on those routes**, are outside 050. This is a conservative model-domain statement, not a claim of worldwide novelty or disjointness from every past experiment. Generic keys and residue elimination already existed in prior work.

No scientific or operational audit blocker remains for the **specified bounded proposal**. A later target run must still be explicitly authorized by the parent, use a fresh context/cache, retain all widths/periods/orders and the stated caps, and report complete operator/plaintext counts or honest INCONCLUSIVE. A witness would establish only model-conditional compatibility and require exact re-encryption/independent checks; complete UNSAT would exclude only this frozen family. Neither benchmark success nor the literal-pattern fixtures establish that the historical target belongs to the family.

## Evidence files

In this directory: `freeze-verification.json`, `independent-resource-probe.json`, `full-reference-replay.json`, `numerical-replay.json`, `resource-receipt-replay.json`, `auditor-resource-ledger.json`; independent sources `independent_full_reference.cpp`, `replay_full_sets.py`, `replay_numerics.py`, `replay_resource_receipts.py`. Original and tiny/coverage audit evidence remain in the parent audit directory. Primary frozen sources, inputs, outputs, seals and author replay remain in `/workspace/shared/candidate-first-056/recovery-v2`.

### Subsequent authorized stage

The statements above that the target was unrun refer to benchmark clearance. After that clearance, the parent expressly authorized exactly one S target pass and one independent full-route verification. They both completed UNSAT within the frozen family and caps. That separate, later result is documented in `../target/FINAL-TARGET-AUDIT.md`; it does not alter the benchmark gates or the no-learning/no-S-over-P conclusions.

## Final all-study budget reconciliation

The final cumulative ledger was independently summed and reconciled: **1,490.148355917 charged CPU seconds (24.84 minutes)** across original development, both holdouts, all resource-recovery probes, independent audits, target calls and conservative reporting/packaging reserves, versus the shared **28,800-second** cap. Auditor charges are included once; the target reference is inside the target-audit reserve. The original memory-monitor limitation remains explicit, while replacement and target aggregate resource receipts pass. See `FINAL-RESOURCE-RECONCILIATION.json` in the audit root and `candidate-first-056/audit/final-resource-ledger.json`.
