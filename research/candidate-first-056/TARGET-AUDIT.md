# Study 056 — independent bounded target audit

## Result: PASS audit; UNSAT_COMPLETE target

The authorized S evaluation and separately written full-route reference were each executed **exactly once** after the additive target freeze. Both completed and returned **zero compatible raw descriptions, zero canonical operators and zero plaintexts**. S completed all 28 width/period cells; the independent reference exhaustively checked **2,862,720 complete route/nominal-period trials**. Full keys were inferred exactly from the 24 clues, not restricted to words or sampled: the contiguous 13-letter clue block covers every allowed residue. The independent complete solution sets agree.

**This excludes only the frozen family:** standard A–Z additive periodic Vigenère at plaintext indices with phase zero, followed by row-filled, unpadded, top-to-bottom keyed columnar transposition, widths 6–9, nominal periods 2–8, every column emission order and unrestricted key letters. It does not exclude other widths, periods, alphabets, stage orders, padding, additional transformations or wider classical compositions. It is not a solution of K4 and is not a claim about the historical construction beyond this bounded exclusion. No widening, tuning, retries or additional target methods followed.

## Input integrity — PASS

The 97-symbol ciphertext was independently fetched from the [pinned repository data file](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/data/k4.json), Git blob `361714e4d9b19393bcc89df59e73d1c0522eeedb`. Its exact 308-byte JSON hash is `08a1a84bd0dddf2449a2c7f67ee770d093ed47f6ad9a795630b77a2c8062f241`; the literal ciphertext hash is `eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab`, also matching the parent's separately pinned earlier record.

All 97 symbols were cross-checked against Table 1 of Richard Bean's primary research paper; the two 24-letter known-plaintext mappings were cross-checked against section 2.4. The numeric loader was independently verified to encode EASTNORTHEAST at zero-based indices 21–33 and BERLINCLOCK at 63–73, without off-by-one shifts. [Bean, *Cryptodiagnosis of “Kryptos K4”*, HistoCrypt 2021](https://ecp.ep.liu.se/index.php/histocrypt/article/download/153/109/52).

## Frozen authority and execution chronology — PASS

The parent explicitly authorized this target stage only after the fresh replacement benchmark passed its required independent review. The additive manifest was committed before either evaluation, at 2026-10-31 03:03:20 UTC:

`99e92e5c6efb8dbac992081ed0621313a5963973bf33a764713928c24b58a6c7`

All 18 dependencies were independently verified at 03:03:33 UTC, with neither result present. They pin the unchanged S solver, corrected resource supervisor, canonical input, exact clues, S-once loader and the independent reference prefreeze. The latter is `45345b752810b6f44bf36ede293decdd1aeb164fe28b8f6454bd8e4a72c5c77d`; the direct-route reference itself was written and hashed before the held-out benchmark, well before any target input was read.

Both wrappers refuse a second evaluation/output overwrite. After completion, all combined and independent frozen dependencies were rechecked unchanged.

- S output hash: `6c4edb86ab199c682fbeb4ee98e255a0b40a2372b8e8167b9e9c78f2553500c6`.
- Independent reference output hash: `0c1a5982298b6095ca4c23da6689ad19277ff389a92a885b6b5ec37ed3e1a529`.

## Resources — PASS

Both once-only calls used the independently tested corrected supervisor: exactly one worker plus one persistent engine; 1 GiB hard address-space limit for each, a hard additive 2 GiB bound; CPU hard-limit partition 2 s + 16 s and a 20 s aggregate completion check. Both had positive live-child/RSS samples, exact waited CPU, zero failures and no orphan reserve.

| Call | Inclusive CPU | Conservative measured pair peak upper bound |
|---|---:|---:|
| S once | 0.055047297 s | 28,049,408 bytes |
| Independent full-route reference once | 0.112906117 s | 19,660,800 bytes |

All limits were met. The target auditor conservatively charges **10 CPU seconds total**, including the measured 0.112906117-second reference and unmetered source checks, wrappers and reporting. The S call is charged separately by the execution worker; do not add the reference a second time.

## Preserved methodological conclusions

The fresh 256-case benchmark independently established a 17.327× inclusive-CPU S/E speed ratio and passed correctness, completion, identifiability and uniform-reference calibration. It did **not** establish learning benefit: L/S was 1.00236× with a confidence interval spanning 1, with only two qualifying reuses in one fixture. It also did not establish S superiority over ordinary prefix propagation P. The target exclusion does not change or erase those negative methodological findings.

## Artifacts

- `target-audit.json`: machine-readable complete-set, input, freeze and resource verification.
- `reference-once.json`: complete independent reference result and resource receipt.
- `canonical-input-verification.json`, `canonical-k4.json`: independent input receipt and exact pinned bytes.
- `reference-prefreeze.json`, `target-freeze-verification.json`: pre-evaluation commitments.
- `run_reference_once.py`, `target_reference_worker.py`: additive once-only verifier wrappers.
- Primary S result: `/workspace/shared/candidate-first-056/target/results/S-once.json`.

The authorized experiment and independent verification are finished. No further search is implied by this report.

## Final all-study budget reconciliation

The final cumulative ledger was independently summed and reconciled: **1,490.148355917 charged CPU seconds (24.84 minutes)** across original development, both holdouts, all resource-recovery probes, independent audits, target calls and conservative reporting/packaging reserves, versus the shared **28,800-second** cap. Auditor charges are included once; the target reference is inside the target-audit reserve. The original memory-monitor limitation remains explicit, while replacement and target aggregate resource receipts pass. See `FINAL-RESOURCE-RECONCILIATION.json` in the audit root and `candidate-first-056/audit/final-resource-ledger.json`.
