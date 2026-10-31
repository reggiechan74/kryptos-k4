# Study 063 findings

## Exact negative, not a recovery success

One approved production pass and one independent reference pass returned **UNSAT_COMPLETE**: no compatible alphabet/period/key/message-start-state/plaintext tuple. This excludes only AZ or KRYPTOS, periods 1–6, all 624 initial states, the exact old-high/new-low readout and no additional layers. Every periodic key in the finite domain is covered by lossless constraints and global replay; this is not a claim to have enumerated every possible key individually.

**All 624 blind plants were ambiguous, and none recovered uniquely.** The passed benchmark establishes complete compatibility/exclusion behavior, not plaintext identification. No English selection or candidate-ranking claim is made. No target-dependent rule changes or extra target runs occurred.

## Model and independent implementation

The state has low digit a in 0–25 and high counter h in 0–23. For plaintext rank x and key digit k, t=a+x+k, a'=t mod 26, output y=(a'+old h) mod 26, h'=(h+floor(t/26)) mod 24. All-zero keys remain included. Equivalently T=26 h+a updates by adding x+k modulo 624, with the nonlinear digit readout using the OLD high digit. This is a scalar modular accumulator, not a new physical gearing invention. The choice 24 is thematic speculation, not a measured clock operation.

Production uses explicit low/high state; independent reference uses the scalar state. Both agree on 46,656 tiny forward/inverse cases, 104,976 complete solver sets and local filters, and 7,488 full-size alphabet/period/start-state direct synthetic settings. Old-high timing and carries 0/1/2 are explicitly checked.

The two clue blocks each cover every key residue for these periods. Enumerating possible entry states forces complete seed keys; intersecting those key sets is only a relaxation. Every retained seed is replayed continuously from all actual message-start states. A tiny reset-trap fixture has a nonempty local intersection at key 2 but no globally reachable solution, independently confirmed by exhaustive forward enumeration. No target state is restarted at a clue.

## Prior-equivalence review

Five external primary sources were verified against exact Git blobs and SHA 256. Actual adjacent carry-noise constraints, fixed linear mod 26 chains, no-carry per-letter digit codes, position-driven odometers/Alberti and clock-alphabet models were distinguished by equations, not titles. A non-executed comment was not counted as coverage. No external code was executed or unlicensed source contents redistributed.

The fixed-alphabet causal-affine separation proof checks the full relabeling argument: after two inputs, reachable states contain an aligned 26-state block and hence all 26 conditional translations. Equivalent fixed input/output alphabet relabelings must be affine units; those cannot erase the native third-output nonlinearity. The proof is not extended to arbitrary nonlinear prefix initializers or set-valued machines.

The local geometric-radix family is itself nonlinear, requiring a separate proof. Its even-glyph parity invariant is contradicted by 104 synthetic reachable state-pair witnesses, independently checked with 2,704 next-key extensions. All 624 states are reachable after 25 input letters for any fixed initial state/key prefix. This supplies a whole-function distinction for that precise prior family, not a target contradiction.

No known whole fixed-parameter alias was found in the reviewed domains. Coincidental finite-message overlap with older set-valued carry-noise constraints remains possible; this is not a universal pair-disjointness or worldwide novelty theorem.

## Fresh benchmark and identifiability

The fresh 688-case holdout contains one plant for every initial state, with a frozen balanced assignment giving 26 plants in each alphabet/period/uniform-literal cell, plus 64 matched nulls. Both complete output files were sealed before answers. All 688 sets agree, all 624 true tuples are retained, 55,263 returned parameterizations exactly re-encrypt, and no null has any compatible tuple.

Every plant retains 8–126 distinct plaintexts. Separately labelled post-reveal analysis of the sealed outputs, independently verified, finds:

- 63 cases vary only at plaintext position 0.
- 424 additional cases vary only within the pre-crib prefix, positions 0–20.
- 137 cases also vary at later unknown positions.
- Across cases,1–34 positions vary.
- All 624 cases have same-key first-letter-only alternatives that reach the identical post-first state.

Per-case key groups, initial-state counts, varying positions and pre-crib convergence are retained. These are observed descriptive results, not a universal alias theorem. One structural ambiguity source is that different valid initial-low-digit/first-plaintext pairs with the same integer sum and fixed high digit/key emit the same first symbol and enter the same next state. Later clues cannot distinguish those alternatives. Neither a chosen plausible sentence nor an arbitrary representative parameterization solves this identification problem.

## Costs and next research decision

Production/reference benchmark costs were approximately 11.367/39.743 CPU seconds; candidate analysis used 3.493 seconds. Independent audit and all source/control/diagnostic costs are separately recorded. Calibration changed the proposed benchmark size before freeze, not its correctness or null gates. No search-speed bottleneck appeared.

Close this bounded family and reconcile the canonical ledgers. Further useful research must bring a genuinely different prior-art-cleared mechanism or independent evidence addressing initial-state/identifiability constraints. Nothing here justifies tweaking readout timing, adding resets, enlarging moduli, rerunning old families with a stronger solver or introducing an English scorer. The retained improvements are exact local-filter/global-reachability validation, scoped prior-family proofs and explicit identification diagnostics—not a claimed new cryptanalytic invention.

## Preserved audit correction

The first non-search target auditor assumed an explicit `blocks` field in the input. Both unchanged frozen engines legitimately use the exact canonical default blocks when that field is absent. The auditor assumption was corrected, with its original script and failure receipt retained. No target data, solver, frozen file or output was changed, and no additional target search was performed.
