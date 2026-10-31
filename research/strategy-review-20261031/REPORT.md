# New cryptanalysis strategies for Kryptos K4

> Archive note: This is a faithful Markdown rendition of the completed report. The original report’s statement that it was private describes its preparation status; it was subsequently authorized for public repository publication on 31 October 2026. Proposed experiments remain proposals in this archived report. See [archive provenance](README.md).

*Research comparison for Reggie Chan*

31 October 2026  |  Research through this date  |  Repository snapshot de3654a

## The best opportunity is a different inference task

The clearest missing capability is **jointly inferring an unrestricted English plaintext and an English running key**, subject to exact cipher arithmetic. It is not a new cryptanalytic invention: it differs locally from 053, which scored keys induced by 1,024 fixed messages, and 054, which searched a frozen source corpus. But it is not yet the best direct K4 bet. The public cribs already force unusual key fragments under all 12 tested conventions. The immediate recommendation is a cheap, calibrated fragment feasibility check before building an expensive decoder. [R2](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/candidate-first-053/README.md) [R3](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/candidate-first-054/README.md) [L1](https://aclanthology.org/P12-2016.pdf) [R12](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/candidate-first-054/results/target_result.json)

The other worthwhile directions are narrower: conflict learning over a small, independently justified composed cipher grammar; and structure aware stochastic search within one explicitly specified composite family. Both must earn their place on blind, K4 length known-answer tests before any target run. A different solver name, a larger message bank or more fluent output is not a new cryptanalytic result.

## Recommended order

| Priority | Proposed experiment | What would be new here |
| --- | --- | --- |
| 1 | Forced fragment preflight then joint decoding | Test the English key assumption first; only then search beyond fixed banks or exact sources. |
| 2 | Shared parameter constraint synthesis with learned conflicts | Reuse contradictions across partial programs; show gains beyond existing exact propagation and enumeration. |
| 3 | Nested stochastic search for one composite family | Couple structural moves with inner key or state recovery; compare at equal compute. |

The report separates **recent developments from 2024 to 2026** from **older algorithms that may be new to this project**. Recent AI assisted decipherment is relevant chiefly as a source of scoring, search and benchmark ideas. None of the reviewed evidence establishes a general method that should solve K4.

This is a research and comparison report, not a solution claim or an experiment receipt. No new K4 solver runs or paid checker submissions were performed. The report is private; separate source archival work is not a new cryptanalysis result. Recommendations require a separate execution decision.

The comparison is based on a read-only audit of 125 primary experiment Python files, focused 053 Python and C scorers, recorded findings, and a curated primary literature review. A missing implementation means “not found in the inspected record,” not “never tried anywhere.” Results recorded in the repository were not freshly reproduced.

## What the project has already established

The existing work is substantially more rigorous than a collection of cipher guesses. It already includes custom exact constraint solving, lossless pruning, meet in the middle, character language models, finite grammar enumeration with equivalence reduction, conditional description length, planted recovery and full search null calibration. Recommendations must add a missing inference capability or a demonstrably better representation, not rebrand these techniques. [R4](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/HAND-GRAMMAR-050-FINDINGS.md) [R5](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/GROMARK-ALPHABET-FINDINGS.md) [R6](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/SIGABA-CSP889-STATE-FINDINGS.md) [R8](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/candidate-first-052/README.md)

### Two exact screens should remain at the front

A direct fixed monoalphabetic substitution is incompatible with the confirmed plaintext: ciphertext V at one-based positions 25 and 67 would have to decode to T and L. A literal pure transposition is also impossible: the confirmed words require three Es, but the full ciphertext contains only two. These are structural contradictions, not poor language scores. Better monoalphabetic or pure permutation optimizers cannot overcome them. [R1](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/STRUCTURAL-FINDINGS.md)

The scope matters. Those arguments do not rule out every stateful or layered system. A proposed additional transformation must be stated and justified before using a solver for an otherwise excluded direct model; adding a free layer after failure can simply remove falsifiability.

### The most important recent project comparison

Experiment 053 evaluated 1,024 frozen messages under 12 tableaux, inducing 12,288 keys. Its primary order-four score excluded the crib derived key letters and their context; a separate full-key entropy gate included them. All four K4 evidence gates failed; the conditional p-value was .932. Planted pairs could be recovered within that candidate framework, but semantic stress controls exposed limitations. This is evidence about that frozen search, not all English running keys. [R2](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/candidate-first-053/README.md)

Experiment 054 searched 89 source files containing 17,619,191 eligible 97-letter windows. None matched its two crib derived key fragments under the 12 tableaux. That is a strong exact negative for the specified normalization, corpus, alignment and arithmetic. It is not a rejection of an absent source, paraphrase, another tableau or unrestricted natural language key. [R3](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/candidate-first-054/README.md)

### Feasible is not identified

Custom Gromark constraint solving already handles modular graph potentials and global alphabet injectivity. The identifiability audit shows why a compatible witness is not enough: within the stated model, some noncrib letters are forced while many remain variable. Similarly, resource limited real size SIGABA engineering does not establish a completed search over the full joint state space. Keep compatible, excluded and inconclusive as separate outcomes. [R5](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/GROMARK-ALPHABET-FINDINGS.md) [R11](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/GROMARK-IDENTIFIABILITY-FINDINGS.md) [R7](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/SIGABA-SUPPORT-SIGNATURE-041-FINDINGS.md)

## Comparison matrix

“New here” refers only to the inspected code and records at the pinned commit. It is not a claim of novelty in cryptanalysis.

| Method | What is already present | Useful distinction or verdict |
| --- | --- | --- |
| Joint English plaintext and key inference | 053 fixed message bank; 054 exact source lookup. | Different search space. Forced fragment gate first, then a 97-letter benchmark. |
| SAT SMT and constraint programming | Custom modular propagation, AllDifferent, MRV depth first search and state support. | A generic backend alone adds no model coverage. Test learned conflicts and joint partial parameters. |
| Meet in the middle | Exact SIGABA cipher start joins under fixed schedules. | Already used. Only a new justified factorization is a new contribution. |
| Language models | 045 trigrams; 053 order-four character scoring. | Neural scoring is unverified here. Test whether better ranking, rather than search, is the bottleneck. |
| Annealing MCMC tempering | No implementation found in inspected primary code; genetic coverage is unresolved. | Potentially new implementation, not a new cipher hypothesis. Must preserve structural constraints. |
| Program synthesis | 050 exhausts depth three hand grammar and canonical operators. | Incremental learned exclusions may help; unrestricted grammar expansion mainly adds overfit. |
| Neural monoalphabetic solvers | Not implemented in inspected code; direct model already contradicted. | Do not run directly on K4. Conditional subroutine only in a justified composite model. |
| MDL and null calibration | Conditional model costs and full frozen search maxima already evaluated. | Retain and extend to every new adaptive choice. Not a novelty claim. |
| LLM orchestration | Existing agent aided research and provenance workflow. | Convenience and auditability, not independent cryptanalytic evidence. |
| Projected ambiguity | Gromark marginal identifiability and model volume work. | Extend across a joint grammar only if useful. Count distinct plaintexts, not auxiliary assignments. |
| Algebraic elimination | Exact modular and graph consistency routines already used. | Useful only for an unexploited cross-stage relation. Mod 26 addition is not XOR. |
| Finite state inference | No language-weighted joint WFST decoder identified; other DP and segmentation routines exist. | Conditional tool for small state models; arbitrary routes and rotor states may explode. |

Evidence for the matrix is linked in the repository appendix: 053 and 054; Gromark; fixed schedule SIGABA and 041; grammar 050; language 045; and candidate first 052. [R2](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/candidate-first-053/README.md) [R3](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/candidate-first-054/README.md) [R12](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/candidate-first-054/results/target_result.json) [R5](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/GROMARK-ALPHABET-FINDINGS.md) [R6](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/SIGABA-CSP889-STATE-FINDINGS.md) [R7](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/SIGABA-SUPPORT-SIGNATURE-041-FINDINGS.md) [R4](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/HAND-GRAMMAR-050-FINDINGS.md) [R9](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/COVER-LANGUAGE-045-FINDINGS.md) [R8](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/candidate-first-052/README.md)

The audit did not locate MCMC, annealing, parallel tempering, a neural likelihood scorer or a generic SAT SMT MILP backend in the inspected primary implementations. Some planning documents mention genetic or continuation coverage without an identified code path or run receipt. Treat that item as unverified rather than “never used.”

## What changed in the recent literature

Recent work is most useful when its demonstrated task matches the proposed subproblem. A neural system that solves an ordinary substitution cipher is not evidence that K4 uses substitution, and a tool wrapper is not a new attack. The relevant question is which capability transfers under a stated model and can be verified at 97 letters.

### Recent methods to assess cautiously

**Z340 in 2024:** the primary paper documents a solution achieved in 2020. Its transferable workflow couples bounded outer transformations with a strong inner substitution solver and independent verification. A solved 340 character homophonic plus transposition cipher is not evidence of comparable power on K4’s 97 letters. AZdecrypt is available, but its applicability depends on an admissible outer model. [L6](https://arxiv.org/abs/2403.17350)

**ALICE in 2025:** a released neural monoalphabetic solver reports strong short text results, but spaces and punctuation are preserved. Its direct model contradicts K4’s cribs. **The 2026 attention LSTM result** uses a shared fixed code mapping across training and testing, not an unseen independently keyed cipher. Neither warrants a direct K4 attack or training on desired K4 messages. [L7](https://arxiv.org/abs/2509.07282) [L8](https://arxiv.org/abs/2606.05078)

**Recent symbolic automation:** Divide and Conquer SAT in 2025 and BONC and CLAASP MP in 2026 analyze known primitive structures or implementations. Their differential, linear and algebraic results do not supply the missing cipher specification or chosen input data for K4. Borrow modeling techniques only after constructing a sound classical cipher model. Dream Decompiling’s 2024 revision concerns noncryptanalytic program synthesis, not recovery from 24 crib letters. [L10](https://tosc.iacr.org/index.php/ToSC/article/view/12479) [L9](https://doi.org/10.1186/s42400-026-00556-9) [L11](https://eprint.iacr.org/2026/735) [L19](https://arxiv.org/abs/2306.07856)

### Infrastructure and evaluation in 2026

DescryptTool uses language models to orchestrate existing cryptanalytic tools in an auditable workflow. That is operationally useful, but overlaps the project’s existing emphasis on agents, provenance and reproducible receipts. It should not be presented as a demonstrated general cipher solving breakthrough or a reason to relax verification. [L3](https://www.tandfonline.com/doi/full/10.1080/01611194.2026.2693460)

HistCiph provides synthetic historical multilingual cipher data across lengths from 50 to 1,000 characters, with independent keys and noise variants. Its value here is benchmark design: separate text sources and keys, stress realistic variation, and test at the target length. Its homophonic settings do not imply that K4 is homophonic. [L4](https://aclanthology.org/2026.resourceful-4.2.pdf)

### A private plaintext checker is not an inference oracle

The current keeper describes a paid check against a privately held Sanborn supplied plaintext. That is different from public validation of a cryptanalytic derivation. Do not use this service as a search score or query it without authorization. Archival access to a plaintext and recovery of the mechanism from ciphertext are different achievements. [L5](https://www.paradigm.xyz/writing/kryptos)

The review found no verified 2024 to 2026 result establishing a broadly applicable attack on a 97-letter, unknown family, partly cribbed cipher with K4’s constraints. This is a limit of the reviewed evidence, not a proof that no such work exists. Specific recent results belong in benchmark comparisons, not in a promise of recovery.

## Mature ideas that may still add capability

### Joint running key inference

Reddy and Knight jointly estimate an English plaintext and English running key under a known substitution function using blocked Gibbs sampling. At 100 characters, their reported mean character accuracy was 42 percent on Gutenberg and 58 percent on Wall Street Journal data. These are partial character accuracies, not exact solution rates; the experiment did not reproduce K4’s 24 known positions. Unknown keyed tableau inference was not an established result. The paper motivates a benchmark, not confidence in K4 recovery. [L1](https://aclanthology.org/P12-2016.pdf)

The local gap is a decoder that is allowed to discover texts absent from both the candidate bank and the source corpus. It must search under exact arithmetic rather than generate a persuasive sentence and attach an unconstrained key afterward. Existing crib derived key fragments remain binding constraints under the selected tableau. [R2](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/candidate-first-053/README.md) [R3](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/candidate-first-054/README.md)

### Separate a search failure from a scoring failure

The 2014 short substitution study combines word and character language information with tree search. Its task is not a direct K4 candidate. The transferable lesson is diagnostic: finding a higher scoring string is not necessarily finding the true plaintext, so improving the optimizer and improving the objective are separate jobs. [L2](https://sites.ualberta.ca/~hayward/papers/substncipher.pdf)

On known-answer fixtures, score the true solution even when the search misses it. If truth outranks the returned candidate, improve search. If a wrong candidate outranks truth, improve the model or reject that scoring objective. If many distinct candidates remain indistinguishable, report nonidentifiability rather than forcing a winner. This diagnostic is especially important at 97 letters.

### Constraint learning and synthesis

Transalg and CDCL Crypto provide precedents for verified encodings and domain aware propagation or conflict analysis. They do not establish tractability for an unknown classical cipher. The local extension worth testing is shared unknown stage and key parameters with reusable learned contradictions. Existing MRV search, AllDifferent constraints and dynamic support filtering already propagate constraints; ordinary incremental calls alone are not the novelty. [L13](https://lmcs.episciences.org/6177/pdf) [L12](https://arxiv.org/abs/2005.13415) [R4](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/HAND-GRAMMAR-050-FINDINGS.md) [R5](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/GROMARK-ALPHABET-FINDINGS.md)

### Stochastic methods are tools rather than cipher families

Annealing, MCMC, sequential sampling and tempering describe ways to explore a defined state space. Their usefulness depends on moves that respect the cipher’s structure, a score with measured discrimination and a budget that reaches meaningful candidates. The project’s missing implementation is an opportunity to test these ingredients, not evidence that repeated restarts will reveal the answer.

Chen and Rosenthal provide a mature MCMC basis and author software, but their longer, spaced material is not a matched K4 benchmark. Neural guided constrained search from 2018 is a possible scoring component, not a license for unconstrained generation. Finite state decoding and dissection are conditional alternatives: first demonstrate a small reachable state space or a valid, selective join over known information. [L14](https://probability.ca/jeff/ftpdir/decipherartpub.pdf) [L15](https://aclanthology.org/D18-1102.pdf) [L16](https://aclanthology.org/N10-1068.pdf) [L17](https://eprint.iacr.org/2012/217.pdf)

## Priority one joint plaintext and key decoding

**Question:** Can an open-vocabulary decoder recover both unknown texts in K4 length fixtures when the correct message and key source are absent from the frozen banks? This directly tests the most clearly identified coverage gap. It does not assume that K4 uses an English running key.

### Gate zero fixed fragments before a decoder

Under the 054 conventions, the public cribs fix 13 key letters at positions 22 to 34 and 11 at positions 64 to 74, with starts 42 letters apart. For ordinary alphabet Vigenère the first fragment is BLZCDCYYGCKAZ; for KRYPTOS alphabet on both axes it is RDUMRIYWOYNKY. None of the 12 first fragments occurred in the frozen corpus. No proposed plaintext can repair them within its fixed convention. This is corpus absence, not proof that English is impossible. [R12](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/candidate-first-054/results/target_result.json)

Before decoder development, independently verify all pairs and preregister a plausibility diagnostic against genre diverse normalized English windows, allowing word boundary crossings and stressing names and compressed language. Preserve both lengths and spacing; account for selection among all 12 conventions. **Do not use crib-preserving ciphertext nulls here:** they leave the fragments unchanged. If no convention passes the frozen criterion, stop this direct English key branch rather than invent an arbitrary alphabet. The diagnostic is proposed, not executed.

### Model and implementation

Freeze a small set of explicitly defined tableaux, indexing conventions and spelling normalization before scoring. For each fixture, require the cipher relation at all 97 positions and the same 24-position clue mask as the real task. Maintain separate language priors for plaintext and key; retain uncertainty over word boundaries and unknown words instead of forcing one dictionary segmentation.

If the preflight passes, compare a blocked sampler with an independent bounded beam or finite state baseline where feasible. Start with character and word models; add neural rescoring only if fixtures expose a ranking bottleneck. Preserve exact arithmetic at every retained state. Agreement between implementations is a debugging check, not independent evidence about K4.

### Benchmark before the target

- Create a development set and a separate blind test set, split by source document and attributed author. Include ordinary prose, proper names, terse language and misspellings without K4 themed authoring. Ensure the test plaintext and key are absent from all candidate and training sources used for direct lookup.

- Proposed initial scale: 100 held-out positive fixtures per model class, including source-absent English keys, and 200 family-appropriate negatives, including mismatched families and word order disruption. These counts are design proposals, not established standards.

- Report exact 97-letter recovery, noncrib character accuracy over 73 letters, key accuracy, true solution rank, restart variation, CPU time and memory. Compare with the existing fixed bank scorer on shared fixtures where that comparison is meaningful, and with a simple constrained decoding baseline on source-absent fixtures.

### Go or stop

Use an initial **8 CPU hour and 8 GB memory pilot cap** to measure throughput, not as a promised completion time. Tune on development data only. Before opening the blind set, freeze the final compute allocation, seeds, minimum useful exact recovery rate and confidence procedure. Proceed to proposing a target run only if exact recovery improves over an equal-budget baseline and calibrated positives are distinguishable from negatives.

Stop this implementation if the frozen benchmark cannot separate true recoveries from false selections, if apparent gains are only character accuracy without useful exact recovery, or if results depend on inserting K4 themed messages. A failed decoder is not an exclusion of English running keys. A passed decoder authorizes no automatic K4 run; it supplies evidence for the next decision.

## Priority two learned conflicts over a small grammar

**Question:** Can a shared parameter representation eliminate repeated work across partial composed cipher programs while preserving complete, checkable semantics? Merely adding a SAT solver is not the experiment. Existing custom propagation and depth three grammar enumeration are the baselines. [R4](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/HAND-GRAMMAR-050-FINDINGS.md) [R5](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/GROMARK-ALPHABET-FINDINGS.md)

### Define what is genuinely different

Choose one compact grammar on independent historical or mechanical grounds. Explicitly define each operator, inverse, key domain, global position alignment and allowed composition depth. Compare its canonical operator closure with 050. If all new descriptions reduce to operators already tested, this is an engineering benchmark only; it adds no K4 coverage.

Represent shared unknown keys and structure jointly while the program is partial. Learn reusable nogoods from contradictions, with clear validity conditions, rather than enumerating a completed program and rediscovering the same failure. Use incremental assumptions to compare related structures. A candidate program must have one global rule; do not repair individual letters with exceptions introduced after seeing the target.

A refinement loop may start with a sound relaxation and add only provably valid cuts after checking the exact admissible model. UNSAT of that overapproximation excludes its concrete subset; SAT does not establish concrete feasibility. There is no true K4 encryption oracle from which counterexample guided synthesis can obtain fresh plaintext. Available counterexamples concern encoding, implementability or equivalence, not whether an unknown plaintext is historically correct.

### Benchmark and ablate

- First reproduce small exhaustive domains in which every compatible solution can be independently enumerated. Check soundness of every learned exclusion and exact equality of solution sets. Include contradictions, multiple solutions and planted solutions.

- Then use blind 97-letter fixtures with the 24-position mask, including an out-of-grammar set. Compare plain enumeration, the existing propagation style, the same new representation without learning, and the learned version under equal compute.

- Measure exact recovery, complete bounded exclusions, time to first and all witnesses, visited states, memory and effective reuse of learned conflicts. Count canonical operators, not syntactic aliases. Preserve proof or independently replayable contradiction receipts when the backend supports them.

### Go or stop

Begin with the shared 8 CPU hour and 8 GB pilot cap, then freeze a measured benchmark budget. Stop if learned exclusions are unsound, gains disappear after equalizing representation and compute, the grammar is already covered, or larger models produce many unrelated fluent fits. Only a sound new representation with measured recovery or pruning gains earns consideration for a narrowly scoped target experiment.

A timeout is **inconclusive**. An exhaustive contradiction excludes only the precisely encoded bounded family. A satisfiable witness demonstrates compatibility, not uniqueness or historical correctness. The new method is valuable only if it improves a verifiable outcome, not simply because it uses SMT, CP SAT or a modern synthesis label.

## Priority three nested stochastic search

**Question:** For one justified composite family that survives the structural screens, can structure aware stochastic moves find exact solutions more efficiently than simple restarts or deterministic search? This is lower priority because a flexible composite model can fit short texts without identifying the true mechanism.

### Keep the hypothesis narrow

Select one family before target inspection, such as an explicitly specified substitution plus transposition construction or a defined fractionation construction. State its key lengths, operator order, padding, alignment and equivalences. Do not reopen direct monoalphabetic substitution or pure transposition: their literal K4 forms are already contradicted. [R1](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/STRUCTURAL-FINDINGS.md)

Use an outer search over a small structural choice and an inner recovery step over key or state parameters, borrowing the nested search architecture rather than the cipher assumptions of Z340. Moves should preserve valid permutations, alphabet bijections or state transitions. Cache only mathematically reusable quantities. Consider annealing or tempering only if diagnostics show trapping; replica exchange would be a proposed optimizer comparison, not an established K4 method. [L6](https://arxiv.org/abs/2403.17350) [L14](https://probability.ca/jeff/ftpdir/decipherartpub.pdf)

Compare a plain hill climber or bounded beam, multistart local search and the proposed nested sampler at equal compute. Freeze scoring and move schedules on development fixtures. If a language model changes, rerun the comparison and the negative controls; do not carry over thresholds from the old objective.

### Benchmark before considering K4

- Use 100 blind positives per declared family and 200 appropriate negatives as an initial proposed design. Match length and clue geometry, but vary text sources, keys and structural parameters. Include the correct structure missing from the search space as a control.

- Record exact plaintext and key recovery, success versus restart count, acceptance and mixing diagnostics where applicable, wall time, CPU time and peak memory. Distinguish key equivalence from a genuinely different key, and count any score or family selection in the total search budget.

- Evaluate the true solution’s score independently. Where tractable, exact low order optimization can expose search error under the same objective. If the correct key scores worse than false candidates, more restarts are not the remedy. If truth scores well but is rarely reached, assess whether moves or decomposition improve access to it. [L18](https://aclanthology.org/D08-1085.pdf)

### Go or stop

Use the same bounded pilot policy, then preregister the blind evaluation. Stop if equal-budget gains are absent, the method succeeds only on long texts but fails at 97 letters, false controls produce equally persuasive output, or the fitted rule needs arbitrary per position adjustments. Do not expand key length or composition depth after each failure without treating that as a new model and recalibrating.

This direction is best treated as a **method development pilot**, not a broad cipher fishing campaign. A negative heuristic search cannot exclude its family. A successful synthetic pilot shows capability under its generating assumptions; it still does not establish those assumptions for K4.

## A shared evidence standard for all three experiments

### Freeze the task before measuring it

Write a manifest containing ciphertext convention, alphabet order, crib coordinates, allowed models, source normalization, training data, seeds, budgets and exact metrics. Separate development and blind evaluation. Choose the minimum useful success rate before opening the blind test, based on intended research value and pilot cost rather than the result obtained. Report confidence intervals for recovery and false selection rates.

Use blind synthetic fixtures for held-out evidence. Public K4 clues are already known: masking a group diagnoses sensitivity but does not make it independent confirmation. Model forced letters must not become public cribs. The same 24-position mask is not necessarily the same information: repeated letters and equality patterns affect constraint strength. Report that difference and add literal crib or equality matched stress tests where feasible, without treating artificially forced sentences as representative English.

### Calibrate the complete adaptive procedure

Negatives should preserve relevant task information and pass through the same candidate generation, model selection, restarts and ranking as positives or the target. Uniform random strings alone may be too easy. Include family specific mismatches, absent sources and adversarial language controls. The existing full frozen search null methodology is a foundation, not a ready made threshold for a new adaptive decoder. [R2](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/candidate-first-053/README.md) [R8](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/candidate-first-052/README.md)

Maintain a cumulative decision ledger. A per experiment conditional p-value is not a project wide error guarantee after many model changes. An MDL preference is not a posterior probability that the artist used the winning construction. Report both the model cost and the exact search choices that were available.

### Candidate acceptance checklist

- All 24 confirmed plaintext letters agree at their fixed coordinates, with no shifted or respelled clue substitutions.

- An independent implementation encrypts the complete 97-letter candidate to the canonical ciphertext exactly, using the stated alphabet, key, state and normalization.

- The key and rule are bounded and reproducible. No freely selected 97-letter key, per letter exceptions or after the fact padding changes are used as evidence of discovery.

- The same frozen pipeline shows meaningful recovery and discrimination in blind controls. The result is stable enough to survive independent reconstruction, not just one favorable seed.

- Historical key or source provenance, an independently motivated mechanism, or new independent evidence supports the interpretation. Grammatical prose and thematic resemblance are not independent cryptographic evidence.

### Use precise outcome labels

**Recovered** means the known-answer was recovered in a fixture. **Compatible** means a model satisfies constraints. **Excluded** requires a complete contradiction within an explicit bounded domain. **Not found** describes a finished limited search. **Inconclusive** covers timeouts, underpowered controls and unresolved nonidentifiability. These labels prevent both inflated positives and inflated negatives.

## Technical appendix on scope and reproducibility

### What the recorded negatives do and do not say

| Recorded result | Defensible conclusion | Not established |
| --- | --- | --- |
| 053 all evidence gates failed | No support under its frozen candidate bank, tableaux, scorer and calibration. | All natural language running keys are impossible. |
| 054 zero corpus window hits | No exact hit in the frozen source windows and declared variants. | The true key source does not exist or is not English. |
| 050 zero exact grammar hits | The defined depth zero to three operator closure does not fit. | No hand executable composition can fit. |
| Fixed schedule SIGABA rejection | The tested cipher starts under those fixed schedules fail. | All controller states, wiring assumptions and joint rotor models are excluded. |
| Real size joint solver budget limits | The present representation has not met its recovery gate. | K4 has been exhaustively tested under the full historical machine. |

These distinctions are grounded in the pinned records, not fresh reexecution. [R2](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/candidate-first-053/README.md) [R3](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/candidate-first-054/README.md) [R4](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/HAND-GRAMMAR-050-FINDINGS.md) [R6](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/SIGABA-CSP889-STATE-FINDINGS.md) [R7](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/SIGABA-SUPPORT-SIGNATURE-041-FINDINGS.md)

### Minimal future run receipt

A useful receipt should include the code commit and environment, source hashes and licenses, exact model domain, canonicalization rule, train and test split, seed list, compute usage, all candidate maxima, control outputs and an independent roundtrip verifier. Retain failed controls and every target facing model choice, not only the winning plaintext. Preserve machine readable results alongside a short explanation of what was and was not tested.

### Research limits

This review combines primary source reading with an implementation and findings audit. Literature performance is reported only in the setting measured by its authors. No historical machine specification, cipher family or authorial intent was inferred from a language score. The cited 2026 sources were available by the research date; the report does not claim an exhaustive survey of every preprint or unpublished attack.

The audit covers 125 primary experiment Python files plus focused 053 scorers and supporting records at commit de3654a098162185d47b7c14ee1eef1631ab1804. Repository results were read, not rerun. Separate archival work may advance the current branch without altering this research snapshot. Absence claims are restricted to the inspected code and execution record.

The next useful result is a decoder or representation that demonstrably recovers blind 97-letter fixtures under a matched information budget. That is more informative than another impressive looking K4 paragraph, a larger unfalsifiable grammar, or a solver applied to a model already contradicted by the clues.

## Sources and implementation evidence

References are clickable. Literature sources support only their stated task and performance scope. Repository links are pinned to the research snapshot rather than a moving branch.

### Primary literature and current context

- **[L1]** [Reddy and Knight 2012 Decoding Running Key Ciphers](https://aclanthology.org/P12-2016.pdf) — ACL 2012. Primary paper on simultaneous English plaintext and running key inference. Not a K4 evaluation.

- **[L2]** [Hauer Hayward and Kondrak 2014 Solving substitution ciphers with combined language models](https://sites.ualberta.ca/~hayward/papers/substncipher.pdf) — COLING 2014. Short monoalphabetic cryptograms, language scoring and tree search. Direct model is incompatible with K4 cribs.

- **[L6]** [Oranchak Blake and Van Eycke 2024 The solution of the Zodiac 340 cipher](https://arxiv.org/abs/2403.17350) — Primary account posted March 2024 of the December 2020 solution. A different, longer cipher and model.

- **[L7]** [ALICE 2025 neural substitution decipherment](https://arxiv.org/abs/2509.07282) — September 2025 preprint. Monoalphabetic task retains word spaces and punctuation. Author code at github.com/al-jshen/alice.

- **[L8]** [Attention LSTM cipher decoding 2026](https://arxiv.org/abs/2606.05078) — June 2026 preprint. Shared fixed code mapping across training and test, not independent unknown keys.

- **[L3]** [Kopal and Megyesi 2026 DescryptTool](https://www.tandfonline.com/doi/full/10.1080/01611194.2026.2693460) — Published 7 September 2026. LLM orchestration of existing cryptanalytic tools; not a demonstrated general K4 attack.

- **[L4]** [Bruton Beloucif and Megyesi 2026 HistCiph](https://aclanthology.org/2026.resourceful-4.2.pdf) — RESOURCEFUL 2026. Historical multilingual synthetic cipher data and benchmark design, not evidence for a K4 cipher family.

- **[L5]** [Paradigm 2026 Kryptos](https://www.paradigm.xyz/writing/kryptos) — Keeper statement dated 12 June 2026. Describes a private plaintext checker and future K5 plans; does not independently validate a submitted encryption method.

- **[L9]** [BONC 2026 automatic cryptanalysis framework](https://doi.org/10.1186/s42400-026-00556-9) — Published 16 February 2026. Known implemented primitives and supported frontend operations, not unknown mod 26 cipher discovery.

- **[L10]** [Divide and Conquer SAT 2025](https://tosc.iacr.org/index.php/ToSC/article/view/12479) — September 2025. Differential and linear characteristic search for known block ciphers, not direct K4 plaintext recovery.

- **[L11]** [CLAASP MP 2026](https://eprint.iacr.org/2026/735) — April 2026 ePrint. Algebraic degree, monomial prediction and related known primitive analysis.

- **[L19]** [Dream Decompiling revised 2024](https://arxiv.org/abs/2306.07856) — Initial 2023 preprint revised May 2024. Learned library selection on noncryptanalytic synthesis tasks.

- **[L12]** [Nejati and Ganesh 2020 CDCL Crypto](https://arxiv.org/abs/2005.13415) — Domain aware propagation and conflict analysis. Architectural precedent; published speedups are not K4 estimates.

- **[L13]** [Transalg 2020](https://lmcs.episciences.org/6177/pdf) — Primary paper on procedural cipher to SAT translation. Encoding a problem does not make it tractable.

- **[L14]** [Chen and Rosenthal 2011 and 2012 Decrypting classical cipher text using Markov chain Monte Carlo](https://probability.ca/jeff/ftpdir/decipherartpub.pdf) — Online 2011 and journal 2012. Author implementation at probability.ca/decipher. Longer, spaced test material limits transfer.

- **[L15]** [Kambhatla and colleagues 2018 neural language guided decipherment](https://aclanthology.org/D18-1102.pdf) — EMNLP 2018. A neural scorer guides constrained substitution search; not free form text generation.

- **[L16]** [Chiang and colleagues 2010 finite state cascade training](https://aclanthology.org/N10-1068.pdf) — NAACL 2010. Bounded state inference and training; global key tying and state explosion remain relevant.

- **[L17]** [Dinur Dunkelman Keller and Shamir 2012 Dissection](https://eprint.iacr.org/2012/217.pdf) — Primary work on independently decomposable structures. Partial cribs do not automatically provide a usable join interface.

- **[L18]** [Ravi and Knight 2008 exact decipherment optimization](https://aclanthology.org/D08-1085.pdf) — EMNLP 2008. Integer programming can diagnose search versus language model error in a stated substitution setting.

## Pinned implementation evidence

### Pinned project records

- **[R1]** [Structural findings](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/STRUCTURAL-FINDINGS.md) — Pinned repository evidence. Exact exclusions apply to the stated direct literal models.

- **[R2]** [Candidate first 053 findings](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/candidate-first-053/README.md) — Pinned repository evidence. Fixed message bank and order four language scoring, controls and conditional calibration.

- **[R3]** [Candidate first 054 findings](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/candidate-first-054/README.md) — Pinned repository evidence. Exact frozen corpus lookup and its limited negative scope.

- **[R12]** [Candidate first 054 exact target receipt](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/candidate-first-054/results/target_result.json) — Pinned source for all twelve forced key fragment pairs and exact lookup counts.

- **[R4]** [Hand grammar 050 findings](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/HAND-GRAMMAR-050-FINDINGS.md) — Pinned repository evidence. Depth three grammar, canonical operators and finite negative result.

- **[R5]** [Gromark alphabet findings](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/GROMARK-ALPHABET-FINDINGS.md) — Pinned repository evidence. Modular graph potentials, injectivity and custom exact constraint search.

- **[R6]** [SIGABA fixed schedule state findings](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/SIGABA-CSP889-STATE-FINDINGS.md) — Pinned repository evidence. Exact meet in the middle over stated cipher starts and fixed schedules, not full SIGABA exclusion.

- **[R7]** [SIGABA support signature 041 findings](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/SIGABA-SUPPORT-SIGNATURE-041-FINDINGS.md) — Pinned repository evidence. Synthetic engineering and resource limits, not a new K4 target result.

- **[R8]** [Candidate first 052 findings](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/candidate-first-052/README.md) — Pinned repository evidence. Conditional description length and full frozen search null calibration.

- **[R9]** [Cover language 045 findings](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/COVER-LANGUAGE-045-FINDINGS.md) — Pinned repository evidence. Character trigram rescoring and recovery versus null behavior.

- **[R10]** [Candidate first 048 findings](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/CANDIDATE-FIRST-048-FINDINGS.md) — Pinned repository evidence. Pattern and frozen Brown document source search.

- **[R11]** [Gromark identifiability findings](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/research/GROMARK-IDENTIFIABILITY-FINDINGS.md) — Pinned repository evidence. Compatible models need not uniquely identify plaintext.
