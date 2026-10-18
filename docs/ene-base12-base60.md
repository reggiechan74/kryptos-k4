# ENE, base 12 and base 60 — research note

18 October 2026. User hypothesis: “East northeast represents degrees or radians.
Is there anything that is base60 or base12 we haven’t thought of?” ENE can be
expressed numerically; this does not prove the clue is an instruction to do so.

## Exact conventions

Clockwise from true north, ENE is **67.5° = 67°30′00″ = 3π/8 radians = 3/16 turn**.
Counterclockwise from east in mathematical coordinates it is **22.5° = π/8**.
The [US Naval Observatory](https://aa.usno.navy.mil/faq/alt_az) defines the north-based
azimuth convention and gives the 15-degrees-per-hour conversion. These are unit
conversions, not competing bearings. Base 60 occurs in angular minutes/seconds
and clock minutes/seconds; those quantities must not be conflated.

On an abstract clockwise dial with zero at north, the same turn fraction puts the
**hour hand at 2:15 on a 12-hour dial**, or **4:30 on a 24-hour dial**. These are
hour-hand positions, not minute-hand readings. Their elapsed increments are
8,100 and 16,200 seconds respectively. They do not read the physical World Clock
without a ring phase, time reference and historical orientation.

The [official Berlin city description](https://www.berlin.de/en/attractions-and-sights/3561749-3104052-world-clock.en.html)
documents a 24-corner cylinder representing time zones, city inscriptions,
a rotating hour ring and a ground wind rose. A mathematical common grid for
24 sectors and 16 compass directions has lcm(24,16) = **48 half-sector slots**:
ENE is 9 slots; repeated +9 modulo 48 has period 48/gcd(48,9) = **16**.
This assumes aligned abstract origins, not a surveyed physical alignment.
ENE spans 4.5 of the 15° sectors; do not round this to a city face. A physical
city/ring selector remains open pending the [historical orientation evidence](historical-clock-inscriptions.md).

## What is already contradicted

Any fixed output function of that wrapped 16-state cycle repeats after 16 steps.
Its direct AZ/KRYPTOS additive, subtractive and true-Beaufort use at unchanged
letter alignment is already excluded by [ROUTE-001](../research/BOUNDED-FINDINGS.md).
No rerun is needed. Positions **22 and 70**, separated by 48, share the key phase:
plaintext/ciphertext are **E/F** and **C/M**. Required zero-based key values are:

| Alphabet | C=P+k | C=P−k | C=k−P (true Beaufort) |
| --- | --- | --- | --- |
| AZ | 1 vs 10 | 25 vs 16 | 9 vs 14 |
| KRYPTOS | 1 vs 9 | 25 vs 17 | 23 vs 1 |

Every pair conflicts. Global starting phase does not change phase equality.
This does **not** exclude arbitrary period-16 bijective substitutions; period 16
passes the more general [equality constraints](../research/STRUCTURAL-FINDINGS.md).
It does not cover extra layers or a clock mechanism retaining carry/memory.
In particular, +8,100 seconds modulo a full 86,400-second day has period **32**,
not 16; the 16-state equivalence uses a 12-hour wrap for that increment (or
+16,200 seconds with a 24-hour wrap).

## Pinned prior-art coverage and remaining specification gaps

Scott's [run_sexa.py](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/run_sexa.py)
and [retained log](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/results/sexa.log)
are read-only third-party evidence at commit `3ce19e3ae164a54af8743222ad3de5f6a93f6faf`;
no third-party code was executed here.

- S1: two base-60 additive recurrences, every primer of lengths 2–4;
  the log reports zero hits for each configuration.
- S2: 38 specified second increments, all 86,400 starting times, eight H/M/S
  projections, including H mod 12: 26,265,600 streams, zero reported hits.
  Starting phase is broadly covered. Literal 8,100/16,200-second steps are absent;
  that omission does not make the equivalent wrapped 16-state fixed-alphabet key new.
- S3: base-12 two-digit no-carry addition, chained digit primers of lengths 2–5;
  the log's best crib counts are 2, 2, 3 and 4 out of 24. These finite models are
  not an exclusion of all base-12 arithmetic.

S1/S2 test a **shared unknown alphabet X(C)=X(P)±d**, despite NOTES calling a
sign flip Beaufort. Genuine Beaufort requires **X(C)+X(P)=d mod 26**. Its absence
for the two S1 base-60 recurrences is a conditional coverage gap in the reviewed
scripts, not proof it is globally untried or a compelling new lead. Conversely,
[C12 run_clock12.py](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/run_clock12.py)
calls true-Beaufort checks in [clocksingle.py](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/clocksingle.py)
for its own specified analogue/date streams. Do not generalize the S1/S2 gap to
all clock tests or infer extra coverage from a method label alone.

K2 supplies a concrete sexagesimal precedent: the [NSA declassified analysis,
PDF page 1](https://www.nsa.gov/portals/75/documents/news-features/declassified-documents/cia-kryptos-sculpture/doc_7.pdf)
records 38°57′6.5″ N and 77°8′44″ W. Preserve **6.5 arcseconds = 13/2 arcseconds**
(13/7200 of a degree), not separate digits 6 and 5. This motivates careful units,
not a K4 decoding rule. Physical selection, mixed-radix carry or persistent clock
state would require an independently specified mechanism and reversible mapping
before testing. No new sweep or cipher-family closure follows from this note.

Reproduce the exact arithmetic, six two-cell witnesses and retained-ledger check:
`python3 experiments/check_ene_note.py`. [Check receipt](../results/ENE-NOTE-CHECKS.json).
