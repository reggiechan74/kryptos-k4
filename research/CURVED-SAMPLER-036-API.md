# Ideal mirror sampler: Site/research contract

Version 1, 24 October 2026 UTC. This is an invented synthetic tabletop model. Actual copper-screen curvature, transmission and reflectance remain separate. No Site files are edited here.

The eight JSON parameters are `D,H,s,aim_deg,tx,ty,rotation_deg,pitch`. All lengths use cylinder radius 1; side height is 2, table `z=0`, eye `(0,-D,H)`. Aim is downward from horizontal, rotations are degrees. Fixed camera basis and table axes are defined in [the immutable protocol](CURVED-SAMPLER-036-SPEC.md). Positive table local Y points toward the top of the printed tableau. Reflected table cell coordinates are `col=15+localX/pitch`, `row=13.5-localY/pitch`. Select nearest cells, with no wrapping or blank repair. Margin at most 0.02 cell is invalid.

`trace(params,u,v,eye_offset=(0,0,0),fixed_reticle=False)` returns the first-hit/reflection/ground result. Side normal is outward; caps, rims, misses, grazing and upward/parallel ground rays are rejected. `sample(params,tableau_rows,...)` returns all 97 point records, `complete`, `key` (null unless all points valid), `distinct_cells`, `distinct_letters` and `minimum_margin`. A nominal key is a centre-cell identity sequence, not a simulation of recognizable mirrored glyphs or measured apertures.

`data/curved-sampler-v1.json` supplies all fixed reticle coordinates and five deterministic ray fixtures. The reticle uses the 4/31/31/31 occupied K4 grid as a public layout only. Its coordinate handedness is fixed; do not apply an undocumented extra reversal. The printed tableau's literal ragged rows and blanks are preserved.

[Post-outcome Site fixtures](../results/CURVED-SAMPLER-036-SITE-FIXTURES.json) contain a complete nominal 97-key case, its first assembly failure, a tiny-pupil failure, and a synthetic plaintext/ciphertext recovery control. Expected coordinates use 1e-9 absolute tolerance. These fixtures are synthetic and selected by the frozen geometric ranking, not by K4 cribs. The `generated_at_utc` is an export time, not the original run time.

For the pupil fixture, retain the nominal reticle plane point `Q=E+0.5(f+s*u*right+s*v*up)` and trace from the offset pupil point toward that same Q. Merely translating the eye while retaining the old angular ray is a different test. This is a parallax/bundle diagnostic, not a full accommodation, diffraction or retinal-resolution model.

The fixed finite study found 54 complete nominal poses, four meeting its explicit utility criterion. None of those four passed the declared assembly or either pupil benchmark. Display both nominal success and perturbation failure. Do not label this a stable physical device, measured monument mechanism, recovered K4 key or proof of optical impossibility. Continuous geometry outside the tested finite panel remains unassessed.

The optional synthetic layer uses modular addition in `KRYPTOSABCDEFGHIJLMNQUVWXZ`, inverse subtraction. The fixtures' plaintext and ciphertext are synthetic; no actual K4 was scored. Supplied-panel recovery is limited to four key classes, not continuous parameter inference. No chart, UI clamp or invalid sample may fabricate a key letter.
