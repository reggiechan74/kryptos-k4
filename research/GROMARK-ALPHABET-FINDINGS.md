# One published Gromark survivor: full alphabet feasibility

GROMARK-ALPHABET-001. Revision: 2026-10-18. **Feasible, not a K4 solution.**

The one selected published tuple passes the local crib filter and admits two
complete bijective alphabets. Our independent implementation constructs a witness
satisfying all 24 crib equations; decryption followed by encryption regenerates
all 97 ciphertext characters. A separately supplied witness also verifies and
differs outside the cribs, even after the same global-shift gauge is fixed.
These alphabets are arbitrary mathematical completions, not recovered historical
alphabets or meaningful plaintext. No full K4 plaintext is published here.

## Published data and deterministic selection

The pinned [Barney text log](https://github.com/barneyjm/kryptos-k4/blob/2db2722cc3f18c52d4d8369d7adc5a1db7e859d7/results/gromark_sweep.out)
publishes 25 exact tuples from its reported 804,684 survivors. We take the **first
printed indented tuple**, with no fallback or additional search:

```text
(3, 16, 6, (5, 6), (6, 12, 12, 4, 4, 8))
```

This serializes the source's explanation score, base, primer length, lag pair and
primer digits. The [pinned sweep source](https://github.com/barneyjm/kryptos-k4/blob/2db2722cc3f18c52d4d8369d7adc5a1db7e859d7/scripts/gromark_sweep.py)
sorts survivors in reverse lexicographic order before printing. Thus first-printed
is reproducible but neither unbiased nor specially promising. The width-21 score
3 is retained **only as provenance**, never as an acceptance or rejection filter.
The whole reported survivor set was not downloaded or reconstructed; no massive
sweep, primer enumeration or second K4 tuple was run.

[Exact source fixture](../data/gromark-one-survivor.json) records the log and model
file blob identities at commit `2db2722cc3f18c52d4d8369d7adc5a1db7e859d7`. Relevant
files were read through GitHub, not imported or executed.

## Exact model

The [imported model source](https://github.com/barneyjm/kryptos-k4/blob/2db2722cc3f18c52d4d8369d7adc5a1db7e859d7/scripts/gromark2.py)
uses two independently unknown permutations of A–Z over coordinates 0–25 and
the crib equation `c_value(C_i) − p_value(P_i) = d_i (mod 26)`.

```text
d[0:6] = [6,12,12,4,4,8]
d[i] = (d[i-5] + d[i-6]) mod 16, i=6..96
```

The numeric digits are used directly as additive coordinate offsets modulo 26.
Alignment is unchanged: EASTNORTHEAST at one-based 22–34 and BERLINCLOCK at
64–74. No additional offset, phase, reversal, substitution family, reset, null,
transposition, spelling repair or language score is introduced.

## Local filter versus complete alphabet existence

The graph has **27 observed nodes** (13 plaintext letters, 14 ciphertext letters),
**24 edges** and **five connected components**. Each edge fixes the difference
between one plaintext coordinate and one ciphertext coordinate. Cycle closure
and same-side distinctness inside each component pass, independently reproducing
the local filter's claim for this exact tuple.

Those checks alone do not prove a full pair of alphabet permutations exists.
Every component has an unknown common translation. Translations must also avoid
plaintext-coordinate collisions between different components and, separately,
ciphertext-coordinate collisions. A toy control passes the local tests but fails
this global packing condition, so the distinction is tested rather than assumed.

Our solver propagates relative modular potentials, then assigns one translation
per component with global AllDifferent conditions. It fixes component 0 at zero:
adding a common constant to both entire alphabets is a harmless symmetry. It
uses minimum-remaining-domain selection, then larger observed-node count and
lexical root order as ties; translations are tried in increasing order. All
node roots, relative potentials and selected offsets are recorded.

Observed injectivity is sufficient for full alphabet existence because unused
letters on either side can occupy the unused coordinates independently. The
canonical witness fills those letters alphabetically into ascending unused
coordinates. This completion is a convention, not an inferred key.

## Checkable certificates

Nodes use `C:<letter>` and `P:<letter>`; roots are in lexical node order, with C
before P. Each root's relative potential is zero. The component roots are C:F,
C:K, C:M, C:N, C:R.

| Certificate | Component translations in that root order |
| --- | --- |
| Our deterministic solver | 0, 7, 8, 11, 1 |
| Independently supplied, locally verified | 0, 1, 3, 5, 17 |

Our solver visited **5 search states**, tried **4 selected translations** and
performed **260 domain checks**. It stopped at a witness; it did not enumerate
all solutions. The supplied oracle reported 31 trial offsets using its own
ordering; that count was not independently rerun and is not the same metric.

Alphabet strings below list the letter at each coordinate 0–25:

| Certificate | Plaintext alphabet | Ciphertext alphabet |
| --- | --- | --- |
| Our completion | `OTIHDACFGBJMPQRUELVWNSXYZK` | `FRTVGSQKMABNCDELYHPIJZOUWX` |
| Independent completion | `OCIBDFGLJRMSPQUVETWKNXYHZA` | `FKTMGNQABLCZDPEHYRIVJSOUWX` |

Both are full bijections, satisfy all 24 crib equations and regenerate the full
ciphertext. Their fixed C:F coordinate is zero and their other observed values
differ, so these are not merely global translations of the same assignment.
Their decodings also differ at noncrib positions. At least two gauge-fixed
observed assignments therefore exist. Each allows another 13! × 12! choices for
unused plaintext/ciphertext alphabet coordinates. The exact number of feasible
component-translation vectors has not been counted.

Regeneration is an implementation check, not evidence of English: a pair of
bijective alphabets always supports inverse encryption. The cribs were used as
constraints; satisfying them is not a withheld prediction. Neither complete
alphabet existence nor this deliberately selected one-tuple result establishes
Gromark as K4's mechanism or says anything conclusive about other logged survivors.

## Validation, provenance and limits

The [specification](specifications/GROMARK-ALPHABET-001.json) and source fixture
were committed at `cd475ae00eda1eddd8b7fe1694922ecbba593270` before implementation
and computation. Code commit: `f4e56d0ae23d140236417fec5d99ed1055c4df94`.
The independent graph counts and witness were supplied after the specification
and before our execution; they did not initialize the solver. Our computed
witness differs from the supplied one. This is an independent implementation
with a known external prediction, not a blind test or execution of its code.

All frozen controls pass:

- Two hand-calculated digit-stream vectors.
- An independent direct oracle over **231 toy graphs**, checking **9,396 full
  alphabet-permutation pairs**; maximum 576 pairs per graph. It includes both
  satisfiable and unsatisfiable cases (56/175), with cycles, injectivity failures
  and the cross-component obstruction. This toy enumeration is not a K4 search.
- Eight planted 97-letter synthetic cases with random complete 26-letter
  alphabets: four with all plaintext known and four with only the canonical
  24 positions known. Witnesses satisfy their known letters and full regeneration.
  Original-text recovery is required only in the fully known controls.
- Empty graphs, unobserved-letter completion, invalid inputs, a state-cap case
  explicitly classified unresolved, and deadline rejection.

Synthetic RNG: Python MT19937, seed 20261018. The registered run, including its
controls and the one K4 tuple, completed in **0.009 s**, one process, standard
library, under its 10-second / 100,000-state limits. Memory target was 64 MiB;
peak memory was not measured. All **104 tests passed in 8.007 s**, including
the previous 97 tests and unchanged audited artifacts. No repairs or retries
were needed for the registered computation.

```sh
python3 experiments/run_gromark_alphabet.py --spec-commit cd475ae00eda1eddd8b7fe1694922ecbba593270 --code-commit f4e56d0ae23d140236417fec5d99ed1055c4df94
python3 -m unittest discover -s tests -v
```

[Manifest](../results/gromark-alphabet-runs/20261018T135606Z-4fed84af3b8340f79ec5e2491071b3a3/manifest.json)
· [complete stream, graph and witness](../results/gromark-alphabet-runs/20261018T135606Z-4fed84af3b8340f79ec5e2491071b3a3/GROMARK-ALPHABET-001.json)
· [independent cross-check](../results/GROMARK-ALPHABET-INDEPENDENT-CROSSCHECK.json)
· [validation](../results/GROMARK-ALPHABET-VALIDATION.json)
· [commit/run chronology](../results/GROMARK-ALPHABET-CHRONOLOGY.json).
All consulted input/code and output hashes were verified, and a fresh local replay
matched the saved model result. Earlier artifacts were preserved.

## Next bounded step — proposed, not executed

The result already proves non-unique alphabets and non-unique noncrib decoding.
A small identifiability audit would determine the exact admissible plaintext-letter
set at **one-based position 1**, the first noncrib position, under this same
single tuple. At most 26 additional edge-feasibility queries, with a frozen
aggregate state/time cap and toy controls, would distinguish forced information
from arbitrary completion without generating messages or testing more primers.
A capped query must remain unresolved. This requires a separate specification;
no such queries, additional survivors or language searches were run here.
