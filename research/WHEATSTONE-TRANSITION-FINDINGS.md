# Wheatstone: source conventions and an arbitrary-ring certificate

23 October 2026. The direct aligned fixed-ring Wheatstone model is excluded for **arbitrary fixed outer and inner permutations**, not merely a selected dictionary of keys. A first-crib contradiction suffices; no K4 key search or Berlin evaluation was needed. The source audit also identifies what remains unverified about original operating procedures and other devices.

## What was sourced

The [MysteryTwister/CrypTool instructions](https://mysterytwister.org/media/challenges/pdf/mtc3-madness-04-wheatstone-01-en.pdf), April 2021, specify 27 plaintext positions including space, a 26-letter keyed inner ring, equal clockwise symbol-step counts, repeated-letter replacement and optional terminal-space encryption. The published MEQT_AT_DAWN_ example regenerates GNKJMZWZCBAIN. The same author's [book, Unit 120](https://www.cipherchallenge.org/wp-content/uploads/2022/09/A-Book-on-Classical-Cryptography-by-Madness.pdf) gives SECRET_MESXSAGE_ → YEQORNCXFLHMRVGA under its displayed key. Both external vectors pass. They are modern worked reconstructions by one author, not two independently authenticated historical-machine vectors.

[IET Archives](https://ietarchivesblog.org/2020/02/17/sir-charles-wheatstone-1802-1875-the-playfair-cipher/) and the [National Cryptologic Foundation](https://cryptologicfoundation.org/ncf-history/wheatstone-cryptograph-and-wheatstone-plett-cipher/) corroborate historical context and distinguish devices. They do not supply all operating details. The original 1879 chapter was located in publisher metadata/first-page preview, but not fully inspected. Several referenced publications were unavailable; the [source receipt](../sources/wheatstone-historical-conventions-2026-10-23.json) records each outcome. No 403 source was retried through an alternate route, and no downloaded third-party software was executed.

## Prior coverage versus the genuine gap

Pinned `fe_wheatstone.py` at `2db2722cc3f18c52d4d8369d7adc5a1db7e859d7` covers its finite generated outer alphabets, every blank slot, reversed alphabets, arbitrary inner labels and an unknown shift between the crib islands. Its positive step expression even allows 27 for an identical plaintext letter. The modern reversible procedure disguises such repeated plaintext letters instead; the distinction does not affect the distinct S→T transitions used here.

That source did not establish coverage of every outer permutation. Repeating its dictionary sweep would be duplicate work; a key-independent invariant removes that finite-domain restriction. All starts and fixed directions are harmless to the proof. No global-novelty claim is made, and third-party full sweep results were not freshly reproduced.

## The certificate

Let `o(P)` be the fixed outer coordinate and `q(C)` the coordinate in the fixed inner permutation. The forward distance `d(u,v)` between consecutive processed plaintext symbols depends only on the ordered pair. The inner pointer changes by that same distance:

`q(C_next) = q(C_previous) + d(u,v) mod26`.

Since the inner alphabet is a permutation, the adjacent ciphertext letters are equal exactly when the displacement is zero modulo 26. Thus all occurrences of one ordered plaintext pair must agree on whether the ciphertext pair is repeated. This holds even in a relaxation granting an arbitrary fixed displacement to every ordered plaintext pair, without requiring those displacements to be realizable as one outer ring.

| Processed positions | Plaintext pair | Ciphertext pair | Equality |
| --- | --- | --- | --- |
| 24–25 | ST | RV | Different |
| 33–34 | ST | SS | Equal |

The same S→T move cannot satisfy both. Unknown prefix and gap states cancel from the equation. No alphabet, starting phase, direction or free inter-island offset can fix the contradiction. [Mechanical certificate](../results/WHEATSTONE-TRANSITION-008.json). This is an analytical exclusion, not an enumeration of factorially many independent hypotheses.

The [independent JavaScript verifier](../experiments/wheatstone_transition_oracle.mjs) assigns each ordered pair an arbitrary displacement domain 0–25. ST's observations require both a nonzero value and zero, leaving an empty domain. It uses neither the ring simulator nor its pointer arithmetic. [Independent receipt](../results/WHEATSTONE-TRANSITION-008-independent.json).

## Correctness and chronology

The [protocol](WHEATSTONE-TRANSITION-SPEC.md) was frozen at `76b0ab0`, with a pre-implementation rotation-quotient annotation at `a1d8739`. The invariant and possible witness were derived using already public crib data during source review; this is honestly recorded, not called blind prediction. Controlled code was committed at `2773fba` before automated K4 replay.

[Controls](../results/WHEATSTONE-TRANSITION-008-controls.json) include both published forward/inverse vectors, independent tooth-by-tooth simulation, a repeated-cipher case requiring a full 26 inner steps, rejection of unprepared repeated plaintext, and 24 continuous literal-crib plants with arbitrary outer/inner permutations and pointer starts. Every plant roundtrips and satisfies the invariant; flipping a repeated-cipher equality at one ST occurrence creates a rejecting mutation.

Complete cyclic-order representatives for small rings of sizes 3–6 versus 2–5 give 443,976 state-transition comparisons. Rotating either entire ring only relabels a pointer coordinate; represented permutation counts and explicitly enumerated representatives remain separate in the receipt. Naive complete size-3/4 systems independently check that reduction. No random sample is used as a proof of the full key domain.

## Limits: spaces, normalization and authentic variants

The inverse reconstructs the **processed stream**, not necessarily original spelling: replacing a repeated letter with Q or inserting X is lossy. Spaces occupy outer-ring positions and emit ciphertext letters. They are not silently advanced without output. The certificate requires both observed ST pairs to be adjacent processed symbols aligned with those disclosed ciphertext positions. Untracked inserted spaces/letters or different anchor interpretation are outside that assumption; no universal preprocessing exclusion follows.

The proof does not exclude state-dependent extra revolutions, changing alphabets, hidden moves, an outer route/substitution, or every device called Pletts/Wadsworth. The book describes Pletts' mixed-outer-ring extension, and the invariant covers that fixed-ring abstraction; full authentic Plett operating conventions were not independently recovered or validated. Wadsworth's different ring sizes and symbol inventory were not folded into this experiment. An exact historical procedure and external reference vectors remain the gate for a materially different machine, rather than arbitrary new gearing or invisible spaces selected to fit K4.
