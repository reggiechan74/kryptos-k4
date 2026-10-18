# World Clock / ENE geographic hypothesis

Source-attributed research note supplied 18 October 2026, after publication of
the current language/masking/word results. H-GEO-ENE is a geographic hypothesis,
not a cipher method. The coding executor records the supplied source checks and
calculations here; it did not repeat a landmark search or independently fetch
these map/monument pages during this documentation step.

## Supplied locations and comparisons

- [World Clock mapped center](https://www.openstreetmap.org/way/417529567):
  latitude 52.5211638, longitude 13.4133059.
- [Neptunbrunnen mapped center](https://www.openstreetmap.org/way/23813204):
  latitude 52.5195950, longitude 13.4068433.
- The [official monument record](https://denkmaldatenbank.berlin.de/daobj.php?obj_dok_nr=09011281)
  is cited by the supplied review for the fountain's present location since 1969
  and 18 m basin diameter. These are attributed source facts, not newly inspected
  primary evidence in this coding phase.

Compass ENE is 67.5° true. The supplied fountain→clock calculation is 68.25° true,
about 471 m. The reverse 247.5° ray from the clock misses the mapped fountain
center by approximately 6 m. This is approximate alignment, not an exact bearing,
proof of intentional placement, or a demonstrated Kryptos connection.

The supplied bounded comparison sample was:

| Direction | Initial bearing, true | Approximate distance |
| --- | ---: | ---: |
| Neptunbrunnen → World Clock | 68.25° | 471m |
| World Clock → [Haus der Statistik](https://www.openstreetmap.org/way/24271930) | 63.06° | 370m |
| World Clock → Haus des Reisens | 46.08° | 308m |
| TV tower → World Clock | 81.91° | 265m |
| Marienkirche → World Clock | 80.58° | 418m |
| Berliner Dom → World Clock | 74.45° | 862m |

Only the three explicit OSM links above were supplied with this receipt; the
other rows reproduce the researcher's reported bounded comparisons, without a
new local coordinate or source lookup. This sample is not exhaustive. It neither
establishes the closest possible landmark nor authorizes further landmark fishing.
The review reports an approximately 44 m offset in an official clock-map point;
do not use that point for meter-level precision. Map centers, present-day geometry,
and a historic intended reference must remain separate claims.

## Reproducible approximate bearing formula

For source latitude/longitude φ1,λ1 and destination φ2,λ2 in radians, let
Δλ=λ2−λ1. The initial great-circle bearing is:

```text
y = sin(Δλ) cos(φ2)
x = cos(φ1) sin(φ2) - sin(φ1) cos(φ2) cos(Δλ)
bearing_degrees = (degrees(atan2(y,x)) + 360) mod 360
```

Distance under a spherical Earth model uses R=6,371,000 m and:

```text
a = sin((φ2-φ1)/2)^2 + cos(φ1) cos(φ2) sin(Δλ/2)^2
distance = 2 R atan2(sqrt(a), sqrt(1-a))
```

At these short distances, cross-track displacement from a proposed bearing is
approximately `distance * sin(actual_bearing - proposed_bearing)`, with the
angle in radians. These are reproduction formulas, not a new computation or
precision geodetic survey in this step. Bearings are true-north bearings, not
magnetic or map-grid bearings.

No keyword, number, plaintext, route dimensions, or encryption mechanism was
derived. Any cipher test based on geography needs a separately fixed hypothesis,
independent source motivation, explicit uncertainties, and a committed finite
specification. The note does not promote geographic proximity into a solution.

[Exact-bearing footprint review](world-clock-exact-axis-footprints.md) refines the
center-versus-footprint distinction: the exact ENE ray intersects part of the
already identified Haus der Statistik despite its off-axis center marker.
Modern and 1985-map evidence are qualified separately; 67.5° remains distinct
from the earlier 68.25° fountain-centre axis. No new key was extracted.
[Inauguration/dedication astronomy](inauguration-dedication-astronomy.md) is a
separate bounded source review, not evidence that either axis encodes a date.
