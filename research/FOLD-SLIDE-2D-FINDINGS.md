# Item 1 — systematic row-plus-column fold/slide

**Completed: no unusual excess under either declared whole-search control.** No cipher or plaintext candidate is claimed. This is a bounded transcript-coincidence experiment, not an exclusion of every physical or cryptographic fold mechanism. Items 2–8 were not started.

The [frozen protocol](FOLD-SLIDE-2D-SPEC.md) and [machine specification](specifications/FOLD-SLIDE-2D-001.json) precede the new rankings. Inputs, glyphs and the two registrations are unchanged from the earlier column study. Specification commit `f6aafc4735b8ff9e4f7e01975a97baf9991e1583` preceded validated implementation commit `0584bbc3340ce8a50a7fed3a53feaed202420c4f`, then the original run.

## Exact scope and extraction

Both OBSERVED_RENDER33 and DUNIN_HEADER33 were compared at every integer column displacement −33…+33 and row displacement −28…+28: **7,638 frames, 7,150 with geometric overlap**. The 134 row-zero frames are prior coverage and reproduce exactly; the extension adds 7,504 raw nonzero-row frames, 7,020 active. Frames overlap, and aliases are not independent tests.

Initial tableau mirroring and seam folding cancel. The glyphs therefore face the same way. Compare C[r,c] with T[r−dy,c−dx], without wrapping; positive columns move right and positive rows move down. Ragged rows, literal header blanks, extra L, question marks and the MYVGT/AABCD anchor remain intact. No new registration, row repair, font or fractional shift was fitted.

Exact A–Z labels and approximate common apertures are separate endpoints. Blanks/padding are solid and punctuation is not a label wildcard. Geometric overlap is (33−|dx|)(28−|dy|); comparable letter pairs and pixel union have separate denominators. Four hundred eighty-eight empty frames have zero counts and undefined ratios, with no p-value. The modeled 5×7 holes assume flat coincident equal-scale sheets and normal rays; they are **not measured copper contours or calibrated light**.

Every match is read in fixed cipher row-major order. No English score, keyword test, Morse parsing, new readout route or shape recognition was applied. Full strings, source/raw/grid coordinates, stream/K4 indices and nonempty aperture masks are retained. A 1/1 coincidence on a tiny overlap is not a solution.

## Whole-search chance controls

Each of 1,999 row shuffles and 1,999 movable-sequence rotations repeats the complete two-dimensional/two-registration selector. All pixel planes are recoded jointly from each shuffled letter, preserving glyph-shape dependence rather than shuffling pixels independently. The tableau, per-row letter histograms, punctuation/padding and five originally supplied cipher anchor letters stay fixed. Rotation preserves the movable sequence’s cyclic order, not adjacency through fixed anchors.

The endpoints are label count and total common square-pixel area. Exact means are derived from row frequencies and fixed contributions, with common denominator 33,227,040. The frozen comparison statistic is (value−E)/sqrt(max(E,1)); **it is not a normal z-test**. Rankings and exceedances use exact signed-squared rational comparisons; floating values are display only. Each null supplies a family maximum. Plus-one p=(k+1)/2000; multiply by four for two endpoints and two null reports. No minimum-overlap threshold or favorable null scheme was selected after results.

| Null | Endpoint | Maxima ≥ actual / 1,999 | Whole-search plus-one p | Four-report adjusted p |
| --- | --- | --- | --- | --- |
| shuffle | label_matches | 1,494 | 0.7475 | 1 |
| shuffle | common_pixel_area | 1,299 | 0.6500 | 1 |
| rotation | label_matches | 1,526 | 0.7635 | 1 |
| rotation | common_pixel_area | 1,217 | 0.6090 | 1 |

All active-frame four-report adjusted values are 1. These controls address the frozen item-1 selector only: they are not an English null, a posterior, a correction across all earlier/future hypotheses, or evidence of Sanborn’s intent. Public clues, the manual UI and prior column results were already known; no historically untouched discovery is claimed.

## What matches at the selected extrema

The following five rows per endpoint were prescribed for display before evaluation, ordered by the frozen statistic with stable tie order. The coordinates are **column dx, row dy**. Fractions and strings remain descriptive. Both family maxima have one exact maximizing frame; all other ties remain in the full data.

### Label-count statistic

| Registration | dx | dy | Identical / comparable letters | Geometric cells | Retained row-major letters |
| --- | --- | --- | --- | --- | --- |
| OBSERVED_RENDER33 | +19 | -7 | 21/248 | 294 | `JFHLNJLNQXIQMUVOYTBAE` |
| DUNIN_HEADER33 | -9 | +23 | 11/109 | 120 | `KLMCDMRGHWX` |
| DUNIN_HEADER33 | +19 | -7 | 20/247 | 294 | `JFHLNJLNQXIQMUVOYTBE` |
| OBSERVED_RENDER33 | +27 | +24 | 4/16 | 24 | `BBYP` |
| DUNIN_HEADER33 | -28 | +24 | 4/12 | 20 | `CDTT` |

The largest label excess is **21/248** at dx=+19, dy=−7 (294 geometric cells), statistic about 3.856. Its whole-search tails are 0.7475 and 0.7635. This normalized excess is different from the maximum raw count.

### Common-aperture-area statistic

| Registration | dx | dy | Common pixels | Identical / comparable letters | Geometric cells | Retained letters |
| --- | --- | --- | --- | --- | --- | --- |
| OBSERVED_RENDER33 | +28 | +23 | 160 | 4/14 | 25 | `KRYP` |
| OBSERVED_RENDER33 | +21 | -25 | 289 | 1/30 | 36 | `Y` |
| DUNIN_HEADER33 | +28 | +23 | 143 | 4/13 | 25 | `KRYP` |
| DUNIN_HEADER33 | +29 | +26 | 41 | 1/3 | 8 | `A` |
| OBSERVED_RENDER33 | +30 | -3 | 216 | 3/21 | 75 | `DEI` |

The area-statistic maximum has only 25 geometric cells and 14 comparable letters: 160 common pixels at dx=+28, dy=+23. Its `KRYP` coincidence is not promoted as a key or message. No lexical-chance test was performed; the tableau itself supplies patterned alphabetic material. Whole-search area tails are 0.6500 and 0.6090.

The maximum raw label count is **37**, attained in three frames (not three independent discoveries):

| Frame ID (model:dy:dx) | Matches / comparable | Geometric cells | Retained letters |
| --- | --- | --- | --- |
| OBSERVED_RENDER33:6:2 | 37/632 | 682 | `UZFUFURTJFBDUAYLHATALIMTUAIAERPFDUTKD` |
| DUNIN_HEADER33:-3:-5 | 37/653 | 700 | `KRMJUHWPZFHNCVKBNQZGQUCMAWTTEAEMETEIE` |
| DUNIN_HEADER33:6:2 | 37/631 | 682 | `EKFUFURTJFBDUAYLHATALIMTUAIAERPFDUTKD` |

## Complete outputs and reproducibility

- [Every frame, both registrations, denominators, readouts and calibrated p-values](../results/FOLD-SLIDE-2D-001-frames.csv).
- [All-offset count maps](figures/fold-slide-2d-001.svg), descriptive rather than significance maps.
- [All 57,674 exact matching positions](../results/fold-slide-2d-001-runs/20261023T234752Z-ddb7425463b745a4b3d70b1b669dd641/label-matches.csv.gz).
- [All 1,506,846 nonempty surrogate intersections and exact masks](../results/fold-slide-2d-001-runs/20261023T234752Z-ddb7425463b745a4b3d70b1b669dd641/aperture-intersections.csv.gz).
- [Complete actual records](../results/fold-slide-2d-001-runs/20261023T234752Z-ddb7425463b745a4b3d70b1b669dd641/actual.json).
- [Independent forward-cell/pixel oracle records](../results/fold-slide-2d-001-runs/20261023T234752Z-ddb7425463b745a4b3d70b1b669dd641/independent.json).
- [Full shuffle calibration, maxima and per-frame tails](../results/fold-slide-2d-001-runs/20261023T234752Z-ddb7425463b745a4b3d70b1b669dd641/null-shuffle.json).
- [Full rotation calibration, maxima and per-frame tails](../results/fold-slide-2d-001-runs/20261023T234752Z-ddb7425463b745a4b3d70b1b669dd641/null-rotation.json).
- [Run summary and source hashes](../results/fold-slide-2d-001-runs/20261023T234752Z-ddb7425463b745a4b3d70b1b669dd641/summary.json).
- [Immutable timing/status/artifact manifest](../results/fold-slide-2d-001-runs/20261023T234752Z-ddb7425463b745a4b3d70b1b669dd641/manifest.json).

The compressed tables are ordinary UTF-8 CSV in deterministic gzip (mtime zero); for example, `python3 -m gzip -d -c path/to/label-matches.csv.gz`. Nothing is omitted from the position tables to make an attractive string. The native integer-polynomial method and independent cell-forward/pixel-string code agree on every field and label position across all 7,638 frames. All 134 prior row-zero count/mean checks also pass.

Pre-evaluation controls include 18 planted 5×4 offsets with whole-domain raw-label-count truth inclusion, an explicit two-way ambiguous fixture, exhaustive tiny permutation/rotation means, exact signed-ranking comparisons, no-carry/boundary/punctuation controls, lossless output replay, null structure/seed replay and a deliberately corrupted packed result. [Controls receipt](../results/FOLD-SLIDE-2D-PRE-EVALUATION-CONTROLS.json), [tests](../tests/test_monument_slide_2d.py). The standardized full selectors were checked against independent complete tiny null traversals before evaluation. A separately timestamped [post-run supplement](../results/FOLD-SLIDE-2D-CONTROL-SUPPLEMENT-001.json) additionally confirms the true offset is in the exact standardized maximum set for both endpoints in all 18 same plants; this later validation is not relabeled as pre-evaluation or added as new search coverage.

To reproduce with the current runner, use `python3.12 experiments/monument_slide_2d.py --run --execution-kind replay --spec-commit f6aafc4735b8ff9e4f7e01975a97baf9991e1583`; a new immutable replay snapshot is created. After the original run, only an explicit execution-purpose argument/default was added to the runner and summary so repetitions are not mislabeled as originals; the mathematical algorithm is unchanged. Original source bytes remain verifiable at the recorded implementation commit. `--controls` runs synthetic controls without examining new actual rankings. `export_monument_slide_2d.py` is presentation only. Do not overwrite retained receipts or confuse a replay with this original run.

## UTC timing, resources and remaining limits

Original manifest start: **2026-10-23T23:47:52.868636Z**. Final publication of staged artifacts: **2026-10-23T23:49:19.600426Z**. These are actual run boundaries, not inferred commit times.

| Job | UTC start | UTC finish | Status |
| --- | --- | --- | --- |
| synthetic-controls | 2026-10-23T23:47:52.869196Z | 2026-10-23T23:47:52.998372Z | completed |
| prepare-and-actual-all-frames | 2026-10-23T23:47:52.998752Z | 2026-10-23T23:47:56.484147Z | completed |
| independent-cell-pixel-oracle | 2026-10-23T23:47:56.635193Z | 2026-10-23T23:47:58.260573Z | completed |
| whole-search-null-shuffle | 2026-10-23T23:47:58.377924Z | 2026-10-23T23:48:38.912731Z | completed |
| whole-search-null-rotation | 2026-10-23T23:48:38.954040Z | 2026-10-23T23:49:19.557949Z | completed |

All configured job and 1 GiB memory guards passed; no stage is budget-unresolved. Peak RSS was not separately logged and no invented peak value is reported. No Site deployment, new shape/geometry tuning or subsequent numbered investigation occurred.

Physical contours, measured registration, curvature, separation and illumination remain uncalibrated. This result tests a coincidence-excess prediction under two transcript registrations; it does not define or reject every possible encryption/extraction using a folded monument. K4 remains unsolved. The separate current SIGABA scope summary now correctly reports COMPACT-018’s 12/14 synthetic controllers, preserving earlier zero-controller stages as historical observations and making no K4 joint-search claim.
