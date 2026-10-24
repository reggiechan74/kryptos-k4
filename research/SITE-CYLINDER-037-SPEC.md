# SITE-CYLINDER-037 — exact vertical-tableau default validation and finite stability

24 October 2026 UTC. Local-only follow-through after e9307503418fb4f60d6f8f4acf296b7da33aeaa0. Preserve 036, do not edit/archive/deploy Site source or push GitHub. No actual K4 ciphertext/crib evaluation or external paid validation. Source code/contract/default key and its existing tests were read before freezing; reproducing that known default is validation, not a blind discovery.

## Exact source model and independent replay

Read-only source: task-3/kryptos-light/candidate/cylindrical-study/core.mjs, its PARAMETER_CONTRACT.md and imported candidate/transcript.mjs. Pin current source hashes/commit and validate no change during snapshot. The inspected import graph contains pure math and literal transcript exports only; a separate Node harness may call this trusted local core read-only and write factual numeric fixtures to /tmp, not copy its source into this repository. Independently implement closest-approach cylinder intersection and angle reflection in Python; compare all source statuses, cells, letters and coordinates to1e-9 absolute tolerance.

Source y is up, cylinder x²+z²=R² with side height3, eye (0,1.5,D), reticle planez2. For indexi0..96, n=i+27,row=floor(n/31),column=n mod31, Q=((column−15)w/31,1.5+(1.5−row).075,2). First positive lateral circle intersection is required to lie within source height; do NOT silently replace this side-only contract with 036's closed cylinder or skip a nearer out-of-height intersection. Reflected ray intersects vertical planez=L behind the eye. Pitch.25, envelope33×28, left=shiftX−4.125, top=5+shiftY; floor cells, per-row centering floor((33−literalRowLength)/2). Literal blank/outside or margin≤.01cell is invalid; no invented letters/clamps/wrapping. Preserve source boundary threshold rather than import 036's .02. Key null if any of97 invalid. Optional card AABB is source-defined; no new obstacle is fitted.

Defaults: radius.8,eyeDistance4,tableauDistance6,shiftX.037,shiftY.043,reticleWidth.225,obstructionfalse. Source selected/view/screenYaw change inspection/display only and must not change key. Source ranges, unknown per-letter override rejection and relative-distance validation stay explicit. Synthetic Site message/alphabet addition are replayed; no new inverse key search is needed for this contract validation.

Fixtures: source default97, obstructiontrue, reticleWidth.9, sample20 boundary via source formula shiftX=P20.x+4.125−16*.25, and padded blank target sample20 displaycell(row1,col0) using shiftX=P20.x+4.125−.5*.25,shiftY=P20.y+1.5*.25−5. Invalid fixtures must null keys, never drop bad samples. Also compare low-level miss, tangent and outside-height rays plus NaN/infinity/range/unknown-field rejection. Inspect each fixture's validity instead of assuming all source test names establish full coverage.

## Finite nearby domain, no per-point adjustment

Fixed729 states, Cartesian product:
- radius {.796,.8,.804}; eyeDistance {3.99,4,4.01}; tableauDistance {5.99,6,6.01};
- shiftX {.032,.037,.042}; shiftY {.038,.043,.048}; reticleWidth {.22275,.225,.22725}.

All other optical constants fixed; obstructionfalse. Every state is validated against source ranges. Save all97 statuses, cell indices, margins and key/null, not only best cases. Compare with default's cell path, key and admission decisions separately. Default key unchanged under some states is not proof the entire neighborhood is stable.

Select baseline plus up to5 complete states having the SAME default cell path and up to5 complete states having a DIFFERENT cell path, by descending minimum margin rounded to1e-9 then lexicographic six-parameter tuple rounded to1e-12. Baseline not duplicated. No utility/cell-diversity cutoff, English ranking or target-key adjustment. Empty strata stay empty. This small deterministic extension is preregistered, not tuned after defaults fail. Unselected nominal states retain an explicit robustness-untested status. No expanding neighborhood or tolerances after results.

## Comparable assembly and pupil panels

Two physical scales, not surveyed dimensions: U100=100mm per Site unit (default radius80mm,tableau825×700mm); R250=312.5mm per unit (default radius250mm,tableau2578.125×2187.5mm). Same fixed units apply across each nearby domain. Report size and uncertainty sensitivity, not a claim either apparatus was built.

At each selected state/scale, six primary parameter tolerances: radius±.5%,eyeDistance±1mm,tableauDistance±1mm,shiftX/Y±.5mm,reticleWidth±1%. All64 primary corners and64 fixed-seed uniform interior states (seed370024; deterministic selection order) are tested. The geometry constants remain source defaults.

Separate one-at-a-time out-of-contract assembly nuisances: eye lateral/vertical±1mm, reticle vertical centre±.5mm, reticle planeZ±.5mm, reticle vertical pitch±1%, and printed-board roll/yaw/pitch±.1degree. Sixteen nuisance configurations. These are perturbations, not additional fitted key parameters or source UI claims. For board rotations use centre (shiftX,1.5+shiftY,L), rigid orthonormal right/up axes and their normal; intersect that actual plane and use its local coordinates. Zero tilt must reproduce source mapping. Keep side-height/obstruction assumptions explicit. No cylinder-axis tilt, support/head occlusion or arbitrary deformations added.

Thus144 assembly cases per selected state/scale. Record source-floor cell changes separately from admission/boundary loss and letter/key changes. A strong pass requires identical97cell identities AND admission decisions for every configuration; label-only agreement is weaker. All finite-panel passes remain finite, not continuous interval certificates or probabilistic fabrication confidence.

Pupil diagnostic: physical reticle points Q remain fixed; eye origins move on camera x/y rim (8angles plus centre) for physical radii.05mm and1.5mm. Trace from E' toward same Q, not angularly translating the original ray. Report every per-cell margin/admission and label change. This is parallax/ray-bundle sensitivity, not a full eye/camera image, focus, diffraction, blur or perceptual-resolution model. A tiny aperture cannot be called readable from geometric rays alone.

## Controls, resources and stopping

Independent Node/Python default+invalid replay, analytic normal-incidence sample20, reflection/reciprocity, zero-nuisance equality, explicit board-coordinate tilt invariants, selected-short default states and synthetic97-letter forward/inverse replay. Full cross-version replay must preserve discrete states and float tolerance; timestamps/RSS remain separate. No K4 search or language scores, so no fabricated cryptanalytic p-value. Geometric ranking, physical tolerances and sample selection are fixed; all negative/counterexample records retained.

Snapshot/replay/neighborhood120seconds/512MiB; stability120seconds/512MiB; saved compressed artifacts64MiB. Check completion and preserve unresolved coverage at caps; never count timeout as exclusion. UTC run/record/export/commit times distinct. Conclude what the exact default and tested nearby states establish, where stability remains unresolved and which bench/readability/illumination/occlusion inputs a hand-operated replica needs. Do not extrapolate to the horizontal 036 apparatus, actual copper or all possible optical ciphers.
