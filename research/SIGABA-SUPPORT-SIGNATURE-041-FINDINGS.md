# Family 4: exact support reuse passes correctness but does not improve the measured gate

Local continuation 041, 24 October 2026. **The proposed exact SIGABA cache is sound in the complete small-system controls, but the real-sized synthetic prefixes have zero cache hits and no coverage gain.** All four comparisons stop at the original time budget; almost the entire requested domain remains unresolved. No K4 joint search is admitted.

[Pre-outcome specification](SIGABA-SUPPORT-SIGNATURE-041-SPEC.md), [implementation](../experiments/sigaba_support_signature_041.py), [independent controls](../results/SIGABA-SUPPORT-SIGNATURE-041-CONTROLS.json), [four-run summary](../results/SIGABA-SUPPORT-SIGNATURE-041-SUMMARY.json), [separate Python 3.12 correctness replay](../results/SIGABA-SUPPORT-SIGNATURE-041-REPLAY.json). Old 024 source/receipts are unchanged. Implementation/control commit `4419203437163a1aa0d4483467b5983aee73da64` precedes the real-sized runs.

## What may be shared, and what never is

For one immutable cipher model and first observed block, necessary root support depends on the collector-set equality partition and each class's exact reachable marginal mask set. Literal collector labels may be renamed if both are preserved. The cache signature also retains the absolute anchor and exact observation pairs. It stores only the necessary initial cipher-root bitmap. Original controllers, reachable shared index maps, unknown prefix/gap, offsets, owners and owner-dependent inverse anchoring remain separate in the unchanged physical verifier. Different models cannot share this cache. Equal marginal supports are not themselves a physical key.

The canonical key uses exact tuples, not a digest-only identity. LRU eviction changes speed only. Interrupted computations are not cached. Cached receipt labels are translated to the requesting controller, and cache hits are not counted as executed edge-support work. The extra root cache is capped at 64 MiB inside the unchanged 1-GiB whole-process cap; predicate, branch and layer caps are unchanged.

## Correctness and finite results

Independent checks cover 70 original and 124 varying-input root graphs, 24 complete physical raw-key streams, and 36 full relation comparisons at zero/one-byte/64-MiB cache caps. All plants and ambiguities are retained. Equality-partition, changed-mask, changed-observation, wrong-model and interrupted-calculation guards pass. An empty-observation statistics KeyError was found before timing, fixed without changing its full root set, and retained in the [preflight receipt](../results/SIGABA-SUPPORT-SIGNATURE-041-PREFLIGHT.json). All twelve published simulator vectors also agree with direct contact execution; these remain simulator controls, not wartime hardware certification.

| Fixture | Backend | Controllers completed of 11,881,376 | Seconds | Peak RSS bytes | Cache hits/misses |
| --- | --- | ---: | ---: | ---: | --- |
| 0 | Uncached necessary filter + exact verifier | 12 | 60.038 | 262,733,824 | — |
| 0 | Canonical root cache + same verifier | 12 | 60.097 | 287,653,888 | 0 / 13 |
| 1 | Uncached necessary filter + exact verifier | 12 | 60.079 | 251,297,792 | — |
| 1 | Canonical root cache + same verifier | 11 | 60.020 | 271,597,568 | 0 / 12 |

Each requests every independent cipher start and 66,058 reachable index maps retaining 100,000 raw aliases. Same REAL014 fixtures, positions and observations; no key restriction, fixture easing or larger budget. All native outcomes are `wall_budget_unresolved`, not a zero total key count. Completed prefixes contain no compatible keys, while unfinished controllers and all later controllers remain unresolved. Root cache payload peaks are about 19.2/17.6 MB. The necessary signatures in these short prefixes are all distinct, so this measured implementation pays cache overhead without reuse. One fewer completed controller is not a statistical slowdown estimate; these are single local runs with uncontrolled background load.

The complete batch ends at 2026-10-24T17:19:26.330832+00:00; each receipt retains its own actual UTC start/end. Temporary publication pauses did not modify the fixtures or rerun them. Historical COMPACT018 already covered the first 12/14 controllers on these fixtures, so the new prefixes add **zero** union coverage beyond that prior result. Do not add overlapping counts. Complete independent real-sized compatible-key-set validation is still absent. The full real-sized admission gate remains failed, and no K4 input is read.

## Other historical/manual branches and masking limits

The [historical source review](../independent/2026-10-24/item7-historical-sources/README.md) and [item 7 findings](STRIP-SOURCE-GATES-027-FINDINGS.md) remain the relevant source gates. The original M-138 illustration is a 25-strip device with one unresolved literal O/Q row; it cannot become an authenticated wartime M-138A issue. Different holders/months used different strip sets. A valid direct nonzero strip excludes self-encipherment, but an unspecified outer substitution can remove that invariant: a synthetic nonzero Caesar strip followed by its inverse is a fully reversible identity. This counterexample illustrates loss of a direct-model invariant, not a new plausible K4 key. In contrast, an outer relabeling already absorbed by an arbitrary-alphabet proof does not evade that proof merely by being renamed a mask.

Missing M-138A inputs remain exact issue/inventory, holder/order, straight/split/channel policy, offsets and the additional masking operation/order. Fixed-ring Wheatstone remains covered; a genuinely different hidden-move Plett procedure needs primary instructions and an external vector. Book/sign mechanisms still lack a creator-selected source/version, traversal, symbol inventory/framing, deterministic inverse and global English-index alignment. Prior Carter/Schliemann context is not a selected K4 edition or extraction. No denied-source route, outreach, paid acquisition or invented codebook was added.

## Completion boundary

This closes the specific proposed memoization question under the measured prefixes, not the SIGABA family. Reuse elsewhere remains possible; discovering a useful controller quotient without computing every expensive root support is an unmeasured algorithmic question, not grounds to raise caps or launch another arbitrary key slice now. Source-selected wirings/initialization/masking remain separately missing. The historical machine/manual family is computationally unresolved and partly source-blocked. No key, plaintext, physical machine attribution or complete-family exclusion follows. New research stays local; no Site change or publication accompanies this report.

A [separate late reviewer-control receipt](REVIEW-CONTROLS-046.md) strengthens active-calculation interruption, explicit wrong-DST and invalid-flag checks without changing this original model, source, receipt or large-run outcome.
