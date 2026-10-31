# Independent adversarial audit — literal-source checker v1

31 October 2026. **PASS within the explicitly narrow literal-selector domain.** Recommend retaining as an internal verification aid, not as a whole-program semantic checker, authenticated provenance service or novel cryptanalytic algorithm.

## Separation and freezes

Reviewer read only SPEC.md before authoring81fresh synthetic fixtures and expected PASS/FAIL outcomes. Fixture manifest SHA256 `a3f677bc9fe84c13b2ef11ad84bc87ed218a5f7556ff5b587babe5f209a70f34` was sealed before opening production code or development tests. Production freeze `29e3912f38661c9304adf37586d22801b0c610bfd866abe899d976d982c263d8` and every manifest member were verified unchanged before execution.

The CLI schema was mapped after sealing. Three malformed/duplicate JSON request supplements were prescribed in the pre-inspection plan, yielding84CLI cases total. No fixture outcome was changed or resampled. Full raw sources, requests, outputs and checks are retained in fixtures.json, inputs/, RESULT.json and the independent harness.

## Results

-84/84expected statuses and exit codes; zero false accepts and zero false rejects under the preregistered expectations.
- All accepted cases returned exact expected sequence, source hash, supplied provenance and non-semantic limitation.
- Independent byte-offset checks of assignment/key/iterable start/end locations pass on the basic fixture.
- Side-effect sentinel absent. Deliberate top-level raise and dangerous-looking comprehension-body calls were parsed as data, never executed.
- Unsupported calls/names/arithmetic/f-strings/star expansion/nested values, wrong order/types, duplicate selected keys and bindings, lexical shadowing, assignment/mutation forms, hash mismatch, malformed UTF8/syntax/JSON, oversized input and AST depth/node limits all fail closed.
- Declared boundary cases PASS: tuple wrapper name shadowing, subsequent method calls, alias mutations and reflective globals writes. This is intentional SPEC behavior, **not evidence those sources are semantically safe or unchanged at runtime**.

Source review confirms no eval/exec, source-module import or execution. CLI opens only explicit request/source paths and writes JSON to stdout. Every fixture invocation establishes2CPU-second/256MiB limits. Python AST is used solely for structural inspection.

A minor scope clarification would help future readers: implementation permits only string-constant keys throughout the selected dictionary; even an unrelated integer-constant key is rejected. The independent fixture expected that conservative behavior. It is narrower than a loose reading of “dynamic keys rejected,” and should not be mistaken for supporting arbitrary literal keys.

## Actual motivating defect

A separately labelled, nonblind four-case supplement inspected pinned zeyeteam source SHA256 `1243ff870bcdd93e9712624b7837b9999dd80c00bcc3308b1514665f50e2516c` as data. Direct textual review confirms the iterable pair is EA, not AE, in both ERRnums shifts_ST and shifts_KA. The checker accepts expected `[LQ,OU,EA,IE]` and rejects `[LQ,OU,AE,IE]` for both selectors. It therefore detects the specific reconstruction transcription error when the operator supplies the correct pin/hash and selector. It does **not** independently validate subsequent shift arithmetic, alphabet definitions, aliases or the provenance string's authenticity.

## Resource/error supplement and limitations

A post-inspection, separately preregistered diagnostic supplement injects parser MemoryError/RecursionError, resource-limit setup failure, and missing source input. All four return structured failure; no PASS leaks. This is not fresh blind evidence and does not empirically force OS CPU/memory exhaustion. Actual OS killing behavior was not stress-tested. The in-process API does not establish process limits; use the CLI for untrusted bytes, as SPEC requires.

Measured fresh84-case child CPU3.000281seconds, wall3.092359541seconds, peak child RSS31,973,376bytes. Actual-source supplement child CPU0.163505seconds, wall0.167004321seconds, peak11,141,120bytes. Fault-injection test-body CPU0.002391868seconds, wall0.002392949seconds, peak19,869,696bytes; these last measurements exclude trusted harness import/startup. No K4 target test, cryptanalysis or external-source execution occurred.

## Decision

Retain frozen v1 unchanged for the declared literal reproduction task. No correction or new holdout is required by these observed results. Preserve this evidence and the original motivating failure; do not generalize84cases to a proof against all malicious Python or a semantic correctness guarantee. Any extension of supported syntax or runtime claims requires a new specification, freeze and fresh independent held-out suite.
