# Adaptive alphabet mechanisms

All entries are proposed and unrun. A specified research question is not a novelty clearance or permission to launch a K4 search. See [README](README.md) for gates, priorities and source limitations.

<a id="n100-036"></a>
## N100-036 — Frequency-order alphabet coding

**Draft reference:** `A01` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Maintain counts n[a], initially zero. Before symbol i, order all 26 letters by (-n[a], fixed tie rank[a]); emit the current rank of P_i, then increment n[P_i]. One fixed output offset b is allowed. Decode by selecting the same ranked letter and updating its count.
- **Bounded test:** Freeze AZ and KRYPTOS tie orders, 26 output offsets, zero counts, no reset: 52 deterministic complete decoders. Exhaustively establish inverse on alphabets of size 2–4 and short strings before a separately admitted 97-letter application.
- **Controls:** All-equal, alternating and all-distinct plants test ties and count reversals; independently permuted ciphertext controls test chance clue agreement.
- **Identifiability limit:** An unrestricted initial count vector would become a fitted key and is forbidden. One surviving decoder is conditional evidence, not creator attribution.
- **Novelty distinction:** Frequency sorting depends on the whole histogram rather than current-symbol exchange, prefix reversal or move-to-front. A distinguishing synthetic trace against those rules must be recorded.
- **Closest local external:** H-EVOLVING-ALPHABET; H-BOUNDARY-STATE; EXT-034
- **Admission:** proposed; exact prior-art comparison and synthetic validation required
- **Priority:** 2
- **Estimated cost:** Design/inverse check first; initial prototype capped at 60 CPU seconds on tiny synthetic cases. Target budget must be frozen separately.
- **Sources:** 
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/EXTERNAL-PRIOR-ART.md

<a id="n100-037"></a>
## N100-037 — Transition-count alphabet coding

**Draft reference:** `A02` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Maintain 26 rows n[a,b]. Given previous decoded plaintext a (fixed initial sentinel A), rank next symbols b by descending n[a,b], ties in fixed AZ order; emit rank, update n[a,b], advance context.
- **Bounded test:** Fix zero counts, AZ ties and all 26 initial context symbols; optional single global output offset gives 676 descriptions. Verify complete deterministic inversion and quotient identical initial states.
- **Controls:** Plants include repeated bigrams and unseen contexts; one-symbol perturbations and matched random ciphertext controls.
- **Identifiability limit:** Most rows may remain tied on 97 letters, making the model observationally close to monoalphabetic coding. Stop if controls establish no discriminating power.
- **Novelty distinction:** Context-indexed empirical transition ordering is not a single global mutable alphabet or periodic key clock. It is not claimed as a new source-coding algorithm.
- **Closest local external:** H-EVOLVING-ALPHABET; EXT-026; EXT-034
- **Admission:** proposed; exact prior-art comparison and synthetic validation required
- **Priority:** 3
- **Estimated cost:** Design/inverse check first; initial prototype capped at 60 CPU seconds on tiny synthetic cases. Target budget must be frozen separately.
- **Sources:** 
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/EXTERNAL-PRIOR-ART.md

<a id="n100-038"></a>
## N100-038 — Tournament-memory alphabet

**Draft reference:** `A03` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Maintain antisymmetric score matrix W[a,b], initially zero. After decoding adjacent plaintext a,b, add 1 to W[a,b] and -1 to W[b,a]. Before each symbol, rank letters by descending number of strictly positive outgoing edges with AZ tie order; emit plaintext rank.
- **Bounded test:** Freeze the update, initial predecessor in AZ, and one output offset: 676 descriptions. Compare exact induced full-string maps with A01/A02 on exhaustive tiny alphabets before retaining.
- **Controls:** Cycle A→B→C→A and reversed-cycle plants distinguish pair orientation; balanced-flow and tie-heavy controls; random ciphertext nulls.
- **Identifiability limit:** Win-degree discards magnitude and can tie heavily. An initial draft used row sums, which telescope to endpoint imbalance; that draft was rejected before execution. Require a distinguishing trace from simple last-letter state before admission.
- **Novelty distinction:** Antisymmetric transition balance records direction of encounters, not counts alone, move-to-front or position-stepped keys.
- **Closest local external:** H-EVOLVING-ALPHABET; H-CIPHERTEXT-EXTRA-STEP; EXT-030
- **Admission:** proposed; exact prior-art comparison and synthetic validation required
- **Priority:** 3
- **Estimated cost:** Design/inverse check first; initial prototype capped at 60 CPU seconds on tiny synthetic cases. Target budget must be frozen separately.
- **Sources:** 
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/EXTERNAL-PRIOR-ART.md

<a id="n100-039"></a>
## N100-039 — Diffusive alphabet ordering

**Draft reference:** `A04` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Let v in F_29^26 start with one unit at an unknown alphabet index. At each step rank letters by the integer representatives of v with AZ ties, encode P_i by rank, then set v <- (I+L)v + e_(P_i) mod29, where L is the Laplacian of the fixed 26-cycle.
- **Bounded test:** Fix this graph, field and update; enumerate only 26 seed locations and 26 output offsets. Prove deterministic inverse and distinguish its maps from additive linear-key recurrences, although the internal vector update is linear.
- **Controls:** One-hot and uniform-state plants; independent encoder and decoder; adjacency/reversal perturbations plus null ciphertext.
- **Identifiability limit:** Arbitrary initial vectors are forbidden. Rank observation makes the induced substitution nonlinear, but may still have equivalent states and poor recovery.
- **Novelty distinction:** The shift is not a linear functional of history: a ranked diffusion state gives an entire time-varying permutation. This is a speculative mathematical construction, not a physical claim.
- **Closest local external:** H-AUTONOMOUS-RECURRENCE; H-EVOLVING-ALPHABET; EXT-048; EXT-051
- **Admission:** proposed; exact prior-art comparison and synthetic validation required
- **Priority:** 3
- **Estimated cost:** Design/inverse check first; initial prototype capped at 60 CPU seconds on tiny synthetic cases. Target budget must be frozen separately.
- **Sources:** 
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/EXTERNAL-PRIOR-ART.md

<a id="n100-040"></a>
## N100-040 — Assignment-memory alphabet

**Draft reference:** `A05` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Maintain integer costs M[a,j]=(a-j)^2 for AZ indices. Before a letter, choose the minimum-cost perfect assignment pi, breaking ties lexicographically; emit pi(P_i). After emission, increase only M[P_i,pi(P_i)] by 27.
- **Bounded test:** Exactly one initial cost matrix and one update penalty; only 26 initial cyclic column origins. Independent assignment solver and brute-force tiny-alphabet oracle must agree on every step.
- **Controls:** Repeated-symbol plants force reassignment; tied-cost matrices check deterministic choice; shuffled controls test false positives.
- **Identifiability limit:** Without fixed cost construction and penalty, matrix fitting would absorb clues. Assignment computation may be disproportionate for 97 letters.
- **Novelty distinction:** Coupled global matching replaces pair swaps/rotations. Need compare exact induced maps, not merely call it a new algorithm.
- **Closest local external:** H-EVOLVING-ALPHABET; EXT-014; EXT-018
- **Admission:** proposed; exact prior-art comparison and synthetic validation required
- **Priority:** 4
- **Estimated cost:** Design/inverse check first; initial prototype capped at 60 CPU seconds on tiny synthetic cases. Target budget must be frozen separately.
- **Sources:** 
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/EXTERNAL-PRIOR-ART.md

<a id="n100-041"></a>
## N100-041 — Partition-refinement alphabet

**Draft reference:** `A06` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Start with one ordered block of 26 symbols. After decoding P_i, stably split every block by whether its AZ cyclic distance from P_i belongs to the fixed set {0,1,3,7,12}; keep selected subblocks first, retaining order inside. Encode by rank in the concatenated blocks before each split.
- **Bounded test:** Fix the subset independently as cumulative increments 1,2,4,5 on the 26-cycle, then test only 26 initial cyclic origins; no alternative subsets after results. First measure whether refinement reaches singleton blocks too early.
- **Controls:** Tiny exhaustive split/inverse controls; adversarial repeated letters and patterns saturating refinement; matched random controls.
- **Identifiability limit:** Once partition saturates, updates cease; if early saturation reduces the proposal to already excluded fixed substitution, transfer that proof and do not run K4. The chosen subset has no creator evidence.
- **Novelty distinction:** State is a monotone ordered partition, not an always-mutable list. Its absorbing-state behavior offers an analytical exclusion route.
- **Closest local external:** H-EVOLVING-ALPHABET; H-PERIOD; EXT-042
- **Admission:** proposed; exact prior-art comparison and synthetic validation required
- **Priority:** 4
- **Estimated cost:** Design/inverse check first; initial prototype capped at 60 CPU seconds on tiny synthetic cases. Target budget must be frozen separately.
- **Sources:** 
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/EXTERNAL-PRIOR-ART.md

<a id="n100-042"></a>
## N100-042 — Patience-pile alphabet coding

**Draft reference:** `A07` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Maintain 26 distinct symbols in ordered piles, initially singleton AZ piles. To update after decoding a, remove a; append it to the leftmost pile whose top exceeds a in AZ order, or create a rightmost pile. Read current alphabet as piles bottom-to-top, left-to-right; emit a's rank before update. Empty piles are removed.
- **Bounded test:** Freeze exact pile insertion/readout, AZ/KRYPTOS initial singleton order and 26 global output offsets; verify every symbol remains present exactly once. Compare with MTF and sorting codecs by exhaustive short traces.
- **Controls:** Increasing/decreasing sequences, pile destruction and many-equal accesses; independent state replay and random ciphertext nulls.
- **Identifiability limit:** Potential collapse to a known self-organizing list or fixed order must be checked; if so classify overlap and remove.
- **Novelty distinction:** The state includes pile boundaries and partial-order insertion, rather than a single exchange/prefix operation. This is not an invention claim about patience sorting.
- **Closest local external:** H-EVOLVING-ALPHABET; H-TREE-STATEFUL; EXT-034
- **Admission:** proposed; exact prior-art comparison and synthetic validation required
- **Priority:** 4
- **Estimated cost:** Design/inverse check first; initial prototype capped at 60 CPU seconds on tiny synthetic cases. Target budget must be frozen separately.
- **Sources:** 
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/EXTERNAL-PRIOR-ART.md

<a id="n100-043"></a>
## N100-043 — Young-tableau promotion alphabet

**Draft reference:** `A08` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Place an AZ-labelled standard tableau of shape (13,13). Encode each plaintext label by its current row-major cell. After each symbol apply Schützenberger promotion t=1+(cipher rank mod3) times; promotion removes minimum label, performs fixed jeu-de-taquin slides, decrements and reinserts maximum.
- **Bounded test:** Freeze row-superstandard and column-superstandard starts only, exact promotion convention and one 26-valued output offset. Establish whether promotion's bounded order makes the full operator an already tested state-clock model.
- **Controls:** All tiny standard tableaux exhaustive forward/inverse rank controls; tie-free slide boundary cases; null ciphertext controls.
- **Identifiability limit:** The update can reduce to a finite periodic orbit sampled by ciphertext values. If exact operator comparison finds prior value-clock coverage, reject as duplicate rather than expand tableau shapes.
- **Novelty distinction:** Updates act through tableau promotion rather than exchange/prefix reversal; potential finite-clock alias is explicitly a gate.
- **Closest local external:** H-EVOLVING-ALPHABET; H-CIPHERTEXT-EXTRA-STEP; EXT-030
- **Admission:** proposed; exact prior-art comparison and synthetic validation required
- **Priority:** 4
- **Estimated cost:** Design/inverse check first; initial prototype capped at 60 CPU seconds on tiny synthetic cases. Target budget must be frozen separately.
- **Sources:** 
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/EXTERNAL-PRIOR-ART.md
