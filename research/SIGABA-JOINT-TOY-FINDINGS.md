# Coupled SIGABA inference: complete toy solver and scaling boundary

23 October 2026. Engineering progress only: **zero actual K4 evaluations**. A coupled constraint solver now retains a shared reachable index mapping, continuous control state and independent cipher starts. Ten complete synthetic truth comparisons agree byte for byte. Real-sized historical-machine inference remains unvalidated; toy recovery is not a K4 decoding.

## The implemented constraint formulation

The [frozen protocol](SIGABA-JOINT-TOY-SPEC.md) declares synthetic rotor permutations, collector, pulse contacts, carry timing, initial domains and observation masks. Machines have three or five cipher/control rotors, small q-symbol alphabets, and two static index rotors on 2r contacts. Raw index settings are grouped only when they induce the same full digit-to-magnet mapping; every original position alias is retained. This is an exact reachable domain, not every mathematically balanced function.

For each complete control-start tuple, the solver computes the continuous sequence of collector inputs. Each live relation contains a domain of index-map classes, cumulative cipher-wheel offsets, and a bitset of every surviving independent cipher start. A known input/output observation filters that bitset using an exact split rotor-path meet-in-the-middle predicate. Each subsequent control output partitions the same index domain by its actual OR-mask; selected cipher wheels advance once. The control counter runs through every unknown prefix/gap character, and output occurs before stepping.

Branches merge only when both their accumulated offsets **and full cipher-start domains** agree. Their index-map domains may then be united safely. Merging only marginal domains would invent false index/cipher combinations. No per-letter free masks, guessed gap states or crib resets are used. Control starts are still exhaustively enumerated, rather than solved as symbolic variables; this remains a scaling cost.

Soundness follows because every retained index map determines its actual mask history and each cipher predicate is exact. Completeness follows because all initial domains are present, mask partitions exhaust each reachable index domain, predicates remove exactly inconsistent starts, and correlation-preserving merging neither loses nor invents assignments. Final compact relations are disjoint in (control start, index class); raw aliases are expanded with exact multiplicities. Counts are raw parameter descriptions, not distinct schedules, plaintexts or independently executed decryptions.

## Independent verification and ambiguity

The [independent simulator](../experiments/sigaba_joint_toy_oracle.py) uses direct physical contact arithmetic, raw index positions and exhaustive cipher-start loops. It does not import production tables, index classes or predicate code. Complete sorted compatible-key streams were written independently and compared as actual bytes, not merely counts or cryptographic hashes. Frozen fixtures and compact solution relations allow regeneration without committing large temporary expansion files.

Completeness comparisons cover all states of each pinned fixture, not all possible rotor wirings. All ten declared truth/control cases agree, including empty observations, inconsistent observations, sparse masks and long masks at zero-based positions 21–33 and 63–73. These are synthetic values at the public clue-mask geometry, not actual K4 ciphertext or literal English clues in a q<26 alphabet. Full-message planted encryption/decryption roundtrips pass. Truth inclusion does not require unique recovery: complete compatible sets range from zero to 807,003 raw keys in the truth cases.

For q<=4 the pulse inputs cover the entire small alphabet, so a permutation control bank presents the same full contact set regardless of its start. Controller ambiguity in those fixtures is structural, not recovered control information. The q=2 cipher rotors also have strong position aliases. These deliberately frozen cases are useful completeness/ambiguity tests but cannot calibrate real-machine discrimination. The deterministic LCG fixtures are reproducible engineering inputs, not an independent linguistic corpus or statistical null ensemble.

## Complete benchmark outcomes

All cases use a separate process, 600-second wall guard, 1-GiB measured-RSS guard and 64-MiB accounted predicate-cache budget. Guards are sampled measurements, not an OS hard allocation guarantee. A parent watchdog bounds a hung worker. Each temporary comparison stream is capped at 256 MiB and two million expanded keys. Exhaustion is unresolved, never a negative.

| Case | q / rotors | Observation mask | Inference | Exact raw fits | Validation | Seconds | Peak MiB |
| --- | --- | --- | --- | ---: | --- | ---: | ---: |
| 0 | 2 / 3 | short | complete | 2,304 | complete truth: identical bytes | 0.012 | 19.9 |
| 1 | 3 / 3 | short | complete | 1,458 | complete truth: identical bytes | 0.029 | 20.0 |
| 2 | 3 / 3 | long | complete | 1,701 | complete truth: identical bytes | 0.124 | 20.1 |
| 3 | 4 / 3 | long | complete | 15,360 | complete truth: identical bytes | 0.480 | 20.0 |
| 4 | 5 / 3 | long | complete | 12 | complete truth: identical bytes | 0.854 | 20.1 |
| 5 | 6 / 3 | long | complete | 2 | complete truth: identical bytes | 1.681 | 20.3 |
| 6 | 2 / 5 | long | complete | 102,400 | complete truth: identical bytes | 1.451 | 20.8 |
| 7 | 3 / 5 | long | complete | 807,003 | complete truth: identical bytes | 15.462 | 23.2 |
| 8 | 2 / 3 | empty | complete | 2,304 | complete truth: identical bytes | 0.008 | 19.9 |
| 9 | 2 / 3 | inconsistent | complete | 0 | complete truth: identical bytes | 0.003 | 19.9 |
| 10 | 4 / 5 | long | complete | 12,582,912 | output_budget_unresolved | 3.968 | 43.6 |
| 11 | 6 / 5 | long | complete | 1 | returned keys checked | 43.844 | 120.0 |
| 12 | 8 / 5 | long | unresolved | unresolved | wall_budget_unresolved | 600.005 | 104.4 |

The q=4 five-wheel solver completed compact inference but could not independently expand all 12,582,912 compatible keys under the frozen output cap. That is a validation-output boundary, not an inference timeout or a passed scaling gate. The q=6 five-wheel case completed all 7,776 control starts, retained the planted raw key uniquely under this toy model, and independently checked its observation constraints. Its 6,046,617,600 raw descriptions were represented by exact relations, not billions of independently executed decryptions; a full independent exhaustive truth run was not performed at that size.

The q=8 five-wheel case reached the wall budget after 600.005 seconds and completed 5080 of 32768 control starts. Its completed prefix accounts for 16,646,144,000 raw parameter descriptions algebraically; it is not that many independently executed decryptions. No fits were found in that completed prefix, while the full key count and remaining domain are **unresolved**. The peak measured RSS was 104.4 MiB. It built 1,552,615 predicates and evicted 1,537,195 cache entries: dense-predicate rebuilding/eviction is an observed bottleneck. The planted key was not in completed coverage, so non-recovery is not an implementation failure or a full-domain negative.

The [summary](../results/SIGABA-JOINT-TOY-012.json) records exact completed-controller coverage, partial lower bounds where relevant, alias domains, branch/predicate/cache work, source hashes, time and measured peak RSS. Original per-case receipts remain separate under [results/sigaba-joint-toy](../results/sigaba-joint-toy). No parameter, wiring or cap was retuned to repair an unfavorable outcome.

## Why this does not pass the real-machine gate

The authentic adapter would need the existing 26-symbol/five-cipher/five-control mechanism, ten-contact **five-index-rotor** reachable domain, actual collector/magnet tables, real input contacts and independently validated carry/contact conventions. Toy index banks contain only two rotors and at most 100 raw index settings, whereas the earlier fixed historical wiring quotient has 66,058 map classes from 100,000 raw starts. The toy notch is floor(q/2); merely setting q=26 would give 13, not the authentic O contact at 14. Real F–I pulse inputs and collector/magnet tables also differ. The old twelve external known-answer tests and existing real-machine code remain intact; this solver has not yet been integrated with them.

At real dimensions, one dense cipher-start bitset has 26^5 bits, about 1.49 MB payload, before Python/container overhead. A 64-MiB cache would hold only roughly 45 such entries. Enumerating 26^5 control starts and materializing many differently filtered cipher domains can dominate even with a shared index domain. This is a representation/cost warning, not a lower bound or proof that a better solver cannot work. No real-sized synthetic protocol or actual K4 key slice was substituted for a failed or incomplete gate.

There is a specific exact reuse opportunity before changing the model. If `D_delta(p,c)` is the set of independent initial cipher starts satisfying one observed pair at accumulated offsets delta, then `D_delta(p,c) = {s : s+delta belongs to D_0(p,c)}` on the coordinate torus `(Z/qZ)^r`. Rotor contact positions depend only on initial position plus accumulated offset. Thus the current repeated meet-in-the-middle builds can in principle be replaced by coordinate-wise cyclic translations of zero-offset predicates. This is an algebraic identity, not a measured speedup. A base predicate needs to be built only for each observed symbol pair; translating a dense bitset still has a cost, and large live domains/controller enumeration remain. A separate frozen prototype should compare every translated predicate with direct complete tiny-state truth, then rerun the same bounded synthetic cases. No such translation backend or extra benchmark was executed in this batch.

A further reasoned representation would retain factorized rotor-path table relations and symbolic control-start variables, or a decision-diagram/constraint backend, instead of enumerating every controller and storing a dense cipher-start bitset for each branch. Index positions could likewise remain coupled composition variables rather than flattening all reachable maps. Such a representation may reduce the materialization/caching costs but must preserve the correlations tested here; its viability is **unproved and unimplemented**. It needs its own complete toy comparisons and resource protocol before any real-sized synthetic test, then external-reference validation before K4.

The algorithmic frontier is therefore narrower: a working complete coupled toy solver exists, but sound scaling and an authenticated real-sized adapter remain missing. K4 remains unsolved, and no full SIGABA exclusion or positive K4 lead follows.


## Subsequent engineering replication — 23 October 2026

[Exact torus predicate reuse](SIGABA-TORUS-FINDINGS.md) uses the same thirteen fixtures and original resource caps. It resolves the q=4 complete-output comparison using independent compact canonical sets, while preserving the original receipts and their historical limitations. Consult the later report for measured scaling outcomes; no actual K4 evaluation was added.
