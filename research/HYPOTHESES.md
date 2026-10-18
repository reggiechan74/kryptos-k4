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
