# C20 target-v1 — independent outcome review

**PASS: complete, bounded seven-phase negative.** All seven saved outputs fail the fixed 24-letter clue requirement. Independent comparison of the saved plaintexts to the public clues reproduces counts **2, 1, 1, 1, 0, 0, 0** for phases 0–6. This rules out only the frozen composition `C = T(P) + KRYPTOS_phase (mod 26)` with standard AZ ranks and the specified successor-queue involution. It does not rule out other graph ciphers, keys, alphabets, layer orders or parameters, and does not solve K4. Partial matches are not promoted into near-solution evidence.

## Authority and immutable identities

The reviewed source freeze is `8f7b984bbdf29a8a9d6fc8bf232f9502bbeffece7fd0ae7c705e26f0a63560ec`. All five source/protocol pins and both Python/timeout binary pins still match. The canonical input is unchanged: 308 bytes, SHA256 `08a1a84bd0dddf2449a2c7f67ee770d093ed47f6ad9a795630b77a2c8062f241`. Extraction and clue framing remain those in the source review; no normalization or offset change occurred.

Prior independent source review: `85ea05612f08139225dae3e8b36d1ccc6fa2fa431e3a03983427d59d9527cd62`. Its retained manifest entries also authenticate.

The exact command proposal is `078e138bc9d0bf0fa1b5645800fbffaf7cddde781671a6bc47ccab7cf69c2aba`; the actual approval is `6090cbac38279d84e6e50e09885d5d45d642ea4aac0a7a55b02bd5f11f5ec304`. Approval bytes equal the proposed object and bind the final freeze, C20-target-once, ten nominal CPU seconds and no retry. The published prerequisite checkpoint is recorded as `ca3e86d21a86c6473593fbdd7920887acc58b026`, with local publication receipt `eea79f5f92efbd4ae7910d6927eb72d504f1b2d2d2c9e11c4564455ba5920836`. This audit authenticates that retained publication evidence; it does not make a new remote verification.

Trusted parent/coordinator history establishes the separate grant and durable consumed start at 12:23:04 UTC. Local files alone are not claimed to establish durable external authorization.

## Actual completion and output integrity

- Sole invocation: trusted external tool completion, final exit 0, no session returned. No second invocation was performed by this review.
- Result: `2f884876de42c87e0229d3ab9c3c96524dfe56700dc2f45604b19c7a495d8e86`.
- Receipt: `97e4fdb1b72d70518fc8449e154cbaac96d3f33264083ecb1dd8654e528a120c`.
- External completion: `4d44e0eaac339d095bebaa4b005de6205b27f8fffb7b62f1ed883b800ab3a810`.
- Attempt marker: `981b545c938f14f325b0115056c845144b1c494e22ff797f025e5c3f8f10d830`.

The receipt reports COMPLETE_TARGET_CHECK, actual child exit 0, reaped child, no error or timeout, complete_target_result=true, and empty stderr. Its child command and outer wall contract agree with the frozen command and approved pin substitutions. Receipt-covered ATTEMPT/stdout/stderr hashes and sizes match. The five runtime/external artifacts total **5,949 bytes**. The separately added 2,632-byte FINDINGS.md is a later narrative, not a retroactively receipt-covered runtime artifact; its content and SHA256 `62483e21b88153094ba9c2bf680efc789dd5f6e8ff06c0f0ab7f961d90c6b2a7` were reviewed separately and are consistent with the bounded result.

There are exactly seven records, phases 0–6 in order, each with a 97-letter uppercase AZ plaintext and 24 strict boolean mask entries. Direct readback against EASTNORTHEAST at one-based positions 22–34 and BERLINCLOCK at 64–74 matches every stored mask and count. Matching positions are [22,74] for phase 0, [70] for each of phases 1–3, and none for phases 4–6. Every compatibility flag is false; compatible_phases is empty and the stored conclusion is EXACT_SEVEN_PHASE_MODEL_NEGATIVE.

All seven records contain true reference-agreement and full97-letter re-encryption controls. Those controls were executed by the authenticated, previously statically reviewed target program; this outcome reviewer checked their presence, strict values, source semantics and successful completion, **not a second reference/inverse computation**. No prepared module was imported, no transform was rerun, and no new plaintext candidate, model or test was generated.

## Resource accounting and finality

The ten-second nominal target permission is consumed, distinct from actual reported usage:

| Component | CPU seconds |
|---|---:|
| OS-reported child | 0.182064 |
| Cumulative supervisor sample | 0.302418 |
| Known instrumented sum | **0.484482** |

Receipt wall sample is 0.4354215 seconds; child peak RSS is 40,576 KiB. These are below the frozen acceptance limits. Receipt serialization/fsync/hash/final print and outer timeout/tool overhead remain unmeasured, not zero. No inner timer is added again. Limits are operational controls, not claims of perfect physical metrology.

The separate read-only metadata/mask-readback checker sampled **0.064338947 CPU seconds**. Together with the prior source review's 0.067327737 sampled seconds, known review-script samples total **0.131666684 seconds**, charged to the existing twenty-second preparation/review portion, not added to the target receipt. Manual review, shell/tool startup and report-writing overhead are unmeasured. No new allocation or permission recycling is implied.

**No retry, rescue variant or next test is authorized by this review.** The synthetic correctness evidence and classical BEST/last-exit foundations remain valid, without a claim of newly invented mathematics, worldwide novelty or creator use. Preserve this completed negative and its exact outputs. K4 remains unsolved.
