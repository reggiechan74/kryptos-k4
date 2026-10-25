# Bounded PG source acquisition for experiment054

This directory contains only the fixed24source-ID acquisition and bibliographic/license evidence. No target-derived fragment lookup, ciphertext scoring, source ranking, or normalization was performed by the source agent.

## Outcome

-24official catalog snapshots;23official current plain-text snapshots, totaling12,768,609raw text bytes.
-20proposed historically eligible works;4exclusions:12,23,1228,5001.
-12: unresolved Millennium Fulcrum Edition1.7 material inside the body.
-23:1992electronic-release note inside the body.
-1228: modern PG edition-selection notice inside the body. This ID is the1859first edition, not the1872sixth edition.
-5001: current catalog and linked directory have no plaintext format; canonical plaintext returned404. No substitution, HTML conversion, or old-file retrieval.

Authoritative input: `corpus_manifest_draft.json`. All20eligible statuses mean ready for independent source audit, not proof that every character of the modern transcription existed before1990. Exact PG print source is often unidentified. Every potential matching passage would require separate historical collation. The bundled Walden/Civil Disobedience file contains two historic works; their modern combined-file boundary is not proof of historical adjacency.

## Preservation and evidence

`raw/` contains untouched official corpus downloads and per-file HTTP/hash receipts. `metadata/` contains untouched official PG catalog bytes, receipts, and original failed linked-URL acquisition logs. `evidence/` contains primary institutional evidence downloaded as bytes where available, labeled web-tool-mediated indexed evidence where direct access failed, and bibliographic body inspection results. `source_snapshot_inventory.json` lists saved raw/metadata/evidence file hashes and sizes.

Two initial connectivity smoke-test bodies for PG1342were read before persistence scripts were created and were not saved. The later authoritative snapshots are saved and hashed. HTTP-error response bodies were not captured, but their URL/status/error details were retained. The National Library of New Zealand raw200response is a challenge page, not date evidence; its cited indexed official catalog record supplies the date evidence instead. Several library sites returned403to direct raw retrieval; no access-control bypass was attempted.

The source agent later opened the parent protocol to check source rules and encountered known-plaintext labels and a target hash. It did not read/derive target key fragments or ciphertext, consult scores/winners, or query sources cryptographically. The24IDs were already fixed and downloaded before that limited protocol exposure; no source selection changed.

## Proposed extraction contract

Read bytes; require exactly one complete conventional PG START line and exactly one following END line. Retain only bytes after START's newline and before END's beginning. Fail closed on missing, reversed, or ambiguous markers. Retain all historical frontmatter, headings, footnotes and appendix material within those bounds. Do not remove individual modern notes; the three affected files above are excluded in full. Do not concatenate documents. All23downloaded texts passed unique-marker inspection. Central code owns ASCII-letter uppercasing and reversible offsets; this agent did not perform normalization.

## License record

Each official catalog states US public-domain status. Complete PG license, permission and terms snapshots are preserved in `evidence/`. The public-domain text and PG trademark/compilation/license conditions are distinct. Raw downloads retain their full supplied license. No redistribution or publication was performed or authorized. Users outside the USA must check applicable local rules as stated by PG.

## Scripts and reproducibility

`acquire_pg.py` records the initial linked plaintext endpoint failures; `fetch_canonical.py` acquires the official current cache plaintext snapshots. `evidence_fetch.py` records raw evidence successes/failures. `build_manifest.py` builds the initial draft and `finalize_manifest.py` attaches evidence hashes and final provenance qualifications. Do not rerun acquisition expecting byte-identical future PG snapshots: the saved SHA256values define this snapshot. No packages were installed.
