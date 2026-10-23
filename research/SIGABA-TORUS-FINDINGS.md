# Exact torus predicate reuse: unchanged fixtures, measured outcomes

23 October 2026. SIGABA-TORUS-013 optimizes the coupled synthetic solver without changing its machine or key domain. **No actual K4 ciphertext is evaluated.** The authentic real-sized adapter remains a separate gate.

## Proof and implementation

For independent initial cipher positions s and accumulated offsets delta, every rotor contact is evaluated at s+delta modulo q. Hence

`D_delta(p,c) = {s : s+delta belongs to D_0(p,c)}`.

The backend builds a zero-offset rotor predicate only for a requested (p,c) pair, then translates its bitset on `(Z/qZ)^r`. With lexicographic base-q state indices, one coordinate translation rotates contiguous stride-sized blocks independently inside each period. Low blocks wrap left and the rest shift right. Exact integer masks preserve width, wrap and correlations. The [implementation](../experiments/sigaba_torus.py) includes both base and translated entries and fixed masks in the same 64-MiB accounted cache; disabling or evicting the cache changes performance only.

The baseline solver received only an optional predicate-factory argument. Its controller enumeration, shared reachable index domain, continuous state updates, independent cipher-start domain and correlation-preserving merge are unchanged. It never substitutes independent per-time masks. The old measured receipts and their executed source remain pinned to main `9840d8af781dc7291683267106f49223959117e7`.

[Identity controls](../results/SIGABA-TORUS-013-controls.json) compare 6,739 complete predicates with both the original meet-in-the-middle evaluator and physical evaluation of 998,515 independent initial states. Every subset of the small binary torus passes translation/inverse checks; unit tests additionally check composition on every subset and every pair of offsets. Coupled relations remain identical under disabled, evicting and enabled caches. This validates an algebraic optimization, not an additional cryptanalytic hypothesis.

## Complete validation without truncated large key sets

The former q=4 five-wheel case has 12,582,912 compatible raw keys, too many for the frozen two-million-key expansion cap. Raising that cap was unnecessary. In this fixture the pulse set is the entire q-symbol alphabet. Every control-bank permutation therefore presents the same full contact set at every time, regardless of controller starts. The index bank is static, so its chosen magnet set is constant for each raw index setting.

An [independent compact verifier](../experiments/sigaba_compact_oracle.py) physically enumerates all 100 raw index settings and all 1,024 cipher starts once. It then represents the same compatible cipher-start domain for each of the 1,024 control starts. Canonical rows are `(control tuple, raw index tuple, complete cipher-start bitset)`. The native and independent complete canonical streams match **byte for byte**: 49,152 rows represent all 12,582,912 keys, using 13,025,280 output bytes within the original 256-MiB limit. Counts/hashes are retained as receipts, not used instead of exact stream comparison. No solution is truncated or silently discarded.

This full-contact symmetry is used only when its precondition holds. It is explicitly rejected for q=5 and does not justify skipping control inference in q=6 or q=8. The original ten tiny/control cases still receive full independent raw-key comparisons. Other scaling cases retain the declared validation strength: complete differential relation comparison where the old run completed, or only old completed-prefix comparison where it did not, plus independent checking of every returned key when it fits the existing limit. A larger-domain exhaustive independent truth comparison is not falsely claimed.

## Honest performance comparison

The [protocol](SIGABA-TORUS-SPEC.md) was frozen at `4b90392`; controlled implementation was committed at `e593cd5` before the new benchmark batch. All thirteen fixtures remain byte-identical, with SHA-256 `2ad409cafff033932a79f4aa45e3f7ac557833e540b0902bef721da4f9d03b9a`. The same 600-second wall guard, 1-GiB measured-RSS guard, 64-MiB cache and output-byte limits apply in fresh separate processes. No fixture, observation, key domain or cap was eased after outcomes.

| Case | q / wheels | Old inference s | New inference s | New total s | Peak RSS MiB | Complete inference / validation |
|---|---|---:|---:|---:|---:|---|
| 0 | 2 / 3 | 0.000 | 0.000 | 0.013 | 19.9 | True / True |
| 1 | 3 / 3 | 0.001 | 0.001 | 0.031 | 20.1 | True / True |
| 2 | 3 / 3 | 0.003 | 0.004 | 0.127 | 20.2 | True / True |
| 3 | 4 / 3 | 0.007 | 0.007 | 0.486 | 20.2 | True / True |
| 4 | 5 / 3 | 0.022 | 0.022 | 0.856 | 20.2 | True / True |
| 5 | 6 / 3 | 0.052 | 0.046 | 1.692 | 20.7 | True / True |
| 6 | 2 / 5 | 0.021 | 0.023 | 1.527 | 21.2 | True / True |
| 7 | 3 / 5 | 0.175 | 0.183 | 15.562 | 25.4 | True / True |
| 8 | 2 / 3 | 0.000 | 0.000 | 0.008 | 20.1 | True / True |
| 9 | 2 / 3 | 0.000 | 0.000 | 0.003 | 20.0 | True / True |
| 10 | 4 / 5 | 0.942 | 0.993 | 1.770 | 57.6 | True / True |
| 11 | 6 / 5 | 43.777 | 39.072 | 39.229 | 118.7 | True / True |
| 12 | 8 / 5 | 600.000 | 534.476 | 534.580 | 144.0 | True / True |


These are single local measurements, not statistical speedup estimates. Total benchmark time includes independent verification/output; inference time is reported separately. The q=4 old validation was incomplete, so its old total is not a comparable complete-verification timing. Old offset-specific builds and new zero-offset builds are different work units, explicitly labeled in [the comparison](../results/SIGABA-TORUS-013.json). Memory did not necessarily decrease.

The largest toy inference completed all 32,768 controllers in 534.476 seconds, retaining 2 raw keys. Both returned keys pass independent physical evaluation; the earlier completed 5,080-controller prefix agrees exactly. Peak measured RSS was 144.0 MiB. This is a toy result, not a real-sized gate. There is no independent exhaustive truth enumeration for the full largest domain.

Original receipts are retained under [results/sigaba-joint-toy](../results/sigaba-joint-toy); optimized receipts are separate under [results/sigaba-torus](../results/sigaba-torus). Complete old/new relations agree across every completed baseline case. The q=8 comparison against the earlier run covers only its 5,080 completed controllers, not its previously unresolved complement.

## Remaining gate

Even a complete toy result does not validate authentic real-sized SIGABA. These fixtures have two static index rotors, small alphabets, synthetic wirings, different pulse contacts/collector and a toy notch. Real adaptation requires the 26-symbol/five-index-rotor reachable domain, real contacts/timing, existing external known-answer checks and a separately frozen real-sized synthetic resource protocol. The existing actual-K4 negatives retain their old finite scope; this batch adds no actual K4 keys or plaintext evidence.

The remaining computational work is the continuous coupled control/index branch relation and its dense domain operations. Translation removes repeated zero-offset predicate construction but does not eliminate that domain. Exact factorized rotor relations or symbolic shared-controller constraints are justified algorithmic avenues; neither has passed a completeness/scaling gate here. No budget is extended. A real-sized adapter, external-reference replay and separately frozen synthetic benchmark are required before K4.

K4 remains unsolved. No extrapolation from a synthetic planted key, no claim of exhaustive SIGABA exclusion and no automatic real K4 run follows from this optimization.

The largest run makes 158 zero-offset predicate builds, 10,073,234 exact translations, 10,059,023 cache evictions and 77,394,917 branch visits. These measured counters identify remaining repeated translation/cache work and coupled branch volume; they are not a time profiler. The immediate next deliverable is a separately frozen authentic real-sized synthetic adapter and validation protocol, rather than another toy budget increase.
