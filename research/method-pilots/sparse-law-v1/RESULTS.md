# Frozen blind40 synthetic pilot — results

## Decision
Retain the simpler common-support CRT oracle as the default exact solver. The join is correct and preserves a large ambiguous relation without expansion, but did not improve timing. No K4 ciphertext/crib letters were used; no target eligibility or solution follows. This is a40-case diagnostic feasibility pilot, not high-powered evidence about arbitrary cryptanalysis.

## Core result
All40 primary projection comparisons and all40 independent oracle replays agreed exactly. Independent audit verified each full factorized relation complete and feasible, not only its marginals. All28 in-family truths were retained at all91 eligible coordinates; **zero false in-family forced values**. **1510/1876 unknown positions** were forced versus219/1876 by dense completion;12/28 in-family cases had all67 unknown positions forced. First6positions were never claimed.

The solver predicts mask responses; subtracting each from the fixed ciphertext gives a bijective plaintext prediction. Features are ciphertext-only and independently reconstructed by the evaluator. Ordinary fixtures sampled uniform ciphertext and derived plaintext, not natural-language or uniform-plaintext samples.

## Model-membership failure stays prominent
All4 deliberately out-of-family observational twins fit all24observations and forced67unknown values, but each had **one wrong forced unknown value** relative to its hidden truth. This is not a numerical bug: their observations are identical to an in-family law and cannot certify membership. Predictions are exact **conditional on this model**, not unconditional recovered truth. Four independent-response nulls and4constructed contradictions were empty; four random nulls do not establish a universal false-positive rate.

|Stratum|Cases|Sparse forced / total unknown|Dense forced|Full unknown vector unique|Wrong forced|
|---|---:|---:|---:|---:|---:|
|global_binary_alias|2|134/134|85|2|0|
|global_repeated|2|134/134|134|2|0|
|inconsistent_repeated_context|4|0/268|0|0|0|
|independent_response_null|4|0/268|0|0|0|
|nonunit|4|245/268|0|1|0|
|observation_equal_alias|2|0/134|0|0|0|
|observation_zero_alias|2|0/134|0|0|0|
|ordinary_support_0|4|220/268|0|1|0|
|ordinary_support_1|4|261/268|0|2|0|
|ordinary_support_2|4|251/268|0|1|0|
|ordinary_support_3|4|265/268|0|3|0|
|out_of_family_observational_twin|4|268/268|268|4|4|

## Program, function and plaintext identifiability
Only3 of28 in-family cases had unique coefficient vectors; all3 were ordinary generating-support3. The other25 had coefficient ambiguity, which can be pure syntax/global identity rather than different functions. The exact global identity13(x²−x)=0 is a counterexample to treating coefficient multiplicity as multiple mechanisms. The earlier disclosed repeated-context diagnostic supplies genuinely different functions: constant7 and17×lag1 give the same predictions on the91 modeled positions of the repeated5 trace, but predict7 and0 on a fresh allzero context. This makes no claim about plaintext positions0..5 or full97-letter recovery. Instance-trace equivalence, global function equivalence and vector uniqueness remain distinct.

## Timing and compression
The same Python3.12.14 standard-library implementations received identical public A,I,b. Inclusive child CPU including startup/output serialization totals: oracle49.321724s, join66.553951s, dense3.111874s, plain27.406985s. Oracle was faster33/40cases. Join additionally serialized the exact relation; stage timings are preserved, so no hidden claim that both output formats incur identical costs. Peak original-method RSS35,632KiB.

Plain join completed28cases and hit the predeclared100000-product cap on12; capped results remain INCOMPLETE, never negatives or uniqueness certificates. Compressed products reached155,112,720 descriptors, including cancellations/global and instance aliases. Descriptor compression is not a count of distinct functions/plaintexts or independent evidence. The oracle also handles these ambiguities without expanding products.

## Blinding and verification
Code/protocol approved and pinned before one custodian-generated seed. Inputs anonymized; true unknown responses/coefficients/explicit labels sealed. Raw lag features reveal ciphertext0..95 and structural strata, so this was truth-blind, not structure-blind. All160 original method processes terminated; source/input guards passed. Output seal preceded independent public-only verification; both seals preceded label release. The original inputs, outputs, release receipt and exact commitment are retained.

After unseal, independently rebuilt all feature rows and causally re-encrypted 1409 distinct-per-case witness laws; all passed. Post-unseal evaluator was authored, hashed and development-smoke-tested before label release. Evaluation CPU 0.803947s. No model/solver/generator code changed after freeze.

## Resource deviation and accounting
Original160methods enforce30CPU seconds/60wall seconds/2GiB AS per process; measured inclusiveCPU146.394534s. Independent pre-unseal replay children use the same limits. Its audit-parent verification process was **not hard-capped and peakRSS was unmeasured**; measured replay+parentCPU113.543704s. This enforcement gap is retained, not converted into a blanket all-stage compliance claim. The separately authorized post-label-release repeat of the unchanged audit also passed all40 cases under an external300CPU-second/2GiB-AS audit-parent limit,600wall timeout, and unchanged30CPU/60wall/2GiB replay-child limits. Measured inclusiveCPU125.239946s and child-tree peakRSS120,436KiB. Its source SHA256 stayed2f495b75382157af913140e9aaccfff04bed119497b5cbd1ba9e611785bbfdf8. It is post-release verification, not a fresh blind result; later RSS cannot establish the missing original peak.

Development charged conservatively120CPU seconds; originalmethods146.394534, firstaudit113.543704, fixturecustody~0.04 and evaluator~0.80, plus125.239946s capped verification repeat and small reporting overhead. Combined measured stages plus conservative development allowance total about506CPU seconds; conservatively charge600seconds to cover residual reporting/static overhead, within3hours. No3hour budget exhaustion observed. Do not infer missing original auditRSS from later repeated measurements.

## Method improvement and stop boundary
Keep the exact oracle and explicit ambiguity/misspecification reporting. A separate next-method proposal may remove provable global feature-function aliases while preserving exact original coefficient-support costs; naive merging can change sparsity and is inadmissible. It needs a new frozen protocol/fresh unseen validation before a speed or capability claim. Do not retune v1 using its revealed cases. Do not widen the dictionary, run old target families or test actual K4 automatically. Further broad reversible-program synthesis remains unsolved by this bounded sparse-additive pilot.

## Immutable provenance
- Approved manifest:21cbfd6793e2c4edbf4d5a676704c614b413bbe236ad7861a9cb88ba30e35bc9
- Protocol:bcd23c496ab6988a3a8316abd66a90c3a6f356f82be1a484e976ce7b7e9bcd6a
- Seed commitment:90bb29c136fa5f04fb9bf78dd526566169259d95e090b4afd5d65b8802f5c0f1
- Public input:0167ef5563c27e67d490974a96b5e65d27ed2800ef0c43d219f1c313e5bcd7ab
- Original output seal:42e17682851129def1911b4200e8af9b79a7d174a1bb6bdc85c003634dfb7643
- Pre-unseal audit seal:0649b585ff7a69e66ab45736f7c0b70500558f60b8266e03fe88ab7cf3960d40
- Release receipt:38f63401362befb46f3f3e92563d4f047209cf1eae52dac55c246403e0bfc933

## Closeout checks
Independent read-only post-unseal audit recomputed every stratum/coverage field and timing total directly from original outputs and labels; PASS. Its reviewed report snapshot is retained as BLIND-REPORT.pre-capped-result.md, SHA2565becb8107f4b41218a695f072b777ae71b82618ee0fdf0afae16d7dc61f7ebe7. Later report edits record completed capped verification/accounting and clarify that the alias example covers91 modeled positions, not all97; no scientific result was revised. Capped audit output seal:e35fd74c7751c6568158e1d444829a0905d1fa4f721f9fee90887ecef6b4339e.
