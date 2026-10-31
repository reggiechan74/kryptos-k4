# Study 059 — short-primer autokey before free column order

## Result and exact boundary

Both the production solver and the independently written exhaustive reference returned **UNSAT_COMPLETE** for K4: no compatible primer cylinder or plaintext in the frozen domain. The reference completed **52,346,880 route/length/convention/feedback trials**. These are descriptive trials, not a count of distinct encryption operators.

The family uses 97 letters, widths 6–9, all physical column emission orders, top-down reads and no padding. Plaintext alphabet A and intermediate-ciphertext alphabet B independently use ordinary A–Z or KRYPTOSABCDEFGHIJLMNQUVWXZ. Sign s is ±1. Write x_i=index_A(P_i) and y_i=index_B(D_i). An arbitrary numeric primer z has length L=1–8. Initially y_i=s*x_i+z_i modulo 26. Thereafter use either y_i=s*x_i+x_(i−L) (plaintext feedback) or y_i=s*x_i+y_(i−L) (intermediate-ciphertext feedback). Transpose D only after this calculation.

**The feedback coefficient is +1 only.** Subtractive feedback y=x−feedback is a distinct untested extension, not a primer-negation alias. This boundary was explicitly reviewed before freeze. No backward feedback, output-ciphertext feedback, extra resets, other lags/widths/alphabets, additional layers, errors or language inference were introduced. A completed bounded pilot does not eliminate the broad autokey family.

## Why ambiguity was retained

For a fixed route, plaintext feedback makes every plaintext chain affine in one primer symbol with coefficient ±1. The 13 consecutive crib positions cover every residue for L≤8, fixing all primer slots. In ciphertext feedback, later plaintext is s*(y_i−y_(i−L)), independently of the primer. Because all public clues occur after every tested primer length, **all L primer symbols remain free**. A single compatible L=8 cylinder would contain 26^8 = 208,827,064,576 distinct plaintexts differing in their initial positions.

We therefore tested exact feasibility and ambiguity, not universal unique recovery. Free symbols were represented explicitly, never filled using preferred English. A nonempty cylinder with any free symbol guarantees multiple plaintexts; otherwise complete fixed plaintexts are compared. Cylinder volumes can overlap, so their sum is only an upper bound. Exact distinct operator counts are withheld. Periodic-study per-position substitution maps are not valid equivalence signatures for coupled feedback.

The target has no cylinders at all, so its empty result does not depend on choosing among ambiguous candidates.

## Validation and blind controls

- Independent tiny proof: all 256 four-symbol ciphertexts of length four under three masks, yielding **768 cases and 207,120 fully expanded witnesses**. Production, independent reference and brute-force all-primer sets agree exactly, including empty/unique/multiple projection. The earlier smaller proof receipt is preserved; its original development script was not separately retained.
- Additional **64 full-alphabet cases** cover all conventions and feedback modes with low/high widths and lags, with complete production/reference agreement and independent re-encryption.
- Blind **600 inputs**: one plant in each of 512 convention/feedback/width/lag cells, balanced as 256 uniform and 256 literal-clue cases; 32 zero/repeated-primer diagnostics; 56 independent random-ciphertext controls. No filtering by solvability, ambiguity or speed.
- All **600** runs completed with identical symbolic cylinder sets and projected classifications.
- All **544/544** planted descriptions were included in their cylinders.
- All **272/272** ciphertext-feedback plants were correctly classified MULTIPLE.
- **0/56** random controls had any compatible cylinder. This is an operational check, not a project-wide false-positive guarantee.
- Descriptive plaintext-feedback unique recovery: **127/128 uniform**, **128/128 literal**, and **16/16 diagnostic** plants. One ambiguous uniform case is retained. All ciphertext-feedback cases remain ambiguous as required by the model.
- Independent audit replayed fixture generation, verified all frozen files and pre-answer output seals, checked **817** representative/free-slot re-encryptions, and confirmed **31,408,128,000** exhaustive reference trials across the benchmark.

The noncrib plaintexts are synthetic uniform letters. These tests demonstrate exact finite-model feasibility and ambiguity behavior, not natural-English inference or the historical likelihood of this mechanism.

## Reproducibility and resources

Final freeze SHA256: adbc136d4ff19a27c448b0bff5e00672c7246b246a6d8441e7a0fb0bc4519c68 (29 files). Inputs were generated once afterward by the independent author. Both result files were sealed at 2026-10-31T13:00:56.363936UTC before answer analysis. Parent reviewed the independent benchmark audit before approving the target stage at 13:02UTC. Additive target freeze SHA256: 242c9739acd86f03f17daf2ed1d0834a4e8b2ff6c2cdf42435df8fb4a009274e.

Production uses necessary partial column-placement constraints and exact primer inference. Independent reference builds literal ragged matrices and tests every descriptive case. Its original and pre-freeze optimized implementations are preserved. The safe direct-crib filter improved development reference runtime without changing its exhaustive sets. No post-blind code, gates or fixtures changed.

Benchmark inclusive CPU: **8.673382187 seconds production**, **1,376.747787377 seconds reference**. Target inclusive CPU: **0.012087199 seconds production**, **1.975588367 seconds reference**. The reference's enumeration cost is verification work, not a production-search bottleneck. No new speedup claim is inferred from this comparison.

Each worker and child had a 1 GiB address-space cap, one child at a time; benchmark conservative combined RSS peaked at 21,020,672 bytes. The shared resource ledger includes a conservative 600-CPU-second preparation reserve and rounded audit/closeout charges, remaining far below the 8-CPU-hour cap. Failed runs would have been retained and charged; none occurred. No paid service, checker submission, new software installation or Site change was used.

## Coverage and next actions

These feedback operators have genuine multi-input dependencies, unlike the one-input-coordinate periodic/permutation operators of 050/057/058. The allowed columnar routes also differ from direct causal aligned autokey: their second output retains dependence on a plaintext coordinate at least six, while direct causal second output cannot depend on future coordinates. This is a local coverage distinction, not a worldwide novelty claim or an exact operator census.

Close Q-03 only for the frozen +1-feedback pilot. Retain subtractive feedback and other excluded settings as untested rather than extending after failure.

- **Q-04 stochastic search: not run; prerequisite not established.** Production already completes the tested domain rapidly. Slow independent exhaustive verification is not a reason to replace a sound exact solver with a heuristic.
- **Q-05 neural ranking: not run; prerequisite not established.** No compatible K4 candidates remain in these tested families, so there is no candidate-ranking bottleneck to solve. A language scorer cannot repair an exact contradiction.

The ledger and experiment log must record these distinctions before any new research scope is selected. Neither conditional pilot is marked completed or scientifically disproved.
