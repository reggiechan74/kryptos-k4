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

The later [World Clock / ENE geographic note](docs/world-clock-ene-geography.md)
records supplied approximate map comparisons and uncertainty, without a cipher
search, exhaustive landmark claim, or key derivation.

The [bounded 1985 map report](docs/berlin-period-map-corridor.md) separates the
clock-terminal approach, fixed geometric reflection, and unequal walking halves.
German-initial extraction remains uninstantiated. The
[direct Enigma boundary](docs/direct-enigma-boundary.md) rejects only the direct
aligned standard reflector model using the confirmed K→K at position 74.
[Latest validation](results/PERIOD-MAP-ENIGMA-VALIDATION.json) records the local
regression replay; earlier validation receipts are preserved.

[Neptune discovery and clock-face assessment](docs/neptune-discovery-assessment.md)
preserves the supplied historical review, both coordinate source pairs, and
unverified panel-orientation/1989-inscription gates. The 11-letter city-name
coincidence is exploratory; no key or new cipher result is claimed.

[Clock-boundary verification](research/CLOCK-RESET-PROOF.md) confirms 13 already
known contradiction certificates, subsuming 72 declared formal cases without a
candidate scan. The identical-reset collision is narrow; stateful feedback,
transposition and different keys are outside its scope. All 90 tests pass;
[validation and chronology receipt](results/CLOCK-BOUNDARY-VALIDATION.json).

[Historical clock inscriptions](docs/historical-clock-inscriptions.md) preserves
dated photographic differences, including before 1990, while exact ENE orientation
and the full 1989 candidate panel remain unresolved.
[The Egyptian sign-list hypothesis](docs/egyptian-sign-list-feasibility.md) records
real Egyptian context and the missing reversible mapping; no new cipher run.

[Barney/Scott prior-art review](docs/prior-art-barney-scott-review.md), revised
2026-10-18, pins source commits and distinguishes exact overlap from incomplete
or heuristic coverage. Third-party code was read, never executed; the 9/10
fingerprint remains descriptive and is not a hard candidate filter.

[Exact direct-autokey audit](research/AUTOKEY-CONSTRAINT-FINDINGS.md) retains
all lags 1–96 without check-count filtering: 732 of 1,152 configurations contradicted,
420 compatible but underdetermined, all with zero independent consistency checks.
No primer search or full plaintext output. All 97 tests pass; existing results retained.

[One published Gromark tuple](research/GROMARK-ALPHABET-FINDINGS.md) passes
complete alphabet feasibility. Two distinct gauge-fixed witnesses verify, showing
nonuniqueness; neither recovers historical alphabets or meaningful plaintext.
All 104 tests pass. No additional survivors or width-21/fingerprint filters tested.

[Fixed-tuple identifiability](research/GROMARK-IDENTIFIABILITY-FINDINGS.md) maps
all 73 noncrib positions: 10 model-forced, 63 variable, 0 unresolved. These are conditional
on the selected arbitrary tuple, not confirmed plaintext. Every classification
has a checked certificate; no K4 search fallback was needed. All 112 tests pass.
[Research strategy](docs/research-strategy.md) separates proofs, finite negatives,
heuristic failures and underdetermination. The audit stops pending independent evidence.

[Photographed silk-chart pilot](research/SILK-PERIODIC-FINDINGS.md) contradicts
all hypothetical direct repeating-key periods 1–12: the first crib requires 13
distinct keys in 13 consecutive positions. All 118 tests pass. [Source scope](docs/silk-chart-source-and-scope.md)
distinguishes modern provenance, checked pixels and unestablished creator use.

[True-Beaufort base-60 audit](research/BASE60-BEAUFORT-FINDINGS.md) now has
complete exact coverage: 23,115,600 unique primers rejected analytically and
3,240,000 evaluated, with zero feasible or unresolved cases. The unchanged two
recurrences at lengths 2–4 are contradicted under direct shared-alphabet
true Beaufort. All 127 tests pass. [Continuation receipts](results/BASE60-BEAUFORT-CONTINUATION-VALIDATION.json)
preserve exact ranges and the earlier partial checkpoint. No broader cipher-family
exclusion follows. [Seasonal light and pool reflection](docs/seasonal-light-source-review.md)
remain separate, source-qualified hypotheses with no optical search.

[Fixed CL→KL spelling pilot](research/PHONETIC-CL-FINDINGS.md) passes 292
synthetic recovery cases and preserves original/transformed crib distinctions.
The mask is lossy. Its periods 1–12 arithmetic models inherit existing first-crib
contradictions: 144 saved witnesses, **no new K4 key search**. All 133 tests pass.

[Stateful key continuation](research/DYNAMIC-KEY-FINDINGS.md), 22 October 2026:
1,248 progressive-cycle cases (known prior art, controlled local replication)
and 96 fixed ciphertext-triggered extra-step cases all contradict the cribs.
199 whole-family shuffled controls show no useful excess of crib agreement.
147 suite tests plus three saved-certificate audits pass. Three distinct
mechanisms are ranked, with asymmetric-alphabet feedback recommended next after
prior-art scope review. No new plaintext or solution is claimed.

[Fixed asymmetric-feedback and plaintext-step pilots](research/FIXED-PILOT-FINDINGS.md)
complete this batch: all six literal PALIMPSEST feedback models and twelve
plaintext-triggered step models fail the cribs. The six-model best score is
5/24 with conditional shuffle tail .015, but it fails 19 confirmed letters and
is rejected. Final full suite: 160 tests pass. The broader arbitrary-primer
audit remains registered but unrun; no score-driven parameter expansion or
solution claim follows.
