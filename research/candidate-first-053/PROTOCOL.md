# Candidate first experiment 053 language running keys

## Status and authorization

Design draft for independent audit. No K4-derived key has been scored with a053language model. Experiments051 and052 remain unchanged and negative. The user explicitly authorized this separate investigation of the previously untested language-key gap. The same immutable1,024-message052bank is used; no candidate prose, topic, or model source is selected from previous winners.

This is a new standalone exploratory test after prior experiments, not cumulative familywise error control across them. A positive result would support a fixed language-structure statistic under its conditional null, not establish historical authorship, semantic meaning, or a solved cipher.

## Fixed corpus provenance and whole-document separation

Use only the official NLTK data repository snapshot at commit `550b6625bcef1f2abff2ff770a5a0d272c9c6b2a`:

- `gutenberg.zip`, SHA256 `2d3c3ab548c653944310f37f536443ec85d0a0ad855fcae217a0c9efdce2d611`.
- `inaugural.zip`, SHA256 `b3b2cb7bd82697b58ff79c75af20ab963810d191a8c3d1f7c240f98e5d27a895`.

Raw downloads, repository metadata, index.xml, DATASET-LICENSES.md, archive README/license texts, individual document bytes/hashes, and normalization mappings are retained under data/. The official index/license summary classifies both collections as Public Domain; Gutenberg's included trademark/distribution terms are preserved. No Brown source-exact admission test or copyrighted commercial corpus is used. Sources were chosen as existing general English collections, not by cryptographic scores or Kryptos topics.

### Training only

Exactly these8Gutenberg documents:

`austen-emma.txt`, `austen-persuasion.txt`, `austen-sense.txt`, `chesterton-ball.txt`, `chesterton-brown.txt`, `chesterton-thursday.txt`, `edgeworth-parents.txt`, `melville-moby_dick.txt`.

Use at most the first200,000 normalized letters of each. The ENTIRE original document/author remains assigned to training; unused tails are not eligible as calibration or controls. No inaugural text or candidate-bank prose enters training.

### Calibration only

Gutenberg: `bryant-stories.txt`, `burgess-busterbrown.txt`, `carroll-alice.txt`.

Inaugural: every `.txt` document whose filename's speaker surname begins A–M, inclusive. All documents for the same filename surname stay together; Adams and Roosevelt family names are conservatively grouped. This is speaker-disjoint separation, NOT guaranteed actual-writer/ghostwriter separation. This rule is fixed before scoring.

### Published prose controls only

Inaugural: every `.txt` document whose filename's surname begins N–Z. These complete documents and speaker groups are disjoint from training/calibration; actual speechwriter identities are not established. The collection includes modern speeches; they are test material for language generalization, not claims of historically available K4 key sources.

### Difficult-style controls only

The remaining7Gutenberg documents: `bible-kjv.txt`, `blake-poems.txt`, `milton-paradise.txt`, `shakespeare-caesar.txt`, `shakespeare-hamlet.txt`, `shakespeare-macbeth.txt`, `whitman-leaves.txt`. These test archaic, poetic and dramatic language. All Shakespeare documents remain in this one role.

### Truly source-absent controls

Obtain12new independently authored prose documents, each200–600 ASCII alphabetic letters before extracting a key, without ciphertext, candidate-bank access, language-model scores, fixed crib words, or prescribed97-letter phrasing. Four ordinary topics, four procedural/technical topics, and four correspondence topics are fixed in CONTROL_SOURCE_PLAN.json. Retain complete prose and revisions. Select one97-letter window per document by the same score-blind rule below. Each must be absent from every frozen published source; these are positive controls whose true key is unavailable to any source-exact lookup.

No original document is divided across training/calibration/controls. Attributed book authors are role-disjoint; inaugural speaker groups are role-disjoint, but shared ghostwriters cannot be ruled out. Sampled windows within each document are separated as defined below. The exact97/48letter overlap checks establish only measured overlap exclusion, not proof against every paraphrase or unrecognized reuse. No source or key may be replaced because it scores poorly. Document/topic coverage is limited and not an independent sample of all English.

## Deterministic preprocessing and passage selection

Normalize by retaining ASCII bytes A–Z/a–z and uppercasing, without transliteration, spaces, punctuation, or digits. Exclude README/metadata files. NLTK's Gutenberg package already removes its main distribution headers; if a document starts with a single bracketed title/author line, omit that first line only. Record raw/normalized hashes and source offsets. No content-based stylistic cleanup.

For a document of normalized length L>=97, set `margin=min(512,floor((L-97)/4))`, `lo=margin`, `hi=L-97-margin`, `phase=rng.randrange(min(512,hi-lo+1))`, and `grid=range(lo+phase,hi+1,512)`. Thus every sufficiently long document has at least one candidate start, including short novel documents. Eligible starts are this deterministic512-spaced grid within both margins. Shuffle the grid once using a document/role-specific RNG. Windows used from the same document have no overlap and at least415letters between them. Short documents may contribute fewer windows; no wrapping or concatenation across documents.

Reject a proposed held-out window only for objective data integrity: fewer than97letters, duplicate97-letter key, or any contiguous48-letter substring shared with a document in a different role. Compare against full normalized documents, not just sampled windows. A novel source-absent key must additionally have no exact97-letter match anywhere in the published collections. This is leakage prevention, not a test of whether a key fits the corpus. Keep all rejected offsets and reasons. Never examine a cryptographic score to select a window.

Calibration takes up to64windows per calibration Gutenberg book and up to4per calibration inaugural document. Published-prose and difficult-style pools are filled by round-robin over sorted document IDs, consuming eligible shuffled windows until their fixed required counts are reached. If these rules cannot supply enough windows, stop for an audit amendment before training/scoring; do not silently weaken separation.

All source documents, roles, offsets, rejected-window log, literal key windows, newly authored documents, and RNG labels are frozen before actual-bank control scoring. RNG scheme: `random.Random(int.from_bytes(SHA256(UTF8('candidate-first-053-v1|' + label)), 'big'))`.

## One fixed language model

Train an order4 character Markov model on the training-only normalized texts, never crossing a document boundary. Do not choose order, weights, sources or smoothing from actual derived keys or control outcomes.

For letters a and suffix contexts h, use hierarchical Dirichlet smoothing:

- `P1(a) = (count(a)+0.5)/(total_letters+13)`.
- `P2(a|h1) = (count(h1,a)+5*P1(a))/(sum_b count(h1,b)+5)`.
- `P3(a|h2) = (count(h2,a)+10*P2(a|suffix1(h2)))/(sum_b count(h2,b)+10)`.
- `P4(a|h3) = (count(h3,a)+20*P3(a|suffix2(h3)))/(sum_b count(h3,b)+20)`.

Every row is a proper probability distribution; unseen contexts back off smoothly. Store exact counts and double-precision log2 probability tables, with hashes and tests. There is no hyperparameter sweep, target-dependent word list, neural model, external model API, or exact-passage prerequisite.

## Fixed12tableau family and key spelling

Retain exactly the12indexed arithmetic transformations from051/052: plaintext/ciphertext index alphabets independently AZ or deduplicated KRYPTOS, with Vigenère, Beaufort or variant Beaufort arithmetic. No additional layers, substitutions, periods, autokey search, or selectable key alphabets.

**Explicit language-specific convention:** inferred key residues are decoded in that model's plaintext-axis alphabet. Thus AZ-axis keys are spelled in AZ; KRYPTOS-axis keys are spelled in KRYPTOS. This explicit fixed per-model assumption makes key spelling unambiguous WITHIN this experiment; it is not uniquely implied by every conventional tableau. Other row/key-label conventions are excluded from the scope. Earlier periodicity tests' arbitrary AZ display labels were irrelevant to equality patterns; they are not silently reused as English spelling. This convention requires explicit design-audit acceptance and limits the result's scope. Each control's true English key is encoded using the same fixed key alphabet.

## Primary statistic excludes every crib letter and context

Let the three non-crib zero-based blocks be `[0,21)`, `[34,63)`, `[74,97)`, totaling73letters. For each candidate/tableau, derive its full97-letter key, but score only these three blocks, resetting language history at each block boundary. Use P1, P2, P3 for each block's first three letters and P4 thereafter. **No known crib key letter contributes to the primary likelihood, even as context.**

Define:

`S = 73*log2(26) + sum_noncrib_blocks log2 P(key_letter | up to3 earlier letters in the same block) - log2(1024) - log2(12)`.

This is a fixed conditional language-coding saving against literal uniform letters, including candidate and model choice penalties. The ciphertext statistic M is the maximum S across all1,024messages and all12tableaux. Preserve all candidate/model scores and ties. Deterministic ties use candidate alias then tableau ID; a different-plaintext tie is not a unique recovery.

The whole97-letter key's cross entropy under the SAME model, with one history reset at its start, is `H=-(sum_{i=1..97}log2 P(key_i|up to3 preceding key letters))/97` bits per letter. It is a secondary plausibility check. For n calibration-only97-letter windows, sort H ascending and freeze the upper ceiling at one-based rank `ceil(.99*n)` (nearest-rank99th percentile). This ceiling is fixed before control results and K4. It is an additional conservative gate, not extra primary evidence or a source-exact requirement. Report the ceiling and every failure. No new word-breaking/semantic score is optimized after seeing a key.

Exact encryption and inverse recovery must be verified for every candidate/tableau. Their success is inevitable with an unrestricted key and is not corroboration. This language stage does not call an arbitrary full-length key "simple" merely because it re-encrypts.

## Whole-pipeline controls

Freeze144targets, with12tableaux in their existing order. Assign prose/hard/novel/uniform controls indices j=0..95 in that order using the existing four-group interleaved schedule and position `(17*j) mod1024`. Letter-permuted controls reuse the corresponding prose controls' plaintext/tableau. Word-order stress diagnostics use j=96..107. True-plaintext-absent controls use the separate rule below. No planted candidate/model is passed to the scorer.

1. **Published unseen prose positives36:**3different held-out inaugural key windows per tableau. All true keys are absent from training/calibration passages.
2. **Difficult-style positives24:**2different held-out hard-style windows per tableau.
3. **Entirely source-absent positives12:**1new blind-authored key per tableau, absent from all published collections, not just training.
4. **Uniform-key negatives24:**2independent uniform97-letter keys per tableau, with true plaintext present.
5. **Letter-permuted-key negatives24:**2per tableau, uniformly permuting the full97letters of registered prose keys, retaining their unigram composition but destroying order. For each tableau, pair with its first two of three prose positives, reusing the same plaintext and tableau. Paired inputs and seeds are literal frozen control definitions.
6. **True-plaintext-absent controls12:**1per tableau, with genuine unseen prose keys and twelve different frozen051plaintexts outside the1024bank. Choose those plaintexts by ascending SHA256 of `candidate-first-053-absent|plaintext`, not prior scores; verify exclusion.
7. **Word-order stress diagnostics12:**1per tableau, using independently frozen word-token-order permutations of held-out prose. For this diagnostic, additionally require the mapped first/last source byte of the97-letter window to be at ASCII-letter-run boundaries: its immediately preceding/following byte must not be A–Z/a–z (or must be a document boundary). Reject and log non-boundary windows before scoring; do not preserve partial edge fragments. Tokenize maximal ASCII letter runs in the mapped source span, assert their normalized lengths sum to97, permute the complete token list with the frozen stress RNG, and concatenate all tokens so length/composition stay fixed. If the first permutation is identical, repeat deterministic shuffles up to100times, then fail integrity rather than silently use the original. Contractions/non-ASCII spellings may split into tokens, so this is a token-order diagnostic, not a claim that every token is a dictionary word. These keys largely preserve words but not coherent syntax. They are diagnostics, not included among random-letter negatives: a character model may recognize their language structure. Report flags and actual plaintext/key recovery openly; passing these is not evidence of semantic comprehension.

Published prose needs60unique windows:36positive,12plaintext-absent and12word-order stress sources. There is no score-selected reserve or replacement pool. Letter-permuted negatives reuse their declared positive source keys only as paired negative construction; no such key enters training/calibration. Difficult styles need24windows. Newly authored keys need12documents.

A positive recovery requires: unique top plaintext equals the planted plaintext; inferred full97-letter English key equals the planted key; chosen representation re-encrypts and inverts exactly; primary S>=32bits; conditional p<=.05; and full-key cross entropy passes the calibration ceiling. Model-label ambiguity is reported separately; merely finding a vaguely English-looking alternative key is not recovery.

For every one of144targets, generate99calibration ciphertext nulls and10independent validation nulls by fixing all crib ciphertext positions and uniformly permuting the73other ciphertext letters. EVERY null uses the same full1,024×12maximum. Conditional p=`(1+#calibration maxima>=observed M)/100`. Validation nulls use the matching calibration set and the SAME detection rule, including the full-key ceiling applied to the selected winner. Store the required winning key/full-key score for nulls; do not gate validation using a statistic unavailable for the null winner.

A flag requires primary S>=32bits, p<=.05, and the full-key ceiling. Record all maxima, null hashes, selected winner identities/full-key scores and flag vectors, not only successful controls. These are matched conditional nulls and clustered controls, not independent universal false-positive trials.

## Pre-target gates fixed before any control scores

1. Source/license/hash audit passes; documents/authors/windows are separated; unchanged1024bank verified; probability/C-reference/crypto/null tests pass.
2. Published unseen prose: at least32/36 correct plaintext AND exact-key recoveries, with at least2/3 per tableau.
3. Source-absent new prose: at least10/12 correct plaintext AND exact-key recoveries.
4. Difficult styles: at least18/24 correct plaintext AND exact-key recoveries. Report failures by source/style.
5. Uniform plus letter-permuted negatives: at most2/48 flagged.
6. True-plaintext-absent controls: at most1/12 flagged.
7. Matched validation ciphertext nulls: at most72/1440 flagged, with all denominators and dependence disclosed.

The word-order stress diagnostic is mandatory reporting, not a secret tuning set or semantic-proof gate. If any required gate fails, stop beforeK4, report the exact failure/scope and request any separately authorized redesign. Do not retune on failure.

## Frozen target test and stopping rule

Only after all gates, independent audit and parent authorization, score the same canonicalK4 (SHA256 `eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab`) once with the frozen model/bank. Generate1,999fresh conditional ciphertext nulls using the same complete maximum and RNG label `K4|conditional-null`. Global p=`(1+#null maxima>=K4 M)/2000`.

Require ALL: primary M>=32bits; global p<=.01; margin>=8bits over the best different plaintext; and selected full97-letter key passing the frozen calibration cross-entropy ceiling. Report every gate separately, full derived key/prose, non-crib block likelihoods, full-key diagnostics, model/key spelling convention, ties, group summaries and exact reencryption/inverse status. Do not infer success from readability alone.

Optional exact matches against the already frozen published documents are secondary corroboration only, never an admission gate or replacement for unseen-key testing. Dates and limitations must be reported; a modern source is not evidence of historical availability. No new corpus search after seeing a target key.

If any target criterion fails, conclude this authorized053test without additional candidates, score tuning or feature search. If all pass, report scoped statistical evidence for separate independent verification, not a solvedK4 claim. No automatic expansion/publication follows.

## Resource and execution bounds

Standard-library training/helpers plus audited local C acceleration if useful; no new installations, external model APIs, paid checker, desktop/Mac access, credential changes, quota-blocked service, or publishing. Bound to144controltargets,15,696control-null replicates and1,999target-null replicates; at most8workers and8GB additional disk. Benchmark only synthetic inputs before production. Aim for under60minutes once sources/model are ready; if resource limits prevent the registered run, pause and report rather than silently reducing coverage.

A dense order4 double log-probability table is under4MB. Preserve source snapshots, train/calibration counts, hashes, all literal controls, full score matrices/winners needed to audit selection, null receipts, independent audits, and reproducible commands. Freeze all code/model/data/threshold/control hashes before actual-bank controls and again bind the passed control evidence before target authorization.
