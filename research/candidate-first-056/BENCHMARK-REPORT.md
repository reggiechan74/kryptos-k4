# Study 056 — resource-corrected blinded benchmark

## Outcome

**The frozen shared-constraint method passed the numerical admission gates and the corrected resource checks. Dynamic learned conflicts did not show a useful advantage. No actual K4 ciphertext was loaded or evaluated.**

The selected nonlearning placement solver S was **17.33× faster** than the fair complete-route baseline on fully inclusive CPU time (paired-bootstrap 95% interval **17.13–17.52×**). All four methods completed every case and agreed exactly. Ordinary prefix propagation P performed essentially the same as S; this is not evidence that learned machinery or the CSP representation uniquely caused the gain.

The fresh benchmark follows a disclosed resource-only correction. The original run remains preserved one directory above, with its failed aggregate-watchdog assumption and all original commitments. Neither its algorithms nor its outcomes were silently replaced. The replacement uses a fresh independent seed namespace and unchanged cipher family, solvers, fixture rules, selected method and numerical gates.

## Exact results

| Stratum | Cases | Unique plaintext | Ambiguous | Complete UNSAT |
|---|---:|---:|---:|---:|
| Uniform positives U | 28 | 28 | 0 | 0 |
| Repeated-symbol positives R | 28 | 27 | 1 | 0 |
| Relabelled literal-pattern positives J | 28 | 27 | 1 | 0 |
| Literal-pattern positives L | 28 | 28 | 0 | 0 |
| Alias positives | 8 | 8 | 0 | 0 |
| Constant-crib degeneracy positives | 8 | 2 | 6 | 0 |
| Independent uniform-ciphertext controls | 56 | 0 | 0 | 56 |
| One-symbol corruption diagnostics | 56 | 49 | 0 | 7 |
| Outside-model generators | 16 | 0 | 0 | 16 |
| **Total** | **256** | **169** | **8** | **79** |

Every one of the **128 in-family planted operators and full plaintexts** was included. Ordinary/equality/literal recovery was **83/84 unique** (exact 95% binomial interval **93.54%–99.97%**), exceeding the frozen 80/84 threshold. All **28/28 literal-pattern fixtures** were uniquely recovered (interval **87.66%–100%**), exceeding 26/28.

All 56 independent uniform-ciphertext controls were UNSAT. The exact two-sided 95% upper bound for their compatible-fit rate is **6.38%**, not zero risk and not a project-wide p-value. All 16 outside-model generator samples were also UNSAT; those labels were not assumed negative before exact solving.

The 49 corruption cases whose changed ciphertext positions mapped from noncrib plaintext positions retained the original operator and their one-letter-modified plaintexts. Every guaranteed witness was recovered. The remaining seven mapped from crib positions and were UNSAT in this sample. These controls measure sensitivity/correctness, not a low false-fit rate.

All 169 unique plaintext results also had one canonical operator. Nominal key-period aliases are counted separately. The eight ambiguous cases have two explicit unequal plaintext witnesses and complete forced-position masks in `audit/ambiguity-witnesses.json` and the per-case results. Guaranteed 12- and 48-plaintext symmetry cases are not mislabelled unique.

## Family, baseline and ablations

The only family tested is standard A–Z periodic Vigenere followed by unpadded row-filled ragged columnar transposition, widths **6–9**, nominal periods **2–8**, arbitrary bounded seed and unknown column emission order. Every solve receives only 97 ciphertext symbols and 24 position/literal clues; it searches all 28 width/period cells.

E infers unrestricted key residues after completing each route; it does not brute-force 26-to-the-period seeds. There are **2,862,720 nominal route/period trials per fixture**. P propagates key constraints during prefix construction. S uses exact placement arc consistency. L adds sound, independently verified dynamic failed-decision clauses to precisely the same CSP/order as S.

| Method | Mean inclusive CPU per complete solve | Complete | Paired speedup over E |
|---|---:|---:|---:|
| E — complete routes | 61.799 ms | 256/256 | 1× |
| P — prefix propagation | 3.592 ms | 256/256 | 17.314× |
| S — placement CSP, no learning | 3.581 ms | 256/256 | **17.327×** |
| L — same CSP plus learning | 3.577 ms | 256/256 | 17.368× |

The preregistered selected method remains **S**. The recovery did not reselect it or tune any solver after seeing original outcomes.

L/S speedup was **1.002×**, with interval **0.988–1.016×**, failing the required 1.20× and lower-bound >1.00. L learned nine sound clauses; three later hits reused two distinct modular clauses across one fixture, below the required 50 clauses across 10 fixtures. S and L visited exactly the same **7,307 states**. L performed 496,229 support checks versus S's 492,004, including proof work. **The learning-benefit claim fails.**

P/S was 1.001× with interval 0.987–1.015×. Thus the main speed gain is explained by early constraint propagation; this pilot does not establish an extra performance benefit of S over simpler P.

## Frozen gate results

| Gate | Frozen requirement | Result |
|---|---|---|
| Correctness | Zero missing/extra solutions or unsound exclusions | Pass; independent full-union replay |
| Completion | S 256/256; E at least 244/256 | Pass; all methods 256/256 |
| Identifiability | At least 80/84 and 26/28 literal | Pass; 83/84 and 28/28 |
| Representation/propagation value | Speedup ≥2; bootstrap lower >1.25 | Pass; 17.327, lower 17.133 |
| Learning-specific claim | Speedup ≥1.2, lower >1; 50 modular reuses/10 fixtures | **Fail**; 1.002, lower 0.988; 2/1 |
| Independent uniform false fits | At most 1/56 unique compatible | Pass; 0/56 compatible |
| Corrected resources | Complete within 20 CPU seconds and 2 GiB per batch | Pass; 1,024 verified complete batches |

Failure of the learning-specific claim is separate from nonlearning method admission. A passing synthetic experiment does not establish historical applicability and does not itself authorize target work; parent review remains the stopping point of this implementation task.

## Resource repair and accounting

The original cloud runtime lacks `/proc/PID/task/PID/children`. The original monitor returned zero rather than traversing the tree. That defect was disclosed after the first output seal; the original outcome is retained as resource-certification-limited.

The independently validated replacement launches exactly one worker and one persistent solver per batch, each with a **hard 1 GiB address-space limit**, giving a hard additive 2 GiB bound. Known PIDs are communicated through a pipe and verified with available `/proc/PID/stat` data. The worker and solver have conservative hard CPU allocations of 2 and 16 seconds. Every abnormal path cleans up its process group and conservatively charges possible unreaped CPU; unverified cleanup aborts the benchmark.

Every replacement batch completed normally. All **1,024 receipts** have positive monitoring, at least two live-child observations and exact waited accounting. The largest measured batch used **1.734 CPU seconds**, below 20. The largest conservative worker-plus-solver peak upper bound was **29,097,984 bytes (27.75 MiB)**, below 2 GiB. There were no resource failures or orphan-CPU reserves in the actual replacement run.

Primary timing includes all worker startup/import, solver preprocessing/search, serialization, driver parsing, canonical projection on every repetition, and parent monitoring CPU. Each method/fixture uses the same fixed 20 repetitions without warmup. All timeouts would be censored INCONCLUSIVE; none occurred. The original inner timing is retained only as a descriptive field, not used for the primary replacement claim.

The replacement consumed **372.289 CPU seconds** and **355.655 wall seconds**. The original run, every preserved development pass, all resource-recovery probes, independent reviews and packaging are charged together in the final ledger under the original eight CPU-hour budget. No paid compute, package installation, settings change, publication or repository/Site mutation occurred.

## Independent verification

The same immutable solver passed main and rectangular tiny suites covering binary/ternary alphabets, ragged and rectangular geometry, empty/partial/full clues and free key residues:

- **288,363 fixtures; 1,153,452 solver calls.**
- **2,277,336 independent witness re-encryptions.**
- **24,780 learned clauses** checked against **697,472 concrete premise-containing completions**.
- **3,040 tiny cross-branch reuse receipts** verified; these establish mechanism soundness, not held-out benefit.

For the fresh holdout, the independent matrix oracle verified **1,600 returned witnesses**, all nominal aliases and **5,120 projection comparisons**. Both learned-clause validity and reuse provenance were checked independently. Fresh-seed replay reproduced input and answer manifests byte for byte. A separate parent reference enumerates every route/period directly, independently of production placement routines.

## Commitments and artifacts

| Artifact | SHA-256 |
|---|---|
| Unchanged protocol v2 | `58cf2196845555b7355f7b6c7f59b11033c462832ad7c1e9ceff79a1ad61d6ea` |
| Original limited-run freeze | `19e2fb273d88a97d15223773b03920ea3aa1585cb21854564bd18372fc3d1410` |
| Replacement freeze | `5eba2499c0a05408330e885c0ba163831c28632655eaf0aa1f787c81dd09d231` |
| Unchanged solver source | `625739e4d4e5a4e0052de4069563319b1a0c13e7b1c82cb0cf2751c09f657573` |
| Unchanged executable | `e9f86df41dec1f3e8289d9e04d8c3faaf80a79ff8ea5188b38ce136bd7bb6b65` |
| Fresh input | `18f2dcd6ca76c1b1882c6b908aa135776b55d736d7388962b71ac4d3d59c9780` |
| Withheld answer commitment | `c3af4afd48fc38b1565f0ec249bb5323896329a990d50c89447a563d9d954a9b` |
| Fresh output hash manifest | `3ca7242d0b940359c4d984e0f88c270ddf443a4ccb8fb2dd24cc53b61dd987fd` |

All 40 public frozen files were reverified unchanged after the run. Private answer/seed bytes were withheld until outputs and timings were sealed. Full per-case outputs, all repetitions, first-witness timings, completed-set timings, aliases, plaintext projections and resource receipts are in `results/`; reproducible source and audit programs accompany them.

The novelty certificate proves at least 408,946 routes lie outside the inspected Study 050 permutation projection, independently of target ciphertext. Earlier arbitrary-key elimination and fixed-route propagation are acknowledged prior work, not claimed as new.

**Stop state: benchmark completed; no actual target run or exclusion. Independent parent review decides any later bounded target experiment. No wider cipher family or new study has been started.**
