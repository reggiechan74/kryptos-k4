# Exact compressed cipher domains: measured storage and coverage

23 October 2026. CSP889-COMPACT-018 remains local pending renewed remote publication authorization. No publication retry, actual K4 evaluation, changed key domain or Site edit. [Protocol](SIGABA-COMPRESSED-DOMAIN-SPEC.md) frozen at `ef57599`; [storage decision](SIGABA-COMPRESSED-DOMAIN-IMPLEMENTATION.md) and profile evidence committed at `f5cb4aa`; controlled implementation committed at `e288739` before uninstrumented benchmark outcomes.

## Evidence that justified compression

The instrumented ANCHOR-017 guard retained 176 distinct integer payloads using 278,155,004 bytes, although each contained only 534–799 states. Sorted unsigned32 indices would need 482,752 bytes including byte-object headers. The separated-window guard retained 192 payloads using 291,806,840 bytes, with only 11–51 states each; its packed estimate was 26,852 bytes. These are exact cardinality/storage observations at partial frontiers, not independent key counts. Raw [density profiles](../results/sigaba-payload-profile) retain histograms, densities, source hashes and the unchanged guard. Instrumentation timing is not the performance comparison.

## Exact adaptive representation

Each immutable cipher-start set uses either its exact bitmap integer or sorted unique unsigned32 little-endian state IDs, selected deterministically by actual payload size. No tuned density cutoff, sampling, truncation or path ranking is used. Cached hashes equal the exact integer-set hash; packed storage computes the same hash algebraically from state IDs. Equality verifies actual values even when representations differ or hashes collide. Native output declares bitmaphex/u32lehex and cardinality, preserving sparse high-index sets without expanding them into megabyte hex integers.

Bitmap filtering retains the original whole-torus predicate. Packed filtering evaluates every stored candidate directly through the same physical rotor tables at the actual offsets. Every candidate is tested, not sampled. Map-dependent anchor inverse translates every packed coordinate tuple and re-sorts, or uses the proven bitmap preimage. Live offset/owner correlations, shared reachable index maps, aliases, actual control timing and all unknown gaps remain unchanged.

Eight complete q=2/3 fixtures are compared under automatic, forced-bitmap and forced-packed storage and three cache policies: 72 correlated-relation comparisons plus 24 independent complete raw-stream comparisons across those representation modes. Counts are engineering control configurations, not new cipher hypotheses. Every small subset/intersection, encode/decode, cross-format equality/hash, anchor preimage, deliberate collision, bad framing, incorrect shared prefix and skipped/shifted transition control passes. The non-full-contact q=5 physical trace checks actual controller time through the gap. A deterministic point panel across all twelve pinned real-vector layouts compares packed filtering against physical contact-pair evaluation, including reversal settings; that panel is a correctness control, not a full-domain search. Empty/ambiguous outputs remain exact sets; deliberate resource failure returns unknown.

## Same real-sized fixtures and budgets

Both REAL-014 plaintexts/ciphertexts, plant keys, observations, full independent start domains, controller order and 66,058 reachable maps are unchanged. Resource limits remain 60 seconds per process, a 65-second watchdog, 1-GiB measured RSS with headroom, 256-MiB conservative branch/output envelopes and 64-MiB cache. Counter names distinguish whole-torus predicate construction from direct candidate evaluations.

| Fixture | Old memory-limited seconds / compact seconds | Old / compact RSS MiB | Completed controllers | Last unfinished time index | Completed-filter point checks | Outcome |
|---|---:|---:|---:|---:|---:|---|
| 0 | 3.385 / 60.001 | 566.4 / 162.6 | 12 / 11,881,376 | 2 | 81,066,780 | wall_budget_unresolved |
| 1 | 4.310 / 60.001 | 733.7 / 152.8 | 14 / 11,881,376 | 23 | 88,043,284 | wall_budget_unresolved |


Actual native controller coverage advances from zero to 12 completed controllers on the dense fixture and 14 on the separated-window fixture. They stop at the unchanged 60-second wall limit, not the old memory envelope, at 162.6 and 152.8 MiB peak RSS. No compatible raw keys occur in either completed controller prefix; the remaining 11,881,364 and 11,881,362 controllers are unresolved. The unfinished controller is retained explicitly. Total key counts remain unknown, not zero. The completed prefixes represent 14,257,651,200,000 and 16,633,926,400,000 raw start descriptions respectively, including index aliases; those are model-domain descriptions, not independent hypotheses or unique plaintexts.

These are single local diagnostic measurements, not general speedup or success-probability estimates. A completed controller means its full compatible relation is resolved for the observation problem, not that a selected plant was recovered. An empty domain may terminate early on a first-window contradiction; later observations and inverse reconstruction are then unnecessary. Any surviving domains must continue through the actual gap and receive their map-dependent inverse. Interrupted totals are unknown. Exact completed-prefix raw description counts are not counts of independent hypotheses.

Native [compact receipts](../results/sigaba-compressed-ownership) retain exact result encodings, source hashes, measured resources and prefix coverage. Original ANCHOR-017 receipts and the density-profile runs remain separate. The raw full domain is unchanged; neither direct plant replay nor a processed prefix passes the full all-controller gate or supplies an independent real-sized complete-set comparison. No K4 inference is authorized by this outcome.

## Remaining boundary

Exact packing removes the measured dense-set memory barrier on these two runs, but full-domain inference is still far beyond this completed prefix. Work now includes 81,066,780 and 88,043,284 candidate checks in completed sparse-filter calls, plus millions of owner transitions and frontier operations. If interruption occurs within a filter call, its partial candidate work is not added to this counter; the reported checks are lower bounds on actual work, not exact total instruction counts. A fresh profile is needed before attributing dominant CPU time or choosing a further optimization. No throughput projection is asserted as a lower bound or proof of feasibility. Published repeated-collector consistency/path-DAG filters remain proposed, separately specified work; they cannot replace shared physical reachability or full-domain validation.

This finite storage batch stops after its two unchanged resource runs. No larger runtime, extra observations, new schedules or automatic next search follows. The physical evidence gaps and unknown historical machine/wiring assumptions remain separate from this software engineering result.
