# PROJECTION-CONCURRENCE-029 — image-ray diagnostic and evidence gate

24 October 2026 UTC. This is a separately authorized physical-data diagnostic after the completed eight-item sequence. **Zero certified real pairs, zero monument fits, zero K4 trials.** Acquisition research is integrated with explicit worker/local attribution; synthetic success is not a monument result. Canonical ciphertext and the published Site are unchanged by this research checkout.

## What is now runnable

The [preregistered protocol](PROJECTION-CONCURRENCE-029-SPEC.md) was committed at `6bf1e23` before real-data fitting. The [native implementation](../experiments/projection_concurrence.py) fits one homogeneous image intersection from aperture/receiver lines. It reports conditioning, all retained-pair residuals, heldout line incidence, and endpoint/source-fit uncertainty sensitivity. [Independent scalar checks](../experiments/projection_concurrence_reference.py) use two-line determinants, finite-coordinate least squares and numerical incidence derivatives. [API/data contract](PROJECTION-CONCURRENCE-029-API.md) supports a separately owned Site demonstration; no live deployment is claimed here.

The scientific prediction is deliberately limited: a withheld receiver point should lie near the line joining its aperture image to the fitted source image. **The full receiving point is not predicted.** Its distance along the line is free without calibrated camera/surface/receiver geometry. Neither image concurrence nor finite versus infinite image coordinates identifies sunlight, a lamp, a reflected virtual source, physical depth, north or a historical date. A Sun direction usually has a finite vanishing point in a perspective photograph.

## Frozen synthetic results

The [complete synthetic receipt, fixtures and residuals](../results/PROJECTION-CONCURRENCE-029-SYNTHETIC.json) records execution at **2026-10-24T11:50:23.445087+00:00–11:50:23.802297+00:00**, 0.357 seconds and 15,712,256 bytes peak RSS, within 60 seconds / 256 MiB. These are diagnostic times, not photographic exposure dates. Eight fixtures × three uncertainty factors were retained: 21 evaluable configurations plus three collapsed-geometry rejections. Each evaluable configuration uses 256 deterministic source-fit perturbations; these are sensitivity calculations, not independent field observations.

| Fixture | Heldout combined RMS at nominal 0.25 px pick sigma | Conditional line result |
| --- | ---: | --- |
| Exact finite source | <1e-10 | Pass |
| Distant finite source | <1e-10 | Pass |
| Exact infinity direction | <1e-10 | Pass; infinity is representable |
| Noisy finite source | 0.569 | Pass |
| Four displaced heldouts | 111.73 | Fail |
| Mixed sources | 257.80 | Fail |
| Coincident image lines | 0 | **Unidentifiable**, fails conditioning despite zero residual |
| Aperture equals receiver | Undefined | Reject collapsed input |

These classifications persist at 0.5×, 1× and 2× the declared pick uncertainty. Fixed synthetic thresholds are heldout combined RMS ≤2 and max ≤4 plus nondegeneracy. They are proposed line-only engineering thresholds, not calibrated probabilities, a universal sufficiency theorem or actual monument error bars. Parameter uncertainty is conditional on independent isotropic Gaussian picks. Lens distortion, material-point misidentification and optical-source extent are not magically covered by those sigmas.

Sixteen core/frozen-artifact tests cover exact finite/infinity reference agreement, independent determinant derivatives, noisy/negative/degenerate controls, projective transforms, coordinate scaling, source/aperture coincidence and along-line displacement non-identifiability. Tests do not assume that a glyph's image centroid and a light patch's centroid correspond to the same physical point.

## Local wrong-correspondence sensitivity

A [separately frozen supplementary protocol](PROJECTION-CONCURRENCE-029-LOCAL-CONTROLS-SPEC.md), committed at `475edf5` before its evaluation, adds nearby receiver alternatives without changing the original fixtures or gate. [All eleven outputs](../results/PROJECTION-CONCURRENCE-029-LOCAL-CONTROLS.json) are retained. Offsets ±0.25, ±0.5 and ±1 pixel **pass** the conditional gate (nominal RMS approximately0.466,0.932,1.864); ±2 and ±5 pixels fail (RMS3.728,9.320). A shared(+2,+2)pixel translation of every receiver also **passes**, RMS1.232. These are deliberately wrong synthetic correspondences/systematics that remain compatible. They are a concrete warning against interpreting a low residual as certified identity or treating independent Gaussian pick errors as a calibrated model for shared bias. Offsets are illustrative local edge-feature alternatives, not measured spacing in real sculpture photographs.

The local panel independently checks raw-pixel determinant distances before native fitting. It does not estimate field false-match probabilities, select a new tolerance or fit any real pair. Concurrence is necessary only: projected image lines can concur even when hypothesized three-dimensional lines do not share a physical source. Uncertain point identity must be resolved independently rather than certified by the estimator.

## Preserved engineering corrections

Initial QA incorrectly expected separated parallel lines to be nonunique. In projective geometry they can determine a valid point at infinity; only coincident/rank-deficient or poorly conditioned constraints are uninformative. The [initial failure receipt](../results/PROJECTION-CONCURRENCE-029-INITIAL-QA.json) and protocol amendment preserve this correction before any real fit. All original positive/negative fixtures and thresholds were retained.

An added adversarial case placed the fitted source at one training aperture. Its residual was explicitly undefined, but an initial gate inspected only holdouts and could still return true. The corrected gate requires **every retained pair residual to be defined**, with no pair dropping. The [failure log](../results/PROJECTION-CONCURRENCE-029-degeneracy-initial.log.txt), [QA note](../results/PROJECTION-CONCURRENCE-029-DEGENERACY-QA.json) and [initial synthetic receipt](../results/PROJECTION-CONCURRENCE-029-SYNTHETIC-INITIAL.json) are preserved. The current receipt reruns the unchanged fixtures with the corrected guard. Neither issue was a monument negative.

## Completed acquisition review and local check

The [full worker-authored acquisition report](evidence/2026-10-24-projection-acquisition/PHOTO-ACQUISITION-REVIEW.md) is now saved, with a [consumer-transcribed source/ROI inventory](evidence/2026-10-24-projection-acquisition/SOURCE-INVENTORY-AND-GATE.json). The worker found genuinely different CIA/Gillogly views with visible bright patterns, but established **zero certified pairs**. Three reported ROIs are observation rectangles only. Different image sizes of one exposure are not independent observations; different exposures cannot share one source fit without a justified common illumination model.

The consumer separately verified the locally available LOC TIFF SHA256 and 3384×4283 dimensions and visually inspected an existing 2000×1500 ground-detail PNG. It contains bright letter-like forms and blur/texture/occlusion, but no uniquely certified transmitting row/material point. The old crop's original-coordinate transform was not recovered, so no source-pixel annotations were manufactured. [Local receipt](evidence/2026-10-24-projection-acquisition/LOCAL-REVIEW.json) distinguishes this limited check from the worker's broader survey. No original photographs or raw source scrapes are published.

Smithsonian Series8 Box11 Folder34 is an exact **undigitized public-access lead**, not an acquired frame set. The worker reports the official Aeon reproduction route and posted rates as of24 October2026; these are attributed published guidance, not a quote, order or permission. The useful next acquisition would be an inventory/contact sheet and identifiers for overlapping original courtyard frames with mounts/sleeves/sequence metadata. No outreach, payment, account creation or appointment was performed; a paid/access-dependent branch remains outside current authorization. Public CAPTCHA-protected image leads were not bypassed. Missing photographs are not proof that a physical model is false.

**Stage conclusion:** diagnostic engineering complete; real-data concurrence remains **evidence-blocked**, with zero fits. It would be scientifically invalid to run the estimator on arbitrary glyph/spot centroids merely because it is now available. The Site demonstration is a separate implementation handoff, not a change to this result.

## Real evidence required before fitting

The existing [source-space geometry audit](../docs/scott-sun-geometry-audit-2026-10-22.md) remains prior work. Its boundary observations and cross-view aperture centers do not become aperture-to-ground material-point pairs. The original-resolution LOC view is a stronger version of a previously known exposure, not a newly independent view. No correspondence has been certified in this investigation yet.

A practical first dataset requires:

- One identified original exposure, catalogue URL/hash, exact dimensions, orientation/crop mapping and central-camera/lens-distortion assessment.
- At least 12 independently certified **non-K4 physical point** pairs, distributed across at least three rows and three horizontal regions. Fix eight fitting and four spatially distributed heldout pairs before optimization. More pairs do not repair rank degeneracy or wrong identities.
- Literal aperture/receiving-feature correspondence rationale, non-K4 row/position identity, repeated blinded picks and endpoint uncertainty. Letter-name similarity alone is insufficient; uncalibrated glyph centroids can differ from corresponding transmitted material points.
- An independently declared optical/model-error allowance: finite Sun creates an extended directional support; plate thickness can change the active entry/exit aperture; partial occlusion and penumbra can shift visible extrema; curved surfaces do not invalidate straight rays but complicate identification. A single point-source approximation must be justified at the needed tolerance rather than enforced by enlarging error bars after fitting.
- No post-fit reassignment/removal of pairs or tolerance tuning. After line-incidence validation, independently calibrate receiving-plane geometry to make a genuine full-position prediction. Only later could a frozen extraction rule be considered; no date-to-English search is authorized by this diagnostic.

The mathematical minimum to specify a projective intersection is two independent lines, which gives no validation. Three or more provide redundancy, but even many wrong or correlated pairs can be concurrent. The proposed twelve-pair sampling/holdout design is not proof of authenticity, a statistically independent sample or a universal minimum. The same camera exposure can test image geometry without supplying absolute scale or historical time.

## Reproduce

```sh
python3 -m unittest discover -s tests -p 'test_projection_concurrence.py'
python3 experiments/run_projection_concurrence.py --output /tmp/projection-replay.json
```

The replay emits fresh UTC times and current implementation/spec hashes. Preserve original receipts. It consumes only fixed synthetic coordinates and no plaintext/ciphertext. The [API contract](PROJECTION-CONCURRENCE-029-API.md) includes deterministic fixture construction and warns against treating any simplified browser uncertainty display as identical to the research perturbation estimate.

A finite physical emitter lying in the camera-center plane can also project to an image point at infinity. Image homogeneous coordinate `sw=0` describes image projection geometry, not physical source distance. An explicit finite-3D-emitter control tests this distinction.

Final aggregate validation: **587 tests pass on both Python3.9 and Python3.12**, including18 focused projection/artifact/local-mismatch tests. [UTC regression receipt and full logs](../results/PROJECTION-CONCURRENCE-029-VALIDATION.json); [complete cross-version payload replay](../results/PROJECTION-CONCURRENCE-029-PY312-REPLAY.json). Generated-inventory ordering failures are retained separately and corrected by regenerating scope audit after navigation; no scientific fixture or threshold changed.
