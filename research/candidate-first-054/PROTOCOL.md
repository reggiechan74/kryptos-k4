# Experiment054: bounded crib-first exact running-key source lookup

## Authorization and status

The user explicitly requested a changed test and agreed to implementation in the assistant's own cloud VM. This experiment leaves051–053 unchanged. It uses neither guessed full plaintext nor the053language scorer. No canonical target-derived fragment has been calculated or queried when this protocol was drafted. Independent source/code/control audit and hash freeze must precede target lookup.

## Question and prior coverage

For each of the same12finite arithmetic tableaus used in053, do both known-plaintext-derived key fragments occur at their required spacing inside one97-letter running-key window in a frozen, historically eligible text collection?

This exact-source method is **not new in itself**: prior048 searched Brown with six same-axis variants and found no exact matching passage. Its archived report states500documents,4,745,928normalized letters; Brown ZIP SHA256`9b275f9b3b95d7bd66ccfb7cd259f445a13bbe5d1f4107aba09fd3e8364bafa6`; ordered-stream SHA256`62f0154406b697fc022f5295d57931334cca7b0da9a21135a307d821e3a4930b`. The immutable source commit is`6003dae5497ee5a8e53881576776423028205cd7` in`reggiechan74/kryptos-k4`. Its archived implementation was independently verified: key letters use the same plaintext-axis alphabet as054, so all six same-axis domains overlap exactly; the six cross-axis domains are additional relative to that048inventory.

The gain here is bounded additional source coverage, plus any explicitly identified cross-axis variants absent from048—not a relabeling of Brown coverage. Brown is retained as a prior baseline, not counted among newly searched letters. Full-document duplicates/editions within the new collection are reported and never hidden. We do not assume zero excerpt overlap with Brown without checking it.

## Fixed finite corpus acquisition plan

Sources are selected as general English literature, public speeches and a few nonfiction works—not for Berlin/clock/Kryptos themes and not from a target fragment or earlier winning candidate.

1. Reuse the18Gutenberg documents from053's pinned NLTK snapshot, subject to documented historical eligibility. The exact same raw bytes are preserved.
2. Reuse only inaugural speeches with original delivery years<=1989 from that snapshot (51eligible dated filenames; nine1993–2025documents excluded). Modern archive timestamps are not historical speech dates.
3. Consider exactly these24Project Gutenberg IDs, selected before retrieval: `1342,84,1661,98,1400,174,345,76,74,12,120,35,36,43,219,203,1260,768,1080,23,205,1232,1228,5001`.

The24IDs cover ordinary fiction plus memoir/essay/science. There are no replacements, reserve titles, thematic searches or additional IDs. Acquisition is bounded to15minutes,24books and100MB raw text. A failed/unavailable/poorly dated work is logged and excluded, not replaced. Raw metadata/date evidence, download URLs, retrieval times, byte counts, licenses and SHA256 hashes are retained. The final eligible manifest is frozen before deriving target fragments.

The cutoff is **pre1990, inclusive through1989**. Historical work/English-translation/edition dates must be distinguished from digital release/update dates. No invented exact dates. For original English classics, a sourced historical work date establishes the work's eligibility, but unknown exact transcription/edition details remain explicitly recorded. An uncertain modern translation, revision or editorial contribution is not assumed historical; exclude unresolved material/source before freeze. Any eventual hit additionally requires checking the literal passage's historical provenance; a modern transcription alone cannot establish that its exact wording was available to the creator.

## Fixed normalization and document boundaries

- Preserve original raw bytes. Normalize by retaining only ASCIIA–Z/a–z and uppercasing; no transliteration or digit spelling.
- NLTK books: remove only the initial bracketed title/author line, exactly as053; preserve all remaining body text. Inaugural texts: preserve the complete delivered-text transcription.
- New Project Gutenberg texts: retain bytes strictly between the first complete START marker line and the following complete END marker line. Match the conventional THE/THIS PROJECT GUTENBERG marker forms deterministically. Fail closed if markers are missing, reversed or ambiguous. Preserve original work front matter/headings inside the body; no content-based or cryptographic filtering.
- Keep a reproducible normalized-letter-to-raw-byte offset map for every accepted text, bind its uint32-little-endian hash in the manifest, and record all removed spans; raw bytes plus frozen normalization reconstruct the map exactly.
- Never concatenate documents, wrap, skip internal letters, reverse text or cross a document boundary. Different editions remain separately identified; no silent deduplication of hits. PG205combines Walden and Civil Disobedience without an established historical compilation date: its last standalone second-work heading is a frozen boundary annotation. Any97window crossing that boundary is retained but explicitly labeled a modern-transcription candidate with historical adjacency unverified, never automatically certified as an eligible historical key passage. Other exact-edition/compilation uncertainties remain disclosed.

The corpus manifest reports per-document eligibility/source date, raw/body/normalized hashes and lengths, total document/letter counts, valid97window counts and duplicate normalized-document groups. Shared quotations/editions mean these are coverage counts, not independent trials.

## Fixed12tableau scope

Plaintext and ciphertext index alphabets are independently AZ or `KRYPTOSABCDEFGHIJLMNQUVWXZ`, and the operation is Vigenere, Beaufort or variant Beaufort. This is exactly12variants, with no added transposition, reversal, offset layer, autokey or arbitrary substitution.

For each variant, key residues are spelled using its plaintext-axis alphabet, as fixed in053. This is an explicit convention, not a uniquely established historical convention; alternative key labels are outside scope.

Known plaintext: `EASTNORTHEAST` at zero-based positions21–33 (13letters), and `BERLINCLOCK` at63–73 (11letters). Derive each key fragment using only those plaintext letters and the corresponding ciphertext letters under the tableau. No assumptions about the other73plaintext letters enter lookup.

## Exact lookup and complete reconstruction

Let the first derived fragment occur at normalized source indexs. Require:

- source[s:s+13] equals the complete first fragment;
- source[s+42:s+53] equals the complete second fragment;
- window_start=s−21>=0;
- window_start+97<=document length.

Thus fragment starts differ by42letters, with29unknown letters between them. A valid hit has21key letters before the first fragment and23after the second fragment, entirely within one document. Partial-margin pairs are reported as boundary-rejected pairs, not valid97letter hits. Overlapping first-fragment occurrences are all examined.

Save EVERY valid hit, including repeated occurrences and duplicate editions: model, document/source hashes, normalized/raw offsets, both fragments, full97letter key, exact raw source span and surrounding source context, decrypted97letter plaintext, both crib checks and full encryption/inverse checks. The independent auditor reconstructs every hit using separate arithmetic and raw source offsets. No Englishness or guessed-message filter may suppress a hit.

Exact re-encryption is mandatory correctness but tautological for an induced running key. It is not independent evidence of historical intention. A hit is an exact candidate-source match under the frozen convention; it is not automatically a solvedK4 claim.

## Controls and implementation gates

Before target lookup, freeze and run:

1.36planted corpus positives: three per tableau, using a fixed control plaintext with the exact crib positions and registered source97windows. Within each model, plant source-window starts0, a deterministic interior start, and document_length−97 to test both boundaries and interior. Selected source IDs/windows are literal controls fixed before querying; allocate deterministically across the eligible collections, including new PG coverage where available. Search the ENTIRE frozen corpus and all12models for each planted ciphertext without passing planted document/model to the search. The known planted hit must be returned, full key/plaintext exactly recovered, and every additional hit retained.
2.12uniform-random full-key absent-source controls, one planted cipher per tableau, with frozen SHA256-derived RNG labels. No redraw if a collision occurs. Search all corpus/models; expected zero valid hits. Any observed hit is retained and fails this negative implementation/data check pending audit; it is not silently discarded.
3. Pure synthetic fixtures for every tableau: correct spacing42; wrong spacing41and43; one-letter mutations in either crib; source start/end exact boundary; insufficient21letter prefix; insufficient23letter suffix; split-across-document false pair; overlapping occurrences; duplicate documents/occurrences; PG header/footer exclusion; normalized byte-offset reconstruction. Negatives are constructed to have deterministic expected outputs, not asserted from chance alone.
4. Independent reference-vs-optimized complete hit-set equality on synthetic fixtures and all36positive controls. Full encryption/inverse checks and normalization/source hashes must pass.

All gates are implementation/data-correctness gates, not empirical estimates of universal language detection. A random-key control's absence is not a calibratedK4p-value. If a required gate fails, stop and report before target; fixes require audit/refreeze before any target query.

## No misleading significance calibration

This is a deterministic bounded corpus lookup. Crib-preserving noncrib ciphertext shuffles leave both queried fragments unchanged, so they are **invariant and provide no useful significance test**. Do not reuse053nullp-values, MDL thresholds, language scores, sensitivity gates or margins. Report exact coverage and hit counts, not an invented chance probability for dependent English passages.

## Target, stop rule and deliverables

Only after the corpus/code/control manifest is frozen, independent control audit passes and parent authorization is received, load the canonical97letter target and verify SHA256`eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab`. Derive the24fragments (two per model) once, search all frozen documents for every variant, retain complete hits/boundary rejections and independently audit any reconstruction.

Stop after this single exhaustive registered lookup. Zero hits excludes only exact97letter running-key passages in these frozen normalized texts under these12conventions. It does not exclude other sources, editions, text normalization, key alphabets, cipher families or unknown plaintexts. Hits trigger reporting and independent verification—not automatic approximate search, new corpus acquisition, candidate ranking, tuning or publication.

Deliver protocol/code/tests, source/license/date/hash manifest, prior048comparison, controls/results/coverage, complete hit evidence and compact reproducibility artifact. Raw sources remain preserved; compact omissions must have exact inventories and deterministic retrieval/materialization instructions. No paid checker, external modelAPI, desktop/Mac, quota-blocked service, publication or billing changes.
