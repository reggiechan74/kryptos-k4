# Confirmed K4 clue display — Site version 13 source handoff

This preserves the source delta for the already published Kryptos Light
Laboratory version 13. Supplied source commit:
`0ab12260bba31ed3bd03e2a78213482ea6fd72dd`; supplied baseline:
`5b266eb0fc6744c5eda45e30ad089731be97cb35` (version 12).

The research checkout has no `candidate/` or `dist/` Site runtime snapshot.
Accordingly this documentation archive preserves the exact patch and its new
clue component, rather than applying unrelated root paths or claiming a complete
Site checkout. No child checkout was edited, Site redeployed, access changed,
main branch changed, or optical/cryptanalytic behavior added.

- `kryptos-confirmed-k4-clues.patch` is the original 99,546-byte delta across
  twelve Site files, SHA-256
  `875e1498327b30b55134f3235ba310120960af6d4befb98e3a9f07f1930449a3`.
- `source/k4-clues.mjs` is the byte-exact new module; candidate and deployed
  postimages match. Its SHA-256 matches the supplied release-manifest entry:
  `d8af9b8a4d6fa13300e2642bf976d75a6549ee351879ef3df39313e78613768d`.
- `ORIGINAL-HANDOFF.md` is preserved unchanged from the patch.
- `review.test.mjs` independently validates this extracted component against the
  canonical research fixture. It does not simulate missing application files.

The mask contains 21 unknown middle dots, EASTNORTHEAST, 29 unknown dots,
BERLINCLOCK and 23 unknown dots: 97 positions, 24 confirmed letters and 73 unknowns.
First O is position 1. The shared 31-column grid retains 27 initial padding cells;
each confirmed-only cell is directly below its cipher cell. No experimental IPA
or fitted plaintext enters this display.

Run `node --test docs/site-source/confirmed-clues-v13/review.test.mjs` from the
research root. Four isolated tests pass: exact confirmed mask, all logical grid
coordinates, accessible paired DOM cells/selection, and invalid-anchor rejection.
These are source/component tests, not an independent browser rendering replay.

The Site child reports 76 full Site tests passing and rendered checks at 390 px
and 1280 px with zero alignment error and no overflow, preserving K1–K3, optics
and frozen routes. Those are attributed handoff results. Repeating that full
suite requires the separate Site baseline, which is not present here. The final
screenshot attempt lost browser access after the checks; no screenshot deliverable
was requested. Source provenance and verification are in
[the receipt](../../../results/SITE-CONFIRMED-CLUES-SOURCE-HANDOFF.json).
