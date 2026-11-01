# Reversible representation and routing mechanisms

All entries are proposed and unrun. A specified research question is not a novelty clearance or permission to launch a K4 search. See [README](README.md) for gates, priorities and source limitations.

<a id="n100-046"></a>
## N100-046 — Canonical arithmetic-interval message code

**Draft reference:** `C01` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Use a fixed positive distribution w(a)=26-r(a), sum 351, where r is the rank in ETAOINSHRDLCUMWFGYPBVKJXQZ. Starting [L,U)=[0,1), update to the subinterval for each of exactly 97 plaintext letters. Let M=26^97 and N=ceil(M L); encoding exists only when N<M U. Emit Z=base26_97(N). Inverse arithmetic-decodes N/M for 97 steps and accepts only if N is the canonical leftmost integer of the resulting interval.
- **Bounded test:** One frozen distribution, exact rational arithmetic, seven outer phases. On synthetic alphabets 2..4 and lengths 1..8 compare all interval fibers with an independent rational decoder, including endpoints. Only then may a separately admitted full decoder check all 24 English-position constraints and 97-symbol re-encryption.
- **Controls:** 
  - **Positive:** Plants whose intervals contain one or many integer representatives; boundaries exactly on integer-grid points; independent encoder/decoder agreement.
  - **Negative:** Intervals containing no grid point must reject; noncanonical representatives in otherwise valid intervals must reject; whole-pipeline length-matched ciphertext nulls.
- **Identifiability limit:** Arbitrary probability tables can hide the plaintext and are forbidden. A surviving frozen-model decode would not demonstrate historical use; the seven-phase family still needs false-selection calibration.
- **Novelty distinction:** Global nested intervals couple the entire message. This is neither .Z/LZW magic checking nor a local one-/two-plaintext-letter lookup. Changing order or probability smoothing would not count as another mechanism.
- **Closest local external:** H-LANGUAGE / COMPRESS-TRANSPORT-043; EXT-024; H-RADIX-FEEDBACK applies only its fixed affine recurrence, not this interval map.
- **Admission:** Research-only proposal; K4 not run. Mathematical foundations are known prior art, not claimed inventions. Exact public K4 history is unresolved beyond the cited inspected register and finite web search; no worldwide novelty or launch admission is claimed.
- **Priority:** 2
- **Estimated cost:** Research/proof first. Independently written exhaustive tiny oracles, then a frozen finite synthetic protocol; target cost and authorization are separate. Resource-limited or unverified work stays INCOMPLETE.
- **Sources:** 
  - https://doi.org/10.1145/214762.214771
  - https://researchcommons.waikato.ac.nz/bitstreams/46a680e8-47e0-415b-bda2-91a00e2861f1/download
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/EXTERNAL-PRIOR-ART.md
- **Framing and alignment:** The only outer layer is AZ Vigenere with literal key KRYPTOS and one global phase in 0..6: C_i=(Z_i+rank_AZ(KRYPTOS[(i+phase) mod 7])) mod 26. Its key and phase bounds are fixed before target use; no other key, alphabet, layer or rescue is implicit. Public clues constrain decoded English positions 22..34 and 64..74, never positions in an intermediate bit stream.
- **Historical note:** Arithmetic coding predates the sculpture; no creator-use evidence. DOI returned 403 in this pass; author-side later paper describing the 1987 coder was available.
- **Prior art search:** 
  - **Date:** 2026-11-01
  - **Scope:** Read pinned baseline AGENTS.md, relevant H/EXT family records, and experiment headings/scopes. Targeted indexed web/GitHub queries used Kryptos/K4 plus arithmetic coding, Huffman, Tunstall, enumerative coding, Burrows-Wheeler, rotor-router, Pruefer, Foata, RSK, SEQUITUR, Golomb, multiset, functional graph and Fisher-Yates. Primary technical sources were separately sought. No matching exact K4 operator was established; this finite pass is not exhaustive.
  - **Limits:** Detailed linked local protocols were absent from the supplied four-file baseline. Pinned EXT-024 and EXT-034 GitHub page fetches returned cache miss; their exact source scope remains register-level, not freshly source-audited. No K4 calculation, target fitting, code execution of external sources, or external state change occurred.

<a id="n100-047"></a>
## N100-047 — Fixed Huffman-prefix stream, not a file-format compressor

**Draft reference:** `C02` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Construct the binary Huffman tree from weights 26-r(a) in the C01 frequency order; break equal weights by smallest contained AZ letter and put the lesser node left. Concatenate the codewords of exactly 97 letters. Decode the prefix tree and require exactly 97 symbols and no leftover bits.
- **Bounded test:** One specified tree, seven outer phases; no free codebook. Exhaustively check tiny alphabets and prefix-boundary truncations, then establish that the fixed transport has nonempty, useful capacity on blind 97-letter synthetic English before any target proposal.
- **Controls:** 
  - **Positive:** Plants ending at every tree depth, all-equal strings, and codewords crossing base-26 digit boundaries.
  - **Negative:** Truncated paths, appended complete words, and oversize encodings reject; matched full-pipeline random and shuffled controls measure chance clue agreement.
- **Identifiability limit:** Unknown tree shapes/leaf assignments would add a large fitted codebook and are excluded. Failure covers this framed fixed code only.
- **Novelty distinction:** Individual variable-bit prefix codewords with exact framing are not the headered LZW .Z format used in 043, nor EXT-024's reported one-/two-letter code relation. Huffman and arithmetic distributions are shared assumptions, not two renamed versions of the same forward map.
- **Closest local external:** H-LANGUAGE / 043; H-TREE-STATEFUL used carried walk/splay state, not reset-to-root prefix codewords; EXT-024.
- **Admission:** Research-only proposal; K4 not run. Mathematical foundations are known prior art, not claimed inventions. Exact public K4 history is unresolved beyond the cited inspected register and finite web search; no worldwide novelty or launch admission is claimed.
- **Priority:** 3
- **Estimated cost:** Research/proof first. Independently written exhaustive tiny oracles, then a frozen finite synthetic protocol; target cost and authorization are separate. Resource-limited or unverified work stays INCOMPLETE.
- **Sources:** 
  - https://compression.ru/download/articles/huff/huffman_1952_minimum-redundancy-codes.pdf
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/EXTERNAL-PRIOR-ART.md
- **Framing and alignment:** For a finite bit string b, set N=2^len(b)+value_2(b), require N<26^97, and render N as exactly 97 AZ base-26 digits. Decode removes the leading binary 1; require canonical re-encoding and complete bit consumption. Oversize inputs are outside this partial codec, not silently truncated. The only outer layer is AZ Vigenere with literal key KRYPTOS and one global phase in 0..6: C_i=(Z_i+rank_AZ(KRYPTOS[(i+phase) mod 7])) mod 26. Its key and phase bounds are fixed before target use; no other key, alphabet, layer or rescue is implicit.
- **Prior art search:** 
  - **Date:** 2026-11-01
  - **Scope:** Read pinned baseline AGENTS.md, relevant H/EXT family records, and experiment headings/scopes. Targeted indexed web/GitHub queries used Kryptos/K4 plus arithmetic coding, Huffman, Tunstall, enumerative coding, Burrows-Wheeler, rotor-router, Pruefer, Foata, RSK, SEQUITUR, Golomb, multiset, functional graph and Fisher-Yates. Primary technical sources were separately sought. No matching exact K4 operator was established; this finite pass is not exhaustive.
  - **Limits:** Detailed linked local protocols were absent from the supplied four-file baseline. Pinned EXT-024 and EXT-034 GitHub page fetches returned cache miss; their exact source scope remains register-level, not freshly source-audited. No K4 calculation, target fitting, code execution of external sources, or external state change occurred.

<a id="n100-048"></a>
## N100-048 — Tunstall variable-phrase to fixed-word coding

**Draft reference:** `C03` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Grow a 26-ary Tunstall tree from the fixed C01 letter weights, repeatedly expanding the most probable leaf (AZ lexical tie break) until exactly 1001 leaves exist. Lexically number leaves 0..1000 and encode each greedily parsed phrase as 10 bits. Extend the last phrase with only A until a leaf is reached; decode and trim to the known 97-letter source length, then require the removed suffix to be exactly the canonical A completion.
- **Bounded test:** One dictionary-construction rule, one 1001-leaf table, seven outer phases. Test all short strings for tiny complete dictionaries, including every partial-final-phrase state, before a length/capacity gate on fresh 97-letter plants.
- **Controls:** 
  - **Positive:** Plants requiring zero, one and maximum terminal completion symbols; dictionary-leaf coverage; independent trie and table decoders.
  - **Negative:** Unused 10-bit values 1001..1023, non-A terminal completions, wrong final phrase and oversize payloads reject; matched ciphertext nulls use the entire seven-phase selector.
- **Identifiability limit:** Table size and probabilities are frozen, not optimized against clues. The code may be inefficient at length 97; synthetic capacity failure retires the specification before K4.
- **Novelty distinction:** Variable numbers of source letters map to fixed 10-bit words, unlike Huffman's single-letter variable-bit words and EXT-024's bounded local 1-or-2-letter relation. No second candidate is claimed for a different table size.
- **Closest local external:** H-LANGUAGE; H-BOOK-CODEBOOK as nearby dictionary concept, but this table is algorithmically generated, not a sourced edition; EXT-024 unresolved.
- **Admission:** Research-only proposal; K4 not run. Mathematical foundations are known prior art, not claimed inventions. Exact public K4 history is unresolved beyond the cited inspected register and finite web search; no worldwide novelty or launch admission is claimed.
- **Priority:** 3
- **Estimated cost:** Research/proof first. Independently written exhaustive tiny oracles, then a frozen finite synthetic protocol; target cost and authorization are separate. Resource-limited or unverified work stays INCOMPLETE.
- **Sources:** 
  - https://biosig.sourceforge.net/help/freetb4matlab/info-theory/tunstallcode.html
  - https://web.mit.edu/6.441/spring06/handout/sup/Tunstall_codes_-_Notes_1.pdf
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/EXTERNAL-PRIOR-ART.md
- **Framing and alignment:** For a finite bit string b, set N=2^len(b)+value_2(b), require N<26^97, and render N as exactly 97 AZ base-26 digits. Decode removes the leading binary 1; require canonical re-encoding and complete bit consumption. Oversize inputs are outside this partial codec, not silently truncated. The only outer layer is AZ Vigenere with literal key KRYPTOS and one global phase in 0..6: C_i=(Z_i+rank_AZ(KRYPTOS[(i+phase) mod 7])) mod 26. Its key and phase bounds are fixed before target use; no other key, alphabet, layer or rescue is implicit.
- **Historical note:** Tunstall construction is a known 1960s code. Technical implementation/academic notes were available; the original thesis itself was not retrieved.
- **Prior art search:** 
  - **Date:** 2026-11-01
  - **Scope:** Read pinned baseline AGENTS.md, relevant H/EXT family records, and experiment headings/scopes. Targeted indexed web/GitHub queries used Kryptos/K4 plus arithmetic coding, Huffman, Tunstall, enumerative coding, Burrows-Wheeler, rotor-router, Pruefer, Foata, RSK, SEQUITUR, Golomb, multiset, functional graph and Fisher-Yates. Primary technical sources were separately sought. No matching exact K4 operator was established; this finite pass is not exhaustive.
  - **Limits:** Detailed linked local protocols were absent from the supplied four-file baseline. Pinned EXT-024 and EXT-034 GitHub page fetches returned cache miss; their exact source scope remains register-level, not freshly source-audited. No K4 calculation, target fitting, code execution of external sources, or external state change occurred.

<a id="n100-049"></a>
## N100-049 — Greedy LZ77 back-reference transport

**Draft reference:** `C04` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Scan 97 plaintext letters with a 32-symbol sliding history. Greedily take the longest non-overlapping match of length 3..26, nearest-distance tie break; otherwise literal. Literal token is 0 plus 5-bit AZ value; match token is 1 plus 5-bit(distance-1) plus 5-bit(length-3). Decoder copies exactly that earlier interval; reject lengths beyond 26 and decode exactly 97 letters.
- **Bounded test:** One window, one parse rule, seven outer phases. Independent exhaustive tiny encoders must agree on tokenization; blind 97-letter capacity gate comes before target admission.
- **Controls:** 
  - **Positive:** Repeated phrases at window edges; closest-match ties; matches of lengths 3 and 26; suffix ending exactly at symbol 97.
  - **Negative:** Backreferences before history, overlap forbidden by specification, reserved lengths, trailing tokens and oversize payloads reject. Source-disjoint ordinary-text and uniform null cohorts expose overfitting.
- **Identifiability limit:** Changing parser, window or threshold is not another hypothesis. Short messages may not compress enough; no arbitrary seed dictionary is allowed.
- **Novelty distinction:** LZ77 emits explicit backward distances and lengths, whereas the inspected 043 branch transports a headered .Z/LZW dictionary-index file. It is not a cosmetic .Z bit-order/header alteration, but exact K4 LZ77 history remains unverified.
- **Closest local external:** H-LANGUAGE / 043; EXT-024 generic variable-rate scope unresolved.
- **Admission:** Research-only proposal; K4 not run. Mathematical foundations are known prior art, not claimed inventions. Exact public K4 history is unresolved beyond the cited inspected register and finite web search; no worldwide novelty or launch admission is claimed.
- **Priority:** 3
- **Estimated cost:** Research/proof first. Independently written exhaustive tiny oracles, then a frozen finite synthetic protocol; target cost and authorization are separate. Resource-limited or unverified work stays INCOMPLETE.
- **Sources:** 
  - https://pzs.dstu.dp.ua/ComputerGraphics/ic/bibl/ziv_lempel_1977.pdf
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/EXTERNAL-PRIOR-ART.md
- **Framing and alignment:** For a finite bit string b, set N=2^len(b)+value_2(b), require N<26^97, and render N as exactly 97 AZ base-26 digits. Decode removes the leading binary 1; require canonical re-encoding and complete bit consumption. Oversize inputs are outside this partial codec, not silently truncated. The only outer layer is AZ Vigenere with literal key KRYPTOS and one global phase in 0..6: C_i=(Z_i+rank_AZ(KRYPTOS[(i+phase) mod 7])) mod 26. Its key and phase bounds are fixed before target use; no other key, alphabet, layer or rescue is implicit.
- **Prior art search:** 
  - **Date:** 2026-11-01
  - **Scope:** Read pinned baseline AGENTS.md, relevant H/EXT family records, and experiment headings/scopes. Targeted indexed web/GitHub queries used Kryptos/K4 plus arithmetic coding, Huffman, Tunstall, enumerative coding, Burrows-Wheeler, rotor-router, Pruefer, Foata, RSK, SEQUITUR, Golomb, multiset, functional graph and Fisher-Yates. Primary technical sources were separately sought. No matching exact K4 operator was established; this finite pass is not exhaustive.
  - **Limits:** Detailed linked local protocols were absent from the supplied four-file baseline. Pinned EXT-024 and EXT-034 GitHub page fetches returned cache miss; their exact source scope remains register-level, not freshly source-audited. No K4 calculation, target fitting, code execution of external sources, or external state change occurred.

<a id="n100-050"></a>
## N100-050 — Self-generated straight-line grammar code

**Draft reference:** `C05` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Apply deterministic SEQUITUR to the 97-letter input: enforce digram uniqueness and rule utility after each appended letter; freeze tie/repair order from one implementation. Canonically postorder-number the resulting acyclic rules. Serialize rule count, body lengths and terminal/nonterminal IDs with Elias-gamma of each nonnegative integer plus one, followed by the start rule. Expanding the DAG gives the inverse.
- **Bounded test:** One pinned repair order and one explicit serialization; seven outer phases. Freeze the missing implementation/tie details before coding. Tiny all-string grammar reconstruction and fresh 97-letter capacity tests must pass before proposing a target stage.
- **Controls:** 
  - **Positive:** Nested and overlapping repetitions, rules losing their second use, and grammars sharing subrules; independent expansion returns the original string.
  - **Negative:** Cyclic graphs, forward references outside the canonical order, unused rules, noncanonical equivalent grammars and expansion length other than 97 reject. Include repetitive nonlanguage nulls.
- **Identifiability limit:** The grammar must be generated by the fixed algorithm, never invented to fit the ciphertext. Serialization overhead may defeat the 97-letter channel; that is a testable pretarget failure, not permission to strip the header.
- **Novelty distinction:** Hierarchical phrase rules are induced and reused recursively, unlike LZ77 distance copies, LZW sequential phrase indices or a supplied word codebook. This is one grammar mechanism, not separate Re-Pair/SEQUITUR variants.
- **Closest local external:** H-LANGUAGE / 043; H-BOOK-CODEBOOK; EXT-024.
- **Admission:** Specification-blocked proposal: freeze exact SEQUITUR repair and tie order with an independently checkable serializer before synthetic or target execution. No novelty clearance.
- **Priority:** 4
- **Estimated cost:** Research/proof first. Independently written exhaustive tiny oracles, then a frozen finite synthetic protocol; target cost and authorization are separate. Resource-limited or unverified work stays INCOMPLETE.
- **Sources:** 
  - https://arxiv.org/abs/cs/9709102
  - https://researchcommons.waikato.ac.nz/entities/publication/86f76fd2-cf2b-4346-b3ba-0553fa83c941
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/EXTERNAL-PRIOR-ART.md
- **Framing and alignment:** For a finite bit string b, set N=2^len(b)+value_2(b), require N<26^97, and render N as exactly 97 AZ base-26 digits. Decode removes the leading binary 1; require canonical re-encoding and complete bit consumption. Oversize inputs are outside this partial codec, not silently truncated. The only outer layer is AZ Vigenere with literal key KRYPTOS and one global phase in 0..6: C_i=(Z_i+rank_AZ(KRYPTOS[(i+phase) mod 7])) mod 26. Its key and phase bounds are fixed before target use; no other key, alphabet, layer or rescue is implicit.
- **Historical note:** Published in the 1990s; deliberately unconventional mathematics, not evidence of Sanborn use. SEQUITUR homepage fetch failed 502; author paper was retrieved instead.
- **Prior art search:** 
  - **Date:** 2026-11-01
  - **Scope:** Read pinned baseline AGENTS.md, relevant H/EXT family records, and experiment headings/scopes. Targeted indexed web/GitHub queries used Kryptos/K4 plus arithmetic coding, Huffman, Tunstall, enumerative coding, Burrows-Wheeler, rotor-router, Pruefer, Foata, RSK, SEQUITUR, Golomb, multiset, functional graph and Fisher-Yates. Primary technical sources were separately sought. No matching exact K4 operator was established; this finite pass is not exhaustive.
  - **Limits:** Detailed linked local protocols were absent from the supplied four-file baseline. Pinned EXT-024 and EXT-034 GitHub page fetches returned cache miss; their exact source scope remains register-level, not freshly source-audited. No K4 calculation, target fitting, code execution of external sources, or external state change occurred.

<a id="n100-051"></a>
## N100-051 — Asymmetric numeral-state coding

**Draft reference:** `C06` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Let f_s=26-r(s), M=351, and B_s be cumulative frequencies in the fixed frequency order. Starting x=1, push plaintext symbols in reverse order by x <- M floor(x/f_s)+B_s+(x mod f_s). The inverse uses t=x mod M to identify s, then x <- f_s floor(x/M)+(t-B_s). After 97 pops require x=1. Transport final x directly as 97 base-26 digits if x<26^97.
- **Bounded test:** One unnormalized integer ANS map, one state 1, seven outer phases. Exhaustive tiny frequency tables verify pushes/pops and direction; capacity of 97-letter plants is measured before target authority.
- **Controls:** 
  - **Positive:** All residue classes of each symbol, repeated symbols, and endpoint states; independent push/pop implementations.
  - **Negative:** Wrong terminal state, premature exhaustion, wrong push order, noncanonical x and overflow reject. Nulls include numbers in range that decode but fail terminal-state/canonical checks.
- **Identifiability limit:** Free frequency spreads or secret coding tables can encode a large key and are forbidden. Historical plausibility is low; structural mathematical interest is the rationale.
- **Novelty distinction:** A single integer stack with quotient/remainder states is not nested-interval arithmetic coding, a prefix tree or the affine/carry recurrence in H-RADIX-FEEDBACK/H-CARRY-624. Reversing input is necessary stack semantics, not a separate candidate.
- **Closest local external:** H-LANGUAGE / 043; H-RADIX-FEEDBACK; H-CARRY-624; EXT-024/049 nearest but not exact.
- **Admission:** Research-only proposal; K4 not run. Mathematical foundations are known prior art, not claimed inventions. Exact public K4 history is unresolved beyond the cited inspected register and finite web search; no worldwide novelty or launch admission is claimed.
- **Priority:** 4
- **Estimated cost:** Research/proof first. Independently written exhaustive tiny oracles, then a frozen finite synthetic protocol; target cost and authorization are separate. Resource-limited or unverified work stays INCOMPLETE.
- **Sources:** 
  - https://arxiv.org/abs/0902.0271
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/EXTERNAL-PRIOR-ART.md
- **Framing and alignment:** The only outer layer is AZ Vigenere with literal key KRYPTOS and one global phase in 0..6: C_i=(Z_i+rank_AZ(KRYPTOS[(i+phase) mod 7])) mod 26. Its key and phase bounds are fixed before target use; no other key, alphabet, layer or rescue is implicit. Exactly 97 decoded English symbols; no processed-position crib sliding.
- **Historical note:** ANS was introduced after 1990. No historical-use claim.
- **Prior art search:** 
  - **Date:** 2026-11-01
  - **Scope:** Read pinned baseline AGENTS.md, relevant H/EXT family records, and experiment headings/scopes. Targeted indexed web/GitHub queries used Kryptos/K4 plus arithmetic coding, Huffman, Tunstall, enumerative coding, Burrows-Wheeler, rotor-router, Pruefer, Foata, RSK, SEQUITUR, Golomb, multiset, functional graph and Fisher-Yates. Primary technical sources were separately sought. No matching exact K4 operator was established; this finite pass is not exhaustive.
  - **Limits:** Detailed linked local protocols were absent from the supplied four-file baseline. Pinned EXT-024 and EXT-034 GitHub page fetches returned cache miss; their exact source scope remains register-level, not freshly source-audited. No K4 calculation, target fitting, code execution of external sources, or external state change occurred.

<a id="n100-052"></a>
## N100-052 — Inverted occurrence-gap code

**Draft reference:** `C07` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Write counts of A..Y as gamma(n_a+1); infer n_Z from total 97. For each letter A..Y, let U be the ordered currently unassigned positions and encode that letter's successive zero-based gaps in U with Golomb parameter m=max(1,floor(|U|/n_a)); encode nothing when n_a=0. Remove assigned positions after the letter. Z fills the remainder. This gives an exact inverse, including the position map.
- **Bounded test:** One AZ ordering and one parameter rule; seven outer phases. Exhaust all strings over alphabets 2..4 up to length 8, and test capacity on fresh 97-letter plants before any target proposal.
- **Controls:** 
  - **Positive:** Zero-count letters, occurrences at first/last available position, clustered and evenly spaced occurrences; independent direct-set and gap decoders.
  - **Negative:** Counts exceeding 97, gaps outside remaining slots, repeated assignments, unused suffix bits and overflow reject. Use shuffled strings sharing a histogram to distinguish mere count evidence.
- **Identifiability limit:** The counts are encoded, not inferred from desired English. If metadata overhead prevents useful capacity, retire this exact specification; do not silently choose a fitted letter order.
- **Novelty distinction:** Encodes the positions of occurrences after successively removing earlier letter classes. It is neither a letter substitution nor a key-clock based on last occurrence; no extra candidate is counted for Rice instead of Golomb.
- **Closest local external:** H-LANGUAGE / 043; H-RECURRENCE-CLOCK selects an immutable key entry rather than transmitting occurrence positions; EXT-024/030.
- **Admission:** Research-only proposal; K4 not run. Mathematical foundations are known prior art, not claimed inventions. Exact public K4 history is unresolved beyond the cited inspected register and finite web search; no worldwide novelty or launch admission is claimed.
- **Priority:** 4
- **Estimated cost:** Research/proof first. Independently written exhaustive tiny oracles, then a frozen finite synthetic protocol; target cost and authorization are separate. Resource-limited or unverified work stays INCOMPLETE.
- **Sources:** 
  - https://compression.ru/download/articles/low_entropy/golomb_1966_run-length-encodings.pdf
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/EXTERNAL-PRIOR-ART.md
- **Framing and alignment:** For a finite bit string b, set N=2^len(b)+value_2(b), require N<26^97, and render N as exactly 97 AZ base-26 digits. Decode removes the leading binary 1; require canonical re-encoding and complete bit consumption. Oversize inputs are outside this partial codec, not silently truncated. The only outer layer is AZ Vigenere with literal key KRYPTOS and one global phase in 0..6: C_i=(Z_i+rank_AZ(KRYPTOS[(i+phase) mod 7])) mod 26. Its key and phase bounds are fixed before target use; no other key, alphabet, layer or rescue is implicit.
- **Prior art search:** 
  - **Date:** 2026-11-01
  - **Scope:** Read pinned baseline AGENTS.md, relevant H/EXT family records, and experiment headings/scopes. Targeted indexed web/GitHub queries used Kryptos/K4 plus arithmetic coding, Huffman, Tunstall, enumerative coding, Burrows-Wheeler, rotor-router, Pruefer, Foata, RSK, SEQUITUR, Golomb, multiset, functional graph and Fisher-Yates. Primary technical sources were separately sought. No matching exact K4 operator was established; this finite pass is not exhaustive.
  - **Limits:** Detailed linked local protocols were absent from the supplied four-file baseline. Pinned EXT-024 and EXT-034 GitHub page fetches returned cache miss; their exact source scope remains register-level, not freshly source-audited. No K4 calculation, target fitting, code execution of external sources, or external state change occurred.

<a id="n100-053"></a>
## N100-053 — Finite-state language-path rank code

**Draft reference:** `C08` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Fix a six-state automaton tracking the current consonant run, with vowels AEIOU resetting to 0 and a sixth consecutive consonant forbidden. Let F(q,l) count accepted l-symbol completions by F(q,l)=sum_a F(delta(q,a),l-1). Lexically rank each accepted 97-letter word by summing lower-symbol completion counts; emit the rank as 97 base-26 digits. Inverse subtracts the same completion intervals.
- **Bounded test:** Exactly this automaton, AZ order, length 97 and seven outer phases. Tiny exhaustive accepted-language rank/unrank checks precede held-out ordinary-text false-rejection and capacity measurements; no automaton learning on K4.
- **Controls:** 
  - **Positive:** Words reaching every state and the maximal allowed five-consonant run; ranks 0 and |S|-1; independent DP and enumeration.
  - **Negative:** Rank >=|S|, any sixth consonant, and noncanonical length reject; controls include legitimate English outside this arbitrary source restriction, to expose false exclusions.
- **Identifiability limit:** This is a conditional source-code hypothesis, not a claim that all English obeys the automaton. An arbitrary learned DFA could memorize a plaintext and is prohibited.
- **Novelty distinction:** Counts and indexes whole accepted graph paths, rather than assigning fixed word tokens or arithmetic probabilities. The finite-state path restriction is part of the cipher, not post-hoc language scoring.
- **Closest local external:** H-LANGUAGE; H-WORD-COVER-EXTRACTION used lexical cover paths/extraction, not a forward rank code; H-BOOK-CODEBOOK; EXT-024.
- **Admission:** Research-only proposal; K4 not run. Mathematical foundations are known prior art, not claimed inventions. Exact public K4 history is unresolved beyond the cited inspected register and finite web search; no worldwide novelty or launch admission is claimed.
- **Priority:** 3
- **Estimated cost:** Research/proof first. Independently written exhaustive tiny oracles, then a frozen finite synthetic protocol; target cost and authorization are separate. Resource-limited or unverified work stays INCOMPLETE.
- **Sources:** 
  - https://algo.inria.fr/flajolet/Publications/book.pdf
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/EXTERNAL-PRIOR-ART.md
- **Framing and alignment:** The only outer layer is AZ Vigenere with literal key KRYPTOS and one global phase in 0..6: C_i=(Z_i+rank_AZ(KRYPTOS[(i+phase) mod 7])) mod 26. Its key and phase bounds are fixed before target use; no other key, alphabet, layer or rescue is implicit. The decoded path has exactly 97 English letters; the public positions are checked only there.
- **Prior art search:** 
  - **Date:** 2026-11-01
  - **Scope:** Read pinned baseline AGENTS.md, relevant H/EXT family records, and experiment headings/scopes. Targeted indexed web/GitHub queries used Kryptos/K4 plus arithmetic coding, Huffman, Tunstall, enumerative coding, Burrows-Wheeler, rotor-router, Pruefer, Foata, RSK, SEQUITUR, Golomb, multiset, functional graph and Fisher-Yates. Primary technical sources were separately sought. No matching exact K4 operator was established; this finite pass is not exhaustive.
  - **Limits:** Detailed linked local protocols were absent from the supplied four-file baseline. Pinned EXT-024 and EXT-034 GitHub page fetches returned cache miss; their exact source scope remains register-level, not freshly source-audited. No K4 calculation, target fitting, code execution of external sources, or external state change occurred.

<a id="n100-054"></a>
## N100-054 — Multiset-rank affine transposition

**Draft reference:** `C09` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** For the complete plaintext multiset h, M=97!/product_a h_a!. Lexically rank P within that multiset as r. Let a be the least odd integer >=3 coprime to M and set r'=(a r+1) mod M. Unrank r' with the same h to produce Z. Inverse reads h from Z and uses a^-1 mod M. M=1 is the explicitly fixed identity case.
- **Bounded test:** One rank automorphism and seven nonzero outer phases; no free histogram or rank key. Exhaust all tiny multisets and compare with all fixed position permutations on alphabets 2..4 to establish non-aliasing.
- **Controls:** 
  - **Positive:** Constant, heavily repeated and all-distinct plants; ranks crossing 0 and M-1; complete tiny inverse fibers.
  - **Negative:** Whole-family nulls preserve ciphertext histogram after removing the outer layer; identity/pure-transposition lane is excluded by H-PERM and is not a new target test.
- **Identifiability limit:** A free rank offset in 0..M-1 would fit any arrangement and is forbidden. Only the fixed arithmetic rule is proposed.
- **Novelty distinction:** The output route depends on the whole multiset rank, not a sum-controlled rotation or a position-only route. Prove a synthetic pair has different induced routes before admission. This is a new composite specification, not a claim that pure transposition survives.
- **Closest local external:** H-PERM excludes the unwrapped map; H-ROUTE; H-SUM-ROTATION; EXT-002/004/012.
- **Admission:** Research-only proposal; K4 not run. Mathematical foundations are known prior art, not claimed inventions. Exact public K4 history is unresolved beyond the cited inspected register and finite web search; no worldwide novelty or launch admission is claimed.
- **Priority:** 3
- **Estimated cost:** Research/proof first. Independently written exhaustive tiny oracles, then a frozen finite synthetic protocol; target cost and authorization are separate. Resource-limited or unverified work stays INCOMPLETE.
- **Sources:** 
  - https://isl.stanford.edu/~cover/papers/transIT/0073cove.pdf
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/EXTERNAL-PRIOR-ART.md
- **Framing and alignment:** The only outer layer is AZ Vigenere with literal key KRYPTOS and one global phase in 0..6: C_i=(Z_i+rank_AZ(KRYPTOS[(i+phase) mod 7])) mod 26. Its key and phase bounds are fixed before target use; no other key, alphabet, layer or rescue is implicit.
- **Prior art search:** 
  - **Date:** 2026-11-01
  - **Scope:** Read pinned baseline AGENTS.md, relevant H/EXT family records, and experiment headings/scopes. Targeted indexed web/GitHub queries used Kryptos/K4 plus arithmetic coding, Huffman, Tunstall, enumerative coding, Burrows-Wheeler, rotor-router, Pruefer, Foata, RSK, SEQUITUR, Golomb, multiset, functional graph and Fisher-Yates. Primary technical sources were separately sought. No matching exact K4 operator was established; this finite pass is not exhaustive.
  - **Limits:** Detailed linked local protocols were absent from the supplied four-file baseline. Pinned EXT-024 and EXT-034 GitHub page fetches returned cache miss; their exact source scope remains register-level, not freshly source-audited. No K4 calculation, target fitting, code execution of external sources, or external state change occurred.

<a id="n100-055"></a>
## N100-055 — Bijective suffix-sorting transform with no lost primary index

**Draft reference:** `C10` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Apply the Gil-Scott bijective Burrows-Wheeler transform: unique nonincreasing Lyndon factorization; sort all factor rotations by their infinite periodic comparison; output predecessor characters. The LF-cycle inverse recovers each Lyndon factor and restores canonical factor order. No original-row index or delimiter is discarded.
- **Bounded test:** One specified BBWT and seven outer phases, no MTF stage. Independent transform/inverse and exhaustive small-alphabet strings up to length 8 establish bijection and repeated-factor handling.
- **Controls:** 
  - **Positive:** Periodic words, repeated Lyndon factors, single-letter factors and all-equal words; independent LF inverse.
  - **Negative:** Ordinary BWT without its row index is a deliberately failing control, not an accepted substitute. Whole-pipeline nulls preserve multiset; zero outer layer is analytically excluded.
- **Identifiability limit:** The transform is known and modern, and preserves counts before the fixed outer layer. A match would support only this composite; no free sort order or missing index is allowed.
- **Novelty distinction:** Suffix-order depends on message content; this is not fixed columnar routing, move-to-front, or merely a new BWT alphabet ordering. There is exactly one BBWT mechanism here.
- **Closest local external:** H-PERM; H-ROUTE; H-EVOLVING-ALPHABET/EXT-034 MTF differs; EXT-002/004.
- **Admission:** Research-only proposal; K4 not run. Mathematical foundations are known prior art, not claimed inventions. Exact public K4 history is unresolved beyond the cited inspected register and finite web search; no worldwide novelty or launch admission is claimed.
- **Priority:** 3
- **Estimated cost:** Research/proof first. Independently written exhaustive tiny oracles, then a frozen finite synthetic protocol; target cost and authorization are separate. Resource-limited or unverified work stays INCOMPLETE.
- **Sources:** 
  - https://arxiv.org/abs/1201.3077
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/EXTERNAL-PRIOR-ART.md
- **Framing and alignment:** The only outer layer is AZ Vigenere with literal key KRYPTOS and one global phase in 0..6: C_i=(Z_i+rank_AZ(KRYPTOS[(i+phase) mod 7])) mod 26. Its key and phase bounds are fixed before target use; no other key, alphabet, layer or rescue is implicit.
- **Historical note:** Bijective form dates after 1990; speculative mathematical candidate, no creator attribution.
- **Prior art search:** 
  - **Date:** 2026-11-01
  - **Scope:** Read pinned baseline AGENTS.md, relevant H/EXT family records, and experiment headings/scopes. Targeted indexed web/GitHub queries used Kryptos/K4 plus arithmetic coding, Huffman, Tunstall, enumerative coding, Burrows-Wheeler, rotor-router, Pruefer, Foata, RSK, SEQUITUR, Golomb, multiset, functional graph and Fisher-Yates. Primary technical sources were separately sought. No matching exact K4 operator was established; this finite pass is not exhaustive.
  - **Limits:** Detailed linked local protocols were absent from the supplied four-file baseline. Pinned EXT-024 and EXT-034 GitHub page fetches returned cache miss; their exact source scope remains register-level, not freshly source-audited. No K4 calculation, target fitting, code execution of external sources, or external state change occurred.

<a id="n100-056"></a>
## N100-056 — Foata word rearrangement composite

**Draft reference:** `C11` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Use Foata's second fundamental transformation Phi(wx)=gamma_x(Phi(w)) x. If the last letter of v=Phi(w) is <=x, uniquely factor v=v1 b1...vk bk with each b_j<=x and letters of v_j>x; if last(v)>x reverse the inequalities. Set gamma_x(v)=b1 v1...bk vk. Inverse removes x, reverses the factor rotations, and recurses.
- **Bounded test:** One AZ comparison convention, one transformation, seven outer phases. Exhaust tiny words including equality cases; prove inverse and compare against fixed reversals, sum-rotation and fixed-route libraries.
- **Controls:** 
  - **Positive:** Repeated pivot-equal letters, both inequality branches, empty factors and long factors; independent iterative and recursive inverses.
  - **Negative:** Mutated equality convention must fail controls. Whole-family multiset-matched nulls; pure Phi with no outer layer is already excluded by H-PERM.
- **Identifiability limit:** A target-dependent comparison order would be an extra fitted alphabet and is prohibited. A named classical bijection is not evidence of K4 use.
- **Novelty distinction:** Variable factor boundaries depend recursively on the newest value and previously transformed word, unlike fixed-width sum rotation or splay access. This is one Foata bijection, not multiple comparison-order variants.
- **Closest local external:** H-PERM; H-SUM-ROTATION; H-TREE-STATEFUL; H-ROUTE; EXT-002/034.
- **Admission:** Research-only proposal; K4 not run. Mathematical foundations are known prior art, not claimed inventions. Exact public K4 history is unresolved beyond the cited inspected register and finite web search; no worldwide novelty or launch admission is claimed.
- **Priority:** 2
- **Estimated cost:** Research/proof first. Independently written exhaustive tiny oracles, then a frozen finite synthetic protocol; target cost and authorization are separate. Resource-limited or unverified work stays INCOMPLETE.
- **Sources:** 
  - https://irma.math.unistra.fr/~foata/paper/pub43.pdf
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/EXTERNAL-PRIOR-ART.md
- **Framing and alignment:** The only outer layer is AZ Vigenere with literal key KRYPTOS and one global phase in 0..6: C_i=(Z_i+rank_AZ(KRYPTOS[(i+phase) mod 7])) mod 26. Its key and phase bounds are fixed before target use; no other key, alphabet, layer or rescue is implicit.
- **Historical note:** Known combinatorial transformation predating 1990; exact K4 application not found in this bounded search.
- **Prior art search:** 
  - **Date:** 2026-11-01
  - **Scope:** Read pinned baseline AGENTS.md, relevant H/EXT family records, and experiment headings/scopes. Targeted indexed web/GitHub queries used Kryptos/K4 plus arithmetic coding, Huffman, Tunstall, enumerative coding, Burrows-Wheeler, rotor-router, Pruefer, Foata, RSK, SEQUITUR, Golomb, multiset, functional graph and Fisher-Yates. Primary technical sources were separately sought. No matching exact K4 operator was established; this finite pass is not exhaustive.
  - **Limits:** Detailed linked local protocols were absent from the supplied four-file baseline. Pinned EXT-024 and EXT-034 GitHub page fetches returned cache miss; their exact source scope remains register-level, not freshly source-audited. No K4 calculation, target fitting, code execution of external sources, or external state change occurred.

<a id="n100-057"></a>
## N100-057 — RSK recording-tableau evacuation

**Draft reference:** `C12` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Apply ordinary row-insertion RSK to word P, obtaining semistandard insertion tableau I and standard recording tableau Q of the same shape. Replace only Q by its Schuetzenberger evacuation ev(Q), keep I unchanged, and inverse-RSK the pair to Z. Since ev^2=id, the word map is involutive.
- **Bounded test:** One row-insertion/equality convention, one evacuation, seven outer phases. Tiny exhaustive words test shape, duplicates and involution; independent jeu-de-taquin and tableau-operator evacuation must agree.
- **Controls:** 
  - **Positive:** Single-row, single-column and mixed shapes; repeated symbols and equal row values; compare independent inverse-RSK implementations.
  - **Negative:** Evacuating both tableaux is an alias/control for known reversal-complement identities, not another hypothesis. Wrong-shape pairs reject. Histogram-matched full-pipeline nulls calibrate selection.
- **Identifiability limit:** This is a restrictive deterministic word bijection; no choice of tableau shape or per-message tableau permutation is fitted.
- **Novelty distinction:** Only the recording object changes. Message-dependent insertion structure determines letter routing, unlike fixed transpositions, alphabet splay trees or the both-tableau reversal identity.
- **Closest local external:** H-PERM excludes unwrapped counts; H-TREE-STATEFUL had letter-state trees rather than RSK pairs; H-ROUTE; EXT-002/034.
- **Admission:** Research-only proposal; K4 not run. Mathematical foundations are known prior art, not claimed inventions. Exact public K4 history is unresolved beyond the cited inspected register and finite web search; no worldwide novelty or launch admission is claimed.
- **Priority:** 2
- **Estimated cost:** Research/proof first. Independently written exhaustive tiny oracles, then a frozen finite synthetic protocol; target cost and authorization are separate. Resource-limited or unverified work stays INCOMPLETE.
- **Sources:** 
  - https://www.findstat.org/MapsDatabase/Mp00126/
  - https://arxiv.org/abs/1609.02046
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/EXTERNAL-PRIOR-ART.md
- **Framing and alignment:** The only outer layer is AZ Vigenere with literal key KRYPTOS and one global phase in 0..6: C_i=(Z_i+rank_AZ(KRYPTOS[(i+phase) mod 7])) mod 26. Its key and phase bounds are fixed before target use; no other key, alphabet, layer or rescue is implicit.
- **Prior art search:** 
  - **Date:** 2026-11-01
  - **Scope:** Read pinned baseline AGENTS.md, relevant H/EXT family records, and experiment headings/scopes. Targeted indexed web/GitHub queries used Kryptos/K4 plus arithmetic coding, Huffman, Tunstall, enumerative coding, Burrows-Wheeler, rotor-router, Pruefer, Foata, RSK, SEQUITUR, Golomb, multiset, functional graph and Fisher-Yates. Primary technical sources were separately sought. No matching exact K4 operator was established; this finite pass is not exhaustive.
  - **Limits:** Detailed linked local protocols were absent from the supplied four-file baseline. Pinned EXT-024 and EXT-034 GitHub page fetches returned cache miss; their exact source scope remains register-level, not freshly source-audited. No K4 calculation, target fitting, code execution of external sources, or external state change occurred.

<a id="n100-058"></a>
## N100-058 — Pruefer tree relabel conjugation

**Draft reference:** `C13` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Partition the first 96 letters into four 24-letter words, each a Pruefer code on vertices 0..25. Decode to a labelled tree, relabel vertices by the fixed permutation mapping AZ in order to KRYPTOSABCDEFGHIJLMNQUVWXZ, and recode using smallest-leaf Pruefer deletion. Leave the 97th intermediate symbol unchanged. Inverse uses the inverse vertex relabeling.
- **Bounded test:** One 24-letter block origin, one fixed relabeling, seven outer phases. Exhaust all labelled trees for vertex counts 3..6 and compare with simple symbol substitution to establish order-dependent routing.
- **Controls:** 
  - **Positive:** Stars, paths, asymmetric trees, repeated Pruefer values and the unchanged final slot; exact tree/code inverse checks.
  - **Negative:** Identity vertex relabeling is an old identity-layer control; malformed/out-of-range vertex labels reject. Nulls match degree-count profiles where feasible.
- **Identifiability limit:** An arbitrary 26-vertex relabeling would be a large free key and is not proposed. The final singleton is specified, not dropped or padded.
- **Novelty distinction:** Relabeling changes which leaf is smallest at each deletion, so it is generally not simply applying the permutation to every code letter. H-TREE-STATEFUL walks a persistent tree; this encodes the message itself as a tree.
- **Closest local external:** H-TREE-STATEFUL; H-NONLINEAR-BLOCK; H-ROUTE; EXT-034 tree/device scope unresolved.
- **Admission:** Research-only proposal; K4 not run. Mathematical foundations are known prior art, not claimed inventions. Exact public K4 history is unresolved beyond the cited inspected register and finite web search; no worldwide novelty or launch admission is claimed.
- **Priority:** 2
- **Estimated cost:** Research/proof first. Independently written exhaustive tiny oracles, then a frozen finite synthetic protocol; target cost and authorization are separate. Resource-limited or unverified work stays INCOMPLETE.
- **Sources:** 
  - https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.tree.coding.to_prufer_sequence.html
  - https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.tree.coding.from_prufer_sequence.html
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/EXTERNAL-PRIOR-ART.md
- **Framing and alignment:** The only outer layer is AZ Vigenere with literal key KRYPTOS and one global phase in 0..6: C_i=(Z_i+rank_AZ(KRYPTOS[(i+phase) mod 7])) mod 26. Its key and phase bounds are fixed before target use; no other key, alphabet, layer or rescue is implicit.
- **Prior art search:** 
  - **Date:** 2026-11-01
  - **Scope:** Read pinned baseline AGENTS.md, relevant H/EXT family records, and experiment headings/scopes. Targeted indexed web/GitHub queries used Kryptos/K4 plus arithmetic coding, Huffman, Tunstall, enumerative coding, Burrows-Wheeler, rotor-router, Pruefer, Foata, RSK, SEQUITUR, Golomb, multiset, functional graph and Fisher-Yates. Primary technical sources were separately sought. No matching exact K4 operator was established; this finite pass is not exhaustive.
  - **Limits:** Detailed linked local protocols were absent from the supplied four-file baseline. Pinned EXT-024 and EXT-034 GitHub page fetches returned cache miss; their exact source scope remains register-level, not freshly source-audited. No K4 calculation, target fitting, code execution of external sources, or external state change occurred.

<a id="n100-059"></a>
## N100-059 — Ciphertext-driven spatial rotor-router emission

**Draft reference:** `C14` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Use the directed circulant graph on positions Z_97 with ordered neighbors v+1,v+10,v-1,v-10. Rotors start at 0 and cursor at 0. At each step emit/encrypt P at the current unvisited vertex and mark it visited; add the emitted ciphertext rank modulo 4 to that vertex's rotor. For the next slot repeatedly advance the current rotor by one and follow it until an unvisited vertex is reached. Decoder simulates the same history and writes the recovered letter into that slot.
- **Bounded test:** One graph, start, rotor order and initial field; seven key phases, emission-indexed. Tiny connected graphs must prove termination and cover each slot once; independent replay certifies every route before target eligibility.
- **Controls:** 
  - **Positive:** Plants causing repeated visits to already occupied vertices, all four rotor residues, and all-equal ciphertext traces; compare emitted and reconstructed slot lists.
  - **Negative:** Disconnected graphs and nonterminating defective updates must be rejected by preflight, not silently restarted. Whole-pipeline random and histogram-matched nulls.
- **Identifiability limit:** Free initial rotor states at 97 vertices would be an enormous key and are forbidden. The modular graph is a mathematical construction, not measured sculpture geometry.
- **Novelty distinction:** Persistent local rotor fields and walks through occupied vertices are not Josephus' cyclic survivor deletion, a new skip equation, or a fixed route. Need a small full-operator separating witness.
- **Closest local external:** H-CIPHERTEXT-JOSEPHUS; H-OCCUPIED-CELL-FIXED; H-ROUTE; EXT-002/008/030.
- **Admission:** Research-only proposal; K4 not run. Mathematical foundations are known prior art, not claimed inventions. Exact public K4 history is unresolved beyond the cited inspected register and finite web search; no worldwide novelty or launch admission is claimed.
- **Priority:** 3
- **Estimated cost:** Research/proof first. Independently written exhaustive tiny oracles, then a frozen finite synthetic protocol; target cost and authorization are separate. Resource-limited or unverified work stays INCOMPLETE.
- **Sources:** 
  - https://arxiv.org/abs/0801.3306
  - https://lionellevine.github.io/circZd.pdf
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/EXTERNAL-PRIOR-ART.md
- **Framing and alignment:** The only outer layer is AZ Vigenere with literal key KRYPTOS and one global phase in 0..6: C_i=(Z_i+rank_AZ(KRYPTOS[(i+phase) mod 7])) mod 26. Its key and phase bounds are fixed before target use; no other key, alphabet, layer or rescue is implicit. Here i indexes emissions, while clues constrain the reconstructed source slots. The rotor update uses actual emitted C_i, not Z_i.
- **Prior art search:** 
  - **Date:** 2026-11-01
  - **Scope:** Read pinned baseline AGENTS.md, relevant H/EXT family records, and experiment headings/scopes. Targeted indexed web/GitHub queries used Kryptos/K4 plus arithmetic coding, Huffman, Tunstall, enumerative coding, Burrows-Wheeler, rotor-router, Pruefer, Foata, RSK, SEQUITUR, Golomb, multiset, functional graph and Fisher-Yates. Primary technical sources were separately sought. No matching exact K4 operator was established; this finite pass is not exhaustive.
  - **Limits:** Detailed linked local protocols were absent from the supplied four-file baseline. Pinned EXT-024 and EXT-034 GitHub page fetches returned cache miss; their exact source scope remains register-level, not freshly source-audited. No K4 calculation, target fitting, code execution of external sources, or external state change occurred.

<a id="n100-060"></a>
## N100-060 — Ciphertext-weighted shortest-frontier routing

**Draft reference:** `C15` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** On the same fixed four-neighbor Z_97 graph, initialize d(0)=0 and other tentative distances infinity. Pop the unvisited vertex with least (distance,vertex label), emit its plaintext letter through the fixed outer key, and for each unvisited neighbor relax d(u) <- min(d(u), d(v)+1+rank_AZ(C_i)). Each vertex is settled once. Decoder uses ciphertext to reconstruct the exact sequence of relaxations and source slots.
- **Bounded test:** One graph, start, tie order and positive edge-cost rule; seven emission-key phases. Exhaust small graphs and all short emission traces, including ties, then independently audit complete source-slot coverage.
- **Controls:** 
  - **Positive:** Paths with competing frontier entries, equal-distance ties and both accepted/rejected relaxations; independent priority-queue and scan implementations.
  - **Negative:** Negative-cost or revised-settled-distance mutant algorithms must fail tests. Whole-pipeline nulls and constant-cost controls distinguish true data dependence from a fixed route.
- **Identifiability limit:** Per-edge fitted weights, alternative graphs and new tie orders are excluded. Ciphertext determines route for each model; a unique route alone is not plaintext identification.
- **Novelty distinction:** A priority frontier with competing accumulated costs changes global exploration order; Josephus removes ring slots and has no distance-relaxation state. It is not just another direction/period schedule.
- **Closest local external:** H-CIPHERTEXT-JOSEPHUS; H-ROUTE; H-OCCUPIED-CELL-FIXED; EXT-002/008.
- **Admission:** Research-only proposal; K4 not run. Mathematical foundations are known prior art, not claimed inventions. Exact public K4 history is unresolved beyond the cited inspected register and finite web search; no worldwide novelty or launch admission is claimed.
- **Priority:** 3
- **Estimated cost:** Research/proof first. Independently written exhaustive tiny oracles, then a frozen finite synthetic protocol; target cost and authorization are separate. Resource-limited or unverified work stays INCOMPLETE.
- **Sources:** 
  - https://doi.org/10.1007/BF01386390
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/EXTERNAL-PRIOR-ART.md
- **Framing and alignment:** The only outer layer is AZ Vigenere with literal key KRYPTOS and one global phase in 0..6: C_i=(Z_i+rank_AZ(KRYPTOS[(i+phase) mod 7])) mod 26. Its key and phase bounds are fixed before target use; no other key, alphabet, layer or rescue is implicit. Key phase is by emission, clues by reconstructed input position. Dijkstra is the foundation; the ciphertext-cost cipher is speculative, not attributed to that paper.
- **Prior art search:** 
  - **Date:** 2026-11-01
  - **Scope:** Read pinned baseline AGENTS.md, relevant H/EXT family records, and experiment headings/scopes. Targeted indexed web/GitHub queries used Kryptos/K4 plus arithmetic coding, Huffman, Tunstall, enumerative coding, Burrows-Wheeler, rotor-router, Pruefer, Foata, RSK, SEQUITUR, Golomb, multiset, functional graph and Fisher-Yates. Primary technical sources were separately sought. No matching exact K4 operator was established; this finite pass is not exhaustive.
  - **Limits:** Detailed linked local protocols were absent from the supplied four-file baseline. Pinned EXT-024 and EXT-034 GitHub page fetches returned cache miss; their exact source scope remains register-level, not freshly source-audited. No K4 calculation, target fitting, code execution of external sources, or external state change occurred.

<a id="n100-061"></a>
## N100-061 — Swap-delete reservoir routing

**Draft reference:** `C16` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Initialize slot list L=[0,...,96] and h=0. At emission i choose j=h mod |L|, swap L[j] with L[-1], pop that last slot, and emit its plaintext through the fixed outer key. Set h=rank_AZ(C_i)+1. The decoder runs the same swaps/pops from the known ciphertext and writes each recovered letter to its popped slot.
- **Bounded test:** One swap-delete rule, one seed, seven emission-key phases. Exhaust small lists/traces and compare complete operators with order-preserving Josephus removal; retain a distinguishing trace before admission.
- **Controls:** 
  - **Positive:** First/last chosen index, repeated index residues, final singleton, and cases where swap-removal differs on the next selection from stable deletion.
  - **Negative:** A stable-delete mutant must disagree on designated controls. Whole-pipeline nulls and duplicate-slot integrity checks; all-zero pure-route branch is not tested anew.
- **Identifiability limit:** Changing h update or initial list is not another candidate. The fixed rule has no arbitrary 97-position key; accepting a target-determined route is not proof of the rule.
- **Novelty distinction:** Physical rearrangement of the remaining reservoir changes subsequent slot identities; in 062 the remaining circle retains survivor order. This difference must be established as an operator, not by a new parameter label.
- **Closest local external:** H-CIPHERTEXT-JOSEPHUS / 062; H-ROUTE; EXT-002/030.
- **Admission:** Research-only proposal; K4 not run. Mathematical foundations are known prior art, not claimed inventions. Exact public K4 history is unresolved beyond the cited inspected register and finite web search; no worldwide novelty or launch admission is claimed.
- **Priority:** 3
- **Estimated cost:** Research/proof first. Independently written exhaustive tiny oracles, then a frozen finite synthetic protocol; target cost and authorization are separate. Resource-limited or unverified work stays INCOMPLETE.
- **Sources:** 
  - https://github.com/python/cpython/blob/v3.13.0/Lib/random.py
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/EXTERNAL-PRIOR-ART.md
- **Framing and alignment:** The only outer layer is AZ Vigenere with literal key KRYPTOS and one global phase in 0..6: C_i=(Z_i+rank_AZ(KRYPTOS[(i+phase) mod 7])) mod 26. Its key and phase bounds are fixed before target use; no other key, alphabet, layer or rescue is implicit. Key is emission-indexed; actual ciphertext rank determines the next swap. Fisher-Yates-style swap/delete is the implementation foundation, not a claim of identical historical cipher.
- **Prior art search:** 
  - **Date:** 2026-11-01
  - **Scope:** Read pinned baseline AGENTS.md, relevant H/EXT family records, and experiment headings/scopes. Targeted indexed web/GitHub queries used Kryptos/K4 plus arithmetic coding, Huffman, Tunstall, enumerative coding, Burrows-Wheeler, rotor-router, Pruefer, Foata, RSK, SEQUITUR, Golomb, multiset, functional graph and Fisher-Yates. Primary technical sources were separately sought. No matching exact K4 operator was established; this finite pass is not exhaustive.
  - **Limits:** Detailed linked local protocols were absent from the supplied four-file baseline. Pinned EXT-024 and EXT-034 GitHub page fetches returned cache miss; their exact source scope remains register-level, not freshly source-audited. No K4 calculation, target fitting, code execution of external sources, or external state change occurred.

<a id="n100-062"></a>
## N100-062 — Functional-digraph cycle reversal

**Draft reference:** `C17` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Process blocks of at most 26 letters. In a block of length b, define a function f on vertices 0..25 by f(i)=AZ rank of the ith letter for i<b and f(i)=i for i>=b. Reverse every directed cycle of length >=3, leaving all in-tree edges unchanged, to obtain g. Emit g(0)..g(b-1). Padded vertices are fixed self-loops and remain fixed, so the ragged block loses no information. Reversing cycles again is the inverse.
- **Bounded test:** One graph operation, blocks 26/26/26/19, seven outer phases. Exhaust all functions on 2..5 vertices and all ragged fixed-tail subspaces; prove the subspace is closed under reversal.
- **Controls:** 
  - **Positive:** Self-loops, 2-cycles, long cycles, trees feeding cycles, and inputs pointing into fixed-tail vertices; involution and fixed-tail closure.
  - **Negative:** Reversing noncycle edges deliberately breaks the control inverse. Histogram-matched nulls; no-layer branch remains excluded by H-PERM.
- **Identifiability limit:** No arbitrary graph, vertex permutation or per-component choice is allowed. Many inputs with only 1/2-cycles are fixed points; record that weak effective coverage rather than count descriptions.
- **Novelty distinction:** The message is a functional graph and only cyclic edges reverse. This is not a fixed message reversal, alphabet MTF, Pruefer tree relabeling, or dynamic routing through a preexisting graph.
- **Closest local external:** H-PERM; H-NONLINEAR-BLOCK; H-TREE-STATEFUL; EXT-012/034.
- **Admission:** Research-only proposal; K4 not run. Mathematical foundations are known prior art, not claimed inventions. Exact public K4 history is unresolved beyond the cited inspected register and finite web search; no worldwide novelty or launch admission is claimed.
- **Priority:** 3
- **Estimated cost:** Research/proof first. Independently written exhaustive tiny oracles, then a frozen finite synthetic protocol; target cost and authorization are separate. Resource-limited or unverified work stays INCOMPLETE.
- **Sources:** 
  - https://algo.inria.fr/flajolet/Publications/book.pdf
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/EXTERNAL-PRIOR-ART.md
- **Framing and alignment:** The only outer layer is AZ Vigenere with literal key KRYPTOS and one global phase in 0..6: C_i=(Z_i+rank_AZ(KRYPTOS[(i+phase) mod 7])) mod 26. Its key and phase bounds are fixed before target use; no other key, alphabet, layer or rescue is implicit. Functional-graph decomposition is known mathematics; this exact cipher construction is a proposal and requires an independent proof audit.
- **Prior art search:** 
  - **Date:** 2026-11-01
  - **Scope:** Read pinned baseline AGENTS.md, relevant H/EXT family records, and experiment headings/scopes. Targeted indexed web/GitHub queries used Kryptos/K4 plus arithmetic coding, Huffman, Tunstall, enumerative coding, Burrows-Wheeler, rotor-router, Pruefer, Foata, RSK, SEQUITUR, Golomb, multiset, functional graph and Fisher-Yates. Primary technical sources were separately sought. No matching exact K4 operator was established; this finite pass is not exhaustive.
  - **Limits:** Detailed linked local protocols were absent from the supplied four-file baseline. Pinned EXT-024 and EXT-034 GitHub page fetches returned cache miss; their exact source scope remains register-level, not freshly source-audited. No K4 calculation, target fitting, code execution of external sources, or external state change occurred.

<a id="n100-063"></a>
## N100-063 — Sandpile action on message-encoded spanning trees

**Draft reference:** `C18` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** As in C13, decode each 24-letter block to a tree on K_26. Orient it toward sink 0 and use ascending cyclic neighbor orders. Start one chip at vertex 1, repeatedly advance the rotor and move the chip until it reaches sink 0; the final rotors define a spanning tree. Re-encode it as Pruefer. The action has inverse equal to 25 repetitions because the K_26 sandpile group has exponent 26; independently prove this specific action relation before implementation. Pass the final source singleton unchanged.
- **Bounded test:** One complete graph, root, chip source and rotor order; seven outer phases. Tiny K_n trees for n=3..5 must establish output-tree validity, action order n and inverse n-1; do not assume a generic walk leaves a tree.
- **Controls:** 
  - **Positive:** Every spanning tree for n=3..5, source adjacent/nonadjacent to sink, and independent algebraic Laplacian/action comparisons.
  - **Negative:** Rotor rules not realizing the sandpile action must fail closure/order controls. Whole-pipeline nulls; source/sink choices are not tuned on the target.
- **Identifiability limit:** Free rotor fields or arbitrary sandpile-group elements would create a large key and are excluded. This map differs from merely relabeling the same tree and from routing message positions.
- **Novelty distinction:** C13 changes vertex labels; here a fixed group action changes tree edges. C14 routes source slots while preserving a separate graph; here the plaintext encodes the graph state itself. These differences need explicit synthetic witnesses.
- **Closest local external:** H-TREE-STATEFUL; H-NONLINEAR-BLOCK; EXT-034/041 nearest, but finite abelian lag-7 symbol feedback is not a sandpile action on trees.
- **Admission:** Research-only proposal; K4 not run. Mathematical foundations are known prior art, not claimed inventions. Exact public K4 history is unresolved beyond the cited inspected register and finite web search; no worldwide novelty or launch admission is claimed.
- **Priority:** 3
- **Estimated cost:** Research/proof first. Independently written exhaustive tiny oracles, then a frozen finite synthetic protocol; target cost and authorization are separate. Resource-limited or unverified work stays INCOMPLETE.
- **Sources:** 
  - https://arxiv.org/abs/0801.3306
  - https://arxiv.org/abs/1308.2677
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/EXTERNAL-PRIOR-ART.md
- **Framing and alignment:** The only outer layer is AZ Vigenere with literal key KRYPTOS and one global phase in 0..6: C_i=(Z_i+rank_AZ(KRYPTOS[(i+phase) mod 7])) mod 26. Its key and phase bounds are fixed before target use; no other key, alphabet, layer or rescue is implicit.
- **Prior art search:** 
  - **Date:** 2026-11-01
  - **Scope:** Read pinned baseline AGENTS.md, relevant H/EXT family records, and experiment headings/scopes. Targeted indexed web/GitHub queries used Kryptos/K4 plus arithmetic coding, Huffman, Tunstall, enumerative coding, Burrows-Wheeler, rotor-router, Pruefer, Foata, RSK, SEQUITUR, Golomb, multiset, functional graph and Fisher-Yates. Primary technical sources were separately sought. No matching exact K4 operator was established; this finite pass is not exhaustive.
  - **Limits:** Detailed linked local protocols were absent from the supplied four-file baseline. Pinned EXT-024 and EXT-034 GitHub page fetches returned cache miss; their exact source scope remains register-level, not freshly source-audited. No K4 calculation, target fitting, code execution of external sources, or external state change occurred.
- **Paper proof note:** For K_26 with one sink, the reduced Laplacian is L=26 I-J on 25 coordinates and L(e_v+1)=26 e_v. Therefore 26 copies of the chip-addition class are zero in the sandpile group. If the specified rotor action is correctly realized, its 25th power is its inverse. This algebraic argument does not replace an independent source/adapter/action audit.

<a id="n100-064"></a>
## N100-064 — Equality-partition rank conjugation

**Draft reference:** `C19` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Decompose P uniquely into first-occurrence letter list L and a restricted-growth string R describing its equality classes, with d distinct letters. Lexically rank R among all length-97 restricted-growth strings with exactly d classes, size S(97,d). Apply r'=(a r+1) mod S with a the least odd >=3 coprime to S, then unrank and relabel classes by the unchanged L. The output has the same first-occurrence list, enabling the inverse to recover L and d.
- **Bounded test:** One partition-rank map, seven outer phases. Exhaust small strings/partitions and independently compare DP ranks with explicit set partitions; check S=1 identity cases.
- **Controls:** 
  - **Positive:** All-equal, all-distinct, interleaved repeated classes, changes in class sizes and first-occurrence positions; full inverse fibers.
  - **Negative:** Illegal restricted-growth strings and altered first-occurrence order fail controls. Nulls matched on number of distinct letters, not only letter frequency, expose flexibility.
- **Identifiability limit:** A free partition rank offset would be a fitted message key and is forbidden. This deterministic proposal is distinct from C09 only if a witness confirms changed multiplicities while preserving first-occurrence list.
- **Novelty distinction:** C09 preserves the entire histogram; this preserves equality-class labels/order and count d but can change class multiplicities. The structural fiber is genuinely different, not a cosmetic radix or period change.
- **Closest local external:** H-CANONICAL-RESIDUAL-FEEDBACK compares a few recent equalities, not a globally encoded equality partition; H-EVOLVING-ALPHABET; EXT-048/051 unknown broader nonlinear scope.
- **Admission:** Research-only proposal; K4 not run. Mathematical foundations are known prior art, not claimed inventions. Exact public K4 history is unresolved beyond the cited inspected register and finite web search; no worldwide novelty or launch admission is claimed.
- **Priority:** 3
- **Estimated cost:** Research/proof first. Independently written exhaustive tiny oracles, then a frozen finite synthetic protocol; target cost and authorization are separate. Resource-limited or unverified work stays INCOMPLETE.
- **Sources:** 
  - https://www2.math.upenn.edu/~wilf/website/CombAlgDownld.html
  - https://www2.math.upenn.edu/~wilf/website/Unified%20setting.pdf
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/EXTERNAL-PRIOR-ART.md
- **Framing and alignment:** The only outer layer is AZ Vigenere with literal key KRYPTOS and one global phase in 0..6: C_i=(Z_i+rank_AZ(KRYPTOS[(i+phase) mod 7])) mod 26. Its key and phase bounds are fixed before target use; no other key, alphabet, layer or rescue is implicit.
- **Prior art search:** 
  - **Date:** 2026-11-01
  - **Scope:** Read pinned baseline AGENTS.md, relevant H/EXT family records, and experiment headings/scopes. Targeted indexed web/GitHub queries used Kryptos/K4 plus arithmetic coding, Huffman, Tunstall, enumerative coding, Burrows-Wheeler, rotor-router, Pruefer, Foata, RSK, SEQUITUR, Golomb, multiset, functional graph and Fisher-Yates. Primary technical sources were separately sought. No matching exact K4 operator was established; this finite pass is not exhaustive.
  - **Limits:** Detailed linked local protocols were absent from the supplied four-file baseline. Pinned EXT-024 and EXT-034 GitHub page fetches returned cache miss; their exact source scope remains register-level, not freshly source-audited. No K4 calculation, target fitting, code execution of external sources, or external state change occurred.

<a id="n100-065"></a>
## N100-065 — Euler-trail local-successor queue reversal

**Draft reference:** `C20` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** View the 97-letter word as a trail of 96 directed edges between its letter labels; retain start s and end t. For each vertex v list successors in visit order. For v!=t keep its final successor fixed and reverse the preceding successor queue; for v=t reverse its whole queue. Starting at s, consume the transformed queues to emit the new trail Z. The retained last exits form a tree toward t; the BEST last-exit construction supplies validity. Reversing the same queues again is the inverse.
- **Bounded test:** One queue involution, seven outer phases. Independently prove validity for open trails, closed trails s=t, loops, and parallel edges, then exhaust small words. No independent choice of queue ordering is permitted.
- **Controls:** 
  - **Positive:** Revisited vertices, self-loops, closed trails, several identical outgoing edges, and vertices with one successor; verify first/last letter and directed-bigram multiset preservation.
  - **Negative:** Reversing all queues without preserving last exits is a deliberately failing control. Nulls should match directed-bigram counts where possible; pure no-layer case is already excluded.
- **Identifiability limit:** A free Euler-trail order would generate huge ambiguity and is forbidden. Some words are fixed points; record effective operator support, not only syntactic distinctness.
- **Novelty distinction:** Transposition is induced by last-exit trees and local edge queues, not fixed message slots, checksum rotations, splay topology or BBWT suffix ordering. It preserves directed-bigram counts, a sharper invariant than ordinary multiset preservation.
- **Closest local external:** H-PERM; H-ROUTE; H-TREE-STATEFUL; EXT-002/008/034.
- **Admission:** Research-only proposal; K4 not run. Mathematical foundations are known prior art, not claimed inventions. Exact public K4 history is unresolved beyond the cited inspected register and finite web search; no worldwide novelty or launch admission is claimed.
- **Priority:** 2
- **Estimated cost:** Research/proof first. Independently written exhaustive tiny oracles, then a frozen finite synthetic protocol; target cost and authorization are separate. Resource-limited or unverified work stays INCOMPLETE.
- **Sources:** 
  - https://research.tue.nl/nl/publications/circuits-and-trees-in-oriented-linear-graphs-3/
  - https://arxiv.org/abs/0801.3306
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/EXTERNAL-PRIOR-ART.md
- **Framing and alignment:** The only outer layer is AZ Vigenere with literal key KRYPTOS and one global phase in 0..6: C_i=(Z_i+rank_AZ(KRYPTOS[(i+phase) mod 7])) mod 26. Its key and phase bounds are fixed before target use; no other key, alphabet, layer or rescue is implicit.
- **Prior art search:** 
  - **Date:** 2026-11-01
  - **Scope:** Read pinned baseline AGENTS.md, relevant H/EXT family records, and experiment headings/scopes. Targeted indexed web/GitHub queries used Kryptos/K4 plus arithmetic coding, Huffman, Tunstall, enumerative coding, Burrows-Wheeler, rotor-router, Pruefer, Foata, RSK, SEQUITUR, Golomb, multiset, functional graph and Fisher-Yates. Primary technical sources were separately sought. No matching exact K4 operator was established; this finite pass is not exhaustive.
  - **Limits:** Detailed linked local protocols were absent from the supplied four-file baseline. Pinned EXT-024 and EXT-034 GitHub page fetches returned cache miss; their exact source scope remains register-level, not freshly source-audited. No K4 calculation, target fitting, code execution of external sources, or external state change occurred.

<a id="n100-066"></a>
## N100-066 — Euclidean-quotient reversal on bounded integer pairs

**Draft reference:** `C21` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** For each four-letter block, split into two two-letter base-26 integers plus one, so u,v are in 1..676. Retain which slot contains A=max(u,v) and let B=min(u,v). If A/B<2 leave the pair unchanged. Otherwise divide by g=gcd(A,B), compute the canonical regular continued fraction of A/B with last quotient >=2 unless it is a singleton, reverse its quotient list, and reconstruct the reduced fraction A0/B0prime. Continuant symmetry preserves A0=A/g. Output A in its original larger slot and g*B0prime in the other; subtract one and render two letters each. Pass final singleton unchanged. This is an involution: reversed first/last quotients stay >=2, the guard stays true, numerator/gcd/orientation remain fixed, and reversing again restores the pair.
- **Bounded test:** One block size 4, origin 0, ratio guard 2 and canonical convention; seven outer phases. Independent exact-rational proof plus exhaustive integer pairs on bounds 1..32 must precede any larger plant/test. Establish non-equivalence to fixed symbol substitutions, affine digraph maps and fixed-modulus fractional-linear maps.
- **Controls:** 
  - **Positive:** Ratios below/exactly/above 2, equal inputs, nontrivial gcds, singleton continued fractions, leading and trailing quotient 2, and nonpalindromic quotients; independent Euclid and continuant-matrix implementations.
  - **Negative:** Naive unguarded quotient reversal or accepting a noncanonical final quotient 1 must fail designated controls. Whole-pipeline nulls and matched fixed-point/nonfixed-point strata expose weak effective coverage.
- **Identifiability limit:** No free rational function, quotient permutation or message-dependent threshold is allowed. Many pairs are fixed; operator support must be measured on independent synthetic inputs. The mechanism is speculative and mathematically defined, not a claimed historical cipher.
- **Novelty distinction:** The larger coordinate supplies a data-dependent modulus and a Euclidean parse; the smaller coordinate changes via reversed quotients while preserving gcd. This is not merely changing radix, adding a carry, or applying a fixed Mobius matrix. The equivalent parity-signed inverse modulo the variable numerator must be compared explicitly against any variable-modulus inversion proposal before final deduplication.
- **Closest local external:** H-NONLINEAR-BLOCK; H-AFFINE-DIGRAPH; H-RADIX-FEEDBACK; EXT-012/041/049. Structural-pool exact overlap review requested; no matching operator established in the inspected baseline.
- **Admission:** Research-only proposal; K4 not run. Mathematical foundations are known prior art, not claimed inventions. Exact public K4 history is unresolved beyond the cited inspected register and finite web search; no worldwide novelty or launch admission is claimed.
- **Priority:** 3
- **Estimated cost:** Research/proof first. Independently written exhaustive tiny oracles, then a frozen finite synthetic protocol; target cost and authorization are separate. Resource-limited or unverified work stays INCOMPLETE.
- **Sources:** 
  - https://dlmf.nist.gov/1.12
  - https://www.cecm.sfu.ca/organics/papers/corless/knuth/html/knuth.html
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/EXTERNAL-PRIOR-ART.md
- **Framing and alignment:** The only outer layer is AZ Vigenere with literal key KRYPTOS and one global phase in 0..6: C_i=(Z_i+rank_AZ(KRYPTOS[(i+phase) mod 7])) mod 26. Its key and phase bounds are fixed before target use; no other key, alphabet, layer or rescue is implicit.
- **Historical note:** Continued-fraction identities are classical; this bounded conjugation is a speculative application, not a worldwide novelty claim.
- **Prior art search:** 
  - **Date:** 2026-11-01
  - **Scope:** Read pinned baseline AGENTS.md, relevant H/EXT family records, and experiment headings/scopes. Targeted indexed web/GitHub queries used Kryptos/K4 plus arithmetic coding, Huffman, Tunstall, enumerative coding, Burrows-Wheeler, rotor-router, Pruefer, Foata, RSK, SEQUITUR, Golomb, multiset, functional graph and Fisher-Yates. Primary technical sources were separately sought. No matching exact K4 operator was established; this finite pass is not exhaustive. Additional targeted queries: Kryptos K4 continued fraction; Kryptos mixed radix; Kryptos K4 Chinese remainder. These did not establish an identical K4 operator in the returned indexed results.
  - **Limits:** Detailed linked local protocols were absent from the supplied four-file baseline. Pinned EXT-024 and EXT-034 GitHub page fetches returned cache miss; their exact source scope remains register-level, not freshly source-audited. No K4 calculation, target fitting, code execution of external sources, or external state change occurred.
  - **Additional queries:** Kryptos K4 "continued fraction" cipher; Kryptos K4 "mixed radix" CRT. These additional queries on 2026-11-01 did not locate an exact K4 operator; no global novelty inference follows. Continued-fraction cryptography itself has older literature and is not an invention here.
- **Paper proof note:** For M(q)=[[q,1],[1,0]], each factor is symmetric; reversing the factors transposes their product. The upper-left entry, the reduced numerator continuant, is unchanged. The canonical first and last quotients are both >=2 on the nontrivial branch, so reversal stays canonical and its denominator is <= half that numerator. Scaling by the original gcd preserves the bounded pair, and the larger-slot ordering remains unchanged. This is a paper derivation, not independently validated execution.

<a id="n100-067"></a>
## N100-067 — CRT residues recoded as mixed-radix digits

**Draft reference:** `C22` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** For each three-letter block let x be its AZ base-26 integer, 0<=x<26^3. Set r2=x mod 2^3 and r13=x mod 13^3, then y=r2+2^3*r13 and render y in three base-26 letters. For the final one-letter block use the identical formula with b=1. In general the inverse extracts r2=y mod 2^b and r13=floor(y/2^b), then solves x=r2 (mod 2^b), x=r13 (mod 13^b), uniquely in 0..26^b-1.
- **Bounded test:** One block width 3, origin 0 and residue order, plus specified final width 1; seven outer phases. Independently prove CRT bijection and exhaust all b=1..3 integer inputs only after synthetic authorization. Compare complete tiny operators to digit permutations, single-letter substitutions and Z26-affine block maps.
- **Controls:** 
  - **Positive:** Both residue extremes, carries across base-26 digit boundaries, x=0 and x=26^b-1, and the final ragged digit; independent constructive-CRT and lookup inverses.
  - **Negative:** Using noncoprime moduli or dropping one residue is a deliberately failing control. Whole-pipeline nulls and shuffled block controls calibrate clue specificity; no free moduli are inferred from the target.
- **Identifiability limit:** An arbitrary family of moduli/packing maps could become a large cipher key; only 2^b and 13^b, fixed residue order and width are proposed. A single-letter branch alone is just a substitution and cannot be counted as novel coverage.
- **Novelty distinction:** The value changes because simultaneous CRT residues are treated as positional mixed-radix digits; this is not ordinary base conversion preserving the integer. It acts on multi-letter integers, not the per-letter CRT split used merely to solve equations, and is not an alphabet/period extension of H-RADIX-FEEDBACK. Deduplicate against structural-pool CRT block operators before counting.
- **Closest local external:** H-NONLINEAR-BLOCK; H-RADIX-FEEDBACK; H-AFFINE-DIGRAPH; H-CARRY-624; EXT-008/041 use CRT/group arithmetic in different operators, not this residue packing.
- **Admission:** Research-only proposal; K4 not run. Mathematical foundations are known prior art, not claimed inventions. Exact public K4 history is unresolved beyond the cited inspected register and finite web search; no worldwide novelty or launch admission is claimed.
- **Priority:** 3
- **Estimated cost:** Research/proof first. Independently written exhaustive tiny oracles, then a frozen finite synthetic protocol; target cost and authorization are separate. Resource-limited or unverified work stays INCOMPLETE.
- **Sources:** 
  - https://dlmf.nist.gov/27.15
  - https://xlinux.nist.gov/dads/HTML/chineseRmndr.html
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/HYPOTHESES.md
  - https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/EXTERNAL-PRIOR-ART.md
- **Framing and alignment:** The only outer layer is AZ Vigenere with literal key KRYPTOS and one global phase in 0..6: C_i=(Z_i+rank_AZ(KRYPTOS[(i+phase) mod 7])) mod 26. Its key and phase bounds are fixed before target use; no other key, alphabet, layer or rescue is implicit.
- **Prior art search:** 
  - **Date:** 2026-11-01
  - **Scope:** Read pinned baseline AGENTS.md, relevant H/EXT family records, and experiment headings/scopes. Targeted indexed web/GitHub queries used Kryptos/K4 plus arithmetic coding, Huffman, Tunstall, enumerative coding, Burrows-Wheeler, rotor-router, Pruefer, Foata, RSK, SEQUITUR, Golomb, multiset, functional graph and Fisher-Yates. Primary technical sources were separately sought. No matching exact K4 operator was established; this finite pass is not exhaustive. Additional targeted queries: Kryptos K4 continued fraction; Kryptos mixed radix; Kryptos K4 Chinese remainder. These did not establish an identical K4 operator in the returned indexed results.
  - **Limits:** Detailed linked local protocols were absent from the supplied four-file baseline. Pinned EXT-024 and EXT-034 GitHub page fetches returned cache miss; their exact source scope remains register-level, not freshly source-audited. No K4 calculation, target fitting, code execution of external sources, or external state change occurred.
  - **Additional queries:** Kryptos K4 "continued fraction" cipher; Kryptos K4 "mixed radix" CRT. These additional queries on 2026-11-01 did not locate an exact K4 operator; no global novelty inference follows. Continued-fraction cryptography itself has older literature and is not an invention here.
- **Paper proof note:** CRT maps [0,26^b) bijectively onto [0,2^b) x [0,13^b). Mixed-radix packing (r2,r13) -> r2+2^b*r13 is a second bijection onto the same integer range. Their composition has the stated inverse. This does not establish non-equivalence to every prior block construction; that remains a separate gate.
