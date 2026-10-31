# Study 059 — short-primer feedback before unknown column order

Status: pre-freeze proposal. No blind fixture generation until parent review, measured development cost, and independent preflight PASS. No target evaluation until audited blind gates and separate parent approval.

## Selection and prior coverage

Q-03 is selected from the reconciled ledger after exact bounded exclusions in 057 and 058. Those studies addressed periodic arithmetic with columnar transposition in each order, not feedback. Earlier direct autokey tests explicitly exclude unknown transposition/composite models. This study preserves the same route bounds but changes the key generator under explicit equations. No historical attribution or new cryptanalytic invention is asserted.

## Exact model

Length n=97. Plaintext alphabet A and intermediate-ciphertext alphabet B independently use ordinary A–Z or KRYPTOSABCDEFGHIJLMNQUVWXZ. Sign s is +1 or −1. Let x_i=index_A(P_i), y_i=index_B(D_i), and arbitrary primer z have length L in 1–8. For i<L, y_i=s*x_i+z_i modulo 26. Thereafter choose exactly one feedback mode:

- Plaintext feedback: y_i=s*x_i+x_(i−L) modulo 26.
- Intermediate-ciphertext feedback: y_i=s*x_i+y_(i−L) modulo 26.

Fill D left to right into unpadded rows of width w in 6–9. Emit physical columns in an arbitrary permutation, each top to bottom. Fixed initial alignment, no padding, reverse, resets, errors, extra stages, other alphabets, output-ciphertext feedback, subtractive feedback or variable lag. In particular y=x−feedback is a distinct untested convention: arbitrary primer negation does not negate the later feedback stream. Parent explicitly retained this eight-convention, feedback-coefficient +1 pilot before freeze; it is not exhaustion of all autokey equations.

Eight alphabet-role/sign conventions × two feedback modes × eight primer lengths × 408,960 routes gives 52,346,880 descriptive route/length/convention/feedback trials in an exhaustive reference. These are not necessarily distinct encryption operators. No per-position substitution-map canonicalization from periodic models is valid for feedback; the functions couple positions. Keep raw symbolic description counts and explicitly withhold distinct operator counts. Equal physical operators across model descriptions may overlap. A repeated primer does not by itself make a different feedback lag equivalent.

## Exact primer cylinders and plaintext identifiability

After undoing a fixed route, all y_i are known. In plaintext feedback, each chain satisfies x_i=a_i*z_(i mod L)+b_i with a_i=±1; a clue uniquely constrains its residue. The 13 consecutive crib positions cover all L≤8, so every primer slot is fixed in this primary domain. In ciphertext feedback, x_i=s*(y_i−y_(i−L)) for i≥L independently of z. All public clues are at i≥21, so every primer slot is free. Initial plaintext letters vary bijectively with those slots.

Represent a complete family by convention, feedback mode, width, lag, column order and a primer vector whose unconstrained entries are −1. The compatible set is the union of these exact cylinders. Empty union means UNSAT_COMPLETE. If any cylinder has a free slot, the plaintext projection is MULTIPLE; provide two explicit different plaintext witnesses. If every cylinder is fixed, decrypt and compare complete plaintexts to classify UNIQUE versus MULTIPLE. Do not sum cylinder volumes as an exact union count. Report the maximum individual volume as a lower bound and their sum as an upper bound, improved by distinct representatives where available. No English text selection fills free slots.

## Engines and controls

Production uses prefix column-placement pruning with only necessary feedback constraints, followed by exact primer inference. The independent C++ reference constructs each literal ragged row matrix and tests the equations directly. Independent Python complete-key enumeration proves tiny solution-set and projection correctness. Every returned representative and alternative free-slot witness must exactly re-encrypt and satisfy all clues.

Tiny proof: all 256 four-symbol-alphabet ciphertexts of length 4, three clue masks (768 total cases), widths 2–3, lags 1–2, both feedback modes and all eight alphabet-role/sign conventions. Fully expand tiny primer cylinders and compare exact primitive-description and plaintext sets to a brute-force all-key oracle. Include empty, unique and multiple cases. Additional full-alphabet development examples cover all conventions, feedback modes and low/high lags before freezing.

Blind 600 inputs, approved before freeze after measured reference cost of about 1.97 CPU seconds per development input:
- 512 positive cells: all eight conventions × two feedback modes × four widths × eight lags. Uniform versus literal-crib plaintext classes are deterministically balanced by (feedback + convention + width + length) parity (256 each), with both classes present within each convention/feedback/width combination across lags.
- 32 diagnostic plants: each convention/feedback pair gets one zero primer at L=1/w=6 and one alternating [2,7] repeated primer at L=8/w=9, both with literal crib values. These are degeneracy checks, not assumed lag aliases.
- 56 independent uniformly random ciphertext controls, 28 with independent uniform clue values and 28 with the literal clue values.

All input plaintexts outside literal clue positions are IID uniform letters, not English. Mask is zero-based 21:34 and 63:74. The literal stress letters are EASTNORTHEAST and BERLINCLOCK. Independent fixture author uses fresh 256-bit secret entropy after final code/protocol freeze, records the seed and answers separately, shuffles opaque IDs, and never filters by solvability, ambiguity or runtime. Solvers receive only ciphertext and clues, not generating parameters. Both result files are sealed before opening answers. No language model, key corpus or paid checker is used.

## Frozen target gates

1. Independent tiny complete sets and plaintext projections agree, including expanded free primers and cross-description overlap cases.
2. Every blind input completes under resource caps; failures remain inconclusive and are retained.
3. Exact symbolic cylinder sets and empty/unique/multiple projections agree independently for every blind input.
4. Every planted primitive description is contained in its returned cylinder. All ciphertext-feedback plants are classified MULTIPLE; all declared primer freedoms agree with independent equations.
5. At most one of 56 independent random-ciphertext controls has any compatible cylinder.
6. Independent audit verifies all frozen files, synthetic seed replay, resource receipts, novelty limits, witness re-encryption, gates and no discarded cases.

Unique-recovery rates are descriptive, stratified by feedback mode and clue class. They are not a go/no-go gate because the ciphertext-feedback arm is intrinsically non-identifiable under these cribs. This objective is exact feasibility and ambiguity characterization. A negative result can exclude the bounded model; a compatible family is not an identified solution.

Any failed gate stops target evaluation and returns for review. No post-blind threshold weakening, model expansion or fixture removal. A post-unblinding software/resource repair must retain original artifacts, obtain review and use a fresh seed namespace before a renewed blind claim.

## Resource budget and stopping

Maximum shared study budget 8 CPU hours and 8 GiB including independent work. Prefer a substantially smaller pilot. The 600-input independent reference is estimated at about 20 CPU minutes from development. Each sequential worker has a 1 GiB address-space cap and one child with a 1 GiB cap, internal 60 CPU seconds, hard 65 CPU seconds and 90 wall seconds per input. Include parent and all child usage, including terminated children. Charge a conservative 600-CPU-second preparation reserve; write receipts in finally and stop before a new case unless enough study budget remains for its worst-case allowance. No unrecognized software, installs or external submissions.

## Target and closeout

Only after parent approval following independent benchmark PASS, prepare the canonical K4 transport under an additive hash freeze and perform one production plus one independent reference target evaluation. Preserve all cylinders, representative witnesses and ambiguity, not only a preferred candidate. Independently verify target receipts.

Reconcile HYPOTHESES.md, EXPERIMENTS.md and reviewed classifications; regenerate and validate navigation before deciding any next experiment. Close Q-03 only within tested bounds. Q-04 requires an actual exact-search bottleneck; Q-05 requires an actual language-scoring bottleneck. Do not run those conditional pilots merely because they are listed next.
