# Probability calibration of the period-12 crib fit

22 October 2026. The EASTNORTHEAST fit was worth checking, but it supplies only
one constraint beyond fitted key values. Under the frozen 24-model selection
procedure, comparable first-crib fits occur in 1,731 of 19,999 histogram-preserving
shuffles. The actual fitted model already fails the public Berlin check.

## What was fitted and what was predicted

The frozen geometric alphabet is `OCSQVXWAGZITYDPBRKLFENMHJU`. The tested family
has 24 structures: periods 1–12 with unrestricted periodic keys under C=P+K or
true Beaufort C=K-P, modulo 26. It is the same family used in
[GEOMETRIC-PILOT-001](GEOMETRIC-PILOT-FINDINGS.md); no geometry, alphabet order,
period range or key rule was tuned for this probability calculation.

For period 12, thirteen consecutive crib letters determine all twelve key slots
and revisit just one slot. Positions 22 and 34 share residue 9 in zero-based
key indexing. Their pairs are E→F and T→S. In the frozen alphabet, F=19, E=20,
S=2 and T=11. The true-Beaufort closure is therefore
`(19+20) mod 26 = (2+11) mod 26 = 13`.

The other entries were fitted. This is one closure check, not thirteen independent
predictions. Under iid-uniform ciphertext the fixed-model chance is 1/26.
Preserving the observed K4 histogram gives the exact without-replacement chance
`382/(97*96) = 191/4656 = 4.1022337%`. The additive period-12 equation has the same
chance. Their required endpoint differences, 17 and 9 modulo 26, are distinct,
so their closure events are disjoint: their exact union probability is 8.2044674%.
This calculation does not assume independent model tests.

## Matched calibration of the complete frozen family

The supplied plan was fixed before simulation, after the actual fit was known.
It is a post-discovery calibration plan, not a prospective registration of the
original cryptanalytic idea. Each trial starts with a fresh copy of all 97 K4
ciphertext letters and shuffles them, preserving the full histogram. All 24
models are refitted to the first crib for every shuffle. The statistic is the
number of training survivors; the actual count is one and the tail is at least
one survivor. No periods are removed using actual-K4 exclusions.

| Survivors in a shuffle | Number of shuffles |
| ---: | ---: |
| 0 | 18,268 |
| 1 | 1,728 |
| 2 | 3 |

The empirical frequency is 1,731/19,999 = 8.6554%. The plus-one Monte Carlo
p-value is `(1731+1)/(19999+1) = 0.0866`. The descriptive Wilson 95% interval for
the chosen null's exceedance probability is 8.2736%–9.0531%. It describes finite
simulation uncertainty, not uncertainty over the null model itself.

This calibrates only the frozen 24 periodic models. It does not calibrate the
3,640 feedback models, all prior research choices, alternative alphabets or
geometries. A shuffle is an explicit exchangeability null, not an established
physical model of K4's encryption. The number is not a posterior probability
that the cipher is correct. One survivor among 24 structures is not a 1/24 chance.

## The decisive independent constraint

The period-12 true-Beaufort key predicts `ZBVJDFKRUCA` at positions 64–74, matching
only one of eleven required BERLINCLOCK letters. It is therefore contradicted
under the fixed model. Berlin is a public second-stage check, not historically
untouched data. It was not part of this null statistic. The first-crib chance
calculation cannot repair this exact second-crib failure.

## Replay and validation

Original files are preserved unchanged under
`independent/2026-10-22/periodic-crib-calibration/`. Source SHA-256 is
`3b41f37b3f7d911cb55eb61a8f5ab9188f6b3bf311992ea876d86b91f634a1a7`.
The received archive had SHA-256
`82e64742457729d04d92a9a02bc819c83cee85f03c02e6628436502cde9f575e`.
All member hashes were checked before execution.

The local replay reproduces the entire shuffle/count trace, all numerical fields
and all controls. The only changed result field is Python version: the original
used 3.12.14 and the local replay used 3.9.6. This metadata difference is recorded
explicitly; neither original source nor original output was patched.

Validation includes all 479,976 null/model outcomes against a separate pairwise
checker, 5,256 comparisons to the earlier oracle, 24 full planted recoveries,
and exact enumeration of all 9,312 ordered distinct position pairs for each
period-12 equation. The local integration also verifies Wilson endpoints through
the binomial score equation and all original file hashes.

```sh
python3 experiments/probability_radix_review.py
python3 -m unittest discover -s tests -v
```

That command copies calibration inputs to a temporary directory before replay,
so originals remain unchanged. The [local replay receipt](../results/GEOMETRIC-PROBABILITY-RADIX-LOCAL-REPLAY.json)
and [transfer receipt](../results/GEOMETRIC-PROBABILITY-RADIX-TRANSFER.json) preserve
exact hashes, checks, scope and the metadata difference. The separately supplied
[changing-base admissibility audit](RADIX-FEEDBACK-FINDINGS.md) is an exact
contradiction test, not another significance calculation.

Integration validation: all 267 repository tests pass in 9.545 seconds.
