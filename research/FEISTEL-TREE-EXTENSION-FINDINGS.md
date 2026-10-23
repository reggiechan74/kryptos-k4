# Feistel symmetry, exact three-round volume and arbitrary tree state

23 October 2026. The expanded two-round models reject. The three-round arbitrary-function models fit but are **non-identifiable**, with two distinct full plaintext witnesses in each case. The prioritized follow-up to the registered tree mechanism excludes its two fixed tree/update primitives even with arbitrary crib-start labelings. None of these results identifies K4's cipher or plaintext.

## 1. Symmetries: 24 new cases, not aliases or new alphabet guesses

The [frozen protocol](FEISTEL-EXTENSION-SPEC.md) allows input/output swaps around the existing two-round map, the same AZ/KRYPTOS input/output coordinates and both adjacent-pair origins. There are 32 raw labels, including eight previously rejected no-swap labels. All 32 are proved different as transformation families under these definitions; this does not mean their members are disjoint or that outcomes are statistically independent.

The alias audit constructs complete 26×26 synthetic pair maps. For all 120 unordered comparisons among the sixteen same-origin wrapper/alphabet families, it preserves a source key whose map violates an exact target function-entry constraint. A single counterexample establishes unequal sets; passing finite probes would not establish an alias. Sixteen endpoint witnesses separately distinguish the origins: origin 1 can change the first raw character while every origin 2 model copies it. Arbitrary coordinate relabeling cannot simply be assumed harmless when the model uses addition modulo 26. The relation between swapping both ends and an inverse map is recorded, but prior inverse roundtrip controls were not actual inverse-family K4 tests.

All **24 newly tested swap labels reject**: twelve at training and twelve after training against the public Berlin equations. The eight old labels were skipped. The [raw result](../results/FEISTEL-SYMMETRY-005.json) preserves all training branches, fitted-key volumes and contradictions. [Alias witnesses and 32 literal-crib plants](../results/FEISTEL-SYMMETRY-005-controls.json) are separate. No final swap, coordinate role or pair-origin alias is silently counted twice.

## 2. Three rounds: exact compatibility is not a decoding

Four frozen coordinate-role cases use canonical origin 1 and no outer swaps:

`A=L+F(R); X=R+G(A); Y=A+H(X) (mod26)`.

All three round functions are arbitrary shared functions. The map is reversible without requiring them to be injective. The choice of origin 1 makes every partial crib pair known on its right side and permits exact counting; it is a computational choice, not historical evidence. Other three-round origins/wrappers remain untested. Covered two-round slices such as H=0 are included, not called independently new hypotheses.

All four cases admit **more than 10^75 complete key descriptions after all 24 cribs**. Exact integers for training and the all-crib family, full component descriptions and witnesses are in [the result](../results/FEISTEL-THREE-005.json). There are eleven F/H components, ten observed F inputs and twelve observed H inputs, leaving thirty F/H entries unobserved. Only 26 multi-point core-offset combinations are explicitly counted per all-crib case; singleton components are handled by exact combinatorics. No 26^78-key sweep occurred.

The equation F(R)+H(X)=Y−L supplies modular component potentials. Every known right letter also requires G(Y−H(X))=X−R. Equal G inputs must receive equal outputs, but G need not be a permutation. Component offsets, existing compatible G-input values, new distinct input values and free G entries are all retained in the count. One global translation gauge is removed and restored for **raw complete-function parameter counts**. These are not counts of distinct encryption functions or distinct 97-character plaintexts; additional function aliases are not claimed classified.

For every coordinate case, two complete F/G/H keys decrypt the same ciphertext to **different 97-letter streams**, preserve all 24 confirmed letters, and exactly regenerate the ciphertext. The second witness changes a free function entry used outside observed pairs. This proves actual plaintext ambiguity, beyond merely counting unused key entries. Both streams are deliberately labeled arbitrary crib fits, with no English scoring or solution claim. No historically untouched plaintext checks exist here, and training-stage Berlin marginals were not computed or claimed forced. Compatibility-volume ratios are not posterior probabilities or calibrated evidence for the cipher.

The independently written [JavaScript counter](../experiments/feistel_three_oracle.mjs) propagates signed F/H potentials and uses a sequential existing/new-color recurrence, rather than the production Q=−H graph and Stirling/binomial polynomial. It reproduces every exact training/all-crib count. Its own complete tiny-function checks are retained in [the independent receipt](../results/FEISTEL-THREE-005-independent.json). Production controls include eight full small F/G/H enumerations, five independent modulus 4 weighted F/H enumerations, sixteen singleton-count enumerations, four literal-crib plants, zero-observation/gauge controls and mutated incompatible constraints. [Controls](../results/FEISTEL-THREE-005-controls.json).

## 3. Priority pivot: arbitrary starting labels in the fixed trees

Instead of adding another Feistel round, [TREE-STATE-SUPPORT-006](TREE-STATE-SUPPORT-SPEC.md) removes the cyclic-seed restriction from the registered tree primitive. It keeps exactly the prior geometry/Morse trees, subtree update, directions and timing. The free labeling is the cipher-label state; plaintext-to-path assignments remain frozen. Within a disclosed plaintext island, the selected paths and updates are known permutations. Propagating symbolic initial slot IDs therefore gives exact conditions on an arbitrary start labeling.

Each island is granted every permutation at its start. This is a conservative **necessary-condition relaxation**, not a proposed reset or an assertion that every granted state can arise from the actual unknown prefix. A repeated slot requiring different letters, or different slots requiring the same letter, excludes every permutation. If a local window were compatible, its count would be (26−assigned_slots)!, but that would not establish a global initial key or license multiplying the two local counts.

All four tree/direction primitives fail **each island independently**. First-island examples:

| Primitive | Exact obstruction |
| --- | --- |
| Geometry, +1 | Positions 25 and 26 select initial slot 21 but require V and Q |
| Geometry, −1 | Positions 26 and 27 select slots 11 and 10 but both require Q |
| Morse, +1 | Positions 22 and 24 select initial slot 0 but require F and R |
| Morse, −1 | Positions 26 and 27 select slots 15 and 14 but both require Q |

The [complete slot traces and certificates](../results/TREE-STATE-SUPPORT-006.json) rule out those same continuous primitives for every initial labeling, regardless of unknown prefix/gap state. This strengthens the earlier 104 cyclic-seed negatives without enumerating 26! keys or asserting anything about all possible trees. [Controls](../results/TREE-STATE-SUPPORT-006-controls.json) compare complete compatible sets in forty toy permutation systems, detect forty injectivity mutations, and retain true per-window states in twelve continuous literal-crib plants using non-cyclic labelings. A separate path-prefix dictionary oracle agrees. Different trees, traversal/update rules, encodings or framing are outside coverage.

## Boundaries and next priority

These experiments are exact or explicitly underidentified; no null significance, arbitrary extra round or attractive completion is used to rescue a model. The tree extension was separately frozen after the three-round identifiability result, before its own implementation/evaluation. Existing physical geometry and archival access limits remain unchanged; no exhausted public archive was requeried and the Site was not changed.

A read-only prior-art follow-up checked pinned Wheatstone generation. Its alphabet generator explicitly includes reversals, and the test handles every blank slot and arbitrary inner alphabet with an unknown inter-island shift. Plain ring reversal is therefore not an untouched next experiment. The source-scope receipt retains pins/hashes; downloaded source was not executed. A new Wheatstone convention needs actual source evidence of a different mechanism, not another already-covered ring direction. The priority is a source-grounded restrictive mechanism or a demonstrably distinct registered state rule with a non-fit prediction; a fourth arbitrary Feistel round would increase unidentifiability rather than supply that missing evidence.
