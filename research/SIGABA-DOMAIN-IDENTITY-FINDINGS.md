# Profiler-directed exact domain-key optimization

23 October 2026. CSP889-DOMAIN-016 follows the unchanged SPARSE-015 fixtures. Phase-A [protocol](SIGABA-DOMAIN-IDENTITY-SPEC.md) was frozen at `3bff89c`. After profiling, the [implementation annotation](SIGABA-DOMAIN-IDENTITY-IMPLEMENTATION.md) selected one change; controlled code was committed at `f6c5cec` before uninstrumented benchmark outcomes. No actual K4 evaluation.

## Measured reason for the change

Portable cProfile function tables and exact interrupted solver receipts are preserved under [results/sigaba-domain-profile](../results/sigaba-domain-profile). Each diagnostic used the same fixture and resource caps; profiler overhead affects coverage and is not an uninstrumented speed estimate.

For the separated-window fixture, `merge` has 58.075 seconds self / 58.079 cumulative out of 60.009 total, across 68,409 calls. No cipher predicates were requested. The function repeatedly places `(offset tuple, large integer domain)` keys into dictionaries. Cipher-domain integers at real size can occupy nearly 1.5 MB, and those same unchanging values occur throughout the unknown prefix. The selected change targets this measured repeated-key cost. The dense-fixture profile instead spends 2.488 seconds self in translation out of 4.093 total; translation was not changed in this batch.

## Exact representation and controls

An immutable `Domain` stores the exact nonnegative bitset and a hash computed once at construction. Equality compares full exact bitsets, including deliberately colliding hash values. Independently constructed equal sets still merge; unequal sets never merge merely because hashes match. An unchanged intersection reuses its existing object. There is no global retained-domain pool or fitted domain label. Live ownership, schedules, predicate/cache policy and branching order remain the prior exact mechanism. Allocation admission now counts wrappers plus their underlying integer payloads, preserving shared references and headroom.

This changes key representation, not the represented cipher-start sets or controller/index correlations. Six q=2/3 empty/short/long fixtures pass complete independent raw-key stream comparison; 18 cache-policy relation comparisons match the earlier exact solver. All 243 q=3 three-wheel offset/symbol predicates match direct evaluation under each of disabled, evicting and full caches. Collision, equality, immutability, unchanged-intersection, conflicting-observation and deliberate resource-failure controls pass. Shared trajectory DAGs and compressed cipher sets were not added opportunistically.

## Same real-sized fixtures and limits

Both fixtures, plants, plaintext/ciphertext, observed positions, full independent start domains and shared reachable index quotient match REAL-014 and SPARSE-015 exactly. Each fresh process retains 60 seconds, 1-GiB measured RSS with headroom, the 256-MiB branch-domain envelope and 64-MiB total cache. No cap was raised.

| Fixture | SPARSE-015 / DOMAIN-016 seconds | Old / new peak RSS MiB | Old / new last time index | New peak nodes | Completed controllers | Outcome |
|---|---:|---:|---:|---:|---:|---|
| 0 | 3.800 / 3.426 | 590.0 / 546.3 | 2 / 2 | 410 | 0 / 11,881,376 | conservative_branch_domain_envelope_unresolved |
| 1 | 60.016 / 60.003 | 58.4 / 84.9 | 7 / 17 | 35,290 | 0 / 11,881,376 | wall_budget_unresolved |


These are individual local timing diagnostics. Profiler runs are separate from these uninstrumented measurements. Work counters retain their actual meanings; raw declared key-domain size is not examined-key coverage.

The prefix run advances from time index 7 to 17, retaining all 66,058 class owners at peak and reaching 35,290 peak nodes, 1,186,963 owner transitions and 249,550 branch visits. It still completes zero controllers and makes zero predicate requests. Therefore actual controller coverage does not advance, although the partial prefix does. It times out at 60.003 seconds with 84.9 MiB peak RSS. The dense case stops at the same time-2 memory frontier after 3.426 seconds with 546.3 MiB RSS. Both total key counts remain unknown; neither is a K4 negative.

Neither complete inference nor independent full real-sized compatible-set validation has passed. Direct plant regeneration remains only a control, not blind selector recovery. Empty totals from interrupted runs are not zero-survivor claims. The K4 gate remains closed, and the puzzle remains unsolved.

## Remaining engineering boundary

The current solver still reconstructs increasing offset/owner frontiers and repeatedly scans them for conservative resource admission. These operations are visible implementation costs, but the next dominant CPU routine has not been measured after this change, so no new profiler-based attribution is claimed. A shared trajectory DAG or incremental exact resource accounting would need a new measured correctness/performance gate. The separate dense-case limit remains nearly 1.5-MB cipher-domain payloads on many simultaneous branches. Exact compressed or multi-observation rotor relations are a plausible representation change, not implemented evidence of real-sized tractability. The immediate boundary is this implementation/resource gate, not a mathematical proof that authentic inference is impossible.

This finite batch stops after its two frozen benchmark runs. No additional representation, trajectory DAG, compressed domain, budget extension or K4 search was introduced after the outcomes. An implementation/resource failure here is not a proof of global SIGABA impossibility.
