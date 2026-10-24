# Item 5: 24 lamp fields and 24 Greek letters

**The three frozen exploratory constructions have no K4 first-crib survivor. This does not reject Greek or clock ciphers generally.** They are complete working codecs/ciphers with explicit inverses, not historical claims. The Mengenlehreuhr is distinct from Sanborn's confirmed Alexanderplatz World Clock.

## What was built

The declared Greek alphabet ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ labels the 24 lamp positions. Two orders only: physical row-major, with seconds first, and full reversal. Lit fields contribute ordinal weights 1–24; these are our weights, not ancient Greek numerals. The display uses H=5a+b and M=5c+d with 4/4/11/4 rows; it is not ordinary positional base 5. Colors add no bits.

Every role uses all 1,440 starting minutes, both constant seconds-indicator states under minute sampling, AZ/KRYPTOS coordinates and addition/true Beaufort. No clock reset, fitted weights or alternative rate was introduced after results.

| Role | Complete bridge and cipher | Actual result |
| --- | --- | --- |
| L: letter key | Ordinal sum modulo 26; one minute per English letter, total reversible A–Z cipher | All 23,040 descriptions fail first-crib constraints |
| B: pair key | Two English letters rank in 0–675, represented by three Greek base-24 digits; ordinal-sum cipher modulo 676. Odd singleton uses two Greek digits and modulo 26. One minute per block | All 23,040 descriptions fail first-crib constraints |
| G: framed Greek stream | A–W map to first 23 Greek letters; ΩΑ/ΩΒ/ΩΓ encode X/Y/Z. Encrypt modulo 24, one minute per token, serialize in first 24 Latin coordinates | All 23,040 descriptions support-excluded before any phase test |

The adjacent-pair rank arithmetic includes carries and is not the previously excluded fixed affine 2×2 map over Z26. Greek base-24 digits are a reversible internal representation, not an additional source of cipher strength. The L readout has 5,760 distinct 97-value clock streams; none equals a stream of the older binary-weight LAMP-STREAM-001 family. B has 5,568 distinct 49-operation clock streams from 5,760 clock descriptions; aliases are not independent evidence.

## Exact rejection and alignment

L and B jointly evaluate 46,080 fixed descriptions. First-crib constraints alone eliminate every one. The explanatory certificate shows the remaining phase counts after each constraint for all 16 role/alphabet/equation/order groups; each group starts with 2,880 clock descriptions and reaches zero after two or three checks. No full plaintext candidate, Berlin prediction or positive lead survives.

G is excluded by an invariant, without 23,040 simulated phase trials. Its AZ serialization cannot emit Y/Z; its KRYPTOS serialization cannot emit X/Z. Actual K4 contains every A–Z letter. This does not depend on assuming English indices survive expansion. The codec itself is valid on its declared ciphertext domain. A naive 26-to-24 map cannot be injective: the explicit modulo-24 comparison merges A/Y and B/Z. Our escape framing resolves that issue for plaintext, but does not expand the encrypted output support.

The length-preserving L/B models explicitly keep English clue positions. G fully decodes and parses the message before testing English positions 22–34 and 64–74. The synthetic plaintext expands from 97 to 104 tokens; its first clue starts at token index 25, not English index 21. No prefix or gap reset is used. These ordinal codecs are not phonetic Greek transliteration.

## Controls, ambiguity and chance baseline

- All 5,760 display/order comparisons agree with independent triangular sums and a separate direct row builder. Complete valid-state inverse checks pass; existing and new tests reject invalid rows/time states.
- All 18,279 English strings through length three round-trip the prefix codec. All 676 pair ranks and 26 singleton ranks round-trip the fixed Greek digits; five invalid framing/rank controls reject.
- All 69,120 raw descriptions round-trip an unrelated message and agree with bit-summed encryption.
- All 24 literal-crib plants are retained by the complete 69,120-description selector. Twenty-four timing and twenty-four known-symbol mutations are detected for the planted settings.
- One B plant has **two distinct full plaintexts** satisfying all 24 clues. Four G plants have two raw settings but one plaintext. All alternatives are retained; planted inclusion is not a universal claim of blind unique recovery.
- A separately written direct-decoder audit agrees on the **complete candidate set** for all 24 plants and actual K4. Its row arithmetic and direct plaintext checks do not use the optimized key-constraint compiler. This is same-author independent implementation, not an external blinded audit.
- All 199 histogram-preserving shuffles rerun the full selector, with fixed seed 250024. None has a first-crib or all-24 survivor. This is a descriptive control for this frozen family; no significance claim follows from a negative actual result, and no posterior probability or all-prior-hypothesis correction is asserted.

The public Berlin clue is a second-stage constraint, not historically untouched data. Actual K4 never reaches that stage. Constant-key parity from the old binary model is not reused to exclude the new variable-parity ordinal models.

## Reproduce and chronology

The [protocol](LAMP-GREEK-025-SPEC.md) was committed at `b19f89c` before the original K4 comparison. Public cribs and prior results were already known during design. Original run: `2026-10-24T01:51:34.425418+00:00` controls start; actual selection `01:51:39.584120`–`01:51:39.593230+00:00`; null panel ends `01:51:41.494966+00:00`. The enclosing manifest gives exact start/end and source hashes. The post-outcome independent replay is separately timestamped.

From the repository root:

```sh
python3 experiments/run_lamp_greek.py --spec-commit b19f89ccb834f2fe5808378507939b77c6c11b36
python3 experiments/audit_lamp_greek.py
python3 experiments/lamp_greek_certificates.py
python3 -m unittest discover -s tests -p test_lamp_greek.py
```

The first command writes a fresh immutable run directory; it does not overwrite original receipts. The independent audit writes a validation receipt and must be directed/copied separately if preserving the published original validation file. [Original run, controls, all plants and nulls](../results/lamp-greek-025/README.md), [independent validation](../results/LAMP-GREEK-025-INDEPENDENT-VALIDATION.json), [finite certificates](../results/LAMP-GREEK-025-CERTIFICATES.json), [implementation](../experiments/lamp_greek.py), [direct checker](../experiments/audit_lamp_greek.py).

Final aggregate validation: **529 tests pass on Python 3.9 and 3.12**. [UTC validation receipt and log hashes](../results/LAMP-GREEK-025-VALIDATION.json). The original computation, independent replay and regression timestamps remain separate. Documentation has no new broken targets; 13 known exceptions remain in one preserved independent source. No CI workflows are configured.

## Boundary

No historically grounded creator link, physical lamp registration or intended alphabet bridge was found or presumed. Other lamp orders, non-ordinal weights, color, timing rates, nonlinear state, other framing/serialization, Greek numeral systems and genuine phonetic preprocessing remain outside coverage. They are not automatically justified next searches. No adaptation after these negatives, no Site change, no item 6. K4 remains unsolved.
