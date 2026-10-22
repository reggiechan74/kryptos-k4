# Fixed-key K4 occupied-cell route pilot

22 October 2026. **All 288 fixed branches fail the 24 confirmed crib letters.**
No candidate, decoding or solution. This separate pilot follows the completed
[frozen K3/clock batch](K3-CLOCK-ROUTE-FINDINGS.md), without changing its scope,
results or sixteen prior-equivalent skips.

## Scope and coverage before scoring

The local branch was clean after the preceding batch at
`7b13316714b6fa40fd118c30b0e311fe0819beb5`. The parent's methodology reviewer
proposed only the following finite occupied-cell family, which was then frozen.

The mask has four rows and 31 columns. Within K4, row 0 occupies zero-based
columns 27–30 (one-based 28–31, OBKR); rows 1–3 each occupy all 31 columns.
Indices 0–96 are assigned row-major over those 97 K4 cells. The preceding cells
of row 0 are **excluded from the K4 mask**, not claimed to be physical holes in
the copper; the published row contains the end of K3 and its separator there.
This is a test of carved textual layout, not surveyed aperture coordinates,
angles, sunlight or shadows.

The mask was checked exactly against `data/controls.json` panel rows and
`data/k4.json`: the first row is 31 characters ending OBKR at columns 28–31,
and the next three rows are each 31 characters. Their K4 portions reproduce
all 97 baseline characters. No padding, moved holes or repaired positions.

Four columnwise readings use ascending/descending columns and ascending/descending
rows within a column. Include the exact inverse of each: **eight distinct routes**.
Score-free full-permutation comparison found none in either the earlier 66-route
ROUTE-001 catalogue or the newer 97-route K3/clock catalogue. Prior unrestricted
period-8/10 additive KRYPTOS domains and both layer orders were checked: no stronger
prior negative covers these exact routes. Similar width alone is not equivalence.
The eight routes are not asserted to be new across all published literature.

Use only PALIMPSEST (10 cyclic phases) and ABSCISSA (8 cyclic phases), in the
fixed KRYPTOS alphabet with addition. Both cipher-layer orders:

```
C = T(V_k(P))
C = V_k(T(P))
k[i] = index_A(word[(i + phase) mod length(word)])
```

Eight routes x eighteen fixed phased keys x two orders = **288 raw and exact
unique new branches**, zero prior skips. Exact function signatures comprise the
complete 97-position source permutation plus the complete output-shift vector;
no duplicate branch is silently counted as independent. There are **zero fitted
parameters** per branch. The phases are predeclared enumerated models, not keys
fitted independently to plaintext letters. No other primer, phase, alphabet,
sign, route or layer was introduced.

## Chronology and outcomes

Specification: `29bf8e997b0290f56366ad27a7adb52a50ccb1b9`.
Implementation and controls: `6cc4b0d4b0d71002a55d59bd07a96c7d7ebe0332`.
The single actual run followed both commits and took **0.092467 seconds** under
its 15-second cap. The runner verified committed input/code bytes and prior
specification ancestry; an atomic snapshot preserves complete outputs, routes,
coverage records, controls and every case/phase.

| Literal key | Branches | All-crib candidates | Largest partial match |
| --- | ---: | ---: | ---: |
| PALIMPSEST, all 10 phases | 160 | 0 | 4/24 |
| ABSCISSA, all 8 phases | 128 | 0 | 5/24 |
| Total | 288 | 0 | 5/24 |

Score distribution: 0(111), 1(113), 2(49), 3(12), 4(2), 5(1).
The single 5/24 result, OCC-K-250, uses OCC-06, ABSCISSA phase 7, substitution
then route. Its matches at positions 22,27,64,66,68 give 2/13 East and 3/11 Berlin;
it fails **19 confirmed letters** and is rejected. It is descriptive bookkeeping,
not a lead or a reason to alter a key.

Every deterministic output re-encrypts all 97 ciphertext letters. That confirms
invertibility only; the outputs are labeled **rejected_model_output**, not decoded
plaintext. No training/key fitting was done; splitting the two known crib blocks
is diagnostic only, and neither is historically untouched evidence.

All cases fail the exact 24-letter gate, so **no additional null simulation was
needed or run** and no p-value is reported. No partial English or fitted letter
was used in acceptance. The result excludes exactly the declared eight routes,
two literal words/all eighteen phases and two layer orders. It does not exclude
other carved-text extraction rules, arbitrary periodic keys on these routes,
composite ciphers or surveyed physical effects.

## Controls and final verification

Before the actual run:

- All 288 planted 97-letter messages, containing both exact crib blocks, recover
  all letters and all 24 cribs; all 288 altered-crib negatives reject.
- All 288 encodings agree with a separate direct modular/index implementation
  covering both layer orders and every fixed phase.
- Eight unique-index mask controls verify every route/inverse against a separate
  explicit cell-fill/scatter implementation, including excluded cells/corners.
- All 676 plaintext/key single-symbol combinations round-trip in the fixed alphabet.
- Existing baseline and complete K1–K3 controls pass.

The saved-result audit independently re-encodes every **27,936 output letters**,
recomputes all matches, verifies all 288 exact function signatures, mask/coverage,
consulted hashes, chronology and absence of an unrequested null run. It also
compares the independent reviewer's simple sandwich contradictions against the
previous batch's unchanged saved equations.

**195 tests pass in 9.135 seconds**, preserving all earlier experiments and
source artifacts. [Validation receipt](../results/OCCUPIED-CELL-VALIDATION.json).
No actual experiment or null search was repeated by the suite. All changes remain
local; no public Site edit or remote push. This bounded pilot is complete, with
no additional family invented or parameter range expanded afterward.

## Independent earlier-batch cross-check, not new search coverage

The parent's independent reviewer reports reproducing all 336 K3 letters and
planted positives for all six K3-derived constructions. The reviewer independently
found all 384 raw clock structures contradicted by the first crib and passed
384 planted positives. These are attributed cross-check reports, not another
384 novel cases counted toward this executor's coverage. Our earlier accounting
remains **374 newly tested structures and 16 prior-equivalent skips**.

The reviewer's simple sandwich pairs were checked against our saved edges and
agree exactly; readable examples are now appended to the earlier findings.
Together the two separate batches added **662 actual new branches**, with sixteen
old equivalents recorded rather than rerun. These negatives supply no K4 lead.

The next decision should be based on an independently justified new mechanism
or constraint. No further search is authorized by a tempting partial match here,
and no further family was implemented in this batch.

## Reproduce

```sh
python3 experiments/occupied_cell_routes.py --spec-commit 29bf8e997b0290f56366ad27a7adb52a50ccb1b9
python3 -m unittest discover -s tests -v
```

The runner verifies consulted files against its recorded HEAD and creates a new
atomic snapshot; the implementation commit above identifies the exact version.
A read-only replay of `test_occupied_cell_artifacts.py` verifies existing results
without rerunning the experiment.

[Full result and rejected outputs](../results/occupied-cell-routes-001-runs/20261022T193953Z-6f4f8efe83e345168a18fdc2f134d845/OCCUPIED-CELL-ROUTES-001.json),
[atomic manifest](../results/occupied-cell-routes-001-runs/20261022T193953Z-6f4f8efe83e345168a18fdc2f134d845/manifest.json).
