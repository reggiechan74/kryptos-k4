# K4 item 2: physical shadows, astronomy and navigation

Research date: 24 October 2026. Scope: item 2 only. No World Clock panel investigation, date/angle-to-English search, outreach, purchase, or change to the live model. Repository baseline inspected: main tree 91b49e233787e3bd449407247602a1b02a7ff9ae.

Provenance: independent research supplied by the parent as plain text. This preserved research narrative is not a claim that the repository owner personally repeated every search or image inspection. The separately supplied arithmetic source has HTML transport operators decoded. Local validation and scope notes are in the adjacent README and replay receipt. No original images or source scrapes are included.

## Conclusion

**No new public source recovered a surveyed orientation, original installed aperture dimensions/contours, emitter coordinates, or authenticated observation time. The physical hypotheses remain evidence-blocked, not disproved.**

This pass nevertheless adds three useful things: an original-resolution optical calibration asset, several quantitative pre-decoding rejection tests, and a concrete protocol that separates image/physics validation from historical-date claims. It does not repeat the previous 252-image Smithsonian screen or manufacture missing dimensions.

## 1. What is genuinely new, and what was already known

### A. Original-resolution Highsmith image: new acquisition, not a new photograph

The [Library of Congress record, LCCN 2011631531](https://www.loc.gov/pictures/item/2011631531/) was already in the geometry audit. That audit inspected the 809 × 1024 service version. This pass downloaded the catalogue-linked [41.5 MB original-resolution TIFF](https://cdn.loc.gov/master/pnp/highsm/13300/13337u.tif), decoded it as **3384 × 4283, 8-bit RGB**, and inspected the overall image and a native-pixel ground crop.

The frame shows actual letter-shaped light on the paving, with detailed forms in the left part of the visible projection field and broader spots toward the right. These are observations of this exposure, not measurements of penumbra alone: perspective, different transmitting letters, depth, incidence, occlusion and image processing can all contribute. No aperture-to-spot identities or physical distances are claimed.

This improves available image-space detail by about 4.18× per linear dimension over the previously inspected service image. It does **not** create an independent exposure or supply metric scale.

- TIFF SHA-256: `302fb88dee8db7f484a85d9d7f9bbd39f69de37cbf7bb25ae5a2e35bf8b8cf52`.
- TIFF/IPTC inspection found description, photographer and broad location metadata, but no exposure timestamp, camera/lens specification, GPS or north registration.
- The catalogue still dates the transparency broadly **[between 1980 and 2006]**, and warns that the digital representation may differ from the original film.
- Its approximately 169.2 dpi tag concerns image/print representation, not millimetres on the sculpture.
- This photograph has not been fitted in this pass. Its ground pattern is a potential independent optical check, not a dated solar calibration.

The earlier source-space reconstruction is real prior work: 44 boundary observations, 21 usable non-K4 cross-view glyph correspondences and a partial rubbing contour. Its 800- and 1200-pixel first-camera scenarios both fitted held-out glyph centers to about 3 pixels while retaining materially different curvature. Do not erase this work or call a generic new font model progress. The old held-out points have already been inspected and are not fresh final validation data. See the existing [geometry audit](https://github.com/reggiechan74/kryptos-k4/blob/91b49e233787e3bd449407247602a1b02a7ff9ae/docs/scott-sun-geometry-audit-2026-10-22.md) and the retained source-space calibration package.

### B. A physical prototype is explicitly dimensioned, but not the installed screen

The already-known [Paradigm archive gallery](https://www.paradigm.xyz/kryptos/archive) specifically captions a curved proof-of-concept plate as **12 × 24 inches, 3/8 inch thick, 1988**. The close-up was retrieved and visually confirms the engraved “J.S. 1988” date. The dimensions remain catalogue statements, not this pass's instrument measurements.

This is an independently inspectable artifact lead consistent with the artist's retrospective 3/8-inch account. It cannot resolve the installed screen's thickness, curve, overall dimensions, lettering or seams: a prototype is not the completed sculpture. The gallery was already in the dossier; this exact dimensional distinction is the added use of it, not a newly discovered archive.

### C. Fresh source routes that did not clear the gate

- Targeted manufacturer/fabrication, conservation and landscape-construction searches did not locate an as-built plan or measured light installation. Results chiefly returned the already-audited artist papers, CIA/GSA summaries and unrelated material.
- A newly checked [LOC aerial, LCCN 2011631596 / highsm.13402](https://www.loc.gov/item/2011631596/) was visually inspected at 2290 × 1781. The sculpture is not resolved in the view; the broad catalogue date also supplies no solar timestamp. It is not useful new screen geometry.
- [Elonka's video catalogue](https://elonka.com/x/videos.html) identifies 1991 ABC courtyard B-roll and 1999 footage. The listed 1991 WMV request returned a CAPTCHA interstitial rather than video. No CAPTCHA was completed, no alternate route used to evade it, and no frames or measurements were obtained. The year in the catalogue is not an exposure clock time.
- The known undigitized Smithsonian Box 11 Folder 34 photographs and Box 9 Folders 11–13 sketchbooks remain access-dependent. No hidden images were inferred and no paid or contact route was attempted.

### D. Important old evidence retained unchanged

The artist draft's 3/8-inch plate and two-inch letters, the **1990 typed small-pool 500 W lamp schedule**, and the static/metaphorical compass needle were all established previously. They are not discoveries of this pass. Neither “small pool” nor the twelve-inch water-level warning measures the emitter's height or beam direction. The handwritten seasonal wording conflict remains separate from the typed instructions. [Locally verified primary-scan addendum](https://github.com/reggiechan74/kryptos-k4/blob/91b49e233787e3bd449407247602a1b02a7ff9ae/research/evidence/2026-10-23-lodestone-compass/PHYSICAL-ADDENDUM-LOCAL-REVIEW.md).

## 2. New quantitative discriminators before any cipher scoring

These are derived physical constraints under stated assumptions, **not a newly measured Kryptos model**. A short replay and JSON receipt accompany this report.

### 2.1 A lower lamp cannot directly project through higher letters onto lower ground

Let L be the emitting point, A an aperture point, and P a point beyond the aperture on the same ray:

`P = L + s(A − L), s > 1`.

If `A_z > L_z`, then `P_z > A_z`. Therefore a lamp below the aperture cannot send a direct transmitted ray through it to a receiver below that aperture. A lamp below the plaza and an above-plaza letter cannot form that letter's direct transmitted-light image on the plaza.

This is a strict rejection of **that conditional optical path only**. The source does not yet establish the actual emitter height, so it does not reject the historical lamp installation. It also does not reject projection onto an upper wall, illumination of the copper itself, an independent external lamp, or a path containing a reflector. Simple transmission from water into air at a level interface preserves the upward vertical sign; it does not bend an upward ray downward. A reflector would need its own documented location and orientation.

The immediate missing measurement is consequently not just bulb wattage: it is **emitter position relative to the selected aperture and receiving surface**.

### 2.2 Finite sunlight imposes non-negligible blur

[NASA's Sun Fact Sheet](https://nssdc.gsfc.nasa.gov/planetary/factsheet/sunfact.html) gives a full apparent diameter of 1919 arcseconds at 1 AU, ranging from 1887 to 1952. Using 1919 arcseconds gives `d = 0.0093036 rad`.

For an infinitesimal zero-thickness aperture at height z above a flat horizontal receiver, unobstructed sunlight of elevation h produces an extended-source footprint. To first order its **full diameters**, not radii, are:

- Along the solar vertical plane: `B_parallel ≈ z d / sin²(h)`.
- Across it: `B_perpendicular ≈ z d / sin(h)`.

For **one metre of aperture height**, the full widths are:

| Solar elevation | Along-ground major width | Across-ground minor width |
|---|---:|---:|
| 9.55° | 338 mm | 56 mm |
| 15° | 139 mm | 36 mm |
| 30° | 37 mm | 19 mm |
| 45° | 19 mm | 13 mm |
| 60° | 12 mm | 11 mm |

Multiply by the actual height in metres; that height has not been measured here. The replay also checks the exact conical footprint, agreeing with these approximations within 0.1% for the listed angles.

These are blur-support sizes, **not an automatic illegibility threshold**. A finite glyph contributes its own projected footprint; a partly clipped solar disk can change the kernel. A defensible model must propagate the finite source, actual contours, thickness and occlusions rather than cast one center ray per letter or render hard-edged point-Sun typography.

### 2.3 Plate thickness can erase narrow channels at modest obliquity

For an ideal straight channel of width w along the in-plane ray displacement, thickness t, and incidence angle θ from the **local plate normal**, the front-to-back displacement is `t tan(θ)`. The one-dimensional clear overlap is `max(0, w − |t tan(θ)|)`.

Using the retrospective **3/8-inch = 9.525 mm** plate scenario:

| Hypothetical channel width | Zero-overlap incidence |
|---|---:|
| 3 mm | 17.48° |
| 5 mm | 27.70° |
| 10 mm | 46.39° |

These channel widths are illustrative, **not measured Kryptos strokes**. Local curvature determines the local normal. Real hand-cut channels may taper or differ across faces, so a measured two-face contour supersedes the ideal prism.

The conflicting plate reports matter materially: for a hypothetical 5 mm channel the cutoff is 38.22° at 1/4 inch, 27.70° at 3/8 inch, and 21.49° at 1/2 inch. Preserve these as named source scenarios, not endpoints of a measured probability distribution. A zero-thickness renderer cannot settle this branch.

### 2.4 Exact ENE sunlight has a stringent local-horizon gate

The earlier seasonal review already derived the solar-center bound for illustrative latitude **38.95° N**, exact true azimuth **67.5°**, and annual declination within **±23.44°**:

`sin(δ) = sin(φ)sin(h) + cos(φ)cos(h)cos(A)`.

This pass reproduces the maximum geometric solar-center elevation **9.5505°** and adds a directly testable obstruction criterion:

`(obstacle top height − aperture height) / horizontal distance > 0.16825`

blocks the center of direct ENE sunlight at all annual dates under that geometry, provided the opaque obstruction lies in the exact azimuth and extends below the relevant sightline. For example, an obstruction 1.68 m above an aperture at 10 m distance is already near the limit. **No such obstruction has been measured at Kryptos in this pass.**

Finite solar radius, atmospheric refraction and the object's actual sky profile must be included near the cutoff. This criterion is not valid for window-reflected light. Nor does it concern an **ENE shadow**: that uses a WSW Sun, the distinct branch already retained in the seasonal review. [Existing conditional solar analysis and NOAA reference](https://github.com/reggiechan74/kryptos-k4/blob/91b49e233787e3bd449407247602a1b02a7ff9ae/docs/seasonal-light-source-review.md).

### 2.5 Required angular precision can be stated before fitting

For a point at height z, the horizontal shadow displacement has magnitude `z cot(h)`. Small direction errors give approximately:

- Heading error ΔA: transverse error `z cot(h) ΔA`.
- Altitude error Δh: longitudinal error `z csc²(h) Δh`.

At h = 30° and z = 1 m, a one-degree error is about **30 mm transverse** or **70 mm longitudinal**. These are first-order sensitivities, not actual error bars. They explain why a roughly reported bearing or unverified camera time cannot support millimetric letter-selection claims. Choose allowable angle/time uncertainty from the smallest relevant measured feature, not from a desired plaintext.

## 3. Feasible calibration and falsification protocol

1. **Freeze source identity and coordinate conventions.** Preserve originals, hashes, crop transforms and capture-date uncertainty. Distinguish true north, engraved N, engraved needle, stone vector and a real instrument reading. Use the existing source-pixel observations rather than rebuilding an unreferenced grid. Do not promote scan DPI, nominal paper size or a prototype dimension into installed scale.
2. **Finish a shape check before an optical decoder.** Carry forward multiple surviving partial surface scenarios. Annotate additional non-K4 correspondences on the original-resolution LOC view, with repeated blinded picks to estimate measurement disagreement. Fit only that view's camera and explicitly declared nuisance parameters. Reserve spatially distributed observations before optimization. Do not choose a curvature from the old holdouts and then call those same points independent confirmation.
3. **Treat absolute scale, solar direction and clock time as separate questions.** Image-space geometry can be tested without claiming metres or a historical date. A nuisance illumination direction fitted from non-K4 physical features is permissible for an optical feasibility test, but is not an authenticated celestial observation or a K4 time key. An absolute scale needs an independently measured length. A historical solar claim additionally needs authenticated site, date, time-zone convention and horizon.
4. **Require real aperture-to-projection correspondences.** Before numerical optical fitting, establish a predeclared set of unambiguous non-K4 aperture/ground-feature pairs distributed over multiple rows and portions of the visible curve. If the photo cannot establish them, stop that fit instead of assigning each spot to whichever letter makes the model work. Keep projection-shape/position holdouts distinct from camera-fitting landmarks. A concrete proposed first gate is at least 12 unambiguous pairs across at least three non-K4 rows and three horizontal portions, with eight training pairs and four spatially separated holdouts fixed before fitting. Estimate each annotation covariance from repeated picks, then require held-out normalized point RMS ≤2 and no point residual >4 annotation-standard-deviation units. These are proposed engineering acceptance thresholds, not a calibrated probability or a result already achieved; publish systematic-error sensitivity as well. Keep all source/receiver/model alternatives fixed before testing. Extend to held-out contour overlap and brightness profiles only after position correspondence passes.
5. **Enforce physics and path identity.** Compare direct solar, reflected solar and fixed artificial light as different models. Test emitter/receiver vertical ordering, finite-source blur, thickness clipping, screen self-occlusion and real receiver extent. For reflection, record the reflecting surface normal; for submerged light, water level/interface and housing optics are additional inputs. The 500 W rating does not specify source size, angular emission or a point projector.
6. **Only after calibration, specify one decoding rule.** Freeze date/direction rationale, receiver, glyph classification, traversal, tolerances and every remaining searched parameter. Require exact full 97-character re-encryption and whole-pipeline negative/planted controls. The public cribs are constraints, not unseen validation. If results change across independently admissible geometry/contours, report non-identifiability rather than selecting the English-looking scenario.

A useful first success would be predicting withheld **ordinary light spots** in the LOC image. It need not and should not begin by generating words. A failed calibrated model rejects that model/path; a failed uncalibrated renderer does not reject physical Kryptos.

## 4. Status and stopping boundary

- **H-OPTICAL / H-SHADOW-TIME:** still evidence-blocked for an actual decoding claim. Better source pixels and new analytic tests are available; no optical key was recovered.
- **H-CELESTIAL-ALTITUDE:** no new independently anchored observation, date, horizon or observation-to-key mapping. No new ephemeris coincidence hunt was performed.
- **H-COMPASS-FRAMES / H-COMPASS-REVERSE / H-GEO-ENE:** no new surveyed axes, historically fixed endpoint or extraction. Exact ENE/WSW nomenclature remains a conditional input, not an installed measurement.
- **H-NEPTUNE:** no new creator linkage or uniquely determined mechanism. Previously reviewed discovery history/bearings are not rerun.
- **Historical World Clock item 3:** not started.

The bounded fresh search used five Exa searches requesting 39 result slots and five Firecrawl searches, plus targeted page retrieval. Slots include duplicates and off-topic results, not 39 independently reviewed sources. The meaningful new acquisition is the full-resolution version of a known ground photograph; the other fresh routes did not resolve the missing physical metadata. This is a defined evidence gap, not a declaration that no relevant records exist.

## Reproducibility package

- `replay_physical_constraints.py`: pure standard-library arithmetic; no ciphertext or plaintext input.
- `physical-constraints.json`: exact conditional values and unit/assumption labels.
- Source originals were inspected locally but are **not part of the suggested repository publication**. Preserve catalogue links and hashes instead of rehosting copyrighted imagery or raw source scrapes.
