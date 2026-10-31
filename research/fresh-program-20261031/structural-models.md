# Fresh structural K4 hypotheses — 2026-10-31

Research only. No target experiment, synthetic experiment, or repository modification performed. Comparison baseline: reggiechan74/kryptos-k4 c860d9a47455478f2b64b595be7d404cbf57533d, HYPOTHESES.md and EXTERNAL-PRIOR-ART.md, and pinned public-survey caches. These are unlocated exact mechanisms in the inspected material, NOT claims of worldwide novelty or of Sanborn intent.

## J: Ciphertext-steered Josephus removal

Alphabet A is AZ or KRYPTOS-keyed alphabet, ranked 0..25. Key K has period p in 1..8 and digits 0..25. Place 97 plaintext positions in a circle. Choose start s in 0..96 and fixed direction d in {clockwise,counterclockwise}. At output time t, remove the slot at the cursor, emit C[t] = A[(rank_A(P[slot])+K[t mod p]) mod 26]. Unless this was the final slot, cursor first becomes the next survivor in direction d, then advances 1+rank_A(C[t]) survivors in that direction, modulo the remaining list length. No padding, no per-position step key, no unspecified final-state handling.

Inverse: using the observed C and parameters (A,s,d), reproduce each removed slot; subtract K[t mod p] from C[t] and place the recovered letter in that slot. Thus exactly reversible. Unlike fixed-route composition, encrypting different messages with the same key generally changes the permutation itself.

Finite pilot: 2 alphabets × 97 starts × 2 directions × 8 periods = 3,104 structural cases. Key digits need not be enumerated: each known plaintext position, mapped to its emission t, requires a specific value of K[t mod p]. Reject a case immediately on inconsistent repeated requirements. Unconstrained key residues must be reported, not fabricated into a solution.

Nearest tested cases: Scott C7 fixed-step Josephus k=2..97/all starts with periodic substitution; zeyeteam section16 periodic 1/2/3/4-number alternating-direction dial combinations, section39 artifact-literal steps. These step streams are independent of the message. Our feedback comes from each emitted ciphertext letter and uses a fixed orientation. This is not merely increasing their key bounds.

Preflight stop: find an earlier ciphertext-feedback elimination implementation, or show the realized K4 removal order already belongs to an exhaustively tested route+same substitution/order family; then mark duplicate rather than run. Also test invertibility on planted messages before K4 work, with explicit direction/index conventions. Pure-transposition count and direct periodic-alphabet exclusions do not automatically cover a composed, non-direct model. Existing local 057/058 columnar cases do not cover this elimination operator. If all finite cases fail exact cribs, reject this precise model; do not add alternate step multipliers/feedback layers post hoc.

## B: Sum-locked block rotations

Alphabet A AZ or KRYPTOS-keyed, rank0..25. Apply X[i]=(rank_A(P[i])+K[i mod p]) mod26, p=1..8. Partition into consecutive blocks of width m=3..12; the final block has its actual remaining length l (no padding). For each block, compute r=(sum of integer ranks X in that block) mod l, and rotate the block right by r positions. Render with A. Direction is frozen RIGHT, not an extra knob.

Inverse: block sums are invariant under rotation, so compute r directly from the observed C block, rotate left by r, and subtract periodic key K. This is a bijection for every fixed key. The route depends on the message via its block sums, with no independent per-block offsets. A one-letter final block has r=0.

Finite pilot: 2 alphabets × 10 widths × 8 periods = 160 structural cases. C fixes the unrotation for each (A,m); crib positions then induce key-residue requirements, allowing exact conflict elimination without 26^p enumeration. Report unobserved residues as nonidentifiable. Roundtrip and planted-recovery controls before target testing.

Nearest work: fixed geometric/row/block rotations, columnar+periodic substitution in local057/058, arbitraryfunction two-/three-round Feistel blocks. This is neither a constant route across messages nor an arbitrary fitted nonlinear function: the operator is fixed by a rotation-invariant statistic. Local H-NONLINEAR-BLOCK does not exclude general nonlinear block operators. Exact sum-conditioned rotation was not located in our ledger or targeted public searches.

Preflight stop: inspect any source testing arbitrary independent block rotations at these widths with the same alphabets/periodic key and layer order; that could already contain every realized K4 route even though the proposed mechanism differs. Also reject any rediscovery of this exact sum-lock rule. If all cases violate cribs, retire this bounded model. Do not rescue with arbitrary checksums, width schedules, phase shifts, or another cipher layer.

## Provenance and limitations

Scott pinned NOTES.md, C7:
https://github.com/scott-dunphy/kryptos-k4/blob/a75178587efe9401ebf2a4edf3828472dd6fb2a2/NOTES.md

zeyeteam pinned README.md, sections16/17/39:
https://github.com/zeyeteam-debug/kryptos-k4-eliminations/blob/00696f393c861db2dcfaf3adfef29823c601cf7a/README.md

Public targeted searches included Kryptos Josephus feedback; Kryptos counting-out ciphertext; Kryptos sum block rotation; Kryptos data-dependent transposition; Kryptos checksum transposition; Kryptos block sum; Kryptos plaintext-dependent permutation. No matching K4 test located, but absence from search is not proof. Public repositories sometimes make broad 'arbitrary transposition' claims under model-specific assumptions; those claims must be source-audited before applying to either candidate.

Both are speculative, hand-executable rules. We have no evidence Sanborn used either. They merit finite novelty-gated pilots, not high-confidence claims. Their attraction is an exact new operational dependency with unusually cheap falsification, not extra flexibility.
