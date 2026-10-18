# Masking source boundary and two fixed pilots

Supplied research-worker specification, 18 October 2026; reviewed against prior
repository scope at 6371d63. Source observations below are attributed to that
research, not an independent local re-reading of every interview/manual. The
coding executor separately checks arithmetic fixtures and the ACA example before
K4 execution. These mechanisms are exploratory, not identified Scheidt methods.

## What the sources establish

[Scheidt's edited 2005 WIRED interview](https://www.wired.com/2005/01/inside-info-on-kryptos-codes/)
concerns hiding statistical access to English and, separately, interpreting a
readable message. It specifies no physical stencil or layer order, and he had
not checked Sanborn's final implementation. [Sanborn's interview](https://www.wired.com/2005/01/questions-for-kryptos-creator/)
describes adapting systems and visual encodings, without a cipher/key/geometry.
The [1991 Scheidt B-roll transcript](https://www.thekryptosproject.com/media/transcripts/pdfs/1991c.pdf)
reports tailored tutorials, without naming the final method. It was transcribed
in 2004. [Sanborn's 1991 transcript](https://www.thekryptosproject.com/media/transcripts/pdfs/1991a.pdf)
separates decipherment from interpretation and allows construction-time changes.
A statistical mask, semantic code, and physical selection mask are distinct models.

## Fixed-primer autokey: 12 models

The Army's April 1950 [TM32-220, section122, printed pp.144–145 / PDF150–151](https://www.nsa.gov/portals/75/documents/news-features/declassified-documents/friedman-documents/publications/FOLDER_238/41748889078809.pdf#page=150)
describes plaintext/ciphertext feedback after a primer. This grounds availability,
not an attested Sanborn lesson. K1/K2's demonstrated alphabet arithmetic and keys
provide the narrow bridge; reusing them for K4 is an inference.

The [frozen specification](../research/specifications/MASK-AUTO-001.json) permits
only two alphabets, three literal primers, and two feedback types: exactly12
complete deterministic outputs. Primer length includes repeated letters. Addition
and sequential inverse subtraction are modulo26 in the same alphabet. There are
no routes, offsets, reversals, alternate equations, free lags, or key searches.
Hand vectors cross the primer boundary twice; all12 planted models must be
recovered by the actual scanner and fail after a known-crib alteration.

## Fractionated Morse: two maps

Sanborn's [construction letter](https://www.thekryptosproject.com/kryptos/cia/letter.php)
identifies International Morse as part of the artwork, without stating a K4 use.
The [ACA procedure](https://www.cryptogram.org/downloads/aca.info/ciphers/FractionatedMorse.pdf)
defines separators, triple grouping and keyword alphabet. The [issue index](https://toebes.com/aca/FullIndex.html)
records Fractional Morse in1950 and a study in1951; the original issues were not
inspected. This is weaker chronology than the Army manual, not an invention-date
or attested-lesson claim.

The [frozen specification](../research/specifications/MASK-FM-001.json) permits
only A–Z and KRYPTOS alphabets over lexicographic dot/dash/x triples excluding
xxx. Use x between letters and xx between words; append only the0–2x needed
for divisibility by3. Decode97ciphertext letters into291ternary symbols, with
strict parsing and no repaired separators. Final English crib positions apply
after Morse decoding and space removal. Require exact re-encoding. The ACA
ROUND TABLE alphabet example is a control only, not a third K4 search key.

## Common acceptance and stopping rule

Use the unchanged97letter baseline and all24crib characters under the usual
97letter final-English working model. No scoring is needed if exact conditions
fail. Commit each specification before implementation/run, retain commit/hash,
use immutable snapshots/deadlines, and report one record per fixed case. A
survivor requires independent audit before further work; it is not a solution.
The complete authorized scope is12autokey cases and2Fractionated Morse maps.

Do not run arbitrary grilles, free97position masks, context-free homophonic
substitution alone, semantic codebook guesses, or extra variants on failure.
