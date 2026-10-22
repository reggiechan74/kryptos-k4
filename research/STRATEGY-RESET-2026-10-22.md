# K4 strategy comparison after the bounded route and feedback batches

22 October 2026. **Comparison and proposed pilots only. All pilots below are
unrun. No new K4 search, candidate plaintext, solution or confirmed cipher clue.**
This dated revision expands the four-direction reset first committed at
`d879c28b36fdc3095caaf7a3701b4a7e09f870d3`: source checking changes priorities,
related-art convention recovery becomes part of a construction-pipeline audit,
and historical clock reconstruction is separated from abstract routes. Earlier
versions remain in Git history. This is not an executable preregistration.

## Decision and ranking

Acquire constraints independently of K4 before enlarging the search. First audit
available construction evidence and check whether an independent related-art pair
is actually accessible. Then prefer the four fixed state models with a small blind
control harness over building a large architecture classifier. Clock reconstruction
needs a concrete mapping question. Broader diagnosis and model synthesis are
conditional tools only when cheaper work leaves a decision they could resolve.
These priorities weigh cost and discrimination as well as historical support;
they are not numerical probabilities of Sanborn's intent.

Reviewed baseline: branch `research/dynamic-key-20261022`, preceding HEAD
`d879c28b36fdc3095caaf7a3701b4a7e09f870d3`, clean and synchronized with origin;
last code validation **195 passing tests**. The two latest route batches added
662 tested branches and 16 prior-equivalent skips, with no candidates. This
revision changes documentation only and does not rerun that regression suite.

| Priority / direction | Novelty relative to the actual ledger | Discrimination / identifiability | Pilot deliverable and cost | Go/no-go gate; what success establishes |
| --- | --- | --- | --- | --- |
| 1. Construction-pipeline audit | Known K1/K2 controls and related-art context already exist. New work is source-by-source alignment of intended text, entered key, worksheet ciphertext and carving, with stage-specific discrepancies | Can distinguish a plaintext spelling difference from a key-entry or alignment difference; cannot determine accident versus deliberate choice | Small source-tagged alignment table, one K1 discrepancy and existing K2 deletion control; mainly manual image work, negligible compute | Exact source correspondence and forward reproduction, with ambiguity logged. Success establishes a convention or error mechanism for that source, not K4 edits |
| 2. Four deterministic evolving alphabets | Specific symbol-permutation update is untested locally; failed cursor stepping keeps the symbol map fixed | Zero fitted parameters within each of four models; any crib contradiction rejects it | Four full traces, independent inverses and planted controls; linear in message length | All 24 cribs plus exact 97-letter regeneration, with audit and family controls for survivors. Success is a crib-compatible candidate only |
| 3. Historical World Clock operator | Clock, historic inscriptions and 24-sector routes already considered/tested. New deliverable is a date-aware observed city/hour operator, not another route | One shared phase must predict multiple independently observed mappings; missing historical panels may prevent identification | Partial dated label/band/order inventory plus forward operator; archival data dominate cost, CPU trivial | Reproduce withheld visible mappings without per-city phases; otherwise stop. Success validates clock reconstruction, not its use in K4 |
| 4. Blind architecture diagnosis | Synthetic recovery was already proposed locally and exists in reviewed external work. New-to-ledger target is blind cross-family discrimination with abstention and sealed evaluation | Tests whether our available statistics separate specified families at length 97; may establish only an equivalence/ambiguity class | Frozen generators, disjoint-source/key benchmark, confusion and abstention tables; small CPU feasibility run before scaling | Predeclared evaluation gate and uncertainty; failure stops use of that diagnostic. Success validates a method on represented generators, not K4 classification truth |
| 5. Compatible-key volume and bounded synthesis | SAT, graph potentials and marginal identifiability are already implemented. New target is predictive volume across a small new grammar, charging all fitted choices | Separates impossible, compatible-but-ambiguous and forced predictions; requires quotienting harmless gauges and retaining real free offsets | Exhaustive four-symbol counting oracle, then a separately frozen grammar only if justified; toy is tiny, full counting may be expensive | Exact counts/gauge-invariant predictions or explicit unresolved result. Success measures capacity and predictions under assumptions, not historical posterior probability |

## What the ledger already covers

Read dated outcomes together with older unrun headings. Local novelty is not
worldwide novelty; an absent exact pilot does not make its broad theme new.

| Mechanism class | Established scope | Remaining limit |
| --- | --- | --- |
| Pure permutation / fixed substitution | E-count proof excludes literal permutation-only pipelines; crib collisions exclude direct monoalphabetic decoding and 19 specified periodic-bijection periods | No proof against every composition or stateful alphabet |
| Periodic arithmetic plus routes | 66-route catalogue; four K3 one-layer and two sandwich cases; 368 new 24-sector cases with 16 equivalents skipped; 288 occupied-cell fixed-key cases rejected | 282 earlier long-period fits were vacuous; no blanket route/composition exclusion |
| Feedback and cursor stepping | Same-alphabet audit: 732 contradicted and 420 zero-check underdetermined cases; 72 mixed-role plaintext-feedback configurations rejected; specified fixed-primer/dynamic/class-triggered cursor cases negative | More freedom can remove predictions rather than supply evidence; state-permutation evolution remains distinct |
| Fractionation / representation | 144 fixed Trifid, two fixed Fractionated Morse and 32 split-coordinate cases negative; scoped language/GOST/respelling/word checks | No general fractionation or language-family exclusion |
| Arbitrary alphabets / Gromark | Fixed tuple admits nonunique alphabets; ten noncrib positions conditionally forced and 63 variable | No recovered historical alphabet or validated decoding; fitting another tuple is not independent evidence |
| Base-60 / silk chart | Specified true-Beaufort search exhausted 26,355,600 tuples; fixed chart periods 1–12 rejected | Does not exclude unrelated arithmetic; number reuse alone does not justify a mapping |
| Clock / geography / optics | Historical inscriptions reviewed; landmark ranks descriptive; current Sun Study audited | Unsurveyed heading, shape and optical paths block physical conclusions; Site output is not decoder evidence |
| Already considered, unrun | Affine digraphs, codebooks/language encodings, selected machine families, related-art conventions | Backlog requiring source/specification gates, not newly discovered strategies |

Audit trail: [hypotheses](HYPOTHESES.md), [experiments](EXPERIMENTS.md),
[policy](POLICY.md), [earlier strategy](../docs/research-strategy.md),
[designer labs](../docs/designer-context.md),
[prior-art inventory](../sources/EXPERIMENTS.md),
[external scope/power review](../docs/prior-art-barney-scott-review.md),
[feedback/coordinate results](CONTINUATION-FINDINGS.md),
[K3/clock results](K3-CLOCK-ROUTE-FINDINGS.md),
[occupied-cell results](OCCUPIED-CELL-FINDINGS.md), and
[Gromark identifiability](GROMARK-IDENTIFIABILITY-FINDINGS.md).
These records already distinguish known-structure planted controls, statistical
replication, exact feasibility and unresolved recovery; none licenses a new lead.

## 1. Construction pipeline: establish which stage changed

**Independent observation, not a new K4 experiment.** On this revision date the
[worksheet image](https://www.thekryptosproject.com/kryptos/images/sb_notes.jpg)
was downloaded and visually inspected. Its K1 plaintext spans the row ending
`ILLUSIO` and following `N`; the aligned key segment reads `PALIMPCEST`, rather
than the usual `PALIMPSEST`. This supports testing a key-entry-stage explanation
of decoded `IQLUSION`; it does not establish accident or intention. Do not silently
correct the canonical fixture. Receipt: JPEG 219,438 bytes, SHA-256
`7a550e9b8790b3b20f79bcca0f2b81fa1ced0773086c98c09d2e049e21900b64`.
The [attribution page](https://www.thekryptosproject.com/kryptos/charts/pt_k1_k2.php)
is reported to attribute this to NYT material; fresh retrieval did not complete,
so this revision independently verifies visible letters, not archival authorship
or publication chain. The image itself is not republished here.

**Proposed deliverable.** Align exact indices across source plaintext, entered
key, worksheet ciphertext and canonical carving for K1/K2. Record source IDs,
image cells, punctuation advancement, row continuation and uncertainty. Replay
existing K1/K2 reference encoders, including the documented K2 omitted-character
case and restored endpoint as separate inputs. Require exact named downstream
differences, not an assertion that an edit merely makes English look better.
This is an extension of existing designer Lab 1/2, not a new cipher family.

**Gate.** Disagreeing transcriptions stay unresolved; no inferred cell may be
promoted to observation. A successful pipeline account establishes that a
particular convention/error can explain a known artifact. K4 insertion, deletion,
substitution or movable punctuation requires an independently observed discrepancy;
K1 anomalies are not permission to fit K4 edits. No such discrepancy is identified
here. A separately preregistered bounded construction-error hypothesis could be
studied as speculation; it must not be presented as correcting canonical K4 or
introduced post hoc to rescue a failed candidate. Related-art known-pair recovery
is a second source lane: first obtain an
authoritative complete independent pair, exclude copied K4/Antipodes text, then
freeze at most six convention bundles, fit the first two-thirds and demand exact
last-third prediction. Later artworks do not prove a shared 1990 cipher.

## 2. Exactly four evolving-alphabet models

This concrete pilot is unrun. Unlike failed cursor stepping, it changes the
substitution permutation after each symbol. A symbolic counterexample to mere
rotation: moving D to the front of ABCDE... yields DABCE..., whereas a cyclic
rotation starting D yields DE...ABC. The cyclic neighbor order changes. Thus this
is not just a cursor shift over one fixed cyclic alphabet; this does not prove
inequivalence to every general state-machine representation. No local result
covers this exact update. General masking statements do not select move-to-front.

Choose immutable reference R and initial permutation S0 independently from
AZ/KRYPTOS (`ABCDEFGHIJKLMNOPQRSTUVWXYZ` / `KRYPTOSABCDEFGHIJLMNQUVWXZ`):
four models, no fitted key. Start at index 0 of the canonical 97-letter message;
exclude the preceding separator and make no boundary resets. Encrypt `C[i] = S[i][index_R(P[i])]`,
then move that ciphertext character to the front of S, preserving all other
characters' relative order. Decrypt `P[i] = R[index_S(C[i])]`, followed by the
same observed-ciphertext update. No extra rotations, reset, reversed update,
primer, alphabet search or rule changes after scoring.

Proposed controls: permutation invariants, all 26 one-step symbols, independent
full-message inverses and state traces. Before K4, include blinded positives for
each rule, a nearby incompatible fixed mechanism and histogram-matched decoys
through the identical four-model selector. For K4-specific power, positive
plaintext fixtures must retain the actual 24 crib letters/positions (including
repeated EAST/letter relations); the same constraints govern the decoys. Declare
the resulting synthetic conditioning, filler source, seeds, decoy count and
acceptance threshold before running. Decoy compatibility diagnoses weak
discrimination; it does not automatically justify a larger classifier. Then
require all 24 fixed crib letters
and exact 97-character regeneration. Record first contradiction; reject each
failed fixed model. If all fail, no null simulations are needed. For any survivor,
rerun the same complete four-model selection on matched nulls and audit independently.
A full crib fit is not independently validated plaintext; re-encryption alone
only checks implementation. Broader evolving alphabets would remain untested.

## 3. Historically correct World Clock data and operator

The existing [historic inscription review](../docs/historical-clock-inscriptions.md)
already establishes partial dated coverage and warns against modern substitutions.
The next useful change is observable mechanism reconstruction, not more 24-column
routes, city keywords or arbitrary per-letter time offsets.

[The constructor](https://kunsch-metallbau.de/referenzen-/weltzeituhr-berlin-alexanderplatz/)
describes two city bands, a daily rotating hour ring, and a simplified planetary
assembly rotating together once per minute. That last motion is not actual orbital
positions. Its hemisphere description cannot be used as a strict binary rule:
independent inspection of the 579 × 786 image
[Bundesarchiv Bild 183-E1003-0001-001, Peter Koard, 3 October 1969](https://commons.wikimedia.org/wiki/File:Bundesarchiv_Bild_183-E1003-0001-001,_Berlin,_Weltzeituhr_am_Alexanderplatz.jpg)
shows Ankara, Cairo and Casablanca in the lower band. Image receipt: 75,598 bytes,
SHA-256 `d11e7d21ebbf72853a914ab3a63d6574cb611177b8c5a7ee7b9884aa4ac748f3`.
Only visible panels are established. This is not a complete 1989 inventory.
The [12 December 1997 restoration report](https://www.berliner-zeitung.de/article/20-staedtenamen-wurden-bei-der-restaurierung-ergaenzt-frisch-poliert-die-weltzeituhr-dreht-sich-bald-7079)
records 20 added cities and changed zone assignments. Modern lists are insufficient.

**Proposed deliverable/gate.** Build a source-tagged partial historic label table:
spelling, band, sector order, date, legibility and contradictory observations.
Missing panels remain unknown. Define one shared hour-ring phase and explicit
historical zone convention; fit on some visible city/hour alignments and require
exact prediction of withheld visible alignments from the same observable state.
Unverified photograph time or phase prevents a timed check; do not infer both
freely for every city. Stop if data cannot identify the operator. Even success
only validates the clock model. A mapping from that operator to K4 letters would
need a separate independently motivated specification and budget. Without a
concrete mapping question, more label collection has no cryptanalytic go/no-go
payoff; keep it a provenance result. The two fixed bands are not extra rotors.
Unsurveyed CIA
geometry cannot fill missing clock data; see the [geometry audit](../docs/scott-sun-geometry-audit-2026-10-22.md).

## 4. Conditional architecture diagnosis

[Bean 2021](https://ecp.ep.liu.se/index.php/histocrypt/article/download/153/109)
uses Monte Carlo statistics to argue for structural possibilities. Those results
are statistical evidence under their nulls, not a universal one-to-one theorem.
The paper's lamp-clock/base-5-or-12 argument does not transfer to the subsequently
identified Alexanderplatz World Clock. Existing local STAT-001 already checks
selection across lags; another attractive lag alone is not new diagnosis.

**Proposed deliverable.** Before K4 evaluation, freeze a small generator set
(periodic substitution, PT autokey, CT autokey, fixed Trifid and the specified
evolving alphabet are candidates). Use independently sourced 97-letter passages
and disjoint keys/source works for calibration and sealed evaluation. Reveal
actual plaintext at the 24 clue indices in this natural-text track.
That natural-text track measures general transfer, not recovery under K4's actual
repeated crib structure. Keep a separate explicitly constraint-conditioned track
with the actual EASTNORTHEAST and BERLINCLOCK strings at their fixed indices;
synthetically imposing them is not ordinary sampled prose. Report both tracks
separately, and use the same actual crib constraints in matched-decoy evaluation.
Predeclare coincidence, equality/collision patterns, the entire repeated-pair lag
profile and crib-conditioned distances; charge feature/lag selection to the
calibration process. Distinguish families only where the data support it and
allow abstention. Include shuffled and outside-generator challenges: this is an
open-world problem, not an assertion K4 belongs to the five generators.

The prior reset proposed 40 generated examples (20 calibration/20 evaluation)
plus 20 random negatives, with a feasibility gate of at least 16/20 correct unique
assignments, at most one wrong unique assignment and one false unique negative.
These are proposed engineering thresholds, not calibrated statistical guarantees;
report intervals and confusion/abstention tables. A larger proposal such as 1,000
cases per six families needs a separate power/cost justification. No dataset,
classifier or accuracy result is created by this note. Freeze generator/key
ranges, budgets and abstention rules before generation; keep K4 quarantined.
Failure rejects the diagnostic's discrimination claim, not the cipher families.

## 5. Conditional model volume and bounded synthesis

The existing SAT/graph work already asks whether exact compatible keys exist and
which characters are forced. Calling another implementation SAT is not a strategy
change. The proposed change is comparing predictive capacity across a small
**new, justified grammar**, rather than best crib score or prettiest completion.

**First deliverable, proposed/unrun.** On a four-symbol toy, enumerate all
24 × 24 = 576 ordered alphabet pairs on 20 planted and 20 matched-null instances.
Compare exact compatible sets, normalized key mass and non-fit predictions against
an independent exhaustive oracle. Identify genuine gauge multiplicities; count
plaintext-equivalent keys once when reporting distinct predictions, retaining
their induced prior mass for probability calculations. Compare uniform
permutation and independently fixed construction-list priors. A rank reversal
under defensible priors means the ranking is prior-sensitive, not artist intent.

Only after this works, freeze a genuinely new small grammar and a complexity
account charging seed, alphabet, route, signs, update rules, resets and edits.
A 48-bit cap, two-stage limit or five-symbol seed would be optional engineering
guardrails, not a theorem or a guarantee of identifiability. The four state models
above offer a concrete finite grammar; their internal state changes are not extra
fitted choices. Do not reopen rejected models by hiding freedom in a solver.

Fit EASTNORTHEAST alone, preserve every free offset symbolically, and count only
BERLINCLOCK constraints actually predicted. Public clues informed earlier research,
so this is fitting separation, not historically untouched validation. Record
parameter/key and distinct-plaintext volume separately. In graph models an edge
joining components fits a free offset; only cycles/previously connected endpoints
supply checks. Impossible, compatible-but-ambiguous, uniquely compatible and timeout
are different outcomes. Toy counts and harmless-reparameterization invariance are
hard gates. Full-size counting outside the fixed resource budget remains unresolved.

## Source limits and staged next action

[Scheidt's edited interview](https://www.wired.com/2005/01/inside-info-on-kryptos-codes/)
uses masking for statistical disguise and semantic cover; it specifies neither a
physical stencil nor preprocessing order. PBS vowel/phonetic suggestions must
remain attributed to narrator/Gillogly speculation, not Scheidt instructions.
[Sanborn's interview](https://www.wired.com/2005/01/questions-for-kryptos-creator/)
distinguishes deciphering text from subsequent location interpretation; it does
not make every physical association a cryptanalytic constraint. The
[Smithsonian interview](https://www.aaa.si.edu/collections/interviews/oral-history-interview-jim-sanborn-15700)
reference to sentence strips concerns CIA disclosure review, not authenticated
K4 encipherment. That distinction comes from the supplied source review; this
revision makes no new successful retrieval claim for that transcript. The
DocumentCloud letter was inaccessible to the reviewer and private auction coding
materials were not inspected. Do not cite them as directly verified algorithms.

The skeptical alternative to a large classifier is persuasive on cost: use the
small control harness first. Next batch should finish the available K1/K2 source
alignment and check the independent known-pair gate, then preregister the four
state cases and their blind/decoy harness. If no authoritative related-art pair
is available, stop that lane rather than guess. Pursue clock sources only to
answer a declared observable mapping question. Broader classification needs an
explicit unresolved choice between mechanisms that its features could separate;
model-volume synthesis needs a small genuinely new grammar. Neither is a default
next build. Validate toy counts before applying them at full size. No pilot is
started by this comparison. Save inputs/hashes, actual costs, rejected scope and
all negative outcomes when a future authorized batch runs. End-to-end fitting and
selection must be repeated in controls; 199 controls can never yield a corrected
Monte Carlo tail below 1/200. A fluent fragment or post-hoc fitted crib is no lead.
