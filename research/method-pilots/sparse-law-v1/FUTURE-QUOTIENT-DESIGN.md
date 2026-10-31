> **Future design / toy mathematical checks only.** No v2 performance, fresh holdout or K4 result is established here. Public prose sanitization is mapped in PUBLIC-PROVENANCE.json.

# Exact global-function quotient and support cost: independent audit

2026-10-31. **Verdict: proposed theorem and asymmetric-support consequence are correct.** This is a separately verified elementary specialization of standard finite-function/CRT algebra, not a claim of globally novel mathematics or a speedup.  No K4 data, repository, v1 prototype, or holdout files were read or modified. This is a future-design note, not a frozen-protocol amendment.

## Model and distinction that matters

Domain X=(Z/26Z)^6. Feature order: 1; x_1,...,x_6; x_1²,...,x_6²; the 15 x_j x_k for j<k; E_1=[x_1=x_2], E_2=[x_3=x_4], E_3=[x_5=x_6]. Equality is **full equality modulo26**, not equality in just one CRT component. A coefficient vector theta in (Z26)^31 defines F_theta on *all* X. Coefficient support counts nonzero residues modulo26.

Write x_j=(u_j,v_j) under CRT, u_j in F13, v_j in F2. These coordinates are independently selectable. E_i=[u_a=u_b][v_a=v_b]. In particular, these indicators are not ordinary polynomial functions over Z26: an output polynomial reduced modulo13 cannot depend on parity, whereas E_i can. Thus polynomial canonicalization references cover the polynomial core, not automatically this entire augmented dictionary.

## Theorem 1: complete global kernel

The 31 reduced feature functions to F13 are independent. The reduced functions to F2 have exactly the six independent relations x_j²-x_j=0. Consequently the canonical global function descriptor is

    (alpha,beta) in F13^31 × F2^25,

where alpha=theta mod13; beta has the unpaired-feature parities and, for each lag/square pair, beta_j=theta_lag_j+theta_square_j mod2. Every descriptor is realizable. Two vectors induce the same function iff their descriptors coincide. The global coefficient kernel is exactly

    {13 sum_j epsilon_j (e_lag_j-e_square_j): epsilon_j in {0,1}}.

There are 64 coefficient vectors for each global function (before imposing sparsity), and 13^31 2^25 global functions. The quotient is an additive/module descriptor, not a claim that this degree-limited span is closed under multiplication.

### Proof of independence modulo13

Suppose Q(u)+sum lambda_i E_i=0 identically, where Q is a linear combination of the 28 listed polynomial monomials. Fix u_a=u_b for one equality pair. Keep all u and all other parity variables fixed, and change v_a alone so v_a=v_b in one context and v_a≠v_b in the other. Only that pair's indicator changes; the pairs are disjoint. Subtract the identities to obtain lambda_i=0. Repeat for each i. Hence Q vanishes on F13^6. Its degree in each variable is at most2<13. A polynomial with each variable degree less than the field size is zero if it vanishes on the entire field grid: induct on the number of variables, applying the univariate root bound to each slice. Thus all 28 coefficients vanish.

### Proof modulo2

First replace squares by linears, leaving 22 multilinear monomials (constant, six singletons, 15 pairs). Fix v_a=v_b for an equality pair. Keep all v and the other u fixed; vary u_a to toggle u_a=u_b. Only this indicator changes, so its coefficient is zero. Repeat. The remaining multilinear polynomial vanishes on F2^6; the same degree-bound argument (individual degree≤1<2) gives zero coefficients. Thus rank25 and only the stated six aliases.

### CRT conclusion

A globally zero vector must be zero coefficientwise modulo13, so write it 13 epsilon with epsilon binary. The modulo2 kernel just proved forces every unpaired epsilon to zero and the two epsilons in each lag/square pair to coincide. Conversely 13(x²−x)=0 modulo26 for every x. Since ±13 coincide modulo26, the signs in each generator are immaterial. CRT also realizes any alpha and any choice of coordinate parities; select parity sums to obtain any beta. This proves the claim completely, including constant/product/indicator non-aliasing.

## Theorem 2: exact minimum support, constructive lift

For one lag/square pair let t count its nonzero alpha entries and let e be its beta bit. Its minimum support is t if t>0 and e if t=0. For an unpaired feature its minimum is 1 precisely when its alpha or beta component is nonzero. Sum these costs across disjoint groups.

**Lower bound:** every nonzero alpha entry requires a nonzero mod26 coefficient. A group with zero alpha but beta=1 requires at least one nonzero coefficient. Independence of the descriptor prevents moving this cost to another group.

**Construction:** for t>0 set all zero-alpha entries in that pair to parity0 and allocate the required parity sum to an already-active entry (all other parities0). For t=0,e=0 use both zero; for t=0,e=1 put13 on either one entry. For an unpaired entry use its prescribed alpha and beta. For alpha representative a in {0,...,12} and chosen parity b, explicitly lift by

    CRT(a,b) = a + 13*((b-a) mod2), in {0,...,25}.

A nonzero a stays nonzero under either parity choice. Therefore construction attains the lower bound, proving exactness rather than merely preserving the full span. If deterministic tie-breaking is wanted, assign a free parity bit to the first active coordinate; when both alpha entries vanish assign13 to the lag.

### Equivalent support-set form and asymmetric search

Let S=supp(alpha) in the original31 coordinates and G(S) be its image in the25 groups that merge lag/square pairs. Then

    min_support(alpha,beta) = |S| + wt(beta restricted outside G(S)).

Hence a global function is representable with at most s terms iff this quantity≤s. All parity bits within G(S) are free at zero *additional* support cost; outside it at most s−|S| bits may be1. Zero alpha gives exactly wt(beta); two nonzero alpha entries in one pair cost2 even if their parity contributions cancel. For example alpha=(1,1), e=0 has cost2, not1 or0. Alpha=(0,0), e=1 has cost1; alpha=(0,0), e=0 has cost0 even though the redundant coefficient pair(13,13) also represents it with cost2.

Exact prospective inference strategy on a finite observation matrix: enumerate/represent all alpha solutions to the mod13 observations with |S|≤s; for each S solve the25-coordinate binary observation equations allowing unrestricted bits on G(S) and at most s−|S| ones outside. Lift resulting descriptors constructively. Preserve all alpha fibers and all qualifying beta solutions, not just independent fieldwise sparse minima. Full enumeration has at most sum_{k=0}^s binom(31,k)12^k alpha vectors prior to observation filtering; for s=3 this is7,834,693. Degenerate observations may leave many alpha solutions, so compressed representation remains important. No runtime superiority follows from the theorem.

## What this buys, and what it cannot buy

- Removes only *global* dictionary redundancy; labels genuine function identifiability separately from coefficient identifiability.
- Gives exact sparsity admission and a sparse representative after canonicalization. Naively counting nonzero canonical coordinates would be wrong.
- Allows deduplication by descriptor and more precise support/ambiguity reporting. It may reduce parity work from31 to25 coordinates without expanding the≤3 function class.
- Does not eliminate observation-specific aliases. Two different global descriptors can agree on every available context, including a complete synthetic97-position trace, and disagree on a new context. Crib-only equivalence is still coarser.
- Cannot certify model membership, force correctness outside the model, identify the intended law merely because a plaintext is unique, or justify touching K4. Does not improve the first-six-position coverage limit.
- The 64-element coefficient fiber is unrestricted: the number of its members meeting a particular sparsity budget varies. Do not divide sparse representation counts by64 to count functions.

## Fresh validation (not the proof)

`python ../k4-function-quotient-audit/verify.py` passed. Python standard library, independently written algebra only; no downloaded code. Generated1,000 six-tuples with seed20261031, and Gaussian elimination found ranks25 modulo2 and31 modulo13. `validation.json` contains selected context witnesses (25 and31 rows). Exhausted all676 pair lifts, covering338 canonical pair descriptors: every minimum support matched. Exhausted17,576 pair-plus-singleton lifts, covering8,788 descriptors: every grouped formula matched. Checked13(x²−x)=0 for all26 residues. Recorded process CPU0.104790358 seconds (not a benchmark or comparative performance result). No actual target or v1 artifacts involved.

## Prior-art/source assessment

Sources inspected2026-10-31; this is a focused comparison, not an exhaustive novelty search.

1. Specker, Hungerbühler, Wasem, *The Ring of Polyfunctions over Z/nZ*, [arXiv2106.11788v2](https://arxiv.org/html/2106.11788), especially introduction, null-polynomial decomposition, multivariate section. Studies polynomial functions as functions rather than formal expressions, unique null-polynomial representation, and multivariate counts. Direct prior foundation for quotienting polynomial coefficients by global functional aliases. Our small squarefree-modulus degree2 kernel is elementary relative to that theory; full-equality indicators require the separate toggling proof above.
2. Xiumei Li and Min Sha, *Polynomial functions in the residue class rings of Dedekind domains*, [arXiv1704.04965v6](https://arxiv.org/pdf/1704.04965), introduction and canonical-representation framework. Establishes more general canonical representations/counting formulas, extending earlier P-ordering work. Again, our calculation should not be sold as inventing canonicalization over finite rings.
3. Mahdi Cheraghchi and João Ribeiro, *Simple Codes and Sparse Recovery with Fast Decoding*, [primary journal article](https://epubs.siam.org/doi/full/10.1137/21M1465354), [author preprint](https://arxiv.org/abs/1901.02852). Connects exact sparse recovery and syndrome decoding and develops designed measurement/decoder constructions over fields. This supports the established sparse-recovery lineage, not a claim that its runtime guarantees apply to this fixed arbitrary feature matrix or composite-ring augmented dictionary.

The useful local contribution is a checked, model-specific **support-cost-preserving canonicalization and CRT lift rule**, ready for separately gated future design. It is not evidence of a new general mathematical theory, a new sparse-recovery algorithm with proved speedup, or an untried cryptanalytic attack. No directly identical31-feature treatment was located in this limited source pass; absence in that pass does not establish novelty.
