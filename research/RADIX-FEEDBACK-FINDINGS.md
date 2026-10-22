# Changing-base geometric feedback — exact admissibility result

22 October 2026. All eight frozen first-order affine feature-feedback families
are contradicted within EASTNORTHEAST. This remains true even if every letter
gets any independently chosen integer base at least two. Consequently no root,
root degree, digit radix or offset search is needed for this specified family.
This is not a rejection of all geometric ciphers or all root-driven algorithms.

## Frozen scope and provenance

For the unchanged 35-feature glyph vectors, define
`code_b(T)=sum(v(T)[j]*b**j, j=0..34)`. Each position may choose any integer b>=2.
In AZ or KRYPTOS coordinates, the letter equation is either C=P+K or C=K-P modulo
26. After emitting letter i, update
`K_(i+1)=a*K_i+c+d*code_b_i(T_i) mod 26`, with T globally chosen as P or C.
The coefficients a,c,d are arbitrary fixed residues modulo 26. The initial key
is arbitrary; there are no resets, routes, fitted masks or changing coefficients.
Two alphabets × two equations × two sources give eight formal families. They
include old degenerate subcases such as d=0; this count is not a claim of eight
globally new methods or independent searches.

Independent per-position base freedom is a relaxation containing every fixed
digit-plus-two schedule, including digits from pi, e or nth roots in radices
10, 12, 16 and 60. It does not model every possible use of those digits. Allowing
an arbitrary key at the start of the crib further relaxes prefix reachability;
a contradiction in that relaxed model excludes any constrained prefix too.

The operational specification was frozen before feasibility testing, with prior
knowledge of a candidate parity argument disclosed. It was not a blind discovery.
A dated pre-test amendment corrected a validation reference to a nonexistent
dense-vector field by deriving vectors from the unchanged sparse core. Neither
the mathematical family nor geometry/order changed. Core SHA-256 remains
`6a5c6eae644dedf88afb68df911f0c3161a969af3815972aa5694479155aa010`.

## Why the base schedule cannot rescue these cases

For any integer base, code parity is v[0] when the base is even and sum(v) modulo
2 when it is odd. A glyph with component zero absent and an even component count
therefore has an even code for every base. E, L, Q, S and T all qualify in this
frozen model. Their transitions reduce to
`K_next mod 2 = a*(K mod 2)+c mod 2`, independently of d and the chosen base.

The following pairs require opposite outputs for the same input parity:

| Coordinates | Feedback | Transition starts, one-based | Source glyphs | Contradictory requirements |
| --- | --- | --- | --- | --- |
| AZ | Plaintext | 22 and 24 | E and S | a+c=1; a+c=0 |
| AZ | Ciphertext | 23 and 26 | L and Q | a+c=1; a+c=0 |
| KRYPTOS | Plaintext | 22 and 29 | E and T | a+c=0; a+c=1 |
| KRYPTOS | Ciphertext | 23 and 33 | L and S | c=1; c=0 |

Each obstruction applies to both equations: their full inferred keys C-P and
C+P differ, but their parity sequences agree because the difference is 2P.
There are eight formal families and four shared parity obstructions, not eight
independent statistical discoveries. All certificates use only the first crib.
The minimum two-transition cores are selected lexicographically; one transition
alone always admits some coefficients. Local checks recompute the full key
sequences, source alignment, attainable residues and every certificate.

Both supplied implementations also enumerate all 26^3 coefficient triples per
family, independently allowing every attainable code residue at each transition.
All eight have zero survivors. Bases 2–27 cover every base residue modulo 26,
and these integer polynomials depend only on that residue; this covers all
integer bases, not just a truncated base search. The proof does not assume
invertible coefficients or a guessed initial key. No significance test is needed
for an exact contradiction.

## Controls and independent replay

Both result files replay byte for byte. The primary audit records 3,264 full
synthetic round trips across all families, twelve varied schedules and 34
coefficient triples. Schedules include huge bases and exact sqrt(2) digit
schedules in radices 10, 12, 16 and 60, using integer square roots without floats.
Sparse-power encryption and dense Horner decryption agree on plaintext and full
key traces. All planted coefficient choices remain admissible; this is truth
inclusion, not a claim of unique inference from arbitrary-base observations.

Additional controls include all coefficient-parity triples, full positive
modulo-26 solves, 286 polynomial/parity checks, odd-code counterexamples and an
alignment mutation: the pinned after-letter procedure emits H whereas advancing
before the letter incorrectly emits O. The independent implementation separately
checks certificates and full modular constraints without reading primary code.

No Berlin feasibility evaluation was performed in this audit. The phrase remains
public and has been used elsewhere; it is not historically untouched evidence.
No actual root/digit sequence was searched against K4. Synthetic root schedules
are implementation controls only.

## Separate auxiliary direct-map check

The frozen specification also includes a separately labeled map
`index(C_i)=code_b_i(P_i) mod 26`, with independently chosen bases 2–61.
It fails at position 22 in both alphabets: E's attainable residues are
`{0,2,4,6,10,14,16,22}`, whereas F's AZ and KRYPTOS indices are 5 and 12.
This direct-map result does not stand in for the feedback proof. No additional
affine shift, mask or alternative standalone map was introduced.

## Files and limits

Original specifications, amendment, reports, code, results and checksum manifest
are preserved unchanged in `independent/2026-10-22/radix-feedback/`. The received
archive SHA-256 is
`9bfdf80275d668281e7309e4ea97a5c1e604dd76dcc15cb956ca61c23839ad84`.
Primary and independent result hashes are respectively
`dc7253ba8619df6e8994852b474e2b90e79ce7acf1cb2e0c45e946a2094cbc3e`
and `3f572b8988e1573ea7055748a5da77dd286132f5e7e2f407152fa69a058b9291`.

Run `python3 experiments/probability_radix_review.py` for isolated replays and
local exact checks. The [receipt](../results/GEOMETRIC-PROBABILITY-RADIX-LOCAL-REPLAY.json)
keeps replay evidence separate from originals. The [probability report](PERIODIC-CRIB-CALIBRATION.md)
concerns the older 24 periodic models, not this exact-proof family. The separate
[raw-number security audit](GEOMETRIC-BASE-SECURITY-AUDIT.md) has different output
assumptions and is not a K4 decoding test.

Different glyphs, feature order, non-affine updates, larger states, timing,
resets, routes or extra transforms are outside this result. None was added after
these failures. The bounded batch stops here.

Integration validation: all 267 repository tests pass in 9.545 seconds.
