# New overlay source modules

These four files are unchanged copies of the patch’s new `dist/fold-overlay/` modules; the candidate copies are byte-identical. They are a delta, not a full Site runtime. Local checks parse data and inspect bytes without executing this JavaScript.

- [core.mjs](core.mjs): state validation, source coordinates, no-wrap translations and comparison/export logic.
- [data.mjs](data.mjs): pinned research transcript and approximate glyph dictionary.
- [module.mjs](module.mjs): manual controls and explanatory UI.
- [view.mjs](view.mjs): SVG presentation.

[Archive provenance and limitations](../README.md).
