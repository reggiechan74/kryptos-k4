# SIGABA literature and a finite exact-filter experiment

Research date: 2026-10-23. Repository reviewed at 03f77ff6707de30821904d614185ff992f1098ae. Research only: no repository writes, no external code execution, no paid access, no actual K4 evaluation.

## Decision

There is an applicable published *filter*, but no published result located that demonstrates complete inference for the repository's 13+11 separated known letters within 60 seconds and 1 GiB. The most useful next experiment is exact crib anchoring plus a short-crib selectivity/soundness test of Lasry's controller-consistency filter. It must not be described as reproducing his practical full-key attack or passing the original full-domain gate.

## Primary literature, assumptions and limitations

### Lasry, HistoCrypt 2019, sections 2.2–2.6

“A Practical Meet-in-the-Middle Attack on SIGABA,” pp. 41–49:
https://ep.liu.se/ecp/158/005/ecp19158005.pdf

The two phases meet on cipher-stepping sequences, not intermediate plaintext symbols. Phase 1 maps seven successive step masks to cipher settings matching eight consecutive known letters; phase 2 generates physically possible sequences from control/index settings. Additional crib letters or full-message statistics validate matches. Eight is a practical trade-off, not a strict lower bound: footnote 7 permits fewer with worse efficiency. Known rotor wirings are assumed; orders, orientations and starts may be unknown.

The full-key analysis estimates 2^60.2 work and approximately 80 GB for its per-partition hash table. The solved example in section 2.6 used an extra equal-start restriction, reducing phase-2 work to 2^41.3, and took days on a ten-core PC. Do not describe that example as an unrestricted full-key performance demonstration.

Application: either K4 crib contains eight consecutive letters, so “insufficient plaintext for MITM” would be wrong. Its resource estimates cannot simply be transplanted to the narrower fixed-layout repository domain; nevertheless, literal enumeration there still entails 26^5 × 66,058 ≈ 7.85×10^11 controller/map pairs. The paper supplies no 60-second complete-inference result for that domain.

### Lasry, Cryptologia 47(1), online 2021 / issue 2023

“Cracking SIGABA in less than 24 hours on a consumer PC”:
https://www.tandfonline.com/doi/full/10.1080/01611194.2021.1989522
Accessible author-publication copy, successfully read without authentication:
https://www.researchgate.net/publication/357104979_Cracking_SIGABA_in_less_than_24_hours_on_a_consumer_PC

Sections 4.3.2–4.3.3 provide the useful filter: identical collector-output digit sets must produce identical cipher-step masks because the index bank is static. For a cipher-path subgraph, intersect the possible-mask sets over every occurrence of each collector set; an empty intersection rejects that controller/subgraph pair. Surviving pairs still require physical index-setting verification. The filter is necessary, not sufficient.

The CSP-889 attack uses 100 consecutive known symbols and statistical ranking. Section 4.4.1 reports about 83.4% success near 24 hours on 64 cores; footnote 21 gives roughly 3 GB per worker. Sections 4.3.2–4.3.3 empirically require roughly 55–60 positions for reliable rejection and trim ten layers at each end. Those are experimental observations, not bounds applicable to short cribs.

Do not import scoring or trimming. Twelve within-crib transitions may offer little pruning.

### Stamp and Chan, Cryptologia 31(3), 2007, sections 4.1–4.2

“SIGABA: Cryptanalysis of the Full Keyspace”:
https://www.cs.sjsu.edu/faculty/stamp/papers/Sigaba2.pdf
Publisher record:
https://doi.org/10.1080/01611190701394650

The primary phase enumerates cipher settings and legal stepping paths through consecutive known plaintext; identical current states may be merged for this phase. With 30 possible masks and random matching probability 1/26, expected branching is 30/26, explaining why additional known letters do not automatically collapse all paths. The secondary phase must recover compatible controller/index settings. Their full-key analysis using 100 known letters estimates 2^86.7 work; their optional statistical improvement is not exhaustive.

The static index quotient is at most 10!/2^5 = 113,400 observable digit-to-magnet maps. The repository already enumerates its fixed-order reachable subset of 66,058 maps. Replacing that subset by the literature's larger unrestricted quotient is not a new speedup and would expand scope unless used only as a clearly identified necessary-condition relaxation.

Targeted searches located no primary publication demonstrating practical full CSP-889 SAT/SMT/CSP recovery from 24 scattered known letters. A generic SAT encoding remains an experiment, not a literature-supported tractability claim.

## What the repository measurements actually show

Reviewed:
- https://github.com/reggiechan74/kryptos-k4/blob/03f77ff6707de30821904d614185ff992f1098ae/research/SIGABA-DOMAIN-IDENTITY-FINDINGS.md
- https://github.com/reggiechan74/kryptos-k4/blob/03f77ff6707de30821904d614185ff992f1098ae/research/SIGABA-REAL-ADAPTER-FINDINGS.md
- https://github.com/reggiechan74/kryptos-k4/blob/03f77ff6707de30821904d614185ff992f1098ae/research/SIGABA-REAL-ADAPTER-SPEC.md
- https://github.com/reggiechan74/kryptos-k4/blob/03f77ff6707de30821904d614185ff992f1098ae/experiments/sigaba_real_adapter.py

Cached domain hashes advance the unknown prefix to index 17, but still produce no cipher predicate requests and complete no controller. A new cipher-only filter cannot prune that prefix if the existing recurrence insists on materializing it first. The dense fixture is independently blocked by many large cipher-domain payloads. Fixing one is not evidence that the other is solved.

## Original derivation: anchoring is exact under this particular domain

This is an engineering deduction from the pinned adapter, not a runtime claim from a paper.

Let q0 be the original controller start, h a persistent reachable index map, c0 the cipher-start vector, and Δ(q0,h;0→a) the signed, modulo-26 cipher displacement before the first observed position a.

Define ca = c0 + Δ(q0,h;0→a), coordinatewise modulo 26.

REAL-014 independently admits every c0 in the full five-dimensional torus. For each fixed (q0,h), this translation is a bijection. Therefore ca also ranges independently over the full torus. One may start the constraint solver at a=21 with ca as its cipher-domain variable, keep q0 as the enumerated controller variable, and obtain controller outputs at actual times 21 onward from the unchanged continuous controller schedule.

No controller inversion is required. No prefix index-owner frontier is needed. The unobserved prefix displacement can be computed lazily when a surviving h must be expanded back into original starts:

c0 = ca − Δ(q0,h;0→21).

The inverse displacement depends on h, so the returned compact relation must retain that dependence. It is incorrect to relabel one shared anchored cipher-start set as a shared original-start set for all owners. A symbolic back-translation map or per-owner reconstruction preserves the correlation.

This equivalence relies on unrestricted independent cipher starts. It does not automatically apply to common-letter starts, indicator-derived setup, restricted starting domains, resets, or other historical initialization hypotheses. It does not authorize resetting at the second crib. The controller and the same h continue through every intervening character.

## Recommended finite experiment

Priority: first prove exact anchoring and benchmark the unchanged full-domain fixtures. The selectivity diagnostic below is a possible subsequent experiment, not a replacement or parallel excuse to relax that gate.

Objective: establish whether the borrowed filter has useful selectivity on the unchanged short-crib regime, after validating exact anchoring. Do not attempt the full 2019 MITM or claim full-key recovery.

1. Freeze the experiment before outcomes. Retain the existing two synthetic ciphertexts, planted keys, exact observations and resource limits. Add only a separate diagnostic panel whose construction is deterministic and disclosed; it must not replace or ease either original gate fixture.

2. Correctness gate: on all existing complete q=2/3 fixtures, compare the full raw compatible-key stream of anchored and unanchored implementations after owner-dependent inverse translation. Include empty observations, one observation, a delayed first observation, two separated windows, multiple aliases, conflicting observations and a nonzero prefix crossing controller carry. Check the full relation, not only planted inclusion or counts.

3. Real-size diagnostic: construct the legal cipher-state DAG for the existing 13-letter observed block from the known synthetic planted anchor and a frozen deterministic wrong-anchor panel. Retain all paths using the original legal step masks, preserve actual state/edge identity, and discard only paths inconsistent with observed plaintext/ciphertext. This is a control experiment with supplied anchors, not discovery of unknown starts.

4. Apply the published necessary-condition filter to a frozen panel of original controller starts that includes the plants. Use actual controller time indices. Report collector-set repeat counts, rejected controller/DAG pairs, surviving pairs, runtime and peak RSS. Keep disconnected candidate subgraphs separate; pooling everything into universal per-layer mask sets can destroy selectivity. Do not mistake independently possible per-layer masks for a single realizable path.

5. Independent physical check: for the tested panel, compare the filter with reachable-map execution using the repository's 66,058 exact maps and raw aliases. Every physically feasible pair must survive. Add a deliberate equal-input/different-output contradiction case to prove rejection is active. A filter survivor need not have a reachable map.

6. For physically feasible local candidates, retain their actual cipher state, controller and h, propagate continuously through the gap, and apply the second observed block. Reconstruct original cipher starts and replay the complete synthetic ciphertext. Do not concatenate the cribs or inject invented plaintext in the gap.

7. Stop at the frozen resource cap with an honest diagnostic result if incomplete. Report filter false negatives (required zero), selectivity and verification work avoided. The original full-domain gate remains failed unless its original all-start/all-controller conditions and independent compatible-set validation actually complete. A successful planted diagnostic is not a substitute.

## Negative versus positive implications

- Exhaustive rejection by this necessary-condition filter, across every relevant anchor/subgraph and controller in a declared domain, supports a negative for that declared model. Rejection of a selected panel does not.
- A timeout is unresolved, not a negative.
- A surviving subgraph/controller combination is not yet a physical key. It needs a single reachable index map and a connected compatible trajectory.
- A local physical key is not a K4 solution. It must satisfy both windows with the same continuous machine, regenerate all ciphertext, and yield independently supportable plaintext.
- Statistical path pruning can help candidate discovery, but cannot produce an exhaustive exclusion.
- Neither literature nor these proposed controls resolves unknown wartime rotor wirings, historical initialization, other layouts, or whether SIGABA was used for K4.
