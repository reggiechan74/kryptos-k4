# Study 055 target — independent audit

## Decision

**Verification PASS; target screen not survived.** The independently confirmed outcome is **NO DIRECT-ENGLISH-KEY CONTINUATION UNDER THIS SCREEN**. No convention survives the unchanged threshold. This is the protocol’s narrow stop result, not a proof that all English running keys are impossible.

This stage was authorized by the parent only after the separately completed 17/17 calibration admission and external replay. The calibration report remains unchanged in `AUDIT_REPORT.md`. The additive target-stage freeze was issued before target scoring. Original model, core arithmetic, threshold, fixtures and calibration hashes remain unchanged.

## Verified result

Threshold: **-4.385648037504633 bits/letter**. Best convention: **AZ-KR-variant_beaufort**. Maximum score: **-7.992896749427596**; maximum margin: **-3.607248711922963**. All margins are below zero.

| Convention | Score (bits/letter) | Score − threshold | Survives |
|---|---:|---:|---|
| AZ-AZ-vigenere | -10.070059854 | -5.684411817 | No |
| AZ-AZ-beaufort | -9.214748165 | -4.829100128 | No |
| AZ-AZ-variant_beaufort | -11.098893782 | -6.713245744 | No |
| AZ-KR-vigenere | -9.367218980 | -4.981570943 | No |
| AZ-KR-beaufort | -9.021258870 | -4.635610832 | No |
| AZ-KR-variant_beaufort | -7.992896749 | -3.607248712 | No |
| KR-AZ-vigenere | -9.146597536 | -4.760949499 | No |
| KR-AZ-beaufort | -11.875352076 | -7.489704039 | No |
| KR-AZ-variant_beaufort | -9.128419525 | -4.742771488 | No |
| KR-KR-vigenere | -8.414195562 | -4.028547525 | No |
| KR-KR-beaufort | -9.791699588 | -5.406051551 | No |
| KR-KR-variant_beaufort | -10.713466753 | -6.327818716 | No |

## Verification scope

- Reviewed the additive primary orchestration and separately frozen independent target script before running verification. The independent script imports the unchanged independent inverse/scorer, not the primary target module.
- Executed **one independent repeat**, computing exactly 12 target scores, after exactly one primary 12-tableau evaluation. No third numerical target run was performed.
- Checked the authorization, all calibration and target-stage dependency hashes, actual 97-letter ciphertext checksum, fixed crib coordinates, all 12 original 054 fragment pairs, all 12 scores/margins/survival flags, the best convention, maximum, and exact outcome.
- Maximum primary/independent score difference: **3.55e-15 bits/letter**, below the frozen 1e-10 tolerance.
- Checked every saved per-tableau and overall-max reference comparison using a separate rank-count implementation. Post-run recheck confirms all 314 original frozen inputs and every additive target-stage dependency still match.

## Reference comparison semantics

The target maximum is below **every held-out true-key positive score**: 100/100 in each of archaic, fiction and nonfiction, and every fixture in each source group. It is also below every positive-case maximum in every stratum for **all 12 generating conventions**. True-key distributions remain labeled separately from the 12-way-max distributions; no favorable generating convention was selected.

For the **overall target maximum**, 86/200 independent uniform-case maxima are at least as high. The prescribed uniform-reference upper-tail rank is **(1 + 86) / 201 = 0.43283582089552236**. This is neither a probability that English is impossible nor a probability that K4 is solved. Per-tableau comparisons against uniform maxima are separately labeled descriptive comparisons; the overall max comparison is the multiplicity-aware case statistic.

All calibration limitations remain: few archaic source groups, correlated source windows, narrow authentic stress coverage, arbitrary-substring local scoring, no inference about syntax or the 29-letter bridge, and no global project-wide error guarantee.

## Budget and stopping

The independent target repeat used **0.236567 CPU seconds** including process overhead, with **55,664,640 bytes** peak RSS. Recorded study total immediately afterward is **120.880420 CPU seconds**, comfortably within the 3,600-second cap. The largest recorded study peak remains below 8 GB.

**Stop study 055 here.** No decoder, larger source hunt, changed alphabet/key labels, new model, relaxed threshold, or revised hypothesis is implied or authorized by this negative screen. No GitHub or Site mutation was performed by this audit.

## Artifacts

Primary directory: `/workspace/shared/candidate-first-055/`

- `results/target_result.json` — primary outcome and all scores/ranks.
- `results/independent_target.json` — the one independently repeated target calculation and all verification results.
- `results/execution/13-target-independent.json` — automatically aggregated compute receipt.
- `target_stage_freeze.json`, `target_authorization.json` — additive stage freeze and authority.
- `independent_target.py` — reviewed independent target orchestration.

External audit directory: `/workspace/shared/candidate-first-055-audit/`

- `TARGET_AUDIT_REPORT.md` — this target-stage report.
- `target_postrun_integrity.json` — post-run hash verification; no additional target scoring.

| Artifact | SHA-256 |
|---|---|
| `freeze.json` | `489d519d2d507d3104433f2e8ca55fa5fd96e3f066233ea39a4f60a8e9fcf324` |
| `threshold.json` | `e87318170f134d2679463a0f6a9401f16ff274d453850246e476870e4e606b1f` |
| `target_stage_freeze.json` | `ed1108abce0a19af37eaf153550b59fffd7779b996c275a479bac0de28994540` |
| `results/target_result.json` | `d8a1525fc76722fa8592d74e242fca6a6c4d02c3655b930c4c6f007ab0d1d03d` |
| `results/independent_target.json` | `6e6122e32a90ca4ee90ba35b9e95d60a992a354c90f3855fa684344bbd787eb4` |
| `independent_target.py` | `82eb4a589b88f02ae08e428e4645169af5b2cedbc71b901d1a1ee116e7167c59` |
