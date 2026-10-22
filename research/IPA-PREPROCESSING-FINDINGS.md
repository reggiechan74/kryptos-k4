# Dictionary-IPA preprocessing — bounded local findings

The declared Cambridge US code-point representation fits the two local English
crib lengths, but all 48 fixed-Latin periodic arithmetic structures fail within
the first crib. This is a negative for this particular preprocessing and outer
cipher model, not for every phonetic or IPA-based cipher.

## Frozen representations and alignment

The [protocol](IPA-PREPROCESSING-SPEC.md) was committed at 2c40fca before local
K4 fitting; source normalization had already observed the 13/11 lengths with
public clue lengths known. The [implementation notes](IPA-PREPROCESSING-PREFIT-NOTES.md)
record preliminary independent results and their staging correction. Inputs and
controls were committed at 6499d17; the final run interface at e09593f preceded
the local K4 evaluation. This was an operational freeze, not a blind discovery.

The [input record](../data/ipa-cambridge-us-v1.json) uses the supplied Cambridge US
forms. Uniformly remove stress marks, whitespace and syllable separators; retain
vowel-length marks. Whole phonemic segments (R1) have lengths 10 and 9. Literal
Unicode code points (R2) give `iːstnɔːrθiːst` and `bɝːlɪnklɑːk`, lengths 13 and
11. R1 does not fit the unchanged spans under one-segment/one-cipher-letter
transport. That is an alignment restriction, not a general exclusion of R1.

The R2 model assumes those windows occupy positions 22–34 and 64–74. It does not
establish cumulative alignment through unknown prefixes or the gap, or a total
97-character phonetic encoding. The English disclosures remain EASTNORTHEAST
and BERLINCLOCK; no crib was replaced or shifted. Modern dictionary notation is
an operational test input, not evidence of Sanborn's 1990 notation. Sound-to-
spelling reconstruction is not universally unique.

## Necessary equality constraints

Direct deterministic substitution fails: IPA i at positions 22 and 31 would have
to produce F and G. Mapping-independent injective substitution per periodic phase,
using both disclosed R2 windows, rejects periods 1,2,3,4,5,6,7,9,10.
Periods 8,11,12 are not contradicted, but this survival is vacuous: their observed
phase pairs contain no repeated IPA or ciphertext symbol on which to test a
repeat equality. Distinct observations simply fit free phase maps. This is not
evidence for any of these periods.

The arithmetic test below independently evaluates every structure; the two-window
necessary check is not used to filter its first-window trials.

## Fixed-Latin alias model: 47 anchor failures and one shared-symbol failure

Keep i/s/t/n/r/b/l/k as I/S/T/N/R/B/L/K. Allow all 26^3 assignments to the first
window's special symbols ː, ɔ and θ, initially including collisions. Use AZ or
KRYPTOS, C=P+K or true Beaufort C=K-P, periods 1–12: 48 formal structures.
Unrestricted key phase and additive key sign do not add cases.

Same-phase differences eliminate key slots, leaving exact linear equations in
three alias values. The solver retains complete affine spaces over F2 and F13
with CRT, including singular cases. Forty-seven structures already contradict
fixed ordinary-letter anchors within positions 22–34.

The remaining AZ-additive period-10 case has consistent ordinary anchors at
24/34 (both require key 25), but its shared length marker is impossible:

- Positions 22/32 require the alias index for ː to be 13.
- Positions 23/33 require that same alias index to be 11.

This is a shared-special-symbol contradiction, not an ordinary-anchor failure.
The modular certificate is stored explicitly; it is inconsistent modulo 13 even
though its parity constraints alone are consistent. All 48 relaxed structures
are therefore impossible. Zero alias assignments were enumerated in the actual
run: symbolic contradictions exclude every completion, including the injective
subset. The 26^3 potential assignments per structure are not executed trial counts.

No first-window structure survives, so Berlin aliases ɝ, ɪ and ɑ are not fitted.
Were a structure to survive, those three new values would be parameters, not
predictions; only eight second-window positions use previously specified symbols.
The fourteen-symbol partial model is not a universal A–Z encoding of IPA.

## Controls and current verification state

All 48 synthetic literal-IPA plants pass the complete 48-structure selector,
retain the true aliases/key and round-trip exactly. Some retain multiple second-
stage-compatible mappings; no unique inference is assumed. Nine complete small-
ring comparisons and three exhaustive planted 26^3 alias-set comparisons agree
with independently expressed key constraints. Unicode/length mutations, forbidden
alias collisions and unknown-symbol rejection are tested.

The [local results](../results/IPA-PREPROCESSING-001.json) preserve all 48 systems,
field ranks, certificates and first-window-only staging. The
[control receipt](../results/IPA-PREPROCESSING-001-controls.json) records all plants.
Reproduce with `python3 experiments/ipa_preprocessing.py controls` or `actual`.
All 273 current repository tests pass in 9.683 seconds.

The corrected independent source/audit archive is supplied as Library file
`libfile_8b54608d88708191833dd3160805090c`, expected ZIP SHA-256
`163eb3d44e38c3824b3ffd8f47887601dc3c21915236f9c419cf5a053235c850`.
Its consumer-local materialization and replay are currently pending because the
required fresh Library helper resource is unavailable. No original archive
success, source-link verification or independent replay is claimed here. The
frozen input's pending-source status records that pre-run state. The already
supplied literal source strings were sufficient for the separate local checks.
No dialect, period, cipher family or shifted-index variant was added after failure.
