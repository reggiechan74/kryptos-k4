# Source-fixed unanchored IPA audit: 24 structures, zero survivors

## Finding

Removing **all** Latin-letter identity anchors still leaves no exact fit in the
frozen family. Of 24 structures, 21 have nonzero modular-cycle residuals and
three force two distinct IPA glyphs to have the same code. Every rejection has
a machine-verifiable certificate in `results.json`.

This is a negative result for this bounded family, **not** a rejection of every
phonetic preprocessing hypothesis, not a decryption, and not proof that the
stipulated transformed positions are the correct positions in a 97-glyph text.
No period beyond 12, transcription variant, shifted crib, transposition, or
language-based optimization was added after the results.

## Exactly what was frozen

- Ciphertext: the canonical 97-character K4 text in `protocol.json`.
- Fit positions 22–34: `iːstnɔːrθiːst` (13 glyphs, 10 segment tokens).
- Check positions 64–74: `bɝːlɪnklɑːk` (11 glyphs, 9 segment tokens).
- Source: the preceding pilot's frozen Cambridge US forms, with stress, spaces,
  syllable dots and delimiters removed, length marks retained. No fresh source
  lookup or pronunciation selection was performed in this audit.
- Alphabet ranks: A–Z or `KRYPTOSABCDEFGHIJLMNQUVWXZ`.
- Periods: 1 through 12, with global zero-based position modulo period.
- Equation: C_i = f(P_i) + k_(i mod p), modulo 26.
- The 14 observed glyphs have arbitrary, shared, pairwise-distinct values in
  Z/26Z. Even i, s, t, n, r, b, l and k have no Latin-identity anchors.

There are exactly 2 × 12 = 24 canonical structures. Reversing the key sign or
changing its phase only renames unrestricted key variables. True Beaufort is
equivalent via negating the entirely free f map, so it is not another test.

The full IPA inventory is larger than 26. This experiment is only a necessary-
condition relaxation on these 14 seen glyphs, not a universal one-letter IPA
codec. An injective arbitrary map on the observed subset was deliberately the
only relaxed assumption.

## Chronology and provenance

`protocol.json` was written and hashed before the first comparison in this
audit. It is a working pre-test freeze, not a repository preregistration commit.
The prior pilot's source choices had already been made with the public crib
lengths known; this is not a blind held-out-source experiment.

Frozen protocol SHA-256:
`53202e5b0708eb3e71380668cca418f6dcc5f1b4812a1bde27cc6aa110def2c8`

The original source bundle is included as `sources/ipa-pilot-bundle.zip`:
`163eb3d44e38c3824b3ffd8f47887601dc3c21915236f9c419cf5a053235c850`

The source bundle preserves the original source audit, source URLs,
normalization, alignment caveats, earlier protocol and replay scripts. Its
historical baseline was a40e69c510f74e4048403c250fc82010281779aa. This audit used
cloud scratch only and did not inspect or modify the user's Mac or repository.

## Exact method

Write q_j = -k_j. Each observation becomes f(g) - q_j = C_i. A bipartite graph
has one node per glyph and one per key phase. Directed steps from f to q have
weight -C_i; reverse steps have weight C_i, all modulo 26.

For each connected component, breadth-first traversal gives a potential for
every node. All equality solutions in that component have the form
potential(node) + t_component. No division modulo 26 is needed.

1. A cycle whose weights sum to a nonzero residue contradicts the equations.
2. Equal potentials for two distinct glyphs in the same component contradict
   injectivity, regardless of that component's shift.
3. Otherwise the remaining exact condition is that the shifted glyph-value
   sets from different components be disjoint. Components and this finite
   constraint representation are preserved in the results, not one selected fit.

The simultaneous shift of every f and q is a free 26-fold gauge. Counting fixes
f(i)=0, solely to choose one representative per gauge orbit. This is not an IPA
or Latin identity anchor. Multiply gauge-fixed counts by 26 for raw f/key
assignments.

To count first-stage solutions without enumerating billions of assignments,
the solver enumerates shifts of multi-glyph components and factors labelled
singleton placements as a falling factorial. Components with rotationally
symmetric value sets retain their multiplicities because the glyphs are
labelled. All requested counts finished exactly; none hit the search bound.

## First-stage counts

Periods 1–6 and 9 fail already on the 13-glyph first window, for both alphabets.
The remaining first-stage gauge-fixed counts, including the compatible key,
are:

| Period | A–Z: 8 fitted glyphs | KRYPTOS: 8 fitted glyphs |
|---:|---:|---:|
| 7 | 14 | 13 |
| 8 | 380 | 380 |
| 10 | 175,560 | 175,560 |
| 11 | 3,862,320 | 3,862,320 |
| 12 | 96,909,120 | 96,909,120 |

The first window has eight observed glyphs. Adding the six as-yet-unseen
Berlin glyphs without using any Berlin ciphertext multiplies each count by
18P6 = 13,366,080. These are unconstrained alphabet extensions, not predictions.
The results record both counts explicitly; they are never conflated.

The eight-glyph component sizes for p=7,8,10,11,12 are respectively
[4,4], [6,1,1], [4,1,1,1,1], [2,2,1,1,1,1], and [2,1,1,1,1,1,1].

## What Berlin does and does not predict

Before observing any Berlin ciphertext, only these individual outputs are
uniquely forced by the first-stage solution set:

| Alphabet | Period | Position | Forced ciphertext | Actual ciphertext |
|---|---:|---:|---|---|
| A–Z | 8 | 66 | I | P |
| A–Z | 8 | 73 | L | P |
| A–Z | 10 | 73 | L | P |
| KRYPTOS | 8 | 66 | I | P |
| KRYPTOS | 8 | 73 | O | P |
| KRYPTOS | 10 | 73 | L | P |

All six forced predictions fail. For each first-stage survivor and each Berlin
position, the program tests all 26 possible ciphertext residues against the
entire first-stage injective solution set. `results.json` preserves the exact
allowed residue domains, proving there are no other individually forced outputs.

The other positions are still constrained, not arbitrarily unrestricted:
injectivity can rule out some residue choices without forcing one output.
In particular, the known repeated glyphs at positions 66, 69 and 73 sometimes
link separately free first-stage components. Six new glyphs b, ɝ, l, ɪ, k and ɑ
occur eight times in Berlin and require new code values. Fitting their values is
never called a prediction. Joint repetition and injectivity constraints can
reject a block even when each position separately permits its observed value.
This is exactly what happens at p11 and p12: their positions are individually
compatible, but the joint block is not.

## Full-block classification and explicit witnesses

- A–Z p1–10 and p12: inconsistent modular cycles.
- A–Z p11: cycle-consistent, but the map cannot be injective.
- KRYPTOS p1–10: inconsistent modular cycles.
- KRYPTOS p11 and p12: cycle-consistent, but the map cannot be injective.

Thus 21 cycle rejections plus 3 injectivity rejections, zero full-block solutions.
No cross-component placement search is required for the final rejection.

For the three cycle-consistent structures, short supplementary witnesses use
distinct single-segment symbols rather than only vowel/length-mark details.
In the following, C_j means the zero-based numeric rank of the ciphertext at
one-based position j in the specified alphabet:

- A–Z p11:
  f(n) - f(ɪ) = -C68+C24-C33+C66-C23+C34-C25+C69
  = -19+17-18+15-11+18-21+19 = 0 modulo 26.
  Therefore f(ɪ)=f(n), forbidden for distinct glyphs.
- KRYPTOS p11:
  f(t) - f(b) = -C64+C31-C22+C66-C23+C34
  = -19+13-12+3-17+6 = -26 = 0 modulo 26.
  Therefore f(b)=f(t), forbidden.
- KRYPTOS p12:
  f(θ) - f(b) = -C64+C28-C66+C30
  = -19+3-3+19 = 0 modulo 26.
  Therefore f(b)=f(θ), forbidden.

Each alternating pair uses the same phase under its specified period; the
complete directed paths are machine-checked. These supplementary witness pairs
were chosen for explanatory clarity after the classifications, not as new models.
The solver's original certificates are also retained unchanged.

## Validation and replay

Run with Python 3.10+ and no third-party dependencies:

```
python3 replay.py
```

This regenerates `results.json`, prints all 24 classifications, and reruns:

- 24 deterministic synthetic positive controls, one per canonical structure,
  each using all 14 glyphs, a randomly generated injective map, and a random key.
- 24 additional positive checks using exactly the two real window geometries,
  with synthetically generated ciphertext and the same random maps/keys.
- All 26 global shifts for each synthetic structure, checking equation and
  injectivity preservation and the unique f(i)=0 representative.
- True-Beaufort/free-map equivalence on all synthetic observations.
- 225 independent tiny-ring exhaustive comparisons over moduli 3,4,5,6, using
  a direct map-and-key enumerator with no graph or singleton-factorization code.
  Cases include empty constraints, isolated glyphs, unseen key phases, composite
  moduli, synthetic consistent data and random inconsistent data.
- Verification of every reported certificate against the original equations,
  plus checks that corrupted certificate residues are rejected.
- Exact single-position Berlin domains and exact first-stage counts.

All checks pass. RNG seeds and full synthetic inputs are saved in the results.
No empirical success rate or statistical evidence for IPA is inferred from
these controls; they validate the implementation only.

The conclusion is complete for the frozen 24 structures and stops there.
