# Study 060 — two ciphertext-driven evolving alphabets

**Completed exact bounded exclusion:** two independent engines found zero compatible descriptions or plaintexts among 208 distinct encryption functions. This is not a K4 solution or an exclusion of all evolving alphabets.

- [Findings and limitations](REPORT.md)
- [Frozen protocol](PROTOCOL.md)
- [Independent blind-benchmark audit](BENCHMARK-AUDIT.json)
- [Independent target audit](TARGET-AUDIT.json)
- [Complete reproducible code, data, seeds, raw outputs and receipts](study-060-evolving-alphabets.zip)
- [Archive manifest](MANIFEST.json), [checksum](SHA256SUMS), [verification receipt](ARCHIVE-RECEIPT.json)
- [Method learning](METHOD-LEARNING.md)
- [Canonical working to-do list](../HYPOTHESES.md)

The two arms are ciphertext-driven alphabet exchange and fixed-reference-index prefix reversal. Each has 104 fixed configurations using AZ/KRYPTOS reference and initial alphabets, plus one pointer/offset. No arbitrary alphabets, resets, extra layers or rescue tweaks were tried.

Before K4, all 480 blind complete solution sets agreed, all 416 plants were uniquely recovered, and 0/64 matched random controls fit. Independent tiny truth tables and pairwise separating witnesses validate correctness and distinctness. Extract the archive and follow its README to reproduce; the original sealed evidence is retained unchanged.
