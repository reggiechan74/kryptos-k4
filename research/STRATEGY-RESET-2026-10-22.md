# K4 strategy reset after the bounded route and feedback batches

22 October 2026. **Brainstorm and proposed pilots only. No new experiment,
candidate plaintext, solution or independently confirmed cipher clue.** This
note reviews the full hypothesis ledger and its subsequent dated corrections;
older headings marked unrun are not read in isolation from completed outcomes.
Novelty here means a proposed method change not executed in this repository,
not a claim of worldwide originality or absence from every external program.

## Decision

Stop enlarging route/key lists on the basis of their partial scores. First test
whether our evidence can identify a generating mechanism under blind conditions,
then prefer constraints obtained independently of K4. There is no current positive
lead that warrants a bigger brute-force search. Four directions below are new
operational proposals here; only the fourth names a new concrete toy mechanism.
The others change how we select or constrain mechanisms rather than adding cipher
names. Existing ideas are explicitly retained as backlog rather than relabeled new.

Repository state reviewed: `research/dynamic-key-20261022` at
`d3a4115794c6915b8c4fa0e0ffa6d41a42d3e9dd`, 195 passing tests. The two latest
route batches added 662 actually tested branches and 16 prior-equivalent skips,
with no candidates. This note implements no code or Site change. It is not a
preregistration for any proposed pilot: each needs a separate frozen specification
before implementation or K4 evaluation.

## Tested versus still open

| Mechanism class | What is established locally | What is not established |
| --- | --- | --- |
| Pure letter permutation / fixed substitution | E-count rejects every literal permutation-only pipeline; exact crib collisions reject direct monoalphabetic decoding and 19 specific periodic-bijection periods | Does not reject substitution plus permutation or a stateful alphabet |
| Periodic arithmetic plus routes | Full 66-route catalogue, frozen K3 one-layer/sandwich/24-sector families, and 288 fixed occupied-cell branches have scoped negatives; 282 long-period fits are vacuous | No exclusion of every possible route, alphabet or composition; more route parameters are not a fresh strategy |
| Direct feedback and fixed stepping | Same-alphabet lags 1–96 fully classified: 732 contradictions, 420 zero-check underdetermined cases; all 72 mixed-role PT cases at lags 9–12 rejected; finite fixed-primer and class-triggered cursor cases fail | Does not eliminate arbitrary state machines; longer primers with no independent checks supply no evidence |
| Fractionation and representations | 144 fixed Trifid cases, two fixed Fractionated Morse maps, 32 fixed split-coordinate transforms, restricted GOST/respelling/word-scrambling cases fail their declared gates | Other precisely sourced codecs are not excluded; unconstrained translation/transliteration is not a decoder |
| Gromark and arbitrary alphabets | One fixed published tuple admits complete nonunique alphabets; ten noncrib positions conditionally forced, 63 variable | No recovered historical alphabet, meaningful full plaintext or K4 solution; no need to try more tuples absent independent restriction |
| Base-60 and photographed silk chart | Declared true-Beaufort recurrence/primer audit exhausted 26,355,600 tuples; fixed chart periods 1–12 fail | Other mathematical constructions are not excluded; reusing a number with another ad hoc mapping is not independent motivation |
| Geography / clock / optical interpretations | World Clock identification sourced; landmark orientation comparisons are descriptive; complete newer Sun Study geometry audit saved | Period footprints, surveyed geometry, heading and optical paths are not calibrated; the Site is a tool, not evidence for a decoder |
| Considered but unrun / weakly specified | Affine digraph mapping, broader historical encoding/codebook, selected machine families and source-backed restrictions already appear in the catalogue/prior-art review | These are backlog, not newly discovered ideas. Historical availability or a thematic name alone does not select a mechanism |

Primary local records: [hypotheses](HYPOTHESES.md), [experiments](EXPERIMENTS.md),
[prior-art inventory](../sources/EXPERIMENTS.md),
[prior-art scope review](../docs/prior-art-barney-scott-review.md),
[exact feedback/coordinate results](CONTINUATION-FINDINGS.md),
[K3/clock results](K3-CLOCK-ROUTE-FINDINGS.md),
[occupied-cell results](OCCUPIED-CELL-FINDINGS.md),
[identifiability](GROMARK-IDENTIFIABILITY-FINDINGS.md), and
[geometry audit](../docs/scott-sun-geometry-audit-2026-10-22.md).

## 1. Blind mechanism identification before another K4 search

**Why distinct.** Our planted controls usually supply the true structure to the
right solver or test a finite scanner within its own family. They verify code,
not whether a solver can tell which family generated an unknown 97-letter
ciphertext. A blind cross-family tournament can expose that gap before we spend
another round fitting K4.

**Independent evidence.** Known generator labels and independently selected
plaintexts are actual ground truth. K1–K3 controls provide verified operations;
they do not prove any generator was used for K4. The pinned third-party review
already reports poor recovery power for some free-alphabet methods, which is a
warning to measure this ourselves, not a replicated numerical result.

**Cheap falsifiable pilot, proposed/unrun.** Freeze five generators before using
K4: periodic substitution, PT autokey, CT autokey, one fixed Trifid and a simple
evolving-alphabet transform. Generate eight 97-letter examples per family from
nonoverlapping public-domain English passages: 40 examples, balanced 20 for
calibration and 20 sealed for evaluation, with disjoint keys and source passages.
Reveal the actual plaintext letters at the same 24 indices as the K4 clues,
not artificially insert EASTNORTHEAST/BERLINCLOCK into unrelated prose. Keep
family labels hidden from the selector. Require it to identify a unique generating
family or abstain; feed a further 20 matched random negatives through the same
pipeline. Set the exact small parameter domains and one-minute budget in advance.

**Failure gate and overfitting control.** A first feasibility gate is at least
16/20 correct unique identifications, no more than one wrong unique assignment,
and at most one false unique assignment on the 20 negatives; report uncertainty
from the small sample. Failure rejects this diagnostic pipeline at this evidence
size, not the generating cipher families. Freeze features, solver budgets,
thresholds and tie/abstention rules using calibration only. K4 is quarantined
until the gate and report format are frozen; no LLM plaintext cleanup or scoring
on known challenge text. Passing is permission to evaluate a method, not evidence
that K4 belongs to its preferred class.

## 2. Count the compatible-key volume instead of rewarding the best fit

**Why distinct.** Existing work proves feasibility and marginal identifiability;
current search diagnostics mostly maximize crib agreement. A flexible model can
look excellent at its best completion while almost all keys predict something
else. Counting/integrating the entire compatible key set asks a different question
from finding one witness or the prettiest plaintext. This is a capacity diagnostic,
not a revival of contradicted models or a new Gromark sweep.

**Independent evidence.** The already verified distinct Gromark alphabet witnesses
and vacuous high-period fits demonstrate real nonuniqueness. They do not establish
a historical prior over keys. The declared prior is a modeling assumption that
must stay visible; a numerical score is not a probability of artist intent.

**Cheap falsifiable pilot, proposed/unrun.** Start on a four-symbol toy with two
arbitrary alphabet permutations: exactly 24 squared = 576 ordered pairs. For
20 planted and 20 histogram-matched null instances, enumerate all 576 pairs,
count exact compatible assignments, remove the known gauge multiplicity, and
compare marginal predictions with the truth. Verify normalized compatible-key
mass, not raw survivor counts across differently sized parameter spaces. Compare
two explicit priors, uniform permutations and a fixed independently chosen small
construction list. Do not use English scoring or new K4 tuples in this pilot.

**Failure gate and overfitting control.** Exact counts must agree with exhaustive
truth and gauge-equivalent parameterizations must give identical predictions.
If a supposed signal vanishes under a harmless reparameterization, reject the
measure. If rankings reverse under plausible declared priors, report
nonidentification and do not claim a historical conclusion. Only a validated,
bounded counting method could later be applied to a separately justified fixed
K4 model; finite-budget unresolved counting remains unresolved. All fitted
constraints must be imposed in null instances too.

## 3. Recover conventions from an independent related ciphertext/plaintext pair

**Why distinct.** Related artworks and artistic vocabulary already appear as
context in the repository. The new action would be known-pair system identification
on a different encryption, followed by prospective transfer of a constraint to K4.
That differs from guessing a thematic word, another language or a key from a title.

**Independent evidence and source gate.** The existing designer/language reports
identify related cryptographic work, including Cyrillic Projector, but this note
has not verified a complete authoritative ciphertext/plaintext pair. Obtain one
publicly documented pair and exact alphabet/normalization first; if unavailable,
stop the pilot at a provenance result. Exclude copied Kryptos passages on related
sculptures: a second physical copy of the same K4 text is not independent evidence.
Later artworks can reveal habits but cannot prove the same method was used by 1990.

**Cheap falsifiable pilot, proposed/unrun.** On one independently sourced known
pair, freeze at most six competing convention bundles before looking at K4:
alphabet indexing, punctuation advance, row continuation/restart and exact
reading/inversion conventions. Fit only the earlier two-thirds of that pair;
require exact prediction of the final third and full roundtrip. Publish complete
source pins and ambiguity rather than a thematic similarity. At most six models,
no dictionary or broad route sweep.

**Failure gate and overfitting control.** Reject a convention bundle on any
held-out character discrepancy; if several remain equivalent, record the whole
class. Transfer only the independently supported operation/convention, never a
selected noncrib phrase or an invented historical association. Even a perfect
related-art result prioritizes a K4 hypothesis rather than forcing K4 to use it.
Do not contact anyone, inspect restricted archives or query a private solution
verifier without separate authorization.

## 4. Small evolving-alphabet pilot: change the symbol map, not the key cursor

**Why distinct.** The failed class-triggered stepping models moved a cursor over
a fixed alphabet/key. A substitution alphabet that changes after each symbol is
a different mechanism: equality/cursor-phase invariants need not survive. No such
specific state-permutation pilot appears in the local experiment catalogue. This
is a mathematical proposal, not a claim that a named historical machine or a
particular unreleased method was taught to Sanborn.

**Independent evidence is weak.** The general reported goal of masking English
supports considering transformations of its visible statistics; it does not select
a state update. There is no K4-specific evidence here for move-to-front. Rank this
below the methodology/source gates and reject the four cases cheaply if tested.

**Cheap falsifiable pilot, proposed/unrun.** Choose immutable reference alphabet
R and initial state permutation S0 independently from AZ/KRYPTOS: exactly four
models. Encrypt C[i] = S[i][index_R(P[i])]. After the current symbol, move that
ciphertext character to the front of S while retaining all other characters'
relative order. Decrypt by P[i] = R[index_S(C[i])], then perform the same update
from the observed ciphertext character. The state is deterministic and the step
is bijective. Fix the move-to-front rule, starting position and four initial
pairs in a new specification; no rotations, back/front choice, extra alphabet,
key guessing or alternative update after failures.

**Failure gate and overfitting control.** First verify every state is a permutation,
all 26 one-step symbols, planted complete-message inverses and an independently
coded state trace. Then require all 24 K4 letters and full 97-letter regeneration;
any mismatch rejects that fixed model. Record first contradictory state/index,
not attractive partial English. No null simulation is needed if all four fail.
Any all-crib survivor needs complete auditing and same-four-model null calibration;
it would still be only a crib fit, not independently validated decoding. Broader
stateful ciphers would remain open after a four-case negative.

## Sources, cautions and practical order

[Scheidt's edited 2005 interview](https://www.wired.com/2005/01/inside-info-on-kryptos-codes/)
was reread for this note. He discusses disguising access to English and uncertainty
about final changes; neither statement specifies an algorithm. The interview's
Cyrillic reference is context, not a newly verified known-pair dataset. Existing
[designer-context](../docs/designer-context.md) and
[language/source review](../docs/language-and-alphabet-layers.md) retain the
related-art chronology. Fresh Smithsonian transcript/biography retrievals returned
errors; no new inspection of those source contents is claimed. The 97-letter
fixture is unchanged despite erroneous counts in some prose sources.

Recommended next action is pilot 1 on synthetic/non-K4 data. In parallel, establish
the public known-pair source gate for pilot 3. Pilot 2 is a toy counting validation;
pilot 4 is an optional four-case mechanism test with weak historical support.
All are unrun. Do not add another family until a specification fixes its domain,
acceptance gate, runtime, aliases, free parameters and controls.

Neither a fluent continuation nor its automatic re-encryption establishes a
solution when parameters were fitted to the same known letters. Keep physical
interpretation separate from exact character recovery. No new null tail, English
score or count of extra rejected branches is created by this strategy note.
