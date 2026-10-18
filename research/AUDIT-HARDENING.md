# Focused audit hardening

18 October 2026. This change responds to the independent audit of commit
b83b0f9259ce000160032e55eed8d05d30a0037b. No broader search is authorized or run.
The original input data, raw results, hashes, source receipts, and provenance
remain intact. An explicit checksum manifest preserves all audited result bytes.

## Interpretation and historical-record corrections

All 282 ROUTE-001 fits are vacuous: 47 periods × 2 alphabets × 3 equations.
Every known crib position is in a distinct key phase, yielding zero repeated-
phase comparisons. Arbitrary values at those positions can be fitted. This gives
no evidence for extending searches at those periods or interpreting a key.
The hardened scanner now labels `vacuous_fit` and the exact count of independent
repeated-phase comparisons in each compatible record. Original artifacts are
not rewritten to add the labels; replay tests independently check the deduction.

The original 20 route controls supplied true parameters to `constrain`, at
period 4 and route indices 0–19 only. They did not recover models through the
full scanner. The earlier experiment-log statement is corrected. The original
literal running-key controls did use the real scanner for forward windows.

The original specification and results entered the same commit. Repository
history does not independently prove preregistration. For future new experiments,
commit the specification before execution and reference that commit in results.
The offline runner requires a full specification SHA, records the spec file hash,
and states that existence, contents, and chronology require a Git-history audit.
A caller-supplied SHA alone is not evidence of prior registration. Replaying the
already committed b83 specification is explicitly a replay of existing scope.

## Added validation

- Independent hand-arithmetic vectors distinguish substitution-before-route
  from route-before-substitution for all three modular equations.
- Actual `route_scan` recovery plants periods 1 and 16, both operation orders,
  both fixed alphabets, and a route beyond the former first-20 subset. A separate
  period-96 case checks incomplete phases, vacuous-fit labeling, and absence of
  fabricated plaintext for unknown phases.
- Reversed contiguous running-key windows are recovered through `running_scan`
  for both alphabets and all three equations.
- All original route assignments, running-key counts/histograms, Trifid results,
  all 9,999 statistical null draws, calibration values, evaluation maxima, and
  tail estimates replay against the immutable artifacts. No search bounds expand.
- Failure injection exercises initial and final deadlines, including Trifid,
  statistics postprocessing, and the runner's final check after output staging.
- Atomic-publication tests cover successful output, a subsequent timeout with no
  stale success pointer, invalid-baseline preflight, and byte preservation.

## Runner behavior

The runner checks the baseline schema and verified ciphertext SHA256. Every
scanner checks its declared deadline initially, during work, and before return.
The runner checks again after computation and after staged serialization/writes.

Each attempt receives a unique run ID. Result bytes and manifest are staged in
a hidden directory; one directory rename publishes a completed snapshot. Each
file and the latest-status pointer use atomic replacement. On a caught failure,
new result artifacts are removed and only an incomplete manifest is published,
with outcome/error type and no completed artifacts. The latest pointer is marked
running at attempt start, so the preceding successful run cannot appear to be the
latest attempt. Old audited artifacts and prior snapshot directories are untouched.
A sudden process kill can leave pending/running state; consumers must never treat
that as completion. A disk failure can prevent recording status, but cannot turn
an unpublished pending directory into a completed snapshot.

## Worksheet provenance reconciliation

The supplied [independent worksheet review](../docs/k3-worksheet-verification.md)
is incorporated and the designer-context report is qualified accordingly. The
K3 method remains a fully verified 336-letter algorithm and a worksheet-supported
reconstruction. It is not a complete observation of the original paper procedure.
The audit checks both coordinate directions at every position, three anchor
mappings, terminal Q at ciphertext index 144, and the two readable intermediate
rows. No K4 route dimensions are inferred and no search scope expands.

Final validation: all **45 tests pass**, including full replay of the 9,999
archived null draws and failure-injected atomic-publication checks. No original
artifact changed and no result-changing bug was found. A CLI smoke test exercised
new snapshot publication in a temporary output directory; it tests I/O behavior,
not the historical existence or byte identity of a caller-supplied spec reference.
The offline reference/chronology limitation remains explicit.
