# Filtered-affine v1: exact residual projections, with explicit limits

**Reviewed generic mathematics and a hardened prime-field module—not a K4 result or globally new mathematics.** The work makes exact projection possible after excluding affine subdomains; it does not yet compile or validate the proposed K4 residual.

## What is established

- For an affine base over F_q with **fewer than q forbidden affine sets**, exact scalar projection removes precisely the fibers wholly contained in one forbidden set. Empty, constant and zero-dimensional cases are handled separately.
- At **r ≥ q**, the shortcut is unsafe. The hardened module uses budgeted exact inclusion–exclusion, with checked witnesses and elimination certificates. It returns **EXACT / EMPTY / INCOMPLETE**; partial masks are never presented as exact.
- Independent module audit passed **10,931 valid cases**, **95,713 witness checks**, **46 malformed-input rejections**, **74 budget checks** and **8 tamper rejections**, in both normal and optimized Python. These are generic finite-field controls, not cryptanalytic performance measurements.
- The old toy is preserved and explicitly **unsafe as a reusable API**: incomplete input checks and assertions disabled under `-O`. Its proof verdict does not make that implementation production-ready.

[Independent publication review](PUBLICATION-REVIEW.md) · [Results and next decision](RESULTS.md) · [Mathematical argument](THEORY.md) · [Historical toy review](TOY-REVIEW.md) · [Hardened API](MODULE.md) · [Independent module audit](MODULE-REVIEW.md)

## Source separation, not target exclusion

The source/operator review distinguishes **whole fixed causal operators on all reachable histories** from agreement on a single finite trace. The full-symbol equality family E is globally separate from the specified fixed-alphabet causal linear chains and fixed deterministic position-only maps. This proves neither target membership nor finite-trace separation.

The pinned Scott carry domain intersects E in exactly **156 old functions**, C = {b ± E12, b ± E34, b ± E56 : b ∈ Z26}; remove them as already attempted, without promoting the author's coverage claims to authenticated exact negatives. The inherited parity-negative set B is independently transferred from a retained receipt, **not recomputed**. Current direction: **R = E ∖ (B ∪ C)** compiler development on synthetic inputs only.

[Source operator map](OPERATOR-MAP.md), [dated clarifications](CLARIFICATIONS.md), [R6 supplement](E167-R6-SUPPLEMENT.md), [independent audit](INDEPENDENT-OPERATOR-AUDIT.md) and [final source decision](DECISION-STATUS.md) preserve the sequence of pending and resolved claims. Matbalez's exact historical recurrence scope remains **unresolved**. No target run is admitted and no worldwide novelty is claimed.

## Reproducibility and publication provenance

The [evidence archive](proof-module-and-source-evidence.zip), [archive receipt](ARCHIVE-RECEIPT.json) and [original/public provenance map](PUBLIC-PROVENANCE.json) contain the original toy, separate hardened module, tests, receipts and independent review programs. Computational bytes are unchanged. Sanitized prose and metadata have explicit original/public hashes; seven third-party source/log caches are omitted because redistribution rights were not established. Pinned links and source hashes remain.

Original manifests still identify original bytes, including omitted source bodies and sanitized prose; use the public map for distributed-byte verification. Historical audit programs retain generic execution-layout paths. Reproduce in an isolated matching layout or use a separately versioned path adapter, never silently change the frozen code. Source-alphabet checks require independently acquired pinned source bytes; no external program needs to be executed. Publication ran only static/docs and archive checks, not the scientific tests again.

The generic API is prime-field-only, has finite input/work limits and cooperative timeout checks, and does not claim a hard OS memory cap. Its independent audit checker is not a hardened public untrusted-result verifier. A canonical residual compiler still needs equivalence proofs, support-preserving lifts, fresh independent controls and a separate freeze. Existing [v1/v2 method results](../README.md) stay unchanged; active v3 work is separate and unpublished here.
