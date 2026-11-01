# Cryptanalysis method hypotheses

All entries are proposed and unrun. A specified research question is not a novelty clearance or permission to launch a K4 search. See [README](README.md) for gates, priorities and source limitations.

<a id="n100-079"></a>
## N100-079 — Counterexample-guided operator deduplication

**Draft reference:** `M01` · **Type:** method · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** A bounded symbolic equivalence checker can reject duplicate mechanism programs before any K4 fitting, using a concrete distinguishing trace whenever equivalence cannot be proved.
- **Bounded test:** On 60 independently authored tiny cipher programs with planted aliases and genuinely distinct pairs, compare structural hashes against exhaustive semantic equivalence on alphabet sizes2–5/length≤6. Require no false-equivalence certificate and fewer distinct solver launches than raw syntax hashing.
- **Controls:** Hide equivalent programs under alpha-renaming, state conjugacy and commuting stages; include programs equal on short traces but different later.
- **Identifiability limit:** Finite counterexamples prove difference; no bounded counterexample does not prove global equality. Restrict proof claims to formally exhausted domain.
- **Closest local external:** Existing literal checker; EXT-012/025/050; H-EVOLVING-ALPHABET
- **Novelty distinction:** Extends literal reconstruction to certified operator semantics; classical program equivalence/e-graph ideas, not an invention claim.
- **Admission:** synthetic research proposal; not a new K4 cipher family or target authorization
- **Estimated cost:** Synthetic pilot ≤180 CPU seconds; no real K4 search.
- **Priority:** 1
- **Sources:** 
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/AGENTS.md
  - https://github.com/matthewdgreen/decipher/blob/2dace19a0309e08e9ea8e6c40af81c26f29276a3/README.md
  - https://arxiv.org/abs/2004.03082

<a id="n100-080"></a>
## N100-080 — Dependency-cone prior-art fingerprints

**Draft reference:** `M02` · **Type:** method · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Causal dependence graphs plus intervention witnesses can separate position-only, ciphertext-history and plaintext-state operators faster than reading names or comparing output samples.
- **Bounded test:** Blindly classify40 published/synthetic operator snippets into dependency classes; every positive distinction must include a pair of input histories with equal currently observed symbol but different output. Compare manual equation audit time and exact classification.
- **Controls:** Dead code, canceled dependencies, alias variables and hidden table mutation challenge syntactic false positives.
- **Identifiability limit:** A shared fingerprint is not proof of equal operators or prior coverage. Soundness first; unsupported code abstains.
- **Closest local external:** Source-literal checker; EXT-048/050/051
- **Novelty distinction:** Targets the documented source-scope bottleneck and cancellation errors with semantics-aware witnesses.
- **Admission:** synthetic research proposal; not a new K4 cipher family or target authorization
- **Estimated cost:** Read-only source pilot ≤120 CPU seconds.
- **Priority:** 2
- **Sources:** 
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/AGENTS.md
  - https://github.com/matthewdgreen/decipher/blob/2dace19a0309e08e9ea8e6c40af81c26f29276a3/README.md

<a id="n100-081"></a>
## N100-081 — Treewidth-driven exact feedback elimination

**Draft reference:** `M03` · **Type:** method · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Eliminating hidden letters in dependency-graph separator order can reduce joint-model solve cost relative to raw position order for mixed feedback constraints.
- **Bounded test:** On fresh length97 generated models with fixed clue masks and widths2–8, compare exact solution relations and total proof cost under natural versus min-fill ordering; require identical solutions and a prespecified20% median cost reduction without >2x worst-case penalty.
- **Controls:** Independent exhaustive tiny oracle, disconnected and high-treewidth adversarial instances, ambiguity and empty cases.
- **Identifiability limit:** No benefit means retain existing engine. Runtime benefit does not admit an old cipher as novel or make high-width cases identifiable.
- **Closest local external:** H-AUTOKEY-EXACT; H-NONLINEAR-BLOCK; METHOD-RESIDUAL
- **Novelty distinction:** Not another coefficient scan: exploits graph separators across nonlocal hidden-state constraints; standard variable elimination foundations.
- **Admission:** synthetic research proposal; not a new K4 cipher family or target authorization
- **Estimated cost:** Synthetic paired pilot ≤300 CPU seconds.
- **Priority:** 2
- **Sources:** 
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/AGENTS.md
  - https://github.com/matthewdgreen/decipher/blob/2dace19a0309e08e9ea8e6c40af81c26f29276a3/README.md
  - https://ics.uci.edu/~csp/r48b.pdf

<a id="n100-082"></a>
## N100-082 — Prediction-set cross-model intersection

**Draft reference:** `M04` · **Type:** method · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Computing intersection and disagreement of complete conditional plaintext sets across independently motivated models can expose model-specific forced letters without ranking a preferred story.
- **Bounded test:** Construct24 fresh problems with two misspecified and one correct model, plus no-correct-model controls. Enumerate joint sets on tiny analogues; measure whether intersection warning rejects false consensus rather than accepting it.
- **Controls:** Models sharing the same wrong assumption; nonempty marginal intersections with empty joint intersection.
- **Identifiability limit:** Agreement across models is not truth if all are wrong. This is an abstention diagnostic, not K4 plaintext evidence.
- **Closest local external:** Misspecified twins in METHOD-RESIDUAL-010; H-ARCHITECTURE-DIAGNOSIS
- **Novelty distinction:** Adds exact cross-model joint comparison, unlike scoring one model or treating marginal masks as products.
- **Admission:** synthetic research proposal; not a new K4 cipher family or target authorization
- **Estimated cost:** Synthetic pilot ≤180 CPU seconds.
- **Priority:** 3
- **Sources:** 
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/AGENTS.md
  - https://github.com/matthewdgreen/decipher/blob/2dace19a0309e08e9ea8e6c40af81c26f29276a3/README.md

<a id="n100-083"></a>
## N100-083 — Distinguishing-suite synthesis for cipher states

**Draft reference:** `M05` · **Type:** method · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Actively synthesizing short plaintext traces that separate state-update rules can catch implementation aliases missed by random planted tests.
- **Bounded test:** For each of20 finite-state model pairs, solve for shortest distinguishing word up to length20; compare fault detection per test with a fixed random suite. Verify each witness with independent interpreters.
- **Controls:** Equivalent-state pairs, outputs equal until long delay, reset and direction timing faults.
- **Identifiability limit:** No witness below bound is inconclusive. Synthetic suite design is not querying an oracle on real K4.
- **Closest local external:** METHOD-ADAPTER-011; H-TREE-STATEFUL; H-EVOLVING-ALPHABET
- **Novelty distinction:** Uses active automata-testing ideas to address state-update validation, not extra random cases.
- **Admission:** synthetic research proposal; not a new K4 cipher family or target authorization
- **Estimated cost:** Synthetic pilot ≤180 CPU seconds.
- **Priority:** 2
- **Sources:** 
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/AGENTS.md
  - https://github.com/matthewdgreen/decipher/blob/2dace19a0309e08e9ea8e6c40af81c26f29276a3/README.md
  - https://arxiv.org/abs/2401.12703

<a id="n100-084"></a>
## N100-084 — State-gauge quotient before constraint search

**Draft reference:** `M06` · **Type:** method · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Canonicalizing simultaneously relabelable hidden states can collapse redundant keys in nonabelian/projective models without losing distinct plaintexts.
- **Bounded test:** For small groups/orders≤32, compare complete raw search with canonical orbit representatives, exact stabilizers and recovered plaintext fibers. Require a verified bijection between raw solution orbits and canonical outputs.
- **Controls:** Non-free group actions, unequal stabilizers and two inequivalent keys yielding same finite trace.
- **Identifiability limit:** Global function, key orbit and finite plaintext equivalence are different quotients. Incorrect identification invalidates result.
- **Closest local external:** Sparse-law quotient audit; H-FEISTEL-3ROUND; EXT-041
- **Novelty distinction:** Extends proven coefficient alias handling to independently defined state conjugacies; standard group-action mathematics.
- **Admission:** synthetic research proposal; not a new K4 cipher family or target authorization
- **Estimated cost:** Synthetic oracle pilot ≤240 CPU seconds.
- **Priority:** 2
- **Sources:** 
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/AGENTS.md
  - https://github.com/matthewdgreen/decipher/blob/2dace19a0309e08e9ea8e6c40af81c26f29276a3/README.md

<a id="n100-085"></a>
## N100-085 — Proof-relevant knowledge compilation

**Draft reference:** `M07` · **Type:** method · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Compiling a complete cipher constraint relation to a decomposable circuit may answer all undisclosed-position projections without repeatedly enumerating the same solution fibers. A full97-symbol/24-clue contract has73 undisclosed positions; any smaller residual-tail contract must explicitly freeze its domain and excluded initial positions.
- **Bounded test:** Use30 fresh finite-state/sparse polynomial cases where exact oracle fits tiny domains; compile once, compare counts, joint witnesses and all masks to oracle, then measure total certificate+query cost.
- **Controls:** Circuits with falsely assumed disjoint branches, repeated variables, empty cases and ambiguous joints.
- **Identifiability limit:** Compilation can explode; a cap gives INCOMPLETE, never an exclusion. This must beat current certified-fiber reference on matched output contracts.
- **Closest local external:** METHOD-REFERENCE-007; METHOD-SATURATION-004
- **Novelty distinction:** Different relation representation, not another ambient-fiber traversal or automatic replacement. Knowledge compilation is established.
- **Admission:** synthetic research proposal; not a new K4 cipher family or target authorization
- **Estimated cost:** Synthetic pilot ≤300 CPU seconds; default off.
- **Priority:** 3
- **Sources:** 
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/AGENTS.md
  - https://github.com/matthewdgreen/decipher/blob/2dace19a0309e08e9ea8e6c40af81c26f29276a3/README.md
  - https://arxiv.org/abs/1106.1819

<a id="n100-086"></a>
## N100-086 — Rank-stratum certificates for support families

**Draft reference:** `M08` · **Type:** method · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** A symbolic partition of parameter/support space by rank and consistency may certify many equivalent observation systems with one small proof instead of one certificate per support.
- **Bounded test:** On reduced dictionaries with exhaustively enumerable supports, compare stratum unions against every individual system and full solution counts. Measure certificate bytes plus verification cost, not producer speed alone.
- **Controls:** Rank drops on exceptional parameter sets, inconsistent augmented ranks, overlapping strata and missing sparse lifts.
- **Identifiability limit:** Grouping by numerical rank alone is unsound; row-space equivalence and parameter guards must be proved.
- **Closest local external:** Full31 preflight; METHOD-REFERENCE-007; repeated certificate archive size
- **Novelty distinction:** Targets certificate bloat via exact symbolic strata, distinct from projecting saturated masks.
- **Admission:** synthetic research proposal; not a new K4 cipher family or target authorization
- **Estimated cost:** Synthetic pilot ≤240 CPU seconds.
- **Priority:** 2
- **Sources:** 
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/AGENTS.md
  - https://github.com/matthewdgreen/decipher/blob/2dace19a0309e08e9ea8e6c40af81c26f29276a3/README.md

<a id="n100-087"></a>
## N100-087 — Semantic negative-certificate transport

**Draft reference:** `M09` · **Type:** method · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** A counterexample-producing containment checker can transport an existing negative to a genuinely new mechanism only when its clue relation is proved a subset.
- **Bounded test:** Freeze20 synthetic source/target model pairs with known containment and noncontainment; require checkable witness maps for transfers and counterexamples for refusals. Measure avoided solver calls.
- **Controls:** Global-equivalent but differently aligned models; strict crib supersets, changed alphabet roles and reset boundaries.
- **Identifiability limit:** No hit is not eligibility; correct transport may show the proposed new model is already excluded and should not run.
- **Closest local external:** Retained-negative index; study064; study056 learned-conflict negative
- **Novelty distinction:** Extends narrow partition matching to relation containment with certificates, not re-running056 conflicts or broadening old negatives by name.
- **Admission:** synthetic research proposal; not a new K4 cipher family or target authorization
- **Estimated cost:** Synthetic-only pilot ≤240 CPU seconds.
- **Priority:** 1
- **Sources:** 
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/AGENTS.md
  - https://github.com/matthewdgreen/decipher/blob/2dace19a0309e08e9ea8e6c40af81c26f29276a3/README.md

<a id="n100-088"></a>
## N100-088 — Island-blind model-selection calibration

**Draft reference:** `M10` · **Type:** method · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Training only on one disclosed-like clue island and predicting a second can detect flexible mechanism overfit on fresh synthetic data better than all-clue compatibility alone.
- **Bounded test:** Fresh 97-letter plants/nulls with synthetic13+11 masks; choose model only using first island, freeze predictions, then unseal second. Compare calibration to all-clue fitting under a fixed candidate portfolio.
- **Controls:** Misspecified twins, model selection leakage, reversed-island order and ambiguity; no withholding of already seen K4 clues represented as fresh.
- **Identifiability limit:** All actual K4 clues are public and already inspected; this method cannot manufacture new held-out target evidence.
- **Closest local external:** H-ARCHITECTURE-DIAGNOSIS; METHOD-RESIDUAL twins; EXT-026
- **Novelty distinction:** Targets selection leakage on fresh synthetic model portfolios, not reranking the same target sentence.
- **Admission:** synthetic research proposal; not a new K4 cipher family or target authorization
- **Estimated cost:** Synthetic pilot ≤180 CPU seconds.
- **Priority:** 3
- **Sources:** 
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/AGENTS.md
  - https://github.com/matthewdgreen/decipher/blob/2dace19a0309e08e9ea8e6c40af81c26f29276a3/README.md

<a id="n100-089"></a>
## N100-089 — Minimum misspecification witness search

**Draft reference:** `M11` · **Type:** method · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** For a synthetic observation contract fixing the entire ciphertext and a disclosed plaintext mask, find the smallest edit to a bounded cipher-program AST that preserves every observation but changes a plaintext position outside the mask. This measures model-membership fragility without changing observed ciphertext.
- **Bounded test:** For 20 tiny planted relations, freeze a finite AST grammar, maximum three instruction substitutions, and unit edit metric. Enumerate or SAT-minimize program changes with the entire ciphertext and masked plaintext fixed. Independently certify minimum edit distances and compare discovery cost with random model-twin search. Parameter values within an unchanged program have distance zero and are reported separately.
- **Controls:** Zero-distance global-law aliases, one-change counterexamples, no witness within bound and perturbations affecting hidden-state propagation.
- **Identifiability limit:** Distance depends on the frozen program grammar and edit metric; it is not a probability the model is true. Only synthetic inputs are used. No canonical K4 ciphertext, clue, or claimed observation may be changed.
- **Closest local external:** Dependent twins in sparse-law pilots
- **Novelty distinction:** Generalizes one bespoke twin into a minimal adversarial certificate; known optimization ideas applied to the actual membership bottleneck.
- **Admission:** synthetic research proposal; not a new K4 cipher family or target authorization
- **Estimated cost:** Synthetic pilot ≤240 CPU seconds.
- **Priority:** 2
- **Sources:** 
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/AGENTS.md
  - https://github.com/matthewdgreen/decipher/blob/2dace19a0309e08e9ea8e6c40af81c26f29276a3/README.md

<a id="n100-090"></a>
## N100-090 — Evidence-value ranking from joint ambiguity

**Draft reference:** `M12` · **Type:** method · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Given a complete surviving model relation, rank hypothetical additional observations by worst-case remaining joint candidates instead of by word appeal.
- **Bounded test:** On synthetic ambiguous cases, choose one unrevealed position or state observation using minimax partition size, compare to random and maximum marginal entropy, then reveal synthetic truth.
- **Controls:** Nonuniform duplicate keys, correlated positions and inaccessible observations.
- **Identifiability limit:** No new K4 oracle or private plaintext access is implied. Ranking cannot be used to solicit unauthorized third-party disclosures.
- **Closest local external:** H-FEISTEL-3ROUND ambiguity; METHOD-RESIDUAL-010
- **Novelty distinction:** Operationalizes ambiguity into a next-evidence decision with complete joint relations, not heuristic language ranking.
- **Admission:** synthetic research proposal; not a new K4 cipher family or target authorization
- **Estimated cost:** Synthetic pilot ≤120 CPU seconds.
- **Priority:** 3
- **Sources:** 
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/AGENTS.md
  - https://github.com/matthewdgreen/decipher/blob/2dace19a0309e08e9ea8e6c40af81c26f29276a3/README.md

<a id="n100-091"></a>
## N100-091 — Source-to-equation audit with proof obligations

**Draft reference:** `M13` · **Type:** method · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** A restricted source parser plus generated semantic obligations may recover external operator scope reliably enough to reduce unresolved prior-art comparisons without executing arbitrary repositories.
- **Bounded test:** Freeze supported arithmetic/table/update AST subset; independently hand-annotate30 snippets, compare extracted equations, domains and mutation timing; unsupported constructs must abstain.
- **Controls:** Dynamic imports, alias mutation, hidden normalization, dead branches and loop-bound discrepancies.
- **Identifiability limit:** This is not general program understanding or proof of external run completion. Source presence and execution remain separate.
- **Closest local external:** Read-only source-literal checker; EXT-051 missing scope
- **Novelty distinction:** Concrete expansion from literals to restricted operator semantics addressing actual audit cost; not a generic LLM summary.
- **Admission:** synthetic research proposal; not a new K4 cipher family or target authorization
- **Estimated cost:** Static source study ≤180 CPU seconds.
- **Priority:** 2
- **Sources:** 
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/AGENTS.md
  - https://github.com/matthewdgreen/decipher/blob/2dace19a0309e08e9ea8e6c40af81c26f29276a3/README.md
  - https://arxiv.org/abs/2004.03082

<a id="n100-092"></a>
## N100-092 — Monotone partial-relation certificates

**Draft reference:** `M14` · **Type:** method · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** A solver can preserve useful certified lower/upper joint bounds under resource exhaustion without confusing partial coverage with EMPTY or unique recovery.
- **Bounded test:** On deliberately interrupted tiny exact searches, verify that every reported lower relation is a subset and every upper relation a superset of the exhaustive truth; test monotonicity as more blocks complete.
- **Controls:** Empty-but-unfinished searches, apparent singleton partials, duplicate blocks and process loss before journal finalization.
- **Identifiability limit:** Only bound statements survive interruption; never infer target solution or exclusion from incomplete search.
- **Closest local external:** Original INCOMPLETE cohorts; certified preflight
- **Novelty distinction:** Generalizes resource lower bounds to semantic relation envelopes; not a retroactive repair of failed runs.
- **Admission:** synthetic research proposal; not a new K4 cipher family or target authorization
- **Estimated cost:** Synthetic interrupt pilot ≤180 CPU seconds.
- **Priority:** 3
- **Sources:** 
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/AGENTS.md
  - https://github.com/matthewdgreen/decipher/blob/2dace19a0309e08e9ea8e6c40af81c26f29276a3/README.md

<a id="n100-093"></a>
## N100-093 — Independence-aware experiment portfolio design

**Draft reference:** `M15` · **Type:** method · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Selecting mechanism tests by distinct predicted constraint relations rather than by cipher names may increase information gained per compute budget.
- **Bounded test:** On a blind synthetic mixture of30 candidate mechanisms, compare equal-cost name-order queue with quotient/diversity queue using frozen diagnostic signatures. Measure eliminated distinct operators and correct-model retention.
- **Controls:** Many aliases presented as different families, exotic models that fit everything, and absent true models requiring abstention.
- **Identifiability limit:** A portfolio result is workload-dependent; it cannot certify that a century-old puzzle favors the selected family. No adaptive target retuning.
- **Closest local external:** Canonical hypothesis queue; finite prior-art audit; H-ARCHITECTURE-DIAGNOSIS
- **Novelty distinction:** Targets duplicated computational coverage and weakly discriminating tests; standard experimental-design principles, novel application unestablished.
- **Admission:** synthetic research proposal; not a new K4 cipher family or target authorization
- **Estimated cost:** Synthetic-only pilot ≤240 CPU seconds.
- **Priority:** 2
- **Sources:** 
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/AGENTS.md
  - https://github.com/matthewdgreen/decipher/blob/2dace19a0309e08e9ea8e6c40af81c26f29276a3/README.md

<a id="n100-094"></a>
## N100-094 — Typed reversible-program synthesis

**Draft reference:** `M16` · **Type:** method · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** A typed grammar that permits only constructors with explicit inverse witnesses can find compact unseen mechanisms while eliminating ill-posed programs before search.
- **Bounded test:** Freeze12 constructors spanning genuinely distinct state/block/coding operations and description length≤5. On20 fresh synthetic programs outside existing cipher baselines, compare enumerative search with counterexample-guided synthesis under identical budgets; require exact forward/inverse recovery, not text resemblance.
- **Controls:** Identity wrappers, algebraic aliases, irreversible constructors falsely tagged reversible, and a true program outside the grammar.
- **Identifiability limit:** A compact compatible program is not necessarily the intended cipher. Grammar selected independently of K4; known prior operators excluded rather than rebranded.
- **Closest local external:** EXT-012/025/050 finite grammars; H-NONLINEAR-BLOCK
- **Novelty distinction:** The falsifiable proposal is inverse-witness-constrained synthesis with semantic novelty filters, not unbounded AI program guessing.
- **Admission:** synthetic research proposal; not a new K4 cipher family or target authorization
- **Estimated cost:** ≤300 CPU seconds synthetic pilot.
- **Priority:** 3
- **Sources:** 
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/matthewdgreen/decipher/blob/2dace19a0309e08e9ea8e6c40af81c26f29276a3/README.md

<a id="n100-095"></a>
## N100-095 — Shared-control CRT compilation

**Draft reference:** `M17` · **Type:** method · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Represent control-flow predicates once and share them between mod2 and mod13 constraints, rather than solving independently and combining incompatible branches.
- **Bounded test:** Create30 fresh piecewise-polynomial models with equality/comparison branches; compare a shared Boolean decision diagram plus field solvers against a monolithic brute-force tiny oracle and independent-factor baseline. Require exact common-law relation and measure avoided spurious combinations.
- **Controls:** Predicates distinguish full Z26 equality from equality in one field; zero divisors, inconsistent branch paths and common-support aliases.
- **Identifiability limit:** Not all control predicates decompose over CRT. Any unsupported branch remains explicit; no unsound independence assumption.
- **Closest local external:** Canonical residual common-support compilation; EXT-048/049
- **Novelty distinction:** Extends shared-support reasoning to arbitrary frozen finite control-flow conditions rather than changing residual features/lag bounds.
- **Admission:** synthetic research proposal; not a new K4 cipher family or target authorization
- **Estimated cost:** ≤240 CPU seconds synthetic pilot.
- **Priority:** 3
- **Sources:** 
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/matthewdgreen/decipher/blob/2dace19a0309e08e9ea8e6c40af81c26f29276a3/README.md

<a id="n100-096"></a>
## N100-096 — Certified state bridges across clue gaps

**Draft reference:** `M18` · **Type:** method · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** For a reversible finite-state cipher, bidirectional reachability with orbit quotient can join two clue-island state sets without enumerating every full plaintext gap.
- **Bounded test:** On fresh small-state97-letter plants, compare exact left/right state-frontier join with whole-chain solver; retain symbolic gap-language relations and count every connecting path. Measure peak relation size and complete-answer time.
- **Controls:** Two paths sharing endpoint but distinct plaintexts; unreachable endpoints; noninvertible update incorrectly assumed reversible.
- **Identifiability limit:** State reachability does not identify intervening plaintext. Compressed relations must preserve all paths and any language restriction must be explicit.
- **Closest local external:** H-TREE-STATEFUL; H-FEISTEL-3ROUND; H-AUTOKEY-EXACT
- **Novelty distinction:** Specific meet-in-the-middle state-relation compilation targets the long unknown gap; classical bidirectional search foundations.
- **Admission:** synthetic research proposal; not a new K4 cipher family or target authorization
- **Estimated cost:** ≤240 CPU seconds synthetic pilot.
- **Priority:** 3
- **Sources:** 
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/matthewdgreen/decipher/blob/2dace19a0309e08e9ea8e6c40af81c26f29276a3/README.md

<a id="n100-097"></a>
## N100-097 — Exact joint-language optimization without a veto

**Draft reference:** `M19` · **Type:** method · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Intersect a complete cipher relation with a fixed weighted finite-state language model to compute the true best-scoring full plaintext and runner-up gap without treating coordinate masks independently.
- **Bounded test:** On fresh ambiguous small models, compare exhaustive full-language scores with semiring dynamic programming over the exact joint relation; separately measure ability to abstain on misspecified/random controls.
- **Controls:** A high-scoring combination assembled from incompatible marginal letters; equal-score different laws; real-language strings outside a lexicon.
- **Identifiability limit:** Scores are preferences, not proof. No lexicon veto or claimed K4 solution; model and weights frozen from disjoint data.
- **Closest local external:** Study045 non-veto trigram scoring; canonical residual joint ambiguity
- **Novelty distinction:** Different primary output is exact optimization over factorized common-law relations, not reweighting the same105456 old autokey descriptions.
- **Admission:** synthetic research proposal; not a new K4 cipher family or target authorization
- **Estimated cost:** ≤240 CPU seconds synthetic pilot.
- **Priority:** 3
- **Sources:** 
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/matthewdgreen/decipher/blob/2dace19a0309e08e9ea8e6c40af81c26f29276a3/README.md

<a id="n100-098"></a>
## N100-098 — Low-degree hidden-state elimination certificates

**Draft reference:** `M20` · **Type:** method · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Polynomial consequences obtained by eliminating hidden state may reject nonlinear generators cheaply before full parameter search.
- **Bounded test:** For20 fresh degree≤3 finite-field state models, derive bounded-degree elimination ideals and check each consequence by independent reduction/exhaustive tiny evaluation; compare early rejection and total proof cost to complete solve.
- **Controls:** A truncated basis mistaken for a full basis, field equations omitted, empty-elimination ideal despite inconsistent full model.
- **Identifiability limit:** Only proved consequences transfer negatives; absence of a consequence is inconclusive. Composite-ring control flow requires separate treatment.
- **Closest local external:** H-AUTONOMOUS-RECURRENCE; METHOD-RESIDUAL; EXT-051
- **Novelty distinction:** Moves from linear/parity certificates to certified nonlinear elimination, not another higher-order recurrence parameter sweep. Gröbner methods are established.
- **Admission:** synthetic research proposal; not a new K4 cipher family or target authorization
- **Estimated cost:** ≤300 CPU seconds synthetic pilot.
- **Priority:** 3
- **Sources:** 
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/matthewdgreen/decipher/blob/2dace19a0309e08e9ea8e6c40af81c26f29276a3/README.md

<a id="n100-099"></a>
## N100-099 — Exact framing-capacity filters for variable-length codes

**Draft reference:** `M21` · **Type:** method · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** A finite-state codec/transport product can certify whether97 decoded plaintext letters with fixed internal positions can yield exactly97 A–Z ciphertext symbols, before any language fitting.
- **Bounded test:** For12 frozen tiny prefix/grammar codecs, construct a product automaton tracking plaintext length, code length, transport remainder and prescribed letters. Verify exact counts against exhaustive enumeration and measure pruning against crude entropy bounds.
- **Controls:** Leading-zero ambiguity, incomplete final codeword, hidden header digits, clipping, and distinct messages mapping to the same transport.
- **Identifiability limit:** A capacity pass is only necessary unless the full encoder relation is checked. Never slide public plaintext clues to ciphertext positions opportunistically.
- **Closest local external:** Compression043; EXT-024; new codec proposals
- **Novelty distinction:** Addresses a concrete missing admissibility test across variable-length codecs; not another compression library or unconstrained re-encoding.
- **Admission:** synthetic research proposal; not a new K4 cipher family or target authorization
- **Estimated cost:** ≤180 CPU seconds synthetic pilot.
- **Priority:** 3
- **Sources:** 
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/matthewdgreen/decipher/blob/2dace19a0309e08e9ea8e6c40af81c26f29276a3/README.md

<a id="n100-100"></a>
## N100-100 — Joint defect-channel localization with abstention

**Draft reference:** `M22` · **Type:** method · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Compose a frozen cipher relation with a bounded observation-channel transducer permitting either no defect, one substituted symbol, or one adjacent swap. Jointly solve plaintext, key and defect location rather than silently editing transcription to fit a crib. Compare minimum defect costs across correct and deliberately misspecified cipher families.
- **Bounded test:** On 48 fresh small-alphabet synthetic plants split evenly across pristine, one-substitution, one-adjacent-swap and wrong-family cases, enumerate complete channel-constrained solutions with an independent exhaustive oracle. Require exact defect-position sets, no missed zero-defect solutions and calibrated abstention when multiple explanations survive. Compare localization and false-correction rates to a greedy repair baseline under a frozen equal budget.
- **Controls:** Blind true defect locations; substitutions equal to original are disallowed, swaps of equal letters count zero, edge positions included. Include a wrong family that can fit only by spending a defect and an ambiguous pristine plant; the system must not label either as proven transcription error.
- **Identifiability limit:** A minimum-edit explanation is not evidence that the carved or transcribed K4 is wrong. Target use is blocked without independent transcription evidence and an explicitly authorized observation model; canonical ciphertext and clues remain untouched. Synthetic methodological success cannot justify repairing K4 to rescue an excluded cipher.
- **Closest local external:** H-PERM; existing canonical transcription policy; EXT-012/025 model validation; no direct observation-channel experiment located in the inspected ledger. Exact wider prior art remains unresolved.
- **Novelty distinction:** The test concerns a finite error-channel relation and false-correction calibration, unlike M11 which holds the entire ciphertext fixed and edits model programs. Joint decoding and edit channels are established ideas, not inventions claimed here.
- **Admission:** synthetic research proposal only; no target repair or new cipher-family admission
- **Estimated cost:** First exhaustive tiny synthetic pilot at most180 CPU seconds; no real K4 fitting.
- **Priority:** 3
- **Sources:** 
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/AGENTS.md
  - https://arxiv.org/abs/1106.1819
  - https://research.ibm.com/publications/correcting-dependent-errors-in-sequences-generated-by-finite-state-processes
