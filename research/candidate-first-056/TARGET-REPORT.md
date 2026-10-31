# Study 056 target result: complete bounded exclusion

**UNSAT_COMPLETE.** The canonical 97-letter target has no compatible plaintext/key/operator in the exact frozen family:

- Standard A–Z periodic Vigenere, phase zero, with unrestricted nominal-period 2–8 seeds;
- Followed by row-filled, unpadded ragged columnar transposition;
- Widths 6–9, every column emission order, each column read top to bottom;
- Exactly the 24 public literal clues at zero-based positions 21..33 and 63..73.

Selected solver S was evaluated **once**, completing all 28 width/period cells. Its exact placement constraints rejected every cell at the root: 28 visited states, 1,584 support checks and 28 conflicts. It enumerated no surviving full route or key; those eliminated descriptions are not falsely counted as individually evaluated.

The separately written row-matrix reference was evaluated **once** and completed **2,862,720 full route/period trials**. It derives all key coordinates from the supplied clues for each route rather than brute-forcing 26-to-the-period seeds. It independently returned the same empty complete set.

| Projection | Count |
|---|---:|
| Compatible nominal descriptions | 0 |
| Canonical operators/keys | 0 |
| Distinct full plaintexts | 0 |
| Surviving aliases or witnesses to re-encrypt | 0 |

This is a complete exact result, not a timeout, ranking score or failure to find readable text. The independent target audit certifies identical complete sets, all frozen dependencies unchanged and resource limits satisfied.

## Provenance and resources

The pinned source is [data/k4.json at de3654a](https://github.com/reggiechan74/kryptos-k4/blob/de3654a098162185d47b7c14ee1eef1631ab1804/data/k4.json), Git blob `361714e4d9b19393bcc89df59e73d1c0522eeedb`. The ciphertext literal SHA-256 is `eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab`. The exact 13- and 11-letter cribs and indexing were independently checked before the target freeze. Target loading occurred only after the corrected fresh blind benchmark and explicit parent authorization.

- Additive target freeze: `99e92e5c6efb8dbac992081ed0621313a5963973bf33a764713928c24b58a6c7`.
- S output: `6c4edb86ab199c682fbeb4ee98e255a0b40a2372b8e8167b9e9c78f2553500c6`.
- Independent reference output: `0c1a5982298b6095ca4c23da6689ad19277ff389a92a885b6b5ec37ed3e1a529`.
- S inclusive CPU: **0.055047 seconds**; conservative pair-memory upper bound **28,049,408 bytes**.
- Reference inclusive CPU: **0.112906 seconds**; conservative pair-memory upper bound **19,660,800 bytes**.
- Both satisfied the corrected 20 CPU-second / 2 GiB envelopes with exact waited accounting and no failure reserve.

## Interpretation and stop

This excludes **only the specified standard-AZ, Vigenere-then-unpadded-columnar family and these bounds**. It does not exclude reversed operation order, other alphabets, other substitutions, wider columns, longer periods, padding, added layers or classical cryptography generally. Those alternatives were not tested.

The synthetic study supports early/shared constraint propagation, not a learned-conflict advantage. L failed its preregistered gate, and S did not materially outperform simpler P. No such benefit is claimed from this target result.

**The authorized target stage is finished. No additional search, model expansion, reverse-order experiment, new study, paid checker or publication followed.**
