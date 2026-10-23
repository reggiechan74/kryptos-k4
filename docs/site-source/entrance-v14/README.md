# Entrance installation — published Site version 14 source handoff

The Site owner published version 14 before this repository integration. Supplied
source commit: `d4155931cd760d4222c9f66916551110eb40053b`. This archive is saved
on main; no Site deployment or child-checkout change is performed here.

The research checkout contains no complete `candidate/` or `dist/` Site runtime.
As with [version 13](../confirmed-clues-v13/README.md), the exact reviewed patch
and new standalone module are preserved here instead of applying root paths to
an absent baseline. This is a source delta, not a claim of a complete Site snapshot.
The original tests and QA page remain unchanged for replay with that separate
baseline; their relative dist imports are intentionally not fabricated here.

The patch is 139,833 bytes, SHA-256
`c86dab6ac8231ee931f5a602211ffa21921bbfedb19459c632fbc19ee42eacd3`.
Its candidate and dist entrance modules are identical and match the release
manifest SHA-256 `3ebcafcdba599a1a441a1082ba134d55425c82a1af522bc50b0245b2b7ea2d4c`.
[Original handoff](ORIGINAL-HANDOFF.md), [reference ledger](ENTRANCE_REFERENCE_LEDGER.json),
and [verification receipt](../../../results/SITE-ENTRANCE-V14-SOURCE-HANDOFF.json)
preserve provenance separately from this explanatory text. Source photographs
are referenced, not redistributed; their pixel inspection is attributed to the
Site owner, not independently repeated here.

The new illustration shows the entrance granite rose, fixed carved needle and
adjacent lodestone separately from the courtyard screen. Coordinates, spacing,
shape and relief are drawing choices. Engraved N, the carved needle and true north
are explicitly distinct. There is no calibrated magnetic model, surveyed bearing
or new cryptanalytic result. The app diff adds a third mode, pauses existing
animation, hides optical controls in that view and exports its illustrative
state. Index and CSS changes supply the separate panel and responsive controls;
no optical geometry module is changed in the patch. The confirmed-only K4 row
and prior source archive are retained.

Local verification inspected all patch paths and changes, verified module and
archive hashes, and ran three isolated tests for finite accessible drawings,
view/label/reset controls and source links without copied image pixels:

```sh
node --test docs/site-source/entrance-v14/review.test.mjs
```

The Site owner reports 80 full Site tests and Arc previews at 390 px and 1280 px
passing, including front/back aperture tests and unchanged optical geometry.
Those results are attributed, not rerun here because the full Site baseline is
absent. The owner's final live-browser check was blocked by the locked Mac;
native deployment and packaged assets were verified. This integration does not
claim an additional live-browser check or bypass that lock.
