# Repeated-collector consistency: sound and selective on a supplied panel

23 October 2026. CSP889-FILTER-019 is a separately frozen **local-only synthetic diagnostic**, not a K4 search, blind key recovery or full-domain gate pass. [Protocol](SIGABA-COLLECTOR-FILTER-SPEC.md) frozen at `aeeb894`; controlled implementation committed at `d72221d` before panel outcomes. The unchanged all-controller admission fixtures/results remain separate: COMPACT-018 completed only 12/14 controllers under its resource caps; FILTER-019 adds no full-domain controller coverage.

## Mechanism and retained path constraints

For each supplied cipher anchor, the implementation retains every legal transition under masks 1–30 that matches the next known symbol, merging equal states by layer but keeping all edges. Backward/forward pruning removes only edges off complete root-to-final paths. The stored DAGs retain actual state/edge identity and connected alternatives; different anchors are never pooled. No beam search, statistical ranking, probability threshold or endpoint trimming is used.

For a fixed original controller, its actual collector digit sets at the twelve absolute transition times must map to constant cipher-step masks because the index bank is static. The [published necessary condition](SIGABA-LITERATURE-AND-FILTER-REVIEW.md) intersects allowed mask sets over every occurrence of an equal collector set. Empty intersections reject; constrained edges must still contain a connected path. Passing is only necessary: a connected path could choose differing masks from the common set at repeated occurrences, and even a consistent abstract assignment might not correspond to a reachable physical index map. Unit controls explicitly demonstrate this insufficiency. No passing filter pair is promoted to a key without exact physical execution.

## Deterministic panel and complete physical audit

Each fixture includes the synthetic true anchor plus up to two different anchors chosen by the frozen bounded rule: lexicographic IDs 0–4095, at most 16 first-pair-matching candidates, retain the first two with a complete 13-letter DAG. Wrong means different from the planted state, not proven cryptographic inequivalence. This is an intentionally first-window-conditioned panel, not an independent null or unknown-anchor search. Four controller starts are fixed in advance: plant, zero, plant fast+1 and plant outer+1.

Fixture 0 produced only one retained wrong anchor after 16 candidates. We kept its two-anchor/eight-pair panel instead of changing the rule. Fixture 1 produced two wrong anchors after seven candidates, giving twelve pairs. Both encryptions use the same declared synthetic plaintext, so these are not independent language/corpus samples.

Every panel pair—including filter rejections—was independently checked against all 66,058 reachable index functions with all raw aliases represented. Each map executes the actual continuous control trace and cipher path through the first block. Any feasible path's edges must belong to the original DAG. Thus the audit can detect false-negative pruning rather than assuming rejected pairs are impossible.

| Fixture | Retained anchors / attempted wrong roots | Panel pairs | Repeat-bearing pairs | Filter rejects | Filter false positives | Physically feasible pairs | Map trials | Seconds | Peak RSS MiB |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 2 / 16 | 8 | 6 | 5 | 2 | 1 | 528,464 | 0.828 | 47.2 |
| 1 | 3 / 7 | 12 | 12 | 7 | 4 | 1 | 792,696 | 1.158 | 47.4 |


Across 20 pairs, the filter rejects 12 and passes 8. Physical execution finds exactly two feasible pairs, both the supplied plant anchor/controller; six filter passes have no physical map. **Zero false negatives** occur across 1,321,160 map trials and 2,696,855 cipher point checks. This establishes soundness on this exhaustive panel audit, not a global empirical error bound or selectivity estimate for unseen anchors/controllers.

Collector-set repetition counts are modest: 0–2 additional occurrences per pair. Eighteen of 20 pairs contain repeats. The stored DAGs are small (220 retained edges across the five selected anchors). Their source-pinned [native receipts](../results/sigaba-collector-filter) retain all graphs, attempted roots, pair decisions, mask intersections and physical feasible classes.

## Continuous second-window and original-key checks

Each feasible class retains its actual anchor, original controller and one physical map. The fixture1 key advances all 29 unknown gap positions without invented plaintext, then satisfies the second observed block. Per-map prefix inverse reconstructs the original cipher start. Both fixture keys decrypt/re-encrypt all 97 synthetic symbols exactly and match the generated plaintext. Fixture 0 has no second block in its frozen input. Its feasible map has three raw index-position aliases; fixture1 has one. Alias ambiguity is preserved rather than calling the representative settings unique.

These are supplied-anchor/controller controls. They do not discover either unknown, do not test new K4 keys, and cannot replace unrestricted independent-start inference. Full ciphertext regeneration is a consistency check, not independent evidence for a cipher choice. The sparse completed-controller prefixes from COMPACT-018 are not enlarged by adding these panel trials; overlapping subsets must not be counted twice.

## Selectivity cost and limits

The two fixture processes take 0.828 and 1.158 seconds at about 47.3 MiB RSS, within the unchanged 60-second/1-GiB limits and separate graph caps. Aggregate filter time is about 0.00065 seconds; aggregate physical-audit time about 1.659 seconds. Single microtimings are diagnostics, not calibrated performance statistics.

If these decisions were used to skip physical execution, 12 rejected pairs would avoid 792,696 map trials and 1,613,512 cipher checks on this fixed panel. The audit actually performed that work. These are **counterfactual panel savings**, not a measured pipeline speedup or a projection to all 11,881,376 controller starts and all cipher anchors. Graph construction/anchor selection and index-quotient cost are included in the overall fixture timings.

There is useful conditional pruning here, so the avenue is not disproved by the short crib. Its demonstrated limitation is the need for a supplied, already first-window-compatible anchor and a tiny selected controller panel. Building/retaining the unknown-anchor cipher DAG and validating any full-domain integrated filter within memory/time remain open algorithmic tasks. A separately frozen integration would need complete tiny truth, false-negative checks and exact physical reachability; neither statistical scoring nor universal per-layer mask pooling can replace them.

This finite diagnostic stops at its frozen panel. No new anchors/controllers, extra known letters, larger budgets, K4 evaluation, public Site change or publication retry follows from these results.
