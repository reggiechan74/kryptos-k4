# Later addendum: regional magnetic declination near Langley

23 October 2026 UTC. This is separate from the original four-file research ZIP.
Neither its bytes, SHA-256 nor the original report/dossiers were changed.

The official BGS IGRF-14 API was independently queried at approximate coordinates
38.951° N, 77.146° W, with an assumed altitude of 0 km above the WGS84 ellipsoid.
This is a declared model location/height, not a survey of the entrance rose.
The regional estimate puts magnetic north about **9.6° west of true north in
1989**. Rounded results are:

| Model date | Declination |
| --- | ---: |
| 1 January 1988 | 9.5° west |
| 1 January 1989 | 9.6° west |
| 1 January 1990 | 9.7° west |

Exact API precision, units, dates, coordinates, URLs and byte hashes are retained
only in the [raw receipts and manifest](../../../sources/igrf14-langley-20261023/manifest.json).
Reproduce by requesting each listed public URL; no credentials, paid service or
external message is needed. The raw JSON responses are preserved unchanged.

The [BGS calculator documentation](https://geomag.bgs.ac.uk/data_service/models_compass/igrf_calc)
defines declination as positive east and geodetic altitude in kilometres above
the WGS84 ellipsoid. With clockwise bearings, true bearing equals magnetic
bearing plus east-positive declination, modulo 360°. Thus a **hypothetical**
247.5° magnetic bearing would become about **237.9° true** in the 1989 model.
This arithmetic does not establish that the carved needle, engraved N or a real
compass at the monument had either bearing.

[BGS model documentation](https://geomag.bgs.ac.uk/research/modelling/IGRF.html)
covers these historical dates but explains that IGRF approximates the main field
and omits small-scale crustal anomalies. It is not a model of the nearby
lodestone, ferrous structures or position-dependent instrument disturbance.
It cannot turn an unsupported physical azimuth into a measured fact. No bearing
fit, phase search, optical test or K4 cryptanalysis was run for this addendum.
