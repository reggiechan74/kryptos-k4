# C20 synthetic pilot — independent read-only outcome closeout

**PASS_SYNTHETIC_ONLY.** The sole authorized batch completed, all frozen correctness checks were reported successful, and source/receipt/result/external-completion integrity checks pass. **No K4 target is admitted, and no further execution or retry is authorized.**

## Evidence and fixed result

- Freeze: **3ecdaf1c4191a45bc37a2cb7e907f149e7ccf68c680313b6ba5b0b0ab60134c1**.
- Root grant: **d500c124505e6363106cc457dcb24c675d12b3bc4b2b6f904eb6a0fd02ba5878**.
- Result: **29d3c53ae99348bdb7c843122102f4b03f65ff8d40be008f03ab93d575e7adeb**.
- Receipt: **a4399fc88147e4fa213e71fd2e651d4510fa8aeef7f04caeba9063c488c3380e**.
- External completion: **4a8b1bf2ec4043baeb2fe192a0648cebc6127f6925b0168294a904ff5a85b51d**.
- Independent readback: `OUTCOME-READBACK.json`, SHA256 **7c46cba4a52868a6c6f7817404a44610394be8378009a077e870c1683a01bb62**.

The result reports the exact **17,349 tiny cases**: 2,047 over q=2, 9,841 over q=3, and 5,461 over q=4. The independently implemented enumerated-signature oracle agreed with production; involution and specified invariants passed. All **91 disclosed 97-letter plant/phase pairs** passed full output/inverse/re-encryption checks; each of the13 plants produced seven distinct phase ciphertexts.

The four literal directional fixtures, deliberately broken naive-queue control and non-fixed-route witness passed. Exactly16 malformed-input and12 malformed-phase requests were rejected. Fixed-point counts307, 2,005 and3,277 sum to **5,589**; these are diagnostics, not independent observations, likelihoods or cryptanalytic success scores. Trace commitments were authenticated but not recomputed by the reviewer.

## Integrity and execution review

All four source/document hashes and both pinned executable hashes remain unchanged. The root grant and exclusive ATTEMPT bind the exact freeze and one synthetic-only invocation. The inner argv and frozen outer timeout template match the source contract. Trusted actual tool history and its retained external record identify a retained launch and final completion with exit0; there was no retry. The child was reaped, stderr is empty, timeout is false and receipt error is null.

The output directory contains exactly five regular artifacts—ATTEMPT, stdout result, empty stderr, receipt and external completion—totaling **3,716 bytes**. All receipt inventory sizes/hashes match. This review did not import or run the cipher/oracle/prepared supervisor, recompute a trace, read K4, generate additional cases or change any source/result.

## Resource accounting

The one **60-second nominal pilot permission is consumed**, regardless of its much smaller observed usage. The authoritative receipt reports:

- Child OS CPU: **0.951498 seconds**.
- Cumulative supervisor sample: **0.178968 seconds**.
- Known sampled CPU components: **1.130466 seconds**.
- Wall sample: **1.102165920 seconds**; child peak RSS: **45,716 KiB**.

The child's internal0.875572741-second timer is a subset and is not added again. All reported acceptance bounds hold. Receipt serialization/fsync/hash/print and external timeout/tool overhead remain explicitly unmeasured; nominal allocation is not measured CPU. No unused permission is restored.

The read-only outcome metadata process sampled **0.055568255 CPU seconds**, separate from static-review samples0.512394779: **0.567963034 sampled reviewer seconds** within the reserved60-second preparation/review allocation. Shell/startup/manual review/report overhead remains unmeasured. The total parent allocation stays120 nominal =60 pilot +60 preparation/review; this report creates no additional allocation.

## What this establishes—and does not

This finite result corroborates that the implementation matches the specified classical last-exit queue involution and fixed additive KRYPTOS phase layer. The mathematical proof/source review is preserved in `SOURCE-REVIEW.md` (SHA256 **8e59e6ded8a29cd9d932dde4b0532dd971ee64997cf933cae9ed6be17c490108**).

The cases were predetermined and disclosed, not a blind sample or statistical calibration. Alphabet domains overlap, and13 plants are not exhaustive coverage of all97-letter strings. The reviewer independently checked stored evidence, not a second experimental execution. Neither round-trip correctness nor a synthetic PASS is evidence that this was used for Kryptos, proof of global novelty, or a plaintext result.

A future target decision would be separate and must retain the exact seven deterministic decoders, input/framing and candidate-compatibility criteria, with no free queue choices, key changes, scoring or automatic rescue. That decision is **not** made here. No remote write was performed or authorized by this closeout.
