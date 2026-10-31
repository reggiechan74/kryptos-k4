# Hypothesis history — archived scheduling and dated notes

**Historical reference only; not a working queue.** Read [HYPOTHESES.md](HYPOTHESES.md) for current status and the single next-action queue. New chronological receipts belong in [EXPERIMENTS.md](EXPERIMENTS.md), not this archive.

This companion preserves the pre-reorganization opening and historical notes from commit `89f150e5baf46d11ad06419df8ccbd56cb9da395` (31 October 2026) without rewriting their contents. Old “next”, “unrun” and authorization language describes its original moment and may be superseded. In particular, studies 060–063 and the 810-cell tableau audit are complete to their stated bounds; the old next-transcription instruction is stale. No historical proposal here grants current execution authority.

- [Former opening, study summaries and queues](#archived-opening)
- [Dated research notes](#historical-entries-preserved)
- [Current family register](HYPOTHESES.md#family-records) · [Experiment chronology](EXPERIMENTS.md)

## Archived opening

<details><summary>Expand the original opening and superseded queues (unaltered snapshot)</summary>

<!-- ARCHIVED-OPENING:START -->
# Hypothesis log

Use [the template](templates/hypothesis.md) for new hypotheses. Exact structural
proofs and finite tests have separate scope; compatibility is not a solution.

## Working to-do list and current status — 31 October 2026

**This is the canonical reference for deciding what to test next.** Consult it before selecting an experiment and reconcile it at the end of every run, including a failed, interrupted or inconclusive run. The [agent workflow](../AGENTS.md) makes this check mandatory. The [experiment log](EXPERIMENTS.md) records our individual runs. The [external hypothesis and prior-art register](EXTERNAL-PRIOR-ART.md) records other researchers’ attempted models, source pins and evidence limits; both registers must be checked before selecting work. Generated trackers are navigation, not a second source of truth.

- **Published through study 063; execution and independent audit complete.** Studies 058 and 059 artifacts and their reconciled tracking are published together. The table below reconciles the latest studies. A completed bounded test is not an eliminated broad hypothesis.
- **Study 057 (Q-01) is complete: exact bounded exclusion, independently audited.** Queue rank is a recommendation, not authorization by itself. The user separately authorized continuation through this queue on 31 October 2026. Q-02 is complete in 058; the bounded +1-feedback Q-03 pilot is complete in 059. Q-04 and Q-05 were not run because their prerequisites were not established. Target evaluation still requires the frozen benchmark and independent audit gates.
- **Public prior-art gate (31 October 2026):** the external survey found substantial overlap with our completed studies. At that survey closeout, no proposed new execution-ready hypothesis cleared the not-already-tried requirement. The later [four-family proposal and independent review](fresh-program-20261031/README.md) supplied new bounded mechanisms; execution was separately authorized at 15:03 UTC. Stronger-solver reruns, completion of attempted searches and cosmetic parameter extensions are not eligible next tests under the current direction. Proposed-but-unrun models may qualify only after precise overlap and analytical-subsumption checks. This is not a claim that no untried model exists. See [external records and admission procedure](EXTERNAL-PRIOR-ART.md).
- **Next-action decision:** Q-01–Q-03 are closed only within studies 057–059 bounds. No eligible Q-04/Q-05 run is currently justified: exact production search is fast and no compatible K4 candidates remain to rank. Subtractive feedback and other omitted model settings remain untested and require a new frozen scope, not automatic expansion.
- **Stopped branch:** direct aligned English-running-key decoding did not pass study 055's screen. Do not reopen it merely because an unrestricted decoder was never built. Study 056 also found no demonstrated learned-conflict advantage.

- **Evidence closeout, not a cipher test:** The [independent 810-cell tableau audit](tableau-cell-audit-20261031/REPORT.md) found 806 agreed letters (774 high-confidence, 32 tentative), one agreed unreadable and three disagreements. Four cells remain unresolved; no reproducible high-confidence noncyclic entry or supported mechanism was established. Close this avenue without filling uncertain glyphs or enumerating them as keys. Reopen only on better evidence or separately grounded semantics. The K4 goal stays open; no fifth execution-ready model is admitted. [Next research decision](fresh-program-20261031/NEXT-DECISION.md).

### Recent completed tests

| Study | Exact tested scope | Outcome and evidence | Remaining gap / next action |
| --- | --- | --- | --- |
| 051 | 32 frozen messages; 12 tableaux; periodic/plaintext-autokey/ciphertext-autokey lengths 1–32 | **Completed, narrow negative:** all three gates failed; p = .916; no exact structural fit. [Report](candidate-first-051/README.md) | Outside-bank plaintexts and natural-language key inference were not tested. The failed expansion gate remains failed; 052 was separately authorized. |
| 052 | 1,024 new frozen messages under the same structural-key model | **Completed, narrow negative:** all three gates failed; p = .519; no exact structural fit. [Report](candidate-first-052/README.md) | Not all possible plaintexts or key generators. Preserve omitted raw-control inventories; do not interpret the standalone p-value as project-wide evidence. |
| 053 | The 1,024-message bank, 12 fixed tableaux, order-4 scoring of induced English keys | **Completed, narrow negative:** all four criteria failed; p = .932. [Report](candidate-first-053/README.md) | Not open-vocabulary joint decoding; 054 and 055 separately tested source lookup and forced-fragment feasibility. |
| 054 | 89 frozen documents, 17,619,191 eligible 97-letter windows, 12 tableaux and fixed fragment spacing | **Completed, exact bounded corpus exclusion:** zero source matches. [Report](candidate-first-054/README.md) | Other sources, editions, normalization and layers remain untested. No approximate-match or corpus expansion is authorized by this negative. |
| 055 | Direct aligned running-key fragments under 12 fixed tableaux; calibrated order-4 local-English screen | **Completed, heuristic screen negative:** 17/17 calibration gates passed, then 0/12 target pairs survived. [Report and audits](candidate-first-055/README.md) | Not an impossibility proof for all English keys. Stop the direct decoder under this screen; no decoder was launched. |
| 056 | Standard A–Z Vigenère then unpadded ragged columnar; all emission orders, widths 6–9, nominal periods 2–8, fixed alignment/top-down reads | **Completed, exact bounded exclusion:** independent reference covered 2,862,720 route/period trials; zero compatible solutions. [Target and benchmark audits](candidate-first-056/README.md) | Those gaps were subsequently addressed only within studies 057–059 bounds; other settings remain untested. Original resource-monitor defect and fresh corrected benchmark remain disclosed. |
| 057 | AZ/KRYPTOS plaintext and ciphertext alphabet roles, sign ±; nominal periods 2–8; all ragged-columnar orders, widths 6–9, arithmetic then transposition | **Completed, exact bounded exclusion:** both engines return zero solutions; reference 22,901,760 route/period/convention trials, including the 056 baseline. [Report and audits](candidate-first-057/README.md) | Close Q-01 only for these bounds; reverse stage order was subsequently tested in 058 and bounded feedback in 059. |
| 058 | Unpadded ragged columnar first, widths 6–9 and all orders; then output-index periodic arithmetic, periods 2–8, eight AZ/KRYPTOS role/sign conventions | **Completed, exact bounded exclusion:** both engines return zero compatible key cylinders; independent reference 22,901,760 descriptive trials. [Report and audits](candidate-first-058/README.md) | Close Q-02 only within these bounds. Free-key ambiguity and period aliases were retained; the bounded +1-feedback Q-03 pilot was subsequently tested in 059. Artifacts published. |
| 059 | Plaintext or intermediate-ciphertext autokey with feedback coefficient +1; eight AZ/KRYPTOS role/sign conventions; primers 1–8; then all ragged-column orders, widths 6–9 | **Completed, exact bounded exclusion:** both target engines return zero primer cylinders; independent reference 52,346,880 descriptive trials. [Report and audits](candidate-first-059/README.md) | Close Q-03 only for this pilot. Subtractive feedback is distinct and untested. Q-04/Q-05 prerequisites not established; artifacts published. |
| 060 | Ciphertext-driven alphabet exchange and fixed-reference-index prefix reversal; AZ/KRYPTOS reference and initial alphabets; 26 pointers/offsets per arm | **Completed, exact bounded exclusion:** both engines UNSAT_COMPLETE, zero compatible descriptions/plaintexts; 208 distinct functions certified. [Report](candidate-first-060/README.md) | Not all evolving alphabets. Artifacts published; select Q-07 only after this ledger reconciliation and its own gates. |
| 061 | Sum-locked right block rotation after periodic addition; AZ/KRYPTOS, widths 3–12, periods 1–8; zero key already analytically covered | **Completed, exact bounded exclusion:** both engines UNSAT_COMPLETE, zero compatible key cylinders in 160 structural cases. [Report](candidate-first-061/README.md) | Not nonlinear block ciphers generally. Artifacts published; next Q-08 ciphertext-steered Josephus requires its own overlap and validation gates. |
| 062 | Ciphertext-steered Josephus deletion; AZ/KRYPTOS, 97 starts, two fixed directions, emission-key periods 1–8; prior zero-key domain excluded | **Completed, exact bounded exclusion:** both engines UNSAT_COMPLETE; zero compatible cylinders across 3,104 structural descriptions / 388 target maps. [Report](candidate-first-062/README.md) | Not all data-dependent routes. Artifacts published; next Q-09 coupled carry requires new equivalence/validation gates. |
| 063 | Coupled 26/24 accumulator, OLD-high-digit readout; AZ/KRYPTOS, periods1–6, all624 initial states, zero keys included | **Completed, exact bounded exclusion:** both engines UNSAT_COMPLETE, zero compatible tuples. [Report](candidate-first-063/README.md) | All624 blind plants had8–126 plaintexts; no unique-recovery claim. Artifacts published. All four fresh families closed only within frozen bounds; [next research decision](fresh-program-20261031/NEXT-DECISION.md), no fifth target admitted. |

### Fresh authorized queue — after the public survey

Only exact mechanisms not located in the inspected prior record advance; this is not a worldwide novelty guarantee. Each target requires its own frozen protocol, independent implementation, tiny exhaustive checks, fresh blind controls and audit approval. The original proposals are [retained here](fresh-program-20261031/README.md).

| Queue ID | Family and bounded proposal | Current decision |
| --- | --- | --- |
| Q-06 | H-EVOLVING-ALPHABET: 104 exchange and 104 prefix-reversal functions | Study 060 complete: exact bounded exclusion; no rescue tweaks. |
| Q-07 | H-SUM-ROTATION: AZ/KRYPTOS, block widths 3–12, key periods 1–8, 160 structural cases | Study 061 complete: exact bounded exclusion; prior zero-key coverage separated, no rescue changes. |
| Q-08 | H-CIPHERTEXT-JOSEPHUS: 388 start/orientation/alphabet routes, periods 1–8, 3,104 structural cases | Study 062 complete: exact bounded exclusion; free-key ambiguity preserved and zero-key prior coverage separated. |
| Q-09 | H-CARRY-624: coupled 26/24 state, all 624 initial states, AZ/KRYPTOS, periods 1–6 | Study 063 complete: exact bounded exclusion, not unique recovery. All624 blind plants ambiguous; global reachability enforced. |

### Historical ranked queue and current eligibility

The first three proposals below were executed as studies 057–059; their original decisions are retained as history. Their local coverage is not a worldwide novelty claim. Q-04/Q-05 remain unrun and are not automatically eligible if a bottleneck later appears: they also require a genuinely untried hypothesis and public prior-art clearance. The superseded ten-item residual/recovery shortlist from the subsequent survey is not queued. Original proposals came from the [research comparison](strategy-review-20261031/REPORT.md); that dated report is not current execution authority.

| Priority / queue ID | Proposed test and family | Status | Required first action and go/no-go | Evidence / dependency |
| --- | --- | --- | --- | --- |
| 1 / Q-01 | KRYPTOS-alphabet and distinct Beaufort extensions of 056 across all column orders; widths 6–9, periods 2–8. Related family: H-ROUTE. | **Completed: 057 exact bounded exclusion** | All 520 blind checks and independent target audit pass; no compatible K4 solution. Close this bounded item and advance to Q-02. Full 97-position maps remove aliases; the 056 baseline is not new coverage. | [057 findings and audits](candidate-first-057/README.md); [earlier restricted routes](BOUNDED-FINDINGS.md); [050 closure](HAND-GRAMMAR-050-FINDINGS.md). |
| 2 / Q-02 | Reverse the stages: columnar transposition before periodic arithmetic, across the same free column orders and initial bounds. Related family: H-ROUTE. | **Completed: 058 exact bounded exclusion** | All 520 blind feasibility/ambiguity checks and independent target audit pass; zero compatible K4 cylinders. Close only this domain and advance to Q-03. Unconstrained keys and nominal-period aliases were represented exactly, not filled with English. | [058 findings, protocol and audits](candidate-first-058/README.md); [earlier fixed-route coverage](BOUNDED-FINDINGS.md). |
| 3 / Q-03 | Plaintext- or intermediate-ciphertext autokey then unknown columnar; +1 feedback, eight alphabet-role/sign conventions, primers 1–8 and widths 6–9. Related families: H-AUTOKEY-EXACT, H-MASK-AUTO, H-ROUTE. | **Completed: bounded 059 exclusion** | All 600 blind feasibility/ambiguity checks and independent target audit pass; zero target cylinders. Subtractive feedback remains untested and is not an arbitrary-primer alias. | [059 findings and audits](candidate-first-059/README.md); [direct-alignment predecessor](AUTOKEY-CONSTRAINT-FINDINGS.md). |
| 4 / Q-04 | Structure-aware stochastic search for one admitted composite family; compare multistart local search with MCMC/annealing, and tempering only if trapping is observed. Method pilot, not a new family. | **Not run; prerequisite not established** | Studies 057–059 showed no production-search bottleneck; independent exhaustive verification time is not one. A future pilot first needs a genuinely untried model passing the public prior-art gate and an actual exact-search bottleneck. Freeze one model and equal-compute benchmark. Advance only for improved exact recovery without increased false selection; heuristic failure never excludes the family. | [Research comparison](strategy-review-20261031/REPORT.md); [Chen and Rosenthal](https://probability.ca/jeff/ftpdir/decipherartpub.pdf). |
| 5 / Q-05 | Whole-text neural scoring inside a cipher-constrained decoder. Method pilot, not an unconstrained plaintext generator. | **Not run; prerequisite not established** | No compatible K4 candidates remain in the tested families, so no ranking bottleneck was established. For a separately justified, genuinely untried model passing the public prior-art gate, first test true-solution versus wrong-candidate ranking on source-disjoint 97-letter fixtures. Only then compare constrained beam search; require recovery and false-positive improvements over existing n-grams. | [Research comparison](strategy-review-20261031/REPORT.md); [Kambhatla et al.](https://aclanthology.org/D18-1102/). |

### Next evidence task (not a fifth cipher experiment)

Independently transcribe the 810 cells of public IMG_1223; freeze literal readings before comparison with expected cyclic KRYPTOS rows. Keep uncertain cells explicit. Parent coordinates this separately; no marked-letter key search or K4 test is authorized by this task. See the [next research decision](fresh-program-20261031/NEXT-DECISION.md). Not run in this closeout.

### Required end-of-run reconciliation

Before marking any run finished or selecting the next item, check and reconcile [external prior art](EXTERNAL-PRIOR-ART.md), then update its exact tested bounds, completion/outcome, evidence and audit links, remaining uncertainty, blockers and next action in this ledger and [EXPERIMENTS.md](EXPERIMENTS.md). Record interrupted/resource-limited runs as inconclusive unless a narrower completed result is justified. Review queue order and state why an item advances, stops or remains blocked. Update reviewed classifications and regenerate the navigation as [AGENTS.md](../AGENTS.md) specifies. Keep original frozen reports, failed gates and corrections intact; publication status is separate from scientific status.

<!-- ARCHIVED-OPENING:END -->

</details>

<!-- ARCHIVED-NOTES:START -->

## Historical entries (preserved)
| ID | Claim | Evidence class | Related sources | Experiment IDs | Status | Narrow conclusion |
| --- | --- | --- | --- | --- | --- | --- |
| H-PERM | A literal permutation-only pipeline produces K4 | Hypothesis | Fixed public cribs | STRUCT-001 | Contradicted under stated model | E counts cannot match; no substitution component tested |
| H-PERIOD | Untransposed fixed bijection per periodic phase | Hypothesis | Bean 2021; crib equality | STRUCT-001 | Partly constrained | Exactly 19 periods rejected among 1–96; others unproven |
| H-LANGUAGE | A language/script representation precedes encryption | Hypothesis | Historical alphabet source receipt | STRUCT-001; LANG-001 | Restricted encoding audited; complete pipeline unspecified | GOST literal/fixed-character transport models fail under their stated domain; Shavian transport/English inverse unspecified |
| H-ROUTE | One listed route plus fixed-alphabet periodic arithmetic | Hypothesis | K1–K3 controls; width observations | ROUTE-001 | Finite cases constrained | No listed nonidentity-route model survives at periods 1–16; 282 identity-route fits are vacuous |
| H-RUNKEY | Literal nearby solved text is a nonwrapping running key | Hypothesis | Corrected K2 and K3 | RUNKEY-001 | Tested finite version rejected | None of 28,488 declared cases matches all cribs |
| H-TRIFID | A literal fixed cube implements K4 | Hypothesis | Historical availability; no attested lesson | TRIFID-001 | Tested finite versions rejected | None of 144 declared cases matches all cribs |
| H-LAG | Width-21 repeated pairs differ from histogram-preserving permutations | Published diagnostic | Bean 2021 | STAT-001 | Limited replication | Count 11 confirmed; maximum-over-48 conditional tail about 0.0108, no mechanism inferred |
| H-MASK-AUTO | One fixed-primer autokey procedure explains K4 | Exploratory historical mechanism, not identified Scheidt method | Army TM32-220; existing K1/K2 keys as inference | MASK-AUTO-001 | 12 fixed cases rejected | All regenerate C but fail the English cribs; broader autokey remains open |
| H-MASK-FM | One of two literal Fractionated Morse maps explains K4 | Exploratory historical mechanism | ACA procedure/index; Morse artwork connection | MASK-FM-001 | Two fixed cases rejected | Both streams contain invalid internal xxx; no broader keyed/composite family conclusion |
| H-WORD-SCRAMBLE | Preserve endpoints and permute word interiors before a cipher | User-proposed hypothesis, not established history | Fixed WORD-SCRAMBLE-001 specification | WORD-SCRAMBLE-001 | 24 fixed combinations rejected | Both assumed segmentations fail endpoints for all 12 frozen autokey settings; broader pre-scrambling plus cipher remains open |
| H-PHONETIC-RESPELLING | English → stylized pronunciation respelling → cipher | User-proposed, not a historical Sanborn claim | User examples; bounded specification pending | PHONETIC-SUBSET-001 only | Length-preserving subset: no rescue; broader model unspecified | W→V, voiced TH→Z, unvoiced TH→S, short I→EE, final D→T, final G→K are not universal German pronunciation. Lossy/length-changing rules need an exact inverse; no flexible mapper or crib shifting |
| H-GERMAN-TRANSLATION | English → one specified German rendering → cipher | User-proposed translation hypothesis | User proposal; bounded specification pending | No run | Missing exact rendering/inverse/codebook | Word order and length may change. No translator-choice fitting, shifted English crib positions, or claim that Berlin proves a German layer |
| H-GEO-ENE | The World Clock may be ENE of another referenced place, or a reference may lie ENE of it | User-proposed geographic hypothesis with supplied source receipt | OSM centers and Berlin monument record; geographic note | No cipher run | Approximate, nonexhaustive geometry only | Fountain→clock about68.25°/471m versus ENE67.5°; no key or intentional Kryptos link established, no landmark search expansion |

H-WORD-SCRAMBLE concerns interior permutation, not the K1 IQLUSION or K3
DESPARATLY spelling anomalies. Readability is conditional; SALT/SLAT and
FORM/FROM show that preserving endpoints does not identify an original word.
An explicit retained schedule is invertible; discarding it leaves ambiguity.

H-PHONETIC-RESPELLING (requested as H-PHONETIC-RESPelling) is an English
respelling layer, distinct from H-GERMAN-TRANSLATION. Neither was added to the
completed finite runs. A fixed rule domain, ambiguities/losses, cross-layer
alignment, exact English inverse, and cipher/key scope must precede a search.

The narrow W/final-D/final-G subset was subsequently registered and checked in
PHONETIC-SUBSET-001. It leaves all known words unchanged and rescues none of the
12 fixed outputs. TH/I changes and German translation remain outside that run.

## Geographic branches and extraction gate

The [1985 period-map report](../docs/berlin-period-map-corridor.md) separates
H-GEO-ENE's clock-terminal approach (Neptunbrunnen WSW → clock ENE) from a
geometric-midpoint model. The latter fixes the reflected point at
52.52273224799, 13.41976896153; it must not be snapped to a named landmark.
Current walking halves 532 m and 622 m make the clock unequal as a walking
midpoint. Period map geometry supplies no printed gateway/Tor label; gateway
wordplay is a modern architectural interpretation. German-initial extraction
has no unique route, names, eligibility or tie rules and remains uninstantiated;
no forced ten-feature list or key has been produced.

## H-ENIGMA-DIRECT

The direct aligned standard wartime reflector Enigma model is contradicted by
one-based position 74: plaintext K and ciphertext K. See the
[proof and exact scope](../docs/direct-enigma-boundary.md), DIRECT-ENIGMA-001.
Extra transforms and other Enigma/composite models are outside this conclusion.

## H-NEPTUNE and H-CLOCK-FACE — supplied research, no cipher run

The [bounded Neptune/clock-face assessment](../docs/neptune-discovery-assessment.md)
records a real Neptune → Le Verrier → Berlin history without a documented bridge
to Kryptos. The residual-inference analogy is methodological; NEPTUNE/Hora XXI
key material lacks a unique extraction rule. The actual discovery observatory
→ clock bearing is reported near 34°, contradicting that specific ENE route.

Keep both fountain/clock source pairs: pinned OSM centers yield the earlier
reported 68.25°/471 m; the new secondary points yield reported 67.76°/470 m.
Neither is exact ENE; the earlier geometry and fixed reflected point remain pinned.
See the report for every input coordinate and provenance limitation.

BERLINCLOCK/KRASNOJARSK both having 11 letters is the user's weak length
coincidence. A modern photo suggests an Asian arc roughly east but verifies
neither the absolute true-ENE panel nor 1989 inscriptions. SINGAPUR is German
spelling, not an error. An ENE approach from the fountain sees the opposite
WSW-facing side. No city name is a confirmed key; no cipher pilot was run.

## H-CLOCK-RESET — specification pending

The [reset preflight](CLOCK-RESET-PREPARATION.md) records prior period-11
arithmetic exclusions and independent synthetic boundary controls. The pending
shared-key-reset pilot is a distinct model. No actual K4 run precedes the frozen
specification commit. KRASNOJARSK is a candidate hypothesis only; the confirmed
BERLINCLOCK crib is unchanged.

Independent review subsequently supplied the [exact reset contradiction](CLOCK-RESET-PROOF.md):
positions 25/67 lie at offset 3 after starts 22/64, with T/L mapping to V/V.
The declared identical restarted positionwise bijection cannot satisfy that.
The proof/regression implementation is prepared but awaits final specification
before execution; no keyword scan or rescue variant has been run.

CLOCK-BOUNDARY-REG-001 subsequently completed after specification commit
4e2d002925bfc7f3b332f94cd4472617919f52fa and implementation commit
000b8c3a4e480fd773f131cf85eef6bc30d47206. All 13 known certificates and declared
controls verify; 72 fixed formal period-11 cases are analytically subsumed, zero
candidate-search trials. The shared-reset collision concerns identical restarted
positionwise bijections; transposition, feedback and different keys remain outside
scope. See [completed proof and receipts](CLOCK-RESET-PROOF.md).

## H-CLOCK-FACE — dated photographic update

The [historical-inscription report](../docs/historical-clock-inscriptions.md)
preserves the worker's direct inspection of dated 1972, 1984, 1989 and 2015
photographs. Differences occur even before 1990; a generic pre-restoration image
cannot establish 1989. Exact true-ENE orientation and the full 1989 candidate
panel remain unresolved. External source links/attribution are provided; no local
image crop is claimed uploaded. The clock-reset proof and its scope are unchanged.

## H-EGYPTIAN-SIGN-LIST

User-proposed hieroglyphics hypothesis; [evidence and feasibility boundary](../docs/egyptian-sign-list-feasibility.md).
Egypt has genuine context through K3's Carter text and the reported 2025
Egypt-trip clue, but no hieroglyphic mechanism is proven. The Met's printed
pages 47–48 describe approximately 24 single consonants, bi-/triliterals, word
signs, silent determinatives, vowel omission and reading orientation. Gardiner
1927 is historical availability, not an artist link. Exact edition, sign
selection/mapping, direction, normalization, inverse and key are missing.
No invented 26-glyph alphabet or Unicode arithmetic was implemented. Simple
one-to-one glyph renaming alone inherits the excluded monoalphabetic model;
layered models are not excluded. No new search or experiment.

## Prior-art scope update — 2026-10-18

The [pinned Barney/Scott review](../docs/prior-art-barney-scott-review.md) treats
maps as experiment indexes and retires exact duplicated configurations only.
Existing periodic-bijection proofs already subsume their selected collision
observations; our complete identity-period/running-key ledgers, opposite Trifid
direction, missing longer-primer autokey cases, full-stream Morse parses, word
invariants, sourced codecs and dated clock evidence are preserved.

H-KRYPTOS-FINGERPRINT is descriptive only: 9/10 known KRYPTOS-member positions
fit AZ circular distance at most 2, but only K/O/R/S/T occur, with no P/Y. The
biconditional has three known-crib exceptions. The selected pattern and proposed
90% extrapolation are not hard candidate filters; signal.log's corrected .0029
belongs to a different 15-statistic family. No fingerprint null search was rerun.

Interrupted-key rules, fully constrained Gromark completion and Wheatstone27/26
remain narrowly specifiable leads. No success, new experiment or general family
elimination is claimed. The identical shared-reset proof retains its assumptions.

## H-AUTOKEY-EXACT — threshold-free direct audit

[AUTOKEY-CONSTRAINT-001 findings](AUTOKEY-CONSTRAINT-FINDINGS.md) classify all
1,152 forward same-alphabet configurations (AZ/KRYPTOS, three equations, PT/CT
feedback, arbitrary independent primer of lag1–96): 732 contradicted, 420
compatible but underdetermined, zero untested. Every compatible case has zero
independent consistency checks. No primer was searched or filled and no full
plaintext produced. PT lag26 is rejected by propagation22→48→74 even though no
immediately known predecessor pair exists. This closes the declared chain/
threshold gap, not all autokey. Earlier fixed-primer results remain historical.

## H-GROMARK-ONE — complete alphabets exist for one published tuple

[GROMARK-ALPHABET-001](GROMARK-ALPHABET-FINDINGS.md) selects the first printed
Barney tuple at the pinned commit: base16, lags5/6, primer6,12,12,4,4,8. Local
cycle/injectivity checks pass; complete global alphabet bijections also exist.
Our witness and an independent supplied witness both satisfy all24cribs and full
regeneration, but differ outside cribs at the same fixed global gauge. Arbitrary
completion is not recovered historical alphabets, meaningful plaintext or a K4
solution. No width21/fingerprint filter, other survivor or mass sweep was used.

## H-CLOCK-FACE — 1972 transcription correction, 2026-10-18

The [dated evidence report](../docs/historical-clock-inscriptions.md) now records
PEKING / HANOI / MANILA for the installed clock's 28 March 1972 lower panel,
following the parent's independent visual recheck. The earlier SHANGHAI reading
is explicitly superseded with its original commit retained; 1984/2015 readings
are separate. The Narva museum model has different ring placement and cannot
stand in for the installed 1989 clock. Its museum page records a 1972 gift and
separate 1968 metadata; the 48-image layout assessment is attributed to the parent.
Exact ENE calibration/full 1989 panels remain unresolved. The reported 1968 study
source was subsequently supplied and is linked in the evidence report; it has no
orientation calibration. No cipher hypothesis, key or scoped result was changed.


Final bounded clock-source review: 1968 perspective studies supply no north
reference or inscription schedule. The 2024 Kunsch interview identifies possible
archival construction documents and original letter patterns, whose unpublished
contents were not inspected and may not resolve the 1989 state. No public
north-referenced face plan/full 1989 list was found in the supplied review. This
negative is bounded; no outreach or new cryptanalytic search was performed.

## H-GROMARK-ONE — exact marginal identifiability

[GROMARK-IDENTIFIABILITY-001](GROMARK-IDENTIFIABILITY-FINDINGS.md) freezes the
same tuple and verifies all 73 noncrib difference-existence queries: 10 conditionally
forced, 63 variable, 0 unresolved. All variable cases have complete checked alphabet
counterexamples; all forced cases have exact component proofs. These are not new
confirmed cribs or a recovered message. Marginal variation does not remove joint
constraints or permit combining witnesses. No new primer, score or K4 search
fallback was used. Stop here pending an independently supported alphabet/key
construction restriction or new confirmed evidence; see the strategy note.

## H-SILK-PERIODIC — fixed photographed chart

[Exact bounded proof](SILK-PERIODIC-FINDINGS.md): hypothetical direct periodic
keys 1–12 are contradicted by the 13 distinct required keys at positions 22–34.
No claim about nonperiodic/OTP keys, longer periods, other tables or added layers.
Historical creator use and authentic repeated-key doctrine are unestablished.

## Stateful key continuation — 2026-10-22

[DYNAMIC-KEY-001](DYNAMIC-KEY-FINDINGS.md) ranks three distinct mechanisms:
H-ASYMMETRIC-FEEDBACK (unrun; next priority, explicitly reindexes feedback across
independent alphabets), H-CIPHERTEXT-EXTRA-STEP (96 finite configurations rejected),
and H-AFFINE-DIGRAPH (unrun; pair coupling with explicit odd-edge rule). Their
models, controls and falsification gates are recorded in the findings.

The same run rejected 1,248 progressive-cycle configurations. Subsequent pinned
source inspection identified direct progressive prior art in cokernel.py/gap1.py;
this part is a controlled local replication, not a new mechanism or a threshold
coverage gap. Four first-crib fits fail Berlin with only 0–1 of 11 matches.
199 whole-family shuffled controls provide no useful excess of crib agreement.
No model fits all 24 known letters; no solution or new plaintext is claimed.

## Fixed feedback/stepping outcomes — 2026-10-22

- H-ASYMMETRIC-FEEDBACK: ASYMMETRIC-PRIMER-001 tests precisely six AZ/KRYPTOS
  role triples, PALIMPSEST, lag 10, addition; zero candidates. Scores
  1,1,0,1,1,5 out of 24. The best still fails 19 confirmed letters. Its six-model
  conditional shuffle tail .015 is exploratory and does not change rejection.
- H-PLAINTEXT-EXTRA-STEP: PLAINTEXT-STEP-001 tests three fixed words, two
  alphabets, vowel/consonant after-plaintext steps of 1/2: twelve cases, zero
  candidates, best 3/24, whole-family conditional shuffle tail .54.
- Alongside the earlier ciphertext-driven step mechanism these supply three
  distinct tested mechanisms. Progressive remains known prior-art replication.
- ASYMMETRIC-FEEDBACK-001, the registered 72-case arbitrary-primer design, was
  superseded for execution by the narrower parent-supplied pilot before code or
  scoring. It remains DEFERRED/UNRUN; no general autokey-family exclusion follows.
- Updated ranked interpretation, controls and exact scopes:
  [FIXED-PILOT-FINDINGS.md](FIXED-PILOT-FINDINGS.md). No solution is claimed.

## H-SPLIT-COORDINATE-ROUTES — proposed, unrun

Low-evidence coordinate-fractionation hypothesis: AZ/KRYPTOS letters become
row/column pairs in fixed row-major 2x13 or 13x2 grids. Independently route the
two 97-coordinate streams through ragged row-fill/column-read permutations of
widths 7 and 21, either assignment and forward/inverse independently; recombine.
32 formal cases, with equivalence/deduplication still to verify. No padding,
shifts, fitted alphabet or extra substitution. Unlike whole-letter permutation,
independent coordinate re-pairing can change letter counts; unlike 2x13 modular
addition, this is separate stream routing. Widths 7/21 are postselected diagnostics,
not independent clues. Global novelty and creator use are unproved.

Proposed gates: all 24 confirmed letters, full97 regeneration, 32 independently
verified planted inverse controls and 199 whole-family shuffled maxima, under a
new committed specification before any execution. **No experiment or score.**
Source context and exact scope are documented in the
[unrun proposal](FIXED-PILOT-FINDINGS.md#h-split-coordinate-routes--unrun-low-evidence):
[Friedman Part IV](https://www.nsa.gov/portals/75/documents/news-features/declassified-documents/military-cryptanalysis/mil_crypt_IV.pdf)
and [LANAKI Lesson 17](https://www.cryptogram.org/downloads/LANAKI%20Crypto%20Lessons/LESSON17.pdf).
The 1996 lesson is explanatory, post-installation context; neither source
establishes the exact proposed recipe or a Kryptos connection.

## Completed continuation — 22 October 2026, 19:19–19:21 UTC

The earlier unrun/deferred statuses are superseded by
[CONTINUATION-FINDINGS.md](CONTINUATION-FINDINGS.md):

- ASYMMETRIC-FEEDBACK-001: all 72 mixed-role AZ/KRYPTOS configurations at PT
  lags 9–12, three equations, contradict the cribs for **every primer**. One
  first-crib survivor has lag 12 and only one training check; its fixed roots
  predict 2/11 Berlin letters. No all-crib fit or full plaintext candidate.
  All-crib equality checks are 24-L, training checks 13-L; all lanes are trained.
  Best modal-root agreement 15/24, 35/199 shuffled maxima equal/higher, tail .18.
- SPLIT-COORDINATE-001: 32 formal cases are 32 exact distinct transformations.
  All fixed AZ/KRYPTOS coordinate-route cases fail, best 3/24. Full-family
  shuffled maxima equal/higher 160/199, tail .805. Widths 7/21 remain postselected.
- Each actual run completed once after specification/code commits. Null scans
  repeat fitting and selection end-to-end for the relevant family; .005 is the
  minimum plus-one tail with 199 controls. No global multiple-testing correction
  or independently obtained validation text is claimed. Regeneration is not
  evidence of a decoding. Final suite: 174 tests pass in 9.324 seconds.
- The provisional K3-derived two-stage route family is NOT implemented. Existing
  ROUTE-001 covers both component widths and periods 8/10, but exact composite
  overlap must await the full route definition and reference control.

## K3 and 24-sector route families — completed 22 October 2026

The full parent-frozen route definition arrived after the earlier provisional
status. [K3-CLOCK-ROUTES-001](K3-CLOCK-ROUTE-FINDINGS.md) completed once:

- H-K3-COMPOSITE-PERIODIC: U14 after U42 reproduces all 336 canonical K3 letters
  and the existing position permutation. Its 97-position permutation is new to
  the old catalogue. All four period-8/10, unrestricted-key, additive KRYPTOS
  single-layer-order cases fail already within the first crib.
- H-K3-SANDWICH: both period pairs (8,10)/(10,8) fail graph cycle constraints.
  c_train=5, c_all24=1, c_full=1 in both cases; first-crib training has zero
  cycle checks and four plaintext-relevant free offsets. There are seven joint
  held-out compatibility checks, only one/two individually predictable Berlin
  edges, all failing. Actual compatible keys and plaintexts are zero.
- H-CLOCK-24-ROUTE: 96 distinct routes / 384 raw structures; sixteen cases are
  exact prior equivalents in route, key domain, period, equation, alphabet and
  layer order and were skipped. All 368 new cases fail. No sandwich was skipped
  on the basis of a one-layer prior result.
- All 374 new structures rejected; no null simulations needed or run. No K4
  plaintext candidate, worldwide novelty, optical or Site claim. The public
  sources motivate the number 24, not the ragged route grammar.
- Full suite: 187 tests pass, including independent certificate/skip audits.
  No width/period/direction/layer was added after the results.

## H-OCCUPIED-CELL-FIXED — completed separate pilot, 22 October 2026

Verified K4 text mask: OBKR in first-row columns 28–31, three full 31-character
rows afterward. Eight columnwise/inverse routes are absent from both prior
route catalogues, so no unrestricted-key prior negative covers them. The eight
routes with PALIMPSEST/ABSCISSA, all eighteen phases, both layer orders yield
288 exact unique fixed branches; all rejected, best 5/24 fails 19 known letters.
No fitted keys or null simulation. This is textual occupancy, not surveyed
physical geometry; row-prefix cells are excluded from K4, not missing copper.
[Findings](OCCUPIED-CELL-FINDINGS.md) preserve exact scope and full outputs.
Final regression suite: 195 tests pass. No new family added after scores.


## 22 October: four-track execution after strategy comparison

The four fixed AZ/KRYPTOS role-pair move-to-front models proposed in the strategy
reset are now **tested and rejected**, each0/24. This changes the substitution
permutation, not merely a cursor: reachable-state next-letter maps lie outside
the prior affine-tableau superset. No global evolving-alphabet exclusion follows.
See [STRATEGY-FOLLOWUP-001](STRATEGY-FOLLOWUP-FINDINGS.md) for full frozen scope,
blinded planted/nearby/decoy controls and exact contradiction receipts.

K1/K2 construction-stage accounts pass known-answer controls; they are not new
K4 algorithms or corrections. Historical clock data support a shared-phase
visible-hour control but leave a K4 letter operator underidentified. Exact toy
compatible-volume calibration passes its oracle/gauge checks while exposing
ambiguity and null compatibility. Broader classifier and independent recurrence
results are not counted as locally executed work here.


### Follow-on independent evidence, same date

A published Cyrillic Projector pair now passes local fixed-convention replay
(1133letters, reset at778). This supports message-boundary phase handling in that
later artwork, not a physical3letter omission or transferable K4 algorithm.
The supplied bounded affine-feedback recurrence is exactly contradicted by
internal EASTNORTHEAST transitions in both alphabets; local proof verification
did not duplicate the independent parameter run.
See [follow-on audit](STRATEGY-FOLLOWUP-FINDINGS.md) and preserve scope/overlap.


## Single shared-state boundary initialization — 22 October 2026

Weak later-art motivation from the CP semantic phase change was tested without
assuming a K4 sentence boundary. Exactly one unknown internal reset, to the same
original state/seed/key, does not rescue the four fixed move-to-front mappings,
the registered two-alphabet affine-feedback grammar or periodic arithmetic of
periods 1–12. All reject the first crib under the bounded audit.

The move-to-front doublets and independent within-island recurrence contradictions
provide short exclusions; a fixed-four local corollary concerns arbitrary reset
timing analytically and is not a new sweep. Neither excludes all message-based
initialization or other alphabets/rules. Uncertain boundaries create real planted
plaintext ambiguity; it is reported rather than treated as a unique recovery.

[Full frozen scope, exact counts and independent replay](SINGLE-BOUNDARY-RESET-FINDINGS.md).
The bounded test stops here; no automatic second reset or new cipher family.


## Autonomous multi-step mathematical key generator — 22 October 2026

The user-approved finite audit of orders 2–6, homogeneous/affine, in AZ/KRYPTOS
coordinates is complete: all 20 formal structures fail the first crib modulo 2.
Repeated six-predecessor parity states require opposite next parities, so neither
initial seed choice nor prefix ambiguity can repair the registered formula.
This is an exact scoped negative, not a ban on every mathematical generator.

The audit retains singular coefficient and reachable-prefix spaces and verifies
complete small-ring counts. It does not turn mod-13-only fits, zero-check fitting,
parameter aliases or partial predictions into evidence. Homogeneous order-two
prior-art overlap and higher-order startup freedom are explicit.
[Results, independent replay and limitations](AUTONOMOUS-RECURRENCE-FINDINGS.md).
The Morse/tree question and private image are separate; no tree cipher was tested.

## H-LETTER-GEOMETRY — representation verified; two finite mechanisms rejected

The user's refined lines/curves/orientation/placement proposal is encoded as a
versioned idealized 35-component skeleton dictionary, not measured copper glyphs
or pen-stroke counts. All 26 arrays and exact positional codes are unique; sums
and residues collide. Feature order is declared rather than fit to K4.
[GEOMETRIC-PILOT-001](GEOMETRIC-PILOT-FINDINGS.md) rejects the frozen code-ranked
periodic arithmetic and 35-bit rotation/XOR feedback models. This does not
exclude all geometric encodings. No alternative order or state rule was added.

The subsequent root-digit/changing-base refinement has a separate
[finite raw-token security audit](GEOMETRIC-BASE-SECURITY-AUDIT.md). With public
geometry/order, known exact-number boundaries and b=d+2 over bases 2–61, only
8 and 27 are ambiguous; all other emitted numbers identify letter and base.
This neither attacks a root generator nor tests a new K4 modular-arithmetic
family. That separate admissibility specification remains pending; no root,
offset, weight-order or transform search was added.

### Changing-base follow-up completed — 22 October 2026

The previously pending arithmetic admissibility specification is now frozen and
[completed](RADIX-FEEDBACK-FINDINGS.md). All eight first-order affine geometric
feedback families are excluded, even allowing each base to be any independent
integer >=2. Fixed geometry/order and two designated letter equations remain
assumptions; nonlinear updates and other cipher constructions are untested.
The older period-12 crib fit also has a separate
[chance calibration](PERIODIC-CRIB-CALIBRATION.md), not a positive candidate.

## H-IPA-DICTIONARY — bounded current-US source model rejected

The user's dictionary-phonetics proposal is tested separately from earlier
respelling and script-transport work. The [IPA report](IPA-PREPROCESSING-FINDINGS.md)
records frozen Cambridge US forms: R1 segment lengths 10/9, R2 code-point lengths
13/11. Unchanged transformed-window alignment is an explicit assumption, not
proved global alignment. Arbitrary phase injectivity leaves 8/11/12 vacuous;
all 48 fixed-ordinary-Latin periodic arithmetic structures fail within the first
crib, 47 by ordinary anchors and one by a shared length-marker contradiction.
No dialect/offset search, special-alias enumeration or English inverse is claimed.
Original independent full-window certificates and the later first-window
supplement are preserved with their distinct chronology and staging.

## H-AFFINE-DIGRAPH — status correction, 23 October 2026

The four fixed adjacent same-alphabet affine models (AZ/AZ and KRYPTOS/KRYPTOS,
both pair origins) are [analytically excluded by parity](AFFINE-DIGRAPH-PARITY-BOUNDARY.md).
No matrix search was run or required. Earlier unrun headings and the original
frozen proposal are historical; this exact family is not an open unrun candidate.
No claim about all polygraphic models or mixed alphabets follows.


## 23 October 2026: stateful tree/path pilot and independent IPA integration

The two fixed tree/subtree-permutation constructions were implemented, controlled and tested continuously across all 97 positions. All 104 settings fail the first crib; this is a bounded negative, not a general tree-cipher exclusion. See [TREE-PATH-CIPHER-FINDINGS.md](TREE-PATH-CIPHER-FINDINGS.md). Independent free-map IPA and source-fixed pronunciation codec audits now replay exactly; see [IPA-CODECS-INTEGRATION.md](IPA-CODECS-INTEGRATION.md). No additional search was launched after these failures.
<!-- ARCHIVED-NOTES:END -->
