# C20 / N100-065: successor-queue reversal admission audit

Date: 1 November 2026. Baseline: `608fc123567b77ba48616c9c2191825d08964ea7`.

## Decision

**Mathematical definition passes this static audit. Recommend a finite synthetic inverse/oracle check; target admission is still pending.** No K4 input was read, transformed or fitted; no cipher or synthetic batch was executed. This is not a completed experiment or an assertion of worldwide novelty.

Unlike A01, no specific report of this exact K4 operator was located in the inspected sources. The construction is nonetheless a simple specialization of classical Euler-walk/last-exit mathematics and sequence shuffling, not an invented graph theorem. The local fixed-route negatives do not subsume its data-dependent operator. The seven fixed-key phases remain a speculative K4 application without independent creator-use evidence.

## Exact proposed operator

For a nonempty word x = x[0]…x[n−1], let s=x[0], t=x[n−1]. Build each vertex's successor list Q[v] by scanning adjacent pairs in input order. For v≠t, reverse Q[v] except its final entry; for t, reverse the entire list. Starting at s, consume these lists from the front until all n−1 edges have been consumed; emit the visited vertices. Call the resulting word T(x). Empty and one-symbol inputs are identity conventions for synthetic checks; target length is exactly 97.

The draft's only outer layer is standard A=0,…,Z=25 Vigenère with literal key KRYPTOS, phase p∈{0,…,6}: C[i] = T(P)[i] + K[(i+p) mod 7] mod26. Decryption is T(C−K_p), not subtraction after T. The tree is derived from the entire input word and is not a secret key or an extra fitted choice. There is no randomized tree, local-order choice, padding, reset, new alphabet, key search or layer reordering.

## Independent proof of the queue transformation

The following direct argument covers open and closed trails, loops and repeated directed edges.

1. Give each adjacent-pair occurrence a distinct identity solely for the proof. Every visited vertex v other than t has a last outgoing edge. If that edge leads to w≠t, the last departure from w occurs later in the original trail: after arriving at w the trail must depart again to reach t. Last-departure times therefore strictly increase along these selected edges until t. The selected edges form a directed tree toward t. A selected self-loop outside t would contradict the same argument.
2. Reordering outgoing edges while keeping the selected last edge last preserves that tree. Starting at s and consuming the reordered lists cannot stop at a vertex other than t: the original degree imbalances and the partial trail's degree imbalances would leave an unused outgoing edge there. This also covers s=t.
3. Suppose the walk stops at t before all edges are consumed. The remaining directed graph is balanced, since both the full and partial trails have endpoints s,t. Let U contain vertices with unused outgoing edges. The exhausted terminal vertex t is not in U. For v∈U its reserved last edge is still unused. Its endpoint w has an unused incoming edge, hence, by residual balance, an unused outgoing edge. Thus w∈U. Following the reserved tree edges would remain in U but eventually reach t, a contradiction. All edges are therefore consumed and the output ends at t.
4. Each output visit consumes exactly the next item in that vertex's transformed list. Reading successor lists from the output reconstructs precisely those transformed lists, with the same final entries at every v≠t. Applying the same prefix/full reversals again restores every original list. Deterministic walking from s then reconstructs x. Hence **T²=id**.
5. Consequently T preserves length, first/last symbol and the complete directed-bigram multiset. Unigram counts also follow: the count of a symbol equals its outdegree plus one if it is t. Parallel identical edges do not cause ambiguity because only their successor labels matter in the emitted word.

The outer layer is a fixed invertible coordinate map for each phase, so the complete encryption/decryption pair is bijective at every length. This says nothing about which, if any, phase fits K4.

### Hand-derived witnesses, not executed tests

- Open nontrivial pair: T(ABACAD)=ACABAD and T(ACABAD)=ABACAD. A's list B,C,D becomes C,B,D; B and C return to A.
- Closed pair: T(ABACA)=ACABA. The terminal/root A has its full B,C list reversed; the same rule reverses it back.
- Deliberately broken rule: reversing **all** queues of ABAC gives A's list C,B. A greedy walk emits AC and gets stuck with edges unused. This is a required negative implementation control, not the proposed T.
- A length-97 proof witness uses x=ABACAD followed by 91 copies of D, and y=ABECAD followed by 91 copies of D. Then T(x)=ACABAD followed by 91D, while T(y)=y. No fixed position permutation represents T on the length-97 domain: output position 1 (zero-based) of x is the unique C from input position 3, forcing that source index, but output position 1 of y is B while input position 3 remains C.
- T fixes every constant word. Thus a representation T(x)[i]=g_i(x[π(i)]) with fixed coordinate symbol maps would force every g_i to be identity, reducing to the impossible fixed-position case. Removing the known outer additive layer transfers this distinction to the complete composite.

## Prior-art comparison and limitations

### Local records

- **H-PERM:** the no-layer transformation is a pure permutation and is already covered by the retained baseline multiset exclusion. It must not be run or counted anew. That target-dependent exclusion is historical evidence, not recomputed in this audit. The specified outer Vigenère layer changes the ciphertext multiset, so the pure-layer argument alone does not exclude the composite.
- **H-ROUTE, 049 and 050:** inspected source and reports generate position maps from dimensions/geometry/keywords, independent of letter content. Study050 uses complete operators of the form s*x[π(i)]+b[i]. The length-97 witness above rules out equality of T with every fixed-position operator, not merely with a sampled route. This does not exclude isolated coincidences on particular inputs or validate the new composite.
- **Studies056–059:** their enumerated ragged-columnar route geometry is likewise input-independent. Their bounded negative conclusions cannot be transferred solely because C20 also permutes letters. Their other feedback families are not claimed exhaustively compared here.
- **H-TREE-STATEFUL:** the retained fixed-tree/access-splay state updates are not a proof about a whole-message directed-bigram graph. No claim is made that all conceivable tree mechanisms are globally disjoint.

Local file SHA256s are in `LOCAL-SOURCE-PINS.json`; no source was imported or executed. Relevant immutable links:

- [H-PERM/H-ROUTE/H-TREE-STATEFUL](https://github.com/reggiechan74/kryptos-k4/blob/608fc123567b77ba48616c9c2191825d08964ea7/research/HYPOTHESES.md)
- [049 source](https://github.com/reggiechan74/kryptos-k4/blob/608fc123567b77ba48616c9c2191825d08964ea7/experiments/ene_route_049.py)
- [050 source](https://github.com/reggiechan74/kryptos-k4/blob/608fc123567b77ba48616c9c2191825d08964ea7/experiments/hand_grammar_050.py)

### External K4 work

- **EXT-002, Scott Dunphy E1:** the pinned source imports route/columnar constructors and builds all permutations before crib filtering. Its position maps are independent of input symbols. Source read: [run_e1.py at a7517858](https://github.com/scott-dunphy/kryptos-k4/blob/a75178587efe9401ebf2a4edf3828472dd6fb2a2/run_e1.py), Git blob `0dc15f8199d5ea1373d5cfceb79ae6fbf5331d84`. This inspected E1 grammar does not implement C20. No numerical result was reproduced.
- **EXT-008, ActiveTK E218/E227:** pinned E218 source explicitly constructs index permutations for selfkey/routed autokey; it does not construct successor queues from the complete input word. Source read: [e218_selfkey_chain_exact.cu at 992c9668](https://github.com/ActiveTK/dekrypt/blob/992c9668b9f0783221cb570abbff969e59cbf27c/src/e218_selfkey_chain_exact.cu), Git blob `f12d62a2553ddc5fac35e23aba57dc04eab665a5`. This is an implementation-scope distinction, not a proof excluding every accidental functional equality under arbitrary alphabets.
- **EXT-034:** available register is documentation-only classical/clock/moving-alphabet scope. It supplies no exact Euler-queue source or full external exclusion. Missing sources are unresolved coverage, not affirmative novelty evidence.
- **EXT-051/052/053:** broader undocumented campaigns and source-selection limits remain. A01's specific frequency-count overlap is not transferred to C20 without matching equations. No specific matching C20 attempt was located in this finite pass.

On 1 November 2026, indexed searches used Kryptos/K4 with Euler/Eulerian, last-exit, successor queue, bigram, dinucleotide and uShuffle. Most results were irrelevant or generic graph literature. Four GitHub code searches (`Eulerian`, `last_exit`, `successor queue`, `dinucleotide`) across scott-dunphy/kryptos-k4, ActiveTK/dekrypt, mruckman1/k4_cipher and matthewdgreen/decipher returned no results. These are search coverage receipts, **not** whole-repository semantic audits; code search covers default branches and may omit unindexed content. Existing finite-discovery claims are not strengthened to a worldwide survey.

### Classical technical foundation

- Van Aardenne-Ehrenfest and de Bruijn, *Circuits and trees in oriented linear graphs* (1951), [institutional record](https://research.tue.nl/nl/publications/circuits-and-trees-in-oriented-linear-graphs-3/). Record read; linked scan returned403 and was not bypassed or treated as read.
- [MIT 18.314 author/course notes, section2.2, claims1–2](https://ocw.mit.edu/courses/18-314-combinatorial-analysis-fall-2014/99d707393fabef4e95c3d2bd1690af91_MIT18_314F14_mt2.pdf) provide the last-exit/tree reconstruction argument. PDF text read. The proof above independently extends the direct residual-balance presentation to the proposal's open and closed word trails.
- [Holroyd et al., *Chip-Firing and Rotor-Routing on Directed Graphs*, arXiv0801.3306v4](https://arxiv.org/html/0801.3306v4) supplies related stack/rotor foundations; it is not evidence of a K4 attempt or this exact reversal.
- [Altschul and Erickson (1985)](https://academic.oup.com/mbe/article/2/6/526/981780) already formulate dinucleotide-preserving randomization as Eulerian walks. [Jiang et al., uShuffle (2008)](https://pmc.ncbi.nlm.nih.gov/articles/PMC2375906/) explicitly describe permuting outgoing edge lists while retaining a chosen last edge, followed by guided walking. The indexed primary-paper text was read; direct PMC open returned a browser check, which was not bypassed. C20 keeps the input's existing last exits and deterministically reverses the remaining lists, rather than drawing a random tree/order. This is a classical specialization, not an independently established algorithmic invention.

## Next finite step

`SYNTHETIC-PROTOCOL.md` proposes a 60-CPU-second, 128-MiB, 120-wall-second synthetic-only check. Its reference reconstructs transformed words through independently enumerated queue signatures rather than a second copy of the walk algorithm. It tests 17,349 tiny word/alphabet cases, explicit malformed/naive-rule failures, and 91 fixed 97-letter phase plants. No target read, crib match, language ranking or target nulls are included. Source implementation/review, exact freeze and a parent execution decision remain outstanding. A failure stops the proposal; no changed queue rule or extra key phase follows automatically.
