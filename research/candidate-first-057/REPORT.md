# Study 057: alphabet-role and Beaufort extensions of free column order

## Result

**UNSAT_COMPLETE within the frozen domain.** The production solver and an independent exhaustive reference both returned zero compatible descriptions, canonical operators or plaintexts for K4. This is an exact bounded exclusion, not a solution and not an exclusion of all layered ciphers.

The independent target run completed **22,901,760 route/period/convention trials**. That includes the study 056 baseline, not 22.9 million wholly new hypotheses. Seven additional convention loops contain 20,039,040 route/period/convention trials; shorter-period aliases and the zero-key identity overlap must not be counted as new operators.

## Exact family

At plaintext position i, use D_i = B[(s index_A(P_i) + K_(i mod p)) mod 26], then fill rows left to right and emit physical columns in any permutation, top to bottom, without padding. A and B independently use ordinary A–Z or KRYPTOSABCDEFGHIJLMNQUVWXZ. Sign s is +1 (Vigenère-type) or −1 (Beaufort-type). Widths 6–9; nominal periods 2–8; arbitrary numeric seeds; fixed zero alignment; 97 letters and the 24 established crib positions.

All 8 alphabet-role/sign conventions were included, with AZ/AZ/+ as a regression of056. Their 208 one-letter descriptions contain 207 distinct mappings. The sole cross-convention overlap is the identity at zero key for AZ/AZ/+ and KR/KR/+. Canonicalization uses the full 97-position route and all 26 letter outputs at every position, not names or key spellings. Variant Beaufort is already covered by arbitrary key negation, and arbitrary key phase by seed rotation.

No reverse stage order, autokey, padding, errors, additional widths/periods, other alphabets or additional layers were introduced. Earlier restricted route/grammar studies do not equal this free-column-order domain. The previous 056 baseline is retained, not relabeled as new.

## Validation before target use

The protocol and code were frozen before fresh synthetic fixtures. Final freeze SHA256: d49542e537fa6ae1c731e16ec73fff12c9d390d9d9ac0bcc98542c3aad3cc39f. An initial pre-heldout manifest is preserved; the final manifest adds the final independent preflight audit without changing code or gates.

- Tiny exact checks: 512 cases, 4,096 production adapter calls, 21,236 independently re-encrypted witnesses; complete sets match the brute-force oracle. Another 96 full-alphabet round trips cover signs, alphabet roles, widths and aliases.
- Heldout 520 inputs: 224 uniform positives, 224 literal-clue positives, 16 alias cases, 56 independently uniform ciphertext controls. Inputs hide generating keys, convention, route and period. Both engines search the whole union.
- All 520 runs completed and their raw, canonical-operator and plaintext sets agreed.
- All 464 planted operators were included.
- Unique plaintext: 221/224 uniform positives (98.66%; Wilson 95% 96.14–99.54%), 224/224 literal-clue positives (100%; Wilson 95% 98.31–100%). Three ambiguous uniform cases remain valid multiple-solution outcomes, not discarded failures.
- No compatible solutions in 56 independent random-ciphertext controls. The Wilson 95%  upper bound is 6.42%; zero observed fits is not a guarantee of zero false positives and is not project-wide calibration.
- Independent review replayed fixture generation, verified frozen and pre-answer output hashes, checked 875 physical-letter re-encryptions, and confirmed 11,908,915,200 total reference trials in the benchmark.

The plaintexts outside the literal clue positions are synthetic uniform letters. These tests establish exact model recovery and constraint behavior, not recovery of natural English or likelihood that Sanborn used this family. The language-score screen from 055 was not reopened.

## Execution and scope limits

The numeric shared-placement solver from 056 is unchanged; 057 applies a mathematically exact alphabet-role adapter. The independent reference uses direct physical-letter equations and literal ragged row matrices. No learned-conflict or new speedup claim is made. All source code, inputs, answers, seeds, raw results and audits are in the archive.

Benchmark inclusive CPU: production 23.841839287 seconds, reference 527.587440487 seconds. Target inclusive CPU: production 0.071858759 seconds, reference 1.026414776 seconds. These are measured separate implementations, not a matched algorithm competition. Resource accounting also retains a conservative 600-second preparation reserve and rounded analysis/audit charges. Each worker and child has a 1 GiB address-space cap, with one child at a time; observed benchmark worker-plus-child maximum was 22,577,152 bytes. Failed/incomplete runs would have been retained and charged, but none occurred in this study. Overall cap 8 CPU hours / 8 GiB was not approached.

Both blind output files were sealed at 2026-10-31T11:53:30.141875UTC before answer analysis. Parent reviewed the independent benchmark audit before approving the target stage at 11:55UTC. Additive target freeze SHA256: c23afa9037bcbc1b12d0cc5f189e203db0b6007fd50d69514af53b40a29dc07d. Canonical ciphertext SHA256: eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab. Neither target engine was rerun to tune settings.

## Next action

Close Q-01 only for these exact bounds. Reconcile the canonical hypothesis ledger and experiment log before selecting Q-02: reverse the stage order with separately frozen assumptions and explicit handling of unconstrained key residues. Q-03 feedback composites and conditional method pilots remain separate. The result does not authorize arbitrary expansion or make a compatible future witness a unique solution.
