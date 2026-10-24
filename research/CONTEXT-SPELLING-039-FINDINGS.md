# Family 2: one-letter context fails; two-letter context overfits

Local039,24October2026. **A consistent reversible contextual channel can fit the two confirmed spelling anomalies, but the fit is massively underdetermined and predicts neither held-out mistake.** This is a stronger distinction than032's uniform-substitution negative; it is not evidence that such a channel was used.

[Pre-outcome protocol](CONTEXT-SPELLING-039-SPEC.md), [complete source constraints/witnesses](../results/CONTEXT-SPELLING-039-ORIGINAL.json), [solver and independent brute force](../experiments/context_spelling_039.py), [cross-version replay](../results/CONTEXT-SPELLING-039-REPLAY.json).

Twelve descriptions cover source memory0/1/2, each scan direction and each normal→literal/literal→normal role. Memory0 repeats032 for calibration. All four memory1 descriptions fail; all four memory2 descriptions fit. These counts are model descriptions, not independent keys or historically selected rules.

A direct contradiction is normal O after R: it becomes U in UNDERGRUUND but stays O elsewhere in K2 (including its ending). Looking from the other side also fails: O before U changes at the anomaly but stays O at another occurrence. Exact full-stream coordinates and corresponding inverse/injectivity witnesses are retained. The tested representation removes nonletters and resets only between complete K sections; it does not assert a word-boundary rule. Q→L and U→O still have different shifts.

For memory2, there are703reachable contexts including beginning padding. Each fit leaves17,942context/input entries unspecified, with more than10^18232 possible complete permutation tables. Exact counts are encoded as prime exponents, avoiding a huge decimal serialization. A deterministic completion reproduces both entire known source streams and reverses them, but this is only an ambiguity witness. It does not locate mistakes in fresh text.

Training on K1 alone forces22correct K2 positions while347remain unconstrained. Training on K2 forces10correct K1 positions while53remain unconstrained. For every fitting direction/role, the held-out changed letter is unconstrained; the rule has learned no predictive error pattern. No post-hoc exception/longer memory was added. K3's A→E plus insertedE is not silently reduced to a substitution; its full length-changing channel remains outside this family, and its intent remains uncertain.

Independent enumeration compares all341binary source/target relations through length4 against every one of the8reachable memory1 permutation tables. All248full-table roundtrips pass. Saved contradiction witnesses, completed-table forward/inverse controls, held-out anomaly checks and Python3.12 semantic replay pass. Exact constraints need no English-fragment ranking or chance p-value.

**Completion boundary:** arbitrary short contextual bijections are now classified within this finite class; larger/contextual insertion systems remain open. A source-selected context rule or independently predictable mistake remains missing. No actual K4 cipher trials, inferred error sites, recovered key, Site changes or public push. The broader deliberate-spelling family survives as uninstantiated, not solved or globally rejected. UTC original/replay times are separate in the receipts.
