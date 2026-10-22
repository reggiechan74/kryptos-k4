# Hypothesis log

Use [the template](templates/hypothesis.md) for new hypotheses. Exact structural
proofs and finite tests have separate scope; compatibility is not a solution.

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
