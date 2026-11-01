# Earlier-section derived mechanisms

All entries are proposed and unrun. A specified research question is not a novelty clearance or permission to launch a K4 search. See [README](README.md) for gates, priorities and source limitations.

<a id="n100-044"></a>
## N100-044 — Earlier-section conditional-frequency permutation bank

**Draft reference:** `E01` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Kind:** mechanism
- **Status:** specified speculative proposal; unrun; eligibility conditional
- **Evidence grade:** Earlier sections are real independent data; the proposed statistical use is invented and explicitly unattributed.
- **Mechanism:** Build a static alphabet permutation for each previous-plaintext letter from bigram frequencies in K1-K3. The previous decoded letter selects the next row. This is a fixed finite-context substitution bank, not a keyword search, adaptive count model, or ordinary running key.
- **Forward model:** 
  - **Source:** Freeze one baseline-consistent transcription of the solved as-carved K1, K2, and K3 plaintexts; preserve their literal spelling, X separators and as-carved K2 ending, strip nonletters, and count bigrams WITHIN each section, not across artificial concatenation boundaries. Do not sweep corrected/uncorrected editions.
  - **Table:** For a,b in AZ, n[a,b] is the number of within-section occurrences of ab. L_a is AZ sorted by descending n[a,b], ties by AZ order. Thus every L_a is a permutation, even when a never occurs. No learned numerical weights or fitted entries.
  - **State:** s_0 is the final literal letter of K3. For each input plaintext P_i, emit C_i=AZ[index(L_s,P_i)] and set s=P_i.
  - **Inverse:** At state s, P_i=L_s[index(AZ,C_i)]; then s=P_i. Each row is a permutation, so encryption and decryption are sequential and exact.
  - **Alignment:** Exactly one plaintext letter per ciphertext letter, no resets at public clues, global stream begins at i=0. All public plaintext positions retain their ordinary global indices.
  - **Finite domain:** One source policy, one deterministic bank, one fixed initial state, one AZ output convention, one 97-symbol model. No alphabet/phase/keyword/normalization sweep. If source ambiguity cannot be resolved independently, status becomes evidence-blocked rather than a source-choice search.
- **Measurable prediction:** The independently built 26-row bank determines exactly one complete decryption and full re-encryption. A disagreement at any disclosed plaintext position falsifies this exact model. The empirical rows and all decoded symbols are fixed without fitting to K4.
- **Prior art:** 
  - **Closest local:** 
    - H-AUTOKEY-EXACT
    - H-ASYMMETRIC-FEEDBACK
    - H-EVOLVING-ALPHABET
    - H-RUNKEY
  - **Closest external:** 
    - EXT-009
    - EXT-030
    - EXT-044
    - EXT-047
    - EXT-048
  - **Additional primary source:** https://github.com/mruckman1/k4_cipher/blob/e4912152555f635c35e73fe454a8302a98a5902f/experiments/033b_per_position_state_dependent.py
  - **Comparison:** The additionally inspected 033b source uses a finite keyword-derived pool with position/current-ciphertext/ciphertext-prefix selectors; it does not construct K1-K3 bigram-ranked rows selected by recovered plaintext. Its source is not a negative for E01. Ordinary additive autokey has cyclic/conjugate row structure; E01 permits independently noncyclic rows. Unlike a literal earlier-section running key, E01 reads a conditional frequency table, not one successive source character. Unlike A02's adaptive transition-count proposal, E01 never updates counts.
  - **Required operator gate:** Before any target run, inspect the actual source-built row table without K4. Test whether it collapses to a previously attempted same-alphabet/autokey/finite-bank operator. A column collision in the context-to-output table can certify non-Latin behavior, separating it from ordinary common-alphabet additive autokey; absent such a witness, do not assert separation. Wider prior arbitrary-bank/selector scope remains a bounded uncertainty.
  - **Novelty limit:** No exact source-trained operator was located in the finite inspected record. This is not worldwide novelty or completed eligibility. Merely selecting another corpus or tie-break would not create another hypothesis.
- **Finite falsifiable test:** After source freeze, independent inverse audit, source-degeneracy audit and separate authority: decode once continuously, compare all 24 public clue letters, and re-encode all 97 symbols. Return exact incompatible, exact compatible, or incomplete. Do not retune the source/tie-break after failure. A compatible output is conditional on this model, not an intended-solution claim.
- **Positive controls:** 
  - Independently verify each of the 26x26 row mappings and inverses before target use.
  - Exhaustively test tiny-alphabet surrogate banks and all short messages through length 5; include zero-frequency contexts and tied counts.
  - Freeze a blind batch of 64 independent 97-letter synthetic messages and require exact full roundtrip under the unmodified source-building procedure. These are proposed controls, not completed tests.
- **Negative controls:** 
  - For each planted message, change one asserted plaintext position away from its unique decoded value; the exact compatibility checker must reject.
  - Use length-matched shuffled-reference sources preserving unigram counts but changing bigrams, and independently shuffled ciphertexts. Report accidental clue survival instead of presuming that every shuffle must reject.
  - Confirm the program never inserts supplied clues into the decoded output and never restarts state at a clue boundary.
- **Required independent input:** Authenticated, versioned literal K1-K3 plaintext transcription and an independently declared normalization policy. Existing known plaintexts may supply this input, but no K4-derived table entries, corpus selection, or additional clues are allowed. No source has been found linking Sanborn to conditional-frequency sorting.
- **Identifiability limit:** With the bank and start state fixed, decryption is unique. That trivial conditional uniqueness does not identify the intended mechanism; many unrelated bijections can also determine one output. Compatible cribs and roundtrip do not authenticate the source-to-table rule. Sparse source counts make the bank heavily tie-break-dependent.
- **Priority:** Low; worthwhile only as a fully disclosed small speculative mechanism, not an evidence-led physical lead.
- **Estimated cost:** Source freeze and operator audit first; proposed tiny-oracle/synthetic pilot cap60 CPU seconds after an exact protocol is frozen. One deterministic97-symbol decoder is specified, but target feasibility and authorization are separate and no timing has been measured.

<a id="n100-045"></a>
## N100-045 — Circular earlier-text next-occurrence rank cursor

**Draft reference:** `E02` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Kind:** mechanism
- **Status:** specified speculative proposal; unrun; eligibility conditional
- **Evidence grade:** Uses independently known earlier text as a finite reference object; no creator evidence for the cursor/ranking rule.
- **Mechanism:** At a moving cursor on a circular earlier-section text, the order in which distinct letters next appear supplies a complete substitution alphabet. Encrypt a letter by its rank in that order, then move the cursor past that letter's first encountered occurrence. The reference text is immutable, but cursor travel is plaintext-dependent.
- **Forward model:** 
  - **Source:** Use the same single independently frozen as-carved K1-K3 plaintext normalization as E01. Concatenate in section order, then append each AZ letter absent from the whole reference exactly once in AZ order. This completion convention is a disclosed design choice, not a clue. Call the resulting finite circular string R of length N.
  - **Alphabet at state:** At cursor q, scan at most one full circuit of R and retain each letter only at its first encounter. The resulting A_q is a permutation of AZ. Let d(q,p) be the least nonnegative distance to an occurrence of p.
  - **State:** q_0=0. Emit C_i=AZ[index(A_q,P_i)] and set q'=(q+d(q,P_i)+1) mod N.
  - **Inverse:** P_i=A_q[index(AZ,C_i)], then use the same first-occurrence rule to update q. The output rank uniquely selects a letter at each state, so the entire stream is invertible.
  - **Alignment:** One plaintext symbol becomes one ciphertext symbol. There are no clue-boundary resets, padding, deleted symbols, or unknown processed indices.
  - **Finite domain:** One reference policy, forward scan, AZ output, q_0=0, 97 sequential symbols. No all-starts search, reversed source, alternative alphabet, correction sweep or extra substitution layer is included.
- **Measurable prediction:** The independent reference and fixed cursor produce a complete deterministic ciphertext/plaintext mapping. Source-derived state traces and every output letter are reproducible without choosing positions from K4. Any public clue mismatch rejects the exact model.
- **Prior art:** 
  - **Closest local:** 
    - H-EVOLVING-ALPHABET
    - H-RUNKEY
    - H-RECURRENCE-CLOCK
    - H-BOUNDARY-STATE
  - **Closest external:** 
    - EXT-008
    - EXT-030
    - EXT-034
    - EXT-047
  - **Primary sources:** 
    - https://github.com/mruckman1/k4_cipher/blob/e4912152555f635c35e73fe454a8302a98a5902f/experiments/033b_per_position_state_dependent.py
    - https://github.com/ElodineOfficial/KrackersAndCheese/blob/2ea3c11e9b80ccbac1c928c8688d01154f976e1b/full_password_slider.py
    - https://github.com/markmnl/kryptos/blob/090347cbd3fd9329d59df3edcf999964edc9b873/WHAT_WE_TRIED.md
  - **Comparison:** E02 is not literal running-key subtraction, a key indexed by ciphertext recurrence distance, or a single mutable alphabet updated by the covered swap/prefix-reversal rules. The next-occurrence order depends on repeated letters in an immutable source ring and an evolving cursor. EXT-034's broad MTF/MTB reporting remains an overlap gate, not a newly inherited negative.
  - **Operator witness:** Pure synthetic symbolic witness, not executed: on reference ABACBC over ABC, state q=0 has alphabet ABC. Selecting C moves to q=4 and alphabet BCA. A single move-to-back C would leave ABC, move-to-front C yields CAB, and reversal through C or head/C swap yields CBA; therefore those stated one-step rules are not the same operator. Also prefixes A and ABA end in the same plaintext letter but reach alphabets BAC and CBA, respectively, separating this source-cursor grammar from E01's last-letter-only bank.
  - **Required operator gate:** Prove actual source-induced automaton nondegeneracy and compare it with the exact evolving/MTF/MTB source grammars before admission. The toy witness proves a grammar difference, not a blanket difference for every possible reference or evidence about the selected K1-K3 trace.
  - **Novelty limit:** Finite web searches found no matching K4 next-occurrence-rank cursor. Unknown broader source scope is retained. Changing reference text or cursor origin would be a parameter variant, not a new hypothesis.
- **Finite falsifiable test:** After the independent source freeze, nondegeneracy/overlap review, controls and separate authority, perform exactly one continuous decode, require all 24 public clues and full 97-symbol re-encryption. Report exact incompatibility or a conditional compatible plaintext without retuning. No target calculation has been performed here.
- **Positive controls:** 
  - For all N source states and all 26 letter inputs, independently verify that the rank alphabet is a permutation and that forward/inverse transitions coincide.
  - Exhaustively test tiny circular references containing every toy-alphabet symbol, including repeated symbols, wraparound, and absent-symbol completion; enumerate short messages through length 5.
  - Use 64 blind 97-letter plants, including repeated-letter runs that repeatedly wrap the reference. Require exact full plaintext and final-cursor recovery.
- **Negative controls:** 
  - A deliberately incorrect asserted plaintext letter must be rejected against the unique decoded stream.
  - A mutant decoder that advances only one source position or uses the last rather than next occurrence must fail a predeclared separating toy case.
  - Shuffle the reference while preserving all letter counts; record how often the frozen clue test survives. This probes whether order, rather than an accidental histogram feature, supplies apparent evidence. Do not claim every shuffled reference must fail.
- **Required independent input:** Versioned K1-K3 plaintext, exact section order and fixed absent-letter completion policy. A historical link to this next-occurrence ranking device is absent. If provenance of the source literal cannot be fixed, the proposal is evidence-blocked; no fabricated reference letters are allowed beyond the explicitly declared mathematical completion rule.
- **Identifiability limit:** The fixed source and start state give unique decoding, but not intended-mechanism identification. Equivalent reference strings may induce the same reachable automaton. A finite target trace may coincide with an already-tried operator even when the full grammar differs. Source changes/start searches would inflate flexibility and are outside this proposal.
- **Priority:** Low speculative; more mechanically concrete than unsupported geometry, but no physical or archival endorsement.
- **Estimated cost:** Source freeze and operator audit first; proposed tiny-oracle/synthetic pilot cap60 CPU seconds after an exact protocol is frozen. One deterministic97-symbol decoder is specified, but target feasibility and authorization are separate and no timing has been measured.
