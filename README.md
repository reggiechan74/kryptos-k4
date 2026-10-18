# Kryptos K4 research

A reproducible workspace for investigating Kryptos K4. No solution is claimed.

## Baseline

The ciphertext contains 97 uppercase letters. Confirmed plaintext cribs use
**one-based, inclusive** positions:

| Positions | Plaintext | Python slice | Ciphertext at those positions |
| --- | --- | --- | --- |
| 22–34 | EASTNORTHEAST | `[21:34]` | FLRVQQPRNGKSS |
| 64–74 | BERLINCLOCK | `[63:74]` | NYPVTTMZFPK |

The machine-readable baseline is [data/k4.json](data/k4.json). Trailing spaces
and punctuation in prose are not part of the ciphertext. Cribs constrain the
plaintext at those indices; they are not literal substrings of the ciphertext.

## Status and evidence

The research brief reports that archival researchers privately recovered the
plaintext in September 2025 without deriving the cipher, and that no publicly
accepted cryptanalytic solution is recognized by the current steward. Recovery
of plaintext from archives and derivation of a reproducible cipher solution are
different achievements. See [sources](sources/README.md) for the supplied links
and the source-verification limitation of this initial scaffold.

Separate public facts, hypotheses, and unverified third-party experiments.
Neither a plausible phrase nor a crib match establishes a solution. A candidate
method should account for all 97 characters and support independent reproduction.

## Run locally

Requires Python 3.8+; standard library only. From this directory:

```sh
python3 experiments/check_baseline.py
python3 -m unittest discover -s tests -v
```

These commands validate data and indexing only. They do not test cipher families.

## Research documents

- [Designer context and working vocabulary](docs/designer-context.md): source-attributed
  evidence, historical boundaries, and a proposed K1–K3 workshop.
- [Language and alphabet layers](docs/language-and-alphabet-layers.md): translation,
  transliteration, Shavian, crib constraints, and falsifiable experiment designs.

These documents were supplied as research findings dated 18 October 2026 and
are preserved as supplied. Their statements about reviewed sources and prior
computational checks belong to that supplied research; the repository update
did not independently retrieve those pages or reproduce those checks. Proposed
experiments are not completed results or a K4 solution. The source-provenance
limitation recorded for the initial scaffold remains separate from this material.

## Initial roadmap

1. Verify baseline transcription and crib positions against primary sources;
   record source dates and exact evidence.
2. Follow the [designer-context workshop](docs/designer-context.md#reproducible-workshop-k1k3-before-k4)
   to reproduce published K1–K3 techniques and known plaintext as controls before
   applying implementations to K4. Preserve K2 correction variants and require
   full K3 permutation/inverse comparisons.
3. Inventory published experiments, distinguishing author claims from local
   reproduction; record coverage, assumptions, and missing artifacts.
4. Specify the [language-layer feasibility checks](docs/language-and-alphabet-layers.md#6-falsifiable-experiment-sequence):
   historical conventions, reversible encodings, length/framing constraints, and
   crib alignment before any search. Then test bounded hypotheses with explicit
   budgets, deterministic commands, and narrowly stated conclusions.

The [research roadmap](research/ROADMAP.md) gives the next-step sequence and
acceptance gates. This documentation update implements and runs no new searches.

See [research policy](research/POLICY.md), [hypothesis log](research/HYPOTHESES.md),
[experiment log](research/EXPERIMENTS.md), and [published inventory](sources/EXPERIMENTS.md).
