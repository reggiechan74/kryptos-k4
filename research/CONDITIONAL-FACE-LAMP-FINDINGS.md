# Conditional carved-row reflection and lamp stream — bounded outcomes

23 October 2026 UTC. Neither approved pilot yields an all-crib candidate. The
row test has two first-crib fits, both failing every Berlin letter. The lamp
readout is analytically impossible on the first crib; no actual phase scan was
needed. These conclusions do not exclude physical clues or other lamp ciphers.

## Chronology and scope

The complete [source report and three dossiers](evidence/2026-10-23-lodestone-compass/README.md)
were materialized, verified and read before the [protocol](CONDITIONAL-FACE-LAMP-SPEC.md)
was committed in 3eeb0b1. The pre-evaluation parity annotation was added in
ac6a3f1. Parent review approved the unchanged specification as published at
cdefbb4. Implementation and controls were committed in 25e107f before K4 scoring.
A separately written JavaScript cross-check was added afterward; it is a second
implementation in this executor, not a second researcher's blinded result.

No measured bearing, date, astronomical target, historical city or missing
orientation was invented. The actual carved mask is 4/31/31/31 occupied cells,
including columns 27–30 of its initial row. A physical mirrored cutout is not
silently relabeled as another letter. Mengenlehreuhr is a user-proposed alternative
display, distinct from Sanborn's confirmed World Clock referent.

## FACE-ROW-001

The complete coordinate-operation/inverse coverage audit has 768 raw aliases,
five distinct permutations and 372 distinct full model signatures. Of these,
280 are covered by retained ROUTE-001 results, with alphabet, equation, key domain,
phase partition and layer order checked; they were skipped. Only horizontal
reflection within each actual carved row contributes new models: 96 descriptions
before period-1 order equivalence, 92 afterward. The older occupied-column/fixed-
word pilot is different and was not used to claim an unrestricted-key rejection.
The [coverage records](../results/FACE-ROW-001-COVERAGE.json) retain every alias.

All 92 new models were tested: periods 1–12, AZ/KRYPTOS, addition/true Beaufort,
and substitution before or after the row operation. The thirteen first-crib
letters observe every phase in both orders, so compatible keys are fully fixed.
No missing key entry, unknown plaintext gap or free completion was guessed.
Ninety models contradict a repeated key-phase requirement inside the first crib.
The remaining two are:

| Coordinates / equation | Period | Layer order | Fitted key values | Independent training closure checks | Predicted Berlin | Exact matches |
| --- | ---: | --- | --- | ---: | --- | ---: |
| KRYPTOS / addition | 12 | substitution then reflection | 1,13,3,16,17,0,2,24,18,1,8,11 | 1 | HSTZCLZPDSB | 0/11 |
| KRYPTOS / addition | 12 | reflection then substitution | 3,13,1,11,8,1,18,24,2,0,17,16 | 1 | LQHXLMKCWIQ | 0/11 |

Each fit spends twelve key values on thirteen first-crib letters. It is not
thirteen independent predictions. Both keys have minimal period 12, both full
97-character decryptions are retained and regenerate the ciphertext exactly,
and both fail the public second block without refitting. The complete compatible
set after all 24 letters is empty. These are correlated constructions and public
clues, not historically untouched evidence. No partial-score significance or
new plaintext claim is made; an exact negative needs no shuffle simulation.

Controls include 92 literal-crib plants through the complete 92-model selector
(8,464 model descriptions). All true keys/plaintexts are retained. Compatible
canonical-model counts range from 1 to 23, and eight plants admit two distinct
full plaintexts; every compatible model and key is preserved rather than picking
the attractive one. The independent cell encoder, inverse controls and all-phase
checks pass. Ninety-two wrong-row mutations and 88 phase-shift mutations are
detected. A period-1 phase shift is equivalent, so is not counted as a negative.
The full selector rejects the separate constant-cipher incompatible fixture.

## LAMP-STREAM-001

The exact readout uses 24 binary fields, seconds at bit 0, then the four rows
in top-to-bottom/left-to-right order. The state advances one minute per character,
keeping the seconds-indicator state p constant. Every other field has even
weight; reducing modulo 26 preserves parity. Therefore every key symbol must
have the same parity p throughout the message, for every starting minute.

The known first crib demands incompatible parities:

| Coordinates | Equation | One-based positions | Required keys | Parities |
| --- | --- | --- | --- | --- |
| AZ | addition | 22,25 | 1,2 | odd,even |
| AZ | true Beaufort | 22,25 | 9,14 | odd,even |
| KRYPTOS | addition | 22,23 | 1,10 | odd,even |
| KRYPTOS | true Beaufort | 22,23 | 23,24 | odd,even |

The equation variants share parity obstructions because C+P and C−P differ
by 2P. These four formal certificates exclude all 11,520 raw starting-phase/
alphabet/equation descriptions. **Zero actual start-phase models were enumerated and Berlin was
not consulted by this proof.** This is an analytical exclusion of the fixed
bit order, minute sampling, modulo-26 readout and cipher layer, not 11,520 newly
simulated discoveries or a rejection of every lamp-based method. No field order,
color, sampling interval or Greek weight was changed to evade the result.

Controls still validate the construction: all 2,880 valid hour/minute/indicator
patterns are distinct and invert exactly; five invalid display patterns reject.
The inverse recovers indicator state, not an exact second. Hand vectors and
independent subtractive lamp logic verify five-minute, hour and midnight carries.
There are 2,832 distinct complete key streams among 2,880 starting states; alias
lists remain available. None of these complete streams belongs to the audited
period-1..12 or progressive period-1..12/drift-0..25 domains. Repeating fixed words
are subsets of the periodic domain. No wider prior-art novelty is inferred.

Thirty-two literal-crib plants retain their true settings through the complete
11,520-description selector and pass fixed-model 97-letter round trips with the
independent lamp oracle. They happen to have one compatible raw setting each;
that is a fixture observation, not a general uniqueness theorem. The selector
accounts for 368,640 raw descriptions across these controls: 184,320 are pruned
by the same parity condition, and 181,248 unique-stream/alphabet/equation models
are explicitly checked for the remainder. This accounting distinguishes aliases
and proof pruning from individual simulation. Thirty-two step-timing mutations
are detected, and the constant-cipher incompatible control rejects in all four
coordinate/equation structures.

## Reproduction and retained records

```sh
python3 experiments/face_row_coverage.py
python3 experiments/conditional_face_lamp.py controls --output /tmp/face-lamp-controls.json
python3 experiments/conditional_face_lamp.py actual --output /tmp/face-lamp-actual.json
node experiments/conditional_face_lamp_oracle.mjs
```

[Controls and full key-stream aliases](../results/CONDITIONAL-FACE-LAMP-001-controls.json),
[all actual constraints/certificates and the two training decryptions](../results/CONDITIONAL-FACE-LAMP-001.json),
and [post-run independent implementation results](../results/CONDITIONAL-FACE-LAMP-001-independent.json)
are separate. Timing fields vary on replay. The JavaScript implementation agrees
on all 92 classifications, both complete training decryptions and all four lamp
certificates. Current Python actual evaluation took about 0.10 seconds, within
the declared 120-second stage cap; controls also completed within their caps.

This finite batch stops here. Physical bearing, shadow and celestial reconstructions
still lack the measurements identified in the source report. Historical World
Clock extraction, lamp/Greek labels, Greek phonetic rendering and genuinely new
tree mechanisms retain their separate open or evidence-blocked statuses in the
[canonical register](HYPOTHESES.md). No Site change or expanded search followed.
