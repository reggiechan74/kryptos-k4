# Proposed finite C20 correctness pilot — NOT RUN / NOT YET FROZEN

Purpose: independently test the stated involution and seven-phase outer-layer inverse. This is implementation validation, not historical plausibility or novelty proof, and not a K4 test.

## Fixed scope

- Exact operator and literal KRYPTOS outer key from REPORT.md, no alterations.
- Tiny cases: lexicographic words over integer alphabets q=2,3,4, lengths 0..10, 0..8, 0..6 respectively. Totals 2047+9841+5461=17,349 cases; overlaps between alphabets are not independent evidence.
- Production implementation: explicit successor queues and greedy walking, validating termination, endpoint and complete edge usage.
- Independent oracle: for each q,n enumerate all words once and map `(start, ordered successor lists)` to the unique word. For each input, form the specified reversed-list signature and look up its word. The oracle must not call the greedy implementation or its helpers. Failure of uniqueness or missing signature is a hard failure. Empty input uses a separate sentinel signature. This checks existence and complete reconstruction without duplicating the traversal algorithm.
- Check equality of both outputs; involution; unchanged length/endpoints/unigram/directed-bigram counts; preserved nonterminal last-exit labels. Record fixed-point counts only as diagnostics, not success scores.
- Explicit hand fixtures: ABACAD↔ACABAD; ABACA↔ACABA; ABAC with naive all-queue reversal gets stuck at AC. Length97 x=ABACAD+91D and y=ABECAD+91D verify the stated non-fixed-position witness.
- Malformed inputs: reject noninteger symbols, bools, negative/out-of-range integers, and malformed q. The hypothetical empty-word convention is not a target framing change.

## Full-alphabet phase checks

Define `repeat(w)` as repeating a nonempty literal word and taking its first97 characters. Thirteen predetermined plants:

1. repeat(A)
2. repeat(AB)
3. repeat(ABC)
4. repeat(ABCDEFGHIJKLMNOPQRSTUVWXYZ)
5. repeat(ZYXWVUTSRQPONMLKJIHGFEDCBA)
6. repeat(ABACAD)
7. repeat(ABECAD)
8. repeat(AABBAACCAADD)
9. repeat(ABACABA)
10. repeat(AAAABBBBCCCCDDDD)
11. ABACAD +91D
12. ABECAD +91D
13. repeat(ABCDDCBA)

Use all seven phases, exactly91 plant/phase pairs. For every pair verify the entire97-letter plaintext after decrypt/encrypt, exact phase-key indexing and re-encryption. The reference uses direct immutable tuples/dictionaries written independently from production; no K4 source/crib or archive is imported. Full-alphabet plants are disclosed regression cases, not a blind sample or statistical calibration.

Record distinct phase outputs and collisions honestly. Seven nonidentical phase key streams imply distinct ciphertext outputs for a fixed plaintext under the fixed additive outer map; no claim that all decoded plaintexts are distinct for arbitrary ciphertext is needed without checking the exact argument.

## Proposed execution contract

One synthetic-only invocation, no normal/-O duplication needed unless source review identifies an actual mode-sensitive risk. Proposed total60CPU seconds,128MiB address-space limit,120seconds external wall timeout, ≤10MiB output. Enumerated tiny input data is generated deterministically; no entropy or network and no external code execution. Use explicit exceptions, not assertions as sole validity checks. Freeze source, interpreter, exact command and expected case counts after independent source review; no code or executable grant exists yet.

On any mismatch, invalid oracle, resource limit or uncertain completion: retain outputs and classify INCOMPLETE/FAILED, do not run target or automatically retry. On full success: recommend a separate target decision for exactly seven complete deterministic decoders, after final scope/prior-art reconciliation. No free local queue ordering, random tree, different key/alphabet, repair or plaintext scoring is authorized.

No statistical null study is needed for this correctness-only pilot. A later target protocol must specify what candidate compatibility means and must not convert exact re-encryption into proof of intended plaintext. There is currently no demonstrated performance bottleneck warranting an optimized solver.

## Prefreeze implementation contract

The source freeze will pin c20.py, pilot.py, run_once.py and this protocol, plus the actual Python executable. The one-shot supervisor allocates58CPU seconds to its sole child and2to itself (60total nominal), each128MiB. The supervisor uses soft2/hard60 with default SIGXCPU termination so its child can install hard58 after fork; CPU accounting is subject to operating-system signal granularity, not an exact stopwatch. The supervisor child wall termination at115seconds and requested external wall bound120seconds. Each child log is capped at1MiB; three initial artifacts plus final receipt stay below10MiB. A Linux parent-death signal prevents an orphan child; no descendant process is created by the pilot. Missing/invalid receipts remain INCOMPLETE, never a retry permit.

The caller supplies a fresh root-authorized approval hash. The approval file is outside the source root and must bind the exact freeze and job C20-synthetic-once with status APPROVED_SYNTHETIC_ONLY. The exclusive ATTEMPT record is created before launching. Neither an existing result nor a failed attempt permits a second launch. The root records the consumed attempt and actual external completion in the persistent conversation as protection against loss of this disposable directory.

All experiment checks use explicit exceptions. Source bytes are hash-authenticated before compile/exec; no local bytecode module cache is loaded. Python's standard library/runtime is trusted infrastructure, not independently frozen here. The interpreter executable is pinned. Source comparison before/after and expected result counts authenticate completion; they do not replace independent result review.


### Exact outer command contract

`/usr/bin/timeout --signal=KILL 120s <pinned-python> -I -B <original-source-root>/run_once.py --freeze-sha256 <FINAL_FREEZE_SHA256> --approval-sha256 <ROOT_APPROVAL_SHA256>`

The fixed argv template and timeout binary SHA256 are included in the freeze. The parent must retain the actual external command, session/exit and completion; a local receipt alone cannot prove the tool invocation ended. No child or wrapper relaunch is permitted after an attempt begins. The supervisor tests final child CPU≤58, cumulative own CPU sample≤2, and wall sample<120 before accepting PASS. Its own sample includes startup and artifact hashing but excludes final receipt serialization/fsync/hash/print; outer timeout/tool overhead is also unmeasured. Nominal reservation remains60, with this known measurement boundary stated rather than represented as zero overhead.
