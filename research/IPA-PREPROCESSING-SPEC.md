# IPA-PREPROCESSING-001 — bounded pre-fit protocol

22 October 2026 UTC. This protocol is recorded before repository implementation
fits the supplied K4 windows. The parent supplied preliminary period exclusions
and commissioned a separate audit. Necessary fixed-Latin endpoint contradictions
are also apparent from the proposed model, so this is an operational freeze,
not a blinded hypothesis discovery. Source references and independent artifacts
will be imported unchanged when received.

## Inputs and normalization

Use the supplied Cambridge US pronunciations only: EAST /iːst/,
NORTH /nɔːrθ/, NORTHEAST /ˌnɔːrθˈiːst/, BERLIN /bɝːˈlɪn/ and
CLOCK /klɑːk/. The full east-northeast form /ˌiːst.nɔːrθˈiːst/
is a normalization reference for the concatenated first window. Do not change
accent, dictionary, stress convention or spelling in response to results.

Treat slash delimiters as source notation, not phonetic characters. Uniformly
remove stress marks U+02C8 and U+02CC, whitespace and the source's full-stop
syllable separators. Retain the vowel-length mark U+02D0 and every remaining
IPA character. Do not apply transliteration, Unicode case folding or accent
substitution. Work in Unicode code points, not UTF-8 bytes.

R1 consists of the explicitly listed whole phonemic segments, with length marks
attached to their vowels: first window [iː,s,t,n,ɔː,r,θ,iː,s,t], second
[b,ɝː,l,ɪ,n,k,l,ɑː,k]. Lengths are 10 and 9. R2 is the literal normalized
code-point representation: iːstnɔːrθiːst (13) and bɝːlɪnklɑːk (11).
These two representations must not be conflated or adjusted to match lengths.

The unchanged final English disclosures remain EASTNORTHEAST at one-based
positions 22–34 and BERLINCLOCK at 64–74. The operational R2 test assumes their
phonetic windows occupy those same positions in a length-preserving outer
cipher. Local span agreement does not prove cumulative alignment through the
unknown prefix or gap. R1 does not fit those local spans under one-symbol to
one-cipher-letter transport; no padding, shifted indices or inserted symbols.

## A — mapping-independent necessary checks

For R2 at the disclosed positions, check direct deterministic substitution and
one injective substitution per position phase for periods 1–12. A repeated input
must have the same output in its phase; injectivity also requires equal outputs
to have equal inputs. Record every repeated-symbol or equality contradiction.
Passing these necessary checks is not a cipher solution or evidence of intent.

## B — two Latin-coordinate alphabets and all relaxed aliases

Fix ordinary IPA Latin symbols to uppercase identities:
i→I, s→S, t→T, n→N, r→R, b→B, l→L, k→K. These identities apply globally.
The first window adds three special symbols, in fixed parameter order ː, ɔ, θ.
The second introduces ɝ, ɪ, ɑ. The union is fourteen disclosed symbols, not a
universal encoding of the IPA inventory into A–Z.

Test outer alphabets AZ and KRYPTOS, equations C=P+K and C=K-P modulo 26,
and unrestricted periodic keys of lengths 1–12. There are exactly 48 formal
structures. Key phase and an additive key-sign reversal are redundant and do
not add trials. No dictionary keys, routes, resets or alphabet reorderings.

First allow each first-window special symbol every A–Z value independently,
including collisions: 26^3 assignments per structure. This is a necessary
relaxation containing the injective domain. Eliminate key slots by same-phase
differences, solve the resulting three-variable equations exactly modulo 2 and
13 with CRT, and retain the complete affine solution sets, singular cases and
free parameters. Independently compare complete relaxed assignment sets against
a tiny exhaustive enumerator or an independently expressed all-pairs checker.
A contradiction in the relaxation excludes the injective subset too.

If a relaxed structure survives, require its first three aliases to be mutually
distinct and distinct from all eight fixed ordinary letters. Preserve every
compatible alias assignment and its key; do not select one attractive mapping.
The first thirteen positions cover every key slot at all tested periods, so the
key is fixed conditional on an alias assignment, but aliases may remain free.

Check Berlin only for surviving first-window mappings and keys. Its three new
aliases are new fitted choices, not independently predicted letters. Report
conditional predictions at the eight positions whose symbols were already
specified, plus compatibility and degrees of freedom for the new aliases;
retain correlations across whole assignments rather than choosing separate
witnesses per position. Never report an underidentified full plaintext.

## Controls, budget and stopping

Use deterministic synthetic literal R2 windows at positions 22–34 and 64–74;
retain the disclosed English labels separately. Plant injective maps and periodic
keys across both equations, alphabets and all twelve periods. Complete-selector
controls require truth inclusion and correct multiplicity, not assumed unique
recovery. Check independent encrypt/decrypt round trips, noninjective-alias
controls, Unicode normalization/length mutations and exact contradiction
certificates. Use the existing exact modular solver and provenance conventions.

Finite budget: one process; 120 seconds for the actual 48-case run, 300 seconds
for controls, at most 256 MiB of retained results. If exceeded, label unresolved
rather than reject. If every relaxed case fails, stop without Berlin alias
fitting, significance simulation, extra periods or dialect changes. If anything
survives, report compatibility and identifiability; no positive K4 claim or null
significance claim without a separately frozen matched calibration.

This model is separate from earlier respelling, Shavian-transport and fixed
phonetic-mask checks. Sound-to-English-spelling reconstruction is not generally
unique; this partial representation does not solve that inverse problem.
