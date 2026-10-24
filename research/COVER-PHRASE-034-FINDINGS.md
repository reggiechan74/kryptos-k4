# Short multiword outputs: complete finite corpus test

24 October 2026 UTC. **No corpus phrase matched the original all-word initials arm.** None matched a 15-letter/all-word output in any declared dictionary or letter position. Expanded alternate-word families admit many conditional matches, and one all-word match uses third letters with the EN compound model. These are corpus/cover feasibility results, not decryptions.

[Protocol](COVER-PHRASE-034-SPEC.md), [original summary](../results/COVER-PHRASE-034-original-summary.json), [all matching references/counts](../results/COVER-PHRASE-034-original-windows.jsonl.gz), [word-boundary metadata](../results/COVER-PHRASE-034-MESSAGE-SPLITS.json), [implementation](../experiments/cover_phrase.py), [runner](../experiments/run_cover_phrase.py). [Core cover counts and exact scope](COVER-EXTRACTION-033-FINDINGS.md) are separate.

## Frozen language bank and complete coverage

The pinned, data-only Brown corpus snapshot contains 500 texts sampling 1961 US publications. The digital distribution is not evidence that Sanborn used it. No downloaded software was executed. All source hashes and the official NLTK distribution/format pins are in the [source receipt](../results/COVER-033-034-SOURCES.json). Raw corpus texts are not republished.

All 500 members were scanned: 57,340 nonempty sentence lines and 1,161,192 tagged tokens. Fixed parsing keeps ASCII alphabetic words and single A/I; punctuation, other single letters, hyphens, apostrophes and numbers break runs. It never joins across a break or sentence. Proper names remain eligible as an explicitly broad lexical filter. The entire corpus supplies the 40,210-word vocabulary used in the separate segmentation controls.

There were **2,673,853 contiguous two-to-five-word windows**, of which 1,771,338 have lengths allowed by the frozen cover/extractor models. The complete bank contains 1,335,926 distinct eligible joined strings. This is exhaustive for this snapshot and normalization, not all English. No arbitrary vocabulary-to-the-fifth-power phrase generation, target-specific phrase list or illustrative-message seed was used.

The original complete run was **2026-10-24T14:01:20.542852+00:00–14:01:29.259691+00:00**, 8.717 seconds, peak 225,230,848 bytes, within the frozen resource caps. The corpus stage itself took 8.533 seconds. No timeout or partial stage is represented as a negative.

## Results by requested subtest

- **First-letter/all-word output:** zero Brown-window matches across both ENE and EN tokenizations and both custom dictionary architectures, over their full cover-word ranges. This is a finite corpus negative, not proof that no English phrase exists.
- **Exactly 15 coverwords:** the core proves R26-ENE impossible. A30-ENE has 3,787,080 covers but no corpus-window match under any of the 12 extractors. The EN compound models have corpus matches only under N2 in this run. No N1 15-letter output matched anywhere; N2 outputs have seven/eight letters and must not be described as 15-letter messages.
- **Second/third/fourth letter of all words:** one occurrence, under A30-EN/k3/N1/all, with 168 compatible covers. Its reference is Brown `cp18`, source line 103, start token 9 (zero-based), four output words; the stored hash identifies it without marketing a selected natural-sounding answer. It is not the original ENE/BC initials interpretation.
- **Every-other-word variants:** most matches come from N2 and its two phases. Across the entire predefined family, there are **6,358 matched corpus occurrences**, **3,139 distinct joined strings**, and **3,147 distinct spaced strings**. Counts overlap between model/extractor lanes; they are not added as independent results. All references and exact cover multiplicities are retained. No actual K4 cover stream has been recovered to choose among them.

The k1 clue-derived markers are not imposed on k2–4 or on skipped-word variants. Hidden output spaces may cross a marker. Codewords, token order and every selected position stay fixed; nothing is reversed to place BC before ENE. Single-token EASTNORTHEAST, other English dictionaries, N≥3 and arbitrary schedules are outside this experiment.

## Independent verification and synthetic recovery

A separate full-position oracle verified **all 7,266 distinct positive message/lane cover counts**, processing every one of the 6,358 occurrence records in 6.66 seconds. [Audit receipt](../results/COVER-PHRASE-034-INDEPENDENT-AUDIT.json). This independently confirms recorded positive counts; it is not a second exhaustive corpus false-negative implementation. Complete tiny positive/negative languages, word-window generation and every word-split set are independently checked. A full Python 3.12 replay matches the original core, corpus records and capacity-control payloads exactly after decompression; gzip metadata differs. [Replay receipt](../results/COVER-EXTRACTION-PHRASE-PY312-REPLAY.json).

Six deterministic first-eligible model/stratum examples were used only as synthetic plants. Their control Caesar key was withheld from the solver; each recovered the full 97-letter synthetic cover and extracted output and regenerated every ciphertext letter. The dictionary/extractor was supplied. No eligible A30-ENE/15 plant was invented, and R26-ENE/15 is empty. These validate the pipeline, not a Sanborn cipher or independent hidden-message prediction.

## Chance controls: what can be claimed

Thirty-one fixed-seed draws sampled full covers exactly, conditioned on the same 97 letters/cribs and each nonempty cover-word stratum. All k/N/phase choices were applied to the same sampled cover to preserve correlation. The whole-family maximum includes both corpus membership and every two-to-five-word dictionary split.

**24 of 31 draws** produced at least one dictionary segmentation somewhere in the family; **none** produced a contiguous-corpus-window membership. Dictionary segmentation is weaker than a grammatical or meaningful phrase. Saved control records retain every output and its complete bounded split DAG/counts. [All controls](../results/COVER-PHRASE-034-original-controls.json.gz).

This is **conditional model capacity**, not a p-value for K4. The backward corpus query itself does not use actual ciphertext. Repeating that entire query under ciphertext nulls while retaining the same length, public cribs and dictionaries gives exactly the same feasible corpus bank. A phrase selected backward from over a million English strings cannot be compared with one random extracted string as though it were an observed decryption. No significance, posterior probability or likelihood ranking is reported.

## Remaining identifiability boundary

An independently grounded outer cipher must first supply a complete cover, and evidence must select the codebook/segmentation/extractor rather than permit all of them after seeing English. The known words have a meaningful external referent: a firsthand Scientific American report attributes BERLINCLOCK to the Berlin World Clock. That does not disprove meaningful words serving a second initial-reading role, but it does not establish such a role either. [Source review](COVER-033-034-SOURCES.md).

```sh
python3 experiments/run_cover_phrase.py --brown-zip /path/to/pinned/brown.zip --output-prefix /tmp/cover-phrase-replay
```

The script rejects a different corpus hash. Original compressed outputs are complete, not truncated. No K4 decryption, public push or Site change occurred. Local findings preserve both the useful conditional constraints and the much larger untested region.

Final regression: **625 tests pass on Python 3.9 and 3.12**. [Separate UTC validation receipt and full logs](../results/COVER-033-034-VALIDATION.json). Canonical ciphertext and 210 unrelated duplicate files are preserved; no publication or Site change.
