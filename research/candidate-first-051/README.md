# Candidate first Kryptos pilot 051

## Outcome

**No evidence for any of the 32 proposed plaintexts under the registered structural key test. The scientific expansion gate failed.**

The frozen K4 test scored every message against all 1,152 registered descriptions. Its best conditional description saved **−8.879 bits**, with global conditional Monte Carlo **p = 0.916** and a **0.570 bit** lead over the next different plaintext. All three target gates failed.

| Registered target gate | Required | Observed | Outcome |
| --- | ---: | ---: | --- |
| Conditional description saving | At least 16 bits | −8.879 bits | Fail |
| Whole bank and model null p value | At most 0.01 | 0.916 | Fail |
| Different plaintext score margin | At least 8 bits | 0.570 bits | Fail |

There were 1,831 of 1,999 null maxima at least as large as the observed maximum: `(1831 + 1) / 2000 = 0.916`. This is not a posterior probability that a message is true or false.

## What was tested

The bank contains 16 thematic and 16 neutral messages, each exactly 97 normalized A–Z letters, drafted in two blind batches before cryptographic scoring. Every message has EASTNORTHEAST at positions 22–34 and BERLINCLOCK at 64–74. All original IDs and draft revisions are retained. Distinct messages do not imply statistical independence; fictional geography and recurring travel language are not verified facts.

The finite model family is 12 AZ/KRYPTOS indexed Vigenère/Beaufort variants, each with periodic, plaintext autokey, or ciphertext autokey structure at lengths 1–32. The fixed score charges candidate/model selection, seed length, and all non-crib residual exceptions. **It is a conditional code for the 73 non-crib letters, not a full 97-letter-key MDL score.** Crib exceptions are conditioned on and disclosed, not credited or charged. Exact models contradicted by cribs are not restored by an approximate residual score; every message was still scored.

Each null fixes the crib ciphertext positions and permutes the remaining ciphertext letters, preserving their marginal counts. Its statistic is the maximum over the entire frozen bank and model family.

## The highest ranked message is not a decryption

N02, neutral:

> The morning breeze blows east-north-east as we sit eating fresh bagels by the Berlin Clock before our early train ride.

Its highest scoring description uses AZ plaintext indexing, KRYPTOS ciphertext indexing, Vigenère arithmetic, and ciphertext autokey lag 6 with seed `MBWPHO`. It needs **57 exceptions among 67 scored tail letters**, plus **23 crib exceptions**: 80 exceptions in the full tail. The exact lag-6 model is independently contradicted by the cribs. The induced full stream has minimum exact period 97.

Across all 384 candidate/tableau pairs, **none** has an exact registered periodic or autokey fit. Full inverse and re-encryption checks passed for all 384 because a full induced keystream always exists; that fact is a correctness check, not evidence for a plaintext.

| Rank | Candidate | Group | Best score in bits |
| ---: | --- | --- | ---: |
| 1 | N02 | Neutral | −8.879 |
| 2 | T11 | Thematic | −9.450 |
| 3 | N15 | Neutral | −9.891 |
| 4 | N09 | Neutral | −10.273 |
| 5 | T01 | Thematic | −10.292 |

Group summaries are descriptive only, not separately calibrated significance tests.

| Group | Messages | Best | Mean | Median | Minimum |
| --- | ---: | ---: | ---: | ---: | ---: |
| Thematic | 16 | −9.450 | −11.762 | −11.470 | −13.427 |
| Neutral | 16 | −8.879 | −11.625 | −11.559 | −14.404 |

## Controls and the important limitation

The control stage passed its preregistered gate before K4 was accepted. It covered all 32 messages, evenly across both groups, and evaluated 9,036 matched null maxima through the same complete pipeline.

| Control family | Result |
| --- | --- |
| Simple periodic and autokey plants | 36/36 exact plaintext recoveries; 12/12 in each structural class |
| Length-29 random periodic and autokey seeds | 24/24 exact plaintext recoveries |
| In-scope matched validation nulls | 0/600 flagged |
| True plaintext absent from the bank | 0/12 targets falsely flagged; 0/120 separate validation nulls flagged |
| Natural-language running keys | 0/12 flagged; true plaintext ranked first in 5/12, without evidential support |

All 60 in-scope plaintexts and structural classes were recovered. In eight periodic cases, Vigenère was represented by variant Beaufort with a negated key, an algebraically equivalent encryption. Explicit label-match fields preserve this distinction.

Validation flags share calibration sets and a fixed bank; they are not 600 independent Bernoulli trials. These rates describe the registered controls and nulls, not universal error bounds.

**Natural-language running-key recognition was not implemented.** The running-key diagnostic confirms this gap. This result does not reject a meaningful running key, exhaust plausible-key methods, or rule out plaintexts outside this small authored bank. No post-result threshold changes, candidate edits, enlarged search, external model calls, paid checks, or external submissions were made within experiment051. After this negative result, the user explicitly authorized a separate exploratory1024-message experiment052. That later user-directed decision does not turn this failed gate into a pass;052 is outside this package.

## Files

- `CANDIDATES.txt`: all 32 original IDs and complete prose, without scores.
- `PROTOCOL.md`: the historical pre-target protocol; its original pre-audit status line is retained unchanged for hash integrity.
- `pilot.py`, `run_experiment.py`, `test_pilot.py`, `config.json`: standard-library implementation and tests.
- `bank.json`, `authors/`: exact frozen bank, full drafts, revision notes, and authoring/length-check scripts. Authoring scripts are provenance, not instructions to regenerate or edit the frozen bank.
- `controls.json`, `running_key.txt`, `heldout.json`, `controls/held_out_message.json`: literal control definitions, keys, RNG labels, and held-out provenance.
- `freeze.json`, `implementation_audit.json`: pre-score source hashes and independent implementation certificate.
- `results/controls/`: all 84 control receipts, full rankings, exact diagnostics, null maxima, and reproducible null hashes.
- `results/pretarget_gate.json`, `results/pretarget_gate_audit.json`: control gate and independent audit.
- `target.txt`, `results/target_receipt.json`, `results/target.json`: verified canonical target and complete frozen target results, including all 32 rankings and every winning-description residual position.
- `results/target_summary.json`, `results/target_audit.json`: derived readable statistics and independent target audit.
- `ARCHIVE_MANIFEST.json`, `validate_archive.py`: package integrity inventory and validator.

## Verification and reproduction

Python 3.12 was used; the experiment needs only the standard library. Preserve the recorded package before rerunning anything.

```bash
python -m unittest -v test_pilot
python run_experiment.py verify-freeze
python validate_archive.py /path/to/candidate-first-051-deliverable.zip
```

The validator checks ZIP integrity and safe paths, all packaged hashes, the frozen source hashes, candidate aliases and prose, data/audit consistency, and tests from a fresh extraction. It does not rerun all 11,035 null scores.

For a complete numerical rerun, make a disposable copy of the extracted directory, rename its `results` directory to `recorded_results`, then run:

```bash
python run_experiment.py controls --workers 8
python run_experiment.py target target.txt --workers 8
```

Use fewer workers if necessary. The original RNG labels, bank, models, and statistic remain fixed. Runtime timestamps and elapsed time change; ciphertext hashes, primary scores, rankings, and p values should reproduce. The runner refuses changed frozen sources or a second target result in the same results directory.

Canonical target SHA256: `eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab`.

Frozen manifest SHA256: `ae27b08bb8918b4ffa0b3d5e89fbb42784dfba0017a3e43bd8e100045b7bbadd`.
