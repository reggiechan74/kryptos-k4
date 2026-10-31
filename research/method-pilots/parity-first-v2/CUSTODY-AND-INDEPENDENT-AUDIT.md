# Fresh validation custody and independent audit

31 October 2026. **PASS for the frozen40-case synthetic validation protocol and all240 solver outputs.** No target data or earlier holdout data were read. This validates the fixed model and implementations, not real-target applicability or worldwide novelty.

## Freeze, generation and disclosure chronology

1. Approved manifest SHA256 `30e9950c7073f608fb4e62b5991eaf77bdb6e9c44417d85ff4f1475a84873302` and protocol SHA256 `7e934b9e4ba1dffe18d4a9eee638ae7dc3c9f0bef82e82b4a87cabed17bdd9cd` were checked against every source pin before randomness was drawn. Pre-generation bounded controls passed.
2. One initial root invocation failed137 before seed draw or generator execution: the shell's final-command exec optimization invalidated an explicitly supplied expected-parent PID. The guard correctly rejected that mismatch. The absent seed/output files were verified, failure retained, and an explicit invocation-only correction approved. No scientific draw was discarded and no source changed.
3. Exactly one cryptographic-random generator seed and one public run-order seed were drawn at18:47:00UTC. The seed commitment was written before invoking the frozen generator. It was executed once without filtering by solver results. `generation-commitment.json` contains timestamps and hashes; `generation-resource-receipt.json` records bounded exit0.
4. Solver inputs contain only opaque IDs, ciphertext ranks and observed mask values. Original descriptive IDs remain in released truth as `source_id`. The fixed case ordering makes the stratum schedule inferable from the frozen generator. Seed/truth/source terms remained procedurally withheld from the solver runner until sealing; the shared filesystem provides **no cryptographic access isolation**. This is not a claim of fully hidden category labels.
5. Before disclosure, all240 completed stage outputs,240 receipts, inputs and frozen sources were sealed. Independent custody verification checked all523 seal entries, every stage's successful receipt, the original source/input/truth commitments and the exact projection from truth to stripped inputs. Seal SHA256 `3deac935255b28f32a1839e8f4911fd80f22ef35aec6f43bbf9ebd3c3baa1781`.
6. Seed and truth were released at18:49:44UTC, after that verification. See `release-verification.json`, `released-seed.json` and `released-truth.json`. No scientific source was changed after release.

The40 cases are not40 independent unseen draws:24 ordinary,6 degeneracy controls,2 same-crib/different-outside parity controls,4 contradictions and4 dependent observational twins. One zero-law/all-zero trajectory is explicitly deterministic structural replay. The generator labels this provenance; none is silently counted as fresh independent evidence.

## Independent exact audit

The frozen source-independent auditor enumerated all4992 coefficient-support containers of size0–3, used independent field elimination/projection, and compared both methods across three repetitions. It checked all91 exact marginal masks and feasibility, then independently replayed every returned supporting witness against all24 observations and its claimed row/value. The timed solver contract is identical: exact masks, empty/nonempty status and sparse supporting witnesses; no one-sided full-relation burden.

- 40/40 cases and240/240 solver outputs agree with the independent oracle.
- 25,806 marginal-value witness checks pass; each uses at most3 distinct nonzero coefficients.
- All32 generated in-family truths are retained; no false-forced prediction on those truths.
- All4 deliberately inconsistent observation cases are empty.
- All4 dependent twins remain compatible at their solver inputs but each has one forced prediction incompatible with its altered hidden truth. Generation correctly labeled their full-law membership unknown. The exact audited singleton exclusions now certify those specified full twin truths outside the model, without retroactively changing frozen labels. Compatibility of observations alone does not certify model membership.
- Tiny exhaustive17,576-vector/8,788-function controls and all four maximal-container budget checks pass.

The final audit used the frozen `audit_inputs.py` unchanged. Result SHA256 `91b3ea17e282fff411ac1900f54345cea8ceb19a4e2b8792c529f93e54719b83`; resource receipt SHA256 `b143d2b1af75421c22969708a220c4b378aa21a9ae3d84d5a35c2788ebb960a8`.

## Resource and inference limits

Independent audit:22.857CPU seconds for the stage plus0.0279 supervisorCPU; peak14,572KiB stage RSS and8,320KiB supervisor RSS; bounded600CPU/512MiB per process and900wall seconds, exit0, no timeout. Generation/release/summary stages have their own bounded receipts. Benchmark accounting and paired timing analysis remain in their separate receipts/report; this audit does not substitute a new timing workload.

Grouped full91 parity predictions preserve marginal masks, feasibility and representative sparse witnesses, not an enumerated global-function relation. No global-function uniqueness or full-law count follows from the grouped output. Finite-trace prediction uniqueness, global-function uniqueness and coefficient uniqueness remain distinct.

No additional target run, model expansion or source tuning is authorized by this result. Any later source correction is a new development revision requiring fresh validation rather than reuse of this revealed seed as a new blind test.
