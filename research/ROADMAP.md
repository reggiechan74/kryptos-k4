# Research roadmap

Updated 18 October 2026. The approved direction is to learn and reproduce the
designer's available procedures, then assess small, falsifiable combinations.
The original documentation-only plan is retained below. **CTRL-001 update:**
full K1, both K2 variants, and K3 now pass known-answer and inverse controls;
see [experiment log](EXPERIMENTS.md) and [source verification](../sources/VERIFICATION.md).
K3 image transcription and physical paper reconstruction remain outstanding.

## Inputs and evidence

Read [Designer context](../docs/designer-context.md) for the evidence ledger,
historical limits, and workshop, and [Language and alphabet layers](../docs/language-and-alphabet-layers.md)
for encoding distinctions and proposed feasibility checks. These are supplied
research documents. Their citations and reported past checks are attributed to
that research, not independently verified by this repository update. Retain the
distinction between public facts, participant recollections, transcription,
inference, and unverified third-party experiments.

## Next steps and acceptance gates

1. **Freeze inputs and provenance.** Establish canonical K1–K3 ciphertext and
   plaintext fixtures alongside the existing K4 baseline. Keep physical layout,
   normalized letters, punctuation, misspellings, and corrections separate;
   record sources, hashes, and position-level disagreements. Preserve unresolved
   dates and source conflicts rather than choosing values to fit a hypothesis.
2. **Validate K1 and K2 controls.** Reconstruct the actual KRYPTOS tableau and
   arithmetic conventions from primary evidence. Use PALIMPSEST for K1 and
   ABSCISSA for K2 as proposed in the workshop; compare the opening known-answer
   case before complete fixtures. Require exact decrypt/re-encrypt equality for
   every accepted character, with explicit punctuation/key advancement and
   separate as-inscribed/corrected K2 variants. Resolve any convention mismatch
   before reusing code on K4.
3. **Validate K3 controls.** Reconstruct the proposed 8 rows × 42 columns,
   clockwise rotation, reshape to 24 rows × 14 columns, clockwise rotation
   workflow. Compare all 336 canonical characters, preserve the documented
   anomalous spelling and terminal Q, and define the separator treatment.
   Require full permutation/inverse equality and a paper reconstruction;
   matching endpoints alone does not pass.
4. **Inventory published work.** Add source-attributed claims and local
   reproduction status to the [published inventory](../sources/EXPERIMENTS.md).
   Record assumptions, exact tested bounds, and missing code or data. The
   supplied documents' findings are reading leads, not blanket eliminations.
5. **Specify language-layer feasibility checks.** Before implementation, freeze
   one sourced classical/Cyrillic romanization convention and, separately, one
   historical 1962/1963 Shavian convention with an explicit reversible A–Z
   representation. For each model record symbol inventory/order, pronunciation
   or translation ambiguities, forward/inverse maps, framing, permitted keys,
   resource budget, and rejection rule. Plan symbol and unrelated-text round
   trips, length/parity checks, crib-collision checks, and an audit for mere
   alphabet relabeling. Keep final English crib positions distinct from any
   length-changing intermediate representation. Reject only the exact model
   contradicted; this does not reject all uses of a language or script.
6. **Register bounded hypotheses before searching.** After the controls and
   feasibility gates pass, choose at most one new operation beyond validated
   primitives per experiment. Record source motivation, finite parameters,
   fixed seeds where relevant, trial counts, controls, and exact negative-result
   scope. Require all confirmed cribs, coherent remaining text, and complete
   ciphertext regeneration by independently specified rules. Round-trip alone
   is insufficient if parameters or keystream are freely fitted.

Use the [hypothesis template](templates/hypothesis.md),
[experiment template](templates/experiment.md), and [research policy](POLICY.md).
Planning these steps does not authorize broad compute, paid services, external
submissions, or contacting third parties.

## Completed bounded milestone and remaining evidence gates

See [current findings](BOUNDED-FINDINGS.md), [exact specification](BOUNDED-SPEC.md),
and [Firecrawl worker receipt](../docs/source-verification-2026-10-18.md).
Controls and structural feasibility checks are implemented. Finite route/period,
literal running-key, and fixed-cube Trifid checks are complete; lag diagnostics
include split-sample maximum-statistic calibration. None yields a K4 solution.

The next extension requires an independent model specification: a sourced
historical reversible language encoding, a new justified physical/key rule,
or a selected tightly bounded generator. The absence of such a specification
is a research constraint, not a reason to expand arbitrary search freedom.
K3 photographic transcription and a structured claim/date/conflict ledger remain
useful evidence tasks. No broad search, external verifier, or paid submission
is authorized by the existence of these results.

## Focused audit update

[Audit hardening](AUDIT-HARDENING.md) establishes that all 282 route survivors
are vacuous fits with zero repeated-phase comparisons, not evidence for those
periods. The [worksheet provenance review](../docs/k3-worksheet-verification.md)
distinguishes complete algorithmic verification from partly reconstructed
history. Neither result motivates a larger search. Future new specifications
must be committed before execution and the run must reference that SHA.

## User-selected next branch order

Investigate the language/alternative-alphabet idea first, prioritizing historical
Shavian and Cyrillic conventions; then investigate source-supported masking.
The [planning manifest](specifications/LANGUAGE-PREPARATION.json) and
[validation interfaces](../docs/language-experiment-interfaces.md) establish
loss/ambiguity, round-trip, length, and crib gates. They contain no historical
map and run no K4 candidate search. Each final operational specification will
be committed before its run and referenced by commit and exact file hash.

## Completed requested sequence

[Language feasibility](LANGUAGE-FINDINGS.md) completed first, then the
[two masking pilots](MASKING-FINDINGS.md), followed by the separately authorized
[word-interior extension](WORD-SCRAMBLING-FINDINGS.md). Each fixed specification
was pushed before implementation/execution. No general language or masking
family was eliminated. Further work needs a new independently motivated finite
specification; none of these failures authorizes more variants automatically.

A subsequent [narrow respelling feasibility check](PHONETIC-FEASIBILITY.md) is
complete without search expansion. The user's length-changing phonetic rules
and German translation idea remain distinct hypotheses requiring an exact
rendering/inverse/alignment specification; no flexible mapper was introduced.

## After the exact direct-autokey audit

AUTOKEY-CONSTRAINT-001 leaves only zero-consistency-check compatible cases in
its declared domain. Do not expand arbitrary long primers or invent plaintext.
The next justified small proposal is a complete alphabet-feasibility check for
one source-pinned logged Gromark survivor, with all-different constraints, planted
controls and hard state/time limits. Freeze a separate specification before
execution; width21 and language scores are not necessary acceptance conditions.
No such Gromark run has been launched by this audit.
