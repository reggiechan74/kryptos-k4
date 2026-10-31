# Candidate-first 057 — alphabet-role and Beaufort extensions

**Completed exact bounded exclusion.** Both independently checked engines return `UNSAT_COMPLETE`: no K4 plaintext/key/route satisfies the frozen family. This does not exclude reverse stage order, feedback or arbitrary layered ciphers.

- [Detailed findings and limits](REPORT.md)
- [Frozen protocol](PROTOCOL.md)
- [Independent benchmark audit](BENCHMARK-AUDIT.json)
- [Independent target audit](TARGET-AUDIT.md)
- [Complete code, fixtures, seeds, results and audits](candidate-first-057-20261031.zip)
- [Archive checksum](SHA256SUMS)
- [Canonical working to-do list](../HYPOTHESES.md)

Scope: plaintext and ciphertext alphabet roles each AZ or KRYPTOS, sign ±, arbitrary nominal periodic keys 2–8, then unpadded ragged columnar transposition widths 6–9 and all column orders. Eight conventions include the 056 baseline as regression. The independent reference covers 22,901,760 route/period/convention trials; these are not all distinct new operators. Complete 97-position permutation maps remove key-period and cross-convention aliases.

Before target evaluation, all 520 blind cases completed with exact independent solution-set agreement; 464/464 planted operators included; 221/224 uniform and 224/224 literal-clue positives uniquely identified; 0/56 random controls fit. The three ambiguous positives are retained. No natural-language score, paid checker or Site change was used.

The archive contains the original initial/final freezes, independent checks, synthetic answer files, raw solver outputs and resource receipts. It contains no source-corpus downloads. Reproduction commands are in its `source/README.md`; compile the bundled C++ source on your platform. Frozen historical artifacts are retained unchanged.
