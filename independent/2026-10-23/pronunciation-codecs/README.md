# Dictionary-pronunciation alternatives: bounded feasibility audit

## Useful result

Three independently documented notation families were frozen, counted and checked without searching keys or crib offsets. None supplies a literal same-character-count replacement for both disclosed 13/11-character blocks. A new necessary condition also rejects a larger **stateless concatenative encoding** family: the first phonetic block starts and ends with EAST, while its fixed ciphertext block has no repeated prefix/suffix.

This is not an exclusion of pronunciation preprocessing followed by a stateful cipher, transposition or other independently specified outer transformation. It is not evidence of Sanborn's intent or a K4 solution.

## Frozen sources and spellings

All sources were accessed on 2026-10-23. Source spelling, dialect, stress policy and whole lexical alternatives were fixed in `spec.json` before the program was run. The public crib sizes were already known during source selection; this is a working freeze, not blind preregistration or a repository commit.

### 1. CMU ARPABET

Dictionary commit: `74790861f652b15e4ac49015a90074ad62a27690` (24 October 2025). Its dictionary body was retrieved and verified identical to the retrieved master body. Exact selected lines:

| Headword | Source transcription |
|---|---|
| EAST | IY1 S T |
| NORTH | N AO1 R TH |
| NORTHEAST | N AO2 R TH IY1 S T |
| BERLIN | B ER0 L IH1 N |
| CLOCK | K L AA1 K |

No numbered alternate occurs for these five headwords in that snapshot. Remove vowel stress digits 0/1/2, then concatenate the phone labels. Token/word boundaries remain in metadata. Do not replace the dictionary's ER0 in BERLIN with a more convenient spelling or vowel.

Primary sources: [fixed dictionary](https://raw.githubusercontent.com/cmusphinx/cmudict/74790861f652b15e4ac49015a90074ad62a27690/cmudict.dict), [39-phone inventory](https://raw.githubusercontent.com/cmusphinx/cmudict/74790861f652b15e4ac49015a90074ad62a27690/cmudict.phones), [symbol inventory](https://github.com/cmusphinx/cmudict/blob/74790861f652b15e4ac49015a90074ad62a27690/cmudict.symbols), [CMU README](https://github.com/cmusphinx/cmudict/blob/74790861f652b15e4ac49015a90074ad62a27690/README).

Historical qualification: Lloyd Rice's April 1976 article explicitly describes ARPABET and prints its one- and two-character forms. Thus the notation predates 1990. The current CMU lexicon is only a reproducible modern pronunciation source, not proof those exact entries existed in 1990. Rice's original vocabulary, inventory and stress conventions are not silently equated with modern CMUdict. [Original article, printed pp. 6–8 / collected volume pp. 92–94](https://archive.org/details/dr_dobbs_journal_vol_01?view=theater), [readable transcription](https://archive.org/stream/dr_dobbs_journal_vol_01/dr_dobbs_journal_vol_01_djvu.txt).

### 2. Original English SAMPA, separate UK model

SAMPA is not a dictionary. Freeze Cambridge's current UK lexical entries, then apply the independently documented English SAMPA table. The source entries are EAST iːst, NORTH nɔːθ, NORTHEAST ˌnɔːθˈiːst, BERLIN bɜːˈlɪn, CLOCK klɒk. BERLIN is the English city-name pronunciation, not German.

Remove stress and boundaries, retain vowel length. The relevant mapping is iː→i:, ɔː→O:, θ→T, ɜː→3:, ɪ→I, ɒ→Q, with b k l n s t unchanged. Case is meaningful. This is a separate UK/non-rhotic model, not a US stream with the inconvenient r deleted. No US/UK forms are combined.

Lexical sources: [east](https://dictionary.cambridge.org/us/pronunciation/english/east), [north](https://dictionary.cambridge.org/us/pronunciation/english/north), [northeast](https://dictionary.cambridge.org/us/pronunciation/english/northeast), [Berlin](https://dictionary.cambridge.org/us/pronunciation/english/berlin), [clock](https://dictionary.cambridge.org/us/pronunciation/english/clock). The retrieved copies were cached on 2026-10-22; the UK/US labels and phonetic strings are recorded in `source-excerpts.json`.

Primary coding/historical sources: Wells's [July 1989 paper](https://doi.org/10.1017/S0025100300005892), and the [EAGLES 1995 SAMPA specification](https://latel.upf.edu/morgana/altres/cibres/EAGLES_SLWG_1995/node85.htm), English section. The latter records development in 1987–89 and lists the language-specific inventory. The 1989 journal paper, not its 2009 online-upload date, establishes pre-1990 availability.

**X-SAMPA is different.** Wells's general extension is dated 28 April 1995 in the [W3C specification bibliography](https://www.w3.org/TR/2006/WD-pronunciation-lexicon-20061026/#Informative-References). It can be a modern serialization control but is not a plausible named pre-1990 system without separate evidence. The UCL primary PDF and legacy pages could not be retrieved in this pass; no new X-SAMPA cipher model or purported 1990 X-SAMPA alphabet was introduced.

### 3. American Heritage dictionary respelling

Freeze the current Fifth Edition online entries. Exact source forms, with primary stress displayed here as its original U+E01F glyph:

| Headword | Source transcription |
|---|---|
| EAST | ēst |
| NORTH | nôrth |
| NORTHEAST | nôrth-ēst ; nôr-ēst |
| BERLIN, city | bûr-lĭn |
| CLOCK | klŏk |

Both complete NORTHEAST alternatives are retained; no post-fit choice or combination is allowed. The separate lowercase carriage entry for berlin is not a city-name variant. HTML was inspected for NORTHEAST and BERLIN to exclude spaces introduced around font spans by text extraction.

Normalize to NFC and remove stress marks, syllable hyphens, enclosing delimiters and interword spaces. Preserve all vowel diacritics and the th digraph. The chart-key units ôr and ûr are each counted as one **key unit**, not asserted to be one physical phoneme; characters and key units are counted separately.

Primary sources: [east](https://ahdictionary.com/word/search.html?q=east), [north](https://ahdictionary.com/word/search.html?q=north), [northeast](https://www.ahdictionary.com/word/search.html?q=northeast), [Berlin](https://www.ahdictionary.com/word/search.html?q=berlin), [clock](https://www.ahdictionary.com/word/search.html?q=clock), [publisher's pronunciation key](https://www.ahdictionary.com/application/resources/misc/pronkey.pdf), [stress and variant rules](https://ahdictionary.com/word/howtouse.html).

Historical qualification: Gertrude Hildreth's contemporaneous comparative study describes the 1969 AHD's 45 respelling symbols, including 15 digraphs, establishing a pre-1990 dictionary-respelling tradition. The exact five entries above come from the current edition; continuity with a particular pre-1990 printing has not been verified. [Spelling Progress Bulletin, Spring 1978, printed pp. 12–15, PDF pp. 23–28](https://www.spellingsociety.org/uploaded_bulletins/b78spring-bulletin-1420024612.pdf).

## Count results

The pairs always mean EAST+NORTHEAST, then BERLIN+CLOCK. UTF-8 bytes are storage counts, not evidence of a historical byte cipher.

| Model | First stream | Second stream | Tokens / key units | NFC code points | UTF-8 bytes |
|---|---|---|---|---|---|
| CMU ARPABET | IYSTNAORTHIYST | BERLIHNKLAAK | 10 / 9 | 14 / 12 | 14 / 12 |
| English SAMPA, UK | i:stnO:Ti:st | b3:lInklQk | 9 / 9 | 12 / 10 | 12 / 10 |
| AHD full TH | ēstnôrthēst | bûrlĭnklŏk | 9 / 9 | 11 / 10 | 14 / 13 |
| AHD omitted TH | ēstnôrēst | same second stream | 8 / 9 | 9 / 10 | 12 / 13 |

ARPABET is already A–Z when stress/spaces are removed, but its lengths are 14/12. Its stress-retaining compact audit is 17/15; with canonical token spaces it is 26/23. Neither is 13/11. SAMPA needs a recoding for case-sensitive letters, ':' and '3'; uppercasing loses distinctions. AHD needs a recoding for diacritics. Its raw punctuation-retaining lexical concatenations are 13/12 for full TH and 11/12 for omitted TH, so raw punctuation does not repair both windows either. No selective punctuation removal was fitted.

Every individual word's raw and normalized counts, word/token boundaries and symbol inventories are in `results.json`.

## Mapping domains and reversibility

- CMU: 39 base phone labels globally, using 24 distinct A–Z characters. The frozen words use 13 phone labels and 13 distinct characters. Stress-aware lexical labels number 69 (24 consonants plus 15 vowels times three stress values); the symbols file's 84 entries additionally include the 15 bare vowels. One letter per phone cannot inject all 39 into 26 and also gives the wrong local lengths.
- English SAMPA: 44 standard English phoneme labels, using 36 distinct characters. The frozen words use 12 token labels and 13 characters. The source's additional weak-vowel indeterminacy codes are not silently substituted. One letter per full-inventory token or character needs a restricted inventory or a non-injective/variable-length scheme; no such choice is inferred from these cribs.
- AHD: 12 chart-key units and 13 NFC characters occur in the frozen words. The complete historical key is larger than 26; the publisher's current chart also distinguishes many diacritics and digraphs. This audit does not invent an A–Z mapping for its full inventory.
- Delimited ARPABET tokens are recoverable as tokens. Removing boundaries is not universally uniquely decodable: NG can mean [NG] or [N,G]. Similar framing witnesses are SAMPA tS versus [t,S], and AHD th versus [t,h]. JSON token-array roundtrips pass for all selected words and blocks; they only demonstrate storage, not a historical cipher.
- Even perfectly recovered pronunciation is not exact recovered spelling. In the same pinned CMU snapshot, NIGHT and KNIGHT both have N AY1 T. Word boundaries, stress and spelling exceptions need a separate recovery rule if the goal is exact English plaintext.

## New structural test: repeated-edge certificate

For every frozen normalized first stream, the source-token sequence is E + M + E, where E is the nonempty token sequence for EAST. Any deterministic concatenative code h assigning each token the same nonempty A–Z codeword must yield h(E) + h(M) + h(E). Therefore its output must have a nonempty proper prefix identical to a suffix, even if individual codewords have different lengths.

The fixed target FLRVQQPRNGKSS has no nonempty proper border. In particular, its initial F never recurs. Consequently **no such code can map any frozen first stream exactly to that block**. This proves a small but real exclusion without selecting codeword lengths, enumerating a key, or assuming ordinary-letter aliases.

The test does not cover stateful/polygraphic encryption after transcription, transposition, inserted padding, or a token code that erases the whole EAST sequence. A synthetic unequal-length code provides a positive border control, and a last-character mutation breaks the expected border. Independent Python and JavaScript agree on all seven normalized stream count rows and the target's empty border set.

## Alignment is still unknown

The disclosed positions refer to ordinary English plaintext. Treating FLRVQQPRNGKSS as the entire encoded phonetic first block is an explicit extra assumption, not an established fact about K4's pipeline. Let the orthographic message be A + EASTNORTHEAST + B + BERLINCLOCK + D. Variable-length transformation/serialization moves the starts to |f(A)| and |f(A)| + |f(EASTNORTHEAST)| + |f(B)|. The unknown surrounding text prevents deriving these starts from the ordinary-English indices. None of the new representations is freely shifted against ciphertext here.

## Replay and stopping point

Run `python replay.py` inside this bundle. It writes `results.json`, checks source-to-token joins, counts, framed roundtrips, ambiguity witnesses and the repeated-edge certificate. It does not run Vigenere, Beaufort, periodic substitution, a phonetic alphabet fit, Soundex, Metaphone, crib sliding or a whole-message search. The existing IPA periodic-family campaign is not repeated. No user-computer or repository file was modified.

The next useful question is architectural, not another respelling guess: what independently motivated outer operation can preserve recoverable phonetic information while breaking the repeated EAST codeword and handling the unknown transformed alignment? A specific proposal can be frozen and tested; arbitrary recoding plus arbitrary offsets has no evidential value.
