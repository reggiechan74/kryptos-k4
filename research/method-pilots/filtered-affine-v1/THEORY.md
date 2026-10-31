> **Historical toy: unsafe as a reusable API.** Input guards are incomplete and assertions disappear under Python -O. Preserve for proof history only; use the separately audited hardened module for its documented generic scope.

# Exact scalar projections of affine spaces with forbidden affine subdomains

31 October 2026. **The proposed small-union theorem is correct.** This is proof work and a fresh general-purpose toy prototype, not target admission or an integrated cryptanalytic solver. No target feature matrices, responses, predictions, holdouts, frozen studies, or remote files were used or changed. The theorem works over every finite field; the supplied toy implementation deliberately supports prime fields only.

## 1. Exact theorem, including degenerate cases

Let V be a nonempty affine subspace of a finite-dimensional vector space over F_q. Let W_1,...,W_r be affine sets (empty sets may also be included), where r < q. Write F = V minus the union of the W_i. Duplicates are allowed. Let ell be a scalar linear functional on the ambient space; adding a fixed scalar to ell changes none of the conclusions.

**Feasibility.** F is empty if and only if some W_i contains V. If dim V = 0, V consists of one point, and this statement follows directly. If dim V = d >= 1 and no W_i contains V, each V intersect W_i is empty or an affine space of dimension at most d-1, so their union has at most r q^(d-1) < q^d points. In fact at least (q-r)q^(d-1) points survive.

**Constant projection.** If ell is constant with value c on V and F is nonempty, ell(F) = {c}. If F is empty, its image is empty: no value is vacuously certified.

**Nonconstant projection.** If ell is nonconstant on V and F is nonempty, define V_t = {x in V : ell(x)=t}. Every t in F_q has a nonempty affine fiber of dimension d-1. Then

    ell(F) = F_q minus {t : V_t is contained in some W_i}.

Proof: if a forbidden set contains V_t, t cannot survive. Otherwise apply the feasibility argument to V_t. When d=1, the fiber is one point and every proper intersection is empty; no negative-dimension cardinality expression is used. When d>=2, fewer than q proper affine intersections cannot cover the fiber. This proves the reverse inclusion.

Each proper V intersect W_i contains at most one complete scalar fiber: two distinct parallel fibers have affine hull V. Thus at most r values are removed. The bound is sharp: removing r distinct parallel fibers removes exactly r values. The condition r < q is a sufficient condition based on the number of sets, not a necessary condition for any particular input. Empty/redundant sets may first be eliminated with proofs; the guard then applies to the actual retained union.

## 2. Matrix form and the exact rank-one test

Parameterize V = a + N z, where N has full column rank d, z ranges over F_q^d, and a,N describe the **entire** solution space. Write W_i = {x : B_i x = b_i}. Restrict its equations:

    D_i z = e_i,   D_i = B_i N,   e_i = b_i - B_i a.
    ell(a + N z) = c + h z,   c = ell(a),   h = ell N.

First classify each restricted system using exact field elimination:

- Inconsistent: the forbidden intersection is empty; ignore it.
- Consistent and rank D_i = 0: it contains all V; return EMPTY.
- Consistent and rank D_i >= 1: it is proper.

For h != 0, a proper forbidden intersection contains a full scalar fiber **if and only if** rank D_i = 1 and row(D_i) = span(h). In that case it is exactly that fiber. To obtain its removed value, take any solution z_i and return t_i = c + h z_i. It is independent of the chosen solution.

Proof: the fiber direction is ker h, of codimension one. Containment requires ker h subset ker D_i. Since D_i is nonzero, this forces rank D_i = 1 and its row space to equal span(h). Conversely these conditions, together with consistency, make the forbidden set a translate of ker h, hence precisely one fiber. Rank at least two cannot contain a whole fiber. A rank-one system with a different row direction cuts fibers but removes no whole one. This is a statement about the restricted D_i, not the rank of the original ambient B_i.

An explicit certificate for removed t_i is D_i = u h and e_i = u(t_i-c), for a nonzero column u. Verification requires only multiplication. Another valid certificate is a particular solution plus a full kernel basis with rank checks. Rank must not be guessed from a numerically fitted matrix.

Unfiltered singleton-or-full projection is therefore wrong after exclusions: V=F_3^2, W={x=0}, ell(x,y)=x gives image {1,2}, not F_3. Removing a point from that plane, however, leaves all three x values. Removing the point from a one-dimensional V removes its one corresponding projected value.

## 3. Constructive witnesses without enumerating all field points

For an allowed t, solve the fiber equations to obtain V_t = a_t + N_t z with free dimension e. The small-union theorem ensures no W_i contains this fiber. If e=0, return its point after direct checking. Otherwise fix the free coordinates of z one at a time.

At each step, the current slice S is not contained in any W_i. Its q child slices, obtained by assigning the next free coordinate u, are nonempty parallel affine subspaces. A particular W_i can contain at most one child: containing two would make it contain their affine hull S, contrary to the invariant. Therefore at most r values u are forbidden. Since r<q, choose a remaining u and retain that child. The invariant is preserved. After e steps, the slice is one point outside every W_i.

Containment can be tested directly: for S=p+Kz, B_i p=b_i and B_i K=0. This avoids full repeated Gaussian solves. Always verify the final point against original base equations, the requested projected value, and every original forbidden set. The toy prototype performs these checks, as well as checking the at-most-r bad-value invariant. It does not claim that different marginal witnesses can be combined into a single joint vector.

## 4. Failure at r >= q and exact fallback

Two distinct failures already occur at r=q:

1. In V=F_q^2, the q lines x=t cover all V. None contains V, yet F is empty. The feasibility shortcut fails.
2. In V=F_q^2 with ell(x,y)=x, the q forbidden singleton points (0,t), t in F_q, cover the whole fiber x=0. No individual forbidden set contains that fiber. The actual image is F_q minus {0}, whereas the individual-fiber-containment shortcut would incorrectly return the full field. Codimension-two cuts CAN collectively erase a fiber once the cardinality guard fails.

The supplied small-union API rejects r>=q even when a particular instance happens to remain easy.

**Reference inclusion–exclusion.** For every subset T of {1,...,r}, solve V_T = V intersect all W_i for i in T. Empty intersections contribute zero; otherwise let its dimension be d_T. Then

    |F| = sum_T (-1)^|T| q^d_T.

For each scalar value u, its count is the analogous sum of |V_T intersect {ell=u}|. If ell is nonconstant on V_T, every u contributes q^(d_T-1). If ell is constant at c_T, only u=c_T contributes q^d_T. The resulting nonnegative integer vector is exact for arbitrary r. A value survives precisely when its count is positive. Greedy witness construction is possible by selecting a next-coordinate slice whose remaining inclusion–exclusion count is positive.

This is exponential in r, not a claimed polynomial general solution. Deduplicating intersections via an intersection semilattice/Möbius coefficients is a classical compression, not a novelty claim. Alternatively enumerate the q^d free-parameter points under an explicit resource bound and check all exclusions. Any cap hit returns INCOMPLETE, never rejection or a certified full image. The q=13 boundary examples in the toy suite use bounded enumeration rather than 8192-subset inclusion–exclusion.

## 5. Certificates, costs, and generic integration contract

A proof-carrying result should retain:

1. Field specification and base affine equations; verified a,N spanning exactly their solution space (particular solution, full nullspace rank, and elimination/rank receipt).
2. Exact forbidden equations plus canonical predicate identity; optionally proofs for redundant-set removal. Record the retained r<q guard explicitly.
3. Reduced D_i,e_i and inconsistency/full-containment/rank classifications, verifiable from elimination identities or recomputation. Full-containment certificates prove EMPTY immediately.
4. For each scalar coordinate, c,h and the complete removed-value list with rank-one identities. The general theorem proves no other values are lost. For every retained value requested by the output contract, a final checked witness.
5. Status EMPTY, EXACT, or INCOMPLETE; never reuse a partial cache without the full instance, beta, forbidden predicates and scalar-row identities in its key.

Let n be ambient dimension, d the dimension of V, M the total number of forbidden equation rows, r the number of forbidden systems, and k the number of scalar projections. After obtaining V, forming reduced forbidden matrices costs O(M n d), and eliminating them costs O(M d^2) field operations. Cache their consistency, rank and rank-one normals. A straightforward scalar pass costs O(n d + r d) to compute h,c and compare cached rank-one directions; materializing a q-bit mask costs O(q), giving O(k(n d+r d+q)) after preprocessing. These are conservative arithmetic-operation bounds, not measured runtime comparisons.

A straightforward greedy witness, after parameterizing one requested fiber and restricting equations to it, costs O(q M d^2 + n d), plus setup. Tail coefficient tests can be cached to reduce this; no improvement claim is necessary. Inclusion–exclusion requires at most 2^r affine solves on at most M plus base rows and d free coordinates, followed by q-entry exact integer-count accumulation. Point enumeration costs O(q^d M d), after reducing constraints. Integer count storage needs O(d log q + r) bits for intermediate signed sums. The tiny prototype is for correctness, not these optimized bounds.

**Proposed generic interface:** `project_filtered_affine(field, base_equations, canonical_forbidden_systems, scalar_rows, witness_policy, resource_cap)`. It returns exact masks and certified witnesses or INCOMPLETE. It must reject non-field arithmetic and unknown predicate types. The theorem applies to prime powers; representing F_4 as integers modulo 4 would be invalid. `verify.py` only uses primes 2,3,5,13 and is not a general finite-field library.

## 6. Why it addresses the sparse-law admission gap, without authorizing a target

For a fixed canonical binary descriptor beta and a support container, the possible alpha descriptors form an affine F_13 space. Previously tested global-function subdomains can sometimes be represented as a small union of affine equation systems in alpha after beta is fixed. The theorem then gives exact filtered scalar marginals and valid witnesses without enumerating all 13^d coefficient assignments.

Examples of predicate compilation, not selection of an actual target residual:

- Requiring an essential equality indicator means NOT(alpha_E=0 AND beta_E=0). If beta_E is already nonzero, there is no exclusion; otherwise alpha_E=0 is one forbidden linear subspace.
- Excluding global affine functions uses canonical square/product/indicator zero conditions, with beta's nonlinear coordinates checked first. Raw feature presence is wrong because the known lag/square parity aliases can make a formal square globally linear.
- A fixed-beta constant-plus-one-indicator family with arbitrary remaining indicator coefficient is an affine/linear subspace described by zeroing the other canonical coordinates. Unit-indicator or adjacent-value restrictions generally require specific alpha values and compatible beta values; finite choices may yield several affine sets. It is not sound to label a narrower previously tried unit family as the whole arbitrary-coefficient family without stating the deliberate conservative exclusion.
- Intersect all such forbidden systems with the current support piece; empty, whole-piece and redundant cases must be recognized before projecting.

General Boolean filters require an explicit equivalence-preserving decomposition. The number of sets after decomposition, not the number of informal predicates, is r. Mixed-field conditions must be compiled after beta is fixed, or represented with their true coupling. No independent field-filter factorization may be assumed. An original sparse representative must still be lifted from the actual canonical descriptor and checked against the verified minimum-support formula, not merely against container size. Multiple pieces require unioning masks and preserving which piece/beta supplied each witness. This theorem proves projection mechanics only: it does not settle prior-art scope, model membership, full-message or law uniqueness, benchmark advantage, or target admission.

## 7. Fresh validation and next minimal implementation steps

`verify.py` is self-authored, uses only Python's standard library and fresh synthetic affine equations. It compares three routes: direct pointwise satisfaction enumeration, inclusion–exclusion counts from elimination, and the guarded rank-one projection rule. Direct enumeration does not use the elimination code. It also verifies every constructed witness in the original equations.

Recorded PASS in `validation.json`:

- 1,200 random cases: 300 each over F_2,F_3,F_5,F_13; ambient dimensions 0 through 3; arbitrary/inconsistent/empty equation systems; zero and nonzero projection rows; forbidden counts below and at the bound.
- Exhaustive F_3^2 check: all 23 distinct affine subsets including the empty set, every unordered pair with repetition, all 9 scalar linear rows: 2,484 cases. This includes full-space forbidden sets, identical sets, points, crossing/parallel lines and zero scalar maps.
- Six additional inclusion–exclusion boundary cases at q=2,3,5, and two separately enumerated q=13 boundary cases.
- 3,690 total brute-count/inclusion–exclusion comparisons; 7,375 verified returned witnesses, including four sharp r=q-1 examples.
- CPU 0.772218824 seconds; peak RSS 8,704 KiB. Caps: 90 CPU seconds, 512 MiB address space. These figures are a resource receipt, not a performance benchmark. An initial attempt to use `/usr/bin/time` found it unavailable; the successful run measures CPU and RSS with Python resource/time and enforces limits in-process.

Further implementation admission requires: explicit tests for translated bases and nontrivial embeddings, independently audited field/rank certificates, prime-power field support if desired, the actual canonical-predicate compiler and sparse witness lift, adversarial r>=q fallback/cap status, cross-piece mask union, and cache-key invalidation. Fresh toy validation is not sufficient to authorize target use. Do not modify a frozen solver or benchmark under this proof note; integrate into a distinct development version and compare against exact finite enumeration on small models first.

## 8. Primary-literature comparison and novelty limits

Focused web pass, 31 October 2026; no exhaustive novelty claim.

- Robert E. Jamison, *Covering finite fields with cosets of subspaces* (1977), [publisher record](https://doi.org/10.1016/0097-3165(77)90001-2). Its abstract studies minimal coset covers of nonzero vector-space points via polynomial methods. It establishes the longstanding covering-problem lineage; our all-points elementary bound should not be confused with that different omitted-origin question.
- Mohsen Aliabadi, *Extremal Subspace Covers in Finite Vector Spaces*, [arXiv v2, Theorem 4.1 and Corollary 4.2](https://arxiv.org/html/2610.07051v2). Explicitly states the affine union bound m q^(n-1), its parallel-hyperplane equality case, and the q-set affine covering number. This directly matches our elementary counting foundation. The scalar projection result here applies that fact to fibers; it is not evidence of a newly discovered covering theorem.
- Anders Björner and Torsten Ekedahl, *Subspace Arrangements over Finite Fields: Cohomological and Enumerative Aspects*, [primary preprint](https://arxiv.org/pdf/math/9612217), Proposition 3.2; [published record](https://www.sciencedirect.com/science/article/pii/S0001870897916479). The characteristic polynomial of a finite-field affine arrangement counts points outside its union. Our inclusion–exclusion reference is the uncompressed elementary arrangement-complement count, applied fiber by fiber. This is established machinery.
- Anurag Bishnoi, Pete L. Clark, Aditya Potukuchi and John R. Schmitt, *On Zeros of a Polynomial in a Finite Grid*, [primary paper](https://cage.ugent.be/geometry/Files/421/AlonFuredi.pdf), especially its finite-geometry and grid-code discussion. It develops stronger polynomial/grid nonvanishing and cover bounds. No such stronger theorem is needed here, and its coding discussion does not establish speed or cryptanalytic success for this application.

Honest contribution: an exact, guarded, certificate-friendly **local use of classical affine-cover facts to enforce canonical no-repeat filters in a sparse-law decoder**. The focused search did not establish whether this exact interface has appeared before. No claim of a new mathematical theory, globally original algorithm, or solved cipher follows.
