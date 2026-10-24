# Why the unknown-anchor collector restriction is sound

This is the proof obligation for [CSP889-COUPLED-024](SIGABA-UNKNOWN-ANCHOR-COLLECTOR-SPEC.md), not a proof of tractability or historical use. The implementation's surviving support is a necessary relaxation; the final persistent-map recurrence determines keys.

## Implicit connected graph

At each observed time in the first consecutive block, the initial layer contains every current cipher state satisfying every disclosed input/output pair at that time. For a mask with signed coordinate increment d, an implicit edge is `u → u+d`. Its source bitmap is `L_i ∩ preimage(L_(i+1), d)`, and its image uses the inverse translation. The exact torus translation convention is tested against point states and independent set-valued graphs. No edge triple need be materialized, and no supplied cipher anchor is inserted.

For a fixed original controller and a reachable static index map h, the actual mask for collector digit set B is a deterministic function of B and h. Initially allowed masks include every such physical value. Any compatible physical trajectory therefore belongs to every initial symbol layer and every initial mask set.

Backward pruning removes a state only if it has no allowed successor; forward pruning removes it only if no allowed predecessor remains. Neither operation can remove a member of an actual compatible path. An actual static map uses the same mask whenever B repeats. Intersecting supported masks across all occurrences of B cannot remove that map's mask. Induction over monotone sweeps proves that every compatible physical anchor remains in the returned root support. Eight sweeps need not reach a fixed point: stopping early preserves a weaker necessary superset, never a stronger rejection. A time/memory interruption instead leaves the whole controller unresolved; no partial support is returned as a proved zero.

Connected support and repeated-mask intersections still do not imply one globally consistent path or one physically reachable map. Different paths/roots can contribute different supporting masks. The filter's false positives are therefore expected; no pass is called a key.

## Exact verification and correlations

The new solver starts the COMPACT-018 recurrence with that controller's necessary anchor restriction. Thereafter it keeps the exact `(cumulative offset, original anchor-domain, persistent reachable-map owners)` relation. Owners split by their actual masks; only equal offsets and equal cipher domains merge. The filter never substitutes independent per-letter masks for h. Consequently every returned key satisfies the original exact model, and the necessary root restriction removes none of its compatible keys. Completed output relations must equal the baseline; incomplete output is unresolved outside its explicitly completed controller prefix.

The observation anchor is a coordinate reparameterization of the unrestricted independent cipher-start torus. The original controller trace begins at time zero. Prefix displacement and original-start reconstruction depend on h; this dependence is retained. Unknown prefix and inter-crib positions are neither reset nor assigned invented plaintext. The filter uses only the first contiguous block as a lookahead restriction; the exact verifier propagates all later times and uses the same h through the gap.

## Validation strength and limits

The complete controls compare bitmaps to independent explicit state-set graphs and the full correlated raw-key stream to an independent physical-contact simulator on declared tiny systems. They retain ambiguous outcomes and plants. Mutation controls expose incorrect common-prefix reconstruction, skipped unknown steps and reversed/disconnected transitions. These tests support the implementation/proof correspondence, not universal empirical error bounds.

Real-sized synthetic plants are independently replayed under the pinned simulator tables. The 12 published vectors are simulator-to-simulator references, not a surviving hardware transcript. Direct plant replay is not blind selector recovery or an independent complete-set oracle at real size. The real-domain admission gate stays separate and cannot pass merely because tiny controls or supplied plants pass.
