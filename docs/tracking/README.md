# Research trackers

[Project overview](../../README.md) · [Canonical hypothesis ledger](../../research/HYPOTHESES.md) · [Canonical experiment log](../../research/EXPERIMENTS.md)

- [Hypothesis families](HYPOTHESES.md): 60 stable IDs, statuses and links to exact tested / untested scopes.
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
