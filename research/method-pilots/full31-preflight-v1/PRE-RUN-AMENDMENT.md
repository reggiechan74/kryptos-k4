# Explicit pre-run beta accounting clarification

The accounting clarification was approved on October 31, 2026, before any pilot run.
The original proposal remains immutable at SHA-256
cdd02be85e643b4226eb4a58bb7eade35f8d28108ea979ba82f87765025c7c0a.

The proposal requires beta-list generation and independently recomputed serialized
beta lists. Accordingly its 35,264 beta / 846,336 parity-row ceilings are now
explicitly separate generation and audit counters, each with those ceilings.
The combined maxima are 70,528 candidate instances and 1,692,672 parity row tests.
Both passes debit the same unchanged 50,000,000 logical-work counter and same
20-second per-control wall cap. The unchanged stage allocation is 320 CPU seconds.
No GF2 alternate solver, pruning, early parity-row skipping or cache is introduced.
No other cap or traversal changes are authorized by this amendment.

Preparation expands only the fixed public B recurrence and all public outputs;
it performs no solver, rank, workload, mask or semantic computation. Preparation,
source review, hashing and final-write tails are unmeasured, not zero CPU.
