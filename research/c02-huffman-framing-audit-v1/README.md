# C02: fixed Huffman framing — source/proof audit only

**No C02 experiment has run; the model is not excluded and is not target-admitted.** The [source/proof audit](REPORT.md) specifies the fixed tree, sentinel framing, width-97 positional transport and seven fixed outer phases. It identifies missing synthetic utility and independent-adapter gates, not a K4 result.

## M21 applicability correction

A fixed 97-digit base-26 inverse candidate already satisfies `0 <= N < 26^97`. Rechecking that capacity bound with M21 adds no target discriminator. **Do not run a standalone M21 capacity-count experiment for C02.** The forward boundary stratum does have a genuine content-dependent capacity restriction; therefore this is neither proof that M21 is universally useless nor exclusion of C02 itself. Whole-family capacity is nonempty for each fixed phase.

The [static certificate](STATIC-CERTIFICATE.json) and [codebook](CODEBOOK.json) retain exact table/constants and the analytic boundary witness. No 97-symbol message encoder or synthetic message batch was run; the fixed table and integer constants were derived statically. A syntax error before execution was corrected and disclosed in the report. The derivation source is retained for inspection, not replayed by publication checks.

## Evidence and gates

- [Source policy](SOURCE-POLICY.json) and [current audit status](STATUS.json).
- [Original source commitments](ORIGINAL-SHA256SUMS.json), [transparent publication mapping](PUBLICATION-PROVENANCE.json) and current `SHA256SUMS.json`. Only the report's private administrative reference was sanitized; computational artifacts remain exact.
- Primary-source links and Git blob pins in the report distinguish Colossus's implemented related ternary/trigraph codec from a verified K4 run. No third-party source bodies are bundled.

Before a synthetic gate, freeze the independent decoder, unseen English generation policy, useful-capacity threshold, finite controls and resources. No budget or execution authority is supplied here. The original 100 drafts remain historical, including the imprecise local bit/digit-boundary wording; a prospective protocol must replace it explicitly with whole-integer threshold and leading-zero tests. Three proposals remain K4-target-tested and 97 target-unrun; no canonical cipher family is added.
