# Item 6: frozen dynamic tree, nonlinear geometry and IPA-derived key pilots

24 October 2026 UTC, before new model scoring. Our exploratory rules, not Sanborn evidence. No Site change, item 7, free wiring, adaptive operator/phase/notation expansion, or language score.

## Prior scope and exact distinction

TREE-STATE-SUPPORT-006 proves contradictions for the old fixed geometry/Morse trees with fixed subtree label rotations, even granting arbitrary initial labelings. Here T changes topology by standard splaying. The old feature-rank/base invariance only concerns numerical order; old 35-bit feedback rotates then XORs, and RADIX-FEEDBACK covers first-order affine updates of the modulo-26 key. Here G keeps a nonlinear full 35-bit state. IPA-free-map models transform plaintext and assume conditional offsets; here I leaves English intact and uses an already sourced pronunciation stream only as key material. Known public phrases are not independent secret-key evidence.

## T: access-splayed search tree

Initial node order is either AZ or ascending frozen full geometry code (unique code, no retuned weights). Rotate that label list by seed s=0..25, then recursively choose the floor median to build a balanced binary tree. Every node bears one letter. Output the node's zero-based PREORDER rank in AZ or KRYPTOS coordinates. Encrypt by finding the plaintext node; decrypt by selecting ciphertext rank in current preorder. After output, splay the accessed node to root using bottom-up zig, zig-zig, zig-zag rotations. Full state continues through all 97 characters. No additional direction or traversal choice. 2 orders ×26 seeds ×2 output alphabets =104 raw models. Each fixed state is a 26-letter permutation; shared deterministic update proves inverse by induction. Variable paths are internal, not unframed bit ciphertext.

## G: full-width geometry ARX feedback

Reuse unchanged 35-feature binary codes and order, mask M=2^35−1. Seed S=code(letter), all 26 letters. At each letter use k=S mod26, C=P+k or C=k−P in AZ or KRYPTOS coordinates. AFTER output, choose fixed feedback source T=P or C, then update S=(rotl35(S,1)+(S XOR code(T))) AND M. Rotation is exactly one; no rotation sweep, changing bases, extra constants or fitted masks. Both addition carries and rotation stay in the 35-bit state. 26×2 alphabets×2 equations×2 sources=208 raw descriptions. The state update need not be invertible: causal encryption/decryption starts with the same seed, recovers the same P/C and advances identically. Show a structural state-residue counterexample to a first-order modulo-26 affine reduction, rather than claiming all nonlinear methods novel.

## I: source-fixed pronunciation-derived running keys

Only the already sourced Cambridge US phrases from the existing fixture: normalized EAST+NORTHEAST `iːstnɔːrθiːst` and BERLIN+CLOCK `bɝːlɪnklɑːk`. Existing source normalization removes slash/stress/dot/space only; retains length marks and IPA glyphs. Encode literal UTF-8 bytes; each byte modulo26 is a key value. Both phrases separately, every cyclic byte phase, AZ/KRYPTOS, addition/true Beaufort. One byte per English letter, continuous from position 1; English is never respelled or expanded. Exactly 4*(UTF8_length(first)+UTF8_length(second)) raw descriptions, calculate lengths without model scoring. This is an explicit modern numerical serialization hypothesis, not claimed as authenticated 1990 notation. It does not solve arbitrary English pronunciation/spelling inversion. Do not invent an IPA A–Z codec or treat phonetic glyphs as Latin aliases.

Compare actual key periods/streams with prior unrestricted period1..12 coverage and mark any inherited overlap; no duplicate negative claim. All phases of a key are descriptions, not independent evidence. The phrase choices come from public clues and cannot be promoted as an independently recovered key. New Cambridge requests for other keywords returned403; do not retry them or bypass that boundary; those keywords are not used.

## Controls, selection and budgets

Before K4: independently implement T with nested trees/path rotations and G with bit-list rotation/ripple addition; I's UTF-8 serializer checked by a separate code-point encoder. All raw models must roundtrip unrelated odd/even/empty messages and agree with references. Validate T's permutation across states, mutation of update timing and a topology change witness; G boundary/carry and same-key-residue/different-next-residue witnesses; all 26 symbols and long-prefix/gap continuity.

24 literal-crib plants, 8 per family: choose evenly spaced indices floor(j*(N−1)/7), j=0..7, from the deterministic domain. Fixed 97-letter pangram with public windows. Run FULL combined selector for every plant, keep all compatible settings/plaintexts, require true setting retained and full reencryption, never infer uniqueness from planted inclusion. Compare full candidate sets with independent reference selector. No reset at21/63 and no concatenated crib islands.

Actual: decrypt every model fully from position1, deduplicate output plaintexts, retain all first-crib fits then exact Berlin checks with unchanged model; no partial score. No fit licenses declaring a solution. If all-24 fits exist, stop for ambiguity/independent evidence assessment; do not add variants. 199 histogram-preserving shuffles with seed260024 rerun the entire selector to describe whole-family exact-fit events; no partial-match promotion or significance claim for a negative actual result.

Control stage180seconds, actual30seconds, null panel180seconds, each512MiB RSS. Budget checks between models; stop unresolved on exhaustion, never call timeout a rejection. Freeze source hashes and record original/replay UTC timestamps separately. Tests in both supported Python versions. Publish validated work under existing authorization, then stop before item7. Broader topology/initial-state/feature/IPA mechanisms remain untested.
