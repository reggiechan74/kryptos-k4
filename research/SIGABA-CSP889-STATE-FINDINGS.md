# CSP-889 full cipher-state inference

23 October 2026. **No first-crib-compatible state remains** in the frozen domain. Unlike the earlier repeated-start pilot, this audit retains all five independent cipher-rotor start letters. It uses exact meet-in-the-middle constraints, not a larger random sample.

## Scope and chronology

The [protocol](SIGABA-CSP889-STATE-SPEC.md) was committed at `4ce3ca1` before implementation and K4 evaluation; implementation and successful controls were checkpointed at `fc00f8b` before the actual run. The historical CSP-889 mechanism and public simulator wiring set remain unchanged, with two fixed wheel layouts, normal orientations, control AAqAA and index rrrrr. Published simulator large-wheel wirings are not recovered wartime secret permutations. Other wheel orders/orientations and independent control/index positions remain outside coverage. The publicly known Berlin phrase is a second-stage check, not untouched evidence.

There are 520 distinct control/index/layout schedules and 26^5 possible cipher starts for each: **6,178,315,520 raw state descriptions**. The old 13,520 repeated-start descriptions are a subset. The total is not a count of independent new hypotheses, distinct encryption functions or billions of explicit full decryptions.

## Exact inference and results

For each schedule, all 676 two-wheel left starts and 17,576 three-wheel right starts are joined on the intermediate contact values for plaintext positions 22–24 and their corresponding ciphertext. Both sides include the continuously propagated step offsets from position 1. Every compatible full start appears in the join, including collisions; no unknown plaintext before a crib is guessed and no state is reset there. This is valid because the specified CSP-889 controller evolves independently of plaintext/ciphertext.

Actual work: 351,520 left-pair signature evaluations, 9,139,520 right-triple signature evaluations, and **350,311 joined full starts**. Their first mismatch after the join is:

| Position | Joined starts rejected |
| --- | ---: |
| 25 | 336,487 |
| 26 | 13,333 |
| 27 | 475 |
| 28 | 15 |
| 29 | 1 |

All 520 schedules completed within the frozen per-selector budget; none is unresolved. There are zero complete first-crib survivors, zero Berlin evaluations and zero full candidate plaintexts. The [complete per-schedule result](../results/SIGABA-CSP889-STATE-002.json) includes aliases, counts and a deterministic SHA-256 of the ordered joined-state conflict stream. The digest is a reproduction check, not by itself a proof of exhaustive coverage. Completeness follows from the Cartesian left/right decomposition and is checked independently on full finite control domains.

## Controls

- All twelve external CSP-889 vectors remain in the regression suite; the rotor implementation is unchanged.
- Sixteen complete small-ring comparisons at moduli 2, 3, 4 and 6 agree on every compatible state, not merely whether the planted state appears. Ambiguous control solutions are retained, with incompatible repeated-state mutations rejected. A separately saved JavaScript synthetic oracle agrees and was replayed on the Mac after the temporary disconnect; it is not a second independent historical implementation.
- One actual 26-symbol fixed-schedule comparison explicitly enumerates all **11,881,376** full cipher starts using a direct method. Its complete set of 648 three-letter-compatible starts exactly equals the split-path result.
- Two full 520-schedule literal-crib planted selectors recover their true independent cipher starts, and two additional fixed-schedule plants pass. Each has one compatible key/plaintext on that fixture; this is not a universal uniqueness theorem.
- Full encryption/decryption regeneration is required for any complete survivor. Controls and source hashes are saved in [the separate receipt](../results/SIGABA-CSP889-STATE-002-controls.json).

Reproduce using `python3 experiments/sigaba_state_inference.py --controls --output /tmp/csp889-state-controls.json` and `--actual --output /tmp/csp889-state-actual.json`. The production runner stops and reports budget-unresolved if a selector exceeds 180 seconds. No null significance simulation or attractive partial-text ranking was performed.

## What remains open

This strengthens exclusion of this public wiring/layout domain by removing the arbitrary repeated cipher starts. It does not establish that historical SIGABA generally fails. A tractable next machine step would need a separately frozen joint controller/index inference method or independently grounded historical key restrictions, rather than silently extending this schedule domain. The physical evidence addendum supplies real source constraints, but still no numerical bearing, lamp beam or complete screen survey. No positive K4 lead is claimed.
