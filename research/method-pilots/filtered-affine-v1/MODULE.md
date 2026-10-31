> **Historical producer documentation.** The pending-audit wording below records its original stage; the separately preserved independent review subsequently passed at the exact source pin. This is a sanitized public prose copy, not byte-identical to the original.

# Hardened affine-minus-union module — development version 1

This separate implementation follows the independently reviewed finite-field proof. It does not modify that historical toy or any frozen cryptanalytic study. No target data, canonical K4 predicate compiler, old holdout, or remote write is involved. Independent implementation audit remains pending.

## API

```python
from affine_filter import project_filtered_affine, Budget
result = project_filtered_affine(
    q=3, n=2,
    base=[],                      # Each equation: n coefficients then rhs.
    forbidden=[[[1, 0, 0]]],      # Exclude x = 0.
    scalars=[[1, 0], [0, 1]],
    budget=Budget(max_work=20_000_000, max_solves=200_000,
                  max_terms=65536, max_seconds=10.0),
)
# result['status'] == 'EXACT'
# result['masks'] == [[1, 2], [0, 1, 2]]
```

Strictly accepts built-in integer prime q in [2,65521], integer n in [0,64], list/tuple systems, at most 256 input equations total, 256 forbidden systems, and 256 requested scalar rows. Every coefficient/right-hand side must be a built-in integer in [0,q). Booleans, floats, negative residues, oversized residues, composite moduli, noncanonical lengths and unsupported containers raise `ValueError`. Prime powers represented as integers modulo q are NOT supported. Empty equation systems mean the entire ambient space; a zero-dimensional space has one empty vector; `[1]` is an inconsistent zero-dimensional equation.

Status contracts:

- **EXACT:** all requested marginal masks and one checked witness per retained value, plus a feasibility witness even if no scalars were requested.
- **EMPTY:** the relation is proved empty; every requested mask is empty, not vacuously forced.
- **INCOMPLETE:** a valid request exhausted a work, solve, subset or cooperative wall-time budget. Masks, witnesses and evidence are `None`; no partial result may be interpreted as exact or as rejection.
- Malformed input raises `ValueError`. Internal certificate failures raise `CertificateError`, not a misleading budget status.

Witness keys are integers in the in-memory API; normal JSON serialization converts mapping keys to strings. A vector assembled from different scalar witnesses is not necessarily feasible.

## Computation and checks

If the original number r of forbidden systems is less than q, the implementation uses the rank-one filtered projection theorem and greedy slice witnesses. It does not deduplicate to sneak past the guard. Every base and restricted Gaussian solve replays its sequence of reversible row operations, verifies pivot/rank certificates, checks particular/nullspace equations in the original system and checks free-coordinate independence. All checks use explicit exceptions and remain active under `python -O`. Removed scalar values also receive checked rank-one normal/offset identities. Witnesses are checked against all original equations/exclusions and the scalar row.

For r >= q it uses exact inclusion–exclusion. The main enumeration stores subset elimination certificates, dimensions/constant-or-full projections, exact counts and total count. A main pass requires 2^r affine solves in addition to the initial base solve and O(k q 2^r) accumulation for k scalar queries. One extra zero scalar is queried to retain a feasibility witness. Each requested witness is built by fixing ambient coordinates and rerunning exact positive-count tests. Thus the complete witness obligation can be much more expensive than the main projection pass; it is intentionally budgeted rather than hidden.

Before **every** inclusion–exclusion pass, the module checks remaining capacity for all 2^r terms/solves and at least max(1,kq)2^r count work. The check avoids constructing a giant exponent before verifying its bit-length bound. Actual elimination, restriction, accumulation and verification work is additionally charged during execution. Subset/solve budgets are cumulative across the main pass and all witness construction. A sufficient main-pass budget does not guarantee that witness construction will finish; failure then returns INCOMPLETE without publishing partial masks. Counts use Python exact integers.

`max_work` counts conservative charged computational units, not CPU cycles or an exact field-operation complexity. Wall-time checks are cooperative at charged operations, not hard real-time interrupts. External process termination cannot return an API status and must be handled by a caller. The module imposes finite input limits but does not claim a hard OS memory cap; an embedding application should retain an outer process memory/time limit. The test driver uses 90 CPU seconds and 512 MiB address space. No cache is implemented. The instance SHA-256 includes module version, field, dimension, base, all ordered exclusions and requested scalar rows; callers must additionally bind any future canonical-beta/support interpretation.

## Fresh tests

Run from this directory:

```sh
python3 test_affine_filter.py
python3 -O test_affine_filter.py
```

Both recorded PASS:

- 1,460 valid-input cases; 4,082 returned marginal witnesses checked by independent direct point enumeration.
- 405 small-union and 1,055 inclusion–exclusion cases.
- 480 fresh seeded cases across primes 2,3,5,13 and dimensions 0..3.
- All affine subsets of F2^2 as bases and forbidden pairs, all four scalar maps.
- Explicit translated embedded planes, restricted-rank defects, duplicates, empty/full exclusions, inconsistent systems, zero-dimensional inputs and no-scalar requests.
- 23 malformed-input rejections and eight budget checks, including q2^r counting preflight and witness-stage exhaustion after the main IE pass finishes.
- Normal receipt: 1.5710 CPU seconds, 12,416 KiB peak RSS. Optimized-Python receipt: 1.4311 CPU seconds, 17,588 KiB peak RSS. These are resource receipts, not speed comparisons.

Files: `affine_filter.py`, `test_affine_filter.py`, `validation.json`, `validation-optimized.json`.

## Remaining boundaries

This is usable generic development code, not a field-general library or a vetted cryptanalytic integration. Independent audit is required. Future canonical predicate compilation must prove equivalence after fixing beta and preserve the actual sparse witness lift. Cross-piece union, target-family admission, prior-scope resolution and any fresh holdout are outside this implementation. No global novelty or performance claim is made.
