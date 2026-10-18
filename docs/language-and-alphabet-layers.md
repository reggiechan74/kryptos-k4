# K4: ancient languages, alternative alphabets, and translation layers

Research date: 18 October 2026. This is a hypothesis assessment and experimental design, not a proposed decryption. No external repositories were executed, paid solution checks submitted, or third parties contacted.

## Bottom line

A language or script layer is possible in principle, but it becomes useful only when it specifies an independently motivated, reproducible conversion. “Try ancient languages” is too unconstrained. The strongest first experiments are small, historically documented encodings that can be rejected by exact round-trip and crib tests.

Shavian deserves a bounded test because it existed before Kryptos, but it is an alternative alphabet for **English**, not an ancient or dead language. It is not a 26-letter alphabet. Greek, Latin, Russian/Cyrillic, and Egyptian-related material have more specific connections to Sanborn or Kryptos than Shavian does; none of those connections establishes a K4 language layer.

There is already a cheap elimination: the two ciphertext Qs at positions 26–27 correspond to English N and O. Consequently, no overall context-free, one-cipher-symbol-to-one-English-letter substitution can satisfy the known clues. Renaming the alphabet cannot fix that. This does **not** eliminate an alphabet layer combined with transposition, polyalphabetic substitution, fractionation, or variable-length encoding.

## 1. Four different operations

| Operation | What changes | Example of the relevant distinction | What must be specified |
|---|---|---|---|
| Translation | Language and wording | English into Latin; meanings survive approximately, exact wording need not | Period/dialect, lexicon, grammar, chosen wording, and reverse-translation rule |
| Transliteration | Written representation | Cyrillic text into Latin-script character sequences | Exact table, treatment of digraphs/diacritics, direction, and ambiguities |
| Phonemic respelling | Orthography via pronunciation | English conventional spelling into Shavian | Pronunciation standard, proper names, compounds, word breaks, and spelling conventions |
| Cryptographic substitution/encoding | Symbols or their representation under a formal rule | A keyed alphabet, a coordinate pair, or a numeric encoding | Alphabet order, mapping, key, framing, padding, and inverse |

These can be composed, but they should not be conflated. A script is not a language: Greek-script English is not automatically Greek, and Cyrillic can write languages other than Russian. Egyptian hieroglyphs and Coptic also are not interchangeable “Egyptian alphabets.” The British Museum documents Egyptian text represented with Greek letters plus Demotic signs in the development of Coptic. [British Museum object EA10808](https://www.britishmuseum.org/collection/object/Y_EA10808)

Romanization is not automatically lossless. The Library of Congress’s introduction describes special characters, modifiers, and cases with omitted characters; discarding those features to obtain A–Z requires an additional declared rule. Its current tables are useful references, but a 1997 or later edition alone does not establish what Sanborn used in 1988–90. [ALA-LC introduction](https://www.loc.gov/catdir/cpso/romanization/intro.pdf), [table editions](https://www.loc.gov/catdir/cpso/roman)

## 2. Evidence about Sanborn, with chronology kept separate

- **Contemporary statement:** Sanborn’s letter to Agency employees dated 15 December 1989 describes a progression from International Morse and mentions “certain ancient ciphers.” That is evidence for historical cryptographic techniques, not a statement that K4 uses an ancient language. [Reproduction of Sanborn’s letter, page 1](https://www.thekryptosproject.com/kryptos/cia/thecryptogram/pdfs/Binder2.pdf)
- **Title:** CIA identifies *Kryptos* as Greek for hidden and dates the dedication to 3 November 1990. A Greek title supplies a thematic lead, not an encryption alphabet. [CIA’s sculpture history](https://www.cia.gov/legacy/headquarters/kryptos-sculpture)
- **First-person artistic context:** In his 2009 Smithsonian interview, Sanborn discusses his archaeology background, visual interest in Greek/Russian/Arabic lettering, Latin and Indigenous-language texts, and multilingual works. He distinguishes the encrypted Cyrillic Projector from later legible multilingual pieces, which he describes as a language-based code in an artistic sense. This supports taking language seriously while cautioning against treating every foreign inscription as encryption. [Smithsonian oral history](https://www.aaa.si.edu/collections/interviews/oral-history-interview-jim-sanborn-15700)
- **Actual Russian cryptographic artwork:** A UNC Charlotte archival walking-tour entry dates Cyrillic Projector to the early 1990s and its university purchase to 1997. It identifies the decrypted material as Russian KGB documents. This is a concrete related-work lead, but postdates Kryptos. [UNC Charlotte archivist’s entry](https://theclio.com/tour/2021/6)
- **Later related sculpture:** The Hirshhorn dates its *Antipodes* to 1997. Its existence cannot independently establish a pre-1990 K4 mechanism. [Hirshhorn collection record](https://hirshhorn.si.edu/collection/artwork/?edanUrl=edanmdm%3Ahmsg_98.22)

The targeted sources reviewed did not yield a documented Sanborn–Shavian connection. That is an absence of supporting evidence in this search, not proof that he never encountered it.

## 3. Evidence-weighted shortlist

These are research priorities, not numerical probabilities. Historical availability is a necessary screening condition, not positive evidence of actual use.

| Priority | Candidate | Why it merits consideration | Main obstacle / first useful test |
|---|---|---|---|
| Baseline | English in the existing Latin/KRYPTOS alphabet | Public English cribs and the solved sections provide direct grounding | Every new layer must beat this simpler baseline under the same scoring and search budget |
| Secondary | Greek or Latin | Greek title; documented classical/linguistic interests | Specify ancient/modern Greek or a Latin convention. A title or artistic interest does not select a text, alphabet order, or cipher |
| Secondary | Russian/Cyrillic | A genuinely encrypted related Sanborn artwork | Establish a pre-1990 bridge, exact Cyrillic inventory, romanization, and cipher before treating this as K4 evidence |
| Exploratory | Egyptian language or Coptic | Egyptian subject matter is relevant to Kryptos’s Carter passage | Choose a particular language stage and script. Tutankhamun-related subject matter is not evidence of Egyptian-language plaintext |
| Exploratory, tightly bounded | Shavian | A documented pre-1990 English orthography with distinctive structure | No specific artist link found; 48-symbol inventory, phonemic ambiguity, and A–Z output need explicit handling |
| Lower | Arabic | Appears in Sanborn’s later account of his artistic practice | Classical/modern variety, vowel treatment, and transliteration must be fixed; no K4-specific link established |
| Lower | Biblical Hebrew, Sanskrit, other ancient languages | Historically available, but that is a very broad criterion | No specific K4 link found here; choosing texts and conversions after seeing attractive output creates too much freedom |

Calling the whole list “dead languages” is misleading. Modern Greek, Hebrew, and Arabic are living languages; historical varieties, script choices, and liturgical usage must be named separately. There is no reason to exhaustively sweep every ancient language before establishing a concrete encoding model.

## 4. Shavian: plausible chronology, substantial modeling requirements

The Unicode specification identifies Shavian as a 1950s invention for English and records the 1962 bilingual-script edition of *Androcles and the Lion*. It describes **48 letters**, no letter case, a proper-name mark, and eight letters that are mandatory ligatures in that system. The first two ten-letter groups are related by 180-degree rotation. These facts offer testable structural hypotheses, but no direct Kryptos connection. [Unicode, §8.16](https://unicode.org/versions/Unicode17.0.0/core-spec/chapter-8/)

Kingsley Read’s 1963 spelling guide and the 1962 *Androcles* conventions are appropriate historical anchors. The modern Shavian spelling guide explicitly notes that it updates some of Read’s spellings. Therefore a modern converter must not silently stand in for a 1990-era convention. [Spelling guide and link to Read’s original](https://shavian.info/spelling/)

Three pitfalls matter:

1. **Alphabet-size mismatch.** A globally one-to-one mapping of all 48 Shavian letters into one A–Z letter each is impossible: there are only 26 outputs. This does not rule out a message using at most 26 Shavian symbols, context-dependent decoding, a variable-length code, or block packing. Each is a distinct hypothesis requiring its own rule.
2. **Pronunciation is not English spelling.** A purely phonemic mapping can collapse homophones such as *right* and *write*. Reconstructing exact conventional spelling requires context, a constrained dictionary, or extra information. Likewise, the pronunciation of a proper name such as Berlin must be chosen before evaluating candidates. A readable back-translation is weaker evidence than recovery by a specified inverse.
3. **Modern numerical labels are anachronistic evidence.** Shavian’s Unicode allocation is documented in Unicode 4.0, from 2003, with encoding proposals in 1997 and 2001. A modern code-point number, keyboard layout, or library ordering may be a convenient implementation label; it is not evidence for Sanborn’s original arithmetic. An alleged pre-1990 numerical order needs a historical source. [1997 proposal](https://www.unicode.org/L2/L1997/97103-shavian.pdf), [Unicode 4.0 Shavian chart](https://www.unicode.org/charts//PDF/Unicode-4.0/U40-10450.pdf)

Do not substitute visual glyph similarity for an encoding table. Selecting whichever Latin letter a Shavian glyph resembles best is not a determinate decoder.

### Cheap Shavian length checks

These are mathematical deductions, not claims about Sanborn’s method:

- Exactly two Latin letters per Shavian symbol, followed only by length-preserving operations, produces an even length. It cannot produce 97 characters without a declared framing, padding, or exception rule.
- Variable-length and block encodings can yield 97. Therefore odd length alone does not reject Shavian.
- Arbitrary 97-symbol Shavian strings contain a larger state space than arbitrary 97-letter Latin strings: about 542 versus 456 maximum bits. A lossless, equal-length conversion for every possible string is impossible. Natural-language restrictions, shorter intermediate strings, or extra information change that conclusion.

## 5. Where the English cribs constrain a multilayer model

Use one-based indexing:

| Positions | Ciphertext | Public plaintext |
|---|---|---|
| 22–34 | FLRVQQPRNGKSS | EASTNORTHEAST |
| 64–74 | NYPVTTMZFPK | BERLINCLOCK |

The letters and alignment are recorded in the contemporary researcher account of the EAST disclosure and in Dunin’s reference page. [August 2020 clue report](https://scienceblogs.de/klausis-krypto-kolumne/2020/08/24/jim-sanborn-publishes-another-new-kryptos-clue/), [Dunin’s reference page](https://www.elonka.com/kryptos/)

The standard ciphertext has 97 letters. A local consistency check confirmed both spans, all 26 ciphertext letters being present, and the substitution contradictions described below. The ciphertext source is [Dunin’s transcription](https://www.elonka.com/kryptos/transcript.html).

**Do not force these English letter positions onto an intermediate language.** A viable model could be:

English message → specified foreign-language rendering → specified romanization/encoding → encryption → 97 Latin ciphertext letters.

Or:

English message → Shavian spelling → symbol encoding → encryption → 97 Latin ciphertext letters.

The full decoder must return the confirmed English strings at their reported locations in the normalized final output. Intermediate stages may change length. If translation changes lengths, the model must explain the alignment between final English and ciphertext; it cannot simply assert that a foreign word at intermediate position 64 satisfies BERLIN at English position 64.

In the usual 97-letter English-plaintext working model, both endpoints have 97 letters; that still does not require every intermediate stage to have 97 symbols. The cribs by themselves do not prove that every unexposed plaintext position contains English, or identify the cipher class.

### What is ruled out already

- Ciphertext Q at positions 26 and 27 would have to decode to N and O. A fixed symbol-to-letter decoder cannot do both.
- Conversely, the same English letter E occurs in the cribs with ciphertext F, G, and Y. A fixed letter-to-symbol encoder cannot do all three.
- These contradictions rule out a complete plain monoalphabetic substitution at the published alignment. They do not rule out a substitution *component* inside a multilayer system.
- Merely relabeling 26 symbols with Greek, runic, or invented glyphs introduces no distinct cryptographic evidence. It becomes a new test only if the script supplies a specific order, geometry, grouping, or other operation. Renaming arbitrary substitution keys otherwise duplicates an existing search family.

### What ordinary translation fails to supply

An English→Latin→English round trip generally is not an inverse. Multiple wordings can express the same meaning. To claim a reproducible cryptosystem, specify a finite phrasebook, canonical vocabulary/grammar, a stored text with a known translation, or another mechanism that recovers exact text. A codebook can do this, but then the identity and indexing of that codebook are part of the key.

## 6. Falsifiable experiment sequence

### A. Freeze a manifest before searching

Record the ciphertext transcription, indexing, exact cribs, candidate family, historical source/edition, symbol inventory/order, normalizations, forward and reverse transformations, permitted keys, and every variable. Preserve spaces and punctuation in a separate representation if they carry information. Declare whether diacritics, I/J or U/V, Shavian ligatures, proper-name marks, or vowel marks are retained, merged, expanded, or omitted.

Reject any candidate that requires an unannounced correction, insertion, deletion, dialect switch, alphabet reorder, or new key after inspecting output. If a genuine new variant is worth testing, register it as a new experiment and count it toward the search budget.

### B. Unit-test the encoding, before K4

- Round-trip all individual symbols and ambiguous combinations.
- Use English test sentences outside Kryptos, including homophones, proper names, repeated words, and punctuation.
- For a lossy transformation, expose every ambiguity and state the side information or canonicalization that resolves it. Do not call a lossy round trip exact.
- Check output lengths and framing. A two-character code with no header fails the 97-character requirement immediately if all subsequent steps preserve length.

### C. Test the strongest small families first

1. **Alphabet relabeling audit:** eliminate models mathematically equivalent to a previously tested substitution family. Apply the crib-collision tests before any language-model scoring.
2. **Historically fixed romanization:** choose one sourced pre-1990 convention for one candidate language; combine it with a small, explicitly selected cipher family. Stop if no member satisfies the exact constraints. Do not generalize that result to all conceivable uses of that language.
3. **Shavian literal encoding:** choose the 1962/1963 convention, one independently justified encoding, and a bounded cipher family. Enumerate phonemic/spelling ambiguities explicitly. Do not let a modern transliterator silently choose the answer.
4. **Specific historical source-text hypothesis:** test a named pre-1990 text/edition and a specified extraction rule. A complete text plus arbitrary extraction is effectively an unlimited key, not a meaningful prediction.

### D. Separate fitting from validation

If parameters are fitted using EASTNORTHEAST, hold BERLINCLOCK out until those parameters are frozen; also reverse the roles. This is an engineering cross-check, not genuine unseen historical evidence, since both cribs are already public and may have influenced model choice. Never give extra evidential weight for reproducing a crib that was imposed as a hard constraint.

Require additional performance: coherent non-crib text, no invented repairs, a short independently motivated key, and a complete forward encoding that reproduces every ciphertext letter. A freely chosen 97-letter keystream can encode any chosen 97-letter message, so round-trip alone is necessary but not sufficient.

### E. Control multilingual false positives

- Compare each candidate against language-matched corpora normalized exactly the same way. English n-gram scores cannot be directly compared with raw Latin, Russian, or Shavian scores.
- Calibrate on equal-length genuine snippets, shuffled controls preserving relevant counts, and random keys under each tested family.
- When cribs are forced, force them in the null experiments too. Otherwise the candidate receives an unfair scoring advantage.
- Count all tried languages, spellings, alphabet orders, segmentations, keys, and postprocessing variants. Evaluate the maximum score from the whole search, not a single attractive result in isolation.
- Keep retrieval, scoring, and validation corpora separate. Avoid training or retrieval leakage from Kryptos pages and the published crib phrases.
- Ask a fluent reader to judge an anonymized full output only after the mechanical tests pass. A model’s fluent English gloss is not evidence that an ungrammatical foreign string is a real plaintext.

## Recommended next decision

Keep the language-layer idea, but turn it into two bounded branches: (1) a documented classical/Cyrillic romanization model with an independently motivated cipher; (2) a historical Shavian model with an explicit, reversible A–Z representation. First eliminate contradictions and redundant relabelings. Expand to another language only when a source or a measurable result supplies a reason.

At present, the defensible conclusion is **possible but unsubstantiated**. The useful progress is in making models rejectable, not in accumulating more languages or plausible-sounding translations.
