# M21 / N100-099 — framing-capacity feasibility review

Status: **synthetic exactness and limited-utility pilot completed; no K4 target admitted.**
Date: 2026-11-01. Review baseline: repository commit `294c37f3d601437f128ec062fc4bd9e356601b76`.

The design analysis below predates the completed pilot; statements about then-unmeasured utility are historical. README.md gives the measured result and limitations.

## Decision
Narrow the proposal to **exact input-string counting under a framed binary encoder and an integer interval**. Do not build or claim a generally small binary-to-base26 conversion automaton. Whole-message output **width** has a cheap interval characterization; arbitrary output contents, adaptive dictionaries, clipped digits and ambiguous grammars do not inherit that guarantee.

The mathematics is classical weighted-automaton/product dynamic programming, not a newly invented cryptanalytic primitive. A useful local contribution remains plausible: a verified framing-contract-aware zero-count certificate that can reject encoder families before language fitting, with stronger pruning than exact attainable-length checks. Practical payoff remains unmeasured. Do not open a separate novelty repository or mark this hypothesis scientifically tested on the strength of this design.

## Exact model and theorem
Let a finite deterministic encoder have state q, initial state q0, input alphabet Sigma, and transitions delta(q,a)=(q',w), where w is a finite binary word. Each transition consumes exactly one input letter, even when w is empty. A finite header h is emitted once; an explicit terminal accept predicate and state-dependent finite trailer tau(q) are applied once. Input length n and allowed plaintext-letter domains D_i are fixed. All framing bits count. Define B as a proved maximum emitted length for these n inputs, including header/trailer.

Transport interprets the entire framed bitstring as an unsigned big-endian integer N. For ordinary canonical base b digits with the usual one-digit zero representation, exact digit count d means:

- d=1: 0 <= N <= b-1;
- d>1: b^(d-1) <= N <= b^d-1.

Fixed-width d-digit zero-padded transport instead means 0 <= N <= b^d-1. A positive-only convention is a different explicit contract. Bijective base-b transport is out of this first pilot: its interval can be derived separately, but must not be silently substituted for positional arithmetic.

For every possible total bitlength L in [0,B], intersect the allowed integer interval with [0,2^L-1]. If nonempty, represent its two inclusive endpoints in exactly L bits. Run a DP indexed by (input position i, encoder state q, emitted length t, relation to lower bound, relation to upper bound). Each comparison relation is less/equal/greater; the emitted word updates both relations at successive bit positions. Reject overflow t>L. Emit header before input and trailer after exactly n letters; accept only valid terminal encoder states, t=L, lower relation >= and upper relation <=. Empty bitstring maps to zero only where the frame contract explicitly permits it; it is not implicitly a one-bit payload.

**Proof.** Determinism associates every allowed input string with exactly one encoder path and one emitted bitlength. Inductively, comparison states are precisely the lexicographic ordering of the emitted prefix against both bound prefixes. At equal length, lexicographic order equals unsigned numeric order. Thus terminal acceptance is equivalent to the specified framed encoder satisfying the integer interval. Every accepted input is counted once in exactly one L stratum. Summing terminal path counts in natural-number arithmetic therefore gives the exact number of admissible plaintext strings. A zero count proves impossibility only for this specified encoder, framing, transport and input domain. It cannot exclude other compression families.

Empty emissions cause no cycle because input position always increases. Rejecting terminal states correctly represent incomplete codewords. A nondeterministic encoder would count paths/derivations instead, unless unambiguity or deduplication is separately proved.

A straightforward separate-L implementation costs O(n |Q| |Sigma| B^2 max(1,wmax)) transition-bit operations, plus explicit header/trailer work; sequential strata need O(|Q| B) rolling-layer cells up to constant comparator factors. Counts require arbitrary-precision integers: arithmetic bit-cost is additional. These are upper bounds, not measured speed claims. State-dependent maximum trailer length belongs in B.

## Why this is stronger than a length check
Hand-derived witness (not an experiment): A->0, B->1; header `11`; n=2. Every encoded string has four bits and integer value12..15. Exactly two canonical base3 digits allow3..8. Even a length-only baseline granting a nonzero leading bit passes because the four-bit range8..15 intersects at8. The exact bit-aware filter excludes every input.

Second witness: A->00, B->11, no header, n=2, first plaintext letter fixed to B. Possible integers12 and15 again fail the same3..8 interval. Domain constraints attach to **plaintext transition positions**, never to emitted-bit or transported-digit positions.

Entropy estimates concern averages under a source model and are not zero-error individual-message rejection bounds. The honest strong baseline is exact attainable-length DP, then numeric-range overlap consistent with the declared framing guarantee. Full-prefix knowledge may strengthen that baseline; record exactly what it knows.

## Framing and scientific boundaries
- Leading zero bits may make a long bitstring represent a small integer. Never reject solely because L exceeds the bound's binary width. Left-pad threshold endpoints to L bits.
- Integer conversion loses leading zeros unless fixed length is recoverable or a sentinel is used. A `1 || payload` sentinel is an injective framing of arbitrary payload bitstrings; it does not make a noninjective codec injective.
- Exact counts are counts of **input strings**, not distinct outputs. Integer collisions and encoder collisions must be surfaced separately. A capacity pass cannot establish a decodable cipher model.
- Positive feasibility says nothing about matching a particular ciphertext. Width is only a necessary condition for a full target relation. Marginal letter supports do not describe all jointly feasible combinations.
- Clipping/modulo b^d is not an interval test. Either use a separately justified exact remainder construction (potentially b^d states), or return unsupported. Never turn unsupported into zero-count.
- No generic small-state claim for LZW's adaptive dictionary, arithmetic coding, unbounded grammar stacks, or general base conversion. A bounded prefix grammar must have an explicit finite encoder and terminal behavior.
- A97-symbol base26 output gives an interval with large endpoints, not automatically a practical full ciphertext constraint. A97-letter alphabet/domain and a large encoder state space can still make this DP expensive.

## Comparison to recorded work
**Local Compression043.** Inspected specification, findings, sources, and `experiments/compress_transport_043.py` statically, without running them. It tests97-uppercase input -> native default16-bit block-mode .Z -> big-endian integer -> eight transports (two alphabets, positional/bijective, two directions). Its old target interpretations failed .Z header checks; that narrow result is not to be replayed or generalized. Its synthetic round trips/header controls are not a generic exhaustive input-count DP, and they do not establish that all plants have97 transported digits. Header magic already provides a very effective specialized framing rejection; M21 must not claim to improve that existing negative or certify a new target family. Adaptive .Z is outside the small-state pilot.

**EXT-024.** The pinned README describes a one/two-plaintext-letter-per-cipherletter assumption and English-word filtering. This is documentation-level evidence of a variable-rate attempt; no exhaustive receipt or exact framed capacity counter was verified. The present proposed tool does not relabel that search as novel, and its distinct implementation gap is provisional, not proof that nobody has built one.

## Primary-source comparison and receipts
1. Mehryar Mohri, [Weighted Automata Algorithms](https://cs.nyu.edu/~mohri/pub/hwa.pdf), especially generic semiring distance/counting and acyclic graph treatment. Finite weighted composition and path aggregation are established machinery. This proposal instantiates them; it does not claim their invention.
2. Gilles Pesant (2004), [A Regular Language Membership Constraint for Finite Sequences of Variables](https://doi.org/10.1007/978-3-540-30201-8_36); [university publication record](https://publications.polymtl.ca/24731/). Regular-language constraints on fixed variable sequences are established. Bibliographic record/abstract checked; no assertion that this review inspected every implementation detail of the paper.
3. [Choco official integer-constraint documentation](https://choco-solver.org/docs/modeling/intconstraints/), regular/costRegular/multiCostRegular sections: practical regular and cost-automaton constraints predate this proposal.
4. [EXT-024 pinned README](https://github.com/neuroretransmit/kryptos-k4/blob/5a2a598cde181444769ef4fbe48dfb1bea12b44c/README.md), connector-read blob `15eb9802fbeecb411cf0e2dce719df3b0eadf97c`.

Bounded public searches included Kryptos+compression+finite-state, Kryptos+framing+automaton, the EXT-024 repository, author weighted-automata sources and regular-constraint documentation. No matching K4-specific counter was verified in that bounded pass. Search absence is not novelty evidence. No externally retrieved code was executed. Historical Compression043 findings were read, but no K4 ciphertext was newly fetched, transformed, fitted or evaluated.


Independent static design/source review and full retained-output readback passed. See README.md for the completed pilot, cost limits and evidence.
