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
