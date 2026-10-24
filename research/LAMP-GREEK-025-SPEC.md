# LAMP-GREEK-025: frozen exploratory lamp/Greek codecs

Frozen before item 5 K4 evaluation, 24 October 2026 UTC. These are our constructions, not evidence of Sanborn's design. Mengenlehreuhr is not the confirmed Alexanderplatz World Clock. The public cribs and prior exclusions were known during design.

## Inputs and common convention

Use the unchanged 97-character `data/k4.json` ciphertext and English windows at zero-based 21 and 63. Greek order is the declared modern alphabet ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ, without archaic letters. Ordinals are our weights, not historical Greek numerals or phonetic values. The display has seconds, four five-hour, four one-hour, eleven five-minute and four one-minute fields. H=5a+b, M=5c+d; each row is left-consecutive. This is not positional base 5.

Only two orders: physical top-to-bottom, left-to-right (seconds first), or reversal of all 24 fields. Attach Greek ordinals 1..24 in that order. Sum ordinals of lit fields: S. Seconds indicator p is 0 or 1 and constant at one-minute sampling; no color weights. Start t=0..1439, advance exactly one minute per operation, modulo 1440, with no reset. Output coordinates AZ or KRYPTOS; equations addition or true Beaufort. Exactly 23,040 raw descriptions per role, 69,120 total, before aliases or necessary-condition pruning. No alternative rates, feature permutations, pairing origins, clock weights or fitted constants.

## Three complete roles

L: one operation per English letter. C=P+S or C=S-P modulo 26. This is a total reversible A–Z cipher. Greek labels provide ordinal weights only. Compare all 97-value key streams with old LAMP-STREAM-001 binary readouts and disclose overlap.

B: adjacent pairs from position 1; rank=26*x+y in the selected coordinates. Each rank has a fixed-width three-digit Greek base-24 representation (reject decoded ranks >=676). Encrypt ranks by addition or true Beaufort with S modulo 676, then return two Latin coordinates. An odd final singleton has rank 0..25, two Greek digits, modulo-26 cipher. One minute per block. This is total, reversible and length-preserving in English. Greek digits are an internal representation, not extra encryption. Partial crib pairs must constrain only known letters, or use the fully decrypted message; do not fill gaps with guessed letters.

G: English A..W map to Greek indices 0..22; reserve Ω as escape, with X=ΩΑ, Y=ΩΒ, Z=ΩΓ. Reject dangling escape and other escape tails. This prefix code is total and injective, variable length, not phonetic. Encrypt each Greek index by addition or true Beaufort with S modulo 24, one minute per Greek symbol. Serialize using the first 24 symbols of the selected Latin coordinate alphabet. Decode all tokens and framing before testing English length 97 and clue windows. Never reuse English positions in the expanded ciphertext. A support contradiction may reject this entire role without phase enumeration. Record the naive modulo-24 A/Y and B/Z collisions separately; that lossy map is not an additional cipher trial.

## Controls and predeclared selection

Independent closed-form sum versus display bits for all 2,880 states and both orders; complete display inverse, carries, midnight, invalid-state tests. All English strings through length 3 round-trip the escape codec; all 676 pair and 26 singleton ranks round-trip Greek digits. Reject invalid framing/ranks. Independent arithmetic encryption checks for every role and complete parameter dimensions on unrelated messages.

Twenty-four literal-crib plants: roles L/B/G, both orders, starts [0,58,719,1438]. In role/order/start enumeration, alphabet=(role_index+order_index+start_index)%2, equation=(start_index//2+order_index)%2, indicator=(role_index+start_index)%2. Plaintext is fixed 97-character repeated pangram with public cribs inserted; positions 1..3 are XYZ and zero-based 40/50 are X/Y, exercising expanded prefix and gap. For each plant, run the entire family selector, preserve every survivor and plaintext class, require planted inclusion and full reencryption. Mutation controls change timing, framing and one known cipher symbol; account for true aliases rather than demand false uniqueness.

Actual selection: retain every full-message parse/first-crib fit; apply Berlin with the same model, no refit. Save all first-stage survivors, full plaintext classes and exact aliases. Public Berlin is a second-stage check, not untouched data. Use no partial-match score or English-looking fragment ranking.

Null control: 199 full histogram-preserving ciphertext shuffles, seed 250024. Rerun the entire identical selector, including codec support and length checks. Record any first-stage and all-24 survivor events. If no actual all-24 survivor, report a bounded negative, no significance claim. If one survives, report plus-one whole-family event p=(1+null hits)/200, not posterior probability or correction for all prior research; no solution claim.

## Budgets and stopping

Controls 120 seconds; actual selection 30 seconds; null panel 120 seconds; each at 512 MiB peak RSS. Check budgets between candidates, retain incomplete status on exhaustion and never relabel a timeout as negative. No new variants after outcomes. Original timestamps and source hashes go in immutable run receipts. Tests on both supported Python versions; no Site changes. Stop after item 5.

Broader Greek/lamp, other framing, historical numeral weights, timing schedules, color, physical light and phonetic models remain outside coverage. A count match alone is not historical support, and codebook uniqueness alone is not cryptographic strength.
