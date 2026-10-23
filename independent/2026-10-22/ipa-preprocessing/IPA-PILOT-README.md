# IPA preprocessing pilot: source-fixed, bounded results

## Result

The Cambridge US source-normalized glyph form fits the local crib lengths:
- EAST + NORTHEAST: iːstnɔːrθiːst, 13 Unicode code points, 10 segment tokens.
- BERLIN + CLOCK: bɝːlɪnklɑːk, 11 Unicode code points, 9 segment tokens.

The separately frozen 48-structure ordinary-letter-preserving relaxation rejects
all 48 cases. These are Vigenere addition and true Beaufort, each using either
A–Z or KRYPTOSABCDEFGHIJLMNQUVWXZ, for key periods 1 through 12. Each case already
contradicts the known ordinary-glyph anchors. Therefore every assignment of the
six special glyphs fails within those structures. Zero special assignments were
enumerated. For clarity, the first crib alone rejects 47 of the 48 structures
using ordinary anchors. A–Z addition at period 10 is the sole first-crib anchor
survivor, and the second crib rejects it: position 24 s→S gives R−S=25, while
position 64 b→B gives N−B=12. Those positions share the same period-10 phase.
Thus the 48-anchor-only count uses both crib blocks, not only the first. This is not an exhaustive exclusion of IPA preprocessing.

Independent JavaScript and Python implementations agree on every certificate.
Python also passed 48 synthetic encrypt/decrypt roundtrips, 4 mutation-negative
controls, 2 JSON-ASCII roundtrips, and 2 X-SAMPA subset roundtrips.

## Decision chronology and provenance

The source-derived 13/11 glyph-length coincidence was noticed during the source
audit, with the public crib lengths already known. The representation choices
were NOT blind to those public lengths. The two forms, normalization, and first
structural period range were then recorded before their cipher comparison.
The 48-case protocol was subsequently specified and written to its own JSON
before its first evaluation. These cloud records are working pre-test freezes,
not repository preregistration commits. The repository owner should preserve the
protocol in its own prior commit before independent implementation and replay.

Only cloud scratch files and read-only sources were used. No Mac or repository
files were edited. The baseline was read at repository commit
a40e69c510f74e4048403c250fc82010281779aa.

## Fixed source and normalization

Cambridge Dictionary, current US pronunciation:
- EAST: /iːst/
- NORTH: /nɔːrθ/
- NORTHEAST: /ˌnɔːrθˈiːst/
- BERLIN: /bɝːˈlɪn/ (English pronunciation of the German city name, not German)
- CLOCK: /klɑːk/

The frozen segmentation is EAST + NORTHEAST and BERLIN + CLOCK. A later source
check of Cambridge's EAST-NORTHEAST /ˌiːst.nɔːrθˈiːst/ gives the same normalized
stream; it was not tested as another candidate. EAST + NORTH + EAST also has
the same normalized stream. No phrase-level stress variants were optimized.

Apply NFC. Remove stress marks ˈ and ˌ, syllable periods, slash delimiters, word
spaces, and hyphens uniformly. Keep every phonetic letter and every ː length
mark. In the segment-token view, a vowel and its ː form one token; in the glyph
view, ː is a separate code point. Do not swap Cambridge r for ɹ or expand ɝ.

The raw joined transcriptions with lexical stress retained have lengths 15 and
12. The normalized glyph strings have lengths 13 and 11. Their UTF-8 lengths
are 18 and 16 bytes. Their JSON ASCII-escaped payloads are 38 and 36 characters,
excluding the surrounding quotes. These units must not be conflated.

Exact segment arrays:
- [iː, s, t, n, ɔː, r, θ, iː, s, t]
- [b, ɝː, l, ɪ, n, k, l, ɑː, k]

## Assumptions that remain conditional

The public cribs are English orthographic plaintext at one-based positions
22–34 and 64–74. A pipeline in which these disclose an English stage before
phonetic preprocessing is an additional interpretation, not a fact established
by the disclosures. The structural tests additionally assume the transformed
blocks start at unchanged zero-based offsets 21 and 63.

For P = A + EASTNORTHEAST + B + BERLINCLOCK + D, the original block lengths are
21,13,29,11,23. An aligned 97-glyph R2 stream requires |f(A)|=21, |f(B)|=29 and
|f(D)|=23. None is proved because the surrounding English is unknown. Local
13/11 equality alone is not full-message alignment.

For the segment-token form, local lengths 10/9 defeat a one-segment-to-one-letter
model occupying the exact 13/11 windows. A variable-length model is not thereby
excluded. Its transformed starts would be |f(A)| and |f(A)|+10+|f(B)|, which the
English crib indices do not determine. No offsets were shifted or searched.

The 14 observed glyphs fit in a subset of 26, but a one-letter code for every
English phoneme or IPA symbol is not supplied. CMU's primary inventory lists
39 phone types, and ARPABET is not IPA. No CMU-based model was tested.

A phonetic forward model need not be uniquely reversible to be tested. However,
homophones and discarded boundaries prevent promising exact-spelling recovery
without an additional spelling/exception channel. No exact-English inverse is
claimed.

## Outer-cipher relaxation

Fix the ordinary glyph aliases:
i→I, s→S, t→T, n→N, r→R, b→B, l→L, k→K.

Allow every shared injective assignment of ː, ɔ, θ, ɝ, ɪ, ɑ to the 18 remaining
A–Z letters. This is a deliberately generous feasibility relaxation, not a
historical alphabet. At most 18P6 = 13,366,080 assignments per structure would
exist; the first crib uses three specials (18P3 = 4,896).

For each of the 48 structures, derive K=C−P for addition, or K=C+P for true
Beaufort, modulo 26 using the chosen alphabet ranks. A repeated key phase must
give the same K at every ordinary-glyph anchor. All 48 fail this necessary
condition without assigning the specials.

Examples for A–Z addition:
- Period 12: position 22 i→I gives F−I=23, while position 34 t→T gives S−T=25.
- Period 11: positions 22 and 33 give 23 versus 0.
- Period 8: positions 25 and 33 give 2 versus 0.

All phase labels are global ciphertext indices modulo p, not word resets.
No plaintext outside the cribs or complete 97-character candidate was produced.

## Earlier mapping-independent structural test

With no ordinary-letter aliases assumed, repeated-symbol consistency already
excludes deterministic periodic glyph substitutions at periods 1,2,3,4,5,9,10.
Requiring each phase's substitution to be injective also excludes 6 and 7.
Periods 8,11,12 are not contradicted, but have no same-source/same-phase or
same-cipher/same-phase pairs in the known slots. Their pass is vacuous under
that test. The stronger, separately frozen ordinary-alias test rejects them too.

## Standard ASCII contrast, not an additional phonetic search

The Unicode CLDR IPA↔X-SAMPA transform documents:
ː→:, ɔ→O, θ→T, ɝ→3`, ɪ→I, ɑ→A.

Literal conversion of the fixed source glyph strings is:
- i:stnO:rTi:st (13 ASCII characters)
- b3`:lInklA:k (12 ASCII characters)

This case-sensitive ASCII notation is not an A–Z alphabet and does not preserve
both disclosed interval lengths. Uppercasing it or deleting punctuation would
be a new lossy transformation, not standard X-SAMPA. The conversion/reverse on
this observed subset passes; no universal X-SAMPA inversion claim is made.

## Primary source links, retrieved 22 October 2026

- https://dictionary.cambridge.org/us/pronunciation/english/east
- https://dictionary.cambridge.org/us/pronunciation/english/north
- https://dictionary.cambridge.org/us/pronunciation/english/northeast
- https://dictionary.cambridge.org/us/pronunciation/english/berlin
- https://dictionary.cambridge.org/us/pronunciation/english/clock
- https://dictionary.cambridge.org/pronunciation/english/east-northeast
- https://dictionary.cambridge.org/us/help/phonetics.html
- https://www.internationalphoneticassociation.org/content/history-ipa
- https://github.com/unicode-org/cldr/blob/main/common/transforms/IPA-XSampa.xml
- https://github.com/cmusphinx/cmudict/blob/master/cmudict.phones
- https://github.com/cmusphinx/cmudict/blob/master/README.developer
- https://github.com/reggiechan74/kryptos-k4/blob/a40e69c510f74e4048403c250fc82010281779aa/data/k4.json
- https://github.com/reggiechan74/kryptos-k4/blob/a40e69c510f74e4048403c250fc82010281779aa/research/PHONETIC-FEASIBILITY.md

Cambridge's notation guide explicitly states that it uses the International
Phonetic Alphabet. The International Phonetic Association's own history dates
its foundation to 1886 and discusses its 1989 revision. Thus IPA predates K4,
but neither a current Cambridge rendering nor these modern storage formats
establishs Sanborn's historical method or intent.

Cambridge direct web fetches initially returned 403; subsequent Firecrawl
read-only retrievals returned the cited entry contents with status 200. The
CLDR transform was read through the GitHub connector, blob SHA
f52415305bc082ad061bf064206b40367ea6d41b. The UCL X-SAMPA site did not return
usable content; the primary CLDR implementation supplies the exact codec used.
The cloud worker retrieved these sources. The local runner should describe them
as supplied evidence unless it independently retrieves them.

## Replay

Run python3 replay_ipa_pilot.py beside the three JSON files. Standard library
only; no network or installation is needed. The script compares all 48
JavaScript-produced certificates to an independently implemented Python
calculation and runs the controls described above. The known K4 data is pinned
to the supplied repository baseline, not fetched from a changing branch.

Files:
- ipa-feasibility-001.json: base profile, counts, repeat constraints, assumptions.
- ipa-feasibility-001b-spec.json: separately frozen 48-structure protocol.
- ipa-feasibility-001b-results.json: all 48 contradiction certificates.
- replay_ipa_pilot.py: independent Python replay and controls.
- IPA-PILOT-README.md: this report.


## Supplementary first-crib algebraic check (derived after the frozen audit)

This is an additional verification, not a rewrite of the original all24-slot
ordinary-anchor protocol. The original specification and 48 certificates are
unchanged.

The sole first-crib ordinary-anchor survivor, A–Z addition with period 10,
also fails within the first crib if the length mark ː has one global alias:
- Positions 22/32 share a key phase. At 22, i→I and ciphertext F require
  K=5−8=23 mod26. Ciphertext K at 32 then requires alias(ː)=10−23=13 mod26.
- Positions 23/33 share another key phase. At 33, s→S and ciphertext S require
  K=18−18=0. Ciphertext L at 23 then requires alias(ː)=11−0=11.

The same mark cannot have both aliases N (13) and L (11). Combined with the
47 first-crib ordinary-anchor rejections, all48 structures are therefore also
contradicted by the first crib alone once shared-marker consistency is used.
This is distinct from the original result, which rejects all48 using ordinary
anchors across both disclosed blocks. No new method, dialect, period, or
normalization was introduced.

The separate machine-readable certificate is
ipa-first-crib-marker-supplement.json. Run python3 replay_ipa_marker_supplement.py
to verify it. This check was added after the original audit at the parent's
request and is explicitly not represented as originally preregistered.
