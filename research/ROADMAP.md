# Research roadmap

Updated 18 October 2026. The approved direction is to learn and reproduce the
designer's available procedures, then assess small, falsifiable combinations.
This is a plan; no K1–K3 controls or language-layer searches have been implemented
or run in this documentation update.

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
