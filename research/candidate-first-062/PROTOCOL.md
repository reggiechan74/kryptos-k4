# Study 062 protocol — ciphertext-steered Josephus

## Model and finite domain

Alphabet A is AZ or KRYPTOS; initial selected slot s=0..96; fixed direction d=+1 or−1. At emission t remove the selected surviving plaintext slot i and emit C[t]=A[(rank_A(P[i])+K[t mod p]) mod26], p=1..8. After removal, cursor first becomes the next survivor in direction d, then advances 1+rank_A(C[t]) more surviving slots in that same direction. Stop after the last removal. No direction alternation, alternate steps, reset, padding, new alphabets or extra layer. There are 388 route-generating descriptions and 3,104 route/period descriptions, not that many independent keyed functions.

The observed ciphertext determines the entire removal map. At each known plaintext slot, its emission t requires one residue K[t mod p]. Inconsistent requirements reject the case; otherwise return the exact key cylinder. Free residues remain explicit. Public plaintext clue positions do NOT guarantee coverage of all emission-key residues. Neither uniqueness nor a fully specified key is an admission requirement. Do not sum overlapping nominal-period cylinder volumes as a union count.

## Prior-work gate

Before target admission, compare the actual 388 target-induced maps, alphabet roles, emission-index key domains, stage order, bounds and threshold/completion scope against inspected local and external coverage. Deriving maps is allowed preflight; solving target clue constraints is not. Skip covered cells with exact receipts. Unknown potentially subsuming scope blocks eligibility. Width96/97 all-order columnar supersets may intersect but are not established completed exhaustive prior coverage.

The all-zero key is already excluded by the local pure-transposition E-count proof. Target output therefore represents cylinders minus the zero vector: subtract one from cardinality only when every fixed digit is zero and omit a zero-only singleton. Record excluded_zero_key explicitly. Generic synthetic benchmarks test the full mathematical model, including zero vectors. No other constant-key domain is silently excluded.

## Correctness and performance calibration

An independent linked-circle implementation is authored before production's alive-list implementation is inspected. Tiny exhaustive forward-generated truth must match complete cylinders, including free residues and both directions/every start. Separate deterministic synthetic checks cover all 3,104 full-domain settings before freeze, without any K4 input. A synthetic per-case union timing justifies the fixed budget; it is not reused as a held-out case.

## Fresh blind benchmark: 872 cases

Generate a fresh 256-bit seed only after code/protocol/eligibility freeze. Shuffle opaque IDs; engines receive ciphertext and crib maps only. Seal both complete output files before reading answers.

- 776 full-mask plants: for every alphabet index a=0,1, start s=0..96, direction index j=0,1 (directions +1,−1), generate one uniform (b=0) and one literal-crib (b=1) random plaintext/key. Period is 1+((s+3*j+5*a+4*b) mod8). Clues occupy the canonical 24-position plaintext mask; literal letters are the public crib concatenation. Text outside those clues is random, not English.
- 32 sparse plants: each alphabet and k=0..15, start=(7*k) mod97, direction +1 for even k and−1 for odd, period8. Encrypt a random plaintext/key; choose plaintext clue slots removed at emissions0,8,16,24. The planted cylinder must retain exactly seven free residues. Mask selection intentionally tests ambiguity, not general recovery difficulty.
- 64 matched full-mask null controls: independent uniform97 ciphertext;32 independent uniform clue assignments,32 literal clue assignments. No rejection sampling or fixture regeneration.

Admission gates: all872 complete cylinder sets agree exactly; every plant's setting/key is contained; every full singleton candidate re-encrypts; for each returned free cylinder, test canonical zero-filled completion, all-free-ones completion, and one-at-a-time free digit1. These probes are controls, not proof of completeness; exact residue equations and tiny forward truth supply that proof. All32 sparse planted cylinders have seven free residues. At most one of64 null controls may have ANY fit across all3,104 cases. Unique plaintext recovery is descriptive only. No post-outcome gate changes.

## Resource and freeze rules

Whole study28,800CPU seconds/8GiB maximum, including route audits, benchmark and independent checks. Each sequential engine batch180CPU seconds/300wall seconds/512MiB address space. Charge measured costs plus explicitly conservative reserves for unmeasured setup; do not invent RSS. Preserve failed commands, incomplete outputs and original receipts. No paid services or execution of untrusted external programs. Parent independent-audit approval precedes exactly one production and one reference K4 pass. Separate additive target transport freeze, output seal and non-search final audit follow. Third-party source contents remain private unless redistribution rights are verified; publish URL/pin/hash inventories and our own comparators.

## Stop and next decision

An empty complete eligible union excludes only this finite family. A compatible/free cylinder is not a K4 solution. Do not alter step count, key indexing, update order or direction after a negative. Coordinator reconciles canonical local/external ledgers before choosing the next family. Record measured bottlenecks and retained validation methods; do not claim established mathematical techniques as globally novel inventions.
