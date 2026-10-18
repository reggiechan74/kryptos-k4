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

## Initial roadmap

1. Verify baseline transcription and crib positions against primary sources;
   record source dates and exact evidence.
2. Reproduce published K1–K3 techniques and known plaintext as controls before
   applying implementations to K4.
3. Inventory published experiments, distinguishing author claims from local
   reproduction; record coverage, assumptions, and missing artifacts.
4. Test bounded hypotheses with explicit budgets, deterministic commands, and
   narrowly stated conclusions.

See [research policy](research/POLICY.md), [hypothesis log](research/HYPOTHESES.md),
[experiment log](research/EXPERIMENTS.md), and [published inventory](sources/EXPERIMENTS.md).
