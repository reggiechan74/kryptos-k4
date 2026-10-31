# Independent audit: hardened filtered-affine module

2026-10-31. **PASS for the documented, bounded generic prime-field development API.** No supported-input correctness blocker found at the exact pins below. This is not production deployment approval, canonical-predicate compiler validation, K4 admission, holdout authorization, or a speed claim.

The original proof/toy and hardened producer sources were not edited. Work used fresh generic affine instances, source inspection, and an independent certificate verifier; no target data, holdouts, or remote writes were involved.

## Exact reviewed SHA-256 pins

| File under `../filtered-affine-hardened/` | SHA-256 |
|---|---|
| `affine_filter.py` | `1e19e9ad872d517487cfe7968a9f4b906756007d5e710be216807620f078c90d` |
| `README.md` | `eccced031bda3698e84805231a8cf487418b38b7ffdd596c6a71a6c0722b20c9` |
| `test_affine_filter.py` | `9bb39ff04f0c8e204bf4a292d32a797d17f04afa18e48028d7565d0ac32c48e5` |
| `validation.json` | `e0047f6289e90688cc75cd72bdc73fb77bcd5931f5f0ae5f2b0f63d11f886da5` |
| `validation-optimized.json` | `2551c082c8dde5576ba2cb053e914c6e105ff0dd01d822f0fc67a2cc961a8ecd` |

Source, README, and test hashes matched before and after the audit. Any implementation change requires a new reviewed pin; the instance fingerprint binds the declared VERSION rather than the source-file hash.

## Verification results

Both the normal and `python -O` independent runs passed identical non-timing checks:

- **10,931 valid API cases**: 9,889 small-union and 1,042 inclusion-exclusion.
- **95,713 witness checks**, including successful budget-sweep calls.
- **38,086 elimination-certificate replay attempts**, including expected-negative tamper cases. This counter is attempts, not a claim that malformed certificates passed.
- **46 malformed-input rejections**.
- **74 budget checks**, covering zero/low work, solve, subset and wall-time budgets; witness-stage exhaustion; count preflight; and a 256-forbidden-set request that must be rejected by preflight rather than enumerate.
- **8 deliberate result/certificate tamper rejections**: missing cuts, altered masks, omitted removed values, zero row scaling, missing IE subsets, altered IE counts, invalid pivot claims, and wrong instance identity.

Coverage includes every affine base over F2^3 with zero/one forbidden set and every scalar row (2,756 API calls); every affine base over F3^2 with zero/one/two forbidden sets and every scalar row (6,900 calls); every F2^2 base and forbidden pair via IE (936 calls); and 339 fresh seeded/boundary/zero-dimensional/no-scalar cases across q=2,3,5,13. The q=13 full parallel cover was checked through the actual IE route. Lower-field singleton-fiber cover examples also exercised IE witness generation.

Normal independent run: 8.11 CPU seconds, 28,800 KiB peak RSS. Optimized run: 8.33 CPU seconds, 32,804 KiB. Each had 90 CPU-second / 512 MiB outer process limits. These are resource receipts, not benchmarks.

The producer's normal and optimized test scripts were separately rerun: both reproduced 1,460 cases, 4,082 marginal witnesses, 23 malformed rejections, and eight budget checks. The producer's explicit translated ambient-dimension-four fixtures therefore also passed under both modes.

## Source and API findings

### Strict domain checks — PASS

Public `project_filtered_affine` validates a built-in integer prime q in [2,65521], built-in integer n in [0,64], exact Budget type, bounded finite budgets, list/tuple input containers, equation and scalar dimensions, canonical integer residues, and size limits. Booleans, floats, composites, noncanonical residues, invalid dimensions, generators/unsupported containers, and NaN/infinite time budgets are rejected. The former modulo-4 and truncated-scalar examples now raise ValueError. Internal `dot` additionally checks dimensions.

The audit applies to the public entry point. Low-level helpers assume validated internal inputs and are not separately advertised hardened input APIs. This remains a prime-field implementation, not a general prime-power field library.

### Linear algebra and completeness evidence — PASS

The independent audit does not use producer `solve`, `dot`, or membership helpers. It replays each claimed operation from the original equations, verifies reversibility, checks the actual final matrix, checks pivot/rank structure, and independently reconstructs a particular solution and complete kernel basis. This verifies equivalence of the entire affine solution space, not just existence of one satisfying point.

For small-union EXACT results, it requires every forbidden restriction to appear, recomputes the restriction from the original equations and base parameterization, replays its rank/consistency receipt, recomputes every scalar restriction, and reconstructs the complete removed-value list. Thus scalar completeness follows from the already-reviewed r<q theorem plus complete restriction classifications. Rank-one normal and offset identities are checked independently. A proper whole-base exclusion or inconsistent base is sufficient for EMPTY; further irrelevant cuts need not be recorded in those early exits.

For IE results, the audit requires exactly every subset once, reconstructs that subset's original equation system, replays its certificate, independently recomputes dimension and constant/full scalar contributions, sums signed counts, and checks totals and masks. A witness alone cannot pass these checks. Missing subsets or altered counts fail even when individual surviving witnesses remain valid.

Output evidence is sufficient for such independent verification, but the module does not export a standalone untrusted-result verifier. Our audit checker is a separate test artifact, not an authorized integration addition. A caller accepting externally stored or untrusted certificates should use an independently hardened verifier rather than trust the transcript or fingerprint alone.

### Failure and cap semantics — PASS, with documented limitations

Malformed requests raise ValueError. Explicit internal certificate failures remain CertificateError and are not hidden as exhaustion. Budget exhaustion returns INCOMPLETE with masks, witnesses and evidence all None, including when the main projection pass finished but required witness construction did not. EMPTY is supported by a base/containment proof or a complete exact zero IE count. EXACT includes every requested marginal witness and an additional feasibility witness, even for no-scalar calls.

All correctness checks use explicit exceptions and survive `-O`; both independent runs confirm this. No partial masks leak from the audited exhaustion paths.

Before each IE pass, the implementation checks cumulative remaining terms, solves, and at least max(1,kq)*2^r count work. It checks the exponent against the bounded term budget before constructing it. The main pass has k+1 scalar queries because of the feasibility probe. Additional elimination/restriction/verification work is charged during execution; preflight is a necessary lower bound, not a promise that the pass or its witnesses will finish.

A safe worst-case description for successful witness construction is: if W is the number of marginal witnesses plus the feasibility witness, at most W*n*q coordinate-trial IE passes, in addition to the main pass. Hence a crude upper bound is 2^r*(1+W*n*q) subset solves plus the initial base solve, with W <= k*q+1. Actual early choices can reduce this drastically. All passes debit the same cumulative budgets. The procedure is exponentially expensive in r and can be INCOMPLETE under reasonable caps.

`max_work` is a bound on charged units, not on every Python operation or exact field-operation count. For example, constructing standard basis vectors in the greedy loop is not individually charged. Wall-time checks are cooperative, not hard interrupts; validation/fingerprinting precede the timer; and memory is not hard-capped by this API. These limitations are compatible with the README's operational boundary. Callers needing hard resource guarantees must retain external process time/memory limits and treat worker death as incomplete/no result. This audit does not upgrade the meter to a hard CPU or memory guarantee.

### Sparse/canonical integration suitability — conditional only

The generic affine core is a suitable reviewed development component under its stated contract. It does not establish the actual residual model. Before integration, separate authorized work must:

1. Prove fixed-beta/support pieces equal the feasible alpha sets, rather than outer containers.
2. Compile each canonical residual predicate equivalently, respecting aliases, mixed-field coupling and exact historical family scope; count the resulting affine systems.
3. Verify original sparse representatives and minimum-support bounds, not just coefficient-container size.
4. Union masks across pieces with witness provenance and correct cache identities; do not combine independent scalar witnesses into an unsupported joint solution.
5. Bind beta, support semantics, canonical compiler and module versions/source pins to any cache or serialized result.
6. Validate compilation, sparse lifting, cross-piece behavior and budget-failure semantics against fresh bounded enumeration before any separate admission decision.

No canonical compilation was performed or authorized by this audit. No K4 target or holdout is admitted. The underlying mathematics remains a local application of classical affine-cover and arrangement-counting facts, not a new general covering theorem.

## Audit files and reproduction

Separate audit directory: `../filtered-affine-hardened-independent-review/`

- `audit.py`: direct finite-set oracle plus independent completeness-evidence verifier and negative tests.
- `result.json`: normal receipt.
- `result-optimized.json`: optimized-Python receipt.
- `REVIEW.md`: this review.

Reproduce without writing producer bytecode:

```sh
PYTHONDONTWRITEBYTECODE=1 python ../filtered-affine-hardened-independent-review/audit.py
PYTHONDONTWRITEBYTECODE=1 python -O ../filtered-affine-hardened-independent-review/audit.py
```

No denied or uncertain operation remains in this hardened-module audit. No producer fix was required or performed.
