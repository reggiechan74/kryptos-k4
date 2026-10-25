# Experiment054 — crib-first exact running-key source lookup

## Result: no exact source match in this frozen corpus

The confirmed plaintext words were used directly to derive two key fragments under each of12fixed tableaux. **No full plaintext guess or candidate-message bank was used.**

The exhaustive lookup returned:

- **0 valid97-letter running-key source windows**;
-0 exact first-fragment occurrences, hence0 correctly spaced fragment pairs;
-0 boundary-rejected pairs;
-89documents,17,627,735normalized letters and17,619,191file-contained97-letter window positions searched under all12variants;
-1,068complete document/model searches, with independent first-fragment and second-fragment search agreement.

This is a **deterministic, bounded corpus exclusion—not a p-value and not a rejection of all running-key ciphers**. Other sources, editions, normalization rules, key-label conventions or cipher layers remain outside scope. The registered stopping rule was reached; no approximate matching, new sources, hypothesis changes or tuning followed.

## Coverage and what is genuinely new

| Collection searched in054 | Documents | Normalized letters | Full97-letter window positions |
|---|---:|---:|---:|
| Pinned NLTK Gutenberg works | 18 | 8,925,568 | 8,923,840 |
| Inaugural speeches through1989 | 51 | 580,690 | 575,794 |
| Additional preselected Project Gutenberg works | 20 | 8,121,477 | 8,119,557 |
| **Total** | **89** | **17,627,735** | **17,619,191** |

There are no identical complete normalized documents in this corpus. Shared passages, quotations and editions are still possible; counts are not independent trials or a claim of uniquely new English text.

The method itself is not new: experiment048 already reported zero exact matches across Brown's500documents/4,745,928normalized letters under six same-axis variants. Its immutable report, results and implementation are identified in `BASELINE_048.json`, at [commit6003dae](https://github.com/reggiechan74/kryptos-k4/tree/6003dae5497ee5a8e53881576776423028205cd7).048uses the same plaintext-axis key spelling for those same-axis models.054adds these source collections and six cross-axis variants; Brown was not downloaded/rerun or counted again. Exact excerpt overlap with Brown was not exhaustively measured.

The20additional works came from a fixed24-ID list chosen before retrieval, independently of Berlin/clock/Kryptos themes. No substitutes were added. Four PG IDs were excluded:12,23,1228had unresolved modern editorial material inside the retained body;5001had no current plain-text download. Nine inaugural speeches dated1993–2025were excluded. All exclusions and original source/date/license receipts are retained.

## Exact test

The known strings are `EASTNORTHEAST` at zero-based21–33 and `BERLINCLOCK` at63–73. Under each variant they imply a13-letter and11-letter key fragment. Search requires their starts to be **42letters apart**, with29unknown letters between them,21letters before the first fragment and23after the second: one complete97-letter key inside one source file.

Plaintext/ciphertext alphabets are independently AZ or`KRYPTOSABCDEFGHIJLMNQUVWXZ`, with Vigenere, Beaufort or variant Beaufort arithmetic. Key residues are spelled using the chosen plaintext-axis alphabet. Other conventions are not silently searched. ASCIIletters alone are retained/uppercased; documents are never concatenated, wrapped, reversed or approximately matched. All occurrences, duplicate editions and boundary failures would have been retained.

| Tableau | First fragment | Second fragment | Valid hits |
|---|---|---|---:|
| AZ–AZ Vigenere | BLZCDCYYGCKAZ | MUYKLGKORNA | 0 |
| AZ–AZ Beaufort | JLJODEGKUKKKL | OCGGBGOKTRU | 0 |
| AZ–AZ variant Beaufort | ZPBYXYCCUYQAB | OGCQPUQMJNA | 0 |
| AZ–KR Vigenere | IRJDHGMIMJAON | SYMLWRQOYBQ | 0 |
| AZ–KR Beaufort | QRTPHIUUARAYZ | UGUHMRUKAFK | 0 |
| AZ–KR variant Beaufort | SJRXTUOSORAMN | ICOPEJKMCZK | 0 |
| KR–AZ Vigenere | QTELWEHGZUPFH | OGHTTKPBKSD | 0 |
| KR–AZ Beaufort | JMWZCUJURLLXV | UCJFBFUJDXD | 0 |
| KR–AZ variant Beaufort | SVICPIFGROWHF | UGFVVKWMKQJ | 0 |
| KR–KR Vigenere | RDUMRIYWOYNKY | ELYOIECBAQK | 0 |
| KR–KR Beaufort | WXAKGZTOAXAFD | RGTGNWRJLFK | 0 |
| KR–KR variant Beaufort | ZJOBZEXPUXAKX | ICXUEILMNSK | 0 |

The machine-readable `results/target_result.json` is authoritative for exact fragments, coordinates and coverage. A full97-letter key/plaintext reconstruction is required for every hit; none exist for this target. Re-encryption would be a correctness check, not independent proof of historical intention.

## Controls and audits

All36planted corpus controls recovered the exact source coordinates, full97-letter key and complete plaintext, with3controls per tableau testing source start/interior/end. All12frozen random-key absent controls returned zero hits. Every control searched the whole corpus and all12variants without an oracle identifying the planted model/source. There were no additional hits or boundary pairs. All48full receipts are included in the compact deliverable.

18synthetic tests cover arithmetic/key spelling, spacing41/42/43, altered cribs, exact/truncated boundaries, cross-document rejection, overlapping/duplicate occurrences, PG marker exclusion, raw-byte offset reconstruction, fail-closed crypto/audit gates, and compilation-boundary qualification. The independent implementation auditor additionally checked240naive synthetic complete-hit sets. Its control audit independently replayed all51,264document/model searches and every planted reconstruction.

Controls are correctness/data tests—not a calibrated probability of aK4match. Crib-preserving noncrib shuffles leave the queried fragments unchanged, so no such invariant shuffle p-value is reported.053language/MDL thresholds were not reused.

Frozen manifest SHA256:
`a126bd9f465ca26e31aee0f307fba461426e19cd66f7c9466e354a8f924c5170`

Controls completed in8.27seconds; the target pass, including source normalization, took2.98seconds. See `implementation_audit.json`, `results/pretarget_gate_audit.json` and `results/target_audit.json` for exactly what was independently checked.

## Historical and access qualifications

The cutoff is historical English-work/translation availability through**1989-12-31**, not an assertion ofK4's exact composition date. E-book upload/update dates were not treated as publication dates. NLTK bracket years are metadata only; library/official evidence supports historical work eligibility. **Exact modern transcription editions were not blanket-certified.** Any future exact passage hit would still require independent pre1990wording/edition verification.

PG205combines *Walden* and *Civil Disobedience* without an established historical compilation date. The transition is frozen as a boundary annotation; any cross-work window would be retained but labeled a modern-transcription candidate with historical adjacency unverified. The generic Blake compilation and other edition details have their own explicit caveats. No target hit exists, so no uncertain historical adjacency is being promoted as evidence.

Source selection was fixed before target lookup. The PG source collector later saw public crib labels/target hash while reading extraction rules, but not ciphertext, derived fragments, scores or prior winners; selection remained unchanged. We do not claim completely blinded source acquisition. Several library metadata sites denied direct HTML; accessible indexed primary catalog evidence was clearly labeled instead of pretending it was a raw page snapshot. Two early PG connectivity smoke-test bodies and HTTP-error bodies were not preserved; the authoritative corpus snapshots and successful metadata/date evidence were preserved and hashed.

Official NLTK and PG public-domain classifications, jurisdiction/trademark caveats and original distribution notices are retained. No external modelAPI, paid checker, Mac/desktop, quota-blocked service, publication or billing change was used.

## Compact reproduction

`ARCHIVE_MANIFEST.json` lists every included payload file. `OMITTED_FILES_INVENTORY.json` accounts for intentionally omitted nonessential acquisition artifacts and any duplicate source archives by exact path,size,hash; all original files remain locally intact. Accepted raw texts, their full original notices, frozen code/config/manifest/control specifications, all48control receipts, complete target result and audits are included. Bibliographic evidence summaries/URLs/hashes are included; omission accounting must not be mistaken for physical verification of omitted bytes.

```sh
python reproduce_compact.py --validate
```

The validator checks included payload/frozen/audit hashes, runs all18tests in a fresh extracted copy, independently reconstructs normalized texts/offset hashes, and deterministically replays all48control searches plus the canonical target search, comparing complete result dictionaries. It performs no acquisition, new-source search, scoring adjustment or approximate lookup. Reproduction outputs go to temporary storage; frozen files are never changed. Validation states exactly which omitted files are not physically present.
