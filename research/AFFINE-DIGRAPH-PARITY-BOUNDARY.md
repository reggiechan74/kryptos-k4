# Adjacent affine digraphs — analytical exclusion, not an unrun search

23 October 2026 UTC. The four specified same-alphabet adjacent affine-digraph
models are contradicted by exact parity witnesses in the first English crib.
No matrix/key search is needed or was run. Earlier backlog labels calling this
recipe unrun are superseded by this note.

The old proposal is `C_pair=M*P_pair+b mod 26`, with one fixed 2×2 matrix and
2-vector offset, same AZ/AZ or KRYPTOS/KRYPTOS coordinates, and either adjacent
pair origin. Reducing modulo 2 gives a fixed affine function on input parity.
Identical input-parity vectors must therefore give identical output-parity
vectors. The witnesses below disagree. Invertibility is unnecessary for this
exclusion, so the original invertible-matrix subset is excluded too.

| Coordinates | Pair starts, one-based | Plain pairs | Cipher pairs |
| --- | --- | --- | --- |
| AZ, odd origin | 25 / 29 | TN / TH | VQ / RN |
| AZ, even origin | 22 / 32 | EA / AS | FL / KS |
| KRYPTOS, odd origin | 27 / 31 | OR / EA | QP / GK |
| KRYPTOS, even origin | 22 / 26 | EA / NO | FL / QQ |

Every row has equal input parity and unequal output parity. Positions and all
letters were independently checked against the unchanged canonical fixture.
Only complete internal pairs are used, so copying the sole edge symbol cannot
repair a contradiction. The original frozen DYNAMIC-KEY specification remains
unchanged as a historical proposal; current status is analytically excluded.

The parent supplied these exact witnesses, and an independent gap review is
checking them separately. The [local result](../results/AFFINE-DIGRAPH-PARITY-001.json)
contains actual parity vectors. [Verification code](../experiments/affine_digraph_boundary.py)
performs no search. Sixteen fixed affine positive cases, including singular and
nonunit-determinant matrices, have consistent parity; sixteen output-parity
mutations are correctly rejected.

This is not an exclusion of all polygraphic ciphers, mixed input/output alphabets,
phase-dependent matrices, reordered pairs or a different preprocessing layer.
Those would be different models. A stale unrun label must not promote this
already excluded recipe as a wholly new strategy.
