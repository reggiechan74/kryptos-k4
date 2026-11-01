# M21 synthetic protocol (completed once)

## Scope
Validate exact framed capacity counts; measure whether bit-aware filtering improves on exact length-only feasibility. No K4 text, clues, corpus, key fitting, target transport, or target score. Twelve fixtures below are coverage adapters for classical mechanisms, **not twelve novel hypotheses**, independent cryptanalytic discoveries, or evidence of broad real-codec tractability. If implementation reveals redundant coverage, consolidate and disclose the change before freezing; do not pad a quota.

## Twelve fully specified tiny adapters
Input alphabet order is the listed order. All start at the stated empty/initial state. Invalid terminal state rejects. Binary words below are literal emissions. Framing is applied outside the codec.

1. **Fixed binary:** alphabet A,B; A->0, B->1; no state/trailer.
2. **Static ternary prefix:** A->0, B->10, C->11.
3. **Bounded gamma:** symbols A,B,C,D denote positive1,2,3,4; emissions1,010,011,00100 respectively. No general integer search.
4. **Bounded Rice(k=1):** symbols A,B,C,D denote0,1,2,3; emissions00,01,100,101, i.e. unary quotient ones then zero then one remainder bit.
5. **Bounded Fibonacci:** A,B,C,D denote1,2,3,4; emissions11,011,0011,1011 respectively. This explicit table, not an external implementation, is the definition.
6. **State-switched prefix:** alphabet A,B,C. State0 codes A0 B10 C11; state1 codes A11 B0 C10. Start0; toggle state only after input B. No trailer.
7. **Bit stuffing:** alphabet A,B emits source bits0,1. State is trailing-one count0,1,2, initially0. After each emitted source bit, if count reaches2 emit an extra0 and reset count0. A resets count0. No trailer. This threshold is deliberately tiny for complete coverage.
8. **Buffered pairs:** alphabet A,B. First letter of each pair emits empty word and is buffered; second completes AA->0, AB->10, BA->110, BB->111, then clears buffer. At end a single buffered A emits0; B emits1; empty buffer emits nothing. Input n is declared, so final one-letter tail length is known by n parity.
9. **Bounded run chunks:** alphabet A,B, bits0,1. Buffer symbol and run length1..2; incoming same symbol increases count, and at3 immediately emit symbolbit followed by110 (unary run-length3), clear buffer. Incoming different symbol flushes old symbolbit followed by (r-1) ones then0, then buffers new symbol with count1. At end flush any buffer identically. Empty input emits empty. This deterministic convention handles runs longer than3 in canonical chunks.
10. **Move-to-front prefix:** alphabet A,B,C, initial list ABC. Encode zero-based rank0,1,2 as0,10,11, then move input symbol to list front. Six possible list states, no trailer.
11. **Parity trailer:** alphabet A,B emits0,1, tracks XOR of all source bits initially0. Emit that one parity bit at end, including empty input. This is a terminal-framing fixture, not a compression novelty.
12. **Variable-to-fixed phrase:** alphabet A,B, greedy phrase dictionary A->00, BA->01, BBA->10, BBB->11. Buffer incomplete prefixes empty/B/BB. Complete phrase emits code and clears buffer. At end accept only empty buffer: B or BB is incomplete and rejected, not silently padded.

The fixture set covers static prefix codes, integer-code tables, state-conditioned codes, stuffing, buffering, run length, adaptive finite permutation, trailers, and incomplete phrases. Tables3–5 overlap mathematically with static prefix coding; they are explicit boundary fixtures, not separate mechanism-level novelty.

## Frozen finite matrix
- Input lengths n=0..6.
- Domain modes: unrestricted; first input fixed to least alphabet symbol; first input fixed to greatest symbol. At n=0 all three coincide; deduplicate those case IDs.
- External headers: empty, `1`, `11`. Codec trailers apply after payload and after the header only once. Empty header is explicitly a possibly noninjective integer framing, not asserted decodable.
- Output bases b in {2,3,26}; requested widths d=1..6.
- Transport convention: canonical minimal digits including zero as one digit; fixed-width digits allowing leading zero digits.
- At most27,216 case requests before empty-domain-mode deduplication. At most65,532 raw input strings across all12 adapters and all n if every alphabet were size4; actual alphabet bounds are smaller. Encode each input once per adapter before applying framing/case filters in the independent oracle.
- No97-length or full26-letter alphabet target proxy in this correctness pilot. Scalability to those dimensions is not established by tiny cases.

## Independent implementations
A. Production method: natural-number DP from REPORT.md, explicit maximum bitlength and terminal handling. Return exact input count, zero/nonzero decision, and one witness if nonzero.
B. Oracle: direct exhaustive input Cartesian products, independently written encoder transitions/terminal handling, concatenate literal bits, use ordinary big integer parsing and direct radix arithmetic for width. Do not reuse DP transitions, threshold comparators, or result caches. Cross-check adapter tables by hand fixtures before differential comparison. Reusing the specification is necessary; reusing the implementation is not independent.
C. Baselines: (1) safe min/max emitted-length envelope; (2) exact attainable-length DP, ignoring bit values, accepting if any feasible length's permitted numeric envelope intersects requested interval. Distinguish weak range[0,2^L-1] from strengthened nonzero-leading-bit range[2^(L-1),2^L-1] when the frame guarantees it; never assume the latter for empty-header frames. Report both. (3) entropy expected-size diagnostic under uniform fixture symbols, clearly not a sound rejector. Do not credit invalid entropy rejections as useful pruning.

Compare A and B exact counts on every supported case. Compare zero/nonzero decisions separately. Record visited states/transitions, peak count bitlength, elapsed CPU and memory, oracle work, and cases where A excludes while baseline2 passes. Do not promise runtime superiority on tiny cases or selectively report only positive pruning. Report cases where all methods agree or bit-aware DP costs more.

## Mandatory controls / acceptance contract
1. Inclusive endpoints b^d-1 and b^d, lower endpoint b^(d-1), and zero with d1 vs d2; construct synthetic finite raw-bit framing adapters if these boundary integers are absent from the main matrix. These are controls, not extra hypothesis count.
2. Leading-zero payloads at several L, empty payload and explicit empty-bitstring zero convention; fixed-width versus minimal digits must differ where appropriate.
3. Mandatory header once, missing/doubled header, parity trailer once and missing trailer. Mutation controls compare against their own declared altered model: no assumption every mutation must change the answer.
4. Incomplete phrase B/BB for adapter12 must reject. No clipping or implicit padding to make it pass.
5. Deliberately colliding encoder A->0,B->00: count input strings, separately enumerate distinct integers, demonstrate these are different quantities. Mark noninvertible, do not call it a validated cipher.
6. Synthetic clipped transport N mod b^d must be rejected by the interval API as unsupported; use a hand case N=b^d to demonstrate why treating it as ordinary width would be unsound.
7. Plaintext position restrictions at first/middle/last positions on small control cases; no transporting position indices to bits/digits.
8. Domain restriction cannot increase count; interval expansion cannot decrease count; splitting a domain into disjoint parts must give additive counts. Verify against exhaustive oracle, not only DP self-consistency.
9. The two hand witnesses in REPORT.md must exhibit genuine improvement over exact attainable-length baseline. These demonstrate mechanism, not empirical prevalence.
10. A deliberately nondeterministic duplicate path must be refused or labeled derivation-count mode; it must not silently double plaintext counts.

Pass requires zero exact-count mismatches and zero false-pruning across all supported cases; unsupported controls must return unsupported explicitly. Failure stops scientific promotion and produces a reproducible counterexample. A limited utility pass additionally requires the hand witnesses and honest matrix pruning/work report, but does not establish a new mathematical technique or a practical97-symbol attack.


## Actual frozen scope and execution
The deduplicated manifest contains24,624cases;132mandatorycontrols. One execution was bounded by180childCPU seconds,240wall seconds and1GiB address space. Actual childCPU4.11879517seconds. No target data or remote mutation. The whole raw original protocol was frozen before execution; this publication removes administrative allocation/approval coordination only. Original hashes remain in provenance.
