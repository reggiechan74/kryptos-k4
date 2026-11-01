# Experiment log

**Current tracking:** [working to-do list and hypothesis status](HYPOTHESES.md). Reconciled through study063 and METHOD-LITERAL-001 on31 October2026. Studies051–063 and the validated literal utility are published. Historical stage labels retain chronology.

**Separate evidence closeout (not a cipher experiment):** [The 810-cell tableau audit](tableau-cell-audit-20261031/REPORT.md) preserves both frozen readings and unresolved cells. No supported new mechanism was established; no target run or cipher-experiment ID is added. Current admission decisions remain in the canonical ledger.

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

## OCCUPIED-CELL-ROUTES-001 — 22 October 2026, 19:39 UTC

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
- [Findings](OCCUPIED-CELL-FINDINGS.md), [validation](../results/OCCUPIED-CELL-VALIDATION.json).
  Snapshot results/occupied-cell-routes-001-runs/20261022T193953Z-6f4f8efe83e345168a18fdc2f134d845/.
- Local-only, no Site change, no new optical claim, no expanded parameters/families.


## STRATEGY-FOLLOWUP-001 — 22 October 2026

- Frozen spec/source commit `4ec45e0`; implementation committed at `b238209` before
  K4 evaluation. [Findings](STRATEGY-FOLLOWUP-FINDINGS.md) link complete provenance.
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
  [the dated findings addendum](STRATEGY-FOLLOWUP-FINDINGS.md).


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
- [Integration findings](INDEPENDENT-FOLLOWUP-INTEGRATION-2026-10-22.md);212tests pass.
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
- [Final integration report](INDEPENDENT-FOLLOWUP-INTEGRATION-2026-10-22.md): bounded
  four-track batch complete, no K4 lead; clock's specific data/operator limits remain.


## SINGLE-BOUNDARY-RESET-001 — 22 October 2026

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
- [Readable findings and scope](SINGLE-BOUNDARY-RESET-FINDINGS.md). No K4 lead,
  second reset, extra model, canonical change, main or Site update.


## AUTONOMOUS-RECURRENCE-001 — 22 October 2026

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
  242 local regression tests pass. [Findings](AUTONOMOUS-RECURRENCE-FINDINGS.md).
- No order expansion, resets, tree layer, edits, new route, main or Site change.

## ALPHABET-GEOMETRY-001 and GEOMETRIC-PILOT-001 — 22 October 2026

The [representation](ALPHABET-GEOMETRY-REPRESENTATION.md) gives 26 unique binary
arrays and exact base-2/base-3 codes; 325 pair comparisons, strict codebook
round trips and 910 mutations pass. Ordinary sums and modulo-26 codes collide.
The [frozen pilots](ALPHABET-GEOMETRY-PILOT-SPEC.md) were committed before K4
evaluation. A has 18 baseline rechecks and six new geometric-alphabet cases;
only Beaufort period 12 fits training and fails Berlin. B has zero first-crib
survivors among 3,640 raw models and 3,640 distinct outputs. All 72 complete-selector
plants retain truth, including one ambiguous feedback plant. See
[findings](GEOMETRIC-PILOT-FINDINGS.md) and full result/control records. No new
null calibration is needed for these exact rejections; no scope expansion.

## GEOMETRIC-FOLLOWUP-001 — independent replay and numeric security audit

22 October 2026. Original independent pilot and changing-base security bundles
are preserved unchanged with archive/member hashes and exact replay receipts.
All 24 periodic conflict/fit records and all 3,640 prior full feedback outputs
match the independent oracle. This is reproduction, not new K4 search coverage.
The separate finite raw-number lookup across bases 2–61 has 1,560 letter/base
pairs, 1,558 numbers and only the documented 8/27 ambiguities; it requires known
token boundaries, public geometry/order and no extra transform. No roots or
root offsets were searched. [Security findings](GEOMETRIC-BASE-SECURITY-AUDIT.md)
and [exact comparisons](../results/GEOMETRIC-FOLLOWUP-COMPARISON.json) preserve the
full scope, ambiguity controls and every lookup result.

## GEOMETRIC-PERIODIC-NULL-001 — requested first-crib chance calibration

22 October 2026. The independent plan was frozen before null simulation, after
the actual first-crib fit was known. Full 24-model refitting on 19,999 shuffles
reproduces 1,731 exceedances and plus-one Monte Carlo p=0.0866; distribution
18,268/1,728/3 for zero/one/two survivors. Exact single period-12 closure chance
is 382/(97*96). All 479,976 outcomes match the pairwise checker, 5,256 match the
prior oracle, and 24 plants pass. Replay numerical fields and draw/count trace
are exact; only Python version metadata differs (3.12.14 versus local 3.9.6).
[Report](PERIODIC-CRIB-CALIBRATION.md). No rotor or global-hypothesis calibration.

## K4-FROZEN-GLYPH-AFFINE-FEEDBACK-001 — arbitrary-base relaxation

22 October 2026. Original frozen specification, pre-test schema amendment and
two independent implementations are preserved. Both replay byte for byte and
exclude all eight formal affine feature-feedback families within the first crib,
using minimum two-transition parity certificates and full modulo-26 checks.
All 3,264 primary synthetic round trips and retained-coefficient controls pass.
Arbitrary independent bases >=2 contain every proposed digit-plus-two root
schedule, so no root/degree/radix/offset search is needed for this exact family.
Berlin is not evaluated here; the auxiliary direct map remains separately
labeled. [Report](RADIX-FEEDBACK-FINDINGS.md). No post-failure scope expansion.

## IPA-PREPROCESSING-001 — source-fixed phonetic preprocessing

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
[Findings](IPA-PREPROCESSING-FINDINGS.md), [actual records](../results/IPA-PREPROCESSING-001.json),
[local source/replay checks](../results/IPA-SOURCE-COMPARISON.json). Prior phonetic
respelling records are unchanged. No scope expansion after negatives.

## AFFINE-DIGRAPH-PARITY-001 — existing analytical boundary recorded

23 October 2026. Four parent-supplied exact first-crib witnesses are independently
verified against canonical fixtures. Identical two-symbol input parity has
different output parity, excluding the specified same-AZ or same-KRYPTOS fixed
affine 2×2 map for both pair origins, even without invertibility. Zero keys or
matrices searched. Sixteen fixed affine positive cases and sixteen parity
mutations pass. [Boundary and corrected status](AFFINE-DIGRAPH-PARITY-BOUNDARY.md).


## 23 October 2026: stateful tree/path pilot and independent IPA integration

The two fixed tree/subtree-permutation constructions were implemented, controlled and tested continuously across all 97 positions. All 104 settings fail the first crib; this is a bounded negative, not a general tree-cipher exclusion. See [TREE-PATH-CIPHER-FINDINGS.md](TREE-PATH-CIPHER-FINDINGS.md). Independent free-map IPA and source-fixed pronunciation codec audits now replay exactly; see [IPA-CODECS-INTEGRATION.md](IPA-CODECS-INTEGRATION.md). No additional search was launched after these failures.


## REGISTRY-20261023 — current hypothesis scope and evidence gates

Documentation and coverage audit only; zero new K4 evaluations. The current
[canonical section in HYPOTHESES.md](HYPOTHESES.md#current-canonical-coverage-register--reconciled-31-october-2026)
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


## FACE-ROW-001 / LAMP-STREAM-001 — source-gated conditional protocols

The deep evidence synthesis and three source dossiers were materialized, hash-
verified, read locally and preserved unchanged. [Integration receipt](../results/LODESTONE-COMPASS-EVIDENCE-INTEGRATION-001.json).
The [protocol](CONDITIONAL-FACE-LAMP-SPEC.md) was frozen in 3eeb0b1 before any
new K4 evaluation. Parent review is pending; both actual pilots remain unrun.

FACE-ROW-001 coverage only: 768 orientation aliases reduce to 372 distinct full
model signatures. 280 are covered by the retained ROUTE-001 negatives; 92
horizontal carved-row cases remain new. [Complete coverage](../results/FACE-ROW-001-COVERAGE.json),
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
missing a complete codec. [Current readiness receipt](../results/HYPOTHESIS-REGISTER-002.json).


## FACE-ROW-001 / LAMP-STREAM-001 — completed finite batch

Parent review approved the protocol at cdefbb4. Implementation and controls were
committed at 25e107f before K4 evaluation. [Findings](CONDITIONAL-FACE-LAMP-FINDINGS.md)
and [complete actual result](../results/CONDITIONAL-FACE-LAMP-001.json).

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


## GREEK-PHONETIC-001 / SIGABA-INSPIRED-001 — completed candidate batch

[Specification](GREEK-SIGABA-CANDIDATE-SPEC.md) committed at 7bc893f; complete
implementation/planted controls at 6f5ba70; conditional null seeds clarified
before actual runs at a9e4db1. [Full findings](GREEK-SIGABA-CANDIDATE-FINDINGS.md).

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

## 23 October 2026 — historical SIGABA and exclusion-scope audit

SIGABA-CSP889-001 implements the historical mechanism with the published simulator wiring set. Twelve external known-answer vectors pass after an explicit source-derived convention translation; no downloaded software is executed. The frozen 13,520-key domain has zero first-crib survivors; no Berlin evaluation, no broad SIGABA exclusion. [Specification](SIGABA-CSP889-SPEC.md), [findings](SIGABA-CSP889-FINDINGS.md), [controls](../results/SIGABA-CSP889-001-controls.json), [complete result](../results/SIGABA-CSP889-001.json).

The [exclusion audit](EXCLUSION-SCOPE-AUDIT-2026-10-23.md) reviews all 57 canonical records with exact finite coverage, alias accounting and preprocessing assumptions; historical long searches are not represented as freshly rerun. Its concrete untested affine-digraph gap led to AFFINE-DIGRAPH-CROSSED-001: four crossed-role structures, all inconsistent on the first crib, with sixteen literal plants and thirty-six complete small-ring comparisons. [Frozen protocol](AFFINE-DIGRAPH-CROSSED-SPEC.md), [findings](AFFINE-DIGRAPH-CROSSED-FINDINGS.md), [proofs](../results/AFFINE-DIGRAPH-CROSSED-001.json).

## 23 October 2026 — exact full cipher-state inference and physical sources

SIGABA-CSP889-STATE-002 removes the repeated-cipher-start restriction using a two-/three-wheel meet-in-the-middle join. All 520 fixed schedules and all five independent cipher starts are covered: 6,178,315,520 raw descriptions, including the old 13,520 subset. The 350,311 three-letter joined states all fail by position29; zero full first-crib survivors, zero Berlin evaluations. This is not billions of independently executed decryptions or a complete SIGABA exclusion. [Frozen specification](SIGABA-CSP889-STATE-SPEC.md), [findings](SIGABA-CSP889-STATE-FINDINGS.md), [controls](../results/SIGABA-CSP889-STATE-002-controls.json), [complete schedule results](../results/SIGABA-CSP889-STATE-002.json).

The supplied [physical addendum](evidence/2026-10-23-lodestone-compass/KRYPTOS-PHYSICAL-EVIDENCE-ADDENDUM-2026-10-23.md) is preserved separately from the original ZIP. [Local visual verification](evidence/2026-10-23-lodestone-compass/PHYSICAL-ADDENDUM-LOCAL-REVIEW.md) covers eleven selected scans and maintains source conflicts and archival access limits. No invented optical geometry, bearing test or Site change follows from the new source evidence.

## 23 October 2026 — joint-controller boundary and exact non-rotor pivot

SIGABA-JOINT-FEASIBILITY-003 exactly collapses 100,000 index starts to 66,058 magnet functions, but leaves full joint controller inference unimplemented/budget-unresolved. No new actual K4 rotor key search ran. Synthetic timings are projections, not impossibility proofs. The [findings](JOINT-STATE-NONROTOR-FINDINGS.md) give a sound symbolic formulation and resource limits.

NONROTOR-STRUCTURAL-004 tests the frozen cyclic-disc invariant and eight two-round additive Feistel structures with arbitrary shared round functions. Four fail training; four fit 13 letters with 39 function entries still free, then force an incorrect plaintext letter at position 68. All eight reject without function-key enumeration. Unknown partners at crib edges are handled exactly. Original source-table defects and initial redundant second-stage diagnostics are preserved. [Specification](NONROTOR-STRUCTURAL-SPEC.md), [final constraints](../results/NONROTOR-STRUCTURAL-004.json), [controls](../results/NONROTOR-STRUCTURAL-004-controls.json), [independent certificates](../results/NONROTOR-STRUCTURAL-004-independent.json). No extra rounds or variants were added after failure.

## 23 October 2026 — exact wrapper audit, three-round ambiguity and tree-state support

[FEISTEL-SYMMETRY-005](FEISTEL-EXTENSION-SPEC.md) proves all 32 wrapper/coordinate/origin families unequal by explicit synthetic counterexamples. The eight previous no-swap cases are skipped; all 24 newly evaluated cases reject (twelve in training, twelve at the public second stage). Family inequality does not imply disjointness or independent evidence.

FEISTEL-THREE-005 exactly counts four canonical three-round arbitrary-function structures. Each is compatible with all 24 cribs and has more than 10^75 complete-function key descriptions; two different full plaintext witnesses per case prove non-identifiability. The independent signed-potential/sequential-allocation JavaScript counter agrees on all eight training/all-crib counts. Raw key volumes are not plaintext-class counts or probabilities. No additional round was tested.

[TREE-STATE-SUPPORT-006](TREE-STATE-SUPPORT-SPEC.md), frozen separately before its evaluation, prioritizes a registered alternative: all four fixed tree/direction primitives fail each known island even when every initial cipher-label permutation is granted. The plaintext-to-path assignment remains fixed. No prefix reset or reachable-state assumption is used. Forty complete toy permutation comparisons, forty mutation controls and twelve continuous literal-crib plants validate this necessary-condition relaxation. [Combined findings and limitations](FEISTEL-TREE-EXTENSION-FINDINGS.md).

## 23 October 2026 — arbitrary-key Fractionated Morse constraints

MASK-FM-ARBITRARY-007 replaces the prior two fixed alphabets with every bijection between A–Z and the 26 standard Morse trigrams. All 348,160 first-crib word-break/stream-offset contexts reject on repeated cipher-symbol coordinate conflicts, without Berlin evaluation or 26!-key enumeration. Plaintext letter indices are not equated to ciphertext positions. Six complete planted first-stage selectors retain the true keys; 100 complete small permutation comparisons and an independent coordinate-slot oracle validate the result. [Frozen protocol](FRACTIONATED-MORSE-ARBITRARY-SPEC.md), [scoped findings and frontier](FRACTIONATED-MORSE-ARBITRARY-FINDINGS.md), [results](../results/MASK-FM-ARBITRARY-007.json). Other Morse procedures and outer layers remain outside coverage.

## 23 October 2026 — Wheatstone fixed-transition invariant

WHEATSTONE-TRANSITION-008 closes the arbitrary-outer-alphabet gap beyond pinned dictionary-ring tests. Repeated processed ST pairs have different ciphertext equality flags (RV versus SS), excluding the aligned fixed-ring model for arbitrary ring alphabets and starts. No K4 key enumeration or Berlin evaluation ran. Two published modern worked vectors, a tooth-by-tooth oracle, 443,976 factored toy transitions, naive complete size-3/4 controls and 24 continuous literal-crib plants pass. [Protocol](WHEATSTONE-TRANSITION-SPEC.md), [source findings and precise alignment limits](WHEATSTONE-TRANSITION-FINDINGS.md), [certificate](../results/WHEATSTONE-TRANSITION-008.json). Full original historical instructions and other authentic machine variants remain source-gated; no denied source was retrieved through an alternate route.

## 23 October 2026 — disciplined frontier review, no new K4 search

FRONTIER-011 reviews all 60 canonical entries and identifies nine concrete evidence/algorithm gates. No new evidence-grounded cryptanalysis protocol is currently ready; this is a human research assessment, not a universal exhaustion theorem. Stale scope/input pointers (crossed-role affine digraphs, authentic versus inspired SIGABA and its joint solver, finite asymmetric feedback, regional declination and K2 restoration controls) were corrected without duplicate evaluation. [Concise frontier](RESEARCH-FRONTIER-2026-10-23.md), [runnable inventory/preflight and retained replay specifications](specifications/FRONTIER-2026-10-23.json), [complete assessment](../results/FRONTIER-011.json). No new K4 trials, denied-source requests or Site changes.

## 23 October 2026 — complete coupled synthetic SIGABA inference

SIGABA-JOINT-TOY-012 implements a shared reachable index-domain constraint solver with continuous control evolution and independent cipher starts. Ten complete tiny-system raw-key truth streams match byte for byte, with ambiguity preserved. A five-wheel q=6 case completes and retains one raw planted key; a q=4 case exceeds the independent validation-output cap, and q=8 hits the frozen 600-second cap after 5,080/32,768 control starts. The real-sized scaling gate is not passed. No actual K4 ciphertext is evaluated, no free per-time masks or sampled substitute key slice is introduced, and no packages are installed. [Frozen protocol](SIGABA-JOINT-TOY-SPEC.md), [engineering findings](SIGABA-JOINT-TOY-FINDINGS.md), [complete summary and per-case hashes](../results/SIGABA-JOINT-TOY-012.json). Real historical contacts/five-index adapter and stronger factorized or symbolic-control representation remain future work.


## SIGABA-TORUS-013 — exact predicate reuse, unchanged coupled domain

The largest toy inference completed all 32,768 controllers in 534.476 seconds, retaining 2 raw keys. Its declared validation status is True. This is a toy result, not a real-sized gate. Ten independent complete raw-set comparisons and one complete compact-set comparison pass. Predicate identity is checked over 6,739 predicates and 998,515 direct states. No actual K4 evaluation, real-sized gate, package install or Site change. [Protocol](SIGABA-TORUS-SPEC.md), [findings](SIGABA-TORUS-FINDINGS.md), [measured comparison](../results/SIGABA-TORUS-013.json).


## CSP889-REAL-014 — authentic adapter, failed synthetic resource admission

Twelve published vectors pass both directions through adapter, direct machine and physical contacts; six complete tiny systems match independent full raw-key truth. The two frozen real-sized fixtures stop at 17.223 seconds (branch envelope) and 60.161 seconds (wall), both with zero completed controllers. Totals are unknown; no K4 evaluation or negative key coverage. [Protocol](SIGABA-REAL-ADAPTER-SPEC.md), [findings](SIGABA-REAL-ADAPTER-FINDINGS.md). [STAT-001 cross-version diagnosis](STAT-CROSSVERSION-FINDINGS.md) preserves integer draws/tails and archives, checking derived floats against rational moments.


## CSP889-SPARSE-015 — exact sparse ownership and reserved cache

Both runs remain unresolved, with zero completed controllers and unknown total key counts. The dense case reaches the same time-2, 410-node envelope guard, with 202 predicate requests but only three zero-offset builds. The separated-window case still stops at time index 7 with 6,652 peak nodes and zero predicate requests; memory falls to 58.4 MiB, but prefix CPU work remains unresolved. It performed 519,540 owner transitions and 14,181 branch visits. Direct plants remain valid, but no selector recovery or full real-sized compatible-set validation is established. Same two REAL-014 fixtures and caps; six complete independent tiny raw-key comparisons, 18 cache-policy relation comparisons and complete q=3 predicate controls pass. [Protocol](SIGABA-SPARSE-OWNERSHIP-SPEC.md), [findings](SIGABA-SPARSE-OWNERSHIP-FINDINGS.md), [comparison](../results/CSP889-SPARSE-015.json). No actual K4 evaluation or budget expansion.


## CSP889-DOMAIN-016 — profiler-supported immutable domain keys

The prefix run advances from time index 7 to 17, retaining all 66,058 class owners at peak and reaching 35,290 peak nodes, 1,186,963 owner transitions and 249,550 branch visits. It still completes zero controllers and makes zero predicate requests. Therefore actual controller coverage does not advance, although the partial prefix does. It times out at 60.003 seconds with 84.9 MiB peak RSS. The dense case stops at the same time-2 memory frontier after 3.426 seconds with 546.3 MiB RSS. Both total key counts remain unknown; neither is a K4 negative. The unchanged prefix profile attributes 58.075/60.009 seconds self time to merge; phase B caches exact-domain hashes with collision-safe equality. Six complete independent tiny sets and cache invariance pass. [Protocol](SIGABA-DOMAIN-IDENTITY-SPEC.md), [implementation freeze](SIGABA-DOMAIN-IDENTITY-IMPLEMENTATION.md), [findings](SIGABA-DOMAIN-IDENTITY-FINDINGS.md), [comparison](../results/CSP889-DOMAIN-016.json). No adaptive extra optimization, cap increase, Site change or K4 evaluation.


## CSP889-ANCHOR-017 — exact full-torus observation anchoring

Eight complete tiny original-key streams and 24 cache-policy correlated relations agree with physical/unanchored truth, including map-dependent inverse and final offsets. The unchanged separated-window real fixture now reaches observations 21–24 in 4.310 seconds, then hits the branch-memory envelope; zero controllers complete and totals remain unknown. A premature run after an inert mutation-test failure is quarantined and not counted as official coverage. The corrected full gate passed before official rerun. [Protocol](SIGABA-FIRST-OBSERVATION-SPEC.md), [findings](SIGABA-FIRST-OBSERVATION-FINDINGS.md), [chronology](../results/ANCHOR-017-chronology.json). No K4, statistical pruning, filter panel or cap increase.


## CSP889-COMPACT-018 — exact storage, local-only measured controller progress

Actual native controller coverage advances from zero to 12 completed controllers on the dense fixture and 14 on the separated-window fixture. They stop at the unchanged 60-second wall limit, not the old memory envelope, at 162.6 and 152.8 MiB peak RSS. No compatible raw keys occur in either completed controller prefix; the remaining 11,881,364 and 11,881,362 controllers are unresolved. The unfinished controller is retained explicitly. Total key counts remain unknown, not zero. The completed prefixes represent 14,257,651,200,000 and 16,633,926,400,000 raw start descriptions respectively, including index aliases; those are model-domain descriptions, not independent hypotheses or unique plaintexts. Eight tiny fixtures under three representations and three cache policies preserve complete original-key sets, final offsets and anchor inverses. The native result uses explicit exact set encodings. [Protocol](SIGABA-COMPRESSED-DOMAIN-SPEC.md), [pre-run storage choice](SIGABA-COMPRESSED-DOMAIN-IMPLEMENTATION.md), [findings](SIGABA-COMPRESSED-DOMAIN-FINDINGS.md), [comparison](../results/CSP889-COMPACT-018.json). No K4, extra observation, cap increase or remote publication.


## CSP889-FILTER-019 — supplied-anchor necessary filter, local only

Two frozen panels retain 2/3 anchors and 4 controllers each: 20 pairs, 12 filter rejections, 6 false-positive passes and 2 physical feasible pairs. All 1,321,160 reachable-map trials are actually audited, including rejects; zero false negatives. Both supplied plants regenerate the full synthetic ciphertext; fixture1 advances the 29-position unknown gap and passes its second block. The smaller fixture0 panel is preserved after its 16-candidate anchor cap. Counterfactual savings are panel-only, not a full-domain speedup. [Protocol](SIGABA-COLLECTOR-FILTER-SPEC.md), [findings](SIGABA-COLLECTOR-FILTER-FINDINGS.md), [summary](../results/CSP889-FILTER-019.json). No new full-domain controller coverage, K4, cap expansion or publication retry.


## FOLD-SLIDE-020 — anchored progressive monument overlay

- Date: 2026-10-23 UTC. Exact run start/end were not recorded and are unknown; commit/publication times are distinct.
- Type: actual inscription-layout comparison with approximate optical apertures, not a K4 decryption search.
- Protocol: [frozen progressive model](MONUMENT-SLIDE-OVERLAY-SPEC.md), [pre-score registration amendment](MONUMENT-SLIDE-REGISTRATION-AMENDMENT.md).
- Input: full canonical cipher/tableau rows and existing modeled font; MYVGT/AABCD anchor reproduced with no row shift.
- Coverage: 134 frames across two registrations, −33…+33 inclusive; 130 active. Every frame retained.
- Outcome: zero-shift primary 35/856 identical letters; no unusual full-scan label/area excess under 1,999 row shuffles and 1,999 movable-row rotations. Four-report adjusted p=1 for each endpoint/scheme.
- Code: [native evaluator](../experiments/monument_slide.py), [independent pixel oracle](../experiments/monument_slide_oracle.mjs).
- Receipt: [exact positions and masks](../results/FOLD-SLIDE-020-actual.json); [findings and limitations](MONUMENT-FOLD-SLIDE-FINDINGS.md).
- No measured optical calibration, plaintext extraction, Site change or new decoding candidate.


## SITE-OVERLAY-015 — live Site source handoff and static validation

- Date: 2026-10-23 UTC, integration record date; exact original Site-test and publication times were not supplied.
- Type: Site source archive and static data validation, not an additional K4 cipher experiment.
- The parent relayed native publication confirmation: Site version 15 live, public access revision 2 unchanged. Source commit `086ace2bfb2ca6e23ddddf76fe5f37c51dd75aea`, based on `d4155931cd760d4222c9f66916551110eb40053b`. No deployment performed here.
- Exact local patch archived; all 25 changed paths and 18 new-file bodies independently match the source commit, with no child-checkout write. Candidate/dist new modules agree.
- Input/glyph values and all 134 embedded column-frame oracle records match retained research data. Local validation is static and executes no handed-off JavaScript.
- Owner reports 87 code tests passed. Actual rendered-browser QA remained blocked by locked Mac; no local full Site suite or native-browser replay is claimed.
- Row movement is exploratory; no systematic row scan or inherited column-only null p-value.
- [Archive and limitations](../docs/site-source/manual-overlay-v15/README.md), [receipt](../results/SITE-MANUAL-FOLD-V15-SOURCE-HANDOFF.json), [static verifier](../experiments/verify_manual_overlay_handoff.py).


## FOLD-SLIDE-2D-001 — item 1 systematic row-plus-column overlay

- Date: 2026-10-23 UTC, original computation. Manifest start `2026-10-23T23:47:52.868636Z`, end `2026-10-23T23:49:19.600426Z`; job-level start/end are retained separately. Commit/publication times are not substituted.
- Type: inscription-layout comparison and whole-search chance calibration, not a cipher or plaintext-generation model. Item 1 only; items 2–8 not started.
- Frozen specification `f6aafc4735b8ff9e4f7e01975a97baf9991e1583`, validated implementation `0584bbc3340ce8a50a7fed3a53feaed202420c4f`, then original run. Later runner change adds execution-purpose metadata only, defaulting repeats to replay.
- Domain: both existing registrations, dx −33…+33, dy −28…+28, no wrapping and same-facing double reflection. 7,638 raw frames / 7,150 active; 134 prior row-zero frames reproduce exactly, 7,504 nonzero-row frames newly covered.
- Largest standardized label excess: 21/248 comparable pairs, dx=+19, dy=−7, primary registration. Whole-search tails 0.7475 shuffle / 0.7635 rotation. Area tails 0.6500 / 0.6090. All four-report adjusted p-values are 1. No unusual excess or cipher candidate.
- Controls: 1,999 full-selector draws per scheme, fixed original anchor/row histograms/punctuation/tableau; exact means and exact signed-rational ranking. Independent cell/pixel code checks all 7,638 frames and positions; 18 complete-selector toy plants and ambiguity/expectation/mutation controls precede evaluation.
- Complete positions: 57,674 label matches, 1,506,846 positive surrogate intersections. No lexical scoring or arbitrary extraction. Measured physical optics remain outside coverage.
- [Findings](FOLD-SLIDE-2D-FINDINGS.md), [frozen protocol](FOLD-SLIDE-2D-SPEC.md), [all-frame table](../results/FOLD-SLIDE-2D-001-frames.csv), [summary](../results/fold-slide-2d-001-runs/20261023T234752Z-ddb7425463b745a4b3d70b1b669dd641/summary.json), [manifest](../results/fold-slide-2d-001-runs/20261023T234752Z-ddb7425463b745a4b3d70b1b669dd641/manifest.json), [native implementation](../experiments/monument_slide_2d.py).
- The stale current SIGABA scope wording is corrected to COMPACT-018’s 12 and 14 synthetic controllers; historical zero-controller stages remain preserved. No new SIGABA/K4 joint search, Site deployment or subsequent item.

## PHYSICAL-SOLAR-002 — item 2 conditional sunlight, lamp geometry and evidence gates

- Original quantitative run start/end UTC: 2026-10-24T00:17:28.772639+00:00 / 2026-10-24T00:17:29.483736+00:00. This is not a source exposure time. Independent worker run times are unknown; separate local replay receipt records validation times.
- Kind: physical analytical constraints and source research; no K4 cipher evaluation.
- Frozen specification: `b2cc1dffdbb71b7a11c38f8041d220f3fce82932`; [protocol](PHYSICAL-SOLAR-002-SPEC.md), [findings](PHYSICAL-SOLAR-002-FINDINGS.md), [runner](../experiments/physical_solar_002.py), [complete receipt/output](../results/physical-solar-002/README.md).
- Scope: 96 declared solar-envelope scenarios including old exact-bearing baselines; 39 independently source-fixed calendar samples; 125 dimensionless height-order cases. 960,096 dense grid, 39 USNO/NOAA and 125 ray checks pass. No parameters fitted to K4.
- Outcome: conditional solar and direct-ray constraints verified. ENE Sun versus ENE ground shadow differ; a below-aperture source cannot directly project onto lower ground. Actual source/aperture/receiver heights and surveyed heading remain unknown. No source-fixed optical key, decoder or intended celestial time identified.
- Independent addition: [evidence/arithmetic package](../independent/2026-10-24/physical-item2/README.md), received with outcomes known and separately replayed. Finite solar disk, ideal thickness clipping and angular sensitivities verified; these are not measured installed blur/strokes. No original images/scrapes committed.
- Image feasibility: original LOC TIFF SHA verified and native crop inspected; same exposure as prior service image. No certified aperture-to-ground pairs established, no camera/light fit. Proposed 12-pair calibration remains unpassed. All broader physical/navigation hypotheses retain evidence-blocked status. Item 3 not started; no Site change.
- Aggregate validation: 497 tests pass on both supported Python versions; [validation receipt](../results/PHYSICAL-SOLAR-002-VALIDATION.json) records validation start/end separately from the original physical calculation.

## WORLD-CLOCK-003 — item 3 partial historical ring registration and phase identifiability

- Original analysis start/end UTC: 2026-10-24T00:29:46.751515+00:00 / 2026-10-24T00:29:46.860170+00:00. Historical exposure clock times remain unknown.
- Kind: conditional historical mapping/invariance analysis; no K4 cipher evaluation.
- Frozen protocol commit `53aa67b86da286d45012d957a25b4763c77ab04f`; [specification](WORLD-CLOCK-003-SPEC.md), [findings](WORLD-CLOCK-003-FINDINGS.md), [source](../experiments/world_clock_003.py), [complete original results/receipts](../results/world-clock-003/README.md).
- Selected fixed input: 41 labels/ten panels/three dated runs. Under explicitly unverified common-inventory continuity, 576 gauge-fixed offset pairs yield 240 compatible registrations and 336 exact rank conflicts. Retain all compatible layouts. No global compass registration or 1989 completeness inferred.
- 272 within-segment pair differences forced; all 548 cross-segment pairs remain ambiguous. Pair equations are dependent, not independent clues. All 24 integer phases over 240 layouts give 236,160 inverse checks; continuous physical phase is not enumerated. Separate photos have separate exposure phases. No semantic UTC offset or per-character city mapping assigned.
- Controls: 36 complete tiny-ring sets match independent direct unification; all 36 plants included; 117 rational phase/gauge cases and mutation checks pass. Old pilot exactly replayed in a temporary directory without overwriting original data/results.
- Separate prior evidence: corrected 1972 inscriptions and narrow 1989 labels are retained without an unsupported join. Broader clock/face hypotheses remain evidence-blocked for an actual cipher bridge and historical calibration. Fresh parent research is integrated separately: two dated arrangement discrepancies, five full May 1989 lower labels, explicitly post-1989 comparison and an undated removed plate. Original three-run input/results remain unchanged; no item 4 or Site change.
- Local engineering validation: 504 tests pass on Python 3.9 and 3.12; [separate validation receipt/logs](../results/WORLD-CLOCK-003-VALIDATION.json). That checkpoint preceded the final separately recorded source integration.
- Final evidence: [supplied report/inventory](../independent/2026-10-24/world-clock-item3/README.md), [independent local source checks](../sources/world-clock-003/LOCAL-SOURCE-REVIEW.json), [post-outcome analytical revision amendment](WORLD-CLOCK-003-SOURCE-AMENDMENT.md). Known dates are day/month/year precision as documented; unknown worker execution times remain unknown.
- Final source-integrated validation: 508 tests pass on both supported Python versions; [separate final receipt/logs](../results/WORLD-CLOCK-003-FINAL-VALIDATION.json). Unknown historical exposure times remain unknown.

## CSP889-COUPLED-024 — item 4 unknown-anchor collector inference and exact byte masks

- Kind: synthetic exact-solver engineering, not new K4 cryptanalysis. Original and corrective run timestamps are recorded separately in linked manifests and every child receipt; no historical exposure time is inferred.
- Frozen primary protocol `950ba4c`; [specification](SIGABA-UNKNOWN-ANCHOR-COLLECTOR-SPEC.md), [method/proof](SIGABA-UNKNOWN-ANCHOR-COLLECTOR-METHOD.md), [findings](SIGABA-UNKNOWN-ANCHOR-COLLECTOR-FINDINGS.md), [coupled implementation](../experiments/sigaba_unknown_anchor_collector.py). Twelve published simulator vectors remain controls, not hardware certification.
- Complete correctness: 70 original explicit graph comparisons/12 independent physical raw-key streams; 124 supplementary varying-input graph/controller checks/12 further raw-key streams, four genuinely varying fixtures. Byte masks match 9,743 small subset/translation cases and declared real boundary points. Prefix/gap, disconnected paths and deliberate resource controls pass.
- Original comparison [manifest](../results/sigaba-unknown-anchor-024/20261024T011347Z-0372961a832e4fefa3630289212ad464/manifest.json), [summary](../results/sigaba-unknown-anchor-024/20261024T011347Z-0372961a832e4fefa3630289212ad464/summary.json): fresh baseline completes 9/7 controllers, original integrated children hit the 65-second watchdog without native coverage/RSS. Preserve unknown, not zero.
- Correction [manifest](../results/sigaba-unknown-anchor-024b/20261024T012556Z-68fabf5fec944bdb82cd9971546c2a6e/manifest.json), [summary](../results/sigaba-unknown-anchor-024b/20261024T012556Z-68fabf5fec944bdb82cd9971546c2a6e/summary.json): exact byte-generated masks applied to BOTH backends, same fixtures/domains/caps; baseline completes 9/9, integrated 11/11 before wall limits. Each requests 11,881,376 controllers and all 66,058 reachable maps. Almost all remain unresolved.
- These first-eleven prefixes are contained in prior COMPACT-018 first-12/14 coverage; no new historical full-domain coverage or K4 inference. No real-sized gate pass, no claim of recovered plant from the full selector, and no statistical speedup/general SIGABA exclusion.
- Initial receipt bug and supplementary control assumption are preserved with [bounded diagnostic evidence](../results/sigaba-unknown-anchor-diagnostic/README.md). No new fixture or cache/time expansion after the byte-mask comparison. The proposed canonical support-signature reuse is unrun.
- Item 5 and public Site unchanged. Publication follows the later renewed owner approval; no denied transport workaround.
- Final validation: 519 tests pass on both supported Python versions; [separate UTC validation receipt/logs](../results/CSP889-COUPLED-024-VALIDATION.json). Original and corrected synthetic run windows remain in their manifests, not inferred from publication.

## LAMP-GREEK-025 — item 5 ordinal lamp labels and complete Greek codecs

- Kind: finite K4 model tests plus a support exclusion and synthetic complete-selector controls. No historical creator claim or Site change.
- Frozen specification `b19f89c` precedes actual comparison. [Protocol](LAMP-GREEK-025-SPEC.md), [findings](LAMP-GREEK-025-FINDINGS.md), [source](../experiments/lamp_greek.py), [original run/UTC manifest](../results/lamp-greek-025/README.md).
- Original controls start/end UTC: 2026-10-24T01:51:34.425418+00:00 / 2026-10-24T01:51:39.517632+00:00; actual selection 2026-10-24T01:51:39.584120+00:00 / 2026-10-24T01:51:39.593230+00:00. Null panel ends 2026-10-24T01:51:41.494966+00:00. These are computation timestamps, not publication or historical clock observations.
- Scope: two physical orders, ordinal lit-field sums, 1,440 starts, two indicator states, AZ/KRYPTOS and addition/true Beaufort. Letter and adjacent-pair roles each test 23,040 descriptions and fail first-crib constraints. Framed Greek role support-excludes 23,040 descriptions with zero phase simulation; no alignment assumption needed for that invariant.
- Results: no first-crib or Berlin-stage candidate; no full solution. All 199 histogram-shuffled whole-family controls also have zero first fits; descriptive baseline only, no significance claim.
- Controls: 5,760 display/order comparisons, 18,279 prefix-code string roundtrips, 702 rank inverses, 69,120 raw-model unrelated-message roundtrips, all 24 literal plants retained. One pair plant has two distinct all-crib-compatible plaintexts; preserve that ambiguity. Four framed plants have two descriptions/one plaintext.
- Separate [direct checker](../experiments/audit_lamp_greek.py) verifies complete candidate sets for 24 plants and K4, using independent row arithmetic and direct decoding; same-author implementation, not external blinded verification. [Validation receipt](../results/LAMP-GREEK-025-INDEPENDENT-VALIDATION.json); [finite phase/support certificates](../results/LAMP-GREEK-025-CERTIFICATES.json).
- The Greek frame expands the plant 97→104 tokens and computes clue offsets after full parsing; ordinal Greek labels are not phonetic Greek. Other mechanisms remain outside coverage. Stop before item 6.
- Final validation: 529 tests pass in both Python 3.9 and 3.12; [validation receipt and logs](../results/LAMP-GREEK-025-VALIDATION.json). No new documentation-link errors; no configured CI workflows.

## TREE-GEOMETRY-IPA-026 — item 6 dynamic topology, full-state feedback and pronunciation keys

- Kind: three finite exploratory model tests, synthetic complete-selector controls and historical qualification; no creator-use evidence or Site change.
- Frozen protocol `e35121c31d34c62c8f836d9169214f79d53de8b5`; [specification](TREE-GEOMETRY-IPA-026-SPEC.md), [findings](TREE-GEOMETRY-IPA-026-FINDINGS.md), [native code](../experiments/tree_geometry_ipa.py), [independent reference](../experiments/tree_geometry_ipa_reference.py).
- Exact scope: 104 bottom-up access-splay tree descriptions, 208 nonlinear 35-bit geometry feedback descriptions, 136 source-fixed IPA byte-key descriptions. All 448 full decryptions are distinct; no first-crib survivor, no Berlin-stage candidate. No arbitrary states/functions or general-family exclusion.
- Original completed controls start/end UTC: 2026-10-24T02:05:03.782641+00:00 / 2026-10-24T02:05:12.193005+00:00. Actual start/end 2026-10-24T02:05:12.193900+00:00 / 2026-10-24T02:05:12.247353+00:00. Whole-family nulls end 2026-10-24T02:05:23.118605+00:00. [Original and failed-control manifests](../results/tree-geometry-ipa-026/README.md) preserve separate chronology; no publication timestamp substitution.
- Controls: 1,792 fixed-model/reference message roundtrips, 24,336 tree permutation checks, 104 topology-change and 104 wrong-timing witnesses, 24 full-family plants with exact complete-reference candidate-set agreement and truth inclusion. All 199 histogram shuffles have zero first/all fits; descriptive only, no significance claim. Initial control attempt failed on reference rotation grouping before K4 and is preserved, not counted as a negative.
- Separate [post-outcome direct replay](../experiments/audit_tree_geometry_ipa.py) agrees on all actual model records and 1,040 geometry carry/boundary cases; [receipt](../results/TREE-GEOMETRY-IPA-026-INDEPENDENT-VALIDATION.json). Same-author independent implementation, not external blind verification.
- IPA output periods 18/16 exceed the older direct period 1–12 baseline, but UTF-8 was devised in 1992. This explicitly modern serialization is not a historical 1990 hypothesis or an IPA spelling inverse. Public clue phrases used as keys are not independent recovered evidence. No encoding retune, new dialect or item 7.
- Final aggregate validation: 538 tests pass on Python 3.9 and 3.12; [separate UTC receipt/logs](../results/TREE-GEOMETRY-IPA-026-VALIDATION.json). No configured CI workflow or new documentation-link errors.

## STRIP-SOURCE-GATES-027 — item 7 strip boundaries, historical QA and five source gates

- Kind: source-conditioned analytical exclusion, historical worked-example validation and explicit evidence-blocked mechanisms; no strip-key sweep or universal historical-family rejection.
- Frozen conditional protocol `0e6693e`; [specification](STRIP-SOURCE-GATES-027-SPEC.md), [findings](STRIP-SOURCE-GATES-027-FINDINGS.md), [conditional code](../experiments/strip_source_gates.py), [source QA](../experiments/item7_historical_source_qa.py), [source-data admission](../experiments/strip_inventory_admission.py), [row-candidate relation](../experiments/strip_row_candidates.py).
- Original controls start/end UTC: 2026-10-24T02:16:36.497919+00:00 / 2026-10-24T02:16:36.634250+00:00. Original conditional replay and post-source QA/replay times are separately retained in [receipts](../results/strip-source-gates-027/README.md); worker execution times are unknown. Publication time is not substituted.
- Direct nonzero valid-strip operation cannot self-encipher: first-crib S→S at 33 already rejects, with public K→K at 74 as explanatory additional evidence. SRH-366 printed 83–84 nonzero rule independently visually verified; changing strip sets/nonzero subgroup offsets does not evade it. Zero-column/outer-layer/preprocessing alternatives remain outside that proof.
- Separate zero-per-block relaxation: changed/fixed/changed at 32–34 rejects every width>=2 and registration. Finite widths 1..30/all origins have 465 bookkeeping descriptions, 464 contradictions, width 1 necessary-only pass. Prior M-94 width 25/origin 0 overlaps. No independent-search or global-novelty count.
- Controls: 872 toy permutations/29,366 symbol checks, 24 continuous synthetic plants, 11,160 independent block partitions. [Resource replay](../results/STRIP-SOURCE-GATES-027-ARITHMETIC-REPLAY.json) reproduces original payloads, peak 15,122,432 bytes; original peak was not recorded.
- Historical QA: original 1935 M-138 observed pairs reproduce +15 example; 24 complete rows validate, strip 1 O/Q literal fails complete-inventory gate without repair. Wheatstone REFERENCE→XZAABGQAM forward/inverse reproduces; conflicting printed XZZZBGQAM and unused ? slot retained. An explicitly inferred W completion is not pixel authentication. [Source QA receipt](../results/ITEM7-HISTORICAL-SOURCE-QA-027.json).
- [Supplied report/transcription/original script](../independent/2026-10-24/item7-historical-sources/README.md) preserved; original arithmetic adapter substitutes only output path and declared PDF metadata, not arithmetic. [Local source review](../results/ITEM7-LOCAL-SOURCE-REVIEW.json) distinguishes direct SRH visual inspection, NSA web text, worker pixels and failed downloads. No source 403 retry/alternate route.
- Complete authentic M-138-A issues, distinct Pletts rules, specific book extraction, Egyptian codec and German recovery/alignment remain source-gated. No invented model was run merely to fill those gaps, no Site change, stop before item 8.
- Final validation: 553 tests pass on Python 3.9 and 3.12; [UTC validation receipt/logs and preserved earlier documentation failure](../results/STRIP-SOURCE-GATES-027-VALIDATION.json). No new broken links or configured CI workflow.

## ONE-EDIT-028 — item 8 complete counterfactual edit robustness

- Kind: bounded exact cipher sensitivity, unrestricted-permutation ambiguity, necessary-certificate diagnostics and full-search controls; no assertion of K4 error or canonical change.
- [Frozen protocol](ONE-EDIT-028-SPEC.md) commit `786f864`; pre-scoring implementation/control fix `aef83ca`. [Findings](ONE-EDIT-028-FINDINGS.md), [eight-item summary](EIGHT-ITEM-INVESTIGATION-SUMMARY.md), [channel](../experiments/one_edit_channel.py), [exact models](../experiments/one_edit_models.py), [independent reference](../experiments/one_edit_reference.py), [all original results](../results/one-edit-028/README.md).
- Original UTC controls: 2026-10-24T03:00:31.710149+00:00 / 2026-10-24T03:00:50.610903+00:00; actual 2026-10-24T03:00:50.611166+00:00 / 2026-10-24T03:00:51.315755+00:00; nulls end 2026-10-24T03:01:06.353305+00:00. Post-audit/regression timestamps are separate, not publication times.
- Exact channel count: 5,071 raw descriptions (1 baseline, 2,425 substitutions, 2,548 missing-letter insertions, 97 extra-letter deletions), 4,968 latent strings, 6,317 complete (latent,mask) instances. Two explicit coordinate interpretations; 596 transport cases inadmissible without dropping any known letter. All 9,546 admitted raw alignment cases evaluated.
- Periodic scope: 48 same-coordinate AZ/KRYPTOS plus/true-Beaufort structures, unrestricted periods 1–12; 458,208 logical checks (303,216 unique instance checks), 41 raw first fits/29 unique records, zero complete fits. Every phase is fitted by the first 13 letters; no refit at Berlin. First-fit period 12 is guaranteed by at most one substitution, not a lead.
- Unrestricted permutations: 191 primary raw edits and 169 conditional transport cases fit the letter counts. Two arbitrary non-language witnesses/keys per compatible instance regenerate latent text and every aliased channel to canonical 97. Independent post-audit deduplicates 27 compact plaintext sets (25 primary), checks 351 pairs disjoint and counts the exact huge union. No historical route/error/English solution claim; original bounds unchanged.
- Diagnostics: nonzero-strip fixed-point contradiction survives all admitted cases. Wheatstone's necessary pair certificate is lost in 925 primary/51 transport cases; these are not fixed-ring keys or cipher fits. Other prior families were not silently included.
- Controls: all 5,071 tagged maps, 30 complete tiny edit sets, 24 tiny permutation and 96 tiny periodic truth sets, 144 independent fixed-model table checks, K1/K2 and 7 original offline convention controls. All 24 full-selector plants retain truth, 137,600 compatible representations and 1–3,827 plaintexts per plant preserved. No unique-recovery claim.
- Whole-search nulls: all 99 histogram shuffles have permutation repairs and periodic first fits; none has a full periodic fit. No partial-score promotion or positive significance claim. Lossless gzip avoids a preflight format cap without truncation; a pre-scoring summary-writer failure is preserved as incomplete, not a negative.
- [Independent actual solver/union/certificate audit](../results/ONE-EDIT-028-INDEPENDENT-AUDIT.json), [preflight](../results/one-edit-028-preflight/README.md). Canonical data unchanged; no Site change, no ninth investigation.

- Final item 8 aggregate validation: 568 tests pass on Python 3.9 and 3.12; [UTC receipt and complete logs](../results/ONE-EDIT-028-VALIDATION.json). All eight investigations are complete at their declared scope; [overview](EIGHT-ITEM-INVESTIGATION-SUMMARY.md). No ninth investigation or Site change.

## PROJECTION-CONCURRENCE-029 — synthetic image-ray validation and physical-data gate

- Date: 24 October 2026 UTC; separately authorized after the eight-item sequence, not a cipher search.
- Kind: synthetic geometric diagnostic, independent scalar checks and real-data admission protocol; zero certified monument pairs, real fits or K4 trials.
- [Preregistered protocol](PROJECTION-CONCURRENCE-029-SPEC.md), [findings](PROJECTION-CONCURRENCE-029-FINDINGS.md), [API/data contract](PROJECTION-CONCURRENCE-029-API.md), [native code](../experiments/projection_concurrence.py), [independent checks](../experiments/projection_concurrence_reference.py), [tests](../tests/test_projection_concurrence.py).
- Original corrected diagnostic UTC start/end:2026-10-24T11:50:23.445087+00:00 /2026-10-24T11:50:23.802297+00:00. [Complete fixtures/outputs](../results/PROJECTION-CONCURRENCE-029-SYNTHETIC.json): 24 uncertainty configurations, 21 evaluated and3 collapsed; finite/infinity/noisy positives pass, heldout/mixed-source negatives fail, coincident rays unidentifiable despite zero residual.
- Initial parallel/infinity QA misconception and undefined-training-ray gate error are preserved separately, corrected before any real fitting; no discarded points or threshold easing.
- Actual physical-data stage remains evidence-blocked. Line concurrence predicts only line incidence, not complete spot position or solar/time identity. [Source acquisition review](evidence/2026-10-24-projection-acquisition/PHOTO-ACQUISITION-REVIEW.md) and [local LOC check](evidence/2026-10-24-projection-acquisition/LOCAL-REVIEW.json) integrated: additional views/observation ROIs, still zero certified pairs; no synthetic success promoted to monument evidence.

- [Separately frozen local-control supplement](PROJECTION-CONCURRENCE-029-LOCAL-CONTROLS-SPEC.md) and [eleven complete outputs](../results/PROJECTION-CONCURRENCE-029-LOCAL-CONTROLS.json): small wrong picks and a correlated receiver shift can pass. This exposes conditional-gate limits; no tolerance retuning or real-data fit.

- Final regression:587 tests pass on Python3.9 and3.12; [separate UTC receipt/full logs](../results/PROJECTION-CONCURRENCE-029-VALIDATION.json). [Complete Python3.12 record replay](../results/PROJECTION-CONCURRENCE-029-PY312-REPLAY.json) agrees within declared1e-8 absolute/1e-9 relative tolerance. Real-data stage is evidence-blocked, not a monument negative.

## SITE-PROJECTION-030 — version16 source archive and publication provenance

- Date:24 October2026 UTC; source archival/integrity work only, not a new cipher or optical fit.
- [Archive/provenance](../docs/site-source/projection-20261024/README.md), [original manifest](../docs/site-source/projection-20261024/snapshot/HANDOFF_MANIFEST.json), [static verifier](../experiments/verify_projection_site_handoff.py), [local UTC receipt](../results/SITE-PROJECTION-20261024-SOURCE-HANDOFF.json).
- Native owner publication relayed by parent confirms public Site version16/source543634f866b74a778b7f1b4de58a4815237dcb2f, public access revision2 unchanged. Exact publication time unknown. Owner reports105 tests; rendered desktop/mobile QA unverified because Mac locked. Local archive step did not deploy or execute the handed-off JavaScript.
- All33 original ZIP entries safely inspected;31 source files match owner Git blobs and patch;8 fixtures and complete11-local-control payloads match research bytes. This is a partial source delta, not a complete runtime or independently rerun full Site suite.
- Original copied contract has8 repository-relative links in its two source copies; preserve exact bytes with explicit original-source link exceptions and working canonical links in the archive guide. No silent source repair. Zero real-photo fits or new K4 trials.

- Local aggregate archive regression:592 tests on Python3.9/3.12, [UTC receipt/logs](../results/SITE-PROJECTION-030-VALIDATION.json). Parent cloud review confirms version16 fixtures/controls/photo/export, with narrow QA-page encoding correction still pending source handoff; no corrected version is claimed archived.

## SITE-PROJECTION-031 — corrected version 17 source archive

- Date: 24 October 2026 UTC. Source archive integrity and publication provenance only; no new cipher or physical fit.
- [Current source guide](../docs/site-source/projection-v17-20261024/README.md), [original seven-file manifest](../docs/site-source/projection-v17-20261024/snapshot/HANDOFF_MANIFEST.json), [static verifier](../experiments/verify_projection_v17_handoff.py), [UTC handoff receipt](../results/SITE-PROJECTION-V17-SOURCE-HANDOFF.json).
- Parent-relayed native owner publication confirms version 17 live, source `2cb85a7714e12a627495f42dd3a7581c09b0b809`, public access revision 2 unchanged. Owner reports 107 tests; this full Site suite was not rerun here. Exact publication time unknown.
- Seven-file delta and 31-file full-feature ZIP match manifest hashes and source Git blobs. Full feature equals immutable version 16 source plus delta. Encoding/visible residual wording corrected; numerical core, fixtures, photo and export code unchanged.
- Parent cloud Chrome rendered QA passed targeted v17 fixes after earlier full eight-case/control/photo/export/390-and-768-iframe/fold checks. Not physical-device emulation or local Mac QA. No handed-off JavaScript executed or Site redeployed by archive integration.

- Final local aggregate regression: 595 tests pass on Python 3.9 and 3.12; [UTC receipt and full logs](../results/SITE-PROJECTION-V17-VALIDATION.json). Version 16 archive is unchanged; corrected version 17 is separately archived.

## SPELLING-CORRECTION-032 — deliberate spelling source-rule constraints

- Date: 24 October 2026 UTC. Local source-consistency/identifiability study; zero K4 trials, no push or Site edit.
- [Frozen protocol](SPELLING-CORRECTION-032-SPEC.md), [findings](SPELLING-CORRECTION-032-FINDINGS.md), [source/prior coverage](SPELLING-CORRECTION-032-SOURCES.md), [native code](../experiments/spelling_correction.py), [independent oracles](../experiments/spelling_correction_reference.py).
- Original run UTC start/end: 2026-10-24T13:18:35.633896+00:00 / 2026-10-24T13:18:35.659389+00:00; [full output and controls](../results/SPELLING-CORRECTION-032-ORIGINAL.json). Source retrieval/attribution and later regression times are separate.
- All minimal word alignments retain Q→L, U→O and uncertain K3 A→E plus inserted E. Uniform full-source letter functions fail; 624 invertible affine changed-site maps fail; keyboard/copy/permutation/vowel constraints fail. These are overlapping exact constraints, not independent statistical trials.
- All 42 repeated-mask phase descriptions fail on both complete primary texts (84 source applications). They are direct source-transformation diagnostics, not K4 keys or tests of every correction-derived outer cipher. No new trigger or key sweep follows.
- Independent controls: 394 tiny alignment sets, 436 function-count systems, 24 planted substitutions, 624 affine and 126 mask roundtrips; all pass. General contextual correction family remains evidence-blocked, not universally excluded.

- Final local validation: 608 tests pass on Python 3.9/3.12; [UTC receipt and full logs](../results/SPELLING-CORRECTION-032-VALIDATION.json), [complete cross-version replay](../results/SPELLING-CORRECTION-032-PY312-REPLAY.json). No new K4 trial or publication.

## COVER-EXTRACTION-033 — post-decryption word-cover and fixed-letter constraints

- Date: 24 October 2026 UTC. Local only, no push or Site change.
- [Frozen protocol](COVER-EXTRACTION-033-SPEC.md), [findings](COVER-EXTRACTION-033-FINDINGS.md), [sources](COVER-033-034-SOURCES.md), [native solver](../experiments/cover_extraction.py), [independent oracle](../experiments/cover_extraction_reference.py), [complete original receipt](../results/COVER-EXTRACTION-033-ORIGINAL.json).
- Original UTC start/end: 2026-10-24T13:55:39.526279+00:00 / 2026-10-24T13:55:39.790810+00:00. Strict NATO full unanchored lattice has zero covers. Four explicit custom dictionaries have huge exact cover counts; A30-ENE exact15 has 3,787,080 covers and necessary pattern ???ENE????BC???. No unknown text was decrypted.
- Four fixed letter positions and global N1/N2 schedules, both N2 phases; all feasible coverword counts and exact15 strata, 84 nonempty lanes. Selected short words fail, no counter reset or arbitrary per-word index. ENE versus EN is separate.
- Independent complete tiny languages, 252 real-sized fixed-message count checks and 21 synthetic Caesar roundtrip/recovery plants pass. Outer cipher/codebook supplied in controls; zero actual K4 cipher/key trials. [Cross-version replay](../results/COVER-EXTRACTION-PHRASE-PY312-REPLAY.json).

## COVER-PHRASE-034 — bounded Brown short-phrase feasibility and capacity controls

- Date: 24 October 2026 UTC. Local only, no push or Site change.
- [Frozen protocol](COVER-PHRASE-034-SPEC.md), [findings](COVER-PHRASE-034-FINDINGS.md), [source pins](../results/COVER-033-034-SOURCES.json), [runner](../experiments/run_cover_phrase.py), [original summary](../results/COVER-PHRASE-034-original-summary.json), [all matched references/counts](../results/COVER-PHRASE-034-original-windows.jsonl.gz), [all controls](../results/COVER-PHRASE-034-original-controls.json.gz).
- Original UTC start/end: 2026-10-24T14:01:20.542852+00:00 / 2026-10-24T14:01:29.259691+00:00. All 500 frozen Brown texts, 2,673,853 contiguous 2..5-word windows, 1,771,338 eligible occurrences and 1,335,926 distinct joined strings processed. No arbitrary word-product generation.
- All-word initials have zero matches. Exact15/all-word readout has zero for all k; every-other-word cases may produce 7/8-letter output. General family has 6,358 matched occurrence references, 3,139 joined strings / 3,147 spaced strings, mostly N2. These are compatibility counts, not recovered messages or keys.
- Six deterministic eligible synthetic plants re-encrypt full97 letters; no missing exact15 ENE plant invented. Whole-family 31 capacity draws: 24 dictionary-splittable, zero contiguous-bank matches. Not an observed K4 significance test. [Independent positive-count audit](../results/COVER-PHRASE-034-INDEPENDENT-AUDIT.json) verifies 7,266 message/lane counts; complete tiny negative controls and exact Python3.12 replay retained. No claim of a second exhaustive corpus false-negative implementation.

- Final aggregate local validation for COVER-033/034: 625 tests pass on Python3.9/3.12; [separate UTC receipt/full logs](../results/COVER-033-034-VALIDATION.json). Canonical ciphertext unchanged, no push or Site change.

## PROSE-COVER-035 — length-free ordinary lexicons and complete minimum-free autokey domain

- Date:24 October2026 UTC. New local-only test, prior033/034 preserved.
- [Frozen protocol](PROSE-COVER-035-SPEC.md), [findings](PROSE-COVER-035-FINDINGS.md), [native solver](../experiments/prose_cover.py), [runner](../experiments/run_prose_cover.py), [independent implementation](../experiments/audit_prose_cover.py), [original full receipt](../results/PROSE-COVER-035-ORIGINAL.json).
- Original UTC start/end:2026-10-24T14:41:14.223979+00:00 /2026-10-24T14:41:22.639303+00:00. Three fixed Brown-derived lexicons, no forced crib boundaries or15-word limit,36 selector distributions, cover paths span7–79 words. Counts are segmentation descriptions, not typical prose or unique messages.
- Complete lag27 plaintext-autokey minimum-free domain: six AZ/KRYPTOS/equation structures ×26^3 =105,456 descriptions; zero complete lexical covers, hence no actual candidate enters second-stage extraction. Vocabulary-conditioned negative; not an extraction or broad autokey exclusion.
- Six97-letter source plants retained, lexical solutions1/4/1/1/12/3;31 identical-search conditional shuffles each105,456 settings, all zero. Full97-letter re-encryption and exact ambiguity retained. K1–K3 calibration demonstrates false-negative/infinite-language limits: even augmented lexicon rejects genuine K3, so no broad English exclusion.
- [Complete independent actual-domain sets/negative replay](../results/PROSE-COVER-035-INDEPENDENT-AUDIT.json), [full Python3.12 semantic equality](../results/PROSE-COVER-035-PY312-COMPARISON.json), [interrupted verification note](../results/PROSE-COVER-035-VERIFICATION-NOTES.json). No corpus phrase selection, arbitrary97-letter key, publication or Site change.

- Final local validation: 638 tests pass on Python3.9/3.12; [UTC receipt/full logs](../results/PROSE-COVER-035-VALIDATION.json). Earlier033/034 reports/receipts unchanged, no publication or Site change.

## CURVED-SAMPLER-036 — ideal mirror feasibility, sensitivity and source gate

- Date: 24 October 2026 UTC; synthetic horizontal-table sampler only, no actual K4 fit or publication.
- [Frozen protocol](CURVED-SAMPLER-036-SPEC.md), [findings](CURVED-SAMPLER-036-FINDINGS.md), [API](CURVED-SAMPLER-036-API.md), [full summary](../results/CURVED-SAMPLER-036-SUMMARY.json), [lossless original](../results/CURVED-SAMPLER-036-ORIGINAL.json.gz), [all poses](../results/CURVED-SAMPLER-036-poses.jsonl.gz).
- Original UTC start/end: 2026-10-24T15:02:42.758132+00:00 / 2026-10-24T15:02:55.969582+00:00. 560 optical settings, 419 complete/141 invalid footprints, 45,252 table poses, 54 nominal 97-cell keys. Four utility cases (82–83 cells/all 26 letters) fail assembly/pupil benchmark; 50 lower-density complete cases not stability-tested. No continuous-domain exclusion.
- [Independent 54,320-ray validation](../results/CURVED-SAMPLER-036-RAY-VALIDATION.json), [independent 4,389,444-cell audit](../results/CURVED-SAMPLER-036-INDEPENDENT-CELL-AUDIT.json), [full Python3.12 comparison](../results/CURVED-SAMPLER-036-PY312-COMPARISON.json): discrete exact, floats within 1e-9 absolute.
- Supplied four-key panel:all 4 plants recovered,13 known letters leave 2 classes and 11 held-out retain 1; 31 synthetic whole-family nulls maximum 5/24, zero full matches. Not continuous geometry recovery or real K4 significance.
- [Site fixtures](../results/CURVED-SAMPLER-036-SITE-FIXTURES.json) and [read-only Site contract comparison](../results/CURVED-SAMPLER-036-SITE-CONTRACT-COMPARISON.json). Site vertical tableau is different from research horizontal table; no Site test/deployment/source archive performed here. Physical replica, glyph/reflectance/pupil realism and independent K4 geometry rationale remain unresolved.

- Final local aggregate validation: 651 tests pass on Python3.9/3.12; [UTC receipt/full logs](../results/CURVED-SAMPLER-036-VALIDATION.json). No actual K4 fit, repository publication, Site edit or owner-source archive by this task.

## SITE-CYLINDER-037 — exact vertical Site replay and physical-scale sensitivity

- Date: 24 October 2026 UTC. Local exact-source optical validation, not actual K4 or Site UI/publication work.
- [Frozen protocol](SITE-CYLINDER-037-SPEC.md), [findings](SITE-CYLINDER-037-FINDINGS.md), [summary](../results/SITE-CYLINDER-037-SUMMARY.json), [all default margins](../results/SITE-CYLINDER-037-DEFAULT-MARGINS.csv), [numeric source snapshot](../results/SITE-CYLINDER-037-SOURCE-SNAPSHOT.json.gz), [complete original](../results/SITE-CYLINDER-037-ORIGINAL.json.gz).
- Original computation UTC start/end: 2026-10-24T15:28:59.235487+00:00 / 2026-10-24T15:29:03.878526+00:00; final archive-write resources separate. Pinned inspected Site core5b7e883, same vertical-tableau contract. Independent485fixture and70713neighbor sample comparisons agree to1e-9; default97valid, minmargin0.017841939pitch at25/56/87.
- Frozen729neighbors:441complete,186same default key,11keys. Baseline plus10margin-ranked states:22state/scale cases,all full assembly panels fail; tiny pupil10/11U100 and11/11R250 pass, human-scale0/22. Other430complete states not full stability-tested. All3564configurations/per-cell outputs retained; no probabilities or continuous exclusion.
- [Complete semantic replay](../results/SITE-CYLINDER-037-PY312-COMPARISON.json), [whole-process streaming resource receipt](../results/SITE-CYLINDER-037-RESOURCE-REPLAY.json): unchanged geometry, full data, peak356155392bytes/4.65seconds on measured replay. Original pre-serialization RSS does not claim final write peak.
- Actual copper and horizontal036 remain distinct. No Site source copied/edited/archived; read-only inspected math/data executed to snapshot factual outputs. No repository push, paid check or actual K4 candidate.

- Final local aggregate validation: 665 tests pass on Python3.9/3.12; [UTC receipt/full logs](../results/SITE-CYLINDER-037-VALIDATION.json). Prior036 preserved, no actual K4 comparison or Source edit/archive/publication.

## COVER-SELECTOR-038 — boundary-free selector follow-through

- Date: 2026-10-24 UTC.
- Actual original calculation start: `2026-10-24T17:02:06.639063+00:00`; end: `2026-10-24T17:02:08.592232+00:00`. These are receipt values, not commit/publication times.
- Scope/result: 120 selector descriptions complete; 84 newstride descriptions, no outer cipher identified. General family limits remain explicit.
- [Findings/protocol/control links](COVER-SELECTOR-038-FINDINGS.md); [original receipt](../results/COVER-SELECTOR-038-ORIGINAL.json); [seven-family matrix](SEVEN-FAMILY-REVIEW-046.md).
- New results are local-only; no Site or canonical ciphertext change. Original/replay/control times are distinct.

## CONTEXT-SPELLING-039 — reversible context prediction limits

- Date: 2026-10-24 UTC.
- Actual original calculation start: `2026-10-24T17:05:27.894998+00:00`; end: `2026-10-24T17:05:27.957067+00:00`. These are receipt values, not commit/publication times.
- Scope/result: One-letter contexts fail; two-letter fits are underdetermined and predict no held-out mistake. General family limits remain explicit.
- [Findings/protocol/control links](CONTEXT-SPELLING-039-FINDINGS.md); [original receipt](../results/CONTEXT-SPELLING-039-ORIGINAL.json); [seven-family matrix](SEVEN-FAMILY-REVIEW-046.md).
- New results are local-only; no Site or canonical ciphertext change. Original/replay/control times are distinct.

## PHYSICAL-IDENTIFIABILITY-040 — source ambiguity and scale

- Date: 2026-10-24 UTC.
- Actual original calculation start: `2026-10-24T17:09:08.890519+00:00`; end: `2026-10-24T17:09:09.091089+00:00`. These are receipt values, not commit/publication times.
- Scope/result: Identical image pairs admit different physical sources; real reviewed pairs remain uncertified. General family limits remain explicit.
- [Findings/protocol/control links](PHYSICAL-IDENTIFIABILITY-040-FINDINGS.md); [original receipt](../results/PHYSICAL-IDENTIFIABILITY-040-ORIGINAL.json); [seven-family matrix](SEVEN-FAMILY-REVIEW-046.md).
- New results are local-only; no Site or canonical ciphertext change. Original/replay/control times are distinct.

## SIGABA-SUPPORT-SIGNATURE-041 — exact memoization without scaling gain

- Date: 2026-10-24 UTC.
- Actual original calculation start: `2026-10-24T17:15:25.791070+00:00`; end: `2026-10-24T17:19:26.330832+00:00`. These are receipt values, not commit/publication times.
- Scope/result: Exact tiny sets pass; real synthetic prefixes have zero cache hits and remain unresolved. General family limits remain explicit.
- [Findings/protocol/control links](SIGABA-SUPPORT-SIGNATURE-041-FINDINGS.md); [original receipt](../results/SIGABA-SUPPORT-SIGNATURE-041-SUMMARY.json); [seven-family matrix](SEVEN-FAMILY-REVIEW-046.md).
- New results are local-only; no Site or canonical ciphertext change. Original/replay/control times are distinct.

## CLOCK-CIVIL-042 — whole-year shared-phase interpretation

- Date: 2026-10-24 UTC.
- Actual original calculation start: `2026-10-24T18:27:33.660889+00:00`; end: `2026-10-24T18:27:33.928489+00:00`. These are receipt values, not commit/publication times.
- Scope/result: Automatic civil-time interpretation fails; literal/standard-time/single-date models remain open. General family limits remain explicit.
- [Findings/protocol/control links](CLOCK-CIVIL-042-FINDINGS.md); [original receipt](../results/CLOCK-CIVIL-042-ORIGINAL.json); [seven-family matrix](SEVEN-FAMILY-REVIEW-046.md).
- New results are local-only; no Site or canonical ciphertext change. Original/replay/control times are distinct.

## COMPRESS-TRANSPORT-043 — legacy compression with fixed transports

- Date: 2026-10-24 UTC.
- Actual original calculation start: `2026-10-24T18:35:43.988050+00:00`; end: `2026-10-24T18:35:44.455127+00:00`. These are receipt values, not commit/publication times.
- Scope/result: All 8 fixed.Ztransports fail magic; other compressors/transports/layers remain untested. General family limits remain explicit.
- [Findings/protocol/control links](COMPRESS-TRANSPORT-043-FINDINGS.md); [original receipt](../results/COMPRESS-TRANSPORT-043-ORIGINAL.json); [seven-family matrix](SEVEN-FAMILY-REVIEW-046.md).
- New results are local-only; no Site or canonical ciphertext change. Original/replay/control times are distinct.

## MINIMUM-REPAIR-044 — exact multi-substitution distances

- Date: 2026-10-24 UTC.
- Actual original calculation start: `2026-10-24T18:41:58.298226+00:00`; end: `2026-10-24T18:41:58.732664+00:00`. These are receipt values, not commit/publication times.
- Scope/result: 1536 minimum profiles complete; no observed error or English plaintext identified. General family limits remain explicit.
- [Findings/protocol/control links](MINIMUM-REPAIR-044-FINDINGS.md); [original receipt](../results/MINIMUM-REPAIR-044-ORIGINAL.json); [seven-family matrix](SEVEN-FAMILY-REVIEW-046.md).
- New results are local-only; no Site or canonical ciphertext change. Original/replay/control times are distinct.

## COVER-LANGUAGE-045 — non-veto language calibration and source-rule review

- Date: 2026-10-24 UTC.
- Actual original calculation start: `2026-10-24T18:49:48.099574+00:00`; end: `2026-10-24T18:50:32.936437+00:00`. These are receipt values, not commit/publication times.
- Scope/result: K3 retained; 5 of 6 plants rank first; 2 of 7 matched null maxima equal/exceed actual; no positive identification. General family limits remain explicit.
- [Findings/protocol/control links](COVER-LANGUAGE-045-FINDINGS.md); [original receipt](../results/COVER-LANGUAGE-045-ORIGINAL.json); [seven-family matrix](SEVEN-FAMILY-REVIEW-046.md).
- New results are local-only; no Site or canonical ciphertext change. Original/replay/control times are distinct.
- Separate [late 038 control](../results/REVIEW-CONTROLS-045.json) and [memoryless length-changing spelling review](SPELLING-MORPHISM-REVIEW-045-FINDINGS.md) preserve original chronology; neither is a new ciphertext domain.

## REVIEW-CONTROLS-046 — explicit independent review corrections

- Date: 2026-10-24 UTC.
- Actual original calculation start: `2026-10-24T18:55:29.101871+00:00`; end: `2026-10-24T18:55:29.116792+00:00`. These are receipt values, not commit/publication times.
- Scope/result: Active-root interruption, wrong-DST calculation and invalidflags pass; original runs unchanged. General family limits remain explicit.
- [Findings/protocol/control links](REVIEW-CONTROLS-046.md); [original receipt](../results/REVIEW-CONTROLS-046.json); [seven-family matrix](SEVEN-FAMILY-REVIEW-046.md).
- New results are local-only; no Site or canonical ciphertext change. Original/replay/control times are distinct.

## PHOTO-NATIVE-047 — bounded native LOC correspondence admission

- Date: 2026-10-24 UTC. Frozen protocol saved at `2026-10-24T19:17:13.787510+00:00`; native inspection finished at `2026-10-24T19:19:56.054606+00:00`. Validation/replay times are separate.
- Scope: one verified 3384 × 4283 LOC exposure, initial 800 × 800 ROI plus eight native crops; ten rejected bright-feature boxes. Zero certified material-point pairs, no geometric fit and no K4 evaluation. This is bounded manual failure to establish identities, not proof the photo can never yield them.
- [Findings](PHOTO-NATIVE-047-FINDINGS.md); [frozen protocol](PHOTO-NATIVE-047-SPEC.md); [native crops/transforms/annotations](evidence/2026-10-24-native-loc/README.md); [exact crop check](../results/PHOTO-NATIVE-047-CROP-CHECK.json); [validation](../results/PHOTO-NATIVE-047-VALIDATION.json). Local only.

## CANDIDATE-FIRST-048 — exact source-key preflight before message generation

- Date: 2026-10-24 UTC. Original calculation started `2026-10-24T19:40:49.963515+00:00`, finished `2026-10-24T19:40:52.486912+00:00`. Replay and regression timings are separate.
- Result/scope: 582 models;42 free-key survivors, zeroBrown source-key/97 letter plaintext matches; conditional bank omitted. No global family exclusion.
- [Findings](CANDIDATE-FIRST-048-FINDINGS.md); [frozen protocol](CANDIDATE-FIRST-048-SPEC.md); [original receipt](../results/CANDIDATE-FIRST-048-ORIGINAL.json); [full Python 3.12 replay](../results/CANDIDATE-FIRST-048-REPLAY.json); [shared replay/resource verification](../results/048-050-REPLAY-VALIDATION.json); [prior coverage](048-050-PRIOR-COVERAGE.md). Local only; no paid verifier, Site edit or push.

## ENE-ROUTE-049 — literal and digital ENE with fixed arithmetic

- Date: 2026-10-24 UTC. Original calculation started `2026-10-24T19:45:19.185573+00:00`, finished `2026-10-24T19:45:36.969399+00:00`. Replay and regression timings are separate.
- Result/scope: 56,454 descriptions/34,569 routes/656,811 fixed cases; zero 24 letter hits; actual/null maxima 8 versus 7–8. No global family exclusion.
- [Findings](ENE-ROUTE-049-FINDINGS.md); [frozen protocol](ENE-ROUTE-049-SPEC.md); [original receipt](../results/ENE-ROUTE-049-ORIGINAL.json); [full Python 3.12 replay](../results/ENE-ROUTE-049-REPLAY.json); [shared replay/resource verification](../results/048-050-REPLAY-VALIDATION.json); [prior coverage](048-050-PRIOR-COVERAGE.md). Local only; no paid verifier, Site edit or push.

## HAND-GRAMMAR-050 — complete fixed-key hand-operation grammar

- Date: 2026-10-24 UTC. Original calculation started `2026-10-24T19:49:16.853596+00:00`, finished `2026-10-24T19:49:24.990209+00:00`. Replay and regression timings are separate.
- Result/scope: 56,355 depth 0–3 descriptions/27,323 operators; no 24 letter hit; maximum 7 versus null 6–8; keys/widths fixed. No global family exclusion.
- [Findings](HAND-GRAMMAR-050-FINDINGS.md); [frozen protocol](HAND-GRAMMAR-050-SPEC.md); [original receipt](../results/HAND-GRAMMAR-050-ORIGINAL.json); [full Python 3.12 replay](../results/HAND-GRAMMAR-050-REPLAY.json); [shared replay/resource verification](../results/048-050-REPLAY-VALIDATION.json); [prior coverage](048-050-PRIOR-COVERAGE.md). Local only; no paid verifier, Site edit or push.

## CONTROL-CORRECTION-048-049 — actual lookup, returned witnesses and prior profiles

- Date: 2026-10-24 UTC. Corrected 048 calculation: `2026-10-24T20:11:28.873110+00:00` to `2026-10-24T20:13:08.724291+00:00`; corrected 049 calculation: `2026-10-24T20:13:49.930304+00:00` to `2026-10-24T20:14:07.042196+00:00`. Scientific replay and regression UTCs are separate.
- Scope/result: all 24 full-source lookup plants, six actual returned-hit witnesses and 576 prior-profile comparisons pass. All original actual/null payloads and model domains remain unchanged; no candidate bank or new family.
- [Correction/provenance](048-049-CONTROL-CORRECTION.md); [048 current receipt](../results/CANDIDATE-FIRST-048-CONTROLLED.json); [049 current receipt](../results/ENE-ROUTE-049-CONTROLLED.json); [replay validation](../results/048-049-CONTROL-CORRECTION-REPLAY.json); [new regression](../results/048-049-CONTROL-CORRECTION-VALIDATION.json). Local only.

## CANDIDATE-FIRST-051 — frozen 32-message structural-key pilot

- Date: 2026-10-25 UTC; target-receipt instant `2026-10-25T01:50:50.322793+00:00` is not asserted to be calculation start/end.
- Scope: 32 blinded 97-letter messages, 12 AZ/KRYPTOS tableaux, periodic/plaintext-autokey/ciphertext-autokey lengths 1–32; 1,152 descriptions per message, 1,999 full-search conditional nulls.
- Result: Completed narrow negative: all three gates fail; conditional saving −8.879 bits, p=.916, margin .570 bits. No exact structural fit. Its scientific expansion gate failed; separately authorized 052 does not change that outcome.
- Evidence: [report and reproduction instructions](candidate-first-051/README.md); [target result/report](candidate-first-051/results/target_summary.json); [independent target audit](candidate-first-051/results/target_audit.json).
- Status/next action: completed and published; consult the [current working queue](HYPOTHESES.md) before selecting another experiment. This reconciliation ran no cryptanalysis and changed no frozen payload.

## CANDIDATE-FIRST-052 — separately authorized 1024-message structural-key expansion

- Date: 2026-10-25 UTC; target-receipt instant `2026-10-25T02:34:02.434593+00:00` is not asserted to be calculation start/end.
- Scope: 1,024 new frozen 97-letter messages, 12 tableaux and periodic/plaintext-autokey/ciphertext-autokey lengths 1–32; 1,179,648 descriptions per target maximum, 1,999 matched null maxima.
- Result: Completed narrow negative: all three gates fail; saving −7.420649 bits, p=.519, margin 1.262599 bits. No exact structural fit. Standalone exploratory calibration is not project-wide error control. Compact archive intentionally omits the 84 bulky raw control receipts and retains their inventories/reproduction instructions.
- Evidence: [report and reproduction instructions](candidate-first-052/README.md); [target result/report](candidate-first-052/results/target_summary.json); [independent target audit](candidate-first-052/results/target_audit.json).
- Status/next action: completed and published; consult the [current working queue](HYPOTHESES.md) before selecting another experiment. This reconciliation ran no cryptanalysis and changed no frozen payload.

## CANDIDATE-FIRST-053 — fixed-bank ordinary-language running-key test

- Date: 2026-10-25 UTC; audit recorded `2026-10-25T03:38:57.147537+00:00`, not calculation start/end.
- Scope: 1,024 frozen messages × 12 tableaux; frozen order-4 character language model of induced keys; 1,999 full-search conditional null maxima.
- Result: Completed narrow negative: all four criteria fail (M=−237.145512 bits, p=.932, different-plaintext margin 3.218139 bits, full-key entropy 8.272177 bits/letter). No open-vocabulary joint plaintext/key decoder was implemented. Exact re-encryption with an unrestricted induced key is not evidence for a message.
- Evidence: [report and reproduction instructions](candidate-first-053/README.md); [target result/report](candidate-first-053/results/target_result.json); [independent target audit](candidate-first-053/results/target_audit.json).
- Status/next action: completed and published; consult the [current working queue](HYPOTHESES.md) before selecting another experiment. This reconciliation ran no cryptanalysis and changed no frozen payload.

## CANDIDATE-FIRST-054 — exact crib-derived running-key source lookup

- Date: 2026-10-25 UTC; audit recorded `2026-10-25T04:24:50.562963+00:00`, not calculation start/end.
- Scope: 89 documents, 17,619,191 eligible file-contained 97-letter windows, 12 fixed tableaux; forced 13/11-letter fragments start 42 letters apart; no candidate-message bank.
- Result: Completed exact bounded corpus exclusion: zero first-fragment occurrences, valid pairs or full source windows in 1,068 document/model searches. Other sources, editions, normalization and layers remain outside scope; no approximate search or expansion followed.
- Evidence: [report and reproduction instructions](candidate-first-054/README.md); [target result/report](candidate-first-054/results/target_result.json); [independent target audit](candidate-first-054/results/target_audit.json).
- Status/next action: completed and published; consult the [current working queue](HYPOTHESES.md) before selecting another experiment. This reconciliation ran no cryptanalysis and changed no frozen payload.

## CANDIDATE-FIRST-055 — calibrated forced-fragment English-key screen

- Date: 2026-10-31 UTC; historical report and archived receipts distinguish calibration, target and audit times.
- Scope: 12 fixed direct aligned tableaux, independently scored 13+11-letter key fragments, unchanged 053 order-4 model; no fabricated context across the 29-letter gap.
- Result: Completed heuristic screen negative: all 17 calibration gates pass; 0/12 target pairs survive threshold −4.385648037504633 bits/letter; best −7.992896749427596. Source clustering and weak semantic discrimination remain limitations. Stop the direct English-key decoder under this screen; no impossibility claim and no decoder launched.
- Evidence: [report and reproduction instructions](candidate-first-055/README.md); [target result/report](candidate-first-055/REPORT.md); [independent target audit](candidate-first-055/TARGET-AUDIT.md).
- Status/next action: completed and published; consult the [current working queue](HYPOTHESES.md) before selecting another experiment. This reconciliation ran no cryptanalysis and changed no frozen payload.

## CANDIDATE-FIRST-056 — joint periodic-key and free-column-order constraints

- Date: 2026-10-31 UTC; target report and archived original/corrected receipts retain exact calculation/audit chronology.
- Scope: Standard A–Z Vigenère, unrestricted nominal periods 2–8, then row-filled unpadded ragged columnar transposition widths 6–9, all emission orders/top-down reads, fixed alignment and 24 literal cribs.
- Result: Completed exact bounded exclusion: selected S and independent reference return complete empty sets; reference covers 408,960 routes × 7 periods = 2,862,720 trials. Fresh corrected 256-case benchmark passes before target; S gives 17.33× inclusive-CPU speedup over enumeration but no material advantage over simpler P. Learned-conflict L fails its separate benefit gate. Original resource-monitor defect, resource-only repair and fresh holdout are retained; numerical-only original results were not used to authorize target.
- Evidence: [report and reproduction instructions](candidate-first-056/README.md); [target result/report](candidate-first-056/TARGET-REPORT.md); [independent target audit](candidate-first-056/TARGET-AUDIT.md).
- Status/next action: completed and published; consult the [current working queue](HYPOTHESES.md) before selecting another experiment. This reconciliation ran no cryptanalysis and changed no frozen payload.

## CANDIDATE-FIRST-057 — alphabet-role and Beaufort free-column extensions

- Date: 2026-10-31 UTC. Both blind outputs sealed at 11:53:30.141875 UTC before answer analysis; parent target stage approved at 11:55 UTC. Target and resource receipts retain chronology; no commit time is asserted as run time.
- Scope: AZ/KRYPTOS plaintext and ciphertext alphabet roles, sign ±, arbitrary nominal periodic keys 2–8, then unpadded ragged columnar widths 6–9 and every column order. Eight conventions include 056 baseline; variant-Beaufort, phase, period and zero-key identity aliases are not counted as new operators.
- Result: Completed exact bounded exclusion: both production and independent reference return UNSAT_COMPLETE, zero compatible descriptions/operators/plaintexts. Reference completed 22,901,760 route/period/convention trials, including 2,862,720 baseline trials. Blind benchmark: 520/520 complete exact-set agreement, 464/464 plants included, 221/224 uniform and 224/224 literal-clue positives unique, 0/56 random controls fit. Three ambiguous positives retained.
- Evidence: [report and archive](candidate-first-057/README.md), [frozen protocol](candidate-first-057/PROTOCOL.md), [independent benchmark audit](candidate-first-057/BENCHMARK-AUDIT.json), [target audit](candidate-first-057/TARGET-AUDIT.md).
- Status/next action: scientific execution and audit complete; artifacts published. Q-01 closes only within these bounds. Reconciled [working ledger](HYPOTHESES.md) selects Q-02 reverse stage order for its own protocol and controls; at that closeout, no 058 target run had occurred. No Site change or paid submission.

## CANDIDATE-FIRST-058 — reverse-stage columnar and periodic-key cylinders

- Date: 2026-10-31 UTC. Blind outputs sealed at 12:21:03.520988 UTC before answer analysis; parent target stage approved at 12:22 UTC. Original receipts distinguish execution, audit and publication.
- Scope: Unpadded ragged columnar transposition first, all column orders and widths 6–9, followed by output-index arithmetic under eight AZ/KRYPTOS alphabet-role/sign conventions and arbitrary nominal periods 2–8. Complete compatible key cylinders retain free residues. No guessed English or sum of overlapping cylinders as a distinct count.
- Result: Completed exact bounded exclusion: both target engines return UNSAT_COMPLETE, zero cylinders/operators/plaintexts; reference 22,901,760 descriptive trials. All 520 blind complete cylinder/projection sets agree, all 464 plants included, 0/56 random fits. Unique plaintext counts 156/224 uniform and 150/224 literal are descriptive only. The unsound conditional uniqueness gate was removed before blind generation; superseded draft and decision retained.
- Evidence: [report and complete archive](candidate-first-058/README.md), [frozen protocol](candidate-first-058/PROTOCOL.md), [independent benchmark audit](candidate-first-058/BENCHMARK-AUDIT.json), [target audit](candidate-first-058/TARGET-AUDIT.md).
- Status/next action: execution and independent audit complete; artifacts published. Reconciled [working ledger](HYPOTHESES.md) closes Q-02 only for this scope and selects Q-03 feedback composites for separate preparation. At that closeout, no 059 target run had occurred.

## CANDIDATE-FIRST-059 — short-primer feedback before free column order

- Date: 2026-10-31 UTC. Blind outputs sealed at 13:00:56.363936 UTC before answer analysis; parent target approval at 13:02 UTC. Resource receipts retain measured CPU/wall durations, not inferred commit-time run timestamps.
- Scope: Eight AZ/KRYPTOS plaintext/intermediate-ciphertext role/sign conventions; feedback coefficient +1 only; plaintext or intermediate-ciphertext autokey, arbitrary primers 1–8, followed by unpadded ragged-columnar widths 6–9/all orders. Subtractive feedback is distinct and explicitly untested.
- Result: Completed exact bounded exclusion; both target engines return zero compatible primer cylinders/UNSAT_COMPLETE. Independent reference exhausts 52,346,880 descriptive trials. Blind feasibility/ambiguity benchmark: 600 complete independent cylinder/projection agreements, 544 plants, all 272 ciphertext-feedback plants correctly MULTIPLE, 0/56 random fits. Unique recovery descriptive only: plaintext-feedback primary plants 127/128 uniform and 128/128 literal; all ciphertext-feedback primers remain free.
- Evidence: [report/archive](candidate-first-059/README.md), [frozen protocol](candidate-first-059/PROTOCOL.md), [independent benchmark audit](candidate-first-059/BENCHMARK-AUDIT.json), [target audit](candidate-first-059/TARGET-AUDIT.md).
- Status/next action: scientific execution and audit complete; artifacts published. Q-03 closes only for this pilot. Q-04 and Q-05 not run because no production-search or surviving-candidate ranking bottleneck was established. No further model expanded, Site changed or paid submission made.

## CANDIDATE-FIRST-060 — two ciphertext-driven evolving-alphabet rules

- Date: 2026-10-31 UTC; parent target approval 15:13:41 UTC, final independent audit 15:15:09 UTC. Measured durations are in retained resource receipts.
- Scope: AZ/KRYPTOS reference and initial mutable alphabets; exchange with 26 initial pointers, or fixed-reference-index prefix reversal with 26 constant offsets. Two fixed 104-configuration arms; all 208 functions proven distinct by 21,528 separating witnesses. No resets, free alphabets, additional layers or post-failure changes.
- Result: Both independent target engines UNSAT_COMPLETE: zero compatible descriptions/plaintexts. Exact bounded exclusion only, not all evolving-alphabet ciphers. Canonical ciphertext SHA256 `eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab`.
- Validation: 5,832 tiny forward/inverse cases and 6,561 complete tiny solution sets; 480/480 blind complete-set agreements, 416/416 unique plants, 0/64 matched random fits. Benchmark manifest SHA256 `6e825558692b49bcb1b41cc11cec86d217e56c174a0c2c28867fe7bf6dbc6439`. Two target runs together used 0.10484779 CPU seconds; final audit ran no extra target search.
- Evidence: [Findings, frozen protocol, complete source/raw data, receipts and independent audits](candidate-first-060/README.md). Fresh public comparisons are preserved in the [proposal archive](fresh-program-20261031/README.md).
- Method improvement: Retain independent tiny truth-set and pairwise separating-witness tooling. No production bottleneck was observed; no stochastic/neural replacement justified. Future changes require fresh controls, not reuse of revealed holdouts.
- Status/next action: Execution and independent audit complete; artifacts published. Reconcile local/external ledgers and generated views, then select Q-07/study 061 for target-route/key-domain overlap checks and separate validation. At this closeout no 061 target run has occurred.

## CANDIDATE-FIRST-061 — sum-locked block rotation

- Date: 2026-10-31 UTC; parent target-stage approval 15:33:42 UTC. Seals and resource receipts retain actual timing; commit times are not run times.
- Scope: AZ/KRYPTOS same-alphabet periodic addition at original-position phase zero, periods 1–8, then right rotations of consecutive blocks widths 3–12 by integer block sum modulo actual length; final block unpadded. 160 structural cases, not distinct keyed operators. All-zero keys are previously excluded pure-transposition coverage and removed from eligible target domain; no blanket nonzero p=1 exclusion was justified.
- Result: Both independently implemented target engines return UNSAT_COMPLETE, zero compatible key cylinders. Exact bounded exclusion only; no new checksum, direction, width schedule or additional layer after failure.
- Validation: 19,656 independent tiny roundtrips, 137,268 complete tiny cylinder comparisons including free keys; all 416 sealed blind sets agree, all 352 plants included, all 320 full-mask plants uniquely recovered, all 32 sparse planted cylinders retain seven free residues, 0/64 nulls fit. Independent audit checks 79,865 candidate/free-coordinate roundtrips; those probes are controls, not exhaustive enumeration of huge cylinders. Completeness follows from exact residue equations and tiny truth sets.
- Prior overlap: Exact target-route membership compared with local001/049/050, columnar, grid/rotation/cylinder/irregular/disrupted/Myszkowski/grille and EXT012 route compositions. No intersections in inspected domains. EXT012 historical484-spec universe hash and250,348 configuration counts reconstructed exactly; unavailable historical executable revision remains a semantics limitation. Millions of permutation membership comparisons are NOT cipher-search trials. Sources are pinned/hashes retained; external programs were not executed.
- Provenance/resources: Benchmark freeze SHA256 `05be2644387a92cb3610123d566dc325f9526a164701a36ee05d6924e7bdc719`; target transport `2010f5155153fe91f2db4bc82a2e9b142e407a5a0f9a59d1e346203b7cde1701`. Canonical ciphertext unchanged. Complete resource ledger includes eligibility reconstruction/comparison work and explicitly labelled conservative reserves where historical measurements are missing.
- Evidence: [Report, frozen protocol, independent audits, complete code/control data and receipts](candidate-first-061/README.md); [readable prior-coverage decision](candidate-first-061/PRIOR-COVERAGE.md).
- Method improvement: Retain route-membership comparators with positive controls and source-universe hash reconstruction. Separate different mechanisms, actual target-route aliases, key-domain overlap and unsupported broad external negatives. Exact solving is fast; no scoring or stochastic-search bottleneck warrants a replacement. Any future changed method requires fresh held-out validation.
- Status/next action: Scientific execution and independent audit complete; artifacts published. Reconciled local/external ledger closes Q-07 and selects Q-08/study 062 for its own overlap and validation gates. No 062 target run at this closeout; no Site or paid service change.

## CANDIDATE-FIRST-062 — ciphertext-steered Josephus with exact key cylinders

- Date: 2026-10-31 UTC; parent target approval 15:46:09 UTC. Seals and measured resource receipts retain execution chronology.
- Scope: AZ/KRYPTOS, all97 start slots, two fixed directions, emission-index periodic additive keys p1–8. Remove slot, emit C, select next directional survivor then advance1+rank_A(C). 388 distinct target maps,3,104 structural descriptions; not a count of distinct keyed functions. All-zero keys already analytically covered are removed from cylinders symbolically; no other constant-key exclusion inferred.
- Result: Both independently implemented target engines UNSAT_COMPLETE, zero compatible key cylinders. Exact bounded exclusion only. No direction flips, changed step rule, new layer or extra target run after failure.
- Validation: 51,012 tiny roundtrips/routes,365,616 complete tiny cylinders and all3,104 deterministic full-size configuration controls. Blind872-case exact-set agreement,808/808 plants included,32 sparse planted cylinders retain7free residues,0/64 matched null fits. Of776 full-mask plants,656 were unique and120 ambiguous/free; ambiguity was correctly preserved. Independent audit replayed85,924 roundtrip probes, not claimed exhaustive enumeration of huge free cylinders.
- Prior-work gate:388 maps compared with exact local catalogs and inspected external fixed/alternating/periodic/artifact deletion, columnar/grid/Myszkowski/grille and composed routes; no completed-domain intersections. Column widths96/97 mathematical supersets intersect but are not established completed prior domains. One redundant EXT012 membership pass arose from crossed coordination; both receipts/costs retained, not double-counted coverage.
- Corrections: Independent primary-source check found and corrected a manually copied artifact E-to-A pair before freeze; original erroneous comparator and receipts retained. The corrected literal campaign cardinality agrees with source. Historical EXT012 universe hash proof retained; unavailable original executable remains a limitation.
- Provenance/resources: freeze `8538c95ffde07c6718435068c96c3d5d8c9a854723f256d08d3629043028e434`; target transport `446cc666ea49c3de05a7a84dbffd6f7b04eb7f650787a410de8ff4070d6e3cd1`. Canonical ciphertext unchanged. Benchmark53.543CPU seconds and independent audit61.962CPU seconds; full ledger includes all route-overlap costs and conservative reserves.
- Evidence: [Findings, code/control archive and independent audits](candidate-first-062/README.md); [prior-domain review](candidate-first-062/PRIOR-COVERAGE.md).
- Method improvement: Exact symbolic ambiguity handling is essential, not optional. A proposed read-only pinned-source AST literal checker addresses the observed manual transcription failure; it requires fresh synthetic/adversarial validation, never external-code execution, and does not replace semantic domain review. It is a separate tool task, not already-validated capability or a novel cipher algorithm.
- Status/next action: Scientific execution and independent audit complete; artifacts published. Reconcile ledger and advance to063 coupled carry plus the separately authorized validation-tool task. No063 target run at this closeout; no frozen062 artifact modification or paid-service/Site change.

## METHOD-LITERAL-001 — independently validated read-only source literal checker

- Date: 2026-10-31 UTC; authorized after062 closeout. This is validation tooling, not a K4 cipher experiment or another hypothesis.
- Observed failure:062's external artifact-step reconstruction initially transcribed EA as AE; independent source review caught it before freeze. Original erroneous and corrected receipts remain untouched.
- Change: Add a read-only hash-pinned Python AST selector for one explicit dictionary/comprehension iterable of literal strings. No source execution, dynamic expression evaluation, network access or whole-program semantic claim. Unsupported selector/iterable forms fail closed. Provenance string is supplied, not authenticated.
- Validation: Builder froze v1 before independent reviewer authored81fresh fixtures and three preplanned JSON supplements. All84CLI cases pass, zero false accepts/rejects within stated expectations. Four separately labelled actual-source tests accept EA and reject AE for both selectedkeys. Four post-inspection diagnostic fault injections also failclosed; actual OS exhaustion was not tested. Frozenv1 remains unchanged.
- Boundaries: Comprehension body, runtime tuple shadowing, alias/reflection/update mutations and source meaning are deliberately outside literal-only scope. Accepted syntax is not a guarantee of safe runtime behavior. Every selected-dictionary key must be a string literal. Use bounded CLI for untrusted bytes; library does not impose OSlimits.
- Evidence: [Specification, method record, independent audit and immutable evidence archive](source-literal-checker-v1/README.md); utility `experiments/source_literal_check.py`; seven focused regression methods include replay of84 archived cases, not a new holdout. Blind fixturemanifest `a3f677bc9fe84c13b2ef11ad84bc87ed218a5f7556ff5b587babe5f209a70f34`; toolfreeze `29e3912f38661c9304adf37586d22801b0c610bfd866abe899d976d982c263d8`.
- Resources: Independent84-case childCPU3.000281seconds; actualsource supplement0.163505seconds; post-inspection fault-test body0.002391868seconds (excludes harnessstartup). All receipt bounds and caveats retained.
- Decision: Retainv1 as an internal transcription aid; no separate repository/global invention claim. Syntax extensions require a new specification/freeze/fresh independentholdout.063 eligibility did not depend on this utility; no frozen cipher experiment changed or target rerun.

## CANDIDATE-FIRST-063 — coupled 26/24 accumulator compatibility test

- Date:2026-10-31 UTC; parent target-stage approval16:03:52UTC, explicitly compatibility/exclusion only, not plaintext recovery.
- Scope: AZ/KRYPTOS, phase-zero arbitrary periodic keys1–6, all624 initial(a,h) states, t=a+x+k,a'=t mod26,y=(a'+OLDh) mod26,h'=(h+floor(t/26)) mod24. No changed modulus, readout timing, signs, routes or layers. Zero keys INCLUDED; this machine is not pure transposition at keyzero.
- Result: Both independent target engines UNSAT_COMPLETE; zero compatible alphabet/key/start-state/plaintext tuples. Exact bounded exclusion only; no extra target runs or rescue tweaks.
- Correctness: Independent scalar-T and explicit(a,h) implementations, complete tiny forward truth and all7488 direct full-size A/period/state controls. Local13/11-letter entry-state filters intersect complete keys only as a superset; continuous97-letter replay from actual initial states is mandatory. A retained tiny reset-trap has a shared local key but no globally reachable solution.
- Blind benchmark:688 complete independent tuple sets agree,624/624 plants retained,55,263 compatible parameterizations allfully roundtrip,0/64 union null fits. Everyinitialstate represented,26 plants in each of24 alphabet/period/kind cells. Benchmark51.111CPU seconds, independentaudit43.702CPU seconds; full resources include all prior/control/audit costs.
- IDENTIFIABILITY LIMIT: ZERO unique recovery among624plants, each8–126plaintexts. Post-reveal projection of existing sealed outputs only:63 plants vary onlyposition0;424 additionalplants onlyprefix0–20;137 also laterunknown positions. Everyplant has a same-generating-key first-symbol-only alternative with identical postfirst state. Independent non-search ambiguity audit confirms this. Not a probabilistic recovery success, no English scoring or arbitrary candidate selection.
- Prior work: Exact fixed-alphabet causal-affine non-equivalence uses all26 reachable conditional translations forcing affine relabelings, then a carry-discontinuity witness. Nonlinear local radix is separated by its own reachable-state parity certificates, not by a false linearity assumption. Scott adjacent-noise is set-valued; finite-message intersection caveat retained. Source files match pinned Git blobs; no externalprogram execution.
- Provenance: freeze `5b0d6d5ea6e3b10f2ced28474d09bd1e475281969bb3a19ba12e82819f568827`; targettransport `8c399cc7abb46336a5eda6ebb8beef1bf2fd18589212487bb3fa9b8bd41cada8`. Canonical ciphertext unchanged; artifacts retain salts/seeds/seals, aliases, reset-trap and ambiguity diagnostics.
- Evidence: [Findings, frozen protocol, independent benchmark/ambiguity/target audits and archive](candidate-first-063/README.md); [prior-equivalence report](candidate-first-063/PRIOR-COVERAGE.md).
- Method improvement/decision: Correct compatibility solvers need not uniquely identify plaintext. Future proposed models must declare which unknowns the clue mask can identify before presenting a recovery objective. No compatible K4 tuple remains to rank here. Close this bounded family; [next decision](fresh-program-20261031/NEXT-DECISION.md) prioritizes independently sourced genuinely new mechanisms, not arbitrary variations. Literal-checker utility is independently validated but separate;063 did not depend on it.
- Audit correction: Final non-search audit initially assumed an explicit block field; original failed script/receipt and corrected audit are retained. No solver, data, output or target-run changes.
- Status: Scientific execution and independent audit complete; artifacts published. Four fresh families finished at their frozen scopes. No fifth target is admitted or started by this closeout.

## CANDIDATE-FIRST-064 — ciphertext recurrence-distance key clock

- Date:2026-10-31UTC; parent approved residualp5target16:46:13UTC after independent source/structural/math/blind audits and pretarget clarification.
- Frozen scope: AZ additive, immutable primitive cyclic keyp2–8, pointer0, empty history; emit then step1 for first ciphertext occurrence, otherwise gap to its previous occurrence. Allconstant/nonprimitive seeds excluded; no addedsign/alphabet/reset/phase/history/route.
- Result: Complete exact bounded negative. Sixperiods2,3,4,6,7,8 inherit completed044ordinary-period negative crib supersets and were NOT rerun. Onlyp5 newly evaluated once per independent implementation, both empty. One-based24/25samekeyresidue requires25versus2. No fitted candidate or language ranking.
- Prior gate:159,160raw descriptions reconstructed, no externalcode executed. AlltenpinnedGitblobs verified; source materialization extraLFcorrections retained. Original/correctedE122banks separate. p5has604strict0–2check crib containers but no equivalentfull/cribmap; documentarythresholdskips differ from the19checkrecurrencerelation. Initialunresolved concern resolved by exact semantic/outcome review; originalprotocol preserved beside independentlyreviewed pretargetaddendum. Notworldwide novelty.
- Controls: Production169,516tiny complete-relation/union cases; independent167,961relations/1,119,740bruteseedcomparisons. Fresh auditor9,865cyclic-orbit cases throughp8. Blind309cases/2163exactrelations agree,224/224plants retained109unique/115ambiguous,64nullsempty,21diagnostics14unique/7ambiguous;367certificates replay. No failed/omittedcontrols or postrevealrepair.
- Exactness: Recursiveversusspan-sum clocks; divisor-recursionversusDSUinclusion-exclusion. Completeprimitivecylinders projected existentially onto usedcoords; crossperiodunions notsummed. Singlekeyfit notplaintextidentification.
- Provenance/resources: Productionfreeze f4bd1ce5cfa9f4bb98261a0f003203b00e9d2a6cb042118ae2d7a093894d9681; canonicaldata08a1a84bd0dddf2449a2c7f67ee770d093ed47f6ad9a795630b77a2c8062f241 unchanged. Targettimers0.0CPU atresolution, positivewallintervals retained. Full[resource ledger](candidate-first-064/RESOURCE-LEDGER.json) includes prior/control/audits and explicit unmeasuredreserve, below8CPUhours/8GiB. No paidservice/checker or securitychanges.
- Evidence: [Findings, frozenprotocol/addendum, independentlyaudited controls/source/target and immutablearchive](candidate-first-064/README.md).
- Method improvement/next: Transfer completednegative containingdomains before new keysearch; distinguish fullclockequivalence from strictweakercribsupersets and actualskips. Closefixed064, norescuerule. Researchonly for a genuinelydifferent independentlymotivated mechanism; no sixthmodeladmitted/started. Update existingqueue, not competingnarratives.
- Publication status: Scientific execution and independent audit complete; artifacts published.

## METHOD-SPARSE-LAW-001 — synthetic sparse modular-law inference pilot

**31 October 2026 — synthetic-only method study, not a numbered cipher hypothesis.** [Readable result and reproducibility evidence](method-pilots/sparse-law-v1/README.md). No K4 ciphertext or crib letters were used; all 68 family records remain unchanged.

The frozen 31-feature, at-most-three-coefficient model covers positions 6–96: 91 modeled positions, 24 observations and 67 unknowns; the first six positions are excluded. All 40 exact marginal-projection comparisons agreed; independent replay and full factorized-relation verification passed. Among 28 in-family cases, 1510/1876 unknown positions were conditionally forced (dense baseline 219), with no false forced values; 12/28 recovered all 67 unknown modeled values. Four misspecified observational twins each induced one wrong conditional prediction: compatibility does not certify model membership. Twelve plain expansions retained their declared caps as incomplete outcomes.

The oracle was faster in 33/40 recorded workloads (49.321724 CPU seconds versus join 66.553951). The join additionally serialized a factorized relation; the reference primarily delivered exact marginals/witnesses. These are observed end-to-end workloads, not an identical-output or universal algorithm ranking. No join speedup is demonstrated; retain the oracle for the needed projection task.

The original independent audit parent lacked resource caps and peak-RSS instrumentation; its original receipt remains intact. An unchanged, externally capped post-label-release repeat passed at 125.239946 inclusive CPU seconds and 120436 KiB peak RSS. It is not new blind evidence and does not repair the original missing measurement retrospectively. Conservative charge: 600 CPU seconds. [Results](method-pilots/sparse-law-v1/RESULTS.md) preserve the full execution history.

**Method lesson / next decision:** distinguish coefficient, global-function and instance-trace equivalence; enforce identical primary output contracts in a separately frozen future comparison. The quotient and parity-first documents are design/toy-proof evidence only, not v2 performance or K4 results. Any later implementation needs fresh independent controls. This is a model-specific application/combination of standard foundations, not a demonstrated global invention; no separate repository or target admission follows. Public prose redactions and original/public hashes are explicit; computational artifacts remain unchanged.

## METHOD-PARITY-FIRST-002 — matched synthetic decoder validation

**31 October 2026 — synthetic-only; no new cipher-family ID or target run.** [Results, code and immutable evidence](method-pilots/parity-first-v2/README.md). All 40 cases / 240 timed outputs matched the independent oracle; 25,806 sparse marginal witnesses passed. Thirty-two in-family cases forced 2103/2144 unknown modeled values with no false forced values; 27 determine all 67. First six positions are excluded. Four contradictions are empty; four dependent twins each have one wrong model-conditional prediction. Structural replay and dependent controls mean this is not 40 independent random draws.

The exact prediction sets equal the CRT baseline. Matched summed case-median solver CPU was 19.612 versus 14.403 seconds (26.6% lower), with 38/40 wins, two alias losses (13.6%/46.9% slower), higher peak RSS (8448 versus 21760 KiB), and three-repeat variability up to 1.97×/2.95×. No universal speed or cross-v1 recovery gain follows. Completed validation receipts total 148.455768 CPU seconds before packaging; nested stages are not double-counted.

Preserved development failures, rejected hybrid, root-invocation exit 137 before seed generation, exactly one subsequent valid draw, post-release reporting failure, output seal and full resource-topology review remain traceable. Public receipt-path redactions have original/public provenance; scientific bytes and original commitments are unchanged.

**Next decision:** retain v2 unchanged and investigate the two alias-loss mechanisms through a separate projection-saturation design review. No prototype/holdout or K4 target is admitted by this closeout. Any future benefit needs a new freeze and fresh independent controls; no separate repo/global invention claim.

## METHOD-FILTERED-AFFINE-003 — generic residual projection and source-operator review

**31 October 2026 — generic theory/module and source review only; no target run or new cipher-family ID.** [Readable result and exact provenance](method-pilots/filtered-affine-v1/README.md). The r < q affine-cover projection theorem is reviewed; r ≥ q requires an exact bounded fallback. The historical toy remains explicitly unsafe as a reusable API. The separate hardened prime-field module independently passed 10,931 valid cases, 95,713 witness checks, 46 malformed rejections, 74 budget checks and eight tamper rejections in normal and optimized Python. Certificate replay counts include expected-negative attempts. Resource receipts are not performance claims.

The source/operator audit separates E globally from the specified fixed-alphabet causal linear and deterministic position-only grammars, not from every finite trace. Scott's exact global carry intersection contributes 156 already-attempted functions C; remove them without authenticating broad external negative claims. The B parity implication transfers from an existing receipt without new target computation. Matbalez recurrence scope remains unresolved. Original drafts, clarifications, later audits, failed toy API examples and source pins are preserved; third-party source caches are omitted with explicit provenance.

**Next decision:** develop synthetic R = E ∖ (B ∪ C) canonical compilation with exact support-preserving lifts, Boolean exclusions, complete projections and independent controls. Generic API validation is not compiler validation or K4 admission. No global novelty, cryptanalytic speedup or solution is claimed; all 68 family records and prior method studies remain unchanged.

## METHOD-SATURATION-004 — completed synthetic projection-saturation validation

**31 October 2026 — methodology only, no new target-study ID.** All 480 outputs from one fixed 40-case/four-arm/three-repeat draw matched the complete maximal-support oracle; 47,412 sparse witnesses and 78 certificates verified. Charged-stage sums of paired case medians were CRT 24.405472→13.323356 and parity 16.280120→9.048368 seconds, with 14/10 slower cases. Ordinary aggregate improvements were only 1.32%/0.83%; worst regressions 79.65%/35.40%. Both arms returned identical exact conditional masks; dependent twins each forced one wrong value. Retain optional/default-off and model-membership limits. Total deduplicated managed CPU 488.783194, including historical work; nested costs not doubled. [Original freezes, outputs, released truth and review](method-pilots/projection-saturation-v3/README.md). No failed residual-cohort truth is included.

## METHOD-RESIDUAL-005 — canonical compiler development and reference API correction

**31 October 2026 — methodology only, no new target-study ID.** Fixed R = E minus (B union the exact 156-function C), with the unchanged canonical dictionary and common original support ≤ 3. Audited development checked complete padded support/beta fibers, minimal original lifts and cross-piece provenance on disclosed tiny/full-feature controls. Reference v1 allowed NaN through two max_points paths; separate v2 added strict built-in nonnegative-integer guards, retaining originals and historical fixed-integer evidence. This was a reference API correction, not a demonstrated decoder-predicate error. [Development, full audit and correction history](method-pilots/canonical-residual-checkpoint/README.md). No K4 admission, new cipher family or global novelty claim.

## METHOD-RESIDUAL-006 — permanently incomplete fresh validation and capacity obstruction

**31 October 2026 — methodology only, no new target-study ID.** The single approved fresh residual cohort scheduled 48 cases / 96 jobs. 23 output artifacts were accepted; job 24 failed and 72 jobs never started. The failing worker reported 47.947867 CPU seconds under nominal 40/41 limits; the controller stopped and the 82-second reserve was retained. These are not 23 successful independent cases. No retry/resume/redraw or released-truth analysis follows. [Approved sanitized preservation, independent failure review and static proof](method-pilots/canonical-residual-checkpoint/README.md) exclude seed/truth/custody.

A separate static capacity proof found at least 1,393 required padded support/beta pieces representing seven constructed laws—not 1,393 distinct functions. The frozen reference charges 1,393 × 2,197 = 3,060,421 ambient points beyond its 2,000,000 cap; the 911th piece already exceeds it. Thus legitimate VERIFIED was impossible for that verifier traversal, regardless CPU. This does not identify the killed phase or explain the OS overshoot. Separate modest-limit controls did not establish or repair that root cause. Failed cohort stays permanently INCOMPLETE.

## METHOD-REFERENCE-007 — certified-fiber residual reference disclosed development

**31 October 2026 — methodology only, no new target-study ID.** Independent residual reference v3 is a different project from projection-saturation v3 and fresh-validation protocol r3. Two separately authored suite/oracle implementations each ran normal and optimized once on the same 42 disclosed fixtures: 25 exact nonempty / 17 empty. Complete ranks/kernels and two-way base equivalence precede observation-fiber enumeration; pieces, original lifts, joints, masks and provenance agree. [Frozen 55-artifact evidence and audit](method-pilots/canonical-residual-checkpoint/README.md).

Stage ledger reports 37.395377 worker CPU plus 0.503533 supervisor samples = 37.898910 known components, excluding control/final tails; the full 20 supervisor allocation is separate, not measured cost. Subset timers are not added again, no reserve remains open. Conservative project allocations 16,880/28,800 CPU seconds are not a measured project total. The separate full-31 resource pilot/rank-beta preflight remains **design only, not authorized or run**; the ledger checkpoint is not permission to launch it. No revival of the failed cohort or K4 target admission.

## METHOD-PREFLIGHT-008 — full-31 certified workload pilot

**31 October 2026 — two disclosed controls, not a fresh holdout or target study.** [Frozen sources, paired-counter pre-run amendment, all four slots and independent outcome audit](method-pilots/full31-preflight-v1/README.md). Author/reviewer normal/optimized slots all passed. Control A stopped after the first fully checked above-cap prefix: 89 original supports, certified lower bound 1,006,226 > 1,000,000, exact W unknown; it was not sent to semantic solvers and is not EMPTY. Control B scanned all 4,495 supports with exact W = 1, then the unchanged producer returned EXACT and the full independent reference VERIFIED_EXACT for its disclosed law. Fiber-count equality is necessary, not a substitute for full verification.

The pre-run amendment separates generation and audit beta/row counters while retaining the shared 50,000,000 work limit, 20-second per-control cap and 320-second stage allocation. It is not a post-hoc weakened gate. Runtime emitted exactly eight certificate files (two per slot); approved publication stores one archive/member copy, preserving exact bytes and provenance. All nominal/semantic/resource distinctions remain explicit.

Reported workers total 41.862310 CPU seconds plus 0.653631 exclusive supervisor samples = 42.515941 known components, excluding tails and unmeasured preparation/closeout. Full supervisor policy charge is 20 seconds; worker plus full charge 61.862310 is not measured CPU and samples must not be added again. Conservative project allocations are 17,200/28,800 seconds, not a measured project total. No scheduled slot, reservation or retry remains open; prior CPU-overshoot cause is not repaired by this PASS.

**Next decision:** prepare and review a separate fresh residual-validation protocol; no draw or execution authorized by this closeout. Two known controls do not establish representative workload completion, recovery, speedup, global novelty or K4 admission. The old failed cohort remains permanently INCOMPLETE and sealed; all 68 cipher-family records stay unchanged.

## METHOD-RESIDUAL-009 — fresh residual v2 stopped INCOMPLETE

**1 November 2026 closeout — failed fresh synthetic validation, not a K4 experiment or validation PASS.** [Full failure, preserved sources/receipts and independent reviews](method-pilots/fresh-residual-v2-incomplete/README.md). Eight of 28 slots executed: four disclosed control gates, three VERIFIED_EXACT individual slots, and one cooperative preflight wall failure; 20 successors canceled. Only v000 completed a fresh normal/optimized pair. The unpaired v001 normal result is not paired coverage. No truth-based accuracy, twin outcome or cohort coverage was evaluated.

The failed v001 optimized slot checked 4,153/4,495 supports with lower bound 1 and exact W null; producer and full reference were not attempted. Its 20-second cooperative gate expired, with preflight wall 20.322845 seconds and worker CPU 16.325925. Ordinary exit 1 and reaped child distinguish this from an OS timeout; the triggering I/O/computation/scheduling cause remains unresolved. A matching normal-mode W = 1 cannot substitute for missing completion.

Known worker plus supervisor-sample CPU totals 56.075505 seconds across mocks, generation and eight slots. Full supervisor policy 133 and worker-plus-policy 184.756527 are not measured CPU. Failed-slot reservation 80 is within attempted cohort allocation 640; stage 3,000 and project 20,200/28,800 allocations remain unchanged. Tails/control overhead are unmeasured, not zero. Original stop lock, reservation and eight certificates (including partial failure) remain preserved; publication uses the one approved archive without extraction or replay.

**Method lesson / next decision:** preserve the elapsed-wall protocol failure instead of silently adjusting caps or drawing replacements. Separately design a whole fixed-data post-failure re-evaluation with finite schedule, resource/custody gates and explicit new authority before execution. No source change, seed access, replacement draw, selective suffix retry, truth release or target run follows. Any later success on reused post-failure data is not fresh replication or retroactive PASS. The older failed cohort remains permanently INCOMPLETE and sealed. All 68 cipher-family records are unchanged.

## METHOD-RESIDUAL-010 — whole fixed-data post-failure re-evaluation

**1 November 2026 — bounded conditional implementation validation on reused synthetic data, not fresh replication or K4 evidence.** [Result, sources, released synthetic data and independently reviewed immutable evidence](method-pilots/fixed-data-residual-v1/README.md). All 28 new slots completed once: four disclosed resource gates and 24 VERIFIED_EXACT slots, with 14 exact normal/optimized pairs and all 12 supported base pairs (four per stratum). There were 791 informative distinct-per-base hidden contexts among 804 supported positions, zero supported wrong forced values, and three dependent misspecified twins each false-forced only row 84. Informative is not necessarily singleton; modes/contexts/twins are not independent trials.

Ambiguity persists: v006 has 50 canonical/joint alternatives, v008 has 13; ten other bases have one each. v003 has two coefficient lifts but one function. Model membership is not established. The uniform preflight wall envelope changed 20 to 60 seconds under a separately reviewed freeze; mathematics, fixed data, logical caps, outer constraints and full schedule remained fixed. Maximum observed preflight wall 19.237141729 does not prove the larger gate was necessary or diagnose the earlier cause. No old-slot reuse, selected suffix completion or replacement draw occurred.

Known worker/supervisor CPU components total 294.313402 across 33 stage invocations; full supervisor policy 420 and worker-plus-policy 704.002774 are separate non-measured charges. Nominal stage 3,000 includes 2,800 invocations and 200 control allowance; project allocation 23,200/28,800 is not measured consumption. Original failed reserve 80 remains; current reserve zero. Remaining tails/control overhead are unmeasured. Current synthetic truth/embedded seed was released only after terminal acceptance and separate authority; older failed-cohort truth remains sealed and excluded. Publication transfers one archive containing all 28 new certificates without extraction/replay.

**Lesson / next decision:** retain complete conditional relations and ambiguity, preserve both original INCOMPLETE outcomes, and distinguish resource re-evaluation from independent fresh validation. A separately assembled adapter source/admission review is the next gate; no mocks, actual controls, target arithmetic/run, new cipher family or general novelty claim is granted by this checkpoint. Matbalez historical scope remains unresolved. All 68 canonical family records remain unchanged.

## METHOD-ADAPTER-011 — sparse residual pretarget source and disclosed controls

**1 November 2026 — pretarget method evidence, K4 UNRUN.** [Accepted prefix, immutable sources and derivative provenance](residual-pretarget-v1/REPOSITORY-STATUS.md). Source freeze fe2864d656a426635731c7f4a0be07329c67eb5e4b0fe15e6fb10e8661c9f11d remains unchanged. Two operational mocks each passed 159 named assertions (not independent samples). Positive disclosed control returned EXACT/VERIFIED_EXACT, W=1 and one function/lift/piece/joint; contradictory-context control returned EMPTY/VERIFIED_EMPTY, W=0 and complete zero relation. Each certified all 4,495 supports; W=0 alone is not semantic EMPTY.

Four accepted prefix jobs consumed 284 nominal CPU seconds, with zero current reserve. Known worker plus supervisor-sample CPU is 19.957271 seconds; policy supervisor 72 and nominal 284 are not measured or additive CPU. The same single 600-second/256-MiB reservation remains; project allocation 23,800/28,800, 5,000 unallocated. Original failed reserves are not reused. Overhead/tails are explicitly unmeasured or separately scoped. The sole two-certificate archive and original/public mappings preserve exact scientific bytes; public administrative copies are NON_RELAUNCH_READY.

**Lesson / next:** retain complete EXACT/EMPTY interface handling and prospective exact-byte loader authentication; no historical cache error was observed and no speedup is claimed. H-CANONICAL-RESIDUAL-FEEDBACK is the new specified-but-unrun family, not a target result or run count. Preserve all 68 prior family bodies. Bounded EXT-051 uncertainty is accepted only for planning; B/C known-repeat exclusions and global-versus-finite-trace limits remain. Complete the coherent checkpoint, then separately decide one fixed target stage. No target arithmetic, sealer, retry, first-six claim, score winner, retuning or automatic successor is authorized here.

## RESIDUAL-R-TARGET-001 — canonical sparse residual bounded negative

**1 November 2026 — one finite K4 hypothesis, two prescribed mode checks.** [Sealed result, recovery, original/public provenance and independent pair/seal reviews](residual-target-v1/REPOSITORY-STATUS.md). Immutable run identity k4-canonical-residual-recovered-target-v1; recovered source freeze 53ecd1af6cb8e965f4ca824152c413e9dff2370c90ba4b26c5705dc5a5660262. Canonical 97 symbols/24 clues, 91 tail rows; AZ/Z26, six newest-first prior ciphertext letters, fixed 31-feature global law, at most three nonzero original coefficients, full-symbol equality before CRT. The exact domain is R = E minus (B union C), not all sparse nonlinear feedback.

Both normal and optimized modes completed 4,495 support containers: preflight W=0, producer EMPTY and reference VERIFIED_EMPTY, zero pieces/functions/lifts/joints and all masks empty. W=0 alone is not the semantic proof. No plaintext candidate, first-six claim, scoring winner, uniqueness claim or retuning. B retains its separate negative; C's 156 functions remain excluded as known attempted overlap, not newly validated external negatives. External-history uncertainty remains a novelty limit.

Workspace loss did not refund old consumption or fabricate authority. Public source recovery retained unchanged scientific modules and prior 284 nominal prefix consumption; two metadata-only 16-group recovery checks passed before fresh frozen target authority. Prior mocks/controls and same-data synthetic validation were not rerun. Final metadata seal and independent closeout completed; all three local permissions spent and no in-flight reserve. One unique 10,152,363-byte certificate payload is archived once with both original-mode references, not duplicated or extracted for publication.

Known target-plus-seal CPU components: 25.175256 worker  + 1.171793 supervisor samples  = 26.347049 seconds. Supervisor policy 16 and nominal 172 are separate non-measured charges. Original 600 is 284 historical runtime  + 160 target  + 12 seal  + 144 overhead; separate repair 120 is 24 metadata runtime  + 96 committed overhead. Project reservation 23,920/28,800 leaves 4,880 unallocated, not measured consumption or reusable old reserve. 256 MiB evidence is disk reservation; target worker 1 GiB, supervisor 256 MiB, sealer 512 MiB memory envelopes. Preparation/review/write tails remain separately sampled or unmeasured.

**Method lesson / next:** preflight dominated recorded phase wall time, but all caps completed; retain exact engines without result-driven optimization. Close the existing 69th family as a narrow negative, preserving all 68 others and all old failed/UNRUN snapshots. The next 100 annex is unrun/unadmitted: A01 blocked by specific prior-art uncertainty; C20 is only a source/proof candidate. No retry, expanded residual domain, synthetic pilot or next K4 target follows automatically.

## METHOD-C20-012 — successor-queue synthetic correctness

**1 November 2026 — synthetic-only correctness, no K4 target.** [Exact sources/result, administrative derivative provenance, independent source/outcome review and target proposal](c20-successor-queue-v1/REPOSITORY-STATUS.md). One frozen invocation passed 17,349 exhaustive tiny cases (2,047 / 9,841 / 5,461 over alphabets 2 / 3 / 4) against an independent enumerated queue-signature oracle and 91 disclosed length-97 plant/phase pairs. Four directional fixtures, deliberately broken naive reversal, non-fixed-route witness, 16 malformed-input and 12 malformed-phase rejections passed. All 13 plants produced seven distinct phase ciphertexts. The 5,589 tiny fixed points and overlapping/disclosed cases are diagnostics, not independent statistical trials or blind validation.

The exact classical last-exit involution plus fixed AZ/KRYPTOS additive layer is implemented consistently within these checks. Finite source/proof distinctions do not establish worldwide novelty or historical creator use. The no-layer pure permutation was already excluded and was not rerun. During this synthetic pilot, no K4 ciphertext was read or transformed.

Known child CPU 0.951498 plus cumulative supervisor sample 0.178968 = 1.130466 seconds; wall 1.102165920 seconds; child peak RSS 45,716 KiB. Internal child timer is a subset, not additive. Receipt-write/final-print/outer-tool tails remain unmeasured. One 60-second pilot permission consumed within 120 nominal stage allocation (60 preparation/review separately committed); no retry or refunded permission. Administrative public freeze/receipt copies are NON_RELAUNCH_READY; scientific source/result hashes remain exact.

**Lesson / next:** the tiny complete queue-signature oracle supplies useful independent correctness without a larger solver framework; retain the simple engine. A seven-phase target protocol is proposed only, accepted for source preparation with 30 nominal seconds allocated (20 source/review + 10 target), with later target source/freeze review passed, but not finally admitted to execute. No automatic target, extra benchmark or rescue follows. C20/N100-065 is now synthetic-validated; all 100 proposals remain K4-target-unrun/unadmitted and A01 stays blocked. All 69 canonical family bodies remain unchanged.

## C20-TARGET-001 — fixed seven-phase successor-queue negative

**1 November 2026 — one finite K4 model, seven fixed phase descriptions, one invocation.** [Findings, exact stored outputs/masks, source/receipt provenance and independent outcome review](c20-successor-queue-v1/target/README.md). Standard-AZ/KRYPTOS addition after the specified successor-queue involution, no alternative key/alphabet/layer order: zero compatible phases. Clue counts [2,1,1,1,0,0,0]/24; all seven complete 97-letter outputs agree with the separate reference and re-encrypt exactly. Partial matches are diagnostics, not ranked near-solutions. Retire only this exact composition, not all Euler/graph ciphers.

Freeze 8f7b984bbdf29a8a9d6fc8bf232f9502bbeffece7fd0ae7c705e26f0a63560ec; independent outcome 4458f23af97c2fff4c124d24f85213eaf423705043c00786d8234bfe3998f125. One authorized invocation after synthetic validation/source review, external exit 0, child reaped, no timeout/error/retry. Public administrative derivatives are NON_RELAUNCH_READY; exact scientific source/result bytes remain pinned.

Child CPU 0.182064 plus supervisor sample 0.302418 = 0.484482 known sampled seconds, wall 0.4354215 seconds, peak RSS 40,576 KiB. Ten nominal target seconds consumed within 30 allocated (20 preparation/review separately committed); tails/outer-tool overhead unmeasured. Project allocations remain 24,070/28,800, not measured consumption. No recycled permissions or new allocation.

**Lesson / next:** correctness validation supported a cheap deterministic test but not K4 compatibility. Preserve the reusable classical involution and tiny oracle without claiming a novel cryptanalysis tool. Add H-SUCCESSOR-QUEUE-COMPOSITE as the 70th canonical family, preserve all prior 69 bodies and original100 draft, and update only C20’s effective status. Select unrelated source/proof work; no retuning or next execution is admitted. A01 remains blocked.

## METHOD-E01-013 — fixed conditional-alphabet synthetic validation

**1 November 2026 — synthetic-only correctness and declared controls, not an E01 K4 result.** [Fixed source policy, local 208-description comparison, stored evidence and independent review](e01-conditional-alphabet-v1/REPOSITORY-STATUS.md). One invocation passed 235,872 tiny cases, 676 source-row cells, 24 malformed cipher calls and four malformed assertion cases. Both engine result maps agree on all 320 cases: 64 positives recovered; 0/64 compatible in each wrong-assertion, independent-null, ciphertext-shuffle and source-shuffle category. These zeros are descriptive, not calibrated rates or independent statistical evidence.

The frozen literal K1/K2-as-inscribed/K3 policy builds a static conditional bigram bank with descending-count/AZ ties and previous-plaintext state, starting Q. Source-row construction and inverse/state semantics passed. Local 208 first-emission witnesses and the fixed-axis shift-bank lemma separate inspected domains only; arbitrary/unavailable external selectors remain unresolved. Prior incidental raw K4 transcription exposure from a shared-fixture read is disclosed; no observational blinding, E01 target transformation, fit or clue evaluation claimed. Procedural answer separation is not a fresh-blind guarantee.

External child/timeout CPU 8.825865 plus supervisor 0.116051 = 8.941916 known sampled aggregate; worker-command wall 8.828568523 seconds, peak child RSS 40,960 KiB. Internal worker timer already included; receipt/final-exit/outer-tool tails unmeasured. One 60-second pilot consumed within 120 allocated (preparation/review 60 separately committed). A concurrent tool-completion file required an explicitly retained metadata-inventory correction, not scientific retry. Scientific evidence remains unchanged; public administrative derivatives retain original/public pins.

**Lesson / next:** retain the simple fixed-bank method and independent source-row/reference checks, with sparse-corpus/tie assumptions and exposure limitations explicit. Separate one-candidate target proposal requires exact source/freeze review and finite grant; later 10 nominal seconds allocated (5 preparation/review + 5 runtime), but source/static review and final execution grant pending. No target, parameter sweep, new canonical family or global novelty claim follows. All 70 family records/original100 specifications unchanged; C20 narrowly negative, A01 blocked, E01 target-unrun.

## E01-TARGET-001 — fixed conditional-alphabet bank negative

**1 November 2026 — one fixed speculative model, one candidate, one invocation.** [Full result, exact scientific evidence and independent outcome review](e01-conditional-alphabet-v1/target-v1/README.md). Frozen as-inscribed earlier-section source bank, descending-count/AZ ties, previous-plaintext state starting Q and AZ output: COMPLETE_ONE_CANDIDATE / EXACT_INCOMPATIBLE, 0/24 public clue matches. Both full 97-letter outputs agree; both full re-encryptions pass. The entire candidate and failed assertions are retained, not ranked or filtered. This retires only the fixed E01 model, not all source-derived/conditional alphabets.

Freeze 2756209215f4464bdc04a748b7e69701a1baf3e2cf6ed7ce8859acaa0c1e9e13; independent outcome 7df3cf0c1d07ac621f715b0589c7f40cf2a8491eb9d7ba918dc4f3971922db82. Exact source/input dependencies unchanged, external exit 0, child reaped, no error/timeout/retry. Earlier incidental raw-text exposure remains disclosed; the later target transformation was separately authorized, not observationally blinded.

Known child/timeout CPU 0.177131 plus supervisor 0.104766 = 0.281897 seconds; wall 0.172584477 seconds; peak RSS 40,936 KiB. Internal worker timing already included, receipt/final-exit/OS/tool tails unmeasured. Five nominal execution seconds consumed within 10 allocated, preparation/review separately committed; no permission recycled. Static outcome review did not repeat the cipher/inverses.

**Lesson / next:** invertibility and successful synthetic controls do not imply K4 compatibility; preserve the fixed-policy diagnostic and source omissions. No corpus/tie/start/offset rescue. Add the exact H-CONDITIONAL-ALPHABET-BANK as family71, preserving prior70 bodies and original100 draft; two proposals target-tested narrowly negative, 98 target-unrun. A01 remains blocked. Select unrelated source/proof work before any new admission; no next target granted.

## METHOD-E02-014 — reference-cursor disclosed implementation checks

**1 November 2026 — synthetic implementation validation, not blind recovery or K4 evidence.** [Source audit, fixed policy, pre-run amendment, exact evidence and independent artifact readback](e02-reference-cursor-v1/REPOSITORY-STATUS.md). One frozen invocation passed 22,230 tiny cases, 20,020 real-reference one-step cells and 48 disclosed length-97 plants between independent scanning and indexed implementations. Wrong-reference plaintext mismatches: reversed 48/48, AZ-only 47/48, wrong-start 15/48; respective coincidences 0/1/33 retained. Descriptive diagnostics, not p-values or calibrated rejection. Full-size transcripts retained; toy/cell evidence is assertion counts. Null raw decoded text was not retained, so independent readback recounted stored flags, not independently decoded controls.

The zero-fit operator's catalog blind-plant gate was explicitly amended before execution to independent exhaustive/transition/disclosed consistency checks. The original catalog is immutable historical evidence; no blind PASS or post-result weakening claimed. A source-search snippet displayed K4 text after source/table freeze; no E02 target transformation followed. Next-occurrence book-cursor prior art is acknowledged; rank coding/advance-past convention is incremental, not a novel primitive. Reference 770 positions / 746 distinct alphabets is not a proved minimized-state count.

Known aggregate CPU 6.594916 seconds excludes final receipt serialization/exit tail; wall 6.477682 seconds, child peak RSS 40,832 KiB. Nominal 120 = 60 pilot + 60 source/review, not measured project consumption; no retry/refunded permission. Original runtime source/pins and historical generic paths remain evidence, not current launch authority.

**Lesson / next:** preserve null coincidences and prospective admission changes; disclosed consistency supports software only, not historical intent or model identification. Exact one-candidate target proposal suggests 10 nominal seconds but has later 10 nominal seconds allocated (5+5), but source/static review passed and final execution grant remains pending. No target or automatic variants. All 71 canonical family bodies/original 100 specifications unchanged; two target-tested and 98 unrun, A01 blocked.

## E02-TARGET-001 — fixed reference-cursor rank negative

**1 November 2026 — one fixed composition, one candidate, one invocation.** [Full result, exact sources/receipt and independent artifact readback](e02-reference-cursor-v1/target-v1/README.md). Literal earlier-section circular reference plus JZ, start 0, current position eligible, next-occurrence distinct-letter rank on AZ, advance past selected occurrence: EXACT_INCOMPATIBLE, 0/24 clues. Both 97-letter outputs agree, both saved inverse strings match authenticated ciphertext, and four final cursors equal 756. All failed assertions retained; no scoring, early rejection, fit, variant or retry.

Freeze 9d9621bcb21b9a9a7a1dd4f065e31228352137858c250e88259b15fcae9602f4; independent readback 72bf9844dc623f107a75b430672c2899d4855ce94a195d7c775519b497533999. External resource PASS means execution/integrity success, not cipher compatibility. The readback compared stored outputs/inverses and recomputed assertions, not a third independent decoding. Next-occurrence book-cursor prior art and bounded coverage omissions remain.

Known aggregate CPU 0.328628 seconds, wall 0.205243 seconds, peak RSS 44,972 KiB. Final receipt serialization/exit tail excluded. Five nominal invocation seconds consumed within 10 allocated (5 preparation/review separately committed); no permission recycled. Synthetic blind gate remains explicitly replaced before execution, not retroactively passed blind; original evidence/catalog unchanged.

**Lesson / next:** inverse/transition consistency is not K4 compatibility. Retire only this fixed composition, not all book/rank/adaptive ciphers; no source/start/direction rescue. Add H-REFERENCE-CURSOR-RANK as family72 while preserving all prior71 bodies. Three proposals target-tested narrowly negative, 97 target-unrun. M21/N100-099 exact framing-capacity filters is next source/proof/benchmark-design task only, with no experimental allocation or target authority. A01 remains blocked.

## METHOD-M21-015 — exact framing-capacity synthetic pilot

**1 November 2026 — one disclosed synthetic method invocation, no K4 input or target inference.** [Frozen design, complete compressed rows, controls, source and independent result readback](m21-framing-capacity-v1/README.md). All 24,624 matrix cases and 132 controls passed; zero exact-count mismatches or false-pruning events against independent exhaustive enumeration. Stored attainable lengths, witnesses and baseline soundness checks passed. The exact bit-aware filter excludes 1,930 cases admitted by the stronger exact-attainable-length baseline with mandatory nonzero-prefix guarantees; 8,453 versus the weaker baseline. These are case requests, not independent discoveries or K4 exclusions. The 16,171 all-baseline agreement cases and overlapping fixture feasibility patterns remain retained.

Measured DP case CPU 2.313976845 seconds versus cached-oracle case CPU 0.507157471 seconds; no speedup. Oracle input encodings/digit histograms are reused across requests, so these timings describe the recorded workloads, not a universal algorithm ranking. Whole child CPU 4.11879517 seconds, wall 4.12233698 seconds, peak RSS 43,440 KiB. DP totals 375,129 visited states, 761,882 transitions and 1,301,302 emitted-bit comparisons; maximum count bit length 13. Supervisor overhead was not separately instrumented and remains charged to the existing 60 nominal preparation/review reserve; 180 nominal applied to the scientific child within 240 allocated. No budget increase, retry or recycled unused reservation.

**Lesson / next:** classical finite-state/counting mathematics is exact on this bounded fixture matrix and prunes more than safe length-only checks, but is slower than the cached oracle and has no demonstrated practical 97-symbol scaling. Retain as an infrastructure gate, not a novel primitive or new cipher family. Any target application first needs a separately justified finite encoder, framing/invertibility/transport contract, public-equation deduplication, state-size/utility review and distinct finite authority. No target model is currently admitted. All 72 canonical families and original 100 drafts are unchanged; three proposals target-tested, 97 target-unrun, A01 blocked.

Current selection after this closeout: C02 prefix-code/Huffman framing source/proof audit only, checking exact tree/framing/prior-art and nontrivial utility before implementation. No experimental allocation or target admission.
