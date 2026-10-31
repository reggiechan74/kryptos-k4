# Parity-first v2: frozen synthetic validation

31 October 2026. **PASS: all40 cases and240 timed outputs match the independent exact oracle.** This validates the frozen31-feature,≤3-term model-specific decoder and its matched output contract—not a real-target solution, general speed theorem or worldwide novelty claim. No target was tested.

**Comparison boundary:** v2 and the strong CRT baseline return identical prediction sets. The measured advance is computational efficiency, not additional recovered information from the same complete constraints. Recovery fractions describe this cohort only; they must not be compared with a different version's cohort as an algorithmic recovery gain.

## What was frozen and tested

Approved freeze manifest: `30e9950c7073f608fb4e62b5991eaf77bdb6e9c44417d85ff4f1475a84873302`. Selected decoder: `9c5c6232cd31167f751f404f636832414fd52cc0c90a624cb9640dfb899bd17e`. No scientific source changed after the freeze or seed draw. The rejected zero-syndrome hybrid was not run on this validation set.

The fixed model uses constant1, six ciphertext lags, six squares,15 pair products and3 full-Z26 equality indicators, with at most3 nonzero modular coefficients. All indicators are evaluated before field reduction.97-rank synthetic ciphertexts supply91 modeled positions6–96, with24 observed mask values C−P and67 unobserved positions. The first6 positions are not claimed.

Both methods return identical kinds of output: exact91-row marginal masks, feasibility/emptiness and a sparse supporting witness for every admitted value. The baseline enumerates4495 maximal3-feature supports with shared-support CRT solves. The parity-first method filters2626 sparse quotient beta vectors, caches eligible mod13 support solves, and groups only identical **full91-row** parity predictions per support. Both use the same Python optimization level/kernel and include preprocessing and witness construction in solver timing. Full relation serialization/global-function uniqueness is not required of either.

## Custody and composition

One fresh seed was drawn after approval and successful final nested-process controls. The independent custodian sealed seed/truth, supplied stripped inputs, and withheld labels until all240 outputs, receipts and scientific sources were sealed. Output seal: `3deac935255b28f32a1839e8f4911fd80f22ef35aec6f43bbf9ebd3c3baa1781`; release verification records18:49:44UTC after completion. All523 sealed files verified before release.

The fixed40 cases comprise24 ordinary draws (6 per beta weight0–3),6 degeneracy controls,2 same-crib/different-outside parity controls,4 constructed contradictions and4 dependent observational twins. **These are not40 independent unseen random draws.** One deterministic zero/zero-law fixture is explicitly a structural replay; twins reuse ordinary inputs. Opaque IDs hide descriptive labels, but the generator's fixed order exposes the stratum schedule. Shared-filesystem custody was procedural, not cryptographic access isolation. No development random draw or prior blind fixture/seed was reused for tuning; deterministic controls remain explicitly identified.

See [custody and independent audit](CUSTODY-AND-INDEPENDENT-AUDIT.md), `generation-commitment.json`, `release-verification.json`, `released-seed.json`, `released-truth.json` and `OUTPUT-SEAL.json`.

## Correctness and inference limits

- Independent source-disjoint4992-support CRT oracle: **40/40 exact masks and feasibility**, all3 repeats of both methods.
- **25,806** sparse marginal-value witness checks passed: at most3 distinct nonzero coefficients, all observations reproduced, claimed value reproduced.
- Tiny exhaustive17,576-vector/8,788-function support-cost/maximal-container controls passed.
-32 generated in-family cases: **2103/2144 unobserved positions forced**, **zero false forced**;27/32 force all67.
- All4 duplicate-context contradictions are empty, not vacuously certain.
- Each of4 observational twins forces all67 positions yet disagrees with its altered hidden truth at1 position. Membership was unknown at generation; the exact singleton exclusion now certifies each specified twin truth incompatible with this class. The visible solver inputs remain compatible. Frozen labels are not rewritten retroactively.

Marginal witnesses may differ between coordinates: masks do not permit arbitrary independent choices to form a valid whole message. Unique finite-trace predictions do not establish a unique coefficient vector or global function. Full beta fibers are not preserved by projection grouping, so global-function enumeration/uniqueness is not claimed. Independent algebraic basis evidence in the development audit distinguishes genuine functions from coefficient aliases.

## Matched performance on this fixed workload

Three fresh-process repetitions per method/case, seeded randomized paired order; all240 stages completed. Values below sum the per-case medians, not the median of an aggregate and not a universal speed ratio.

| Metric | Maximal-support CRT | Grouped parity-first |
| --- | ---: | ---: |
| Sum of40 case-median solver CPU |19.612s|14.403s|
| Solver CPU across all120 repetitions |59.476s|46.352s|
| Largest individual process RSS |8,448KiB|21,760KiB|
| Largest within-case repetition max/min CPU ratio |1.97|2.95|

Parity-first used **26.6% less summed median CPU** on this workload, but more memory. It was faster by case-median CPU in38/40 cases. Both losses were same-crib/different-outside parity controls:13.6% and46.9% slower. Each loss had M=1694 matching beta, U=4495 support solves and E=F=29032 incidences/feasible pieces. These retained losses identify a concrete ambiguity/projection overhead, not a reason to filter cases.

| Stratum | Cases | CRT summed median CPU | Parity summed median CPU |
| --- | ---: | ---: | ---: |
| Ordinary beta0 |6|1.746s|1.100s|
| Ordinary beta1 |6|0.760s|0.176s|
| Ordinary beta2 |6|0.728s|0.099s|
| Ordinary beta3 |6|0.696s|0.094s|
| Zero contexts |2|2.543s|1.779s|
| Constant contexts |2|3.763s|2.318s|
| Indicator degeneracy |2|3.640s|2.359s|
| Crib-parity aliases |2|4.623s|5.966s|
| Contradictions |4|0.556s|0.296s|
| Dependent twins |4|0.555s|0.216s|

The median of40 paired case ratios is0.255, **not** the aggregate speedup; easy cases and heavy degeneracy have different weights. Repetition variability is substantial and only3 repetitions were taken. Report this fixed-workload comparison, not a general acceleration guarantee or statistical population claim. Exact raw timings, wall times, inclusive child CPU, RSS, U/M/E/F and every loss are in `validation-analysis.json` and `benchmark/`.

## Resource enforcement and retained failures

The unchanged reviewed Linux launcher capped every scientific stage and supervisor, measured both, enforced nested expected-parent guards and wall cleanup including pre-session startup. Mandatory122-second reservations guarded the4,000-second inclusive inner-stage budget.

-240-stage inner inclusive CPU:120.694s.
- Driver receipt inclusive of nested stages:122.714CPU s plus0.028supervisorCPU;122.737wall;21,760/8,320KiB stage/supervisor RSS. Do not add the already included inner total again.
- Independent audit:22.857CPU s plus0.028supervisorCPU;14,572/8,320KiB RSS, no cap hit.
- Final controls, generation, release and analysis have separate bounded receipts. All work is well below the6,754-second conservative overall envelope and intended2GiB process-tree address-space ceiling.

The first **custody root invocation** exited137 because a shell-derived expected-parent PID was invalidated by shell exec optimization. No seed/data/receipt existed; no generator or scientific stage ran. The failure was retained, explicitly approved for root-invocation correction, and followed by exactly one successful draw. Nested guards were never weakened. A later post-release detail-printing command had a SyntaxError; its failure receipt is retained, followed by a corrected reporting-only script. Neither failure discarded a case or changed frozen scientific code. Earlier development wrapper defects remain in the development package.

## Next decision—not started

Keep v2 and all validation evidence immutable. The two alias losses motivate **separately gated development**, not retuning this set: consider retaining sparse-parity support admission but projecting each eligible support's entire binary affine family once, rather than iterating its matching beta predictions. This may remove the measured repeated-projection cost; it requires a separate exactness review, development comparison and a new freeze/fresh validation before any benefit claim. It is close to common-support CRT machinery, not a claimed new general theory.

No new method version, expanded feature family, target run, separate repository or publication action follows automatically from this pass.
