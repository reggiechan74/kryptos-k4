# Scott's public Sun Study — source/UI review

18 October 2026. [Public artifact](https://claude.ai/artifact/R4dbpABxFqWKNLjDDxykGR).
This records the supplied source/UI audit and recommendations already delivered
to the user. The application script was inspected at **2026-10-18 16:46:05 UTC**:
12,887 characters excluding script tags and external libraries; SHA256
`f27d18b53c9793d314351e542fe7fbc0daccf78a8837a213dc039ec93bf2ca99`.
That is the supplied inspection fingerprint, not a hash recomputed by this executor.
The cloud browser failed WebGL initialization, so **no working 3D scene was
validated**. This executor's web retrieval also could not access the artifact.
No third-party source is republished here; the artifact was not modified and no
new experiment was run.

## 22 October 2026 update: current v2 audit

The [complete geometry and measurement audit](scott-sun-geometry-audit-2026-10-22.md)
covers the newer **ray-traced v2** retrieved on 22 October 2026. It models both
pools and includes analytic occlusion. The statements below about absent pools
and the earlier default overlay's missing occlusion describe the **18 October
version only** and are stale as descriptions of v2. The new audit documents
remaining geometry, calibration, aperture and optical-path limitations; the
presence of pools or occlusion does not establish physical accuracy.

The full audit is preserved verbatim from the researcher's supplied Markdown:
24,143 UTF-8 bytes, SHA-256
`8d60cfdc23372d90fe9517ef1e11a84b1022e2fd6d8988d73559df1e0fc8a2db`.
Its source inspections and measurements belong to that dated audit; this
repository-preservation step did not independently repeat them. The companion
PDF remains in the user's Library and is not included in this checkout because
its supported Library-to-Mac transfer failed. The dated historical review below
is retained unchanged.

## What the inspected implementation supports

The code has actual font-shaped alpha cutouts and shadow mapping. It is more
than a grid of rectangular holes. However, its default sharp projected-letter
canvas overlay ignores blocking by other panels and the post. Thus plausible
looking default letter light is not evidence that the corresponding optical path
is unobstructed. The receiver is flat ground only: there is no water surface,
virtual-image reflection, or reflected illumination path.

The geometry assumes two equal half-cylinders of radius 1.52 m and height 3.66 m,
plus a central post. These are approximations, not a calibrated reconstruction.
The UI says 31 columns while code uses 32. Copied rows range from 29 to 33 letters;
one 33-character row loses its final T. K4's sequence itself is the correct
97 letters, but its artificially assigned spacing is not a measured aperture
layout. **Do not blindly replace 32 with 31**: first establish physical positions,
row offsets and the full text layout from appropriate images or drawings.

The opposite tableau parameterization may intentionally represent back reading.
The [CIA description and gallery](https://www.cia.gov/legacy/headquarters/kryptos-sculpture/)
explicitly describe the flipped tableau. Without a working render and a defined
viewing side, it should not be called a mirror bug. Official
[full-sculpture](https://www.cia.gov/static/abd544959a29872a36a9a76b7ef28542/d8196/kryptos_sculpture_3_lg.jpg)
and [basin](https://www.cia.gov/static/a27ae725e303b7c021384ac9688579e8/1949f/kryptos_sculpture_5_lg.jpg)
images are reference material, not calibrated scene coordinates by themselves.

## Time, heading and solar assumptions

The date/time defaults are November 3, 1990 at 09:00, heading 0 and DST off.
The date matches the dedication date documented by CIA; the time, true-north
heading and other settings are not thereby established as historical measurements.
The manual-angle defaults of azimuth 135° / elevation 35° are separate from the
Sun derived from date/time, and must not be conflated with it.

Converting 09:00 at UTC−5 to 14:00 UTC is correct. The inspected implementation
uses a NOAA-style solar calculation, with manual DST, an always-365-day year
denominator, no refraction and no solar-disk blur. These are accuracy/model
limitations, not a demonstrated UTC-sign bug. The
[NOAA equations](https://gml.noaa.gov/grad/solcalc/solareqns.PDF) specify leap-year
handling and timezone/longitude conventions. Exact timestamp, timezone/DST,
heading and angle mode must be recorded together to reproduce a scene.

## Recommended order of work

1. Make projected-letter overlays respect panel/post occlusion; distinguish the
   overlay from physically shadow-mapped illumination.
2. Correct and calibrate the physical letter layout, including row lengths,
   offsets and aperture positions, before changing the column count.
3. Calibrate curvature, dimensions, post, placement and true-north heading.
4. Specify the actual receiver and any reflection path, distinguishing the
   separate calm pond from the bubbling basin and object reflection from light
   transmitted through apertures.
5. Validate a reproducible scene against a real photograph using independent
   features; reserve other features for checking rather than fitting all of them.
6. Export all geometry, solar/manual-angle mode, date/time, timezone/DST,
   receivers, occlusion settings and uncertainty with every result.

Until that validation, this is an illustrative model, not a measured solar key,
a reconstruction of the 2002 reflected-light event, or a K4 optical exclusion.
The [seasonal-light and pool-reflection review](seasonal-light-source-review.md)
records the source evidence and the gates before any extraction rule is tested.
