# Independent final release review — PASS

2026-10-31. This review is separate from the custodian's descriptive reporting. It found **no scientific or artifact-integrity blocker to release of the completed synthetic result**. This is not a K4 result, target admission, universal speedup claim, comparative recovery improvement, novelty determination, or authorization to publish remotely.

## Independently checked

- The original source manifest SHA256 remains `cdc5c7db8df5775817798653daa82f756a7dbdc7e41058884abd7e7e53b65b41`; the analysis manifest remains `4dea59eddf446019f8130cb3d8c66f2dff95e42dc33e8391d03d89fcd778be06`. Every listed source matches its pre-draw pin. The prior implementation/protocol audit report still matches its supplied pin.
- The retained pre-draw marker, one-call draw script, 256-bit seed-byte commitment, solver-input and truth hashes, fixed schedule, release-gate chronology and post-run source/input seals are consistent. The solver input contains only IDs and instances. The released seed matches its original byte commitment. No generator was executed by this reviewer.
- All **480 raw outputs and 480 resource receipts** match the complete progress seals and frozen analysis output pins. There are **zero missing, failed, capped or silently excluded stages**, no pending in-flight reservation, and no outstanding CPU reserve. The exact 480-job schedule was independently reconstructed from the fixed schedule seed.
- All **480 masks and feasibility results** equal the frozen independent full-support oracle records. Each oracle record covers all **4,495 maximal supports**. This review did not execute a second expensive oracle: the pre-draw pinned analysis had already performed the full enumeration successfully.
- Independently revalidated all **47,412 original-coordinate per-value sparse witnesses** directly against the observation equations and advertised response, including canonical coordinates and support budget. Rechecked all **78 certificates** with the pinned independent identity verifier.
- Recomputed each paired arm's raw-receipt child/stage medians, internally checked/kernel medians and checked-time minima/maxima, phase medians, support counts and peak solver RSS. These match the frozen analysis. Independently recomputed all **32 descriptive summary groups**, including wins/losses/ties, aggregate changes, paired regression distributions, status rates and phase totals.
- Independently recomputed every hidden-truth exclusion, forced-position count and dependent-twin error. The 32 in-family planted cases have no hidden truth outside their conditional masks and no wrong forced values. Ordinary cases force 54–67 of 67 unknown positions; zero-law cases force 63–67; constant/periodic/binary/even cases each force all 67. Each of four dependent twins forces all 67 but is wrong at one changed hidden position. Four observation-contradiction controls are infeasible.

The per-case raw files and frozen analysis remain the authoritative evidence. The independently authored checker does not merely accept the custodian's aggregate tables.

## Interpretation checked against evidence

Both saturation-on methods have **9/40 SATURATED, 4/40 DENSE_UNSAT and 27/40 ENUMERATED** cases (three repetitions per case). Their off arms enumerate all 40 cases. All arms have identical exact conditional masks; there is no comparative recovery gain.

| Method | Sum of paired case-median charged-stage CPU, off → on | Strictly faster / slower cases |
| --- | ---: | ---: |
| CRT | 24.405472 → 13.323356 s | 26 / 14 |
| Parity | 16.280120 → 9.048368 s | 30 / 10 |

The approximately 45% mixture reductions are descriptive and composition-dependent. They include alias-rich strata and dependent twins. Ordinary-case aggregate stage changes are small (−1.32% CRT, −0.83% parity), while the ordinary CRT median case regresses by about 5.00%; the worst charged-stage individual regressions are +79.65% CRT and +35.40% parity. Small timing differences and three repeats do not establish robust universal speedups. The report's **optional/default-off** interpretation and retained overhead regressions are appropriate. The conditionally exact masks do not prove true model membership, a unique law, joint compatibility of arbitrary marginal choices or recovery of unmodeled positions 0–5.

## Resource accounting

The single independently authored release checker ran under the pinned bounded launcher with 10-second soft CPU / 11-second hard CPU limits and 256 MiB per process, 30-second wall timeout, and the parent-death guard. It exited successfully:

- Child CPU: **2.418576 s**.
- Supervisor CPU: **0.039932 s**.
- Inclusive checker charge: **2.458508 s**.
- Wall time: **2.426891 s**.
- Peak checker process RSS: **49,604 KiB**.

The holdout outer inclusive charge is **220.291440 CPU s**; its **211.994508 inner CPU s is included, not added again**. Frozen analysis costs **15.352397 CPU s**. Historical managed work plus new draw, release gate, summary and this checker total **253.139357 CPU s** against the 500-second control/history reserve, leaving **246.860643 s**. Total deduplicated managed experimental CPU including this review is **488.783194 s**, below the conservative 4,908-second allocation. Lightweight orchestration and file bookkeeping are not represented as exhaustively metered CPU.

## Custody and release limitations

The one-draw/noninspection history is supported by the retained script, commitments, prescribed execution and operational records. Shared-filesystem custody is **not cryptographic or access-control blindness**. This review does not claim to prove absence of all possible unrecorded access. The release gate was completed before the frozen analysis opened truth, and the immutable hashes preserve the actual draw and outputs.

No source, solver, protocol, original output or original commitment was edited during this review. Any public-path sanitization must occur in a separate copy, retain an original-to-public hash mapping and avoid misrepresenting rewritten bytes as matching original seals. Private coordination details must not be included in a public-facing bundle. Publication and remote verification remain separate steps.
