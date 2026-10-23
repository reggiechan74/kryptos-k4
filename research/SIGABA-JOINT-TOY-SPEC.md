# SIGABA-JOINT-TOY-012: complete coupled inference benchmark

23 October 2026. Frozen before solver implementation or benchmark outcomes. Engineering only: no actual K4 ciphertext is read or evaluated. Toy success is not historical SIGABA validation or K4 success. Existing CSP-889 wirings/vectors remain unchanged.

## Synthetic machine definition

For alphabet size q and r in {3,5}, use r cipher and r control rotors, normal orientations, output before stepping. Each rotor is a declared synthetic permutation on 0..q-1; normal contact at position p is `(w[(x+p)%q]-p)%q`. Cipher traversal is forward; control traversal is backward through inverse contacts. Inputs are 0..min(4,q)-1. Collector maps an output x to x modulo 2r.

The static index bank has two permutation rotors on 0..2r-1, each independently positioned. A digit passes forward through both, then selects magnet `digit mod r`. Thus the index variable ranges only over mappings actually produced by the full (2r)^2 starting-position domain; identical maps retain all raw position aliases. The two-index toy bank is not the authentic five-index bank.

For each time step, OR the magnets selected by all control inputs; each selected cipher rotor advances minus one exactly once. Let f=floor(r/2), m=f+1, s=f-1 and notch=floor(q/2). On the pre-step control state, if rotor f is at notch, advance m minus one; if m was also at notch, also advance s minus one. Advance f minus one every step. Other control rotors are static. All r control starts and all r cipher starts are independent unknowns. No per-time independent mask choice, resets or inferred prefix state is allowed.

Deterministic wiring generation: Fisher–Yates driven by unsigned 32-bit LCG `state=1664525*state+1013904223 mod2^32`, one fixed seed derived from q,r,variant and bank. Record every actual permutation and generator seed in the fixture. Synthetic plaintext and planted starts use the same declared generator with separate seed; no tuning after results. Full messages have 97 symbols. The short observation mask is {2,3,6,9}; the long mask is {21..33,63..73}, zero-based. Values are synthetic q-symbol observations, never K4 ciphertext.

## Constraint solver

Unknowns: one control-start tuple, one reachable static-index mapping, and an independent cipher-start tuple. For each control start, derive its entire continuous digit-input sequence. Retain a bitset domain of reachable index maps. Partition it by each step's actual OR-mask, update cumulative cipher offsets, and filter the cipher-start domain at known positions. A fixed index map stays in the same domain along the whole path.

Merge branches only if time/control state, cumulative offsets **and the entire surviving cipher-start domain** agree; union the index-map domains. Do not merge unequal cipher-start domains, which would invent cross-correlated keys. Generate a cipher constraint by an exact meet-in-the-middle rotor-path join, producing a bitset of every matching independent cipher start. Cache by (offset vector, plaintext symbol, ciphertext symbol). Unknown gaps still advance all state.

Return disjoint compact relations between control starts, index-map classes and cipher-start sets, with exact raw alias multiplicities. These count parameter descriptions, not distinct schedules/plaintexts. Expand sorted full raw key tuples to a temporary stream for complete small-system comparisons; compare the actual bytes, not only a digest. Never require unique recovery when observations are ambiguous.

## Independent truth and cases

An independent contact-by-contact simulator computes raw index settings and continuous schedules without production tables or index classes. It exhaustively tries every independent cipher start for each raw control/index start and writes all compatible full tuples. It must agree with the complete relation, retain the planted key, and reject contradictory duplicate observations. Empty observations on q=2,r=3 must retain the whole domain. An adversarial relation-merge control must preserve correlation rather than take an unsound Cartesian union.

Complete truth cases: (q,r,variant,mask) = (2,3,0,short), (3,3,0,short), (3,3,1,long), (4,3,0,long), (5,3,0,long), (6,3,1,long), (2,5,0,long), (3,5,0,long). Also q=2,r=3 empty and inconsistent-observation controls. Full raw domain is q^(2r)*(2r)^2; no state sampling.

Scaling-only cases: (4,5,0,long), (6,5,0,long), (8,5,0,long). Run the complete solver domain within budget and independently validate every returned key up to the output cap; do not claim an independent exhaustive truth comparison where one was not run. These still use two toy index rotors and small alphabets. They cannot establish viability at the real 26-symbol/five-index-rotor domain.

Each declared benchmark runs in a separate process with a 600-second wall budget and 1-GiB measured resident-memory limit; a guard checks RSS and time during search. Parent watchdog stops a hung process shortly after the wall deadline. Temporary key-comparison output cap 256 MiB per stream; complete-result expansion cap 2,000,000 keys. Cache size is capped to 64 MiB; eviction changes performance only. Exact partial coverage and reasons must be saved on exhaustion; no incomplete case is a negative or full inference result.

## Gate and reporting

First require full-set equality on all completed truth cases, independent full-message planted roundtrips, exact alias counts and no-observation domain counts. Scaling must report controller/map domains covered, branch counts, predicate/cache work, ambiguity, elapsed time and peak RSS. A failure or cap is classified precisely; toy success never authorizes an actual K4 run. Before real-sized inference, separately freeze and validate the 26/10 contacts, five-index reachable map set, authentic continuous control transition and a real-sized synthetic resource test. No arbitrary subset of real keys is substituted for that gate.
