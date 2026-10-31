# Study 060 Evolving alphabet mechanisms

## Scope and novelty admission

This study evaluates exactly the two specifications in the copied source proposal: A ciphertext-driven alphabet exchange, B fixed-reference ciphertext-indexed prefix reversal. Each uses R and S0 independently selected from ordinary AZ and KRYPTOSABCDEFGHIJLMNQUVWXZ. A varies q0=0..25; B varies constant input offset k=0..25. There are 104 descriptions per arm and 208 in the union. No extra key, arbitrary alphabet, reset, stage, padding, alternate update or shift in clue positions is permitted.

The state persists from the first character. In A, emit from old S at j=index_R(P), exchange j with old q, then advance q by index_R(C)+1 modulo26. In B, emit at (index_R(P)+k) modulo26, then reverse the prefix of length1+index_R(C), measured in the fixed R rather than the changing S. Decryption uses the inverse current permutation and performs the identical update.

The source proposal and independent review copied into this archive were created before execution authorization. Their copied texts preserve the earlier ideation-only wording as historical provenance; the user subsequently authorized execution on31October2026 at15:03UTC. Novelty here means no matching K4 experiment located in the reviewed records, not a claim of globally new cryptography. The closest comparisons are local move-to-front/tree-path updates and external EXT-002 (Scott CONDI/Chaocipher notes), EXT-008/009 (ActiveTK equation-based selfkey). Existing optimizer alphabet swaps are not cipher-state swaps. Related RC4/Chameleon/LC4 designs are acknowledged, not claimed as our inventions. The dated targeted search and pinned-source comparison in the source proposal and review form the prior-art admission evidence. Neither model is justified as Sanborn's actual system.

## Outputs and alias handling

For every input, exhaust all208 raw descriptions, return every matching description and its complete plaintext, then deduplicate identical full plaintexts. Count raw descriptions and distinct plaintexts separately. Do not infer distinct global encryption operators from one ciphertext's state traces or sampled probes. B's104 descriptions have only four ciphertext-driven histories; different offsets can still give different plaintexts. An explicit separating plaintext for every pair of configurations proves they are different encryption functions; if every witness is independently replayed, this certificate can justify a distinct-operator count. Mere failure to find a separator cannot prove equivalence. Zero candidates after complete enumeration excludes this finite union, whether or not descriptions alias. All matching descriptions must independently re-encrypt the entire input.

## Development validation

An independent reference is authored before inspecting production. Tiny analogue: alphabet ABC and ACB; both mechanisms; 3 parameters; message length5. Compare all forward encryptions, decryptions and every possible 5-letter ciphertext with all3^3 crib assignments at positions0,2,4 against a forward-generated truth table. Both implementation result sets must agree exactly. Verify each full26-symbol first-step mapping is a bijection for all208 descriptions. Tiny controls contain wrong cribs, ambiguity and plaintext aliases, and do not use K4.

## Blind benchmark

Freeze this protocol, source proposal, production, independently authored reference, fixture generator, runner, analysis and development receipts before drawing a fresh seed. The generator creates416 positives: one uniform random 97-letter plaintext and one literal-clue plaintext for each of208 generating descriptions. Literal fixtures contain EASTNORTHEAST at zero-based21:34 and BERLINCLOCK at63:74; the remaining letters are uniform random, not natural language. Uniform fixtures use24 independently generated plaintext letters at the same positions. Add64 independent uniform ciphertext controls,32 with uniform clue values and32 with the literal clues. No rejection, uniqueness filtering or resampling.

Shuffle the480 cases using a fresh256-bit seed. Solver inputs reveal only opaque ID, ciphertext and crib values. Answers and configurations are stored separately and not inspected until both output files have been sealed by SHA256. Procedural synthetic blinding does not make the already public K4 clues unknown to the researchers.

Frozen gates:
1. All tiny exact controls and full-alphabet bijections pass.
2. Both engines complete all480 inputs under the resource caps and return identical full raw-description/plaintext sets and deduplicated plaintext sets.
3. All416 generating descriptions and plaintexts are present; every returned candidate independently re-encrypts all97 symbols.
4. At most1 of64 random controls returns any compatible plaintext in the full two-arm union. This operational gate is not a posterior probability or project-wide significance claim.
5. Independent audit verifies all frozen hashes, seed replay, seals, completeness, result sets, gates and resource receipts. Unique recovery is descriptive only; aliases or multiple valid plaintexts are not failures.

Failed gates stop target evaluation. A post-unblinding corrective change must preserve the failed run and use a separately reviewed fresh holdout, never silently change thresholds. Target stage requires explicit parent approval after the audit. The approved target would be one production and one reference evaluation of the canonical97-letter K4 string with the24 fixed clues, followed by independent audit. No target input is included in the benchmark source or fixtures.

## Resources and closeout

Shared upper cap8CPUhours and8GiB. This small study reserves120CPUseconds for preparation, tiny checks and compilation. Each sequential production/reference batch has hard120CPUseconds,512MiB address space and300seconds wall time. The runner records elapsed time, child CPU, parent CPU, exit status and max RSS even on failure. Analysis and independent audits have separately recorded CPU entries. Stop if a cap is exceeded; partial output is not complete exclusion.

At study closeout, retain raw inputs, answers, seed, result sets, hashes and audits. Reconcile canonical HYPOTHESES/EXPERIMENTS, reviewed classifications, generated navigation and external overlap notes before selecting the next family. Scientific completion and public publication are separate. No new cipher rule is introduced following a negative result.
