> **Future design / toy mathematical checks only.** No v2 performance, fresh holdout or K4 result is established here. Public prose sanitization is mapped in PUBLIC-PROVENANCE.json.

# Parity-first quotient decoder: independently audited future v2 design

2026-10-31.  Inputs read: quotient audit REPORT.md and crib-completion-code-design.md. No frozen v1 code, holdout, labels, K4 target, or remote repository was read/modified. This is NOT a v1 protocol amendment. Verdict: all five proposed steps are sound, with the qualifications below. No performance or global-novelty claim.

## Model and exactness

Use the verified 31-feature dictionary: constant; six lags; six squares; fifteen distinct pair-products; three full-Z26 equality indicators. Let G map31 feature indices to25 groups: six lag/square pairs and19 singletons. Write H for the24×25 binary evaluation matrix and A for the24×31 mod13 evaluation matrix. Indicators must be evaluated on original full-Z26 contexts before reduction; neither field component alone determines equality. Use b=C−P at the24 allowed cribs, not plaintext itself.

The independent quotient theorem establishes a unique global function descriptor `(alpha,beta)∈F13^31×F2^25`. Its minimum modular coefficient support is

    f_beta(T)=|T|+|supp(beta)\G(T)|,  T=supp(alpha).

Hence every ≤3-term function has wt(beta)≤3: each active beta group needs a distinct nonzero coefficient, including groups already occupied by alpha. The converse wt(beta)≤3 alone is NOT sufficient.

**Container monotonicity.** Adding a feature to S increases |S| by1 and can remove at most one previously uncovered beta group. Therefore f_beta changes by0 or1. If T⊆S and f_beta(S)≤3, then f_beta(T)≤3. Thus allowing zero coefficients inside an affine support solve admits no invalid function. Conversely any admissible descriptor occurs in the container S=T. All affine points in every admitted container are valid, not just generic/nonzero points. This removes any need for nonzero-coordinate exclusions.

Enumerate every beta of weight0..3 whose H beta=b2. For each, enumerate admitted S, and retain every solution of A[:,S]alpha_S=b13, embedded with zeros outside S. This union is exactly the admissible global-function relation. Proof: soundness follows from the two field equations and monotone cost; completeness uses the true beta and S=supp(alpha). Distinct beta with identical crib syndromes cannot be merged into one law. Duplicate alpha spaces from nested containers are harmless but do not represent independent evidence.

## Precise pseudocode

```
build A13_all[91,31], H2_all[91,25] from full-Z26 ciphertext contexts
b13,b2 := CRT residues of (ciphertext-known_plaintext) at I
R := []                         # exact union-of-affine-pieces descriptor
cache := {}                     # keyed by tuple S; SAME instance b13
for B in every subset of25 groups of size at most3:
    if XOR(H2_I.column[g] for g in B) != b2_bitvector: continue
    parity_prediction[B] := XOR(H2_J.column[g] for g in B)
    for S in every subset of31 features with |S|+|B\G(S)|<=3:
        if S not in cache:
            cache[S] := exact_field_solve(A13_I[:,S],b13)
            # inconsistent OR particular a plus full nullspace basis N
            if consistent: cache[S].images := project_affine(a,N,A13_J[:,S])
        if cache[S] consistent:
            append (B,S,a,N) to R
            for j in J:
                U := cache[S].images[j] # singleton or F13
                mask[j] |= { CRT(u,parity_prediction[B][j]) : u in U }
if R empty: return COMPLETE_MODEL_REJECTION, not forced letters
otherwise:
    return COMPLETE, exact masks, R, and sparse supporting witnesses
```

Each scalar projection is a singleton iff its row annihilates N, else all13 residues. To witness a desired projected u, solve a scalar affine equation in nullspace coordinates; then embed alpha and lift using its ACTUAL support. For an active alpha group, allocate required beta parity to its first nonzero alpha coordinate; zero-alpha coordinates get parity0. If an entire group has alpha0 and beta1, set one representative coefficient to13. For singletons use prescribed beta. Lift with `CRT(a,e)=a+13*((e-a) mod2)`. This achieves exactly f_beta(supp(alpha))≤3. Arbitrary allocation to zero-alpha pair coordinates may inflate support and is forbidden.

R is a union, not a Cartesian product of coordinate masks. A full candidate plaintext requires ONE common R member and common nullspace parameter vector satisfying all its coordinates. Marginal witnesses may differ across positions. Check replay using the declared model, without claiming coverage of positions0..5.

**Uniqueness:** a positive-dimensional nonempty affine piece contains at least13 distinct alpha descriptors and therefore globally distinct functions. If every feasible piece is zero-dimensional, compare complete embedded `(alpha,beta)` descriptors: one distinct descriptor means globally unique function. Repeated singleton pieces do not destroy uniqueness. More than one descriptor can nevertheless produce one identical full91-position message prediction; label instance-only uniqueness separately. Empty R is neither unique nor vacuously certain.

## Exact combinatorics and complexity

Let w=wt(beta) and r be the number of active lag/square groups. The exact generating polynomial counting containers by cost is

    (2z)^(w-r) (3z+z²)^r (1+z)^(31-w-r).

For active singleton groups, empty or chosen both cost1. For active pairs, empty/first/second cost1 and both cost2. Inactive features cost1 each. Summing coefficients through degree3 gives:

| w | r | admitted containers |
|---|---|---|
|0|0|4992|
|1|0 / 1|932 / 1338|
|2|0 / 1 / 2|120 / 176 / 258|
|3|0 / 1 / 2 / 3|8 / 12 / 18 / 27|

There are2626 beta candidates. Across ALL beta, the exact unfiltered incidence count is100,916 (checked by direct enumeration), not2626×4992. This is a safe upper bound before parity filtering, not an attainable same-syndrome claim. The constant parity column is never zero on nonempty observations. In the actual realizable all-zero-context design, constant plus three indicator columns are1, other21 columns0: b2=0 admits1694 beta candidates. See validation.json for the corresponding container count. Repeated contexts can leave many beta and mod13 affine pieces feasible. Therefore caching ≤4992 field solves does not prevent substantial relation/projection overhead.

Let m=24, t=67, s=3; P=2626; M=#matching beta; U=#distinct requested supports≤4992; E=sum over matching beta of N_beta≤100916; F≤E=#consistent relation pieces. Packed parity filtering costs O(P*s*ceil(m/wordbits)); direct bounded-cost container generation costs O(E*s), versus an avoidable naive O(M*4992*s) filter. Mod13 solves cost O(U*m*s²), affine projection cache O(U*t*s²), binary predictions O(M*s*ceil(t/wordbits)), and straightforward mask union O(F*t*13), or O(F*t) with precomputed CRT masks. Stored relation costs O(F*s²), cached algebra O(U*s²), cached projections O(U*t), plus inputs. These are finite-operation bounds, not CPU predictions.

Can avoid repeated projection arithmetic by grouping feasible beta per S and OR-ing packed parity outcome bitsets; exact relation still must retain S↔B associations. Lazy R generation can reduce memory, but complete global uniqueness needs enough traversal to prove no omitted descriptors. Any cap hit means INCOMPLETE; partial absence is not rejection or uniqueness.

Common-support CRT oracle considers4992 supports, solving both fields and projecting on each feasible support. It may exploit binary affine subspaces much more efficiently on degenerate traces, while this method explicitly lists sparse beta. Both return the identical ≤3 modular function family. Quotient-first can replace many paired-field solves with a cheap parity filter and fewer mod13 solves in favorable cases; beta0 and degeneracy undermine this. The v1 weighted-atom join enumerates partial modular assignments and matches crib signatures; quotient-first never enumerates 13-valued alpha assignments and removes global pair aliases before search. Neither structural observation proves faster CPU. The strong oracle baseline must remain in comparisons, not only plain join expansion.

## Traps and explicit counterexamples

- `alpha=(1,1)` in one lag/square pair, beta0 has cost2, not0 or1. Parity cancellation does not delete nonzero mod13 support.
- `alpha=0`, beta1 in that pair has cost1, represented by13 on either feature. Ignoring nonunits loses it.
- `theta=(13,13)` on a pair is globally zero, so coefficient-vector multiplicity does not imply function ambiguity.
- With contexts all zero at the cribs, beta on lag1 and beta on lag2 have identical zero syndromes, but differ on a context with x1 odd and x2 even. Keeping only one loses genuine functions.
- For x1=0,x2=13, equality modulo13 holds but full-Z26 equality does not. Field-local indicators change the model.
- Using support containers as EXACT nonzero support unnecessarily fragments affine spaces; allowing zeros is sound only because the proved cost is monotone.
- Inconsistent mod13 or binary equations give no relation, regardless of language plausibility.
- Same law on one observed trajectory does not imply same global function; independent bases certify only global descriptor comparison.
- Cache keys must include instance identity/observations if reused across messages. A support alone is a sufficient key only within one fixed b13/A instance.

## Safe dense certificate option

Solve the entire dense descriptor family (no support bound) in both fields. It contains the sparse relation. If every unknown-coordinate dense projection is singleton AND one valid sparse witness exists, the sparse family is nonempty and all those predictions are forced. This safely concludes complete marginal plaintext output early. It does NOT conclude unique law or enumerate the full sparse relation. Without a sparse witness, dense consistency cannot distinguish sparse rejection from sparse feasibility. Timed comparisons must have identical output obligations; do not compare early marginal-only completion against a baseline required to materialize R or determine law uniqueness. For individual dense-forced coordinates the same argument applies, but the remaining coordinates still require sparse work.

## Fresh bounded validation, not a blind benchmark

verify.py independently enumerates all4992 support containers and2626 beta subsets to check counts. A separate tiny dictionary `(x,x²,[x=y])` over Z26 exhausts17576 coefficient vectors, yielding8788 canonical descriptors. For budgets0..3 it compares the direct minimum-support descriptor set to all allowed container descriptors, then compares entire relation partitions by observation syndromes for three fixed fresh context sets. This tests zero alpha, pair aliases, full-equality indicator, nonunits, distinct same-syndrome beta, and container duplication. It is not a full31-feature inference prototype, not a randomized performance benchmark, and not evidence about K4. Algebra above supplies the general proof.

## Prior art: bounded primary-source pass

- Cheraghchi and Ribeiro, [Simple Codes and Sparse Recovery with Fast Decoding](https://arxiv.org/abs/1901.02852), explicitly connects syndrome decoding and exact sparse recovery over fields, with specially constructed measurement codes. Our fixed ciphertext evaluation matrices do not inherit their guarantees. Enumerating low-weight parity syndromes is established decoding machinery.
- Cheraghchi, [Coding-Theoretic Methods for Sparse Recovery](https://arxiv.org/abs/1110.0279), surveys coding/sparse-learning connections and list-decoding structure. Maintaining every compatible sparse solution is not a new general paradigm.
- Specker, Hungerbühler, Wasem, [The Ring of Polyfunctions over Z/nZ](https://arxiv.org/html/2106.11788), treats polynomial functions modulo global null polynomials, including multivariate settings. Our quotient calculation specializes standard finite-function algebra; the full-equality indicators need the separate independence proof.

Sources inspected2026-10-31; focused web search included CRT sparse support and low-weight syndrome enumeration. No directly identical31-feature support-cost/parity-first combination identified in this small pass. This does not establish absence or global novelty. Honest label: **model-specific algorithmic combination and implementation proposal**, not an invented general cryptanalytic theory.

## v2 prototype and independently held-out benchmark plan

1. Keep v1 immutable through its existing audit. Implement v2 in a distinct directory/branch, with no imported hidden fixtures or seed and no threshold tuning against v1 blind results. Known aggregate v1 timing may motivate engineering, not select holdout examples.
2. Implement ordinary exact Gaussian oracle independently from parity-first. Add tiny exhaustive tests, full31-feature synthetic developmental tests, indicator toggles, inconsistent systems, beta0, weight1/2/3 mixtures, repeated/zero contexts, positive-dimensional relations, global versus trace-only aliases, and witness-cost/replay checks. Compare full descriptor sets on small dictionaries and exact marginal masks on31 features.
3. Freeze feature order, budgets, output contract, resource caps, implementation hashes, generator, success criteria and analysis BEFORE a different custodian draws fresh holdout randomness. Do not reuse frozen v1 holdout for improvement claims. Include both diverse and degenerate traces without filtering by identifiability or winning runtime.
4. Compare (a) common-support CRT oracle, (b) frozen compressed join, (c) parity-first, optionally(d) identical dense-certificate acceleration enabled for EVERY applicable solver. Separate marginal-only from full-relation/law-identifiability workloads. Randomize/interleave run order and account preprocessing consistently. Fresh validation must precede a speed claim.
5. Record exact agreement, false forced predictions on in-family cases, mismatch/misspecification behavior, U/M/E/F, nullspace dimensions, coefficient/function/message uniqueness separately, full replay witnesses, CPU/wall/RSS, timeout/incompleteness. Report paired distributions and stratified degeneracy, not cherry-picked weight3 cases. Publish negative speed results if oracle remains faster.
6. Independent auditor reconstructs witnesses and exact masks, verifies frozen artifacts and data separation, then considers any next target-admission decision. This plan authorizes no K4 run, remote mutation, separate repo or full blind evaluation under this design.

## Further exact simplification: maximal containers only

The down-set proof yields a stronger OPTIONAL v2 variant. Retain only containers of exactly3 original features that cover every active beta group:

    |S|=3 and B⊆G(S).

**Proof.** Start from any admissible T. For each active group missing from G(T), add one representative. These additions increase cardinality and decrease uncovered-group count equally, so the resulting set U has |U|=f_beta(T)≤3 and covers B. Pad U with arbitrary unused features to size3; there are31 available, and coverage cannot be lost. The resulting S is admitted, and every alpha supported in T is in the affine solution space on S by setting new entries to0. Conversely every alpha on such an S has cost≤f_beta(S)=3 by monotonicity. Thus these maximal containers give exactly the SAME relation, not an approximation. Every admitted nonmaximal container is subsumed. This also works for budgets s≤31, using |S|=s and covering B.

Counts for size3 covering containers: beta weight0:4495; weight1 singleton/pair:435/841; weight2 with0/1/2 active pairs:29/57/112; weight3 with0/1/2/3 active pairs:1/2/4/8. For weight2, count the third feature outside the chosen two groups plus cases using both features of one active pair. Duplicate size3 sets must be removed if generated through multiple representatives. Direct set enumeration is a simple independent check.

This is a stricter optional future-v2 reduction than the original all-container algorithm. It also applies to the ordinary common-support oracle: all ≤3 supports can be covered by exactly3 supports with zero coefficients, so a fair optimized baseline may use4495 rather than4992 supports. Do not attribute that generic support-padding improvement solely to quotienting. Maximal parity-compatible containers retain the stronger asymmetric group-cover filter.

The all-zero-context b13=0 example makes EVERY admitted support solve feasible (alpha0 is a solution), so the reported all-container76,972 incidences are not merely a prefilter artifact: they all correspond to nonempty relation pieces. Maximal reduction lowers duplicates but cannot remove genuine discrete beta ambiguity. A dense singleton-projection certificate can shortcut marginal-only output here, not full law enumeration.

Direct maximal-container enumeration passed:35,264 unfiltered beta-container incidences total;29,032 on the realizable all-zero-context b=0 instance. Fresh tiny check additionally verified every direct sparse descriptor extends to an exact-budget covering container for budgets0..3. Across the three context sets and four budgets,10,610 nonempty syndrome relations matched. No wall-time comparison was performed.
