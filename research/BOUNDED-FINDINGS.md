# Tested milestones and current decision boundary

18 October 2026. No K4 solution is claimed. The exact baseline is unchanged.
Source-method checks and the separate Firecrawl-worker receipt are linked from
the README. Supplied reports remain preserved, with later verification separate.

## Controls and structural results

CTRL-001 verifies complete K1, original K2, restored-S K2, and 336-letter K3
known-answer encryption and decryption. IQLUSION, UNDERGRUUND, DESPARATLY,
terminal Q, and literal question marks are explicit fixtures, not silently fixed.
The K3 rotation method matches all characters; independent photograph transcription
and physical paper reconstruction remain outstanding.

[STRUCT-001](STRUCTURAL-FINDINGS.md) proves the E-count contradiction for a
literal permutation-only pipeline, and saves all equality-conflict witnesses
for periodic bijective substitutions at the original alignment. Those statements
have exact model assumptions and no novelty claim.

## ROUTE-001: 13,056 exact constraint models

The [declared specification](BOUNDED-SPEC.md) generated 66 distinct complete
97-position permutations after deduplicating six widths, eight readings per
width, all inverses, and identity. Both operation orders, two alphabets, and
three modular equations were tested. Nonidentity routes tested periods 1–16;
identity tested periods 1–96. No missing phase was guessed.

All 282 compatible models use the identity route. Their periods are 27–29 or
53–96; each has between 3 and 72 unobserved key phases. **Zero complete keys or
plaintexts emerged.** Passing sparse constraints at a long period supplies no
positive evidence for that period. The route result excludes only these concrete
route/alphabet/equation/period combinations; it does not reject all spatial
operations, arbitrary mixed alphabets, or other operation grammars. Plus/minus
models overlap by key negation and are not independent supporting observations.

## RUNKEY-001: 28,488 literal-window models

Streams: corrected K2 (370 letters), K3 (336), and K1+corrected K2+K3 (769),
plaintext and ciphertext separately. There were 4,748 window/direction cases,
2,692 unique key strings, and 28,488 cases after two alphabets and three equations.
Windows were exactly 97 consecutive letters, without wraparound; question marks
were removed explicitly. **No case matched all 24 crib letters.** The maximum
partial match was 6/24, reported descriptively only. Many source windows recur
inside the concatenated stream, so case count is not a count of independent keys.

The preregistered 199-shuffle whole-search calibration was conditional on an
all-crib survivor. Since there were none, it was not run. Nothing here rejects
a different text source, extraction, key transform, as-carved K2 variant, unknown
alphabet, or different composition.

## TRIFID-001: 144 fixed-cube models

A–Z+? and KRYPTOS+? cubes, 36 block periods (1–32,42,49,63,97), both directions,
exactly as specified. All complete inverse checks pass, including the 27th symbol
and short final blocks. **No model matched all cribs**; the largest descriptive
match was 4/24. This does not reject a differently keyed cube, framing convention,
separator inclusion, or Trifid as a component in a multilayer construction.

## STAT-001: diagnostic calibration, not cipher identification

The published width-21 phenomenon is reproduced: among 76 ordered lag-21 pairs,
11 are duplicate excess, with exactly the published repeated pair types. At
this particular input all repeated types occur twice. The implementation uses
sum(count−1), which differs from sum(count choose 2) when a pair occurs three
or more times; those alternatives must not be silently conflated.

With seed 20261018, 9,999 histogram-preserving shuffles were split into 4,999
calibration and 5,000 evaluation draws. Width 21 was the observed raw maximum
among widths 1–48. Evaluation results:

| Statistic | Exceedances / 5,000 | Plus-one empirical tail | Wilson 95% interval for underlying null tail |
| --- | --- | --- | --- |
| Fixed width 21 | 1 | 0.000400 | 0.0000353–0.001132 |
| Standardized maximum over 48 widths | 53 | 0.010798 | 0.008113–0.013838 |

The maximum uses calibration-only means/standard deviations, then the same
frozen maximum statistic on held-out evaluation permutations. Width-specific
and maximum statistics have different reference distributions. These are
conditional permutation-tail estimates, not probabilities that a cipher model
is correct. The intervals quantify finite evaluation-sampling uncertainty,
conditional on the calibration estimates; they do not include uncertainty from
choosing the diagnostic family after observing K4, historical multiple testing,
or selecting another null model. This is a limited independent diagnostic check,
not a reproduction of Bean's entire paper or Gromark search. The anomaly does
not determine whether any substitution, transposition, or numeric generator caused it.

## Reproduction and resource use

```sh
python3 experiments/check_baseline.py
python3 experiments/check_controls.py
python3 experiments/structural_checks.py
python3 experiments/run_bounded.py
python3 experiments/statistical_diagnostics.py --write-results
python3 -m unittest discover -s tests -v
```

All runs use one local process, the Python standard library, and no network.
The first three bounded model scans together took under one second, excluding
synthetic controls; the 9,999-shuffle diagnostic took about 3.3 seconds. Code and
input hashes, environment, seed, parameters, complete compatible assignments,
and raw null draws are saved in `results/`. Large detailed JSON artifacts are
gzip-compressed with deterministic headers; summary JSON stays readable.

To inspect a compressed result with the standard library:

```sh
python3 -m gzip -d -c results/ROUTE-001.json.gz
python3 -m gzip -d -c results/STAT-001.json.gz
```

Seeded controls recover 20 planted route/period models and 20 planted contiguous
running-key windows through the actual constraint/scanning code. Every Trifid
symbol and stated period is covered by inverse controls. No external solution
checks, paid submissions, third-party contact, or executable third-party code.

## What supplies the next useful constraint

Expanding alphabets, translations, routes, or arbitrary keystreams merely to
obtain readable output is not a next milestone. The useful branches now need
an independent specification: a historical script/romanization table with a
reversible A–Z representation, a new physically justified route or keyword,
or a tightly defined numeric generator supported by source evidence. Before
expanding compute, register the selected branch, its finite parameter bounds,
and a source-based reason to prefer it. K3 photograph transcription and the
biographical claim ledger are useful evidence work that can continue without
asserting a cipher solution. The completed finite checks do not establish that
any such branch is right.
