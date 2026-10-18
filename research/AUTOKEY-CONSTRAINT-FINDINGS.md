# Direct autokey: exact constraint coverage, including vacuous cases

AUTOKEY-CONSTRAINT-001. Revision: 2026-10-18. No K4 solution or recovered key.

The completed audit classifies **1,152** declared configurations: **732
contradicted**, **420 compatible but underdetermined**, **0 untested**. Every
compatible configuration has **zero independent consistency checks**. Compatibility
therefore supplies no positive evidence for this mechanism. No primer strings
were searched or filled, and no full K4 plaintext was emitted.

## Exact scope

Two fixed alphabets: ordinary A–Z and `KRYPTOSABCDEFGHIJLMNQUVWXZ`. Plaintext,
ciphertext, primer and feedback use the **same selected alphabet** for indexing.
Three equations modulo 26: C=P+K, C=P−K, C=K−P. Both feedback modes use a
forward, left-to-right recurrence with unchanged letter alignment and lag L in
1–96 inclusive. The first L key symbols are independent arbitrary primer symbols;
afterward K_i is P_(i−L) or C_(i−L). The primer does not repeat or cycle.

This is 2 alphabets × 3 equations × 2 feedback modes × 96 lags. It excludes no
backward, mixed-alphabet, indicator-shift, reset, transposition, typo, null,
language-layer or unspecified composite model. Earlier finite literal-primer
results and their artifacts remain intact.

| Feedback | Contradicted lags, for each alphabet/equation | Compatible but underdetermined lags | Configurations contradicted / compatible |
| --- | --- | --- | --- |
| Plaintext | 1–26 and 30–52 | 27–29 and 53–96 | 294 / 282 |
| Ciphertext | 1–73 | 74–96 | 438 / 138 |

The complete records retain all lags, counts and a first exact conflict witness.
No minimum-check threshold was applied. A zero-check case still has 24 crib
constraints anchoring independent parameters; it lacks any remaining comparison
that could test consistency. In compatible cases there are exactly 26^(L−24)
primer solutions: plaintext-feedback cases have 3–5 or 29–72 free symbols;
ciphertext-feedback cases have 50–72. These are counts, not candidate keys.

## Why the constraints are exact

Write C_i = sigma P_i + tau K_i, with sigma and tau equal to ±1 as fixed by the
three equations. The inverse uses sigma because its square is one.

For plaintext feedback,

```text
P_i = sigma C_i − sigma tau P_(i−L)
P_i = alpha_i x_(i mod L) + beta_i
alpha_i ∈ {−1,+1}; x_r = P_r for r < L
```

Propagating known ciphertext along each residue chain determines alpha and beta.
Each crib fixes that chain's root. Two incompatible root values prove an exact
contradiction, including when the intervening plaintext is unknown. If R distinct
residue chains contain cribs, there are 24−R independent consistency comparisons
and L−R free primer parameters if compatible. All coefficients used to solve for
a root are units modulo 26; no field assumption is made. The first-L plaintext
roots and initial key symbols are bijectively related, so consistent roots are
also sufficient for a complete algebraic model.

For ciphertext feedback, P_i = sigma(C_i−tau C_(i−L)) is deterministic when
i≥L. Every crib there is an independent check. A pre-lag crib instead fixes its
own otherwise arbitrary primer entry. Thus checks = #known i≥L, and free primer
symbols = L−#known i<L, provided those deterministic checks pass.

### Regression that immediate-neighbor checks miss

At plaintext-feedback lag 26 with A–Z and C=P+K, the known E at one-based
position 22 propagates through unknown position 48 and predicts **P** at
position 74, contradicting confirmed **K**. There is no pair of known positions
separated by exactly 26; checking only a known immediate predecessor misses the
chain 22→48→74. The audit records this witness without inventing the rest of a
plaintext. Ciphertext-feedback lag 73 checks the final crib at position 74;
lag 74 checks none. Both boundary behaviors have dedicated tests.

## Prior-art overlap and the coverage gap

This review uses pinned sources from [the prior-art ledger](../docs/prior-art-barney-scott-review.md).
Sources were read, never executed; reported large search results are not adopted
as independently reproduced coverage. The selected implementations do **not**
fully duplicate the threshold-free full-chain audit, so no substitute model was
needed to justify this small computation.

| Prior implementation | Relevant overlap | Difference retained here |
| --- | --- | --- |
| [Barney autokey_dict.py](https://github.com/barneyjm/kryptos-k4/blob/2db2722cc3f18c52d4d8369d7adc5a1db7e859d7/scripts/autokey_dict.py) | Direct known-predecessor checks in selected alphabet-role slices; effective forward CT lags 1–33 and PT 1–8 | At least 12 CT checks / 8 known PT pairs; no propagation through unknown PT gaps; dictionary inventory not rerun; no all-lag classification |
| [Barney gap_phr_ak.py](https://github.com/barneyjm/kryptos-k4/blob/2db2722cc3f18c52d4d8369d7adc5a1db7e859d7/scripts/gap_phr_ak.py) | Calls the same autokey scanner with phrase-derived alphabets | Inherits its check thresholds and local-predecessor scope; changing the alphabet inventory does not complete the missing chain audit |
| [Barney mask_autokey.py](https://github.com/barneyjm/kryptos-k4/blob/2db2722cc3f18c52d4d8369d7adc5a1db7e859d7/scripts/mask_autokey.py) | Necessary repeated-letter/injectivity tests for an additional arbitrary mask, including the identity special case | CT requires at least 14 forced entries; PT requires at least 8 immediately known predecessor pairs. Its two branches are separately thresholded. A nominal 1–96 loop is not an exhausted all-lag result |
| [Barney backak.py](https://github.com/barneyjm/kryptos-k4/blob/2db2722cc3f18c52d4d8369d7adc5a1db7e859d7/scripts/backak.py) | Related feedback idea | Looks ahead i+L and uses thresholds/tolerances; outside this forward audit, not silently counted as a duplicate |
| [Scott run_p2.py](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/run_p2.py), [retained p2.log](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/results/p2.log) | CT lags 1–40 and PT 1–7, three equations and selected alphabet roles; permits a constant indicator shift | Requires at least 10 directly checkable pairs. It does not eliminate unknown PT intermediates or classify remaining lags. Its zero-hit log is third-party evidence, not our rerun |
| Local MASK-AUTO-001 | Same-alphabet addition with KRYPTOS/ABSCISSA/PALIMPSEST literal primers, both feedback modes | This arbitrary-primer audit subsumes those 12 specific failures in its exact domain; preserve their full outputs, controls and chronology as earlier work |

The source inspection is selected and bounded, not a claim to have proved that
no other source ever performed the same mathematics. No general autokey family
is eliminated by these narrow results.

## Specification, controls and chronology

Initial scope was committed at `44a03c9f53dd1e95107a6a5b1bb7a7dc0c79470a`.
Before any new execution, a toy-control wording error was corrected: a full
`ABC` crib must cycle within `ABC`, rather than include D. The operative
[specification](specifications/AUTOKEY-CONSTRAINT-001.json) was committed at
`7f83582026045f318fa8dcd2224190cc44a5b432`. K4 models/case counts did not change.
Implementation commit: `a13bd721af4bac68a1fb29b3e1ff05d61db47e80`.

An independent reviewer supplied expected K4 lag sets after the initial scope
commit and before execution. Our independently implemented affine solver agrees
with that supplied exhaustive 26-root-per-chain calculation. This agreement is
an attributed comparison, not a claim that we executed the reviewer's code or
were blind to its predictions. Our own independent toy oracle was executed.

All frozen controls pass:

- 1,152 synthetic 97-letter round trips, full regeneration and planted-compatible
  checks, using independent sequential-reference ciphertexts.
- 732 deliberately altered nonvacuous crib fixtures rejected; 420 altered
  zero-check fixtures remain compatible, preventing false rejection of vacuous cases.
- 5,220 exhaustive small-oracle configurations over toy alphabets `ABC` and
  `ABCD`, all ciphertexts of lengths 4 and 3 respectively, lags 1/2, all three
  equations, both feedback modes and three crib masks. Enumerating 40,536 toy
  primer/decryption trials checks exact solution cardinalities against the
  affine solver; at most 16 toy primers per case. **No K4 primer enumeration.**
- Boundary/invalid-input tests, lag-26 gap propagation, lag-73/74 transition,
  empty/single/full crib masks, whole-message toy primers and deadline rejection.

Synthetic RNG: Python `random.Random`, MT19937, seed 20261018. Standard library,
one process. The complete registered run including controls took **0.230 s**
under its 10-second cap. Memory target was 64 MiB; peak memory was not measured.
The full suite passes **97 tests in 8.519 s**, including all prior 90 tests and
unchanged audited artifacts.

```sh
python3 experiments/run_autokey_constraints.py --spec-commit 7f83582026045f318fa8dcd2224190cc44a5b432 --code-commit a13bd721af4bac68a1fb29b3e1ff05d61db47e80
python3 -m unittest discover -s tests -v
```

[Immutable manifest](../results/autokey-constraint-runs/20261018T134147Z-7499a732804146f48f2121f5453be844/manifest.json)
· [all 1,152 records, groups and controls](../results/autokey-constraint-runs/20261018T134147Z-7499a732804146f48f2121f5453be844/AUTOKEY-CONSTRAINT-001.json)
· [validation](../results/AUTOKEY-CONSTRAINT-VALIDATION.json)
· [commit/run chronology](../results/AUTOKEY-CONSTRAINT-CHRONOLOGY.json).
All consulted input/code hashes and the result's SHA-256 were checked after the
run; a fresh replay matched every saved record/group. Existing artifacts were
not overwritten.

## Most justified next experiment — proposed, not run

The retained Gromark streams have a concrete unresolved step: satisfying the
complete two-alphabet bijection constraints, beyond the published crib-graph
filter. A useful next small experiment would choose **one source-pinned logged
survivor**, freeze its base/primer/recurrence and test complete alphabet-assignment
feasibility with synthetic positive/negative controls and a deterministic state/
time cap. A capped incomplete run would remain unresolved. The width-21 ranking
would not be an acceptance condition, and no language-model completion would
be invented. This directly checks a documented gap rather than extending the
vacuous autokey primers. A separate exact specification must precede that run;
no Gromark search, survivor expansion or plaintext claim was made here.
