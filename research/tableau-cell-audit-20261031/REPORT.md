# Handwritten tableau: independent 810-cell evidence audit

## Decision

**No reproducible high-confidence noncyclic entry was established. Close this avenue as providing no supported new cipher mechanism.** Four cells remain unresolved; therefore this is **not** a proof that every literal inscription is cyclic. Unclear pixels must not become candidate key bits, alternate alphabets or repair parameters. No K4 decryption or cipher sweep was performed.

## Results

Two independent blind visual readers each recorded all **810 displayed cells: 27 rows × 30 columns**. Both original JSON/CSV files were frozen and SHA-256 verified before comparison with each other or with the expected table.

- **806 agreed letters**, all consistent with the expected table: **774** independently high-confidence, **32** with at least one retained visual uncertainty.
- **1 agreed unreadable cell**, at (27,2), is counted separately from agreed letters.
- **3 literal disagreements**, all left unresolved below.
- **0 confirmed noncyclic entries**; **0 proven plain examiner errors** in the two frozen transcriptions. Disagreement alone does not establish reader error.

| Cell | Examiner A | Examiner B | Expected | Pixel reconciliation |
|---|---|---|---|---|
| (17,21) | Q; alternatives D/R | R; alternative D | D | Closed loop and lower-right tail visible in both photographs. D/Q/R remains ambiguous. |
| (18,20) | D; alternative P | P; alternative D | D | Narrow loop with descending left stroke; D/P unresolved even in close-up. |
| (27,2) | Unreadable; B/R | Unreadable; B/R | B | Finger obscures lower portion; close-up does not cover footer. |
| (27,4) | Unreadable; B/D | B; alternative D | D | Overdrawn loop form; B/D unresolved. |

The remaining 32 tentative agreements retain both readers' alternatives and notes. Mark/stroke ambiguities at (13,14) and (14,13) are explicitly categorized separately from a confirmed letter anomaly. The cellwise files distinguish clear matches, handwriting ambiguities, stroke/mark artifacts and occlusion. No unresolved cell was filled from a cyclic template. No visible anomaly was promoted to an intended substitution.

**Row bijectivity:** no reproducible noncyclic letter has been established to justify a modified-row analysis. Rows 17 and 18 contain unresolved D-like glyphs, so their literal bijectivity cannot be certified from these images. We do not manufacture an invertible repair.

## Method and coordinate convention

Coordinates are 1-based from the upper-left K=(1,1); footer is row 27. Both readers inspected original pixels and independent non-destructive enlarged/geometrically rectified crops. Neither received the expected alphabet, a generated cyclic template, other examiner output or an external transcription. No OCR, external OCR API or third-party research code was executed. Only handwritten case was normalized to uppercase. Independence is procedural, not a claim of statistically independent model errors.

After both freezes, the comparator used `KRYPTOSABCDEFGHIJLMNQUVWXZ[(row+column-2) mod 26]` for rows 1–26 and `ABCDEFGHIJKLMNOPQRSTUVWXYZ[(column-1) mod 26]` for the footer, including four repeated displayed columns. These expected entries appear only as comparison fields, not replacements for observations.

The separate close-up was registered using the visibly circled H at **(21,21)** and surrounding strokes/grid; it covers parts of rows 15–24, columns 18–25. It improves visibility of the two middle-table disagreements but does not settle their letter identities. The earlier published H coordinate (20,22) is incorrect for this convention. Its correction is a coordinate correction, not a new key. Nothing about circles establishes K4 relevance.

## Sources, provenance and prior work

- [Full photograph, IMG_1223](https://www.kryptosbot.com/static/archive/IMG_1223.jpg)
- [Separate close-up, IMG_1224](https://www.kryptosbot.com/static/archive/IMG_1224.jpg)
- [Photographer-hosted archive gallery](https://www.kryptosbot.com/archive/)
- [Smithsonian collection record](https://collections.si.edu/search/detail/edanmdm%3AAAADCD_coll_22298)

The gallery attributes the photographed materials to Jim Sanborn's papers. This is photographer-hosted provenance, **not Smithsonian item-level authentication**: no matching box/folder/item identifier or institutional image record has been established. Original photographs and derived image crops are not redistributed in this package.

**This is not the first claimed blind examination.** [Colin Patrick's pinned archive doctrine, item 11](https://github.com/jcolinpatrick/kryptos/blob/6dfc420d65432988be524e0992c1735a4c466b1e/docs/archive_aaa_doctrine.md) already reports a June 11 SPEC-E extraction by two independent examiners, a 27×30 grid and cyclic structure. It retracts an earlier extra-L interpretation. Its cited `analysis_runs/spec_e_circled_tableau_2026_06_11/` packet was not retrievable at that pinned commit; targeted web searches located the summary but not a complete literal cell transcript. Accordingly no cell-by-cell comparison to that prior packet was possible, and no novelty/priority claim is made. Sculpture inscriptions and K1/K2 encoding worksheets are different artifacts, not substitutes for this photograph. Search scope and limitation are recorded in `prior-work-search.json`.

## Reproducibility and next decision

`examiner-a.json/.csv` and `examiner-b.json/.csv` are unchanged independent originals. `comparison-start.json` records their verified hashes and the post-freeze comparison time. `cellwise-audit.json/.csv` preserves every original assessment beside expected entry, reconciliation and classification. `methodology.json` records original photograph hashes; `SHA256SUMS` covers public artifacts. No photograph is bundled.

The evidence gap could be reduced by an unobscured higher-resolution photograph or item-level archive access, not by enumerating speculative letter choices. **No new cipher experiment is licensed by this audit.** Reopen only on better source evidence or a concrete separately evidenced mechanism.
