# C20 synthetic pilot — independent static source/protocol review

**PASS, finite static scope. The definition, implementation, independent tiny oracle and one-shot corrected execution contract agree. No synthetic batch or K4 test has run under this review; root execution authority is still required.**

## Reviewed freeze

Root: `<original-source-root>`.

Final `FREEZE.json` SHA256: **3ecdaf1c4191a45bc37a2cb7e907f149e7ccf68c680313b6ba5b0b0ab60134c1**. It differs from the reviewed draft only by the planned `FROZEN_NOT_EXECUTION_AUTHORITY` status. All four source/document pins and both executable pins were independently checked:

| File | SHA256 |
|---|---|
| c20.py | bf2534a63b51952bab38afac973f35411bbedc6c9055e8181eb060cb10013867 |
| pilot.py | 7c1f7c7cff307d9cb37e87bbd710fd30d83eebf63952168d7f3bef8256c96c7f |
| run_once.py | 146d9b6b5041348f5e9bdf570f5ae808ce086a7f9804eb0f8e8295d9ee459fdb |
| PROTOCOL.md | ec8b9d3ba875f6c675072c47c6fec2b4ac39617133aaef133cbee6130fb30fe3 |
| Python executable | fa67443527ed9647f760d807e2a38f26340757123e643c4639cf273ed15d5ea7 |
| /usr/bin/timeout | 6ca1891dfc0b05d7680770c2884c0391b92467c7bb6500a5c84677e6481739f1 |

Admission report reviewed: `ADMISSION-AUDIT.md`, SHA256 **39f3b6d25981b7f8adcde8f371cf0698ed0502b67876fbbe08196ee8fa8126c9**. This review independently checks the mathematics/source below; it does not repeat the prior-art search or strengthen its finite coverage into worldwide novelty.

## Mathematical and implementation review

For an input trail ending at t, the last outgoing edge from each visited vertex v other than t forms a directed tree toward t: along a selected edge not yet reaching t, the last departure time strictly increases. Preserving those last exits while reordering earlier successors therefore retains a valid last-exit tree, including for closed trails, loops and repeated edge labels.

A greedy traversal cannot become stuck at a nonterminal vertex: its residual outdegree exceeds its residual indegree there. If it stops at t with unused edges, the residual graph is balanced. Vertices with unused outgoing edges form a nonempty set closed under the retained last-exit edges, contradicting their paths to the exhausted t. Consequently every edge is consumed and the endpoint stays t.

The output's successor lists are precisely the transformed lists. Reversing every nonterminal prefix and the complete terminal list twice restores the original ordered lists. Starting at the same first symbol reconstructs the original word, so T squared is identity. Length, endpoints and directed-bigram counts are preserved; unigram counts follow from outdegrees plus the terminal symbol. The implementation directly implements this rule and explicitly rejects premature termination, wrong endpoint or unconsumed queues. Empty/singleton conventions and strict built-in integer/alphabet checks are consistent with the declared synthetic domain.

The outer fixed A=0 additive KRYPTOS map uses `(i+phase) mod 7`. Encryption adds after T; decryption subtracts before T. The literal ranks `(10,17,24,15,19,14,18)` and phase bounds0..6 are correct. This yields an inverse pair, not evidence of an intended historical cipher. The graph argument is classical last-exit/Euler-trail mathematics, closely related to BEST and dinucleotide-preserving shuffling/uShuffle; this audit does not call it a newly invented graph theorem.

Hand fixtures agree with the rule: ABACAD maps to ACABAD, and the closed ABACA maps to ACABA, with reverse fixtures also checked. The isolated broken all-queues-reversal control for ABAC reaches AC with two edges unused, so it discriminates the missing last-exit reservation rather than falsely testing the proposed rule. The length97 witnesses x=ABACAD+91D and y=ABECAD+91D establish non-equivalence to a fixed position permutation: x forces output position1 to use input position3 (its unique C), while y's output position1 is B although its input position3 remains C. Constant-word fixed points also rule out rescuing that representation with fixed coordinate symbol maps.

No mathematical or algorithmic defect was found in the reviewed source.

## Independence and exact finite coverage

The tiny oracle enumerates every word once for each fixed alphabet/length, independently computes its `(start, ordered successor lists)` signature, checks uniqueness, and looks up the prescribed transformed signature. It never uses production `transform`, its greedy walk, or its helper to construct the expected output. Shared mathematical specification is unavoidable; the implementation of reconstruction is genuinely different. Missing or duplicated signatures fail explicitly. Empty input has its own sentinel.

The declared counts are exact:

- q=2, lengths0..10: 2,047 cases.
- q=3, lengths0..8: 9,841 cases.
- q=4, lengths0..6: 5,461 cases.
- Total: **17,349**, including overlapping words across alphabets; not17,349 statistically independent observations.

Every tiny case checks oracle equality, involution, length/endpoints, unigram and directed-bigram counts, and retained nonterminal last exits. Four literal directional fixtures, the broken naive control and two length97 witnesses are separate. Malformed-input checks contain exactly16 cases (seven q-values and nine word forms); malformed-phase checks contain12 (six phases through each of encrypt/decrypt). Their required exceptions match the production API.

The 13 literal97-letter plants and seven phases give exactly **91 plant/phase pairs**. The full-alphabet reference uses independently written tuples/dictionaries but the same guided-walk construction; it is not misrepresented as a second enumerative oracle. Checks cover all97 letters, independently formed additive outputs, inverse recovery and re-encryption, not only round-trip self-consistency. The single-letter known answer anchors the alphabet/key convention. Seven phase ciphertexts per fixed plaintext are distinct because the seven key symbols differ already at position0. No observed distinctness count or fixed-point count is an inferential success score.

These are disclosed deterministic correctness fixtures, not blinded plants, null calibration or a target sample. The source's diagnostic phrase “hidden plant recovery” does not change their disclosed status. No K4 source/crib, language scoring, random generator, key search or queue-order fitting is imported. No mode-sensitive assert-only check was found; one normal batch is sufficient for this declared pilot, without adding an unapproved second mode or test battery.

## Bounded one-shot execution contract

The final freeze pins the exact outer template:

`/usr/bin/timeout --signal=KILL 120s <pinned Python> -I -B <source root>/run_once.py --freeze-sha256 <FINAL_FREEZE_SHA256> --approval-sha256 <ROOT_APPROVAL_SHA256>`

Only the two typed hashes may be substituted. Parent should authenticate the timeout/Python/source pins and retain the actual argv and actual external terminal result. The source freeze itself is not a grant.

The supervisor binds the outside-root approval to this freeze and `C20-synthetic-once`, requires an empty run directory, and creates exclusive ATTEMPT before the sole child launch. Any attempted failure, cap, missing receipt or uncertain external completion remains consumed/incomplete and cannot authorize retry. Durable parent conversation consumption protects against disposable-directory loss; local emptiness alone cannot reopen a spent permission.

The sole pilot child has CPU58, address space128MiB and per-file1MiB limits, and no child launches of its own. The supervisor has soft CPU2/hard60 with default SIGXCPU so its forked child can install hard58; this is deliberately not mislabeled a physical supervisor hard2 limit. Both process usage and OS signal timing are subject to accounting granularity. Child waiting is bounded to the remaining115-second inner deadline; pinned GNU timeout supplies the120-second external kill. The child parent-death guard/race check prevents it surviving a killed supervisor. Failure cleanup kills/reaps an active child; a missing final receipt is fail-stop, not success.

Two prefreeze operational findings were corrected without changing scientific/oracle bytes:

1. The120-second external limit now has an exact pinned timeout binary/argv, not merely a metadata number.
2. Final PASS now checks child CPU≤58, cumulative supervisor CPU sample≤2 and wall sample<120. Supervisor sampling includes startup and artifact hashing. Receipt serialization/fsync/hash/final print and outer timeout/tool overhead remain explicitly unmeasured, not claimed zero.

Source bytes are authenticated before the production module is compiled/executed; no local bytecode module cache is used. The trusted Python standard library/runtime is not claimed separately frozen. Pre/post source seals and expected count checks supplement, rather than replace, independent result review. The three pre-receipt artifacts plus the capped final receipt fit below10MiB; a process killed before receipt creation remains incomplete.

## Verdict, resource scope and next gate

**Static PASS with no remaining source blocker at the pinned final freeze.** Final readback found no approval or run directory. No prepared module was imported/executed, no synthetic case was run, and no K4 data was read by this reviewer. Only source reads, AST parsing, byte hashes and fixed-count arithmetic were used.

Static metadata processes sampled0.424263835 +0.088130944 = **0.512394779 CPU seconds**. Startup/shell/manual review/report-writing overhead is unmeasured within the separately reserved60-second preparation/review allocation. This does not consume the pilot's60-second one-use permission. The parent120 allocation remains60 pilot +60 preparation/review, not permission for extra batches. External timeout/tool overhead must remain disclosed rather than added twice to inner samples or asserted to be zero.

Root must still issue the exact finite execution grant and record the consumed attempt before the batch. A clean final external exit, matching output/receipt/source seals and independent read-only outcome review are prerequisites to calling the pilot successful. Any mismatch, resource exhaustion or uncertainty stops; no retuning or automatic retry. Even a synthetic PASS would only support a **separate** future decision about the seven fixed target decoders, not target admission or a claim that re-encryption proves intended plaintext. No remote edit was made or authorized by this report.
