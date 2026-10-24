# Word covers and fixed extraction after decryption

24 October 2026 UTC. **The custom models are feasible and massively ambiguous; no K4 decryption was obtained.** This study starts from the 97-letter cover stream that a cipher would have to recover, not from a shorter replacement for the public cribs. The actual 97 ciphertext letters and 24 known plaintext letters are unchanged. No actual K4 cipher/key trial, push or Site change occurred.

[Protocol](COVER-EXTRACTION-033-SPEC.md), [complete core output](../results/COVER-EXTRACTION-033-ORIGINAL.json), [codebooks](../data/cover-codebooks-033.json), [native implementation](../experiments/cover_extraction.py) and [independent position-lattice oracle](../experiments/cover_extraction_reference.py) preserve exact domains. Preliminary reviewer counts were known before protocol freezing; independent reproduction is not a blind discovery. The [short-phrase add-on](COVER-PHRASE-034-FINDINGS.md) is reported separately.

## The conditional model

Consume all 97 decoded letters as complete codewords. Main custom cases assume EAST|NORTH|EAST or EAST|NORTHEAST at positions 22–34 and BERLIN|CLOCK at 64–74. This leaves complete-token runs of **21, 29 and 23 letters**. Those boundaries are assumptions, not disclosed facts. The same normalized EASTNORTHEAST can produce ENE or EN; neither segmentation is silently preferred.

Strict NATO uses the historically established 1956 vocabulary, ALFA/JULIETT and XRAY normalization. Four custom dictionaries either add EAST/NORTH(or NORTHEAST)/BERLIN/CLOCK to NATO (30 words) or replace the B/C/E/N entries (26 words). These are explicitly user-motivated models, not authenticated Sanborn codebooks. [Sources and prior coverage](COVER-033-034-SOURCES.md) distinguish historical vocabulary from invented adaptation.

| Dictionary and segmentation | Feasible total coverwords | Exact compatible cover count | Exactly 15 coverwords |
| --- | --- | ---: | ---: |
| A30-ENE: additions, EAST NORTH EAST | 15–22 | 158,540,149,214,580,072,342 | 3,787,080 |
| R26-ENE: replacements, EAST NORTH EAST | 17–22 | 27,493,275,220,775,879,424 | 0 |
| A30-EN: additions, EAST NORTHEAST | 14–21 | 100,440,147,392,998,450,816 | 608,203,972,224 |
| R26-EN: replacements, EAST NORTHEAST | 14–21 | 16,451,132,603,788,940,826 | 56,911,808,214 |

Strict NATO has **zero compatible covers**, even in a separate full word-lattice check with no assumed clue boundaries. Its aligned interpretation also lacks the required custom tokens. This rejects only that finite complete-token vocabulary, not custom or ordinary-English word-cover systems.

These are **cover counts**, not unique hidden messages or independent cipher keys. All four custom vocabularies are prefix-free, so a given complete cover has a unique tokenization within its declared vocabulary. In replacement dictionaries, first letters give one codeword per letter, making N1/k1 message counts equal cover counts. Added dictionaries have synonyms sharing an initial; their distinct-initial-message counts are bounded below by the corresponding replacement count and above by the added cover count. For example, ECHO/EAST can replace each other in an unknown four-letter slot without changing its initial. We do not claim exact distinct-message counts for all generalized extractors.

## Fifteen words and the extraction sensitivity

For A30-ENE, 15 coverwords force filler counts (3,4,3), hence the necessary N1/k1 pattern **???ENE????BC???**. ENE starts at output letter 4 and BC at 11. The general 15–22 case permits ENE at 4–6 and the designated BC at 11–16; incidental earlier occurrences are not forbidden. These bounds depend on this vocabulary and aligned-token assumption. They are not universal English bounds. The 26-word replacement model's 15-word case is empty because its longest word is seven letters. Other dictionaries or compound policies can change the result.

Fixed letter positions are applied consistently to every selected word:

| Letter position | EAST NORTH EAST | EAST NORTHEAST | BERLIN CLOCK |
| --- | --- | --- | --- |
| 1 | ENE | EN | BC |
| 2 | AOA | AO | EL |
| 3 | SRS | SR | RO |
| 4 | TTT | TT | LC |

Schedules are all words (N1) and every other word (N2), both global phases. The counter never restarts at clues or gaps. There are 12 extractors per nonempty model/stratum and **84 lanes** overall. No arbitrary per-word index is fitted. Too-short selected words fail rather than being skipped; frozen coverwords all have at least four letters. On exactly 15 coverwords, N1 gives 15 output letters, while N2 gives 8 or 7. N≥3, varying per-word positions, partial words and other vocabularies remain untested.

The example SIERRA CHARLIE EAST NORTH EAST gives SCENE, but it is hypothetical and was not a target or seed. It does not determine the rest of a 97-letter message. Output word boundaries are independent: the short-phrase test allows a clue-derived substring to cross output spaces.

## What actually ran

The core run was **2026-10-24T13:55:39.526279+00:00–13:55:39.790810+00:00**, 0.264 seconds, peak 16,138,240 bytes. Exact generating-polynomial counts agree with an independent full-position word lattice. Complete tiny positive/negative output languages are checked against word-sequence enumeration. Twenty-one synthetic Caesar controls recover their hidden control key, full cover and segmentation and regenerate all 97 synthetic ciphertext letters; 252 fixed-message count checks agree with the independent oracle. The codebook/extractor is supplied in those controls, so this is not unknown-codebook cryptanalysis. Actual K4 ciphertext is never scored under that control cipher family.

Without an independently constrained outer cipher, the counts are a feasibility construction. An unrestricted length-97 additive key can fit any chosen length-97 cover algebraically; that fact does not recover a key or select a message. No such arbitrary key was fitted here. Historical grounding must select a codebook and cipher before an English-looking output can become evidence.

```sh
python3 -m unittest discover -s tests -p 'test_cover*.py'
python3 experiments/run_cover_extraction.py --output /tmp/cover-core-replay.json
```

The general family is recorded as non-identifiable at present, with exact tested limits and missing cipher/codebook evidence. This work remains local only.

Final regression: **625 tests pass on Python 3.9 and 3.12**. [Separate UTC validation receipt and full logs](../results/COVER-033-034-VALIDATION.json). Canonical ciphertext and 210 unrelated duplicate files are preserved; no publication or Site change.
