# Clock-key/reset preparation: synthetic controls only

18 October 2026. The frozen specification is pending. No new K4 execution is
authorized before its specification commit, and none has been performed here.
KRASNOJARSK is an exploratory clock-key observation; BERLINCLOCK remains the
confirmed plaintext at positions 64–74. Modern panel orientation and 1989
inscriptions remain unverified; see the [supplied report](../docs/neptune-discovery-assessment.md).

## Existing exclusions to avoid duplicating

The supplied reviewer check identifies ROUTE-001's identity route as having
already tested periods 1–96, A–Z/KRYPTOS and three modular equations. Its only
survivors are periods 27–29 and 53–96, all vacuous. Therefore continuous
fixed-alphabet period 11, including literal KRASNOJARSK or BERLINCLOCK at any
phase, is already excluded within that arithmetic family. Repeating these keys
would not be a new result. See [bounded findings](BOUNDED-FINDINGS.md).

Period 11 surviving the weaker arbitrary-bijective-substitution equality test
is a different model, not a contradiction: arithmetic shifts are a restricted
subset of bijections. See [structural findings](STRUCTURAL-FINDINGS.md).
The earlier 12 autokey failures likewise concern only their stated uninterrupted
models. Shared-key resets are not automatically eliminated by those tests.

## Control preparation and remaining gate

`tests/reset_control_reference.py` is an independent, synthetic encoder. It
does not load the K4 baseline or contain a K4 scanner. Resets occur before a
specified zero-based index, restart the same key at index zero, and reject
duplicate/unsorted/out-of-range/ambiguous schedules rather than normalizing them.
This convention is control preparation, not the pending experiment specification.

Four preparation tests supply two hand vectors, 24 seeded synthetic checks
(two alphabets × three equations × four schedules), segment-wise inverse recovery
and full regeneration using the existing primitive, shifted-boundary negatives,
and invalid-schedule rejection. Seed: Python MT19937 20261018. Some synthetic
schedules exercise indices 21/63; their texts are random and contain no actual
K4 plaintext or ciphertext. No search parameters are inferred from these tests.

After the reviewer supplies and commits the frozen specification, the actual
scanner must be tested end-to-end against independently encoded plants for every
specified case, including altered-crib and wrong-boundary rejection. These
preparation tests do not yet establish scanner recovery. Any actual experiment
must retain all canonical crib letters, full forward regeneration, hard case and
time limits, exact negative-result scope, and prior specification provenance.

Subsequent reviewer steering supersedes the proposed scanner: an exact
[identical-reset bijection contradiction](CLOCK-RESET-PROOF.md) makes the shared
keyword scan redundant. Its implementation/regressions are prepared but await
the final frozen proof specification before execution. No new variants are added.

Final reviewer specification subsequently arrived as CLOCK-BOUNDARY-REG-001 and
was committed at 4e2d002925bfc7f3b332f94cd4472617919f52fa. It requests known-witness
verification only: no scanner or candidate-key trial. The pending language above
records the earlier preparation stage and is superseded by that exact specification.
