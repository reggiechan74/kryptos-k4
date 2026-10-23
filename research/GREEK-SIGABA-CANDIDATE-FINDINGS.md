# Greek phonetic and SIGABA-inspired pilots — completed bounded batch

23 October 2026 UTC. Both declared families have zero complete survivors. The
Greek experiment rejects its fixed approximation and periodic outer layer over
all declared transformed-window placements. The rotor experiment rejects its
custom, tightly restricted starting-key family. Neither result rejects Greek
phonetic preprocessing generally or authentic SIGABA.

## Registration and sources

The [specification](GREEK-SIGABA-CANDIDATE-SPEC.md) and exact
[Greek map](../data/greek-phonetic-v1.json)/[rotor wirings](../data/sigaba-inspired-v1.json)
were committed at 7bc893f before evaluation. Implementation and complete controls
were committed at 6f5ba70. A pre-evaluation clarification at a9e4db1 fixed the
already conditional null seeds/statistics; it changed no model or range. Actual
results follow that commit. The separately written JavaScript verification is
post-run work in this executor, not a blinded second researcher or historical
reference emulator. Its complete classifications agree.

Arvaniti's [primary Modern Greek description](https://bpb-us-w2.wpmucdn.com/u.osu.edu/dist/7/103192/files/2024/08/Arvaniti-StandardModernGreek-1999.pdf)
provides linguistic context: a five-vowel system and consonant/rhotic distinctions.
It does not prescribe our English transcription. The source phones are the
previously frozen Cambridge-US forms, whose independent audit is already archived.
Our choice of Greek approximations is explicitly model design, not a standard
or purported 1990 Sanborn notation.

The [NSA historical publication](https://www.nsa.gov/portals/75/documents/about/cryptologic-heritage/historical-figures-publications/publications/technology/The_SIGABA_ECM_Cipher_Machine_A_Beautiful_Idea3.pdf),
Appendix B, and [original patent](https://patents.google.com/patent/US6175625B1/en)
ground the separate cipher/control/index-bank architecture and irregular motion.
Our wiring and collector are custom, not authenticated SIGABA settings. A public
SJSU thesis endpoint returned HTTP 403; no credentials or access workaround were
used. No authentic machine reference vector or full historical keyspace test is
claimed. That remains outside this pilot, not a blocker to testing the declared
SIGABA-inspired construction.

## GREEK-PHONETIC-001

### Transcription, inverse and alignment

The observed 13-phone map yields ΙΣΤΝΟΡΘΙΣΤ (10 Greek characters) and
ΜΠΕΡΛΙΝΚΛΑΚ (11). In particular, /b/ uses the two-character ΜΠ, US /ɑː/ maps to
Α and the rhotic vowel is approximated by ΕΡ. No alternate accent, Greek dialect,
spelling or word order was selected after scoring. This is not a Greek translation,
lamp-label map or English alphabet with two letters removed.

The phonetic operation is lossy: iː and ɪ both yield Ι. We do not claim to recover
English spelling or even a unique phone sequence. Separately, the outer cipher
has an exact inverse on valid uppercase Greek strings. It uses the natural
24-letter Greek ranks and a periodic modular shift into AZ or KRYPTOS ciphertext;
decryption rejects residues 24/25 rather than inventing Greek fillers.

Since preprocessing changes lengths, English crib positions were not reused.
The experiment relaxes alignment to every ordered, nonoverlapping 10/11-character
window pair in the 97-symbol cipher: 3,003 pairs. This includes some placements
that might not arise from a complete English transcription. No unknown prefix,
intervening word lengths or cumulative alignment was silently reconstructed.
Therefore even a surviving fit would only be a necessary-condition match.

### Exact finite result

Two ciphertext alphabets × two equations × periods 1–10 give 40 structures;
combined with 3,003 placements there are 120,120 descriptions. Phase is absorbed
by the free key. The first ten Greek characters determine every key entry;
there is no unobserved key fill. Cached first-window work accounts for every
placement rather than re-solving identical constraints for each second start.

| Stage | Result |
| --- | ---: |
| Structure/first-window sites examined | 3,080 |
| First-window fits at period 9 | 16 |
| First-window fits at period 10 | 308 |
| First-window fits at periods 1–8 | 0 |
| Second-window placements checked after training | 12,664 |
| Complete transformed-crib fits | 0 |
| Fits rejected only by full Greek-domain validation | 0 |
| Complete compatible Greek plaintexts | 0 |

Period 9 has one redundant training equality and period 10 has none. The latter
308 fits are fitted ten-entry keys, not ten predictions. The second location
is also selected from the declared range and cannot be called untouched evidence.
Every retained first-stage key fails the second transformed window at every
eligible placement. No full Greek or English candidate is produced, and no
null significance calculation is needed or claimed.

### Controls

All 24 Greek characters, unrelated Greek strings and fixed-key complete messages
roundtrip. Unknown phones, non-NFC input and invalid Greek residues reject. The
loss collision is tested explicitly. Forty literal-window plants use all 40
outer structures; each complete selector recovers the true key and unknown
locations among the full 120,120-description domain. All compatible alternatives
are retained. Plant compatibility ranges from 1 to 10 descriptions, with one
full Greek plaintext in these particular fixtures; this is not general key or
English-spelling uniqueness. The incompatible constant-cipher selector rejects.
Controls account for 4,804,800 descriptions, with shared first-stage work cached.

## SIGABA-INSPIRED-001

### Reversible mechanism and limits

This is a genuine rotor-permutation cipher with three banks of five rotors,
not merely an irregularly indexed additive key. Five cipher permutations are
fixed from the existing KRYPTOS/PALIMPSEST/ABSCISSA keyword alphabets and inverses.
Five control permutations feed a fixed custom 26-to-10 collector and five static
index permutations. Their outputs select distinct cipher wheels to advance.
The data file fully specifies every permutation, position convention and update.
The state progresses after each letter, with a separate control counter; it
never resets at either crib. Since stepping is plaintext-independent, state at
position 22 follows exactly from the initial key through the preceding 21 steps.
Skipping unknown plaintext computations is not guessing or fitting their state.

Its differences from historical SIGABA are material: custom rotor wirings,
collector/grouping, a very small correlated starting-position domain, no reversed
wheel search, no historical key-list procedure and no operating Z/space conversion.
We test that specified model only. A post-run fixed-state check also verifies
that its first-state substitution is neither a uniform additive shift nor true
Beaufort in AZ or KRYPTOS coordinates, unlike the earlier cursor layers. The lack of a reflector also makes the earlier
direct-Enigma self-letter proof irrelevant here. No historical-use inference is
made from a successful roundtrip or architecture resemblance.

### Exact finite result

The raw domain is 26 cipher-common offsets × 26 fast-control starts × 10
common static-index starts = 6,760 keys. The 260 control/index starts generate
130 distinct complete 97-position stepping schedules; all raw aliases are kept.
Thus 3,380 schedule-normalized models were checked. We do not claim this is a
proof of globally distinct encryption functions across every offset.

Every model fails within the first four letters of EASTNORTHEAST:

| First contradicting one-based plaintext position | Schedule-normalized models |
| ---: | ---: |
| 22 | 3,269 |
| 23 | 105 |
| 24 | 4 |
| 25 | 2 |

Zero thirteen-letter first-crib survivors, zero Berlin evaluations and zero full
candidates remain. The second block was not needed to reject this domain; it
remains publicly known and is not historically untouched data. No null calibration
or phase/wiring expansion followed the exact failure.

### Controls

All 7,260 individual rotor-position/input inverses across the three banks pass.
An independent direct-wiring/closed-form-counter oracle agrees through 805 steps
for three carry-boundary keys, including both 26- and 676-step carries. Actual
schedule generation yields selector sizes 2,3,4; generic selector-cardinality
checks also cover the allowed one-wheel case. No source claim is made that this
custom model realizes every historical machine's motion distribution.

Twelve literal-English-crib plants pass the complete 6,760-raw-key selector,
retain the true key and preserve schedule aliases. Each has one compatible
schedule/offset class containing two raw keys and one complete plaintext. All
fixed-key roundtrips, unrelated messages, twelve wrong-timing mutations and the
constant-cipher incompatible control pass. These controls validate this custom
implementation, not an authentic SIGABA emulator.

## Cross-check and reproduction

The post-run JavaScript implementation independently reconstructs every Greek
first-stage constraint/second-window mismatch and every raw rotor key without
using production tables or saved stepping schedules. It agrees on all 120,120
Greek descriptions and 6,760 rotor aliases, and an unrelated fixed-key ciphertext
matches the Python implementation. It does not add new search coverage.

```sh
python3 experiments/greek_phonetic_candidate.py controls --output /tmp/greek-controls.json
python3 experiments/greek_phonetic_candidate.py actual --output /tmp/greek-actual.json
python3 experiments/sigaba_inspired.py controls --output /tmp/rotor-controls.json
python3 experiments/sigaba_inspired.py actual --output /tmp/rotor-actual.json
node experiments/greek_sigaba_oracle.mjs
```

[Greek results](../results/GREEK-PHONETIC-001.json) preserve all 3,080 weighted
first-stage records and all 12,664 second-stage failures. [Greek controls](../results/GREEK-PHONETIC-001-controls.json)
are separate. [Rotor results](../results/SIGABA-INSPIRED-001.json) preserve every
schedule, raw alias and first contradiction; [rotor controls](../results/SIGABA-INSPIRED-001-controls.json)
retain all plants. [Independent results](../results/GREEK-SIGABA-001-independent.json)
cover the identical frozen domains. Recorded runtimes are far below the 120-second
caps; timing fields vary on replay. No budget-unresolved cases occurred.

Both candidates are finished within their declared scope. Other Greek mappings,
other outer ciphers and authentic historical SIGABA remain untested rather than
excluded. No Site change, external outreach, new credential or paid compute was
used. [Source-access receipt](../sources/greek-sigaba-candidate-evidence.json). The batch stops without adding variants after either negative result.
