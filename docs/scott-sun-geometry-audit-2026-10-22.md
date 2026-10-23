# Current Scott Sun Study: geometry and measurement audit

Audited 22 October 2026, approximately 13:21–13:27 UTC. Read-only public-source audit; no user repository or computer changed, no fitting or optical key search performed.

## Decision

Reuse the current artifact's explicit coordinate conventions, separation of the two pools, acknowledgement of uncertainty, and requirement for photo validation. Do not reuse its numerical geometry, sans-serif apertures, uncalibrated justified layout, or optical output as measured physical truth. Current v2 is materially better than the 18 October version, but its own first photo check failed and it does not contain the observations or fitting procedure needed to reproduce that conclusion.

## Exact version

Source: https://claude.ai/artifact/R4dbpABxFqWKNLjDDxykGR . Fresh retrieval requested with maxAge=0. The last inline application script identifies its JSON model as “Kryptos Sun Study, ray-traced v2”. Saved UTF-8 script: 32,238 bytes, SHA-256 0adbb2ddaf5036f14c1b22c24e52277fc1986b30e37f57ba28bb5249fe222f2f. Acquisition is a retrieval timestamp, not an artifact publication timestamp. The surrounding page's build-git-hash/build-timestamp describe Claude's host and must not be treated as Scott's artifact version/date. No authenticated author ID or publication revision was returned.

The earlier repository review https://github.com/reggiechan74/kryptos-k4/blob/main/docs/scott-sun-study-review.md identifies the 18 October script as 12,887 characters and SHA-256 f27d18b53c9793d314351e542fe7fbc0daccf78a8837a213dc039ec93bf2ca99. Its 1.52 m radius/3.66 m height, central post, no pools, unoccluded default overlay, 32-column layout, 1990-11-03 09:00/heading 0° defaults are historical findings. They are NOT accurate descriptions of this live v2.

## Geometry matrix

Ranges below are Scott's chosen plausible intervals, not confidence intervals or surveyed tolerance. Confidence is our interpretation of provenance, not the source UI's color coding. All position dimensions are in the artifact's local frame.

| Variable | Default | Source range | What it is | Provenance and confidence |
|---|---:|---:|---|---|
| H | 2.75 m | 2.55–3.02 | Vertical copper height, common to both halves | Inferred from 28 rows times claimed pitch plus margins. WIRED's overall main-sculpture height is not a sheet measurement. Low. |
| y0 | 0.05 m | 0–0.20 | Bottom of copper above y=0 paving | Visual estimate, no annotated photograph or points. Low. |
| L | 2.85 m | 2.30–3.10 | SURFACE ARC LENGTH of EACH half | Derived from 31 pitches; source also reports failed 7-point fit favoring L/H~0.88. Neither reproducible. Low. |
| Rc | 1.45 m | 1.20–1.70 | Cipher circular radius | Photos/aerial estimate without identified image or picks. Low. |
| Rt | 1.45 m | 1.20–1.70 | Tableau circular radius | Same; equal defaults not evidence of equal radii. Low. |
| mTop | 0.055 of H | 0.03–0.08 | Upper text-band margin | Chosen to produce ~2.45 m text height. Low. |
| mBot | 0.055 of H | 0.03–0.08 | Lower text-band margin | Same. Low. |
| mSide | 0.023 of L | 0–0.05 | End margin at each side | Derived from assumed arc/pitch. Low. |
| glyph | 0.87 of row cell | 0.80–0.92 | Canvas font em-height ratio | UI calls it published, but Sheldon reports 3 inches, not ratio 0.87. Ratio is derived from 3/3.45 and estimated pitch. Low for this ratio. |
| treeX | -2.80 m | -3.10 to -2.50 | Petrified tree center x | Qualitative left-of-screen description plus chosen position. Low. |
| treeZ | 0 m | -0.40–0.40 | Tree center z | Explicit placeholder. Unknown. |
| treeR | 0.30 m | 0.20–0.45 | Tree top/render and analytic radius | Explicit placeholder. Unknown. |
| treeH | 3.35 m | 3.20–3.50 | Tree height | Rounded WIRED 11 ft=3.3528 m. Reported physical dimension, not survey; other accounts conflict. Medium as published report only. |
| bubX | 1.20 m | 0.80–1.60 | Bubbling pool center x | Sanborn tree-hole account supports approximate size/existence, not this coordinate. Low. |
| bubZ | 0.20 m | -0.30–0.60 | Bubbling pool center z | Same. Low. |
| bubR | 1.10 m | 0.90–1.22 | Bubbling pool disk radius | Derived upper bound from reported8 ft hole; finished waterline not measured. Low. |
| bubW | -0.30 m | -0.40 to -0.20 | Analytic bubbling water elevation | Unidentified1999 photo estimate. Low. |
| calmX | 6.40 m | 3–10 | Calm pond center x | Aerial estimate with no imagery acquisition, scale, or measured points. Low. |
| calmZ | 30.30 m | 27–33 | Calm pond center z | Same. Low. |
| calmR | 1.60 m | 1.20–2.20 | Calm pond substitute disk radius | Explicit disk approximation to claimed 6 × 2.5 m slot. Not actual shape. Low. |
| water | -0.05 m | -0.25–0 | Analytic calm-water elevation | Explicit placeholder. Unknown. |
| heading | 140° | ±10° | Bearing of local+z front toward courtyard | Dunin's roughNW viewing direction supports SE-facing front, not140° precise. Aerial45–50° axis untracked. Low. |
| minutes | 0 min | ±10 | Clock perturbation | Chosen tolerance, not camera clock measurement. Unknown statistical meaning. |
| LAT,LON | 38.95227,-77.14577 degrees | none | Sculpture coordinate for solar calculation | Aerial estimate, no survey/source image supplied. Low, adequate approximate latitude only. |

## Derived dimensions and exact surface definition

Not two half-cylinders: each half is a circular arc with angle φ=L/R. At defaults φ=1.96551724 radians=112.61584249°. Both halves meet at local x=z=0. Cipher u=0 is its outer end, u=1 the seam; tableau u=0 is its outer end, u=1 the seam, read from the opposite side. For b=+1 the cipher bulges toward courtyard (+z), tableau toward -z. Circular centers are (-Rc sin(φc/2), -b Rc cos(φc/2)) and (+Rt sin(φt/2), +b Rt cos(φt/2)); y=y0+vH. No evidence the built surface exactly follows this two-circular-arc family. Independent perturbation of radii with common L can also break the smooth tangent at the join.

At defaults:
- Each surface arc2.85 m; each straight endpoint chord2.412889385 m.
- Both halves' straight overall endpoint span4.825778770 m; total unfolded width5.70 m.
- Each sagitta0.645642366 m; total front/back depth1.291284731 m.
- Bottom copper y0.05 m, top2.80 m.
- Top/bottom text-band margins 151.25 mm; side arc margin 65.55 mm.
- Text band 2.4475 m high; center pitch 87.410714 mm=3.44137 in.
- Fixed31-column arc pitch 87.706452 mm=3.45301 in.
- Top/bottom row centers y2.605044643 m and0.244955357 m.
- Nominal font em height 76.047321 mm=2.994 in. This is not the glyph ink height.
- Calm-disk center distance 30.968532 m from seam, bearing 128.073227° under140° front heading.

Coordinates: local x runs along overall screen, y up, +z courtyard/front. World x East,y up,z South. rotation.y=π−heading. At140° front, screen chord axis is50°/230°. Solar azimuth clockwise from true North; elevation above horizontal. Tableau's mirrored appearance from the cipher side is intentional and independently consistent with the CIA's description, not automatically a rendering bug.

## Text and apertures

Both halves use28 rows. Current text arrays are attributed to the Dunin transcript at https://elonka.com/kryptos/transcript.html and are consistent with inspected row breaks; a complete byte-for-byte transcript reconciliation was not performed. Cipher row lengths range29–33; tableau generally31 slots, one32 and two leading spaces. Script counts: LEFT869 nonspace characters including4 question marks; RIGHT867 nonspace letters; total1736 apertures=1732 letters+4 question marks. The UI label1735 letters+4 question marks does not match its arrays. K4 is97 characters, begins row 24,index 27 (zero-based), then rows 25–27.

Default justify: each row independently spreads n character slots across0.954L; no measured x centers. Fixed pitch: denominator31 irrespective of row length; the final character in the 33-character row has center outside the plate, so even v2's optional pitch mode is not a measured complete layout. No built-in raised Y/A/R offsets, inter-quarter seam gap, letter-specific width, glyph contour, bridge/stencil details or manufacturing irregularity.

Measured mode: starts with empty measured={}. User may paste face,row,i,u,v, with u normalized along the arc, v normalized bottom-to-top. Unlisted letters revert to justified layout. This is a center override, not measured aperture contours or metric survey. It does not import scale, normals, width/height, uncertainty, measured source IDs or camera geometry. Validation checks face and numeric u/v only, not finite values, row/index validity or v within plate. Export includes the calculated solar direction, camera and parameter settings, but does not include the measured coordinate dictionary, so results using imported positions are not reproducible from exported settings alone.

Font: bold Arial Black, fallback Helvetica Neue/Arial/sans-serif. Independently inspected dnq,kry,pto rubbings and LOC image show serifed letters. These are visibly different aperture outlines. A 4096×2048 texture is mapped onto L×H=2.85×2.75 m. Thus physical x/y scale ratio=L/(2H)=0.5181818; an ordinary font is compressed horizontally to roughly52% of its correct aspect. Font size sets em size, not actual capital ink height. Do not preserve this texture-coordinate scheme. A separate trace bug divides horizontal sample displacement by πR instead of L; defaults make physical offsets0.6256436 of requested offsets. The traced glyph layer and rendered cutout have different distortions.

## Objects and renderer versus analytic geometry

Tree: render is20-sided cylinder tapering radius0.33 m bottom to0.30 m top. Analytic intersection uses constant0.30 m, no caps. The source imagery shows irregular segmented petrified wood, not this cylinder. No additional supports are modeled.

Bubbling pool:48-segment disk displayed at y=+0.004 m, not analytic y=-0.30 m. Calm pool:64-segment disk displayed at+0.005 m, not analytic y=-0.05 m. Ground is90×90 m plane with no openings. Analytic ray logic recognizes pool disks at paving height, then moves to water elevation without rechecking shifted coordinates against pool boundaries; no vertical rim/walls. Its separate reflected-letter visibility check also ignores whether a letter is illuminated and tests the water-to-letter segment but not obstacles on the eye-to-water segment. The calm pool is an ideal planar mirror; bubbling pool merely terminates rays. Eye preset is(calmX,1.6,calmZ+calmR+0.3), acknowledged placeholder. Displaying the pools or hiding them only changes visibility, not analytic intersections.

No rock geometry, white receiving rock, granite benches, building walls/windows, actual live courtyard tree, terrain/paving elevation, or true pool boundaries. Plate thickness is0 in both rendering and rays; footer acknowledges competing0.25–0.5 in accounts. Sheldon's6.35 mm and1991 memo/WIRED 12.7 mm are conflicting reported alternatives, not a validated uniform random interval.

Rendering has alpha-shaped cutouts and GPU shadows. Analytic ray functions hitFace/sunReaches/traceOut treat both sheets as opaque circular surfaces at every intersection: they never evaluate the glyph alpha mask. Thus rays through receiving/opposite cut letters are incorrectly stopped; point-at-letter classification is not exact aperture membership. Five samples per glyph (center,left,right,down,up) cannot classify full aperture illumination. nearestCell uses an arbitrary normalized3×horizontal distance weight and vertical-only check for onLetter, not a physical outline. The source is not a full cutout-aware optical model despite having occlusion.

GPU shadow map4096² covers18×18 m; ground letter overlay4096² covers16×16 m. These are rendering resources, not physical dimensions. Infinite analytical ground differs from finite display, and distant pond is outside small overlay/shadow areas.

## Provenance audit

1. WIRED,20 April 2009: https://www.wired.com/2009/04/ff-kryptos/ explicitly reports9ft11 in main sculpture,11 ft wood column, half-inch copper. It supports reported values, not Scott's2.75 m sheet height or exact R/L. It is a journalistic description, not a dimensioned drawing.
2. SPYSCAPE interview with actual cutter David Sheldon: https://spyscape.com/article/kryptos-the-cryptic-cia-mystery-is-bigger-than-you-think reports3 in-high letters and0.25 in plate. Strong maker recollection, but approximate late account, not an as-built survey. The artifact's glyph=.87 published tag overstates what this source publishes.
3. Dunin's firsthand 2002 notes: https://elonka.com/kryptos/ establish8.5 × 11 in rubbing paper, roughNW direction of the reference view, raised-letter anomalies, direct and window-reflected letter light. They do not state3.45 in pitch,140° heading, radii or sheet sizes. The rubbing images have near11:8.5 aspect (most649×500 px), making retrospective scaling plausible, but no recorded page-edge picks, aperture centers, crop guarantee or measurement error accompanies Scott's number. Treat3.45 in as Scott's unverified image-derived estimate, not Dunin's measurement.
4. Rubbings: https://www.elonka.com/kryptos/rubbings/images1.html . Visually inspected full dnq,kry,pto; no claim of precise measurement made here. Preserve original file identity/crop and extract multiple consistent intervals before using them as metric evidence.
5. The eight-foot tree-hole story exists in attributed Dunin excerpts https://www.geocities.ws/pf008/kryptos/kquotes.htm and corroborating compiled notes https://scirealm.org/KryptosHints.html . It concerns a pre-existing hole, not measured finished water diameter or center. Those excerpts do not justify bubX/bubZ/bubW. Do not imply the numerical coordinates were quoted by Sanborn.
6. Aerial source https://elonka.com/kryptos/KryptosAerial.html documents approximate site relationships. Scott's precise128°/31 m/6×2.5 m claim has no identified aerial frame, acquisition date, scale, control points or measurement worksheet. It remains unverified inference.
7. Dunin's https://elonka.com/kryptos/wishlist.html explicitly requests measurements for all four copper plates and contextual photographs. This is evidence the public visual references are not themselves a complete measured reconstruction; it is not permission to contact anyone.

## Calibration photographs and failed fit

Gillogly reference https://www.voynich.net/Kryptos/full/cipherback.jpg downloaded and inspected,768×1024 px. Its current JPEG has no EXIF timestamp/camera data (only generic image-editor comment), and https://www.voynich.net/Kryptos/ has no14:23 annotation. Dunin's main page corroborates the1999-10-27 photo outing, but the particular14:23 camera time remains unverified from the linked public files. Do not call it a reliable solar calibration timestamp.

The page says its 7-letter camera fit tends toward infinite camera distance and no realistic camera fits the current proportions, and the L source field mentions a preferred L/H≈0.88. No 7 labeled points, source-pixel coordinates, lens model/distortion, fitted parameters, objective function, residuals, uncertainty, fitting code or held-out points are supplied. It is an author-reported failed fit, not a reproduced result. Failure alone cannot uniquely diagnose plate proportions: incorrect feature correspondence, font centers, surface family, crop/intrinsics and optimization degeneracy can also fail. Do not silently adopt2.4 m as measured corrected L.

The current artifact has only manual image loading as a translucent overlay and camera position/FOV controls; no photo is preloaded, no optimizer included. It says nothing has been matched to a photograph. The shadow-band tree identification and columns0–4 obscuration are qualitative interpretations, not calibration constraints with residuals.

Highsmith/LOC source https://www.loc.gov/pictures/item/2011631531/ and image https://cdn.loc.gov/service/pnp/highsm/13300/13337v.jpg inspected. Catalog dates it broadly [between1980and2006], from4 × 5 in-or-smaller film transparency; camera position/lens/time unavailable. It warns the digital representation may differ from film. Original TIFFs41.5 MB/83 MB are linked. The record and image are strong shape/layout references, NOT a known-time sunlight validation photo. It shows curved sheets and serif/stencil details, with major perspective and partially clipped extent. The photograph was inspected at its 809 × 1024-pixel service version, not the full original TIFF.

GSA reference https://www.elonka.com/kryptos/pics/images/GSA-Kryptos.jpg is an undated visual reference in the artifact, not a calibrated camera. No pixel measurements sourced to it are provided.

## Robustness test is narrower than its label

Runs 200 independent uniform perturbations of H,y0,Rc,Rt,mTop,mBot,mSide,glyph,treeX,treeZ,treeR,treeH,heading and clock minutes, plus random justify/pitch layout (unless measured mode is selected, in which case it remains measured). Despite UI saying every dimension, it NEVER varies L, any pool coordinate/size/elevation, imported center values, thickness, font outlines, surface model, missing objects, latitude/longitude or lens. There is no seeded RNG. Clock perturbation has no effect in manual-sun mode. A 90% stability rate is conditional on this arbitrary incomplete ensemble, not a calibrated probability that reality agrees. In particular it omits L, the very parameter flagged by its failed photo fit.

## Implementation recommendation

- Preserve named reported-source alternatives rather than averaging disagreeing descriptions into false precision. Keep sheet height, arc length, chord width, assembly height, and site envelope distinct.
- Use a visibly approximate prior model until photogrammetry succeeds; do not claim a physical reconstruction merely because defaults have citations.
- Use the maker's reported letter height as a reported scenario; measure actual contours/centers against photographs and rubbings. Correct font family, aspect ratio, cap-height versus em definition, stencil bridges, row offsets and four-sheet seams.
- Parameterize each half's shape with measurable arc/chord/sagitta and independent physical units; do not force exact semicircles or silently equate8 ft sheet width with8 ft chord.
- Make measured input first-class with source IDs, pixel picks, scale assumption, metric coordinate convention, per-point uncertainty, contours and full export.
- Require physical photo fitting with non-K4 features, camera intrinsics/crop constraints and independent withheld features/view before labeling calibrated. Missing camera timestamps prevent strict solar-photo validation even when shape fitting is possible.
- Model receiver rocks/windows/live trees, actual pool perimeter/rims/elevation, and thickness when claiming those optical paths. Distinguish illustrative absent context from validated clear rays.
- Replace incomplete numerical robustness with sensitivity scenarios including alternative source dimensions and model family; retain provenance and seeded reproducibility.

## Additional source conflicts, not new defaults

The 18 November 1991 George C. Dalmas installation description, NSA-released document 3, PDF page 4, gives an 8 ft × 8 ft tableau half and half-inch copper. The cipher-side size's first numeral is degraded and must not be silently resolved from conflicting OCR. Neither its width definition (arc, chord or stock blank) nor its dimensional measurement method is supplied. Its 12-foot tree description differs from WIRED's 11-foot account. This is an installed-work description, not an as-built fabrication drawing: https://www.nsa.gov/portals/75/documents/news-features/declassified-documents/cia-kryptos-sculpture/doc_3.pdf .

Sanborn's own public-works page describes the courtyard installation with a 12 ft × 20 ft × 10 ft overall envelope. It does not establish sheet height, unfolded width or circular radius: https://jimsanborn.net/content.html#PUBLIC_SPACES . Do not substitute these overall assembly/site dimensions for an individual copper sheet.

Together, these sources justify separate named reconstruction scenarios and a search for dimensional documentation, not a single supposedly measured default. In particular, 6.35 mm and 12.7 mm plate thickness are competing accounts, not endpoints of a measured probability distribution.

## Application source references

References below are line numbers in the frozen application JavaScript identified by SHA-256 above, with the initial blank line numbered 1. They identify small functional regions without republishing the full source. HTML-control defaults are separately recorded because they precede that script.

| Finding | Exact application reference |
|---|---|
| Transcripts, row count, coordinates | LEFT/RIGHT lines 4–6 |
| Published/estimated/unknown labels, all parameters | SRC and DIMS lines 8–40 |
| Empty measured input, layout and K4 indexing | apertures lines 51–71 |
| Arc and world-to-surface definition | arcs/facePoint/faceUV lines 74–91 |
| Opaque analytic sheet/tree intersection | hitFace/hitCyl lines 93–109 |
| Pools at ground entry, lower water level and reflection | traceOut lines 113–127 |
| Solar occlusion | sunReaches lines 129–132 |
| Solar formula, historical date-only DST | lines 135–156 |
| World axis and heading transformation | lines 159–165 |
| Five-point aperture sampling and πR error | traceAll lines 168–185, especially 178 |
| Non-outline receiving-cell classification | nearestCell lines 189–195 |
| Camera and font family | lines 204–207 |
| 4096×2048 font texture and physical aspect distortion | plateTexture lines 209–217 |
| Zero-thickness mesh, warped arc and alpha cutouts | buildSculpture lines 219–234 |
| 90 m ground and pool display heights | lines 235–248 |
| Decal dimensions and shadow-map camera | lines 249–258 |
| Projected font constructed from sample derivatives | drawDecal lines 261–277 |
| Reflected-letter eye geometry and occlusion limitations | reflectionCheck lines 280–293 |
| Exported settings and camera | settings lines 297–303 |
| Claimed camera time and heading note | lines 324–325 |
| Reflected-eye placeholder | lines 341–345 |
| Uncertainty dimensions, sample distribution and comparison | lines 347–367 |
| Export content and explicit validation failure | lines 368–374 |
| Measured import validation and missing export data | lines 377–383 together with 368–374 |
| Manual photo overlay and camera controls | lines 384–388 |
| Camera presets and startup | lines 392–403 |

Current HTML defaults: date 1999-10-27; local hour 14.3833 (14:23 displayed); time zone auto US Eastern (EDT on that date); heading 140°; bulge +1; layout justify; trace K4 only; manual sun off (unused slider defaults azimuth 180°, elevation 35°); shadows, decal and pools all enabled. Initial camera local position (6, 4, 9) m, target (0, 1.4, 0) m; vertical FOV 45°. Camera presets and observer positions are visualization choices, not measured photograph poses.

## What is still unknown

For a defensible physical reconstruction we still need: individual four-sheet dimensions and seams; precise lower/top boundaries and ground gap; the sheet surfaces' measured 3D shape; thickness resolved or explicitly scenario-selected; physical aperture contours and center coordinates including offsets; surveyed site heading; tree/support and rock geometry; receiver rock position/normal; pool footprint and water elevations; reflecting-window position/normal; camera intrinsics, crop and stable features for at least two independent views. Exact timestamp and time-zone verification are additional requirements for a timed shadow test, not something shape fitting can infer automatically.

No precise new pitch or cap-height measurement is asserted from the rubbing images in this audit. Their nominal paper size is useful evidence, but calibration must record actual paper edges, crop/scaling assumptions and repeated letter-center intervals before a defensible metric estimate exists.
