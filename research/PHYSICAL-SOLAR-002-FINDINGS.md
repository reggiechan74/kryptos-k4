# Item 2 — shadows, astronomy and navigation

**Conditional constraints verified; no K4 decoder or intended date identified.** These calculations extend the existing solar-bound note and separate direct sunlight, its opposite ground shadow and a possible pool lamp. Surveyed orientation and source/aperture/receiver geometry remain missing. Independent source research and arithmetic are now integrated below. No measured optical key or authenticated observation time was recovered.

## What was actually calculated

[Protocol](PHYSICAL-SOLAR-002-SPEC.md) committed at `b2cc1dffdbb71b7a11c38f8041d220f3fce82932`; [implementation](../experiments/physical_solar_002.py) committed before original execution. Original run: **2026-10-24T00:17:28.772639+00:00 → 2026-10-24T00:17:29.483736+00:00**. The [complete output](../results/physical-solar-002/20261024T001728Z-f2895d4425214b2bbed15c832235acf2/physical-checks.json) retains all 96 scenario envelopes, 39 fixed calendar samples and 125 ray-height cases; its adjacent manifest pins hashes. No ciphertext, plaintext fit, celestial-body search or numerical bearing fit is used.

The old exact 67.5°/247.5° bounds are explicitly prior coverage. New work adds sector/frame/horizon sensitivity, independent numerical consistency checks and the source-height necessary condition. Scenario records are correlated sensitivity cases, not independent cryptanalytic hypotheses.

## Direct Sun and ground shadow mean different bearings

Azimuth here is clockwise from **true north**, pointing from the observer toward the Sun. A direct ray travels the other way. On a lower horizontal receiver, its shadow/light-image displacement is opposite the Sun azimuth; a WSW Sun can yield an ENE displacement. Reflection or a wall receiver changes the geometry.

At representative latitude 38.951°N, solar declination constrained to ±23.5° and geometric center altitude at least zero:

| True source bearing | Reachable center altitude | Meaning/limit |
| --- | --- | --- |
| 56.25° | none | Northern edge of the declared ENE sector is beyond this solar envelope |
| 67.5° | 0°–9.647° | Exact ENE sunlight requires declination at least +17.314° |
| 78.75° | 0°–24.499° | Sector interpretation materially differs from the exact center |
| 236.25° | 2.984°–66.016° | One WSW-sector edge, with its own lower bound |
| 247.5° | 0°–60.313° | Exact WSW Sun, corresponding to an ENE ground displacement |
| 258.75° | 0°–51.635° | Other WSW-sector edge |

These are necessary angular envelopes, not visible unblocked trajectories, dates, times or measurements. Full results include the legacy ±23.44° cap, three illustrative latitudes and a −0.833° center allowance. The latitude box is not a confidence interval. The allowance represents a conventional upper-limb/refraction sensitivity, not measured skyline, weather or a valid projection when the center is below the horizon.

A purely hypothetical magnetic ENE center plus archived 1989 regional declination −9.628° gives true 57.872°. That direction has **no** reachable altitude even with the −0.833° allowance under this cap; its hypothetical opposite 237.872° does. This does not calibrate the static carved needle, engraved N or local lodestone. Magnetic, engraved and true-north frames cannot be silently substituted.

The older model pair azimuth 72°, altitude 40° requires declination **36.028°**, outside the declared solar envelope **if** its azimuth denotes true Sun direction at Langley. Its rendering heading is uncalibrated, so this is not a rejection of every interpretation of that rendering.

## Fixed historical dates do not identify an intended observation

USNO approximate declinations at noon UTC are −2.837° on 1969-09-30, −15.066° on 1990-11-03 and −15.683° on 1990-11-05. The two November dates preserve the CIA account versus typed dedication-header discrepancy; neither is selected for a favorable result. All three are far from the positive declination needed for above-horizon exact ENE Sun at this latitude. They do not rule out a WSW Sun/ENE shadow, reflection, artificial illumination or another mechanism. The receipt records endpoints and noon, not a continuously surveyed event; its November 1988 inventory is 30 representative noons, not an exact selection-day or time claim.

For a fixed location, azimuth and altitude constrain declination through

`sin δ = sin φ sin h + cos φ cos h cos A`.

They do not uniquely determine a year or civil time. Away from solstitial extrema, the same solar declination ordinarily occurs on two annual branches and in successive years. Longitude, equation of time, time zone/DST and actual horizon enter a timed observation. Unknown object/date, an attractive conjunction, a clock's symbolic planets or an arbitrary screen heading cannot supply those inputs. Existing event-date/planetary source reviews remain attributed prior work, not new independent evidence here.

## Pool-lamp discriminator — a conditional impossibility

After source `S` and aperture `P`, a direct transmitted ray is `P + t(P−S)`, with `t ≥ 0`. Its intersection with a horizontal receiver at height `zR` has

`t = (zR−zP)/(zP−zS)`.

If `zS < zR < zP`, the numerator is negative and denominator positive: the intersection is behind the aperture. Thus **a below-receiver lamp cannot project through a higher aperture onto that lower horizontal receiver by this direct path**. This statement uses height order only, not assumed lengths or compass headings. Source above aperture, higher/wall receivers, reflections, different rays and sunlight remain different models.

The already inspected typed 1990 instructions place the lights/pump in the small pool and warn about operating with water more than twelve inches below plaza paving. They establish neither the emitter's installed height nor the aperture/receiver ordering or beam profile. The warning is not a measurement of lamp depth. Seasonal times describe intended operation, not verified uptime or cryptographic purpose. The algebra excludes a specified height-order model, **not the actual installation without those missing measurements**.

## Photograph and evidence boundary

The supplied LOC TIFF was retrieved and its SHA256 independently matched `302fb88dee8db7f484a85d9d7f9bbd39f69de37cbf7bb25ae5a2e35bf8b8cf52`. Local visual inspection confirms bright letter-shaped marks on pavers, with clearer shapes left and broader patches right. It is the same exposure as the older low-resolution view, not independent corroboration. No exposure time, north registration, emitter identification or metric scale was inferred. The original and inspection derivative remain outside the repository; [source receipt](../sources/physical-solar-002/SOURCE-RECEIPT.json) records provenance and access limits. The catalogue request returned 403; no restricted catalogue route was attempted. The [independent evidence report](../independent/2026-10-24/physical-item2/PARENT-EVIDENCE-REPORT.md) is now preserved with attributed searches and source limits. The repository owner also inspected a native-resolution ground crop (top 2700, left 1300, height 1500, width 2000 pixels in the original TIFF). Inspection produced **no certified aperture-to-ground identity pairs**; this is not a proof that annotation is impossible. Repeated glyphs, the partially visible curved screen and unknown camera/light/receiver geometry prevent treating an attractive spot assignment as established correspondence. No camera or optical fit was attempted; the proposed twelve-pair calibration gate remains unpassed.

The worker reports prior source-space boundary/glyph-center reconstruction. Those data are different from aperture-to-ground correspondences. Its exact calibration package was not located in the current tracked tree during this integration, so its quoted counts/residuals remain attributed and were not locally replayed. The earlier geometry audit is retained; no generic font fit replaces it.

## Independent finite-source and plate-thickness checks

The [supplied arithmetic and replay receipt](../independent/2026-10-24/physical-item2/README.md) add a separate physical-sensitivity calculation. This was received with outcomes already known, not a new blind experiment or amendment to the original 96-scenario protocol. NASA's [Sun Fact Sheet](https://nssdc.gsfc.nasa.gov/planetary/factsheet/sunfact.html), independently read locally, gives full apparent diameter 1919 arcseconds at 1 AU (range 1887–1952). For a zero-thickness point aperture one metre above a flat receiver, that finite disk at 9.5505° elevation produces an exact conical footprint about **338.2 mm by 56.1 mm**. At 30° the corresponding diameters are **37.2 mm by 18.6 mm**. Scale linearly with aperture height; no installed height has been measured. These are kernel-support widths, not measured blur or an automatic readability threshold. Occlusion can clip the solar disk; a finite real glyph contributes its own shape.

For an ideal straight aperture channel, front/back ray displacement is `t tan θ`, with θ measured from the local plate normal. A hypothetical 5 mm channel closes at 38.22°, 27.70° or 21.49° under the named 1/4-, 3/8- or 1/2-inch plate scenarios. These are source-conflict scenarios, not a measured uncertainty distribution, and 5 mm is not a measured Kryptos stroke width. Curvature and real two-face contours matter.

The legacy exact-ENE bound also implies an obstacle rise/distance cutoff **0.168249** for the solar center: an opaque obstruction in that azimuth above this sightline blocks center rays under that model. No such obstruction was measured here; finite solar radius/refraction matter near the limit. At elevation 30°, one degree of heading or altitude error causes first-order displacement about 30 mm transverse or 70 mm longitudinal per metre of aperture height. None of these calculations fixes a compass bearing, timestamp or decoding rule.

Local independent validation checked all 26 supplied numeric values, replayed the complete output in a temporary directory, verified 1,800 cone-boundary rays against an independently derived ellipse, and checked all nine channel thresholds. The original worker timestamps were not supplied and remain unknown; local replay timestamps are separately recorded. The parent report's proposed 12 non-K4 aperture/spot pairs, eight training plus four spatial holdouts and repeated annotation controls is a future calibration gate, not a result achieved here. No original imagery or raw copyrighted scrape is committed.

## Validation and practical limits

Ten new unit tests pass, including 444 independent ENU forward/inverse checks, 18 dense root/branch grids, shadow-direction mutation, singular and countermodel ray cases, Julian-date epoch and fixed-date method comparison. The original run independently checks **960,096** altitude-grid points, **39** USNO/NOAA calendar pairs and **125** ray substitutions. All pass. Peak recorded RSS is 14,712,832 bytes; quantitative runtime 0.708 seconds, within frozen 60-second/256-MiB budget.

Maximum USNO/NOAA declination difference is 0.3602° and equation-of-time difference 0.2364 minutes, within the predeclared 0.75°/2-minute consistency tolerances. This is a lower-precision independent approximation comparison, not full high-precision ephemeris validation. Optional official SPA vector retrieval failed (DNS/502); no remembered numeric vector is presented as verified. USNO's stated approximate coordinate accuracy does not establish monument geometry. UTC approximates UT for these broad angular checks; no subsecond claim. No statistical null is needed for the exact conditional ray identity or declination envelope.

Remaining gates: independently timed and registered imagery; surveyed surface/receiver/source geometry; frame conversion; a uniquely specified extraction/key operation. **K4 remains unsolved.** This item narrows conditional physical interpretations and does not exhaust physical/navigation hypotheses. No later numbered investigation or Site change was started.

Final aggregate validation: **497 tests pass on Python 3.9 and 3.12**; [timestamped validation receipt and logs](../results/PHYSICAL-SOLAR-002-VALIDATION.json). The preserved independent specification retains its historical link exceptions; new Markdown targets and fragments pass. No configured CI workflow was present at the pre-publication check.
