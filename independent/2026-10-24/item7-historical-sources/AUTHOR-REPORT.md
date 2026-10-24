# K4 item 7: authenticated historical sources and source gates

Checked 24 October 2026 UTC. Scope: H-M138A, H-WHEATSTONE/Pletts, H-BOOK-CODEBOOK, H-EGYPTIAN-SIGN-LIST, H-GERMAN-TRANSLATION. Repository baseline inspected at main tree `8ba613df2549f3ab7b111923094397722d66586c`: `research/HYPOTHESES.md`, Wheatstone transition report/source ledger, Egyptian feasibility, and research frontier. No item 8 work or new K4 key search was performed.

## Result

1. **New authentic historical evidence is available.** A 1935 M-138 patent draft supplies a photographic worked example and 24 completely legible numbered strips. Its remaining strip has an unresolved O/Q glyph, so it does **not** authenticate a complete inventory, and it is the 25-strip M-138, not a 100-strip M-138A set.
2. **A primary Army operating rule supports an inventory-independent boundary.** SRH-366 quotes the July 1943 SIGUHR-2 ban on zero/26 column displacement. A direct, aligned, nonzero cyclic-strip encryption cannot map a letter to itself, whereas K4's confirmed position 74 is K→K. This is a conditional structural exclusion, not a search result or a rejection of layered/adapted strip families.
3. **An independent historical Wheatstone vector was recovered and replayed.** REFERENCE→XZAABGQAM, start G/A. It validates the existing fixed-ring abstraction, not a distinct Pletts operation. The original source has a conflicting forward-line typo and one unused occluded ring slot, both preserved below.
4. **No inspected creator evidence selects a reproducible book, Egyptian-sign, or German intermediate mechanism.** These remain uninstantiated, not disproved. No invented keys, repaired alphabets, or convenient editions were admitted.

## A. M-138 and M-138A

### A1. Original M-138 photographic vector

Primary source: William F. Friedman, *Draft Specifications for Basis of Patent Application on Cipher Device Type M-138; SISDE 15 and 16*, draft dated 5 July 1935, NSA metadata dated 6 July 1935. NSA A67592, Folder 084, accession 47270, 22 PDF pages.

[Official NSA PDF](https://www.nsa.gov/portals/75/documents/news-features/declassified-documents/friedman-documents/patent-equipment/FOLDER_084/41702569074189.pdf)

- PDF page 4 specifies the strip order and message. PDF page 16, Figure 4, independently displays the aligned plaintext column and right reading-guide edge.
- Numbered strips, top to bottom: `14 16 9 6 22 25 23 5 12 24 13 21 18 1 7 17 20 19 15 8 11 2 3 10 4`.
- Plaintext, first 25 letters: `ACCORDINGTOANOFFICIALREPO`.
- Photographic ciphertext: `VMIZK KJGFC DWVMK HYYXI ATMCC`.
- Ungrouped ciphertext: `VMIZKKJGFCDWVMKHYYXIATMCC`.
- Under the photographed left-to-right alphabet orientation, every displayed pair has cyclic offset +15. This arithmetic was checked after independently transcribing both columns, not used to choose them.

Source limitations matter:
- Strip 1 visually reads `KUYJWSALPVBIMGOCXNFZEHROTD`: both one-based positions 15 and 24 are O-like, leaving Q unresolved. The photographed O→M pair uses position 24 and is consistent with +15; it cannot authenticate the other glyph. Do not silently replace the first O by Q.
- All other 24 rows were visually cross-checked across repeated source photographs and independently pass the 26-unique-letter check. Full rows and pair ledger are in `K4-ITEM7-M138-VISUAL-CHECK.md`; machine-readable data are in `item7-historical-sources/visual-transcription.json`, expressly marked incomplete.
- The typed cipher groups on PDF page 5 are struck out. The admitted ciphertext comes from the Figure 4 pixels, not repair of that line.
- This original 25-strip illustration is not an authenticated wartime 100-strip M-138A inventory. It does not establish a set selected for Kryptos.

Operational model supported by the draft: put the agreed numbered strips in the holder, slide each to align a block of plaintext, select another parallel column, and read its letters in strip order. The receiver aligns ciphertext and searches the other columns for readable text; the offset is not transmitted in this example. A software decoder must expose the finite candidate rows unless a row is supplied, rather than assuming a mathematically unique English reading. Preserve the draft's occasional textual numerical errors rather than using them as operational authority over the figure.

### A2. Genuine M-138A operating variants

Primary source: *Resurvey of the Cryptographic Systems of the Department of State*, 14 January 1944, NSA A67293, Folder 467, accession 47270, Enclosure B printed page 4 (PDF page 14).

[Official NSA PDF](https://www.nsa.gov/portals/75/documents/news-features/declassified-documents/friedman-documents/reports-research/FOLDER_467/41731179077042.pdf)

Visually authenticated:
- Straight board: 30 strips, one ciphertext column.
- Split board: first 15 and second 15 use different columns.
- Channel elimination: five strips omitted for a message part.
- Different strip sets were issued to different holders, and sets changed monthly. Common numerical key lists did not imply a universal alphabet inventory.

This is authentic procedural evidence, not a complete strip set or worked M-138A KAT. A materially specified experimental model must still identify the exact issue/set, selection/order, block/channel policy, and offset policy.

### A3. Primary nonzero-column rule and its exact K4 implication

Primary historical record: US Army Security Agency, *The History of Army Strip Cipher Devices (July 1934–October 1947)*, SRH-366, declassified scan. Archive item `ticom`, original PDF 310 pages. Relevant printed pages 83–84 are physical PDF pages 101–102. Page 83 identifies SIGUHR-2 as effective July 1943; page 84 continues its quotation: “Intervals of zero and of twenty-six must never be selected.” Both pages were visually inspected. This is a distinct public archival source, not the previously denied maritime manual.

[Public archival scan](https://archive.org/download/ticom/Srh-366UsArmyStripCiphers1934-1947.pdf)

For a valid 26-letter strip permutation s and displacement d, the direct operation is:

`C[i] = s[(index_s(P[i]) + d) mod 26]`.

If `d mod 26 != 0`, then `C[i] != P[i]`, independent of the strip's alphabet, strip order, direction, or choice of nonzero offset. Consequently the confirmed aligned K4 position 74 (`P=K`, `C=K`) excludes this direct nonzero-shift model without acquiring its inventory. Different strips, straight/split boards, channel elimination, or changing nonzero offsets do not by themselves evade the per-character fact.

**Boundary:** this does not exclude zero-shift adaptations, preprocessing that changes crib alignment, an extra substitution/transposition layer, non-permutation/duplicated-symbol strips, or another historically modified mechanism. The evidence selects a documented operating rule, not a historically selected K4 procedure. This is related to the repository's existing cyclic-permutation/M94 invariant and should not be counted as a new brute-force family sweep. Do not apply it to the unresolved literal strip transcription as though that transcription were a valid permutation.

## B. Wheatstone/Pletts

Primary testimony: William F. Friedman, lecture VI, *The Friedman Legacy*, official NSA third printing 2006, printed pages 141–146; figure 112 and reverse example on page 144. The foreword identifies the original lecture series/publication history. Physical PDF pages 152 and 155 display the conflicting strings.

[Official NSA PDF](https://www.nsa.gov/portals/75/documents/resources/everyone/digital-media-center/video-audio/historical-audio/friedman-legacy/friedman-legacy-transcript.pdf)

Reproducible historical vector:
- Outer clockwise ring: `_ABCDEFGHIJKLMNOPQRSTUVWXYZ` (`_` is space).
- Initial outer/plain pointer: G. Initial inner/cipher pointer: A.
- Inner clockwise from A: `AGMUCIP?EJQXFBKSYNHOVRDLTZ`.
- Plaintext: `REFERENCE`.
- Ciphertext: `XZAABGQAM`.
- Clockwise step sequence: `11,14,1,26,13,14,9,16,2`.
- Visited inner zero-based indices: `11,25,0,0,13,1,10,0,2`.

The long hand advances in the same direction to the next plaintext symbol, moving both pointers by the same number of symbol positions on their unequal rings. Inverse replay advances positively to each successive ciphertext symbol. Both forward and inverse traces pass.

Caveats:
- The hand occludes inner index 7. W is the unique completion if it is an A–Z permutation, but none of this vector's positions visits that slot. Use `?` in source transcription; do not label the completed ring entirely pixel-verified.
- Printed page 141 actually says `XZZZBGQAM`. Page 144 says `XZAABGQAM`, which agrees with figure 112 and the procedure. This is a source typo, not OCR uncertainty.
- The example exercises a repeated ciphertext letter from a 26-step movement; it does not test repeated plaintext, word-space preparation, or a Pletts-specific rule.

Friedman's account of the British modification describes a single hand/window and both alphabets mixed, still fixed-ring gearing. An authentic [IWM Pletts object, COM 476](https://www.iwm.org.uk/collections/item/object/30005261) confirms the physical device and inventor but provides no distinct full operating instructions or KAT. [Beeman's original patent US801964A](https://patents.google.com/patent/US801964A/en) supplies a related, differently sized mechanism, not a Pletts attribution and complete outside-invariant vector.

Disposition: retain the repository's fixed-ring transition exclusion. No authenticated stateful/hidden-move Pletts escape was obtained; that broader possibility remains source-gated, not universally false. Detailed evidence and access log: `K4-ITEM7-PLETT-SOURCE-CHECK.md`. Standalone source-only replay: `item7-historical-sources/friedman_reference_source_qa.py`; trace: `friedman-reference-source-qa.json`.

## C. Independently selected book, Egyptian, or German source mechanism

- [Smithsonian's primary Sanborn oral history](https://www.aaa.si.edu/collections/interviews/oral-history-interview-jim-sanborn-15700) attests Carter notebooks and Schliemann's Troy as favorites, including ownership of an original late-1800s Schliemann copy. It supplies neither the exact relevant edition nor K4 extraction. A [Carter first-edition auction lot](https://www.rrauction.com/auctions/lot-detail/350816407302005-howard-carter-signed-book-set-the-tomb-of-tutankhamen/) does not identify that copy as his construction source or key.
- [Sanborn's 12 November 2025 letter](https://www.documentcloud.org/documents/26229389-adobe-scan-nov-12-2025/) was partially retrieved as indexed OCR, not visually authenticated scan. It supplies Egypt/Berlin/message-delivery context, not one of these mechanisms. Conflicting chronology in related sources remains unresolved, not key material.
- [Scheidt's primary 2005 interview](https://www.wired.com/2005/01/inside-info-on-kryptos-codes/) says all four messages are English, while noting he did not inspect Sanborn's final alterations. This does not select a German intermediate or strictly disprove every reversible intermediate representation.
- [Sanborn's primary 2005 interview](https://www.wired.com/2005/01/questions-for-kryptos-creator/) confirms earlier-text instructions for later text without disclosing an extraction, and [PBS NOVA Q&A](https://www.pbs.org/wgbh/nova/article/sanborn-puzzle/) supplies artistic preferences rather than a selected sign inventory.

All three remain **uninstantiated pending independent model selection**. Minimum gates: exact creator-linked source/version; exact traversal/mapping/normalization; deterministic inverse; all keys/offsets; and preservation or specified transformation of confirmed crib alignment. Egyptian transcription must address multiconsonant signs, vowels, reading direction and ambiguity. German translation needs a fixed rendering and lossless inverse/alignment, not interpretive back-translation. Full source limitations and missing-variable lists: `K4-ITEM7-CREATOR-SOURCE-CHECK.md`.

## D. Provenance, exclusions, and stopping point

The source directory contains originals, visual crops, machine-readable transcription, replay, and `SOURCE-MANIFEST.json` with URLs, byte counts, SHA-256 hashes and inspected pages. The full SRH-366 file was downloaded, but only targeted relevant pages were visually inspected; this is not an exhaustive census of every archival page or strip issue.

Modern MysteryTwister/Schmeh 100-strip examples explicitly use a fictitious set and were not admitted as historical. A modern photo reconstruction gives only 29 strips and no complete authenticated issue identity. Secondary archival leads point to NARA RG457 Entry9032 Box214 and RG59 119.25/Strip Cipher, but no complete versioned alphabet set was retrieved from them.

Access restrictions respected: no repeat or alternate-route request for the previously denied maritime manual, eprint paper, or Google Books PDF. The new Davies publisher endpoint returned an Access Denial shell, and the Cambridge Wheatstone chapter explicitly lacked full access; neither was bypassed or retried. An isolated search snippet about an extra turn was not admitted as an operating instruction. No paid retrieval, outreach, CAPTCHA, account access, or new K4 key search occurred.

**Item 7 research is complete at the present evidence gate.** Implementable gains are the caveated historical Wheatstone KAT, the M-138 photographic vector/24 verified strips as source QA (not a complete cipher inventory), and the primary-sourced conditional nonzero-column certificate. A full authentic M-138A inventory, a distinct Pletts operation with external vector, and creator-selected book/Egyptian/German mechanisms remain missing.
