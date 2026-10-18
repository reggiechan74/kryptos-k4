# Fixed-tuple identifiability: 73 difference-existence queries

GROMARK-IDENTIFIABILITY-001. Revision: 2026-10-18.
**These are model-conditional deductions, not confirmed K4 plaintext.**

All 73 noncrib positions were classified: **10 forced, 63 variable, 0 unresolved**.
Every variable position has a complete checked alphabet-pair counterexample.
Every forced position has an exact equality-component proof. The tuple, original
24 cribs, reference artifact and full-alphabet model were unchanged. No primer,
language score, annealing process or new historical assumption was introduced.

## The question and its limits

We freeze the [same published tuple and model](GROMARK-ALPHABET-FINDINGS.md):
base 16, primer `(6,12,12,4,4,8)`, lags `(5,6)`, and two independent permutations
of A–Z at coordinates 0–25, with `c(C_i) − p(P_i) = d_i mod 26`.
The [verified reference artifact](../results/gromark-alphabet-runs/20261018T135606Z-4fed84af3b8340f79ec5e2491071b3a3/GROMARK-ALPHABET-001.json)
supplies the fixed arbitrary alphabet pair. Its SHA-256 and Git blob identity are
frozen in the [specification](specifications/GROMARK-IDENTIFIABILITY-001.json).

For each noncrib position i, let r be its letter under that reference. The **single
query** is whether a complete alphabet pair can satisfy every original constraint
and also `c(C_i) − p(r) != d_i mod 26`. This is exactly the existence of a
different decoding at that position. It is not 26 letter-domain queries per
position. Known positions are excluded from the 73-query map.

Variable means that at least one checked alternative exists. It neither lists
all admissible letters nor makes different positions independent. Counterexamples
for different positions need not be combinable. A toy example has two individually
variable positions yet forbids their simultaneous AA decoding because the map is
a bijection. Thus even a completely variable marginal map would not demonstrate
absence of joint constraints. Here the additional ten forced positions also remain
part of the fixed model's joint restrictions.

## Conditional forced letters

| One-based position | Forced letter under this tuple/model |
| --- | --- |
| 12 | A |
| 38 | E |
| 42 | O |
| 44 | S |
| 47 | L |
| 61 | B |
| 62 | E |
| 79 | L |
| 81 | I |
| 86 | I |

These letters were not added to `data/k4.json` as confirmed cribs. The tuple was
already selected using the existing cribs; these consequences are not new,
independent observations of the real plaintext. An independently verified
conflicting plaintext letter would reject this tuple/model, not all Gromark.

All ten proofs use the same-component invariant. Plaintext and ciphertext nodes
joined by the known equality graph have a fixed modular coordinate difference
under every legal component translation. For the reference letter r and target
cipher symbol, that difference equals the target digit, so a different decoding
is impossible. Each certificate records the component root, the two nodes,
relative potentials, modulus/key comparison and proof-completion flag. Positions
38 and 86 require transitive graph paths; they are not just repeated known
ciphertext/digit pairs.

## Counterexamples for all 63 variable positions

Our frozen reference yields the following certificate breakdown:

| Method | Positions | Acceptance |
| --- | --- | --- |
| Swap two unused plaintext labels | 39 | Both labels absent from the original plaintext-side graph; full witness checked |
| Swap two unused ciphertext labels | 21 | Both labels absent from the original ciphertext-side graph; full witness checked |
| Supplied complete alphabet certificate | 3: positions 3, 53, 78 | Full bijections, all original equations, target difference, all 24 cribs and full regeneration checked |

Swapping an unused plaintext label with another unused label changes the target
letter without changing any crib equation. Swapping an unobserved ciphertext
symbol with another unused ciphertext symbol changes its coordinate and therefore
its decoding. The record retains a complete pair of alphabet strings for **every**
variable position, not merely a claim that such a swap should work.

The independent review used a different reference/witness arrangement and reported
41 plaintext swaps, 15 ciphertext swaps and seven other cases. The proof-method
partition depends on the arbitrary reference and which certificate is tried
first. Our 39/21/3 partition is therefore not a classification disagreement:
the invariant result is the same ten forced positions and 63 variable positions.
All three supplied witnesses were checked before use; in the actual query flow
the previously verified independent witness sufficed for the three pooled cases.

No exact-search fallback was needed for K4. The generic fallback remains part of
the tested final implementation: it adds the one modular disequality, includes
otherwise unobserved endpoint variables as isolated components, enforces global
per-side AllDifferent, and uses bounded component-offset search. A forced result
from it requires exact exhaustion; a cap is always unresolved. Canonical filling
of unobserved symbols is never mistaken for a proof of uniqueness.

No full reference or alternative decoded message is emitted. Full 97-character
inverse/regeneration checks validate implementation; they do not establish English
or recover a historical alphabet. Only ten scalar conditional predictions and
the per-position feasibility certificates are reported.

## Protocol, controls and validation

Initial specification: `25fa0615a08a4f629393c9b00c9cb78e92a85f38`.
After that commit, the independent review supplied the expected map and complete
certificates. We transparently committed a pre-execution protocol update at
`bfab3d735e5e73824aeb5a2bfe5a9e471933c666`: use validated supplied certificates
after the analytic symmetry/invariant checks and before bounded search. The
tuple, reference, 73 questions, acceptance conditions and resource caps did not
change. These known predictions were verified locally, not presented as a blind
discovery. The [certificate-pool fixture](../data/gromark-identifiability-counterexamples.json)
records its provenance. Implementation commit:
`5d93af5bd4a434c20b9c8a48a7f68963643ca523`.

The final implementation passed:

- Independent enumeration over 231 toy base graphs and 9,396 full permutation
  pairs, including 56 satisfiable and 175 unsatisfiable bases.
- **515 difference queries**, compared against **27,052 full permutation-pair
  evaluations**. They include 425 forced and 90 variable query outcomes. The
  supplied certificate pool was disabled for these controls, exercising the
  symmetry rules, component proofs and actual disequality search directly.
- A globally forced case with one unused label on each side, which requires
  AllDifferent reasoning and explicit missing endpoints; positive variable
  controls; invalid references/targets; state/time caps that remain unresolved;
  a 73-record aggregate-cap check; and the joint-constraint counterexample.
- Complete independent checking of every K4 counterexample, the exact forced
  map, source/reference pins, and the two transitive forced positions.

No randomness is used. Caps were fixed before execution: one process, **0.25 s
and 10,000 search states per query**, five seconds for controls, twenty seconds
for the audit, and 25 seconds for the registered job including publication.
The run completed in **0.018 s**; the maximum recorded K4 query time was
**0.000119 s**. All 73 logical queries were answered with certificates or
invariants; zero K4 search fallbacks, no caps reached. Memory target was 64 MiB;
peak memory was not measured.

All **112 tests passed in 8.302 s**, including the previous 104 tests and unchanged
historical artifacts. A fresh local replay matched all proof-bearing records
(timing fields excluded), and all consulted input/code and output hashes verified.

```sh
python3 experiments/run_gromark_identifiability.py --spec-commit bfab3d735e5e73824aeb5a2bfe5a9e471933c666 --code-commit 5d93af5bd4a434c20b9c8a48a7f68963643ca523
python3 -m unittest discover -s tests -v
```

[Complete 73-position map and certificates](../results/gromark-identifiability-runs/20261018T150335Z-5b16b46678154416add3015ab8676aa9/GROMARK-IDENTIFIABILITY-001.json)
· [manifest](../results/gromark-identifiability-runs/20261018T150335Z-5b16b46678154416add3015ab8676aa9/manifest.json)
· [validation](../results/GROMARK-IDENTIFIABILITY-VALIDATION.json)
· [chronology](../results/GROMARK-IDENTIFIABILITY-CHRONOLOGY.json).

## Independent constraint needed next

This audit stops here. More arbitrary completion, English scoring or primer
variation would not turn conditional consequences into evidence. A documented,
independently sourced alphabet/key-construction rule, or a newly confirmed public
plaintext constraint not used in choosing this tuple, is needed to discriminate
the model from alternatives. Any proposed rule must be fixed before checking it;
one additional fact may still leave substantial freedom. The ten conditional
letters are possible falsification targets, not confirmed new clues. See the
[source-linked strategy note](../docs/research-strategy.md).
