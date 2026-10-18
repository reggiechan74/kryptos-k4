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
