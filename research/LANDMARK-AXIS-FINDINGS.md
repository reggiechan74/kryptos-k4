# LANDMARK-AXIS-001: independent regional exploratory comparison

19 October 2026. **The exact 67.5°/247.5° axis scores above the median in the
frozen sample, but is not uniquely aligned.** It intersects four canonical sites;
the full-cycle median is two, maximum six, and **13.666% of orientations** intersect
at least four. This is a descriptive rotational comparison, **not a discovery
p-value or evidence of designer intent**. The target was already noticed.

Most importantly, this tests **documented pre-1990 site existence using modern
protected footprints**. No independent pre-1990 outline was verified for this
regional sample. A strict historic-footprint test therefore remains unresolved.
No landmark-derived key or unrelated cipher experiment was run.

## Frozen design and independent source

The [specification](specifications/LANDMARK-AXIS-001.json) was committed before
comparative scores at `333ff330be8078de16584960d1aa9d59949360ce`.
Origin is 52.5211638 N, 13.4133059 E, with WGS84 geodesic initial bearings
67.5°/247.5° and a 5,000 m bound on each ray. One canonical site can count at most
once on the paired axis; directional counts are also retained. The full comparison
covers 0.00–179.99° in 0.01° steps, plus continuous angular-interval measures.
The fixed local robustness window is ±10°. Nearby bearings are correlated,
not independent trials. There is no preferred endpoint beyond the distance bound.

The earlier corridor's hand-picked landmarks are **not the comparison inventory**.
Instead this uses the official [Berlin Denkmale WFS](https://gdi.berlin.de/services/wfs/denkmale)
([official service metadata](https://gdi.berlin.de/geonetwork/srv/api/records/12f0f9ed-5430-345a-a313-7421a99335c0)).
A surrounding-region query returned **3,433 complete features**, with
`numberMatched=numberReturned`, no next page, native EPSG:25833 multipolygons.
The response timestamp is **2026-10-19T03:07:19.101Z**. Source capabilities state
Datenlizenz Deutschland Zero 2.0 and no access restrictions. This is a current
heritage inventory, not an exhaustive inventory of all historically interesting
regional features.

Rules include Baudenkmal, Gesamtanlage and Gartendenkmal; they exclude urban
Ensemble administrative areas and subsurface Bodendenkmal. Root official IDs
combine multipart records. Geometric containment clusters merge nested units,
retaining constituent IDs. Partial overlaps remain distinct; administrative
identity across disjoint IDs can still be imperfect. Two sites containing the
clock origin are excluded to avoid a trivial hit at the start of every ray.
Footprints touching the disk qualify even when their centroid is outside it.

A deterministic **SHA256-ID ordering** selects the first 200 disk-eligible canonical
sites, without reference to bearing or old corridor names. This covers the region
independently of the chosen axis, but is a bounded heritage subset, not a random
sample of every Berlin landmark. There were 2,103 native-disk candidates and
2,054 containment clusters before precise radial filtering; these are conservative
prefilter counts, not an asserted exact population size. Only 201 precise tests
were needed to select the first 200 eligible hash-ordered sites.

The frozen inventory/source excerpts were committed **before scoring**, at
`63fa98dfa39a846b125d9f7414631fdf8b477171`. Its gzip SHA256 is
`ea0e8cc45a9b157e6358ff22e8adc1ab73140eaf585506ed7251dec4fa55289d`.
All **206 requested official record pages** were retrieved. Strict primary
Fertigstellung/Datierung fields qualify a completed date/range ending by 1989;
Entwurf alone does not. Ambiguous or missing date fields remain uncertain.
No axis-conditioned historical research was added to rescue selected sites.

| Historical stratum | Sites | Use |
| --- | ---: | --- |
| H0: independently verified historic outline | 0 | strict historical-outline result not estimable |
| H1: pre-1990 existence, modern geometry proxy | 175 | primary descriptive comparison |
| U: uncertain chronology | 24 | reported separately; excluded from primary |
| POST: primary completion/date after 1989 | 1 | excluded from pre-1990 comparison |

A site's original completion year does not certify that its current outline is
unchanged through reconstruction, extension or demolition. The date-row excerpts,
response hashes and every inclusion/classification are retained, not silently
promoted to historic geometry.

## Results

| Measure | Full 180° cycle | Fixed ±10° window |
| --- | ---: | ---: |
| Grid orientations | 18,000 | 2,001 |
| Target paired-axis count | 4 | 4 |
| Median count | 2 | 1 |
| Maximum count | 6 | 4 |
| Target minus median | +2 | +3 |
| Orientations with equal/higher count | 13.6667% | 9.5452% |
| Strict rank, 1 = no better orientation | 893 | 1, tied |
| Orientations tied at target score | 1,568 | 191 |

The continuous angular-interval result is **13.66635%** equal or higher, almost
identical to the grid. This is a fraction of orientations under fixed data/rules,
not a chance probability. The target is tied for the local maximum and not the
unique optimum. For example:

| Initial bearing / reverse | H1 paired count |
| --- | ---: |
| 0° / 180° | 2 |
| 22.5° / 202.5° | 2 |
| 45° / 225° | 1 |
| 62.5° / 242.5° | 2 |
| 66.5° / 246.5° | 3 |
| 67° / 247° | 3 |
| **67.5° / 247.5°** | **4** |
| 68° / 248° | 3 |
| 68.5° / 248.5° | 4 |
| 72.5° / 252.5° | 0 |
| 90° / 270° | 1 |
| 112.5° / 292.5° | 2 |
| 135° / 315° | 0 |
| 157.5° / 337.5° | 1 |

All four sampled hits lie on the **WSW** ray; ENE has zero sampled H1 hits.
This is not a denial of earlier independently verified ENE landmarks: the
predeclared hash sample does not force those corridor-selected sites into it.

| Canonical site | Official subject / counting class | Primary completed date |
| --- | --- | ---: |
| [Deutsche Bank, 09080262](https://denkmaldatenbank.berlin.de/daobj.php?obj_dok_nr=09080262) | bank; mixed protected complex | 1874 |
| [Schloßbrücke, 09030067](https://denkmaldatenbank.berlin.de/daobj.php?obj_dok_nr=09030067) | bridge/figure group; built-footprint class | 1857 |
| [Prinzessinnenpalais, 09095951](https://denkmaldatenbank.berlin.de/daobj.php?obj_dok_nr=09095951) | government building; built footprint | 1730 |
| [Berliner Handels-Gesellschaft, 09080268](https://denkmaldatenbank.berlin.de/daobj.php?obj_dok_nr=09080268) | bank; built footprint | 1900 |

The bridge is a built footprint, not a generic solid ground-level obstruction.
The palace's original date does not replace its reconstruction history. No hit
is automatically a 3D sightline or an unobstructed pedestrian route.

Predeclared class diagnostics, not a selection of the most attractive subset:

| Class | Eligible sites | Target | Median | Maximum |
| --- | ---: | ---: | ---: | ---: |
| Built footprints (including bridge) | 127 | 3 | 1 | 4 |
| Compact monuments | 2 | 0 | 0 | 1 |
| Garden/grounds | 4 | 0 | 0 | 2 |
| Mixed complexes | 42 | 1 | 1 | 4 |

The 24 uncertain sites contribute zero target hits, versus a full-cycle maximum
of two; they are not mixed into the historical proxy score. There is no claim
that this bounded heritage sample represents parks/plazas or monuments uniformly.

## Numerical checks, robustness and missing sensitivity

Native polygon edges are densified and mapped to an origin-centered geodesic
azimuthal-equidistant frame; rays are radial there. All multipolygon rings,
including holes, are retained. Segment/disk clipping and merged angular support
implement the **unbuffered closed-footprint intersection criterion**, including
boundary contacts. The implementation uses numerical polygon approximation,
not surveyed exactness.

The primary edge spacing is 5 m. Repeating at **2.5 m** changes **zero of 18,000
counts**, including the four target hits. A 0.02° grid gives median two, maximum
six and 13.7% equal/higher. Continuous interval measures avoid depending on a
single grid step. These checks establish numerical convergence for the data;
they do not verify the historical outlines or map accuracy.

Two hits are close to direction boundaries: Schloßbrücke is about **0.0863°**
from its nearest interval edge, Berliner Handels-Gesellschaft about **0.0470°**.
Mapped-origin error, ETRS89/WGS84 epoch differences or changed source outlines
can matter. The frozen 5 m/10 m metric-buffer sensitivities were **not computed**:
there is no independently validated buffering implementation in the available
stdlib-only environment, and the predeclared fallback permits omission rather
than substituting an undeclared angular buffer. This is a material limitation,
not evidence that those nearby hits are physically robust.

**Eight geometry/metadata/statistics tests pass** in 0.013 s. Controls include
independently server-reprojected official coordinates (maximum observed discrepancy
0.00525 m), separate meridional-curvature integration, equatorial distance,
Vincenty direct/inverse, holes/multiparts/nesting, a centroid-outside disk hit,
endpoint/tangency contacts, brute-force synthetic ray/segment comparisons and
date parsing that excludes design-only and subobject dates. Existing cipher
modules and the earlier 133-test baseline were not changed; unrelated cipher
tests were not rerun for this task.

The final scoring run took **3.708404 s** under the 180-second cap. After the first
run, only the predeclared class diagnostics and boundary-margin reporting were
completed; the selection, primary metric and every primary count remained
unchanged. Final implementation commit:
`53cd50ad85e443c4f22f59aa4f0115c6ba5047f2`.

## Reproduction, source retention and publication status

```sh
python3 -m unittest discover -s tests -p test_landmark_axis.py -v
python3 experiments/landmark_axis.py --spec-commit 333ff330be8078de16584960d1aa9d59949360ce --inventory-commit 63fa98dfa39a846b125d9f7414631fdf8b477171 --code-commit 53cd50ad85e443c4f22f59aa4f0115c6ba5047f2
python3 experiments/check_landmark_receipts.py
```

The frozen selected inventory and source-date excerpts are already on the remote
branch. Full regional raw geometry is archived as eight reconstructable hashed parts
under `sources/landmark-axis/`, with `region-parts.json` defining order and hashes.
Concatenating `official-region.geojson.gz.part000` through `.part007` restores
the 3,949,292-byte `official-region.geojson.gz`; the unsplit local copy is redundant. Local offline verification reconstructs all
3,433 source features, reproduces the same 200 canonical IDs/polygons, reparses
206 date-row excerpts and confirms every chronology stratum. The full raw response
SHA256 is `752249a2d206083be667d0987a4b74bfc7851b0c3fdd2d44b4330fc3ffe3c1e3`.
The public source has only official `gisid/id/link/typ` properties and polygons;
it contains no private research/cipher or credential fields.

**Publication:** this report, results and the eight-part public Berlin source
archive are included together in this publication commit, authorized by the user
on 19 October 2026. Earlier upload attempts were stopped by automatic approval
review; they did not update the public branch. The source archive and selected
inventory have been verified offline again before this publication.

[Result](../results/landmark-axis/LANDMARK-AXIS-001.json),
[full orientation grid](../results/landmark-axis/orientation-grid.csv.gz),
[site intervals and target identities](../results/landmark-axis/site-intervals.json.gz),
[offline source check](../results/landmark-axis/OFFLINE-RECEIPT-CHECK.json),
[validation](../results/landmark-axis/VALIDATION.json).

The result supports an above-median alignment in this particular modern-geometry
heritage proxy. It does not establish that the axis is exceptional in a complete
historical landmark inventory, that the exact bearing was intended, or that it
encodes Kryptos. A stronger historical test needs independently verified period
outlines across the comparison region, with a new design frozen before examining
its scores—not extra landmarks selected because they favor this axis.
