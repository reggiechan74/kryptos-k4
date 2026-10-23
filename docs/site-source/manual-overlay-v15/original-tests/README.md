# Original Site tests and column oracle

[fold-overlay.test.mjs](fold-overlay.test.mjs) and [fold-offline-records.json](fold-offline-records.json) are copied unchanged. Their relative imports expect the separate full Site `dist/` baseline. They were not run from this archive; no missing baseline was invented or imports rewritten.

The Site owner reports the full 87-test suite passed. Repository-local static checks independently compare every field of all 134 embedded column-only oracle records with the retained research result; that is data agreement, not execution of the Site comparison code. Row controls are not a statistical row scan.

[Archive provenance](../README.md).
