# Finite discovery-set triage: middle batch

Reviewed 2026-10-31. Current hypothesis/prior-art ledgers read first. No downloaded code executed, K4 search run, author contacted, schedule created or remote state changed.

## Coverage
15 assigned discovery hits: **8 implemented K4 projects, 3 unsupported/retracted solution claims, 2 irrelevant learning-only projects, 1 documentation-only handoff, 1 empty/unavailable repository**. Fourteen nonempty distinct repositories; none declares itself a fork. Complete recursive trees were read, and cross-comparison found no identical Python/Rust/C/C++/Go blobs *within this batch*. That is not proof of independent origin; parent must cross-compare other batches. All 14 nonempty repositories have immutable HEAD pins in triage-middle.json.

Source/model inspection includes the eight implemented projects (Flavia supplies executable Python embedded in Markdown), two unsupported claims, plus the irrelevant Rust example. **Three newly inspected repositories have separately named result artifacts:** Keith Adler, claudlos, aciderix. Expected outputs and embedded narrative tables are not separate run receipts. No experiment independently reproduced.

## Proposed additive external-register records (publisher assigns permanent IDs)

### Two-key periodic sums — keithadler/kryptos
- Pin: `714e7c252165e106b2b827eacab156c4005f2b90`.
- Sources: `layer2.py`, `results/17_layer_two.txt`, `SEARCH.md`.
- Model: same AZ or KRYPTOS coordinate alphabet; effective key u[i mod a]+v[i mod b], 1≤a≤b≤26; Vigenère and Beaufort. Linear consistency checked modulo 2 and 13. Cases with zero redundancy are explicitly skipped.
- Result receipt: **932 testable combinations, TWO consistent cases**, both KRYPTOS Beaufort: lengths 12+15 and 9+19; each one redundant constraint. This is not a universal double-encryption exclusion. Broader README wording “applied twice ruled out” needs this correction.
- Overlap: periodic/composite-key families already attempted. Not a new hypothesis.

### Projection/overlay keys and decoded key chains — ZeroDay-Labz/kryptos-k4
- Pin: `854534543a93ddf2534758b620ae05cb36dd0a04`.
- Source: `k4/projection.py`, `k4/chain.py`; results embedded in `docs/RESULTS.md`.
- Affine grid key: column=round(scale×column+offset), row=row+shift+round(shear×column). Scale −3..3 by .02 excluding |scale|<.2, offset −40..70 by .25, shear −.5...5 by .1, row shift −30..5; tableau and cipher-side grids, complete coverage of all 24 crib cells required. Documentation reports 1,699,625 placements×16 arithmetic/alphabet settings, best 10/24. Overlay source implements eight orientations and row/column offsets −40..40. These are numerical model sweeps, **not measured sculpture geometry**.
- Curved warp code considers order-preserving mappings within a tableau row via LIS; reported best 8/13. It chooses first/last repeated-letter column placements, not arbitrary choices at every position.
- Chains: readable source X decrypted by a repeating key to form a running key; third-level and feedback variants. Source includes **MIN_EQ=6** for level two, **MIN_EQ3=8** for level three and default feedback minimum five. Low-redundancy cases are omitted; zero retained candidates cannot exclude them.
- Also important documentation correction: larger columnar widths 12–15 results retain ≥9, ≥10 or ≥11 equalities, not all possible period cells. Do not import the README's broad “none” as exact universal elimination.
- Already attempted physical key extraction/chained keys; no new mechanism admitted.

### Fragment diagnostics, not full Gromark elimination — malak333/kryptos-k4
- Pin: `de74e803ca17ad16227f834b94f818f02387f485`.
- Source: `src/analysis.rs`, `src/routes.rs`, `src/hypotheses.rs`; `experiments/STOPPED_LANES.md`.
- Derives additive/subtractive/Beaufort crib fragments on three fixed alphabets. “Gromark” screen actually checks **adjacent** fragment triples (a+b) mod10=c mod10, not a general Gromark primer recurrence.
- Routes apply to *known key fragments*, not a 97-letter cipher: identity, reversal, rectangular row-to-column widths7/13; incompatible fragment lengths skipped without padding. Seeded shuffles compare diagnostics. Code explicitly does not promote candidates.
- Stopped-lane document reports 37 source-backed observation archives, all nonsignificant after archive-surface correction; raw minimum .0436 becomes corrected1.0. This is documented evidence, not separately audited archive results.
- Avoid renaming this as novel recurrence or route work; no precise novel unrun mechanism in inspected hypothesis list.

### One free alphabet with finite Gromark/running-key sources — tylerj-spec/kryptos-k4
- Pin: `c0e2a6847d0f7a505ccfa3bea2b0c58a5ccf2f3c`.
- Sources: `r40/PREREGISTRATION.md`, `r40/sealed/whole_family.cpp`, `HANDOFF.md`.
- R40 any plaintext alphabet; seven fixed cipher alphabets (AZ,KRYPTOS,PALIMPSEST-prefix,ABSCISSA-prefix,and three ACA constructions), two effective signs. Chain addition k[i]=k[i-b]+k[i-b+1] modbase: base 10 primers of length 5/6/7 and base 26 length 5, every primer; Carter and K1–K3 running texts in both directions, AZ/KRYPTOS numbering, every offset.
- Code enumerates and checks equality-pattern equivalence of all 24 known plaintext letters and y=CA^-1(C)±key, a necessary and sufficient in-place free-plaintext-alphabet constraint. Handoff reports **337,634,136 settings, zero consistent**, and 12 plants passing; receipt itself not located/read in this finite pass, so outcome remains **documented**, not independently reproduced.
- R41 post-substitution K3-style routes and R42 free cipher alphabet are documentation-only here. Handoff distinguishes R42 exact checks from failed blind recovery gate (4/6).
- Proposed word-level moves/beam word segmentation for two free alphabets are solver improvements to already attempted models, **not eligible new cipher hypotheses**.

### Bounded SAT toolkit and forced crib interpolation — claudlos/Kryptos
- Pin: `c9366802759f9d3185c2a2bedb8d4e2dd41bc400`.
- Sources: `strategy16_sat_elimination.py`, selected generator/model lines of `strategy40_mathematical_key_generation.py`, named `runs/mathematical_key_generation.json`.
- SAT driver: AZ Vigenère/Beaufort periods 1–30; pure columnar widths 2–15 (5-second Z3 timeout; no-Z3 fallback enumerates only≤10); fixed listed primers for autokey; five fixed 5×5 squares and periods 5–10; Vigenère-columnar periods3/5/7 and widths3–7. Unknown/timeouts explicitly retained, not negatives.
- Mathematical-key receipt: 3435 attempts, 27 retained candidates; every retained one is an **interpolated/forced-fill crib fit**, not independent discovery. Code deliberately inserts crib-derived key positions. Fibonacci/Lucas/coordinate/prime/positional candidates are finite generated dictionaries, not full family exclusions.
- No acceptance of dashboard counts as independent operators or solved result.

### Lag-seven autokey in finite abelian groups — aciderix/kryptos-research-handoff
- Pin: `6b82bd5364b6fea78b6ef3cfd73fafaf85ac3462`.
- Sources: `audits/autocle_groupes_2026_09_25/{README.md,t36_autocle_groupes.py,results_t36.txt}`.
- Shared injective map σ from26 letters into 23 explicitly listed abelian groups with orders26–36, including Z3³, Z2⁵ and Z6×Z6. Lag7 plaintext feedback, three signs (one for exponent-two group), free offset d. Eliminates intermediate plaintext by17 chain equations; relaxes intermediate values to arbitrary group elements. CP-SAT maximizes satisfied equations; 30s default and explicit optimality/status fields.
- Exact component moduli: (26), (27), (3,9), (3,3,3), (28), (2,14), (29), (30), (31), (32), (2,16), (4,8), (2,2,8), (2,4,4), (2,2,2,4), (2,2,2,2,2), (33), (34), (35), (36), (2,18), (3,12), (6,6). Order26 is cyclic up to relabelling; Z5×Z6 is an alias of Z30, not another case.
- Variables are created for letters occurring in the17 equations, with coordinate bounds, mixed-radix indices and AllDifferent. A partial injection extends to 26 letters because each group has at least26 elements. One letter is fixed to zero using translation symmetry with free d. There is **no projection back to26**. The forward image need not be closed; intermediate plaintext is deliberately allowed outside that image. Thus a proved UNSAT in this weak supermodel excludes its exact shared-map model, but a satisfying relaxed assignment would not prove valid plaintext.
- Named receipt: **all 67 K4 cases record optimal minimum 1 or 2 violated equations**. Thus author reports bounded relaxed-model infeasibility, not arbitrary-group/all-lag exclusion. Many English plant generations fail because26-letter image is not closed in larger groups; separate README discusses non-English controls, not source-inspected here. No independent solver replay.
- Grid-coordinate, five-bit XOR and alternate-base aliases are already prior art. Separate σ/τ mapping mentioned in another file was not inspected; do not claim excluded.

### Explicit elementary contradictions — FlaviaOrtiz307/k4-evidence-gap
- Pin: `559daaa6d4348285423a4ee7120c02f0a08d16ea`.
- Source: `K4-Verified-Negative-  Results.md`, including embedded Python.
- Direct AZ periodic Vigenère periods 19/20/21/24/42; expected conflicting crib-pair counts 7/11/11/5/11. Monoalphabetic F→E/O contradiction; all 26 ciphertext letters against a strict 25-symbol output alphabet. Explicitly not arbitrary preprocessing/fractionation exclusion.
- Already local analytical territory. Expected output is not an observed run receipt.

### Mengenlehreuhr weighted lamp-cycle model — LazaUK/AIFoundry-GPT5-KryptosCIA
- Pin: `6fd51a31708df580f513d98c736ac6917bf305a6`.
- Source: `Kryptos_VariantA.py`; B/C/D README descriptions only.
- VariantA:23/24 lamp cyclic mask, optional seconds/reversed rows/snaking; weighted row/color/quarter, affine lamp-position factor and phase.120000 random samples, seed 1337, eight thematic Vigenère keys (nonletters stripped).
- The two advertised stage orders commute as additive subtractions, so they are duplicate operators. Samples are not exhaustive; no completion receipt found in tree. This documents implementation, not completed negative.
- Generic clock-mask/periodic composite family already attempted, no novelty claim.

## Other dispositions
- **rbonifacino**: two documents, proposed running key derived as C−P, header/null reinterpretation and later city-change provenance narrative. No independently frozen source-to-key construction established. Unsupported candidate, not accepted solution.
- **slightofmind369**: explicitly retracted in README; ordinary Vigenère implementation uses a malformed/truncated noncanonical ciphertext. Do not treat as a valid K4 test.
- **Sofia Martins**: `k4_validation.py` literally calls tests simulated, prints success and increments counters without checking ciphertext. Claimed crib mappings/positions are inconsistent. Unsupported solution claim.
- **soma2-stack**: documentation-only inherited conversation.942 TOKIO→57973 route cases and935 unfinished double-route cases need original source/hash reconstruction. Not reproducible newly tested coverage; unfinished attempted route work is not a new hypothesis.
- **anantnrg** and **chillhackr**: learning-only substitution/K1–K2 code, no K4 investigation implemented in inspected trees.
- **polancan**: public metadata, size0; contents API explicitly returns “This repository is empty,” no main branch. No immutable source commit exists to inspect.

## Actionable decision
Expand the prior-art register with bounded records above before proposing alternate-base autokey, chained keys, projection masks or free-alphabet running-key models. **No genuinely new, precisely specified untried cipher lead qualifies from this batch.** The only concrete future algorithm proposal found (Tyler's word-level moves) improves an already attempted model and is ineligible under current novelty rules. None of these reads authorizes a new experiment.


## Focused source-only validation: T36 zero gauge
The zero gauge is valid **because d is free**, not because translations alone preserve additive autokey. For σ′(x)=σ(x)+g, set d′=d−g in VIG and d′=d+g in BEAU/VAR. All component d variables span the entire cyclic component.

For the actual derived equation Σ co(x)σ(x)+cd·d=0, put m=(b−a)/7 and S=Σ over t=1..m of (−1)^(m−t). VIG has cd=S and Σco=1−(−1)^m−S=S (0 for even m,1 for odd m); hence translation changes its left side by Sg−Sg=0. BEAU has Σco=m and cd=−m; VAR has Σco=−m and cd=m; the d′=d+g choice cancels both. Repeated-letter coefficient aggregation does not alter these sums. Translation preserves injectivity and the transformed image's membership relations. Choosing g=−σ(first constrained letter) makes its mixed-radix index zero without losing any feasible assignment or changing the number of satisfied equations. This is a source-level algebraic check, not a solver replay.

## Cross-batch provenance reconciliation
The parent's complete-tree blob comparison finds **261 identical implementation blobs** between aciderix primary `audits/*` and ActiveTK's clearly vendored `refs/aciderix/*`, including T36 (`74ec911f7b1adf7ddef6c2ce752968e2a6d6c174`). Keep these as distinct projects with different native programs, but count imported T36 **once**, attributed to aciderix, not as independent ActiveTK reproduction. The within-batch zero-shared-blob result above did not compare ActiveTK and must not imply worldwide independence.
