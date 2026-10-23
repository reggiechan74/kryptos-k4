# Authentic CSP-889 adapter: correctness passes, resource gate fails

23 October 2026. The [protocol](SIGABA-REAL-ADAPTER-SPEC.md) was frozen at `2fc80eb`, and the adapter/runner committed at `88ce73f` before synthetic evaluation. No actual K4 ciphertext was read or evaluated. This is a synthetic engineering result, not a cipher exclusion.

The new adapter uses the pinned CSP-889 / ECM Mark II conventions: real 26-symbol large wheels, five static ten-contact index wheels, F–I pulses, the source collector and magnet tables, backward control-bank traversal, pre-step notch O=14 and continuous fast/medium/slow carry. All five cipher starts and control starts are independent. Every one of 100,000 raw index starts contributes to the exact shared reachable index quotient; the resulting 66,058 functions and their multiplicities reproduce the earlier independent quotient hash `3a257b5d35ea1aae7cd76e06786c67798e19101f147431e0031eb6a2d7e526ec`.

All twelve externally published Sullivan-attributed vectors pass encryption and decryption through the adapter, existing direct implementation and a separate physical-contact-pair loop, including non-normal orientations and differing wheel orders. These remain software-to-software vectors with documented fixture translation, not surviving wartime hardware transcripts. The large-wheel wirings are the documented simulator set, not recovered historical secret wirings. The six complete q=2/3 tiny fixtures compare exact coupled relations and full raw compatible-key streams against independent physical enumeration. Empty/ambiguous domains stay ambiguous; no planted key is selected as the only answer.

## Real-sized preflight and measured outcomes

The frozen layout fixes cipher wheels 1–5, control wheels 6–10, index wheels 1–5, all normal orientations. Each full controller and cipher-start domain has 11,881,376 elements. Raw full-start descriptions number 14,116,709,565,337,600,000. A single dense cipher-domain payload occupies 1,485,172 bytes. Assigning such a separate payload to every index function would exceed 98 GB. That is a conservative planning scenario, **not a proved necessary memory lower bound**; no such Cartesian table was allocated.

The declared 60-second, 1-GiB measured-RSS limits, 64-MiB cache and 256-MiB conservative branch-domain envelope were retained. Shared immutable integers are counted once in the envelope; per-node overhead and two live frontiers remain conservatively guarded. The RSS guard is measured with reserved allocation headroom, not an OS hard allocation limit.

| Synthetic fixture | Outcome | Seconds | Peak RSS MiB | Completed controllers | Last time index | Peak live nodes |
|---|---|---:|---:|---:|---:|---:|
| Dense early observations, 0–12 | Branch-domain envelope exceeded | 17.223 | 653.9 | 0 / 11,881,376 | 2 | 410 |
| Two separated windows, 21–33 and 63–73 | Wall budget exceeded | 60.161 | 296.4 | 0 / 11,881,376 | 7 | 6,652 |

Both runs were inside the first controller when interrupted. Total compatible-key counts are **unknown**, not zero; zero fully processed controllers provide no meaningful negative key coverage. The prescribed plants regenerate each complete synthetic ciphertext through all three implementations, but neither selector reached their controller. Direct planted validation is not blind selector recovery. No independent full real-sized compatible-set comparison completed. Therefore the real-sized admission gate fails, and no K4 evaluation follows.

Per-case receipts retain the actual fixture text, exact plant, observations, unknown totals, unfinished controller, counters, budget and executed source hashes: [case 0](../results/sigaba-real-adapter/case-0.json), [case 1](../results/sigaba-real-adapter/case-1.json). No fixture was eased or resource cap extended.

## Specific remaining engineering bottlenecks

The dense case made 202 predicate requests and 202 zero-offset builds. At this dimension the existing translation backend reserves 65,633,608 bytes for fixed masks inside a 67,108,864-byte cache. The remaining 1,475,256 bytes are smaller than one 1,485,172-byte predicate payload, even before integer overhead: base predicates cannot be cached. This is a measured cache-layout failure, not evidence that the translation identity is wrong. A future separately frozen policy should reserve space for base predicates and construct or factor translation masks on demand; it must reproduce the same complete tiny sets and unchanged real fixtures.

The separated-window case made **zero predicate requests** before timing out. Continuous unknown-prefix control/index evolution alone produced 6,652 live nodes and 14,181 branch visits by index 7. Cache tuning cannot fix that branch's pre-observation bottleneck. Sparse index-class ownership, grouping complete reachable-map trajectories, or symbolic control-state relations offer a concrete reason to investigate an alternative representation: each index class follows exactly one trajectory for a fixed controller, so its class membership need not be copied as dense high-bit-position sets at every split. Any replacement must retain one shared reachable map, continuous timing and complete compatible-set comparison. It is not permission to replace the controller with independent per-letter masks, sample starts or enlarge budgets.

The current representation has not demonstrated authentic real-sized tractability. K4 remains unsolved; broad SIGABA, unknown historical wirings and other wheel orders remain outside the earlier finite negative coverage.
