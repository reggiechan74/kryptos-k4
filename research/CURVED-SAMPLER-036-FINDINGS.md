# Curved optical sampler: nominal keys, fragile assembly and an open evidence gate

24 October 2026 UTC. **The invented ideal-mirror model can generate complete 97-letter nominal keys, but none of the four utility-gate cases tested passed its declared assembly or pupil benchmarks.** This is not a K4 cipher result or a physical replica. Fifty other complete nominal poses were outside the frozen stability panel and remain untested for robustness. Neither the continuous model nor real curved-screen mechanisms are excluded.

The [immutable protocol](CURVED-SAMPLER-036-SPEC.md), [compact summary](../results/CURVED-SAMPLER-036-SUMMARY.json), [full lossless original](../results/CURVED-SAMPLER-036-ORIGINAL.json.gz), [every table pose](../results/CURVED-SAMPLER-036-poses.jsonl.gz), [mathematical/API contract](CURVED-SAMPLER-036-API.md) and [Site-ready synthetic fixtures](../results/CURVED-SAMPLER-036-SITE-FIXTURES.json) preserve complete finite coverage. No actual K4 plaintext/ciphertext/crib scoring, parameter fitting or external checker submission occurred. No Site file was edited or repository pushed.

## Two mechanisms, not one

The monument's curved, perforated copper can affect viewing, aperture transmission and illumination. Its shape, two-face contours, seams, local normals, pose and real reflectance are incompletely calibrated. The existing [source-space geometry audit](../docs/scott-sun-geometry-audit-2026-10-22.md) and [physical investigation](PHYSICAL-SOLAR-002-FINDINGS.md) must not be replaced by a perfect cylinder. The actual-surface branch remains evidence-gated; this study does not turn copper into a polished mirror or claim the observer needs secret on-site measurements.

The numerical branch is an **invented tabletop apparatus**: an opaque radius-1, height-2 cylinder with ideal mirror sides, a horizontal printed tableau, fixed reticle and point eye. Eight global parameters set eye distance/height, reticle scale/downward aim and table translation/rotation/pitch. Ninety-seven independent adjustments are forbidden. The reticle's 4/31/31/31 occupied cells use public inscription layout; the sampled table preserves literal ragged rows and blanks. This tests centre-cell identity, not measured glyph apertures, optical character recognition or a light intersection between letters.

The user’s artist-first motivation permits a visual look/copy/align procedure: place a curved mirror, printed tableau and reticle, identify cells and copy their symbols, then use ordinary reversible arithmetic. Our ray equations analyze that proposed process; they do not establish that its inventor would need to derive them. The apparatus has not been built or manually validated. Classical reflected-ray simulation is not physics invented after Kryptos: [Whitted’s 1980 primary paper](https://my.eng.utah.edu/~cs6965/papers/p343-whitted.pdf) explicitly models reflection and curved surfaces. That historical reference establishes availability of the physics, not creator use or guaranteed AI recovery.

## The frozen finite test

| Stage | Exact completed coverage | Outcome |
| --- | --- | --- |
| Optical panel | 560 global optical settings × 97 rays | 419 complete ground footprints; 141 invalid footprints |
| Fixed global table assembly | 108 table poses per complete footprint | 45,252 poses evaluated; no pointwise repair |
| Nominal key admission | All 97 cells interior/letter-valid, margin above 0.02 cell | 54 complete keys, 54 distinct cell paths and key strings |
| Utility diagnostic | At least 80 distinct cells and 12 letters | Four poses, sampling 82–83 cells and all 26 letters |
| Assembly and pupil tests | Four utility poses, 340 perturbation/bundle configurations each | No tested case stable under the complete benchmark |
| Synthetic recovery | Four utility-key classes, no true parameter supplied to matcher | All four plants retained; 13 known letters leave two classes, 11 held-out letters select one |

The utility cutoff is an explicit engineering choice, not a Kryptos clue or necessary condition for an optical cipher. The 50 other complete keys sample 52–79 distinct cells and 22–26 letters. Their lower density is not a cryptographic contradiction. They were not silently reclassified as invalid or stability-tested after the four utility failures. Up to 60,480 descriptions were possible; 15,228 table constructions were not instantiated because a required optical footprint already missed/failed. All 560 optical outcomes and all 45,252 actual table records are retained, not only attractive keys.

Table placement follows a frozen global bounding-box rule and fixed pitch/offset/rotation choices using geometry alone. No K4 clue or English word ranks a pose. Cylinder cap occlusion, rims, misses, grazing, upward/parallel ground rays, outside/ragged/blank cells and near-boundary ambiguity produce explicit invalid states. One invalid point makes the key null. No clamp, wrap or replacement invents a letter. Repeated sampled cells and symbol coincidences remain visible.

## A nominal recipe is not a stable manual device

The most interior utility case has parameters:

```json
{"D":3,"H":1.2,"s":0.06,"aim_deg":15,"tx":0.02806339729818461,"ty":-3.3809568845614844,"rotation_deg":0,"pitch":0.06875991962215679}
```

At illustrative radius 250 mm this means a 500 mm diameter/height cylinder, eye distance 750 mm and height 300 mm, with table pitch about 17.19 mm. The table centre is roughly (7.02 mm, −845.24 mm). These are arithmetic scale examples, not measurements or a constructed replica. A tabletop/support, reticle frame, observer body, illumination, real mirror roughness and actual printed glyph recognition require their own checks.

Its minimum cell margin is only 0.02338 pitch; the other utility pair has about 0.02165. Both barely exceed the frozen 0.02 admission threshold. The benchmark perturbs D/H by ±1 mm, table translation by ±0.5 mm, aim/rotation by ±0.1 degree, reticle scale by ±1% and pitch by ±0.5%, at radius 250 mm. All 256 corners, 64 seeded interior configurations and two lateral-eye checks are saved per case. This is a deterministic sensitivity panel, not a probability distribution of fabrication errors or a continuous interval certificate.

The pupil diagnostic holds each physical reticle-plane point fixed while moving the ray origin around an aperture rim. Both 0.05 mm and 1.5 mm radius panels fail for every tested utility pose. This reveals parallax/bundle sensitivity under this model, not a complete theory of accommodation or human perception. Diffraction, blur and retinal resolution are not simulated; a tiny peep aperture cannot be declared usable merely from ray geometry. The selected tiny-aperture failure fixture changes two cell assignments and loses the boundary safety margin at six points. The first assembly-corner fixture changes 40 cell assignments and has ten boundary-invalid samples. Admission loss and actual cell changes are distinguished; neither is averaged into a fabricated key.

The measured conclusion is therefore **nominal synthetic sampling succeeds; the declared robust/manual gate is not passed by the tested utility cases**. Other finite poses, a better constrained continuous assembly or a different apparatus may behave differently. No extra parameter tuning, smaller tolerances or larger search was added after the results.

## Independent validation, recovery and chance controls

An independent circle-closest-approach/angle-reflection oracle agrees on all 54,320 frozen ray statuses, with maximum ground-coordinate difference 1.16e−14. Analytic central rays, angle equality, unit norms, reverse-path reciprocity and negative fixtures pass. [Ray validation](../results/CURVED-SAMPLER-036-RAY-VALIDATION.json). Before the sweep, QA corrected a cap fixture that actually hit a rim and replaced inappropriate bitwise float-dictionary equality with the declared numerical tolerance; neither changed a physical threshold.

A separate complex-coordinate lookup independently reproduces all 4,389,444 cell/status decisions over the full 45,252-pose record stream. It confirms all 54 complete and four utility-gate cases. [Cell audit](../results/CURVED-SAMPLER-036-INDEPENDENT-CELL-AUDIT.json). These checks establish the stated numerical model, not mirror quality or monument geometry.

The synthetic layer adds/subtracts in KRYPTOSABCDEFGHIJLMNQUVWXZ. Plaintexts are seeded synthetic letters, not actual K4. Each plant’s true key/parameter owner is withheld from the finite-panel matcher. All four true full messages regenerate all 97 synthetic ciphertext letters. Thirteen planted known letters leave two key classes; the 11 genuinely held-out synthetic letters retain one. This is supplied **four-key-panel recovery**, not continuous eight-parameter inference, language discovery or actual K4 cryptanalysis. The continuous map is piecewise constant in cell regions; even a full key does not uniquely identify exact real-valued parameters.

All 31 matched synthetic null draws repeat the entire four-key/four-plant comparison. Maximum known-letter agreement is five of 24; none matches all 24. This is a finite synthetic control, not a p-value for K4 or a claim about arbitrary optical models. First-stage fit and held-out comparison are separated. No English fragments, adaptive reticle placement or 97-character backsolved key enter the test.

The complete original run was 2026-10-24T15:02:42.758132+00:00–15:02:55.969582+00:00. Sweep time was 10.27 seconds; peak RSS was 457,932,800 bytes, within 512 MiB. Original full-result/pose archives total about 7.35 MB compressed. Python 3.12 reproduces every discrete decision, key and recovery result and all saved pose records; floating values differ by at most 4.78e−13 under the predeclared 1e−9 absolute tolerance. [Full comparison](../results/CURVED-SAMPLER-036-PY312-COMPARISON.json). Timestamps, RSS and archive byte hashes remain separate rather than being rewritten as original data.

## The Site model is a different apparatus

A read-only inspection of the Site owner’s v18 parameter contract found a vertical tableau plane behind the eye, a fixed physical reticle, a variable-radius cylinder and rows centred in 33 display columns. The research model uses a horizontal table, angular reticle, radius 1, downward aim and literal left-registered rows. A coordinate-axis rename cannot turn the vertical object plane into the horizontal tabletop. [Dated comparison](../results/CURVED-SAMPLER-036-SITE-CONTRACT-COMPARISON.json).

These research results do **not** validate or invalidate the Site default or its separate curved-screen perspective illustration. The [API](CURVED-SAMPLER-036-API.md) and [nominal/failure fixtures](../results/CURVED-SAMPLER-036-SITE-FIXTURES.json) let a Site implementation demonstrate this exact research geometry if explicitly chosen. The Site’s reported tests/publication are owner/parent provenance, not independently rerun here. Its handoff inventory was inspected without extraction/execution; no Site source archive or deployment is part of this local study.

## Scope and next evidence

Earlier fold/slide studies compare registered transcript labels/surrogate apertures. Projection concurrence tests image-line incidence with certified real correspondence gates. This new model instead generates a key by ideal reflection and global cell sampling. It shares geometry principles and ordinary keyed arithmetic, but those earlier tests do not constitute coverage of its ray/registration family. Conversely, this synthetic key does not supply real aperture-ground pairs or a physical north/date/light observation.

No independent source fixes this mirror, reticle, printed table placement, readout or eight-parameter geometry as a K4 mechanism. Curvature motivates an investigation but does not choose a key. A useful next step is a separately frozen bench replica/calibration or source-selected visual alignment, with robustness, glyph readability, occlusion and independent held-out observations. More arbitrary crib-fitted geometry is not warranted. The actual copper/viewpoint branch needs its own source-grounded surface/optical model; it is not excluded by ideal-mirror sensitivity. The finite experiment ends here, with no actual K4 evaluation, public push or Site change by this task.

Final aggregate validation: **651 tests pass on Python 3.9 and 3.12**. [Separate UTC receipt and full logs](../results/CURVED-SAMPLER-036-VALIDATION.json). Canonical ciphertext and 210 unrelated duplicate files are preserved; no actual K4 evaluation, GitHub push or Site edit by this task.
