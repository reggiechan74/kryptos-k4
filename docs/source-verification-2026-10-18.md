# K4 source verification through Firecrawl

Verified 2026-10-18, 02:52–02:56 UTC. All source reads below used the connected Firecrawl scraper and returned HTTP 200. This file records verification results, short excerpts and essential cipher data; it does not reproduce complete articles or the Smithsonian interview. No paid solution submission, account action, or external write was performed.

## Immediate conclusions

- **K4 remains publicly unsolved cryptanalytically in the latest verified steward publication.** Paradigm's project article, published 2026-06-12 and last modified 2026-09-14, still calls it unsolved. This is compatible with archival plaintext recovery in September 2025; discovery of plaintext is not recovery of the encryption method or key.
- **K4 is exactly 97 letters.** The 97 numbered letters on Paradigm match the last 97 letters in Elonka's sculpture transcription, byte-for-byte.
- **K1–K3 ciphertexts also match byte-for-byte between the two sources.** Keep punctuation-aware raw transcription separate from A–Z-only cipher inputs.
- **Important source error:** Paradigm's K3 page metadata says Vigenère. Do not repeat that classification. Gillogly's firsthand 1999 account identifies columnar transpositions.
- **Important correction:** Canonical K2 as carved is different from the corrected reconstruction. Keep both variants explicitly labeled.

## Source receipts

### 1. Current steward and verifier

URL: https://www.paradigm.xyz/writing/kryptos

Title: Project Kryptos. Authors in metadata: Dan Robinson and Matt Huang.

Publication metadata: 2026-06-12T18:00-07:00. Modification metadata: 2026-09-14T15:23:51.022Z.

Firecrawl scrape ID: 01a14ced-522d-7684-bd86-a97ada891034.

Short exact excerpt: “But it's still unsolved.”

Verified: Paradigm became steward of the private Kryptos archive. Its verifier uses the plaintext supplied by Sanborn. The page describes SHA256 followed by a Google Cloud KMS HMAC and says the plaintext did not leave the entry device. A submission costs $1. It announces a separate K5 ciphertext of 97 characters for future release. The ten $1,000 CTF puzzles are a separate challenge; the Q&amp;A offers no cash prize for solving K4.

Caveat: These are publisher claims, not an independent audit of the verifier or proof that nobody privately solved K4. We did not submit a candidate.

### 2. K4 numbered ciphertext

URL: https://www.paradigm.xyz/kryptos/k4

Title: Kryptos K4 | Paradigm. No article publication date returned.

Firecrawl scrape ID: 01a14ced-424e-70c6-9ac1-d0a2ad8df832.

Short exact metadata excerpt: “97 characters, unsolved for 35 years.”

Verification: Parsed one letter at every consecutive index 1–97. Exact normalized ciphertext:

```text
OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR
```

ASCII SHA256, no newline:
`eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab`

Caveat: The scraped page exposed a “Show Hint” control but not its interactive hint content. The clue positions below were independently recovered from Elonka's published 97-character mask, not inferred from this control.

### 3. Full sculpture transcription

URL: https://www.elonka.com/kryptos/transcript.html

Title: Transcript of Kryptos Sculpture. No publication/modification date returned.

Firecrawl scrape ID: 01a14ced-807c-75a5-b605-cfbaabba65c2.

Verified: The page contains two ciphertext panels and the tableau. Only the ciphertext panels were used for comparisons; tableau letters must not accidentally enter corpus extraction. The upper-left panel is K1+K2; the lower-left panel is K3+K4.

Exact cross-source comparison results after removing layout whitespace:
- K1: 63 characters, all letters.
- K2 as carved: 372 characters, consisting of 369 letters and three question marks.
- K3 raw segment: 337 characters, consisting of 336 letters and the trailing question mark before K4.
- K4: 97 letters, begins OBKR, ends EKCAR.

Each segment matched the corresponding Paradigm page exactly. The question mark immediately before OBKR is not part of the 97-letter K4 solver input.

Additional independent page receipts:
- https://www.paradigm.xyz/kryptos/k1 — scrape 01a14cee-7934-755a-a46d-0c009df74a40
- https://www.paradigm.xyz/kryptos/k2 — scrape 01a14cee-98dc-753a-9e4d-2f68e38dea8f
- https://www.paradigm.xyz/kryptos/k3 — scrape 01a14cee-8a1a-75a3-9237-50bb27faccae

### 4. K4 public crib locations

URL: https://www.elonka.com/kryptos/

Title: Elonka's Kryptos Page. The unsolved-status section explicitly says August 2025; do not use it alone as current status evidence.

Firecrawl scrape ID: 01a14cee-15b6-768a-872b-9bd91a0dc5f0.

The published clue mask has exactly 97 characters after removing layout whitespace. Computed, 1-based inclusive positions:

| Positions | Ciphertext | Plaintext |
|---|---|---|
| 22–25 | FLRV | EAST |
| 26–34 | QQPRNGKSS | NORTHEAST |
| 64–69 | NYPVTT | BERLIN |
| 70–74 | MZFPK | CLOCK |

The page dates BERLIN to November 2010, CLOCK to November 2014, NORTHEAST to January 2020, and EAST to April 2020 correspondence approved for public release in August 2020. These supply 24 fixed plaintext letters. They constrain candidates; matching them is not proof of a solution.

### 5. K2 correction and calibration warning

URL: https://www.elonka.com/kryptos/CorrectedK2Announcement.html

Title: Kryptos Part 2 Was Wrong. Dateline: April 19, 2006.

Firecrawl scrape ID: 01a14cee-ab7e-743e-81aa-10a2b088fe89.

Short exact technical fragments: “EWJLLAETG”, “EsWJLLAETG”, “IDBYROWS”, “XLAYERTWO”.

Verified: The group reports Sanborn confirmed the corrected ending. Insert S between E and W in the final EWJLLAETG to restore key alignment. The reconstructed K2 has one more letter than the carved transcription. The source specifies a keyed-alphabet Quagmire III variation, KRYPTOS alphabet key and ABSCISSA indicator key.

Implementation consequence: Preserve the original ciphertext, add a separately named corrected variant, and test both intended behavior and historical output. Do not silently insert S in the canonical-as-carved file. Keep original spelling peculiarities when calibrating plaintext.

### 6. Firsthand historical solve classification

URL: https://www.elonka.com/kryptos/mirrors/cypherpunks/1999/0930.html

Mirrored June 16, 1999 messages, including Jim Gillogly's own explanation.

Firecrawl scrape ID: 01a14cef-2b43-76c1-a4a1-8b860a077047.

Short exact excerpt for K3: “Keys: three columnar transpositions.”

Verified: Gillogly gives KRYPTOS/PALIMPSEST for K1, KRYPTOS/ABSCISSA for K2, and transpositions for K3. This is firsthand evidence against Paradigm's erroneous K3 Vigenère metadata. The mirror predates the 2006 K2 correction and therefore includes the historical ID BY ROWS ending.

### 7. Smithsonian oral-history interview

URL: https://www.aaa.si.edu/collections/interviews/oral-history-interview-jim-sanborn-15700

Title and required citation: Oral history interview with Jim Sanborn, 2009 July 14–16. Archives of American Art, Smithsonian Institution. Interviewer: Avis Berman.

Firecrawl scrape ID: 01a14ced-63f9-73ac-8edc-da153c07fd5f.

Short exact excerpt: “These are the parts of Kryptos that have already been cracked.”

Verified relevant passages:
- Near the interview's [01:24:00] section, Sanborn describes Scheidt teaching older and more contemporary systems, and Sanborn wanting methods that did not necessarily require mathematics. He explicitly limits the matrix-code discussion to already-solved portions.
- Near [01:26:00], Sanborn describes cutting English sentences into strips, rearranging them, and gluing them to pages for a CIA content review. This independently explains why sentence-fragment plaintext documents could exist in an archive.
- The final [01:20:00] segment discusses plain-text copyright, K4's unresolved status at interview time, and meaning extending beyond the sculpture.

Caveats: Timestamp numbering restarts across interview recordings. This is a 2009 historical source, not evidence of current K4 status or the 2025 archive discovery. Do not promote “matrix codes” or “nonmathematical” remarks into a proven K4 cipher constraint. This interview contains no Berlin-clock clue; those disclosures came later. It is not the later papers collection in which plaintext fragments were found.

### 8. Archival discovery versus cryptanalysis

URL: https://content.rrauction.com/kryptos-k4-discovered-not-solved-heres-what-actually-happened/

Title: Kryptos K4: Discovered, Not Solved—Here's What Actually Happened.

Publication: 2025-10-23T14:59:36+00:00. Modification: 2025-10-23T15:00:21+00:00.

Firecrawl scrape ID: 01a14cee-0022-736e-b167-b971f08dce0d.

Short exact excerpt attributed to Sanborn: “K4 has not been solved. K4 has been discovered and it points in the direction of K5.”

Verified: RR Auction reports that Jarett Kobek and Richard Byrne found five pages of scrambled text in September 2025 and used public clues to reconstruct plaintext. The source says they did not acquire the encryption method/key and did not intend to publish the plaintext.

Caveat: RR Auction had a commercial interest in the sale. Use its direct quotations and discovery/method distinction with attribution; do not adopt every promotional claim as an independent technical fact.

### 9. Official November 2025 clue clarification

URL: https://www.youtube.com/watch?v=QTGcaCPIYl4

Title: Jim Sanborn Reveals New Kryptos Clues Ahead of Auction — K4 and K5 Explained.

Publisher: RR Auction Official. Upload metadata: 2025-11-14T07:52:28-08:00.

Firecrawl scrape ID: 01a14cef-7e9e-7634-891f-c62792d91217.

Short exact description excerpt: “Why ‘BERLINCLOCK’ refers to the World Clock in Berlin” (quotation marks normalized).

Verified: The official event-video description specifies World Clock in Berlin, references the Egypt trip and Berlin Wall fall, and describes K5 as a surviving alternate ending. The transcript reiterates that scrambled plaintext was found without the coding method/key.

Caveats: The exact World Clock clarification was in the publisher's description, not the returned spoken transcript. Automatic captions contain spelling errors. This receipt does not independently establish the Egypt trip's exact year; do not cite it alone for “1986.” A Berlin clock model used in a search should distinguish this World Clock clarification from older speculative choices.

## Reproducible hashes for fixtures

These are SHA256 hashes of uppercase ASCII ciphertext without whitespace or a final newline. “Raw” retains question marks; “letters” removes them. The hashes were computed locally from the retrieved strings after exact cross-source equality checks.

| Part | Raw length | Letter length | SHA256 raw |
|---|---:|---:|---|
| K1 | 63 | 63 | 0da44afce6ff53845dee12a15f164036b598fcf40b6c0b3edc83996053c4e2fc |
| K2 as carved | 372 | 369 | 385bb27d230b5e903ba04b1256cd1a66f10c5dcc0f4f300b6b89f5879eaa714f |
| K3 with trailing ? | 337 | 336 | ab2efc0bf304377f0ea6dd24ed1697f29161407d3e6bb6283ac2cb5538315bb9 |
| K4 | 97 | 97 | eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab |

A–Z-only K2 SHA256:
`4118a78c60a6335c30c7fc2946f6c71fd6c2828fd550ea647c3b713313c0f9ff`

A–Z-only K3 SHA256:
`db8807dfc8354a42dc2f52aed3f0b54ac938873372c6b504b4c8d69fdfc85c35`

## What this verification does not establish

No candidate K4 plaintext was validated. No unverified online “solution” was adopted. No proof of K4's cipher family, number of layers, key length, or role of K1–K3 follows from these sources. Clue compliance, English-like text, or a high language score is insufficient: a defensible solve needs a reproducible method and authoritative verification.
