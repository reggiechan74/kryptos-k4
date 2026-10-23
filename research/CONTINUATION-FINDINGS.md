# K4 continuation: exact feedback constraints and split-coordinate routes

22 October 2026. **No candidate or solution.** The previously unrun
ASYMMETRIC-FEEDBACK-001 and SPLIT-COORDINATE-001 families are now complete:
all 72 mixed-alphabet feedback configurations are impossible for any primer;
all 32 fixed split-coordinate routes fail the confirmed cribs. This does not
exclude other alphabet constructions, feedback rules, lags or fractionation.

## Priorities, inputs and chronology

The repository was clean on `research/dynamic-key-20261022` at
`6eba0fd0166852da5b1c9301f85def34e2b45657`. Existing ledgers, specifications,
artifacts, tests and policy were read before work. No applicable AGENTS.md was
found. Previous negative experiments and the geometry audit were preserved.
No Site edit, optical test, remote fetch, push or third-party execution occurred.

Priority 1 was the 72-case arbitrary-primer feedback audit because it closes a
specific local proof assumption and selected published threshold gaps, rather
than trying more words after the earlier five-letter partial score. Its
previously committed specification remained unchanged. Priority 2 was the
split-coordinate proposal, whose component routing differs from whole-letter
transposition; its widths 7 and 21 remain postselected diagnostic choices,
not independent clues. A new full specification was committed before its code.

| Experiment | Specification commit | Code commit | Run time / cap |
| --- | --- | --- | --- |
| ASYMMETRIC-FEEDBACK-001 | `56b2919e4af7bbce644ed476d5fde8c0546627b7` | `0a5ad2dea648397e40678177c0d1f0515d96e029` | 0.503 s / 60 s |
| SPLIT-COORDINATE-001 | `afcb5e6297d868b38722b695c96e1ee8468363a3` | `11ce1453f0480103af21cd7c964084f3bf1e5a4b` | 0.290 s / 30 s |

Both actual runs completed exactly once after their specification/code commits.
The shared runner verifies the specification's unchanged bytes and ancestry,
and every consulted code/input file against its recorded implementation commit.
Existing atomic snapshot infrastructure preserves results and marks interrupted
attempts incomplete. No scope or parameter was changed after seeing K4 scores.

The verified 97-letter fixture and one-based inclusive crib positions were used.
The parent's independent methodology reviewer supplied these primary-source
anchors; all four agree exactly with `data/k4.json`:

| Positions | Ciphertext | Plaintext |
| --- | --- | --- |
| 22–25 | FLRV | EAST |
| 26–34 | QQPRNGKSS | NORTHEAST |
| 64–69 | NYPVTT | BERLIN |
| 70–74 | MZFPK | CLOCK |

Source: [CIA sculpture page](https://www.cia.gov/legacy/headquarters/kryptos-sculpture/).
The comparison was performed locally against supplied anchors; this executor did
not conduct a new photographic transcription. The baseline and K1–K3 controls
ran before each actual experiment. No shifted cribs or speculative plaintext
was added.

## ASYMMETRIC-FEEDBACK-001: all primers, 72 fixed models

Select plaintext, ciphertext and key/feedback alphabets independently from AZ
and KRYPTOS, excluding the two all-equal triples. Six role triples, three
modular equations and plaintext-feedback lags 9–12 give **72 configurations**.
For i below the lag L, each primer character is independent; afterward the key
is the plaintext character P[i-L], explicitly reindexed through the key alphabet.
No indicator shift, ciphertext feedback, route or extra alphabet was allowed.

Writing sigma/tau for (+1,+1), (+1,-1), or (-1,+1):

```
index_Ac(C[i]) = sigma * index_Ap(P[i]) + tau * index_Ak(K[i]) mod 26
```

Each residue class modulo L has one free initial root (equivalently one primer
symbol). Every symbol-to-symbol transition is a bijection, even when reindexing
makes the same-alphabet affine formula inapplicable. Back-propagating a known
letter through its ciphertext lane forces one unique root. Two different
required roots in a lane are a complete contradiction, including when the
path crosses unknown plaintext positions. Every implied root and first conflict
is retained. A first constraint in a lane fixes a parameter; it is not an
independent check.

| Lag | Configurations | Primer symbols before cribs | First-crib occupied lanes | Actual training checks | Berlin predictions if training passes | All-crib equality checks | First-crib survivors | All-crib compatible |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 9 | 18 | 9 | 9 | 4 | 11 | 15 | 0 | 0 |
| 10 | 18 | 10 | 10 | 3 | 11 | 14 | 0 | 0 |
| 11 | 18 | 11 | 11 | 2 | 11 | 13 | 0 | 0 |
| 12 | 18 | 12 | 12 | 1 | 11 | 12 | 1 | 0 |

The 13 consecutive EASTNORTHEAST positions cover every lane for these lags.
Thus all roots are fixed after training if it is consistent; there are no
untrained lanes in Berlin. All 11 Berlin predictions are checked **without
refitting**. Both crib blocks were public before model selection, so this is a
useful held-out consistency diagnostic, not independently obtained evidence.
All 72 models have zero compatible primers; no arbitrary primer was filled,
no full plaintext from a rejected model was generated or promoted to a candidate.

The only training survivor uses Ap=AZ, Ac=AZ, Ak=KRYPTOS, true Beaufort, lag 12.
After fitting the first crib it predicts **BUMFOPKVOMG**, versus **BERLINCLOCK**:
only positions 64 and 72 agree, **2/11**. Known positions 29 and 65 force root
values 4 and 23 in lane 4. Their retained paths pass through one-based positions
5,17,29 and 5,17,29,41,53,65. This is an exact model contradiction, not a language
score. No solution is claimed from a training fit with only one real check.

### Null calibration and controls

For each of 199 histogram-preserving ciphertext shuffles, every configuration
was re-evaluated and roots were refitted exactly as for K4. The statistic is
maximum achievable same-data crib agreement, computed by taking the modal
required root within each lane and maximizing over the 72 configurations.
A partial match count with fitted roots is not comparable to a fixed-key score.
Seed 20261023, `random.Random`/MT19937; fresh original ciphertext each draw.

Observed maximum **15/24**; **35/199** null maxima are equal/higher;
plus-one conditional tail **36/200 = 0.18**. Null maximum distribution:
13(35), 14(129), 15(34), 16(1). Total **14,400 model evaluations**. The result
provides no useful support for the family under this exploratory diagnostic.

Controls pass:

- 72 planted arbitrary-primer sequential encrypt/decrypt recoveries, exact root
  recovery, complete candidate gates and 72 altered-constraint rejections.
- 108 tiny-alphabet role/equation/lag/constraint cases, compared against 1,080
  exhaustive primer decryptions, including empty/underdetermined constraints.
  Both exact solution counts and optimized modal-root scores agree.
- 24 synthetic same-alphabet limiting cases agree with the established affine
  solver's classifications and independent-check counts.
- An independent saved-certificate audit forwards all 26 possible roots through
  each known-letter lane, verifying each forced root and every rejection witness.
  It separately regenerates the first-crib survivor's Berlin predictions.

This closes exactly the declared mixed-role lags/equations for arbitrary primers,
which is stronger than the earlier six literal PALIMPSEST negatives. It is not
an exclusion of different lags, keys with extra state, other alphabets or composites.
Historical source/threshold context remains in the unchanged specification and
prior-art review; no general novelty claim is made.

## SPLIT-COORDINATE-001: 32 distinct fixed routes

Map letters through AZ or KRYPTOS into a row-major 2x13 or 13x2 grid. Independently
permute its row-coordinate and column-coordinate streams using ragged row-fill,
column-read routes of widths 7 and 21, in either assignment and forward/inverse
independently. Empty cells are skipped; no padding, phase, shift, fitted alphabet,
key or extra substitution is allowed. Each configuration has **zero fitted
parameters**. Candidate acceptance requires all 24 letters and complete 97-letter
inverse/regeneration; first/second crib scores are reported separately.

All 32 formal cases are also **32 distinct transformations**. Equivalence was
checked by complete functional truth tables at every output position over its
one or two source-letter variables, canonicalizing variable order and collapsing
coincident sources to the reachable diagonal. SHA256 records the signatures;
exact byte equality, not hash equality alone, determines equivalence. This is
stronger than assuming different parameter labels imply different transforms.

All 32 cases fail. Maximum **3/24**, attained twice:

| Case | Alphabet/grid | Encoding row route | Encoding column route | Matched one-based positions | East/Berlin |
| --- | --- | --- | --- | --- | --- |
| SC-004 | AZ, 2x13 | width 21 forward | width 7 forward | 22,65,74 | 1/13, 2/11 |
| SC-026 | KRYPTOS, 13x2 | width 7 inverse | width 21 forward | 30,34,73 | 2/13, 1/11 |

The run decrypts with each encoding transform's exact inverse; all outputs
re-encode fully, which is an invertibility control, not cryptanalytic evidence.
Complete outputs are retained as **rejected_model_output**, not decoded plaintext.
There was no candidate generation or crib fitting within this family.

Each of 199 fresh histogram-preserving shuffles was evaluated on the whole
32-model catalogue: seed 20261027, `random.Random`/MT19937. Maximum matched crib
letters was equal/higher in **160/199** draws; plus-one conditional tail
**161/200 = 0.805**. Null maxima: 1(1), 2(38), 3(86), 4(54), 5(17), 6(3).
Total **6,400 formal and distinct model evaluations**. No route was changed
or added after these scores.

Controls pass:

- 32 planted full-message inverses containing both exact crib blocks, 32 altered
  crib rejections, and 64 comparisons with a separate explicit matrix-cell oracle.
- 21,632 source-letter-pair grid/recombination checks across all formal cases.
- 24 ragged-route checks on unique position indices, plus hand-computed ragged
  answers and full inverse permutations, including holes and short streams.
- Exact-signature controls include identical copies, a deliberately different
  route and different alphabet/grid descriptions of the same whole-letter route.
- Independent saved-output audit re-encodes every one of 3,104 output letters,
  recomputes crib matches and checks no free parameters/candidates were introduced.

Width choices remain postselected and geometric fractionation remains speculative.
The general historical fractionation sources do not establish this exact recipe
or artist use. No other fractionation scheme is excluded.

## Multiplicity, validation and next decision

The two statistics differ because one optimizes unknown roots while the other
has no fitted parameters. They must not be ranked by raw agreement count.
Each empirical maximum corrects only for the correlated configurations searched
within its own declared family. Resolution is 1/200; neither calculation corrects
for all previous exploratory work, validates historical intent, or supplies new
plaintext evidence. No language model or attractive partial English was used.

**174 tests pass in 9.324 seconds**, including both new control sets, independent
artifact/certificate checks, all prior fixtures and saved experiments. The full
suite did not repeat either new actual experiment/null search. Hashes and
specification ancestry match. [Validation receipt](../results/CONTINUATION-VALIDATION.json).
The physical geometry and heading remain unsurveyed; no shadow/altitude conclusion
or public Site change is part of this batch.

The immediate next step is **exact route-overlap bookkeeping** for the independent
researcher's forthcoming K3-derived two-stage route definition. ROUTE-001 already
covered 66 complete 97-position permutations, including width-14/42 single routes
and inverses, periods 8/10 within 1–16, both alphabets, three equations and both
layer orders. Its existing 282 compatible cases are vacuous identity-route fits,
not candidates. The ledger does not explicitly list the proposed two-stage
composition; equivalent composite permutations may nevertheless already be
present. Do not infer the route from shorthand or claim novelty. Wait for the
complete fill/read/hole/inverse definition and reference control, compare exact
97-position permutations to the frozen catalogue, and retire exact duplicates
without rerunning their cipher tests. Only a distinct fully specified route could
justify a newly committed bounded experiment. No provisional route was implemented.

**Status correction, 23 October 2026:** the four specified adjacent affine-digraph
cases are [analytically excluded](AFFINE-DIGRAPH-PARITY-BOUNDARY.md); no key search
is required. The following earlier next-step suggestion is historical.

The previously formulated affine-digraph feasibility audit remains a lower-evidence
alternative, unrun and requiring its own exact prior-art check. Neither suggestion
extends this completed batch or provides a reason to tune rejected families.

## Reproduce and artifacts

```sh
python3 experiments/asymmetric_feedback.py --spec-commit 56b2919e4af7bbce644ed476d5fde8c0546627b7
python3 experiments/split_coordinate.py --spec-commit afcb5e6297d868b38722b695c96e1ee8468363a3
python3 -m unittest discover -s tests -v
```

The runner requires all consulted files to match its recorded HEAD commit and
writes a new atomic snapshot; use the recorded implementation revision when
replaying that exact code. A rerun is unnecessary for certificate verification.
The four artifact tests independently audit the existing saved results.

[Feedback result](../results/asymmetric-feedback-001-runs/20261022T191952Z-44bf1543c641497e82f4b948d0cd94ea/ASYMMETRIC-FEEDBACK-001.json),
[feedback manifest](../results/asymmetric-feedback-001-runs/20261022T191952Z-44bf1543c641497e82f4b948d0cd94ea/manifest.json),
[coordinate result](../results/split-coordinate-001-runs/20261022T192126Z-2ff96ae3a6914cab8db6cd9c0c7ceb5c/SPLIT-COORDINATE-001.json),
[coordinate manifest](../results/split-coordinate-001-runs/20261022T192126Z-2ff96ae3a6914cab8db6cd9c0c7ceb5c/manifest.json).

## Subsequent frozen-route batch — 22 October 2026, 19:32 UTC

The complete K3-derived/clock route definitions arrived and the earlier overlap
check recommendation was completed. Sixteen full-domain prior equivalents were
skipped; all 374 new structures were rejected. The
[K3/clock findings](K3-CLOCK-ROUTE-FINDINGS.md) record the verified K3 reference,
gauge-aware sandwich counts, exact certificates, controls and 187-test validation.
This updates the earlier provisional status without changing its results.
