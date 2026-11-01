# A01 / N100-036 admission audit

**1 November 2026 — BLOCKED: unresolved specific prior-art overlap. No cipher or synthetic experiment executed.**

The 52-description frequency-order proposal is mathematically well-defined, but is not cleared as an untried K4 model. Do not allocate its proposed 60-CPU-second pilot or promote it from the draft backlog. Preserve its original proposal and add this dated status correction; it remains one of 100 research proposals, not one of 100 admitted experiments.

## Decisive primary evidence

[Matbalez's public July 18 handoff, section 6.6](https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0#66-moving-alphabets-and-historical-machines) expressly includes adaptive **“frequency-count state rules”** among attempted models. It reports 5,234,944 configurations for each public-strip adaptive model. This is an author-reported search, not an independently reproduced negative. The linked adaptive report is an unbundled original-workspace artifact. Count initialization, ranking/tie policy, plaintext versus ciphertext update, mapping direction, offsets and tested key domain cannot be recovered from this prose. Consequently inclusion or disjointness of A01's exact 52 descriptions is unresolved. Generic frequency-count adaptation cannot be advertised as untried.

The rendered gist and revision list were accessible. Its Raw link advertised revision `9ca53efbbecdda0469a992c992ef4cc8af3f2d21`; the raw retrieval returned a non-retryable safe-redirect failure and the revision-rendered URL was inaccessible. Thus **this is an observed revision identifier, not an authenticated raw-body hash or source-code pin**. No alternate route was used to obtain denied raw content. The existing EXT-051 record covers the same handoff but currently emphasizes recurrence scopes; add this distinct adaptive overlap consequence there.

## Exact proposed operator and inverse

Let `T` be AZ or the literal permutation `KRYPTOSABCDEFGHIJLMNQUVWXZ`. Begin with all symbol counts zero. Before position i, let `L_i` sort letters by descending count, with ties resolved by T. For offset b in 0..25, encode plaintext x as AZ symbol with rank `(index(L_i,x)+b) mod 26`; increment only x's count after emission. Decode rank c by choosing `L_i[(c-b) mod 26]`, then increment that recovered letter. No reset, nonzero prior count, second offset or alternate output alphabet is present.

Induction proves inverse correctness: both ends begin with the same count vector; the deterministic total order is a permutation; offset addition is a bijection; decoding selects the unique original x, so both ends make the same update. This gives a full bijection on each fixed-length string set for every description. It does not identify the intended K4 system.

The 52 descriptions have distinct first-step maps. Within a tie order, different offsets differ. Across AZ and KRYPTOS, the rank difference is not constant (A differs by 7 while K differs by -10 modulo 26), so no offset makes the initial maps identical. This is a symbolic distinction, not an executed enumeration.

## Local and external comparisons

- **H-BOUNDARY-STATE:** the retained local MTF rule emits through a changing output permutation and moves the emitted ciphertext symbol to the front; its 388 schedules are not an exhaustive frequency-count family. The proof for that exact MTF rule does not transfer automatically to A01.
- **H-EVOLVING-ALPHABET / study 060:** exactly 104 ciphertext-driven pointer/exchange descriptions and 104 fixed-reference prefix reversals were tested. Their operations do not maintain plaintext frequency counts. A01 is not merely changing a pointer/offset, but a complete global non-alias proof against all 208 composed input/output maps has not been supplied by this audit. Names and sample traces do not establish disjointness.
- **EXT-034:** markmnl's documentation lists MTF/MTB, wheels and triggers/resets; no source-complete A01 comparison follows. Absence from the short register is not absence from that research.
- **EXT-052:** the inspected mruckman 033b source uses a fixed keyword-derived alphabet pool and position/ciphertext/prefix selectors; it does not implement A01's online decoded-plaintext count sorting. This narrow distinction does not repair the matbalez overlap gap.

### Simple grammar witnesses, not blanket 208-function separation

On toy alphabet ABC, offset zero and AZ tie order, compare rank-before-update list-access rules with the same input interpretation:

| Update rule compared with frequency count | Plaintext prefix | Frequency-count next order | Other rule next order | Separating next plaintext |
|---|---|---|---|---|
| Move requested symbol to front | AB | ABC | BAC | A: ranks 0 versus 1 |
| Move requested symbol to back | A | ABC | BCA | A: ranks 0 versus 2 |
| Swap requested symbol with head | C | CAB | CBA | A: ranks 1 versus 2 |
| Reverse prefix through requested symbol | C | CAB | CBA | A: ranks 1 versus 2 |

These four symbolic witnesses distinguish the stated list-update grammars. The exchange/prefix rules in study 060 instead use their own ciphertext-indexed operations, so the table is not a substitute for exact source-equation comparison with those rules.

## Execution decision and dormant finite protocol

**Current decision: no pilot and no target run.** To reopen, obtain exact public source/precise equations for the reported frequency-count bank and compare the complete initialization, two alphabet roles, mapping direction, update timing, tie-breaking, offsets and resets. If A01 is a subset, retire it as covered without repeating it. If exact differences are established, independently review those differences; do not treat unavailable evidence as novelty.

Only after that gate, a small synthetic proposal could freeze two independent encoders/decoders and enumerate all plaintext strings through length 6 on alphabets of sizes 2, 3 and 4, both ascending and reversed tie orders, every offset. Compare each inverse and full output against a forward truth table; retain all descriptions, not only a winner. Add the literal witnesses above, zero-length/all-equal/alternating cases, wrong asserted letters and malformed symbols. Proposed total hard cap: 60 CPU seconds, 256 MiB, 120 seconds elapsed; stop on any mismatch, limit or uncertain completion, no automatic retry. This is an unallocated, unexecuted design, not a benchmark outcome or K4 admission.

## Next concrete source/proof candidate

Prefer the existing **C20 / N100-065 successor-queue reversal composite** for the next bounded admission audit, not automatic execution. A quick check of H-PERM and H-ROUTE found only a pure-permutation multiset exclusion and specified fixed-position route/periodic domains, not an explicit last-exit queue involution. Its fixed seven-phase KRYPTOS outer layer must still be compared against retained route/key scopes. Prove the open/closed-trail inverse and last-exit invariant, and audit exact external coverage before creating controls. Its claimed structure is not an invention, and this quick comparison is not full novelty clearance. No target-derived permutation or K4 arithmetic was computed.

## Sources and provenance

- Baseline repository: `reggiechan74/kryptos-k4`, published commit `3e128d9a617af377516a0b9878a942b29bf2e3b8`; current local publisher also contains an uncommitted next-100 annex.
- [Study 060 protocol](https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/candidate-first-060/PROTOCOL.md), local exact SHA256 `8d799939fbfcb9bd124966fe492d8ea247e88dbe4e5124e6eb1315e2d07c7689`.
- [Boundary-state findings](https://github.com/reggiechan74/kryptos-k4/blob/3e128d9a617af377516a0b9878a942b29bf2e3b8/research/SINGLE-BOUNDARY-RESET-FINDINGS.md), local exact SHA256 `d74c7258854ceafec9c529b4e1ea671e51747c9a0bcb18ec9ede6bec6e62c185`.
- [Mruckman 033b](https://github.com/mruckman1/k4_cipher/blob/e4912152555f635c35e73fe454a8302a98a5902f/experiments/033b_per_position_state_dependent.py), prior inspected blob `a9d9c2810fdb35deb8d57d9b4d219f08845c08bb`; this audit relies on the source-scope dossier, not new execution.
- Original draft catalog SHA256 `1b58132bd63c42618c5d1c20bff280c01ea6ffa89d44582c4dfe21a154801862`; left unchanged.
- Targeted web queries on 1 November: `Kryptos frequency adaptive alphabet`, `Kryptos frequency-count`, `Kryptos frequency count adaptive`, and `Kryptos successor Euler cipher`. Finite indexed search, not a full corpus census.

All work in this audit was source reading, symbolic reasoning and document preparation. No K4 input, target fit, cipher program, synthetic batch, archive extraction or external mutation was performed. Applicable project instructions and repository AGENTS were read first. Publisher owns subsequent ledger integration; this audit edits no shared repository files.
