# Fixed asymmetric-feedback and plaintext-step pilots

22 October 2026. **All six fixed asymmetric-feedback models and all twelve
plaintext-driven extra-step models fail the confirmed K4 cribs.** These are two
distinct tested mechanisms beyond the earlier ciphertext-driven extra-step rule.
No candidate, independently validated decoding or solution is claimed. Every
output is labeled a rejected model output, even though invertibility checks pass.

## Scope, chronology and prior-art gap

The parent requested these two final small pilots on the existing local branch
`research/dynamic-key-20261022`. Work stayed in the active Mac mini checkout.
Previous results, including the progressive-key replication, remain unchanged.
No remote operations or third-party executable code were used.

The first continuation specification, `ASYMMETRIC-FEEDBACK-001`, was committed at
`56b2919` as a 72-case arbitrary-primer constraint design. The parent then supplied
a narrower six-case fixed-primer pilot before implementation or any actual score
was computed. The 72-case design remains **DEFERRED / UNRUN**; no results for it
are implied. It was superseded for this execution by a separate unchanged spec.

| Experiment | Specification commit | Implementation commit | Actual run time |
| --- | --- | --- | --- |
| ASYMMETRIC-PRIMER-001 | `2d23dab6bbe773aa7d00de699834ce4df5bc446d` | `74792b65bc2f591f99e94ac06df52b727444e5d7` | 0.067 s |
| PLAINTEXT-STEP-001 | `37bc4bf1635089d51f361f33bfd771b691e836fa` | `ea210bd5c63ce21e9b3c21e65226cc81f99a858e` | 0.102 s |

Each specification is the direct parent of its implementation commit. Both actual
runs occurred afterward and verify all consulted file bytes against their code
commit. Each completed once under its 15-second, one-process budget.

The existing exact autokey audit explicitly assumes a single alphabet. Direct
static reads of the pinned [Barney autokey source](https://github.com/barneyjm/kryptos-k4/blob/2db2722cc3f18c52d4d8369d7adc5a1db7e859d7/scripts/autokey_dict.py)
confirm its eight-known-predecessor gate skips lag 10, which has only four pairs.
The pinned [Scott P2 source](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/run_p2.py)
runs plaintext feedback only through lag 7. These are exact gaps in selected
inspected programs, not a claim of novelty across all cryptanalytic literature.

The pinned [interrupted-key source](https://github.com/barneyjm/kryptos-k4/blob/2db2722cc3f18c52d4d8369d7adc5a1db7e859d7/scripts/fe_interrupt.py)
uses single-letter plaintext advance/pause rules. Its cursor increments are 0/1,
rather than the present vowel/consonant-class increments of 1/2. This distinction
was confirmed by reading the generator; third-party searches were not run.

The parent additionally identified Scott `run_e5.py` as prior art for the exact
progressive form. That source finding is attributed to the independent researcher;
our earlier progressive result remains replication, not a new mechanism.

## ASYMMETRIC-PRIMER-001: six fixed role triples

Plaintext order Ap, ciphertext order Ac and feedback/primer order Ak independently
use AZ or KRYPTOS. Exclude the two all-equal triples. The literal primer is
PALIMPSEST, lag 10, addition only. For positions after the primer, the key is the
plaintext character ten positions earlier, reindexed through Ak. Decryption is
sequential. Each role triple has **zero fitted parameters**, no indicator shift
and no alphabet or primer search. K1 use of PALIMPSEST motivates the fixed word;
it is not evidence that K4 uses this mechanism.

| Ap | Ac | Ak | East / 13 | Berlin / 11 | Total / 24 |
| --- | --- | --- | ---: | ---: | ---: |
| AZ | AZ | KR | 0 | 1 | 1 |
| AZ | KR | AZ | 0 | 1 | 1 |
| AZ | KR | KR | 0 | 0 | 0 |
| KR | AZ | AZ | 0 | 1 | 1 |
| KR | AZ | KR | 0 | 1 | 1 |
| KR | KR | AZ | 3 | 2 | 5 |

The largest partial score is 5/24 at one-based positions **23,26,33,64,73**.
That model fails 19 confirmed letters and is rejected by the predeclared hard
criterion. All six outputs re-encrypt exactly because the transforms are
invertible; this supplies no evidence that they describe the actual cipher.

For 199 fresh histogram-preserving shuffles (seed 20261024), all six models were
evaluated each time, 1,200 total model evaluations. Two null family maxima are
at least five; the plus-one conditional tail is **3/200 = 0.015**. Null maxima:
0: 4, 1: 45, 2: 98, 3: 42, 4: 8, 5: 2.

This modest-resolution exploratory tail is conditional on the frozen ciphertext
histogram and six-model family. It does not account for the wider history of
experiment selection, establish historical intent or override the 19 hard
contradictions. Only two exceedances make its Monte Carlo estimate imprecise.
No additional primer, sign, role order or phase was selected to improve it.

## PLAINTEXT-STEP-001: twelve fixed cursor models

Three words (KRYPTOS, PALIMPSEST, ABSCISSA), two alphabets (AZ/KRYPTOS) and two
trigger classes (AEIOU or its 21-letter complement) give twelve models. Cursor
starts at zero. Encrypt by addition with the word character at cursor modulo
word length; afterward advance by one plus an extra step if the **plaintext**
character is in the trigger class. Decrypt first, then update using recovered
plaintext. There is no key fitting, alternate phase or reset.

| Word | Alphabet | Trigger | East / 13 | Berlin / 11 | Total / 24 |
| --- | --- | --- | ---: | ---: | ---: |
| KRYPTOS | AZ | vowel | 0 | 0 | 0 |
| KRYPTOS | AZ | consonant | 0 | 1 | 1 |
| KRYPTOS | KRYPTOS | vowel | 1 | 0 | 1 |
| KRYPTOS | KRYPTOS | consonant | 2 | 1 | 3 |
| PALIMPSEST | AZ | vowel | 0 | 0 | 0 |
| PALIMPSEST | AZ | consonant | 1 | 0 | 1 |
| PALIMPSEST | KRYPTOS | vowel | 0 | 0 | 0 |
| PALIMPSEST | KRYPTOS | consonant | 0 | 1 | 1 |
| ABSCISSA | AZ | vowel | 1 | 1 | 2 |
| ABSCISSA | AZ | consonant | 1 | 0 | 1 |
| ABSCISSA | KRYPTOS | vowel | 0 | 0 | 0 |
| ABSCISSA | KRYPTOS | consonant | 0 | 1 | 1 |

All twelve fail; the best score is 3/24. The full twelve-model maximum was
equaled/exceeded by 107 of 199 histogram-preserving shuffles (seed 20261025),
giving the plus-one conditional tail **108/200 = 0.54**. All 2,400 model
evaluations completed. No score-driven variant was added.

Neither experiment used a crib to fit a key. East/Berlin scores therefore report
separate diagnostic blocks, rather than independently collected validation
evidence. Full acceptance always required all 24 positions and all 97-character
regeneration. The correlated-model null maximum accounts for the tested family
only; it does not combine either result with earlier families. Scores from
arbitrary-key fitting in DYNAMIC-KEY-001 cannot be compared directly with these
fixed-model match counts.

## Controls and validation

- Asymmetric pilot: 4,056 exhaustive single-symbol/key roundtrips, six planted
  97-letter recoveries containing all 24 crib letters, six altered-crib rejections,
  and 48 comparisons with an independently indexed circular-buffer decoder.
- Plaintext step: 2,600 symbol/key-phase roundtrips, twelve planted full recoveries
  and altered-crib rejections, plus 96 independent numeric-oracle comparisons.
  A hand-indexed AA→PL example distinguishes plaintext from ciphertext triggering.
- Existing verified baseline and K1–K3 controls passed before both runs.
- The saved-output audit independently re-encodes every one of the 1,746 output
  letters (18 x 97), recomputes crib acceptance, checks every consulted hash
  against the recorded implementation commit, verifies chronology and all null
  maximum/tail accounting. No repeated experimental search is needed.

Final suite results are recorded in [validation receipt](../results/FIXED-PILOTS-VALIDATION.json).

## Ranked interpretation and next experiment

1. **Asymmetric-alphabet feedback:** a concrete gap beyond the same-alphabet
   proof, now tested with a historically demonstrated fixed primer. All six
   frozen models are rejected. It retains the strongest contextual motivation
   among these speculative mechanisms; the five-letter coincidence supplies no
   basis for tuning a key or selecting a new alphabet.
2. **Plaintext-driven extra stepping:** genuinely changes the source of cursor
   state, with exact sequential inverses. All twelve fixed cases are rejected.
   No independent K4 evidence currently favors a vowel-class cursor.
3. **Ciphertext-driven extra stepping:** all 96 declared cases previously
   rejected, including arbitrary periodic base keys. Its outcome is preserved in
   [DYNAMIC-KEY findings](DYNAMIC-KEY-FINDINGS.md). It is not equivalent to the
   plaintext-triggered mechanism above.

The affine-digraph idea remains unrun. The next proposed computational experiment
is the already registered 72-case asymmetric-feedback **arbitrary-primer
constraint** audit, if further work is requested: it asks whether any primer can
satisfy the cribs for lags 9–12, rather than trying more words after a partial
score. Its rationale must remain the independently identified audit gap, not
0.015. It must report exact remaining degrees of freedom and modal-root null
calibration, and remain separate from the six-case negative. This batch stops
here without executing that design or expanding any tested parameter range.

## Reproduce

```sh
python3 experiments/asymmetric_primer.py --spec-commit 2d23dab6bbe773aa7d00de699834ce4df5bc446d
python3 experiments/plaintext_step.py --spec-commit 37bc4bf1635089d51f361f33bfd771b691e836fa
python3 -m unittest discover -s tests -v
```

Both runners verify their consulted bytes against HEAD and write new atomic
snapshots. Existing run directories are retained; manifests govern completeness.
Results include complete rejected outputs, so they should never be quoted as
decoded plaintext.

[Asymmetric result](../results/asymmetric-primer-runs/20261022T120817Z-ef4199fc397e4bd9bc6ca2fb3bfdc2e2/ASYMMETRIC-PRIMER-001.json),
[plaintext-step result](../results/plaintext-step-runs/20261022T121001Z-38f7134c1bc3445ea7bf00efc70d2e11/PLAINTEXT-STEP-001.json).
