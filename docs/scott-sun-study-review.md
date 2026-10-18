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
