# Study 056: joint periodic-key and column-route constraints

**The canonical K4 target has no solution in the exact frozen family, independently verified.**

Excluded scope only: standard A–Z periodic Vigenère, arbitrary nominal-period **2–8** seed, then **unpadded ragged columnar transposition of width 6–9**, all column emission orders, top-to-bottom reads, fixed alignment and the 24 public literal plaintext clues. Other alphabets, operations, layer orders, widths, periods, offsets, padding or additional layers remain outside this result.

- The direct exhaustive reference covered **408,960 routes × 7 nominal periods = 2,862,720 route/period trials**. Both it and the selected constraint solver returned complete empty solution sets.
- A fresh corrected blind benchmark completed all 256 cases. All 128 in-family planted solutions were included; 83/84 ordinary-pattern positives and 28/28 literal-pattern positives were uniquely recovered. Uniform controls produced 0/56 fits.
- Selected shared-constraint solver S was **17.33× faster** than the fair complete-route baseline on fully inclusive CPU (paired-bootstrap 95% interval 17.13–17.52×). It did not materially outperform simpler prefix propagation P. Learned-conflict method L failed its separate benefit gate, so no learned-algorithm breakthrough is claimed.
- The original benchmark's resource-monitor defect is retained and disclosed. Numerical results alone did not authorize a target run. A resource-only harness repair and fresh independent holdout retained the same algorithms, selected method, model and gates. The corrected run and independent audit passed before the target stage.
- Total charged study compute, including original run, correction and audits, was about **1,490 CPU seconds (24.8 minutes)**.

Read the [corrected benchmark report](BENCHMARK-REPORT.md), [target report](TARGET-REPORT.md), [corrected benchmark audit](BENCHMARK-AUDIT.md), and [target audit](TARGET-AUDIT.md). The original limited-run results, corrected run, all source code and full audits are preserved in the ZIP.

## Reproducible archive

[Download the original study archive](candidate-first-056-20261031.zip). It contains the implementation, frozen protocols, fixtures, full recorded results, resource receipts and independent audits. The ZIP is byte-for-byte identical to the delivered archive. Extract it into a fresh directory, preserving its sibling directories; do not overlay an existing research workspace. This publication did not rerun cryptanalysis or change the live Site.

The original files retain historical labels such as “private”, “not published”, or “target not yet run” at the time each file was written. Those labels are historical, not the current publication status. The result and scope below describe the completed study. Nothing here constitutes a recovered K4 plaintext or encryption method.

SHA-256: `1a0108413a4ca8dee33197f5add25bedd9a3a5ca85a089a022fe8c2804e210ec`. [`SHA256SUMS`](SHA256SUMS) covers this directory's publication files.

`ARCHIVE-CONTENTS.json` records every payload hash; `OMISSIONS.json` identifies three exact duplicate files reconstructed from included authoritative copies. Both benchmark runs, freezes, target outputs and independent audits remain available, including superseded records. Absolute paths in historical code and records describe the original execution layout, not portable setup instructions.

## Publication provenance

Published with explicit owner authorization on 31 October 2026. The readable report/audit copies below are unchanged from the archive; any relative paths inside those historical documents refer to the extracted archive layout. Use the archive for complete source and linked artifacts.
