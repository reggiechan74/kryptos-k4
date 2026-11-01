# Fresh residual v2 — independent failure preservation and cause review

**Preservation/integrity review PASS; the scientific experiment remains INCOMPLETE/FAILED under its frozen protocol.** The eighth slot, `v001-optimized`, exhausted the cooperative 20-second preflight wall allowance. Its semantic fields are cleared; the producer and full reference were not attempted. The supervisor stopped, retained the failed slot's 80-second policy reservation and canceled all 20 successors. No resume, retry, source/cap alteration, replacement draw, success sealer, truth release or analysis is authorized by this report.

This review is read-only source/metadata/hash inspection and local report preparation. No experimental code was imported, compiled or run; no certificate was mathematically replayed or copied; no seed/truth or older failed-cohort input was accessed. Full reports and byte inventories were inspected, not a new scientific result calculated from the data.

## Exact preserved evidence

Runtime root: `/workspace/shared/residual-fresh-validation-v2/runs`.

| Artifact | SHA-256 |
|---|---|
| Source FREEZE.json | `77bda1efb5878971eb7ff42feeca26acd1e79813329ca30108b72aeeeebe8767` |
| ANALYSIS-MANIFEST.json | `11c5f756f5f1bd233c0994cc201c3099e929bbb995449e2f1381062001b1382a` |
| Public solver input | `79319cb9272242cd7f44b7bf2ccf6c9a630450ddab82c7cc2adb6457bd297747` |
| Public RUN_APPROVAL.json | `d01367cebf095b45dd5272c1b11a640373ef3786fc7c6dca73c49c40f1e44ee4` |
| RUNNER-EXTERNAL-COMPLETION.json | `5bac8954641593797d82ceaaf878253e6a527c1a73ad294dac4e2f8dc257aca6` |
| runs/state.json | `11b9e0c6b7291520d9feb38bce6f0b50ad2e1a11ae19e43639e65e91f6b1d71b` |
| runs/IN_FLIGHT.lock | `f7cde537161151785ecd9c176431c3e5aef905831cac5c0aa59afdb77f375450` |
| v001-optimized/resource.json | `ce688178d3bce7087888f55d6904e559eed646f6d47c04ec0d93da38eefa2976` |
| v001-optimized/result.json | `69eab32ab8962c187c62a312ecde9e1453111023b1f656bdc3524a15c5da69cb` |
| Authority FAILURE-PRESERVATION.json | `33a6f1e91c13a4fc819cf4f53b8eccf3baecc76891ae1d5d8a58f43b9ce7c001` |
| Authority STAGE-RESOURCE-ACCOUNTING.json | `f60290972c18188fe974182313c17746e60bba5f3fbb7b38a4e151c310f66a74` |

The source/two-mock PASS and command-instantiation PASS remain immutable separate historical evidence. All 21 source/freeze pins still match. Generation's externally completed receipt, parent acknowledgment, public attestation and active approval link consistently to this one input and freeze. Generation receipt SHA is `5687c586da254350a4e271894ddec98377e807b3212c35c5781db74272094cb0`; its external completion record SHA is `5b15ff7bc5cb96f5cf7fe3844a3f96cb5efedd86b9a978b4159e468910738bca`. Parent generation acknowledgment is retained as transcript/metadata evidence, not inferred merely from approval JSON.

## Failure and result limits

The failed worker reports:

- PRECHECK_INCOMPLETE, reason `wall-time cap`;
- 4,153 fully checked support records out of 4,495; 4,154 support/solve attempts;
- 8,306 certificate checks, 32,528 generation and 32,528 audit beta candidates, and 780,672 parity-row tests on each side;
- 1,090,941 row operations and 26,472,380 work units;
- lower bound 1, **exact_W null**, certificate completion descriptor null; the incomplete evidence file is retained;
- preflight elapsed wall 20.32284503599658 seconds;
- producer/reference attempt flags false, their counters null, and producer/verification/semantic_summary all null.

The final external tool result is chunk `5e5512`, exit 1. The resource receipt records ordinary child exit 1, not a termination signal: worker CPU 16.325925 seconds, supervisor exclusive sample 2.748263, supervised wall 21.78825701900496. Child reaped is true; no OS wall timeout, log overflow or collector error is recorded. Both failed-slot logs are empty. Reported component CPU is below the nominal 75/5 ceilings. These facts establish a cooperative wall-cap failure, **not** recurrence or resolution of the earlier OS CPU-limit anomaly.

Stored outcomes before failure are four safe resource-gate claims (G0/G1 in both modes) and three VERIFIED_EXACT claims (v000 both modes, v001 normal). For G0, both modes record 89 supports and lower bound 1,006,226; for G1, 505 supports and lower bound 1,001,832. The v000 pair records all 4,495 supports and W=1. The v001 normal report also records complete W=1; this value must not be transplanted into the failed optimized run.

The reviewer independently compared G0, G1 and v000 complete reports using **only the frozen pair-exclusion paths**, and compared each pair's certificate bytes. All three pairs match. This is artifact/mode consistency, not post-run re-solving or certificate replay. Only one fresh base has a completed pair. The unpaired v001 normal result contributes zero paired semantic coverage; the two disclosed controls are not fresh base observations. There is no released truth comparison, stratum/twin coverage analysis, accuracy estimate or successful cohort validation. The frozen failure rule dominates; do not relabel this stopped experiment as a smaller successful sample or merely omit the failed pair.

## Inventory, custody and cleanup

The original runtime tree contains **42 files / 40,761,555 bytes**, including **8 certificate files / 40,699,407 bytes**. Forty slot files are accompanied by the stopped state and retained lock. The state's 40,758,753 artifact bytes are slot artifacts; adding state 2,565 bytes and lock 237 bytes gives the exact tree total. The independent ORIGINAL-RUN-SHA256SUMS and ORIGINAL-RUN-INVENTORY.tsv match the custodian's preservation inventory. Every slot receipt's four original artifact hashes, all eight state-bound resource hashes and every frozen inner command/cwd were checked. No runtime symlink was found. No certificate copy was made.

The final state contains eight accounted slots, `stopped=true`, paired cases G0/G1/v000, and exactly v002 through v011 in both modes canceled. The failed in-flight reservation remains 75 worker +5 supervisor CPU seconds, 32 MiB certificate and 40 MiB artifact allowance. The lock and retained reservation are conservative stop-policy evidence, **not evidence of an unreaped process** and not authority to resume. All eight receipts record reaped children; the runner's externally observed final tool completions are retained, including temporary session polling histories and final exits. Cleanup evidence is limited to these supervised launches/visible namespace, not a machine-global process audit.

Success-sealer/analysis receipts, start markers and output manifests are absent at the approved authority destinations. The preservation inventory is explicitly **not** a successful terminal seal. The reviewer did not stat, hash, open or parse the actual private seed/truth. Custodian/runner attest no release or analysis; the original custody separation remains in force. No public prediction claim is treated as truth.

## Deduplicated accounting

The single combined authority ledger above was checked against the original eight cohort receipts, generation receipt and previously reviewed two-mock ledger. No extra runner ledger is required.

| Component | Worker wait4 CPU seconds | Supervisor exclusive samples |
|---|---:|---:|
| Two earlier mocks | 0.547645 | 0.240450 |
| One generation | 0.131048 | 0.047872 |
| Eight cohort slots | 51.077834 | 4.030656 |
| Total | **51.756527** | **4.318978** |

Known reported components total **56.075505 CPU seconds**, excluding final-write/exit tails and control overhead. Internal phase timers and polling wall durations are subsets or different quantities and are not added. Namespace-local repeated PID numbers do not deduplicate distinct launches; command/receipt identities do.

Full supervisor policy charges are **133 seconds** (62 mocks +31 generation +40 cohort), distinct from the samples. Worker actual plus those full charges is 184.756527, **not measured CPU**. Attempted nominal allocations are 124 mocks +62 generation +640 cohort =826 seconds. The retained failed-slot 80 is a **subset of the 640**, never another measured or nominal charge. Canceled/unstarted slots account for 1,600 seconds; unlaunched sealer/analysis allocations are 12/362; the control/preparation/closeout allowance is 200. These partitions total the unchanged 3,000-second allocation. None authorizes reuse, replenishment or a recovery run. Project allocation remains 20,200/28,800, not measured project consumption.

Supervisor final receipt/state/write/exit tails, shell/tool startup and static preparation/review/metadata overhead are unmeasured, not zero. This reviewer adds no experimental-process receipt or duplicate scientific CPU charge. Nominal limits are not guarantees about physical CPU maxima or RSS. All original state and ledger facts remain preserved even though the observed child is reaped.

## Read-only cause assessment

Frozen reference Meter checks `time.monotonic() - started >= max_seconds` on each metered charge. The preflight's single 20-second clock spans input checking, all support certification, generation beta tests, canonical serialization, per-line flush/fsync/readback, independent serialized audit and completion hashing. A charge can notice elapsed wall after time spent in any of these operations or while descheduled. The final elapsed receipt is not the exact instant at which the cap was first crossed. Final metadata accounting may also encounter the already-expired wall gate, leaving the evidence file retained without a completion descriptor.

The counters and checked cursor locate interruption before the 4,154th support completed its audit. They do not identify the triggering subphase, filesystem latency, CPU contention, scheduler delay or hardware cause. The failed worker's whole-worker wall/CPU gap likewise is not an I/O timing measurement. Normal v001 completed in 13.985172431996034 preflight wall seconds; optimized did not finish at 20.32284503599658. One sequential execution per mode on a shared environment cannot establish that Python optimization caused the difference, nor that any specific revised wall cap would guarantee completion.

Deterministic work counts, complete source proof obligations and completed-pair byte equality are a different kind of evidence from a load-sensitive elapsed-wall deadline. They support the reviewed algorithm/fail-closed mechanism; they do not negate this protocol failure, certify all unstarted bases, or prove that elapsed time alone has a stable distribution.

## Recommendation only — no recovery authorized

Prefer preserving the fixed data and scientific implementation over drawing replacement cohorts until a run passes. If a later authorized study requires a resource investigation, first approve one finite, separate instrumentation protocol using an **already disclosed generic full31 control**, never this failed cohort's private truth or the older failed cohort. Two sequential normal/-O invocations could record aggregate phase process CPU and monotonic time, fsync/readback totals/counts and completion-hash time, with fixed output caps, unchanged logical work limits, explicit new nominal CPU/wall/memory allocations and no retry. A proposed ceiling of two 75-worker +5-supervisor slots plus a separately approved 20-second control allowance (180 total nominal CPU) is a planning option, not permission or a physical-hard-limit claim. Keep the diagnostic 20-second gate if the question is where that gate is spent; instrumentation overhead and incomplete diagnostics must be reported. No such source or test was created or executed here.

For a later scientific recovery decision, distinguish:

1. **Separately labeled post-failure re-evaluation of this exact sealed cohort.** This is the preferred option if a revised resource envelope can be justified in advance. Preserve the original freeze, outputs, INCOMPLETE status, stop lock and failed reservation untouched. Use a new versioned protocol/result namespace and an independently reviewed freeze that explicitly lists every resource/instrumentation/path-binding change while retaining the mathematical engine/reference, dictionary, public data hash, support/beta traversal, denominators and semantic verification requirements. Preregister one finite schedule, resource profile, failure rule and interpretation before execution. Prefer a complete fixed normal/-O schedule rather than selectively filling successful suffixes and combining them with old results. Keep truth sealed until a newly authorized external terminal/release gate. A successful re-evaluation would be evidence on a **reused, post-failure selected dataset under a revised envelope**, not an independent fresh validation and not a retroactive PASS for this experiment. It must receive explicit project authority for reusing the sealed input, exact commands/caps, new budget/storage, custody/release and no-repeat rules; no current authorization supplies this.
2. **Another fresh draw.** This is not currently allowed and is not the recommended workaround for a load-sensitive deadline. Replacing datasets after resource failures risks repeated replacement/selection until success and changes what is being validated. A genuinely new scientific question could justify a separately preregistered fresh study, retaining all failures and full denominators, but not a silent replacement of this one or unlimited generation.

No numerical cap increase is justified merely because one mode finished or because the remaining prefix was small. Do not remove the stop guard, mark W complete from its lower bound, release truth for convenience, or run either option before explicit approval. The old 48-case failed cohort remains permanently sealed and outside both options. K4 remains NO-GO; unresolved prior-art/model-membership scope is unchanged.

## Custodian handoff readback

The later custodian drafts were also read and hash-checked: CUSTODIAN-CLOSEOUT.md SHA-256 `fa60f5bd0d66b74386cfc046386bdc2e487c9ce3cf3c07c4956236957453ae21` and PUBLICATION-HANDOFF.md SHA-256 `e388c9ef464432f2909452ea2b73fec951470ef999bd8ab8a960c3b09527fabb`. Their outcome counts, accounting distinctions, unresolved cause, preferred separately authorized same-input re-evaluation and prohibition on new-fresh claims agree with this review. Their historical statement that this independent review was pending is correct at their creation and should be supplemented by this pin, not silently rewritten.

The publication handoff is a proposal, not publication or copy authority. It correctly excludes private seed/truth, raw authority commands/receipts and wholesale copying of the private command-instantiation review, and defers certificate copies to a separate decision. This check does not authorize a repository/remote write, certify the current remote checkpoint, or run documentation/scientific tests. Any later package must preserve the failure and receive its own privacy/provenance review.

The applicable project instructions were read. No remote state was changed. No permission denial or uncertain scientific execution occurred. Harmless shell/JSON inspection errors were corrected without importing or executing target source. **The present review closes preservation and bounded diagnosis; it does not restart the experiment.**
