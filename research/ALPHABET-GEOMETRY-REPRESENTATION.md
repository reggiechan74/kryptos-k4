# Alphabet geometry representation

This task defines an auditable representation, not a cipher or K4 experiment.
It uses idealized uppercase skeletons, not serif outlines, pen trajectories or
measurements of the copper sculpture. Primitive geometry is the source; fixed
arrays are generated from a shared declared geometric dictionary. Letter labels
identify records but are not appended as array components.

The user's original pen-stroke anchors were A=3, B=2, C=1, D=2, E=4. They describe
hand movements, not the refined geometric decomposition. In the latter, B has one
straight segment and two curves, D one straight segment and one curve. No pen-stroke
counts are inferred for the rest of the alphabet. I bars, the decomposition of S,
and U's bottom curve are declared modeling choices, not universal glyph facts.

## Frozen model and numeric audit

The [core](../data/alphabet-skeleton-v1.json) has SHA-256
`6a5c6eae644dedf88afb68df911f0c3161a969af3815972aa5694479155aa010`.
Its explicit ASCII-sorted dictionary contains 26 straight segments and nine
elliptic arcs. Endpoints preserve line orientation, placement and extent; arc
centers, radii, start angles, signed sweeps and closure preserve curve geometry.
Undirected segments and an unordered primitive multiset deliberately discard
writing direction and pen order. No feature is a letter ID or whole-glyph label.
The 35 components are sufficient for this model, not claimed minimal.

I is a single unbarred vertical; J is an unbarred hook; G has a near-closed arc
and inward horizontal bar; S has two opposed lobes; U has two upper verticals
and a lower semicircle. M and W use half-height central vertices. Q has a closed
oval and lower-right tail. All are versioned choices; changing a font or shape
requires a new schema, not silent feature additions. An individual open arc may
combine with a line to close a glyph, as in D; these are different notions.

The [atlas](../independent/2026-10-22/alphabet-geometry/modeled-uppercase-geometry-001.svg)
was visually inspected. The original independent bundle, auditor and manifest are
preserved under `independent/2026-10-22/alphabet-geometry/`. Our separate encoder
is [alphabet_geometry.py](../experiments/alphabet_geometry.py); generated dense
[arrays and decimal codes](../data/alphabet-features-v1.json) are reproducible with
`python3 experiments/alphabet_geometry.py --write`. That module reads no K4 data.

All 325 unordered letter pairs have different vectors and full codes, with an
explicit first-differing-feature certificate in the
[representation report](../results/ALPHABET-GEOMETRY-001.json). Array, integer and
feature-tree lookups all round-trip all 26 letters. A deterministic tree always
queries the lowest-index distinguishing feature and stops at one remaining glyph;
full codebook membership is checked after traversal. Among 910 one-bit mutations,
12 are valid other glyphs and 898 are rejected, never silently assigned a leaf.
Removing Q's tail correctly yields O; removing R's diagonal yields P.

Ordinary sums collide: 1 gives C/I/O; 2 gives D/G/J/L/P/Q/S/T/V/X;
3 gives A/B/F/H/K/N/R/U/Y/Z; 4 gives E/M/W. To retain all components,
`N=sum(v[i]*2**i)`, index zero least significant, is exactly reversible by integer
division or bit operations. Python integers avoid fixed-width truncation. A future
count vector bounded by M needs a frozen base M+1; binary carries cannot encode
counts above one safely. The codec exhaustively checks 353 small vectors in bases
2, 3 and 4, plus a 100-bit value. Decimal strings keep JSON consumers exact.

Full codes are unique; their residues modulo 26 have only 14 distinct values.
For example O and Z share residue 2. Feature order changes numeric codes and their
ordering, proximity and residues; these are not intrinsic geometry or historical
facts. A reversible identifier alone supplies no cryptographic secrecy.

The frozen follow-up [pilot specification](ALPHABET-GEOMETRY-PILOT-SPEC.md) is
separate from this representation success. No cryptanalytic result is implied by
unique arrays. The theoretical boundaries below were checked from existing cribs,
not discovered by a new search.

## Existing analytical boundaries

These facts are checks of stated equations, not a new cryptanalysis search. Let A
be AZ or KRYPTOS and define the implied additive shift
K_i = index_A(C_i) - index_A(P_i) modulo 26 at confirmed crib positions.

For a literal fixed word W with arbitrary cursor schedule s_i,
C_i=A[(index_A(P_i)+index_A(W[s_i])) mod26]. Its output shift must belong to the
support of W. Concrete witnesses for the three existing words are:

| Alphabet | Word | Position | Required shift | Missing key letter |
| --- | --- | ---: | ---: | --- |
| AZ | KRYPTOS | 22 | 1 | B |
| AZ | PALIMPSEST | 22 | 1 | B |
| AZ | ABSCISSA | 23 | 11 | L |
| KRYPTOS | KRYPTOS | 23 | 10 | D |
| KRYPTOS | PALIMPSEST | 22 | 1 | R |
| KRYPTOS | ABSCISSA | 22 | 1 | R |

This excludes those literal additive-word supports, not every word, added layer,
other arithmetic equation or arbitrary key generator. No scheduling feature can
add a letter absent from the fixed word's support.

A separate model K_(i+1)=K_i+f(phi(P_i)) mod26, where phi is a fixed per-letter
feature array and f is memoryless, also fails. E→A at 22→23 requires shifts
1→11 (increment 10) in AZ, while E→A at 31→32 requires 2→10 (increment 8).
In KRYPTOS the corresponding shifts are 1→10 (increment 9) and 2→19 (increment 17).
The same fixed E features cannot yield two different memoryless increments.
The repeated ordered E,A pair also precludes replacing f by a function solely
of that ordered pair's fixed features. This does not exclude state-dependent,
position-dependent or multi-stage procedures. All facts use existing fixed crib
letters; they are not additional independent evidence.
