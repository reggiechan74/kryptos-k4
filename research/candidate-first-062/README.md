# Study 062 — ciphertext-steered Josephus

**Completed exact bounded exclusion:** both independent engines returned zero compatible cylinders across 3,104 structural descriptions / 388 target maps. This is not a K4 solution or a general exclusion of message-dependent routes.

- [Findings and limits](REPORT.md)
- [Frozen protocol](PROTOCOL.md)
- [Independent benchmark audit](BENCHMARK-AUDIT.json) and [target audit](TARGET-AUDIT.json)
- [Prior-route/key-domain review](PRIOR-COVERAGE.md)
- [Complete code, fixtures, raw outputs and receipts](study-062-ciphertext-steered-josephus.zip)
- [Manifest](MANIFEST.json), [checksum](SHA256SUMS), [archive verification](ARCHIVE-RECEIPT.json)
- [Method learning and proposed source-checking improvement](METHOD-LEARNING.md)
- [Canonical working to-do list](../HYPOTHESES.md)

Scope: AZ/KRYPTOS, 97 initial slots, two fixed directions, key periods 1–8 indexed by emission. After emitting a letter, advance from the next directional survivor by one plus the emitted letter's rank. Previously excluded all-zero keys are removed symbolically; free residues are not guessed.

All 872 blind sets agreed, all 808 plants were retained, and 0/64 null controls fit. Importantly, 120 of 776 full-mask plants remained ambiguous/free: the implementation preserves ambiguity rather than inventing unique answers. No target-dependent change or extra target search occurred.

The archive retains original and independently corrected external-literal transcription receipts, resource costs and all controls. Third-party sources remain private; pinned source URLs/hashes are public. A read-only literal checker is proposed as a separate validation task, not claimed already validated or globally novel.
