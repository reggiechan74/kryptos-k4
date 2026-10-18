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

The [Firecrawl source-verification receipt](docs/source-verification-2026-10-18.md)
records RR Auction's report that archival researchers recovered plaintext in
September 2025 without acquiring the method/key. The latest checked steward
publication still calls K4 unsolved. These are compatible, attributed statements:
plaintext discovery and a reproducible cryptanalytic solution are different
achievements. See [local fixture provenance](sources/VERIFICATION.md) for the
separate exact-transcription and method checks.

Separate public facts, hypotheses, and unverified third-party experiments.
Neither a plausible phrase nor a crib match establishes a solution. A candidate
method should account for all 97 characters and support independent reproduction.

## Run locally

Requires Python 3.8+; standard library only. From this directory. Before the
snapshot runner commands, set `KRYPTOS_SPEC_COMMIT` to a full commit SHA that
contains the unchanged current `research/BOUNDED-SPEC.md`. In a clean Git
checkout containing that specification, `git rev-parse HEAD` supplies the SHA.
The offline runner records this reference and file hash; repository history must
be checked separately. Baseline checks and unit tests do not require the variable.

```sh
python3 experiments/check_baseline.py
python3 experiments/check_controls.py
python3 experiments/structural_checks.py
python3 experiments/run_bounded.py --spec-commit "$KRYPTOS_SPEC_COMMIT"
python3 experiments/statistical_diagnostics.py --write-results --spec-commit "$KRYPTOS_SPEC_COMMIT"
python3 -m unittest discover -s tests -v
```

The baseline command validates data and indexing. The controls command checks
full K1, both K2 variants, and K3 encryption/decryption against fixed fixtures.
It does not establish a K4 method.

## Latest registered outcomes

The requested language → masking → word-scrambling sequence is complete:

- [Language feasibility](research/LANGUAGE-FINDINGS.md): 37,060 exact GOST
  round trips pass; two narrowly defined output models fail support constraints.
  Shavian lacks a sourced complete reversible pipeline; none was invented.
- [Masking pilots](research/MASKING-FINDINGS.md): all 12fixed autokey models fail
  cribs; both fixed Fractionated Morse maps fail strict parsing.
- [Word-interior proposal](research/WORD-SCRAMBLING-FINDINGS.md): all 24fixed
  combinations fail endpoint/count invariants; no broader cipher claim follows.

The subsequent [narrow respelling gate](research/PHONETIC-FEASIBILITY.md) leaves
all four clue words unchanged and rescues none of the same 12 autokey outputs.
Length-changing phonetic rules and German translation remain unspecified; no
flexible decoding or shifted cribs were used.

Each specification was committed before implementation and the actual run;
immutable manifests record spec/code commits, hashes, controls, and status.
No K4 solution is claimed. Older milestones and audited results remain preserved.

## Research documents

[Current milestones](research/BOUNDED-FINDINGS.md) and the
[Firecrawl verification receipt](docs/source-verification-2026-10-18.md) record
subsequent source checks and tested results. The receipt was supplied by the
research worker who performed those Firecrawl reads; the local coding executor
did not independently perform that scrape session.

- [Designer context and working vocabulary](docs/designer-context.md): source-attributed
  evidence, historical boundaries, and a proposed K1–K3 workshop.
- [Language and alphabet layers](docs/language-and-alphabet-layers.md): translation,
  transliteration, Shavian, crib constraints, and falsifiable experiment designs.

These documents were supplied as research findings dated 18 October 2026 and
are preserved as supplied. Their statements about reviewed sources and prior
computational checks belong to that supplied research; the original documentation update
did not independently retrieve those pages or reproduce those checks. Later
verification is recorded separately in [the source ledger](sources/VERIFICATION.md). Proposed
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
acceptance gates. See the milestone records in [the experiment log](research/EXPERIMENTS.md).

See [research policy](research/POLICY.md), [hypothesis log](research/HYPOTHESES.md),
[experiment log](research/EXPERIMENTS.md), and [published inventory](sources/EXPERIMENTS.md).

Current results: [exact structural constraints](research/STRUCTURAL-FINDINGS.md)
and [experiment log](research/EXPERIMENTS.md). No K4 solution is claimed.

[Focused audit hardening](research/AUDIT-HARDENING.md) preserves the original
artifacts and corrects interpretation/control-coverage claims. All 282 long-period
fits are vacuous, not candidate evidence. New runner snapshots require a prior
specification commit and publish explicit completion status atomically. The
original spec/results shared a commit, which does not prove preregistration.

[K3 worksheet verification](docs/k3-worksheet-verification.md) distinguishes
336-letter computational equivalence from partly reconstructed historical procedure.

Current validation: [77 passing tests](results/SEQUENTIAL-BRANCHES-VALIDATION.json),
including immutable artifact/hash replays. [Specification chronology](results/SPECIFICATION-CHRONOLOGY.json)
records each new specification before its code and actual run.
