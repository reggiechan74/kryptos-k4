# Source verification and fixture provenance

Verified retrieval date: 18 October 2026 UTC. Earlier failed retrievals remain
part of the history; this record supersedes the initial unread status for the
specific pages below. Download hashes and byte counts are in
[retrieval-hashes.json](retrieval-hashes.json). Full third-party web pages are
not committed. Retrieval does not make every statement on a page correct.

## Controls

- **S4 — [Dunin's sculpture transcription](https://www.elonka.com/kryptos/transcript.html):**
  retrieved directly. Its HTML credits a Douglas Gwyn transcription and Dunin's
  October 2002 hand verification. `data/controls.json` preserves both ciphertext
  panels as displayed rows. This is a specialist transcription, not a new
  photographic survey of the sculpture. Only layout whitespace is removed.
- **S5 — [NSA document 2](https://www.nsa.gov/portals/75/documents/news-features/declassified-documents/cia-kryptos-sculpture/doc_2.pdf):**
  read through the web PDF text extraction, especially PDF pages 5–8. Direct
  download returned HTTP 403. It independently identifies KRYPTOS mixed
  alphabets, PALIMPSEST, ABSCISSA, the K1 spelling anomaly, and the K3 Carter
  passage. Its historical counts and OCR are inconsistent; do not treat noisy
  OCR as an exact machine-readable fixture. Its K3 analytical route differs
  from the rotation workshop. We reproduce the latter, not the NSA's route.
- **S6 — [2006 K2 correction announcement](https://www.elonka.com/kryptos/CorrectedK2Announcement.html):**
  retrieved directly. The ciphertext block agrees with S4's complete K2.
  The announcement reports Sanborn's confirmation of the corrected endpoint.
  Insert S between E and W in the last `EWJLLAETG`, producing `ESWJLLAETG`;
  do not alter the original. The resulting endpoint is `WESTXLAYERTWO`.
  The original decrypts to `WESTIDBYROWS`. Question marks pass through and do
  not advance the key. UNDERGRUUND remains in both variants.
- **S7 — [Dunin's K3 reconstruction](https://www.elonka.com/kryptos/part3.html):**
  retrieved directly. Its complete row-reformatted ciphertext agrees with S4;
  the first displayed physical-row block omits RI in `...RYDLORIT` and is not
  used as canonical. The full displayed plaintext agrees with our independent
  fixed fixture after removing layout and the external question mark.
- **S8 — [K3 worksheet reconstruction](https://www.thekryptosproject.com/tjp/observations/k3_method.php):**
  read via web extraction; describes two clockwise rotations with intermediate
  reshaping. Dimensions are made unambiguous here as rows × columns: 8 × 42,
  then 24 × 14. Its K4 extrapolations are commentator hypotheses. Images were
  not independently transcribed in this run; no physical paper reconstruction
  is claimed. Complete computational comparison, inverse, and unique-position
  tests pass for every one of the 336 positions.

K1 plaintext is fixed independently as the accepted 63-letter string with
IQLUSION, compared against the NSA record and S6. K2 expected plaintext is a
literal fixture cross-checked against S6, not regenerated inside the tests.
K3 retains DESPARATLY and terminal Q. The displayed `?` after K3 is retained as
separate metadata and excluded from the 336-letter permutation.

## Original baseline sources

- **S1 — [Steward K4 page](https://www.paradigm.xyz/kryptos/k4):** retrieved directly.
  Its indexed 97 letters agree with the existing baseline and S4. Crib locations
  also agree with Dunin's reference page. No verifier submission was made.
- **S2 — [Richard Bean, *Cryptodiagnosis of “Kryptos K4”*](https://ecp.ep.liu.se/index.php/histocrypt/article/view/153):**
  metadata and abstract retrieved. Published 9 August 2021; DOI
  [10.3384/ecp183153](https://doi.org/10.3384/ecp183153), CC BY 4.0. The abstract
  discusses permutation tests and a Gromark hypothesis; it does not establish a
  solution. Full PDF downloaded and read using local PDFKit extraction; any partial
  reproduction is recorded separately.
- **S3 — [Paradigm, *Project Kryptos*](https://www.paradigm.xyz/writing/kryptos):**
  retrieved directly; dated 12 June 2026, by Dan Robinson and Matt Huang. The
  steward describes K4 as unsolved and an automated private verification system.
  This page does not itself substantiate the brief's September 2025 archival
  recovery account. The subsequent supplied
  [Firecrawl receipt](../docs/source-verification-2026-10-18.md) records RR Auction’s
  direct account of that discovery. This resolves the brief-only provenance gap
  with an attributed auction-house report, not an independent cryptographic audit.

## Limits

These checks resolve the exact transcription and method gaps needed for the
controls, not every biographical citation in the two supplied research reports.
Their claims about historical source reading and earlier checks remain supplied
research until a specific verification record says otherwise. The 97-letter
K4 and fixed English crib alignment remain working inputs. No claim of new
historical or cryptanalytic discovery is made.

## Supplied Firecrawl research-worker verification

The [dated receipt](../docs/source-verification-2026-10-18.md) records separate
Firecrawl reads by the research worker, including cross-source equality of all
four ciphertext segments, the public crib mask, Gillogly's firsthand account,
the Smithsonian interview, and the archival discovery report. The local coding
executor did not perform that Firecrawl session. Its fixture hashes agree with
the locally retrieved/transcribed fixtures. Paradigm's K3 Vigenère metadata is
erroneous; it is not used as a method source. The Smithsonian matrix-code remark
explicitly concerns already-solved sections, so it supplies no proof of a K4
matrix mechanism. The World Clock clarification is attributed to the official
event video's description, with the receipt's caption/date caveats retained.
