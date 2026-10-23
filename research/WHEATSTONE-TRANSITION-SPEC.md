# WHEATSTONE-TRANSITION-008: fixed-ring transition invariant

23 October 2026. Frozen before implementation and automated certificate replay. The invariant and possible ST witness were identified using already public crib data during source comparison; this is not a blind preregistration or an independent prediction.

## Historical and coverage audit

Use the independently published [MysteryTwister/CrypTool instructions and worked example](https://mysterytwister.org/media/challenges/pdf/mtc3-madness-04-wheatstone-01-en.pdf), April 2021, especially pages 2–3 and 7–10. They specify an outer 27-symbol plaintext ring (space plus A–Z), an inner 26-letter permutation, equal step counts, clockwise motion, repeated-letter replacement and an enciphered terminal space as an optional check. The external worked case is processed `MEQT_AT_DAWN_`, inner `SAMZEBNCDORFPGQTHUKIVJWYLX`, ciphertext `GNKJMZWZCBAIN`, with outer `_ABCDEFGHIJKLMNOPQRSTUVWXYZ` and initial pointers at space/inner index zero. A second worked reconstruction in [A Book on Classical Cryptography](https://www.cipherchallenge.org/wp-content/uploads/2022/09/A-Book-on-Classical-Cryptography-by-Madness.pdf), Unit 120 pages 382–385 (zero-based PDF pages), uses processed `SECRET_MESXSAGE_`, key `WBPHCQEDRAFUTGVSIXJYOKZNLM`, ciphertext `YEQORNCXFLHMRVGA`.

These are modern operational reconstructions, not newly recovered 1867 machine records. The IET and National Cryptologic Foundation establish historical context but not every operating convention. Wheatstone's original 1879 chapter was located in publisher metadata and a public first-page preview, not fully inspected. IACR's separate modern attack paper returned 403; Google Books' PDF returned 403; neither will be retried through another route. Public access failures must remain in the source receipt.

Pinned external `fe_wheatstone.py` already covers a finite dictionary of outer alphabets, all blank slots, reversals and an arbitrary inner permutation with a free inter-island phase. Its positive step expression is `((next-prev-1)%27)+1`. The source does not prove coverage of every outer permutation. The new theorem removes that remaining ring-label restriction. No dictionary sweep is rerun or counted as a new negative.

## Exact model and invariant

The formal model grants arbitrary fixed bijective outer and inner alphabets, all pointer starts and either fixed cyclic orientation through alphabet reversal. For distinct processed consecutive plaintext letters u,v, let d(u,v) be their fixed positive forward outer distance (1 through 26). Inner state updates by `q_next=q+d(u,v) mod26`; output is one shared inner permutation at the state. Unknown prefixes determine an unknown q, which cancels from equality tests.

For two occurrences of the same processed pair (u,v), `C_previous == C_next` must have the same truth value: output equality holds exactly when `d(u,v)=0 mod26`. This needs no alphabet recovery and is valid even if the actual fixed-distance function is granted independently for every ordered pair. It is not an invariant of arbitrary state-dependent stepping, changing alphabets or hidden moves.

Plaintext spaces are real outer symbols and produce ciphertext letters; they are not invisible state changes. The two observed letters in each tested adjacent pair must be adjacent processed symbols at their disclosed ciphertext positions. Repeated-letter substitution/insertion is lossy preprocessing: an encoder/decryptor roundtrip recovers the processed string, not necessarily the original English. The two ST pairs are not internally doubled letters, but any untracked preprocessing that shifts their global anchors or inserts a hidden space is outside the aligned certificate. No guessed spaces or prefix states will be inserted to obtain a contradiction.

## Frozen finite verification

Implement the historical reconstructed forward/inverse on processed strings. Verify both external worked vectors, repeated-cipher decoding (a full 26 inner steps), rejection of unprepared repeated plaintext, and independent tooth-by-tooth simulation. Validate continuous literal-crib plants with random outer/inner permutations and pointer starts. Retain exact machine states and processed/plaintext distinctions.

Prove the invariant symbolically as above, then exhaustively verify complete small unequal-ring systems (outer sizes 3–6, inner one fewer) across every outer/inner permutation, all ordered distinct letter pairs and inner states. No large K4 key enumeration is authorized or required. Find all repeated processed plaintext digrams within EASTNORTHEAST and check equality flags in the corresponding ciphertext. If a certificate rejects, stop without Berlin. Otherwise repeat jointly and report only necessary compatibility, not a solution.

One process, controls 120 seconds / 2,000,000 state-transition comparisons; actual certificate replay 5 seconds / all 24 public crib letters. Any cap exceeded is unresolved, not exhausted. Mutation and independently implemented certificate controls are required. No new alphabets, extra rotations, silent spaces, ring-size variants, routes or post-hoc Plett/Wadsworth parameter searches. A separate source audit must retain what is and is not established for those devices.
