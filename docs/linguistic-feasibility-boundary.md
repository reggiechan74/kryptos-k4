# Respelling and German translation: distinct proposals

The user proposed two different models after the completed alphabet/masking/word
sequence. H-PHONETIC-RESPELLING is English → stylized pronunciation respelling →
cipher. H-GERMAN-TRANSLATION is English → a specified German rendering → cipher.
Neither is established historical Sanborn practice. Berlin is no proof of either.

Only a small deterministic respelling subset is specified for immediate testing:
W→V and word-final D→T/G→K on explicit uppercase word tokens. These synthetic
rules preserve length. The [fixed specification](../research/specifications/PHONETIC-SUBSET-001.json)
checks their action on EAST/NORTHEAST/BERLIN/CLOCK and the same12fixed autokey
outputs. It admits no new key, pronunciation choice, segmentation, or crib shift.

TH→Z/S contracts two letters to one and short I→EE expands one to two. Their
application needs a fixed pronunciation dictionary, dialect/rule conditions,
word boundaries, and cumulative input/output alignment. Many such transformations
are lossy. No flexible mapper or language-model reconstruction is implemented.
The [phonetics source supplied by the research worker](https://pure.mpg.de/rest/items/item_355213_16/component/file_420941/content)
was cited for variation, not as an exact table licensing the user's rules; the
local executor does not claim a new reading of this source or a universal German
accent. The implementation tests only the explicitly synthetic subset.

German translation changes more than spelling: wording, word order, and length
may change. A fixed dictionary/grammar/codebook and exact reverse rule are absent.
No translator choices or German candidates were fitted to K4.

## Source-interpretation and alignment caveat

Sanborn's public clues are normally presented as directly enciphered English
letter spans. Treating their indices as applying only after a linguistic
reconstruction is an additional hypothesis, not an established interpretation.
A wholly German intermediate cannot simply replace those directly aligned English
spans without explaining exact English↔German recovery and index alignment.
This caveat does not prove that every layered or multilingual construction is
impossible; it prevents silently moving the fixed English cribs to a convenient
intermediate location.
