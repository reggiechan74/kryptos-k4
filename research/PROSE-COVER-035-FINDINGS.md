# Ordinary prose covers: length-free constraints and a complete autokey slice

24 October 2026 UTC. **Fifteen is not an observed hidden-message length.** This study removes the prior custom vocabulary, forced clue boundaries and 15-word stratum. The ordinary-lexicon models admit complete 97-letter cover paths spanning 7–79 words, with readout length determined by segmentation and selector. These are lexical feasibility bounds, not an estimate of typical prose or recovered text.

The ciphertext-facing test completes all 105,456 model/key descriptions in the smallest previously compatible plaintext-autokey lag domain. None yields a complete cover in the frozen vocabularies. This is a **narrow vocabulary-conditioned negative**, not rejection of ordinary English, autokey generally or post-decryption extraction. The lexicons also reject genuine solved text, making their incompleteness explicit. No plaintext/key was recovered and nothing was pushed or deployed.

[Preregistered protocol](PROSE-COVER-035-SPEC.md), [original full result](../results/PROSE-COVER-035-ORIGINAL.json), [engine](../experiments/prose_cover.py), [runner](../experiments/run_prose_cover.py), [independent full-domain replay](../results/PROSE-COVER-035-INDEPENDENT-AUDIT.json), [cross-version equality](../results/PROSE-COVER-035-PY312-COMPARISON.json).

## What is fixed, and what remains hypothetical

Observed inputs remain the 97 ciphertext letters and 24 confirmed English letters, not spaces. The models permit words crossing every crib edge. Neither EAST|NORTH|EAST nor EAST|NORTHEAST is forced; a known substring need not be a sequence of complete words at all. Therefore ENE/EN/BC are not universally imposed on the readout. Output word boundaries are independently unknown.

The reused, hash-pinned Brown corpus samples 1961 US print. It was already inspected in 033/034 and is **not pristine held-out data**. Three nested diagnostic lexicons are frozen: S has 40,210 alphabetic tokens (single A/I); J has 45,820 after explicitly joining internal apostrophes/hyphens; O has 45,826 after adding only prior K1–K3 artifact tokens IQLUSION, UNDERGRUUND, DESPARATLY, X, Q, WW. Proper names are allowed. These are not claimed to be Sanborn's vocabulary. O is source-calibrated, not independent confirmation. Raw corpus is not republished; [source pins and licence context](COVER-033-034-SOURCES.md) remain valid.

Punctuation may separate words without consuming letters. The internal joining alternative is explicit, not silently applied to every mark. Whole-word endpoints and the particular lexicons are assumptions; other spelling, partial-token endpoints and linguistic interpretations remain outside coverage. A word-path can be grammatically nonsensical; lexical admission is not readability certification.

## Exact boundary-free cover constraints

All 97 letters are consumed, with each known letter matched exactly. Word-edge multiplicities count literal vocabulary choices. Exact integer DP preserves position and global word count; selected short words invalidate a path. Fixed k 1..4, all-word or alternate-word selection and both alternate phases give 12 readouts per lexicon,36 model/selector descriptions. N>=3 and arbitrary per-word choices are not added.

| Lexicon | Cover-word span, k 1/all words | Output span, k 4/all words | Output span, k 1/every other, phase 0 |
| --- | --- | --- | --- |
| S | 8–79 | 8–22 | 4–40 |
| J | 7–79 | 7–22 | 4–40 |
| O | 7–79 | 7–22 | 4–40 |

The full receipt retains exact distributions for every k/N/phase, including phases with a 3-letter minimum. Ranges are model support, not uniform probabilities or ordinary-prose word-count estimates. Cover-path counts are enormous and count **word-sequence descriptions**, not unique cover strings or hidden messages: ordinary dictionaries are not prefix-free and segmentation can be ambiguous. No attractive full-mask witness was selected. Thus the known letters alone fail to identify a short-message length or extraction rule.

## Cipher-facing test: why lag 27 and what it proves

The prior [exact autokey audit](AUTOKEY-CONSTRAINT-FINDINGS.md) rejected plaintext-feedback lags 1–26. Lag 27 is the smallest compatible lag and has exactly three free root/primer symbols after all 24 crib constraints. We exhaust 26^3=17,576 settings for each of six same-coordinate constructions: AZ/KRYPTOS and C=P+K, C=P−K, C=K−P. Continuous forward feedback is K_i=P_(i−27), no reset, transposition or preprocessing.

All 105,456 descriptions completed, with zero lexical survivors even in O, the largest lexicon. Nested S/J rejection follows as well; lazy screening is not 315,000 independent cipher tests. This is not an exhaustive autokey exclusion. Longer compatible primers, mixed alphabets, other feedback/init conventions, cipher layers, unknown vocabulary and source-defined concealment systems remain open. There is no candidate cover on which to reject or confirm the second-stage readout: this domain fails **before extraction**.

A separate implementation propagates each known letter backward to its root and decrypts forward. Its complete sorted plaintext sets equal the native generator's 17,576 states per construction. An independent substring/word-set recognizer reproduces zero survivors for the whole actual domain. This is a full-domain negative replay, not just planted inclusion. Per-model hashes and independent counts are retained.

## Calibration warns against broad conclusions

| Solved stream | S complete paths | J complete paths | O complete paths |
| --- | ---: | ---: | ---: |
| K1, literal IQLUSION preserved | 0 | 0 | 2 |
| K2 restored-S stream, literal UNDERGRUUND/carriers preserved | 0 | 0 | 3,627,970,560,000 |
| K3, literal DESPARATLY and terminal Q preserved | 0 | 0 | 0 |

No calibration miss was repaired after the result. Even O fails K3 after a furthest reachable 167-letter prefix of 336. This is a demonstrated false-negative risk of the diagnostic vocabulary, not a claim K3 is not English. The enormous K2 path count also shows why dictionary segmentation is not a reliable sentence or hidden-message detector. Calibration uses all letters after explicitly removing non-letter punctuation; it does not assert a K4 delimiter scheme or force K1–K3 to share a readout.

## Controls, chance and reproducibility

Complete tiny word-path truth sets check all selectors, crossings and selected-short-word behavior; complete tiny literal-primer systems independently verify root enumeration. Six deterministic first eligible 97-letter Brown passages were encrypted with hidden 27-letter primers, one per construction. All six true full plaintext/primer pairs were retained and re-encrypted, but total lexical plaintext counts were 1,4,1,1,12,3: only three plants were unique under this lexical model. Recovery means truth inclusion, not guaranteed unique English recovery. No plant was selected to carry a desired short message.

All 31 fixed-seed null searches complete the identical six-model/three-lexicon domain (3,269,136 additional descriptions), preserving the 24 observed crib ciphertext positions while shuffling the 73 others. Every whole-family distinct lexical-plaintext count is zero. This is no positive distinction for the actual zero. Conditional exchangeability/histogram assumptions are disclosed; there is no universal cryptographic p-value. No independent expected extracted text exists, so no English-fragment promotion or extracted-output significance is computed. The previous backward corpus-bank search was not rerun as a new discovery.

Original full run:2026-10-24 T14:41:14.223979+00:00–14:41:22.639303+00:00,8.415 seconds, peak 127,942,656 bytes. All stages complete within frozen caps. Python 3.12 reproduces every semantic payload, including 36 selector distributions, all actual states/counts, six plant candidate sets and 31 nulls; timing/RSS fields are deliberately separate. The post-outcome independent replay completes in 2.105 seconds. Its initial inefficient attempt was interrupted before any completed receipt, then an immutable word-length inventory was hoisted without changing the domain; [verification note](../results/PROSE-COVER-035-VERIFICATION-NOTES.json).

```sh
python 3 experiments/run_prose_cover.py --brown-zip /path/to/pinned/brown.zip --output /tmp/prose-cover 035-replay.json
python 3 experiments/audit_prose_cover.py --source /tmp/prose-cover 035-replay.json --brown-zip /path/to/pinned/brown.zip --output /tmp/prose-cover 035-audit.json
```

## Prior coverage and stopping point

Earlier aligned periodic, Wheatstone and nonzero-strip contradictions still apply to their exact first-stage English models; adding a later extraction cannot alter those confirmed-letter equations. Length-changing *pre*-encryption IPA/codecs and ONE-EDIT are different channels. Gromark arbitrary alphabets, longer autokey primers and flexible Feistel fits are not independently decoded covers; none was completed with invented 97-letter keys or English chosen afterward. See the [scope audit](EXCLUSION-SCOPE-AUDIT-2026-10-23.md) and [current register](HYPOTHESES.md#h-word-cover-extraction).

The finite study ends here. A stronger next test needs an independently restricted outer cipher, language model calibrated to retain relevant real prose, and a source-motivated extractor. The ordinary-cover hypothesis remains non-identifiable; neither 15 nor 7–79 is a fact about K4. No additional cipher model, larger lag, extra vocabulary or desired phrase was added after the results. Local-only authorization remains in force.

Final regression: **638 tests pass on Python 3.9 and 3.12**; [separate UTC receipt and full logs](../results/PROSE-COVER-035-VALIDATION.json). Canonical ciphertext and all210 unrelated duplicate files preserved. No public push, external submission/payment or Site change.
