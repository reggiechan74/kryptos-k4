# World Clock inauguration and Kryptos dedication: bounded astronomy review

18 October 2026. This records a supplied independent astronomical review,
with primary-source checks identified below. It is not an exhaustive catalogue
of astronomical events, an ephemeris rerun by this executor, or a cipher test.
No designer intent or unique astronomical key is established.

## Dates and lunar context

[Berlin's official clock page](https://www.berlin.de/sehenswuerdigkeiten/3561749-3558930-weltzeituhr.html)
dates the World Clock's public inauguration to **30 September 1969**.
The [CIA history](https://www.cia.gov/legacy/headquarters/kryptos-sculpture/)
dates Kryptos's dedication to **3 November 1990**, and design selection to
**November 1988**, without an exact selection day. Dedication, design selection
and an unspecified construction/installation time must not be conflated.

The NASA catalogues contain **no solar or lunar eclipse on either event date**:
[1961–70 solar](https://eclipse.gsfc.nasa.gov/SEdecade/SEdecade1961.html),
[1961–70 lunar](https://eclipse.gsfc.nasa.gov/LEdecade/LEdecade1961.html),
[1981–90 solar](https://eclipse.gsfc.nasa.gov/SEdecade/SEdecade1981.html),
[1981–90 lunar](https://eclipse.gsfc.nasa.gov/LEdecade/LEdecade1981.html).
This executor read these year entries. An eclipse on another nearby date is not
an eclipse on the inauguration/dedication date.

The supplied USNO phase review gives full Moon **25 September 1969, 20:21 UT**,
and last quarter **3 October, 11:05 UT**: the clock opened during a waning-gibbous
phase. It gives full Moon **2 November 1990, 21:48 UT**, the day before dedication.
[1969 USNO API query](https://aa.usno.navy.mil/api/moon/phases/date?date=1969-09-01&nump=8),
[1990 query](https://aa.usno.navy.mil/api/moon/phases/date?date=1990-11-01&nump=4).
Those numerical results are supplied independent source checks; this executor's
web tool could not fetch the API URLs, and did not recompute lunar phases.
A nearby full Moon alone supplies neither an intended date code nor a key.

## Direct ENE sunlight does not fit these dates

Using the [USNO approximate solar-coordinate method](https://aa.usno.navy.mil/faq/sun_approx),
the independent calculation gives solar declination approximately **−2.84°**
at noon UT on 30 September 1969 and **−15.07°** on 3 November 1990.
This executor read the algorithm but did not rerun those calculations.

For latitude φ, geometric solar elevation h and true-north clockwise azimuth A,
`sin(δ)=sin(φ)sin(h)+cos(φ)cos(h)cos(A)`.
At ENE A=67.5° and nonnegative elevation, a visible geometric Sun requires
positive declination: minimum about **+13.47° at Berlin**, **+17.31° at Langley**.
Both event dates instead have negative declination. Thus direct visible ENE
sunlight does not fit either day at the respective locations. These are geometric
horizon statements, not a calibrated building/site-light model.

This does **not** exclude WSW sunlight casting an ENE ground shadow, nor reflected
illumination. Solar geometry recurs seasonally and does not by itself identify a
year. Exact civil time also needs location, timezone/DST and equation-of-time
conventions. See the [seasonal-light review](seasonal-light-source-review.md).

## One computed coincidence, with substantial limits

The independent [JPL Horizons](https://ssd.jpl.nasa.gov/horizons/app.html) review
reports apparent **geocentric ecliptic longitude** crossing for Mercury/Uranus
on 30 September 1969, around **17:22 UT**. This is a linear interpolation between
six-hour samples, not a precisely solved event time or a known ceremony time:

| UT on 30 September 1969 | Mercury longitude | Uranus longitude |
| --- | ---: | ---: |
| 12:00 | 184.8377° | 184.5821° |
| 18:00 | 184.5680° | 184.5979° |

At noon the reported ecliptic latitudes were −2.1453° and +0.6861° respectively.
Consequently equal longitude is not equal sky position: their angular separation
was about **2.8°**, both roughly **3° from the Sun**. This was not an ordinary
naked-eye spectacle or a literal three-dimensional alignment. The samples and
interpolation are supplied review results; a full Horizons query/response was
not rerun or archived by this executor. The landing-page link documents the
service, not an independently reproduced numerical receipt.

[Kunsch's clock description](https://kunsch-metallbau.de/referenzen-/weltzeituhr-berlin-alexanderplatz/)
says the simplified solar-system representation rotates once per minute. It does
not describe a frozen dedication-day ephemeris. An Earth-view conjunction cannot
simply be read onto a Sun-centered model, and schematic rings are not measured
orbital coordinates. The coincidence establishes no designer intent, extraction
rule, unique date selection, or Kryptos connection.

The next useful evidence would be a documented designer instruction, calibrated
model orientation/phase or another independently specified mechanism—not a new
choice of astronomical event to fit the clue. No numerical key or cipher
experiment was derived from this bounded review.

[Structured supplied-review receipt](../sources/inauguration-dedication-astronomy-review.json).
The [exact ENE/WSW footprint review](world-clock-exact-axis-footprints.md) answers
a separate groundplan question and establishes no astronomical sightline.

## Deeper conjunction review — 18 October 2026

A fresh independent JPL **DE441** analysis refines the earlier six-hour estimate.
The apparent geocentric **ecliptic-longitude conjunction** is about
**30 September 1969, 17:22 UTC / 18:22 Berlin CET**, reported to minute precision
from one-minute interpolation, not as a solved subsecond event. The
[PTB historical time table](https://www.ptb.de/cms/ptb/fachabteilungen/abt4/fb-44/ag-441/darstellung-der-gesetzlichen-zeit/sommerzeiten-und-hochsommerzeiten-in-deutschland-bis-1979.html)
supports CET rather than a modern DST assumption for that date.

At that event the supplied longitude is 184.59625°; latitudes are Mercury
−2.07387°, Uranus +0.68609°, giving **2.75996° separation**. Their Sun elongations
are 3.460° and 2.853°. At Alexanderplatz the reported elevations are Mercury
−8.918°, Uranus −6.235°, Sun −6.232°: both planets are below the horizon. This
was not a locally visible display, even before considering solar glare.

Definitions change the date/time:

| Definition | Supplied approximate UTC | Angular qualification |
| --- | --- | --- |
| Equal apparent right ascension | 29 September 1969, 13:31 | different coordinate criterion |
| Equal apparent geocentric ecliptic longitude | 30 September, 17:22 | separation 2.75996° |
| Closest apparent approach | 1 October, 09:54 | separation 2.64912° |

The [USNO glossary](https://aa.usno.navy.mil/faq/asa_glossary) distinguishes
conjunction coordinate equality from appulse/minimum apparent distance.
Do not choose whichever definition retrospectively best matches a desired date.

The independent daily and six-hour series over **1960-01-01 to 1980-01-01** each
find **28 longitude conjunctions**: 16 years have one; 1964, 1969, 1974 and 1979
have three each. In 1969 they fall on **29 August, 30 September and 16 October**.
This is agreement between two sampled numerical counts, not a formal continuous
root-count proof or a probability of design intent. Selecting the planets,
coordinate definition and opening date after seeing the coincidence matters.

The [Horizons manual](https://ssd.jpl.nasa.gov/horizons/manual.html) defines
quantity 31 as apparent observer-centered ecliptic-of-date coordinates; the
reported conjunction uses the geocenter. Quantity 18 is geometric heliocentric
J2000 output at each target's **individual light-emission time**. Its supplied
longitudes here are Mercury 13.21377°, Uranus 184.87259°, difference 171.65881°.
They are not a simultaneous-date planet diagram, but clearly do not show a
heliocentric conjunction. Earth-view equality cannot simply be transferred to
the clock's Sun-centered schematic. This executor checked the quantity definitions,
not the ephemeris itself. The worker's reproducible query URLs and numerical receipt have now been saved
as a received source artifact (linked below). Raw API responses were not fetched
here and no ephemeris was independently rerun. The new numbers remain supplied
independent results.

## Historical bridge: documented symbolism, unproved date selection

The [designer-authorized clock account](https://www.weltzeituhr-berlin.de/die-urania-weltzeituhr)
is reported in retrieved indexed text as linking development to the DDR's
20th anniversary and the planetary top to astronomical timekeeping. Direct
fetch failed, so that content is attributed to the supplied indexed-source review.
[Erich John's 2019 interview](https://www.tagesspiegel.de/berlin/die-weltzeituhr-kennt-jeder-niemand-ihren-erfinder-6541270.html)
dates the first sketch to **24 June 1968**, already with the solar-system top,
and discusses Sun/Earth and axial tilts. The consulted text names no Mercury–Uranus
conjunction as a design or opening-date rule. This executor read those passages.
[Kunsch's account](https://kunsch-metallbau.de/referenzen-/weltzeituhr-berlin-alexanderplatz/)
describes the simplified top rotating once per minute, not a dedication ephemeris.

A supplied public issue excerpt for [Neues Deutschland, 3 October 1969,
page 8](https://www.nd-archiv.de/ausgabe/1969-10-03) reports the handover after
seven months of construction. The full 69-word article is paywalled and was not
read; this executor's issue-page extraction did not expose the item. Neither
that excerpt nor the consulted sources establish a conjunction-driven date.
No authoritative planet-identification/angle plan was located in this bounded
review. That is an evidence gap, not proof the designer had no such intention.

### Received numerical receipt and reproduction queries

The [complete supplied Horizons receipt](../sources/mercury-uranus-horizons-received-receipt.json)
retains 13 public reproduction query URLs, the refined event, alternative event
definitions, Berlin elevations and all 28 approximate crossings. It distinguishes
received calculations from this executor's JSON/query-parameter/count checks.
Original HTML-escaped URLs are preserved, with decoded copies for use in the API;
none was executed in this documentation update. Raw subsecond interpolation
values are calculation outputs, not asserted uncertainty. The broad-series
approximate crossing list uses coarser sampling than the separately refined
one-minute event; do not equate their numerical seconds. Before 1962 the listed
Horizons UT basis is UT1, while the 1969 event uses UTC. The sampled-year counts
and 1969 dates agree internally; that verification does not reproduce the
underlying ephemeris or turn a retrospective coincidence into evidence of intent.
