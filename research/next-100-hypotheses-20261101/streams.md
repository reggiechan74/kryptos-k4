# Nonlinear or irregular stream mechanisms

All entries are proposed and unrun. A specified research question is not a novelty clearance or permission to launch a K4 search. See [README](README.md) for gates, priorities and source limitations.

<a id="n100-068"></a>
## N100-068 — Irregularly decimated two-register stream

**Draft reference:** `B01` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Clock binary registers A and B together; keep B's outgoing bit only when A's outgoing bit is1. A uses s[t+5]=s[t+2] xor s[t], B uses s[t+7]=s[t+1] xor s[t]. Convert consecutive emitted bits to MSB-first5-bit values reduced mod26; use AZ additive C_i=P_i+K_i mod26, with no additional alphabet or sign search.
- **Bounded test:** All nonzero5- and7-bit seeds (31×127); enforce a maximum4096 source clocks per97-symbol message. First reproduce the generator and round-trip fresh synthetic97-letter plants; compare exact generated shift streams against all recovered external banks before target admission.
- **Controls:** Independent small-register exhaustive streams; all-zero selector must reject, not hang. Include uniform ciphertext nulls and all24 fixed clue checks only after the source/synthetic gate.
- **Identifiability limit:**  A stream matching clues is only compatibility; report all full decryptions and complete parameter equivalence classes. Finite generators may alias prior short-period models. No source/creator evidence selects this generator.
- **Novelty distinction:** Irregular output deletion differs from EXT-010's consecutive fixed chunks. Shrinking generators themselves are established cryptography, not invented here.
- **Closest local external:** H-AUTONOMOUS-RECURRENCE; EXT-010; EXT-040; EXT-050; EXT-051; mruckman1 generator dossier
- **Admission:** proposed; prior mathematical-generator scope unresolved; no target admission
- **Priority:** 5
- **Estimated cost:** Design/source comparison first. Synthetic implementation pilot ≤120 CPU seconds; full parameter scan cost must be preflighted separately, no automatic target run.
- **Sources:** 
  - https://doc.sagemath.org/html/en/reference/cryptography/sage/crypto/stream.html
  - https://github.com/mruckman1/k4_cipher/blob/e4912152555f635c35e73fe454a8302a98a5902f/docs/shift_sequence_hypotheses.md

<a id="n100-069"></a>
## N100-069 — Self-decimating register stream

**Draft reference:** `B02` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Use one register s[t+11]=s[t+2] xor s[t]. Read nonoverlapping outgoing pairs (u,v); emit v iff u=1. Convert consecutive emitted bits to MSB-first5-bit values reduced mod26; use AZ additive C_i=P_i+K_i mod26, with no additional alphabet or sign search.
- **Bounded test:** All2047 nonzero seeds; source-clock cap8192, no alternate taps after results. First reproduce the generator and round-trip fresh synthetic97-letter plants; compare exact generated shift streams against all recovered external banks before target admission.
- **Controls:** Independent pair-decimation oracle, phase0/1 regression fixture without treating extra phase as new hypothesis, starvation controls. Include uniform ciphertext nulls and all24 fixed clue checks only after the source/synthetic gate.
- **Identifiability limit:**  A stream matching clues is only compatibility; report all full decryptions and complete parameter equivalence classes. Finite generators may alias prior short-period models. No source/creator evidence selects this generator.
- **Novelty distinction:** The selector and data share one state, unlike B01; exact alias check must separate their generated stream sets rather than assume names prove difference.
- **Closest local external:** H-AUTONOMOUS-RECURRENCE; EXT-010; EXT-040; EXT-050; EXT-051; mruckman1 generator dossier
- **Admission:** proposed; prior mathematical-generator scope unresolved; no target admission
- **Priority:** 5
- **Estimated cost:** Design/source comparison first. Synthetic implementation pilot ≤120 CPU seconds; full parameter scan cost must be preflighted separately, no automatic target run.
- **Sources:** 
  - https://www.injoit.org/index.php/j1/article/view/615
  - https://github.com/mruckman1/k4_cipher/blob/e4912152555f635c35e73fe454a8302a98a5902f/docs/shift_sequence_hypotheses.md

<a id="n100-070"></a>
## N100-070 — Majority-clocked register stream

**Draft reference:** `B04` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Use binary shift registers of lengths 3,4,5, with recurrences x[t+3]=x[t+1] xor x[t], y[t+4]=y[t+1] xor y[t], z[t+5]=z[t+2] xor z[t]. State index0 is the outgoing bit; a clock shifts toward index0 and appends the recurrence bit. At each tick, inspect their middle state bits; advance exactly those equal to the majority, then output xor of their outgoing bits. Convert consecutive emitted bits to MSB-first5-bit values reduced mod26; use AZ additive C_i=P_i+K_i mod26, with no additional alphabet or sign search.
- **Bounded test:** All 7×15×31=3255 nonzero initial-state tuples; fixed middle-bit indices1,2,2. First reproduce the generator and round-trip fresh synthetic97-letter plants; compare exact generated shift streams against all recovered external banks before target admission.
- **Controls:** Every possible three-clock-bit pattern; independent state transition; lockstep vs majority stepping fault fixtures. Include uniform ciphertext nulls and all24 fixed clue checks only after the source/synthetic gate.
- **Identifiability limit:**  A stream matching clues is only compatibility; report all full decryptions and complete parameter equivalence classes. Finite generators may alias prior short-period models. No source/creator evidence selects this generator.
- **Novelty distinction:** Irregular state clocking changes the state transition rather than only choosing output, separating it from a lockstep Geffe combiner and fixed-step LFSRs.
- **Closest local external:** H-AUTONOMOUS-RECURRENCE; EXT-010; EXT-040; EXT-050; EXT-051; mruckman1 generator dossier
- **Admission:** proposed; prior mathematical-generator scope unresolved; no target admission
- **Priority:** 5
- **Estimated cost:** Design/source comparison first. Synthetic implementation pilot ≤120 CPU seconds; full parameter scan cost must be preflighted separately, no automatic target run.
- **Sources:** 
  - https://cacr.uwaterloo.ca/hac/about/chap6.pdf
  - https://github.com/mruckman1/k4_cipher/blob/e4912152555f635c35e73fe454a8302a98a5902f/docs/shift_sequence_hypotheses.md

<a id="n100-071"></a>
## N100-071 — Nonlinearly observed single register

**Draft reference:** `B06` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Use s[t+13]=s[t+4] xor s[t+3] xor s[t+1] xor s[t]. Output s0 xor (s1 and s3) xor (s5 and s8 and s12). Convert consecutive emitted bits to MSB-first5-bit values reduced mod26; use AZ additive C_i=P_i+K_i mod26, with no additional alphabet or sign search.
- **Bounded test:** All8191 nonzero seeds; no free Boolean function fitting. First reproduce the generator and round-trip fresh synthetic97-letter plants; compare exact generated shift streams against all recovered external banks before target admission.
- **Controls:** Exhaustive Boolean truth table and tiny-register oracle; linear observer as known-overlap control. Include uniform ciphertext nulls and all24 fixed clue checks only after the source/synthetic gate.
- **Identifiability limit:**  A stream matching clues is only compatibility; report all full decryptions and complete parameter equivalence classes. Finite generators may alias prior short-period models. No source/creator evidence selects this generator.
- **Novelty distinction:** Nonlinear observation of linear state is globally different from EXT-010's direct register output; must compare exact previous generator banks.
- **Closest local external:** H-AUTONOMOUS-RECURRENCE; EXT-010; EXT-040; EXT-050; EXT-051; mruckman1 generator dossier
- **Admission:** proposed; prior mathematical-generator scope unresolved; no target admission
- **Priority:** 5
- **Estimated cost:** Design/source comparison first. Synthetic implementation pilot ≤120 CPU seconds; full parameter scan cost must be preflighted separately, no automatic target run.
- **Sources:** 
  - https://cacr.uwaterloo.ca/hac/about/chap6.pdf
  - https://github.com/mruckman1/k4_cipher/blob/e4912152555f635c35e73fe454a8302a98a5902f/docs/shift_sequence_hypotheses.md

<a id="n100-072"></a>
## N100-072 — Quadratic-character sequence

**Draft reference:** `B09` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** For prime257, emit bit1 when n is a nonzero quadratic residue, otherwise0; use n increasing cyclically. Convert consecutive emitted bits to MSB-first5-bit values reduced mod26; use AZ additive C_i=P_i+K_i mod26, with no additional alphabet or sign search.
- **Bounded test:** All257 phases of this fixed sequence; no fitted primes or character maps. First reproduce the generator and round-trip fresh synthetic97-letter plants; compare exact generated shift streams against all recovered external banks before target admission.
- **Controls:** Euler-criterion and explicit-square-set implementations agree; zero-residue convention tested. Include uniform ciphertext nulls and all24 fixed clue checks only after the source/synthetic gate.
- **Identifiability limit:**  A stream matching clues is only compatibility; report all full decryptions and complete parameter equivalence classes. Finite generators may alias prior short-period models. No source/creator evidence selects this generator.
- **Novelty distinction:** Number-theoretic character sequence differs from finite linear/polynomial recurrence output; EXT-040 mathematical-key inventory must be checked before admission.
- **Closest local external:** H-AUTONOMOUS-RECURRENCE; EXT-010; EXT-040; EXT-050; EXT-051; mruckman1 generator dossier
- **Admission:** proposed; prior mathematical-generator scope unresolved; no target admission
- **Priority:** 5
- **Estimated cost:** Design/source comparison first. Synthetic implementation pilot ≤120 CPU seconds; full parameter scan cost must be preflighted separately, no automatic target run.
- **Sources:** 
  - https://doc.sagemath.org/html/en/reference/rings_standard/sage/arith/misc.html
  - https://github.com/mruckman1/k4_cipher/blob/e4912152555f635c35e73fe454a8302a98a5902f/docs/shift_sequence_hypotheses.md

<a id="n100-073"></a>
## N100-073 — Rudin–Shapiro overlap-parity stream

**Draft reference:** `B10` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** At index n, output parity of the number of overlapping11 patterns in binary n. Convert consecutive emitted bits to MSB-first5-bit values reduced mod26; use AZ additive C_i=P_i+K_i mod26, with no additional alphabet or sign search.
- **Bounded test:** Offsets0..96 only; fixed increasing indexing and bit convention. First reproduce the generator and round-trip fresh synthetic97-letter plants; compare exact generated shift streams against all recovered external banks before target admission.
- **Controls:** Direct bit-pattern counter versus two-state recurrence on n; overlapping111 must count two matches. Include uniform ciphertext nulls and all24 fixed clue checks only after the source/synthetic gate.
- **Identifiability limit:**  A stream matching clues is only compatibility; report all full decryptions and complete parameter equivalence classes. Finite generators may alias prior short-period models. No source/creator evidence selects this generator.
- **Novelty distinction:** Pattern-overlap parity is distinct from Fibonacci/LCG and a constant's digits; it may still be in uninspected mathematical-key banks.
- **Closest local external:** H-AUTONOMOUS-RECURRENCE; EXT-010; EXT-040; EXT-050; EXT-051; mruckman1 generator dossier
- **Admission:** proposed; prior mathematical-generator scope unresolved; no target admission
- **Priority:** 5
- **Estimated cost:** Design/source comparison first. Synthetic implementation pilot ≤120 CPU seconds; full parameter scan cost must be preflighted separately, no automatic target run.
- **Sources:** 
  - https://oeis.org/A020985
  - https://github.com/mruckman1/k4_cipher/blob/e4912152555f635c35e73fe454a8302a98a5902f/docs/shift_sequence_hypotheses.md

<a id="n100-074"></a>
## N100-074 — Paperfolding recursion stream

**Draft reference:** `B11` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Generate the regular binary paperfolding word by w_next=w,1,reverse(complement(w)), starting empty. Convert consecutive emitted bits to MSB-first5-bit values reduced mod26; use AZ additive C_i=P_i+K_i mod26, with no additional alphabet or sign search.
- **Bounded test:** Offsets0..96, fixed recursion and no rotated physical-grid story. First reproduce the generator and round-trip fresh synthetic97-letter plants; compare exact generated shift streams against all recovered external banks before target admission.
- **Controls:** Recursion versus arithmetic-index definition; boundary lengths2^k−1 and complement/reversal negative fixtures. Include uniform ciphertext nulls and all24 fixed clue checks only after the source/synthetic gate.
- **Identifiability limit:**  A stream matching clues is only compatibility; report all full decryptions and complete parameter equivalence classes. Finite generators may alias prior short-period models. No source/creator evidence selects this generator.
- **Novelty distinction:** The folding recursion is a generator relation, not evidence that the sculpture must physically fold. Exact prior sequence-library overlap unresolved.
- **Closest local external:** H-AUTONOMOUS-RECURRENCE; EXT-010; EXT-040; EXT-050; EXT-051; mruckman1 generator dossier
- **Admission:** proposed; prior mathematical-generator scope unresolved; no target admission
- **Priority:** 5
- **Estimated cost:** Design/source comparison first. Synthetic implementation pilot ≤120 CPU seconds; full parameter scan cost must be preflighted separately, no automatic target run.
- **Sources:** 
  - https://oeis.org/A014577
  - https://github.com/mruckman1/k4_cipher/blob/e4912152555f635c35e73fe454a8302a98a5902f/docs/shift_sequence_hypotheses.md

<a id="n100-075"></a>
## N100-075 — Self-describing run-length stream

**Draft reference:** `B12` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Generate the standard Kolakoski sequence on{1,2} from seed122, whose entries give its successive run lengths; subtract1 to obtain bits. Convert consecutive emitted bits to MSB-first5-bit values reduced mod26; use AZ additive C_i=P_i+K_i mod26, with no additional alphabet or sign search.
- **Bounded test:** Offsets0..96; generation must be independently specified and checked against public prefix before any target. First reproduce the generator and round-trip fresh synthetic97-letter plants; compare exact generated shift streams against all recovered external banks before target admission.
- **Controls:** Run-length re-encoding of the generated prefix, sufficient trailing context, and incorrect seed/boundary controls. Include uniform ciphertext nulls and all24 fixed clue checks only after the source/synthetic gate.
- **Identifiability limit:**  A stream matching clues is only compatibility; report all full decryptions and complete parameter equivalence classes. Finite generators may alias prior short-period models. No source/creator evidence selects this generator.
- **Novelty distinction:** The self-describing run condition is distinct from linear feedback and fixed substitution morphisms; no claim that the underlying mathematics is new.
- **Closest local external:** H-AUTONOMOUS-RECURRENCE; EXT-010; EXT-040; EXT-050; EXT-051; mruckman1 generator dossier
- **Admission:** proposed; prior mathematical-generator scope unresolved; no target admission
- **Priority:** 5
- **Estimated cost:** Design/source comparison first. Synthetic implementation pilot ≤120 CPU seconds; full parameter scan cost must be preflighted separately, no automatic target run.
- **Sources:** 
  - https://oeis.org/A000002
  - https://github.com/mruckman1/k4_cipher/blob/e4912152555f635c35e73fe454a8302a98a5902f/docs/shift_sequence_hypotheses.md

<a id="n100-076"></a>
## N100-076 — Greedy unvisited-integer stream

**Draft reference:** `B14` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Recamán recurrence: a0=0; a_n=a_(n−1)−n if nonnegative and unseen, otherwise a_(n−1)+n. Emit a_n mod26. Use AZ additive C_i=P_i+K_i mod26, without other alphabets or signs.
- **Bounded test:** Offsets0..96, fixed nonnegativity and complete history, no alternate recurrence after result. First reproduce the generator and round-trip fresh synthetic97-letter plants; compare exact generated shift streams against all recovered external banks before target admission.
- **Controls:** Independent set-history implementation and published prefix; duplicate-avoidance branch tests. Include uniform ciphertext nulls and all24 fixed clue checks only after the source/synthetic gate.
- **Identifiability limit:**  A stream matching clues is only compatibility; report all full decryptions and complete parameter equivalence classes. Finite generators may alias prior short-period models. No source/creator evidence selects this generator.
- **Novelty distinction:** Global visited-set dependence differs from finite-order affine generators and ciphertext occurrence clocks; prior mathematical-key libraries remain unresolved.
- **Closest local external:** H-AUTONOMOUS-RECURRENCE; EXT-010; EXT-040; EXT-050; EXT-051; mruckman1 generator dossier
- **Admission:** proposed; prior mathematical-generator scope unresolved; no target admission
- **Priority:** 5
- **Estimated cost:** Design/source comparison first. Synthetic implementation pilot ≤120 CPU seconds; full parameter scan cost must be preflighted separately, no automatic target run.
- **Sources:** 
  - https://oeis.org/A005132
  - https://github.com/mruckman1/k4_cipher/blob/e4912152555f635c35e73fe454a8302a98a5902f/docs/shift_sequence_hypotheses.md

<a id="n100-077"></a>
## N100-077 — Longest-suffix avoidance bitstream

**Draft reference:** `B15` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Use the Ehrenfeucht–Mycielski binary sequence from fixed seed010: extend by complement of the bit following the most recent earlier occurrence of the longest repeated suffix; freeze fallback and tie conventions from the source definition before implementation. Convert consecutive emitted bits to MSB-first5-bit values reduced mod26; use AZ additive C_i=P_i+K_i mod26, with no additional alphabet or sign search.
- **Bounded test:** Offsets0..96; no free seed or longest-suffix rule tuning. First reproduce the generator and round-trip fresh synthetic97-letter plants; compare exact generated shift streams against all recovered external banks before target admission.
- **Controls:** Independent naïve suffix search and suffix-tree implementation on a fixed prefix; tie and unseen suffix cases. Include uniform ciphertext nulls and all24 fixed clue checks only after the source/synthetic gate.
- **Identifiability limit:** The exact source definition is a prerequisite; until frozen this is specification-blocked, not executable. It is not a symbol-wise ciphertext feedback rule. A stream matching clues is only compatibility; report all full decryptions and complete parameter equivalence classes. Finite generators may alias prior short-period models. No source/creator evidence selects this generator.
- **Novelty distinction:** Adaptive avoidance of repeated bit contexts differs from fixed automatic sequences; historical or K4 use is unsupported.
- **Closest local external:** H-AUTONOMOUS-RECURRENCE; EXT-010; EXT-040; EXT-050; EXT-051; mruckman1 generator dossier
- **Admission:** Specification-blocked proposal: freeze exact longest-previous-suffix indexing, occurrence tie and seed convention against independent reference before any synthetic or target run. Prior mathematical-key scope unresolved.
- **Priority:** 5
- **Estimated cost:** Design/source comparison first. Synthetic implementation pilot ≤120 CPU seconds; full parameter scan cost must be preflighted separately, no automatic target run.
- **Sources:** 
  - https://oeis.org/A038219
  - https://github.com/mruckman1/k4_cipher/blob/e4912152555f635c35e73fe454a8302a98a5902f/docs/shift_sequence_hypotheses.md

<a id="n100-078"></a>
## N100-078 — Stern binary-index recursion stream

**Draft reference:** `B16` · **Type:** mechanism · **Status:** proposed, unrun; exact prior-art/inverse/control gates pending.

- **Mechanism:** Use Stern's diatomic sequence a0=0,a1=1,a_(2n)=a_n,a_(2n+1)=a_n+a_(n+1); shift by a_n mod26. Use AZ additive C_i=P_i+K_i mod26, without other alphabets or signs.
- **Bounded test:** Offsets0..96, fixed recurrence and initial values. First reproduce the generator and round-trip fresh synthetic97-letter plants; compare exact generated shift streams against all recovered external banks before target admission.
- **Controls:** Independent iterative and recursive definitions, powers-of-two identities and modular versus integer evaluation agreement. Include uniform ciphertext nulls and all24 fixed clue checks only after the source/synthetic gate.
- **Identifiability limit:** This is a simple mathematical-key hypothesis with low prior; reject if a prior numerical-key bank contains the exact generator/offset scope. A stream matching clues is only compatibility; report all full decryptions and complete parameter equivalence classes. Finite generators may alias prior short-period models. No source/creator evidence selects this generator.
- **Novelty distinction:** Index-recursive coupling differs from a fixed linear time recurrence, but known sequence generation is not invention.
- **Closest local external:** H-AUTONOMOUS-RECURRENCE; EXT-010; EXT-040; EXT-050; EXT-051; mruckman1 generator dossier
- **Admission:** proposed; prior mathematical-generator scope unresolved; no target admission
- **Priority:** 5
- **Estimated cost:** Design/source comparison first. Synthetic implementation pilot ≤120 CPU seconds; full parameter scan cost must be preflighted separately, no automatic target run.
- **Sources:** 
  - https://oeis.org/A002487
  - https://github.com/mruckman1/k4_cipher/blob/e4912152555f635c35e73fe454a8302a98a5902f/docs/shift_sequence_hypotheses.md
