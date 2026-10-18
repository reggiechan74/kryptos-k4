# Historical alphabet source receipt and fixed feasibility scope

18 October 2026. This receipt incorporates the supplied Firecrawl researcher's
historical-source review. That researcher checked unreliable OCR against rendered
primary-source images. The local coding executor separately downloaded the GOST
facsimile, matched its SHA256, read the PDF text, and visually inspected Table 2
on PDF pages 6–7. No private source paths are recorded here.

## Russian romanization

Primary facsimile: [GOST 16876-71](https://files.stroyinf.ru/Data/450/45002.pdf),
official January 1981 reprint incorporating amendments approved December 1973
and March 1980. The effective date is 1 July 1973. Do not assume every 1981
detail appeared in the original 1971 version. Table 2's Russian column is on
printed pages 5–6 / PDF pages 6–7; modifier rules and reprint dates are on PDF p.2.

The exact restricted implementation is frozen in
[gost1981_table2_russian.json](../data/gost1981_table2_russian.json). It accepts
already-uppercase modern Russian letters only. Latin combinations shown in mixed
case in the source are explicitly represented by uppercase Latin labels here;
this restricted-domain convention does not claim recovery of source case.
The table's hard and soft signs remain distinct atomic double-quote and
single-quote marks. A hard sign must not become two apostrophes, which would
collapse it with two soft signs. The ASCII labels are implementation choices,
not a historical digital encoding claim.

The supplied review predicts a uniquely decodable concatenated code: residual
suffix set H/HH, then empty. The fixed test will independently check complete
codeword parsing, all 1+33+1,089+35,937 = 37,060 strings of lengths 0–3, and
exact forward/inverse equality. These are implementation checks, not statistical
support for K4. Dictionary order is enumeration order, not cryptographic evidence.

The restricted table emits 23 Latin letters plus two quote marks. Q/W/X do not
occur. A literal output/permutation model and a fixed individual-transport-
character substitution/permutation model therefore have specific support bounds.
The latter substitution acts on output characters, not whole codewords. A source
apostrophe is explicitly outside the 33-letter domain: Table 2 row 49 encodes it
as an asterisk, admitting a 26th possible output character and defeating the
25-symbol proof. Padding, extra markers, polyalphabetic/homophonic encryption,
and fractionation likewise fall outside that proof. Deleting quote marks is
lossy: Б, БЬ and БЪ all become B. No exact English-to-Russian inverse/codebook,
alignment, cipher, or key is supplied by a romanization standard.

## Shavian

Primary source: [Kingsley Read, July 1963, Guide to Shavian Spelling](https://www.shavian.info/downloads/guide_to_shavian_spelling_1963.pdf).
The research worker inspected its rendered pages: p.1 names the 1962 Androcles
edition as a basis, p.2 distinguishes conventional spelling from sound spelling,
p.3 gives the same Shavian spelling for too/two, and p.4 admits regional and
proper-name pronunciation variants. The entire 1962 edition was not inspected.
These page observations are attributed to that worker; the local executor has
not independently transcribed the glyphs.

The inspected material supplies spelling practice, not a pre-1990 Shavian-to-A–Z
transport table. No such reversible representation was found in this pass.
Unicode order or a modern keyboard is not a historical encoding rationale.
Only the following mathematical gates are admitted: all 48 symbols cannot be
injected into 26 single letters; a uniform two-letter code plus length-preserving
operations cannot give odd length 97 without declared framing; phonemic spelling
alone does not invert conventional English spelling. A message using a smaller
inventory, a multicharacter/framed code, context, or a fixed codebook is a
different model. No Shavian cipher search is specified or authorized here.

## Source provenance cautions

The supplied [ISO/R9 sample](https://cdn.standards.iteh.ai/samples/3587/d548837bae564467a224a5e90b2cc1f1/ISO-R-9-1968.pdf)
is watermarked 1968, but the research worker visually found ISO/R9–1954,
first edition October 1955, on the scan. It cannot ground an exact 1968 table.
The [1972 UN conference paper](https://unstats.un.org/unsd/geoinfo/ungegn/docs/2nd-uncsgn-docs/2uncsgn_econf61_L43.pdf)
supports chronology/discussion of ISO/R9:1968 and GOST, not a substitute for the
1981 code table. Supplied source hashes are retained in the frozen manifest;
only the GOST hash was independently verified locally at this milestone.

The [LANG-001 specification](../research/specifications/LANG-001.json) is to be
committed before implementation/execution. It permits zero cipher-key searches
and no Monte Carlo scoring run. Any future actual cipher search requires a new
committed finite specification with matched synthetic/null controls. These
narrow feasibility results cannot reject an entire language or script family.
