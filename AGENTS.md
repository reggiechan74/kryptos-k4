# Agent instructions for Kryptos K4

## Canonical working to-do list

[research/HYPOTHESES.md](research/HYPOTHESES.md) is the project's authoritative working to-do list and hypothesis-status reference. Read its current-status section, proposed queue and relevant family records **before choosing or starting work**. Read [research/EXPERIMENTS.md](research/EXPERIMENTS.md) and linked evidence to avoid repeating an already completed test. The latest user direction controls authorization; a queued proposal is not permission to run, expand, publish or submit it externally.

## Mandatory end-of-experiment checklist

At the end of **every experiment run**, including negative, failed, interrupted and inconclusive runs, reconcile the ledger before declaring completion or deciding what runs next:

1. Record the experiment ID, exact model and tested bounds, frozen assumptions, execution status, result and its limits. Distinguish completed from excluded, compatible from identified, and heuristic not-found from exact contradiction.
2. Link the immutable protocol, code, receipts, results and independent audit. Keep original failures, corrections and superseded records; never silently replace them. Label missing evidence and compute limits explicitly. Do not fabricate run times from commit times.
3. Update the relevant family records in `research/HYPOTHESES.md`: tested and untested scope, remaining uncertainty, blockers/dependencies and next discriminating action. Update the current recent-results summary and queue status/order. Explain why the next item advances, stops, remains blocked or requires a separate decision. A completed finite test does not eliminate the broader family.
4. Add or update the run in `research/EXPERIMENTS.md`. Review its explicit category/outcome in `docs/tracking/curated-records.json`; do not let a title guess determine classification. Keep publication status separate from scientific outcome and preserve separately authorized exploratory expansions as such.
5. Regenerate derived views with `python3 experiments/build_research_navigation.py`. Do not hand-edit generated tracker tables or `docs/tracking/tracker.json`. Run the relevant documentation/ledger tests and local-link checks, and verify the generated views agree with canonical sources.
6. Consult the reconciled ledger again to select the next eligible action under the current user authorization and protocol gates. If no eligible test exists, record the blocker rather than inventing a target run. State whether the proposed next experiment has actually started.

## Evidence and execution safeguards

Read [research/POLICY.md](research/POLICY.md), the selected frozen protocol and applicable folder guidance. Preserve canonical ciphertext and public clue indexing. Any changed family, alphabet, stage order, key range, scoring rule or search budget needs explicit scope and appropriate controls. Tiny exact checks and blind length-matched benchmarks precede target use when the protocol requires them. Count equivalent operators once. A plausible sentence or unrestricted key that re-encrypts is not a solution.

Run instructions are in [experiments/README.md](experiments/README.md) and [tests/README.md](tests/README.md). A documentation-only task should regenerate/validate documentation without rerunning cryptanalysis. For publication, inspect the current remote head, preserve unrelated changes, avoid force-pushes, and verify the resulting remote commit and applicable checks before claiming success. No documentation command changes the live Site.
