# Independent preimplementation oracle design

Validation class: fresh synthetic. No historical ciphertext, crib values, key arithmetic or schedule generation.

For n=1..5 enumerate every set partition (restricted-growth strings). For each candidate partition, enumerate all binary value assignments to its blocks; materialize only synthetic vectors of n residues. The old unrestricted equality-model contains this candidate iff every materialized candidate vector satisfies all old same-block equalities. Compare this independently derived relation to the implementation's implication decision. Include label renamings to test that numerical labels are not mistaken for key values.

Adversarial metadata: equation/sign/q/alphabet role/order, alignment, normalization, coordinates/order/duplicates, unknown status, heuristic or skipped status, zero outcome, restricted old domain, malformed JSON booleans, absent rows, wrong hashes, deliberately free old partition without a completed contradiction. These must reject or report ineligible, never transfer a negative. A free partition may structurally contain everything but cannot inherit exclusion from mere existence.

Trusted-boundary review: hashes pin bytes, not truth. 044 completeness is inherited from the reviewed exact analytic specification and completed original receipt; no claim to rerun/prove solver correctness. Candidate partition correspondence to a proposed mechanism remains independent semantic review unless separately source authenticated. No output asserts full-message equivalence.
