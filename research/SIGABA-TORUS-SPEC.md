# SIGABA-TORUS-013: exact predicate translation and compact verification

23 October 2026. Frozen before implementation/outcomes. Engineering only, no actual K4 ciphertext. Baseline main: `9840d8af781dc7291683267106f49223959117e7`.

## Unchanged experiment

Keep all thirteen cases, synthetic wirings/messages/planted keys, observation masks, reachable index maps, carry timing, merge rules and output-before-step conventions from SIGABA-JOINT-TOY-012. The fixture file SHA-256 is `2ad409cafff033932a79f4aa45e3f7ac557833e540b0902bef721da4f9d03b9a`. No fixture easing, added observations or real-machine key sample. Maintain 600 seconds and 1 GiB measured RSS per separate benchmark process, 64 MiB accounted cache and 256 MiB temporary output streams. Keep incomplete, incompatible and compatible classifications separate.

## Exact optimization

For initial cipher positions s, accumulated offsets delta and fixed rotor contacts, encryption at that time depends only on s+delta coordinatewise modulo q. Therefore the one-observation domain satisfies `D_delta(p,c)={s:s+delta in D_0(p,c)}`. Build only zero-offset rotor predicates, then translate their bitsets on `(Z/qZ)^r`.

Bit index is the existing lexicographic base-q encoding. For coordinate j, stride=q^(r-1-j), period=q*stride, shift=delta[j]*stride. In each period, bits at positions below shift wrap left by period-shift; the remaining bits shift right by shift. Use exact Python integers and fixed width q^r. Distinct-coordinate translations commute. A shared LRU accounts for base and translated predicates; fixed translation masks also count toward the same 64-MiB budget. A cache miss or eviction affects performance only.

Only add a backwards-compatible predicate-factory injection to the baseline solver. Its reachable-index domains, continuous controller, cipher-state filtering, correlation-preserving merge and complete relation semantics stay unchanged. Preserve baseline receipts and executed source through their original commit rather than rewriting measured results.

## Correctness before benchmark

For q=2..5,r=3 and q=2..3,r=5, compare every translated predicate for every offset and symbol pair with direct physical evaluation of every independent initial cipher start. Also compare with the old meet-in-the-middle evaluator. Verify translation on every subset in a small ring, inverse/composition properties, zero offsets, wrap boundaries and cache-disabled/evicting behavior. Keep all old coupled-set and unsafe-merge controls. Controls cap: 120 seconds / two million directly checked seed/observation combinations; a cap is unresolved, not a pass.

## Validation without truncated solutions

Cases 0..9 retain complete independent raw-key stream comparisons within the old limits. For case 10 (q=4,r=5), the pulse set is the entire alphabet, so the control-bank permutation always presents the same collector set, independently of controller positions/time. Independently enumerate every raw index setting and every cipher start once using physical schedules; extend the resulting domain identically to all controller starts. Compare complete canonical rows `(control tuple, raw index tuple, cipher-start bitset)` with the production relation, byte for byte and with exact raw-key counts. This covers every key, including all 12,582,912 prior fits, without expanding one line per key. The two-million row/256-MiB limits apply to canonical rows; this is an exact representation change, not a solution truncation or budget extension.

For other scaling cases, compare the optimized canonical relation against all completed baseline coverage (case 11 full; case 12 only its 5,080-controller completed prefix). This differential check is not independent full truth for the larger domain. Independently validate every returned raw key when expansion fits the existing cap. If output still exceeds the cap without an independently justified compact equality check, mark verification unresolved rather than weaken it.

## Gate

Record per-case total and inference time, peak RSS, base builds, translations, cache work, controller coverage, exact/partial key counts and verification strength. Compare the same fixtures with the retained baseline receipts, separating solver time from independent verification/output time. Do not infer real-size performance from a toy speed ratio. Even complete toy success still requires an authentic 26-symbol/five-index-rotor adapter and separately frozen real-sized synthetic/reference validation before any actual K4 run.
