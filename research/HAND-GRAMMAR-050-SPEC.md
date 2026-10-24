# Hand-operation grammar 050 — finite depth-three proposal for audit

Local only, queued after 048/049 inside existing family 7. Hand-executable does not imply unrestricted keys are searchable or establish a creator-selected construction.

Data: canonical 97 cipherletters/all 24 English positions, unchanged. Work entirely in the fixed KRYPTOS alphabet coordinates. Literal independently selected inventory: KRYPTOS, PALIMPSEST, ABSCISSA. No thematic keyword expansion. Grammar primitives decode an input 97-stream to an output 97-stream:

- Six columnar permutations: standard row-major ragged keyword columns, stable A–Z keyword sorting with original-column tie order, read columns in sorted order; include each exact inverse. No padding or missing letters.
- Twenty-two skip permutations: for steps s=2..12 include indexp(i)=s×i mod 97 and each modular inverse step; fixed start 0. Prime 97 makes them bijective. Step 1 identity is not an extra primitive. No character is discarded.
- One reversalp(i)=96−i.
- Nine arithmetic maps: each of the three literal keys repeated at position 1, with explicit input x/output y maps y=x+K, y=x−K, y=K−x modulo 26. Signs/role are explicit; inverse aliases stay in the descriptor inventory, not independent evidence.

Primitive upper count 38; exact duplicate primitives must be removed and aliases retained. Enumerate all ordered compositions of lengths 0–3, including identity: raw bound 1+38+38²+38³=56,355 descriptions. Operation order is left-to-right application to the stream. Do not add ENE routes, new alphabets, free keys, offsets or larger skips to this grammar after results.

Compile each composition as a global affine/permutation operator T(x)[i]=s×x[p(i)]+b[i]mod 26 withs∈{−1,+1}. Compose exactly, and deduplicate by the complete canonical(p,s,b), not by equality on K4 alone. This proves equivalence on every 97-symbol input. Keep depth, all aliases and exact inverse; no score-based beam, genetic sampling or heuristic pruning. Report actual unique counts per depth and descriptor count separately. Compare exact existing route/key/continuation coverage before counting novelty.

After parent audit, validate every primitive and representative composed plants at each depth, full random-input round trips, independent list-based reference replay and small exhaustive alphabets/operators. Plants must recover their canonical operator equivalence class and full hidden plaintext, while allowing honest aliases/collisions. Where possible use known K1/K2 arithmetic vectors as external controls; otherwise label synthetic controls. No source lookup is evidence of historical selection.

Evaluate all unique operators against all 24 English letters, save every exact survivor and full 97 inverse regeneration. Safe pruning checks only mathematically necessary crib equalities. For partial-match summaries rerun alloperators on 31 seed 50001 conditional ciphertext permutations of 73 unanchored positions; report the whole-family maximum, not selected English fragments. Also report ties/short primitive aliases. These nulls are conditional diagnostics, not a universal p-value or independent evidence for a source-themed message.

Budget 180 seconds/1 GiB for compile/oracle preflight and 600 seconds/1 GiB for actual+31 null selector, finite upper 56,355 operator descriptions before dedup. If the measured budget cannot finish, preserve exact completed/unresolved coverage and do not extend or sample silently. New results stay local, no Site edits, external LLM, paid checker or publication. Await parent design audit before a large search.

## Source/provenance caveats supplied for this design

The parent source reviewer identifies [Sanborn's 12 November 2025 letter](https://www.documentcloud.org/documents/26229389-adobe-scan-nov-12-2025/) as primary support for the second Egypt trip in late 1986, the Berlin Wall's fall, the World Clock and message delivery. Its simultaneous 1988 writing statement and Wall-fall reference are preserved as a chronology inconsistency, not repaired into a trip/date. These are optional generation priors, not additional plaintext constraints. The source facts are parent-reviewed; this design does not claim a fresh local visual authentication of the letter.

[Sanborn's Smithsonian oral history](https://www.aaa.si.edu/collections/interviews/oral-history-interview-jim-sanborn-15700), recorded 14–16 July 2009 and artist-reviewed in 2020, supports a manually adaptable artistic workflow and Scheidt's teaching of old/contemporary systems. It supplies no exact K4 algorithm, key, three-step maximum or tractability theorem. Its hand-jigsaw discussion concerns fabrication. The 2011 simple/rememberable description remains indirectly reported because the underlying Hannon message is unavailable; it is not an admitted algorithm specification.

[The prior author's 8 April 2026 depth-three audit](https://github.com/jcolinpatrick/kryptos/blob/main/docs/exhaustion_audit_2026_04_08.md) reports particular substitution/columnar/substitution domains and remaining gaps. Exact operator/key-domain overlap still requires a source-pinned audit; its numerical completeness claims are not adopted here. The narrow source search found no verified prior exact 2-across/1-up test, which is not proof of novelty. Existing local route, periodic, autokey and genetic/continuation coverage must be compared explicitly before counting new results.
