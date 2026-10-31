# Study 061 — sum-locked block rotation

**Completed exact bounded exclusion:** both independent engines return zero compatible key cylinders across 160 structural cases. This is not a K4 solution or a general exclusion of nonlinear block ciphers.

- [Findings and limitations](REPORT.md)
- [Frozen protocol](PROTOCOL.md)
- [Independent benchmark audit](BENCHMARK-AUDIT.json) and [target audit](TARGET-AUDIT.json)
- [Exact prior-route/key-domain review](PRIOR-COVERAGE.md)
- [Complete source, fixtures, raw outputs and receipts](study-061-sum-locked-block-rotations.zip)
- [Manifest](MANIFEST.json), [checksum](SHA256SUMS), [archive verification](ARCHIVE-RECEIPT.json)
- [Method learning](METHOD-LEARNING.md)
- [Canonical working to-do list](../HYPOTHESES.md)

Scope: AZ/KRYPTOS, phase-zero periodic additive keys of periods 1–8; consecutive blocks of widths 3–12 rotated RIGHT by integer block sum modulo actual length, no padding. Previously excluded all-zero keys are not new coverage. These are structural descriptions, not 160 distinct keyed operators.

All 416 blind solution sets agreed, all 352 plants were retained, sparse plants correctly retained seven free key residues, and 0/64 random controls fit. Complete tiny truth sets and the sum-invariance proof support completeness. Route overlap checks are separately accounted computations, not cipher-search trials. No post-failure rule changes or extra target runs.

Extract the archive and follow its README. Third-party sources are represented by pinned URLs and hashes, not redistributed without verified permission. The EXT012 historical serialized universe was reconstructed exactly; its unavailable original executable revision remains an explicit limitation.
