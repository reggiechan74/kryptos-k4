# Language-layer experiment interfaces

The user selected language/alternative-alphabet work first, then source-supported
masking. The planning manifest is
[LANGUAGE-PREPARATION.json](../research/specifications/LANGUAGE-PREPARATION.json).
It is not an executable historical hypothesis or an authorization for K4 search.

[language_interfaces.py](../experiments/language_interfaces.py) provides exact
finite-map auditing, token-based forward conversion, bounded inversion, length
reachability, and final-English crib checks. The unit-test mappings are explicitly
toy controls. No Shavian, Cyrillic, Unicode-derived, or invented historical table
is embedded in these interfaces.

A mapping must distinguish at least three different operations: English spelling
or translation into an intermediate language/script; the intermediate symbols;
and an explicit transport encoding into A–Z. A historical spelling guide does not
by itself supply a reversible transport code or an inverse to exact English
orthography. Keeping those interfaces separate prevents a modern numerical label
or a convenient glyph resemblance from being promoted into historical evidence.

## Required gates before a historical run

1. Record a source URL, edition/date, exact map, normalization, framing, and what
   has and has not been verified by the source reviewer.
2. Audit symbol collisions, deleted marks, and sequence ambiguity. One-to-one
   symbol mappings do not guarantee that variable-length concatenated sequences
   have a unique inverse. Conversely, a non-prefix code need not be ambiguous.
3. Round-trip every symbol and declared unrelated control sequence. Unknown
   symbols, invalid inputs, ambiguity, budget exhaustion, and deadlines fail
   explicitly; they are not silently repaired or reported as exhaustive negatives.
4. Audit the 97-letter output length under the exact framing rules. A deduction
   about one fixed transport code says nothing about every conceivable language
   layer. Do not force final English crib positions onto an intermediate script.
5. Commit a fixed operational specification before execution. Verify its bytes
   against the referenced commit, then record that SHA, map hashes, parameters,
   fixed seed, budgets, and controls in an atomic run snapshot. No scoring or
   search is enabled by this planning/interface milestone.

No branch may choose pronunciations, translation variants, alphabet orderings,
keys, or deletion rules after inspecting attractive output. If source reading
provides no reversible historical encoding, a narrowly stated feasibility limit
is a valid outcome; it does not exclude the entire script or language family.
