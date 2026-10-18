# Seasonal light and Kryptos — bounded source review

18 October 2026. User hypothesis: seasonal sunlight or a sundial-like artistic
mechanism. **Real light projection is documented; a seasonal K4 extraction rule
is not established.** No date/key/shadow sweep, contact or site action was performed.
This note supplies no input to the separate Beaufort experiment.

## Observations, interpretation and missing calibration

The [CIA sculpture description](https://www.cia.gov/legacy/headquarters/kryptos-sculpture/)
states that the tableau was intentionally flipped to be read from behind. That
supports intentional visual design, but does not establish an optical decoder.

[Elonka Dunin's firsthand journal](https://elonka.com/kryptos/) dates her first
visit to October 18, 2002. She reports direct letter-light and narrow-bar effects,
then late-afternoon letters on a white rock caused by sunlight reflecting from
New Headquarters Building windows back through the copper. No exact time,
window, receiving rock face or letter sequence is recorded. It is a reflected
optical path, not evidence of a direct-sun compass alignment or a seasonal key.
Her [measurement wishlist](https://elonka.com/kryptos/wishlist.html) asks for
geometry/context and photographs of these effects; it does not supply calibration.
No requests from that page were acted upon.

The [illustrative Sanborn image](https://commons.wikimedia.org/wiki/File:Kryptos_sculptor.jpg)
is an older overview: Commons catalogs 1991, while the original upload description
said 1990. It is not documentation of the 2002 observation. No camera or geometric
calibration was derived from it here.

The supplied independent review of the [2009 Smithsonian oral history](https://www.aaa.si.edu/download_pdf_transcript/ajax?record_id=edanmdm-AAADCD_oh_283557)
places sunlight remarks in general public-art and later projection-work contexts,
not a K4 seasonal date. This executor's transcript fetch failed (HTTP 500), so
that scope assessment is explicitly supplied audit evidence.
In the [2005 Wired interview](https://www.wired.com/2005/01/questions-for-kryptos-creator/),
Sanborn says being onsite is unnecessary to solve the text, while its meaning
may relate to a physical act/place. This weighs against an inaccessible onsite
key; it does not rule out a reproducible optical rule from published information.

## What Scott's simplified models actually tested

All source/log links below are pinned to Scott commit
`3ce19e3ae164a54af8743222ad3de5f6a93f6faf`. Code was read, never executed here.
[run_shadow_egypt.py](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/run_shadow_egypt.py)
is a discrete affine transformation of cell centers onto a tableau grid, with
rounding and selected alphabet/key equations. It is not an aperture optics model.
[run_shadow_overlap.py](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/run_shadow_overlap.py)
assumes two joined half-cylinders, radius 1.52 m and height 3.66 m, projecting
cell centers onto flat ground. Its grid has 7,740 model directions.
The [retained log](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/results/shadow_overlap.log)
reports 166 directions with at least 12 overlapping crib cells; best agreement
6/13 at model azimuth 72°, elevation 40°, versus shuffled maxima 5,6,5.
These are third-party reported outcomes, not our rerun or a measured compass
heading. They do not exclude continuous optics. Real apertures, occlusion,
measured curvature/heading, actual receiving surfaces, reflections and camera
calibration are absent.

## Conditional ENE geometry, not a date prediction

Rearranging [NOAA's solar-position equations](https://gml.noaa.gov/grad/solcalc/solareqns.PDF),
with A clockwise from true north, h geometric elevation and φ latitude:
`sin(δ)=sin(φ)sin(h)+cos(φ)cos(h)cos(A)`.
For illustrative φ=38.95° and annual declination bounded by ±23.44°, above an
unobstructed geometric horizon:

- Direct Sun at ENE 67.5° requires δ ≥17.31° and elevation 0–9.55°.
- A direct ground-shadow bearing ENE instead places the Sun WSW 247.5°:
  δ ≥−17.31° and elevation up to 60.22°.

These ignore refraction, terrain and actual sculpture geometry. Reflections break
the opposite-bearing rule. The same declination commonly occurs twice yearly;
civil time also requires year, longitude, timezone/DST and equation of time.
No date has been selected. [NREL's solar-position algorithm](https://docs.nrel.gov/docs/fy08osti/34302.pdf)
is an ephemeris reference for a future specified model; the executor's fetch
returned HTTP 502, so it was not used to compute positions.
`python3 experiments/check_solar_bounds.py` reproduces only these analytic bounds:
[receipt](../results/SOLAR-BOUNDS-NOTE-CHECKS.json).

## Gate before another optical test

First obtain a lawfully published image with identifiable apertures and receiving
projection. Calibrate geometry with non-K4 features, reserving other features
for validation; reproduce the actual ciphertext-aperture projection rather than
decrypting K1 and projecting its plaintext. Fix true heading, receiver, annual
Sun paths, occlusion and uncertainty. Predeclare one extraction rule before K4
scoring, then require full 97-letter re-encryption and controls for the complete
pipeline. Existing confirmed cribs are not fresh blind holdouts.
The next justified step is a validated optical model or a precise missing
measurement, not selecting calendar dates to improve a crib score.
