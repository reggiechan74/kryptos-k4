# Independent autonomous recurrence oracle

Source supplied inline by the independent reviewer, 22 October 2026. It is kept
separately from the repository's production solver and frozen local run.

The delegation transport HTML-escaped operators. Decoding that single transport
layer yielded exactly the declared original 12,929 bytes and SHA-256. No code,
whitespace or algorithm repair was applied. Raw transport bytes remain outside
the repository; their hash and the complete replay receipt are recorded in
[REPLAY-RECEIPT.json](REPLAY-RECEIPT.json).

The source was read before execution. Node.js v23.9.0 reproduces the exact declared
16,388-byte JSON result and SHA-256. All 20 coefficient-space rank/count results
agree with the independent local Python implementation. The JavaScript oracle
passes 231 numerical controls; this is a separate count from local regression tests.

```sh
node independent/2026-10-22/autonomous-recurrence/k4_recurrence_oracle.js
```

**Limit:** its unused generic positive-survivor branch is illustrative and is not
validated for complete plaintext-class counting. It checks prefix reachability
only after Berlin. Actual K4 rejects before that branch, so the negative ranks
and certificates do not depend on it. It has not been adopted as a production
survivor solver. Its coefficient and prefix controls do not establish full-family
blind unique recovery or a K4 significance value.

The source and deterministic output remain byte-identical to the supplied hashes.
The local production audit separately validates early prefix reachability, exact
small-ring full-state counts and overlapping affine-space union counts.
