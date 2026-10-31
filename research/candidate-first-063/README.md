# Study063 — coupled26/24 accumulator

**Exact bounded target exclusion:** both independent engines returned zero compatible key/start-state/plaintext tuples. **This was a compatibility test, not a unique-recovery demonstration:** all624 planted plaintexts were ambiguous.

- [Findings and limitations](REPORT.md)
- [Frozen protocol](PROTOCOL.md)
- [Independent benchmark audit](BENCHMARK-AUDIT.json), [ambiguity audit](AMBIGUITY-AUDIT.json), [target audit](TARGET-AUDIT.json)
- [Prior-equivalence and source review](PRIOR-COVERAGE.md)
- [Complete code, fixtures, raw tuples, source proofs, reset-trap and receipts](study-063-coupled-carry-accumulator.zip)
- [Manifest](MANIFEST.json), [checksum](SHA256SUMS), [archive verification](ARCHIVE-RECEIPT.json)
- [Method learning](METHOD-LEARNING.md) and [next research decision](../fresh-program-20261031/NEXT-DECISION.md)
- [Canonical working to-do list](../HYPOTHESES.md)

Scope: AZ/KRYPTOS, periodic keys1–6, all624 initial states, OLD-high-digit output and no other layer. Zero keys remain included. Independent crib-entry filters are only lossless supersets; every returned tuple must survive continuous whole97-character replay. No state reset at cribs.

All688 blind complete sets agree, all624 plants are retained and0/64 nulls fit. But each plant has8–126 plaintexts.63 plants vary only at position0,424 more only in the pre-crib prefix,137 also later. Everyplant has a same-key first-symbol alternative with identical nextstate. No English ranking or arbitrary selection resolves that ambiguity.

The final non-search auditor initially assumed an explicit block field; the field-handling repair and original failure/script are retained. No frozen solver, data or output changed, and no extra target search occurred. Third-party source contents stay private; source pins/hashes and our own proof/comparison code are public.
