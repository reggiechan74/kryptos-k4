# Frozen Greek/phonetic and SIGABA-inspired candidate batch

23 October 2026 UTC. Written before either new K4 evaluation. User authorizes
completing both bounded candidates; no per-pilot approval or parameter expansion
is needed. These are our fixed hypotheses, not authenticated Sanborn methods.
Current baseline is 7de429d. Existing finite IPA/route/stepping exclusions remain
intact. Preserve unrelated suffix-copy files and make no Site change.

## Source and equivalence audit

Arvaniti, *Standard Modern Greek* (1999), pp. 167–172,
[primary paper](https://bpb-us-w2.wpmucdn.com/u.osu.edu/dist/7/103192/files/2024/08/Arvaniti-StandardModernGreek-1999.pdf),
describes a five-vowel system and rhotic/stop differences from English. That
constrains the approximation; it supplies no English-to-Greek cipher. Current
source phones remain the already frozen Cambridge-US dictionary forms, not a
new dialect chosen after fitting. Greek transcription is distinct from a Greek
translation, lamp labels, and the previous IPA glyph/alias experiments.

Mucklow, NSA Center for Cryptologic History, *The SIGABA/ECM II Cipher Machine*
(2015), Appendix B, printed pp. 32–33,
[official publication](https://www.nsa.gov/portals/75/documents/about/cryptologic-heritage/historical-figures-publications/publications/technology/The_SIGABA_ECM_Cipher_Machine_A_Beautiful_Idea3.pdf),
describes separate cipher, control and static index banks and irregular cipher-
rotor motion. Our stepping roles follow that architecture. The exact wiring,
collector, initial domain and electrical timing below are custom choices, not
an authentic machine emulator. We do not claim an authentic reference vector.
The [original patent](https://patents.google.com/patent/US6175625B1/en) is further
primary architectural context. The SJSU thesis endpoint returned HTTP 403 during
this review; no alternate credential or full-keyspace claim followed.

Prior local models advance a periodic cursor, update one alphabet or use fixed
modular recurrences. The present five-rotor cascade changes a complete nonlinear
substitution through independently generated multi-wheel stepping. It has no
reflector, so the direct-Enigma self-letter exclusion does not apply. This is
new to the specified local ledger, not a worldwide novelty claim.

## GREEK-PHONETIC-001

The exact map and strings are in `data/greek-phonetic-v1.json`. Reuse the source
phones for EAST+NORTHEAST and BERLIN+CLOCK. Map iː/ɪ→Ι, s→Σ, t→Τ, n→Ν, ɔː→Ο,
r→Ρ, θ→Θ, b→ΜΠ, ɝː→ΕΡ, l→Λ, k→Κ and ɑː→Α. Thus the windows are
ΙΣΤΝΟΡΘΙΣΤ (10 glyphs) and ΜΠΕΡΛΙΝΚΛΑΚ (11). These spellings are our uniform
approximation: English rhotics and rhotic vowels have no asserted exact match.
Only this observed 13-phone inventory is supported; unknown phones reject.
No universal English transcription, Greek dialect or alternative spelling is
silently supplied. Φ,Β,Δ etc retain their distinct Greek identities; Greek is not
English minus two letters. No digraph is silently counted as one Greek character.

Use NFC uppercase Greek order ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ, ranks 0–23. Cipher
symbols use either fixed AZ or KRYPTOS order, ranks 0–25. Per Greek character,
C=(rank(P)+k_phase) mod26 or C=(k_phase−rank(P)) mod26. The key repeats with
period m=1..10. The decoder reverses the arithmetic and rejects ranks 24/25;
this is an exact inverse on valid Greek plaintexts, not a bijection onto every
possible Latin string. No filler glyphs, padding or invented Greek letters.

Phonetic preprocessing loses information (iː and ɪ already collide), and English
spelling cannot be uniquely recovered. It also changes lengths, so do NOT use
English crib offsets. Test the necessary-condition relaxation of every ordered,
nonoverlapping pair of transformed windows in a 97-symbol stream: zero-based
u=0..76 and v=u+10..86, exactly 3,003 pairs. This includes alignments that may
not be reachable from any full English transcription; survivors would not prove
global alignment. No cumulative prefix or intervening word lengths are guessed.

Exactly 2 alphabets × 2 equations × 10 periods × 3,003 placements = 120,120 raw
structural/alignment descriptions. Key phase is redundant with free periodic
entries. Fit only the first ten Greek characters; m≤10 guarantees every key
phase is observed. Save contradiction witnesses or every fitted entry; never
fill a missing key. At period 10 there are zero extra training checks. Predict
the second Greek window at each declared v without refitting. Its unknown location
is a selected parameter, not eleven historically untouched predictions. Require
both complete transformed windows, then valid Greek rank at every position and
exact full regeneration. Report start/key/period aliases and full plaintext
classes; no full English solution claim from a Greek crib fit.

Controls: all 24 Greek characters and unrelated Greek strings roundtrip; reject
invalid ciphertext residues, unknown phones and non-NFC inputs. Verify the exact
loss collision and 10/11 lengths. Plant one example per 40 alphabet/equation/
period structure, using u=7,v=55 and deterministic keys declared in implementation
before scoring. Each passes the complete placement/key selector, retaining true
key and alignment plus all alternative fits. Include a constant-cipher incompatible
control. A second implementation will verify the complete actual finite domain.

Budget: 120 seconds controls, 120 seconds actual; 128 MiB output, one process.
Cache first-window constraints, but account for all 120,120 raw placements. Preserve
full compact rejection records rather than writing a repeated 120,120-row dump.
No extra period, transliteration, accent, alphabet, offset range or route afterward.

## SIGABA-INSPIRED-001

All exact permutations are expanded in `data/sigaba-inspired-v1.json`. Define
keyword alphabets by retaining first occurrences in the keyword then appending
unused AZ letters: A=KRYPTOS, B=PALIMPSEST, C=ABSCISSA. These use existing K1/K2
material to fix an unfitted demonstration construction, not SIGABA's historical
rotor tables. Cipher bank is [A,B,C,inverse(A),inverse(B)]; control bank is
[C,B,A,inverse(C),inverse(A)]. Index wheels over 0..9 are the fixed permutations
(3x+1),(7x+2),(9x+3),(3x+4),(7x+5), all modulo 10. Their static composition may
have equivalent descriptions; count aliases, not artificial complexity.

For a rotor permutation W and position p, forward map is
W_p(x)=(W[(x+p) mod n]−p) mod n. Reverse uses inverse(W). Cipher text traverses
cipher rotors 0..4; decryption traverses inverse rotors 4..0. Alphabet is AZ only.
There is no reflector, plugboard, space/Z substitution or input-dependent stepping.

At the current state, four fixed control inputs {5,6,7,8} pass through control
rotors 0..4. Reduce outputs modulo 10 (custom collector), pass through the five
static index wheels, and select cipher rotor floor(output/2), deduplicating
selectors. After encrypting/decrypting the current letter, increment each selected
cipher rotor once modulo 26. Then increment control rotor 2; its wrap increments
rotor 3, whose wrap increments rotor 1. Control rotors 0 and 4 are static.
The custom collector/grouping is not claimed to reproduce historical SIGABA.

Initial cipher positions [c,c,c,c,c], c=0..25; control [0,0,q,0,0], q=0..25;
index [r,r,r,r,r], r=0..9. Exactly 6,760 raw keys. No rotor permutations,
independent five-position keys, reversed wiring, extra timing variants or free
wiring. Deduplicate identical complete 97-position stepping schedules and keep
all raw aliases. Identical schedules do not by themselves prove distinct cipher
initial offsets yield distinct encryption functions.

Stepping depends only on the declared key and position. Generate it continuously
from position 1; knowing the state at a crib is exact propagation, not resetting
or assuming unknown plaintext. The actual selector may reject at the first crib
letter mismatch. For each fixed key, require all thirteen first English letters,
then all eleven Berlin letters without state refitting; materialize full plaintext
and require exact regeneration for any survivor. All fitted-key selection is charged
against the declared domain. This is not an exhaustive or authentic SIGABA test.

Controls before K4: every rotor position and letter has a tested inverse; independently
compute control signals and cipher states; test all selector sizes and carry boundaries
up to and beyond 676 steps. Fixed-key roundtrips on AZ and unrelated messages. Twelve
literal-English-crib plants use (q,c,r) in {(0,0,0),(25,25,9),(7,14,3),(13,2,4),
(1,8,5),(24,3,8),(5,21,1),(19,10,6),(11,17,2),(3,23,7),(16,6,0),(22,12,9)}.
Each uses the complete raw-key selector, retains true raw key and every equivalent
schedule/key, and reports full plaintext multiplicity. Wrong timing and incompatible
controls must be identified as implementation checks, not statistical evidence.
A separately written direct-rotor implementation will cross-check actual classifications.

Budget: 120 seconds controls, 120 seconds actual; 256 MiB memory and 128 MiB output.
Precomputation of public rotor/state tables is allowed, not extra key choices.

## Shared completion rules

Freeze and commit this specification and data before scoring, and commit controls
before actual evaluation. Record parameter counts, exact raw and canonical work,
compatible sets, SHA-256 provenance and explicit timeouts. If no complete survivor,
report a finite negative only. If survivors remain, run 199 fixed-seed histogram-
preserving ciphertext shuffles through the identical complete selector, within
an additional 120-second cap per family. Report plus-one resolution 1/200, no
posterior or correction over all previous research. A timeout is unresolved.
Regardless of outcomes, finish both declared families, save findings/registry/tests,
push main and stop this batch. No adaptive fifth variant or Site change.

### Null reproducibility clarification before evaluation

Before either actual comparison, fix Python MT19937 seeds 2026102301 for Greek
and 2026102302 for the rotor model. If triggered, the statistic is the count of
complete compatible model/alignment descriptions for Greek, or raw compatible
keys for the rotor model; every null reruns the identical complete selector.
This clarifies the already declared conditional calibration, changing no cipher,
parameter domain, alignment or success criterion. No null is run for zero survivors.
