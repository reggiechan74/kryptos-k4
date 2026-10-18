# Neptune discovery connection: bounded assessment

Research date: 18 October 2026. This is a supplied completed research report,
preserved as documentation. The research worker performed the source review and
photo inspection described below; this repository update did not independently
retrieve those sources. No cipher tests or key search were performed for this
report. Existing regression tests are recorded separately in the experiment log.

## Assessment

The historical connection Neptune → Le Verrier → Berlin is real. No documented
bridge from that history to Sanborn's Kryptos was located in this bounded search.
The best-supported methodological analogy is inference from residuals followed
by an independent prediction. It supplies no unique cipher, key, coordinate
conversion, or text extraction rule.

## How Le Verrier predicted Neptune

He recomputed Uranus's expected motion under known gravitational influences,
compared it with recorded positions, and treated the unexplained differences as
evidence of an unseen outer planet. He solved backward for a planet whose
gravitational perturbations could explain those differences. This was an inverse
problem in celestial mechanics, not cryptographic decoding.

Paris Observatory's detailed IMCCE history reports these assumptions and
limitations: an exterior planet near the ecliptic; an initial distance about
twice Uranus's, guided by the empirical Titius–Bode pattern; final semimajor axis
36.1539 AU and eccentricity 0.1076, compared with Neptune's roughly 30 AU and
0.009. The angular prediction succeeded although the reconstructed full orbit
was substantially wrong, because some parameter errors compensated. Its
illustrated 326°32′ is heliocentric longitude for 1846 measured from the vernal
equinox, not a compass bearing in Berlin. Galle found the object about 52
arcminutes from the assigned sky position. Precise epoch/frame conventions would
need checking in the original memoir before any numerical key claim.

Sources:

- [Paris Observatory overview and manuscript image](https://observatoiredeparis.psl.eu/the-discovery-of-neptune.html).
- [Paris Observatory/IMCCE detailed account](https://lettre-info-lte.obspm.fr/medias/2022/12/docs/Le_Verrier_et_l_astronomie_des_invisibles.pdf).
- [Paris Observatory exhibition with original-document links](http://expositions.obspm.fr/leverrier/Le-Verrier/neptune/intro.html).

## What happened in Berlin

On 23 September 1846, Johann Gottfried Galle and Heinrich Louis d'Arrest searched
at the Berlin Observatory. Galle used the telescope; d'Arrest compared reported
positions with Carl Bremiker's Hora XXI chart from the Berlin Academy's sky-map
series. An object absent from the chart identified the candidate. The chart was
completed in 1844 and printed in 1845. AIP holds an excerpt marked with the
predicted and observed positions; its caption cautiously attributes those later
pencil marks to Galle. The precise chart offers a concrete historical artifact,
but no supported rule maps its stars or coordinates to K4 characters.

Sources:

- [AIP archival account](https://www.aip.de/en/institute/history/the-history-behind-the-aip-logo/).
- [AIP discovery anniversary](https://www.aip.de/en/news/175th-anniversary-of-the-discovery-of-neptune/).
- [Archival chart image](https://www.aip.de/media/images/Bremiker_Hora_XXI.original.jpg).

## Correct observatory and geometry

The discovery occurred at the New Berlin Observatory, opened in 1835 on
Lindenstraße near Hallesches Tor. It did not occur at the earlier Dorotheenstraße
site or the later Babelsberg observatory. AIP's institutional history verifies
that location and chronology, according to the supplied review.

Keep the two published coordinate source pairs explicit. Do not overwrite the
earlier pinned geometry or interpret either approximation as exact ENE (67.5°).

| Coordinate source pair | Fountain latitude, longitude | Clock latitude, longitude | Reported fountain → clock |
| --- | --- | --- | --- |
| Earlier OSM centers, pinned in the geographic note | 52.5195950, 13.4068433 | 52.5211638, 13.4133059 | about 68.25° true, 471 m |
| Secondary published points used in this report | 52.51960, 13.40687 | 52.5212, 13.4133 | about 67.76° true, 470 m |

Earlier sources: [fountain OSM way 23813204](https://www.openstreetmap.org/way/23813204),
[clock OSM way 417529567](https://www.openstreetmap.org/way/417529567), and
[the preserved geographic note](world-clock-ene-geography.md).
This report's secondary points: [Neptune Fountain](https://en.wikipedia.org/wiki/Neptune_Fountain_(Berlin))
and [World Clock](https://en.wikipedia.org/wiki/World_Clock_(Alexanderplatz)).
The reported figures are retained with their respective inputs; this coding
update did not recompute or reconcile them. Their difference is not evidence of
an exact alignment or permission to tune coordinates.

The New Berlin Observatory point used here is 52.50389 N, 13.39417 E. From it to
the secondary Clock point, the reported great-circle initial bearing is about
33.9° true and distance 2.32 km. This does not fit ENE (67.5°); ordinary coordinate
rounding cannot repair that large discrepancy. These are map-scale checks using
published secondary coordinates, not survey-grade measurements. The fountain
point was independently published and was not relocated to improve alignment.

Observatory → fountain is reported as about 26.19° and 1.95 km. The fountain
route remains geographically plausible; substituting the actual discovery
observatory weakens the directional fit. Geography alone establishes no cipher
mechanism. Keep the clock-terminal model and the separate fixed geometric
reflection in [the period-map report](berlin-period-map-corridor.md) unchanged.

Sources:

- [AIP primary location history](https://www.aip.de/en/institute/history/).
- [Secondary observatory coordinates](https://en.wikipedia.org/wiki/Berlin_Observatory).

## The Clock's planetary display

The designer/licensing website confirms a rotating planetary sculpture above
the Urania World Clock and describes planetary motion as the basis of timekeeping.
It identifies no special Neptune feature, encodes no stated 1846 discovery, and
connects no Le Verrier history with the design in the reviewed material. A
solar-system display alone does not establish an astronomical ephemeris or a
usable Neptune position for a specific date.

Source: [Urania World Clock designer/licensing site](https://www.weltzeituhr-berlin.de/die-urania-weltzeituhr).

## Clock-face observation: orientation and inscription gates

The research worker inspected this [modern clock-face photograph](https://www.sehenswuerdigkeiten-berlin.info/wp-content/uploads/2024/05/Berlin-Weltzeituhr-Alexanderplatz.jpg).
The Asian arc is roughly east. A candidate KRASNOJARSK face appears with HANOI,
BANGKOK, PHNOMPENH and JAKARTA, versus adjacent IRKUTSK/ULANBATOR with PEKING,
SHANGHAI, MANILA, PERTH, HONGKONG, KUALALUMPUR and SINGAPUR. These are supplied
visual observations, not a verified geographic panel assignment or 1989 transcript.

The user's separate observation is that **BERLINCLOCK and KRASNOJARSK each have
11 letters**. This is a weak length coincidence, not a confirmed key or extraction
rule. **SINGAPUR is the German spelling**, not a spelling error to repair.

The exact true-ENE 67.5° panel has **not** been verified. Twenty-four faces at
15° spacing do not determine absolute orientation. The
[official Berlin description](https://www.berlin.de/sehenswuerdigkeiten/3561749-3558930-weltzeituhr.html)
confirms a ground compass rose and city corrections after reunification,
according to the supplied review. Consequently historical 1989 inscriptions
remain **unverified**. A modern photograph cannot establish them.

Approaching ENE from the fountain means seeing the opposite WSW-facing side of
the clock. Travel bearing and the outward-facing panel bearing must not be
conflated. No city string is accepted as a confirmed key, and no cipher search
was launched from these observations.

## Ranked falsifiable hypotheses

1. **Residual-inference analogy.** Most useful as a research method, but presently
   unsupported as Sanborn's intended theme. Predeclare a low-complexity cipher
   model, infer parameters using part of the confirmed plaintext, and require
   prediction of withheld plaintext plus exact re-encryption. For an explicitly
   assumed additive alphabetic cipher without transposition, implied key values
   are C_i − P_i modulo 26; a proposed period must agree at every matching phase.
   This is a generic diagnostic, not an algorithm derived from Le Verrier.
   Reject the model on its first hard contradiction; do not add adjustable exceptions.
2. **Neptune/chart as key material.** Historically grounded entities exist,
   especially NEPTUNE and Hora XXI, but no bridge to a unique extraction rule
   exists. A literal NEPTUNE-key pilot could be finite and exploratory in an
   established harness with frozen conventions. No evidence selects it over
   NEPTUN, author names, dates or chart encodings. No pilot was run or derived
   key claimed. Do not expand into dates, reversed spellings, coordinate formats
   and arbitrary shifts. A failed pilot would reject only its declared model.
3. **Discovery-site directional route.** The specific claim that the 1846
   observatory points ENE toward the Clock is contradicted by the published
   coordinates: about 34°, not 67.5°. Changing observatory severs the discovery
   connection. Keep the existing fountain origin separate.

## Search limits

The research worker's targeted searches for Kryptos/Sanborn with Neptune, Galle
and Le Verrier yielded no primary author statement or documented design
connection. This is a bounded negative result, not proof that no connection
exists. No third parties were contacted, no paid verification service was used,
and no arbitrary cryptographic key search was run. This documentation update
performed no additional source search or cipher experiment.
