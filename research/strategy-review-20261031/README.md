# Kryptos K4 strategy review archive

**[Read the research study](REPORT.md)** or download the [original editable Word report](Kryptos_K4_Research_Comparison_2026-10-31.docx).

The completed study, **New cryptanalysis strategies for Kryptos K4**, compares recent literature and mature methods with the project’s inspected implementation record. Its first recommendation is a calibrated forced-key-fragment feasibility study before any expensive joint plaintext and running-key decoder. This is a research comparison, not a K4 solution or a new experiment result.

## Provenance and scope

- Report date and research cutoff: **31 October 2026**.
- Research snapshot: [`de3654a098162185d47b7c14ee1eef1631ab1804`](https://github.com/reggiechan74/kryptos-k4/commit/de3654a098162185d47b7c14ee1eef1631ab1804). All 12 repository references remain pinned to this snapshot; the report also cites 19 primary literature or context sources.
- Archive publication base: [`3c00a5246705ae9bddf81e46e570ea505cc0a2e4`](https://github.com/reggiechan74/kryptos-k4/commit/3c00a5246705ae9bddf81e46e570ea505cc0a2e4), which separately archived the Site source.
- The Word file is preserved byte for byte from the completed 12-page report. The Markdown rendition retains every substantive paragraph, all three tables, references, qualifications, and proposed decision gates. It changes only presentation, omits page breaks and running headers/footers, and adds a clearly marked publication note.
- The report was prepared privately, then authorized for publication in this public repository on 31 October 2026. Its historical “private” statement is retained rather than silently rewriting the original. Publication does not turn the report’s proposed experiments into completed runs.
- The inspected repository results were **not freshly reproduced** for this review. This archival change runs no cryptanalysis, makes no paid checker submission, and does not modify or deploy the live Site.
- This archive contains the finished study, not internal working notes, raw fetched articles, or third-party source extracts. The report’s limited source summaries and links are preserved.

## Integrity

The archived DOCX matches the completed report’s recorded SHA-256:

```text
47ca945b339c99c788e68e280c012ec7390b4c391b3433585141eed729eec977
```

Its 218 nonempty body paragraphs and table cells were compared exactly against the final structured report content. All 31 unique source URLs and 90 hyperlink instances were retained in the source document; all cited destinations are preserved in the Markdown rendition. The 12 rendered pages were inspected, with no content edits made during archiving. There are no tracked changes or comments in the DOCX.

The DOCX’s inherited package metadata contains default 2013 creation/modification timestamps. Those fields are not research or execution dates; use the report’s explicit date and the pinned research snapshot above. They are left unchanged to preserve the original bytes.

[`SHA256SUMS`](SHA256SUMS) covers the original report, Markdown rendition, and this provenance file. To verify locally, run from this directory:

```sh
sha256sum -c SHA256SUMS
```
