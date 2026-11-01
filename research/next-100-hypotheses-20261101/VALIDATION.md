# Validation record

## What was and was not checked

This is a **documentation/static-schema and mathematical desk-review** record. No K4 search, cipher execution, external program execution, synthetic cipher experiment or performance benchmark was run to create this annex. Proposed controls are future tests, never retroactively marked passed.

The final catalog validator checks exactly100 records, unique stable IDs and titles, the declared mechanism/method totals, a mechanism plus bounded test and identifiability field in each record, and deterministic review ranks. It parses and renders JSON; it does not validate the truth of a cipher or benchmark claim. Missing source-level novelty proof remains missing.

An independent contributor reviewed adaptive, stream, codec and method drafts. This caught:
- a removed-record reference in the majority-clock generator (replaced by explicit recurrences and seeds);
- a synthetic observation-contract contradiction (M11 now fixes the complete ciphertext and edits the model);
- 73 undisclosed positions versus 67 in a narrower residual contract (now explicit);
- an analytically dead Ducci proposal (removed, proof retained);
- unfrozen algorithm conventions and several substantive alias risks (retained as blockers).

The guarded continued-fraction involution and CRT representation inverse were checked on paper, not by code. No source/inverse review is promoted to empirical validation. Structural records retain their own proof obligations; the cross-family audit is not a theorem of pairwise distinctness for all 100.

## Baseline preservation

Only new proposal artifacts were written; baseline files were read and left unchanged. SHA256 of the materialized baseline text:

| File | SHA256 |
|---|---|
| AGENTS.md | `6a7f0a5acecb6ee7c4c441ca0216d4f289d8499ef399849ebf7c7ca225b42180` |
| research/HYPOTHESES.md | `de8dd604f30a13c6b9d5665a14e817a13c343a0934151ba597875c915e6e131b` |
| research/EXTERNAL-PRIOR-ART.md | `2329d93e1f17f0210a6b065352d3be746014fa8498bacfc41f3650ff8db55830` |
| research/EXPERIMENTS.md | `06584607251accb649cd762646e58fa95b242cf2ed4fcada1d2be33e3221cacd` |

These are hashes of the local UTF-8 file content, not Git object IDs. Source commit pins and external Git blob IDs are recorded separately in SEARCH-AND-PRIOR-ART.md.

Final static validation passed on 2026-11-01: 100 records, 78 mechanisms, 22 methods, unique IDs/titles/working references, all ranks 1–100, valid local document anchors and required scientific fields. All referenced H/EXT identifiers resolve in the 69-family/51-record baseline. Six records are explicitly specification-blocked: S12/S15/S16/S33/C05/B15. Run `python validate_catalog.py` to repeat metadata validation; this is not a cryptanalysis test.
