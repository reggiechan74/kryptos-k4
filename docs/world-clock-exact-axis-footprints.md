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

## Supplied extension to five kilometres in each direction

The read-only geometry worker extended the **same WGS84 geodesic**, from
52.5211638 N, 13.4133059 E with initial bearings 67.5° / 247.5°, to a bounded
**5 km in each direction**. Five kilometres is the review cutoff, not a chosen
landmark endpoint. The worker retrieved actual OSM nodes/ways and complete key
multipolygons through the main OSM API after Overpass errors. This executor
records the supplied intersections, without repeating the geometry computation
or claiming possession of the worker's raw polygons. Retrieval for this extension
was reported on 18 October 2026; the earlier nearby-map snapshot date does not
establish a uniform historical snapshot for the extension's API geometries.
A constant-bearing rhumb line is a different construction and differs by a few
metres at 5 km.

Distances below are approximate **along-ray groundplan ranges**, not distances
to feature centers, a walkable route or a 3D line of sight. Modern mapped identity
and polygon extent do not establish the corresponding 1989 feature or name.
The earlier nearby map is unchanged; no polished extension map was produced.

### ENE sequence beyond Haus der Statistik

| Approximate range from clock | Supplied intersection | Qualification |
| --- | --- | --- |
| 0.57–0.61 km | [Kindergarten, relation 546236](https://www.openstreetmap.org/relation/546236) | current mapped feature; historical identity unchecked |
| 0.70–1.20 km | housing | multiple groundplan features, not a single named endpoint |
| 1.24–2.28 km | [Volkspark Friedrichshain, relation 3099987](https://www.openstreetmap.org/relation/3099987) | hospital notch at about 1.76–1.82 km; not an uninterrupted park interior |
| 2.38–2.54 km | [Tesla-Schule grounds, way 42697319](https://www.openstreetmap.org/way/42697319) | grounds, not the same as the building footprint |
| about 2.39 km | [school building, way 508727544](https://www.openstreetmap.org/way/508727544) | historical building/name identity unchecked |
| 2.71–2.85 km | [Velodrom, way 7997184](https://www.openstreetmap.org/way/7997184) | opened August 1997; not a 1989 building |
| 3.51–4.06 km | [Volkspark Prenzlauer Berg, way 115704664](https://www.openstreetmap.org/way/115704664) | name dates to 1969; that does not certify identical period boundaries |
| beyond the park toward 5 km | housing | review ends at the fixed distance bound |

The [Velodrom's official facts](https://www.velodrom.de/location/daten-fakten)
confirm its August 1997 opening. The [Pankow park history](https://www.berlin.de/ba-pankow/politik-und-verwaltung/aemter/strassen-und-gruenflaechenamt/gruenflaechen/ausstellung/artikel.1513041.php)
is the source for the park's 1969 naming. These pages were read here; the
intersection geometry is attributed to the independent worker.

### WSW sequence beyond the nearby pavilion/fountain

This is a selected named-feature summary, not an inventory of every intervening
building. Ordinary blocks and other institutions occur between the listed
features; a gap in the table does not imply empty ground.

| Approximate range from clock | Supplied intersection | Qualification |
| --- | --- | --- |
| 0.57–0.77 km | [Marx-Engels-Forum grounds, way 16872940](https://www.openstreetmap.org/way/16872940) | grounds hit, not necessarily the statues |
| 0.77–0.80 km | [Spree, relation 6306415](https://www.openstreetmap.org/relation/6306415) | water footprint |
| 0.81–0.87 km | [mapped razed Palast der Republik footprint, way 229531166](https://www.openstreetmap.org/way/229531166) | historical OSM evidence only; official period-map retrieval failed |
| 1.06–1.10 km | [Spreekanal, relation 7388656](https://www.openstreetmap.org/relation/7388656) | clips [Schloßbrücke, way 339201218](https://www.openstreetmap.org/way/339201218), around 1.06–1.07 km |
| 1.12–1.16 km | [Kommandantenhaus, way 15976890](https://www.openstreetmap.org/way/15976890) | current reconstruction opened 2003 |
| 1.17–1.24 km | [Kronprinzenpalais, relation 4284350](https://www.openstreetmap.org/relation/4284350) | two building segments with a small recess; rebuilt 1968–70 |
| 1.248–1.262 km | [Prinzessinnenpalais, way 24247322](https://www.openstreetmap.org/way/24247322) | rebuilt/interiors reconstructed 1962–64 |
| 1.332–1.388 km | [Staatsoper, way 15976892](https://www.openstreetmap.org/way/15976892) | reopened 1955 |
| 1.393–1.457 km | [Bebelplatz, way 205728152](https://www.openstreetmap.org/way/205728152) | paved square, not a building |
| 2.91–2.98 km | [Henriette-Herz-Park, way 49679770](https://www.openstreetmap.org/way/49679770) | current mapped grounds |
| 3.01–3.06 km | northern Sony Center buildings: [way 216228631](https://www.openstreetmap.org/way/216228631), [way 13649546](https://www.openstreetmap.org/way/13649546) | modern OSM names; no pre-1989 identity inferred |
| 3.10–3.15 km | [Musikinstrumenten-Museum, way 22990151](https://www.openstreetmap.org/way/22990151) | present site since 1984 |
| 3.17–3.26 km | [Philharmonie, complete relation 3626485](https://www.openstreetmap.org/relation/3626485) | opened 1963 |
| 3.35–3.40 km | [Kunstgewerbemuseum, relation 28134](https://www.openstreetmap.org/relation/28134) | building opened 1985 |
| 3.45–3.53 km | [Kulturforum entrance/exhibition building, way 143367746](https://www.openstreetmap.org/way/143367746) | historical eligibility unchecked |
| 3.56–3.62 km | [Gemäldegalerie, relation 3626233](https://www.openstreetmap.org/relation/3626233) | current building opened 1998 |
| 3.66–3.67 km | [Egyptian Embassy building, way 24045732](https://www.openstreetmap.org/way/24045732) | historical eligibility unchecked |
| 3.76–3.78 and 3.84–3.87 km | Bendlerblock wings: complete [relation 1687694](https://www.openstreetmap.org/relation/1687694), [relation 7903504](https://www.openstreetmap.org/relation/7903504) | complex predates 1989; exact wing continuity needs a period map |
| 3.98–3.99 km | [Bundeswehr Memorial, way 53103481](https://www.openstreetmap.org/way/53103481) | do not assume pre-1989 eligibility |
| 4.12–4.16 km | Calandrelli-Anlage | current mapped grounds |
| 4.16–4.23 and 4.45–4.50 km | Landwehrkanal crossings | separate water intersections |
| onward to 5 km | buildings around Lützowplatz and Keithstraße | fixed review cutoff, not an endpoint selected for significance |

The complete modern [Humboldt Forum relation 3007958](https://www.openstreetmap.org/relation/3007958)
**misses the ray by about 27 m**. It must not replace the separately mapped
razed Palast footprint as if their geometry were interchangeable. The Palast
intersection has no independent period-map confirmation in this review because
the attempted official map retrieval failed.

Chronology sources: [Bertelsmann/Kommandantenhaus](https://www.bertelsmann.com/de/unternehmen/unternehmensprofil/bertelsmann-in-berlin/),
[Kronprinzenpalais monument record](https://denkmaldatenbank.berlin.de/daobj.php?obj_dok_nr=09095949),
[Prinzessinnenpalais monument record](https://denkmaldatenbank.berlin.de/daobj.php?obj_dok_nr=09095951),
[Staatsoper history](https://www.staatsoper-berlin.de/de/staatsoper/unter-den-linden/geschichte/),
[Musikinstrumenten-Museum institutional history, PDF p. 2](https://www.simpk.de/fileadmin/user_upload_sim/Dokumente/Museum/Sammlung/Fuehrungsblaetter_EN/FB_12_MIM_GB_pre.pdf),
[Philharmonie history](https://www.berliner-philharmoniker.de/ueber-uns/philharmonie-berlin/architektur/),
[Kunstgewerbemuseum](https://www.smb.museum/museen-einrichtungen/kunstgewerbemuseum/ausstellungen/detail/ein-haus-fuer-angewandte-kuenste-mode-und-design/),
[Gemäldegalerie](https://www.smb.museum/museen-einrichtungen/gemaeldegalerie/ueber-uns/profil/)
and the supplied [Bendlerblock history](https://www.gdw-berlin.de/ort-der-erinnerung/der-bendlerblock).
This executor verified the cited year passages for the first eight; its
Bendlerblock-page extraction did not return the searched passage, so that
historical assessment remains attributed to the supplied review. Dates establish
site/building chronology, not identical 1989 polygons or every wing's continuity.

[Structured extension receipt](../sources/world-clock-axis-5km-extension-review.json)
preserves supplied ranges and historical limits. No new broad sweep, landmark
initials, preferred terminal feature, map rendering or cipher-key test was
introduced in this documentation update. The unchanged origin, bearings and
5-km bound—not a desired destination—define the extended geometry.
