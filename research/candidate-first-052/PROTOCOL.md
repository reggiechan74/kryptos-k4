# Candidate first Kryptos experiment 052

## Status and reason for this experiment

Draft preregistration for independent audit. No actual 052 bank scores have been computed.

Experiment051's scientific expansion gate FAILED: maximum conditional score −8.87924776407408bits, global p=.916, margin .5702893680308421bits. The user subsequently explicitly authorized a separate larger exploratory batch of1024messages, despite that result. Experiment052 proceeds because of that instruction, NOT because051 passed, and does not retroactively alter051. The implementation team knows K4 and051results; authors remain blinded to ciphertext, keys, scores, and rankings. This is an expanded-bank exploration with the SAME frozen structural model/statistic rules, not a new language-key recognizer or a claim of preregistered051success.

## Bank and blinding

Four blind author batches will each contribute256 independently drafted complete messages:

- `authors/a_themes.json`: group `a_themes`.
- `authors/b_neutral.json`: group `b_neutral`.
- `authors/c_berlin.json`: group `c_berlin`.
- `authors/d_messages.json`: group `d_messages`.

Each original file and all draft provenance are preserved byte-for-byte. Importer accepts original fields `id`, `spaced_prose`, `normalized`, `revision_history`, `theme`, `authoring_method` and produces a separate normalized bank with original ID, group, source filename/source SHA256, original plaintext, and prose. The deterministic alias is always `<group>:<original_id>` for EVERY record, preventing cross-author collisions without a score-selected rename. Original IDs remain in the mapping.

Exactly1024 unique normalized `[A-Z]{97}` strings are required; EASTNORTHEAST at1-based22–34 and BERLINCLOCK at64–74. Each normalized string must equal A–Z normalization of its complete prose, be absent from all32frozen051messages, and differ from the frozen bank-absent control text. Duplicate/length/prose corrections must occur before freeze through blinded authors, preserving revisions; no score-based filtering, candidate edits, or substitutions. Distinct messages and broader styles do not establish independence or exhaustive coverage of sensible sentences.

The bank, source/provenance bytes, group mapping, implementation, control definitions, RNG seeds, and this protocol must all be hashed and independently audited before ANY actual052bank score, including its controls.

## Unchanged scientific model and primary score

Use the051protocol mathematics unchanged: AZ and the deduplicated KRYPTOS alphabet; four ordered plaintext/ciphertext index-alphabet pairs; Vigenère, Beaufort, variant Beaufort arithmetic; periodic, plaintext-autokey, ciphertext-autokey descriptions; periods/seeds1–32. Exactly1152 descriptions per candidate,1,179,648 over the complete bank.

Only the candidate-selection cost changes mechanically from `log2(32)=5` to `log2(1024)=10`bits. For the73non-crib positions, baseline is `73*log2(26)`. Each description costs `log2(1024)+log2(1152)+r*log2(26)+log2(n+1)+log2(comb(n,e))+e*log2(25)` with precisely the051definitions of n/e/modal periodic templates and autokey tail positions. Primary score is baseline minus cost. Crib exceptions are conditioned on/disclosed, not paid or credited. Exact full97-letter compatibility and re-encryption/inverse checks remain separate and mandatory.

The ciphertext statistic is the maximum over ALL1024messages and ALL1152descriptions. Candidate ties use normalized aliases; model ties use the same lexicographic tableau ID, structure name, and length order as051. All ties and every candidate's best description are retained. No crib-impossible exact model causes candidate skipping; residual-penalized scoring does not resurrect excluded exact models.

No new transposition, alphabet, key-language, topic, semantic-coherence, or heuristic feature is introduced. Natural-language running-key detection remains unimplemented and outside the negative conclusion's scope.

## Fixed controls and conditional calibration

Keep051control families, literal simple seeds, lengths, success definitions, score threshold, and operational gates. Before scoring, freeze84literal controls:36simple (12tableaux×3structures),24structured-hard (period29 and autokey29 for each tableau),12natural-language-running-key diagnostics,12bank-absent classical controls.

Select in-bank control messages deterministically across the new bank: sort IDs within each of the four groups, interleave groups in the order listed above, then assign sequential control index j to schedule position `(17*j) mod1024` for j=0..71. This samples60distinct in-scope plaintexts,15per group, spread across the bank; it does NOT demonstrate sensitivity for every one of1024messages. Running-key diagnostics use indices60..71. The bank-absent plaintext and running passage are copied unchanged from051; absence from the new bank is verified. Simple seeds remain KRYPTOS(period7), PALIMPSEST(plaintext-autokey10), ABSCISSA(ciphertext-autokey8). Hard autokey type remains plaintext for even zero-based tableau index, ciphertext for odd. Hard seeds use29AZresidues generated before scoring.

Use fresh deterministic052RNG streams: `random.Random(int.from_bytes(SHA256(UTF8('candidate-first-052-v1|' + label)), 'big'))`. Construction labels, control numbering, and null-split labels follow051 exactly apart from the052prefix and new scheduled plaintexts; all resulting literal controls are frozen. Running-key offset remains13×tableau_index in the same passage.

Each of84controls receives99conditional calibration nulls; each of60in-scope and12bank-absent targets additionally receives10independent validation nulls. Every null fixes crib ciphertext letters and uniformly permutes the73remaining ciphertext letters, preserving their multiset, and uses the WHOLE1024×1152 maximum. The conservative p-value is `(1+count(null maximum >= observed maximum))/100`. A control flag requires score>=16bits and p<=.05. Running-key controls are diagnostic, not sensitivity failures. No nulls are calibrated only against their planted candidate or model.

## Pre-target operational gate

Before actualK4 scoring require independent implementation/hash audit, all reference/equivalence tests passing, and:

1. At least34/36 simple controls recover the exact planted plaintext with an exact full97-letter registered representation and flag, at least11/12 per structural class.
2. At least22/24 structured-hard controls meet the same recovery rule.
3. At most30/600in-scope validation nulls flagged.
4. At most1/12bank-absent targets flagged; their120validation-null results are reported separately.

Report all failures, scores, label matches, ties, and denominators. These correlated flags are operational calibration checks, not independent Bernoulli confidence bounds. If a gate fails, stop beforeK4 and report without tuning. User authorization of a larger bank does not authorize dropping pipeline correctness or calibration gates.

## Frozen target stage and stopping condition

After gates and parent authorization, verify the same canonical97-letter K4 SHA256 `eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab`. Score the entire frozen bank once, then evaluate1999fresh052conditional nulls with RNG label `K4|conditional-null` through the complete bank/model maximum. Report `(1+#null maxima>=target maximum)/2000`, full1024ranking, descriptive group statistics, exact-fit status, every top-description component/residual, and full re-encryption/inverse diagnostics.

Keep the same evidence criteria: score>=16bits, globalp<=.01, margin>=8bits over the highest-scoring different plaintext. These do not certify historical intent or a solution. No automatic further expansion or model/threshold tuning follows. If any criterion fails, conclude this authorized1024-message experiment with a negative scoped result; if all pass, report for separate validation/authorization. Existing051evidence remains separate and is not pooled to select a favorable p-value.

## Exact acceleration and audit

Use available local C compiler only; no installation, network service, model API, credentials, paid checker, publication, or desktop access. The C implementation may accelerate exhaustive integer comparisons/counts but must use the SAME Python-precomputed double score tables, with exact equality for table values, deterministic lexicographic model ties, and no candidate/model pruning or altered/null-only scoring.

Independent Python reference tests on synthetic banks must cover every model score, all per-candidate winners and equal-score ties, global maxima, crib invariants, reference residuals/exact diagnostics, all three encryption rules/two alphabets, and boundary lengths1/29/32. Include frozen051test vectors without changing051files. Compare C and Python results on random synthetic banks and constructed tie-heavy cases, and end-to-end simple/hard planted synthetic tests. Compile without fast-math. Hash Csource, build command/compiler version, wrapper, reference code, and produced binary; independent audit must bind source hashes. Benchmark ONLY synthetic banks before production scores; report CPU/wall/resource estimates, not guessed speedups.
