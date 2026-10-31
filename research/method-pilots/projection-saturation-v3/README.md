# Projection saturation v3: completed synthetic validation

**Exact masks preserved; saturation remains optional and default-off.** This completed study is separate from the later incomplete residual cohort and from the independently numbered residual reference v3.

All **480 outputs** in one fixed 40-case, four-arm, three-repeat synthetic run matched the complete maximal-support oracle. The independent release review rechecked **47,412 sparse per-value witnesses**, **78 certificates**, seals and descriptive arithmetic. No stage failed, capped or was dropped.

| Charged-stage sum of paired case medians | Saturation off | Saturation on | Faster / slower cases |
| --- | ---: | ---: | ---: |
| CRT | 24.405472 s | 13.323356 s | 26 / 14 |
| Parity | 16.280120 s | 9.048368 s | 30 / 10 |

These mixture-dependent reductions are **not universal speedups**. Ordinary-case aggregate gains were only 1.32% / 0.83%; the ordinary CRT median case regressed about 5%. Worst individual charged-stage regressions were **79.65% / 35.40%**. Four dependent misspecified twins each forced one wrong hidden response. All arms returned the same exact conditional masks: no comparative recovery gain, model-membership proof or recovery of positions 0–5.

[Full results and retained losses](RESULTS.md) · [Conditional masks](CONDITIONAL-MASKS.md) · [Independent release review](INDEPENDENT-RELEASE-REVIEW.md) · [Resource ledger](RESOURCE-ACCOUNTING.json)

## Evidence and reproducibility

The [complete evidence archive](completed-synthetic-evidence.zip), [archive receipt](ARCHIVE-RECEIPT.json) and [public provenance map](PUBLIC-PROVENANCE.json) preserve the source freeze, pre-draw implementation audit, all outputs/receipts and properly released synthetic truth for **this completed saturation study only**. They contain no failed residual-cohort seed or truth.

Four prose copies remove internal coordination wording or clarify public-byte provenance. Computational sources, results, resource receipts and original manifests remain unchanged. Historical manifests/seals identify original hashes; the new public map identifies distributed bytes. Generic absolute execution-layout paths in frozen receipts/code are disclosed historical provenance, not a portability guarantee. The original-to-standalone map retains hashes with namespace-relative source paths; private omission labels are generalized.

The archive README documents an expensive **archival recheck**, not a fresh validation. Publication ran only static/docs and integrity checks. Shared-filesystem custody was procedural, not access-control blindness. Released fixtures cannot be reused as fresh holdout data.

Total deduplicated managed experimental CPU including historical work and independent review: **488.783194 seconds**, below the 4,908-second conservative allocation. The outer holdout charge includes its inner stages; do not add them twice. Lightweight bookkeeping is not claimed exhaustively metered.

No target run, separate-repository/global novelty claim or further experiment is admitted. Consult the [canonical queue](../../HYPOTHESES.md) for the later residual-method checkpoint.
