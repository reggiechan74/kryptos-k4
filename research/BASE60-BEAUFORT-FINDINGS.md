# BASE60-BEAUFORT-001 — verified partial coverage

18 October 2026. The genuine-Beaufort gap is real for the two reviewed base-60
recurrences, but this bounded audit **does not close the entire length-4 space**.
An exact parity proof excludes all length-2/3 primers and most length-4 primers.
The first 100,000 remaining primers tested are contradicted; **3,140,000 remain
untested**. No full plaintexts, language filters or solar geometry were used.

## Frozen model and prior-art gap

For one shared unknown bijection X from A–Z onto Z26, require
`X(P_i)+X(C_i)=d_i mod26` at all 24 confirmed crib positions, with direct alignment.
Generate 97 base-60 states from every primer digit 0–59 (leading zeros retained):

- rule 0: `a[i]=(a[i-L]+a[i-L+1]) mod60`
- rule 1: `a[i]=(a[i-L]+a[i-1]) mod60`

Then `d[i]=a[i] mod26`; mod26 cannot be moved inside the recurrence. L is 2–4.
L2's rules coincide: 26,359,200 nominal labeled tuples versus 26,355,600 unique
mechanism/primer tuples. No separate negative-stream sweep is necessary: X→−X
bijectively exchanges solutions for d and −d.

[Scott run_sexa.py](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/run_sexa.py)
and imported [run_gromark.py](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/run_gromark.py)
were inspected as text only. S1 calls the shared-alphabet difference checker for
d and −d, not the sum equation. That checker verifies component consistency and
internal injectivity; it does not pack different components globally. The separate
[clocksingle.py](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/clocksingle.py)
sum checker is relevant prior art; it does not make S1's recurrence coverage true
Beaufort. This is a gap in pinned reviewed scripts, not a global novelty claim.
[Earlier clock/base note](../docs/ene-base12-base60.md).

Initial pre-run specification: `85c941a3b1d2f99f5f7cfca45563fd09968ad4cb`.
[Audited specification](specifications/BASE60-BEAUFORT-001.json):
`1217239dfbca5649458b89e94d347a671b805d4e`.
Implementation before the saved run: `dc220493c2db01197b31946bd477465679d4a125`.
The independent graph/parity audit was reconciled before the saved run.

## Readable parity certificate

The crib sum graph has one connected component of **21 observed letters**;
D,J,U,W,X are unused. All indices below are zero-based. Self-loops at 32 (S–S)
and 73 (K–K) require even keys. A triangle and repeated R–P edge additionally give
four necessary binary equations:
`a32=0`, `a73=0`, `a23+a33+a28+a32=0`, `a27+a65=0` over GF(2).
Propagating unit-vector primers through each binary recurrence yields these
coefficient rows (all right-hand sides zero):

| L / rule | Four binary coefficient rows | Nonzero surviving primer parity |
| --- | --- | --- |
| 2 / either | 11; 01; 11; 01 | none |
| 3 / 0 | 011; 110; 001; 100 | none |
| 3 / 1 | 111; 101; 100; 010 | none |
| 4 / 0 | 0010; 1011; 0010; 1001 | 0100, 1001, 1101 |
| 4 / 1 | 0010; 0110; 0010; 0001 | 1000 |

The all-zero parity primer makes all keys even; connectivity then forces all 21
observed X values to the same parity, impossible with only 13 residues of each
parity. Each parity class contains exactly 30^L primers, since both mod60 and
mod26 preserve parity. Thus **23,115,600 unique primers** are analytically
contradicted, leaving four length-4 classes totaling **3,240,000**. The implementation
also solves the entire binary graph and parity-capacity constraint, independently
matching these rows and survivor masks. This pruning is topology-specific;
synthetic controls rebuild their own graphs.

## Exact feasibility and bounded executed range

A component uses `X(v)=sign_v*t+offset_v mod26`. Each edge constrains
`(sign_u+sign_v)*t=d-offset_u-offset_v`. Opposite signs give a zero-coefficient
consistency test. Same signs give ±2t constraints: **enumerate roots 0–25;
never divide by an inverse of 2 modulo26**. Intersect roots and reject internal
collisions. Generic disconnected fixtures additionally require disjoint residue
sets globally; unused letters fill remaining residues. On the real graph there
is only one component, at most two roots after a self-loop, differing by 13 and
having identical injectivity. Complete witnesses are verified as full bijections
against every crib equation. A solver cap is unresolved, never contradiction.

Eligible primers are ordered by original base-60 integer code within each rule,
with rule configurations interleaved deterministically. Parity-rejected codes
are certified separately, so a numeric prefix is not a claim that all its codes
were individually solved.

| Configuration | Parity rejected | Actually evaluated | Last / next eligible code | Unevaluated after parity |
| --- | ---: | ---: | --- | ---: |
| L2 / 0 (both labels) | 3,600 | 0 | exhausted analytically | 0 |
| L3 / 0 | 216,000 | 0 | exhausted analytically | 0 |
| L3 / 1 | 216,000 | 0 | exhausted analytically | 0 |
| L4 / 0 | 10,530,000 | 50,000 | 307959 / 307961 | 2,380,000 |
| L4 / 1 | 12,150,000 | 50,000 | 829958 / 829960 | 760,000 |

All 100,000 tested cases are local sum/injectivity contradictions. There are zero
local-compatible/global-contradictory cases, zero complete feasible alphabets and
zero solver-capped cases **within that executed range**. Untested cases are not
classified. Raw records distinguish analytic coverage from evaluated counters.

The 4,096-case pilot took 0.043652 s. Aggregate action time was 0.986906 s, stopping
at the frozen **100,000-candidate ceiling**, not the 30-second ceiling. One process;
no random search, installation, paid compute or third-party executable code.
No budget extension or whole-family exclusion is claimed.

## Validation and reproduction

All **124 tests pass in 8.026 s**, preserving the previous 118. Local controls
include 4,123 exhaustive Z2/Z3 labeled graphs versus permutation oracles, six
planted real-alphabet cases, even-modulus two-root/self-loop cases, inconsistent
cycles, internal collisions, disconnected global infeasibility, free letters,
caps, parity preservation and independent binary-row certificates.
The independent reviewer's separate 1,000 toy cases and 200 planted/1,000 random
vector comparisons are supplied audit evidence, not part of our test counts.
Checkpoint generators were replayed without new cryptanalytic evaluations;
input hashes and the result hash were verified.

```sh
python3 -m unittest discover -s tests -v
python3 experiments/base60_beaufort.py --spec-commit 1217239dfbca5649458b89e94d347a671b805d4e --code-commit dc220493c2db01197b31946bd477465679d4a125
```

[Raw result and exact checkpoints](../results/BASE60-BEAUFORT-001.json),
[validation receipt](../results/BASE60-BEAUFORT-VALIDATION.json).
Continuation would need a separately frozen budget and checkpoint-aware runner.
Seasonal light/sundial research is separate source work and supplied no experiment
parameters. No historical mechanism or K4 solution follows from this bounded negative.
