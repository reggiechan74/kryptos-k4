# E01 exact target proposal — NOT AUTHORIZED OR EXECUTED

This is a proposal only. Synthetic validation and its publication do not grant target execution. No target implementation was run, and no raw target fixture was reopened to prepare this document. Input metadata below comes from the authenticated C20 input contract.

## Exactly one model and candidate

Use the unchanged production/reference implementations from synthetic freeze `f2987d9fc3b65ac435ec113257facd3d7ec00ed8b47af86a3eda3db06c2fb0c1`:
- production.py SHA256 `d6c2705c15650f81e7d79fdec437b126d61fd11c9b0616c80a19d33c2dcdc753`;
- independently authored reference.py SHA256 `c14c162c499db89cee336cec84bd9c79335913811cd4809f91bef1199e20b3c5`;
- source policy SHA256 `b4f2dec75c5ce39236701e83093b360d097a8f90c4fb7542d749406e2ccef0a6`;
- source bank SHA256 `efa74dabd7ff0448987060c02ac4f045c6188d4a6169c7ed44d314671144b8a8`.

Use the frozen bank as-is; verify all rows are AZ permutations and that its exact bytes match the pin. Corpus is the fixed literal K1/K2-as-inscribed/K3 plaintext fields; within-section counts after uppercase ASCII filtering; decreasing count then AZ tie order. Initial previous-plaintext state Q. For each symbol c: p=L_state[index_AZ(c)], then state=p. Output AZ, continuous stream from index0. No phase, reset, offset, key, additional alphabet, corrected corpus, source sweep, score, or free parameter.

The candidate count is **exactly1**. Two independent implementations verify that same candidate, not two hypotheses. Retain its entire97-letter decoded output even if the first or every clue fails; no early-stop filtering or best-only output. No branch is chosen after observing a clue score.

## Authenticated input and all24 assertions

Canonical repository `data/k4.json`:308 bytes; SHA256 `08a1a84bd0dddf2449a2c7f67ee770d093ed47f6ad9a795630b77a2c8062f241`; Git blob `361714e4d9b19393bcc89df59e73d1c0522eeedb`.

Require exact JSON keys `ciphertext,length,indexing,cribs`; integer length97 (not bool); indexing exactly `one-based inclusive`; ciphertext exactly97 uppercase ASCII AZ symbols without stripping or normalization; cribs exactly these ordered objects:

- start22,end34,plaintext EASTNORTHEAST (13 positions);
- start64,end74,plaintext BERLINCLOCK (11 positions).

Authenticate bytes before parsing and recheck unchanged at completion. Reject missing/extra fields, malformed or mismatched metadata as INCOMPLETE/INVALID_INPUT, never a model negative. Do not search for other strings in the file.

After independent decoders agree on every symbol, require both implementations to re-encode all97 symbols exactly. Separately evaluate every one of the24 fixed positions against the stored candidate; retain position, expected symbol, observed symbol, boolean result,24-bit mask and match count. Supplied assertions are never passed into either decoder or state update.

## Outputs and decision

Store source/input/binary hashes, exactly1 candidate record, full output, both decoder agreement, both full re-encryption results, all24 assertion comparisons, runtime/exit receipts and all candidate compatibility status. Outcomes:

- `EXACT_INCOMPATIBLE`: complete authenticated evaluation with any false clue bit; excludes only this frozen source-conditioned model.
- `EXACT_COMPATIBLE`: all24 bits true plus full independent agreement/re-encryption; conditionally compatible, not authenticated intended solution.
- `INCOMPLETE_OR_INVALID`: malformed input, source/input mutation, disagreement, failed inverse, timeout, resource breach, missing receipt or uncertain completion. No exclusion claim.

No corpus/tie/start/offset adjustment, new synthetic batch or retry follows any result. Preserve complete candidate evidence even for an incompatible result. Independently read back stored comparisons/hashes after execution without silently performing another target invocation.

## Proposed minimal resources and authorization gates

Suggested new allocation only: **10 nominal CPU seconds total**,5 for source preparation/independent reviews and5 for exactly one synthetic-free target invocation. This is not allocated by this document. Proposed worker CPU soft2/hard3 seconds and128MiB; bounded supervisor overhead; measured aggregate below4 seconds with1-second receipt/exit reserve; immediate hard worker wall timeout30 seconds, supervisor startup/tail disclosed. A single97-symbol candidate is tiny; timeout still means incomplete rather than increasing the cap. No paid service, external verifier, external code execution, batch, or claimed plaintext lookup.

Before invocation: freeze the minimal wrapper, exact executable identities/argv/output paths and expected manifest SHA; independently source-review it; obtain a separate explicit one-shot grant and consume the attempt durably. Source/binary/input identity is rechecked before loading authenticated code and before accepting completion. Preserve terminal tool evidence privately and a publication-safe external resource/exit receipt. No allocation/grant/target result is implied by the synthetic checkpoint.
