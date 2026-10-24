# Item 3 — historical World Clock registration and phase

**The partial inventory does not determine a joined historical ring, an intended time or an A–Z cipher bridge.** This study quantifies that ambiguity instead of choosing convenient city placements. Fresh parent source research is pending; this draft is not yet finalized or published. No Mengenlehreuhr or item 4 work.

## Actual finite work and chronology

[Frozen specification](WORLD-CLOCK-003-SPEC.md) committed at `53aa67b86da286d45012d957a25b4763c77ab04f`; [implementation](../experiments/world_clock_003.py) committed before the original run. Original calculation **2026-10-24T00:29:46.751515+00:00 → 2026-10-24T00:29:46.860170+00:00**. [Complete original output](../results/world-clock-003/20261024T002946Z-c05cd21588cd43878a866f2fa1a99cb2/registration-analysis.json) includes all 576 offset pairs, every rejection witness and all 820 unordered observation-pair domains. The adjacent manifest pins hashes. Source input SHA256: `57869e45e24299d04df68b3452f38e7c3d094b91fa1df8cbc160871baf6c9205`.

The [retained evidence](../independent/2026-10-22/historical-clock/README.md) contains 41 literal label observations on ten local panels in three dated segments: EU1969, AM1970 and AS1984. Seventeen sector/band cells hold these labels. Dates and raw spellings remain unchanged. The input retains its provisional single-reader status and original independent-review flags; numerical compatibility does not independently validate the photographic transcription. No admitted observation has a verified 1989 continuity claim or semantic civil UTC offset. Unknown bands are not empty; BERLIN's recorded upper rank is two, and SANTIAGO DE CHILE is one city printed on two lines. The prior pilot's 41 label roundtrips, 1,152 integer slot roundtrips and all other result fields replay exactly in a temporary copy; originals were not overwritten.

This selected input is not the repository's entire historical knowledge. The [earlier dated-inscription review](../docs/historical-clock-inscriptions.md) separately records a corrected 1972 PEKING / HANOI / MANILA reading and three literal labels on two adjacent 30 August 1989 upper panels: CHABAROWSK and MAGADAN / SACHALIN. Those observations lack a verified join to the selected three runs and are not silently merged or claimed newly discovered here. That review already documents changes before 1990, so common-inventory continuity is a deliberately conditional identifiability calculation, not an established historical premise. The museum scale model is a different object and cannot fill installed-screen gaps.

## Conditional registration: 240 possibilities, no selected join

Assume, only for this calculation, that the three photographed local runs retain their placements on one unchanged 24-sector ring and use the same exterior-view local direction. Fix the first EU1969 panel at sector zero as a **coordinate gauge**, not true north, longitude or UTC zero. Enumerate all 24 AM1970 offsets and all 24 AS1984 offsets.

Compatibility honors exact row ranks and complete/partial-band flags. Two different known labels cannot occupy the same rank; a complete band cannot silently acquire an unrecorded rank. The production matcher and an independent simultaneous cell-unification oracle agree:

| Conditional outcome | Count |
| --- | ---: |
| Raw gauge-fixed offset pairs | 576 |
| Rank/label contradictions under the unchanged-inventory assumption | 336 |
| Compatible registrations, all retained | 240 |
| Known observed panels per compatible registration | 10 |
| Individually fixed cross-segment pair differences | 0 |

Pairwise disjointness of the ten observed panels is **derived from these exact constraints**, not imposed as a prior. It supplies a combinatorial cross-check: the three labeled arcs have lengths 3, 3 and 4; distribute 14 unused sectors into three nonnegative gaps, with two possible cyclic orders after fixing the first arc. `2 × C(16,2) = 240` agrees with enumeration.

This is not a claim that the clock was unchanged across 1969–1984, much less through 1989. Without that assumption, conflicts between dated observations can reflect historical changes; the 336 conditional contradictions are not exclusions of those real historical possibilities. No admissible layout is promoted by geography, modern time zones, English fragments or K4 cribs. Global rotation adds aliases of the same gauge-fixed descriptions, not evidence.

## What one shared phase actually constrains

For a hypothetical single exposure, mechanical coordinates satisfy `h = (s + φ) mod 24`, preserving the physical band. Therefore `h_j − h_i = s_j − s_i mod 24`. One common shift cannot alter relative positions. The analysis checks all 24 integer phases on all 240 retained layouts: 5,760 layout/phase descriptions and 236,160 label-slot inverse checks. Physical phase is continuous, so these are discrete validation cases, **not all possible clock states**.

Of 820 unordered label-observation pairs:

- 272 within a local source segment have one forced difference;
- 548 cross-segment pairs remain ambiguous: 310 have 18 possible differences, 238 have 19.

These pair relations are highly dependent. The same 41 observed labels and local ordering generate them; 272 is not an independent-evidence or cryptographic trial count. Multiple city labels share a panel/band, so collapsing label identities to ten sectors or seventeen sector/band cells destroys distinctions. Rank/source retention makes an observation lookup reversible; it does not establish a historical 26-letter encoder. A bare 24-sector assignment cannot bijectively encode 26 English letters, while added bands/ranks/framing would need their own independently defined rule.

A free continuous phase lets any one city take any ring-hour reading; it does not free all pair differences. Separate dated photographs have **separate exposure phases**. Even exact local hour readings would not by themselves register the photographs to one another: changing a segment offset can be absorbed into that photograph's unknown global phase. More explicitly, if a photo supplies a local phase `a_j`, its unknown segment offset `r_j` and exposure phase satisfy `a_j = r_j + φ_j mod 24`. Any alternative offset can be absorbed by `φ_j = a_j − r_j`. Authenticated simultaneous observations or independently timed common-clock phases could remove this freedom; different calendar dates alone cannot. The recorded `display_near` and overlapping-numeral descriptions do not provide a measured seam-to-numeral tolerance, so they supply local adjacency checks only. No fabricated half-hour phase interval or exact exposure clock time is used.

Civil-time semantics are a separate layer: if a source justified same-instant city offsets `u_i`, then their displayed differences would have to equal `u_j−u_i mod 24` under the chosen standard/DST/date convention. This study assigns **zero** such offsets. Panel placement is an observation, not proof that a city's historical civil time was correctly represented. The anomalous-looking 1970 NEW YORK placement cannot be repaired from a modern zone list or used to claim a historical clock error without further evidence.

## Controls, cost and limits

Before actual inventory enumeration, 36 complete tiny-ring compatible-set comparisons over sizes 4, 5 and 6 matched the independent oracle; all 36 planted layouts were retained, including overlapping consistent partial bands. Unknown versus complete-empty, row overrides, wraparound, common-rotation gauge, wrong-direction and inconsistent-phase mutations pass. There are 117 exact rational phase/gauge cases. Six dedicated unit tests pass. Original analysis took 0.101 seconds and recorded 16,400,384-byte peak RSS, within frozen 60-second/256-MiB limits.

No K4 trial, null significance claim, language scoring, alternate route scan or per-character phase/mapping fit occurred. No photographs or source scrapes are added. The numerical constraints are exact for the recorded partial inventory **and stated assumptions**, not a survey or proof of historical completeness.

## Next discrimination and stop

A useful new image or fabrication schedule must establish overlapping literal panels, seams, band/rank and historical version before narrowing registrations. A usable timed civil mapping additionally needs independent date/time-zone evidence; a geographic model needs true-north registration. Finally a source-grounded, deterministic symbol/key bridge with inverse and traversal is needed before ciphertext evaluation. Missing city labels cannot become free fitted key entries. The partial mapping study stops here pending source review; no broader clock-family exclusion follows.

Engineering validation checkpoint: **504 tests pass on Python 3.9 and 3.12**; [timestamped regression receipt/logs](../results/WORLD-CLOCK-003-VALIDATION.json). Fresh source integration and final publication remain pending.
