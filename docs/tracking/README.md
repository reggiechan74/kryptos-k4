# Research trackers

[Project overview](../../README.md) · [Canonical hypothesis ledger](../../research/HYPOTHESES.md) · [Canonical experiment log](../../research/EXPERIMENTS.md)

- [Hypothesis families](HYPOTHESES.md): 63 stable IDs, statuses and links to exact tested / untested scopes.
- [Experiments](EXPERIMENTS.md): a navigable index of log sections, model types and recorded timing.
- [Detailed experiment entries](EXPERIMENT-DETAILS.md): original results, limits, code and receipt links, rebased for this location.
- [Run and artifact receipts](RECEIPTS.md): every tracked JSON result, including synthetic engineering and source reviews. Artifact count is not experiment count.
- [Machine-readable tracker](tracker.json): complete family fields, log entries, source links and explicit timestamp roles.

## Status meanings

**Untested**: no completed specified model. **Specified but not run**: a protocol exists without a result. **Evidence-blocked**: a required observation or physical input is missing. **Narrow negative**: a declared finite domain failed. **Analytical exclusion**: a proof rejects the exact stated assumptions. **Non-identifiable**: fits do not determine a unique key/message or a distinguishing prediction. These statuses are not interchangeable.

## Time and reproduction policy

ISO 8601 UTC is canonical. Run start/end, receipt recording, artifact creation and commit/publication are distinct events. Only explicit timestamp fields are promoted into the tracker. Date-only prose stays date-only; missing run times remain unknown. Directory names and Git timestamps are never used to invent experiment times. Original receipt fields and source paths are retained for inspection.

Regenerate with `python3 experiments/build_research_navigation.py`. This only reads the canonical ledger and tracked receipts; it does not run searches. Edit source records, not generated tables. Historical independent artifacts remain unchanged.

[Preserved original-link exceptions](PRESERVED-LINKS.md) document the only expected unresolved relative file targets in an immutable independent artifact.

## Reviewed record types and future timing

[Curated record classifications](curated-records.json) explicitly assign categories and concise outcomes to every current log section. Mixed records retain combined categories and outcomes. The generator rejects new or renamed entries until their classifications are reviewed; it no longer guesses from titles. Dates in headings or opening dated prose are labeled date-only records, never exact run times.

The shared `RunSnapshot` writer already records UTC start/end for new runs. The common bounded runner additionally records UTC start/end per job, including failed jobs, and an execution kind (`original`, `replay`, `validation` or `unspecified`). Its replay command entrypoints explicitly use `replay`. These fields apply to future runs; no historical receipts are backfilled. Test-only synthetic timing fixtures are validation, not original K4 experiments.

## Overlay scope

FOLD-SLIDE-020 remains a historical column-only study with `dy = 0`. The later [FOLD-SLIDE-2D-001 item-1 study](../../research/FOLD-SLIDE-2D-FINDINGS.md) separately freezes and calibrates all integer row/column offsets under two registrations. Do not transfer old column-only p-values to rows or extend the new calibration to arbitrary words/readouts, fractional offsets or other manual choices. The live Site is a separate presentation/runtime.

[Seven-family subbranch matrix](../../research/SEVEN-FAMILY-REVIEW-046.md) separates completed scoped work from untested or evidence/resource-blocked complements. New 038–046 results remain local for review.
