# Construction audit integration bundle

## Contents

- `REPORT.md`: evidence, exact conventions, results, uncertainties and bounded pilot proposal.
- `audit_construction.py`: standard-library-only executable historical regression test.
- `construction_audit_results.json`: completed numerical run with source-byte hashes.
- `derived_alignment_facts.json`: small machine-readable provenance/stage ledger; no full artwork text.
- `test_audit_construction.py`: seven offline algebra/convention controls, no artwork fixtures.
- `validation_receipt.json`: fresh-network, offline replay and deliberate-corruption checks.
- `.gitignore`: excludes downloaded third-party evidence and local generated outputs.

## Run

Python 3.9+; no packages or credentials required.

```sh
python3 audit_construction.py --cache-dir .audit_cache --output local_results.json
```

Re-run without network after the first successful retrieval:

```sh
python3 audit_construction.py --cache-dir .audit_cache --offline --output local_results.json
```

Offline unit controls: `python3 -m unittest -v`. All seven pass in the delivered run.

Expected summary: Projector restart 1,133/1,133; uninterrupted key 777/1,133; K1 local equivalence passes; K2 confirmed deletion passes; canonical K4 reference unchanged.

This is a regression audit of published solved material, not a K4 search. The report proposes a bounded later sensitivity arm; the executable does not generate or rank K4 variants.

Source pages can change or disappear. Layout, length, normalized transcript agreement and canonical K4 checks fail closed rather than guessing. A cached byte hash establishes exactly which retrieval was used; a new page-byte hash need not mean the artwork changed. Inspect normalized text differences before changing any expected values.

## Rights and evidence handling

Do not add `.audit_cache`, downloaded images, complete source pages, or full aligned artwork fixtures to a public repository without reviewing rights. No public redistribution licence was established for them. The bundle contains no such source-page/image/full-text fixtures. Source URLs and reproducibility code replace them.

The worksheet and historical-document images were examined privately and are not necessary for program execution. The numerical script checks their described local algebra, not image recognition. The physical inscriptions were not independently rephotographed during this audit.

The code may be copied into the intended repository for integration. It makes no edits to canonical project files. Its public-source fetches and local cache writes should remain opt-in in CI; do not make ordinary tests depend on external websites. The supplied completed receipt can be inspected offline.
