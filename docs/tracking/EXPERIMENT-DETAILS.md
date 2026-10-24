# Experiment details

Generated navigation; edit the canonical ledger or receipts, then run `python3 experiments/build_research_navigation.py`. The JSON retains complete scope fields and original log entries. No experiment is executed by this generator.

## LOG-EC63FE0563

**BASE-001 initialization run**

Exact run start/end unknown; date-only record: 2026-10-18 (date statement; not a run timestamp); original date statement: 2026-10-18 UTC.

Type: baseline validation. Outcome: Passed data integrity and indexing checks; no cryptanalysis

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Date: 2026-10-18 UTC.
- Environment: Python 3.9.6; standard library only.
- Commands: as above and `python3 -m unittest discover -s tests -v`.
- Result: baseline check PASS; all 6 unit tests PASS; exit status 0.
- Input: `data/k4.json`; ciphertext ASCII SHA-256 `eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab`.
- Seed: not applicable; deterministic, one input, no search.
- Scope: data shape and indexing only; no cryptanalytic hypothesis tested.
- Code version: this scaffold commit (see Git history); no external dependencies.

Related files: [data/k4.json](../../data/k4.json).

## LOG-2CFB8FEA59

**CTRL-001 — exact K1–K3 controls**

Exact run start/end unknown; date-only record: 2026-10-18 (date statement; not a run timestamp); original date statement: 2026-10-18 UTC; deterministic, Python 3.9.6 standard library.

Type: known-answer validation. Outcome: Passed complete K1–K3 fixture comparisons

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Date: 2026-10-18 UTC; deterministic, Python 3.9.6 standard library.
- Commands: `python3 experiments/check_controls.py > results/CTRL-001.json`
  and `python3 -m unittest discover -s tests -v`.
- Input: `data/controls.json`; source provenance and disagreements in
  [verification](../../sources/VERIFICATION.md). Literal expected plaintext fixtures.
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
  [results](../../results/CTRL-001.json).

Related files: [data/controls.json](../../data/controls.json), [experiments/check_controls.py](../../experiments/check_controls.py), [results/CTRL-001.json](../../results/CTRL-001.json), [sources/VERIFICATION.md](../../sources/VERIFICATION.md).

## LOG-CB0BA28264

**STRUCT-001 — exact structural and encoding constraints**

Exact run start/end unknown; date-only record: 2026-10-18 (date statement; not a run timestamp); original date statement: 2026-10-18 UTC; Python 3.9.6 standard library; under one second.

Type: analytical constraints. Outcome: Direct permutation deficit and 19 periodic contradictions; other models remain open

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Date: 2026-10-18 UTC; Python 3.9.6 standard library; under one second.
- Command: `python3 experiments/structural_checks.py > results/STRUCT-001.json`.
- Inputs: unchanged `data/k4.json`; no normalization, key search, or scoring.
- Parameters: all pairs of the 24 crib positions, periods 1–96 inclusive; literal
  letter counts; synthetic two-character codec inventory 0–47, no framing.
- Result: E deficit 3 required / 2 available; exactly 19 contradictory periods.
  Full witnesses and surviving periods in [result](../../results/STRUCT-001.json);
  interpretation and prior-art limits in [findings](../../research/STRUCTURAL-FINDINGS.md).
- Validation: all 21 tests PASS, including both bijection directions and planted
  true-period controls for periods 1,2,7,8,10,21,42. Seed 20261018 for controls.
- Scope: no substitution-plus-transposition conclusion; no actual language
  converter; surviving constraints are not solutions. No novelty claim.
- Code/version: STRUCT-001 milestone commit in history.

Related files: [data/k4.json](../../data/k4.json), [experiments/structural_checks.py](../../experiments/structural_checks.py), [research/STRUCTURAL-FINDINGS.md](../../research/STRUCTURAL-FINDINGS.md), [results/STRUCT-001.json](../../results/STRUCT-001.json).

## LOG-BC9CFA37FE

**ROUTE-001, RUNKEY-001, TRIFID-001 — bounded model milestone**

Exact run start/end unknown; date-only record: 2026-10-18 (date statement; not a run timestamp); original date statement: 2026-10-18 UTC; Python 3.9.6, standard library, single local process.

Type: finite K4 model tests. Outcome: Running-key/Trifid negatives; route fits are vacuous, with no determined key

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Date: 2026-10-18 UTC; Python 3.9.6, standard library, single local process.
- Command: `python3 experiments/run_bounded.py`; recorded
  [bounds and conventions](../../research/BOUNDED-SPEC.md), [findings](../../research/BOUNDED-FINDINGS.md).
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

Related files: [experiments/run_bounded.py](../../experiments/run_bounded.py), [research/BOUNDED-FINDINGS.md](../../research/BOUNDED-FINDINGS.md), [research/BOUNDED-SPEC.md](../../research/BOUNDED-SPEC.md), [results/ROUTE-001-summary.json](../../results/ROUTE-001-summary.json), [results/RUNKEY-001.json](../../results/RUNKEY-001.json), [results/TRIFID-001.json](../../results/TRIFID-001.json).

## LOG-6B1E22F8E2

**STAT-001 — published lag-pattern diagnostic and maximum correction**

Exact run start/end unknown

Type: statistical diagnostic. Outcome: Conditional lag-pattern excess; not a cipher identification or posterior

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Command: `python3 experiments/statistical_diagnostics.py --write-results`.
- Definition: duplicate excess among ordered overlapping pairs at lags 1–48.
- Null: histogram-preserving shuffles, seed 20261018, Python MT19937; 9,999
  draws, split 4,999 calibration / 5,000 evaluation. Maximum statistic frozen
  using calibration means and sample deviations. 60-second cap; completed in 3.3s.
- Observed: lag 21 has 11 duplicate excess; fixed-lag exceedances 1/5,000,
  plus-one tail 0.000400. Calibrated maximum exceedances 53/5,000, tail 0.010798.
- Scope: conditional null diagnostics with historical/postselection limits,
  not an English null or a probability of a cipher hypothesis. Wilson Monte
  Carlo intervals and exact caveats in [findings](../../research/BOUNDED-FINDINGS.md).
- Outputs: `results/STAT-001-summary.json`, complete compressed raw draws and
  evaluation maxima in `results/STAT-001.json.gz`; code/input hashes included.
- Prior art: Bean 2021, §2.1; independent limited check, not whole-paper or
  Gromark-search reproduction. No external solver code executed.

Related files: [experiments/statistical_diagnostics.py](../../experiments/statistical_diagnostics.py), [research/BOUNDED-FINDINGS.md](../../research/BOUNDED-FINDINGS.md), [results/STAT-001-summary.json](../../results/STAT-001-summary.json), [results/STAT-001.json.gz](../../results/STAT-001.json.gz).

## LOG-C5111807E6

**AUDIT-001 — focused audit hardening and exact replay**

Exact run start/end unknown

Type: regression and replication. Outcome: Audited controls and snapshot safety; no new hypothesis domain

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

The original artifacts at b83b0f9 are byte-preserved; their SHA256 manifest is
`data/audited-results-b83.json`. [Audit notes](../../research/AUDIT-HARDENING.md) correct the
control-coverage and registration claims and document the stronger tests.
No new hypothesis family, range, corpus, parameter, or score is introduced.
Current runners validate the baseline and use atomic unique run snapshots,
run IDs, explicit completion/incomplete outcomes, uniform scanner deadlines,
final checks after staged output, and a required prior specification commit.
`results/AUDIT-001.json` records the final test count and code hashes.

Related files: [data/audited-results-b83.json](../../data/audited-results-b83.json), [research/AUDIT-HARDENING.md](../../research/AUDIT-HARDENING.md), [results/AUDIT-001.json](../../results/AUDIT-001.json).

## LOG-4901554D49

**LANG-001 — historically grounded encoding audit**

Exact run start/end unknown

Type: representation validation; analytical constraints. Outcome: GOST reversible on declared domain; narrow support exclusions; Shavian unspecified

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Prior spec:21c3b4c16615586c525420cfdd6014cc7a6d44c4; code:58646022bf5578e4c193a6cdc7a487ef86c5947d.
- Exact33letter uppercase Russian domain, GOST1981Table2. All37,060 strings of
  lengths0–3 round-trip and have distinct encodings; suffixes H/HH then empty.
- Precise literal/permutation and fixed-character-substitution support rejections;
  punctuation/padding/polyalphabetic exceptions explicit. Quote stripping lossy.
- Shavian transport/English inverse unspecified; no invented mapping or search.
- Oneprocess,30scap,0.497s actual,0keysearches,0MonteCarlo controls; deterministic.
- [Findings and immutable run links](../../research/LANGUAGE-FINDINGS.md).

Related files: [research/LANGUAGE-FINDINGS.md](../../research/LANGUAGE-FINDINGS.md).

## LOG-6409D7E925

**MASK-AUTO-001 and MASK-FM-001 — two frozen masking pilots**

start: 2026-10-18T11:23:16.791919Z; end: 2026-10-18T11:23:16.806864Z; start: 2026-10-18T11:23:17.030203Z; end: 2026-10-18T11:23:17.035825Z

Type: finite K4 model tests. Outcome: All 12 autokeys fail cribs; two fixed Morse maps fail parsing

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Prior specs:9f546aa279ec065f2a4788fe4a1895efbcf87750; code:705f65f50e95f8265f7227a2f91336f39091780b.
- Exactly 12 autokey outputs; all complete and re-encode, all fail24cribletters.
  Controls:2handvectors,72 round trips,12 planted recoveries and12 crib-alteration negatives.
- Exactly2 Fractionated Morse maps; each produces291 ternarysymbols but fails on
  internalxxx. ACAexample, allsymbols/triples, padding, parsing, and2plants pass.
- Implementation-authored invalid fixture .-xx.. corrected to positive A I before
  actual K4 runs; no rule/key/case change. [Fixture review](../masking-fixture-review.md).
- Oneprocess,10scaps;0.014s and0.005s actual including controls. No scores/nulls,
  no extra keys or transformations. [Findings and raw runs](../../research/MASKING-FINDINGS.md).

Related files: [docs/masking-fixture-review.md](../masking-fixture-review.md), [research/MASKING-FINDINGS.md](../../research/MASKING-FINDINGS.md).

## LOG-39A9220FB0

**WORD-SCRAMBLE-001 — user's combined hypothesis, fixed24 checks**

Exact run start/end unknown

Type: analytical constraints; finite K4 model tests. Outcome: All 24 fixed combinations fail endpoint/count requirements

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Prior spec:ef0b3c91e11159886930299878b8636a72252acf; code:30fc403b85998731414160fcd1c5cecb5ec42f73.
- Reuses exactly12 autokey intermediates and2assumed segmentations. All 24 checks
  fail endpoints; fullword/interior counts retained. No fitted keys/permutations.
- Synthetic reverse-interior schedules:24 planted acceptances,24 endpoint negatives,
  24count negatives,24 schedule inversions; SALT/SLAT ambiguity explicit. Seed20261018.
- Oneprocess,10scap,0.069s actual. No scoring/nulls or factorial enumeration.
- [Findings and complete24case records](../../research/WORD-SCRAMBLING-FINDINGS.md).

Related files: [research/WORD-SCRAMBLING-FINDINGS.md](../../research/WORD-SCRAMBLING-FINDINGS.md).

## LOG-21C275007D

**Final validation of this sequence**

receipt recording: 2026-10-18T11:30:39.768784Z

Type: regression and replication. Outcome: 73 checks passed for the recorded sequence; no new model search

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

All 73unit/replay tests pass in7.431 s, including all 37,060GOST round trips and
complete new artifact/hash replays. See [validation](../../results/LANGUAGE-MASKING-WORD-VALIDATION.json).
[Commit/run chronology](../../results/SPECIFICATION-CHRONOLOGY.json) checks prior
specification commits, subsequent code commits, and actual run start times for
all4new runs. This is independent of the older b83 preregistration limitation.
H-PHONETIC-RESPELLING and H-GERMAN-TRANSLATION were recorded as distinct user
proposals only; no mapper, translation fitting, or shifted cribs were implemented.

Related files: [results/LANGUAGE-MASKING-WORD-VALIDATION.json](../../results/LANGUAGE-MASKING-WORD-VALIDATION.json), [results/SPECIFICATION-CHRONOLOGY.json](../../results/SPECIFICATION-CHRONOLOGY.json).

## LOG-0C1886FF72

**PHONETIC-SUBSET-001 — small deterministic follow-up**

receipt recording: 2026-10-18T11:35:01.252332Z

Type: finite K4 model tests. Outcome: Narrow respelling leaves clues unchanged; rescues none of 12 prior outputs

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Prior spec:35477f6c045d4cd831f9c72e60790042e93f6ba4; code:f3b9792ae11afc81a360de12d78c63777d261bc9.
- Only W→V and word-final D→T/G→K on explicit uppercase word tokens.
- All four clue words unchanged; original24character masks remain identical
  across the same12frozen autokey outputs;0rescued cases. No new keys or scores.
- Positive synthetic vectors and WET/VET loss example pass. TH/I rules and German
  translation not implemented; pronunciation/dictionary and alignment absent.
- Five-second cap, one process, immutable run status/hashes;
  [findings and record](../../research/PHONETIC-FEASIBILITY.md).

Final validation after the narrow respelling follow-up: all77tests pass, no
failures/errors, in7.300s suite time. [Validation record](../../results/SEQUENTIAL-BRANCHES-VALIDATION.json)
includes current code/test hashes. All5new run specification/code/start ordering
checks pass in the chronology receipt. The older audited artifacts remain unchanged.

Related files: [research/PHONETIC-FEASIBILITY.md](../../research/PHONETIC-FEASIBILITY.md), [results/SEQUENTIAL-BRANCHES-VALIDATION.json](../../results/SEQUENTIAL-BRANCHES-VALIDATION.json).

## LOG-5A09B41ED3

**Independent audit receipt for ba10b1b**

Exact run start/end unknown

Type: attributed independent review. Outcome: Supplied audit reports no result-changing bugs; not a new local search

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

A supplied independent audit of ba10b1b3f38eb7829ef45ea427348bffd51768cd
reported no result-changing bugs. It independently verified the 37,060 GOST,
12 autokey, 2 Fractionated Morse and 24 word-interior checks, plus specification
chronology. This is an attributed audit receipt; this coding update does not
claim authorship of that independent review. Local regression replay is recorded
separately below.

## LOG-5B01FDC62E

**DIRECT-ENIGMA-001 — exact aligned reflector boundary**

receipt recording: 2026-10-18T12:00:46.104564Z

Type: analytical constraints. Outcome: Aligned fixed-point-free reflector model excluded by K→K at position 74

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

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

Related files: [results/PERIOD-MAP-ENIGMA-VALIDATION.json](../../results/PERIOD-MAP-ENIGMA-VALIDATION.json).

## LOG-35BC648FE4

**Neptune and clock-face documentation update**

Exact run start/end unknown; date-only record: 2026-10-18 (date statement; not a run timestamp); original date statement: 2026-10-18 UTC; parent 744853ed9ec32717bf484ed013baf8b599c382b7.

Type: source documentation. Outcome: Supplied Neptune/clock research preserved; no new cipher test

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Date: 2026-10-18 UTC; parent 744853ed9ec32717bf484ed013baf8b599c382b7.
- Preserved supplied bounded research in `docs/neptune-discovery-assessment.md`;
  no new source retrieval, coordinate adjustment, cipher pilot or key search.
- Existing code, tests and historical result artifacts unchanged.
- Command: `python3 -m unittest discover -s tests -v`.
- Result: all 79 tests passed, 7.406 s suite time; no failures/errors.
- This replay checks existing software/artifacts, not the report's historical
  claims, source inspection, panel orientation or reported coordinate arithmetic.

## LOG-1427CCBA44

**Clock-reset preparation — no new K4 run**

Exact run start/end unknown

Type: protocol preparation; synthetic validation. Outcome: Prepared controls; actual reset search not run in this entry

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

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

## LOG-5419FFCD4F

**CLOCK-BOUNDARY-REG-001 — verification of known deductions**

start: 2026-10-18T12:42:41.282170Z; end: 2026-10-18T12:42:41.301414Z

Type: analytical constraints; replication. Outcome: 13 supplied certificates verified; no candidate search

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

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

Related files: [experiments/clock_boundary_regression.py](../../experiments/clock_boundary_regression.py).

## LOG-761714DBA1

**Historical-clock / Egyptian-sign-list documentation**

Exact run start/end unknown; date-only record: 2026-10-18 (date statement; not a run timestamp); original date statement: 2026-10-18 UTC; parent 528d4902ba81e6791107f9b4b623170923d14933.

Type: source documentation. Outcome: Historical-clock evidence and Egyptian proposal recorded; inputs unresolved

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

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

## LOG-8EA2DFFFD5

**Pinned Barney/Scott prior-art review — revision 2026-10-18**

Exact run start/end unknown; date-only record: 2026-10-18 (heading; not a run timestamp)

Type: prior-art review. Outcome: Pinned source coverage reviewed; external large searches not rerun

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Parent: 2d4b1bca916ce9c3795029b9e9f787be436a4a72.
- Read pinned GitHub source/log files: Barney 2db2722cc3f18c52d4d8369d7adc5a1db7e859d7;
  Scott 3ce19e3ae164a54af8743222ad3de5f6a93f6faf. Selected file/blob identities in
  `sources/prior-art-review-pins.json`; detailed review and exact-overlap matrix
  in `docs/prior-art-barney-scott-review.md`.
- No third-party code executed. Direct own-code bookkeeping on 24 canonical pairs
  confirms effective forward lags 1–33 / 1–8, 9/10 member-distance fits and three
  biconditional exceptions. Reproduction command is embedded in the review.
- Third-party large searches, shuffle statistics and power reports not rerun.
  Supplied audit covers 41 grouped branches, with selected static inspection only.
  Exact duplicates may be retired; families and low-constraint/low-power domains
  are not excluded. Existing local results/proofs/code remain unchanged.
- 2019 testimony page retrieval failed HTTP502; conflicting Bob B comment4 and
  Elonka accounts retained as supplied disputed testimony, without invented quotes.
- Command: `python3 -m unittest discover -s tests -v`.
- Result: 90 tests pass, 8.313 s, no failures/errors. Existing artifact replays pass.
- The Mac lock initially blocked this executor's visibility action; no bypass
  attempted. Final GitHub metadata subsequently reported public visibility. This
  documentation update did not change sharing settings.

Final public-access verification: unauthenticated web reader returned the GitHub
repository page (Public label, Sign in link) and raw README pinned to
4127afb315d821f86cc0240ac49450a6b41eef46. The prior visibility blocker is resolved
at verification time; no visibility mutation was performed by this executor.

## LOG-E7834A43AD

**AUTOKEY-CONSTRAINT-001 — complete declared lag audit**

start: 2026-10-18T13:41:47.786677Z; end: 2026-10-18T13:41:48.020232Z

Type: exact K4 constraints. Outcome: 732 cases contradicted; 420 compatible with zero independent checks

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Initial spec 44a03c9f53dd1e95107a6a5b1bb7a7dc0c79470a; pre-execution toy-mask
  wording correction 7f83582026045f318fa8dcd2224190cc44a5b432; implementation
  a13bd721af4bac68a1fb29b3e1ff05d61db47e80. No K4 model changed by correction.
- Command: `python3 experiments/run_autokey_constraints.py --spec-commit 7f83582026045f318fa8dcd2224190cc44a5b432 --code-commit a13bd721af4bac68a1fb29b3e1ff05d61db47e80`.
- Two same alphabets, three equations, PT/CT feedback, arbitrary independent
  L-symbol primers, forward lags1–96. No minimum-check skips.
- All 1,152 cases classified: 732 contradicted, 420 underdetermined-compatible,
  zero untested. Every compatible case has zero independent consistency checks.
- PT rejects 1–26/30–52; CT rejects 1–73; exact negative scope only. PT lag26
  propagation 22→48→74 and CT lag 73/74 boundaries regress independently.
- Controls: 1,152 synthetic positives/roundtrips/regenerations, 732 negative cases,
  420 vacuous mutations compatible, 5,220 exhaustive toy configurations containing
  40,536 primer decryptions (at most 16 toy primers each). No K4 primer enumeration.
- Independent reviewer supplied expected lag sets after initial spec before execution;
  independent implementation agrees. Own small exhaustive oracle was executed;
  third-party source code was not. Seed 20261018, Python MT19937 for synthetic data.
- One process, standard library, 10 s cap; actual 0.230 s. Full suite 97 pass in 8.519 s.
- Raw snapshot: `results/autokey-constraint-runs/20261018T134147Z-7499a732804146f48f2121f5453be844/`.
  All consulted hashes/output SHA and complete fresh record replay verified.
- Prior artifacts preserved. No full K4 plaintext emitted. Proposed next task is
  one pinned Gromark-survivor full-alphabet feasibility audit, not yet run.

Related files: [experiments/run_autokey_constraints.py](../../experiments/run_autokey_constraints.py).

## LOG-87EE92917B

**GROMARK-ALPHABET-001 — one pinned published tuple**

start: 2026-10-18T13:56:06.417135Z; end: 2026-10-18T13:56:06.427233Z

Type: exact K4 constraints. Outcome: Published Gromark tuple compatible but non-identifiable; differing plaintext witnesses

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Spec/source fixture: cd475ae00eda1eddd8b7fe1694922ecbba593270; implementation:
  f4e56d0ae23d140236417fec5d99ed1055c4df94, both before actual execution.
- Command: `python3 experiments/run_gromark_alphabet.py --spec-commit cd475ae00eda1eddd8b7fe1694922ecbba593270 --code-commit f4e56d0ae23d140236417fec5d99ed1055c4df94`.
- First printed source tuple: (3,16,6,(5,6),(6,12,12,4,4,8)). Source score retained
  only as provenance; no width21/fingerprint/English acceptance filter.
- Local checks pass: 27 nodes, 24 edges, 5 components. Full alphabet feasibility SAT:
  5 search states, 4 selected translation trials, 260 domain checks; no complete count.
- Own witness and separately supplied witness both verify bijections, 24 cribs and
  full 97-character regeneration, but differ outside cribs at the same global gauge. No full
  plaintext output, historical-key claim or K4 solution. Independent prediction
  was supplied after specification before our run; it did not initialize our solver.
- Controls: 2 hand streams, 231 exhaustive toy graphs, 9,396 full permutation pairs,
  56 SAT / 175 UNSAT, 8 synthetic 97-letter plants. Seed 20261018, Python MT19937.
- One process, standard library, 10 s / 100,000 states cap; actual 0.009 s. No registered
  run repair/retry. Full suite 104 tests passed in 8.007 s; prior 97 tests/artifacts retained.
- Snapshot: `results/gromark-alphabet-runs/20261018T135606Z-4fed84af3b8340f79ec5e2491071b3a3/`.
  Output/input/code hashes and complete model replay verified.
- Exactly one K4 tuple tested, no sweep or third-party code execution. Proposed next
  step is one-position letter-domain feasibility, not yet run.

Related files: [experiments/run_gromark_alphabet.py](../../experiments/run_gromark_alphabet.py).

## LOG-CAC907C2B6

**Historical-clock correction — documentation only, 2026-10-18**

Exact run start/end unknown; date-only record: 2026-10-18 (heading; not a run timestamp)

Type: source documentation. Outcome: Corrected model-label transcription; 1989 inventory/orientation still unresolved

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Parent commit: 9d4b4cb6e10ced9d408ef20739c91c4386a8da27.
- Corrected the 1972 panel's middle lower line to HANOI from the parent's independent
  visual inspection; current reading PEKING / HANOI / MANILA. Original erroneous
  SHANGHAI transcription retained in Git history and explicitly noted in the report.
- Directly read LeMO model metadata (accession 1995/09/0108;1972 gift,1968date).
  Supplied 48-image visual assessment distinguishes model layout from installed
  clock; 1989 panel and true-ENE orientation remain unresolved. Sketchbook source pending.
- Checked dependent current summaries and dated readings. No code, tests,
  cryptanalytic artifacts or model scope changed; no new cipher search executed.

## LOG-CDF6EFF148

**Historical-clock source-note completion — documentation only**

Exact run start/end unknown

Type: source review. Outcome: Finite historical-clock review completed; no north-registered 1989 schedule

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Follow-up to 4835cdd1b4c6cc500788254d1364a5828630dde6. Museum der Dinge
  study-image source now supplied: parent visually identifies 24–25 June 1968
  perspective studies without a north reference or inscription schedule.
- Direct page reads confirmed the museum's 1968 calendar caption/credits and
  B.Z.'s 23 November 2024 report of Kunsch construction records/1969 letter patterns.
- Official project page retrieval failed; its lack of published drawings/inventory
  remains attributed to the parent's review. Unpublished contents not inspected;
  their ability to settle orientation/1989 state is not assumed.
- No north-referenced public face plan or full 1989 list found in that bounded review.
  No outreach authorized or made. Documentation consistency checks only; code and
  cryptanalytic results unchanged, no cipher tests or searches added.

## LOG-D7F30249FB

**GROMARK-IDENTIFIABILITY-001 — 73 fixed-model difference queries**

start: 2026-10-18T15:03:35.382531Z; end: 2026-10-18T15:03:35.401845Z

Type: identifiability analysis. Outcome: 10 positions forced, 63 variable under the fixed Gromark tuple; no solution

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Initial spec 25fa0615a08a4f629393c9b00c9cb78e92a85f38. Independent predictions
  and complete certificates arrived afterward; pre-execution protocol update
  bfab3d735e5e73824aeb5a2bfe5a9e471933c666 permits validating those certificates
  before fallback. Model, reference, 73 queries and resource caps unchanged.
- Implementation 5d93af5bd4a434c20b9c8a48a7f68963643ca523, then command:
  `python3 experiments/run_gromark_identifiability.py --spec-commit bfab3d735e5e73824aeb5a2bfe5a9e471933c666 --code-commit 5d93af5bd4a434c20b9c8a48a7f68963643ca523`.
- Result: 10 forced, 63 variable, 0 unresolved, all conditional on the unchanged tuple.
  39 unused-P swaps, 21 unused-C swaps, 3 complete supplied certificates; 10 exact
  component proofs. No exact K4 CSP fallback invoked. No full messages emitted.
- All variable witnesses independently check complete permutations, 24 cribs,
  target difference and 97-character regeneration. Forced positions 38/86 are transitive proofs.
- Controls: 231 toy bases / 9,396 permutation pairs; 515 difference queries / 27,052 pair
  checks (425 forced / 90 variable), including missing endpoints, global AllDifferent,
  positive/negative cases, caps and a marginally-variable/jointly-restricted toy.
  Supplied pool disabled for toy controls; no randomness.
- One process, 0.25 s / 10,000 states per query, 5 s controls, 20 s audit, 25 s registered cap.
  Actual 0.018 s; maximum recorded query 0.000119 s. All 112 tests pass in 8.302 s,
  preserving prior 104 tests and artifacts. Hashes verified; stable replay matched
  all proof-bearing records ignoring elapsed timing fields.
- Snapshot: `results/gromark-identifiability-runs/20261018T150335Z-5b16b46678154416add3015ab8676aa9/`.
- Marginal variability is not absence of joint constraints. Stop this audit; next
  need independently sourced key/alphabet restrictions or new confirmed evidence,
  not arbitrary completion or broader search. Strategy note added from repo evidence.

Related files: [experiments/run_gromark_identifiability.py](../../experiments/run_gromark_identifiability.py).

## LOG-065137A77A

**SILK-PERIODIC-001 — 2026-10-18**

start: 2026-10-18T15:32:21.428512Z; end: 2026-10-18T15:32:21.432293Z; date-only record: 2026-10-18 (heading; not a run timestamp)

Type: analytical constraints; replication. Outcome: All 12 fixed-chart periods contradicted; no keyword enumeration

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Source-first table and 24 decisive cells checked against both photographs; independent check supplied before pilot.
- Frozen specification bb0cfb9c0cd9c75b13782c1cc11cf34535e0fdd9; implementation f82749aa22e14c063d8fc3c02ff4e6f2a381c616.
- [Findings](../../research/SILK-PERIODIC-FINDINGS.md): all 12 periods contradicted, zero keyword enumeration, no full plaintext output. Proof already known before specification.
- Required segments JICEHTUFLMSXZ / TCUFDISXLFX; first segment gives 12 phase-origin-independent contradictions.
- Controls and 118 tests pass; 0.003 seconds action time under 5 seconds cap; no randomness. Stable proof replay and artifact hash checked.
- Snapshot `results/silk-periodic-runs/20261018T153221Z-b7f6cad7292747f6ba81099de8a671e1/`; [validation](../../results/SILK-PERIODIC-VALIDATION.json).
- Stop at fixed-chart, direct period 1–12 scope; no historical doctrine or whole-family exclusion.

Related files: [research/SILK-PERIODIC-FINDINGS.md](../../research/SILK-PERIODIC-FINDINGS.md), [results/SILK-PERIODIC-VALIDATION.json](../../results/SILK-PERIODIC-VALIDATION.json).

## LOG-38F65B1FC1

**DYNAMIC-KEY-001 — stateful key continuation, 2026-10-22**

start: 2026-10-22T12:01:28.661039Z; end: 2026-10-22T12:01:32.902143Z; date-only record: 2026-10-22 (heading; not a run timestamp)

Type: finite K4 model tests; null calibration. Outcome: 1,344 fixed stateful configurations reject; no decoding candidate

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Inspected active repository at 6af8caa, clean main; no applicable AGENTS.md.
  New local branch research/dynamic-key-20261022; no remote operations.
- Specification commit 4f0c056ee633828e88af89f9f6e066cf250a3606 precedes code
  11bc39f705ed24d1d591f0746f8217d78d39bb6f and the one actual run.
- Command: `python3 experiments/dynamic_key.py --spec-commit 4f0c056ee633828e88af89f9f6e066cf250a3606`.
- Result: 1,248 progressive-cycle and 96 ciphertext vowel/consonant extra-step
  configurations rejected; zero compatible/candidate cases. Four progressive
  first-crib survivors predict only 0–1/11 Berlin letters. Best same-data agreement
  is 14/24 in each family. No partial fit is treated as evidence of decoding.
- 199 histogram-preserving whole-family shuffles, seed 20261022; 268,800 total
  evaluations, 4.228 seconds under 60-second cap. Conditional plus-one tails:
  progressive 1.00, extra-step .56, combined 1.00. Exploratory, no historic p-value.
- Controls: 288 independent sequential roundtrips, 288 planted compatible models,
  288 mutated-constraint rejections; manual examples and toy exhaustive key scores.
- Full suite: 147 passing tests in 8.705 seconds. Added afterward: three passing
  artifact audits in .097 seconds, including every contradiction and saved hash.
- After run, static pinned cokernel.py/gap1.py inspection confirms progressive
  prior art, not new invention or a threshold-gap closure. Corrected interpretation
  preserves unchanged specification/results. No third-party code executed.
- Report, exact scopes, three ranked mechanisms and next experiment:
  [DYNAMIC-KEY-FINDINGS.md](../../research/DYNAMIC-KEY-FINDINGS.md). No geographic retest.
- Saved run: results/dynamic-key-runs/20261022T120128Z-c15ba5ffeb55479490d2be553daf60f0/.

Related files: [experiments/dynamic_key.py](../../experiments/dynamic_key.py), [research/DYNAMIC-KEY-FINDINGS.md](../../research/DYNAMIC-KEY-FINDINGS.md).

## LOG-830CBACD57

**ASYMMETRIC-PRIMER-001 and PLAINTEXT-STEP-001 — 2026-10-22**

start: 2026-10-22T12:08:17.094398Z; end: 2026-10-22T12:08:17.163153Z; start: 2026-10-22T12:10:01.334882Z; end: 2026-10-22T12:10:01.439299Z; date-only record: 2026-10-22 (heading; not a run timestamp)

Type: finite K4 model tests; null calibration. Outcome: Six mixed-alphabet and 12 plaintext-step cases reject

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Verified selected pinned prior-art gaps by static source reads: Barney
  plaintext-autokey predecessor threshold excludes lag 10; Scott P2 executes
  through lag 7. Local complete proof assumes one shared alphabet.
- ASYMMETRIC-FEEDBACK-001 specification 56b2919 is deferred/unrun. Parent supplied
  narrower fixed pilot before implementation or scores, registered separately.
- Six-case spec 2d23dab6bbe773aa7d00de699834ce4df5bc446d; implementation
  74792b65bc2f591f99e94ac06df52b727444e5d7. PALIMPSEST, lag 10, addition,
  independent Ap/Ac/Ak in AZ/KRYPTOS excluding all-equal triples. No fitted keys.
  All six outputs fail, scores 1,1,0,1,1,5/24. 199 whole-family shuffled controls,
  seed 20261024, 1,200 evaluations, .067 seconds; plus-one tail .015.
  The best fails 19 known letters; tail is exploratory, not a recovered candidate.
- Twelve-case spec 37bc4bf1635089d51f361f33bfd771b691e836fa; implementation
  ea210bd (full SHA in result). Three words x two alphabets x two PT-trigger
  classes, initial cursor 0 and 1/2 after-plaintext extra steps. Zero candidates;
  best 3/24. 199 whole-family shuffled controls, seed 20261025, 2,400 evaluations,
  .102 seconds; plus-one tail .54. No score-based expansion.
- Asymmetric controls: 4,056 exhaustive symbol cases, six full planted messages
  and altered-crib rejections, 48 numeric-oracle comparisons. PT-step controls:
  2,600 symbol/key-phase cases, twelve planted recoveries/rejections, 96 oracles.
- Original baseline/K1-K3 controls pass. Independent artifact audit re-encodes
  every actual output character, verifies hashes/chronology and null accounting.
- Final full suite: 160 tests pass, 8.876 seconds. No errors/failures.
- Findings/ranking/scopes: [FIXED-PILOT-FINDINGS.md](../../research/FIXED-PILOT-FINDINGS.md).
- Saved runs: results/asymmetric-primer-runs/20261022T120817Z-ef4199fc397e4bd9bc6ca2fb3bfdc2e2/
  and results/plaintext-step-runs/20261022T121001Z-38f7134c1bc3445ea7bf00efc70d2e11/.
  Both completed exactly once after specification and code commits.
- No remote operation; prior experiments/results remain unchanged.

Related files: [research/FIXED-PILOT-FINDINGS.md](../../research/FIXED-PILOT-FINDINGS.md).

## LOG-4836570143

**Documentation-only proposal — 2026-10-22**

Exact run start/end unknown; date-only record: 2026-10-22 (heading; not a run timestamp)

Type: documentation and proposal. Outcome: 32-case coordinate proposal unrun at this stage; later result retained separately

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

Recorded H-SPLIT-COORDINATE-ROUTES in the hypothesis log and fixed-pilot findings:
32 formal independent row/column coordinate-route cases, explicitly unrun and
low evidence; global novelty unproved. Added parent-supplied Friedman/LANAKI
references after targeted PDF text inspection, with historical/source limitations.
No implementation, specification for execution, K4 scores, null controls or test
run was added. Earlier 160-test validation and all result artifacts unchanged.

## LOG-6CF7C1F4A2

**ASYMMETRIC-FEEDBACK-001 / SPLIT-COORDINATE-001 — completed continuation**

start: 2026-10-22T19:19:52.714193Z; end: 2026-10-22T19:19:53.226206Z; start: 2026-10-22T19:21:26.800516Z; end: 2026-10-22T19:21:27.093611Z; date-only record: 2026-10-22 (date statement; not a run timestamp); original date statement: 22 October 2026. Initial state clean at 6eba0fd on

Type: finite K4 model tests; null calibration. Outcome: 72 feedback and 32 split-coordinate cases reject

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Date: 22 October 2026. Initial state clean at 6eba0fd on
  research/dynamic-key-20261022; scoped work, no Site or remote changes.
- Reused unchanged feedback specification 56b2919e4af7bbce644ed476d5fde8c0546627b7,
  implemented at 0a5ad2dea648397e40678177c0d1f0515d96e029, then ran once:
  `python3 experiments/asymmetric_feedback.py --spec-commit 56b2919e4af7bbce644ed476d5fde8c0546627b7`.
  72 configurations, no compatible primer. One training survivor, lag 12 true
  Beaufort with Ap=Ac=AZ, Ak=KRYPTOS, predicts only 2/11 Berlin letters. All roots
  fixed by first crib; only 13-L training consistency checks, all 11 Berlin predictions
  untouched by current fitting (but historically public). No candidate.
- Feedback null: 199 complete fitted-root/family scans, seed 20261023, 14,400 models,
  .503 s under 60 s cap; modal score 15/24, 35 exceedances, plus-one tail .18.
  Controls:72 planted recoveries/mutated rejections,108 toy cases/1,080 exhaustive
  primer decryptions,24 same-alphabet limiting comparisons.
- Coordinate spec afcb5e6297d868b38722b695c96e1ee8468363a3 precedes implementation
  11ce1453f0480103af21cd7c964084f3bf1e5a4b, then ran once:
  `python3 experiments/split_coordinate.py --spec-commit afcb5e6297d868b38722b695c96e1ee8468363a3`.
  32 formal/32 exact distinct transformations; no candidates, max 3/24.
  199 whole-family shuffled scans, seed 20261027, 6,400 models, .290 s under 30 s;
  160 exceedances, plus-one tail .805. Controls:32 planted inverses/rejections,
  64 independent matrix-oracle comparisons,21,632 source-pair checks,24 ragged-route
  checks and 3 exact-signature identity/difference controls.
- Independent artifact tests verify every feedback root by forward lane enumeration,
  all rejection witnesses, Berlin predictions, all 3,104 coordinate-output letters,
  consulted hashes, spec ancestry, null maxima and exact CIA-anchor agreement.
- Full suite 174 tests pass 9.324 s, original artifacts retained. No repeated new
  experiment runs, score-driven variants or language scoring.
- Results: results/asymmetric-feedback-001-runs/20261022T191952Z-44bf1543c641497e82f4b948d0cd94ea/
  and results/split-coordinate-001-runs/20261022T192126Z-2ff96ae3a6914cab8db6cd9c0c7ceb5c/.
- [Findings, parameter counts, scopes and next step](../../research/CONTINUATION-FINDINGS.md);
  [validation receipt](../../results/CONTINUATION-VALIDATION.json). Both bounded
  families rejected; no solution. Next: compare fully specified forthcoming
  K3-derived composite route against existing 66 permutations before any new run.

Related files: [experiments/asymmetric_feedback.py](../../experiments/asymmetric_feedback.py), [experiments/split_coordinate.py](../../experiments/split_coordinate.py), [research/CONTINUATION-FINDINGS.md](../../research/CONTINUATION-FINDINGS.md), [results/CONTINUATION-VALIDATION.json](../../results/CONTINUATION-VALIDATION.json).

## LOG-CCE99A2060

**K3-CLOCK-ROUTES-001 — 22 October 2026, 19:32 UTC**

start: 2026-10-22T19:32:38.042794Z; end: 2026-10-22T19:32:38.167873Z; date-only record: 2026-10-22 (heading; not a run timestamp)

Type: exact K4 constraints. Outcome: 374 new structures reject; 16 prior equivalents skipped

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Initial clean state e83624f on research/dynamic-key-20261022. Local work only.
- Score-free preflight: U14 after U42 matches all 336 K3 fixture letters, exact
  existing K3 permutation and separate matrix oracle. Saved ROUTE-001 catalogue
  matches all 66 current routes. T97 is absent; four clock routes match old IDs
  R036/R040/R038/R042. Complete unrestricted-key plus/KRYPTOS period and layer
  domains verified before skipping their sixteen exact structures.
- Specification dcb246cdd997ecd2f0b4f3a4c536ca65d8a47a14, then implementation
  9ea6b35f46a43374839096a7ac39594df94656ca, then one actual command:
  `python3 experiments/k3_clock_routes.py --spec-commit dcb246cdd997ecd2f0b4f3a4c536ca65d8a47a14`.
- 390 raw structures, 16 prior-equivalent skips, 374 newly tested structures.
  F1 four single-key cases rejected; F2 two sandwich cases rejected; F3 all 368
  new 24-sector cases rejected. No compatible keys/plaintexts or new English.
- Both sandwich training graphs are forests: 18 vertices, 13 edges, five
  components, zero checks, four plaintext-relevant offsets. All-crib graphs
  c=1, full graphs d=1; seven joint held-out checks. Frozen training individually
  predicts only one/two Berlin edges, all fail. Cycle witnesses give residuals
  5/2 modulo 26; inconsistent cases have zero assignments despite exponent c-d=0.
- Runtime .071886 s under 30 s; no null simulations for wholly contradicted
  families. No additional parameter, Site edit, optical experiment or remote push.
- Controls: 372 single-key planted inverses/mutations, two sandwich inverses/cycle
  mutations, five exhaustive base-3 graph cases / 1,215 key assignments, gauge,
  isolates, offset joins, parallel edges, independent K3 oracle and baseline controls.
- Independent artifact audit verifies all 372 exact slot witnesses, both cycle
  sums/component counts, unknown cross-component predictions, prior-domain skip
  receipts, consulted hashes and chronology. Full suite: 187 pass, 8.941 s.
- Snapshot: results/k3-clock-routes-001-runs/20261022T193238Z-99bf9337176c469e9d7742f2a21f2aca/.
- [Findings and exact rejected scope](../../research/K3-CLOCK-ROUTE-FINDINGS.md);
  [validation](../../results/K3-CLOCK-ROUTES-VALIDATION.json). No solution.

Related files: [experiments/k3_clock_routes.py](../../experiments/k3_clock_routes.py), [research/K3-CLOCK-ROUTE-FINDINGS.md](../../research/K3-CLOCK-ROUTE-FINDINGS.md), [results/K3-CLOCK-ROUTES-VALIDATION.json](../../results/K3-CLOCK-ROUTES-VALIDATION.json).

## LOG-146AC47B80

**OCCUPIED-CELL-ROUTES-001 — 22 October 2026, 19:39 UTC**

start: 2026-10-22T19:39:53.371154Z; end: 2026-10-22T19:39:53.467220Z; date-only record: 2026-10-22 (heading; not a run timestamp)

Type: finite K4 model tests. Outcome: All 288 carved-mask fixed-key branches reject

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Separate from completed K3/clock batch at 7b13316714b6fa40fd118c30b0e311fe0819beb5.
- Score-free fixture/coverage check: OBKR columns 28–31 then three full 31-letter
  rows, exact 97-letter baseline; eight routes distinct and absent from original 66 and
  newer 97-route catalogues. Full prior key domains/layer orders checked; no skips.
- Specification 29bf8e997b0290f56366ad27a7adb52a50ccb1b9, then implementation
  6cc4b0d4b0d71002a55d59bd07a96c7d7ebe0332, then one actual run:
  `python3 experiments/occupied_cell_routes.py --spec-commit 29bf8e997b0290f56366ad27a7adb52a50ccb1b9`.
- 288 raw/exact unique new fixed branches: 8 routes x 18 literal phased keys x 2 orders.
  All reject all-24 gate; max 5/24, no lead. Zero fitted parameters per branch.
  Full outputs tagged rejected_model_output. Runtime .092467 s under 15 s cap.
- No null simulation needed/run for entirely contradicted family; no p-value.
- Controls:288 planted full/crib recoveries,288 altered-crib negatives,288 independent
  explicit encoders,8 unique-index cell-oracle/inverse checks,676 symbol controls.
- Independent artifact audit re-encodes all 27,936 output letters, checks every
  score/signature, fixed mask, coverage, hashes/chronology and previous independent
  simple sandwich certificates. Full suite: 195 pass, 9.135 s; earlier results intact.
- Parent reviewer reports independent all 336 K3 matches, six K3 negatives/positives
  and 384 raw clock negatives/positives. Attributed corroboration only; do not add
  these as novel-search coverage. Our 16 prior skips remain 16.
- [Findings](../../research/OCCUPIED-CELL-FINDINGS.md), [validation](../../results/OCCUPIED-CELL-VALIDATION.json).
  Snapshot results/occupied-cell-routes-001-runs/20261022T193953Z-6f4f8efe83e345168a18fdc2f134d845/.
- Local-only, no Site change, no new optical claim, no expanded parameters/families.

Related files: [experiments/occupied_cell_routes.py](../../experiments/occupied_cell_routes.py), [research/OCCUPIED-CELL-FINDINGS.md](../../research/OCCUPIED-CELL-FINDINGS.md), [results/OCCUPIED-CELL-VALIDATION.json](../../results/OCCUPIED-CELL-VALIDATION.json).

## LOG-87A1CDB9B5

**STRATEGY-FOLLOWUP-001 — 22 October 2026**

start: 2026-10-22T20:48:42.987845Z; end: 2026-10-22T20:48:43.398039Z; date-only record: 2026-10-22 (heading; not a run timestamp)

Type: finite K4 tests; source replication; synthetic calibration. Outcome: Four state models reject; clock operator underidentified; synthetic fits often ambiguous

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Frozen spec/source commit `4ec45e0`; implementation committed at `b238209` before
  K4 evaluation. [Findings](../../research/STRATEGY-FOLLOWUP-FINDINGS.md) link complete provenance.
- Four fixed move-to-front state models: all **0/24**, first contradiction at 22.
  No fitted letters or rule expansion; full97 inverses independently checked.
- Four reachable-state witnesses outside 207 distinct affine maps (208 raw role,
  sign, shift descriptions) exclude equivalence to prior cursor stepping.
- Blinded selector:32/32 unique planted recoveries;0/32 nearby-control survivors;
  0/199 matched-decoy survivors. Actual24crib structure preserved throughout.
- K1 observed key-entry/ILLUSION account reproduces all63 letters; K2 restored-S
  deletion reproduces full as-inscribed stream and endpoint. No K4 correction.
- Clock shared-phase visible-hour control passes4 heldout labels; K4 operator
  **underidentified**, not failed or timed out. Missing1989inventory/operator.
- Four-symbol exact volume calibration:23,040 candidate-instance checks;15/20
  plants ambiguous,6/20 shuffles compatible. Not K4 synthesis or a large classifier.
- Run `20261022T204842Z-17a364bb210f4d8799018ef99b496f3a`, Python3.9.6,0.3972s.
  Independent recurrence proposal audited for overlap, not rerun locally.


### Follow-on convention replication and supplied proof audit —22 October

- CP-CONVENTION-REPLAY-001: fresh pinned public pair, two frozen conventions,
  restarted key at letter778 matches1133/1133; uninterrupted matches777 then
  fails356. Full independent inverse, no plaintext repairs or K4 reset tests.
- RECURRENCE-CERTIFICATE-REVIEW-001: supplied AZ parity/KRYPTOS unit-determinant
  contradictions verified from fixed fixtures. Rejects the declared affine
  feedback grammar already in first crib, regardless of primer. Not a duplicate
  913952-description search or a count of globally new models.
- Exact sources, code/spec commits, immutable results and limitations are in
  [the dated findings addendum](../../research/STRATEGY-FOLLOWUP-FINDINGS.md).


### Independent followup package replay —22 October

- Three archives/member manifests verified;40original source/result files saved
  under independent/2026-10-22. All private source photos/crops remain outside repo.
- Independent four-state audit, its recency decoder and JS oracle agree exactly;
  no new model cases. Classifier replay reproduces125/144,44/48uniform forced-label
  warning,all288fixed-key inverses and199label-null values. No K4 posterior.
- Reviewed local-equation auditor reproduces recurrence candidate/plaintext counts
  without repeating full enumeration; known prior overlap remains documented.
- Historical clock replay:41label and1152slot roundtrips; no K4 trial. NEW YORK
  relative panel placement visually checked, without1989orUTCinference.
- [Integration findings](../../research/INDEPENDENT-FOLLOWUP-INTEGRATION-2026-10-22.md);212tests pass.
  Construction-worker artifact still pending at this stage.


### Final independent construction integration —22 October

- Final archive/member manifest verified;9original files added separately,49total
  independent-original files retained across four packages. No pages/photos/caches.
- Fresh retrieval and offline replay match all five original source hashes and
  derived checks. Both corrupted-input controls reject. CP1133pair hashes match
  earlier local replay; second published ciphertext transcript agrees exactly.
- Source row22,column33 identifies semantic start778, not panel boundary566.
  K2 intendedletter362 reconciles retainedcharacter365 via3questionmarks.
- All222offline regressions pass, including7original construction controls.
  Proposed5071sensitivity variants remain unrun; canonicalK4unchanged.
- [Final integration report](../../research/INDEPENDENT-FOLLOWUP-INTEGRATION-2026-10-22.md): bounded
  four-track batch complete, no K4 lead; clock's specific data/operator limits remain.

Related files: [research/INDEPENDENT-FOLLOWUP-INTEGRATION-2026-10-22.md](../../research/INDEPENDENT-FOLLOWUP-INTEGRATION-2026-10-22.md), [research/STRATEGY-FOLLOWUP-FINDINGS.md](../../research/STRATEGY-FOLLOWUP-FINDINGS.md).

## LOG-1282C9929E

**SINGLE-BOUNDARY-RESET-001 — 22 October 2026**

start: 2026-10-22T21:24:16.807343Z; end: 2026-10-22T21:24:19.517134Z; date-only record: 2026-10-22 (heading; not a run timestamp)

Type: exact K4 constraints; finite model tests. Outcome: All declared single-reset families reject; no multi-reset sweep

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Spec `f67e282` committed before implementation `5c22aca` and evaluation.
  Same state/seed/key, no reset or one of 96 internal boundaries; no edits.
- MTF: 388 raw cases (4 covered baselines, 384 new boundaries), all first-crib
  contradictions. QQ/SS local certificate and a fixed-four position-27 analytical
  corollary are verified; no multi-reset sweep.
- Affine feedback: every one of 194 alphabet/schedule structures impossible.
  Untouched-island parity witnesses exclude the full 88,653,344 raw-description
  upper bound; 35,152 local coefficient checks find no training survivors, so no
  seed enumeration. Old baselines and parameter aliases are not novel trials.
- Periodic audit: 6,984 raw descriptions → 3,476 canonical models; 48 covered
  baselines, 3,428 new reset schedules. All fail EASTNORTHEAST. Key negation and
  phase signatures deduplicated; no guessed completion or new period.
- Literal-crib controls: 32/32 true MTF messages retained, 16 uniquely determined
  and 16 ambiguous; 0/8 nearby and 0/32 shuffled acceptances. Recurrence and periodic
  plants/inverses, zero-divisor seed ambiguity and mutation controls pass.
- Run `20261022T212416Z-f634e152375e406d971f9edc1dc91096`, 2.465 seconds.
  Independent archive verified and exactly replayed separately; 231 tests pass.
- [Readable findings and scope](../../research/SINGLE-BOUNDARY-RESET-FINDINGS.md). No K4 lead,
  second reset, extra model, canonical change, main or Site update.

Related files: [research/SINGLE-BOUNDARY-RESET-FINDINGS.md](../../research/SINGLE-BOUNDARY-RESET-FINDINGS.md).

## LOG-50D6A15662

**AUTONOMOUS-RECURRENCE-001 — 22 October 2026**

start: 2026-10-22T21:53:56.923388Z; end: 2026-10-22T21:53:57.013922Z; date-only record: 2026-10-22 (heading; not a run timestamp)

Type: analytical constraints. Outcome: All 20 order-2–6 structures fail first-crib parity equations

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Frozen spec `5615caf`, implementation `4354cc2`, then actual evaluation.
  Two fixed alphabets, orders 2–6, zero/fitted constant: 20 formal structures.
- All 20 inconsistent on first-crib key values modulo 2. Affine order six has
  F2 rank/augmented rank 6/7 and F13 7/7 in both alphabets: no CRT solution.
- Identical six-key parity contexts with opposite next parity provide compact
  internal certificates. Zero coefficient enumeration, prefix states or Berlin
  forecast comparisons on actual K4; empty-set predictions are not applicable.
- 80 literal-crib truth-inclusion plants and 12 complete small-ring parameter/seed
  comparisons pass. Sixty planted coefficient tuples admit ambiguous prefixes;
  nonunit/unreachable states and exact affine-union counts are checked.
- Static pinned Barney lag-two/five-feature overlap reviewed without execution;
  homogeneous order two is not a globally new method. Startup degeneracies audited.
- Independent hash-verified JavaScript source and exact deterministic output replay
  agree on all ranks/counts; 231 independent controls pass. Its unused positive
  branch is not adopted as a general survivor solver.
- Run `20261022T215356Z-4769d0b137d348e99db42ee5918dc799`, 0.087 seconds;
  242 local regression tests pass. [Findings](../../research/AUTONOMOUS-RECURRENCE-FINDINGS.md).
- No order expansion, resets, tree layer, edits, new route, main or Site change.

Related files: [research/AUTONOMOUS-RECURRENCE-FINDINGS.md](../../research/AUTONOMOUS-RECURRENCE-FINDINGS.md).

## LOG-632AA33E27

**ALPHABET-GEOMETRY-001 and GEOMETRIC-PILOT-001 — 22 October 2026**

Exact run start/end unknown; date-only record: 2026-10-22 (heading; not a run timestamp)

Type: representation validation; finite K4 model tests. Outcome: Unique glyph codes verified; periodic/rotor pilots yield no all-crib candidate

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

The [representation](../../research/ALPHABET-GEOMETRY-REPRESENTATION.md) gives 26 unique binary
arrays and exact base-2/base-3 codes; 325 pair comparisons, strict codebook
round trips and 910 mutations pass. Ordinary sums and modulo-26 codes collide.
The [frozen pilots](../../research/ALPHABET-GEOMETRY-PILOT-SPEC.md) were committed before K4
evaluation. A has 18 baseline rechecks and six new geometric-alphabet cases;
only Beaufort period 12 fits training and fails Berlin. B has zero first-crib
survivors among 3,640 raw models and 3,640 distinct outputs. All 72 complete-selector
plants retain truth, including one ambiguous feedback plant. See
[findings](../../research/GEOMETRIC-PILOT-FINDINGS.md) and full result/control records. No new
null calibration is needed for these exact rejections; no scope expansion.

Related files: [research/ALPHABET-GEOMETRY-PILOT-SPEC.md](../../research/ALPHABET-GEOMETRY-PILOT-SPEC.md), [research/ALPHABET-GEOMETRY-REPRESENTATION.md](../../research/ALPHABET-GEOMETRY-REPRESENTATION.md), [research/GEOMETRIC-PILOT-FINDINGS.md](../../research/GEOMETRIC-PILOT-FINDINGS.md).

## LOG-88B9863D50

**GEOMETRIC-FOLLOWUP-001 — independent replay and numeric security audit**

Exact run start/end unknown; date-only record: 2026-10-22 (opening prose; not a run timestamp)

Type: replication; encoding security audit. Outcome: Prior outputs reproduced; raw-number mapping leaks almost all tested letter/base pairs

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

22 October 2026. Original independent pilot and changing-base security bundles
are preserved unchanged with archive/member hashes and exact replay receipts.
All 24 periodic conflict/fit records and all 3,640 prior full feedback outputs
match the independent oracle. This is reproduction, not new K4 search coverage.
The separate finite raw-number lookup across bases 2–61 has 1,560 letter/base
pairs, 1,558 numbers and only the documented 8/27 ambiguities; it requires known
token boundaries, public geometry/order and no extra transform. No roots or
root offsets were searched. [Security findings](../../research/GEOMETRIC-BASE-SECURITY-AUDIT.md)
and [exact comparisons](../../results/GEOMETRIC-FOLLOWUP-COMPARISON.json) preserve the
full scope, ambiguity controls and every lookup result.

Related files: [research/GEOMETRIC-BASE-SECURITY-AUDIT.md](../../research/GEOMETRIC-BASE-SECURITY-AUDIT.md), [results/GEOMETRIC-FOLLOWUP-COMPARISON.json](../../results/GEOMETRIC-FOLLOWUP-COMPARISON.json).

## LOG-2CA57EE155

**GEOMETRIC-PERIODIC-NULL-001 — requested first-crib chance calibration**

Exact run start/end unknown; date-only record: 2026-10-22 (opening prose; not a run timestamp)

Type: statistical calibration. Outcome: Full 24-model null p=0.0866; first-crib fit fails Berlin

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

22 October 2026. The independent plan was frozen before null simulation, after
the actual first-crib fit was known. Full 24-model refitting on 19,999 shuffles
reproduces 1,731 exceedances and plus-one Monte Carlo p=0.0866; distribution
18,268/1,728/3 for zero/one/two survivors. Exact single period-12 closure chance
is 382/(97*96). All 479,976 outcomes match the pairwise checker, 5,256 match the
prior oracle, and 24 plants pass. Replay numerical fields and draw/count trace
are exact; only Python version metadata differs (3.12.14 versus local 3.9.6).
[Report](../../research/PERIODIC-CRIB-CALIBRATION.md). No rotor or global-hypothesis calibration.

Related files: [research/PERIODIC-CRIB-CALIBRATION.md](../../research/PERIODIC-CRIB-CALIBRATION.md).

## LOG-C02D304144

**K4-FROZEN-GLYPH-AFFINE-FEEDBACK-001 — arbitrary-base relaxation**

Exact run start/end unknown; date-only record: 2026-10-22 (opening prose; not a run timestamp)

Type: analytical constraints. Outcome: All eight frozen affine feature-feedback families excluded in first crib

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

22 October 2026. Original frozen specification, pre-test schema amendment and
two independent implementations are preserved. Both replay byte for byte and
exclude all eight formal affine feature-feedback families within the first crib,
using minimum two-transition parity certificates and full modulo-26 checks.
All 3,264 primary synthetic round trips and retained-coefficient controls pass.
Arbitrary independent bases >=2 contain every proposed digit-plus-two root
schedule, so no root/degree/radix/offset search is needed for this exact family.
Berlin is not evaluated here; the auxiliary direct map remains separately
labeled. [Report](../../research/RADIX-FEEDBACK-FINDINGS.md). No post-failure scope expansion.

Related files: [research/RADIX-FEEDBACK-FINDINGS.md](../../research/RADIX-FEEDBACK-FINDINGS.md).

## LOG-422AF7CAEC

**IPA-PREPROCESSING-001 — source-fixed phonetic preprocessing**

Exact run start/end unknown

Type: source normalization; exact K4 constraints. Outcome: All 48 defined IPA arithmetic structures reject; no broad IPA exclusion

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

Protocol commit 2c40fca; controls/input commit 6499d17; final interface e09593f,
all before local actual evaluation. Source audit had already observed the local
13/11 code-point lengths with public clue lengths known; no blind-discovery claim.
Forty-eight synthetic complete selectors retain truth, with expected mapping
ambiguity; nine complete small-ring and three exhaustive planted alias-domain
comparisons pass. Local first-window CRT constraints reject 47 structures by
ordinary anchors and AZ-additive period 10 through shared ː indices 13 versus 11.
Zero actual aliases enumerated; no Berlin aliases fitted. The independent frozen
anchor audit uses both windows and its 48 certificates replay exactly; a separate
post-audit supplement confirms the stronger first-window conclusion. The same
fixed IPA source strings serialize to X-SAMPA lengths 13/12; no extra cipher test.
[Findings](../../research/IPA-PREPROCESSING-FINDINGS.md), [actual records](../../results/IPA-PREPROCESSING-001.json),
[local source/replay checks](../../results/IPA-SOURCE-COMPARISON.json). Prior phonetic
respelling records are unchanged. No scope expansion after negatives.

Related files: [research/IPA-PREPROCESSING-FINDINGS.md](../../research/IPA-PREPROCESSING-FINDINGS.md), [results/IPA-PREPROCESSING-001.json](../../results/IPA-PREPROCESSING-001.json), [results/IPA-SOURCE-COMPARISON.json](../../results/IPA-SOURCE-COMPARISON.json).

## LOG-F7AEB85D53

**AFFINE-DIGRAPH-PARITY-001 — existing analytical boundary recorded**

Exact run start/end unknown; date-only record: 2026-10-23 (opening prose; not a run timestamp)

Type: analytical constraints; replication. Outcome: Four same-alphabet affine-digraph structures excluded by parity

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

23 October 2026. Four parent-supplied exact first-crib witnesses are independently
verified against canonical fixtures. Identical two-symbol input parity has
different output parity, excluding the specified same-AZ or same-KRYPTOS fixed
affine 2×2 map for both pair origins, even without invertibility. Zero keys or
matrices searched. Sixteen fixed affine positive cases and sixteen parity
mutations pass. [Boundary and corrected status](../../research/AFFINE-DIGRAPH-PARITY-BOUNDARY.md).

Related files: [research/AFFINE-DIGRAPH-PARITY-BOUNDARY.md](../../research/AFFINE-DIGRAPH-PARITY-BOUNDARY.md).

## LOG-7A1A7579D4

**23 October 2026: stateful tree/path pilot and independent IPA integration**

Exact run start/end unknown; date-only record: 2026-10-23 (heading; not a run timestamp)

Type: finite K4 tests; independent replication. Outcome: All 104 tree settings reject; unanchored IPA/codecs audits replayed

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

The two fixed tree/subtree-permutation constructions were implemented, controlled and tested continuously across all 97 positions. All 104 settings fail the first crib; this is a bounded negative, not a general tree-cipher exclusion. See [TREE-PATH-CIPHER-FINDINGS.md](../../research/TREE-PATH-CIPHER-FINDINGS.md). Independent free-map IPA and source-fixed pronunciation codec audits now replay exactly; see [IPA-CODECS-INTEGRATION.md](../../research/IPA-CODECS-INTEGRATION.md). No additional search was launched after these failures.

Related files: [research/IPA-CODECS-INTEGRATION.md](../../research/IPA-CODECS-INTEGRATION.md), [research/TREE-PATH-CIPHER-FINDINGS.md](../../research/TREE-PATH-CIPHER-FINDINGS.md).

## LOG-E32CDBB0CC

**REGISTRY-20261023 — current hypothesis scope and evidence gates**

Exact run start/end unknown

Type: documentation and scope audit. Outcome: Canonical coverage registry established; no new K4 evaluation

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

Documentation and coverage audit only; zero new K4 evaluations. The current
[canonical section in HYPOTHESES.md](../../research/HYPOTHESES.md#current-canonical-coverage-register--23-october-2026)
tracks 55 stable mechanisms with evidence, finite coverage, missing inputs,
dependencies and the next discriminating test. Historical entries are preserved.
The template now uses the same status vocabulary and required fields. Registry
regressions check ID uniqueness, previous-ID retention, required fields and local
reference existence; these are documentation checks, not cryptanalysis trials.

Compass frames/reverse bearings, physical mirror/order conventions, shadow/time,
celestial observations and historical World Clock extraction await the incoming
source review and independent measurement gates. No geometry, date, label or
orientation was fitted. Lamp/Greek models lack a declared invertible bridge or
key-generation rule. Greek phonetic rendering separately awaits its sourced
mapping. No lamp/Greek count correspondence was promoted into a cipher.

A proposed lamp representation control would audit H=5a+b, M=5c+d with c up to
11 and retain seconds parity explicitly. The seconds lamp cannot recover all 60
seconds from one bit: full-second timestamps must not be claimed reversible.
This is a preflight proposal, not a frozen or executed K4 experiment. A clock-to-key
operator and progression must be justified separately before a K4 protocol.

The previously completed 104-setting tree pilot is linked as a narrow negative;
future topology/state rules need a separate equivalence audit, framing/inverse,
full-message state treatment and preregistration. Machine/book/nonlinear ideas
remain source/specification-gated; an unrestricted OTP is non-identifiable.

Related files: [research/HYPOTHESES.md](../../research/HYPOTHESES.md).

## LOG-81FEBCA5D6

**FACE-ROW-001 / LAMP-STREAM-001 — source-gated conditional protocols**

Exact run start/end unknown

Type: source review; protocol preparation. Outcome: Source review saved; FACE/LAMP actual runs still pending at this stage

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

The deep evidence synthesis and three source dossiers were materialized, hash-
verified, read locally and preserved unchanged. [Integration receipt](../../results/LODESTONE-COMPASS-EVIDENCE-INTEGRATION-001.json).
The [protocol](../../research/CONDITIONAL-FACE-LAMP-SPEC.md) was frozen in 3eeb0b1 before any
new K4 evaluation. Parent review is pending; both actual pilots remain unrun.

FACE-ROW-001 coverage only: 768 orientation aliases reduce to 372 distinct full
model signatures. 280 are covered by the retained ROUTE-001 negatives; 92
horizontal carved-row cases remain new. [Complete coverage](../../results/FACE-ROW-001-COVERAGE.json),
reproduced by `python3 experiments/face_row_coverage.py`, reads previous results
and never scores actual K4 ciphertext. Every new training phase is observed
under either layer order, so no absent key entry may be guessed.

LAMP-STREAM-001 proposes exactly 11,520 fixed lamp-state phase/alphabet/equation
descriptions, not a free wiring or historical time fit. The modern supplier's
row-count description is a source for representation only. Binary field weights
and one-minute character sampling are declared conditional design choices.
Mengenlehreuhr is distinct from the confirmed World Clock. No Greek label map,
source date, surveyed bearing or historical city list is inferred.

The current register now has 56 stable entries, with physical claims still
blocked on missing independent measurements and Greek transcription still
missing a complete codec. [Current readiness receipt](../../results/HYPOTHESIS-REGISTER-002.json).

Related files: [experiments/face_row_coverage.py](../../experiments/face_row_coverage.py), [research/CONDITIONAL-FACE-LAMP-SPEC.md](../../research/CONDITIONAL-FACE-LAMP-SPEC.md), [results/FACE-ROW-001-COVERAGE.json](../../results/FACE-ROW-001-COVERAGE.json), [results/HYPOTHESIS-REGISTER-002.json](../../results/HYPOTHESIS-REGISTER-002.json), [results/LODESTONE-COMPASS-EVIDENCE-INTEGRATION-001.json](../../results/LODESTONE-COMPASS-EVIDENCE-INTEGRATION-001.json).

## LOG-C08A348378

**FACE-ROW-001 / LAMP-STREAM-001 — completed finite batch**

Exact run start/end unknown

Type: exact K4 constraints; finite model tests. Outcome: 92 new FACE cases reject; frozen LAMP family excluded analytically

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

Parent review approved the protocol at cdefbb4. Implementation and controls were
committed at 25e107f before K4 evaluation. [Findings](../../research/CONDITIONAL-FACE-LAMP-FINDINGS.md)
and [complete actual result](../../results/CONDITIONAL-FACE-LAMP-001.json).

FACE-ROW-001 tested 92 new canonical structures and skipped 280 exact previously
covered ones. Ninety reject in training; two KRYPTOS/additive period-12 structures
fit twelve values plus one closure, then predict HSTZCLZPDSB or LQHXLMKCWIQ:
both zero of eleven Berlin letters. Both full decryptions regenerate C; zero
all-crib candidates. All 92 literal plants retain truth through the full selector;
eight have two compatible plaintexts and remain explicitly ambiguous.

LAMP-STREAM-001 has four exact first-crib parity contradictions. All 11,520 raw
descriptions are excluded analytically; zero actual phase models were enumerated,
and Berlin was not used by this proof. Display/inverse, 32 complete-selector
plants and timing/incompatible controls pass; aliases and logical versus simulated
control counts are retained. The separately written post-run JS oracle agrees
with all face classifications and lamp certificates. No null significance claim,
new sampling rule, bit order, route or other parameter follows these negatives.

Related files: [research/CONDITIONAL-FACE-LAMP-FINDINGS.md](../../research/CONDITIONAL-FACE-LAMP-FINDINGS.md), [results/CONDITIONAL-FACE-LAMP-001.json](../../results/CONDITIONAL-FACE-LAMP-001.json).

## LOG-030EF284F5

**GREEK-PHONETIC-001 / SIGABA-INSPIRED-001 — completed candidate batch**

Exact run start/end unknown

Type: finite K4 model tests. Outcome: Defined Greek-placement and custom SIGABA-inspired domains reject

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

[Specification](../../research/GREEK-SIGABA-CANDIDATE-SPEC.md) committed at 7bc893f; complete
implementation/planted controls at 6f5ba70; conditional null seeds clarified
before actual runs at a9e4db1. [Full findings](../../research/GREEK-SIGABA-CANDIDATE-FINDINGS.md).

Greek uses one fixed approximate 13-phone Modern Greek rendering and a reversible
24-Greek-character/26-cipher-symbol periodic layer. Lossy English transcription
is not an English inverse. All 3,003 ordered transformed-window placements,
40 outer structures and 120,120 descriptions are covered, without assuming English
crib offsets. Of 3,080 first-stage sites, 324 fit; all 12,664 eligible second-window
checks fail. Zero full fits, zero null calibration, no adaptive dialect or offset.
Forty complete selector plants preserve the true key/location and all aliases.

The SIGABA-inspired model is custom, not authentic SIGABA: fixed keyword-derived
wirings, a declared collector and restricted starts. 6,760 raw keys normalize to
3,380 schedule/offset classes; all reject by first-crib position 25. No Berlin
check or full actual candidate is needed. Twelve complete selector plants retain
both raw-key schedule aliases; all 7,260 rotor inverse and carry controls pass.
The post-run independent JS arithmetic agrees on both complete finite domains.
Authentic historical SIGABA remains outside coverage, explicitly tracked separately.

Related files: [research/GREEK-SIGABA-CANDIDATE-FINDINGS.md](../../research/GREEK-SIGABA-CANDIDATE-FINDINGS.md), [research/GREEK-SIGABA-CANDIDATE-SPEC.md](../../research/GREEK-SIGABA-CANDIDATE-SPEC.md).

## LOG-C8DE9E7E6E

**23 October 2026 — historical SIGABA and exclusion-scope audit**

Exact run start/end unknown; date-only record: 2026-10-23 (heading; not a run timestamp)

Type: finite K4 tests; analytical constraints; scope audit. Outcome: 13,520 historical-simulator keys reject; four crossed affine structures inconsistent

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

SIGABA-CSP889-001 implements the historical mechanism with the published simulator wiring set. Twelve external known-answer vectors pass after an explicit source-derived convention translation; no downloaded software is executed. The frozen 13,520-key domain has zero first-crib survivors; no Berlin evaluation, no broad SIGABA exclusion. [Specification](../../research/SIGABA-CSP889-SPEC.md), [findings](../../research/SIGABA-CSP889-FINDINGS.md), [controls](../../results/SIGABA-CSP889-001-controls.json), [complete result](../../results/SIGABA-CSP889-001.json).

The [exclusion audit](../../research/EXCLUSION-SCOPE-AUDIT-2026-10-23.md) reviews all 57 canonical records with exact finite coverage, alias accounting and preprocessing assumptions; historical long searches are not represented as freshly rerun. Its concrete untested affine-digraph gap led to AFFINE-DIGRAPH-CROSSED-001: four crossed-role structures, all inconsistent on the first crib, with sixteen literal plants and thirty-six complete small-ring comparisons. [Frozen protocol](../../research/AFFINE-DIGRAPH-CROSSED-SPEC.md), [findings](../../research/AFFINE-DIGRAPH-CROSSED-FINDINGS.md), [proofs](../../results/AFFINE-DIGRAPH-CROSSED-001.json).

Related files: [research/AFFINE-DIGRAPH-CROSSED-FINDINGS.md](../../research/AFFINE-DIGRAPH-CROSSED-FINDINGS.md), [research/AFFINE-DIGRAPH-CROSSED-SPEC.md](../../research/AFFINE-DIGRAPH-CROSSED-SPEC.md), [research/EXCLUSION-SCOPE-AUDIT-2026-10-23.md](../../research/EXCLUSION-SCOPE-AUDIT-2026-10-23.md), [research/SIGABA-CSP889-FINDINGS.md](../../research/SIGABA-CSP889-FINDINGS.md), [research/SIGABA-CSP889-SPEC.md](../../research/SIGABA-CSP889-SPEC.md), [results/AFFINE-DIGRAPH-CROSSED-001.json](../../results/AFFINE-DIGRAPH-CROSSED-001.json), [results/SIGABA-CSP889-001-controls.json](../../results/SIGABA-CSP889-001-controls.json), [results/SIGABA-CSP889-001.json](../../results/SIGABA-CSP889-001.json).

## LOG-02A279928A

**23 October 2026 — exact full cipher-state inference and physical sources**

Exact run start/end unknown; date-only record: 2026-10-23 (heading; not a run timestamp)

Type: exact K4 inference; physical source review. Outcome: All starts under 520 fixed schedules reject; physical gaps remain

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

SIGABA-CSP889-STATE-002 removes the repeated-cipher-start restriction using a two-/three-wheel meet-in-the-middle join. All 520 fixed schedules and all five independent cipher starts are covered: 6,178,315,520 raw descriptions, including the old 13,520 subset. The 350,311 three-letter joined states all fail by position29; zero full first-crib survivors, zero Berlin evaluations. This is not billions of independently executed decryptions or a complete SIGABA exclusion. [Frozen specification](../../research/SIGABA-CSP889-STATE-SPEC.md), [findings](../../research/SIGABA-CSP889-STATE-FINDINGS.md), [controls](../../results/SIGABA-CSP889-STATE-002-controls.json), [complete schedule results](../../results/SIGABA-CSP889-STATE-002.json).

The supplied [physical addendum](../../research/evidence/2026-10-23-lodestone-compass/KRYPTOS-PHYSICAL-EVIDENCE-ADDENDUM-2026-10-23.md) is preserved separately from the original ZIP. [Local visual verification](../../research/evidence/2026-10-23-lodestone-compass/PHYSICAL-ADDENDUM-LOCAL-REVIEW.md) covers eleven selected scans and maintains source conflicts and archival access limits. No invented optical geometry, bearing test or Site change follows from the new source evidence.

Related files: [research/SIGABA-CSP889-STATE-FINDINGS.md](../../research/SIGABA-CSP889-STATE-FINDINGS.md), [research/SIGABA-CSP889-STATE-SPEC.md](../../research/SIGABA-CSP889-STATE-SPEC.md), [research/evidence/2026-10-23-lodestone-compass/KRYPTOS-PHYSICAL-EVIDENCE-ADDENDUM-2026-10-23.md](../../research/evidence/2026-10-23-lodestone-compass/KRYPTOS-PHYSICAL-EVIDENCE-ADDENDUM-2026-10-23.md), [research/evidence/2026-10-23-lodestone-compass/PHYSICAL-ADDENDUM-LOCAL-REVIEW.md](../../research/evidence/2026-10-23-lodestone-compass/PHYSICAL-ADDENDUM-LOCAL-REVIEW.md), [results/SIGABA-CSP889-STATE-002-controls.json](../../results/SIGABA-CSP889-STATE-002-controls.json), [results/SIGABA-CSP889-STATE-002.json](../../results/SIGABA-CSP889-STATE-002.json).

## LOG-B3E944F67A

**23 October 2026 — joint-controller boundary and exact non-rotor pivot**

Exact run start/end unknown; date-only record: 2026-10-23 (heading; not a run timestamp)

Type: synthetic feasibility; exact K4 constraints. Outcome: Joint controller unresolved; declared cyclic-disc/two-round Feistel models reject

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

SIGABA-JOINT-FEASIBILITY-003 exactly collapses 100,000 index starts to 66,058 magnet functions, but leaves full joint controller inference unimplemented/budget-unresolved. No new actual K4 rotor key search ran. Synthetic timings are projections, not impossibility proofs. The [findings](../../research/JOINT-STATE-NONROTOR-FINDINGS.md) give a sound symbolic formulation and resource limits.

NONROTOR-STRUCTURAL-004 tests the frozen cyclic-disc invariant and eight two-round additive Feistel structures with arbitrary shared round functions. Four fail training; four fit 13 letters with 39 function entries still free, then force an incorrect plaintext letter at position 68. All eight reject without function-key enumeration. Unknown partners at crib edges are handled exactly. Original source-table defects and initial redundant second-stage diagnostics are preserved. [Specification](../../research/NONROTOR-STRUCTURAL-SPEC.md), [final constraints](../../results/NONROTOR-STRUCTURAL-004.json), [controls](../../results/NONROTOR-STRUCTURAL-004-controls.json), [independent certificates](../../results/NONROTOR-STRUCTURAL-004-independent.json). No extra rounds or variants were added after failure.

Related files: [research/JOINT-STATE-NONROTOR-FINDINGS.md](../../research/JOINT-STATE-NONROTOR-FINDINGS.md), [research/NONROTOR-STRUCTURAL-SPEC.md](../../research/NONROTOR-STRUCTURAL-SPEC.md), [results/NONROTOR-STRUCTURAL-004-controls.json](../../results/NONROTOR-STRUCTURAL-004-controls.json), [results/NONROTOR-STRUCTURAL-004-independent.json](../../results/NONROTOR-STRUCTURAL-004-independent.json), [results/NONROTOR-STRUCTURAL-004.json](../../results/NONROTOR-STRUCTURAL-004.json).

## LOG-A614466742

**23 October 2026 — exact wrapper audit, three-round ambiguity and tree-state support**

Exact run start/end unknown; date-only record: 2026-10-23 (heading; not a run timestamp)

Type: exact K4 constraints; identifiability analysis. Outcome: 24 wrapper cases and tree relaxation reject; three-round fits non-identifiable

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

[FEISTEL-SYMMETRY-005](../../research/FEISTEL-EXTENSION-SPEC.md) proves all 32 wrapper/coordinate/origin families unequal by explicit synthetic counterexamples. The eight previous no-swap cases are skipped; all 24 newly evaluated cases reject (twelve in training, twelve at the public second stage). Family inequality does not imply disjointness or independent evidence.

FEISTEL-THREE-005 exactly counts four canonical three-round arbitrary-function structures. Each is compatible with all 24 cribs and has more than 10^75 complete-function key descriptions; two different full plaintext witnesses per case prove non-identifiability. The independent signed-potential/sequential-allocation JavaScript counter agrees on all eight training/all-crib counts. Raw key volumes are not plaintext-class counts or probabilities. No additional round was tested.

[TREE-STATE-SUPPORT-006](../../research/TREE-STATE-SUPPORT-SPEC.md), frozen separately before its evaluation, prioritizes a registered alternative: all four fixed tree/direction primitives fail each known island even when every initial cipher-label permutation is granted. The plaintext-to-path assignment remains fixed. No prefix reset or reachable-state assumption is used. Forty complete toy permutation comparisons, forty mutation controls and twelve continuous literal-crib plants validate this necessary-condition relaxation. [Combined findings and limitations](../../research/FEISTEL-TREE-EXTENSION-FINDINGS.md).

Related files: [research/FEISTEL-EXTENSION-SPEC.md](../../research/FEISTEL-EXTENSION-SPEC.md), [research/FEISTEL-TREE-EXTENSION-FINDINGS.md](../../research/FEISTEL-TREE-EXTENSION-FINDINGS.md), [research/TREE-STATE-SUPPORT-SPEC.md](../../research/TREE-STATE-SUPPORT-SPEC.md).

## LOG-E76967DAFB

**23 October 2026 — arbitrary-key Fractionated Morse constraints**

Exact run start/end unknown; date-only record: 2026-10-23 (heading; not a run timestamp)

Type: exact K4 constraints. Outcome: 348,160 declared Morse contexts reject without key enumeration

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

MASK-FM-ARBITRARY-007 replaces the prior two fixed alphabets with every bijection between A–Z and the 26 standard Morse trigrams. All 348,160 first-crib word-break/stream-offset contexts reject on repeated cipher-symbol coordinate conflicts, without Berlin evaluation or 26!-key enumeration. Plaintext letter indices are not equated to ciphertext positions. Six complete planted first-stage selectors retain the true keys; 100 complete small permutation comparisons and an independent coordinate-slot oracle validate the result. [Frozen protocol](../../research/FRACTIONATED-MORSE-ARBITRARY-SPEC.md), [scoped findings and frontier](../../research/FRACTIONATED-MORSE-ARBITRARY-FINDINGS.md), [results](../../results/MASK-FM-ARBITRARY-007.json). Other Morse procedures and outer layers remain outside coverage.

Related files: [research/FRACTIONATED-MORSE-ARBITRARY-FINDINGS.md](../../research/FRACTIONATED-MORSE-ARBITRARY-FINDINGS.md), [research/FRACTIONATED-MORSE-ARBITRARY-SPEC.md](../../research/FRACTIONATED-MORSE-ARBITRARY-SPEC.md), [results/MASK-FM-ARBITRARY-007.json](../../results/MASK-FM-ARBITRARY-007.json).

## LOG-57CEE0C89F

**23 October 2026 — Wheatstone fixed-transition invariant**

Exact run start/end unknown; date-only record: 2026-10-23 (heading; not a run timestamp)

Type: analytical constraints. Outcome: Aligned fixed-ring Wheatstone model excluded; other conventions outside scope

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

WHEATSTONE-TRANSITION-008 closes the arbitrary-outer-alphabet gap beyond pinned dictionary-ring tests. Repeated processed ST pairs have different ciphertext equality flags (RV versus SS), excluding the aligned fixed-ring model for arbitrary ring alphabets and starts. No K4 key enumeration or Berlin evaluation ran. Two published modern worked vectors, a tooth-by-tooth oracle, 443,976 factored toy transitions, naive complete size-3/4 controls and 24 continuous literal-crib plants pass. [Protocol](../../research/WHEATSTONE-TRANSITION-SPEC.md), [source findings and precise alignment limits](../../research/WHEATSTONE-TRANSITION-FINDINGS.md), [certificate](../../results/WHEATSTONE-TRANSITION-008.json). Full original historical instructions and other authentic machine variants remain source-gated; no denied source was retrieved through an alternate route.

Related files: [research/WHEATSTONE-TRANSITION-FINDINGS.md](../../research/WHEATSTONE-TRANSITION-FINDINGS.md), [research/WHEATSTONE-TRANSITION-SPEC.md](../../research/WHEATSTONE-TRANSITION-SPEC.md), [results/WHEATSTONE-TRANSITION-008.json](../../results/WHEATSTONE-TRANSITION-008.json).

## LOG-42E6620EB8

**23 October 2026 — disciplined frontier review, no new K4 search**

Exact run start/end unknown; date-only record: 2026-10-23 (heading; not a run timestamp)

Type: documentation and frontier review. Outcome: Nine evidence/algorithm gates recorded; no new K4 search

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

FRONTIER-011 reviews all 60 canonical entries and identifies nine concrete evidence/algorithm gates. No new evidence-grounded cryptanalysis protocol is currently ready; this is a human research assessment, not a universal exhaustion theorem. Stale scope/input pointers (crossed-role affine digraphs, authentic versus inspired SIGABA and its joint solver, finite asymmetric feedback, regional declination and K2 restoration controls) were corrected without duplicate evaluation. [Concise frontier](../../research/RESEARCH-FRONTIER-2026-10-23.md), [runnable inventory/preflight and retained replay specifications](../../research/specifications/FRONTIER-2026-10-23.json), [complete assessment](../../results/FRONTIER-011.json). No new K4 trials, denied-source requests or Site changes.

Related files: [research/RESEARCH-FRONTIER-2026-10-23.md](../../research/RESEARCH-FRONTIER-2026-10-23.md), [research/specifications/FRONTIER-2026-10-23.json](../../research/specifications/FRONTIER-2026-10-23.json), [results/FRONTIER-011.json](../../results/FRONTIER-011.json).

## LOG-F2014ABCF5

**23 October 2026 — complete coupled synthetic SIGABA inference**

Exact run start/end unknown; date-only record: 2026-10-23 (heading; not a run timestamp)

Type: synthetic solver benchmark. Outcome: Tiny exact sets agree; larger toy cases resource/validation limited; no real gate pass

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

SIGABA-JOINT-TOY-012 implements a shared reachable index-domain constraint solver with continuous control evolution and independent cipher starts. Ten complete tiny-system raw-key truth streams match byte for byte, with ambiguity preserved. A five-wheel q=6 case completes and retains one raw planted key; a q=4 case exceeds the independent validation-output cap, and q=8 hits the frozen 600-second cap after 5,080/32,768 control starts. The real-sized scaling gate is not passed. No actual K4 ciphertext is evaluated, no free per-time masks or sampled substitute key slice is introduced, and no packages are installed. [Frozen protocol](../../research/SIGABA-JOINT-TOY-SPEC.md), [engineering findings](../../research/SIGABA-JOINT-TOY-FINDINGS.md), [complete summary and per-case hashes](../../results/SIGABA-JOINT-TOY-012.json). Real historical contacts/five-index adapter and stronger factorized or symbolic-control representation remain future work.

Related files: [research/SIGABA-JOINT-TOY-FINDINGS.md](../../research/SIGABA-JOINT-TOY-FINDINGS.md), [research/SIGABA-JOINT-TOY-SPEC.md](../../research/SIGABA-JOINT-TOY-SPEC.md), [results/SIGABA-JOINT-TOY-012.json](../../results/SIGABA-JOINT-TOY-012.json).

## LOG-9CB9A54AA7

**SIGABA-TORUS-013 — exact predicate reuse, unchanged coupled domain**

Exact run start/end unknown

Type: synthetic solver benchmark. Outcome: Largest toy completes with exact validation; no real-sized admission

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

The largest toy inference completed all 32,768 controllers in 534.476 seconds, retaining 2 raw keys. Its declared validation status is True. This is a toy result, not a real-sized gate. Ten independent complete raw-set comparisons and one complete compact-set comparison pass. Predicate identity is checked over 6,739 predicates and 998,515 direct states. No actual K4 evaluation, real-sized gate, package install or Site change. [Protocol](../../research/SIGABA-TORUS-SPEC.md), [findings](../../research/SIGABA-TORUS-FINDINGS.md), [measured comparison](../../results/SIGABA-TORUS-013.json).

Related files: [research/SIGABA-TORUS-FINDINGS.md](../../research/SIGABA-TORUS-FINDINGS.md), [research/SIGABA-TORUS-SPEC.md](../../research/SIGABA-TORUS-SPEC.md), [results/SIGABA-TORUS-013.json](../../results/SIGABA-TORUS-013.json).

## LOG-CA734C7E5B

**CSP889-REAL-014 — authentic adapter, failed synthetic resource admission**

Exact run start/end unknown

Type: synthetic solver benchmark; known-answer validation. Outcome: Published vectors pass; both real-sized synthetic gates stop with zero controllers

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

Twelve published vectors pass both directions through adapter, direct machine and physical contacts; six complete tiny systems match independent full raw-key truth. The two frozen real-sized fixtures stop at 17.223 seconds (branch envelope) and 60.161 seconds (wall), both with zero completed controllers. Totals are unknown; no K4 evaluation or negative key coverage. [Protocol](../../research/SIGABA-REAL-ADAPTER-SPEC.md), [findings](../../research/SIGABA-REAL-ADAPTER-FINDINGS.md). [STAT-001 cross-version diagnosis](../../research/STAT-CROSSVERSION-FINDINGS.md) preserves integer draws/tails and archives, checking derived floats against rational moments.

Related files: [research/SIGABA-REAL-ADAPTER-FINDINGS.md](../../research/SIGABA-REAL-ADAPTER-FINDINGS.md), [research/SIGABA-REAL-ADAPTER-SPEC.md](../../research/SIGABA-REAL-ADAPTER-SPEC.md), [research/STAT-CROSSVERSION-FINDINGS.md](../../research/STAT-CROSSVERSION-FINDINGS.md).

## LOG-A10D7AEA61

**CSP889-SPARSE-015 — exact sparse ownership and reserved cache**

Exact run start/end unknown

Type: synthetic solver benchmark. Outcome: Memory reduced; both gates unresolved with zero completed controllers

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

Both runs remain unresolved, with zero completed controllers and unknown total key counts. The dense case reaches the same time-2, 410-node envelope guard, with 202 predicate requests but only three zero-offset builds. The separated-window case still stops at time index 7 with 6,652 peak nodes and zero predicate requests; memory falls to 58.4 MiB, but prefix CPU work remains unresolved. It performed 519,540 owner transitions and 14,181 branch visits. Direct plants remain valid, but no selector recovery or full real-sized compatible-set validation is established. Same two REAL-014 fixtures and caps; six complete independent tiny raw-key comparisons, 18 cache-policy relation comparisons and complete q=3 predicate controls pass. [Protocol](../../research/SIGABA-SPARSE-OWNERSHIP-SPEC.md), [findings](../../research/SIGABA-SPARSE-OWNERSHIP-FINDINGS.md), [comparison](../../results/CSP889-SPARSE-015.json). No actual K4 evaluation or budget expansion.

Related files: [research/SIGABA-SPARSE-OWNERSHIP-FINDINGS.md](../../research/SIGABA-SPARSE-OWNERSHIP-FINDINGS.md), [research/SIGABA-SPARSE-OWNERSHIP-SPEC.md](../../research/SIGABA-SPARSE-OWNERSHIP-SPEC.md), [results/CSP889-SPARSE-015.json](../../results/CSP889-SPARSE-015.json).

## LOG-BA42F28BCF

**CSP889-DOMAIN-016 — profiler-supported immutable domain keys**

Exact run start/end unknown

Type: synthetic solver benchmark. Outcome: Prefix advances but zero controllers complete; resource gate unresolved

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

The prefix run advances from time index 7 to 17, retaining all 66,058 class owners at peak and reaching 35,290 peak nodes, 1,186,963 owner transitions and 249,550 branch visits. It still completes zero controllers and makes zero predicate requests. Therefore actual controller coverage does not advance, although the partial prefix does. It times out at 60.003 seconds with 84.9 MiB peak RSS. The dense case stops at the same time-2 memory frontier after 3.426 seconds with 546.3 MiB RSS. Both total key counts remain unknown; neither is a K4 negative. The unchanged prefix profile attributes 58.075/60.009 seconds self time to merge; phase B caches exact-domain hashes with collision-safe equality. Six complete independent tiny sets and cache invariance pass. [Protocol](../../research/SIGABA-DOMAIN-IDENTITY-SPEC.md), [implementation freeze](../../research/SIGABA-DOMAIN-IDENTITY-IMPLEMENTATION.md), [findings](../../research/SIGABA-DOMAIN-IDENTITY-FINDINGS.md), [comparison](../../results/CSP889-DOMAIN-016.json). No adaptive extra optimization, cap increase, Site change or K4 evaluation.

Related files: [research/SIGABA-DOMAIN-IDENTITY-FINDINGS.md](../../research/SIGABA-DOMAIN-IDENTITY-FINDINGS.md), [research/SIGABA-DOMAIN-IDENTITY-IMPLEMENTATION.md](../../research/SIGABA-DOMAIN-IDENTITY-IMPLEMENTATION.md), [research/SIGABA-DOMAIN-IDENTITY-SPEC.md](../../research/SIGABA-DOMAIN-IDENTITY-SPEC.md), [results/CSP889-DOMAIN-016.json](../../results/CSP889-DOMAIN-016.json).

## LOG-25534E2EC4

**CSP889-ANCHOR-017 — exact full-torus observation anchoring**

Exact run start/end unknown

Type: synthetic solver benchmark. Outcome: Anchoring validated exactly; observed-domain memory stops full inference

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

Eight complete tiny original-key streams and 24 cache-policy correlated relations agree with physical/unanchored truth, including map-dependent inverse and final offsets. The unchanged separated-window real fixture now reaches observations 21–24 in 4.310 seconds, then hits the branch-memory envelope; zero controllers complete and totals remain unknown. A premature run after an inert mutation-test failure is quarantined and not counted as official coverage. The corrected full gate passed before official rerun. [Protocol](../../research/SIGABA-FIRST-OBSERVATION-SPEC.md), [findings](../../research/SIGABA-FIRST-OBSERVATION-FINDINGS.md), [chronology](../../results/ANCHOR-017-chronology.json). No K4, statistical pruning, filter panel or cap increase.

Related files: [research/SIGABA-FIRST-OBSERVATION-FINDINGS.md](../../research/SIGABA-FIRST-OBSERVATION-FINDINGS.md), [research/SIGABA-FIRST-OBSERVATION-SPEC.md](../../research/SIGABA-FIRST-OBSERVATION-SPEC.md), [results/ANCHOR-017-chronology.json](../../results/ANCHOR-017-chronology.json).

## LOG-FA7E198169

**CSP889-COMPACT-018 — exact storage, local-only measured controller progress**

Exact run start/end unknown

Type: synthetic solver benchmark. Outcome: 12/14 controllers complete in fixed fixtures; full-domain totals unresolved

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

Actual native controller coverage advances from zero to 12 completed controllers on the dense fixture and 14 on the separated-window fixture. They stop at the unchanged 60-second wall limit, not the old memory envelope, at 162.6 and 152.8 MiB peak RSS. No compatible raw keys occur in either completed controller prefix; the remaining 11,881,364 and 11,881,362 controllers are unresolved. The unfinished controller is retained explicitly. Total key counts remain unknown, not zero. The completed prefixes represent 14,257,651,200,000 and 16,633,926,400,000 raw start descriptions respectively, including index aliases; those are model-domain descriptions, not independent hypotheses or unique plaintexts. Eight tiny fixtures under three representations and three cache policies preserve complete original-key sets, final offsets and anchor inverses. The native result uses explicit exact set encodings. [Protocol](../../research/SIGABA-COMPRESSED-DOMAIN-SPEC.md), [pre-run storage choice](../../research/SIGABA-COMPRESSED-DOMAIN-IMPLEMENTATION.md), [findings](../../research/SIGABA-COMPRESSED-DOMAIN-FINDINGS.md), [comparison](../../results/CSP889-COMPACT-018.json). No K4, extra observation, cap increase or remote publication.

Related files: [research/SIGABA-COMPRESSED-DOMAIN-FINDINGS.md](../../research/SIGABA-COMPRESSED-DOMAIN-FINDINGS.md), [research/SIGABA-COMPRESSED-DOMAIN-IMPLEMENTATION.md](../../research/SIGABA-COMPRESSED-DOMAIN-IMPLEMENTATION.md), [research/SIGABA-COMPRESSED-DOMAIN-SPEC.md](../../research/SIGABA-COMPRESSED-DOMAIN-SPEC.md), [results/CSP889-COMPACT-018.json](../../results/CSP889-COMPACT-018.json).

## LOG-8768DC3A4D

**CSP889-FILTER-019 — supplied-anchor necessary filter, local only**

Exact run start/end unknown

Type: synthetic filter diagnostic. Outcome: 20 supplied-anchor pairs: zero false negatives; not blind recovery/full coverage

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

Two frozen panels retain 2/3 anchors and 4 controllers each: 20 pairs, 12 filter rejections, 6 false-positive passes and 2 physical feasible pairs. All 1,321,160 reachable-map trials are actually audited, including rejects; zero false negatives. Both supplied plants regenerate the full synthetic ciphertext; fixture1 advances the 29-position unknown gap and passes its second block. The smaller fixture0 panel is preserved after its 16-candidate anchor cap. Counterfactual savings are panel-only, not a full-domain speedup. [Protocol](../../research/SIGABA-COLLECTOR-FILTER-SPEC.md), [findings](../../research/SIGABA-COLLECTOR-FILTER-FINDINGS.md), [summary](../../results/CSP889-FILTER-019.json). No new full-domain controller coverage, K4, cap expansion or publication retry.

Related files: [research/SIGABA-COLLECTOR-FILTER-FINDINGS.md](../../research/SIGABA-COLLECTOR-FILTER-FINDINGS.md), [research/SIGABA-COLLECTOR-FILTER-SPEC.md](../../research/SIGABA-COLLECTOR-FILTER-SPEC.md), [results/CSP889-FILTER-019.json](../../results/CSP889-FILTER-019.json).

## LOG-470EDB8058

**FOLD-SLIDE-020 — anchored progressive monument overlay**

Exact run start/end unknown; date-only record: 2026-10-23 (date statement; not a run timestamp); original date statement: 2026-10-23 UTC. Exact run start/end were not recorded and are unknown; commit/publication times are distinct.

Type: inscription-layout comparison; null calibration. Outcome: 134 frames retained; no unusual excess under declared controls; optics uncalibrated

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Date: 2026-10-23 UTC. Exact run start/end were not recorded and are unknown; commit/publication times are distinct.
- Type: actual inscription-layout comparison with approximate optical apertures, not a K4 decryption search.
- Protocol: [frozen progressive model](../../research/MONUMENT-SLIDE-OVERLAY-SPEC.md), [pre-score registration amendment](../../research/MONUMENT-SLIDE-REGISTRATION-AMENDMENT.md).
- Input: full canonical cipher/tableau rows and existing modeled font; MYVGT/AABCD anchor reproduced with no row shift.
- Coverage: 134 frames across two registrations, −33…+33 inclusive; 130 active. Every frame retained.
- Outcome: zero-shift primary 35/856 identical letters; no unusual full-scan label/area excess under 1,999 row shuffles and 1,999 movable-row rotations. Four-report adjusted p=1 for each endpoint/scheme.
- Code: [native evaluator](../../experiments/monument_slide.py), [independent pixel oracle](../../experiments/monument_slide_oracle.mjs).
- Receipt: [exact positions and masks](../../results/FOLD-SLIDE-020-actual.json); [findings and limitations](../../research/MONUMENT-FOLD-SLIDE-FINDINGS.md).
- No measured optical calibration, plaintext extraction, Site change or new decoding candidate.

Related files: [experiments/monument_slide.py](../../experiments/monument_slide.py), [experiments/monument_slide_oracle.mjs](../../experiments/monument_slide_oracle.mjs), [research/MONUMENT-FOLD-SLIDE-FINDINGS.md](../../research/MONUMENT-FOLD-SLIDE-FINDINGS.md), [research/MONUMENT-SLIDE-OVERLAY-SPEC.md](../../research/MONUMENT-SLIDE-OVERLAY-SPEC.md), [research/MONUMENT-SLIDE-REGISTRATION-AMENDMENT.md](../../research/MONUMENT-SLIDE-REGISTRATION-AMENDMENT.md), [results/FOLD-SLIDE-020-actual.json](../../results/FOLD-SLIDE-020-actual.json).

## LOG-5BA1042A0F

**SITE-OVERLAY-015 — live Site source handoff and static validation**

receipt recording: 2026-10-23T13:32:55.553417Z; date-only record: 2026-10-23 (date statement; not a run timestamp); original date statement: 2026-10-23 UTC, integration record date; exact original Site-test and publication times were not supplied.

Type: Site source archive; static data validation. Outcome: Live v15 and 87 code tests owner-reported; local bytes/oracle data match; rendered QA blocked

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Date: 2026-10-23 UTC, integration record date; exact original Site-test and publication times were not supplied.
- Type: Site source archive and static data validation, not an additional K4 cipher experiment.
- The parent relayed native publication confirmation: Site version 15 live, public access revision 2 unchanged. Source commit `086ace2bfb2ca6e23ddddf76fe5f37c51dd75aea`, based on `d4155931cd760d4222c9f66916551110eb40053b`. No deployment performed here.
- Exact local patch archived; all 25 changed paths and 18 new-file bodies independently match the source commit, with no child-checkout write. Candidate/dist new modules agree.
- Input/glyph values and all 134 embedded column-frame oracle records match retained research data. Local validation is static and executes no handed-off JavaScript.
- Owner reports 87 code tests passed. Actual rendered-browser QA remained blocked by locked Mac; no local full Site suite or native-browser replay is claimed.
- Row movement is exploratory; no systematic row scan or inherited column-only null p-value.
- [Archive and limitations](../site-source/manual-overlay-v15/README.md), [receipt](../../results/SITE-MANUAL-FOLD-V15-SOURCE-HANDOFF.json), [static verifier](../../experiments/verify_manual_overlay_handoff.py).

Related files: [docs/site-source/manual-overlay-v15/README.md](../site-source/manual-overlay-v15/README.md), [experiments/verify_manual_overlay_handoff.py](../../experiments/verify_manual_overlay_handoff.py), [results/SITE-MANUAL-FOLD-V15-SOURCE-HANDOFF.json](../../results/SITE-MANUAL-FOLD-V15-SOURCE-HANDOFF.json).

## LOG-9B64FD9FE3

**FOLD-SLIDE-2D-001 — item 1 systematic row-plus-column overlay**

start: 2026-10-23T23:47:52.868636Z; end: 2026-10-23T23:49:19.600426Z; end: 2026-10-23T23:49:19.600187Z; date-only record: 2026-10-23 (date statement; not a run timestamp); original date statement: 2026-10-23 UTC, original computation. Manifest start `2026-10-23T23:47:52.868636Z`, end `2026-10-23T23:49:19.600426Z`; job-level start/end are retained separately. Commit/publication times are not substituted.

Type: inscription-layout comparison; whole-search calibration. Outcome: 7,638 frames completed; no unusual label/area excess under either full-search control; physical optics uncalibrated

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Date: 2026-10-23 UTC, original computation. Manifest start `2026-10-23T23:47:52.868636Z`, end `2026-10-23T23:49:19.600426Z`; job-level start/end are retained separately. Commit/publication times are not substituted.
- Type: inscription-layout comparison and whole-search chance calibration, not a cipher or plaintext-generation model. Item 1 only; items 2–8 not started.
- Frozen specification `f6aafc4735b8ff9e4f7e01975a97baf9991e1583`, validated implementation `0584bbc3340ce8a50a7fed3a53feaed202420c4f`, then original run. Later runner change adds execution-purpose metadata only, defaulting repeats to replay.
- Domain: both existing registrations, dx −33…+33, dy −28…+28, no wrapping and same-facing double reflection. 7,638 raw frames / 7,150 active; 134 prior row-zero frames reproduce exactly, 7,504 nonzero-row frames newly covered.
- Largest standardized label excess: 21/248 comparable pairs, dx=+19, dy=−7, primary registration. Whole-search tails 0.7475 shuffle / 0.7635 rotation. Area tails 0.6500 / 0.6090. All four-report adjusted p-values are 1. No unusual excess or cipher candidate.
- Controls: 1,999 full-selector draws per scheme, fixed original anchor/row histograms/punctuation/tableau; exact means and exact signed-rational ranking. Independent cell/pixel code checks all 7,638 frames and positions; 18 complete-selector toy plants and ambiguity/expectation/mutation controls precede evaluation.
- Complete positions: 57,674 label matches, 1,506,846 positive surrogate intersections. No lexical scoring or arbitrary extraction. Measured physical optics remain outside coverage.
- [Findings](../../research/FOLD-SLIDE-2D-FINDINGS.md), [frozen protocol](../../research/FOLD-SLIDE-2D-SPEC.md), [all-frame table](../../results/FOLD-SLIDE-2D-001-frames.csv), [summary](../../results/fold-slide-2d-001-runs/20261023T234752Z-ddb7425463b745a4b3d70b1b669dd641/summary.json), [manifest](../../results/fold-slide-2d-001-runs/20261023T234752Z-ddb7425463b745a4b3d70b1b669dd641/manifest.json), [native implementation](../../experiments/monument_slide_2d.py).
- The stale current SIGABA scope wording is corrected to COMPACT-018’s 12 and 14 synthetic controllers; historical zero-controller stages remain preserved. No new SIGABA/K4 joint search, Site deployment or subsequent item.

Related files: [experiments/monument_slide_2d.py](../../experiments/monument_slide_2d.py), [research/FOLD-SLIDE-2D-FINDINGS.md](../../research/FOLD-SLIDE-2D-FINDINGS.md), [research/FOLD-SLIDE-2D-SPEC.md](../../research/FOLD-SLIDE-2D-SPEC.md), [results/FOLD-SLIDE-2D-001-frames.csv](../../results/FOLD-SLIDE-2D-001-frames.csv), [results/fold-slide-2d-001-runs/20261023T234752Z-ddb7425463b745a4b3d70b1b669dd641/manifest.json](../../results/fold-slide-2d-001-runs/20261023T234752Z-ddb7425463b745a4b3d70b1b669dd641/manifest.json), [results/fold-slide-2d-001-runs/20261023T234752Z-ddb7425463b745a4b3d70b1b669dd641/summary.json](../../results/fold-slide-2d-001-runs/20261023T234752Z-ddb7425463b745a4b3d70b1b669dd641/summary.json).

## LOG-B53BA1797D

**PHYSICAL-SOLAR-002 — item 2 conditional sunlight, lamp geometry and evidence gates**

start: 2026-10-24T00:17:28.772639Z; end: 2026-10-24T00:17:29.483736Z

Type: analytical constraints; source research. Outcome: Conditional solar/ray/blur limits verified; surveyed optical decoder remains evidence-blocked

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Original quantitative run start/end UTC: 2026-10-24T00:17:28.772639+00:00 / 2026-10-24T00:17:29.483736+00:00. This is not a source exposure time. Independent worker run times are unknown; separate local replay receipt records validation times.
- Kind: physical analytical constraints and source research; no K4 cipher evaluation.
- Frozen specification: `b2cc1dffdbb71b7a11c38f8041d220f3fce82932`; [protocol](../../research/PHYSICAL-SOLAR-002-SPEC.md), [findings](../../research/PHYSICAL-SOLAR-002-FINDINGS.md), [runner](../../experiments/physical_solar_002.py), [complete receipt/output](../../results/physical-solar-002/README.md).
- Scope: 96 declared solar-envelope scenarios including old exact-bearing baselines; 39 independently source-fixed calendar samples; 125 dimensionless height-order cases. 960,096 dense grid, 39 USNO/NOAA and 125 ray checks pass. No parameters fitted to K4.
- Outcome: conditional solar and direct-ray constraints verified. ENE Sun versus ENE ground shadow differ; a below-aperture source cannot directly project onto lower ground. Actual source/aperture/receiver heights and surveyed heading remain unknown. No source-fixed optical key, decoder or intended celestial time identified.
- Independent addition: [evidence/arithmetic package](../../independent/2026-10-24/physical-item2/README.md), received with outcomes known and separately replayed. Finite solar disk, ideal thickness clipping and angular sensitivities verified; these are not measured installed blur/strokes. No original images/scrapes committed.
- Image feasibility: original LOC TIFF SHA verified and native crop inspected; same exposure as prior service image. No certified aperture-to-ground pairs established, no camera/light fit. Proposed 12-pair calibration remains unpassed. All broader physical/navigation hypotheses retain evidence-blocked status. Item 3 not started; no Site change.
- Aggregate validation: 497 tests pass on both supported Python versions; [validation receipt](../../results/PHYSICAL-SOLAR-002-VALIDATION.json) records validation start/end separately from the original physical calculation.

Related files: [experiments/physical_solar_002.py](../../experiments/physical_solar_002.py), [independent/2026-10-24/physical-item2/README.md](../../independent/2026-10-24/physical-item2/README.md), [research/PHYSICAL-SOLAR-002-FINDINGS.md](../../research/PHYSICAL-SOLAR-002-FINDINGS.md), [research/PHYSICAL-SOLAR-002-SPEC.md](../../research/PHYSICAL-SOLAR-002-SPEC.md), [results/PHYSICAL-SOLAR-002-VALIDATION.json](../../results/PHYSICAL-SOLAR-002-VALIDATION.json), [results/physical-solar-002/README.md](../../results/physical-solar-002/README.md).

## LOG-F67DC5B966

**WORLD-CLOCK-003 — item 3 partial historical ring registration and phase identifiability**

start: 2026-10-24T00:29:46.751515Z; end: 2026-10-24T00:29:46.860170Z

Type: analytical constraints; source research. Outcome: 240 conditional registrations remain; no cross-segment join, 1989 inventory or cipher bridge identified

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Original analysis start/end UTC: 2026-10-24T00:29:46.751515+00:00 / 2026-10-24T00:29:46.860170+00:00. Historical exposure clock times remain unknown.
- Kind: conditional historical mapping/invariance analysis; no K4 cipher evaluation.
- Frozen protocol commit `53aa67b86da286d45012d957a25b4763c77ab04f`; [specification](../../research/WORLD-CLOCK-003-SPEC.md), [findings](../../research/WORLD-CLOCK-003-FINDINGS.md), [source](../../experiments/world_clock_003.py), [complete original results/receipts](../../results/world-clock-003/README.md).
- Selected fixed input: 41 labels/ten panels/three dated runs. Under explicitly unverified common-inventory continuity, 576 gauge-fixed offset pairs yield 240 compatible registrations and 336 exact rank conflicts. Retain all compatible layouts. No global compass registration or 1989 completeness inferred.
- 272 within-segment pair differences forced; all 548 cross-segment pairs remain ambiguous. Pair equations are dependent, not independent clues. All 24 integer phases over 240 layouts give 236,160 inverse checks; continuous physical phase is not enumerated. Separate photos have separate exposure phases. No semantic UTC offset or per-character city mapping assigned.
- Controls: 36 complete tiny-ring sets match independent direct unification; all 36 plants included; 117 rational phase/gauge cases and mutation checks pass. Old pilot exactly replayed in a temporary directory without overwriting original data/results.
- Separate prior evidence: corrected 1972 inscriptions and narrow 1989 labels are retained without an unsupported join. Broader clock/face hypotheses remain evidence-blocked for an actual cipher bridge and historical calibration. Fresh parent research is integrated separately: two dated arrangement discrepancies, five full May 1989 lower labels, explicitly post-1989 comparison and an undated removed plate. Original three-run input/results remain unchanged; no item 4 or Site change.
- Local engineering validation: 504 tests pass on Python 3.9 and 3.12; [separate validation receipt/logs](../../results/WORLD-CLOCK-003-VALIDATION.json). That checkpoint preceded the final separately recorded source integration.
- Final evidence: [supplied report/inventory](../../independent/2026-10-24/world-clock-item3/README.md), [independent local source checks](../../sources/world-clock-003/LOCAL-SOURCE-REVIEW.json), [post-outcome analytical revision amendment](../../research/WORLD-CLOCK-003-SOURCE-AMENDMENT.md). Known dates are day/month/year precision as documented; unknown worker execution times remain unknown.
- Final source-integrated validation: 508 tests pass on both supported Python versions; [separate final receipt/logs](../../results/WORLD-CLOCK-003-FINAL-VALIDATION.json). Unknown historical exposure times remain unknown.

Related files: [experiments/world_clock_003.py](../../experiments/world_clock_003.py), [independent/2026-10-24/world-clock-item3/README.md](../../independent/2026-10-24/world-clock-item3/README.md), [research/WORLD-CLOCK-003-FINDINGS.md](../../research/WORLD-CLOCK-003-FINDINGS.md), [research/WORLD-CLOCK-003-SOURCE-AMENDMENT.md](../../research/WORLD-CLOCK-003-SOURCE-AMENDMENT.md), [research/WORLD-CLOCK-003-SPEC.md](../../research/WORLD-CLOCK-003-SPEC.md), [results/WORLD-CLOCK-003-FINAL-VALIDATION.json](../../results/WORLD-CLOCK-003-FINAL-VALIDATION.json), [results/WORLD-CLOCK-003-VALIDATION.json](../../results/WORLD-CLOCK-003-VALIDATION.json), [results/world-clock-003/README.md](../../results/world-clock-003/README.md), [sources/world-clock-003/LOCAL-SOURCE-REVIEW.json](../../sources/world-clock-003/LOCAL-SOURCE-REVIEW.json).

## LOG-8675DFA0B4

**CSP889-COUPLED-024 — item 4 unknown-anchor collector inference and exact byte masks**

start: 2026-10-24T01:13:48.757054Z; end: 2026-10-24T01:14:48.962374Z; start: 2026-10-24T01:14:49.024549Z; end: 2026-10-24T01:15:49.025955Z; start: 2026-10-24T01:15:49.100953Z; end: 2026-10-24T01:16:54.110198Z; start: 2026-10-24T01:16:54.111186Z; end: 2026-10-24T01:17:59.124506Z; start: 2026-10-24T01:13:47.200029Z; end: 2026-10-24T01:17:59.125781Z; start: 2026-10-24T01:25:56.464183Z; end: 2026-10-24T01:29:59.954139Z

Type: synthetic solver benchmark; analytical constraints. Outcome: Exact tiny sets pass; corrected unknown-anchor solver completes 11/11 versus 9/9 matched controllers, full domain unresolved

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Kind: synthetic exact-solver engineering, not new K4 cryptanalysis. Original and corrective run timestamps are recorded separately in linked manifests and every child receipt; no historical exposure time is inferred.
- Frozen primary protocol `950ba4c`; [specification](../../research/SIGABA-UNKNOWN-ANCHOR-COLLECTOR-SPEC.md), [method/proof](../../research/SIGABA-UNKNOWN-ANCHOR-COLLECTOR-METHOD.md), [findings](../../research/SIGABA-UNKNOWN-ANCHOR-COLLECTOR-FINDINGS.md), [coupled implementation](../../experiments/sigaba_unknown_anchor_collector.py). Twelve published simulator vectors remain controls, not hardware certification.
- Complete correctness: 70 original explicit graph comparisons/12 independent physical raw-key streams; 124 supplementary varying-input graph/controller checks/12 further raw-key streams, four genuinely varying fixtures. Byte masks match 9,743 small subset/translation cases and declared real boundary points. Prefix/gap, disconnected paths and deliberate resource controls pass.
- Original comparison [manifest](../../results/sigaba-unknown-anchor-024/20261024T011347Z-0372961a832e4fefa3630289212ad464/manifest.json), [summary](../../results/sigaba-unknown-anchor-024/20261024T011347Z-0372961a832e4fefa3630289212ad464/summary.json): fresh baseline completes 9/7 controllers, original integrated children hit the 65-second watchdog without native coverage/RSS. Preserve unknown, not zero.
- Correction [manifest](../../results/sigaba-unknown-anchor-024b/20261024T012556Z-68fabf5fec944bdb82cd9971546c2a6e/manifest.json), [summary](../../results/sigaba-unknown-anchor-024b/20261024T012556Z-68fabf5fec944bdb82cd9971546c2a6e/summary.json): exact byte-generated masks applied to BOTH backends, same fixtures/domains/caps; baseline completes 9/9, integrated 11/11 before wall limits. Each requests 11,881,376 controllers and all 66,058 reachable maps. Almost all remain unresolved.
- These first-eleven prefixes are contained in prior COMPACT-018 first-12/14 coverage; no new historical full-domain coverage or K4 inference. No real-sized gate pass, no claim of recovered plant from the full selector, and no statistical speedup/general SIGABA exclusion.
- Initial receipt bug and supplementary control assumption are preserved with [bounded diagnostic evidence](../../results/sigaba-unknown-anchor-diagnostic/README.md). No new fixture or cache/time expansion after the byte-mask comparison. The proposed canonical support-signature reuse is unrun.
- Item 5 and public Site unchanged. Publication follows the later renewed owner approval; no denied transport workaround.
- Final validation: 519 tests pass on both supported Python versions; [separate UTC validation receipt/logs](../../results/CSP889-COUPLED-024-VALIDATION.json). Original and corrected synthetic run windows remain in their manifests, not inferred from publication.

Related files: [experiments/sigaba_unknown_anchor_collector.py](../../experiments/sigaba_unknown_anchor_collector.py), [research/SIGABA-UNKNOWN-ANCHOR-COLLECTOR-FINDINGS.md](../../research/SIGABA-UNKNOWN-ANCHOR-COLLECTOR-FINDINGS.md), [research/SIGABA-UNKNOWN-ANCHOR-COLLECTOR-METHOD.md](../../research/SIGABA-UNKNOWN-ANCHOR-COLLECTOR-METHOD.md), [research/SIGABA-UNKNOWN-ANCHOR-COLLECTOR-SPEC.md](../../research/SIGABA-UNKNOWN-ANCHOR-COLLECTOR-SPEC.md), [results/CSP889-COUPLED-024-VALIDATION.json](../../results/CSP889-COUPLED-024-VALIDATION.json), [results/sigaba-unknown-anchor-024/20261024T011347Z-0372961a832e4fefa3630289212ad464/manifest.json](../../results/sigaba-unknown-anchor-024/20261024T011347Z-0372961a832e4fefa3630289212ad464/manifest.json), [results/sigaba-unknown-anchor-024/20261024T011347Z-0372961a832e4fefa3630289212ad464/summary.json](../../results/sigaba-unknown-anchor-024/20261024T011347Z-0372961a832e4fefa3630289212ad464/summary.json), [results/sigaba-unknown-anchor-024b/20261024T012556Z-68fabf5fec944bdb82cd9971546c2a6e/manifest.json](../../results/sigaba-unknown-anchor-024b/20261024T012556Z-68fabf5fec944bdb82cd9971546c2a6e/manifest.json), [results/sigaba-unknown-anchor-024b/20261024T012556Z-68fabf5fec944bdb82cd9971546c2a6e/summary.json](../../results/sigaba-unknown-anchor-024b/20261024T012556Z-68fabf5fec944bdb82cd9971546c2a6e/summary.json), [results/sigaba-unknown-anchor-diagnostic/README.md](../../results/sigaba-unknown-anchor-diagnostic/README.md).

## LOG-9A9514387C

**LAMP-GREEK-025 — item 5 ordinal lamp labels and complete Greek codecs**

artifact creation: 2026-10-24T01:53:20.771533Z; start: 2026-10-24T01:52:16.680577Z; end: 2026-10-24T01:52:27.185959Z

Type: finite K4 model tests; analytical constraints; synthetic validation. Outcome: No first-crib survivor: 46,080 finite descriptions reject; 23,040 framed descriptions support-excluded; planted ambiguity retained

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Kind: finite K4 model tests plus a support exclusion and synthetic complete-selector controls. No historical creator claim or Site change.
- Frozen specification `b19f89c` precedes actual comparison. [Protocol](../../research/LAMP-GREEK-025-SPEC.md), [findings](../../research/LAMP-GREEK-025-FINDINGS.md), [source](../../experiments/lamp_greek.py), [original run/UTC manifest](../../results/lamp-greek-025/README.md).
- Original controls start/end UTC: 2026-10-24T01:51:34.425418+00:00 / 2026-10-24T01:51:39.517632+00:00; actual selection 2026-10-24T01:51:39.584120+00:00 / 2026-10-24T01:51:39.593230+00:00. Null panel ends 2026-10-24T01:51:41.494966+00:00. These are computation timestamps, not publication or historical clock observations.
- Scope: two physical orders, ordinal lit-field sums, 1,440 starts, two indicator states, AZ/KRYPTOS and addition/true Beaufort. Letter and adjacent-pair roles each test 23,040 descriptions and fail first-crib constraints. Framed Greek role support-excludes 23,040 descriptions with zero phase simulation; no alignment assumption needed for that invariant.
- Results: no first-crib or Berlin-stage candidate; no full solution. All 199 histogram-shuffled whole-family controls also have zero first fits; descriptive baseline only, no significance claim.
- Controls: 5,760 display/order comparisons, 18,279 prefix-code string roundtrips, 702 rank inverses, 69,120 raw-model unrelated-message roundtrips, all 24 literal plants retained. One pair plant has two distinct all-crib-compatible plaintexts; preserve that ambiguity. Four framed plants have two descriptions/one plaintext.
- Separate [direct checker](../../experiments/audit_lamp_greek.py) verifies complete candidate sets for 24 plants and K4, using independent row arithmetic and direct decoding; same-author implementation, not external blinded verification. [Validation receipt](../../results/LAMP-GREEK-025-INDEPENDENT-VALIDATION.json); [finite phase/support certificates](../../results/LAMP-GREEK-025-CERTIFICATES.json).
- The Greek frame expands the plant 97→104 tokens and computes clue offsets after full parsing; ordinal Greek labels are not phonetic Greek. Other mechanisms remain outside coverage. Stop before item 6.
- Final validation: 529 tests pass in both Python 3.9 and 3.12; [validation receipt and logs](../../results/LAMP-GREEK-025-VALIDATION.json). No new documentation-link errors; no configured CI workflows.

Related files: [experiments/audit_lamp_greek.py](../../experiments/audit_lamp_greek.py), [experiments/lamp_greek.py](../../experiments/lamp_greek.py), [research/LAMP-GREEK-025-FINDINGS.md](../../research/LAMP-GREEK-025-FINDINGS.md), [research/LAMP-GREEK-025-SPEC.md](../../research/LAMP-GREEK-025-SPEC.md), [results/LAMP-GREEK-025-CERTIFICATES.json](../../results/LAMP-GREEK-025-CERTIFICATES.json), [results/LAMP-GREEK-025-INDEPENDENT-VALIDATION.json](../../results/LAMP-GREEK-025-INDEPENDENT-VALIDATION.json), [results/LAMP-GREEK-025-VALIDATION.json](../../results/LAMP-GREEK-025-VALIDATION.json), [results/lamp-greek-025/README.md](../../results/lamp-greek-025/README.md).

## LOG-8B35949B43

**TREE-GEOMETRY-IPA-026 — item 6 dynamic topology, full-state feedback and pronunciation keys**

start: 2026-10-24T02:06:45.670410Z; end: 2026-10-24T02:06:45.999181Z

Type: finite K4 model tests; synthetic validation; source qualification. Outcome: No first fit in 448 descriptions; splay/ARX finite negatives; IPA UTF-8 is explicitly a modern diagnostic

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Kind: three finite exploratory model tests, synthetic complete-selector controls and historical qualification; no creator-use evidence or Site change.
- Frozen protocol `e35121c31d34c62c8f836d9169214f79d53de8b5`; [specification](../../research/TREE-GEOMETRY-IPA-026-SPEC.md), [findings](../../research/TREE-GEOMETRY-IPA-026-FINDINGS.md), [native code](../../experiments/tree_geometry_ipa.py), [independent reference](../../experiments/tree_geometry_ipa_reference.py).
- Exact scope: 104 bottom-up access-splay tree descriptions, 208 nonlinear 35-bit geometry feedback descriptions, 136 source-fixed IPA byte-key descriptions. All 448 full decryptions are distinct; no first-crib survivor, no Berlin-stage candidate. No arbitrary states/functions or general-family exclusion.
- Original completed controls start/end UTC: 2026-10-24T02:05:03.782641+00:00 / 2026-10-24T02:05:12.193005+00:00. Actual start/end 2026-10-24T02:05:12.193900+00:00 / 2026-10-24T02:05:12.247353+00:00. Whole-family nulls end 2026-10-24T02:05:23.118605+00:00. [Original and failed-control manifests](../../results/tree-geometry-ipa-026/README.md) preserve separate chronology; no publication timestamp substitution.
- Controls: 1,792 fixed-model/reference message roundtrips, 24,336 tree permutation checks, 104 topology-change and 104 wrong-timing witnesses, 24 full-family plants with exact complete-reference candidate-set agreement and truth inclusion. All 199 histogram shuffles have zero first/all fits; descriptive only, no significance claim. Initial control attempt failed on reference rotation grouping before K4 and is preserved, not counted as a negative.
- Separate [post-outcome direct replay](../../experiments/audit_tree_geometry_ipa.py) agrees on all actual model records and 1,040 geometry carry/boundary cases; [receipt](../../results/TREE-GEOMETRY-IPA-026-INDEPENDENT-VALIDATION.json). Same-author independent implementation, not external blind verification.
- IPA output periods 18/16 exceed the older direct period 1–12 baseline, but UTF-8 was devised in 1992. This explicitly modern serialization is not a historical 1990 hypothesis or an IPA spelling inverse. Public clue phrases used as keys are not independent recovered evidence. No encoding retune, new dialect or item 7.
- Final aggregate validation: 538 tests pass on Python 3.9 and 3.12; [separate UTC receipt/logs](../../results/TREE-GEOMETRY-IPA-026-VALIDATION.json). No configured CI workflow or new documentation-link errors.

Related files: [experiments/audit_tree_geometry_ipa.py](../../experiments/audit_tree_geometry_ipa.py), [experiments/tree_geometry_ipa.py](../../experiments/tree_geometry_ipa.py), [experiments/tree_geometry_ipa_reference.py](../../experiments/tree_geometry_ipa_reference.py), [research/TREE-GEOMETRY-IPA-026-FINDINGS.md](../../research/TREE-GEOMETRY-IPA-026-FINDINGS.md), [research/TREE-GEOMETRY-IPA-026-SPEC.md](../../research/TREE-GEOMETRY-IPA-026-SPEC.md), [results/TREE-GEOMETRY-IPA-026-INDEPENDENT-VALIDATION.json](../../results/TREE-GEOMETRY-IPA-026-INDEPENDENT-VALIDATION.json), [results/TREE-GEOMETRY-IPA-026-VALIDATION.json](../../results/TREE-GEOMETRY-IPA-026-VALIDATION.json), [results/tree-geometry-ipa-026/README.md](../../results/tree-geometry-ipa-026/README.md).

## LOG-3AA105642E

**STRIP-SOURCE-GATES-027 — item 7 strip boundaries, historical QA and five source gates**

start: 2026-10-24T02:33:00.306741Z; end: 2026-10-24T02:33:00.309185Z; receipt recording: 2026-10-24T02:34:11.715030Z; start: 2026-10-24T02:21:55.067700Z; end: 2026-10-24T02:21:55.198123Z

Type: analytical constraints; historical source validation; source research. Outcome: Direct nonzero strips excluded; partial M138/Wheatstone source QA passes with defects preserved; book/sign/German and distinct variants remain gated

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Kind: source-conditioned analytical exclusion, historical worked-example validation and explicit evidence-blocked mechanisms; no strip-key sweep or universal historical-family rejection.
- Frozen conditional protocol `0e6693e`; [specification](../../research/STRIP-SOURCE-GATES-027-SPEC.md), [findings](../../research/STRIP-SOURCE-GATES-027-FINDINGS.md), [conditional code](../../experiments/strip_source_gates.py), [source QA](../../experiments/item7_historical_source_qa.py), [source-data admission](../../experiments/strip_inventory_admission.py), [row-candidate relation](../../experiments/strip_row_candidates.py).
- Original controls start/end UTC: 2026-10-24T02:16:36.497919+00:00 / 2026-10-24T02:16:36.634250+00:00. Original conditional replay and post-source QA/replay times are separately retained in [receipts](../../results/strip-source-gates-027/README.md); worker execution times are unknown. Publication time is not substituted.
- Direct nonzero valid-strip operation cannot self-encipher: first-crib S→S at 33 already rejects, with public K→K at 74 as explanatory additional evidence. SRH-366 printed 83–84 nonzero rule independently visually verified; changing strip sets/nonzero subgroup offsets does not evade it. Zero-column/outer-layer/preprocessing alternatives remain outside that proof.
- Separate zero-per-block relaxation: changed/fixed/changed at 32–34 rejects every width>=2 and registration. Finite widths 1..30/all origins have 465 bookkeeping descriptions, 464 contradictions, width 1 necessary-only pass. Prior M-94 width 25/origin 0 overlaps. No independent-search or global-novelty count.
- Controls: 872 toy permutations/29,366 symbol checks, 24 continuous synthetic plants, 11,160 independent block partitions. [Resource replay](../../results/STRIP-SOURCE-GATES-027-ARITHMETIC-REPLAY.json) reproduces original payloads, peak 15,122,432 bytes; original peak was not recorded.
- Historical QA: original 1935 M-138 observed pairs reproduce +15 example; 24 complete rows validate, strip 1 O/Q literal fails complete-inventory gate without repair. Wheatstone REFERENCE→XZAABGQAM forward/inverse reproduces; conflicting printed XZZZBGQAM and unused ? slot retained. An explicitly inferred W completion is not pixel authentication. [Source QA receipt](../../results/ITEM7-HISTORICAL-SOURCE-QA-027.json).
- [Supplied report/transcription/original script](../../independent/2026-10-24/item7-historical-sources/README.md) preserved; original arithmetic adapter substitutes only output path and declared PDF metadata, not arithmetic. [Local source review](../../results/ITEM7-LOCAL-SOURCE-REVIEW.json) distinguishes direct SRH visual inspection, NSA web text, worker pixels and failed downloads. No source 403 retry/alternate route.
- Complete authentic M-138-A issues, distinct Pletts rules, specific book extraction, Egyptian codec and German recovery/alignment remain source-gated. No invented model was run merely to fill those gaps, no Site change, stop before item 8.
- Final validation: 553 tests pass on Python 3.9 and 3.12; [UTC validation receipt/logs and preserved earlier documentation failure](../../results/STRIP-SOURCE-GATES-027-VALIDATION.json). No new broken links or configured CI workflow.

Related files: [experiments/item7_historical_source_qa.py](../../experiments/item7_historical_source_qa.py), [experiments/strip_inventory_admission.py](../../experiments/strip_inventory_admission.py), [experiments/strip_row_candidates.py](../../experiments/strip_row_candidates.py), [experiments/strip_source_gates.py](../../experiments/strip_source_gates.py), [independent/2026-10-24/item7-historical-sources/README.md](../../independent/2026-10-24/item7-historical-sources/README.md), [research/STRIP-SOURCE-GATES-027-FINDINGS.md](../../research/STRIP-SOURCE-GATES-027-FINDINGS.md), [research/STRIP-SOURCE-GATES-027-SPEC.md](../../research/STRIP-SOURCE-GATES-027-SPEC.md), [results/ITEM7-HISTORICAL-SOURCE-QA-027.json](../../results/ITEM7-HISTORICAL-SOURCE-QA-027.json), [results/ITEM7-LOCAL-SOURCE-REVIEW.json](../../results/ITEM7-LOCAL-SOURCE-REVIEW.json), [results/STRIP-SOURCE-GATES-027-ARITHMETIC-REPLAY.json](../../results/STRIP-SOURCE-GATES-027-ARITHMETIC-REPLAY.json), [results/STRIP-SOURCE-GATES-027-VALIDATION.json](../../results/STRIP-SOURCE-GATES-027-VALIDATION.json), [results/strip-source-gates-027/README.md](../../results/strip-source-gates-027/README.md).

## LOG-306DBE2114

**ONE-EDIT-028 — item 8 complete counterfactual edit robustness**

start: 2026-10-24T03:07:02.579338Z; end: 2026-10-24T03:07:02.780435Z

Type: finite K4 model tests; exact ambiguity analysis; whole-search controls; analytical constraints. Outcome: No complete periodic fit; transposition repairs massively ambiguous and match all shuffled controls; no error claim

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Kind: bounded exact cipher sensitivity, unrestricted-permutation ambiguity, necessary-certificate diagnostics and full-search controls; no assertion of K4 error or canonical change.
- [Frozen protocol](../../research/ONE-EDIT-028-SPEC.md) commit `786f864`; pre-scoring implementation/control fix `aef83ca`. [Findings](../../research/ONE-EDIT-028-FINDINGS.md), [eight-item summary](../../research/EIGHT-ITEM-INVESTIGATION-SUMMARY.md), [channel](../../experiments/one_edit_channel.py), [exact models](../../experiments/one_edit_models.py), [independent reference](../../experiments/one_edit_reference.py), [all original results](../../results/one-edit-028/README.md).
- Original UTC controls: 2026-10-24T03:00:31.710149+00:00 / 2026-10-24T03:00:50.610903+00:00; actual 2026-10-24T03:00:50.611166+00:00 / 2026-10-24T03:00:51.315755+00:00; nulls end 2026-10-24T03:01:06.353305+00:00. Post-audit/regression timestamps are separate, not publication times.
- Exact channel count: 5,071 raw descriptions (1 baseline, 2,425 substitutions, 2,548 missing-letter insertions, 97 extra-letter deletions), 4,968 latent strings, 6,317 complete (latent,mask) instances. Two explicit coordinate interpretations; 596 transport cases inadmissible without dropping any known letter. All 9,546 admitted raw alignment cases evaluated.
- Periodic scope: 48 same-coordinate AZ/KRYPTOS plus/true-Beaufort structures, unrestricted periods 1–12; 458,208 logical checks (303,216 unique instance checks), 41 raw first fits/29 unique records, zero complete fits. Every phase is fitted by the first 13 letters; no refit at Berlin. First-fit period 12 is guaranteed by at most one substitution, not a lead.
- Unrestricted permutations: 191 primary raw edits and 169 conditional transport cases fit the letter counts. Two arbitrary non-language witnesses/keys per compatible instance regenerate latent text and every aliased channel to canonical 97. Independent post-audit deduplicates 27 compact plaintext sets (25 primary), checks 351 pairs disjoint and counts the exact huge union. No historical route/error/English solution claim; original bounds unchanged.
- Diagnostics: nonzero-strip fixed-point contradiction survives all admitted cases. Wheatstone's necessary pair certificate is lost in 925 primary/51 transport cases; these are not fixed-ring keys or cipher fits. Other prior families were not silently included.
- Controls: all 5,071 tagged maps, 30 complete tiny edit sets, 24 tiny permutation and 96 tiny periodic truth sets, 144 independent fixed-model table checks, K1/K2 and 7 original offline convention controls. All 24 full-selector plants retain truth, 137,600 compatible representations and 1–3,827 plaintexts per plant preserved. No unique-recovery claim.
- Whole-search nulls: all 99 histogram shuffles have permutation repairs and periodic first fits; none has a full periodic fit. No partial-score promotion or positive significance claim. Lossless gzip avoids a preflight format cap without truncation; a pre-scoring summary-writer failure is preserved as incomplete, not a negative.
- [Independent actual solver/union/certificate audit](../../results/ONE-EDIT-028-INDEPENDENT-AUDIT.json), [preflight](../../results/one-edit-028-preflight/README.md). Canonical data unchanged; no Site change, no ninth investigation.

- Final item 8 aggregate validation: 568 tests pass on Python 3.9 and 3.12; [UTC receipt and complete logs](../../results/ONE-EDIT-028-VALIDATION.json). All eight investigations are complete at their declared scope; [overview](../../research/EIGHT-ITEM-INVESTIGATION-SUMMARY.md). No ninth investigation or Site change.

Related files: [experiments/one_edit_channel.py](../../experiments/one_edit_channel.py), [experiments/one_edit_models.py](../../experiments/one_edit_models.py), [experiments/one_edit_reference.py](../../experiments/one_edit_reference.py), [research/EIGHT-ITEM-INVESTIGATION-SUMMARY.md](../../research/EIGHT-ITEM-INVESTIGATION-SUMMARY.md), [research/ONE-EDIT-028-FINDINGS.md](../../research/ONE-EDIT-028-FINDINGS.md), [research/ONE-EDIT-028-SPEC.md](../../research/ONE-EDIT-028-SPEC.md), [results/ONE-EDIT-028-INDEPENDENT-AUDIT.json](../../results/ONE-EDIT-028-INDEPENDENT-AUDIT.json), [results/ONE-EDIT-028-VALIDATION.json](../../results/ONE-EDIT-028-VALIDATION.json), [results/one-edit-028-preflight/README.md](../../results/one-edit-028-preflight/README.md), [results/one-edit-028/README.md](../../results/one-edit-028/README.md).

## LOG-75BA990166

**PROJECTION-CONCURRENCE-029 — synthetic image-ray validation and physical-data gate**

start: 2026-10-24T11:57:53.707507Z; end: 2026-10-24T11:57:53.901610Z; receipt recording: 2026-10-24T11:59:24.450218Z; start: 2026-10-24T11:50:23.445087Z; end: 2026-10-24T11:50:23.802297Z; receipt recording: 2026-10-24T12:02:53.891823Z; date-only record: 2026-10-24 (date statement; not a run timestamp); original date statement: 24 October 2026 UTC; separately authorized after the eight-item sequence, not a cipher search.

Type: synthetic geometric validation; evidence-gated physical diagnostic. Outcome: Synthetic line/uncertainty controls pass; zero certified monument pairs, real-data fit evidence-blocked

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Date: 24 October 2026 UTC; separately authorized after the eight-item sequence, not a cipher search.
- Kind: synthetic geometric diagnostic, independent scalar checks and real-data admission protocol; zero certified monument pairs, real fits or K4 trials.
- [Preregistered protocol](../../research/PROJECTION-CONCURRENCE-029-SPEC.md), [findings](../../research/PROJECTION-CONCURRENCE-029-FINDINGS.md), [API/data contract](../../research/PROJECTION-CONCURRENCE-029-API.md), [native code](../../experiments/projection_concurrence.py), [independent checks](../../experiments/projection_concurrence_reference.py), [tests](../../tests/test_projection_concurrence.py).
- Original corrected diagnostic UTC start/end:2026-10-24T11:50:23.445087+00:00 /2026-10-24T11:50:23.802297+00:00. [Complete fixtures/outputs](../../results/PROJECTION-CONCURRENCE-029-SYNTHETIC.json): 24 uncertainty configurations, 21 evaluated and3 collapsed; finite/infinity/noisy positives pass, heldout/mixed-source negatives fail, coincident rays unidentifiable despite zero residual.
- Initial parallel/infinity QA misconception and undefined-training-ray gate error are preserved separately, corrected before any real fitting; no discarded points or threshold easing.
- Actual physical-data stage remains evidence-blocked. Line concurrence predicts only line incidence, not complete spot position or solar/time identity. [Source acquisition review](../../research/evidence/2026-10-24-projection-acquisition/PHOTO-ACQUISITION-REVIEW.md) and [local LOC check](../../research/evidence/2026-10-24-projection-acquisition/LOCAL-REVIEW.json) integrated: additional views/observation ROIs, still zero certified pairs; no synthetic success promoted to monument evidence.

- [Separately frozen local-control supplement](../../research/PROJECTION-CONCURRENCE-029-LOCAL-CONTROLS-SPEC.md) and [eleven complete outputs](../../results/PROJECTION-CONCURRENCE-029-LOCAL-CONTROLS.json): small wrong picks and a correlated receiver shift can pass. This exposes conditional-gate limits; no tolerance retuning or real-data fit.

- Final regression:587 tests pass on Python3.9 and3.12; [separate UTC receipt/full logs](../../results/PROJECTION-CONCURRENCE-029-VALIDATION.json). [Complete Python3.12 record replay](../../results/PROJECTION-CONCURRENCE-029-PY312-REPLAY.json) agrees within declared1e-8 absolute/1e-9 relative tolerance. Real-data stage is evidence-blocked, not a monument negative.

Related files: [experiments/projection_concurrence.py](../../experiments/projection_concurrence.py), [experiments/projection_concurrence_reference.py](../../experiments/projection_concurrence_reference.py), [research/PROJECTION-CONCURRENCE-029-API.md](../../research/PROJECTION-CONCURRENCE-029-API.md), [research/PROJECTION-CONCURRENCE-029-FINDINGS.md](../../research/PROJECTION-CONCURRENCE-029-FINDINGS.md), [research/PROJECTION-CONCURRENCE-029-LOCAL-CONTROLS-SPEC.md](../../research/PROJECTION-CONCURRENCE-029-LOCAL-CONTROLS-SPEC.md), [research/PROJECTION-CONCURRENCE-029-SPEC.md](../../research/PROJECTION-CONCURRENCE-029-SPEC.md), [research/evidence/2026-10-24-projection-acquisition/LOCAL-REVIEW.json](../../research/evidence/2026-10-24-projection-acquisition/LOCAL-REVIEW.json), [research/evidence/2026-10-24-projection-acquisition/PHOTO-ACQUISITION-REVIEW.md](../../research/evidence/2026-10-24-projection-acquisition/PHOTO-ACQUISITION-REVIEW.md), [results/PROJECTION-CONCURRENCE-029-LOCAL-CONTROLS.json](../../results/PROJECTION-CONCURRENCE-029-LOCAL-CONTROLS.json), [results/PROJECTION-CONCURRENCE-029-PY312-REPLAY.json](../../results/PROJECTION-CONCURRENCE-029-PY312-REPLAY.json), [results/PROJECTION-CONCURRENCE-029-SYNTHETIC.json](../../results/PROJECTION-CONCURRENCE-029-SYNTHETIC.json), [results/PROJECTION-CONCURRENCE-029-VALIDATION.json](../../results/PROJECTION-CONCURRENCE-029-VALIDATION.json), [tests/test_projection_concurrence.py](../../tests/test_projection_concurrence.py).

## LOG-3F1B540764

**SITE-PROJECTION-030 — version16 source archive and publication provenance**

receipt recording: 2026-10-24T12:21:21.929364Z; receipt recording: 2026-10-24T12:13:37.323660Z

Type: source archive integrity; publication provenance. Outcome: Version16 owner-confirmed live; exact source/fixture integrity passes locally; rendered QA unverified and no real-photo fit

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Date:24 October2026 UTC; source archival/integrity work only, not a new cipher or optical fit.
- [Archive/provenance](../site-source/projection-20261024/README.md), [original manifest](../site-source/projection-20261024/snapshot/HANDOFF_MANIFEST.json), [static verifier](../../experiments/verify_projection_site_handoff.py), [local UTC receipt](../../results/SITE-PROJECTION-20261024-SOURCE-HANDOFF.json).
- Native owner publication relayed by parent confirms public Site version16/source543634f866b74a778b7f1b4de58a4815237dcb2f, public access revision2 unchanged. Exact publication time unknown. Owner reports105 tests; rendered desktop/mobile QA unverified because Mac locked. Local archive step did not deploy or execute the handed-off JavaScript.
- All33 original ZIP entries safely inspected;31 source files match owner Git blobs and patch;8 fixtures and complete11-local-control payloads match research bytes. This is a partial source delta, not a complete runtime or independently rerun full Site suite.
- Original copied contract has8 repository-relative links in its two source copies; preserve exact bytes with explicit original-source link exceptions and working canonical links in the archive guide. No silent source repair. Zero real-photo fits or new K4 trials.

- Local aggregate archive regression:592 tests on Python3.9/3.12, [UTC receipt/logs](../../results/SITE-PROJECTION-030-VALIDATION.json). Parent cloud review confirms version16 fixtures/controls/photo/export, with narrow QA-page encoding correction still pending source handoff; no corrected version is claimed archived.

Related files: [docs/site-source/projection-20261024/README.md](../site-source/projection-20261024/README.md), [docs/site-source/projection-20261024/snapshot/HANDOFF_MANIFEST.json](../site-source/projection-20261024/snapshot/HANDOFF_MANIFEST.json), [experiments/verify_projection_site_handoff.py](../../experiments/verify_projection_site_handoff.py), [results/SITE-PROJECTION-030-VALIDATION.json](../../results/SITE-PROJECTION-030-VALIDATION.json), [results/SITE-PROJECTION-20261024-SOURCE-HANDOFF.json](../../results/SITE-PROJECTION-20261024-SOURCE-HANDOFF.json).

## LOG-04D93D0E34

**SITE-PROJECTION-031 — corrected version 17 source archive**

receipt recording: 2026-10-24T12:23:26.128087Z; receipt recording: 2026-10-24T12:27:17.009807Z; date-only record: 2026-10-24 (date statement; not a run timestamp); original date statement: 24 October 2026 UTC. Source archive integrity and publication provenance only; no new cipher or physical fit.

Type: source archive integrity; publication provenance. Outcome: Corrected version 17 owner-confirmed live; source integrity and parent cloud Chrome recheck pass; no real-photo fit

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Date: 24 October 2026 UTC. Source archive integrity and publication provenance only; no new cipher or physical fit.
- [Current source guide](../site-source/projection-v17-20261024/README.md), [original seven-file manifest](../site-source/projection-v17-20261024/snapshot/HANDOFF_MANIFEST.json), [static verifier](../../experiments/verify_projection_v17_handoff.py), [UTC handoff receipt](../../results/SITE-PROJECTION-V17-SOURCE-HANDOFF.json).
- Parent-relayed native owner publication confirms version 17 live, source `2cb85a7714e12a627495f42dd3a7581c09b0b809`, public access revision 2 unchanged. Owner reports 107 tests; this full Site suite was not rerun here. Exact publication time unknown.
- Seven-file delta and 31-file full-feature ZIP match manifest hashes and source Git blobs. Full feature equals immutable version 16 source plus delta. Encoding/visible residual wording corrected; numerical core, fixtures, photo and export code unchanged.
- Parent cloud Chrome rendered QA passed targeted v17 fixes after earlier full eight-case/control/photo/export/390-and-768-iframe/fold checks. Not physical-device emulation or local Mac QA. No handed-off JavaScript executed or Site redeployed by archive integration.

- Final local aggregate regression: 595 tests pass on Python 3.9 and 3.12; [UTC receipt and full logs](../../results/SITE-PROJECTION-V17-VALIDATION.json). Version 16 archive is unchanged; corrected version 17 is separately archived.

Related files: [docs/site-source/projection-v17-20261024/README.md](../site-source/projection-v17-20261024/README.md), [docs/site-source/projection-v17-20261024/snapshot/HANDOFF_MANIFEST.json](../site-source/projection-v17-20261024/snapshot/HANDOFF_MANIFEST.json), [experiments/verify_projection_v17_handoff.py](../../experiments/verify_projection_v17_handoff.py), [results/SITE-PROJECTION-V17-SOURCE-HANDOFF.json](../../results/SITE-PROJECTION-V17-SOURCE-HANDOFF.json), [results/SITE-PROJECTION-V17-VALIDATION.json](../../results/SITE-PROJECTION-V17-VALIDATION.json).

## LOG-3ED35BF8BC

**SPELLING-CORRECTION-032 — deliberate spelling source-rule constraints**

start: 2026-10-24T13:18:35.633896Z; end: 2026-10-24T13:18:35.659389Z; start: 2026-10-24T13:27:34.863824Z; end: 2026-10-24T13:27:34.889269Z; receipt recording: 2026-10-24T13:27:34.928551Z; date-only record: 2026-10-24 (date statement; not a run timestamp); original date statement: 24 October 2026 UTC. Local source-consistency/identifiability study; zero K4 trials, no push or Site edit.

Type: source consistency constraints; exact edit and ambiguity analysis; synthetic reversible controls. Outcome: No supported uniform source rule; general trigger/key role evidence-blocked; zero K4 trials and local only

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Date: 24 October 2026 UTC. Local source-consistency/identifiability study; zero K4 trials, no push or Site edit.
- [Frozen protocol](../../research/SPELLING-CORRECTION-032-SPEC.md), [findings](../../research/SPELLING-CORRECTION-032-FINDINGS.md), [source/prior coverage](../../research/SPELLING-CORRECTION-032-SOURCES.md), [native code](../../experiments/spelling_correction.py), [independent oracles](../../experiments/spelling_correction_reference.py).
- Original run UTC start/end: 2026-10-24T13:18:35.633896+00:00 / 2026-10-24T13:18:35.659389+00:00; [full output and controls](../../results/SPELLING-CORRECTION-032-ORIGINAL.json). Source retrieval/attribution and later regression times are separate.
- All minimal word alignments retain Q→L, U→O and uncertain K3 A→E plus inserted E. Uniform full-source letter functions fail; 624 invertible affine changed-site maps fail; keyboard/copy/permutation/vowel constraints fail. These are overlapping exact constraints, not independent statistical trials.
- All 42 repeated-mask phase descriptions fail on both complete primary texts (84 source applications). They are direct source-transformation diagnostics, not K4 keys or tests of every correction-derived outer cipher. No new trigger or key sweep follows.
- Independent controls: 394 tiny alignment sets, 436 function-count systems, 24 planted substitutions, 624 affine and 126 mask roundtrips; all pass. General contextual correction family remains evidence-blocked, not universally excluded.

- Final local validation: 608 tests pass on Python 3.9/3.12; [UTC receipt and full logs](../../results/SPELLING-CORRECTION-032-VALIDATION.json), [complete cross-version replay](../../results/SPELLING-CORRECTION-032-PY312-REPLAY.json). No new K4 trial or publication.

Related files: [experiments/spelling_correction.py](../../experiments/spelling_correction.py), [experiments/spelling_correction_reference.py](../../experiments/spelling_correction_reference.py), [research/SPELLING-CORRECTION-032-FINDINGS.md](../../research/SPELLING-CORRECTION-032-FINDINGS.md), [research/SPELLING-CORRECTION-032-SOURCES.md](../../research/SPELLING-CORRECTION-032-SOURCES.md), [research/SPELLING-CORRECTION-032-SPEC.md](../../research/SPELLING-CORRECTION-032-SPEC.md), [results/SPELLING-CORRECTION-032-ORIGINAL.json](../../results/SPELLING-CORRECTION-032-ORIGINAL.json), [results/SPELLING-CORRECTION-032-PY312-REPLAY.json](../../results/SPELLING-CORRECTION-032-PY312-REPLAY.json), [results/SPELLING-CORRECTION-032-VALIDATION.json](../../results/SPELLING-CORRECTION-032-VALIDATION.json).

## LOG-40A846EF5A

**COVER-EXTRACTION-033 — post-decryption word-cover and fixed-letter constraints**

start: 2026-10-24T13:55:39.526279Z; end: 2026-10-24T13:55:39.790810Z; start: 2026-10-24T14:12:04.924656Z; end: 2026-10-24T14:12:05.127524Z; date-only record: 2026-10-24 (date statement; not a run timestamp); original date statement: 24 October 2026 UTC. Local only, no push or Site change.

Type: exact conditional cover constraints; synthetic reversible controls. Outcome: Strict NATO fails this full-cover vocabulary; custom covers are numerous and non-identifiable; zero K4 trials

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Date: 24 October 2026 UTC. Local only, no push or Site change.
- [Frozen protocol](../../research/COVER-EXTRACTION-033-SPEC.md), [findings](../../research/COVER-EXTRACTION-033-FINDINGS.md), [sources](../../research/COVER-033-034-SOURCES.md), [native solver](../../experiments/cover_extraction.py), [independent oracle](../../experiments/cover_extraction_reference.py), [complete original receipt](../../results/COVER-EXTRACTION-033-ORIGINAL.json).
- Original UTC start/end: 2026-10-24T13:55:39.526279+00:00 / 2026-10-24T13:55:39.790810+00:00. Strict NATO full unanchored lattice has zero covers. Four explicit custom dictionaries have huge exact cover counts; A30-ENE exact15 has 3,787,080 covers and necessary pattern ???ENE????BC???. No unknown text was decrypted.
- Four fixed letter positions and global N1/N2 schedules, both N2 phases; all feasible coverword counts and exact15 strata, 84 nonempty lanes. Selected short words fail, no counter reset or arbitrary per-word index. ENE versus EN is separate.
- Independent complete tiny languages, 252 real-sized fixed-message count checks and 21 synthetic Caesar roundtrip/recovery plants pass. Outer cipher/codebook supplied in controls; zero actual K4 cipher/key trials. [Cross-version replay](../../results/COVER-EXTRACTION-PHRASE-PY312-REPLAY.json).

Related files: [experiments/cover_extraction.py](../../experiments/cover_extraction.py), [experiments/cover_extraction_reference.py](../../experiments/cover_extraction_reference.py), [research/COVER-033-034-SOURCES.md](../../research/COVER-033-034-SOURCES.md), [research/COVER-EXTRACTION-033-FINDINGS.md](../../research/COVER-EXTRACTION-033-FINDINGS.md), [research/COVER-EXTRACTION-033-SPEC.md](../../research/COVER-EXTRACTION-033-SPEC.md), [results/COVER-EXTRACTION-033-ORIGINAL.json](../../results/COVER-EXTRACTION-033-ORIGINAL.json), [results/COVER-EXTRACTION-PHRASE-PY312-REPLAY.json](../../results/COVER-EXTRACTION-PHRASE-PY312-REPLAY.json).

## LOG-80D6868D4C

**COVER-PHRASE-034 — bounded Brown short-phrase feasibility and capacity controls**

receipt recording: 2026-10-24T14:25:43.810244Z; start: 2026-10-24T14:05:51.422791Z; end: 2026-10-24T14:05:58.083425Z; start: 2026-10-24T14:07:44.116650Z; end: 2026-10-24T14:07:50.283484Z; start: 2026-10-24T14:01:20.542852Z; end: 2026-10-24T14:01:29.259691Z; date-only record: 2026-10-24 (date statement; not a run timestamp); original date statement: 24 October 2026 UTC. Local only, no push or Site change.

Type: finite corpus feasibility query; synthetic pipeline controls; whole-family capacity controls. Outcome: All-word initials: zero Brown matches; generalized selectors: ambiguous covers, not decryptions; outer cipher absent

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Date: 24 October 2026 UTC. Local only, no push or Site change.
- [Frozen protocol](../../research/COVER-PHRASE-034-SPEC.md), [findings](../../research/COVER-PHRASE-034-FINDINGS.md), [source pins](../../results/COVER-033-034-SOURCES.json), [runner](../../experiments/run_cover_phrase.py), [original summary](../../results/COVER-PHRASE-034-original-summary.json), [all matched references/counts](../../results/COVER-PHRASE-034-original-windows.jsonl.gz), [all controls](../../results/COVER-PHRASE-034-original-controls.json.gz).
- Original UTC start/end: 2026-10-24T14:01:20.542852+00:00 / 2026-10-24T14:01:29.259691+00:00. All 500 frozen Brown texts, 2,673,853 contiguous 2..5-word windows, 1,771,338 eligible occurrences and 1,335,926 distinct joined strings processed. No arbitrary word-product generation.
- All-word initials have zero matches. Exact15/all-word readout has zero for all k; every-other-word cases may produce 7/8-letter output. General family has 6,358 matched occurrence references, 3,139 joined strings / 3,147 spaced strings, mostly N2. These are compatibility counts, not recovered messages or keys.
- Six deterministic eligible synthetic plants re-encrypt full97 letters; no missing exact15 ENE plant invented. Whole-family 31 capacity draws: 24 dictionary-splittable, zero contiguous-bank matches. Not an observed K4 significance test. [Independent positive-count audit](../../results/COVER-PHRASE-034-INDEPENDENT-AUDIT.json) verifies 7,266 message/lane counts; complete tiny negative controls and exact Python3.12 replay retained. No claim of a second exhaustive corpus false-negative implementation.

- Final aggregate local validation for COVER-033/034: 625 tests pass on Python3.9/3.12; [separate UTC receipt/full logs](../../results/COVER-033-034-VALIDATION.json). Canonical ciphertext unchanged, no push or Site change.

Related files: [experiments/run_cover_phrase.py](../../experiments/run_cover_phrase.py), [research/COVER-PHRASE-034-FINDINGS.md](../../research/COVER-PHRASE-034-FINDINGS.md), [research/COVER-PHRASE-034-SPEC.md](../../research/COVER-PHRASE-034-SPEC.md), [results/COVER-033-034-SOURCES.json](../../results/COVER-033-034-SOURCES.json), [results/COVER-033-034-VALIDATION.json](../../results/COVER-033-034-VALIDATION.json), [results/COVER-PHRASE-034-INDEPENDENT-AUDIT.json](../../results/COVER-PHRASE-034-INDEPENDENT-AUDIT.json), [results/COVER-PHRASE-034-original-controls.json.gz](../../results/COVER-PHRASE-034-original-controls.json.gz), [results/COVER-PHRASE-034-original-summary.json](../../results/COVER-PHRASE-034-original-summary.json), [results/COVER-PHRASE-034-original-windows.jsonl.gz](../../results/COVER-PHRASE-034-original-windows.jsonl.gz).

## LOG-781FB4F543

**PROSE-COVER-035 — length-free ordinary lexicons and complete minimum-free autokey domain**

start: 2026-10-24T14:43:46.938037Z; end: 2026-10-24T14:43:49.043601Z; start: 2026-10-24T14:41:14.223979Z; end: 2026-10-24T14:41:22.639303Z; receipt recording: 2026-10-24T14:44:24.712644Z; start: 2026-10-24T14:42:58.055974Z; end: 2026-10-24T14:43:04.642202Z; receipt recording: 2026-10-24T14:49:08.570498Z; receipt recording: 2026-10-24T14:46:18.252838Z

Type: exact lexical constraint analysis; bounded actual K4 cipher search; synthetic recovery and matched null controls; source calibration. Outcome: Minimum-free lag27 domain:zero lexical survivors; ordinary-cover length remains undetermined and vocabulary misses genuine K3; general extraction non-identifiable

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Date:24 October2026 UTC. New local-only test, prior033/034 preserved.
- [Frozen protocol](../../research/PROSE-COVER-035-SPEC.md), [findings](../../research/PROSE-COVER-035-FINDINGS.md), [native solver](../../experiments/prose_cover.py), [runner](../../experiments/run_prose_cover.py), [independent implementation](../../experiments/audit_prose_cover.py), [original full receipt](../../results/PROSE-COVER-035-ORIGINAL.json).
- Original UTC start/end:2026-10-24T14:41:14.223979+00:00 /2026-10-24T14:41:22.639303+00:00. Three fixed Brown-derived lexicons, no forced crib boundaries or15-word limit,36 selector distributions, cover paths span7–79 words. Counts are segmentation descriptions, not typical prose or unique messages.
- Complete lag27 plaintext-autokey minimum-free domain: six AZ/KRYPTOS/equation structures ×26^3 =105,456 descriptions; zero complete lexical covers, hence no actual candidate enters second-stage extraction. Vocabulary-conditioned negative; not an extraction or broad autokey exclusion.
- Six97-letter source plants retained, lexical solutions1/4/1/1/12/3;31 identical-search conditional shuffles each105,456 settings, all zero. Full97-letter re-encryption and exact ambiguity retained. K1–K3 calibration demonstrates false-negative/infinite-language limits: even augmented lexicon rejects genuine K3, so no broad English exclusion.
- [Complete independent actual-domain sets/negative replay](../../results/PROSE-COVER-035-INDEPENDENT-AUDIT.json), [full Python3.12 semantic equality](../../results/PROSE-COVER-035-PY312-COMPARISON.json), [interrupted verification note](../../results/PROSE-COVER-035-VERIFICATION-NOTES.json). No corpus phrase selection, arbitrary97-letter key, publication or Site change.

- Final local validation: 638 tests pass on Python3.9/3.12; [UTC receipt/full logs](../../results/PROSE-COVER-035-VALIDATION.json). Earlier033/034 reports/receipts unchanged, no publication or Site change.

Related files: [experiments/audit_prose_cover.py](../../experiments/audit_prose_cover.py), [experiments/prose_cover.py](../../experiments/prose_cover.py), [experiments/run_prose_cover.py](../../experiments/run_prose_cover.py), [research/PROSE-COVER-035-FINDINGS.md](../../research/PROSE-COVER-035-FINDINGS.md), [research/PROSE-COVER-035-SPEC.md](../../research/PROSE-COVER-035-SPEC.md), [results/PROSE-COVER-035-INDEPENDENT-AUDIT.json](../../results/PROSE-COVER-035-INDEPENDENT-AUDIT.json), [results/PROSE-COVER-035-ORIGINAL.json](../../results/PROSE-COVER-035-ORIGINAL.json), [results/PROSE-COVER-035-PY312-COMPARISON.json](../../results/PROSE-COVER-035-PY312-COMPARISON.json), [results/PROSE-COVER-035-VALIDATION.json](../../results/PROSE-COVER-035-VALIDATION.json), [results/PROSE-COVER-035-VERIFICATION-NOTES.json](../../results/PROSE-COVER-035-VERIFICATION-NOTES.json).

## LOG-B430CF3900

**CURVED-SAMPLER-036 — ideal mirror feasibility, sensitivity and source gate**

start: 2026-10-24T15:09:00.471068Z; end: 2026-10-24T15:09:03.640519Z; receipt recording: 2026-10-24T15:12:47.681005Z; start: 2026-10-24T15:02:30.809205Z; end: 2026-10-24T15:02:31.272280Z; receipt recording: 2026-10-24T15:09:49.280627Z; start: 2026-10-24T15:02:42.758132Z; end: 2026-10-24T15:02:55.969582Z; receipt recording: 2026-10-24T15:18:18.850433Z; date-only record: 2026-10-24 (date statement; not a run timestamp); original date statement: 24 October 2026 UTC; synthetic horizontal-table sampler only, no actual K4 fit or publication.

Type: synthetic optical feasibility; finite sensitivity benchmark; synthetic cipher recovery controls; source and physical-data gate. Outcome: 54nominal keys;4tested utility poses unstable;50other nominal robustness unresolved; no actual K4 evaluation or physical replica

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Date: 24 October 2026 UTC; synthetic horizontal-table sampler only, no actual K4 fit or publication.
- [Frozen protocol](../../research/CURVED-SAMPLER-036-SPEC.md), [findings](../../research/CURVED-SAMPLER-036-FINDINGS.md), [API](../../research/CURVED-SAMPLER-036-API.md), [full summary](../../results/CURVED-SAMPLER-036-SUMMARY.json), [lossless original](../../results/CURVED-SAMPLER-036-ORIGINAL.json.gz), [all poses](../../results/CURVED-SAMPLER-036-poses.jsonl.gz).
- Original UTC start/end: 2026-10-24T15:02:42.758132+00:00 / 2026-10-24T15:02:55.969582+00:00. 560 optical settings, 419 complete/141 invalid footprints, 45,252 table poses, 54 nominal 97-cell keys. Four utility cases (82–83 cells/all 26 letters) fail assembly/pupil benchmark; 50 lower-density complete cases not stability-tested. No continuous-domain exclusion.
- [Independent 54,320-ray validation](../../results/CURVED-SAMPLER-036-RAY-VALIDATION.json), [independent 4,389,444-cell audit](../../results/CURVED-SAMPLER-036-INDEPENDENT-CELL-AUDIT.json), [full Python3.12 comparison](../../results/CURVED-SAMPLER-036-PY312-COMPARISON.json): discrete exact, floats within 1e-9 absolute.
- Supplied four-key panel:all 4 plants recovered,13 known letters leave 2 classes and 11 held-out retain 1; 31 synthetic whole-family nulls maximum 5/24, zero full matches. Not continuous geometry recovery or real K4 significance.
- [Site fixtures](../../results/CURVED-SAMPLER-036-SITE-FIXTURES.json) and [read-only Site contract comparison](../../results/CURVED-SAMPLER-036-SITE-CONTRACT-COMPARISON.json). Site vertical tableau is different from research horizontal table; no Site test/deployment/source archive performed here. Physical replica, glyph/reflectance/pupil realism and independent K4 geometry rationale remain unresolved.

- Final local aggregate validation: 651 tests pass on Python3.9/3.12; [UTC receipt/full logs](../../results/CURVED-SAMPLER-036-VALIDATION.json). No actual K4 fit, repository publication, Site edit or owner-source archive by this task.

Related files: [research/CURVED-SAMPLER-036-API.md](../../research/CURVED-SAMPLER-036-API.md), [research/CURVED-SAMPLER-036-FINDINGS.md](../../research/CURVED-SAMPLER-036-FINDINGS.md), [research/CURVED-SAMPLER-036-SPEC.md](../../research/CURVED-SAMPLER-036-SPEC.md), [results/CURVED-SAMPLER-036-INDEPENDENT-CELL-AUDIT.json](../../results/CURVED-SAMPLER-036-INDEPENDENT-CELL-AUDIT.json), [results/CURVED-SAMPLER-036-ORIGINAL.json.gz](../../results/CURVED-SAMPLER-036-ORIGINAL.json.gz), [results/CURVED-SAMPLER-036-PY312-COMPARISON.json](../../results/CURVED-SAMPLER-036-PY312-COMPARISON.json), [results/CURVED-SAMPLER-036-RAY-VALIDATION.json](../../results/CURVED-SAMPLER-036-RAY-VALIDATION.json), [results/CURVED-SAMPLER-036-SITE-CONTRACT-COMPARISON.json](../../results/CURVED-SAMPLER-036-SITE-CONTRACT-COMPARISON.json), [results/CURVED-SAMPLER-036-SITE-FIXTURES.json](../../results/CURVED-SAMPLER-036-SITE-FIXTURES.json), [results/CURVED-SAMPLER-036-SUMMARY.json](../../results/CURVED-SAMPLER-036-SUMMARY.json), [results/CURVED-SAMPLER-036-VALIDATION.json](../../results/CURVED-SAMPLER-036-VALIDATION.json), [results/CURVED-SAMPLER-036-poses.jsonl.gz](../../results/CURVED-SAMPLER-036-poses.jsonl.gz).

## LOG-2F26BB26A8

**SITE-CYLINDER-037 — exact vertical Site replay and physical-scale sensitivity**

start: 2026-10-24T15:40:19.981325Z; end: 2026-10-24T15:40:23.010407Z; receipt recording: 2026-10-24T15:33:51.594977Z; start: 2026-10-24T15:28:59.235487Z; end: 2026-10-24T15:29:03.878526Z; receipt recording: 2026-10-24T15:46:58.897398Z; date-only record: 2026-10-24 (date statement; not a run timestamp); original date statement: 24 October 2026 UTC. Local exact-source optical validation, not actual K4 or Site UI/publication work.

Type: exact source-model replay; finite sensitivity benchmark; synthetic codec controls; physical-scale and eye-model limits. Outcome: Default97valid confirmed;all11selected assembly cases fail atboth scales; some tiny-pupil subsets pass, no full manual validation or actual K4

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Date: 24 October 2026 UTC. Local exact-source optical validation, not actual K4 or Site UI/publication work.
- [Frozen protocol](../../research/SITE-CYLINDER-037-SPEC.md), [findings](../../research/SITE-CYLINDER-037-FINDINGS.md), [summary](../../results/SITE-CYLINDER-037-SUMMARY.json), [all default margins](../../results/SITE-CYLINDER-037-DEFAULT-MARGINS.csv), [numeric source snapshot](../../results/SITE-CYLINDER-037-SOURCE-SNAPSHOT.json.gz), [complete original](../../results/SITE-CYLINDER-037-ORIGINAL.json.gz).
- Original computation UTC start/end: 2026-10-24T15:28:59.235487+00:00 / 2026-10-24T15:29:03.878526+00:00; final archive-write resources separate. Pinned inspected Site core5b7e883, same vertical-tableau contract. Independent485fixture and70713neighbor sample comparisons agree to1e-9; default97valid, minmargin0.017841939pitch at25/56/87.
- Frozen729neighbors:441complete,186same default key,11keys. Baseline plus10margin-ranked states:22state/scale cases,all full assembly panels fail; tiny pupil10/11U100 and11/11R250 pass, human-scale0/22. Other430complete states not full stability-tested. All3564configurations/per-cell outputs retained; no probabilities or continuous exclusion.
- [Complete semantic replay](../../results/SITE-CYLINDER-037-PY312-COMPARISON.json), [whole-process streaming resource receipt](../../results/SITE-CYLINDER-037-RESOURCE-REPLAY.json): unchanged geometry, full data, peak356155392bytes/4.65seconds on measured replay. Original pre-serialization RSS does not claim final write peak.
- Actual copper and horizontal036 remain distinct. No Site source copied/edited/archived; read-only inspected math/data executed to snapshot factual outputs. No repository push, paid check or actual K4 candidate.

- Final local aggregate validation: 665 tests pass on Python3.9/3.12; [UTC receipt/full logs](../../results/SITE-CYLINDER-037-VALIDATION.json). Prior036 preserved, no actual K4 comparison or Source edit/archive/publication.

Related files: [research/SITE-CYLINDER-037-FINDINGS.md](../../research/SITE-CYLINDER-037-FINDINGS.md), [research/SITE-CYLINDER-037-SPEC.md](../../research/SITE-CYLINDER-037-SPEC.md), [results/SITE-CYLINDER-037-DEFAULT-MARGINS.csv](../../results/SITE-CYLINDER-037-DEFAULT-MARGINS.csv), [results/SITE-CYLINDER-037-ORIGINAL.json.gz](../../results/SITE-CYLINDER-037-ORIGINAL.json.gz), [results/SITE-CYLINDER-037-PY312-COMPARISON.json](../../results/SITE-CYLINDER-037-PY312-COMPARISON.json), [results/SITE-CYLINDER-037-RESOURCE-REPLAY.json](../../results/SITE-CYLINDER-037-RESOURCE-REPLAY.json), [results/SITE-CYLINDER-037-SOURCE-SNAPSHOT.json.gz](../../results/SITE-CYLINDER-037-SOURCE-SNAPSHOT.json.gz), [results/SITE-CYLINDER-037-SUMMARY.json](../../results/SITE-CYLINDER-037-SUMMARY.json), [results/SITE-CYLINDER-037-VALIDATION.json](../../results/SITE-CYLINDER-037-VALIDATION.json).

## LOG-958B11958D

**COVER-SELECTOR-038 — boundary-free selector follow-through**

start: 2026-10-24T17:02:06.639063Z; end: 2026-10-24T17:02:08.592232Z; date-only record: 2026-10-24 (date statement; not a run timestamp); original date statement: 2026-10-24 UTC.

Type: analytical constraints; synthetic validation. Outcome: 120selector descriptions complete;84newstride descriptions, no outer cipher identified

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Date: 2026-10-24 UTC.
- Actual original calculation start: `2026-10-24T17:02:06.639063+00:00`; end: `2026-10-24T17:02:08.592232+00:00`. These are receipt values, not commit/publication times.
- Scope/result: 120 selector descriptions complete; 84 newstride descriptions, no outer cipher identified. General family limits remain explicit.
- [Findings/protocol/control links](../../research/COVER-SELECTOR-038-FINDINGS.md); [original receipt](../../results/COVER-SELECTOR-038-ORIGINAL.json); [seven-family matrix](../../research/SEVEN-FAMILY-REVIEW-046.md).
- New results are local-only; no Site or canonical ciphertext change. Original/replay/control times are distinct.

Related files: [research/COVER-SELECTOR-038-FINDINGS.md](../../research/COVER-SELECTOR-038-FINDINGS.md), [research/SEVEN-FAMILY-REVIEW-046.md](../../research/SEVEN-FAMILY-REVIEW-046.md), [results/COVER-SELECTOR-038-ORIGINAL.json](../../results/COVER-SELECTOR-038-ORIGINAL.json).

## LOG-0BD1D35E69

**CONTEXT-SPELLING-039 — reversible context prediction limits**

start: 2026-10-24T17:05:27.894998Z; end: 2026-10-24T17:05:27.957067Z; date-only record: 2026-10-24 (date statement; not a run timestamp); original date statement: 2026-10-24 UTC.

Type: analytical constraints; synthetic validation. Outcome: One-letter contexts fail;two-letter fits are underdetermined and predict no held-out mistake

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Date: 2026-10-24 UTC.
- Actual original calculation start: `2026-10-24T17:05:27.894998+00:00`; end: `2026-10-24T17:05:27.957067+00:00`. These are receipt values, not commit/publication times.
- Scope/result: One-letter contexts fail; two-letter fits are underdetermined and predict no held-out mistake. General family limits remain explicit.
- [Findings/protocol/control links](../../research/CONTEXT-SPELLING-039-FINDINGS.md); [original receipt](../../results/CONTEXT-SPELLING-039-ORIGINAL.json); [seven-family matrix](../../research/SEVEN-FAMILY-REVIEW-046.md).
- New results are local-only; no Site or canonical ciphertext change. Original/replay/control times are distinct.

Related files: [research/CONTEXT-SPELLING-039-FINDINGS.md](../../research/CONTEXT-SPELLING-039-FINDINGS.md), [research/SEVEN-FAMILY-REVIEW-046.md](../../research/SEVEN-FAMILY-REVIEW-046.md), [results/CONTEXT-SPELLING-039-ORIGINAL.json](../../results/CONTEXT-SPELLING-039-ORIGINAL.json).

## LOG-EECF3F88C3

**PHYSICAL-IDENTIFIABILITY-040 — source ambiguity and scale**

start: 2026-10-24T17:09:08.890519Z; end: 2026-10-24T17:09:09.091089Z; date-only record: 2026-10-24 (date statement; not a run timestamp); original date statement: 2026-10-24 UTC.

Type: analytical constraints; synthetic validation. Outcome: Identical image pairs admit different physical sources; real reviewed pairs remain uncertified

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Date: 2026-10-24 UTC.
- Actual original calculation start: `2026-10-24T17:09:08.890519+00:00`; end: `2026-10-24T17:09:09.091089+00:00`. These are receipt values, not commit/publication times.
- Scope/result: Identical image pairs admit different physical sources; real reviewed pairs remain uncertified. General family limits remain explicit.
- [Findings/protocol/control links](../../research/PHYSICAL-IDENTIFIABILITY-040-FINDINGS.md); [original receipt](../../results/PHYSICAL-IDENTIFIABILITY-040-ORIGINAL.json); [seven-family matrix](../../research/SEVEN-FAMILY-REVIEW-046.md).
- New results are local-only; no Site or canonical ciphertext change. Original/replay/control times are distinct.

Related files: [research/PHYSICAL-IDENTIFIABILITY-040-FINDINGS.md](../../research/PHYSICAL-IDENTIFIABILITY-040-FINDINGS.md), [research/SEVEN-FAMILY-REVIEW-046.md](../../research/SEVEN-FAMILY-REVIEW-046.md), [results/PHYSICAL-IDENTIFIABILITY-040-ORIGINAL.json](../../results/PHYSICAL-IDENTIFIABILITY-040-ORIGINAL.json).

## LOG-B657ACC6D6

**SIGABA-SUPPORT-SIGNATURE-041 — exact memoization without scaling gain**

start: 2026-10-24T17:15:25.791070Z; end: 2026-10-24T17:19:26.330832Z; start: 2026-10-24T17:16:25.933126Z; end: 2026-10-24T17:17:26.030296Z; start: 2026-10-24T17:18:26.290111Z; end: 2026-10-24T17:19:26.310318Z; start: 2026-10-24T17:15:25.823933Z; end: 2026-10-24T17:16:25.862384Z; start: 2026-10-24T17:17:26.115467Z; end: 2026-10-24T17:18:26.194608Z; date-only record: 2026-10-24 (date statement; not a run timestamp); original date statement: 2026-10-24 UTC.

Type: synthetic solver engineering; resource benchmark. Outcome: Exact tiny sets pass;real synthetic prefixes have zero cache hits and remain unresolved

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Date: 2026-10-24 UTC.
- Actual original calculation start: `2026-10-24T17:15:25.791070+00:00`; end: `2026-10-24T17:19:26.330832+00:00`. These are receipt values, not commit/publication times.
- Scope/result: Exact tiny sets pass; real synthetic prefixes have zero cache hits and remain unresolved. General family limits remain explicit.
- [Findings/protocol/control links](../../research/SIGABA-SUPPORT-SIGNATURE-041-FINDINGS.md); [original receipt](../../results/SIGABA-SUPPORT-SIGNATURE-041-SUMMARY.json); [seven-family matrix](../../research/SEVEN-FAMILY-REVIEW-046.md).
- New results are local-only; no Site or canonical ciphertext change. Original/replay/control times are distinct.

Related files: [research/SEVEN-FAMILY-REVIEW-046.md](../../research/SEVEN-FAMILY-REVIEW-046.md), [research/SIGABA-SUPPORT-SIGNATURE-041-FINDINGS.md](../../research/SIGABA-SUPPORT-SIGNATURE-041-FINDINGS.md), [results/SIGABA-SUPPORT-SIGNATURE-041-SUMMARY.json](../../results/SIGABA-SUPPORT-SIGNATURE-041-SUMMARY.json).

## LOG-4AEC06FD9C

**CLOCK-CIVIL-042 — whole-year shared-phase interpretation**

start: 2026-10-24T18:27:33.660889Z; end: 2026-10-24T18:27:33.928489Z; date-only record: 2026-10-24 (date statement; not a run timestamp); original date statement: 2026-10-24 UTC.

Type: analytical constraints; source research. Outcome: Automatic civil-time interpretation fails;literal/standard-time/single-date models remain open

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Date: 2026-10-24 UTC.
- Actual original calculation start: `2026-10-24T18:27:33.660889+00:00`; end: `2026-10-24T18:27:33.928489+00:00`. These are receipt values, not commit/publication times.
- Scope/result: Automatic civil-time interpretation fails; literal/standard-time/single-date models remain open. General family limits remain explicit.
- [Findings/protocol/control links](../../research/CLOCK-CIVIL-042-FINDINGS.md); [original receipt](../../results/CLOCK-CIVIL-042-ORIGINAL.json); [seven-family matrix](../../research/SEVEN-FAMILY-REVIEW-046.md).
- New results are local-only; no Site or canonical ciphertext change. Original/replay/control times are distinct.

Related files: [research/CLOCK-CIVIL-042-FINDINGS.md](../../research/CLOCK-CIVIL-042-FINDINGS.md), [research/SEVEN-FAMILY-REVIEW-046.md](../../research/SEVEN-FAMILY-REVIEW-046.md), [results/CLOCK-CIVIL-042-ORIGINAL.json](../../results/CLOCK-CIVIL-042-ORIGINAL.json).

## LOG-7FA3D57DFA

**COMPRESS-TRANSPORT-043 — legacy compression with fixed transports**

start: 2026-10-24T18:35:43.988050Z; end: 2026-10-24T18:35:44.455127Z; date-only record: 2026-10-24 (date statement; not a run timestamp); original date statement: 2026-10-24 UTC.

Type: finite K4 model tests; representation validation. Outcome: All8fixed.Ztransports fail magic;other compressors/transports/layers remain untested

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Date: 2026-10-24 UTC.
- Actual original calculation start: `2026-10-24T18:35:43.988050+00:00`; end: `2026-10-24T18:35:44.455127+00:00`. These are receipt values, not commit/publication times.
- Scope/result: All 8 fixed.Ztransports fail magic; other compressors/transports/layers remain untested. General family limits remain explicit.
- [Findings/protocol/control links](../../research/COMPRESS-TRANSPORT-043-FINDINGS.md); [original receipt](../../results/COMPRESS-TRANSPORT-043-ORIGINAL.json); [seven-family matrix](../../research/SEVEN-FAMILY-REVIEW-046.md).
- New results are local-only; no Site or canonical ciphertext change. Original/replay/control times are distinct.

Related files: [research/COMPRESS-TRANSPORT-043-FINDINGS.md](../../research/COMPRESS-TRANSPORT-043-FINDINGS.md), [research/SEVEN-FAMILY-REVIEW-046.md](../../research/SEVEN-FAMILY-REVIEW-046.md), [results/COMPRESS-TRANSPORT-043-ORIGINAL.json](../../results/COMPRESS-TRANSPORT-043-ORIGINAL.json).

## LOG-0EBDC03044

**MINIMUM-REPAIR-044 — exact multi-substitution distances**

start: 2026-10-24T18:41:58.298226Z; end: 2026-10-24T18:41:58.732664Z; date-only record: 2026-10-24 (date statement; not a run timestamp); original date statement: 2026-10-24 UTC.

Type: analytical constraints; finite K4 model tests. Outcome: 1536minimum profiles complete;no observed error or English plaintext identified

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Date: 2026-10-24 UTC.
- Actual original calculation start: `2026-10-24T18:41:58.298226+00:00`; end: `2026-10-24T18:41:58.732664+00:00`. These are receipt values, not commit/publication times.
- Scope/result: 1536 minimum profiles complete; no observed error or English plaintext identified. General family limits remain explicit.
- [Findings/protocol/control links](../../research/MINIMUM-REPAIR-044-FINDINGS.md); [original receipt](../../results/MINIMUM-REPAIR-044-ORIGINAL.json); [seven-family matrix](../../research/SEVEN-FAMILY-REVIEW-046.md).
- New results are local-only; no Site or canonical ciphertext change. Original/replay/control times are distinct.

Related files: [research/MINIMUM-REPAIR-044-FINDINGS.md](../../research/MINIMUM-REPAIR-044-FINDINGS.md), [research/SEVEN-FAMILY-REVIEW-046.md](../../research/SEVEN-FAMILY-REVIEW-046.md), [results/MINIMUM-REPAIR-044-ORIGINAL.json](../../results/MINIMUM-REPAIR-044-ORIGINAL.json).

## LOG-FC810AFBC4

**COVER-LANGUAGE-045 — non-veto language calibration and source-rule review**

start: 2026-10-24T18:49:48.099574Z; end: 2026-10-24T18:50:32.936437Z; start: 2026-10-24T18:51:07.776485Z; end: 2026-10-24T18:51:07.777457Z; date-only record: 2026-10-24 (date statement; not a run timestamp); original date statement: 2026-10-24 UTC.

Type: statistical diagnostic; synthetic validation. Outcome: K3retained;5of6plants rank first;2of7matched null maxima equal/exceed actual;no positive identification

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Date: 2026-10-24 UTC.
- Actual original calculation start: `2026-10-24T18:49:48.099574+00:00`; end: `2026-10-24T18:50:32.936437+00:00`. These are receipt values, not commit/publication times.
- Scope/result: K3 retained; 5 of 6 plants rank first; 2 of 7 matched null maxima equal/exceed actual; no positive identification. General family limits remain explicit.
- [Findings/protocol/control links](../../research/COVER-LANGUAGE-045-FINDINGS.md); [original receipt](../../results/COVER-LANGUAGE-045-ORIGINAL.json); [seven-family matrix](../../research/SEVEN-FAMILY-REVIEW-046.md).
- New results are local-only; no Site or canonical ciphertext change. Original/replay/control times are distinct.
- Separate [late 038 control](../../results/REVIEW-CONTROLS-045.json) and [memoryless length-changing spelling review](../../research/SPELLING-MORPHISM-REVIEW-045-FINDINGS.md) preserve original chronology; neither is a new ciphertext domain.

Related files: [research/COVER-LANGUAGE-045-FINDINGS.md](../../research/COVER-LANGUAGE-045-FINDINGS.md), [research/SEVEN-FAMILY-REVIEW-046.md](../../research/SEVEN-FAMILY-REVIEW-046.md), [research/SPELLING-MORPHISM-REVIEW-045-FINDINGS.md](../../research/SPELLING-MORPHISM-REVIEW-045-FINDINGS.md), [results/COVER-LANGUAGE-045-ORIGINAL.json](../../results/COVER-LANGUAGE-045-ORIGINAL.json), [results/REVIEW-CONTROLS-045.json](../../results/REVIEW-CONTROLS-045.json).

## LOG-7D6CAE81B9

**REVIEW-CONTROLS-046 — explicit independent review corrections**

start: 2026-10-24T18:55:29.101871Z; end: 2026-10-24T18:55:29.116792Z; date-only record: 2026-10-24 (date statement; not a run timestamp); original date statement: 2026-10-24 UTC.

Type: regression and replication. Outcome: Active-root interruption, wrong-DST calculation and invalidflags pass; original runs unchanged

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Date: 2026-10-24 UTC.
- Actual original calculation start: `2026-10-24T18:55:29.101871+00:00`; end: `2026-10-24T18:55:29.116792+00:00`. These are receipt values, not commit/publication times.
- Scope/result: Active-root interruption, wrong-DST calculation and invalidflags pass; original runs unchanged. General family limits remain explicit.
- [Findings/protocol/control links](../../research/REVIEW-CONTROLS-046.md); [original receipt](../../results/REVIEW-CONTROLS-046.json); [seven-family matrix](../../research/SEVEN-FAMILY-REVIEW-046.md).
- New results are local-only; no Site or canonical ciphertext change. Original/replay/control times are distinct.

Related files: [research/REVIEW-CONTROLS-046.md](../../research/REVIEW-CONTROLS-046.md), [research/SEVEN-FAMILY-REVIEW-046.md](../../research/SEVEN-FAMILY-REVIEW-046.md), [results/REVIEW-CONTROLS-046.json](../../results/REVIEW-CONTROLS-046.json).

## LOG-6DA0BC1C60

**PHOTO-NATIVE-047 — bounded native LOC correspondence admission**

receipt recording: 2026-10-24T19:25:10.697950Z; date-only record: 2026-10-24 (date statement; not a run timestamp); original date statement: 2026-10-24 UTC. Frozen protocol saved at `2026-10-24T19:17:13.787510+00:00`; native inspection finished at `2026-10-24T19:19:56.054606+00:00`. Validation/replay times are separate.

Type: source research; physical evidence admission. Outcome: Native-pixel attempt complete; zero certified material-point pairs, no real fit; crop registration independently exact

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Date: 2026-10-24 UTC. Frozen protocol saved at `2026-10-24T19:17:13.787510+00:00`; native inspection finished at `2026-10-24T19:19:56.054606+00:00`. Validation/replay times are separate.
- Scope: one verified 3384 × 4283 LOC exposure, initial 800 × 800 ROI plus eight native crops; ten rejected bright-feature boxes. Zero certified material-point pairs, no geometric fit and no K4 evaluation. This is bounded manual failure to establish identities, not proof the photo can never yield them.
- [Findings](../../research/PHOTO-NATIVE-047-FINDINGS.md); [frozen protocol](../../research/PHOTO-NATIVE-047-SPEC.md); [native crops/transforms/annotations](../../research/evidence/2026-10-24-native-loc/README.md); [exact crop check](../../results/PHOTO-NATIVE-047-CROP-CHECK.json); [validation](../../results/PHOTO-NATIVE-047-VALIDATION.json). Local only.

Related files: [research/PHOTO-NATIVE-047-FINDINGS.md](../../research/PHOTO-NATIVE-047-FINDINGS.md), [research/PHOTO-NATIVE-047-SPEC.md](../../research/PHOTO-NATIVE-047-SPEC.md), [research/evidence/2026-10-24-native-loc/README.md](../../research/evidence/2026-10-24-native-loc/README.md), [results/PHOTO-NATIVE-047-CROP-CHECK.json](../../results/PHOTO-NATIVE-047-CROP-CHECK.json), [results/PHOTO-NATIVE-047-VALIDATION.json](../../results/PHOTO-NATIVE-047-VALIDATION.json).

## LOG-17280EC9B8

**CANDIDATE-FIRST-048 — exact source-key preflight before message generation**

start: 2026-10-24T20:15:20.481864Z; end: 2026-10-24T20:16:33.914933Z; start: 2026-10-24T20:11:28.873110Z; end: 2026-10-24T20:13:08.724291Z; start: 2026-10-24T19:40:49.963515Z; end: 2026-10-24T19:40:52.486912Z; start: 2026-10-24T19:51:27.981620Z; end: 2026-10-24T19:51:30.294733Z; date-only record: 2026-10-24 (date statement; not a run timestamp); original date statement: 2026-10-24 UTC. Original calculation started `2026-10-24T19:40:49.963515+00:00`, finished `2026-10-24T19:40:52.486912+00:00`. Replay and regression timings are separate.

Type: analytical constraints; synthetic validation. Outcome: 582models;42free-key survivors, zeroBrown source-key/97letter plaintext matches; conditional bank omitted

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Date: 2026-10-24 UTC. Original calculation started `2026-10-24T19:40:49.963515+00:00`, finished `2026-10-24T19:40:52.486912+00:00`. Replay and regression timings are separate.
- Result/scope: 582 models;42 free-key survivors, zeroBrown source-key/97 letter plaintext matches; conditional bank omitted. No global family exclusion.
- [Findings](../../research/CANDIDATE-FIRST-048-FINDINGS.md); [frozen protocol](../../research/CANDIDATE-FIRST-048-SPEC.md); [original receipt](../../results/CANDIDATE-FIRST-048-ORIGINAL.json); [full Python 3.12 replay](../../results/CANDIDATE-FIRST-048-REPLAY.json); [shared replay/resource verification](../../results/048-050-REPLAY-VALIDATION.json); [prior coverage](../../research/048-050-PRIOR-COVERAGE.md). Local only; no paid verifier, Site edit or push.

Related files: [research/048-050-PRIOR-COVERAGE.md](../../research/048-050-PRIOR-COVERAGE.md), [research/CANDIDATE-FIRST-048-FINDINGS.md](../../research/CANDIDATE-FIRST-048-FINDINGS.md), [research/CANDIDATE-FIRST-048-SPEC.md](../../research/CANDIDATE-FIRST-048-SPEC.md), [results/048-050-REPLAY-VALIDATION.json](../../results/048-050-REPLAY-VALIDATION.json), [results/CANDIDATE-FIRST-048-ORIGINAL.json](../../results/CANDIDATE-FIRST-048-ORIGINAL.json), [results/CANDIDATE-FIRST-048-REPLAY.json](../../results/CANDIDATE-FIRST-048-REPLAY.json).

## LOG-9F394BCB00

**ENE-ROUTE-049 — literal and digital ENE with fixed arithmetic**

start: 2026-10-24T20:16:34.000973Z; end: 2026-10-24T20:16:48.028438Z; start: 2026-10-24T20:13:49.930304Z; end: 2026-10-24T20:14:07.042196Z; start: 2026-10-24T19:45:19.185573Z; end: 2026-10-24T19:45:36.969399Z; start: 2026-10-24T19:51:30.356028Z; end: 2026-10-24T19:51:44.413999Z; date-only record: 2026-10-24 (date statement; not a run timestamp); original date statement: 2026-10-24 UTC. Original calculation started `2026-10-24T19:45:19.185573+00:00`, finished `2026-10-24T19:45:36.969399+00:00`. Replay and regression timings are separate.

Type: finite K4 model tests; synthetic validation. Outcome: 56,454descriptions/34,569routes/656,811fixed cases; zero24letter hits; actual/null maxima8versus7–8

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Date: 2026-10-24 UTC. Original calculation started `2026-10-24T19:45:19.185573+00:00`, finished `2026-10-24T19:45:36.969399+00:00`. Replay and regression timings are separate.
- Result/scope: 56,454 descriptions/34,569 routes/656,811 fixed cases; zero 24 letter hits; actual/null maxima 8 versus 7–8. No global family exclusion.
- [Findings](../../research/ENE-ROUTE-049-FINDINGS.md); [frozen protocol](../../research/ENE-ROUTE-049-SPEC.md); [original receipt](../../results/ENE-ROUTE-049-ORIGINAL.json); [full Python 3.12 replay](../../results/ENE-ROUTE-049-REPLAY.json); [shared replay/resource verification](../../results/048-050-REPLAY-VALIDATION.json); [prior coverage](../../research/048-050-PRIOR-COVERAGE.md). Local only; no paid verifier, Site edit or push.

Related files: [research/048-050-PRIOR-COVERAGE.md](../../research/048-050-PRIOR-COVERAGE.md), [research/ENE-ROUTE-049-FINDINGS.md](../../research/ENE-ROUTE-049-FINDINGS.md), [research/ENE-ROUTE-049-SPEC.md](../../research/ENE-ROUTE-049-SPEC.md), [results/048-050-REPLAY-VALIDATION.json](../../results/048-050-REPLAY-VALIDATION.json), [results/ENE-ROUTE-049-ORIGINAL.json](../../results/ENE-ROUTE-049-ORIGINAL.json), [results/ENE-ROUTE-049-REPLAY.json](../../results/ENE-ROUTE-049-REPLAY.json).

## LOG-A9DC171AB1

**HAND-GRAMMAR-050 — complete fixed-key hand-operation grammar**

start: 2026-10-24T19:49:16.853596Z; end: 2026-10-24T19:49:24.990209Z; start: 2026-10-24T19:51:44.463055Z; end: 2026-10-24T19:51:51.024770Z; date-only record: 2026-10-24 (date statement; not a run timestamp); original date statement: 2026-10-24 UTC. Original calculation started `2026-10-24T19:49:16.853596+00:00`, finished `2026-10-24T19:49:24.990209+00:00`. Replay and regression timings are separate.

Type: finite K4 model tests; synthetic validation. Outcome: 56,355depth0–3descriptions/27,323operators; no24letter hit; maximum7versus null6–8; keys/widths fixed

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Date: 2026-10-24 UTC. Original calculation started `2026-10-24T19:49:16.853596+00:00`, finished `2026-10-24T19:49:24.990209+00:00`. Replay and regression timings are separate.
- Result/scope: 56,355 depth 0–3 descriptions/27,323 operators; no 24 letter hit; maximum 7 versus null 6–8; keys/widths fixed. No global family exclusion.
- [Findings](../../research/HAND-GRAMMAR-050-FINDINGS.md); [frozen protocol](../../research/HAND-GRAMMAR-050-SPEC.md); [original receipt](../../results/HAND-GRAMMAR-050-ORIGINAL.json); [full Python 3.12 replay](../../results/HAND-GRAMMAR-050-REPLAY.json); [shared replay/resource verification](../../results/048-050-REPLAY-VALIDATION.json); [prior coverage](../../research/048-050-PRIOR-COVERAGE.md). Local only; no paid verifier, Site edit or push.

Related files: [research/048-050-PRIOR-COVERAGE.md](../../research/048-050-PRIOR-COVERAGE.md), [research/HAND-GRAMMAR-050-FINDINGS.md](../../research/HAND-GRAMMAR-050-FINDINGS.md), [research/HAND-GRAMMAR-050-SPEC.md](../../research/HAND-GRAMMAR-050-SPEC.md), [results/048-050-REPLAY-VALIDATION.json](../../results/048-050-REPLAY-VALIDATION.json), [results/HAND-GRAMMAR-050-ORIGINAL.json](../../results/HAND-GRAMMAR-050-ORIGINAL.json), [results/HAND-GRAMMAR-050-REPLAY.json](../../results/HAND-GRAMMAR-050-REPLAY.json).

## LOG-74E9EAFB2D

**CONTROL-CORRECTION-048-049 — actual lookup, returned witnesses and prior profiles**

receipt recording: 2026-10-24T20:26:19.951534Z; start: 2026-10-24T20:11:28.873110Z; end: 2026-10-24T20:13:08.724291Z; start: 2026-10-24T20:13:49.930304Z; end: 2026-10-24T20:14:07.042196Z; date-only record: 2026-10-24 (date statement; not a run timestamp); original date statement: 2026-10-24 UTC. Corrected 048 calculation: `2026-10-24T20:11:28.873110+00:00` to `2026-10-24T20:13:08.724291+00:00`; corrected 049 calculation: `2026-10-24T20:13:49.930304+00:00` to `2026-10-24T20:14:07.042196+00:00`. Scientific replay and regression UTCs are separate.

Type: regression and replication; synthetic validation. Outcome: Full source lookup and actual returned-hit recovery verified; 576 prior-profile comparisons agree; actual/null results unchanged

Source: [canonical experiment log](../../research/EXPERIMENTS.md).

- Date: 2026-10-24 UTC. Corrected 048 calculation: `2026-10-24T20:11:28.873110+00:00` to `2026-10-24T20:13:08.724291+00:00`; corrected 049 calculation: `2026-10-24T20:13:49.930304+00:00` to `2026-10-24T20:14:07.042196+00:00`. Scientific replay and regression UTCs are separate.
- Scope/result: all 24 full-source lookup plants, six actual returned-hit witnesses and 576 prior-profile comparisons pass. All original actual/null payloads and model domains remain unchanged; no candidate bank or new family.
- [Correction/provenance](../../research/048-049-CONTROL-CORRECTION.md); [048 current receipt](../../results/CANDIDATE-FIRST-048-CONTROLLED.json); [049 current receipt](../../results/ENE-ROUTE-049-CONTROLLED.json); [replay validation](../../results/048-049-CONTROL-CORRECTION-REPLAY.json); [new regression](../../results/048-049-CONTROL-CORRECTION-VALIDATION.json). Local only.

Related files: [research/048-049-CONTROL-CORRECTION.md](../../research/048-049-CONTROL-CORRECTION.md), [results/048-049-CONTROL-CORRECTION-REPLAY.json](../../results/048-049-CONTROL-CORRECTION-REPLAY.json), [results/048-049-CONTROL-CORRECTION-VALIDATION.json](../../results/048-049-CONTROL-CORRECTION-VALIDATION.json), [results/CANDIDATE-FIRST-048-CONTROLLED.json](../../results/CANDIDATE-FIRST-048-CONTROLLED.json), [results/ENE-ROUTE-049-CONTROLLED.json](../../results/ENE-ROUTE-049-CONTROLLED.json).
