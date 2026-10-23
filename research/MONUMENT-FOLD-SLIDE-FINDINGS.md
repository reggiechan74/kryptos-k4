# Fold and slide: the pole-column registration

The user’s MYVGT / AABCD observation is reproduced exactly by the existing rendered transcript: **column 2**, counting from the readable edge of each separately viewed half. No row shift is needed. The tableau sequence includes its header A followed by row keys A, B, C and D. The cipher’s first-row E extends one cell farther than this first complete vertical column.

This is a flat transcript experiment, not a measured physical fold. K4 remains unsolved. At full overlap there are **35 identical A–Z pairs among 856 comparable letter pairs**. Moving the folded tableau one column in the positive direction gives 31 among 832. The complete scan has no unusual excess under either conditional null below.

## What was frozen and compared

[The protocol](MONUMENT-SLIDE-OVERLAY-SPEC.md) and [registration amendment](MONUMENT-SLIDE-REGISTRATION-AMENDMENT.md) precede scoring. The initial tableau view mirrors both cell order and glyph handedness; folding applies a second reflection, leaving **same-facing glyphs**. Positive displacement moves the folded tableau toward increasing cipher-column coordinates. Both directions, every integer displacement −33 through +33, were retained without wrapping.

The primary OBSERVED_RENDER33 registration follows the existing Site source at d4155931cd760d4222c9f66916551110eb40053b. DUNIN_HEADER33 preserves the two literal leading header blanks in the public transcript as a declared sensitivity case. All other rows agree. This makes 134 frames, including four empty endpoint frames; the 130 frames with geometric overlap form the scanned family. A 33-cell box and integer centering are modeling conventions, not surveyed copper dimensions. Ragged rows, the extra tableau L, four cipher question marks and header blanks are preserved.

The observed five cipher letters remain fixed in the null controls. There is no alignment search, row adjustment, new extracted alphabet or English-word selection. The earlier static-fold specification was superseded before scoring; its other self-fold axes were not evaluated. Chronology: 0079ed2 (static proposal), b52c288 (progressive double reflection), 0873313 (observed registration), f21e76a (implementation and controls before scoring). Exact run start/end timestamps were not recorded; this work is dated 2026-10-23 UTC. These commit identifiers describe version order, not experiment times.

## Labels and light are different observations

A label match requires identical A–Z letters. Question marks and blanks are never wildcards. The optical surrogate uses the existing modeled 5×7 bridged square-aperture font, with flat parallel sheets, equal scale and baseline, and normal rays. Any nonempty pixel intersection transmits in this surrogate; full coincidence requires equal nonempty masks. Blank/padding cells are solid; outside cells are excluded from the two-layer overlap denominator.

The five supplied pairs M/A, Y/A, V/B, G/C, T/D have zero label matches but respectively **12, 2, 7, 13 and 5 common pixels**. Different letters can transmit through common openings. A real aperture contour, pitch, perspective, sheet thickness, curvature, separation and light direction could change these values. Neither the transcript nor the [geometry audit](../docs/scott-sun-geometry-audit-2026-10-22.md) supplies that calibration.

## The letters that match at the first displacements

Readout is cipher row-major order. These are literal ciphertext/tableau coincidences, not a plaintext extraction. Source coordinates for every pair appear in the [first-shift match tables](FOLD-SLIDE-MATCHES-020.md) and the [complete machine-readable position table](../results/FOLD-SLIDE-020-matches.csv).

| Displacement | Identical labels / eligible pairs | Retained letters, row-major |
| --- | --- | --- |
| +0 | 35/856 | `QEMEWYEUGNXPDPTBDHSNTEHOATNTSSDSSFC` |
| +1 | 31/832 | `QFMXRJJLEVFMPNOIPLWEGEETAHMUXKU` |
| +2 | 18/804 | `JCAQELZEGNBEAELEOF` |
| -1 | 30/840 | `PVCKDWADPUVDYHUORIRDTATRPKQSLY` |
| -2 | 31/812 | `BRDTRSDHUDFDFEVGNPEIMEMWFLQKJWA` |

## Every primary displacement

L is identical labels / comparable A–Z pairs. A is nonempty common-aperture pairs / geometrically overlapping cells. The zero frame is shared, not two independent trials. Counts at ±33 are zero with no overlap; ratios there are undefined.

| Column displacement d | +d: L | −d: L | +d: A | −d: A |
| --- | --- | --- | --- | --- |
| 0 | 35/856 | 35/856 | 860/924 | 860/924 |
| 1 | 31/832 | 30/840 | 836/896 | 844/896 |
| 2 | 18/804 | 31/812 | 808/868 | 816/868 |
| 3 | 22/776 | 27/784 | 780/840 | 788/840 |
| 4 | 26/748 | 27/756 | 752/812 | 760/812 |
| 5 | 21/720 | 28/729 | 724/784 | 732/784 |
| 6 | 31/692 | 27/701 | 696/756 | 704/756 |
| 7 | 24/665 | 16/673 | 668/728 | 676/728 |
| 8 | 29/638 | 30/645 | 640/700 | 648/700 |
| 9 | 34/611 | 28/617 | 612/672 | 620/672 |
| 10 | 26/583 | 23/589 | 584/644 | 592/644 |
| 11 | 27/555 | 17/561 | 556/616 | 564/616 |
| 12 | 29/527 | 28/533 | 528/588 | 536/588 |
| 13 | 21/499 | 28/505 | 500/560 | 508/560 |
| 14 | 14/471 | 19/477 | 472/532 | 480/532 |
| 15 | 11/443 | 18/449 | 444/504 | 452/504 |
| 16 | 11/415 | 13/421 | 416/476 | 424/476 |
| 17 | 19/387 | 15/393 | 388/448 | 396/448 |
| 18 | 12/359 | 19/365 | 360/420 | 368/420 |
| 19 | 18/331 | 16/337 | 332/392 | 340/392 |
| 20 | 12/303 | 15/309 | 304/364 | 312/364 |
| 21 | 6/275 | 7/281 | 276/336 | 284/336 |
| 22 | 9/247 | 8/253 | 248/308 | 256/308 |
| 23 | 4/219 | 3/226 | 220/280 | 228/280 |
| 24 | 11/191 | 3/199 | 192/252 | 200/252 |
| 25 | 11/163 | 6/172 | 164/224 | 172/224 |
| 26 | 3/135 | 3/144 | 136/196 | 144/196 |
| 27 | 1/108 | 1/116 | 108/168 | 116/168 |
| 28 | 4/80 | 4/88 | 80/140 | 88/140 |
| 29 | 2/52 | 1/60 | 52/112 | 60/112 |
| 30 | 1/24 | 1/32 | 24/84 | 32/84 |
| 31 | 0/2 | 0/6 | 2/56 | 6/56 |
| 32 | 0/0 | 0/0 | 0/28 | 0/28 |
| 33 | 0/0 | 0/0 | 0/0 | 0/0 |

[All 134 frames, both registrations, areas, expectations and adjusted p-values](../results/FOLD-SLIDE-020-frames.csv) and [every matched position](../results/FOLD-SLIDE-020-matches.csv) preserve the complete sequence. The [full exact result](../results/FOLD-SLIDE-020-actual.json) also retains intersection masks and K4-relative coordinates. The four K4 ciphertext coincidences at zero displacement are positions 14, 44, 72 and 95 (S, S, F, C). They are ciphertext-glyph coincidences, not confirmed plaintext or a discovered message.

[Open the offline slider](figures/fold-slide-020.html) after downloading it with GitHub’s Raw/Download button and opening the saved HTML file locally; it embeds its data and needs no server or network, or inspect the [all-shift plot](figures/fold-slide-counts-020.svg). These are research artifacts; the live Site is unchanged. Independent JavaScript recomputes all 134 frames using cell-forward traversal and pixel strings. A separate offline check validates the slider’s calculations and controls; it is not a claim of native-browser visual inspection.

## Controls account for scanning shifts

Each of two fixed-seed schemes generates 1,999 complete surrogate inscriptions, retains the entire tableau, row letter histograms, punctuation/padding and the five supplied cipher anchor letters, and repeats the complete 130-active-frame selection. Shuffle permutes each row’s movable letters. Rotation cyclically rotates its movable-letter sequence; it does not preserve adjacency across the fixed anchors.

Exact expectations use each row’s movable-letter frequencies plus fixed-cell contributions. The fixed statistic is (observed − expectation) / sqrt(max(expectation, 1)); it is not a normal-distribution z-test. Each surrogate supplies the maximum over both registrations and all shifts, separately for labels and area. Plus-one Monte Carlo p is (exceedances+1)/2000. A conservative factor four accounts for the two endpoints and two reported null schemes.

| Null scheme | Endpoint | Exceedances / 1,999 | Family-max p | Four-report adjusted p |
| --- | --- | --- | --- | --- |
| Row shuffle | Labels | 925 | 0.4630 | 1 |
| Row shuffle | Common area | 1,126 | 0.5635 | 1 |
| Movable-sequence rotation | Labels | 921 | 0.4610 | 1 |
| Movable-sequence rotation | Common area | 907 | 0.4540 | 1 |

Receipts: [shuffle](../results/FOLD-SLIDE-020-null-shuffle.json), [rotation](../results/FOLD-SLIDE-020-null-rotation.json). There is no evidence of unusual excess under these conditional models. These p-values are not the probability that Sanborn used a fold, a probability of correct plaintext, or calibration of every earlier hypothesis. No attractive partial string was selected for a subsequent search.

## Reproduce and limits

Run `python3 experiments/monument_slide.py --actual --output /tmp/fold-actual.json`, and repeat with `--null shuffle` or `--null rotation` instead of `--actual`. `node experiments/monument_slide_oracle.mjs` independently checks counts; `node experiments/monument_slide_visual_check.mjs` checks the offline artifact. [Unit tests](../tests/test_monument_slide.py) cover planted overlaps, boundaries, exact tiny null expectations, mutations and independent pixels. No source photos or private review images are committed.

This completes only the declared transcript registration and integer-pitch surrogate. It does not reject physical optical mechanisms, fractional shifts, other independently justified registrations, or stateful use of an overlay. Actual aperture outlines and measured registration remain missing inputs. Those possibilities stay evidence-blocked rather than being repaired after these results.
