# Research strategy: separate proof, coverage and identification

Revision: 2026-10-18. This note synthesizes existing repository evidence; it adds
no search, source claim or broad cipher-family exclusion.

| Evidence class | What the repository demonstrates | What follows |
| --- | --- | --- |
| Structural proof | [STRUCT-001](../research/STRUCTURAL-FINDINGS.md) uses exact letter-count and equal-phase bijection invariants. [Direct Enigma](direct-enigma-boundary.md) and [identical resets](../research/CLOCK-RESET-PROOF.md) have explicit contradictory witnesses. | Reject every instance satisfying the stated assumptions. Do not extend the proof to transformations that break those assumptions. |
| Bounded negative | [Fixed masking pilots](../research/MASKING-FINDINGS.md) and [word-interior checks](../research/WORD-SCRAMBLING-FINDINGS.md) exhaust their frozen finite cases with controls and exact acceptance. | Reject those cases. A negative keyword list or short parameter range does not exclude its whole family. |
| Heuristic failure | The [pinned prior-art review](prior-art-barney-scott-review.md) distinguishes source bounds, retained artifacts, hard conditions and diagnostic scores. | Failed annealing, weak language scores, empty logs or failure to explain width-21 repeats do not establish impossibility. Recovery power and search completion must be separately evidenced; unreplicated author claims stay attributed. |
| Underdetermination | The [exact autokey audit](../research/AUTOKEY-CONSTRAINT-FINDINGS.md) has 420 compatible cases with zero consistency checks. [One Gromark tuple](../research/GROMARK-ALPHABET-FINDINGS.md) has distinct verified complete alphabet witnesses. | Compatibility can be algebraically cheap. Count free parameters and checks, rather than treating a crib fit or automatic inverse as identification. |

An implementation control checks whether the code can recover or reject declared
synthetic cases; it does not validate the historical choice of cipher or key.
An independent reimplementation can corroborate the calculation while using the
same evidence. It does not create independent plaintext observations.

The [73-position identifiability audit](../research/GROMARK-IDENTIFIABILITY-FINDINGS.md)
sharpens this distinction. Under the one fixed tuple, ten letters outside the
cribs are forced and 63 can vary. The former are **conditional predictions**;
the latter each have a valid alternative, not a license to choose all letters
independently. The all-different and recurrence constraints can couple positions.
A small exact toy control explicitly shows that every position can vary while
some joint combinations remain impossible. No model-conditional letter is added
to the confirmed baseline without independent evidence.

The next useful input is an independently supported restriction: for example a
documented alphabet construction or a new confirmed plaintext constraint not used
to select the tuple. The [historical clock review](historical-clock-inscriptions.md)
also explains why undated city names, an uncalibrated ENE face, a gift model or
uninspected archival leads cannot supply a unique key by themselves. Evidence
may motivate a precise rule; it cannot stand in for one.

Before another experiment, state the exact model, source pin, permitted degrees
of freedom, complete acceptance checks, controls and resource limits. Keep
timeouts unresolved, preserve negative-result scope, and retain original artifacts
with explicit corrections. Reject a model on an independent contradiction; do
not repair it after seeing the answer with arbitrary shifts, keys or spellings.
Neither a fluent string nor successful re-encryption is a recovered message when
the alphabet choices were free to fit the same known constraints.
