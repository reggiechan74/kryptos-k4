# Reproduction inputs and execution order

The saved maps and tables are the archived deliverables. `legacy/` contains the
25 available analysis and drawing scripts, with only environment-specific
import/search paths made portable. `script_provenance.json` records original
and edited hashes. No analytical algorithm was changed.

**This is not a one-command, fully offline reconstruction.** Large raw global
datasets and some selected source polygons are deliberately omitted. Live
source services can change. The three delivered, caveat-enriched CSV exports
are preserved artifacts; the original export wrappers were not present among
these 25 scripts. Intermediate CSVs produced by the analysis are not identical
to those delivered CSVs.

## Checks that work without external packages or downloads

```sh
python3 repro/validate_spherical_route.py
# Optional: override the bundled route file location.
python3 repro/validate_spherical_route.py --route PATH/TO/route.geojson
```

The saved `portable_validation.json` was generated against the archived route:
80,002 vertices, two antimeridian-split parts. This independently checks the
spherical forward formula, closure, initial bearing, and the vertices' distance
from the great-circle plane. It does not verify boundaries, imagery, real-Earth
accuracy, or survey-grade physical touches.

## Prepare a disposable working tree

Copy `legacy/` into a separate work directory. Stage all needed files below at
their original relative paths in that copy; the scripts read and write beside
themselves. Do not run analysis in a repository's archived artifact directory.
Several scripts import `compute_route.py`, which performs calculations and
rewrites derived outputs at import time. `validate_route.py` also rewrites a
source manifest; retain the archived manifest rather than replacing it.

Use Python 3.12 and the versions recorded in `requirements.txt` as a starting
point. Those versions were observed in the source environment, not tested by a
clean installation on every platform. Exact figure bytes also depend on fonts,
Matplotlib rendering, output metadata, and platform. Do not claim byte-identical
regeneration merely because the geometry agrees.

For each omitted input use its published URL and SHA-256 from the bundled source
manifests. Verify the downloaded bytes **before** use. A hash mismatch means a
different source snapshot; do not silently update a historical result. Sources
without an immutable download URL cannot be guaranteed retrievable at the old
version. Record the new retrieval date and version if intentionally recomputing
against newer inputs. Respect access failures and source usage limits; do not
bypass them. No fetch script is run automatically by the validation script.

## Required inputs and pipeline

All paths in this section are relative to the staged `legacy/` copy.

### Global model and overview/country maps

`compute_route.py` requires these Natural Earth snapshots at the root:

- `ne_10m_admin_0_countries.geojson`
- `ne_10m_populated_places.geojson`
- `ne_10m_geography_regions_polys.geojson`
- `ne_10m_geography_marine_polys.geojson`
- `ne_10m_geography_regions_points.geojson`

Additional input for `compute_unesco.py`: `unesco_world_heritage.json`.
Additional inputs for `compute_waterways.py`:
`ne_10m_rivers_lake_centerlines.geojson` and `ne_10m_lakes.geojson`.
The eight input URLs, retrieval date, sizes and hashes are in the root source
manifest. Natural Earth's `master` URLs are mutable; the hashes identify the
retrieved bytes, not an immutable remote commit.

```sh
python3 compute_route.py
python3 build_crossings_layer.py
python3 compute_unesco.py
python3 compute_waterways.py
python3 validate_route.py
python3 draw_map.py
python3 draw_crossings_map.py
```

These produce `route.geojson`, `route_results.json`, the country intersection
layer, nearby point intermediates, `waterways.json`, and the first two map
PNG/SVG pairs. The draw scripts need the country source polygons even when
the derived route and results are already present.

### European checks and Kremlin comparison

Stage the selected raw European inputs in `europe-footprints/`. The European
source manifest lists names and hashes; public OSM IDs/versions/timestamps are
also retained in result metadata. Required categories:

- `*_nominatim.json` candidate polygon responses (the archived candidates,
  not arbitrarily substituted current search matches);
- `berlin_heritage_official.geojson`, `paris_unesco_official.geojson`,
  `unesco_layer1_official.geojson`, `unesco_layer2_official.geojson`;
- `kremlin_bbox_small.osm` for building reconstruction;
- `relation_1360641.osm`, `relation_1577673.osm`, `relation_1149002.osm`,
  `relation_7392626.osm`, `osm_relations_metadata.xml`,
  `osm_ways_metadata.xml` for version enrichment during finalization.

`fetch_candidates.py` and `fetch_additional.py` preserve some of the original
public Nominatim queries; they are not a complete historical raw-input fetcher.
Official query URLs and OSM object IDs must be taken from the source metadata.
Do not rerun these fetchers as bulk or parallel Nominatim retrieval jobs.

```sh
python3 europe-footprints/verify_footprints.py
python3 europe-footprints/verify_official.py
python3 europe-footprints/verify_unesco.py
python3 europe-footprints/verify_kremlin_buildings.py
python3 europe-footprints/finalize_europe.py
python3 europe-footprints/validate_europe.py
python3 europe-footprints/compare_wgs84.py
python3 europe-footprints/draw_kremlin_comparison.py
```

The comparison draw script imports `draw_kremlin.py`, so it also writes the
earlier Kremlin ground-intersection figure. It needs
`moscow_kremlin_nominatim.json`, `red_square_nominatim.json`,
`kremlin_buildings.geojson`, and `wgs84_comparison.json`.

### Non-European targeted checks

Stage in `footprints-non-europe/`:
`gondwana_official.geojson`, `bounty_reserve.geojson`,
`main_range_park.geojson`, their matching `.url` text files,
`san_agustin_osm.json`, `cebu_boundary.geojson`, and
`santa_ana_church.geojson`. `check_footprints.py` consumes these and the root
`route.geojson`. Some missing optional source files are silently skipped by that
legacy script: verify the expected nine feature checks rather than treating
successful exit alone as complete reproduction.

```sh
python3 footprints-non-europe/check_footprints.py
```

`fetch.py` and `fetch_more.py` retrieve only part of the public raw source set.
The original conversion wrappers that prepared the Cebu boundary and Santa Ana
church polygons were not found. Preserve their documented provenance and
archived geometries when available; otherwise reconstruct from the stated
source objects and verify against the original hashes before claiming exact
reproduction. `source_manifest.json` in this subdirectory distinguishes raw
source responses from derived files (derived entries can have a null URL).

### Published UNESCO boundary pass

Review source terms and applicable permission first (see `NOTICE.md`); public availability is not itself a redistribution license. With the root route ready, the following optional network step sends the full
defined line to the official published core/buffer polygon service. It reads
public data and changes no server records. It is a new query of today's service,
not a guarantee of the archived 2026-10-24 snapshot.

```sh
python3 unesco-boundary-pass/query_global_intersections.py
python3 unesco-boundary-pass/analyze_intersections.py
```

For an offline historical analysis, stage the archived
`layer1_route_hit_polygons.json` and `layer2_route_hit_polygons.json` instead.
Coverage metadata and precision flags must be retained; the service does not
publish every UNESCO property polygon. Missing or restricted geometry remains
untested, not a confirmed miss.

### Integrated atlas

Required results: root `route_results.json`, `route.geojson`,
`country_polygon_intersections.geojson`, `waterways.json`;
`europe-footprints/EUROPE_FINAL_FOOTPRINTS.geojson`;
`footprints-non-europe/footprint_results.json` and `verified_footprints.geojson`;
`unesco-boundary-pass/official_unesco_intersection_results.json` plus both
`layer*_route_hit_polygons.json` files. Root country and lake source polygons
are also required for the draw script.

```sh
python3 integrated-intersections/build_inventory.py
python3 integrated-intersections/draw_verified_map.py
```

The archived inventory has 147 rows. That count is a regression reference for
the archived inputs, not a target to force on later or different datasets.
The available atlas script writes PNG only; no original atlas SVG was present.

## Verification status

- All 25 portable legacy scripts were parsed successfully with Python's AST.
- The standard-library validator passed against the archived route.
- Full clean-environment rebuilding, source redownloads, and image byte-for-byte
  regeneration were **not** performed for this bundle.
- Original computed validation artifacts remain separate from the independent
  portable validation; neither certifies real-world source-boundary accuracy.
