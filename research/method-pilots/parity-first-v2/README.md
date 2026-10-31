# Parity-first v2: matched synthetic validation

**Same exact predictions, less CPU on this fixed workload—not more recovered information.** This is a model-specific method pilot, not a K4 result, new cipher family or global invention claim.

- **40 cases / 240 timed outputs** agree with the independent exact oracle; **25,806** marginal witnesses checked.
- Summed **per-case median solver CPU**: **19.612 s CRT versus 14.403 s parity-first (26.6% lower)**. Faster on 38/40 cases, but both alias controls lost: **13.6% and 46.9% slower**.
- Peak process RSS: **8,448 versus 21,760 KiB**; three-repeat variability reached **1.97× versus 2.95×**. This is not a universal speed guarantee or population estimate.
- 32 in-family cases: **2,103/2,144 unknown modeled positions** forced, zero false forced; **27/32** determine all 67. **First six positions remain outside the model.** Four misspecified twins each force one wrong conditional value; membership is not certified.
- Four constructed contradictions are empty. Dependent twins and a deterministic structural replay are explicit: these are **not 40 independent random draws**.

[Detailed results](RESULTS.md) · [Independent release review](INDEPENDENT-RELEASE-REVIEW.md) · [Custody](CUSTODY-AND-INDEPENDENT-AUDIT.md) · [Raw analysis](validation-analysis.json) · [Resource accounting](RESOURCE-SUMMARY.json)

## Reproduction and preserved history

The [complete development/validation archive](development-and-validation-evidence.tar.gz), [archive receipt](ARCHIVE-RECEIPT.json) and [original/public provenance map](PROVENANCE.json) preserve separate development and validation namespaces. Rejected hybrid results, wrapper defects, the root-invocation exit 137 before any seed, exactly one subsequent valid draw, and post-release reporting failure remain visible. No failed scientific draw was discarded. Computational sources, data and measurements remain unchanged.

After extraction, run `python verify_public_package.py` from the bundle root for static hash/provenance verification only. The archival audit command documented in the validation README runs **from validation/**, in a fresh copy; it is a replay, not new blind evidence. Five receipt copies redact execution/custody paths, with original/public hashes and reasons. Historical manifests/seals retain original commitments; the old workspace verifier is under validation/historical and is not the public-package verifier.

Top-level completed validation stages consumed **148.455768 CPU seconds before packaging**; nested costs are already included and must not be added again. Later package verification has separate receipts. The independently reviewed resource topology and its retained failures are in the archive.

## Decision

Both implementations return exact marginal masks, feasibility and a supporting sparse witness per admitted value, with matched timing boundaries. v2 does not extract information the complete CRT baseline misses, and its recovery fraction must not be compared with v1’s different cohort as an algorithmic recovery improvement.

Retain this version and its losses unchanged. Projection-saturation development is a separate design review, not a prototype, fresh validation or target result. Any implementation requires its own scope, proof review, freeze and new independent controls. See the single [canonical queue](../../HYPOTHESES.md); no target model is admitted.
