# MASK-FM-ARBITRARY-007: arbitrary-key local constraints

Frozen 23 October 2026 before implementation and K4 evaluation. Follow-up to H-MASK-FM; no extra Feistel rounds, fitted glyphs, physical inputs or Site changes.

## Rationale and prior scope

The earlier MASK-FM-001 evaluated only AZ and KRYPTOS trigraph alphabets. The American Cryptogram Association's [Fractionated Morse specification](https://www.cryptogram.org/downloads/aca.info/ciphers/FractionatedMorse.pdf), freshly read for this protocol, assigns a keyed alphabet to the 26 trigraphs over dot, dash and x excluding xxx. Its published COME AT ONCE example is already an implementation control. An arbitrary permutation contains every keyed alphabet without guessing keywords. Morse exists elsewhere in Kryptos, but neither that context nor historical availability establishes this K4 mechanism.

## Fixed model and relaxed inference

Use the unchanged standard A–Z Morse dictionary in MASK-FM-001, x between letters and xx between words. Cipher letters map bijectively to the 26 ordered trigrams. One shared map spans the whole ciphertext. No routes, extra substitutions, changed Morse codes or deletions. Terminal x padding is unchanged; local inference does not need to select it.

Known English letter indices remain 22–34 and 64–74 after spaces are removed. These are final decoded-letter indices, not ciphertext/trigram indices. Each internal letter gap in a disclosed block independently permits one or two x: all 2^12 first-window and 2^10 second-window word-break masks. No word segmentation is selected because it looks English. Unknown prefix and gap letters remain unknown, with no invented state or crib reset.

If the first Morse symbol of letter 22 is at stream offset s (zero-based), 21 preceding letters and their 21 separators give 42 <= s <= 126 (each Morse letter has one through four symbols, each separator one or two). For letter 64, likewise 126 <= t <= 378, additionally t plus block length <= 291. Between the end of letter 34 and the beginning of letter 64 are 29 unknown Morse letters and 30 separators; hence 59 <= t-(s+first_block_length) <= 176. These are necessary length bounds, not a proof that a prefix or gap exists. The decoded total need only reach position 74; no unsupported assumption that plaintext length equals ciphertext length is needed.

At every window/trigram overlap, intersect the cipher symbol's possible trigrams with the observed partial or complete ternary pattern. Enforce one globally shared bijection, including equal cipher symbols and different symbols across both windows. At most two boundary trigrams per window are partial. Local compatible maps admit exact counting by enumerating only constrained non-singleton entries, multiplying by the factorial of unconstrained free assignments. Preserve domains and a full permutation completion as a **local constraint witness**, not a valid global Morse parse or plaintext.

## Frozen stages and budgets

1. Enumerate every first-block word-break mask and every s in [42,126] fitting the stream. Count raw contexts and unique resulting domain records separately. Evaluate only first-block constraints. If all reject, stop actual inference with an exact necessary-condition exclusion; do not inspect Berlin to rescue it.
2. Only if first-block records survive, join every second-block word-break mask and t satisfying its prefix/stream/gap bounds. Retain the same map: no refitting separate keys. Count all completed contexts or explicitly report incomplete/budget-unresolved. Report which domain constraints narrow old mappings versus introduce previously unconstrained symbols. Berlin is public and historically used, not untouched evidence.
3. If any joined records remain, stop at a necessary-condition compatibility report. Do not call them full cipher survivors, invent unobserved English or add an adaptive global search. A complete prefix/gap parser and exact compatible-union counting would be separately required. Counts summed over contexts are descriptions and can overlap; do not label that sum distinct keys or plaintexts.

One process; first stage 120 seconds / 400,000 contexts, second stage 120 seconds / 2,000,000 joins, exact domain completion 100,000 branches per context. Any exceeded limit is budget-unresolved, not zero. No shuffle significance is required for exact rejection. No partial English score or posterior claim is allowed for compatibility.

## Controls and acceptance

Before actual K4: reproduce the ACA example and inverse; use six unrelated synthetic messages containing the exact two crib strings at their true decoded-letter positions, with varied word breaks and nontrivial alphabet permutations. The selector must retain the true offset, word-break pattern and key, without requiring unique recovery. Exhaustive tiny-domain permutation comparisons verify feasibility, exact completion counts and witness maps; fixed/incompatible mutations must reject. A separately implemented direct substring oracle will check domain constraints on synthetic windows. Verify corner alignments modulo three and partial-boundary restrictions.

Commit protocol before code; commit controlled implementation before K4. Save complete per-context contradiction-class tallies, surviving domain records if any, timing/cap status, input/source hashes and independent controls. Rejection applies only to this direct standard Fractionated Morse model, exact disclosed English positions, declared word separation and no outer layer. Other Morse procedures and composites remain outside coverage.
