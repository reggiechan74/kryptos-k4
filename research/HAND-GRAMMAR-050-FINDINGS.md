# Fixed-key hand grammar 050: complete depth-three domain, no full crib hit

**The frozen fixed-key grammar completed:38 distinct primitives,56,355 ordered descriptions of lengths 0–3, and 27,323 distinct complete operators.** None satisfies all 24 clue letters. Maximum crib agreement is 7/24; null maxima range 6–8, with 19 of 31 at least the actual maximum. This is a narrow negative for this grammar, not every hand cipher or all possible keys.

[Audited frozen specification](HAND-GRAMMAR-050-SPEC.md), [original receipt](../results/HAND-GRAMMAR-050-ORIGINAL.json), [full Python 3.12 replay](../results/HAND-GRAMMAR-050-REPLAY.json), [complete operator/alias catalogue](../results/HAND-GRAMMAR-050-CATALOGUE.json.gz), [engine](../experiments/hand_grammar_050.py), [UTC/resource logs](../results/048-050-REPLAY-VALIDATION.json).

Primitives are six keyword-columnar forward/inverse maps with widths 7,10,8 only;22 bijective skip maps at steps 2–12 and their modular inverses, fixed start 0; reversal; and nine KRYPTOS-alphabet arithmetic maps using literal KRYPTOS/PALIMPSEST/ABSCISSA. No skipping operation discards letters. Column ties use A–Z order then original column position; rows are ragged without padding. No ENE route, unrestricted keyword, extra alphabet or larger depth was silently added.

Every operator has output-index form T(x)[i]=s×x[p[i]]+b[i]mod 26. Exact composition and canonical (p,s,b)deduplication identify equality on **all inputs**, rather than coincidences on K4. Raw counts at depths 0,1,2,3 are 1,38,1,444,54,872. Distinct operators at each exact depth are 1,38,995,27,124; these sets overlap, so their sizes must not be summed as independent coverage. All 56,355 descriptions retain aliases in the catalogue and pass independent list-based reference replay and inverse checks.

Controls before actual K4 testing include 6,080 complete small-alphabet input/composition comparisons,988 primitive-symbol tests, all published K1 and both K2 version known answers, and 43 whole-selector plants spanning every primitive, identity and noncommuting compositions. Every plant's full hidden plaintext is recovered; aliases/collisions are retained, not treated as unique keys. Full 97 letter re-encryption is required for any exact survivor; there are none. All 31 nulls rerun the entire deduplicated operator set. No partial-score promotion or uncorrected English claim follows.

The first historical-control attempt stopped **before actual K4 search** because my K2 adapter indexed literal `?` as a letter. [Failure record](../results/HAND-GRAMMAR-050-PREFLIGHT-INITIAL.json) preserves the old code hash, recoverable at commit `fbad6b2`. The corrected adapter follows the existing source convention: pass `?` through without advancing the key. Neither canonical K4 nor the 97 A–Zoperator domain changed, and the complete controls were restarted before search. Both full successful executions agree semantically. Python 3.12 replay takes 6.60 seconds and 163,446,784 bytes maximum RSS, within unchanged bounds. Original/replay UTCs are separate in their receipts.

Conservative marginal prior overlaps are 470 operators inside the older route/periodic-key family and 89 inside 049. These sets may overlap; do not add or subtract them as independent negatives. Other authors already document particular depth-three substitution/columnar domains. We do not adopt their broad numerical proof claims or assert worldwide novelty. [Prior coverage](048-050-PRIOR-COVERAGE.md) identifies the source and exact local boundaries. Hand execution is a historical plausibility prior, not evidence that an unrestricted key search is tractable. Other widths, keys, offsets, primitives, nonlinear layers and depths remain outside this grammar. No paid checker, candidate submission, Site edit or publication occurred.

Final integration: all 718 tracked tests pass on Python 3.9 and Python 3.12; [UTC suite receipt and complete logs](../results/048-050-FINAL-VALIDATION.json). Original experiment, scientific replay and regression times are recorded separately. No public push occurred.

Reproduce from repository root, preserving original receipts:

```sh
python3 experiments/hand_grammar_050.py --output /tmp/hand-grammar-050-replay.json
```

Existing compressed catalogues are checked exactly instead of silently overwritten. New replay files receive new UTC times.
