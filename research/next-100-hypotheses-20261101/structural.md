# Structural algebra and finite-state mechanisms

All entries are proposed and unrun. A specified research question is not a novelty clearance or permission to launch a K4 search. See [README](README.md) for gates, priorities and source limitations.

The shared protocol and source receipt are in [STRUCTURAL-COMMON.json](STRUCTURAL-COMMON.json). They are proposed controls, not completed runs.

<a id="n100-001"></a>
## N100-001 — Dihedral plaintext autokey

**Draft reference:** `S01` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Represent AZ rank n by (r=n mod13,e=floor(n/13)) in D13, with (r,e)*(s,f)=(r+(-1)^e s mod13,e xor f). Set C_i=P_(i-1)*P_i; P_-1 is the seed. Invert by left group division.
- **Bounds:** AZ fixed; all26 initial group elements; lag1 only; no extra offset, alphabet search, or transposition.
- **Discriminating prediction:** The previous plaintext reflection bit reverses the rotational coordinate; exchanging two input letters can change the product.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. AZ fixed; all26 initial group elements; lag1 only; no extra offset, alphabet search, or transposition.
- **Closest local:** 
  - H-AUTOKEY-EXACT
  - H-ASYMMETRIC-FEEDBACK
- **Closest external:** 
  - EXT-041
  - EXT-048
- **Novelty distinction:** EXT-041 is abelian-group lag7 feedback. Noncommutative D13 multiplication is not a relabelled abelian group law; this is not a changed lag within that law.
- **Eligibility:** operator-audit-pending
- **Sources:** 
  - https://github.com/aciderix/kryptos-research-handoff/blob/6b82bd5364b6fea78b6ef3cfd73fafaf85ac3462/audits/autocle_groupes_2026_09_25/t36_autocle_groupes.py
  - https://github.com/scott-dunphy/kryptos-k4/blob/a75178587efe9401ebf2a4edf3828472dd6fb2a2/novel/run_chain.py
- **Target run:** False
- **Identifiability limit:** Seed aliases or coincident traces do not identify the intended operation; fixed embedding is an unsupported but falsifiable hypothesis.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. operator-audit-pending
- **Proposed parameter descriptions:** 26
- **Proposed cost:** small-state exact enumeration
- **Specification status:** explicit proposal; independent correctness and prior-art admission gates still pending
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent Cayley-table and semidirect-pair producers; all26 seeds and short words; blind97-letter plants with24 hidden-position clues.
  - **Negative:** Commutative Z26-autokey controls and independently constructed inconsistent clue sets; retain any incidental fits rather than asserting all nulls must fail.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 2

<a id="n100-002"></a>
## N100-002 — Projective-line alphabet transport

**Draft reference:** `S02` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Identify A..Y with F25=F5[t]/(t^2+2), in coefficient order a+5b, and Z with infinity. C_i=M_i(P_i), M_(i+1)=T(C_i) M_i. For finite z, T(z)=[[z,-1],[1,0]]; T(infinity)=[[1,1],[0,1]]. M acts by fractional linear transformation.
- **Bounds:** All15,600 projective classes M0 in PGL2(F25); quotient scalar matrices; fixed field basis and update order.
- **Discriminating prediction:** After undoing the ciphertext-determined transport, all plaintext/ciphertext correspondences share one projectivity and therefore preserve cross-ratios.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. All15,600 projective classes M0 in PGL2(F25); quotient scalar matrices; fixed field basis and update order.
- **Closest local:** 
  - H-EVOLVING-ALPHABET
- **Closest external:** 
  - EXT-018
  - EXT-044
  - EXT-050
- **Novelty distinction:** A 3-transitive projective action with noncommuting matrix updates is not Chaocipher, symbol exchange, or fixed-reference prefix reversal. Exact subset checks still precede admission.
- **Eligibility:** operator-audit-pending
- **Sources:** 
  - https://arxiv.org/abs/2102.10321
  - https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0
- **Target run:** False
- **Identifiability limit:** Three distinct correspondences determine a projectivity only after transport; degenerate repeated points and field-basis assumptions must remain explicit.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. operator-audit-pending
- **Proposed parameter descriptions:** 15600
- **Proposed cost:** medium finite enumeration
- **Specification status:** explicit proposal; independent correctness and prior-art admission gates still pending
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent matrix and permutation-of26 implementations; poles/infinity and all projective initial states on short plants.
  - **Negative:** Four-point controls violating the cross-ratio condition, plus exchange/prefix-reversal evolving alphabets.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 4

<a id="n100-003"></a>
## N100-003 — Latin-trade quasigroup feedback

**Draft reference:** `S03` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Start Q(x,y)=x+y mod26. For one intercalate with rows r,r+13 and columns s,s+13, exchange its two symbols in all four cells. Encrypt C_i=Q(C_(i-1),P_i), with row-wise Latin-square inverse.
- **Bounds:** r,s in0..12; 169 tables, all26 initial ciphertext seeds; freeze AZ; no arbitrary Latin square fitting.
- **Discriminating prediction:** Most transitions obey additive feedback, but the four-cell trade gives a specific reversible nonassociative exception.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. r,s in0..12; 169 tables, all26 initial ciphertext seeds; freeze AZ; no arbitrary Latin square fitting.
- **Closest local:** 
  - H-AUTOKEY-EXACT
  - H-NONLINEAR-BLOCK
- **Closest external:** 
  - EXT-009
  - EXT-041
  - EXT-048
- **Novelty distinction:** The exception depends jointly on previous ciphertext and current plaintext, not an additive shift that depends only on lag history. Quasigroup ciphers are known mathematics, not a new invention.
- **Eligibility:** operator-audit-pending
- **Sources:** 
  - https://arxiv.org/abs/cs/0610017
  - https://github.com/aciderix/kryptos-research-handoff/blob/6b82bd5364b6fea78b6ef3cfd73fafaf85ac3462/audits/autocle_groupes_2026_09_25/t36_autocle_groupes.py
  - https://github.com/scott-dunphy/kryptos-k4/blob/a75178587efe9401ebf2a4edf3828472dd6fb2a2/novel/run_chain.py
- **Target run:** False
- **Identifiability limit:** If no traded cell is visited, the trace is an already-known additive model and must not count as support; associative/isomorphic degeneracies must be removed.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. operator-audit-pending
- **Proposed parameter descriptions:** 4394
- **Proposed cost:** small-state exact enumeration
- **Specification status:** explicit proposal; independent correctness and prior-art admission gates still pending
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent Latin-row inversion; verify every table is Latin, and exercise every traded cell and surrounding untraded cells.
  - **Negative:** Untraded additive-autokey controls and mutated observations inconsistent with every enumerated table; null acceptance measured separately.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 4

<a id="n100-004"></a>
## N100-004 — Cerny synchronizing transducer

**Draft reference:** `S04` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** State q in{0,1,2}; C=P+k_q mod26. After emitting C, apply a:q->q+1 mod3 if C is even, or b:2->0,0->0,1->1 if C is odd.
- **Bounds:** All3 initial states and26^3 shift triples; remove constant triples and operator-equivalent descriptions.
- **Discriminating prediction:** A reset word in the emitted parity stream erases initial-state uncertainty without restarting at a crib.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. All3 initial states and26^3 shift triples; remove constant triples and operator-equivalent descriptions.
- **Closest local:** 
  - H-CIPHERTEXT-EXTRA-STEP
  - H-BOUNDARY-STATE
- **Closest external:** 
  - EXT-030
- **Novelty distinction:** Noninjective state merging in a synchronizing automaton differs from a cyclic pointer advancing or pausing. Ciphertext-induced partition containment against old banks remains an admission gate.
- **Eligibility:** operator-audit-pending
- **Sources:** 
  - https://arxiv.org/abs/1202.4626
  - https://github.com/Barneyjm/kryptos-k4/blob/2db2722cc3f18c52d4d8369d7adc5a1db7e859d7/scripts/fe_interrupt.py
- **Target run:** False
- **Identifiability limit:** States with equal shifts can be observationally equivalent; state-name permutations are not distinct discoveries.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. operator-audit-pending
- **Proposed parameter descriptions:** 52728
- **Proposed cost:** medium finite enumeration
- **Specification status:** explicit proposal; independent correctness and prior-art admission gates still pending
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent DFA table versus transition formulas; synchronizing-word tests from every state and blind full-message plants.
  - **Negative:** Permutation-only key-clock controls and null clue sets; use exact automaton-product equivalence tests for false novelty.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 4

<a id="n100-005"></a>
## N100-005 — Hysteretic plaintext-controlled multiplier

**Draft reference:** `S05` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** State q is0 or1. C=(1+4q)P+b mod26. After recovering/emitting P, set q=0 for P<=7, q=1 for P>=18, otherwise retain q.
- **Bounds:** AZ; both starting states and26 offsets b; thresholds7/18 and multipliers1/5 fixed.
- **Discriminating prediction:** The same middle-range plaintext symbol uses different multiplicative substitutions depending on the last threshold crossing.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. AZ; both starting states and26 offsets b; thresholds7/18 and multipliers1/5 fixed.
- **Closest local:** 
  - H-PLAINTEXT-EXTRA-STEP
  - H-PERIOD
- **Closest external:** 
  - EXT-030
  - EXT-050
- **Novelty distinction:** This changes the symbol multiplier through memory, rather than selecting an entry of a fixed additive keyword or adding another trigger letter.
- **Eligibility:** operator-audit-pending
- **Sources:** 
  - https://github.com/Barneyjm/kryptos-k4/blob/2db2722cc3f18c52d4d8369d7adc5a1db7e859d7/scripts/fe_interrupt.py
  - https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0
- **Target run:** False
- **Identifiability limit:** One-sided histories may never visit both states; compatible fits without both regimes are weak or equivalent to simpler attempted models.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. operator-audit-pending
- **Proposed parameter descriptions:** 52
- **Proposed cost:** small-state exact enumeration
- **Specification status:** explicit proposal; independent correctness and prior-art admission gates still pending
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent forward and inverse transducers, with paired histories reaching opposite hysteresis states before the same middle symbol.
  - **Negative:** Memoryless threshold substitutions and plaintext-extra-step controls; certified inconsistent observations.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 2

<a id="n100-006"></a>
## N100-006 — Rotor-router substitution memory

**Draft reference:** `S06` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Four-cycle graph, pointer v and one binary rotor r_j per vertex. Emit C=P+[v+4 sum_j 2^j r_j] mod26. Then perform1+(P mod3) microsteps: flip rotor at v, then move clockwise for rotor1 or anticlockwise for rotor0.
- **Bounds:** All64 pointer/rotor initial states, fixed graph and formula; message positions never move.
- **Discriminating prediction:** Two histories ending at the same pointer can differ through distributed rotor memory; local departure directions alternate.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. All64 pointer/rotor initial states, fixed graph and formula; message positions never move.
- **Closest local:** 
  - H-RECURRENCE-CLOCK
  - H-SIGABA-INSPIRED
- **Closest external:** 
  - EXT-030
  - EXT-048
- **Novelty distinction:** Rotors store local visit parity and generate substitutions; unlike Josephus or the encoding agent rotor walk, they do not permute emission slots.
- **Eligibility:** operator-audit-pending
- **Sources:** 
  - https://arxiv.org/abs/0904.4507
  - https://github.com/Barneyjm/kryptos-k4/blob/2db2722cc3f18c52d4d8369d7adc5a1db7e859d7/scripts/fe_interrupt.py
- **Target run:** False
- **Identifiability limit:** State-to-shift collisions are expected; all surviving state/plaintext pairs must be reported, not a best state.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. operator-audit-pending
- **Proposed parameter descriptions:** 64
- **Proposed cost:** small-state exact enumeration
- **Specification status:** explicit proposal; independent correctness and prior-art admission gates still pending
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent rotor-table simulator and explicit transition graph; cover all64 states and all26 inputs.
  - **Negative:** Ordinary cyclic pointer and rotor-router message-slot-routing controls; certify at least one operator-separation witness before admission.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 4

<a id="n100-007"></a>
## N100-007 — Abelian sandpile substitution state

**Draft reference:** `S07` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Four line sites have stable heights0..2. Emit C=P+(h0+3h1+9h2+27h3) mod26. Add one grain at site P mod4, then topple any site>=3: subtract3, send one grain to each existing neighbor and the remainder to the sink.
- **Bounds:** All81 stable initial height vectors; fixed threshold3 and open boundaries; no route or keyword.
- **Discriminating prediction:** Legal toppling order does not affect final state; cascades create nonlinear state jumps and sink loss.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. All81 stable initial height vectors; fixed threshold3 and open boundaries; no route or keyword.
- **Closest local:** 
  - H-CARRY-624
  - H-TREE-STATEFUL
- **Closest external:** 
  - EXT-048
  - EXT-049
- **Novelty distinction:** Threshold-triggered spatial redistribution is not the scalar mod624 accumulator or periodic adjacent-pair carry supermodel.
- **Eligibility:** operator-audit-pending
- **Sources:** 
  - https://doi.org/10.1103/PhysRevLett.64.1613
  - https://github.com/scott-dunphy/kryptos-k4/blob/a75178587efe9401ebf2a4edf3828472dd6fb2a2/novel/run_chain.py
- **Target run:** False
- **Identifiability limit:** Different stable states may yield the same shift and later coalesce; complete compatible states matter more than a chosen height picture.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. operator-audit-pending
- **Proposed parameter descriptions:** 81
- **Proposed cost:** small-state exact enumeration
- **Specification status:** explicit proposal; independent correctness and prior-art admission gates still pending
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent leftmost-first and rightmost-first stabilization, all81x26 transitions, blind plants.
  - **Negative:** Linear diffusion and single base-carry accumulator controls; prove non-equivalence on synthetic transitions.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 4

<a id="n100-008"></a>
## N100-008 — Free-group stack reduction feedback

**Draft reference:** `S08` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Maintain a reduced word on generators a,a^-1,b,b^-1 coded0..3. Emit C=P+k+length(stack)+5*topcode mod26 (empty topcode0). Append token P mod4; cancel if it is inverse to the current top, otherwise push.
- **Bounds:** Initial reduced words of length<=2 (17 states),26 offsets; after97 symbols length<=99. No overflow rejection or crib reset.
- **Discriminating prediction:** An appended inverse pair restores stack state; unequal deep prefixes can become visible after cancellations.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. Initial reduced words of length<=2 (17 states),26 offsets; after97 symbols length<=99. No overflow rejection or crib reset.
- **Closest local:** 
  - H-TREE-STATEFUL
  - H-CANONICAL-RESIDUAL-FEEDBACK
- **Closest external:** 
  - EXT-048
  - EXT-051
- **Novelty distinction:** Unbounded-depth cancellation memory over the message is not a six-lag sparse equality polynomial or a splay-tree alphabet.
- **Eligibility:** operator-audit-pending
- **Sources:** 
  - https://www.iacr.org/archive/crypto2000/18800166/18800166.pdf
  - https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0
- **Target run:** False
- **Identifiability limit:** The shift observes only a projection of the stack, so initial words may be indistinguishable; bounded initial memory must not become an arbitrary fitted word.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. operator-audit-pending
- **Proposed parameter descriptions:** 442
- **Proposed cost:** small-state exact enumeration
- **Specification status:** explicit proposal; independent correctness and prior-art admission gates still pending
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent linked-stack and free-word reduction implementations; exhaustive token words through length7 and blind97-letter plants.
  - **Negative:** Finite-window equality-feedback and unreduced-word controls; null clue sets with complete finite initial-state enumeration.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 4

<a id="n100-009"></a>
## N100-009 — Cross-coupled CRT state machine

**Draft reference:** `S09` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Encode each symbol by (p2=P mod2,p13=P mod13). State(e,x) in F2xF13 emits c2=p2 xor e,c13=p13+x. Update e′=e xor 1[x is a nonzero quadratic residue mod13], x′=x+1+p2 mod13; recover C by CRT.
- **Bounds:** All26 initial states; fixed nonzero quadratic-residue predicate; no fitted alphabet.
- **Discriminating prediction:** The mod13 state controls the binary mask, while the plaintext binary coordinate controls the mod13 clock.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. All26 initial states; fixed nonzero quadratic-residue predicate; no fitted alphabet.
- **Closest local:** 
  - H-AUTOKEY-EXACT
  - H-CANONICAL-RESIDUAL-FEEDBACK
- **Closest external:** 
  - EXT-041
  - EXT-048
  - EXT-051
- **Novelty distinction:** The two CRT coordinates feed each other through a residue predicate, unlike independent field recurrences or a different alphabet encoding of a cyclic group.
- **Eligibility:** operator-audit-pending
- **Sources:** 
  - https://github.com/aciderix/kryptos-research-handoff/blob/6b82bd5364b6fea78b6ef3cfd73fafaf85ac3462/audits/autocle_groupes_2026_09_25/t36_autocle_groupes.py
  - https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0
- **Target run:** False
- **Identifiability limit:** A particular trace may accidentally remain in a simpler component; global nonlinearity does not establish unique K4 identification.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. operator-audit-pending
- **Proposed parameter descriptions:** 26
- **Proposed cost:** small-state exact enumeration
- **Specification status:** explicit proposal; independent correctness and prior-art admission gates still pending
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent CRT and direct26-symbol tables; all26x26 transitions and trajectories distinguishing cross-coordinate coupling.
  - **Negative:** Decoupled CRT/abelian feedback and constant-residue controls; mutated clues checked against the complete26-state set.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 2

<a id="n100-010"></a>
## N100-010 — Nonabelian SL2 accumulator

**Draft reference:** `S10` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** State M in SL2(F5); emit C=P+[tr(M)+5*M01] mod26. Update M′=M A^(P mod5) B^floor(P/5), A=[[1,1],[0,1]], B=[[1,0],[1,1]]. Matrix entries use canonical0..4 representatives in readout.
- **Bounds:** All120 SL2(F5) initial states; fixed A,B and readout; no free matrix coefficients.
- **Discriminating prediction:** Swapping two plaintext inputs generally changes the later matrix state because A and B do not commute.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. All120 SL2(F5) initial states; fixed A,B and readout; no free matrix coefficients.
- **Closest local:** 
  - H-AUTONOMOUS-RECURRENCE
  - H-CARRY-624
- **Closest external:** 
  - EXT-041
  - EXT-048
  - EXT-051
- **Novelty distinction:** A product accumulator in a nonabelian matrix group with lossy readout differs from both group-valued autokey and additive scalar carry.
- **Eligibility:** operator-audit-pending
- **Sources:** 
  - https://github.com/aciderix/kryptos-research-handoff/blob/6b82bd5364b6fea78b6ef3cfd73fafaf85ac3462/audits/autocle_groupes_2026_09_25/t36_autocle_groupes.py
  - https://github.com/scott-dunphy/kryptos-k4/blob/a75178587efe9401ebf2a4edf3828472dd6fb2a2/novel/run_chain.py
  - https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0
- **Target run:** False
- **Identifiability limit:** Trace/readout collisions can hide matrix distinctions; report state equivalence classes and plaintext ambiguity.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. operator-audit-pending
- **Proposed parameter descriptions:** 120
- **Proposed cost:** small-state exact enumeration
- **Specification status:** explicit proposal; independent correctness and prior-art admission gates still pending
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent matrix multiplication and precomputed120-state Cayley transitions; determinant1 invariant and blind plants.
  - **Negative:** Commuting-matrix accumulators and scalar linear-feedback controls; null matches assessed exactly.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 4

<a id="n100-011"></a>
## N100-011 — Cut-and-stack baker transducer

**Draft reference:** `S11` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** State(x,y) in{0..25}^2 emits C=P+x mod26. Add P to y mod26, then apply B(x,y)=(2*(x mod13)+floor(y/13),13*floor(x/13)+(y mod13)).
- **Bounds:** All676 states; fixed baker permutation and update order.
- **Discriminating prediction:** The cut bit of one coordinate becomes the low binary digit of the other; fixed-input state updates are permutations.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. All676 states; fixed baker permutation and update order.
- **Closest local:** 
  - H-CARRY-624
  - H-SPLIT-COORDINATE-ROUTES
- **Closest external:** 
  - EXT-048
  - EXT-051
- **Novelty distinction:** A reversible cut-and-stack state map acts on hidden coordinates, not separate transpositions of message coordinate streams or a changed carry modulus.
- **Eligibility:** operator-audit-pending
- **Sources:** 
  - https://github.com/scott-dunphy/kryptos-k4/blob/a75178587efe9401ebf2a4edf3828472dd6fb2a2/novel/run_chain.py
  - https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0
- **Target run:** False
- **Identifiability limit:** Many initial states can have identical early x readouts; a complete path, not isolated crib starts, is required.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. operator-audit-pending
- **Proposed parameter descriptions:** 676
- **Proposed cost:** small-state exact enumeration
- **Specification status:** explicit proposal; independent correctness and prior-art admission gates still pending
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent digit decomposition and explicit inverse B^-1; all676x26 state/input transitions.
  - **Negative:** Affine torus-map and scalar-carry controls, with synthetic transition witnesses separating their laws.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 4

<a id="n100-012"></a>
## N100-012 — Toffoli-gated binary state

**Draft reference:** `S12` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Five-bit state s emits C=P+(integer(s) mod26). After P, xor its five-bit AZ representation into s; cyclically rotate bits by1; then apply Toffoli gate s4 <- s4 xor(s0 and s1).
- **Bounds:** All32 initial states; fixed input encoding, rotation, gate and MSB convention.
- **Discriminating prediction:** Each fixed-input state update is reversible but has a genuine quadratic Boolean term.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. All32 initial states; fixed input encoding, rotation, gate and MSB convention.
- **Closest local:** 
  - H-AUTONOMOUS-RECURRENCE
- **Closest external:** 
  - EXT-010
  - EXT-048
  - EXT-051
- **Novelty distinction:** Nonlinear state feedback through a reversible gate differs from changing bit order or chunking of an ordinary LFSR.
- **Eligibility:** operator-audit-pending
- **Sources:** 
  - https://dspace.mit.edu/entities/publication/06a8b271-428a-4379-955c-8c7334aa0288
  - https://github.com/ActiveTK/dekrypt/blob/992c9668b9f0783221cb570abbff969e59cbf27c/src/s225_lfsr_chunks.py
  - https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0
- **Target run:** False
- **Identifiability limit:** Six collisions in the state-to-mod26 readout can delay identification; tiny state size is a restriction, not historical evidence.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. operator-audit-pending
- **Proposed parameter descriptions:** 32
- **Proposed cost:** small-state exact enumeration
- **Specification status:** Specification-blocked: freeze bit significance, cyclic-rotation direction and gate indexing before implementation; these conventions are not yet unambiguous.
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent truth-table and gate-list implementations, all32x26 transitions, reverse-circuit checks.
  - **Negative:** Linearized-gate LFSR controls and random nonlinear permutations; certified unsatisfiable clue sets.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 4

<a id="n100-013"></a>
## N100-013 — Quadratic moment accumulator over29

**Draft reference:** `S13` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** State t in F29 emits C=P+(t mod26). Update t′=t+P^2 mod29 after emission.
- **Bounds:** All29 initial states; prime29 is fixed as the least prime above26; no free polynomial fit.
- **Discriminating prediction:** State increments depend on squared plaintext ranks, with hidden mod29 wrap distinct from mod26 addition.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. All29 initial states; prime29 is fixed as the least prime above26; no free polynomial fit.
- **Closest local:** 
  - H-AUTONOMOUS-RECURRENCE
  - H-RADIX-FEEDBACK
- **Closest external:** 
  - EXT-048
  - EXT-051
- **Novelty distinction:** Current-plaintext quadratic forcing and hidden prime-state reduction are outside the inspected fixed-alphabet causal linear grammar; EXT-051 polynomial scope remains unresolved.
- **Eligibility:** EXT-051-scope-unresolved
- **Sources:** 
  - https://github.com/scott-dunphy/kryptos-k4/blob/a75178587efe9401ebf2a4edf3828472dd6fb2a2/novel/run_chain.py
  - https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0
- **Target run:** False
- **Identifiability limit:** The29-to26 projection is not injective; recurrence-law compatibility is not intended-law evidence.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. EXT-051-scope-unresolved
- **Proposed parameter descriptions:** 29
- **Proposed cost:** small-state exact enumeration
- **Specification status:** explicit proposal; independent correctness and prior-art admission gates still pending
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent integer and field implementations; force wraps and all29 seeds in planted texts.
  - **Negative:** Linear-moment and mod26 accumulator controls; full finite negative-control solution sets.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 4

<a id="n100-014"></a>
## N100-014 — Small Blum-Blum-Shub stream

**Draft reference:** `S14` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** N=pq for distinct p,q from{7,11,19,23,31,43,47}. State x0 is a distinct nonzero quadratic residue moduloN; x_(t+1)=x_t^2 modN. Read parity(x_t), pack consecutive five bits MSB-first into v, and use K_i=v mod26; C_i=P_i+K_i mod26.
- **Bounds:** Exactly the listed primes, all distinct QR seeds, first bit before squaring, no burn-in or alternative packing.
- **Discriminating prediction:** Exactly485 generated bits determine97 shifts; no arbitrary bit positions are fitted, and short cycles remain visible.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. Exactly the listed primes, all distinct QR seeds, first bit before squaring, no burn-in or alternative packing.
- **Closest local:** 
  - H-AUTONOMOUS-RECURRENCE
- **Closest external:** 
  - EXT-010
  - EXT-051
- **Novelty distinction:** Quadratic-residue dynamics is a classical1986 generator, not an LFSR extraction variant. No identical K4 implementation was located in the bounded search; broad recurrence handoff scope is unknown.
- **Eligibility:** EXT-051-scope-unresolved
- **Sources:** 
  - https://shub.ccny.cuny.edu/articles/1986-A_simple_unpredictable_pseudo-random_number_generator.pdf
  - https://github.com/ActiveTK/dekrypt/blob/992c9668b9f0783221cb570abbff969e59cbf27c/src/s225_lfsr_chunks.py
  - https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0
- **Target run:** False
- **Identifiability limit:** Tiny BBS instances are not secure; repeated/short-cycle generators must be quotient-deduplicated and removed if already covered by an exact prior negative.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. EXT-051-scope-unresolved
- **Proposed parameter descriptions:** None
- **Proposed cost:** medium finite enumeration
- **Specification status:** explicit proposal; independent correctness and prior-art admission gates still pending
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent modular-squaring and CRT producers, QR membership and cycle tests, blind plants.
  - **Negative:** Ordinary LFSR and random five-bit streams; exact incompatibility controls under the full finite generator bank.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 4

<a id="n100-015"></a>
## N100-015 — Stop-and-go two-register stream

**Draft reference:** `S15` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Binary Fibonacci LFSRs A,B have orders5,7 and polynomials x^5+x^2+1, x^7+x+1. At each bit-clock read a=A0, advance A, advance B iff a=1, and then emit B0. Pack five emitted bits MSB-first into v; K=v mod26 and C=P+K mod26. LFSR state orientation and polynomial-to-recurrence convention must be independently frozen and checked before execution.
- **Bounds:** All31x127 nonzero initial register states; fixed tap polynomials, exactly the stated clock/read order, no tap search or burn-in.
- **Discriminating prediction:** Repeated data output during control-zero stretches introduces irregular clocking, rather than a different readout of one regular LFSR.
- **Bounded test:** After separate admission only, enumerate all31x127 seed pairs with the exact stated clock/read order. Retain all matching key-stream/plaintext classes; independently re-encrypt all97 symbols. The implementation must first freeze a source-verified polynomial/state orientation. No alternative clocks or taps after failure.
- **Closest local:** 
  - H-AUTONOMOUS-RECURRENCE
  - H-SIGABA-INSPIRED
- **Closest external:** 
  - EXT-010
  - EXT-030
- **Novelty distinction:** Clock-controlled register state is not a cyclic keyword pointer; exact output containment in EXT-010 still requires review rather than being assumed.
- **Eligibility:** operator-audit-pending
- **Sources:** 
  - https://github.com/ActiveTK/dekrypt/blob/992c9668b9f0783221cb570abbff969e59cbf27c/src/s225_lfsr_chunks.py
  - https://github.com/Barneyjm/kryptos-k4/blob/2db2722cc3f18c52d4d8369d7adc5a1db7e859d7/scripts/fe_interrupt.py
- **Target run:** False
- **Identifiability limit:** Equivalent register phases may produce the same97-shift trace; report trace classes and longer synthetic separating witnesses.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. operator-audit-pending
- **Proposed parameter descriptions:** 3937
- **Proposed cost:** small-state exact enumeration
- **Specification status:** specification-blocked until exact bit/state/canonical-cycle orientation is frozen independently; no target authority
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent bit-level and transition-table producers; hand traces containing runs of both control values.
  - **Negative:** Always-clocked two-register and ordinary order<=30 LFSR controls; certify global separation or drop covered subdomains.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 4

<a id="n100-016"></a>
## N100-016 — Canonical de Bruijn cycle stream

**Draft reference:** `S16` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Generate the canonical binary prefer-one de Bruijn cycle of order n, using the complete visited-n-word rule from all-zero start. Read a chosen cyclic phase, pack5 successive bits MSB-first modulo26, and add to P.
- **Bounds:** n in{9,10,11,12}, all2^n phases; one canonical cycle per n, not all de Bruijn sequences; construction orientation frozen.
- **Discriminating prediction:** Every n-bit word occurs exactly once in a full cycle, including the zero word omitted from a maximal-length LFSR.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. n in{9,10,11,12}, all2^n phases; one canonical cycle per n, not all de Bruijn sequences; construction orientation frozen.
- **Closest local:** 
  - H-AUTONOMOUS-RECURRENCE
  - H-PERIOD
- **Closest external:** 
  - EXT-010
  - EXT-051
- **Novelty distinction:** A visited-word combinatorial generator is not an ordinary linear recurrence; expanding n after failure would be a cosmetic rescue and is excluded.
- **Eligibility:** operator-audit-pending
- **Sources:** 
  - https://www.sciencedirect.com/science/article/pii/0012365X7890002X
  - https://github.com/ActiveTK/dekrypt/blob/992c9668b9f0783221cb570abbff969e59cbf27c/src/s225_lfsr_chunks.py
  - https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0
- **Target run:** False
- **Identifiability limit:** At97 letters the generator has a long period, so ordinary long-period compatibility is uninformative; only the restricted cycle bank is testable.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. operator-audit-pending
- **Proposed parameter descriptions:** 7680
- **Proposed cost:** small-state exact enumeration
- **Specification status:** specification-blocked until exact bit/state/canonical-cycle orientation is frozen independently; no target authority
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent prefer-one and necklace-based generation after verifying their canonical orientation; exhaustive n-word inventories and blind plants.
  - **Negative:** Maximal-length LFSR and shuffled-cycle controls; phase-independent full-cycle invariants.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 4

<a id="n100-017"></a>
## N100-017 — Reversible nonlinear spatial cellular automaton

**Draft reference:** `S17` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** On the97-site path, first update even sites Y_i=P_i+lambda*P_(i-1)*P_(i+1) mod26 while odd sites stay P. Then update odd sites C_i=Y_i+mu*Y_(i-1)*Y_(i+1), while even sites stayY. Missing endpoint neighbors are fixed1. Invert odd pass, then even pass.
- **Bounds:** lambda,mu in1..25; exactly two checkerboard passes on the full path; no padding, extra round, or route.
- **Discriminating prediction:** Local influence propagates across overlapping neighboring triples; each pass is a reversible shear, with explicit endpoint behavior.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. lambda,mu in1..25; exactly two checkerboard passes on the full path; no padding, extra round, or route.
- **Closest local:** 
  - H-NONLINEAR-BLOCK
  - H-FEISTEL-2ROUND
  - H-FEISTEL-3ROUND
- **Closest external:** 
  - EXT-050
  - EXT-051
- **Novelty distinction:** Overlapping whole-message nonlinear cellular updates differ from scalar digraph Feistel and from the publicly proposed Rule30/110 keystream. General nonlinear-block umbrella overlap is acknowledged.
- **Eligibility:** operator-audit-pending
- **Sources:** 
  - https://github.com/mruckman1/k4_cipher/blob/e4912152555f635c35e73fe454a8302a98a5902f/docs/shift_sequence_hypotheses.md
  - https://dspace.mit.edu/entities/publication/06a8b271-428a-4379-955c-8c7334aa0288
  - https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0
- **Target run:** False
- **Identifiability limit:** This is a vector coupling, not a claim that adding rounds makes a solution identifiable; coefficient and plaintext aliases remain.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. operator-audit-pending
- **Proposed parameter descriptions:** 625
- **Proposed cost:** small-state exact enumeration
- **Specification status:** explicit proposal; independent correctness and prior-art admission gates still pending
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent simultaneous-array and inverse-pass producers, endpoint impulses, exhaustive small-path tests and blind97-letter plants.
  - **Negative:** Scalar adjacent-pair Feistel and autonomous CA-keystream controls; exact operator containment audit before counting novelty.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 4

<a id="n100-018"></a>
## N100-018 — CRT-controlled trigraph switchbox

**Draft reference:** `S18` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Add shared key k mod26 to every P symbol. For each full triple split into e in F2^3 and x in F13^3. Set e′=B e with B=[[1,1,0],[0,1,1],[1,1,1]]. Let s=sum(e) mod2. Set x′=A_s x, where A0=[[1,1,0],[0,1,1],[1,0,1]], A1=[[1,2,0],[0,1,2],[2,0,1]]. Recombine CRT. Tail singleton is P+k.
- **Bounds:** 26 keys; first96 symbols in triples from index0, singleton at96. Matrices and selector fixed.
- **Discriminating prediction:** The recovered parity plane determines which invertible mod13 matrix was used; cross-CRT control makes the full block map nonlinear.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. 26 keys; first96 symbols in triples from index0, singleton at96. Matrices and selector fixed.
- **Closest local:** 
  - H-AFFINE-DIGRAPH
  - H-NONLINEAR-BLOCK
- **Closest external:** 
  - EXT-041
  - EXT-050
- **Novelty distinction:** This is a controlled block operation, not merely changing Hill dimension, alphabet, or a CRT solver. Exact fixed-Hill overlap must be removed.
- **Eligibility:** operator-audit-pending
- **Sources:** 
  - https://github.com/nitsuah/kryptos/blob/main/docs/FEATURES.md
  - https://github.com/aciderix/kryptos-research-handoff/blob/6b82bd5364b6fea78b6ef3cfd73fafaf85ac3462/audits/autocle_groupes_2026_09_25/t36_autocle_groupes.py
- **Target run:** False
- **Identifiability limit:** One trace may use only one selector branch and look like Hill; such degenerate support is not evidence for the nonlinear switch.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. operator-audit-pending
- **Proposed parameter descriptions:** 26
- **Proposed cost:** small-state exact enumeration
- **Specification status:** explicit proposal; independent correctness and prior-art admission gates still pending
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent field and direct17576-entry trigraph permutations; verify every inverse and both selector branches.
  - **Negative:** Fixed Hill3x3 and decoupled-coordinate controls; prove a synthetic failure of any fixed linear matrix description.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 4

<a id="n100-019"></a>
## N100-019 — Extension-field power trigraphs

**Draft reference:** `S19` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** For triples identify x0+x1*t+x2*t^2 in F13[t]/(t^3-2); map X -> (X+a)^5. Separately map parity vector e -> B(e+b*1) using B from S18. Recombine CRT. For the last singleton use x->(x+a0)^5 mod13 and e->e xor b.
- **Bounds:** All2197 field shifts a and2 bits b; fixed irreducible polynomial, exponent5, origin and singleton rule.
- **Discriminating prediction:** Power5 is bijective because gcd(5,13^3-1)=1, but produces nonlinear cross-coordinate mixing rather than matrix multiplication.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. All2197 field shifts a and2 bits b; fixed irreducible polynomial, exponent5, origin and singleton rule.
- **Closest local:** 
  - H-NONLINEAR-BLOCK
  - H-AFFINE-DIGRAPH
- **Closest external:** 
  - EXT-041
  - EXT-050
- **Novelty distinction:** A fixed power permutation of an extension field is not a larger affine Hill matrix or an arbitrary extra Feistel round.
- **Eligibility:** operator-audit-pending
- **Sources:** 
  - https://github.com/nitsuah/kryptos/blob/main/docs/FEATURES.md
  - https://github.com/aciderix/kryptos-research-handoff/blob/6b82bd5364b6fea78b6ef3cfd73fafaf85ac3462/audits/autocle_groupes_2026_09_25/t36_autocle_groupes.py
- **Target run:** False
- **Identifiability limit:** The chosen field basis is ungrounded historically; equivalent field automorphisms are not independent hypotheses.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. operator-audit-pending
- **Proposed parameter descriptions:** 4394
- **Proposed cost:** moderate preflight algebra/table/inverse engineering; target domain bounded, runtime unmeasured
- **Specification status:** explicit proposal; independent correctness and prior-art admission gates still pending
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent polynomial-basis and multiplication-table field arithmetic; exhaustive field inversion and block round trips.
  - **Negative:** Linear Hill and scalar symbol-power controls; ensure synthetic cross-coordinate monomials are essential.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 4

<a id="n100-020"></a>
## N100-020 — Cycle-walked add-rotate-xor digraphs

**Draft reference:** `S20` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Rank each pair n=26*P0+P1. On10-bit integers apply F_k(n)=X(rotl10((n+k) mod1024,3)), where X(z)=z xor((z<<5)&1023). Repeatedly apply F_k until return to0..675. For the singleton restrict the same permutation to0..25.
- **Bounds:** All1024 k values; fixed pair origin0; max1024 primitive iterations per restricted application follows from permutation cycles.
- **Discriminating prediction:** Binary carry, rotation and triangular XOR interact before first-return format preservation.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. All1024 k values; fixed pair origin0; max1024 primitive iterations per restricted application follows from permutation cycles.
- **Closest local:** 
  - H-NONLINEAR-BLOCK
  - H-FEISTEL-2ROUND
- **Closest external:** 
  - EXT-050
  - EXT-051
- **Novelty distinction:** The core mixes binary operations with variable first-return iteration, not another alphabet or fixed added Feistel round. Protocol requires a source/operator overlap audit.
- **Eligibility:** operator-audit-pending
- **Sources:** 
  - https://www.cs.ucdavis.edu/~rogaway/papers/subset.pdf
  - https://dspace.mit.edu/entities/publication/06a8b271-428a-4379-955c-8c7334aa0288
  - https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0
- **Target run:** False
- **Identifiability limit:** Cycle walking is established mathematics; this toy10-bit construction has no security or creator-use claim, and trace aliases must be retained.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. operator-audit-pending
- **Proposed parameter descriptions:** 1024
- **Proposed cost:** moderate preflight algebra/table/inverse engineering; target domain bounded, runtime unmeasured
- **Specification status:** explicit proposal; independent correctness and prior-art admission gates still pending
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent explicit1024-permutation and inverse-circuit implementations; enumerate every cycle and every pair/tail input.
  - **Negative:** Affine mod676 and two-round scalar Feistel controls; test operator containment rather than relying on cipher labels.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 4

<a id="n100-021"></a>
## N100-021 — Prime-field power with first-return framing

**Draft reference:** `S21` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Rank a digraph0..675. Use F_k(n)=(n+k)^3 mod701, a permutation because701 is prime and gcd(3,700)=1. Cycle-walk back into0..675; singleton uses the same map restricted to0..25.
- **Bounds:** k=0..700; fixed prime701, exponent3, pair origin and tail rule; max701 primitive steps.
- **Discriminating prediction:** Restricted permutation cycles come from finite-field exponentiation, not coordinatewise letter arithmetic.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. k=0..700; fixed prime701, exponent3, pair origin and tail rule; max701 primitive steps.
- **Closest local:** 
  - H-NONLINEAR-BLOCK
  - H-FEISTEL-2ROUND
- **Closest external:** 
  - EXT-050
  - EXT-051
- **Novelty distinction:** Power permutation and ARX are different primitive operators with different algebraic invariants; no worldwide novelty or pre1990 attribution is asserted.
- **Eligibility:** operator-audit-pending
- **Sources:** 
  - https://www.cs.ucdavis.edu/~rogaway/papers/subset.pdf
  - https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0
- **Target run:** False
- **Identifiability limit:** This shares the cycle-walking wrapper with S20 but has a different core action; whether it merits separate prioritization depends on operator-level separation, not framing.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. operator-audit-pending
- **Proposed parameter descriptions:** 701
- **Proposed cost:** moderate preflight algebra/table/inverse engineering; target domain bounded, runtime unmeasured
- **Specification status:** explicit proposal; independent correctness and prior-art admission gates still pending
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent exponent/inverse-exponent maps and complete first-return tables for all inputs/keys.
  - **Negative:** Affine prime-field and ARX cycle-walk controls; exact comparisons prevent counting shared framing as a distinct result.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 4

<a id="n100-022"></a>
## N100-022 — Whole-message unit-inversion involution

**Draft reference:** `S22` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Rank all97 AZ letters as one big-endian integer N modulo M=26^97. For key b define U=N+b modM. If gcd(U,M)=1, output U^-1-b modM; otherwise outputN. Unrank exactly97 letters.
- **Bounds:** b=0..675; fixed length, endianness and no padding; identity-branch cases are separately marked as already-covered pure identity.
- **Discriminating prediction:** Applying the same transform twice restores N; the unit branch globally couples base26 digits and preserves unit status after translation.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. b=0..675; fixed length, endianness and no padding; identity-branch cases are separately marked as already-covered pure identity.
- **Closest local:** 
  - H-NONLINEAR-BLOCK
  - H-PERM
- **Closest external:** 
  - EXT-050
  - EXT-051
- **Novelty distinction:** Not the encoding proposal quotient reversal: modulus is fixed26^97, not a block-dependent numerator. No literal rearrangement or per-letter inverse is used.
- **Eligibility:** operator-audit-pending
- **Sources:** 
  - https://www.cs.ucdavis.edu/~rogaway/papers/subset.pdf
  - https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0
- **Target run:** False
- **Identifiability limit:** A small key bank is highly falsifiable but historically speculative; compatible whole-message inversion does not authenticate a source key.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. operator-audit-pending
- **Proposed parameter descriptions:** 676
- **Proposed cost:** small-state exact enumeration
- **Specification status:** explicit proposal; independent correctness and prior-art admission gates still pending
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent CRT inverses modulo2^97 and13^97 versus extended Euclid moduloM; exhaustive small-length analogues.
  - **Negative:** Identity/nonunit branches, affine digit maps and random involutions; never treat an identity fit as a fresh mechanism.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 4

<a id="n100-023"></a>
## N100-023 — Whole-message p-adic polynomial permutation

**Draft reference:** `S23` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** On N in Z/(26^97), set C_rank=N+26*a*N^2+b mod26^97. The derivative1+52*a*N is a unit modulo2 and13, and reduction modulo each prime is translation, yielding a bijection through Hensel lifting.
- **Bounds:** a=1..25,b=0..25; fixed big-endian97-digit representation; no arbitrary polynomial coefficients.
- **Discriminating prediction:** Low-order digits constrain successive higher digits by a nonlinear carry relation, allowing a digit-lifting inverse.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. a=1..25,b=0..25; fixed big-endian97-digit representation; no arbitrary polynomial coefficients.
- **Closest local:** 
  - H-CARRY-624
  - H-NONLINEAR-BLOCK
- **Closest external:** 
  - EXT-048
  - EXT-051
- **Novelty distinction:** This acts once on the entire base26 integer via a quadratic p-adic permutation, not a new modulus/readout of the tested scalar periodic-key accumulator.
- **Eligibility:** EXT-051-scope-unresolved
- **Sources:** 
  - https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0
  - https://github.com/scott-dunphy/kryptos-k4/blob/a75178587efe9401ebf2a4edf3828472dd6fb2a2/novel/run_chain.py
- **Target run:** False
- **Identifiability limit:** Finite polynomial permutation does not imply historical plausibility; a target fit must survive all fixed digits, not just low-order crib constraints.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. EXT-051-scope-unresolved
- **Proposed parameter descriptions:** 650
- **Proposed cost:** moderate preflight algebra/table/inverse engineering; target domain bounded, runtime unmeasured
- **Specification status:** explicit proposal; independent correctness and prior-art admission gates still pending
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent Hensel-digit and CRT inverse solvers; exhaustive small-digit bijection checks before97-digit plants.
  - **Negative:** Linear whole-rank and carry624 controls; test invariants and full round trips under both primes.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 4

<a id="n100-024"></a>
## N100-024 — Adler-inspired rational pair scattering

**Draft reference:** `S24` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** For a pair(x,y) in Z26 set s=x+y. If s is a unit modulo26, let R_d(x,y)=(y+d/s,x-d/s); otherwise let R_d(x,y)=(y,x). Apply independently to48 pairs; last singleton unchanged.
- **Bounds:** d=1..25, origin0; division only at units; no padding or fitted exceptional cases.
- **Discriminating prediction:** Pair sum is conserved and R_d is an involution, including the fixed swap branch.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. d=1..25, origin0; division only at units; no padding or fitted exceptional cases.
- **Closest local:** 
  - H-NONLINEAR-BLOCK
  - H-FEISTEL-2ROUND
  - H-SUM-ROTATION
- **Closest external:** 
  - EXT-050
  - EXT-051
- **Novelty distinction:** A sum-dependent rational change of symbol values is not checksum-selected rotation of message positions. Known Adler-map mathematics is only inspiration.
- **Eligibility:** operator-audit-pending
- **Sources:** 
  - https://arxiv.org/abs/math/0307009
  - https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0
- **Target run:** False
- **Identifiability limit:** Conserved sums are a strong necessary condition but not sufficient evidence. The singular extension is NOT claimed to retain the Yang-Baxter property.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. operator-audit-pending
- **Proposed parameter descriptions:** 25
- **Proposed cost:** small-state exact enumeration
- **Specification status:** explicit proposal; independent correctness and prior-art admission gates still pending
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent algebraic inverse and exhaustive676-entry pair tables for every d; unit/nonunit boundary tests.
  - **Negative:** Pure swap and affine digraph controls; synthetic witnesses against the frozen scalar two-round Feistel grammar.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 4

<a id="n100-025"></a>
## N100-025 — Plaintext-switched affine state over29

**Draft reference:** `S25` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** State t in F29 emits C=P+(t mod26). Update t′=(1+2*1[P is A,E,I,O,U])*t+P mod29.
- **Bounds:** All29 starting states; AZ vowels fixed; no free update table, key clock, or offset.
- **Discriminating prediction:** Vowels multiply the stored state by3 while consonants preserve its multiplier; input order matters to the composed affine transformations.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. All29 starting states; AZ vowels fixed; no free update table, key clock, or offset.
- **Closest local:** 
  - H-PLAINTEXT-EXTRA-STEP
  - H-AUTONOMOUS-RECURRENCE
- **Closest external:** 
  - EXT-030
  - EXT-048
  - EXT-051
- **Novelty distinction:** The plaintext class changes a state multiplier and writes the symbol into state, rather than skipping an immutable keyword position.
- **Eligibility:** operator-audit-pending
- **Sources:** 
  - https://github.com/Barneyjm/kryptos-k4/blob/2db2722cc3f18c52d4d8369d7adc5a1db7e859d7/scripts/fe_interrupt.py
  - https://github.com/scott-dunphy/kryptos-k4/blob/a75178587efe9401ebf2a4edf3828472dd6fb2a2/novel/run_chain.py
  - https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0
- **Target run:** False
- **Identifiability limit:** The29-to26 projection causes collisions; zero or special states can mimic simpler traces and should not be promoted.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. operator-audit-pending
- **Proposed parameter descriptions:** 29
- **Proposed cost:** small-state exact enumeration
- **Specification status:** explicit proposal; independent correctness and prior-art admission gates still pending
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent affine-composition and scalar-step implementations, vowel/consonant order-reversal witnesses and blind plants.
  - **Negative:** Vowel extra-step key schedules and fixed-coefficient linear feedback controls; complete finite null relations.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 4

<a id="n100-026"></a>
## N100-026 — Tropical minimum-cost memory cipher

**Draft reference:** `S26` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** State d in{-4..4}; emit C=P+k+d mod26. Let r=1 for a vowel,0 otherwise; update d′=clip(d,-3,3)+1-2*r. Equivalently update two normalized min-plus path costs with switch penalty3 and opposing unit emission costs.
- **Bounds:** 9 initial differences and26 offsets; switch penalty and vowel class fixed.
- **Discriminating prediction:** Repeated classes saturate the cost difference, while mixed classes retain a bounded path-cost memory rather than wrapping modulo a period.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. 9 initial differences and26 offsets; switch penalty and vowel class fixed.
- **Closest local:** 
  - H-CIPHERTEXT-EXTRA-STEP
  - H-PLAINTEXT-EXTRA-STEP
- **Closest external:** 
  - EXT-030
  - EXT-051
- **Novelty distinction:** Min-plus minimization creates noninvertible saturation/merging, not ordinary modular recurrence or another periodic-key width.
- **Eligibility:** operator-audit-pending
- **Sources:** 
  - https://doi.org/10.1109/TIT.1967.1054010
  - https://github.com/Barneyjm/kryptos-k4/blob/2db2722cc3f18c52d4d8369d7adc5a1db7e859d7/scripts/fe_interrupt.py
  - https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0
- **Target run:** False
- **Identifiability limit:** This reduces to a nine-state saturating counter, which must be stated rather than marketed as an unconstrained Viterbi decoder; state aliases are possible.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. operator-audit-pending
- **Proposed parameter descriptions:** 234
- **Proposed cost:** small-state exact enumeration
- **Specification status:** explicit proposal; independent correctness and prior-art admission gates still pending
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent two-cost min-plus recurrence versus clipped-difference implementation; saturation and switching controls.
  - **Negative:** Cyclic keyword clocks and memoryless class substitution; complete compatible state/key sets on null controls.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 4

<a id="n100-027"></a>
## N100-027 — Ehrenfest symbol-parity memory

**Draft reference:** `S27` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Maintain a26-bit set S of letters seen an odd number of times. Emit C=P+k+popcount(S) mod26, then toggle bit P.
- **Bounds:** Initial S is empty or full,26 offsets; no arbitrary26-bit fitted seed.
- **Discriminating prediction:** A repeated pair of the same plaintext letter restores state, while different letters alter global odd-occurrence population.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. Initial S is empty or full,26 offsets; no arbitrary26-bit fitted seed.
- **Closest local:** 
  - H-RECURRENCE-CLOCK
  - H-CANONICAL-RESIDUAL-FEEDBACK
- **Closest external:** 
  - EXT-030
  - EXT-051
- **Novelty distinction:** The shift aggregates parity memory for all26 plaintext symbols; it neither selects an immutable keyword entry nor observes only six preceding ciphertext symbols.
- **Eligibility:** operator-audit-pending
- **Sources:** 
  - https://github.com/Barneyjm/kryptos-k4/blob/2db2722cc3f18c52d4d8369d7adc5a1db7e859d7/scripts/fe_interrupt.py
  - https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0
- **Target run:** False
- **Identifiability limit:** Many histories share the same population count but differ in future response; fitting only the scalar count is insufficient.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. operator-audit-pending
- **Proposed parameter descriptions:** 52
- **Proposed cost:** small-state exact enumeration
- **Specification status:** explicit proposal; independent correctness and prior-art admission gates still pending
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent bitset and per-letter parity-count implementations; repeated-pair restoration and full/empty duality controls.
  - **Negative:** Occurrence-count keyword displacement and finite-lag equality feedback controls; exact null relation enumeration.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 4

<a id="n100-028"></a>
## N100-028 — Deterministic Ising relaxation state

**Draft reference:** `S28` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Four spins s_j on a ring emit C=P+k+binary_code(s) mod26. After P, replace external fields by h_(P mod4)=+3 if P<13 else-3, all others0. With E=-sum s_j*s_(j+1)-sum h_j*s_j, repeatedly flip the lowest-index spin strictly lowering E until none does.
- **Bounds:** All16 initial spin vectors and26 offsets; fixed coupling1, field magnitude3, ring and tie rule. Strict energy descent visits at most16 states per update.
- **Discriminating prediction:** Internal avalanches decrease a fixed energy and may end in metastable states; relaxation order is part of the operator, not interchangeable.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. All16 initial spin vectors and26 offsets; fixed coupling1, field magnitude3, ring and tie rule. Strict energy descent visits at most16 states per update.
- **Closest local:** 
  - H-CARRY-624
  - H-TREE-STATEFUL
- **Closest external:** 
  - EXT-048
  - EXT-051
- **Novelty distinction:** Energy-decreasing spin relaxation is not abelian toppling: its invariant, noncommutation and update semantics differ. This is a mathematical state cipher, not a physical-site claim.
- **Eligibility:** operator-audit-pending
- **Sources:** 
  - https://doi.org/10.1103/PhysRevLett.64.1613
  - https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0
- **Target run:** False
- **Identifiability limit:** Several initial states may coalesce; the physical analogy supplies no evidence of an actual magnetic mechanism in Kryptos.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. operator-audit-pending
- **Proposed parameter descriptions:** 416
- **Proposed cost:** small-state exact enumeration
- **Specification status:** explicit proposal; independent correctness and prior-art admission gates still pending
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent energy-recalculation and local-delta implementations, all16x26 transitions and metastable/tie cases.
  - **Negative:** Global-minimum relaxation, sandpile and single-threshold-state controls; distinguish these operators on synthetic histories.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 4

<a id="n100-029"></a>
## N100-029 — Small Blum-Micali stream

**Draft reference:** `S29` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** For p in{31,47,59,83,107,167, 227}, choose the least positive primitive root g. State x in1..p-1 emits bit1[x>(p-1)/2], then x′=g^x modp. Pack5 bits MSB-first modulo26; C=P+K mod26.
- **Bounds:** Exactly listed primes and all nonzero seeds; least-root convention, no burn-in, fixed first-bit timing.
- **Discriminating prediction:** Thresholded discrete-exponentiation dynamics supplies the entire stream from one small seed.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. Exactly listed primes and all nonzero seeds; least-root convention, no burn-in, fixed first-bit timing.
- **Closest local:** 
  - H-AUTONOMOUS-RECURRENCE
- **Closest external:** 
  - EXT-010
  - EXT-051
- **Novelty distinction:** Discrete-exponentiation state evolution is not quadratic-residue squaring or linear feedback; both are classical external constructions, not inventions here.
- **Eligibility:** EXT-051-scope-unresolved
- **Sources:** 
  - https://epubs.siam.org/doi/10.1137/0213053
  - https://github.com/ActiveTK/dekrypt/blob/992c9668b9f0783221cb570abbff969e59cbf27c/src/s225_lfsr_chunks.py
  - https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0
- **Target run:** False
- **Identifiability limit:** Small instances have no cryptographic-security claim. Equivalent streams across moduli must be counted once.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. EXT-051-scope-unresolved
- **Proposed parameter descriptions:** 714
- **Proposed cost:** small-state exact enumeration
- **Specification status:** explicit proposal; independent correctness and prior-art admission gates still pending
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent modular-exponentiation and complete transition-table generators; primitive-root proof and threshold-boundary controls.
  - **Negative:** BBS, LFSR and random streams; complete finite-bank null tests.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 4

<a id="n100-030"></a>
## N100-030 — Inversive congruential hidden-state stream

**Draft reference:** `S30` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** State x in F251 evolves x′=a*inv0(x)+b, with inv0(0)=0; emit K=x mod26, then C=P+K mod26.
- **Bounds:** a=1..250,b=0..250,x0=0..250; prime251 and emit-before-update fixed; no other output extraction.
- **Discriminating prediction:** Reciprocal transition is a permutation for a!=0 and produces a hidden-state stream not governed by a fixed low-order linear letter recurrence.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. a=1..250,b=0..250,x0=0..250; prime251 and emit-before-update fixed; no other output extraction.
- **Closest local:** 
  - H-AUTONOMOUS-RECURRENCE
- **Closest external:** 
  - EXT-048
  - EXT-051
- **Novelty distinction:** Not S02: here a251-state hidden generator has a many-to-one letter readout, whereas S02 permutes the26-symbol projective alphabet using ciphertext transport. Broad polynomial-recurrence prior scope remains unknown.
- **Eligibility:** EXT-051-scope-unresolved
- **Sources:** 
  - https://doi.org/10.1145/224401.224612
  - https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0
- **Target run:** False
- **Identifiability limit:** 15,750,250 descriptions may collapse to identical observed streams; an exact survivor count is not a count of unique ciphers or plaintexts.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. EXT-051-scope-unresolved
- **Proposed parameter descriptions:** 15750250
- **Proposed cost:** large finite enumeration; benchmark before target
- **Specification status:** explicit proposal; independent correctness and prior-art admission gates still pending
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent inversion table and extended-Euclid producers, zero crossing and complete short transition cycles.
  - **Negative:** Affine congruential and direct PGL alphabet-action controls; independent full-domain consistency checker.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 4

<a id="n100-031"></a>
## N100-031 — Nonabelian Fibonacci key recurrence

**Draft reference:** `S31` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** In D13 with product from S01, choose g0,g1 and set g_i=g_(i-1)*g_(i-2). Emit rank(r,e)=r+13e as K_i and C_i=P_i+K_i mod26.
- **Bounds:** All676 ordered seed pairs, fixed product order and rank readout; no extra offset or alphabet.
- **Discriminating prediction:** Key evolution is autonomous but multiplication order matters; the rotational coordinate is switched by prior reflection bits.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. All676 ordered seed pairs, fixed product order and rank readout; no extra offset or alphabet.
- **Closest local:** 
  - H-AUTONOMOUS-RECURRENCE
- **Closest external:** 
  - EXT-041
  - EXT-048
  - EXT-051
- **Novelty distinction:** Unlike S01 it generates an autonomous key, rather than multiplying plaintext symbols; unlike fixed linear recurrences its sign action is part of the evolving group state.
- **Eligibility:** operator-audit-pending
- **Sources:** 
  - https://github.com/aciderix/kryptos-research-handoff/blob/6b82bd5364b6fea78b6ef3cfd73fafaf85ac3462/audits/autocle_groupes_2026_09_25/t36_autocle_groupes.py
  - https://github.com/scott-dunphy/kryptos-k4/blob/a75178587efe9401ebf2a4edf3828472dd6fb2a2/novel/run_chain.py
  - https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0
- **Target run:** False
- **Identifiability limit:** Commuting seeds can collapse to old cyclic laws; only demonstrably noncommutative residual operators could be admitted.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. operator-audit-pending
- **Proposed parameter descriptions:** 676
- **Proposed cost:** small-state exact enumeration
- **Specification status:** explicit proposal; independent correctness and prior-art admission gates still pending
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent Cayley-table and semidirect-coordinate recurrence; commuting and noncommuting seed pairs tested separately.
  - **Negative:** Abelian Fibonacci and ordinary additive-recurrence controls; remove globally equivalent already-attempted subdomains.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 4

<a id="n100-032"></a>
## N100-032 — Eight-bit feedback-with-carry stream

**Draft reference:** `S32` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** State r0..r7 bits and carry c in0..3. Emit r0, compute w=c+r0+r2+r5+r7, shift left and append w mod2, set c′=floor(w/2). Pack5 output bits MSB-first modulo26; add to P.
- **Bounds:** All256x4 initial states; fixed taps and carry bound; no arbitrary connection integer or bit extraction search.
- **Discriminating prediction:** Integer carry introduces nonlinear memory while keeping the declared carry set closed.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. All256x4 initial states; fixed taps and carry bound; no arbitrary connection integer or bit extraction search.
- **Closest local:** 
  - H-CARRY-624
  - H-AUTONOMOUS-RECURRENCE
- **Closest external:** 
  - EXT-010
  - EXT-049
  - EXT-051
- **Novelty distinction:** Binary feedback carry is not a changed modulus of the tested periodic-key scalar accumulator. Exact prior supersets and short-cycle coincidences still require screening.
- **Eligibility:** operator-audit-pending
- **Sources:** 
  - https://www.cs.uky.edu/~klapper/pdf/fcsr.pdf
  - https://github.com/ActiveTK/dekrypt/blob/992c9668b9f0783221cb570abbff969e59cbf27c/src/s225_lfsr_chunks.py
  - https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0
- **Target run:** False
- **Identifiability limit:** Zero/short-cycle and observationally equivalent states must be removed or labeled as old overlaps;1990s FCSR literature is later than Kryptos, so historical prior is low.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. operator-audit-pending
- **Proposed parameter descriptions:** 1024
- **Proposed cost:** small-state exact enumeration
- **Specification status:** explicit proposal; independent correctness and prior-art admission gates still pending
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent integer arithmetic versus Boolean/carry truth table; all1024 transitions and carry extremes.
  - **Negative:** Carry-suppressed LFSR and base624 accumulator controls; synthetic linear-complexity witnesses against order<=30 containment.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 4

<a id="n100-033"></a>
## N100-033 — Geffe nonlinear combiner stream

**Draft reference:** `S33` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Three regularly clocked binary LFSRs use x^5+x^2+1, x^7+x+1, x^9+x^4+1. Combine simultaneous outputs z=(a AND b) XOR((NOT a) AND c); pack5 z bits MSB-first modulo26 and add to P.
- **Bounds:** All31x127x511 nonzero state triples; fixed taps, output timing and packing; no Boolean-function search.
- **Discriminating prediction:** Multiplicative Boolean cross-terms combine three independent states; switching correlations differ from a single LFSR.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. All31x127x511 nonzero state triples; fixed taps, output timing and packing; no Boolean-function search.
- **Closest local:** 
  - H-AUTONOMOUS-RECURRENCE
- **Closest external:** 
  - EXT-010
  - EXT-051
- **Novelty distinction:** Not merely another5-bit extraction: a nonlinear multi-register product combines states. Geffe1973 is explicit general prior art; exact K4 attempted scope is unresolved.
- **Eligibility:** operator-audit-pending
- **Sources:** 
  - https://www.worldradiohistory.com/Archive-Electronics/70s/73/Electronics-1973-01-04.pdf
  - https://github.com/ActiveTK/dekrypt/blob/992c9668b9f0783221cb570abbff969e59cbf27c/src/s225_lfsr_chunks.py
  - https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0
- **Target run:** False
- **Identifiability limit:** Some seeds produce reducible/short-complexity streams and are old-model overlaps; full observed-trace and plaintext alias counts are required.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. operator-audit-pending
- **Proposed parameter descriptions:** 2011807
- **Proposed cost:** large finite enumeration; benchmark before target
- **Specification status:** specification-blocked until exact bit/state/canonical-cycle orientation is frozen independently; no target authority
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent gate and truth-table combiners; primitive-polynomial verification and blind plants spanning all selector regimes.
  - **Negative:** XOR combiner, ordinary order<=30 LFSR and stop-and-go controls; prove a noncontained synthetic stream before admission.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 4

<a id="n100-034"></a>
## N100-034 — Conjugacy-orbit automaton

**Draft reference:** `S34` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** State q in S4 emits C=P+k+LehmerRank(q) mod26. Let a=(0123),b=(012), g(P)=a^(P mod4)*b^(floor(P/4) mod3). Update q′=g(P) q g(P)^-1.
- **Bounds:** All24 initial permutations and26 offsets; rank order0..23 and composition convention fixed; identity-state Caesar branch excluded.
- **Discriminating prediction:** Cycle type of q is invariant, but state labels move through a conjugacy orbit according to noncommuting plaintext actions.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. All24 initial permutations and26 offsets; rank order0..23 and composition convention fixed; identity-state Caesar branch excluded.
- **Closest local:** 
  - H-EVOLVING-ALPHABET
  - H-AUTONOMOUS-RECURRENCE
- **Closest external:** 
  - EXT-041
  - EXT-048
  - EXT-051
- **Novelty distinction:** Unlike S10 left multiplication, conjugation preserves a nontrivial cycle-type invariant. It does not reorder an alphabet or add a rotor to a known machine.
- **Eligibility:** operator-audit-pending
- **Sources:** 
  - https://github.com/aciderix/kryptos-research-handoff/blob/6b82bd5364b6fea78b6ef3cfd73fafaf85ac3462/audits/autocle_groupes_2026_09_25/t36_autocle_groupes.py
  - https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0
- **Target run:** False
- **Identifiability limit:** Only a conjugacy orbit is explored and some rank shifts can alias k; complete state/plaintext relations are needed.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. operator-audit-pending
- **Proposed parameter descriptions:** 598
- **Proposed cost:** small-state exact enumeration
- **Specification status:** explicit proposal; independent correctness and prior-art admission gates still pending
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent permutation-array and cycle-notation implementations; conjugacy invariants and noncommuting history controls.
  - **Negative:** Left-product accumulator and fixed-substitution controls; operator-equivalence tests remove central/degenerate states.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 4

<a id="n100-035"></a>
## N100-035 — Braid-normal-form feedback

**Draft reference:** `S35` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Maintain a braid in B3=<sigma1,sigma2 | sigma1 sigma2 sigma1=sigma2 sigma1 sigma2>. In left Garside normal form Delta^p x1...xr, emit C=P+k+(p+3r) mod26. Append sigma1,sigma1^-1,sigma2,sigma2^-1 according to P mod4 and normalize.
- **Bounds:** Initial braids represented by words of length<=2, deduplicated by normal form;26 offsets; after97 letters raw word length<=99; fixed normal-form convention.
- **Discriminating prediction:** Braid-related words, not just adjacent inverse pairs, reach the same state and identical continuation behavior.
- **Bounded test:** After separate admission only: enumerate the complete frozen parameter domain, retain every key/state/plaintext matching all 24 clues, independently re-encrypt all 97 symbols. Stop as EMPTY, NONEMPTY_AMBIGUOUS, CONDITIONAL_UNIQUE, or INCOMPLETE; no language-score selection or parameter rescue. Initial braids represented by words of length<=2, deduplicated by normal form;26 offsets; after97 letters raw word length<=99; fixed normal-form convention.
- **Closest local:** 
  - H-TREE-STATEFUL
  - H-CANONICAL-RESIDUAL-FEEDBACK
- **Closest external:** 
  - EXT-048
  - EXT-051
- **Novelty distinction:** This is not adding a stack depth: the braid relation identifies histories that remain different in free-group cancellation, changing future state evolution.
- **Eligibility:** operator-audit-pending
- **Sources:** 
  - https://www.iacr.org/archive/crypto2000/18800166/18800166.pdf
  - https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0
- **Target run:** False
- **Identifiability limit:** The readout(p,r) loses much braid information; initial normal forms and observational equivalence must be reported. Braid cryptography sources are post1990, not historical attribution.
- **Prior art status:** No identical exact K4 operator located in the bounded inspected record; NOT a novelty clearance. operator-audit-pending
- **Proposed parameter descriptions:** 442
- **Proposed cost:** moderate preflight algebra/table/inverse engineering; target domain bounded, runtime unmeasured
- **Specification status:** explicit proposal; independent correctness and prior-art admission gates still pending
- **Cost note:** Description counts are not unique operators, target attempts, or measured runtimes. Control work must separately establish tractability.
- **Controls:** 
  - **Positive:** Independent Garside normalizer and faithful B3 representation/word-problem checker; braid relation, inverse cancellation and blind plants.
  - **Negative:** Free-group stack S08 and abelian exponent-sum controls; verify neither is substituted for braid equality.
  - **Shared:** Before target authority: two independently authored implementations; exhaustive tiny-domain inverse/transition truth sets where practical;64 fresh blind97-letter plants and64 null controls, with24 reveal positions fixed to the K4 clue pattern. Independent analyst supplies controls. Report full compatible sets, never demand intended-key uniqueness when aliases exist. Certify deliberately inconsistent negatives separately from random nulls.
- **Estimated cost:** Design/source/inverse gate first. Proposed tiny-oracle pilot cap180 CPU seconds; complete seed-domain cost must be separately measured and frozen before admission. No target scan allocated or run.
- **Priority:** 4
