# Calibration of the geometric-alphabet periodic crib fit

## Bottom line

The fit is worth checking, but not strong evidence for this cipher. A period-12 key has 12 unrestricted entries. Fitting a 13-letter crib determines those entries and leaves just **one closure condition**, not 13 independent predictions.

- **One fixed period-12 true-Beaufort model:** chance of this closure is 1/26 = 3.8462% for independent, uniformly distributed ciphertext letters. Preserving K4's actual letter histogram instead gives exactly 382/9,312 = **4.1022%**, about 1 in 24.4.
- **The actual searched family of 24 models:** 1,731 of 19,999 histogram-preserving random shuffles produced at least one first-crib survivor when all keys were refitted. The observed rate is **8.6554%**, about 1 in 11.6. The plus-one Monte Carlo p-value is **0.0866**, with a descriptive 95% Wilson interval of 8.2736%–9.0531% for the null exceedance probability.
- The real survivor already fails the second known plaintext check: it predicts **ZBVJDFKRUCA**, not **BERLINCLOCK**. The fixed cipher/key is therefore inconsistent with the supplied known plaintext, irrespective of its first-crib fit.

This is not a posterior probability that the proposed cipher is right. It calibrates only the frozen alphabet and the specified 24-model family, not every geometric representation, alphabet, crib choice, or other hypothesis previously considered. The shuffle null is an explicit exchangeability model, not a claim about how the unknown encryption was generated.

## Why only one test remains

The fixed alphabet is `OCSQVXWAGZITYDPBRKLFENMHJU`. All arithmetic uses its zero-based indices modulo 26.

For true Beaufort, C = K − P, so fitting a known plaintext letter sets K = C + P. Positions 22–34 contain 13 consecutive letters, so a period-12 key visits all 12 residues, repeating only its residue 9 (zero-based), at positions 22 and 34.

At those endpoints the ciphertext is F and S, and the plaintext is E and T. Their indices are F=19, E=20, S=2, T=11. The entire compatibility check at period 12 is thus:

    (19 + 20) mod 26 = (2 + 11) mod 26 = 13.

The other 11 key entries, and the initial value of this repeated entry, were fitted rather than predicted. For a fixed family and period p≤12 under iid-uniform ciphertext, 26^p of the 26^13 possible crib-window ciphertexts are consistent, so the per-model probability is 26^(p−13). This is a counting argument; it does not assume that the 24 model tests are independent.

“One survivor out of 24 tested models” is an outcome, not a probability of 1/24. A matched null must redo the whole fitting and selection procedure.

## Exact histogram-preserving period-12 calculation

Let n[x] be K4's count of the letter with index x. Under a uniform permutation of all 97 positions, the endpoint letters are drawn without replacement. True Beaufort requires C34 − C22 = 9 modulo 26. Therefore:

    Pr(pass) = sum_x n[x] n[(x+9) mod 26] / (97 × 96)
             = 382 / 9,312 = 191 / 4,656.

The additive equation C=P+K instead requires endpoint difference 17. Reversing ordered draws shows that it has the same probability. The two differences are distinct, so their events are disjoint. The union of those two period-12 models alone has exact null probability **8.2045%**. There is no independence approximation in these exact calculations.

## Matched family experiment

The analysis plan was fixed before running these simulations, but after seeing the real first-crib survivor. `preregistration.json` records that plan. It is not a prospective registration of the original geometry or cipher investigation.

Each of 19,999 replicates independently shuffles the original 97 ciphertext letters, preserving their full histogram. It then fits unrestricted periodic keys to EASTNORTHEAST at one-based positions 22–34 for every period 1–12 and both equations C=P+K and C=K−P. No periods were removed using actual-K4 exclusions. The statistic is the number of models passing the entire training crib; the real value is 1. The tail event is at least 1 survivor.

Null survivor-count distribution:

- 0 survivors: 18,268 replicates.
- 1 survivor: 1,728 replicates.
- 2 survivors: 3 replicates.

The empirical tail frequency is 1,731/19,999. The reported Monte Carlo p-value uses (1,731+1)/(19,999+1). The Wilson interval describes finite-simulation uncertainty, not uncertainty about the chosen null model. Berlin was not part of the null statistic, and is a public second-stage check rather than a blind holdout.

## Validation and reproduction

Python 3, standard library only. Run from this folder:

    python calibrate.py

The output is `result.json`. The seed is the big-endian integer represented by SHA-256 of the literal UTF-8 string `GEOMETRIC-PERIODIC-NULL-001`. Each replicate starts from a fresh copy of the original ciphertext and uses `random.Random(seed).shuffle`.

Validation completed:

- Frozen geometry SHA-256 verified; rank alphabet independently derived from primitive memberships, without changing geometry or feature order.
- 24 synthetic plants, one for every family/period, recovered the key, both cribs, and full plaintext.
- All 479,976 null/model pass/fail decisions matched an independent pairwise-difference implementation that never fits a key.
- 5,256 selected null/model cases also matched the pre-existing independent audit oracle, including fitted keys when successful.
- The exact period-12 histogram formula was checked by enumerating every ordered pair of distinct physical ciphertext positions.
- A repeated run produced identical `result.json` bytes.

Inputs, analysis code, results, and file hashes are included. The geometry represents declared modeled glyphs, not measured Kryptos glyphs. The prior audit's K4 source was [this fixed GitHub source revision](https://github.com/reggiechan74/kryptos-k4/blob/0d138240fb248d0b74942efc86a51d895946921d/data/k4.json); the provided input was used unchanged.

## Interpretation

The sensible investigation step was an independent known-plaintext check, which has now been done and failed. A new, independently motivated model could still be tested, but changing the model to rescue this particular fit would create a new hypothesis and require its own full search calibration. This result does not rule out every possible geometric encoding.
