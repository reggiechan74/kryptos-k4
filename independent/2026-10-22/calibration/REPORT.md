# Bounded K4 discrimination and synthesis calibration

## Bottom line

1. **Cheap statistics distinguish these three toy generators, but do not identify K4's architecture.** A fixed eight-feature classifier got 125/144 held-out examples correct (86.8%). It also assigns 44/48 uniform-random controls to the same forced class as K4. Treating the K4 label as cipher evidence would be a mistake.
2. **The exact affine ciphertext-feedback recurrence grammar is incompatible with the first K4 crib in both alphabets.** No seed search is actually necessary: short modular contradictions certify this result. This rejects only the stated grammar, not feedback ciphers, evolving alphabets, or K4 generally. Novelty relative to earlier project stepping tests has not been established.
3. **Identifiability is a real issue even in the toy synthesis grammar.** All six planted targets were recovered, but only one had a unique full plaintext. Parameter multiplicity and plaintext multiplicity differ. We tested the ambiguity and timeout reporting explicitly.

No repository or user-computer files were accessed or modified. All work was confined to this independent cloud-scratch directory.

## What was frozen before results

See PREREGISTRATION.md, SHA-256 e0f0ee230ab73758e841e1dd91d28e571c7d83fe052f70b7aedb8e68a1bd26fc. Master seed20261022. The preregistration predates corpus generation, model fitting, and result inspection; it is an internal frozen protocol, not an externally registered study.

All ciphertexts have exactly97 A–Z characters. Training and testing each use48 plaintext windows, encrypted once by each of three families, for144 examples per split and288 total. Six separately authored passages supply each split, with no shared passage or identical plaintext window across splits. Eight windows per passage are sampled with replacement, so windows overlap; the held-out set contains47 distinct windows. These are twelve passages authored for the experiment, not independent authors, external books, or a representative natural-language corpus.

The three frozen generators are:
- Periodic additive substitution, uniformly selected period2–12 and independent uniform key symbols.
- Fixed block permutation, uniformly selected width5–12 and a uniform permutation, with defined handling of the final short block. This preserves letter counts.
- One ciphertext-driven evolving alphabet: uniformly random starting permutation; emit A[P_i]; rotate the alphabet left by C_i+1 modulo26 and swap entries0 and13. The decoder can reproduce updates. This one arbitrary algorithm does not represent the class of all evolving alphabets.

All families see the same plaintexts and preprocessing. Every one of288 encrypt/decrypt round trips passed.

The eight fixed statistics are IC, symbol entropy, distinct symbols, maximum count, adjacent-bigram collision rate, adjacent-symbol coincidence, maximum lag coincidence over2–12, and maximum mean residue IC over periods2–12. A training-only standardizer and one logistic regression with C=1 were used. There was no tuning, feature selection, generator selection, or post-result expansion.

## Held-out results and limits

Confusion matrix, rows=true and columns=predicted, in periodic / block permutation / evolving-alphabet order:

| True family | Periodic | Block permutation | Evolving alphabet |
|---|---:|---:|---:|
| Periodic |39|1|8|
| Block permutation |2|46|0|
| Evolving alphabet |8|0|40|

- Training accuracy:91.7%.
- Held-out accuracy:86.8%; macro-F1:0.869.
- Held-out recalls:81.3%,95.8%,83.3%, respectively.
- Six-passage cluster bootstrap accuracy interval:81.9%–91.0%, using2,000 resamples. This measures variation across these six authored held-out passages only. It is not a generalization interval for independent authors, corpora, historical cipher design, or K4.
- A fixed199-run randomized-training-label diagnostic had mean held-out accuracy33.0%, maximum69.4%, and add-one p=0.005. This is a conditional toy-label null, not K4 significance. Global training-label permutation does not calibrate source uncertainty. There was no model-selection search; each permuted run retains the complete lag/period-max features. No post hoc statistic inherits this diagnostic.

### Out-of-family controls are the key result

Each row contains48 new length97 examples; columns are forced model labels, not true classifications.

| Control | Periodic | Block permutation | Evolving alphabet |
|---|---:|---:|---:|
| Unencrypted held-out prose |18|30|0|
| Random monoalphabetic substitution |18|30|0|
| Random shuffle preserving all character counts |1|47|0|
| Uniform-random letters |4|0|44|

The selected features are invariant under a global alphabet relabeling, so the plaintext and monoalphabetic feature vectors are exactly identical. The block-permutation label largely detects preserved nonuniform symbol frequencies, not a particular transposition. Uniform noise is usually assigned the evolving-alphabet label. A three-label forced classifier without an abstention mechanism is not a valid open-world architecture decision rule.

K4's IC is0.03608247 and entropy is4.55478092 bits; its forced label is evolving alphabet. **That label supplies no evidence that the real K4 uses this or any evolving-alphabet design.** The model has no calibrated K4 posterior or K4 p-value. Do not use this result to eliminate architectures or justify an expanded classifier campaign.

## Exact bounded synthesis pilot

Alphabet choices: A–Z and KRYPTOSABCDEFGHIJLMNQUVWXZ. In either coordinate system:

C_i = P_i + K_i (mod26)
K_0 = k
K_i = a K_(i−1) + b + d C_(i−1) (mod26)

Each of k,a,b,d ranges over0..25. No resets, routes, transpositions, alternate signs, keywords, or additional grammar productions. Total parameter descriptions:2×26^4=913,952. The parameter encoding is four5-bit slots plus one alphabet-selector bit,21 bits with unused codes, plus a fixed interpreter. It is not a minimum-description-length, prior-probability, or compression claim. The implementation exhaustively enumerates modular parameter constraints; SAT itself and prior graph-constraint methods are not claimed as novel.

K4 cribs are exactly EASTNORTHEAST at1-based22–34 (13 letters) and BERLINCLOCK at64–74 (11 letters),24 distinct positions total. First-crib fitting and second-crib validation are separate. All913,952 parameter descriptions were exhausted for K4 with zero first-crib fits. Therefore the second crib was not needed and offers no additional evidence in this rejection.

### Short independently checked rejection certificates

For A–Z, the known keystream values at22–34 are:
1,11,25,2,3,2,24,24,6,2,10,0,25.

Transitions23→24 and24→25 give previous(K,C) values(11,11) and(25,17), respectively. Both are(odd,odd), so a fixed affine recurrence must produce the same next-key parity. Required next keys25 and2 have opposite parity. Contradiction modulo2 implies contradiction modulo26, for every seed.

For KRYPTOS coordinates, the known values are:
1,10,21,18,1,15,2,23,5,2,19,0,2.

The first three transition equations leave exactly(a,b,d)=(11,23,24). That triple predicts K26=(11×18+23+24×22) mod26=21, while the crib requires1. An alternative parity-only certificate uses22→23 and26→27: both previous(K,C) parities are(odd,even), but the required next-key parities differ.

A second implementation solved the12 adjacent known-key equations first and then independently enumerated seeds and replayed complete decryptions. It matched all candidate sets for K4 and all six planted positives. A separate root-agent JavaScript calculation independently matched the K4 rejection. No field-rank assumption modulo26 was used.

### Recovery, ambiguity and status controls

Synthetic plaintexts are held-out length97 windows with all24 exact crib characters overwritten before encryption. All six planted descriptions survived.

| Planted a | Parameter fits | Distinct full plaintexts | Forced character positions |
|---:|---:|---:|---:|
|0|39|26|96|
|1|3|2|96|
|2|2|2|96|
|5|3|2|96|
|13|13|13|96|
|25|1|1|97|

Every ambiguity in these six particular positives is confined to plaintext position1. A fixed parameter tuple always gives one deterministic full decryption. Noninvertible transitions can erase information about the seed before a crib; multiple fitting tuples may then yield different earlier plaintexts, or even identical full plaintexts. An invertible planted multiplier does not guarantee uniqueness across the entire candidate grammar either.

With only the first character of the first crib, the underconstrained control has35,152 parameter fits,30,590 distinct full plaintexts, and just one forced character position. This is SAT_AMBIGUOUS_DESCRIPTIONS, not success at solving a message. A zero-time-budget control correctly returns TIMEOUT with incomplete enumeration rather than UNSAT. The normal targets all completed; there were no operational timeouts.

## Recommended use

Keep the small classification harness as a negative-control demonstration, not an architecture detector or reason to train a thousand-example classifier. The useful synthesis outcome is its bounded, auditable grammar and honest identifiability/status behavior. Integrate only after the repository owner checks overlap with prior ciphertext-dependent stepping coverage; do not present already tested families as new exclusions. Any next grammar should be explicitly motivated and bounded before running, and any candidate should survive held-out constraints and full forward verification rather than merely fit selected cribs.

## Reproduction and artifacts

Run python run_calibration.py, then python audit.py in this directory. Dependencies and exact installed versions are recorded in classification_results.json. No network access, secrets, third-party corpus downloads, or user-computer access is needed. Randomness and substantive outputs are deterministic for the recorded environment; elapsed-time fields naturally vary.

Files: PREREGISTRATION.md; corpus.json; run_calibration.py; audit.py; classification_results.json; synthesis_results.json; generated_examples.json; label_null_accuracy.json; audit_results.json; run_summary.json; MANIFEST.json. Full position-wise possible-character sets and forced positions are in synthesis_results.json. Output contains only generated prose and the supplied public K4 string.
