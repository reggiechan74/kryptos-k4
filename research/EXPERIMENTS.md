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

## Pinned Barney/Scott prior-art review — revision 2026-10-18

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

## AUTOKEY-CONSTRAINT-001 — complete declared lag audit

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

## GROMARK-ALPHABET-001 — one pinned published tuple

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

## Historical-clock correction — documentation only, 2026-10-18

- Parent commit: 9d4b4cb6e10ced9d408ef20739c91c4386a8da27.
- Corrected the 1972 panel's middle lower line to HANOI from the parent's independent
  visual inspection; current reading PEKING / HANOI / MANILA. Original erroneous
  SHANGHAI transcription retained in Git history and explicitly noted in the report.
- Directly read LeMO model metadata (accession 1995/09/0108;1972 gift,1968date).
  Supplied 48-image visual assessment distinguishes model layout from installed
  clock; 1989 panel and true-ENE orientation remain unresolved. Sketchbook source pending.
- Checked dependent current summaries and dated readings. No code, tests,
  cryptanalytic artifacts or model scope changed; no new cipher search executed.


## Historical-clock source-note completion — documentation only

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

## GROMARK-IDENTIFIABILITY-001 — 73 fixed-model difference queries

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

## SILK-PERIODIC-001 — 2026-10-18

- Source-first table and 24 decisive cells checked against both photographs; independent check supplied before pilot.
- Frozen specification bb0cfb9c0cd9c75b13782c1cc11cf34535e0fdd9; implementation f82749aa22e14c063d8fc3c02ff4e6f2a381c616.
- [Findings](SILK-PERIODIC-FINDINGS.md): all 12 periods contradicted, zero keyword enumeration, no full plaintext output. Proof already known before specification.
- Required segments JICEHTUFLMSXZ / TCUFDISXLFX; first segment gives 12 phase-origin-independent contradictions.
- Controls and 118 tests pass; 0.003 seconds action time under 5 seconds cap; no randomness. Stable proof replay and artifact hash checked.
- Snapshot `results/silk-periodic-runs/20261018T153221Z-b7f6cad7292747f6ba81099de8a671e1/`; [validation](../results/SILK-PERIODIC-VALIDATION.json).
- Stop at fixed-chart, direct period 1–12 scope; no historical doctrine or whole-family exclusion.

## DYNAMIC-KEY-001 — stateful key continuation, 2026-10-22

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
  [DYNAMIC-KEY-FINDINGS.md](DYNAMIC-KEY-FINDINGS.md). No geographic retest.
- Saved run: results/dynamic-key-runs/20261022T120128Z-c15ba5ffeb55479490d2be553daf60f0/.

## ASYMMETRIC-PRIMER-001 and PLAINTEXT-STEP-001 — 2026-10-22

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
- Findings/ranking/scopes: [FIXED-PILOT-FINDINGS.md](FIXED-PILOT-FINDINGS.md).
- Saved runs: results/asymmetric-primer-runs/20261022T120817Z-ef4199fc397e4bd9bc6ca2fb3bfdc2e2/
  and results/plaintext-step-runs/20261022T121001Z-38f7134c1bc3445ea7bf00efc70d2e11/.
  Both completed exactly once after specification and code commits.
- No remote operation; prior experiments/results remain unchanged.

## Documentation-only proposal — 2026-10-22

Recorded H-SPLIT-COORDINATE-ROUTES in the hypothesis log and fixed-pilot findings:
32 formal independent row/column coordinate-route cases, explicitly unrun and
low evidence; global novelty unproved. Added parent-supplied Friedman/LANAKI
references after targeted PDF text inspection, with historical/source limitations.
No implementation, specification for execution, K4 scores, null controls or test
run was added. Earlier 160-test validation and all result artifacts unchanged.

## ASYMMETRIC-FEEDBACK-001 / SPLIT-COORDINATE-001 — completed continuation

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
- [Findings, parameter counts, scopes and next step](CONTINUATION-FINDINGS.md);
  [validation receipt](../results/CONTINUATION-VALIDATION.json). Both bounded
  families rejected; no solution. Next: compare fully specified forthcoming
  K3-derived composite route against existing 66 permutations before any new run.

## K3-CLOCK-ROUTES-001 — 22 October 2026, 19:32 UTC

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
- [Findings and exact rejected scope](K3-CLOCK-ROUTE-FINDINGS.md);
  [validation](../results/K3-CLOCK-ROUTES-VALIDATION.json). No solution.
