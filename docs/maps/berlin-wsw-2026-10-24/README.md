# Berlin WSW maps — 2026-10-24 research snapshot

Preserved map artifacts and bounded analysis for a route launched from Berlin's
World Clock at **52.521146530576253° N, 13.413309039143103° E**, with exact
nominal initial **true bearing 247.5°**. That public landmark is the model origin,
not a claim about anyone's location.

## Maps and tables

All four delivered PNGs are byte-identical to their saved Library originals:

1. [World overview](maps/Berlin-WSW-around-the-world.png).
2. [Direct country-polygon intersections](maps/Berlin-WSW-country-polygon-intersections.png).
3. [Kremlin: sphere versus WGS84](maps/Kremlin-sphere-vs-WGS84.png).
4. [Integrated footprint atlas](maps/Berlin-WSW-Mapped-footprint-crossings-and-misses.png).

The earlier ground-only Kremlin view is superseded by the two-model comparison
and intentionally omitted to avoid confusion. The modest comparison SVG is
included. The two approximately 19.8 MB world SVG originals are deliberately
omitted from this lean repository bundle; their exact hashes are recorded in
`maps/svg-manifest.json`. They remain preserved in the source workspace and a
separate all-SVG archive. Their drawing scripts are supplied. No atlas SVG was
created by the original workflow. No Git LFS or raw global dataset is required
to store or view this bundle.

`tables/` preserves the complete delivered CSVs:

- Nearby points: **104 rows** (57 city records + 47 UNESCO properties, aggregating
  171 matching reference/component-point records). **Not intersections.**
- Countries: **45 intervals in 17 distinct countries**.
- Integrated inventory: **147 rows**, including **34 tested footprint misses**.

`derived/` holds the computed route, clipped route segments, result inventories,
coverage metadata, and a separately identified OSM footprint extract. Rows can
overlap; do not sum across object categories.

## Interpretation is conditional

The principal route is a **closed great circle on a sphere**, radius 6371.0088 km,
length about 40030.229 km. It is neither a constant-bearing rhumb line nor a
WGS84 ellipsoidal geodesic. A same-initial-bearing WGS84 near-return passage
misses the mapped Kremlin grounds by approximately **1.344 km**, whereas the
spherical model crosses them. Narrow building clips are sensitive to bearing,
source geometry and Earth model, not established survey-grade physical touches.

A nearby reference point is not a property or city-boundary intersection. A
UNESCO **buffer** is not the **core property**. Administrative polygons are not
built-up urban footprints. Country polygons may include inland water. River
centerline crossings do not determine banks or channel width. The Bounty marine
reserve is water, not proof that island land is crossed. Natural Earth physical
label regions are geographic context, not accurate object boundaries.

## Coverage and unresolved questions

The published UNESCO service snapshot covered 2265 core-polygon features in
519 property-name groups, and 1146 buffer features in 347 groups—not all UNESCO
properties. Missing polygons are **untested**, not misses. Targeted regional
checks are not an exhaustive world landmark inventory. Unresolved complete
footprints include Santa Ana and San Agustin UNESCO property extents, the full
Bounty UNESCO marine-envelope crossing length, and Cebu's built-up area. Some
Potsdam/Berlin components and Kremlin/Novodevichy official core boundaries were
not available; source-specific substitutes are labeled. Data are contemporary
snapshots, not a reconstructed 1989 landscape. No cipher connection is proved.

## Verify and reproduce

```sh
python3 repro/validate_bundle.py
python3 repro/validate_spherical_route.py
```

The first command verifies archived SHA-256 hashes, required assets, table
counts and image structure. The second independently checks spherical formula,
bearing, closure and saved route vertices without third-party packages.
`manifest.json` inventories every payload file except itself.

See [repro/INPUTS.md](repro/INPUTS.md) before running the 25 preserved scripts.
They are portable with documented path-only changes, but this is **not a
one-command offline rebuild**: large raw sources and some source polygons are
omitted, source services are mutable, and some original conversion/export
wrappers were unavailable. Stage missing inputs in a disposable working copy;
never silently accept changed source hashes. Dependency versions are recorded,
not a cross-platform lockfile. Exact image regeneration was not claimed or tested.

## Provenance and rights

Source URLs, retrieval dates, available source versions and hashes are under
`provenance/`; original artifact Library identities are retained without
connector logs or account state. A SHA-256 identifies retrieved bytes, not an
upstream immutable release. No authenticated URLs, credentials, personal notes,
user-location data or large global source dumps are included.

**Read [NOTICE.md](NOTICE.md) and keep it beside these maps.** © OpenStreetMap
contributors; OSM-derived portions are [ODbL](https://www.openstreetmap.org/copyright).
DataHub UNESCO points and the separate Navigator polygon service have different
licensing evidence. Navigator public-reuse permission was not verified; this is
not a conclusion that all independent analytical maps are prohibited. Raw
Navigator polygon collections and combined copies are excluded. No blanket
license or unrestricted public-release clearance is asserted for this bundle.
