# Reproducible results

Each experiment is scoped in [the log](../research/EXPERIMENTS.md) and
[bounded specification](../research/BOUNDED-SPEC.md). No K4 solution is claimed.

| Artifact | Content |
| --- | --- |
| CTRL-001.json | All complete K1/K2/K3 fixture comparisons and hashes |
| STRUCT-001.json | Exact count and periodic-bijection witnesses, encoding feasibility |
| ROUTE-001-summary.json | Case counts, compatible periods, code/input hashes |
| ROUTE-001.json.gz | Complete route catalogue and all partial key assignments |
| RUNKEY-001.json | Literal-window counts, descriptive match histogram, no survivors |
| TRIFID-001.json | Fixed cubes/periods, no survivors |
| STAT-001-summary.json | Observed lag counts, calibration parameters, corrected tails |
| STAT-001.json.gz | All 9,999 null draws and 5,000 evaluation maxima |

Compressed files are ordinary UTF-8 JSON compressed by Python's standard-library
gzip with mtime zero. The summary records the uncompressed SHA256. For example:

```sh
python3 -m gzip -d -c results/ROUTE-001.json.gz
```

Use the commands in the experiment log to regenerate artifacts. Elapsed time
and environment metadata may change; deterministic draws and substantive outputs
are fixed by the documented implementation and seed. Original ciphertext and
corrected variants remain separately named in `data/controls.json`.

## Audit preservation and current runners

The original files above are preserved byte-for-byte against
`data/audited-results-b83.json`. `AUDIT-001.json` records the focused validation.
Original run metadata is historical and refers to the code at its recorded
commit, not the subsequently hardened code. All 282 ROUTE-001 fits are vacuous
with zero repeated-phase comparisons; they are not positive candidates.

New replay commands require `--spec-commit FULL_SHA` and write unique directories
under `results/runs/`. Read `latest.json`, then the referenced `manifest.json`.
Only `status: completed` in that manifest makes its listed artifacts publishable.
A timeout, invalid baseline, interruption, or exception publishes an incomplete
manifest with no result artifacts, preserving prior runs. An abrupt process kill
may leave a hidden pending directory and a running pointer; neither is complete.
The original specification and results shared a commit; future new specs must
be committed first, with chronology checked from Git history. The offline runner
records a supplied full SHA and the local spec hash; it cannot itself prove that
the commit exists, contains those bytes, or predates execution.

## New preregistered finite branches

- `language-runs/`: GOST37,060roundtrips and Shavian feasibility gates.
- `masking-runs/`: the12 autokey and2 Fractionated Morse pilot records.
- `word-runs/`:24 endpoint/interior-multiset compatibility checks.

Each directory has an atomic latest pointer and immutable run manifests with
prior specification/code commits and exact hashes. Source/specification/result
links are in the three new findings documents linked from the root README.
These specifications genuinely precede the runs in Git history; the older b83
registration limitation remains unchanged and is not retroactively repaired.

`phonetic-subset-runs/` records the subsequent deterministic length-preserving
respelling check. Current overall verification is
[SEQUENTIAL-BRANCHES-VALIDATION.json](SEQUENTIAL-BRANCHES-VALIDATION.json),77tests.
The earlier73test record remains historical. The chronology receipt now covers
all5new runs, each with a genuinely prior specification and code commit.


## Current navigation

See the [project overview](../README.md), [hypothesis tracker](../docs/tracking/HYPOTHESES.md), [experiment tracker](../docs/tracking/EXPERIMENTS.md) and [receipt index](../docs/tracking/RECEIPTS.md). Older entries above are retained historical documentation; current exact scopes live in the canonical ledger.

## Item 1: full integer row/column overlay

[Immutable original run and guides](fold-slide-2d-001-runs/README.md), [all-frame CSV](FOLD-SLIDE-2D-001-frames.csv), [export identity](FOLD-SLIDE-2D-001-export.json), [pre-evaluation controls](FOLD-SLIDE-2D-PRE-EVALUATION-CONTROLS.json), and [separately timestamped post-run supplement](FOLD-SLIDE-2D-CONTROL-SUPPLEMENT-001.json). Native manifests record actual UTC boundaries; row-zero is prior coverage, not an additional independent discovery. The gzip CSVs retain all labels and positive surrogate intersections. [Findings](../research/FOLD-SLIDE-2D-FINDINGS.md) explain the full-search calibration and unmeasured geometry limits.

[Item 2 conditional solar/light checks](physical-solar-002/README.md) retain original UTC run identity and all scenario values; no K4 decoder.

[Item 3 partial World Clock analysis](world-clock-003/README.md) preserves all conditional registrations and ambiguity domains with original UTC execution timestamps.

Item 4 retains [original unknown-anchor comparison](sigaba-unknown-anchor-024/README.md), [byte-mask correction](sigaba-unknown-anchor-024b/README.md) and [diagnostic failures](sigaba-unknown-anchor-diagnostic/README.md) separately.

## Item 5 checkpoint

[Original lamp/Greek receipts and all plants/nulls](lamp-greek-025/README.md), [independent complete-selector audit](LAMP-GREEK-025-INDEPENDENT-VALIDATION.json), [finite support/phase certificates](LAMP-GREEK-025-CERTIFICATES.json). Original run and post-outcome validation times are separate. No first-crib survivor, no significance claim.

## Item 6 checkpoint

[Item 6 run receipts](tree-geometry-ipa-026/README.md) preserve the failed pre-K4 control attempt separately from the complete run, all 448 models, plants and nulls. [Independent post-outcome audit](TREE-GEOMETRY-IPA-026-INDEPENDENT-VALIDATION.json).

## Item 7 checkpoint

[Item 7 original conditional receipts](strip-source-gates-027/README.md), [post-source QA](ITEM7-HISTORICAL-SOURCE-QA-027.json), [local visual/access review](ITEM7-LOCAL-SOURCE-REVIEW.json). Zero strip-key enumeration; no completed historical inventory or universal exclusion.

## Final item 8 checkpoint

[Original one-edit run and maps](one-edit-028/README.md), [lossless preflight](one-edit-028-preflight/README.md), [independent actual/union audit](ONE-EDIT-028-INDEPENDENT-AUDIT.json). Large candidate volumes are non-identifiability, not search work or a solved message.

## Projection-concurrence diagnostic

[Projection diagnostic complete synthetic receipt](PROJECTION-CONCURRENCE-029-SYNTHETIC.json), [initial QA](PROJECTION-CONCURRENCE-029-INITIAL-QA.json) and [training-degeneracy correction](PROJECTION-CONCURRENCE-029-DEGENERACY-QA.json). Zero real correspondences/fits.

## Local deliberate-spelling study

[Original source analysis and controls](SPELLING-CORRECTION-032-ORIGINAL.json), [source retrieval hashes](SPELLING-CORRECTION-032-SOURCES.json), [independent reviewer comparison](SPELLING-CORRECTION-032-INDEPENDENT-REVIEW.json). No spelling correction of K4 is inferred.

## Local word-cover and phrase studies

[Core exact counts](COVER-EXTRACTION-033-ORIGINAL.json), [complete corpus summary](COVER-PHRASE-034-original-summary.json), lossless matched-reference/control gzip files, independent audit, source pins and Python3.12 replay preserve full finite coverage. See [interpretation and replay instructions](../research/COVER-PHRASE-034-FINDINGS.md). No actual K4 trials; local only.

## Ordinary prose cover follow-up

[Original035](PROSE-COVER-035-ORIGINAL.json), [independent full-domain audit](PROSE-COVER-035-INDEPENDENT-AUDIT.json) and [Python3.12 comparison](PROSE-COVER-035-PY312-COMPARISON.json): complete finite results, controls and calibration, no broad English/extraction exclusion or publication.

## Curved optical sampler

[Summary036](CURVED-SAMPLER-036-SUMMARY.json), full lossless original/replay and pose archives, independent ray/cell audits and nominal/failure Site fixtures preserve every finite outcome. Four tested utility cases fail stability;50other nominal cases remain untested for robustness. [Interpretation](../research/CURVED-SAMPLER-036-FINDINGS.md). No actual K4 evaluation or Site edit by this task.

## Exact Site cylinder follow-through

[Summary037](SITE-CYLINDER-037-SUMMARY.json), [all default margins](SITE-CYLINDER-037-DEFAULT-MARGINS.csv), full numeric source/original/replay archives and whole-process resource receipt preserve exact Source validation without bundling Site program code. Nominal validity and tiny-pupil subset passes do not prove manual robustness. [Interpretation](../research/SITE-CYLINDER-037-FINDINGS.md).

## Seven-family local review

New local 038–046 receipts preserve exact UTC original/replay times. [Coverage matrix](../research/SEVEN-FAMILY-REVIEW-046.md) maps them to narrow results and open gates; 044 profiles are counterfactual minimum sets, 045 maxima are not confirmed decryptions, and 046 controls are late supplements.

048–050original and replay receipts distinguish models, aliases, source occurrences and full plaintexts. Complete compressed route/operator catalogues preserve coverage; replay logs record wall/RSS separately. Empty048preflight means no message bank was generated. See [findings and prior scope](../research/048-050-PRIOR-COVERAGE.md).
