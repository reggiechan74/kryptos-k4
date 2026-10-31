# Hypothesis families

Generated navigation; edit the canonical ledger or receipts, then run `python3 experiments/build_research_navigation.py`. The JSON retains complete scope fields and original log entries. No experiment is executed by this generator.

**Family status is not a universal exclusion.** A narrow negative applies only to its specified model. Evidence-blocked and non-identifiable are different from tested and false.

| Stable ID | Status | Mechanism | Exact scope and remaining inputs |
| --- | --- | --- | --- |
| H-AFFINE-DIGRAPH | analytical exclusion | One fixed 2×2 affine map acts on adjacent pairs. | [H-AFFINE-DIGRAPH canonical record](../../research/HYPOTHESES.md#h-affine-digraph) |
| H-ARCHITECTURE-DIAGNOSIS | non-identifiable | Classify architecture from fixed short-text features. | [H-ARCHITECTURE-DIAGNOSIS canonical record](../../research/HYPOTHESES.md#h-architecture-diagnosis) |
| H-ASYMMETRIC-FEEDBACK | narrow negative | Use distinct fixed AZ/KRYPTOS alphabet roles in feedback. | [H-ASYMMETRIC-FEEDBACK canonical record](../../research/HYPOTHESES.md#h-asymmetric-feedback) |
| H-AUTOKEY-EXACT | non-identifiable | Direct same-alphabet feedback with arbitrary independent primer. | [H-AUTOKEY-EXACT canonical record](../../research/HYPOTHESES.md#h-autokey-exact) |
| H-AUTONOMOUS-RECURRENCE | analytical exclusion | A fixed homogeneous/affine multi-lag modular key generator. | [H-AUTONOMOUS-RECURRENCE canonical record](../../research/HYPOTHESES.md#h-autonomous-recurrence) |
| H-BOOK-CODEBOOK | evidence-blocked | An independently identified edition/page/codebook supplies symbols or running-key material. | [H-BOOK-CODEBOOK canonical record](../../research/HYPOTHESES.md#h-book-codebook) |
| H-BOUNDARY-STATE | narrow negative | One internal boundary resets to the same shared seed/state. | [H-BOUNDARY-STATE canonical record](../../research/HYPOTHESES.md#h-boundary-state) |
| H-CARRY-624 | narrow negative | Persistent state a∈0..25,h∈0..23; t=a+x+k, a'=t mod26, emit(a'+OLDh) mod26, h'=(h+floor(t/26)) mod24. Scalar normal form T'=T+x+k mod624 with nonlinear old-high/new-low readout. | [H-CARRY-624 canonical record](../../research/HYPOTHESES.md#h-carry-624) |
| H-CARVED-ROW-REFLECTION | narrow negative | Reverse letters within the actual four carved K4 rows, then combine with one periodic arithmetic layer in either order. | [H-CARVED-ROW-REFLECTION canonical record](../../research/HYPOTHESES.md#h-carved-row-reflection) |
| H-CELESTIAL-ALTITUDE | evidence-blocked | An independently dated celestial observation supplies altitude/time material rather than a fitted astronomical coincidence. | [H-CELESTIAL-ALTITUDE canonical record](../../research/HYPOTHESES.md#h-celestial-altitude) |
| H-CIPHERTEXT-EXTRA-STEP | narrow negative | Advance a fixed periodic key according to ciphertext classes. | [H-CIPHERTEXT-EXTRA-STEP canonical record](../../research/HYPOTHESES.md#h-ciphertext-extra-step) |
| H-CIPHERTEXT-JOSEPHUS | narrow negative | Remove the current plaintext slot, emit its periodically encrypted letter, then move from the next directional survivor by one plus the emitted letter's fixed-alphabet rank. Key is indexed by emission, not plaintext position. | [H-CIPHERTEXT-JOSEPHUS canonical record](../../research/HYPOTHESES.md#h-ciphertext-josephus) |
| H-CLOCK-24-ROUTE | narrow negative | World Clock-inspired ragged 24-column routes plus periodic substitution. | [H-CLOCK-24-ROUTE canonical record](../../research/HYPOTHESES.md#h-clock-24-route) |
| H-CLOCK-FACE | evidence-blocked | A dated historical city panel/face supplies an instruction. | [H-CLOCK-FACE canonical record](../../research/HYPOTHESES.md#h-clock-face) |
| H-CLOCK-HISTORICAL | evidence-blocked | Historical World Clock city sectors and one daily ring phase implement an observable city/time mapping. | [H-CLOCK-HISTORICAL canonical record](../../research/HYPOTHESES.md#h-clock-historical) |
| H-CLOCK-RESET | analytical exclusion | Restart the same positionwise bijection at both known block starts. | [H-CLOCK-RESET canonical record](../../research/HYPOTHESES.md#h-clock-reset) |
| H-COMPASS-FRAMES | evidence-blocked | Treat engraved north, a physical needle, local lodestone attraction and true north as distinct coordinate frames. | [H-COMPASS-FRAMES canonical record](../../research/HYPOTHESES.md#h-compass-frames) |
| H-COMPASS-REVERSE | evidence-blocked | ENE may denote the direction of travel while the observed object faces WSW, or conversely. | [H-COMPASS-REVERSE canonical record](../../research/HYPOTHESES.md#h-compass-reverse) |
| H-CYLINDRICAL-MIRROR-SAMPLER | evidence-blocked | Global ideal-cylinder/eye/reticle/table parameters (eight for horizontal036, six source parameters for vertical037) select 97 public-tableau cell labels, followed by ordinary reversible keyed arithmetic; actual curved-copper viewing is a separate mechanism. | [H-CYLINDRICAL-MIRROR-SAMPLER canonical record](../../research/HYPOTHESES.md#h-cylindrical-mirror-sampler) |
| H-DELIBERATE-SPELLING | evidence-blocked | A rule-governed deliberate spelling change, or information extracted by correcting it, supplies a preprocessing step or key. | [H-DELIBERATE-SPELLING canonical record](../../research/HYPOTHESES.md#h-deliberate-spelling) |
| H-EGYPTIAN-SIGN-LIST | evidence-blocked | An Egyptian sign system represents text or key material. | [H-EGYPTIAN-SIGN-LIST canonical record](../../research/HYPOTHESES.md#h-egyptian-sign-list) |
| H-ENIGMA-DIRECT | analytical exclusion | Direct aligned standard reflector Enigma. | [H-ENIGMA-DIRECT canonical record](../../research/HYPOTHESES.md#h-enigma-direct) |
| H-EVOLVING-ALPHABET | narrow negative | Ciphertext-driven exchange or fixed-reference prefix reversal of a mutable alphabet. Exact equations and update timing are in the dated proposal linked under Evidence. | [H-EVOLVING-ALPHABET canonical record](../../research/HYPOTHESES.md#h-evolving-alphabet) |
| H-FEISTEL-2ROUND | analytical exclusion | Two shared arbitrary round functions in X=L+F(R), Y=R+G(X), with input/output swaps around the pair map. | [H-FEISTEL-2ROUND canonical record](../../research/HYPOTHESES.md#h-feistel-2round) |
| H-FEISTEL-3ROUND | non-identifiable | A=L+F(R), X=R+G(A), Y=A+H(X), shared arbitrary functions. | [H-FEISTEL-3ROUND canonical record](../../research/HYPOTHESES.md#h-feistel-3round) |
| H-GEO-ENE | evidence-blocked | A geographic ENE relation supplies an instruction. | [H-GEO-ENE canonical record](../../research/HYPOTHESES.md#h-geo-ene) |
| H-GERMAN-TRANSLATION | evidence-blocked | Use one source-fixed German rendering before encryption. | [H-GERMAN-TRANSLATION canonical record](../../research/HYPOTHESES.md#h-german-translation) |
| H-GLYPH-VIEW | evidence-blocked | Viewing the rear can mirror glyph outlines independently of reversing the order in which positions are read. | [H-GLYPH-VIEW canonical record](../../research/HYPOTHESES.md#h-glyph-view) |
| H-GREEK-PHONETIC | narrow negative | English speech is rendered approximately using Greek graphemes, then encrypted; speech sounds are not English or Greek letter names. | [H-GREEK-PHONETIC canonical record](../../research/HYPOTHESES.md#h-greek-phonetic) |
| H-GROMARK-ONE | non-identifiable | One fixed published mod-16 lag-5/6 tuple with unknown alphabets. | [H-GROMARK-ONE canonical record](../../research/HYPOTHESES.md#h-gromark-one) |
| H-IPA-DICTIONARY | narrow negative | Use source-fixed dictionary IPA windows before encryption, or explicitly pronunciation-derived running key material without respelling plaintext. | [H-IPA-DICTIONARY canonical record](../../research/HYPOTHESES.md#h-ipa-dictionary) |
| H-K3-COMPOSITE-PERIODIC | narrow negative | K3-verified U14 after U42 combined with periodic substitution. | [H-K3-COMPOSITE-PERIODIC canonical record](../../research/HYPOTHESES.md#h-k3-composite-periodic) |
| H-K3-SANDWICH | narrow negative | Periodic substitution on both sides of the K3-derived route. | [H-K3-SANDWICH canonical record](../../research/HYPOTHESES.md#h-k3-sandwich) |
| H-KRYPTOS-FINGERPRINT | non-identifiable | Selected small-alphabet distances describe crib structure. | [H-KRYPTOS-FINGERPRINT canonical record](../../research/HYPOTHESES.md#h-kryptos-fingerprint) |
| H-LAG | non-identifiable | Use repeated lag patterns to diagnose an architecture. | [H-LAG canonical record](../../research/HYPOTHESES.md#h-lag) |
| H-LAMP-GREEK | narrow negative | A declared ordering of 24 lamp fields might index Greek symbols or generate key material. | [H-LAMP-GREEK canonical record](../../research/HYPOTHESES.md#h-lamp-greek) |
| H-LAMP-MENGENLEHRE | analytical exclusion | Use the Mengenlehreuhr lamp-count representation, not abstract World Clock columns. | [H-LAMP-MENGENLEHRE canonical record](../../research/HYPOTHESES.md#h-lamp-mengenlehre) |
| H-LANGUAGE | narrow negative | Change language/script representation before encryption. | [H-LANGUAGE canonical record](../../research/HYPOTHESES.md#h-language) |
| H-LETTER-GEOMETRY | narrow negative | Represent idealized glyph geometry with unique feature arrays/codes. | [H-LETTER-GEOMETRY canonical record](../../research/HYPOTHESES.md#h-letter-geometry) |
| H-M138A | evidence-blocked | Historical strip selection/alignment produces a row-dependent alphabet. | [H-M138A canonical record](../../research/HYPOTHESES.md#h-m138a) |
| H-M94-CYCLIC | analytical exclusion | A cyclic permutation alphabet per disc, one shared row displacement within each 25-letter block. | [H-M94-CYCLIC canonical record](../../research/HYPOTHESES.md#h-m94-cyclic) |
| H-MASK-AUTO | narrow negative | Fixed-primer same-alphabet autokey. | [H-MASK-AUTO canonical record](../../research/HYPOTHESES.md#h-mask-auto) |
| H-MASK-FM | analytical exclusion | Standard Morse with x/xx separators, fixed trigrams and an arbitrary shared cipher-letter/trigram permutation. | [H-MASK-FM canonical record](../../research/HYPOTHESES.md#h-mask-fm) |
| H-NEPTUNE | evidence-blocked | Neptune/fountain/discovery context identifies an external instruction. | [H-NEPTUNE canonical record](../../research/HYPOTHESES.md#h-neptune) |
| H-NONLINEAR-BLOCK | non-identifiable | A fixed nonlinear block transformation couples several plaintext letters. | [H-NONLINEAR-BLOCK canonical record](../../research/HYPOTHESES.md#h-nonlinear-block) |
| H-OCCUPIED-CELL-FIXED | narrow negative | Use the actual carved K4 occupied-cell mask with fixed phased keys. | [H-OCCUPIED-CELL-FIXED canonical record](../../research/HYPOTHESES.md#h-occupied-cell-fixed) |
| H-ONE-EDIT | non-identifiable | A bounded construction-error sensitivity arm. | [H-ONE-EDIT canonical record](../../research/HYPOTHESES.md#h-one-edit) |
| H-OPTICAL | evidence-blocked | Physical apertures, illumination, reflection or receiving surfaces select or transform letter information. | [H-OPTICAL canonical record](../../research/HYPOTHESES.md#h-optical) |
| H-OTP | non-identifiable | An unrestricted independent pad can explain any chosen plaintext of the same length. | [H-OTP canonical record](../../research/HYPOTHESES.md#h-otp) |
| H-PERIOD | analytical exclusion | One fixed injective substitution per repeating phase. | [H-PERIOD canonical record](../../research/HYPOTHESES.md#h-period) |
| H-PERM | analytical exclusion | Pure permutation preserves the letter multiset. | [H-PERM canonical record](../../research/HYPOTHESES.md#h-perm) |
| H-PHONETIC-RESPELLING | narrow negative | Stylized phonetic respelling precedes encryption. | [H-PHONETIC-RESPELLING canonical record](../../research/HYPOTHESES.md#h-phonetic-respelling) |
| H-PLAINTEXT-EXTRA-STEP | narrow negative | Advance by one or two according to plaintext vowel/consonant membership. | [H-PLAINTEXT-EXTRA-STEP canonical record](../../research/HYPOTHESES.md#h-plaintext-extra-step) |
| H-RADIX-FEEDBACK | analytical exclusion | Changing-base geometric codes enter a fixed affine key recurrence. | [H-RADIX-FEEDBACK canonical record](../../research/HYPOTHESES.md#h-radix-feedback) |
| H-RECURRENCE-CLOCK | narrow negative | Select an immutable repeating-key entry using ciphertext recurrence distance; emit then advance1 for a new letter or its last-occurrence gap. | [H-RECURRENCE-CLOCK canonical record](../../research/HYPOTHESES.md#h-recurrence-clock) |
| H-ROUTE | narrow negative | One enumerated route plus periodic arithmetic. | [H-ROUTE canonical record](../../research/HYPOTHESES.md#h-route) |
| H-RUNKEY | narrow negative | Literal source-text or ordinary-language running keys under explicitly fixed alphabets, arithmetic, normalization and alignment. | [H-RUNKEY canonical record](../../research/HYPOTHESES.md#h-runkey) |
| H-SHADOW-TIME | evidence-blocked | A source-fixed shadow direction or observation time supplies a key or reading instruction. | [H-SHADOW-TIME canonical record](../../research/HYPOTHESES.md#h-shadow-time) |
| H-SIGABA | narrow negative | Authentic CSP-889 three-bank irregular stepping with the published simulator wiring set. | [H-SIGABA canonical record](../../research/HYPOTHESES.md#h-sigaba) |
| H-SIGABA-INSPIRED | narrow negative | Five custom cipher rotors are irregularly stepped by separate control and static index banks, with a fully reversible alphabet path. | [H-SIGABA-INSPIRED canonical record](../../research/HYPOTHESES.md#h-sigaba-inspired) |
| H-SILK-PERIODIC | analytical exclusion | Repeat a direct key from one photographed silk chart. | [H-SILK-PERIODIC canonical record](../../research/HYPOTHESES.md#h-silk-periodic) |
| H-SPLIT-COORDINATE-ROUTES | narrow negative | Permute two coordinate streams separately. | [H-SPLIT-COORDINATE-ROUTES canonical record](../../research/HYPOTHESES.md#h-split-coordinate-routes) |
| H-SUM-ROTATION | narrow negative | Periodic addition followed by right rotation of consecutive blocks, amount equal to their integer rank sum modulo actual block length. Ciphertext sum determines exact inverse rotation. | [H-SUM-ROTATION canonical record](../../research/HYPOTHESES.md#h-sum-rotation) |
| H-TREE-STATEFUL | narrow negative | Letters or geometry fragments walk a tree and update cipher state carried between letters. | [H-TREE-STATEFUL canonical record](../../research/HYPOTHESES.md#h-tree-stateful) |
| H-TRIFID | narrow negative | Apply one of the fixed Trifid cubes/directions. | [H-TRIFID canonical record](../../research/HYPOTHESES.md#h-trifid) |
| H-WHEATSTONE | analytical exclusion | Fixed 27/26 geared rings with displacement determined by the adjacent processed plaintext pair; both ring alphabets and starting phases may be arbitrary. | [H-WHEATSTONE canonical record](../../research/HYPOTHESES.md#h-wheatstone) |
| H-WORD-COVER-EXTRACTION | non-identifiable | Decrypt the full97letter English cover, tokenize under a declared global model and extract fixed letter k from every Nth word at one global phase; output length is derived, not assumed15. | [H-WORD-COVER-EXTRACTION canonical record](../../research/HYPOTHESES.md#h-word-cover-extraction) |
| H-WORD-SCRAMBLE | narrow negative | Permute internal word letters while retaining endpoints before a cipher. | [H-WORD-SCRAMBLE canonical record](../../research/HYPOTHESES.md#h-word-scramble) |
