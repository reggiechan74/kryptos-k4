# Manual fold overlay — live Site version 15 source handoff

Source commit: `086ace2bfb2ca6e23ddddf76fe5f37c51dd75aea`, based on version 14 commit `d4155931cd760d4222c9f66916551110eb40053b`.

The parent relayed the Site owner’s successful native publication result: **version 15 is live**, public access revision 2 unchanged, at the [Kryptos Light Laboratory](https://kryptos-light-laboratory-rc2026.milky-lion-6014.chatgpt.site). Choose its manual fold overlay mode. This archive operation did not deploy the Site or independently inspect its live rendering. Exact publication time is not supplied.

## Archive and provenance

[The exact source patch](site-source.patch) is 250,118 bytes, SHA-256 `48c7192fddf2414d1993b7edcf58852b74910e8d450248a8c440920ec8abafe1`. It was inspected and copied from the owner’s explicit local handoff path. Read-only Git verification against the separate Site checkout confirms byte-for-byte equality with the entire base-to-source diff, all 25 paths, and all 18 new-file bodies. No patch was applied to this repository’s root and no child-checkout files were modified.

This is a source delta, not a complete Site snapshot. [Original handoff](ORIGINAL-HANDOFF.md), [copy manifest](MANIFEST.json), [new modules](source/README.md), [unaltered original tests](original-tests/README.md), [QA page](qa/README.md) and [integration receipt](../../../results/SITE-MANUAL-FOLD-V15-SOURCE-HANDOFF.json) preserve the distinction. The full app/HTML/CSS/release-manifest changes and copied protocol documents remain inside the exact patch; a nonexistent root runtime was not fabricated.

## Behavior and tested scope

The source adds integer column offsets −33…+33 and row offsets −28…+28, one-cell buttons, anchored reset, cell inspection, exact-label and approximate aperture views, source coordinates and JSON export. Initial view reflection and fold reflection cancel; glyphs face the same way. No wrapping is introduced. Blank/padding copper, punctuation, outside cells, changing overlap denominators and the MYVGT/AABCD anchor remain distinct.

The glyphs are the existing modeled 5×7 square-aperture font, not measured copper outlines. Exact label matches and shared openings remain separate. Nonzero row offsets are manual exploration: they have no inherited p-value from the prior column-only `dy = 0` scan. No systematic row scan or new cipher experiment was run for this integration.

## Validation attribution and limits

The Site owner reports **87 Site tests passed**, including all 134 canonical column-frame computations and row-control checks. Those are attributed results, not a locally repeated full Site suite. The owner’s actual rendered-browser QA was blocked by the locked Mac; the supplied 390 px / 1280 px QA page is preserved but is not represented as having run. No independent touch-device or keyboard-rendering claim is made here.

Local verification is **static**: patch paths, Git blob identities, candidate/dist equality, source-commit bytes, exact input and glyph equality, and equality of the 134 embedded oracle records with repository research results. It does not execute the handed-off JavaScript or prove rendered UI behavior. Reproduce these checks with `python3 experiments/verify_manual_overlay_handoff.py` from the research repository root; regression tests exercise archive integrity and malformed-path rejection.

[Research findings](../../../research/MONUMENT-FOLD-SLIDE-FINDINGS.md) and the [offline research HTML](../../../research/figures/fold-slide-020.html) remain separate from the live Site implementation.

## Later research scope update

The unchanged version-15 source is pinned to the earlier column-only study. [The later systematic two-dimensional item-1 study](../../../research/FOLD-SLIDE-2D-FINDINGS.md) now supplies separate whole-search controls for its own fixed integer domain. This research update does not rewrite the archived UI help, transfer old p-values, or deploy a new Site version.
