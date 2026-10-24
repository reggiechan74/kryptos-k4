# Exact Site cylinder: nominal default verified, manual robustness not established

24 October 2026 UTC. **The Site’s actual vertical-tableau default is reproduced independently: all 97 samples, its key and synthetic roundtrip agree.** This closes the numerical-model mismatch left by the separate horizontal-table study036. The default and ten nearby selected states nevertheless fail the full declared assembly panels at both physical scales. Some tiny-aperture cases pass; none passes the human-scale pupil diagnostic. These are finite geometric sensitivity results, not proof a mirror apparatus is impossible or unreadable to a person.

[Preregistered protocol](SITE-CYLINDER-037-SPEC.md), [compact summary](../results/SITE-CYLINDER-037-SUMMARY.json), [all original results](../results/SITE-CYLINDER-037-ORIGINAL.json.gz), [every default margin](../results/SITE-CYLINDER-037-DEFAULT-MARGINS.csv), [full cross-version comparison](../results/SITE-CYLINDER-037-PY312-COMPARISON.json). No actual K4 comparison, source-derived K4 geometry or external checker submission occurred. This task did not edit/deploy Site files, archive the owner’s program source or push GitHub.

## Exact apparatus and source pin

The inspected local Site source is commit `5b7e88365f174106ef7a7f290a0bdcc671014f01`, schema `ideal-cylinder-reticle/1`. Its pure math module and literal transcript import were inspected before a read-only Node snapshot. Source hashes were checked unchanged during execution. The [numeric snapshot](../results/SITE-CYLINDER-037-SOURCE-SNAPSHOT.json.gz) contains factual generated fixtures, public rows and ray outputs, not copied Site JavaScript, UI source or a source ZIP. [Snapshot harness](../experiments/snapshot_site_cylinder037.mjs).

Site y is up. The mirror side satisfies x²+z²=radius², y in (0,3). Eye=(0,1.5,eyeDistance); the physical reticle lies at z=2. The printed tableau is a **vertical plane behind the eye**, z=tableauDistance, with square pitch 0.25 and rows centred in a 33-column envelope. The first positive lateral hit must lie within source height; no closed-cylinder caps were silently imported from036. The boundary guard is the Site’s 0.01 pitch, not 036’s 0.02.

Eye distance is an exported/API parameter currently fixed to4 in the UI; its nearby variations test physical placement sensitivity, not a new UI control.

The independent Python model uses circle closest approach and complex reflection, rather than the source quadratic/vector expression. Source default, obstruction, wide-reticle, explicit boundary and padded-blank fixtures agree:

| Fixture | Valid samples | Full key |
| --- | ---: | --- |
| Default | 97 | Present |
| Hypothetical opaque card | 0 | Null |
| Reticle width0.9 | 27 | Null |
| Boundary fixture | 87 | Null |
| Padded blank fixture | 49 | Null |

All 485 fixture samples and 70,713 nearby-state samples agree with the inspected Site core. Maximum compared coordinate difference is 7.32e−13 model units, below1e−9. Low-level miss/tangent/height, source validation/rejection, normal-incidence sample 20 and synthetic addition/inverse checks also pass. Numeric source validation is not a full browser/UI or published Site test-suite claim.

The [earlier horizontal-table model](CURVED-SAMPLER-036-FINDINGS.md) remains immutable and separate: it has different axes, reticle, table plane, registration, surface/end-cap assumptions and thresholds. Its results are neither substituted here nor retrospectively relabelled as Site validation. The actual curved copper screen is a third, evidence-gated branch; ideal specular reflection is not a measured property of its perforated surface.

## What the default margin means

Defaults are radius 0.8, eye distance 4, tableau distance 6, shiftX 0.037, shiftY 0.043 and reticle width 0.225. The default samples 79 distinct cells. Its smallest fractional distance to a cell edge is **0.01784193946678414 pitch**, at reticle samples **25,56,87**. All three occupy reticle column 20 in the three full rows. This is valid under the 0.01 guard but not a large safety reserve.

| Declared scale | Mirror radius | Printed cell pitch | Tableau envelope | Default closest edge | Reserve above 0.01 guard |
| --- | ---: | ---: | --- | ---: | ---: |
| U100: 100 mm per unit | 80mm | 25mm | 825×700mm | 0.44605mm | 0.19605mm |
| R250: 312.5 mm per unit | 250mm | 78.125mm | 2578.125×2187.5mm | 1.39390mm | 0.61265mm |

These are illustrative scaling arithmetic, not measured apparatus dimensions. The larger case requires a metre-scale mirror/board assembly, not a compact tabletop assumption. The CSV preserves every per-cell margin, key letter, reticle location and display-cell coordinate; minima are not substituted for the rest of the data. A ray picks a **cell label**, not necessarily an ink stroke at that exact point. A replica needs explicit visible cell boundaries/readout rules and legible mirrored glyphs; this model does not supply glyph recognition.

## All729 nearby states, without retuning after the result

A fixed3⁶ neighborhood perturbs the six global optical parameters, with no per-letter positions, plaintext ranking or desired-key fit. Every state was independently compared to the pinned Site core before stability evaluation:

- 441 states retain all 97 valid samples;288 do not.
- 186 retain the default cell path, admission decisions and key.
- The 441 complete states contain 11 distinct key strings.
- The frozen selection takes the baseline, five best-margin same-cell-path cases and five best-margin different-cell-path cases: 11 unique states. The other 430 complete states were **not** given the full stability panels.

The best selected registration preserving the default key has minimum margin 0.04505 pitch, about 2.53× the default. The best selected different-path case reaches 0.04737 but changes the key. Those improvements remain visible; we did not edit the Site default. A source-selected intended key cannot be replaced simply because another geometry has a better margin.

The saved one-axis cases show why a global “looks unchanged” judgment is insufficient. At radius 0.804 the default has six changed cell assignments and six admission changes; at reticle width 0.22275 six cell assignments change despite all 97 remaining valid. At shiftX 0.042 three cell/admission assignments change. Conversely several negative/positive one-axis perturbations preserve the default key. These are deterministic cases, not failure probabilities or measurements of construction error.

## Assembly and pupil results

Each selected state is evaluated at both scales: 64 primary-parameter corners, 64 fixed-seed interior states and 16 one-at-a-time nuisance cases, or 144 assembly cases per state/scale. Primary tolerances are radius±0.5%, eye/tableau distance±1mm, registration±0.5mm and reticle width±1%. Nuisances include eye/reticle shifts, reticle vertical pitch and printed-board roll/yaw/pitch. These are explicit out-of-contract physical uncertainties, not added hidden key parameters or Source UI controls.

| Test across 11 selected states | U100 passes | R250 passes |
| --- | ---: | ---: |
| Entire assembly panel, exact cells/admission | 0/11 | 0/11 |
| Entire assembly panel, same valid key | 0/11 | 0/11 |
| Tiny aperture radius 0.05 mm, nine-point bundle | 10/11 | 11/11 |
| Human-scale pupil radius 1.5 mm, nine-point bundle | 0/11 | 0/11 |

The **default itself** fails the tiny-aperture test at U100, passes it at R250, and fails the human-scale test at both scales. Thus the correct conclusion includes a size/aperture tradeoff; it is not “no optical sampling can work.” All 3,564 configurations and their97 per-cell margins/statuses are retained. Floor-cell changes, admission/boundary losses and valid-letter changes are separate fields. A boundary guard failure is not automatically a changed physical letter.

Pupil tests move the ray origin while holding each physical reticle point fixed. This diagnoses parallax/bundle sensitivity; it is **not** a complete eye/camera image, focus, diffraction, accommodation or perception model. A 0.1 mm-diameter aperture passing a ray test is not automatically readable. Finite rim samples and corners are not continuous interval certificates. Neither the chosen tolerances nor the neighborhood are probabilistic distributions, so no confidence/p-value is asserted.

## What a hand-operated replica would need

A manual process could be look/copy/align, with our equations used only for analysis. The current visualization does not establish that a person can repeat its key. A bench test needs:

1. A measured cylinder radius/figure, stable mounts and a fixed physical reticle/board scale, with registration checked at the sensitive samples rather than by overall appearance.
2. An explicit eye/peep or camera geometry that addresses parallax, focus, pupil size and legibility. Higher precision and larger size may help particular subtests, but no tested selected case passes the complete declared assembly panel.
3. Visible cell-selection/readout rules and actual printed glyphs. The source cell-label rule does not model partial letters or human recognition near cell borders.
4. Unobstructed real paths: supports, observer head/body, illumination and real mirror roughness are absent from the point-eye model. The board is behind the eye; those paths require a real occlusion check, not an invented human-shaped blocker or a claim they must be clear.
5. A frozen physical alignment and independent repeat/held-out observations before any historical or K4 interpretation. No source currently chooses this geometry, reticle or sampled key as Sanborn’s method.

No actual replica, narrower post-hoc error budget, larger neighborhood or K4 parameter search was added. Lower sensitivity under a different untested precision is not ruled out; the exact stated default and finite panels are what this report establishes.

## Reproducibility and honest resource scope

Original computation receipt: 2026-10-24T15:28:59.235487+00:00–15:29:03.878526+00:00. The original 427,835,392-byte RSS was recorded before final joined JSON serialization, so it does not certify the original whole-process write peak. The unchanged computation was replayed on Python 3.12 with an IO-only streaming adapter and `/usr/bin/time -l`: full process 4.65 seconds, maximum 356,155,392 bytes, below 512 MiB. [Resource receipt](../results/SITE-CYLINDER-037-RESOURCE-REPLAY.json). No data were truncated; all original/replay values remain in lossless compressed archives.

The complete cross-version comparison checks every discrete value exactly and all 494,004 floats within1e−9; maximum float difference is 1.81e−12. Timing/RSS fields are kept separate. A sequential float stream avoids simultaneously holding both large decoded result trees. It also tests expected-rejection file cleanup. [Comparator](../experiments/compare_site_cylinder037.py), [full replay](../results/SITE-CYLINDER-037-PY312-REPLAY.json.gz).

```sh
python3 experiments/run_site_cylinder_validation.py --snapshot results/SITE-CYLINDER-037-SOURCE-SNAPSHOT.json.gz --output /tmp/site037.json
python3 experiments/replay_site_cylinder037_stream.py --snapshot results/SITE-CYLINDER-037-SOURCE-SNAPSHOT.json.gz --output /tmp/site037-stream.json
python3 experiments/compare_site_cylinder037.py --original /tmp/site037.json --replay /tmp/site037-stream.json --output /tmp/site037-compare.json --float-work /tmp/site037-floats.bin
```

The numeric source snapshot is enough to reproduce the research comparison without access to the live Site checkout. Re-snapshotting original Site JavaScript requires its separately inspected pinned files; no Site source package is bundled here. Canonical K4 text, previous 036 artifacts and unrelated files are unchanged. This local validation closes the requested cross-model loop while leaving physical manual stability, source-selected K4 geometry and repository publication pending their actual prerequisites.

Final aggregate validation: **665 tests pass on Python 3.9 and 3.12**. [Separate UTC receipt and full logs](../results/SITE-CYLINDER-037-VALIDATION.json). Prior036 and canonical K4 are unchanged;210 unrelated files preserved. No Site edit/deployment, owner-source archive or GitHub push by this task.
