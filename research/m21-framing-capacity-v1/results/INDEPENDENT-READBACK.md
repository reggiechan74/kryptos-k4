# Independent retained-output readback

PASS. Readback only: no encoder/DP imports or rerun, no K4 inputs.

- All 24,624 retained case rows match the frozen manifest in order, IDs and dimensions.
- All 132 indexed control rows pass.
- Every count matches the retained exhaustive oracle count; all length, witness and baseline flags pass. Length sets agree. Witness presence and length were cross-checked; witness encoding validity is the retained independent-oracle result, not a newly executed encoding check.
- Independently recomputed numeric interval and weak/strong/envelope length feasibility for every retained row. No false pruning or count mismatches.
- All ten listed frozen source/document hashes match. Supervisor exit status is 0, stderr is empty, stdout summary equals summary.json.
- Recomputed all matrix-derived aggregate counts and timing sums: 8,453 exclusions beyond weak length baseline; 1,930 beyond nonzero-prefix-guarantee baseline; 375,129 states, 761,882 transitions, 1,301,302 bit operations.
- Summary reports 4.11879517 CPU seconds, 4.12233698 wall seconds and 43,440 KiB peak RSS. These process-level measurements are consistent across retained summaries, not independently remeasured.

These are correlated synthetic case counts over twelve fixtures, not distinct cryptanalytic hypotheses, a new theorem, or evidence of 97-symbol target performance. Cached-oracle timings do not support an uncached speed comparison.
