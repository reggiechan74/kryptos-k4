# PHONETIC-CL-001 — recovery controls and inherited exclusion

18 October 2026. A fixed **CL→KL** adaptation passes synthetic transformed-text
and key-recovery controls. It provides **no new K4 search coverage**: the unchanged
EASTNORTHEAST span already contradicts direct repeating-key periods 1–12 in the
selected arithmetic families. No new key sweep or full K4 plaintext was produced.

## Source, exact adaptation and limits

Ripman and Archer's *New Spelling*, sixth edition (1948),
[chapter I, printed page 21 / PDF page 3](https://www.spellingsociety.org/uploaded_books/nschapter1.pdf#page=3),
proposes K for the hard-C sound and explicitly compares kl/kr with cl/cr.
The [edition introduction](https://www.spellingsociety.org/uploaded_books/ns1948intro.pdf)
confirms the 1948 edition. The exact chapter page and quotation were verified by
the independent source worker; this executor read the edition introduction, but
its chapter-PDF fetch timed out. There is no claim of local chapter pixel review.
No evidence connects this spelling system to Sanborn or Scheidt.

Our rule is a **modern restricted mechanical test inspired by that source**:
on an already-normalized uppercase A–Z stream, simultaneously replace C by K
only when the next original character is L. Copy everything else; infer no word
breaks and use no dictionary. CLOCK becomes KLOCK, with CK unchanged. This is
not full New Spelling, which also contracts CK and would change length. Lowercase,
spaces and punctuation are rejected instead of silently changing context.

The 97 positions stay fixed. Original English cribs remain EASTNORTHEAST and
BERLINCLOCK; transformed cribs are EASTNORTHEAST and **BERLINKLOCK**. Only
one-based position **70** changes. This distinguishes original letters from the
intermediate stream actually encrypted. The earlier W→V/final-D/G pilot left
all crib symbols unchanged; it was not rerun as new work. CL→KL is context-dependent
and noninjective, rather than a global alphabet bijection.

CL and KL both become KL. Unique original-spelling recovery therefore needs extra
information. Three seeded cases explicitly demonstrate two different originals,
differing outside the cribs, with the same transformed stream. We recover the
transformed stream and cryptographic key, not a unique English original.

## Frozen pilot and recovery controls

[Final specification](specifications/PHONETIC-CL-001.json) was committed at
`ea3090ba2ced41c1f687507a2b852c89a00530f5`, before implementation/evaluation.
The main selection pilot uses direct A–Z addition, periods 1–12, identity versus
CL only, and exact crib-derived keys. Four independent fixed seeds plant CL at
periods 5/7/11 and identity at period 7. The solver receives ciphertext and only
the 24 original known positions, not the planted full plaintext, transformed
stream or key. All four recover the correct mask, primitive key and transformed
97-letter stream. The period-5 key also has its equivalent period-10 parameter
alias; neither was discarded to manufacture uniqueness.

Supplementary controls use repeated-alphabet and repeated-CLACKCLOCK streams,
overlaid with the same original crib pattern: 2 streams × 2 masks × 2 alphabets
(A–Z/KRYPTOS) × 3 equations (addition, subtraction, true Beaufort) × 12 periods
= **288 cases**. In every case, inference at the planted family/period recovers
the exact key and full transformed stream and regenerates the ciphertext.
Wrong-mask inference and changing cipher position 22 by +1 each reject at the
planted family/period. These are recovery/negative tests, not merely round-trips
using a supplied key.

Full model selection retains parameter aliases (1–48 per case) rather than
claiming a unique historical cipher. All 288 have one mask/transformed-stream
group within the bounds. Four corrupted seeded cases have no alternative
candidates in the main bounded family. A low-information control reports four
free key phases and no recovered full stream; unsupported unknown C context is
rejected. **24 small-alphabet cases** compare inference with exhaustive key
oracles. These are synthetic algebraic controls, not a natural-language benchmark
or blind historical validation. No LLM generated or ranked attractive messages.

A fixture-construction mismatch was caught: an initial shared helper added the
seeded-case prefix to the two literal fixtures. It was corrected to the frozen
specification, with a regression test, before the final run. The explicitly
[superseded result](../results/PHONETIC-CL-001-superseded-fixture.json.gz) is audit
history, not final control evidence. No rule, key bound or seed was fitted to a
K4 result. Final implementation: `34058c4eb462fa346ca77bb3a426f704a06766ec`.

## Why no new K4 search is needed

Every mask considered leaves original positions 22–34 unchanged. Their required
key spans are:

| Alphabet | Addition | True Beaufort |
| --- | --- | --- |
| A–Z | BLZCDCYYGCKAZ | JLJODEGKUKKKL |
| KRYPTOS | RDUMRIYWOYNKY | WXAKGZTOAXAFD |

Subtraction negates the additive key values and preserves equality conflicts.
For every period 1–12 there are two positions in this first span with the same
phase and different required key values. For example, A–Z addition uses positions
22 and 22+p for each p; A–Z Beaufort at p=2 uses 23/25 (L/O); KRYPTOS addition
at p=4 uses 23/27 (D/I). All avoid changed position 70. A global phase shift
cannot repair equality conflicts.

The saved **144 witnesses** cover 2 masks × 2 alphabets × 3 equations × 12 periods.
They are an inherited [ROUTE-001](BOUNDED-FINDINGS.md) exclusion, not newly searched
keys or new historical evidence. Any preprocessing leaving this span unchanged
inherits these witnesses under the same alignment and arithmetic assumptions.
Longer periods, other masks/ciphers, variable-length phonetics, transposition and
translations remain outside this result. No extra rule was added to escape it.

## Reproduction and verification

```sh
python3 -m unittest discover -s tests -v
python3 experiments/phonetic_cl.py --spec-commit ea3090ba2ced41c1f687507a2b852c89a00530f5 --code-commit 34058c4eb462fa346ca77bb3a426f704a06766ec
```

All **133 tests pass in 7.964 seconds**, preserving all previous 127.
Final controls took 0.164514 seconds under the 10-second cap; proof verification
uses a separate 5-second cap. No randomness beyond frozen Python MT19937 seeds.
[Complete compressed result](../results/PHONETIC-CL-001.json.gz),
[summary](../results/PHONETIC-CL-001-summary.json),
[verification receipt](../results/PHONETIC-CL-VALIDATION.json).
Input hashes and all inherited witnesses were verified. Scott's artifact was
neither changed nor used as an experimental input. Stop this bounded pilot here.
