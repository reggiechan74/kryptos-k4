# Study 063 frozen protocol — coupled 26/24 accumulator

## Exact model

One alphabet A, either AZ or KRYPTOS. Key digits0..25, nominal period p=1..6, original-position phase0. All624 initial states a0=0..25,h0=0..23. For plaintext rankx and current keyk: t=a+x+k; a'=t mod26; emit y=(a'+OLD h) mod26; h'=(h+floor(t/26)) mod24. Carry may0,1,2. No mixed alphabets, routes, signs, padding, alternate readout timing, resets or new moduli.

Normal form T=26h+a in Z624 updates T'=T+x+k mod624. The nonlinear output reads the new low digit and old high digit. This is a scalar modular accumulator, not a new physical-gearing invention. The24 counter is speculative thematic motivation, not a measured clock mechanism.

## Exact solver and reachability

For each alphabet/period, enumerate all624 possible entry states independently for the13-letter and11-letter clue blocks. At the first encounter of each residue, a known plaintext/ciphertext letter forces its key digit; repeated occurrences must agree. Both blocks visit all residues p<=6, so each retained seed is complete. Intersect the two seed sets as a LOSSLESS SUPERSET ONLY. Then decrypt the actual entire97-letter ciphertext continuously from EACH of624 message-start states for each retained seed, requiring all24 clues and full forward re-encryption for every returned candidate. Never restart state at a target crib. Empty global set is exact within these finite bounds.

Return every compatible alphabet/period/key/start-state/plaintext tuple. Keep nominal-period and state/key aliases; no requirement of uniqueness. Distinct plaintext counts are descriptive. Do not claim parameter descriptions equal independent functions. All-zero keys remain included: this model is not pure transposition when keyzero.

## Prior-equivalence gate

Read exact local/external equations and bounds. Prove scalar normal form, native nonlinearity and relevant fixed-alphabet distinctions. The local radix-feature family needs its own even-glyph parity argument, not merely a slogan that the proposed cipher is nonlinear. Record source pins, primary-source reviews and remaining limitations. Unknown potentially containing prior scope blocks admission. Do not execute third-party source or publish unlicensed copies.

## Correctness and calibration

Independent scalar-state reference is authored before explicit(a,h) production inspection. Complete tiny forward truth, local key filters and global solution sets must agree; forward/inverse checks cover OLD high timing and allcarry cases. All7,488 full-size alphabet/period/start-state direct synthetic settings are independently checked before freeze. These development fixtures are not held-out results.

Twelve synthetic calibration cases measured mean0.1344/max0.4306 CPU seconds per independent union solve, with substantial legitimate parameter aliases. This supports a bounded688-case holdout, not an assumed80-second2,560-case run. Exact comparison/roundtrip gates remain unchanged; no uniqueness gate is introduced.

## Fresh688-case blind benchmark

Generate a fresh256-bit seed after code/protocol/eligibility freeze. Shuffle opaque IDs. Engines receive ciphertext, crib maps and block positions only. Seal both complete output files and resources before answer inspection.

624 whole97-letter plants: for each scalar start state s=0..623, alphabet index a=s mod2; period p=1+floor(s/2) mod6; kind is uniform when floor(s/12) is even, literal-clue when odd. This gives exactly26 plants in each of24 alphabet/period/kind cells and every initial state once. Keys are independently uniform digits. Literal clues occupy canonical plaintext positions21..33 and63..73; remaining letters are uniform random, not English.

64 nulls: independent uniform97-letter ciphertexts,32 independently uniform assignments at the24-position mask and32 literal public-clue assignments. No rejection sampling or resampling.

Admission gates: all688 complete tuple sets agree exactly; every plant's actual alphabet/period/key/start-state/plaintext tuple is retained; all returned candidates satisfy allclues and exactly re-encrypt all97letters; every initialstate and each balanced cell covered; at most1 of64 nulls has ANY compatible tuple across the entire union. Unique plaintext recovery is descriptive only. Full parameter aliases and distinct plaintexts remain explicit, not artificially deduplicated into a likely solution.

## Budgets and stop

Whole study at most28,800CPU seconds/8GiB including prior review, controls/audits and publication preparation. Each engine batch300CPU seconds/600wall/512MiB address space; independent benchmark audit600CPU seconds/1GiB. Record measured costs plus transparent reserves for unmeasured setup, never fabricate RSS. Preserve all failures and superseded controls. No paid services or external source execution.

Parent independent-benchmark review must authorize exactly one production and one reference K4 pass under unchanged freeze. Separate target transport freeze and output seal; final independent non-search audit. No model, budget or gate rescue after outcome. Reconcile canonical local/external ledgers before any later research question. A compatible tuple is not a K4 solution; an empty union excludes only this exact bounded accumulator.
