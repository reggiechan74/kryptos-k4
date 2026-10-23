# Sparse index ownership and reserved predicate cache

23 October 2026. CSP889-SPARSE-015 follows the measured REAL-014 bottlenecks. [Protocol](SIGABA-SPARSE-OWNERSHIP-SPEC.md) frozen at `37443df`; controlled implementation committed at `c63b9ab` before resource outcomes. This is a representation optimization, not a new cipher or K4 test.

## Exact relation preserved

For a fixed control start, each reachable static index function has exactly one deterministic magnet-mask trajectory. Every class is stored as an explicit owner ID in exactly one live branch. Updates compute its mask from the same complete ten-digit map and the continuous source-derived control digits. Branches merge only with equal cipher offsets AND equal compatible cipher-start domains. Classes with empty cipher domains are eliminated; no arbitrary per-time mask, reset, independent block key or new schedule is introduced. Raw index aliases remain unchanged.

Class ownership is stored sparsely rather than as a high-position bitset in every branch. Cipher-start domains remain dense bitsets in this batch. The cache reserves 48 MiB for zero-offset/translated values and 16 MiB for on-demand LRU coordinate masks, replacing the earlier fixed-mask saturation without increasing the 64-MiB total. The inherited `fixed_mask_bytes` metric records current on-demand mask occupancy here; explicit mask-cache fields record the new policy and peak. Mask/value eviction or disabling changes performance only.

Six q=2/3 empty/short/long tiny fixtures pass complete coupled-relation comparison under three cache policies and independent full raw-key stream comparison. All q=3 three-wheel offsets and symbol pairs match the original direct predicates under disabled, evicting and enabled caches. Contradictory observations return the exact empty set; deliberate budget exhaustion returns unknown, not zero. Published CSP-889 reference controls are retained and rerun by the aggregate suite.

## Unchanged real-sized resource comparison

Both original fixtures, 97-letter synthetic plaintexts/ciphertexts, plant keys, observation positions, reachable quotient, independent start domains and budgets match REAL-014 exactly. Full controller and cipher-start domains each contain 11,881,376 starts, with 66,058 reachable index functions representing all 100,000 raw index settings. No actual K4 ciphertext is read.

| Fixture | Previous / sparse seconds | Previous / sparse RSS MiB | Current time index | Peak nodes | Completed controllers | Outcome |
|---|---:|---:|---:|---:|---:|---|
| 0 | 17.223 / 3.800 | 653.9 / 590.0 | 2 | 410 | 0 / 11,881,376 | conservative_branch_domain_envelope_unresolved |
| 1 | 60.161 / 60.016 | 296.4 / 58.4 | 7 | 6,652 | 0 / 11,881,376 | wall_budget_unresolved |


These are single local diagnostic timings, not estimated general speedup factors. Work counters with different semantics are labeled rather than added as independent hypotheses. Completed-controller coverage and candidate counts remain separate from direct plant validation.

Both runs remain unresolved, with zero completed controllers and unknown total key counts. The dense case reaches the same time-2, 410-node envelope guard, with 202 predicate requests but only three zero-offset builds. The separated-window case still stops at time index 7 with 6,652 peak nodes and zero predicate requests; memory falls to 58.4 MiB, but prefix CPU work remains unresolved. It performed 519,540 owner transitions and 14,181 branch visits. Direct plants remain valid, but no selector recovery or full real-sized compatible-set validation is established.

The dense fixture demonstrates the intended cache correction: three zero-offset builds replace 202 while reaching the same 410-node memory-limited frontier. It does not remove the large cipher-domain allocations. The separated-window result measures sparse continuous-prefix ownership directly, rather than skipping unknown plaintext or resetting at a crib.

The [native receipts](../results/sigaba-sparse-ownership) preserve fixture text, source hashes, unknown totals, unfinished controller/time, branch and owner counters, cache accounting, and RSS/wall limits. The prior [REAL-014 receipts](../results/sigaba-real-adapter) are unchanged. Neither a direct known plant nor correctness on tiny complete sets constitutes selector recovery or independent real-sized compatible-set validation.

## Remaining boundary

This batch stops without enlarging resource caps or automatically evaluating K4. The unresolved prefix cost is independent of cipher predicate construction. Even without observations the present dictionaries repeatedly use large integer cipher domains as part of their keys and rebuild offset/class partitions. Canonical domain identities with cached equality/hash, shared trajectory DAGs or symbolic continuous-controller relations are justified next representations. No profiler-based claim of a dominant CPU routine is made from these counters alone.

A sparse or factorized cipher-start constraint representation now has a concrete rationale: after observations each branch owns a subset of starts, yet the current bitset occupies nearly 1.5 MB whenever high indices survive. A compressed set or exact multi-observation rotor relation could avoid that cost. Such an approach is unimplemented and unvalidated here; preserving full correlated solutions and proving complete tiny-system equivalence are prerequisites. No claim of real-sized tractability, exhaustive SIGABA exclusion, or a K4 solution follows.
