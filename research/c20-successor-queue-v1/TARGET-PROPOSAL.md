# C20: exact seven-phase target proposal

**PROPOSED — NOT ADMITTED, NOT EXECUTED.** Synthetic validation passed; no target data has been read or transformed for this proposal. This document is not execution authority. No target runner is implemented or frozen yet.

## Fixed candidates

Use the exact validated `c20.py` (SHA256 `bf2534a63b51952bab38afac973f35411bbedc6c9055e8181eb060cb10013867`). Standard AZ ranks 0–25; no alphabet choice. For phase p, subtract KRYPTOS[(i+p) mod7] from ciphertext coordinate i, then apply the successor-queue involution T. The seven repeating keys are:

| p | Repeating key | Decoder |
|---|---|---|
|0|KRYPTOS|T(C − KRYPTOS repeated)|
|1|RYPTOSK|T(C − RYPTOSK repeated)|
|2|YPTOSKR|T(C − YPTOSKR repeated)|
|3|PTOSKRY|T(C − PTOSKRY repeated)|
|4|TOSKRYP|T(C − TOSKRYP repeated)|
|5|OSKRYPT|T(C − OSKRYPT repeated)|
|6|SKRYPTO|T(C − SKRYPTO repeated)|

T scans adjacent pairs into successor lists, reverses each nonterminal list except its last item, reverses the terminal symbol's entire list, then consumes the lists from the original first symbol. The last-exit tree comes solely from the complete word: no fitted tree, free list ordering, reset, padding, transposition key or extra layer. The phase index starts at the first of exactly97 ciphertext letters. T is involutive, so re-encryption is T(P)+the same phase key. Stage order is not interchangeable.

## Input and result contract

After separate admission only: authenticate the established canonical input artifact against SHA256 `08a1a84bd0dddf2449a2c7f67ee770d093ed47f6ad9a795630b77a2c8062f241` and expected308 bytes. This expected identity is inherited from prior project provenance, not freshly read here. Inspect its schema and pin the exact extraction field in the future source review **before execution**, rejecting any schema, framing, length97, or uppercase-AZ mismatch. If identity or schema cannot be authenticated, stop; do not substitute an online ciphertext.

Evaluate exactly seven full97-letter decoders once. Verify each complete output against the already-reviewed separate reference traversal extracted from `pilot.py` (original SHA256 `7c1f7c7cff307d9cb37e87bbd710fd30d83eebf63952168d7f3bef8256c96c7f`); extraction will need its own source pin. Verify re-encryption equals all97 ciphertext letters. Check public plaintext clues at their fixed one-based positions:

-22–34 inclusive: EASTNORTHEAST (13 letters).
-64–74 inclusive: BERLINCLOCK (11 letters).

Record a boolean24-position compatibility mask and exact total for every phase, not just a best phase. Success means all24 match, reference agrees, and exact re-encryption holds. A hit is **a compatible candidate**, not a solved K4 claim: preserve it for separate independent interpretation/authenticity review. Any reference/round-trip error is an implementation failure, not evidence against the model. If all7 valid decoders fail any clue, record exact bounded negative and retire this fixed composition only. No ranking, English scoring, offset shift, rescue, new phase, key or alphabet, or automatic follow-on experiment.

## Proposed finite resources and stop

Request **30 nominal CPU seconds total**, not yet allocated:20 for minimal target source/static review and10 for the single invocation (8 child +2 supervisor),128MiB per process,30 seconds external wall, ≤1MiB result artifacts. Actual overhead/measurement scope must be disclosed. Reuse the proven bounded one-shot pattern rather than build another solver framework. Root must approve exact new source/freeze/argv/input pins following static review. One consumed attempt; error, timeout, missing evidence or uncertain completion does not authorize retry. No extra synthetic batch or benchmark is proposed.

This seven-candidate test is small enough to reject the exact speculative composition cheaply. Historical pure-permutation H-PERM exclusions must not be rerun. Mathematical foundation is classical BEST/last-exit sequence shuffling, including uShuffle; only this exact K4 application was not located in the finite inspected prior-art scope. Broader repositories, unpublished attempts and unavailable sources remain unknown. Source citations and pinned local/external comparisons are in ADMISSION-AUDIT.md. No historical creator-use evidence has been found.
