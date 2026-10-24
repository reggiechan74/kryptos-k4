# Candidate-first 048: fixed-source preflight leaves no admissible message

**All 582 registered model descriptions were checked;42 pass the known-crib consistency test, but none admits a key in the fixed Brown source bank.** There are zero compatible full plaintexts, zero model/key aliases and zero matching source occurrences. No candidate-message bank was generated, as the [audited protocol](CANDIDATE-FIRST-048-SPEC.md) expressly requires when exact source-key preflight is empty. This is not a claim that candidate-first reasoning, another source text or an unknown key is exhausted.

[Original receipt](../results/CANDIDATE-FIRST-048-ORIGINAL.json), [complete Python 3.12 replay](../results/CANDIDATE-FIRST-048-REPLAY.json), [engine](../experiments/candidate_first_048.py), [replay UTC/resource logs](../results/048-050-REPLAY-VALIDATION.json).

The 582 descriptions are two alphabets × three explicit modular equations × (periodic lengths 1–32, plaintext-autokey primers 1–32, ciphertext-autokey primers 1–32, running key 97). Canonical 97 letters and all 24 English positions are unchanged. The 42 structural survivors are exactly the 18 periodic cases at 27–29,18 plaintext-autokey cases at 27–29 and six running-key cases; a free key can fit them, which is not evidence. All shorter direct cases fail before candidate generation. Source admission is an exact contiguous normalized passage, phase 0, within one of 500 separately normalized Brown documents:4,745,928 letters. Corpus ZIP and ordered normalized stream hashes are retained. Brown samples 1961 publication and is historically possible material, but is not creator-selected and was already inspected in earlier studies.

Source lookup uses the longest fixed seed substring only as a lossless index, then checks the full source-key mask, complete stream consistency, all 24 clues and exact 97 letter re-encryption. Arbitrary derived keys, approximate English keys, post-hoc book hunts, rotations or repaired ciphertext are not accepted. Exact preflight already determines every compatible plaintext in this model: a thematic bank could only intersect that set and could not expand cipher coverage. Because that set is empty, authoring 1,000 dependent clause assemblies would be irrelevant here. The count of independently model-written whole messages and the count of assembled messages are both zero; no thousands-of-guesses claim is made.

Before actual K4 evaluation,3,612 complete tiny source/key/plaintext relations, containing 7,956 accepted pairs, matched independent sequential decryption. All 24 real-sized synthetic acceptance plants retained their true source keys and regenerated 97 ciphertext letters, including the hidden 73 positions; uniqueness was not presumed. The 31 complete crib-conditioned null preflights also admit zero full plaintexts. Their primary statistic is distinct compatible full plaintexts; descriptions, keys and source occurrences are separate. These nulls are not a universal p-value. In particular, periodic/running-key source constraints depend only on anchored cipher cells and can remain invariant under the declared 73-position shuffles. No significance or thematic English promotion follows.

The original calculation runs 2026-10-24 T 19:40:49.963515+00:00 to 19:40:52.486912+00:00. Python 3.12 replays every semantic result exactly, with separate UTC timing; measured replay wall time 2.39 seconds and maximum RSS 32,849,920 bytes are in its log. No resource gate was approached or relaxed. No language model service, paid checker, submission, new credential, Site edit or push was used. The primary-supported Berlin/Egypt/message-delivery themes remain optional generation priors; the letter's chronology conflict was not repaired into a plaintext fact.

Remaining scope includes other independently fixed source editions, key phases, lengths beyond 32, other constructors and route/cipher layers. An unrestricted 97 letter additive key can fit arbitrary guessed plaintext and is not confirmation. Existing source-codec/running-key coverage and [prior-overlap boundaries](048-050-PRIOR-COVERAGE.md) remain explicit.

Final integration: all 718 tracked tests pass on Python 3.9 and Python 3.12; [UTC suite receipt and complete logs](../results/048-050-FINAL-VALIDATION.json). Original experiment, scientific replay and regression times are recorded separately. No public push occurred.

Reproduce from repository root, preserving original receipts:

```sh
python3 experiments/candidate_first_048.py --brown /path/to/hash-pinned-brown.zip --output /tmp/candidate-first-048-replay.json
```

The source ZIP is external data, not installed software. Existing compressed catalogues are checked exactly instead of silently overwritten. New replay files receive new UTC times.
