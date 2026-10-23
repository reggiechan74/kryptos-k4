# Exact first-observation anchoring: prefix eliminated, dense-domain gate remains

23 October 2026. CSP889-ANCHOR-017 is an exact change of cipher-start coordinates for the frozen unrestricted full torus. It is not a reset, extra seed, cipher exclusion or actual K4 evaluation. [Protocol](SIGABA-FIRST-OBSERVATION-SPEC.md) was frozen at `55bef8c`. The parent supplied the derivation independently; the implementation and controls below validate it for this solver.

## Bijection and original-key reconstruction

For each fixed original controller start q0 and persistent reachable index map h, let prefix displacement be Delta_h before the first observed time a. The map u=c_a=c0+Delta_h modulo q is bijective over the full independent cipher-start torus. Thus every h may share the unrestricted u domain when propagation starts at a. The actual controller digits still come from its original time-zero start, and the same h controls all later steps, including every unknown gap.

Only after a controller's full observed interval is solved, reconstruct each surviving class separately: original starts satisfy c0+Delta_h in its anchored domain U_h. The proven torus preimage operation computes that exact set. Original final offsets are Delta_h plus post-anchor offsets. The compact output groups only equal original offsets AND exact original cipher domains, preserving each class and all raw aliases. It never reuses a representative h's displacement for other maps. Totals are committed only for a fully reconstructed controller.

Restricted initial starts are explicitly rejected by the API. They require a translated restriction depending on q0 and h; this full-domain equivalence cannot silently be applied to common-letter starts or indicator-derived initialization. Empty observations use a=0. There is no re-anchoring/reset at the second crib.

## Complete correctness controls

Eight complete q=2/3 fixtures cover empty/short/long masks plus delayed single observations. All original-time raw compatible-key streams match independent physical enumeration byte for byte after inverse reconstruction. All 24 cache-policy relation comparisons match unanchored inference, including final offsets and every map correlation; multiple index aliases and ambiguity are retained. Prefixes cross controller carry states and long fixtures contain the separated windows/gap. Every subset of the binary three-coordinate torus and every displacement passes independent preimage checks (2,048 comparisons). Every small map's prefix displacement is checked against physical schedules. Those q=2/3 full-contact fixtures cannot by themselves distinguish shifted controller times, so a separate q=5 non-full-contact physical trace verifies every position through both islands and the gap, and detects deliberately shifting controller time back to the anchor. This is a physical trace control, not an additional complete-set search. Deliberately using one shared wrong prefix, skipping an actual unknown transition, conflicting observations and requesting restricted starts are rejected or detected appropriately.

Chronology is preserved in [ANCHOR-017-chronology.json](../results/ANCHOR-017-chronology.json). The shell initially continued into a resource run after an added mutation-control failure: replacing one collector set by another was inert on the full-contact q=3 fixture. Core set-equivalence controls had passed, but that added gate had not. Those premature receipts are quarantined separately and are NOT the official benchmark or added coverage. The mutation was corrected to skip an actual transition; all five then-existing test methods passed before the identical official benchmark was rerun. The solver algorithm did not change between premature and official runs. No history or failed outcome was erased.

## Unchanged authentic synthetic resource gate

Both REAL-014 fixtures, 97-letter synthetic messages, plants, observations, controller ordering, independent start domains and reachable shared index quotient are unchanged. Limits remain 60 seconds per fresh process, watchdog65, 1-GiB measured RSS with headroom, 256-MiB conservative branch envelope and 64-MiB cache. The 66,058 reachable maps represent all 100,000 raw index starts; no free per-time masks are substituted.

| Fixture | DOMAIN-016 / anchored seconds | Old / new peak RSS MiB | First observed / last reached index | New predicate requests | Completed controllers | Outcome |
|---|---:|---:|---:|---:|---:|---|
| 0 | 3.426 / 3.385 | 546.3 / 566.4 | 0 / 2 | 202 | 0 / 11,881,376 | conservative_branch_domain_envelope_unresolved |
| 1 | 60.003 / 4.310 | 84.9 / 733.7 | 21 / 24 | 318 | 0 / 11,881,376 | conservative_branch_domain_envelope_unresolved |


The separated-window run now starts cipher constraints at time 21, reaches time index 24 and makes 318 predicate requests, with four zero-offset builds. The earlier cached-key run timed out at index 17 before any predicates. This validates removal of the unobserved-prefix frontier; it does NOT mean that all observed constraints at index 24 completed. The branch-domain guard interrupts within that time step. The new 4.310-second / 733.7-MiB result is a memory-limited partial run, not a completed 60-second inference or an estimated general speedup.

Both official fixtures complete zero controllers. Total compatible key counts remain unknown, not zero. Neither reaches a full candidate requiring inverse expansion at real size; per-map reconstruction is proven by complete tiny tests rather than falsely claimed from the real runs. No full real-sized compatible-set comparison or scaling gate passes. K4 stays unevaluated and unsolved.

The remaining measured barrier is simultaneous dense cipher-start domains after observed transitions: each can occupy nearly 1.5 MB. Exact compressed sets, multi-observation rotor constraints or a layered cipher-path DAG are future algorithmic choices, not implemented results in this batch. No budget enlargement follows these failures.

## Literature provenance and unrun diagnostic

The [original independent literature synthesis](SIGABA-LITERATURE-AND-FILTER-REVIEW.md) is saved as supplied, with [local source/provenance notes](../sources/sigaba-literature-anchoring-2026-10-23.json). The published repeated-collector-set filter intersects possible step-mask sets; survivors still require one reachable physical index setting and a connected compatible path. No such filter or statistical ranking is combined into ANCHOR-017. The suggested supplied-anchor/controller panel is explicitly proposed and unrun; it would be a selectivity diagnostic, not full-domain search or recovery of unknown starts. Published assumptions/resource estimates are not transplanted to the 24 separated K4 letters.
