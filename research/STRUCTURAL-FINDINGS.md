# Exact constraints under the fixed K4 baseline

18 October 2026. These are reproducible deductions, not a decryption or a claim
of newly discovered prior art. Commands:

```sh
python3 experiments/structural_checks.py > results/STRUCT-001.json
python3 -m unittest discover -s tests -v
```

## Literal permutation-only pipelines

The disjoint cribs require three E letters: two in EASTNORTHEAST and one in
BERLINCLOCK. The entire ciphertext has only two E letters. Every permutation
preserves the complete letter multiset. Therefore **any composition of
permutations alone**, including repeated rectangular rotations, cannot satisfy
these cribs under the literal A–Z, 97-letter model without insertion, deletion,
or substitution. This is an exhaustive invariant argument, not a partial route
search. It does not constrain substitution followed by transposition, variable
representations, or a revised baseline. No novelty claim is made; a complete
prior-art search for this particular count argument has not been undertaken.

## Periodic bijective substitutions at unchanged alignment

For positions congruent modulo period p, a fixed bijective substitution must
preserve equality in both directions: the same plaintext cannot map to different
ciphertext, and the same ciphertext cannot decode to different plaintext.
Checking every pair of the 24 known positions gives contradictions for exactly:

`1, 2, 3, 4, 5, 6, 7, 9, 10, 14, 15, 17, 21, 25, 34, 42, 43, 45, 50`

within the tested range 1–96. Every conflict witness is saved in the result JSON.
For example, one-based positions 25 and 67 have ciphertext V but plaintext T and
L, contradicting any period dividing 42. This witness is already discussed in
[Bean 2021](https://ecp.ep.liu.se/index.php/histocrypt/article/view/153), PDF p. 6,
using zero-based positions 24 and 66. The enumeration here independently checks
the full stated range; it is not presented as a new cipher insight.

All other periods merely pass a necessary constraint. This result does not
establish keys, English plaintext outside the cribs, a cipher identity, or
absence of transposition. Phase origin cannot repair an equality conflict
because congruence classes are unchanged by a global phase offset.

## Language and script feasibility

- No globally injective one-symbol encoding from all 48 Shavian letters into
  26 single Latin letters exists. A restricted message inventory could differ.
- Exactly two Latin letters per intermediate symbol followed by only
  length-preserving operations cannot produce odd length 97 without a declared
  framing or exception rule.
- A synthetic 48-integer two-letter codec is tested over every symbol and
  multiple sequences. Its 48-symbol output is 96 letters and round-trips exactly;
  a 97-letter input is rejected. This codec is a **test control**, not a sourced
  historical Shavian mapping and not a candidate K4 decoder.

These checks implement no translations, pronunciation conversion, or alphabet
search. A specific historical table, exact inverse, treatment of ambiguity, and
independently motivated parameters are still needed for the actual language
branches. Renaming 26 symbols does not evade the monoalphabetic contradiction.
