# Candidate-first K4 pilot 051 — preregistration for audit

**Status: proposal awaiting independent audit. No K4 ciphertext has been obtained or scored by this experiment.**

## Question and scope

Given 32 independently authored, frozen 97-letter plaintext messages (16 thematic and 16 neutral), do any induce a demonstrably simple key under a small, fixed family of classical tableau transformations? Authors receive the 97-letter length and the two required crib placements, but never ciphertext, induced keys, scores, or control results. We test every message; no message is rejected because a source passage, Brown corpus, or thematic assumption failed elsewhere.

This pilot detects **repetition/short periods, plaintext autokey, ciphertext autokey, and those same patterns with explicitly charged non-crib residual exceptions**. It does **not** test whether an arbitrary 97-letter induced key is meaningful natural language, contains a convincing phrase, or is a historically intended running key. Natural-language-key detection is a deferred limitation, not a negative finding. An unrestricted 97-letter key always exists for an invertible tableau and is vacuous evidence.

## Frozen input bank and blinding

- Exactly 32 unique messages, labeled before scoring: 16 thematic, 16 neutral.
- The messages were drafted in two blinded author batches; thematic/linguistic overlap is allowed and no claim of statistical independence is made.
- Each is exactly `[A-Z]{97}`, with `EASTNORTHEAST` at 1-based positions 22–34 and `BERLINCLOCK` at 64–74.
- Retain the authors' original wording, construction notes, and IDs separately. Only A–Z normalization and objective length/crib correction are permitted before freezing. No ciphertext-informed repair, deletion, or replacement.
- Hash the protocol, complete code/tests, configuration, raw candidate records, normalized bank, and frozen control definitions before accepting K4. Write a manifest with an ISO UTC timestamp. The supplied canonical target is separately hashed on arrival. Amendments require an explicit new version and are never presented as preregistered.

## Fixed tableau family

Alphabet AZ is `ABCDEFGHIJKLMNOPQRSTUVWXYZ`. Alphabet KR is the first occurrence of each letter in `KRYPTOSABCDEFGHIJKLMNOPQRSTUVWXYZ`.

For each of the four ordered pairs `(plaintext_index_alphabet, ciphertext_index_alphabet)` in `{AZ,KR}², evaluate three arithmetic rules modulo 26:

1. Vigenère: `c = p + q`; induced `q = c - p`.
2. Beaufort: `c = q - p`; induced `q = c + p`.
3. Variant Beaufort: `c = p - q`; induced `q = p - c`.

This is 12 fixed indexed-tableau variants, not a claim that all 12 were actually used historically. The unmixed AZ and KR versions and keyed-output/mixed-axis versions cover conventional additive/subtractive tableau choices without an unrestricted permutation search. Key symbols are always displayed in AZ order; switching their display alphabet cannot manufacture additional evidence. No arbitrary substitutions, transpositions, reversals, segmentation, or key/ciphertext-selected alphabet changes.

For every tableau, evaluate these three structural descriptions and each integer period/seed length `r=1..32`:

- **Periodic:** a length-r seed repeats from position 1.
- **Plaintext autokey:** first r key residues are a free seed; thereafter key residue `q[i] = p[i-r]` in that tableau's plaintext index alphabet.
- **Ciphertext autokey:** first r key residues are a free seed; thereafter `q[i] = c[i-r]` in that tableau's ciphertext index alphabet.

Autokey is an explicit classical mechanism, not a permission to invent arbitrary recurrences. Seeds and every non-crib exception are charged. All 1,152 registered descriptions are considered per candidate; statistically equivalent cases remain in the search and the multiplicity penalty, conservatively. No unrestricted-key category is eligible as evidence.

The upper bound 32 was fixed before any scoring to include previously known potentially compatible lengths 27–29, not selected from results of this bank.

## Primary score, chosen before any target/control scores

Let U be the **73 positions outside both known crib blocks**. Crib positions are never evidence letters in the primary score. The baseline literal cost is `73*log2(26)` bits.

Every description pays `log2(32) + log2(12*3*32)` bits for selecting the candidate and description, and `r*log2(26)` bits for its free seed. This charges even seed residues whose values happen to be fixed by cribs, conservatively.

For periodic descriptions, choose the modal induced q in each residue class **using only U**; ties use the smallest residue. Let e be the number of U letters disagreeing with that template, and n=73. For autokey descriptions, let the eligible tail be `{i in U: i>=r}`, with n its size, and let e be the number of mismatches to the specified lagged plaintext/ciphertext. In either case the residual cost is:

`log2(n+1) + log2(binomial(n,e)) + e*log2(25)`.

This explicitly encodes the non-crib mismatch count, positions, and non-template values. Crib residuals are conditioned on and disclosed; they are not charged and contribute no evidence. This is a conditional 73-letter code, NOT a full 97-letter-key MDL score. Residual scoring does not resurrect an excluded exact model. For the periodic key, every seed position is charged even if no evidence position observes it. For autokey, free seed positions are not counted as evidence matches; their cost is charged in full. Define score S as literal baseline minus all description costs. Higher is simpler. The statistic M for a ciphertext is the maximum S across **all 32 messages and all 1,152 descriptions**, not the score of an individually selected message. Deterministic ties are broken by candidate ID, tableau ID, structural class, then r. Equal-score top descriptions and score margins are also reported; equal score alone does not establish model equivalence.

This is a fixed operational simplicity measure, not a universal definition of a deliberate key. Scores and ranks for both message groups will be retained. No post-hoc word-likeness, theme, visually pleasing key, minimum length, or alternative score may determine success.

## Exact checks and honest interpretation

For every non-null target (planted controls and K4) and candidate/tableau, derive all 97 key residues and verify full encryption and inverse recovery. This is necessary correctness checking, **not** corroboration: invertibility makes it true even for random plaintext.

Null replicates use the identical primary scorer but omit these non-scoring diagnostics. Separately determine each induced stream's minimum exact period (including all periods 1..97), whether any registered period <=32 fits all 97 letters, and exact tail consistency for each registered autokey length. Evaluate known-crib constraints directly: for periodic models, contradictory required residues at known positions exclude that exact period independently of the candidate; for autokey, fixed known-input/known-output equations can likewise exclude exact fits. Report these exclusions but **do not skip candidate scoring**. Near-structure with paid exceptions remains registered; all crib and non-crib exceptions are disclosed, and an approximate score is never called an exact short-key solution.

## Frozen controls and calibration

Sensitivity is tested across the frozen bank, not arbitrary wording. Sort IDs within each group and interleave thematic0, neutral0, thematic1, neutral1, etc. Assign controls sequentially modulo32 from this schedule: simple indices0–35, structured-hard36–59, running-key60–71. This covers every candidate and both groups; no control plaintext is selected from scores. All controls are run through the exact same full bank and all registered models; no oracle candidate/model is supplied to the scorer.

**Simple positives (36):** for each of 12 tableaus, plant the scheduled frozen plaintext under (a) a period-7 key `KRYPTOS`, (b) plaintext-autokey with seed `PALIMPSEST` (length 10), and (c) ciphertext-autokey with seed `ABSCISSA` (length 8). The key strings are converted by AZ index. Recovery means the planted candidate is top-ranked (ties including another candidate count as failure), with a same-plaintext registered representation that fits all97 letters exactly; recovery of the exact historical label is not required where algebraic equivalences exist. Also report explicit planted-versus-recovered tableau, structure, seed, and full-key label-match booleans. Equal scores alone are not called model equivalence; an alternative exact representation establishes only that it encrypts this same plaintext to this same ciphertext.

**Structured hard positives (24):** each tableau receives (a) a 29-residue random periodic key and (b) a 29-residue random autokey seed, plaintext feedback for even zero-based tableau index and ciphertext feedback for odd index. Tableau order is plaintext alphabet AZ then KR, ciphertext alphabet AZ then KR, operation Vigenère then Beaufort then variant Beaufort. Random sequences use `random.Random(int.from_bytes(SHA256(UTF8('candidate-first-051-v1|' + label)), 'big'))`, with labels and resulting literal keys frozen in controls.json. These test long, non-mnemonic keys rather than merely convenient dictionary keywords. The same full-pipeline candidate recovery criteria apply.

**Out-of-scope hard keys (12):** each tableau receives a distinct 97-letter segment starting at zero-based normalized position13*tableau_index of the frozen independently written passage running_key.txt, normalized A–Z and at least 97 letters long, with no repeated seed or autokey construction. These are diagnostics: report candidate recovery/ranking and flags, but do not claim that failure rejects running-key encryption. A true 97-letter arbitrary key has no special structural evidence under this metric.

**Bank-absent classical controls (12):** one additional independently authored crib-conforming97-letter message is frozen outside the bank and verified absent from all32 entries. For tableau index t, use structural class t modulo3 in the order periodic, plaintext-autokey, ciphertext-autokey, with the same corresponding simple seeds above. Each receives99 conditional calibration nulls and10 validation nulls. A flag here is a spurious bank attribution: the true plaintext is unavailable. The additional operational gate is at most1/12 held-out targets flagged; all scores/ranks are disclosed. These12 targets share one held-out plaintext and do not establish general out-of-bank specificity. Their120 validation null flags are reported separately, not added to the600-denominator gate.

For **each of the 60 in-scope planted targets**, independently draw 99 calibration nulls and 10 validation nulls by uniformly permuting its 73 non-crib ciphertext letters while holding every crib ciphertext letter fixed in place. Each null passes through the entire bank/model maximum M. This preserves length, ciphertext marginal counts, both fixed crib blocks, and every shared crib-derived key feature exactly. For a target maximum m, its conservative conditional Monte Carlo p-value is `(1 + count(calibration M >= m))/100`. Validation nulls use the same independently generated calibration set for that matched target; report the resulting null flag count, overall fraction, and results by tableau and structural class. Controls are numbered C001–C084 in the construction order above; calibration labels are `<control_id>|calibration` and validation labels `<control_id>|validation`, using the SHA256-to-Random scheme above. K4 uses `K4|conditional-null`. Literal controls and RNG labels are frozen before scoring.

A control is flagged only if `M>=16 bits` **and** its conditional p-value is `<=0.05`. Selection of score, threshold, controls, or tested bank must not be revised after viewing their results. Discrete null distributions/ties use the conservative >= convention. Also report empirical score distributions, minimum recovery margins, and every failure, not only an aggregate percentage. The control false-positive rate describes these matched nulls, not all possible non-K4 messages.

The 12 out-of-scope controls receive their own 99 conditional calibration nulls and are reported with the same flagging rule, but are not counted as in-scope sensitivity failures or as false positives: a structured key description may coincidentally compress a genuine running key.

## Gate and K4 evaluation

**Before K4**, require:

1. All unit, randomized round-trip, independent-vector, and end-to-end planted tests pass; audit accepts implementation with matching audited SHA256 hashes for every required source, and manifest is frozen. Freeze refuses missing/mismatched audit hashes.
2. At least 34/36 simple controls correctly recover and flag the planted candidate, with at least 11/12 in each structural class.
3. At least 22/24 structured-hard controls correctly recover and flag it.
4. At most1/12 bank-absent targets flagged.
5. At most 30/600 (5%) matched validation nulls are flagged; all ties/failures and denominator are disclosed. These flags share matched calibration sets and a fixed candidate bank, so they are not600 independent Bernoulli trials. This is an operational pilot gate, not a confidence-bound claim about universal false positives.

If a gate fails, **stop before K4**, report the failure and scope, and do not tune until a separately authorized preregistration exists.

If it passes, accept and hash the canonical 97-letter K4 supplied by the parent. Score it once with the frozen bank/code. Generate **1,999** new conditional nulls preserving K4's crib ciphertext letters and non-crib ciphertext multiset, and score each through the full pipeline. Report conservative global p=`(1+#null maxima >= K4 maximum)/2000`, the top five candidate/model scores, all relevant complexity components, exact/approximate status, full re-encryption/inverse checks, and all induced-key/template residual positions for the winner. This conditions on crib structure rather than pretending shared known letters are new confirmation.

**Exact expansion gate:** expand only if all pre-target gates passed and K4 has `M>=16 bits`, global `p<=0.01`, and at least an 8-bit score margin over the highest-scoring *different plaintext candidate*. Ties among model-equivalent representations of the same candidate do not erase the margin. Passing authorizes no automatic thousands-message search or claim of solution: it merits a separate frozen 128-message replication proposal, with a newly authored blind bank and fresh controls/nulls. A failed target gate closes this 32-message pilot; no thousands-message expansion. Even a passed statistical gate is evidence only for this preregistered structural simplicity statistic and null, not historical authorship or a verified solution.

## Reproducibility and execution limits

Python standard library only unless an independently audited acceleration is justified before freezing. Publish code, candidate bank, seeds, hashes, complete JSON results, tests, exact arithmetic definitions and runtime environment locally under this experiment directory. No external model APIs, paid checker, quota-blocked service, desktop/Mac access, publishing, or external submissions. Do not retrieve K4 from any source before the audit/freeze gate. A blocked step is reported with action, target, reason, completed work, and explicit pending/denied/uncertain state.
