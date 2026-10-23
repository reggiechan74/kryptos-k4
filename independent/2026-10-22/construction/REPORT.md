# Kryptos construction-convention audit

Audit date: 22 October 2026. Scope: source-backed historical regression tests, not a claimed K4 solution.

## Bottom line

A small, preregistered **robustness test** for construction discrepancies is defensible. A general prior that K4 contains errors, or an error-tolerant search with unrestricted edits, is not supported by this audit.

The most important result is a negative one: the apparent Cyrillic Projector “gap” is **not identifiable as an omission** from the available aligned data. A key restart at the beginning of its second message reproduces all 1,133 ciphertext/plaintext symbol pairs exactly. It is algebraically indistinguishable from advancing a six-character key by three positions. Calling this three missing engraved letters would overstate the evidence.

The supplied program also reproduces the K1 local worksheet equivalence and the historically confirmed K2 correction. It does not alter canonical K4, generate a K4 plaintext, or infer a shared K4 algorithm/key from another artwork.

## 1. Separate the stages

Maintain separate records for:

1. **Composition/adaptation:** intended wording, spelling, punctuation, excerpts, omissions from a quoted source.
2. **Worksheet encryption:** written plaintext, written key, table lookup, intermediate ciphertext, key restart or phase choice.
3. **Layout/fabrication:** copying intermediate text to the design and cutting it into the object.
4. **Observation/transcription:** photographs, human readings, ASCII/Cyrillic normalization, OCR and publication.
5. **Solver interpretation:** language correction, translation and speculation about intention.

A linguistic misspelling in decrypted text does not, by itself, tell us which earlier stage caused it. A repair that produces readable language does not establish intent. A copied artwork is not an independent draw from an error-generating process.

### What the available evidence establishes

- **K1:** the released worksheet image visibly has the keyword heading PALIMPCEST and contains a local L/C/K plaintext/key/ciphertext triple at the ILLUSION location; the sculpture transcript has K. This is compatible with a local key-letter discrepancy and faithful copying of that cipher symbol. It is not proof of accident, deliberate signalling, chronology or a general error rate. The worksheet webpage attributes its image to a November 2010 New York Times presentation; this audit has not established a complete dated chain from the depicted sheet to fabrication. [Worksheet image](https://www.thekryptosproject.com/kryptos/images/sb_notes.jpg), [provenance page](https://www.thekryptosproject.com/kryptos/charts/pt_k1_k2.php).
- **K2 UNDERGRUUND location:** the same image shows O/S/E locally, while the sculpture transcript yields U/S/R. That distinguishes the extant worksheet from the inscribed text. Locating the change specifically in cutting rather than revision, layout copying or another intermediate requires evidence we do not have. The mathematical correspondence is independently reproduced below. [Worksheet](https://www.thekryptosproject.com/kryptos/images/sb_notes.jpg), [transcript](https://elonka.com/kryptos/transcript.html).
- **K2 ending:** the contemporaneous correction announcement documents Sanborn's confirmation and specifies an inserted ciphertext S. Re-encryption independently verifies the exact location. WIRED reports an aesthetic omission described in terms of a plaintext X; those are different alphabet-domain descriptions, not two interchangeable ciphertext characters. [Correction](https://elonka.com/kryptos/CorrectedK2Announcement.html), [WIRED](https://www.wired.com/2006/04/typo-confounds-kryptos-sleuths/).
- **Fabrication:** Sanborn's 2009 oral history describes stencilling and hand-jigsaw cutting, with assistants working on the alphabet panel while he developed the message panel. This supports a multi-stage production process, not a quantified error probability. He also acknowledges that Cyrillic Projector was solved. [Smithsonian oral history](https://www.aaa.si.edu/collections/interviews/oral-history-interview-jim-sanborn-15700), approximately the 01:16–01:24 discussion of construction and the later 00:34–00:36 discussion of projection works.
- **Reader corrections:** Dunin's June 2003 Projector transcription notes describe comparison of three independently prepared transcripts and approximately a dozen corrections before agreement. These were observed-reader corrections, not evidence for an equivalent number of original fabrication errors. [Transcription and notes](https://elonka.com/kryptos/cyrillic.html).

The two worksheet cells were directly inspected in the downloaded image for this audit. Their intentionality was not inferred from visual darkness, overwritten pencil marks or an undated reproduction.

## 2. Trustworthy related-artwork comparison

### Cyrillic Projector: useful, but not a K4 model

The September 2003 contemporary announcement documents independently reached decryption techniques and subsequent translation work. It also separates transcription, decryption and translation. The mirrored solver table is an executable primary record of the technique. [Announcement](https://elonka.com/kryptos/CyrillicProjectorAnnouncement.html), [solver table](https://www.elonka.com/kryptos/mirrors/CPSolution.html).

This audit uses John Wilson's published aligned cipher/plain table and checks its 1,133 Cyrillic ciphertext symbols against Dunin's transcript. They agree after explicitly documented mixed-script normalization. This is cross-publication corroboration, **not** a fresh photographic transcription and not a claim that the two publications are statistically independent. The published plaintext is the spelling-preserving decipherment, not silently corrected Russian. [Aligned table](https://scirealm.org/CyrillicProjector.html), [second transcript](https://elonka.com/kryptos/cyrillic.html).

A scan of the 31 August 1982 KGB document independently corroborates the beginning of the second textual source. Its heading begins at the same semantic boundary as the phase change found below. The scan does not establish how every spelling difference entered the artwork. Its provenance page identifies the Nancy Drysdale gallery files, Box 7. [Document provenance](https://www.elonka.com/kryptos/sanborn/kgb.html), [Russian scan](https://www.elonka.com/kryptos/sanborn/KGBCyrillic.jpg).

### Antipodes: corroboration, not another independent cipher family

The museum identifies the 1997 object as accession 98.22. The contemporary research record describes repeated Kryptos material and a Cyrillic continuation solved in 2003. Therefore its shared passages must not be counted as independent training examples or evidence for a new K4 method. The additional Cyrillic passage is a possible extension corpus, but this pilot does **not** claim fresh photo-level validation or a full independent re-encryption of that continuation. Versions, repetitions, missing MEDUSA, punctuation and layout changes must be resolved before mixing transcripts. [Museum record](https://hirshhorn.si.edu/collection/artwork/?edanUrl=edanmdm%3Ahmsg_98.22), [Dunin's version/history record](https://www.elonka.com/kryptos/sanborn/antipodes.html).

Other Sanborn works were not admitted merely because they contain letters, projections or historical text. No independently validated new aligned corpus for another artwork was established in this focused audit.

## 3. Exact conventions and executed results

All coordinates below are one-based unless explicitly labelled otherwise. Reported hashes are SHA-256 of the indicated UTF-8, unspaced strings. Full source text is retrieved at runtime, not bundled.

### K1 and K2

The alphabet used for both plaintext and ciphertext is:

`KRYPTOSABCDEFGHIJLMNQUVWXZ`

Let index_A mean a zero-based index in that alphabet. Encryption is:

`cipher = A[(index_A(plain) + index_A(key)) mod 26]`.

K1's period is 10, using PALIMPSEST. The parsed sculpture has 63 letters. At position 57:

- plain L + key C produces cipher K;
- plain Q + key S also produces cipher K;
- plain L + key S produces cipher W.

Thus changing the standard-key decipherment's Q to L and changing that one key occurrence S to C reconstructs **all 63** inscribed symbols. This verifies a local equivalence; it is not an exhaustive character-by-character transcription of every worksheet key row and does not distinguish intent.

K2 uses ABSCISSA, period 8. The sculpture excerpt has 369 alphabet letters and three literal question marks. The question marks do not consume key positions in the verified construction. The corrected published plaintext has 370 alphabet letters. Encrypting it and removing its **362nd ciphertext letter, S**, reproduces all 369 observed letters exactly. Equivalently, insert S after observed letter 361, immediately before the final eight letters. The old deciphered ending is WESTIDBYROWS; the corrected ending is WESTXLAYERTWO. This is a confirmed historical omission, not authorization to alter K4.

At K2 alphabet-letter position 115, O/S produces E and U/S produces R. This reproduces the worksheet/inscription difference without assigning it to a specific production event.

### Cyrillic Projector

Plaintext and key-index alphabet N, with Ё absent:

`АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ`

Ciphertext/tableau alphabet C:

`ТЕНЬАБВГДЖЗИЙКЛМОПРСУФХШЦЧЩЪЫЭЮЯ`

Key: `МЕДУЗА`, period 6.

The verified equation is **not** the K1/K2 keyed-plaintext equation:

`cipher = C[(index_N(plain) + index_N(key)) mod 32]`.

The ciphertext alphabet's exact Ш/Ц/Ч ordering matters. Do not regenerate it by mechanically prefixing ТЕНЬ to the ordinary alphabet and deduplicating. That plausible reconstruction fails 105 positions in the full test.

Normalization:

- Remove whitespace and source annotations.
- Preserve the literal Latin MEDUSA as an annotation, not encrypted Cyrillic. It lies after Cyrillic symbol 480.
- Count only Cyrillic symbols for the reported cryptographic positions.
- In Dunin's mixed-script transcript only, explicitly convert ASCII ABCEHKMOPTX to Cyrillic АВСЕНКМОРТХ after removing the complete MEDUSA token.
- Do not replace Ё, correct Russian spelling, reorder the alphabet, or translate letters automatically.

Executed regression results:

- Two published ciphertext transcripts agree on **1,133/1,133** normalized Cyrillic symbols.
- Continuous period-six key: **777/1,133** published plaintext symbols match; all 356 remaining positions differ.
- Restart key at Cyrillic position **778**: **1,133/1,133** match, and full re-encryption has Hamming distance **0**.
- Testing downstream phase deltas 0–5: only delta 3 matches the final 356 symbols; every other delta has 777 total matches.
- Ordinary deduplicated ТЕНЬ alphabet control: **1,028/1,133** matches.
- Applying a Kryptos-style keyed plaintext/key lookup with the same displayed CP letters: **62/1,133** matches.

These controls detect convention mistakes. They are not probability estimates or blind discovery statistics: the aligned decipherment and historical method were already known.

The semantic boundary is after symbol 777, before the second source text's heading. In the published physical rows, symbol 777 is row 22, column 32 and symbol 778 is row 22, column 33. It is **not** the physical panel boundary, which follows symbol 566, nor a new printed line. Hence physical line resets and semantic-message resets are different hypotheses.

Normalized ciphertext hash:

`d7233bdf379ecff94694f7dca3d2cdec8cd51e44e7d1116de24842a67aee988b`

Published spelling-preserving plaintext hash:

`84be71b155da1704e34977a0dbc95ecb3f81550037517232a461f428602b6886`

### Why the historical gap does not identify missing letters

The mirrored early solution describes a gap length congruent to 3 modulo 6 near its positions 777–780. Its text does not explicitly define zero/one-based indexing or whether the literal Latin word participates in its count. Do not quietly resolve those uncertainties by assumption. [Original method/errata](https://www.elonka.com/kryptos/mirrors/CPSolution.html).

Under this audit's explicit counting, the phase change is exactly before symbol 778. Restarting a period-six key there changes its old phase 3 to phase 0, equivalent to advancing it by 3. Adding 3, 9, 15, … hypothetical consumed positions gives the same subsequent phase. The retained ciphertext cannot distinguish those lengths, a restart, or other equal phase changes. It supplies no missing letters and no unique original-production event.

Similarly, skipping the six-letter literal MEDUSA and consuming six key steps have the same downstream effect. The known data cannot determine which mental procedure Sanborn used. These are **identifiability limits**, not evidence for additional hidden instructions.

## 4. Recommended bounded K4 pilot

This is a preregistration proposal for a later candidate-model test. No K4 error variants were evaluated in this audit.

### Freeze first

1. Preserve canonical K4 and the current crib coordinate conventions. This audit's independently fetched reference is 97 letters with SHA-256 `eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab`.
2. Keep alternatives as labelled shadow observations with explicit index maps. Never replace the canonical field, move crib coordinates until they fit, or hide length changes.
3. Freeze the candidate cipher families, key sets, test order, total hypothesis count and scoring rules before examining modified-K4 results.

### Smallest motivated error channel

Alongside an unchanged baseline, allow **at most one** event in a separate sensitivity arm:

- one ciphertext substitution: 97 × 25 = 2,425 raw alternatives;
- one missing intended ciphertext letter: 98 × 26 = 2,548 raw insertion alternatives;
- one extra observed ciphertext letter: 97 raw deletion alternatives.

Total: **5,071 raw alternatives including the baseline**, before deduplication. This counts only text-channel variants, not multiplied cipher families, keys, transformations or crib placements. Report that larger total too. The single-deletion K2 event directly motivates the missing-letter arm; K1/worksheet discrepancies motivate local robustness, not arbitrary combinations.

A local worksheet-key anomaly is a distinct stage model. Do not silently combine it with the text-channel arms or treat mathematically equivalent outputs as independent evidence. CP motivates considering semantic-section key initialization when an independently specified section boundary exists. It does **not** justify unrestricted phase jumps at every K4 position, nor special prior weight for its physical row boundaries after letters 4, 35 and 66.

### Acceptance and stopping rules

- Every candidate must re-encrypt through the declared error channel to the unchanged observed 97 letters, with a complete deterministic index map.
- Evaluate all applicable confirmed cribs without moving their published coordinates opportunistically. Explicitly distinguish observed ciphertext positions, latent pre-error positions and plaintext positions.
- Use no guessed complete K4 plaintext as a training target or uncounted scoring bonus. A readable phrase, a clock-related word or a selected partial crib is not a solution.
- First verify the controls in this report. A pipeline that “repairs” CP's phase restart into a uniquely claimed physical deletion fails the audit.
- Under matched random/synthetic controls, count the full search including edit locations and discarded variants. A larger error-tolerant model must outperform the unchanged arm after its additional freedom is accounted for.
- Stop the bounded arm at the preregistered search-space boundary. Report a null result as a null for that family, not proof that K4 is error-free. Expansion requires a new reason, not merely an improved-looking fragment.

## 5. Reproducibility, rights and integration

Run `python3 audit_construction.py`. It downloads five cited public pages into `.audit_cache`, extracts data without executing third-party code, checks cross-source agreement and writes numerical results. `--offline --cache-dir PATH` reruns against saved input pages. See README for exact commands and limitations.

Source-page copies, the worksheet image, the KGB image, and full aligned artwork text are deliberately **not included** in this archive. Public availability is not a redistribution licence. No licence for publicly rebundling complete Sanborn artwork text, third-party transcriptions, photographs or page prose was established. Keep runtime cache material out of a public repository unless separately cleared. The archive contains newly written analysis/code, short evidentiary fragments, technical alphabets/keys, hashes and numerical receipts.

The program does not read the user's Mac or touch the user's repository. It writes only to its chosen cache and output locations. Nothing in these results proves that K4 has a construction error, that related works share its key, or that the shared source family is a collection of independent samples.
