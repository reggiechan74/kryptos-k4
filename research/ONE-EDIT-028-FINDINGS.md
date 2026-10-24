# Item 8: one-edit construction/transcription sensitivity

**No full fit in the 48 tested periodic structures after any permitted edit. The unrestricted-transposition count exclusion does not survive one edit, but the resulting plaintext sets are enormous and also arise in every matched shuffle. No correction, error location or decryption is established.** Canonical K4 remains unchanged.

This completes the requested eight-item sequence; see the [eight-item overview](EIGHT-ITEM-INVESTIGATION-SUMMARY.md). It does not exhaust all cryptographic possibilities.

## Frozen scope and counts

The [existing proposal](../independent/2026-10-22/construction/REPORT.md) was implemented under [the new frozen protocol](ONE-EDIT-028-SPEC.md), commit `786f864`, before modified-K4 scoring. The potential E-count repair and period-12 weakness were known during design; neither is a blind discovery.

| Repair of observed ciphertext | Raw descriptions | Unique latent strings |
| --- | ---: | ---: |
| Unchanged baseline | 1 | 1 |
| Substitute one cell by a different A–Z symbol | 2,425 | 2,425 |
| Insert one missing intended ciphertext letter at a gap | 2,548 | 2,451 |
| Delete one extra observed ciphertext letter | 97 | 91 |
| Total | **5,071** | **4,968** |

Insertion/deletion are repair directions. Encryption produces latent ciphertext of length 98/96, then the forward channel deletes/inserts a character to reproduce the unchanged 97 observed letters. Substitution/baseline use length 97. No plaintext/key edits, resets, combined events or canonical replacement. Both complete index maps are retained; duplicate strings can have distinct event positions and anchor maps.

Two coordinate interpretations were fixed in advance:

- **ENGLISH_FIXED (primary):** every English letter in the two published phrases stays at its stated latent plaintext position. No crib is moved or omitted.
- **OBSERVED_CELL_TRANSPORT (conditional):** all 24 labels attach to their original observed cells and move by the one edit map. Both complete words must remain contiguous. Deleting a labelled cell or splitting a phrase is inadmissible. This is not a claim that the public numbers really mean observed-cell coordinates; B-only compatibility is not a fit at the primary English positions.

Of 10,142 gross edit/alignment descriptions, 596 transport cases are inadmissible: 24 labelled deletions plus 22 internal gaps ×26 possible letters. The remaining **9,546** descriptions deduplicate to **6,317 distinct (latent string, complete anchor mask) instances**. Dropped cases are explicitly listed; no contradictory known letter is discarded. One map governs both words and the unknown prefix/gap, without a new phase at either crib.

## Exact cipher results

### Periodic additive/true-Beaufort: no complete fit

Tested AZ or KRYPTOS coordinates, equations C=P+K or C=K−P modulo 26, unrestricted periods 1–12: **48 structures**. Plus/minus-key variants and free phase are not counted again. Mixed input/output alphabets, other periods, routes and other state models are outside this family.

All 13 first-phrase letters determine every key entry for these periods. The same absolute-position-zero key spans the whole latent message and all 11 public Berlin letters. Logical coverage is **458,208 admitted edit/alignment/structure checks**, evaluated through 303,216 unique instance/structure checks with exact cache reuse. No underlying 26^p key sample is substituted for the constraint solution.

There are **41 raw first-stage fits**, represented by 29 unique instance/model records, and **zero complete fits** in either coordinate interpretation. All first keys and Berlin predictions are saved, including failures. First-stage fits are not promoted: a period-12 key has only one redundant first-window equation, and at most one substitution can always satisfy it. This is true for arbitrary input, not peculiar evidence in K4. Berlin is a public second-stage constraint, not untouched validation data.

### Arbitrary position permutations: compatible but non-identifiable

This family admits every position permutation, not a selected physical route. The old deficit is one E: the disclosed plaintext needs three while observed K4 has two. In this single-edit domain, compatibility can be manufactured only by inserting E or replacing an eligible non-E symbol with E. That is a property of the count test, **not evidence that an E was omitted or miscut**.

Primary interpretation: **191 raw compatible edits** (98 insertions, 93 substitutions), giving 189 distinct corrected strings. The transport interpretation adds 169 raw compatible descriptions; across both, there are 240 compatible latent/anchor instances. No deletion or unchanged baseline passes the count test. Arbitrary route freedom absorbs the insertion location, so the count fit cannot identify an error position.

Each instance has an exact compact plaintext set: its length, multiset and all 24 known positions, plus exact multinomial plaintext volume and position-permutation-key count. Two deterministic different non-language witnesses are retained where possible, with bijective position keys and complete re-encryption through every aliased edit channel. These are ambiguity witnesses, not proposed English decryptions.

Original run output preserved conservative union bounds. A separately timestamped post-outcome audit deduplicates identical plaintext sets into **25 primary classes / 27 classes across both interpretations**, then checks all 351 class pairs for disjointness. They differ in length/multiset or have conflicting known letters. Exact distinct plaintext counts are therefore:

- Primary English-fixed interpretation: **5,324,897,428,378,869,945,933,678,831,268,714,797,411,768,906,478,036,245,223,958,494,256,824,320,000,000,000,000** (about 5.3×10^84).
- Across both declared interpretations: about **1.06×10^85**; the exact integer and disjointness certificates are in the [independent audit](../results/ONE-EDIT-028-INDEPENDENT-AUDIT.json).

These volumes are neither probabilities nor sums of independent keys. The post-run refinement changes no tested model, channel or original receipt.

## Earlier necessary certificates

These were monitored as diagnostics, not additional completed historical key searches.

- **Direct nonzero-strip no-fixed-point certificate survives every admitted case:** all 5,071 primary and all 4,475 transport cases retain a known self-encipherment. The independent audit records a fixed-point witness for all 6,317 unique instances. This strengthens that conditional exclusion through the frozen one-edit channel, not through arbitrary preprocessing or layered machines.
- **Wheatstone's relaxed adjacent-pair certificate is not uniformly stable:** 925 primary and 51 transport descriptions lose that particular contradiction. This does not establish a fixed-ring key, continuous reachable machine, or Wheatstone solution; the diagnostic is only necessary. The original canonical exclusion remains unchanged.

The study does not revisit all prior recurrences, trees, SIGABA keys or other families under edits.

## Matched controls and ambiguity

All 99 histogram-preserving shuffles rerun the entire edit/alignment/family selector, seed 280024. All 99 admit arbitrary-permutation repairs and first-stage periodic fits; none admits a complete periodic fit. The count repair and first-window fit therefore provide no outperformance over these matched controls. No partial-match, word-fragment or positive significance claim is made.

Before actual scoring: full K1/K2 construction controls and seven original offline convention controls pass. Projector restart/phase-jump non-identifiability is retained, without a new full 1,133-symbol source fetch or a unique-omission claim. Independent tagged-token checks cover every raw channel; 30 complete tiny edit sets, 24 complete tiny permutation truth sets, 96 complete tiny periodic-key sets and 144 fixed-model/table-decoder checks pass.

All **24 full-selector plants retain the true edit/key/interpretation**, including boundary/internal edits. Their complete compatible record sets contain 137,600 representations, with 1–3,827 distinct plaintexts per plant. This is truth inclusion, not 24 unique recoveries. Every alternate fit is retained. Original output is losslessly compressed, not truncated.

## Reproduction, chronology and limitations

[Original run](../results/one-edit-028/README.md): controls 2026-10-24T03:00:31.710149+00:00–03:00:50.610903+00:00; actual 03:00:50.611166–03:00:51.315755+00:00; nulls finish 03:01:06.353305+00:00. Numerical control time is separate from compression/enclosing stage time. Independent audits and regression have their own UTC timestamps. No commit time is substituted.

A preflight found uncompressed controls exceeded the 64 MiB saved-output cap; all data are retained in a [lossless preflight archive](../results/one-edit-028-preflight/README.md). Streamed gzip keeps the original run within the unchanged cap. A summary-writer TypeError stopped one attempt before actual scoring; its incomplete manifest is preserved. No parameter/budget expansion or omitted candidate followed either engineering issue.

```sh
python3 experiments/run_one_edit.py --spec-commit SPEC_FULL_SHA --execution-kind replay
python3 experiments/audit_one_edit.py
python3 -m unittest discover -s tests -p 'test_one_edit*.py'
python3 -m gzip -d -c results/one-edit-028/RUN_ID/actual.json.gz
```

Use the full specification commit and run ID linked in the result guide. Replays write a new directory; audits print fresh JSON. [Native channel](../experiments/one_edit_channel.py), [models/complete compact classes](../experiments/one_edit_models.py), [independent reference](../experiments/one_edit_reference.py), [controls](../experiments/one_edit_controls.py).

No independently observed K4 discrepancy was found or presumed. This user-requested counterfactual arm cannot locate a production stage, establish intent, identify an error rate, or justify two edits next. Canonical data are byte-identical to pre-study main. No Site change or ninth investigation. **K4 remains unsolved.**

Final aggregate regression: **568 tests pass on both Python 3.9 and Python 3.12**. The [separate validation receipt and full logs](../results/ONE-EDIT-028-VALIDATION.json) record UTC suite start/end independently of the original run.
