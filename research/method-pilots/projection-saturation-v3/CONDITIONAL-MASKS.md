# Exact conditional masks and completion status by stratum

All four arms return the same exact scalar masks. These are conditional predictions under the fixed sparse model, **not comparative recovery gains**. The 24 observed positions are excluded below; each case requests 67 unknown positions (zero-based 6–96 except the fixed observations). Counts are per case, not repeated-run successes.

| Stratum | Cases | Feasible | Forced unknowns min / median / max | Wrong forced truths | Hidden truths outside masks |
| --- | ---: | ---: | ---: | ---: | ---: |
| ordinary | 16 | 16 | 54 / 67 / 67 | 0 | 0 |
| constant | 3 | 3 | 67 / 67 / 67 | 0 | 0 |
| periodic | 3 | 3 | 67 / 67 / 67 | 0 | 0 |
| binary | 3 | 3 | 67 / 67 / 67 | 0 | 0 |
| even | 3 | 3 | 67 / 67 / 67 | 0 | 0 |
| zero-law | 4 | 4 | 63 / 66.5 / 67 | 0 | 0 |
| contradiction | 4 | 0 | 0 / 0 / 0 | N/A (no planted truth) | N/A (no planted truth) |
| misspecified | 4 | 4 | 67 / 67 / 67 | 4 | 4 |

The four contradiction controls have certified empty masks; their zero forced values must not be treated as failed recovery. Every in-family hidden truth is contained in its mask. The four misspecified twins retain exactly their source inputs and each force one wrong hidden value at position 6. A singleton is conditional on the model, not proof that the hidden truth follows that model.

## On-arm completion rates

Both methods have identical per-case statuses in all three repetitions. Off always enumerates its fixed support traversal.

| Stratum | Cases | Saturated | Dense-UNSAT rejection | Exhaustive completion |
| --- | ---: | ---: | ---: | ---: |
| ordinary | 16 | 0/16 | 0/16 | 16/16 |
| constant | 3 | 3/3 | 0/3 | 0/3 |
| periodic | 3 | 3/3 | 0/3 | 0/3 |
| binary | 3 | 1/3 | 0/3 | 2/3 |
| even | 3 | 0/3 | 0/3 | 3/3 |
| zero-law | 4 | 0/4 | 0/4 | 4/4 |
| contradiction | 4 | 0/4 | 4/4 | 0/4 |
| misspecified | 4 | 2/4 | 0/4 | 2/4 |

Overall on-arm counts are 9/40 saturation (22.5%), 4/40 dense rejection (10%), and 27/40 exhaustive completion (67.5%). Of the nine saturation cases, two are dependent twins; the seven independent in-family saturation cases comprise three constant, three periodic, and one binary trace. There are no failed, incomplete or cap-stopped stages among the 480 planned stages.

## Explicit dependent-twin errors

| Twin | Position (zero-based) | Exact allowed value | Hidden true value |
| --- | ---: | ---: | ---: |
| ordinary-w0-0-misspecified-twin | 6 | 20 | 21 |
| ordinary-w3-0-misspecified-twin | 6 | 16 | 17 |
| constant-0-misspecified-twin | 6 | 16 | 17 |
| periodic-0-misspecified-twin | 6 | 3 | 4 |
