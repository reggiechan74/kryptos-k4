# Frozen K3 and 24-sector route families: bounded negatives

22 October 2026. **All 374 newly tested structures contradict confirmed crib
letters. No candidate, decoded plaintext or solution.** Another 16 structures
were exact equivalents of already rejected unrestricted-key models and were
recorded rather than rerun. The three frozen families are complete; no added
width, direction, period, alphabet or layer was tested after these outcomes.

## Reproducible scope and chronology

The active checkout was clean at `e83624f2d4eda143300f59e198f78acfefa41b98`, on
`research/dynamic-key-20261022`. Ledgers, prior tests and saved route results were
inspected before changes. No applicable AGENTS.md was found. Existing work,
including the geometry audit and earlier experiments, was preserved. No remote
push, public Site edit, optical claim or third-party executable was involved.

[Specification](specifications/K3-CLOCK-ROUTES-001.json):
`dcb246cdd997ecd2f0b4f3a4c536ca65d8a47a14`.
Implementation and controls:
`9ea6b35f46a43374839096a7ac39594df94656ca`.
The one actual run completed afterward in **0.071886 seconds**, under its
30-second cap. Existing atomic snapshot infrastructure verifies the unchanged
specification, ancestry and all consulted bytes against that implementation
commit. Standard library, one local process, no dictionary or key brute force.

The same verified 97 letters and 24 plaintext positions were used. Known cribs
remain at one-based 22–34 EASTNORTHEAST and 64–74 BERLINCLOCK. Alphabet is only
`KRYPTOSABCDEFGHIJLMNQUVWXZ`; all modular cipher layers use addition modulo 26.
Neither historical public crib block is independently obtained validation text.

| Family | Raw structures | Exact old equivalents skipped | New structures tested | Compatible |
| --- | ---: | ---: | ---: | ---: |
| F1: K3 composite route + one periodic layer | 4 | 0 | 4 | 0 |
| F2: periodic layer / K3 route / periodic layer | 2 | 0 | 2 | 0 |
| F3: 24-sector route + one periodic layer | 384 | 16 | 368 | 0 |
| Total | 390 | 16 | 374 | 0 |

All three families are fully contradicted. **No null simulations were needed
or run, and no p-value is reported.** Partial modal-key agreement is retained
only as bookkeeping; it does not override exact contradictions or motivate
additional parameter choices.

## Route control and complete prior-domain comparison

Define U_w: row-major fill with width w, no padding, then read columns
left-to-right, bottom-to-top within each column, skipping absent cells. Define
T = U_14 after U_42, with T(x)[j] = x[pi(j)].

Before K4 constraints were evaluated, an independently coded matrix-cell oracle
and a position-index implementation both confirmed:

- T reproduces **every one of the 336 canonical K3 ciphertext letters** from the
  fixed published plaintext; the external final question mark is excluded.
- The complete position permutation equals the repository's verified K3
  permutation, and the inverse restores all 336 plaintext letters.
- This is a verified computational equivalent, not a claim to have observed
  every historical construction step.

At length 97, the composite permutation's SHA-256 (JSON list serialization) is
`6aacb561bfd56fb6875c8c4e7e7226c696bc4583a96d07f5ac60d32465edf9ec`.
It is absent from the existing 66-route catalogue. The saved ROUTE-001 catalogue
was compared byte-for-value to the current generator; no drift was accepted.

Equivalence was checked on **both the complete source permutation and the
canonical output-key-phase partition**. A skip also requires the earlier
alphabet, addition equation, key period, layer order and unrestricted periodic
key domain to be covered. The earlier ROUTE-001 experiment derived arbitrary
phase constraints at periods 1–16 in both orders for KRYPTOS and all three
arithmetic equations. It was not limited to PALIMPSEST or ABSCISSA. Saved
survivor records and the earlier specification confirm the skipped exact
plus/KRYPTOS/period-8-or-10 cases were rejected. No sandwich model was skipped
on the basis of a one-layer result.

F3 has 96 distinct route permutations: start s=0..23, direction +1/-1, and
ascending/descending row order. Only these four routes match old ones:

| Start s | Direction | Rows within column | Earlier route ID | Skipped cases |
| ---: | ---: | --- | --- | ---: |
| 0 | +1 | ascending | R036 | 4 |
| 0 | +1 | descending | R040 | 4 |
| 23 | -1 | ascending | R038 | 4 |
| 23 | -1 | descending | R042 | 4 |

For each route, four cases are the two periods and two cipher-layer orders.
The remaining 92 routes give 368 new distinct structures. No additional exact
aliases were found after phase-partition canonicalization. Full permutations,
case descriptors and every prior-model skip receipt are saved in the result.
The old 282 high-period identity-route fits remain vacuous and irrelevant here.

## F1: four single-key composite-route cases

Two layer orders and periods m in {8,10}:

```
C = T(V_k(P))
C = V_k(T(P))
```

For a crib at plaintext position i=pi(j), a required key value is
idx(C[j])-idx(P[i]) mod 26, at slot i mod m in the first order or j mod m in
the second. Key symbols are unrestricted periodic residues. A first observation
at a slot fixes a parameter; a repeated incompatible requirement rejects every
key in that structure. Missing phases are never filled arbitrarily.

All four are already contradicted within EASTNORTHEAST alone:

| Period | Order | Key variables | Occupied training slots | Training equality checks | First conflicting plaintext positions | Required values |
| ---: | --- | ---: | ---: | ---: | --- | --- |
| 8 | substitution then route | 8 | 8 | 5 | 22,30 | 15,3 at slot 5 |
| 8 | route then substitution | 8 | 8 | 5 | 22,26 | 15,4 at slot 2 |
| 10 | substitution then route | 10 | 10 | 3 | 22,32 | 15,25 at slot 1 |
| 10 | route then substitution | 10 | 10 | 3 | 22,27 | 15,24 at slot 2 |

No training survivor exists, so no Berlin predictions are interpreted. The
all-crib equality-check counts are 16 for period 8 and 14 for period 10. Zero
compatible keys; no plaintext output was completed. The maximum fitted modal
agreement, 11/24, is a descriptive partial score only.

## F2: two sandwich cases, with component freedom explicit

The two period pairs are (m,n)=(8,10) and (10,8):

```
C = V_b(T(V_a(P)))
a[i mod m] + b[j mod n] = idx(C[j]) - idx(P[i]) mod 26
```

There are **18 key vertices**, including any isolated vertices. Put x_A=a and
x_B=-b; each crib edge constrains a potential difference x_A-x_B. Tree propagation
chooses a representative zero at each component root, while retaining a symbolic
free offset per component. Only within-component differences are predictions.
A nonzero cycle residual is an exact contradiction modulo 26; it requires no
field division or approximate numerical solver.

For a consistent crib graph with c components, there would be 26^c key
assignments. If the full 97-position graph has d components, those assignments
would produce 26^(c-d) distinct full plaintexts. This separates harmless gauge
freedom from plaintext-relevant offsets. The formulas are conditional on
consistency; the actual inconsistent cases have **zero** assignments/messages.

| Period pair | c_train | Training cycle checks | c_all24 | c_full | Relative offsets after training | Individually predictable Berlin edges | Joint independent held-out checks | Failed all-crib fundamental cycles | Actual compatible keys/plaintexts |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | --- |
| (8,10) | 5 | 0 | 1 | 1 | 4 | position 64: fails | 7 | 7 of 7 | 0 / 0 |
| (10,8) | 5 | 0 | 1 | 1 | 4 | positions 69,70: both fail | 7 | 6 of 7 | 0 / 0 |

Both first-crib fits are **vacuous consistency tests**: thirteen forest edges
fix thirteen relative parameters without a single cycle check. Each training
family has 26^5 key assignments and 26^4 distinct full plaintexts (456,976), not
one predicted English message. Setting component offsets to zero does not make
cross-component predictions legitimate.

Among the eleven Berlin edges, four component joins spend the four remaining
relative offsets; the joint independent compatibility checks are
11-(c_train-c_all24)=7, not eleven independent predictions. Only the one/two
edges whose endpoints were connected in the frozen training graph are individually
predictable. The others are explicitly unknown in those prediction records.
All of the individually predictable edges fail, and the complete crib graph
also has cycle contradictions.

The topological exponent c_all24-c_full is zero for both all-crib graphs, but
that does **not** imply a unique valid plaintext: both graphs are inconsistent,
so actual key and plaintext counts are zero. Representative forest potentials
in the saved contradictory records exist only to certify cycle residuals; they
are not a compatible key assignment. No completed plaintext or arbitrary
component-offset guess was emitted.

Example independently verified cycle certificates:

- (8,10): tree-path crib positions 70,65,73 imply delta 20 for the edge at
  position 22, which requires 15. Residual **5 mod 26**.
- (10,8): tree-path crib positions 72,27,67,64,34,66,26 imply delta 17 for the
  edge at position 22, which requires 15. Residual **2 mod 26**.

These are algebraic checks, not claims of statistical independence between
public clues. The saved certificate lists every oriented edge and its signed
contribution so the contradiction can be checked without trusting the solver.

## F3: the bounded 24-sector hypothesis

Original position i=24*r+c gives four full rows and one extra cell. Read columns
in the order (s+direction*q) mod 24 for q=0..23; read occupied rows ascending or
descending within each column. All 97 letters are retained. Combine each route
with the same unrestricted period-8 or period-10 additive key in either layer
order. No null padding, repaired positions or extra directions were introduced.

After the 16 exact prior skips, **all 368 new structures are rejected**, already
within EASTNORTHEAST. All 24 known letters were nevertheless checked for every
structure and the first exact slot contradiction is retained. Maximum fitted
modal agreement is 13/24; it is not candidate evidence. No complete key/plaintext
was manufactured and no best-looking partial English was selected.

The World Clock's physical 24 sectors motivate only the number 24. The ragged
97-cell layout, starts, traversal directions and cipher composition are our
specified hypotheses, not independently supplied cipher instructions.

## Sources and evidence limits

Sources read through web text extraction on 22 October 2026:

- [CIA sculpture page](https://www.cia.gov/legacy/headquarters/kryptos-sculpture/)
  provides the panel transcript and KRYPTOS tableau. The verified local fixtures
  remain unchanged; the K3 control compares complete strings/permutations.
- [Official Berlin World Clock page](https://www.berlin.de/en/attractions-and-sights/3561749-3104052-world-clock.en.html)
  describes 24 corners representing time zones. It does not prescribe a cipher
  route or establish any proposed key.
- [Scientific American's contemporary report](https://www.scientificamerican.com/article/cia-kryptos-puzzle-creator-releases-final-clues/),
  dated 12 November 2025, attributes the World Clock clarification to Sanborn's
  event/letter. The linked letter scan was **not inspected**. The article's
  erroneous 79-letter description is not used; K4 remains the verified 97-letter
  fixture. Archival plaintext recovery is not a published cryptanalytic method.

These sources motivate bounded tests; they do not substantiate worldwide novelty,
artist use of a particular route or a solution. Unsurveyed monument geometry and
heading supply no optical constraints to this experiment. The public Site was
not changed.

## Controls, validation and next decision

Controls pass before the actual run:

- Full 336-letter K3 known answer, exact position permutation, inverse and a
  separately implemented explicit matrix oracle; complete baseline/K1–K3 controls.
- 372 planted single-key recoveries and 372 deliberate repeated-slot mutations
  rejected, covering every newly tested F1/F3 structure.
- Both planted sandwich inverses, cycle-mutation rejections, and frozen-training
  prediction checks without crossing free component offsets.
- Five tiny graph cases exhaust 1,215 base-3 key assignments and compare both
  key-assignment counts and distinct full-message offset-image counts.
- Isolated vertices, parallel-edge contradictions, relative-offset joins, full
  gauge equivalence, hand-indexed layer-order examples and expired deadlines.

Independent saved-artifact tests recompute all 372 slot contradiction witnesses,
both cycle sums, component counts, unknown cross-component predictions, all skip
receipts with the complete prior model domain, hashes and chronology. The
**187-test full suite passes in 8.941 seconds**. No actual experiment was rerun
by that suite. [Validation receipt](../results/K3-CLOCK-ROUTES-VALIDATION.json).

This batch stops. There is no basis here to add more clock starts, arbitrary
phases, widths or layers. **Later correction, 23 October 2026:** that four-case affine-digraph recipe is
[analytically excluded](AFFINE-DIGRAPH-PARITY-BOUNDARY.md), without a key search.
The following proposal is historical. A next computational candidate was the separately
recorded low-evidence affine-digraph proposal, **only after an exact prior-art
check and a new frozen specification**. It should begin with complete-pair
constraints and an explicit odd-edge rule, followed by the untouched-by-current-fit
Berlin equations and full 24-position/97-letter verification. This is a proposed
next preflight, not a new experiment or a claimed lead.

## Reproduce

```sh
python3 experiments/k3_clock_routes.py --spec-commit dcb246cdd997ecd2f0b4f3a4c536ca65d8a47a14
python3 -m unittest discover -s tests -v
```

The runner verifies committed input/code bytes and writes a fresh atomic snapshot.
The recorded code commit above identifies the exact tested implementation. To
audit this result without repeating any search, run `test_k3_clock_artifacts.py`.

[Full result, routes, constraints and graph certificates](../results/k3-clock-routes-001-runs/20261022T193238Z-99bf9337176c469e9d7742f2a21f2aca/K3-CLOCK-ROUTES-001.json),
[atomic manifest](../results/k3-clock-routes-001-runs/20261022T193238Z-99bf9337176c469e9d7742f2a21f2aca/manifest.json).

## Independent direct contradictions — 22 October 2026, later cross-check

The parent's independent reviewer supplied simpler two-edge certificates, which
were compared to our unchanged saved equations and match exactly. Plaintext and
ciphertext positions below are one-based; key residues are zero-based:

- (8,10): P32=A routes to C44=S, requiring **a7+b3=25**; P64=B routes to
  C94=K requires **the same a7+b3=18**. Impossible modulo 26.
- (10,8): P29=T routes to C2=B, requiring **a8+b1=4**; P69=N routes to
  C66=P requires **the same a8+b1=10**. Impossible.
- Also (10,8): P30=H routes to C16=L, requiring **a9+b7=3**; P70=C routes
  to C80=X requires **the same a9+b7=15**. Impossible.

These pairs expose the failures without trusting graph traversal or cycle-basis
choice. They agree with the previously saved longer cycle certificates. The
reviewer independently reports all six K3-derived negatives and 384 raw clock
negatives/positive controls; these are cross-checks, not additional novel search
counts. Our sixteen prior-equivalent skips remain unchanged. A separate later
[occupied-cell pilot](OCCUPIED-CELL-FINDINGS.md) tests 288 additional fixed branches.
