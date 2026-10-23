# Stateful tree/path cipher: bounded implementation and test

23 October 2026 UTC. All 104 fixed settings fail EASTNORTHEAST. This is a negative result for two explicitly implemented tree constructions, not a dismissal of the user's general tree idea. No K4 plaintext candidate remains.

The [protocol](TREE-PATH-CIPHER-SPEC.md) was frozen in ecf47b3, then implementation and complete planted controls were committed in 2711670 before actual evaluation. Two trees are used: the existing geometric feature decision tree, and an A–Z Morse trie. Each has 26 ordered letter slots, including letter-bearing internal nodes in Morse. A seed rotates initial cipher labels over slots; after each letter the path rotates labels within its chosen subtrees. Two rotation directions give 2 × 2 × 26 settings. The full slot and path tables are saved in the results.

This is a stateful cipher rather than the earlier letter-lookup tree. Proper-subtree permutations change global cyclic adjacency; control receipts give concrete non-global-rotation witnesses. The previous move-to-front rules move a ciphertext symbol in a single global ordering. Here the recovered plaintext path controls a composition of fixed subtree cycles. This establishes a distinct mechanism from those finite prior domains, not worldwide novelty. The standard Morse table is a design input, not evidence of Sanborn's algorithm; the [ITU recommendation page](https://www.itu.int/rec/R-REC-M.1677-1-200910-I/en) identifies the current standard. Its PDF timed out during this audit, so no fresh PDF inspection is claimed.

One ciphertext letter frames each plaintext letter. Morse bits are internal path instructions, not a delimiter-free transmitted stream: framed E,E and I remain different despite sharing concatenated dots. At each step the labels are a permutation; the receiver finds exactly one labeled slot, recovers its letter and applies the same path update. Induction proves unique fixed-model decoding for every A–Z string. Unknown key/model ambiguity is a different question. This small seed space is not a claim of cryptographic security.

All 97 K4 characters were decrypted from position 1 with continuous state. No unknown prefix was guessed and neither crib start reset the state. Every decryption re-encrypts exactly. There are 104 distinct full decryptions, zero first-crib survivors and zero complete 24-letter survivors. The public Berlin check was computed for transparency without fitting; it contributes no rescued candidate. No partial-English scoring, statistical significance claim, or parameter expansion followed the failures.

Controls passed before evaluation: 520 unrelated-message round-trip/path checks, 70,304 letter-bijection checks across sampled states, 104 complete planted selectors totaling 10,816 model decodes, and 104 update-before-output mutation detections. The separately written dictionary-state oracle derives subtree membership from path prefixes and agrees with encoder and decoder. Each literal-crib plant retained its true setting; in this particular fixture each selector had exactly one compatible setting. That observed uniqueness is not a theorem for every possible message. Controls took 12.848 seconds; actual evaluation took 0.115 seconds, within the frozen budgets.

Reproduce:

```sh
python3 -m experiments.tree_path_cipher --output /tmp/tree-controls.json
python3 -m experiments.tree_path_cipher --actual --output /tmp/tree-actual.json
python3 -m unittest discover -s tests -v
```

[Implementation](../experiments/tree_path_cipher.py), [controls](../results/TREE-PATH-CIPHER-001-controls.json), [complete actual results](../results/TREE-PATH-CIPHER-001.json), and [regression tests](../tests/test_tree_path_cipher.py) preserve the finite scope. Timing fields vary on replay; protocol/source hashes and model results are deterministic. A different tree, arbitrary initial permutation, different path action, bit-stream framing or other update mechanism remains outside this experiment. No automatic next search is launched.

Final aggregate verification: 295 repository tests passed in 10.732 seconds. No Site deployment or main-branch change was performed.
