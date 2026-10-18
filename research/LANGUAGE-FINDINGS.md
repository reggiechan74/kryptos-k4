# Language-layer feasibility outcome

LANG-001 ran after the frozen specification commit
`21c3b4c16615586c525420cfdd6014cc7a6d44c4`, using implementation commit
`58646022bf5578e4c193a6cdc7a487ef86c5947d`. The local executor checked the
committed specification/source-manifest bytes through GitHub before execution.
The [source receipt](../docs/historical-alphabet-specification.md) distinguishes
independently inspected GOST pages from the research worker's Shavian review.

The run completed in 0.497 seconds, one process, no key search or scoring. All
37,060 Russian source strings of lengths 0–3 produced distinct encodings and
exact complete DP inverses/re-encodings. Sardinas–Patterson independently returned
suffixes H/HH, then empty, proving unique decodability of this finite code.
The complete alphabet includes a double-quote hard-sign marker and a distinct
single-quote soft-sign marker; the hard sign is not two soft signs.

## What fails, exactly

- Literal 1981 Table-2 code output followed by any permutation cannot explain
  K4: the restricted uppercase-Russian-letter domain never emits Q/W/X.
- A fixed one-character substitution on each **individual transport output
  character**, followed by any transposition, still has at most 25 output
  symbols. K4 contains 26. This proof does not act on whole variable-length
  codewords and does not enumerate unknown keys or routes.
- Stripping the quote marks is lossy: Б, БЬ and БЪ collapse to B. Removing the
  source signs instead defines a different 31-letter domain with support ≤23.

The actual historical source-apostrophe rule adds `*`, allowing support ≤26;
therefore that extension is not rejected by the 25-symbol argument. Padding,
inserted markers, changing alphabets, polyalphabetic/homophonic substitution,
fractionation, and other compositions are also outside these proofs. GOST length
is variable, so there is no odd-length rejection; an encoded length of 97 permits
33–97 source letters. A romanization table alone supplies no exact English
translation/codebook inverse, cross-layer alignment, cipher family, or key.

## Shavian outcome

The inspected 1963 spelling guide supplies no pre-1990 reversible A–Z transport
encoding. The review reports phonemic/dialect variability and the same spelling
for too/two, so a conventional-English inverse needs extra specification.
Mathematically, all 48 symbols cannot inject into 26 single letters, and a
uniform two-letter transport plus length-preserving steps cannot yield 97 without
declared framing. Smaller message inventories, multicharacter encodings, context,
or a fixed codebook remain different models. No historical table was invented.
The outcome is **not yet a specified testable K4 model**, not “Shavian disproved.”

## Provenance and reproduction

See the [immutable run directory](../results/language-runs/20261018T111712Z-27a5aec4af474b789d386fcb5e4e67c0/manifest.json)
and its [LANG-001 result](../results/language-runs/20261018T111712Z-27a5aec4af474b789d386fcb5e4e67c0/LANG-001.json).
They record run ID/status, exact commits, code/input hashes, pair-enumeration
checksum, source counts, precise deductions, and exceptions. No Monte Carlo
control is required for these deterministic code/support arguments. No paid
submission, external verifier, or third-party outreach occurred.

```sh
python3 experiments/historical_language.py --spec-commit 21c3b4c16615586c525420cfdd6014cc7a6d44c4 --code-commit 58646022bf5578e4c193a6cdc7a487ef86c5947d
```

To reproduce the recorded implementation exactly, use the referenced code commit.
The user's next selected branch is the separately frozen masking pilots; the
word-interior-scrambling proposal remains recorded without a new search.
