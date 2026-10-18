# Experiment log

| ID | Purpose | Command | Scope | Result |
| --- | --- | --- | --- | --- |
| BASE-001 | Baseline data integrity | `python3 experiments/check_baseline.py` | Supplied 97-letter transcription and two crib intervals only | PASS: 97 letters; both crib intervals consistent |

Use [the template](templates/experiment.md) for future runs. Baseline validation
makes no statement about a cryptographic method or historical source accuracy.

## BASE-001 initialization run

- Date: 2026-10-18 UTC.
- Environment: Python 3.9.6; standard library only.
- Commands: as above and `python3 -m unittest discover -s tests -v`.
- Result: baseline check PASS; all 6 unit tests PASS; exit status 0.
- Input: `data/k4.json`; ciphertext ASCII SHA-256 `eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab`.
- Seed: not applicable; deterministic, one input, no search.
- Scope: data shape and indexing only; no cryptanalytic hypothesis tested.
- Code version: this scaffold commit (see Git history); no external dependencies.

## CTRL-001 — exact K1–K3 controls

- Date: 2026-10-18 UTC; deterministic, Python 3.9.6 standard library.
- Commands: `python3 experiments/check_controls.py > results/CTRL-001.json`
  and `python3 -m unittest discover -s tests -v`.
- Input: `data/controls.json`; source provenance and disagreements in
  [verification](../sources/VERIFICATION.md). Literal expected plaintext fixtures.
- Parameters: KRYPTOS alphabet, K=0, modular addition, PALIMPSEST / ABSCISSA;
  question marks preserved without key advancement. K2 original and restored-S
  variants separate. K3 8×42 CW → 24×14 CW, row-major, 336 letters.
- Result: all four complete known-answer encrypt/decrypt comparisons PASS.
  All 15 tests PASS, including 120 seeded synthetic text/key round trips,
  independent opening vector, punctuation convention, and all 336 unique indices.
- RNG: Python `random.Random(20261018)` for unit controls only; no search.
- Runtime: under one second on the local Mac. No dependencies or network in checks.
- Scope: exact fixtures and stated conventions only. Images not independently
  transcribed; physical paper reconstruction not claimed. No K4 conclusion.
- Code/version: CTRL-001 milestone commit in history; output hashes in
  [results](../results/CTRL-001.json).

## STRUCT-001 — exact structural and encoding constraints

- Date: 2026-10-18 UTC; Python 3.9.6 standard library; under one second.
- Command: `python3 experiments/structural_checks.py > results/STRUCT-001.json`.
- Inputs: unchanged `data/k4.json`; no normalization, key search, or scoring.
- Parameters: all pairs of the 24 crib positions, periods 1–96 inclusive; literal
  letter counts; synthetic two-character codec inventory 0–47, no framing.
- Result: E deficit 3 required / 2 available; exactly 19 contradictory periods.
  Full witnesses and surviving periods in [result](../results/STRUCT-001.json);
  interpretation and prior-art limits in [findings](STRUCTURAL-FINDINGS.md).
- Validation: all 21 tests PASS, including both bijection directions and planted
  true-period controls for periods 1,2,7,8,10,21,42. Seed 20261018 for controls.
- Scope: no substitution-plus-transposition conclusion; no actual language
  converter; surviving constraints are not solutions. No novelty claim.
- Code/version: STRUCT-001 milestone commit in history.

## ROUTE-001, RUNKEY-001, TRIFID-001 — bounded model milestone

- Date: 2026-10-18 UTC; Python 3.9.6, standard library, single local process.
- Command: `python3 experiments/run_bounded.py`; recorded
  [bounds and conventions](BOUNDED-SPEC.md), [findings](BOUNDED-FINDINGS.md).
- ROUTE-001: 13,056 cases, 66 distinct routes; 282 compatible partial assignments,
  all identity route at periods 27–29 or 53–96. All are vacuous: 47 periods ×
  2 alphabets × 3 equations, zero repeated-phase comparisons. Zero fully observed keys.
- RUNKEY-001: 28,488 cases, 4,748 window/direction cases, 2,692 unique key strings;
  zero all-24-crib matches. Trigger for 199-shuffle validation not met.
- TRIFID-001: 144 cases, zero all-crib matches; all full inverse checks pass.
- Validation (corrected by audit): 20 given-parameter `constrain` checks at
  period 4 using routes 0–19, not end-to-end route-scan recovery. Separately,
  20 planted literal-window recoveries did use the actual window scanner; all
  three equations and both alphabets were exercised.
  Seed 20261018, Python MT19937. Trifid controls cover every symbol and period.
- Runtime: each bounded scan below one second. Limits: 30 seconds / 20,000 route
  cases; 30 seconds / 30,000 running-key cases; fixed 144 Trifid cases.
- Outputs: `results/ROUTE-001-summary.json` plus complete compressed details,
  `results/RUNKEY-001.json`, `results/TRIFID-001.json`. Outputs include exact
  consulted code/input SHA256 hashes and environment. Code version is the
  bounded-model milestone commit containing these artifacts. No external inputs
  were downloaded during execution, and no language score was used.
- Negative-result scope: only declared versions, routes, periods, alphabets,
  equations, windows, and cubes. No family-wide rejection from these finite runs.

## STAT-001 — published lag-pattern diagnostic and maximum correction

- Command: `python3 experiments/statistical_diagnostics.py --write-results`.
- Definition: duplicate excess among ordered overlapping pairs at lags 1–48.
- Null: histogram-preserving shuffles, seed 20261018, Python MT19937; 9,999
  draws, split 4,999 calibration / 5,000 evaluation. Maximum statistic frozen
  using calibration means and sample deviations. 60-second cap; completed in 3.3s.
- Observed: lag 21 has 11 duplicate excess; fixed-lag exceedances 1/5,000,
  plus-one tail 0.000400. Calibrated maximum exceedances 53/5,000, tail 0.010798.
- Scope: conditional null diagnostics with historical/postselection limits,
  not an English null or a probability of a cipher hypothesis. Wilson Monte
  Carlo intervals and exact caveats in [findings](BOUNDED-FINDINGS.md).
- Outputs: `results/STAT-001-summary.json`, complete compressed raw draws and
  evaluation maxima in `results/STAT-001.json.gz`; code/input hashes included.
- Prior art: Bean 2021, §2.1; independent limited check, not whole-paper or
  Gromark-search reproduction. No external solver code executed.

## AUDIT-001 — focused audit hardening and exact replay

The original artifacts at b83b0f9 are byte-preserved; their SHA256 manifest is
`data/audited-results-b83.json`. [Audit notes](AUDIT-HARDENING.md) correct the
control-coverage and registration claims and document the stronger tests.
No new hypothesis family, range, corpus, parameter, or score is introduced.
Current runners validate the baseline and use atomic unique run snapshots,
run IDs, explicit completion/incomplete outcomes, uniform scanner deadlines,
final checks after staged output, and a required prior specification commit.
`results/AUDIT-001.json` records the final test count and code hashes.

## LANG-001 — historically grounded encoding audit

- Prior spec:21c3b4c16615586c525420cfdd6014cc7a6d44c4; code:58646022bf5578e4c193a6cdc7a487ef86c5947d.
- Exact33letter uppercase Russian domain, GOST1981Table2. All37,060 strings of
  lengths0–3 round-trip and have distinct encodings; suffixes H/HH then empty.
- Precise literal/permutation and fixed-character-substitution support rejections;
  punctuation/padding/polyalphabetic exceptions explicit. Quote stripping lossy.
- Shavian transport/English inverse unspecified; no invented mapping or search.
- Oneprocess,30scap,0.497s actual,0keysearches,0MonteCarlo controls; deterministic.
- [Findings and immutable run links](LANGUAGE-FINDINGS.md).

## MASK-AUTO-001 and MASK-FM-001 — two frozen masking pilots

- Prior specs:9f546aa279ec065f2a4788fe4a1895efbcf87750; code:705f65f50e95f8265f7227a2f91336f39091780b.
- Exactly 12 autokey outputs; all complete and re-encode, all fail24cribletters.
  Controls:2handvectors,72 round trips,12 planted recoveries and12 crib-alteration negatives.
- Exactly2 Fractionated Morse maps; each produces291 ternarysymbols but fails on
  internalxxx. ACAexample, allsymbols/triples, padding, parsing, and2plants pass.
- Implementation-authored invalid fixture .-xx.. corrected to positive A I before
  actual K4 runs; no rule/key/case change. [Fixture review](../docs/masking-fixture-review.md).
- Oneprocess,10scaps;0.014s and0.005s actual including controls. No scores/nulls,
  no extra keys or transformations. [Findings and raw runs](MASKING-FINDINGS.md).

## WORD-SCRAMBLE-001 — user's combined hypothesis, fixed24 checks

- Prior spec:ef0b3c91e11159886930299878b8636a72252acf; code:30fc403b85998731414160fcd1c5cecb5ec42f73.
- Reuses exactly12 autokey intermediates and2assumed segmentations. All 24 checks
  fail endpoints; fullword/interior counts retained. No fitted keys/permutations.
- Synthetic reverse-interior schedules:24 planted acceptances,24 endpoint negatives,
  24count negatives,24 schedule inversions; SALT/SLAT ambiguity explicit. Seed20261018.
- Oneprocess,10scap,0.069s actual. No scoring/nulls or factorial enumeration.
- [Findings and complete24case records](WORD-SCRAMBLING-FINDINGS.md).

## Final validation of this sequence

All 73unit/replay tests pass in7.431 s, including all 37,060GOST round trips and
complete new artifact/hash replays. See [validation](../results/LANGUAGE-MASKING-WORD-VALIDATION.json).
[Commit/run chronology](../results/SPECIFICATION-CHRONOLOGY.json) checks prior
specification commits, subsequent code commits, and actual run start times for
all4new runs. This is independent of the older b83 preregistration limitation.
H-PHONETIC-RESPELLING and H-GERMAN-TRANSLATION were recorded as distinct user
proposals only; no mapper, translation fitting, or shifted cribs were implemented.

## PHONETIC-SUBSET-001 — small deterministic follow-up

- Prior spec:35477f6c045d4cd831f9c72e60790042e93f6ba4; code:f3b9792ae11afc81a360de12d78c63777d261bc9.
- Only W→V and word-final D→T/G→K on explicit uppercase word tokens.
- All four clue words unchanged; original24character masks remain identical
  across the same12frozen autokey outputs;0rescued cases. No new keys or scores.
- Positive synthetic vectors and WET/VET loss example pass. TH/I rules and German
  translation not implemented; pronunciation/dictionary and alignment absent.
- Five-second cap, one process, immutable run status/hashes;
  [findings and record](PHONETIC-FEASIBILITY.md).

Final validation after the narrow respelling follow-up: all77tests pass, no
failures/errors, in7.300s suite time. [Validation record](../results/SEQUENTIAL-BRANCHES-VALIDATION.json)
includes current code/test hashes. All5new run specification/code/start ordering
checks pass in the chronology receipt. The older audited artifacts remain unchanged.

## Independent audit receipt for ba10b1b

A supplied independent audit of ba10b1b3f38eb7829ef45ea427348bffd51768cd
reported no result-changing bugs. It independently verified the 37,060 GOST,
12 autokey, 2 Fractionated Morse and 24 word-interior checks, plus specification
chronology. This is an attributed audit receipt; this coding update does not
claim authorship of that independent review. Local regression replay is recorded
separately below.

## DIRECT-ENIGMA-001 — exact aligned reflector boundary

- Scope fixed by the requested update: position 74 K→K only; no rotor/key scan.
- Command: `python3 -m unittest discover -s tests -p 'test_direct_enigma.py' -v`.
- Data: unchanged 97-letter fixture and BERLINCLOCK at positions 64–74.
- Result: position 74 has ciphertext K and confirmed plaintext K, incompatible
  with a direct aligned standard wartime fixed-point-free reflector model.
- Mathematical control: 26 toy bijections, Python MT19937 seed 20261018; no
  historical wiring or sampled rotor-search claim. The general proof supplies
  the conclusion; extra transforms are outside scope.
- Period-map documentation preserves supplied evidence only; no additional map
  search, German-name extraction or new cryptanalytic workload was launched.
- Full local replay: see `results/PERIOD-MAP-ENIGMA-VALIDATION.json`. Earlier
  validation records and audited artifacts remain historical and unchanged.

## Neptune and clock-face documentation update

- Date: 2026-10-18 UTC; parent 744853ed9ec32717bf484ed013baf8b599c382b7.
- Preserved supplied bounded research in `docs/neptune-discovery-assessment.md`;
  no new source retrieval, coordinate adjustment, cipher pilot or key search.
- Existing code, tests and historical result artifacts unchanged.
- Command: `python3 -m unittest discover -s tests -v`.
- Result: all 79 tests passed, 7.406 s suite time; no failures/errors.
- This replay checks existing software/artifacts, not the report's historical
  claims, source inspection, panel orientation or reported coordinate arithmetic.

## Clock-reset preparation — no new K4 run

- Parent: 8c1841edbad1961399a7a264b4c3b52be5e2e1be; frozen reset specification pending.
- Reviewed prior exclusions; continuous period-11 arithmetic is already excluded
  in ROUTE-001's fixed alphabets/equations. No repeat keyword discovery claimed.
- Prepared independent synthetic reference encoder and four tests: hand vectors,
  24 seeded segment recovery/regeneration controls, boundary negatives and strict
  invalid-index rejection. No actual scanner recovery claimed yet.
- Commands: `python3 -m unittest discover -s tests -p 'test_reset_controls.py' -v`
  (4 pass) and `python3 -m unittest discover -s tests -v` (83 pass, 7.359 s).
- Existing code/results unchanged; no new K4 candidate execution, expensive search
  or submission. Astronomy correction documented without date-key search.

Subsequent independent reviewer witnesses make the identical shared-reset keyword
scan redundant. Prepared `reset_boundary_proof.py`, three regression tests and
`CLOCK-RESET-PROOF.md` with explicit bijection/alignment assumptions. These new
proof tests have NOT run; the 83-test result above predates their addition. The
final frozen proof specification is pending. Existing result files remain unchanged.

## CLOCK-BOUNDARY-REG-001 — verification of known deductions

- Spec committed first: 4e2d002925bfc7f3b332f94cd4472617919f52fa; implementation:
  000b8c3a4e480fd773f131cf85eef6bc30d47206. Witnesses were supplied beforehand;
  no new-discovery or blind-preregistration claim.
- Command: `python3 experiments/clock_boundary_regression.py --spec-commit 4e2d002925bfc7f3b332f94cd4472617919f52fa --code-commit 000b8c3a4e480fd773f131cf85eef6bc30d47206`.
- Verified 13 fixed certificates: six period-11, six shared-reset arithmetic,
  one alphabet-free injectivity collision. All 72 declared formal keyword cases
  are analytically subsumed; zero candidate-search trials or fitted variants.
- Controls all pass: 4,056 primitive encrypt/decrypt/key-recovery cases, 388 phase
  comparisons, 24 independent synthetic 97-letter round trips/regenerations,
  24 altered-ciphertext negatives. Deterministic; no RNG needed.
- One process, standard library, 10 s cap; actual 0.018 s. Immutable run:
  `results/clock-boundary-runs/20261018T124241Z-f156ac09cb06401b8bfbcc8e48b8383d/`.
- Output and consulted file hashes independently checked after execution.
- Full suite: `python3 -m unittest discover -s tests -v`, 90 pass, 7.382 s.
- Scope: fixed unchanged-alignment period-11 arithmetic and declared identical
  reset bijections only. No transposition/feedback/different-key exclusion.
- BERLINCLOCK remains confirmed plaintext. City orientation/history unresolved.
  No date-key, reversed-key, longer-key or internal-word-reset extension.

## Historical-clock / Egyptian-sign-list documentation

- Date: 2026-10-18 UTC; parent 528d4902ba81e6791107f9b4b623170923d14933.
- Saved supplied dated photographic evidence with external links/attribution;
  exact ENE orientation and full 1989 candidate panel remain unresolved.
  No inaccessible local image paths or claims of uploaded inspection crops.
- Recorded H-EGYPTIAN-SIGN-LIST with supplied context and missing edition,
  sign mapping, normalization, direction, inverse and key; no invented glyph
  alphabet, Unicode arithmetic, new source search or cipher experiment.
- Existing code, tests, clock-reset certificates and result artifacts unchanged.
- Command: `python3 -m unittest discover -s tests -v`.
- Result: all 90 tests pass in 7.320 s; no failures/errors. This software replay
  does not independently verify the worker's historical-source/photo inspection.
