# World Clock: exact ENE/WSW footprint axis

18 October 2026. This preserves supplied independent geodesic/polygon and
historical-map analysis, not a new K4 test or discovery claim. This executor did
not rerun Vincenty intersections or inspect the 1985 raster in this update.
The historical building-date sources below were directly read here.

Origin: mapped clock point **52.5211638 N, 13.4133059 E**. Rays use true bearings
**67.5° ENE** and **247.5° WSW** on WGS84. The worker used Vincenty geodesics
and mapped-polygon intersections, with an OSM snapshot dated **2026-05-31**,
retrieved 18 October 2026. Distances below are model outputs from that mapped
origin, not surveyed millimetre accuracy. A building's center marker can miss a
ray while part of its footprint intersects it.

## Modern mapped footprints and period evidence

| Direction / feature | Reported intersection or miss | Historical qualification |
| --- | --- | --- |
| ENE [Die Mitte](https://www.openstreetmap.org/way/24273422) | enters 95.465 m; exits 168.355 m | 2009 building; not a 1989 obstruction |
| WSW [Alea 101](https://www.openstreetmap.org/way/159958500) | enters 130.000 m; exits 191.639 m | 2014 building; not a 1989 obstruction |
| ENE [Haus der Statistik](https://www.openstreetmap.org/way/24271930) | enters 326.748 m; exits 352.325 m | 1985 map independently supports about 327–353 m |
| WSW Fernsehturm south pavilion | roughly 257–291 m on 1985 raster | historical raster estimate; exact modern polygon fetch failed |
| WSW [Neptune basin](https://www.openstreetmap.org/way/23813204) | roughly 467.71–475.01 m | footprint intersects off-centre; not a ray through the fountain center |
| WSW tower shaft | misses by about 50.4 m | tower shaft and surrounding pavilion are different objects |
| Modern [station hall](https://www.openstreetmap.org/way/20144781) | misses by about 5.45 m | a 1985 map-edge graze at 90–110 m is within raster uncertainty |
| Berolinahaus | misses by about 22.2 m | nearby flank, not an exact ray hit |
| Alexanderhaus | misses by about 9.95 m | nearby flank, not an exact ray hit |

The [BIM historical description](https://www.bim-berlin.de/landesimmobilien/projekte/haus-der-statistik)
dates Haus der Statistik to **1968–70**. The
[official monument record](https://denkmaldatenbank.berlin.de/daobj.php?obj_dok_nr=09065023%2CT)
dates the Fernsehturm's surrounding pavilion architecture to **1969–72**.
Thus both are period-relevant structures. Their exact unchanged geometry in
1989 is not established merely by their construction dates or a modern polygon.

Haus der Statistik was already identified in the earlier geographic comparison.
The refined finding is **footprint intersection**, rather than treating its
off-axis central marker as the whole building. It is not newly discovered key
material. The 1985 evidence comes from HistoMap K5 sheet 423D, layer
`423_D_1985`; the [period-map note](berlin-period-map-corridor.md) preserves
its source URLs, catalogue dating and the absence of an exact 1989 edition.
A railway/bridge crossing is not proof of a ground-level solid building in the
ray, and a raster-edge graze is not a robust modern station-hall intersection.

## Interpretive boundaries

These are **groundplan footprints**, not 3D visibility, façade hits or unobstructed
light paths. Heights, receiver elevations, openings, roofs and occlusion are not
modelled. The clock is between structures along the axis, but is not their equal
midpoint. Do not move the origin or choose footprint corners to make it one.

Keep exact 67.5° ENE distinct from the earlier **68.25° fountain-centre→clock**
axis in the [geographic note](world-clock-ene-geography.md). Center-to-center
bearings, ray/footprint intersections, an extended line, a walking route and a
midpoint construction answer different questions. Neither proximity nor an
intersection establishes intentional placement or a Kryptos link. No initials,
keyword, cipher dimension, plaintext or new numerical key was extracted.

The supplied map deliverable `clock_axis_verified.png` was separately saved in
Library and visually checked by the parent research task. It includes snapshot
dating, the historical pavilion as a separate orange feature, north arrow, scale
and the station near-miss. This documentation step did not materialize or upload
that image, so no repository image path or byte-verification claim is made.

[Structured supplied-review receipt](../sources/world-clock-exact-axis-review.json).
[Inauguration/dedication astronomy](inauguration-dedication-astronomy.md) records
a separate date hypothesis; these intersections were not selected from an
astronomical alignment or used for a cipher test.

## Building commonalities: a historical baseline, not a key

The real commonality is the area's **late-1960s GDR redevelopment**, with older
art incorporated into a planned ensemble:

| Feature | Historical role/date in the supplied review | Relevance to the exact axis |
| --- | --- | --- |
| Haus der Statistik | central state statistical administration; built 1968–70 | ENE footprint hit; already identified earlier |
| Fernsehturm | broadcasting tower; built 1965–69 | shaft misses the ray |
| Tower's surrounding pavilions | exhibition/restaurant; built 1969–72 | WSW historical footprint hit |
| Neptunbrunnen | sculpture from 1891, relocated here in 1969 | basin intersected off-centre |

The construction dates are supported by [BIM](https://www.bim-berlin.de/landesimmobilien/projekte/haus-der-statistik)
and the [heritage record](https://denkmaldatenbank.berlin.de/daobj.php?obj_dok_nr=09065023,T);
the [fountain record](https://denkmaldatenbank.berlin.de/daobj.php?obj_dok_nr=09011281)
is the period-location source retained in the earlier geography note. The
statistical administration's original role must not be replaced with later
post-reunification Stasi-records use as if that were its 1989 function.

The heritage record describes a hexagonal pavilion/terrace plan and a **60°
planning angle relative to the tower's main axis**. This executor read that
passage. It is not a true-north bearing of 60°, nor the clock's 67.5° ENE ray.
The supplied review places Neptune at the intersection of the tower/town-hall
axes; that is another planning axis, not an interchangeable compass instruction.
Most directly, this ray hits exhibition/restaurant architecture, not the broadcast
shaft. A statistics/broadcasting/time interpretation is a broad thematic reading.

The [tower operator's history](https://tv-turm.de/en//history/) explicitly relates
the sphere to Soviet Sputnik satellites. That is documented space-age symbolism,
not a Mercury–Uranus plan. Neptune as sea god and the fountain's river figures
are not automatically references to the planet Neptune. The urban ensemble
provides a baseline explanation for nearby alignments, without specifying a
cryptographic extraction rule or establishing a Sanborn connection.

A future geographic test would need eligible labels, ordering and extraction
fixed beforehand, with adjacent-bearing comparisons. No arbitrary building-name
initials, new target line or cipher-key search was introduced in this update.
See the [deeper astronomical review](inauguration-dedication-astronomy.md#deeper-conjunction-review--18-october-2026)
for the separate coordinate-frame and historical-intent limits.
