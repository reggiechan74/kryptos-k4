# ALPHABET-GEOMETRY-PILOT-001 — frozen pre-run specification

22 October 2026. This record precedes K4 evaluation. Representation construction
and its validation are separate from these speculative cipher models. The parent
approved this exact pilot after independent review; no geometric feature was fit
to the ciphertext or public cribs.

## Immutable input and arithmetic

The byte-exact core is `data/alphabet-skeleton-v1.json`, SHA-256
`6a5c6eae644dedf88afb68df911f0c3161a969af3815972aa5694479155aa010`.
Its 35 binary components are ordered by its explicit ASCII-sorted primitive IDs.
The full code is `sum(v[i] * 2**i)` using Python arbitrary-precision integers.
It is a geometric codebook identifier, not a measured property or secret cipher.
No alternative order, weight, geometry, alphabet, route, edit or reset is allowed.

Use the unchanged canonical 97-letter fixture and one-based public anchors
22–34 EASTNORTHEAST and 64–74 BERLINCLOCK. Fit only the first island. Berlin is a
public second-stage check, not historically untouched evidence. The 29 letters
between islands must use the same uninterrupted mechanism.

## A — one code-sorted alphabet and unrestricted periodic keys

Sort letters by ascending full code, giving `OCSQVXWAGZITYDPBRKLFENMHJU`.
In these coordinates test `C=P+K` and `C=K-P`, modulo 26, periods 1 through 12.
This is 24 formal structures: 18 baseline rechecks at periods 1–7, 9 and 10,
already excluded by alphabet-independent crib bijectivity; six geometric-alphabet
checks at periods 8, 11 and 12. `C=P-K` is already represented by negating an
unrestricted key; key phase is likewise redundant. There are no dictionary keys.

Each first-crib letter constrains one key residue. Retain every compatible
assignment and every free entry, never fill one arbitrarily. Thirteen consecutive
letters cover every slot at these periods, so a passing training key has no free
entries. Check Berlin with this same key. Record repeated-slot contradiction
certificates, fitted versus checked letters, primitive key periods and duplicate
full outputs. A smaller-period representation is an alias, not a new solution.

## B — full-bit rotation and geometric feedback

For each seed letter, start `S_1=code(seed)` and emit
`C_i=P_i+(S_i mod 26)` in AZ or KRYPTOS coordinates. After emitting each letter,
update `S_(i+1)=rotl35(S_i,r) XOR code(T_i)`, with T either C or P.
All bits remain in state. Test 26 seeds × 35 rotations (0–34) × two feedback
sources × two coordinate alphabets = 3,640 raw models. Rotation zero is identity;
mask to 35 bits. Start at position 1, one shared fixed model throughout.

Encryption and decryption must be causal and invertible for each fixed model.
Enumerate all raw descriptions, training survivors and exact all-24 survivors;
deduplicate exact full plaintext outputs separately. A model is retained only on
13/13 first-island letters and then 11/11 Berlin letters without refitting.
A leading seed is selected by the first island, so those letters are fitting
constraints. No free seed/state masks, constants or additional operators.

## Controls, budget and stopping rule

Before actual K4 scoring, validate complete round trips, independent bit-list
rotation boundary checks and a separately written encoder. B has 48 literal-crib
plants covering r=0,1,17,34, both feedback sources, both alphabets, and seeds A,M,Z.
Run the same complete 3,640-model selector blindly on every planted ciphertext;
require truth inclusion and report all compatible alternatives rather than
assuming unique recovery. Use all 24 A structures as planted reference cases,
including degenerate smaller-period keys. Mutation checks require rejection of
the altered target under that fixed model; another compatible model need not be
absent. Compare decryption against a nearby incompatible rotate-after-XOR rule.

Finite implementation budget: one process; 120 seconds for either pilot's actual
K4 run, 300 seconds for controls, at most 256 MiB of retained result data. Stop
and report budget-unresolved if exceeded. Store all raw model records (not only
best partial scores). No parameter expansion or feature reordering after results.

If there are no exact survivors, report a bounded negative; no null significance
or partial-English claim. If an exact survivor exists, stop before promotion and
request a separately frozen matched null calibration through this full selector.
A fit is not a solution; require full regeneration of the 97-letter ciphertext.
