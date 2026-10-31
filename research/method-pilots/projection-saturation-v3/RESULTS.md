# Fresh synthetic projection-saturation v3 holdout — validated

**Correctness PASS:** all 480 outputs matched the independent complete maximal-support oracle; 47,412 original-coordinate per-value witnesses and 78 certificates verified.

Exactly one fresh 256-bit draw, 40 fixed cases and 480 interleaved runs (four arms, three repetitions). This is a synthetic conditional-model test, not a K4 run. Original sources were frozen before drawing; truth was released only after independently checking all output/resource and post-run seals. Custody was operational on a shared filesystem, not access-control blindness.

## Primary charged timing

Sums of paired case-median CPU seconds, not median speedups. Child costs include interpreter startup/import and final output serialization/write; stage costs additionally include the bounded supervisor. Wins count strictly lower on-cost and do not establish statistical significance.

| Method / stratum | Cases | Child off → on (s) | Stage off → on (s) | Stage wins / losses / ties | Stage change |
| --- | ---: | ---: | ---: | ---: | ---: |
| crt / ALL | 40 | 23.033117 → 12.093043 | 24.405472 → 13.323356 | 26 / 14 / 0 | -45.41% |
| crt / IN_FAMILY_PLANTED | 32 | 18.409414 → 11.314601 | 19.528980 → 12.307992 | 18 / 14 / 0 | -36.98% |
| crt / ordinary | 16 | 3.581647 → 3.563148 | 4.125996 → 4.071382 | 6 / 10 / 0 | -1.32% |
| crt / constant | 3 | 5.098191 → 0.148081 | 5.186135 → 0.232424 | 3 / 0 / 0 | -95.52% |
| crt / periodic | 3 | 2.755826 → 0.159008 | 2.848356 → 0.242725 | 3 / 0 / 0 | -91.48% |
| crt / binary | 3 | 0.840513 → 0.655681 | 0.932181 → 0.756346 | 2 / 1 / 0 | -18.86% |
| crt / even | 3 | 0.669815 → 0.687164 | 0.804240 → 0.767497 | 2 / 1 / 0 | -4.57% |
| crt / zero-law | 4 | 5.463422 → 6.101519 | 5.632072 → 6.237618 | 2 / 2 / 0 | +10.75% |
| crt / contradiction | 4 | 0.850453 → 0.136865 | 0.969235 → 0.249705 | 4 / 0 / 0 | -74.24% |
| crt / misspecified | 4 | 3.773250 → 0.641577 | 3.907257 → 0.765659 | 4 / 0 / 0 | -80.40% |
| parity / ALL | 40 | 14.894970 → 7.814372 | 16.280120 → 9.048368 | 30 / 10 / 0 | -44.42% |
| parity / IN_FAMILY_PLANTED | 32 | 12.014757 → 7.161512 | 13.163353 → 8.153538 | 23 / 9 / 0 | -38.06% |
| parity / ordinary | 16 | 1.713213 → 1.771667 | 2.288478 → 2.269379 | 10 / 6 / 0 | -0.83% |
| parity / constant | 3 | 2.861357 → 0.222872 | 2.982798 → 0.311053 | 3 / 0 / 0 | -89.57% |
| parity / periodic | 3 | 1.721140 → 0.184706 | 1.812105 → 0.274634 | 3 / 0 / 0 | -84.84% |
| parity / binary | 3 | 0.905670 → 0.487762 | 1.002099 → 0.578233 | 2 / 1 / 0 | -42.30% |
| parity / even | 3 | 0.638784 → 0.622530 | 0.742151 → 0.708222 | 2 / 1 / 0 | -4.57% |
| parity / zero-law | 4 | 4.174593 → 3.871975 | 4.335722 → 4.012017 | 3 / 1 / 0 | -7.47% |
| parity / contradiction | 4 | 0.629157 → 0.158934 | 0.743443 → 0.286203 | 4 / 0 / 0 | -61.50% |
| parity / misspecified | 4 | 2.251056 → 0.493926 | 2.373324 → 0.608627 | 3 / 1 / 0 | -74.36% |

## Status rates

| Method | Saturation arm | Enumerated | Saturated | Dense UNSAT |
| --- | --- | ---: | ---: | ---: |
| crt | off | 120/120 | 0/120 | 0/120 |
| crt | on | 81/120 | 27/120 | 12/120 |
| parity | off | 120/120 | 0/120 | 0/120 |
| parity | on | 81/120 | 27/120 | 12/120 |

Each case has three deterministic-status repetitions. Detailed rates by stratum, all paired distributions, component totals, support counts, process RSS and three-repeat spreads are in `descriptive-results.json` and the frozen analysis. No failed/capped stage was dropped.

## Regression distribution

Paired **on minus off** charged-stage CPU across case medians; negative is faster. Percent distributions retain small-baseline sensitivity.

| Method / group | Min (s) | Q25 (s) | Median (s) | Q75 (s) | Max (s) | Median change | Worst change |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| crt / ALL | -2.314749 | -0.236404 | -0.028408 | +0.011309 | +0.989980 | -10.45% | +79.65% |
| crt / IN_FAMILY_PLANTED | -2.314749 | -0.153624 | -0.015883 | +0.016592 | +0.989980 | -6.34% | +79.65% |
| crt / ordinary | -0.236056 | -0.014147 | +0.012769 | +0.028298 | +0.122717 | +5.00% | +79.65% |
| parity / ALL | -1.156255 | -0.228903 | -0.022491 | -0.000283 | +0.162610 | -6.98% | +35.40% |
| parity / IN_FAMILY_PLANTED | -1.156255 | -0.228903 | -0.006961 | +0.002572 | +0.162610 | -5.06% | +35.40% |
| parity / ordinary | -0.054644 | -0.006082 | -0.001962 | +0.012116 | +0.029973 | -1.60% | +35.40% |

## Conditional correctness and dependent twins

The 32 in-family planted cases had 0 wrong forced unknowns and 0 hidden truths outside the exact masks. Four contradiction controls were correctly infeasible. The four dependent twins change a hidden response without changing solver input; they are not independent recovery evidence.

| Dependent twin | Source case | Forced unknowns | Wrong forced unknowns | Hidden truth excluded by mask |
| --- | --- | ---: | ---: | ---: |
| ordinary-w0-0-misspecified-twin | ordinary-w0-0 | 67 | 1 | 1 |
| ordinary-w3-0-misspecified-twin | ordinary-w3-0 | 67 | 1 | 1 |
| constant-0-misspecified-twin | constant-0 | 67 | 1 | 1 |
| periodic-0-misspecified-twin | periodic-0 | 67 | 1 | 1 |

Wrong positions/true values/allowed values are retained in the JSON. Exact conditional marginals do not certify the true model, uniqueness of the law, Cartesian joint compatibility, or unmodeled positions 0–5.

## Interpretation

Retain saturation as an **optional, default-off tactic**, not a universal optimization or a recovery improvement. Describe benefits only for the measured strata and retain all overhead regressions. Aggregate numbers come from a deliberately structured mixture, not a representative workload estimate. Three repeats and small clock-quantized differences do not establish robust per-case speedups. This result does not admit a K4 target run or standalone-repository novelty claim.

## Reproduction and custody

`PROPOSED-FREEZE-MANIFEST.json` SHA256 `cdc5c7db8df5775817798653daa82f756a7dbdc7e41058884abd7e7e53b65b41`; `ANALYSIS-MANIFEST.json` SHA256 `4dea59eddf446019f8130cb3d8c66f2dff95e42dc33e8391d03d89fcd778be06`. Source, solver input, schedule, custody commitment, all raw results/receipts, release gate and frozen analysis are retained. No redraw, auto-resume or method correction occurred. See `RESOURCE-ACCOUNTING.json` for inclusive CPU accounting without descendant double-counting.
