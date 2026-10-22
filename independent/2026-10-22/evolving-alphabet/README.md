# Independent four-model evolving-alphabet audit

Date: 22 October 2026. Performed in separate cloud scratch, without reading or modifying the user's local repository or production pilot implementation.

Specification: [pinned strategy comparison, section 2](https://github.com/reggiechan74/kryptos-k4/blob/725b81fc1bd89eaccc1c9135396765ef4f69ea46/research/STRATEGY-RESET-2026-10-22.md). The full retrieved source is preserved as `PINNED-SPEC.md`.

## Result

All four fixed models are excluded by exact crib contradictions. This excludes only the four specified `(R, S0)` pairs with their single common move-to-front update, not evolving alphabets as a family.

| Immutable R | Initial S0 | First contradiction, 1-based | Matched known positions | Exact 97-letter regeneration |
|---|---|---|---|---|
| AZ | AZ | 22: predicted C, required E | 0/24 | Yes |
| AZ | KRYPTOS | 22: predicted C, required E | 0/24 | Yes |
| KRYPTOS | AZ | 22: predicted Y, required E | 0/24 | Yes |
| KRYPTOS | KRYPTOS | 22: predicted Y, required E | 0/24 | Yes |

Every result used canonical index 0, no separator, no resets, no fitted parameters, and no post-score update changes. The known positions are 22–34 inclusive for the 13-letter EASTNORTHEAST and 64–74 inclusive for the 11-letter BERLINCLOCK: exactly 24 letters.

### Short exclusion proof

The first 21 ciphertext symbols are `OBKRUOXOGHULBSOLIFBBW`. F last appears at position 18, followed only by B, B, W. Moving each emitted symbol to the front means the state immediately before position 22 starts `WBF`, regardless of which allowed initial alphabet was used. The observed ciphertext at position 22 is F, which therefore has zero-based state index 2. Decryption must output `AZ[2] = C` or `KRYPTOS[2] = Y`, neither the required E. This is an exact contradiction, not a statistical shortfall.

The full states before position 22 are:

- S0=AZ: `WBFILOSUHGXRKACDEJMNPQTVYZ`
- S0=KRYPTOS: `WBFILOSUHGXRKYPTACDEJMNQVZ`

No K4 matched-null significance simulation is necessary once all fixed models contradict. The decoys below are implementation/discrimination controls that ran before K4, not a K4 p-value exercise.

## Independent recovery and controls

The generator is a direct mutable-list implementation. The blind selector does not import the generator or its inverse: it computes each alphabet directly from the observed ciphertext prefix. After any prefix, the seen symbols occur in descending order of their last occurrence, followed by unseen symbols in the original S0 order. This follows by induction: the next emitted symbol becomes most recent and all other relative recencies and unseen ordering stay unchanged.

A third JavaScript oracle, run after the pilot, constructs no current alphabet at all. A previously seen ciphertext symbol's rank is the number of distinct symbols since its previous occurrence; an unseen symbol's rank is the number of seen symbols plus initially preceding unseen symbols. This independently checks all 388 K4 ranks and decoded characters.

The protocol, generator, selector and auditor were SHA-256 recorded before control generation and K4 scoring. `pre_run_sha256.txt` verifies their unchanged contents. The protocol declares seeds, filler, conditioning, counts, thresholds and the precise no-null rule. Blinding was algorithmic: the selector process received only opaque case IDs and ciphertexts and wrote predictions before the separate truth file was opened by the grader. It was not investigator blinding or an external sealed benchmark.

- 32 positive fixtures, eight per model. Each full plaintext contains the literal repeated crib strings at their exact positions; filler is deterministic SHA-256-derived synthetic text, not sampled natural prose.
- All 32 planted models uniquely selected; all 32 complete 97-letter plaintexts exactly recovered.
- Zero accepted cases among 32 nearby move-to-back mechanism controls generated from the same literal-crib plaintexts.
- Zero accepted cases among 128 exact-ciphertext-histogram shuffles, four per positive. The identical four-model selector used the same 24 literal crib constraints on every control and decoy.
- All 104 plaintext one-step cases and all 104 ciphertext one-step cases passed, covering 26 symbols per model.
- All 73,116 strings of lengths 0–3 across four models passed in both inverse directions.
- 32 additional independent full-length roundtrips passed; all 3,104 intermediate states agreed between direct encryption and recency recovery, with permutation, front-symbol and stable-other-symbol-order invariants.
- All four K4 full traces passed the same state invariants and exact 97-letter forward regeneration. Regeneration establishes internal consistency, not a crib fit or plaintext validity.

These finite controls demonstrate correctness and discrimination on these fixtures only. They do not establish broad recovery power, natural-language generalization or a universal false-positive rate.

## Not merely cyclic stepping

On AZ, moving D to front yields `DABCEFGHIJKLMNOPQRSTUVWXYZ`, while rotation to D yields `DEFGHIJKLMNOPQRSTUVWXYZABC`. The cyclic adjacent pairs C→D, D→E and Z→A become C→E, D→A and Z→D, respectively. Thus cyclic neighbor order changes and the update is not merely a cursor shift over a fixed cyclic alphabet. This is not a global novelty claim or an inequivalence proof against arbitrary general state-machine representations.

## Reproduction and files

Run with Python 3, no external dependencies:

```
sha256sum -c pre_run_sha256.txt
python generate_controls.py
python blind_selector.py
python audit.py
node recency_gap_oracle.js > recency_gap_oracle.json
```

`k4_results.json` contains every model's full decoded string, first contradiction, matched positions, crib windows and regeneration status. `k4_full_trace.csv` and `.json` contain all 388 state transitions. `blind_cases.json`, `blind_predictions.json`, `sealed_truth.json` and `controls_summary.json` contain the complete finite control corpus and results. `one_step_cases.json`, `primitive_summary.json`, `runtime.json` and `execution.log` preserve validation evidence. `SHA256SUMS` covers all deliverable files except itself.

Integration should preserve this negative outcome and exact scope. Do not replace it with a newly tuned state rule or present the nonsensical decoded strings as candidate plaintexts.
