# Kryptos Light Laboratory — complete version 19 source archive

Archived 31 October 2026 UTC from the canonical Sites Git repository. This is a **complete, unchanged tracked-source snapshot**, not a feature delta or reconstruction from the rendered website. It includes the existing version 18 curved-screen/ideal-mirror feature and version 19 mobile-containment correction.

## Provenance

- Live Site: [Kryptos Light Laboratory](https://kryptos-light-laboratory-rc2026.milky-lion-6014.chatgpt.site).
- Sites project: `appgprj_6ada06694004819191214801c8b9a3b4`.
- Latest saved version verified on 31 October: **19**, `appgprj_6ada06694004819191214801c8b9a3b4~appgver_f6bc775e4b3c8191b3635a57f6dbe48f`.
- Exact source commit: `5b7e88365f174106ef7a7f290a0bdcc671014f01`.
- Exact source tree: `1ade30cf983302a6f27d0ffee4f54c08353b9611`.
- Source commit time: 24 October 2026, 15:07:03 UTC. This is not the publication time.
- Sites deployment `appgdep_6adcc9affe688191b05e4786762f8937` reports **succeeded**, updated 24 October 2026 at 15:08:24.119459 UTC, at the URL above.
- Public access revision **2** is unchanged. This repository archival operation made no Site source push, save, deployment, or access change.

## Contents and integrity

[**source.tar.xz**](source.tar.xz) contains all **450 tracked regular files**, totaling **7,850,463 uncompressed file bytes**, under `source/`. Compressed size: **1,626,832 bytes**.

Archive SHA-256:

```text
bd1acf9a475f48016c20c836d467171cb3a77f5454088375352db120c58d93ed
```

[Source manifest](SOURCE_MANIFEST.json) records every original path, mode, byte length, Git blob SHA-1 and SHA-256, plus the Site/source provenance. [Per-file SHA-256 checksums](SOURCE_SHA256SUMS) allow independent verification after extraction; [archive-package checksums](ARCHIVE_SHA256SUMS) cover this guide and the three payload/manifest files.

Static verification established that every archive member matches the canonical Git blob, that all 450 tracked files are present exactly once, and that paths/member types are safe. The tar's Git commit marker matches the source commit. Sites' saved-version source hash independently matches that commit. The separate Sites deployment tar was not byte-compared: its bytes were unavailable to this archival task. This archive is the verified source snapshot, not a copy of that deployment bundle.

Targeted filename/content review, including an independent read-only review, found no credentials, private unrelated files, or build caches. No Git metadata/history, authentication responses, untracked files, installed dependencies, or unrelated raw research logs are included. The tracked `dist/validation/` routes are intentional frozen browser-QA assets, not disposable build caches, and are preserved.

## Restore locally

From this archive directory, with `tar`, `xz` support, Python 3 and (for tests) Node.js 20 or newer:

```sh
shasum -a 256 -c ARCHIVE_SHA256SUMS
mkdir restored
tar -xJf source.tar.xz -C restored
(cd restored && shasum -a 256 -c ../SOURCE_SHA256SUMS)
python3 -m http.server 8173 --bind 127.0.0.1 --directory restored/source/dist
```

Open `http://127.0.0.1:8173/`. The current static application has no package-install or build step. To run its retained automated suite separately:

```sh
cd restored/source
node --test tests/*.test.mjs
```

Use `dist/` for the published release, not the separately retained `candidate/` development copy. Historical build/promotion scripts reference earlier Git commits; a source-only snapshot does **not** restore that entire historical Git workflow. It does restore the current static application, source, assets, documentation, fixtures and tests.

The original `.openai/hosting.json` retains the existing Site identity for provenance. Do not use restore commands to overwrite or redeploy the live Site. Any later deployment requires separate authorization and the then-current supported Sites workflow; deploying a new independent copy also requires its own Site identity.

## Validation scope and historical wording

No application tests or browser QA were rerun for this archival-only operation. The original publication record reports 119 tests and completed parent cloud-browser responsive checks; those are historical results, not a new archival test run. Source documents remain byte-for-byte historical records: early references to owner-private access, older model versions, or pending QA do not override the verified version 19/public metadata above.

The laboratory remains an illustrative, unsurveyed research model, not physical calibration, a recovered encryption method, or a K4 solution. Existing [version 17](../projection-v17-20261024/README.md) and earlier feature-delta archives remain untouched.

