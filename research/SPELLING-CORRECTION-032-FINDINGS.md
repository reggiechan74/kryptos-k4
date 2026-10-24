# Deliberate misspellings: what the corrections do and do not determine

24 October 2026 UTC. **No supported consistent rule survived the declared source tests.** This is a local investigation, not a K4 decryption or a global rejection of contextual spelling schemes. No new K4 trial, ciphertext change, push or Site edit occurred. The actual missing ingredient is an independently specified context/position trigger, not another list of plausible wrong words.

[Source review](SPELLING-CORRECTION-032-SOURCES.md), [frozen protocol](SPELLING-CORRECTION-032-SPEC.md), [native constraints](../experiments/spelling_correction.py), [independent oracles](../experiments/spelling_correction_reference.py) and [complete original receipt](../results/SPELLING-CORRECTION-032-ORIGINAL.json) keep evidence, postulated interpretation and actual execution separate. The protocol was committed at `cf3f90f2d5b08456ff32b0144e691743089d650f` before rule scoring. The two training anomaly pairs were already publicly known; this is not a blind discovery.

## Inventory and minimum-edit ambiguity

Dunin specifically attributes the intent of the K1/K2 spellings to Sanborn. His 2005 WIRED interview supports intentional mistakes generally, but does not independently say every particular spelling has that origin. K3 intent remains uncertain. Full source strings remain unchanged in data/controls.json; the study creates separate comparison strings.

| Case | Literal → conventional word | All minimum unit-cost corrections | Alignment count | Evidence role |
| --- | --- | --- | ---: | --- |
| K1 | IQLUSION → ILLUSION | Q→L, word position 2 | 1 | Intent attributed by Dunin |
| K2 | UNDERGRUUND → UNDERGROUND | U→O, word position 8 | 1 | Intent attributed by Dunin |
| K3 | DESPARATLY → DESPERATELY | A→E, position 5; insert E at corrected position 9 | 1 | Conditional, intent not established |
| User example | MISTSKE → MISTAKE | S→A, position 5 | 1 | Illustration, not monument evidence |

The ordered primary extraction is **QU → LO**. Including uncertain K3 produces **QUAε → LOEE**, where ε denotes the missing source character. Calling it only QUA→LOE discards the insertion. These are descriptive extractions; they do not select their own sites, alphabet, traversal or next operation. Their strings are not automatically keys or new plaintext.

Unique alignment for these particular pairs does not make spelling correction universally unique. The complete small-system controls retain both AA→A deletion alignments even though their output strings coincide. Exact edit-script reversal requires the edit positions and original/deleted symbols as metadata. Removing such information can merge distinct originals: a toy Q→L correction maps both IQLUSION and ILLUSION to ILLUSION. That toy operation is not claimed to fit all source texts.

The K1 worksheet/key-entry and K2 worksheet/ciphertext alternatives in the [existing construction audit](../independent/2026-10-22/construction/REPORT.md) also prevent assuming one historical pre-encryption spelling stage. K2’s later omitted ciphertext-S correction is separate. Neither a readable repair nor pencil darkness establishes intent or a production stage.

## Exact source-rule constraints

Every rule must reproduce unchanged letters as well as changed ones. The primary full-source comparison includes all 63 K1 and 369 K2 A–Z letters, retaining the original K2 endpoint and not treating a restored version as another independent anomaly.

- **Uniform character replacement fails.** In ILLUSION→IQLUSION, one L becomes Q and the next stays L. In correction direction, UNDERGRUUND requires U→U, U→O and U→U at its three U occurrences. Full-text constraint certificates retain the conflicting indices. Arbitrary many-to-one character functions do not fix the latter contradiction. A reversible bijection also fails when Q and L both need L.
- **All 624 invertible affine changed-letter maps fail**, across A–Z and KRYPTOS coordinates, even generously granting the unknown change sites. In A–Z correction coordinates, Q16→L11 and U20→O14 require `4a = 3 mod 26`, impossible. KRYPTOS coordinates admit only `a=14,b=23` in the unrestricted diagnostic; 14 is not a unit modulo 26, so this is not invertible. The 1,352-map noninvertible-inclusive diagnostic is labelled separately, not added as new reversible-key coverage. Caesar is already a subset.
- **One keyboard displacement fails.** On the declared quarter-key QWERTY grid, Q→L requires (33,1), while U→O requires (8,0). Granting the change sites cannot make those vectors identical. The user’s A/S adjacent-key example works locally but does not explain the historical pair.
- **Reordering alone fails** because letter multisets change. Copying/duplication/deletion alone cannot introduce Q into ILLUSION. Vowel-only substitution cannot change L into Q. These constraints overlap; they are not independent statistical trials or exclusions of layered/contextual mechanisms.

Fitting only the two changed pairs with an arbitrary bijection, while granting their locations, leaves **24!** completions. That is an oracle-assisted ambiguity count, not 24! source-fitting rules or K4 keys. Once unchanged source letters are required, the uniform-function contradictions above apply.

## Correction information versus a transformation

Two explicit arithmetic interpretations were tested, without selecting an outer cipher:

1. Repeat just the two signed correction deltas. In A–Z they are −5,−6; in KRYPTOS −3,−16. These change virtually every ordinary source letter.
2. Retain all neutral entries of the complete 19-letter anomaly-word pair, then repeat that positional correction mask. This reproduces its defining word pair by construction, not independent prediction.

For both alphabets, **all 42 phase descriptions fail the complete source-text tests**, with 84 individual source applications retained. Allowing independent start phases per message cannot help because each message fails every phase individually. Best mismatch counts on K1/K2 are 62/368 for changed-only masks and 5/39 for the neutral-padded masks. No phase is promoted to K4. Forward/inverse roles are aliases, not twice the search count.

This exposes the overfit: extracting a reproducible difference sequence is easy; it does not tell us why the original error sites were selected or when to repeat that sequence. A cipher could use the differences as key material without reproducing the spelling text, but that is a **different, uninstantiated role** needing an independently selected cipher/selector. The source-text negatives do not reject every such cipher. No arbitrary word-name/position exception list, new trigger or outer key sweep was added after failure.

K3 was excluded from seed fitting. Its one-letter length difference already contradicts a length-preserving uniform map/mask interpretation, but uncertain intent makes it an additional conditional check, not proof that both confirmed errors have the same cause. There is no predeclared contextual survivor to make a meaningful new held-out spelling prediction.

## Controls, timing and prior coverage

The original run starts **2026-10-24T13:18:35.633896+00:00** and ends **13:18:35.659389+00:00**. It used 0.0253 seconds and 18,251,776 bytes peak RSS within 60 seconds / 256 MiB. These are original source-analysis times, not source publication dates or later regression times. The [independent-review comparison](../results/SPELLING-CORRECTION-032-INDEPENDENT-REVIEW.json) records local replay of the parent reviewer’s claims.

Controls pass: 394 complete tiny optimal-alignment sets, all 586 retained script roundtrips, 436 complete tiny function-count comparisons, eight independent word-distance BFS checks, 24 planted full substitutions, all 624 affine forward/inverse checks, four independent affine candidate sets, three partial-domain keyboard roundtrips plus boundary rejection, and 126 positional-mask roundtrips. Algebraic reversibility of a fixed mask is not historical evidence for choosing it.

[Prior coverage](SPELLING-CORRECTION-032-SOURCES.md#prior-coverage-and-novelty-limits) includes Scott’s reported misspelling-derived key/alphabet tests (not locally rerun), the narrower phonetic subset/CL work, and ONE-EDIT-028’s ciphertext damage channel. No worldwide novelty or inherited general exclusion is claimed. No null significance simulation was performed: no partial language score or K4 candidate is promoted, and these are exact source-consistency checks.

## What could make a new test defensible

Specify the representation and stage first; supply a context/position predicate independently of these anomaly words; apply one operation to **every** match, including ordinary unchanged text; specify word boundaries and any length/index transformation; and freeze an inverse or retained ambiguity before testing another source anomaly. A good rule should predict a previously unused alteration without adding exceptions. Present evidence supplies no such trigger. The general deliberate-correction idea therefore remains evidence-blocked, while the exact uniform families above are narrowly excluded.

```sh
python3 -m unittest discover -s tests -p 'test_spelling_correction*.py'
python3 experiments/run_spelling_correction.py --output /tmp/spelling-correction-replay.json
```

Replays record new UTC times and current hashes; preserve the original receipt. This investigation is committed locally only under the current instruction. No publication or deployment is attempted.

Final validation: **608 tests pass on Python 3.9 and 3.12**; [separate UTC suite receipt/full logs](../results/SPELLING-CORRECTION-032-VALIDATION.json). A [complete Python 3.12 replay](../results/SPELLING-CORRECTION-032-PY312-REPLAY.json) matches every original study/control payload exactly. Source-input and canonical K4 hashes are unchanged. No push or Site deployment was attempted.
