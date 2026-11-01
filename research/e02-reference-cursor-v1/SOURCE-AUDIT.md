# E02 / N100-045 — finite source and operator admission audit

**2026-11-01. Outcome: source/operator audit passes for a proposed finite pilot; NOT target-admitted, not tested on K4, no new experimental budget allocated.** No claim of worldwide novelty or likely success. No repository mutation. Parent must authorize the pilot separately.

## Exact frozen operator

`SOURCE-POLICY.json` was written before the source table calculation. It pins `data/controls.json` and precisely the K1, K2-as-inscribed and K3 plaintext fields; no corrected K2 substitution. Keep ASCII A–Z in those fields, concatenate in section order, append absent letters in AZ order. The resulting circular reference has 768 source letters plus **JZ**, hence N=770. Completion is an artificial catalog choice, not a Sanborn-supported clue.

Start q=0, scan forward including the current position. A(q) orders the 26 distinct letters by first encounter. For plaintext p, d(q,p) is its least nonnegative forward distance. Output AZ[index(A(q),p)] then set q=(q+d(q,p)+1) mod N. Decode c as A(q)[index(AZ,c)] and make the same update. No alternative source, direction, start, reset, key, offset, padding or relabeling search. This is the frozen E02, not an E01 retune.

## Proof, framing and identifiability

Completion makes every A(q) a permutation. Rank decoding recovers one p, hence exactly the encryptor's next state; induction proves inverse agreement for all finite strings. Framing is one letter per letter, continuous state, known q0. Unknown source or q0 would be a different inference problem. This deterministic decoder has no fitted key; a readable output would not by itself establish historical intent.

There are 746 distinct alphabets across 770 positions. All positions are reachable: selecting the current reference symbol advances one position. Thus at least 746 reachable states are observationally distinguishable by an immediate input; **770 is not a proved minimized-state count**. Duplicate alphabets can still have different transition futures. Periodic/equivalent reference representations are a general degeneracy, not an additional search license.

## Finite difference witnesses (not target traces)

Initial alphabet is `BETWNSULHADIGCOFQYVPRMXKJZ`; initial emission by AZ input is `JANKBPMILYXHVEOTQUFCGSDWRZ`.

| Inspected scope | Difference / limitation |
|---|---|
| Local study060's exact 208 evolving-alphabet machines | All 208 initial emission maps differ; input set {A,B} separates every one. Both archived implementations emit before update. This proves global operator inequality, not disagreement on every possible finite ciphertext. |
| Matched-initial MTF/MTB, prefix reversal, head swap | Selecting B at q0 gives q1=1 and alphabet `ETWNSUBLHADIGCOFQYVPRMXKJZ`. MTF, prefix reversal and head swap leave the head B in place; MTB puts B last. None gives this row. This does not exclude every extended adaptive grammar. |
| Fixed-axis additive / Beaufort running-key or scalar autokey rows | q0 and q1 both map L→H, but B maps A then G. Distinct scalar-shift rows under common fixed bijective axes cannot intersect on one input. Therefore these two E02 rows cannot both belong to such a bank, even if shift selection uses history. State-dependent axes or arbitrary nonlinear tables are outside this proof. |
| Last-plaintext-letter-only bank, including E01's state semantics | Reference B at indices0 and9 gives reachable next states1 and10 with different alphabets. Same previous letter is insufficient to select the E02 row. This is not a claim about unbounded-history autokey models. |
| H-RECURRENCE-CLOCK / occurrence-stepped key schedules | Those use ciphertext-history distances or occurrence schedules for repeating-key shifts, not a fixed-reference next-occurrence rank. Scalar-row witness applies where axes are fixed; broader grammars require their own comparison. |
| EXT008 routed self-key; EXT047 earlier-text slider | Inspected scopes are routed modular key equations / earlier-text substring crib sliding and periodic-key pruning. No next-occurrence rank transducer identified. These statements are source-scope comparisons, not exhaustive algebraic non-equivalence to every route or book cipher. |
| EXT052 mruckman033b | Source has seven position/ciphertext-prefix selectors over a fixed keyword alphabet pool, default k=2..6, not a plaintext-following reference cursor. At most k output maps per configured model cannot reproduce E02's ≥746 distinguishable reachable maps over all input strings. Target-specific coincidences remain possible. |
| EXT034 markmnl; EXT051 matbalez | Primary markmnl summary explicitly scopes MTF/MTB and permits more general state machines outside its result. Broad adaptive-count/wheel descriptions do not prove exact E02 coverage or absence. Underlying uninspected grammars remain uncertainty, not a novelty certificate. |

Local source hashes and the complete finite table/witness certificate are in `STATIC-CERTIFICATE.json`. This audit constructed source tables and initial-map witnesses only; it did not run message encryption/decryption, recovery, target fitting or a synthetic batch. Archived programs were read, not imported or executed.

## Existing technical idea: next-occurrence book cursor

[RootRunners' Booking Key writeup](https://github.com/RootRunners/Nullcon-Goa-HackIM-2026-CTF-RootRunners-Official-Write-ups/blob/main/Crypto/Booking_Key/README.md) uses circular reference-text next occurrences. Its integer output is distance, with the cursor remaining on the selected occurrence and unknown starts searched. E02 instead emits the distinct-letter rank and advances past the occurrence with fixed start. They are not the same frozen transducer, but **the underlying next-occurrence book-cursor idea already exists**. Conditional on a known state, rank and valid distance are bijectively related by that state's first-occurrence table; rank coding is a representation change, while the update convention changes future state. This is an incremental construction, not an invented primitive. Blob b2dc5e39f52212169e00ea918556f1199b732d44 pins the inspected writeup; its URL uses mutable main.

Finite targeted web queries found no exact public K4 E02 implementation. Search absence is weak evidence and no guarantee that nobody tried it. See search receipt. Exact repeat evidence found later should halt admission.

## Exposure and provenance limitations

Only named K1/K2/K3 fields were selected from the shared fixture; its whole bytes were hashed, not printed. No K4 field was selected. A later web search unexpectedly displayed K4 ciphertext in a search-result snippet. Nothing from that snippet was extracted, transformed or used, and the source policy/table preceded it; **this audit is not fully blinded**. Public code comments also expose crib-related context. The primary sources were inspected as text only.

Source copies initially had one extra newline from artifact creation. This was removed, and all three resulting Git object IDs equal connector-reported blobs; the earlier unnormalized local source copy was not treated as byte-identical proof. No external code was executed.

## Minimal next pilot proposal — not run, not funded

1. Freeze an independent scan decoder/encoder and a position-index implementation; pin their hashes before validation. Compare all 770×26 one-step source cells, inverse maps and next states.
2. Exhaustive toy references over alphabets of sizes2 and3, raw lengths1..4, append missing symbols by alphabet order; all circular starts and messages of length0..3. Check both independent methods, round trip and final state. Explicitly include current-position, repeated-symbol and wrap/completion edge cases.
3. Preserve the catalog's blind-plant requirement: have a separate custodian prepare a small fixed 97-letter plant set with truth withheld until candidate output is frozen. Do not rename disclosed round trips as blind recovery. Fix quantity, seeds, scoring, mutations and negative-control acceptance criteria before any batch. Wrong-source controls are diagnostics, not a theorem that each must fail.
4. Stop on any disagreement, source-policy deviation or newly discovered exact duplicate. Require an independent proof/code check. Only then consider a separately allocated **single** fixed K4 decode with all 24 fixed clues, full inverse and no rescue variants. This report does not authorize that target step.

Suggested cap may remain the catalog's 60 CPU seconds, but no cap is allocated here and precise pilot counts/control design still need a freeze. No new framework is needed.
