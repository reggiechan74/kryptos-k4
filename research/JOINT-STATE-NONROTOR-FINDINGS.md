# Joint-state feasibility and exact non-rotor constraints

23 October 2026. Full joint SIGABA inference remains **unimplemented/budget-unresolved**, not excluded. The tractable pivot produced exact exclusions of the stated cyclic-disc model and eight two-round additive Feistel structures. No K4 solution or partial-English lead is claimed.

## Why another joint rotor sweep is not justified

The [frozen assessment](SIGABA-JOINT-FEASIBILITY-SPEC.md) exactly enumerates all 100,000 independent index-position tuples at fixed wheel order/orientation. There are **66,058 distinct ten-digit-to-five-magnet functions**. Each output magnet has two input digits; dropping the unused collector digit zero leaves the same number of function classes. Identical functions guarantee identical stepping under every control input. Class multiplicities range 1–6; this only reduces the index descriptions by about 1.51×.

An instantaneous four-distinct-letter control-output relaxation permits **27–30 of the 30 nonempty proper step masks**, depending on index class. This modest pruning ignores the shared evolving control bank and cannot be substituted for it. The normal three-wheel control counter has one 17,576-state cycle; two static outer positions give 26^5 control starts. Treating moving starts as cycle phases is exact kinematics, but does not remove those unknown phases.

Two layouts × 26^5 control starts × 66,058 index-function classes leave **1,569,719,871,616 controller descriptions**, not proven distinct schedules. Synthetic single-schedule joins provide an empirical naive-sweep timing projection of centuries on this executor; exact timing and raw measurements are in [the result](../results/SIGABA-JOINT-FEASIBILITY-003.json). This is neither a lower bound nor proof that a better algorithm cannot work. Existing Python Z3/OR-Tools bindings were not found; no software was installed. No new actual K4 rotor settings were tested in this assessment.

A sound future symbolic formulation would retain five initial control positions, one reachable index function, and five cipher positions. For time t, compute four control paths, map their collector digits through the shared index function, and OR the resulting magnets. Cipher position j then equals its initial position minus its accumulated selected-step count modulo 26. Apply the known-letter rotor constraints only at disclosed positions while preserving state through gaps. Replacing each time's mask by an independently selected allowed mask would be a relaxation, not authentic SIGABA. The current index quotient and cost projection do not supply a complete solver for this coupled system; another arbitrary key slice would not address that gap.

## Cyclic-disc boundary: no inventory search needed

The original [1942 War Department manual](https://www.cryptomuseum.com/crypto/usa/m94/files/FM24-5_1942_pp70-81.pdf), Section V, provides the M-94 row-choice mechanism. We model a fixed permutation alphabet on each disc and one common cyclic displacement per 25-letter block. A nonzero displacement has no fixed symbols; zero displacement leaves every symbol unchanged. This holds for every valid disc inventory and key order.

Within the first disclosed island, position **33 is S→S**, forcing zero displacement in its block, whereas position **26 is N→Q**, forbidding zero in that same block. Independently, K→K at 74 and B→N at 64 contradict one common row in their block. Allowing the plaintext row as a relaxation therefore does not rescue the model. Zero disc keys or permutations were enumerated. This reuses the known fixed-point principle; it is not a newly discovered cryptographic invariant, and does not exclude an outer substitution, different framing or variable per-letter displacement.

Source checking also found invalid strings in the [museum transcription](https://www.cryptomuseum.com/crypto/usa/m94/): disc 5 repeats U and lacks Y; disc 25 repeats K and lacks H. Exact strings/source hashes are preserved in [the rejected-source receipt](../data/m94-source-quality.json). No repair was guessed and no historical known-answer pass is claimed for that table. The invariant is independent of specific valid alphabets. M-138A's original inventory was not obtained; public manual retrieval returned 403 and was not bypassed. This is not a relabeled full M-138A test.

## Eight unrestricted nonlinear function families

The [protocol](NONROTOR-STRUCTURAL-SPEC.md) freezes input/output coordinates independently AZ or KRYPTOS, pair origin 1 or 2, and

`X = L + F(R); Y = R + G(X) (mod26)`.

Both shared round functions are completely arbitrary, including nonlinear and noninvertible functions. The whole pair map is always reversible: `R=Y−G(X); L=X−F(R)`. IBM's [historical overview](https://research.ibm.com/topics/cryptography) supplies general pre-1990 Feistel context; our two-round Z26 construction is a mathematical hypothesis, not an implementation of DES/Lucifer or evidence of creator use. Affine round functions overlap the older affine boundary; arbitrary nonlinear functions were outside it.

All **eight structures reject**:

| Pair origin | Structures | First-stage result | Second-stage result |
| --- | ---: | --- | --- |
| 2 | 4 | Contradictory F entry already within EASTNORTHEAST | Not needed |
| 1 | 4 | One compact branch each, 6 F entries and 7 G entries fixed; **26^39** complete keys per structure | A forced Berlin right letter disagrees in every case |

For origin 2, the pairs at 24–25 and 28–29 share right plaintext T but require different F(T). For AZ→AZ the required values are 25 and 24. For origin 1, the pairs at 25–26 and 67–68 share ciphertext-left V but require different G(V): AZ→AZ requires 3 versus 11. Equivalently the training branch forces plaintext position 68 to Q, not I. The other three coordinate choices force X, V or P there, also not I. These are model-conditional non-fit predictions; they are not four independent statistical observations. The first-crib fits themselves spend thirteen function values on thirteen known letters and supply no additional training closure.

Unknown partners at crib edges are handled exactly, not discarded. A known right letter fixes G at its ciphertext-left input even if the left partner is unknown. A known left letter retains every compatible free G value and consequent F entry. Compact branches describe all completions with exact integer key volumes; parameter counts are not full-plaintext counts. No complete actual fit survives, so no plaintext candidate or null-calibrated significance is asserted.

The first diagnostic computed all-crib certificates even for four training-negative structures. The final stage accounting now stops those at training; [the original diagnostic](../results/NONROTOR-STRUCTURAL-004-initial-diagnostic.json) is preserved. No model, function domain or alphabet was changed. [Final result](../results/NONROTOR-STRUCTURAL-004.json), [controls](../results/NONROTOR-STRUCTURAL-004-controls.json), [post-run independent JavaScript certificates](../results/NONROTOR-STRUCTURAL-004-independent.json). The JavaScript audit verifies the actual contradictions but deliberately does not implement the general unknown-partner branch solver; the complete tiny-ring comparisons validate that production path.

## Verification and remaining scope

The controls compare entire compatible function sets on twelve complete tiny-ring cases, retain sixteen literal-crib plants across both pair origins/all alphabet roles, and check 10,816 full-pair roundtrips. Repeated-entry mutations reject. Cyclic-disc controls exhaust all permutations on rings 2–6 and all shifts, including zero. Tests preserve the difference between ambiguous fits, analytical exclusions and budget-unresolved inference. No downloaded third-party executable was run.

Three or more rounds, a final swap, larger blocks, stateful/changing functions and other independently justified nonlinear constructions are untested. They were not added after these negatives. The next useful step needs a specific structural rationale and a new freeze, rather than treating an extra round or a free mask as automatically informative. Joint SIGABA remains a solver-design problem with explicit missing implementation, while physical models still require unavailable measured inputs.
