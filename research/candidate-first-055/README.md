# Study 055: forced-fragment English-key screen

**None of the 12 K4 fragment pairs passed the fixed English-language screen.** All 17 calibration admission checks passed first. This supports stopping the direct aligned English-running-key decoder under this screen; it does **not** prove that every English running key is impossible.

- Unchanged order-4 language model from study 053; two independently scored clue-derived fragments of 13 and 11 letters, with no fabricated context across the missing 29-letter bridge.
- Fixed threshold: **−4.385648037504633 bits/letter**. Best target score: **−7.992896749427596**, a margin of **−3.6072487119229635**. No target tableau survived (0/12).
- Held-out true-key retention: archaic 96/100, fiction 98/100, nonfiction 100/100. Uniform and letter-scrambled controls: 0/200 accepted each.
- Local English scores are not semantic coherence: word-order-scrambled and unrelated English pairs often survive. Source-group clustering, authentic-subset overlap and incomplete scored-token coverage remain limitations.
- One primary target computation and one independent repeat agree. No joint decoder or broader search followed.

Read the [full historical report](REPORT.md), [calibration audit](CALIBRATION-AUDIT.md), and [target audit](TARGET-AUDIT.md).

## Reproducible archive

[Download the original study archive](candidate-first-055-20261031.zip). It contains the implementation, frozen protocols, fixtures, full recorded results, resource receipts and independent audits. The ZIP is byte-for-byte identical to the delivered archive. Extract it into a fresh directory, preserving its sibling directories; do not overlay an existing research workspace. This publication did not rerun cryptanalysis or change the live Site.

The original files retain historical labels such as “private”, “not published”, or “target not yet run” at the time each file was written. Those labels are historical, not the current publication status. The result and scope below describe the completed study. Nothing here constitutes a recovered K4 plaintext or encryption method.

SHA-256: `b80fe460bcf4fcba5094b91527ac3914b6e234d5e34d946ffd46aad939d06e65`. [`SHA256SUMS`](SHA256SUMS) covers this directory's publication files.

The package deliberately omits bulky normalized corpora and offset arrays, with exact inventories and reconstruction instructions in `candidate-first-055/ARCHIVE_README.md`. It is dependency-backed, not a self-contained copy of every raw corpus. The unchanged small model/count dependencies are included. For a checksum-only check after extraction, run `python candidate-first-055/verify_package.py`; it does not score K4.

## Publication provenance

Published with explicit owner authorization on 31 October 2026. The readable report/audit copies below are unchanged from the archive; any relative paths inside those historical documents refer to the extracted archive layout. Use the archive for complete source and linked artifacts.
