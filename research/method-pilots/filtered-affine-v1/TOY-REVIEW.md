# Independent filtered-affine projection audit

2026-10-31. **PASS for the stated mathematics and well-formed prime-field toy scope; NOT production-ready and NO K4 admission.** No proof error or supported-input discrepancy found. The original prototype remains unchanged. This audit used only the three requested producer artifacts, fresh affine toys, and public primary references. No target data, old holdouts, remote writes, or producer edits occurred.

## Results first

- Reproduced the producer receipt: 3,690 point-count/inclusion-exclusion comparisons and 7,375 verified witnesses; all non-timing fields match `validation.json`.
- Independent oracle: 85,203 cases, 94,984 returned witnesses checked against direct set membership, and 364 guard checks passed. CPU 16.38 s, peak RSS 12,032 KiB, with 60 CPU-second / 512 MiB limits.
- Exact affine-cover and arrangement-complement primary references were inspected and support the limited classical-math attribution.
- The prototype accepts unsupported composite moduli and malformed scalar dimensions in simple cases. These are explicit integration gates, not counterexamples to the prime-field theorem.

## Proof audit

1. **Feasibility for r < q:** Correct, including a point base, empty forbidden intersections, duplicates, and forbidden sets containing the base. Every proper nonempty intersection has at most q^(d-1) points; their union cannot cover a d-dimensional affine base. The d=0 case is correctly separated.
2. **Scalar projection:** Correct. A nonconstant scalar map has q affine fibers, each of dimension d-1. A fiber disappears exactly when one forbidden set contains it, because otherwise fewer than q proper affine intersections cannot cover it. Dimension-one bases have singleton fibers, as separately handled. Constant maps and empty complements are also handled correctly.
3. **Restricted rank-one criterion:** Correct. With nonzero h and a consistent proper restricted system Dz=e, full-fiber containment is equivalent to ker(h) being contained in ker(D), hence rank(D)=1 and row(D)=span(h). It is rank after restriction to the base, not ambient rank. The identity D=u h, e=u(t-c) certifies the removed fiber. Consistency cannot be omitted.
4. **Greedy witness:** Correct. The current slice must not be contained in any forbidden set. Two distinct child slices span their parent affinely, so each forbidden affine set contains at most one child. At most r<q choices are excluded; choosing another child preserves the invariant until a surviving point is reached. The supplied code checks the final witness against original equations. It does not establish joint compatibility of distinct marginal witnesses.
5. **r=q boundary examples:** Both are correct: q parallel lines cover the entire plane, and q singleton points can cover one scalar fiber although no singleton contains that fiber. These disprove the unguarded feasibility and individual-fiber-removal shortcuts respectively. Both small-union entry points reject r>=q, including independently checked q=13 cases.
6. **Arbitrary-r fallback:** Inclusion-exclusion is exact for all finite r, including duplicate, inconsistent, and whole-space forbidden systems. A nonconstant scalar map contributes q^(d_T-1) to each value; a constant map contributes q^d_T only to its constant. Positive exact counts characterize surviving values. A witness can be constructed by recursively selecting a child with positive exact remaining count. That inclusion-exclusion witness implementation is not provided in the prototype.

## Independent test coverage

`independent_validate.py` loads only the producer's function definitions via AST. It does not import the top-level experiment or reuse producer `dot`, `satisfies`, or `check` in the oracle. Affine subsets are generated through direct point-set intersections of hyperplanes; expected counts and witness membership are computed independently.

| Family | Coverage |
|---|---:|
| F2^3 | All 52 affine subsets, including empty; every base; zero or one forbidden set; all 8 scalar rows: 22,048 cases |
| F3^2 | All 23 affine subsets; every base; every zero/one/two forbidden-set multiset; all 9 scalar rows: 62,100 cases |
| Translated embedded bases | 875 cases over q=2,3,5,13; affine planes in ambient dimension four; constant/nonconstant scalar rows; ambient-rank versus restricted-rank distinctions |
| Arbitrary r inclusion-exclusion | 180 fresh seeded cases over q=2,3,5 with r=q,q+1,q+2, including duplicates and inconsistent systems |
| Boundary guard | Four additional q=13 image/witness calls rejected as required |

The translated planes use x2=x0+x1+1 and x3=2*x0+x1+1. All new tests are tiny finite-field tests, not benchmark observations or holdout data. Timing is only a resource receipt.

## Explicit unsupported-input examples

With function definitions loaded from the unchanged `verify.py`:

```python
image_small([], [], [1], 1, 4)       # returns {0,1,2,3}; composite modulus not rejected
image_small([], [], [1,99], 1, 3)    # returns {0,1,2}; scalar length mismatch not rejected
```

`dot` uses `zip`, which truncates mismatched vectors (line 7). Gaussian elimination assumes invertible nonzero coefficients (line 13), so modular arithmetic on a composite modulus can either return an unjustified result or fail incidentally. Final witness and count checks use Python assertions (lines 65, 68, 81); `python -O` removes them. Resource limits terminate the process rather than emit an INCOMPLETE result. These are acceptable limitations of a documented fixed-prime toy, but not of a reusable proof-carrying interface. Preserve this toy as historical evidence and implement a separately versioned hardened module.

## Required hardened integration contract

1. Validate field identity and arithmetic before computation: either an explicitly supported prime modulus or an audited finite-field implementation for prime powers. Integer arithmetic modulo 4 is not F4. Reject malformed dimensions, equation row lengths, scalar row lengths, invalid field elements, and unknown predicate types. Do not use truncating operations as dimension validation.
2. Prove the base parameterization spans exactly the feasible alpha slice for the fixed canonical beta and support piece. An outer support container is insufficient. If a minimum-support predicate still removes interior points, encode it exactly or split into exact feasible pieces before claiming exact projections; merely rejecting a subsequently lifted witness is not a proof of the mask.
3. Compile canonical predicates with equivalence proofs after fixing beta. Essential-indicator nonzeroness is a joint alpha/beta condition. Canonical affine-family exclusions must respect aliases; raw feature presence is not a substitute. Unit-indicator/adjacent-value prior families must not silently become arbitrary-coefficient families. Count the actual affine sets after Boolean decomposition and proved redundancy removal, not informal predicates.
4. Require retained r<q before the shortcut. Otherwise use an explicit bounded exact fallback, or return INCOMPLETE. Inclusion-exclusion has up to 2^r affine solves and O(q*2^r) count accumulation in this straightforward scheme. Cap work before enumerating subsets, retain exact integer counts, and make exhaustion/timeout/cancellation distinguishable from EMPTY. Process death alone is not a usable API status. No measured speed advantage is established.
5. Emit EXACT / EMPTY / INCOMPLETE with explicit proof receipts and non-optional verifier checks that do not disappear under `-O`. Verify original equations, every original exclusion, scalar value, canonical identity, and the original sparse representative's minimum-support condition. Test completeness and rank receipts independently.
6. Union masks across beta/support pieces while preserving each witness's source. Include all instance, field, base, beta, canonical-predicate, scalar-row, support, and relevant version identities in cache keys. Test stale-cache and partial-cache invalidation. A tuple assembled from scalar marginals or different beta pieces is not automatically feasible; joint output requires a joint solve and witness.
7. Before any integration admission, compare the hardened module and canonical compiler against exhaustive finite enumeration on fresh small models, with adversarial translated/embedded bases, r=q and r>q, failed-input guards, budget exhaustion, cross-piece unions, canonical aliases, and sparse lifts. This review authorizes no target or new holdout.

The proposed canonical-beta examples are algebraically plausible conditional compilation rules. These artifacts contain neither the actual canonical compiler nor its support-lift proof, so this audit does not validate those missing implementations or settle historical prior-family scope.

## Primary references and novelty

- [Aliabadi, Theorem 4.1 and Corollary 4.2](https://arxiv.org/html/2610.07051v2): inspected; directly states the affine union bound and q-set covering boundary.
- [Björner–Ekedahl, Proposition 3.2](https://arxiv.org/pdf/math/9612217): inspected; characteristic-polynomial evaluation counts the affine arrangement complement. This supports the classical inclusion-exclusion/Möbius lineage.
- [Bishnoi–Clark–Potukuchi–Schmitt](https://cage.ugent.be/geometry/Files/421/AlonFuredi.pdf): inspected; finite-grid nonvanishing, covering, and coding applications are present. No speed or cryptanalytic implication is supplied by that reference.
- Jamison DOI retrieval was attempted once at https://doi.org/10.1016/0097-3165(77)90001-2. It failed with a non-retryable 500 redirect to an inaccessible publisher endpoint. This citation was not independently verified in this audit; no bypass or retry was attempted. It is not needed for the proof verdict.

The correct contribution description is a local, guarded application of classical affine-cover facts to canonical residual projections. The sources and audit do not establish globally novel mathematics, an integrated cryptanalytic algorithm, benchmark superiority, uniqueness, or a cipher solution.

## Integrity and files

Producer hashes before and after review match:

- REPORT.md: `16e2b8a46691621f3e72a49465cdc38b23ef73e180d00e2cd5f2cafaeee388a8`
- verify.py: `290f59c38d6f31669c49dfbb31ec7d1ef97ef9b76cdac2d3f36e83ff8d84f78a`
- validation.json: `20c735232ef01be28cbaa07b3444f2a91746f3b0bf2af045df07e0274bdfbd27`

Audit files are separate under `../filtered-affine-projection-independent-review/`: `REVIEW.md`, `independent_validate.py`, and `result.json`.
