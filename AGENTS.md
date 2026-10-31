# Agent instructions for Kryptos K4

## Canonical working to-do list

[research/HYPOTHESES.md](research/HYPOTHESES.md) is the project's authoritative working to-do list and hypothesis-status reference. Read its current-state section, single next-action queue and relevant family records **before choosing or starting work**. Read [research/EXPERIMENTS.md](research/EXPERIMENTS.md), the [external prior-art register](research/EXTERNAL-PRIOR-ART.md) and linked primary evidence to avoid repeating hypotheses already attempted here **or by other researchers**. The latest user direction controls authorization; a queued proposal is not permission to run, expand, publish or submit it externally.

## Required public prior-art gate

Before selecting an experiment, compare its exact operator/equations, alphabet roles, key indexing, stage order, state update, bounds and crib/length alignment against both the local ledger and external register. Check aliases and subset/superset coverage, not just cipher names. Record the closest stable EXT IDs, pinned sources, comparison and a dated targeted web/repository search in the hypothesis entry. Unknown external scope is **unresolved eligibility**, not proof of novelty.

The current direction is to test only hypotheses not already tried. Do not queue stronger-solver reruns, unfinished searches of attempted hypotheses or cosmetic width/period/alphabet extensions as new. Prior proposals that were genuinely never run may qualify, but first check whether a local or external analytical invariant already excludes them. Do not pad a requested shortlist when no candidate clears the gate. Explicit later user authorization may permit a deliberate reproduction; label it reproduction and retain its purpose, rather than presenting it as novel.

Preserve evidence quality independently of the no-duplication decision: third-party “exact” claims, skipped systems, thresholds, timeouts and sampled controls have different meanings. Do not convert them to universal exclusion or add external runs to our local run totals.

## Mandatory end-of-experiment checklist

At the end of **every experiment run**, including negative, failed, interrupted and inconclusive runs, reconcile the ledger before declaring completion or deciding what runs next:

1. Record the experiment ID, exact model and tested bounds, frozen assumptions, execution status, result and its limits. Distinguish completed from excluded, compatible from identified, and heuristic not-found from exact contradiction.
2. Link the immutable protocol, code, receipts, results and independent audit. Keep original failures, corrections and superseded records; never silently replace them. Label missing evidence and compute limits explicitly. Do not fabricate run times from commit times.
3. Update the relevant family records in `research/HYPOTHESES.md`: tested and untested scope, remaining uncertainty, blockers/dependencies and next discriminating action. Update the existing current-state summary and single next-action queue in place; do not prepend another narrative block or competing queue. Detailed chronological receipts belong in `research/EXPERIMENTS.md`, not the working ledger. Explain why the next item advances, stops, remains blocked or requires a separate decision. A completed finite test does not eliminate the broader family.
4. Add or update the run in `research/EXPERIMENTS.md`. Review its explicit category/outcome in `docs/tracking/curated-records.json`; do not let a title guess determine classification. Keep publication status separate from scientific outcome and preserve separately authorized exploratory expansions as such.
5. Regenerate derived views with `python3 experiments/build_research_navigation.py`. Do not hand-edit generated tracker tables or `docs/tracking/tracker.json`. Run the relevant documentation/ledger tests and local-link checks, and verify the generated views agree with canonical sources.
6. Update relevant external-register overlap notes and add any new external evidence with stable IDs, precise scope, method, outcome, source pin/date, evidence tier and limitations. Preserve historical claims and dated corrections. Consult both the reconciled local ledger and external register again to select the next eligible action under the current user authorization and protocol gates. If no eligible test exists, record the blocker rather than inventing a target run. State whether the proposed next experiment has actually started.

## Evidence and execution safeguards

Read [research/POLICY.md](research/POLICY.md), the selected frozen protocol and applicable folder guidance. Preserve canonical ciphertext and public clue indexing. Any changed family, alphabet, stage order, key range, scoring rule or search budget needs explicit scope and appropriate controls. Tiny exact checks and blind length-matched benchmarks precede target use when the protocol requires them. Count equivalent operators once. A plausible sentence or unrestricted key that re-encrypts is not a solution.

Run instructions are in [experiments/README.md](experiments/README.md) and [tests/README.md](tests/README.md). A documentation-only task should regenerate/validate documentation without rerunning cryptanalysis. Before launching validation, classify each selected command as static/documentation, synthetic, archived-target replay or new-target execution, then select only what the change requires. Keep legitimate archived regressions available, but record their replay cost separately and never count them as new research;064closeout retained an unnecessary archived-replay selection as a method lesson. For publication, inspect the current remote head, preserve unrelated changes, avoid force-pushes, and verify the resulting remote commit and applicable checks before claiming success. No documentation command changes the live Site.

## Evidence-driven method improvement

Before manually rediscovering ordinary-period 044 exclusions, consult the [retained-negative index](research/negative-certificates-v1/README.md). Its source-pinned checker transfers only conditional crib-level negatives under identical semantic metadata. Verify the supplied partition’s mechanism-wide necessity independently. No hit is not admission; phase/reset and full-message equivalence remain outside v1.

At every closeout, record a measured bottleneck or useful lesson, the proposed implementation/test/method change (or why the current method should be retained), fresh independent held-out validation needed, and the versioned ledger decision. Preserve frozen artifacts and failures. Never reuse revealed benchmark outcomes as a fresh holdout, weaken admission gates, or rename an old hypothesis as a new one. Reusable tools require technical prior-art and utility review before being presented as globally novel or split into a separate repository.

For source literals within its deliberately narrow supported syntax, use the [read-only literal checker](research/source-literal-checker-v1/README.md) to verify reconstruction against independently pinned source bytes, preserving request/result receipts. It does not authenticate the pin or validate program semantics, formulas, imports, aliases or runtime mutation. Unsupported syntax requires explicit independent source review, not executing untrusted code or silently broadening this tool. The original062 transcription correction remains evidence; extending the checker requires a new freeze and fresh independent tests.
