# Native photograph correspondence attempt: no admissible point pairs

Local follow-through on family 3, 24 October 2026. **The specified native-image inspection has now been attempted. It did not establish any certified aperture-to-ground material-point pair, so no real-data geometric fit is performed.** This is not an exclusion of projection, a claim all possible annotation methods failed, or a K4 test.

[Pre-inspection protocol](PHOTO-NATIVE-047-SPEC.md), [native crops and provenance](evidence/2026-10-24-native-loc/README.md), [annotations and UTC protocol/inspection times](evidence/2026-10-24-native-loc/annotations.json), [independent crop verifier](../experiments/photo_native_047.py), [all exact crop checks](../results/PHOTO-NATIVE-047-CROP-CHECK.json). The TIFF matched the expected SHA-256 before inspection. It is the same known LOC exposure, not a new independent view.

## Actual pixel work

I inspected the full-image overview, the fixed native `[1400,2800,2200,3600)` ground ROI, two screen crops, two ground-context crops and four 400 × 400 quadrants. This exhausts the declared single-exposure/eight-additional-crop inspection budget. The unknown transform of the older 2000 × 1500 PNG was bypassed, not guessed: all new crops were cut directly from the native source conversion, and an independent standard-library PNG scanline decoder verifies every crop against that conversion byte-for-byte in decoded RGB.

The upper-left ground quadrant contains separated bright bars, wedges and angular/open forms. Ten rough observation boxes, sorted by their top coordinate and left coordinate on ties, are recorded as G01–G10. They are not an exhaustive component census. Some tiny marks have no distinctive topology; some larger angular forms have recognizable stroke structure but no unique transmitting row/column. The left source crop shows repeated aperture forms on successive rows; the screen turns rapidly toward edge-on, and some contours are partly hidden or seen with other bright surfaces behind them. The back-screen crop supplies additional visible glyphs but no continuous physical trace from a particular aperture boundary point to a receiver point. A repeated glyph's identity does not select its physical occurrence or a corresponding material corner.

The top/right and lower/right ground quadrants have broader, partly merged and texture-modulated marks. A brightness boundary there is not automatically the image of one aperture edge. The lower-left quadrant includes a substantial dark support/occlusion and sharp V-like open forms; neither establishes the missing aperture identity. Paving joints and the support are context/occluders, not assumed transmitting points. These are observations of the inspected pixels; no Sun size, height, penumbra width, surface normal, north bearing or exposure time was inferred.

## Admission and geometric result

Every recorded feature fails the independently fixed identity criterion before line fitting: its transmitting aperture and corresponding aperture/receiver boundary point are unresolved. Source coordinates, receiver material-point coordinates and numerical endpoint uncertainties are therefore null, rather than made-up centers with arbitrary ±pixel errors. No finite noise allowance resolves a categorical identity ambiguity.

- Certified pairs: **0**.
- Primary 8 fitting / 4 held-out gate: **not passed**.
- Exploratory 3 training / 1 held-out minimum: **not met**.
- Fitted finite/infinite image point, line rank/conditioning, held-out miss and uncertainty sweep: **not computed**.

No arbitrary glyph centroids, best-converging letter assignments, two-line intersection or post-hoc date/angle were substituted. The existing 029 synthetic/reference controls remain the validation of the incidence engine. Image concurrence is necessary only; even successful incidence would not determine physical source type, depth, unique ground location or cipher use.

## What remains

This closes the specifically unattempted native-pixel manual inspection step. It does not make family 3 generally complete. A genuinely better independent annotation may still extract identities from this same exposure; the current result is inability to certify them in this bounded pass, not a resolution theorem. A model-assisted joint correspondence search would require its own frozen assignment domain and held-out validation, since choosing matches to converge cannot independently validate concurrence. Other views, a documented replica or independent aperture/spot markings could add information, but no new acquisition, outreach, site visit or purchase was undertaken or is claimed necessary merely to try this first test.

The exact missing input is a set of defensible non-K4 material-point identities with endpoint uncertainty and independent holdouts. North, scale and capture time are not the blocker for initial image-plane incidence. Finite Sun, thickness, lens/scan distortion and occlusion would still need treatment after point identity, rather than being used now to manufacture a fit.

An executor disconnection interrupted the first right-ground display. Files persisted; one availability check confirmed the outage, then after reconnection the right-ground view and remaining quadrants were completed. The source catalogue refresh returned 403 and was not retried. Neither interruption changed the data or scientific gate. All results remain local; canonical ciphertext, Site and public main are unchanged.

## Verification

The independent PNG scanline decoder confirms all nine declared rectangles exactly against the full native conversion. Python 3.9 and Python 3.12 produce identical crop/admission receipts; all 60 affected tests pass on each interpreter, including the existing 18 projection-engine/reference controls. [UTC validation/log hashes](../results/PHOTO-NATIVE-047-VALIDATION.json) distinguish this follow-through from the previous 702-test full suites, which were not repeated. An initial navigation check failed after the real replay receipt replaced its placeholder; regenerated navigation passes, and the initial logs are retained. No optical coordinates or numerical conclusion were changed to resolve that bookkeeping failure.
