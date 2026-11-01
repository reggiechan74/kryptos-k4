# P1 independent static provenance review

Reviewed 1 November 2026 UTC. Scope: metadata, attribution and canonical-byte checks for the 16-artifact P1 evidence packet. This is not a scientific experiment or independent historical authentication of all linked sources. No cipher implementation, target replay, clue-to-operation coding, recipe construction, new source discovery or repository modification was performed.

## Checks and result

1. Independently fetched `data/controls.json` and `research/puzzle-instruction-discovery-v1/README.md` from GitHub at exact commit `e2f4a1e24acdc8bcd319f01b68fd51afbc924ce3`. Returned Git blob IDs match independently recomputed local Git hashes:
   - Fixture: `febb203e66482da1ccd0aae2ed3a6ec79764cb71`; SHA-256 `54f19ff0ecd1e058a6b84c6ddb4ad75a297e4181edb45803647ed208d8fc011b`.
   - Plan: `93c1ec88e9be2ac09297003db675debcf1591730`; SHA-256 `fc2d38f08aad29ff115e33057d8ba0113fe2333e51ba093327d3bc789d06ad88`.
   These match CANONICAL-PINS.json. Character count versus UTF-8 byte count differs for the plan because of non-ASCII punctuation; recorded byte counts are consistent.
2. Independently rehashed the three nonpublic extracted-Markdown snapshots and checked their byte counts. All agree with SOURCE-RECEIPTS.json. These remain extraction pins, not raw HTTP-object authentication.
3. Compared all four historical download hashes and byte counts in the inventory against the existing retrieval-hashes record. All agree. Historical underlying downloaded bytes were not present, so no independent content equality with today's pages is claimed.
4. Checked the employee-letter, Smithsonian oral-history and Kalinovska-excerpt paraphrases against the available private snapshots. They support the limited admitted statements. The Smithsonian matrix-code remark explicitly concerns previously solved sections. The 2009/2020 transcript distinction is preserved.
5. Cross-checked the two unavailable facsimiles' dates and attribution against the cited earlier evidence review, and worksheet image limitations against the existing worksheet-provenance report. Current access failures are not converted into fresh authentication. Third-party facsimiles and their reproductions are not independent testimonies.
6. Confirmed all 16 IDs occur once in source receipts and inventory; 14 items have a current local or remote text reading, two retain prior-review-only status. Public package contains paraphrases, provenance metadata and exclusions, not wholesale third-party source texts.
7. Reviewed the 1991 and 2005 statement summaries against the retained source-reading context; no new rereading of original recordings is claimed. Solver interpretations are segregated from participant assertions. No inferred physical geometry, instruction mapping or novel cipher conclusion appears.

## Corrections verified before freeze

- Corrected during review: the employee-letter transcription asserts a fiction-writer collaboration; it does not explicitly call that merely an anticipated plan. The final paraphrase now preserves the assertion and its conflict with later recollection.
- Verified closure: receipt entries now use `inventory_section_id` values P1-S01 through P1-S16 rather than falsely implying resolvable short fragment anchors. All 16 identifiers match their inventory section identifiers.
- Verified closure: inventory and receipts both give the approximate source-read window 14:12–14:18 UTC, including the later NSA content reread.

## Disposition and limits

**Static provenance review passes; suitable for final byte-manifest verification and publication.** Missing current raw-source pins, unavailable facsimiles, historical uncertainties and nonblind exposure remain explicit limitations, not claimed resolutions. A packet hash authenticates the published packet version, not every linked live webpage. This review neither authorizes P2 nor establishes an encryption instruction. Future P2 reviewers must receive identical frozen packet bytes and disclose their own prior exposure independently.
