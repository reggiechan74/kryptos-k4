# Candidate-first 053: ordinary-language running keys

## Result: no support among these 1,024 messages and 12 fixed tableaux

The frozen language detector successfully recovered unseen English control keys, but the canonical K4 test failed **all four registered evidence criteria**. This is a negative, standalone exploratory test after experiments051/052—not a proof that every running-key construction or every possible plaintext is impossible.

| Target criterion | Observed | Required | Result |
|---|---:|---:|---|
| Non-crib language-coding saving M | −237.145512 bits | ≥32 | Fail |
| Whole-search conditional p | .932 = (1,863+1)/2,000 | ≤.01 | Fail |
| Margin over another plaintext | 3.218139 bits | ≥8 | Fail |
| Full-key cross entropy H | 8.272177 bits/letter | ≤3.600639 | Fail |

All1,024 candidates and all12tableaux were evaluated; all12,288 induced keys, scores and bidirectional encryption checks are retained in `results/target_result.json`. The1,999 nulls each searched that entire same hypothesis space. No source, candidate, window, model, threshold or scoring rule was changed after the target result. No new expansion or hypothesis search followed.

### Unsupported top-ranked illustration—not a proposed solution

Candidate `b_neutral:B090`, AZ–KR Beaufort:

> That new apartment faces east-north-east and looks across the street toward Berlin Clock through the leaves of a tree.

Its induced key, using the registered plaintext-axis key-letter convention:

```
YPAUIJUFCOMKUKSKUMKMPQRTPHIUUARAYZFRAPIUAMGICORRQOIITIZOIALLTDLUGUHMRUKAFKQUBOTELJQOARAQSNVALTALF
```

A coherent guessed plaintext is not evidence. Any candidate yields an unrestricted97-letter key that re-encrypts; all12,288 such checks passed by construction. The relevant language/statistical gates did not. This stage does not reinterpret unrestricted exact re-encryption as a short-key or language-key fit.

## Did the detector work on controls?

Yes, within its tested scope. It selected the exact planted plaintext, full97-letter key and tableau label in **all72 positive controls**, searching the entire1,024×12 space without knowing which candidate/model was planted.

| Frozen control group | Passed full detection/recovery | Total |
|---|---:|---:|
| Unseen published prose | 36 | 36 |
| Newly blind-authored source-absent prose | 12 | 12 |
| Archaic/poetic/dramatic styles | 19 | 24 |
| Uniform random-key false flags | 0 | 24 |
| Letter-permuted-key false flags | 0 | 24 |
| True plaintext absent: false flags | 0 | 12 |
| Matched validation ciphertext-null flags | 0 | 1,440 |

All five difficult-style misses were Shakespeare passages whose correct keys ranked first but exceeded the frozen full-key cross-entropy ceiling: C040,C047,C049,C054,C055. No threshold was relaxed. Published prose recovered3/3 under each tableau. The72 positive controls use72 distinct bank messages,18 from each group; published prose spans23 speeches, hard styles7books and new prose12documents. These finite, clustered controls do not establish universal or independent-trial error rates.

**Semantic limitation:** all12 word-token-order-shuffled controls were also flagged and correctly recovered. This four-gram model detects English-like character/word structure, not coherent syntax, meaning, historical intent or a historically identified source. This mandatory stress result is not hidden or counted as proof of semantics.

The control gates passed before K4 was scored. Controls used15,696 whole-search nulls and took156.4seconds; the target stage took4.23seconds. Full control receipts remain intact locally (144files,928,767,286bytes).

## Per-group target scores

Each row summarizes the best tableau score of each of the256 messages in that group; these are descriptive summaries, not four additional significance tests.

| Group | Best | Mean | Median | Worst |
|---|---:|---:|---:|---:|
| a_themes | −255.646186 | −329.719358 | −331.437287 | −398.067477 |
| b_neutral | −237.145512 | −323.811193 | −327.262511 | −380.796539 |
| c_berlin | −242.287601 | −325.823133 | −329.449795 | −384.085433 |
| d_messages | −246.310229 | −327.862163 | −327.666368 | −388.896667 |

## What was fixed and audited?

- The exact immutable052bank, SHA256 `e929b4c5a93bab76195dd9d16556aa1def8db530a987f9bdf3dc6861c28b11e7`, with original prose, aliases and source hashes. Recurring author scaffolding, fictional/unverified geography and correlated candidates remain limitations; this is not an exhaustive language space.
- One smoothed character order4 model trained on1.6million letters from eight fixed Gutenberg books. No candidate prose or control document entered training.
-340 calibration-only windows; the fixed ceiling is the337th sorted cross entropy (nearest-rank99th percentile).
- Whole-document role separation, attributed-book-author separation and inaugural-speaker separation. Unknown ghostwriters prevent a claim of actual-writer disjointness for speeches. Exact97/48letter overlap checks exclude measured overlap only, not every paraphrase/reuse.
-12new blind-authored assistant prose documents, created without candidate/cipher/scorer/source access; not an independent human-language sample. Literal documents and authoring log are included.
- Primary likelihood uses only73non-crib letters, resetting context at each unknown block. Shared crib-derived key letters never contribute, even as context. Nulls fix crib ciphertext letters and permute the73others, searching all models/messages.
- Key residues are spelled in the chosen plaintext-axis alphabet. This fixed assumption excludes other key-label conventions and is not claimed to be the unique historical convention.
-22synthetic tests, independent Python/C equivalence, source/window/model/control audits and saved-results audits. Hash-bound freeze: `1c87592e32ff6e7fefaf20a66bbabe358df0154eeac8bc1d356a108c603901ae`.

See `PROTOCOL.md`, `IMPLEMENTATION_SPEC.md`, `implementation_audit.json`, `results/pretarget_gate_audit.json` and `results/target_audit.json`. The independent target audit verified all retained keys/scores and null inputs/winner statistics, plus unchanged exhaustive scorer code; it explicitly did not rerun every full-bank null maximum. The p-value is standalone053 conditional evidence, **not cumulative familywise control across051–053**.

## Compact-archive omissions and reproducibility

**This is not a byte-complete archive of the entire working directory.** `OMITTED_FILES_INVENTORY.json` identifies every intentionally omitted raw control receipt and frozen source file by path,size,SHA256. The144full control receipts remain unchanged in the cloud working directory; their summary, complete hash inventory, controls and deterministic regeneration code are included. The full target receipt is included, not summarized away.

The compact archive omits duplicate extracted published documents (exact originals are retained in the included pinned NLTK ZIPs) and the eight052raw author/validation files (already delivered with052). The exact bank and its source-hash provenance are included. Newly authored053control documents are included. `FROZEN_INPUT_ACCOUNTING.json` distinguishes included from omitted frozen paths; validation must not claim every omitted file physically exists.

Official source snapshot: [NLTK data repository](https://github.com/nltk/nltk_data/tree/550b6625bcef1f2abff2ff770a5a0d272c9c6b2a), commit `550b6625bcef1f2abff2ff770a5a0d272c9c6b2a`. Pinned retrieval URLs and raw hashes are in `data/SOURCE_RECEIPTS.json`; official license metadata and archive README/distribution terms are retained. The repository classifies these collections as Public Domain. No Brown-only source-admission test or external language-model service was used.

The audited native loader deliberately binds the original frozen environment and paths. **Do not edit the original freeze or let it silently rebuild elsewhere.** `reproduce_compact.py` instead verifies archived input hashes, builds an isolated byte-verified scratch copy, runs synthetic tests there, and can regenerate the144full control receipts into a new output directory. It does not modify frozen inputs or search new hypotheses. `--validate` checks archive integrity, included frozen hashes, omitted-file accounting, isolated tests/native equivalence, complete target rankings and deterministic null inputs. `--controls-output /new/empty/path` regenerates controls and requires every regenerated receipt to match its original inventory hash. Published corpus extraction/training verification is available with `--verify-training`; no network retrieval is needed because the exact pinned ZIPs are included.

```sh
python reproduce_compact.py --validate
python reproduce_compact.py --verify-training
python reproduce_compact.py --controls-output /tmp/candidate-first-053-recreated-controls
```

Run these commands in an extracted copy. The script records what was actually checked; omitted full receipts are not pretended present. Rebuilding on another environment requires an equivalent compiler/runtime and the synthetic/reference checks; it is replication, not permission to change this experiment or run new candidates.
