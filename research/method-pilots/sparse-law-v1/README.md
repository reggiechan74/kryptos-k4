# Sparse modular-law inference: synthetic method pilot v1

**Exact model-conditional prediction passed; model membership and K4 recovery did not.** This is an original model-specific application/combination of established tools, not a numbered cipher hypothesis, globally new invention or separate product repository.

## Result at a glance

- **40/40** exact marginal-projection comparisons agreed; the independent audit also verified the join’s factorized relation.
- In **28 in-family** cases, zero false forced values: **1,510/1,876 unknown modeled positions** forced versus **219** for the dense baseline. **12/28** cases determined all **67 unknown modeled positions**.
- The **first six positions are outside the model**. No full 97-letter recovery is claimed.
- Four deliberately misspecified observational twins each produced **one wrong conditional prediction** despite fitting all observations. Model membership is not certified.
- **12 plain expansions hit the declared cap**; they remain incomplete, not negatives.
- The common-support CRT oracle is preferred for the needed projection task. It was faster in **33/40** recorded workloads: **49.322 CPU seconds** versus **66.554** for the join. **The join also serialized a factorized relation; the oracle's primary delivered output was marginals/witnesses.** These are end-to-end workload observations, not a universal algorithm ranking or an equal-output speed comparison. No join speedup is demonstrated and v1 is not retrospectively retimed.

[Detailed results and original timing breakdown](RESULTS.md) retain ambiguity, witness replay, blinding and limits. [Independent publication review](INDEPENDENT-PUBLICATION-REVIEW.md) verifies the retained evidence and public claims.

## Model and evidence

The synthetic model uses 31 fixed features of six preceding ciphertext symbols, at most three nonzero coefficients modulo 26, and 24 observations within **91 modeled positions (6–96, zero-based)**. It is nonlinear in observed history and linear in unknown coefficients. All inputs are synthetic; no K4 ciphertext or crib letters were used.

The [complete evidence archive](synthetic-pilot-and-future-design-evidence.zip) contains code, frozen development artifacts, one truth-blind 40-case bank, sealed original outputs, explicitly released seed/labels, independent audit, and the separately labeled capped repeat. [Archive receipt](ARCHIVE-RECEIPT.json) and [public provenance/redaction map](PUBLIC-PROVENANCE.json) identify exact bytes. See [reproduction and verification](REPRODUCIBILITY.md).

**Resource deviation:** the original independent audit parent lacked hard caps and peak-RSS measurement. Its original receipt remains. An unchanged, externally capped **post-label-release repeat** passed at **125.239946 inclusive CPU seconds / 120,436 KiB peak RSS**. It is verification after release, **not fresh blind evidence**, not replacement timing and not measurement of the missing original peak. The full work is conservatively charged **600 CPU seconds**.

## Current result versus future design

The separately reviewed [global-function quotient/support-cost argument](FUTURE-QUOTIENT-DESIGN.md) and [parity-first design](FUTURE-PARITY-FIRST-DESIGN.md) contain design and toy mathematical checks only. They are **not implemented-v2 performance, a fresh v2 holdout, a v1 protocol change or a K4 result**. A future implementation needs a separate freeze and fresh unseen validation with explicitly identical primary output contracts. Do not retune v1 on its revealed cases.

Finite-field elimination, CRT, meet-in-the-middle joins, sparse inference and function quotients are established foundations. The useful local work is exact conditional prediction and a checked model-specific combination—not a claim to have invented those foundations. Primary mathematical sources and scope comparisons are linked in the future-design reports.

The [canonical queue](../../HYPOTHESES.md) retains the user's focus on genuinely original tactics. This pilot supplies a measured lesson, not target admission or an excuse to repeat attempted cipher families.
