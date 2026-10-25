# Kryptos candidate first experiment 052

## Result

**No structural key signal was found among the 1,024 new messages. All three registered evidence gates failed.**

| Gate | Required | Observed | Result |
| --- | ---: | ---: | --- |
| Conditional description saving | At least 16 bits | −7.420649 bits | Fail |
| Whole bank and model conditional p value | At most 0.01 | 0.519 | Fail |
| Margin over a different plaintext | At least 8 bits | 1.262599 bits | Fail |

The observed maximum was the null median. Of 1,999 conditional null maxima, 1,037 were at least as large, including 62 ties: `(1037 + 1) / 2000 = 0.519`. This is not the probability that a plaintext is true or false.

Experiment052 was a separately user-authorized exploratory expansion after experiment051's negative result and failed expansion gate. It does not retroactively make051 successful. The052 p value is standalone and is **not a cumulative familywise error guarantee across051 and052**. No further expansion, feature changes, threshold tuning, or publication followed within this experiment.

## This is a compact package, not a byte complete archive

**The 84 full control receipts are intentionally omitted from this ZIP.** They occupy about1.73GB and remain unchanged in the original local experiment workspace. `FULL_CONTROL_RECEIPT_INVENTORY.json` records every omitted path, exact byte size, and SHA256, bound to the independent audit.

The package retains frozen code, native binary/build information, all author source/provenance files, all1,024 readable messages, the exact normalized bank, literal control definitions, audit certificates, compact control winners/runners-up and summaries, all9,036 control null values and hashes, and **the complete target receipt** with all1,024 candidate rankings, all12,288 exact diagnostics, and all1,999 target null values/hashes. Nothing was removed from the original raw receipts locally.

Archive validation checks omitted-receipt inventory against the audit certificates; it cannot verify absent payload bytes from the compact ZIP. Deterministic regeneration instructions appear below.

## What was tested

Four blinded author batches supplied256messages each. All1,024 normalized97-letter strings are distinct, have EASTNORTHEAST at positions22–34 and BERLINCLOCK at64–74, and exclude the32prior051messages and held-out control text. Original IDs, prose, raw-source hashes, and draft revisions are preserved; aliases are `group:original_id`.

The model/statistic rules stayed fixed:12 AZ/KRYPTOS indexed Vigenère/Beaufort variants, each with periodic, plaintext-autokey, or ciphertext-autokey structure at lengths1–32. Every ciphertext maximum covered all1,024×1,152 =1,179,648 descriptions. The candidate-choice cost rose mechanically from5bits to10bits for the larger bank; no other scoring feature changed.

The score charges model/candidate choice, seed length, and non-crib residual exceptions. It describes the73 non-crib positions conditional on the cribs, **not the full97-letter key**. Nulls fix crib ciphertext letters and permute the remaining letters, preserving their multiset. Exact whole-message compatibility is checked separately; crib-excluded exact models were not restored by residual scoring, and no message was skipped.

The batches contain recurrent language and genre biases, not an exhaustive or independent sample of sensible sentences. For example, the thematic batch includes198 quoted titles/inscriptions and58 literal directions. Grammatical or contextual coherence is not cryptographic evidence.

## Unsupported top ranked illustration

Alias `a_themes:A043`, original ID `A043`:

> The stone had a faint line. “East-north-east” was all it told us; we looked up at the Berlin clock and asked who had named time.

This is **not a recovered plaintext**. Its highest scoring description uses KRYPTOS indexing on both axes, variant Beaufort, and ciphertext-autokey lag3 with seed `ZGL`. It needs57 exceptions among70 scored tail letters plus all24 crib exceptions:81 exceptions in the94-letter tail. The exact lag3 model is contradicted by the cribs; the induced full stream has minimum exact period97.

Across all12,288 candidate/tableau pairs, there are **zero exact registered periodic, plaintext-autokey, or ciphertext-autokey fits**. All full inverse/re-encryption checks passed because an unrestricted induced keystream always exists; that is a correctness check, not evidence for a message.

## Descriptive group results

These are descriptive summaries, not separately calibrated group significance tests.

| Group | N | Best score | Mean | Median | Minimum |
| --- | ---: | ---: | ---: | ---: | ---: |
| a_themes | 256 | −7.421 | −16.876 | −17.305 | −19.655 |
| b_neutral | 256 | −10.195 | −16.737 | −16.977 | −19.924 |
| c_berlin | 256 | −8.683 | −16.604 | −16.808 | −19.987 |
| d_messages | 256 | −9.682 | −16.534 | −16.808 | −19.987 |

Best aliases respectively: `a_themes:A043`, `b_neutral:B096`, `c_berlin:c_berlin_012`, `d_messages:d_082`. The full ranked list and exact prose are in `results/target.json`.

## Controls and limitations

The independent pre-target gate passed before K4 was scored. Controls sampled60 distinct in-bank plaintexts,15 per group, not all1,024.

| Control family | Result |
| --- | --- |
| Simple periodic/autokey plants | 36/36 exact plaintext recoveries;12/12 per structural class |
| Length29 random periodic/autokey seeds | 24/24 exact plaintext recoveries |
| In-scope validation nulls | 0/600 flagged |
| True plaintext absent from bank | 0/12 targets flagged;0/120 separate validation nulls flagged |
| Natural-language running-key diagnostics | 0/12 flagged; true plaintext uniquely first in1/12 |

All9,036 control nulls used the complete1,024-message/model maximum. The largest null score was8.483bits; the smallest in-scope planted score was180.440bits. All60 plaintexts and structural classes were recovered; eight periodic plants used the algebraically equivalent variant-Beaufort/negated-key label instead of Vigenère. Explicit label comparisons remain in the compact records.

Validation observations share a bank and calibration sets; they are not600 independent Bernoulli trials or universal false-positive bounds. **Natural-language running-key recognition remains unimplemented.** This negative result does not exhaust plausible keys, reject arbitrary meaningful running keys, or rule out plaintexts outside the authored bank.

## Main files

- `Kryptos-K4-1024-Candidate-Messages.md`: all1,024 complete authored messages.
- `bank.json`, `bank_import.json`, `authors/`: exact normalized aliases/source mapping and original author provenance.
- `PROTOCOL.md` is the unchanged pre-score snapshot; its original draft/status wording is historical, and the audit certificates establish approval. `config.json`, `controls.json`, `running_key.txt`, `heldout.json`: frozen rules and literal controls.
- `reference.py`, `scorer.c`, `native.py`, `run_experiment.py`, `import_bank.py`: implementation.
- `test_native.py`, `test_runner.py`:14 independent/synthetic tests, including every-model agreement and a full1,024-message Python/C comparison.
- `scorer.so`, `build.json`: audited Linux x86-64 binary and exact compiler/flags.
- `freeze.json`, `implementation_code_audit.json`, `implementation_audit.json`, `results/*audit.json`: hash-bound stage audits.
- `results/control_results_compact.json`, `results/control_summary.json`, `results/pretarget_gate.json`: compact control evidence and gate.
- `results/target.json`, `results/target_summary.json`: complete target evidence and derived summary.
- `FULL_CONTROL_RECEIPT_INVENTORY.json`: exact inventory of the84 omitted full control receipts.
- `ARCHIVE_MANIFEST.json`, `validate_compact_archive.py`: packaged-byte inventory and validator.

## Verify without rescoring the production bank

Python3.12.14 and GCC14.2.0 were used. The implementation uses the Python standard library and a small local C library; no external models, paid checker, network service, or installed package is needed.

```bash
python -m unittest -v test_native test_runner
python run_experiment.py verify-freeze
python validate_compact_archive.py /path/to/candidate-first-052-compact.zip
```

`verify-freeze` checks the frozen sources/supporting files, **not the omitted control payloads**. The ZIP validator checks all included hashes, audit/inventory consistency, compact gate/null arithmetic, independently regenerates null hashes without scoring, and runs the14 tests and source-hash verification in a fresh extraction. It explicitly reports omitted payloads as absent.

## Native build verification

The included `scorer.so` targets the recorded Linux x86-64 environment. To check a rebuild without overwriting frozen evidence, use the same recorded compiler and compile to a temporary path:

```bash
cc -O3 -std=c99 -Wall -Wextra -Werror -fPIC -shared scorer.c -o /tmp/scorer-052-check.so
sha256sum /tmp/scorer-052-check.so scorer.so
```

The independently reproduced binary SHA256 is `243231d321fce6ae1e94170433ff18834a30cb47d395a9ac67c8ae20ce5ed153`. Do not run `python native.py` inside the evidence directory: it would replace the build receipt. A different platform/compiler may produce different bytes; record and validate any such port separately rather than silently rewriting the original freeze.

## Regenerate the omitted receipts

Preserve this package. Make a disposable copy of its extracted directory and rename that copy's `results` directory to `recorded_results`, then run:

```bash
python run_experiment.py controls --workers 8
python run_experiment.py target target.txt --workers 8
```

This regenerates the same frozen experiment, not a new hypothesis search. Allow roughly2GB for full results. Use fewer workers if necessary. The observed control run took318.4seconds; hardware and I/O change runtime. RNG inputs, null ciphertexts, scores, rankings, and p values are deterministic under the recorded environment. Timing/receipt metadata can differ; the omitted-file inventory enables exact payload comparisons where bytes reproduce. Do not edit the bank, score, controls, or thresholds to obtain a different outcome.

Canonical K4 SHA256: `eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab`.

Frozen manifest SHA256: `21fef3e468bb145563388d5485d19a7cb13b1c095979d31af437a8c87ba305db`.
