# Family 5: one shared clock phase cannot supply differing seasonal city corrections

Local continuation 042, 24 October 2026. **A static set of city panels/corrections plus one shared mechanical phase cannot track date-specific Berlin and London civil times throughout 1989 under the recorded timezone rules.** This excludes that automatic-civil interpretation only. It does not reject the actual World Clock, standard-time conventions, a single source-selected date, or a broader clock/direction key.

[Pre-outcome specification](CLOCK-CIVIL-042-SPEC.md), [source pins](../sources/CLOCK-CIVIL-042.json), [full interval/count receipt](../results/CLOCK-CIVIL-042-ORIGINAL.json), [independent calendar/TZif implementation](../experiments/clock_civil_042.py), [Python 3.12 replay](../results/CLOCK-CIVIL-042-REPLAY.json).

For fixed city sector/correction constants s, moving readings are h_i(t)=s_i+phi(t) modulo24. The shared phase cancels in h_Berlin−h_London even if it changes freely with date. The observed civil difference in the pinned IANA/OS interpretation changes:

| UTC interval in 1989 | Berlin minus London |
| --- | ---: |
| 1 January through 24 September 01:00, exclusive | +1 hour |
| 24 September 01:00 through 29 October 01:00, exclusive | 0 hours |
| 29 October 01:00 through year end | +1 hour |

All8,760UTC hourly instants and ±1second transition boundaries agree between the native timezone tables and independent calendar formulas:17,538offset comparisons. There are7,920hours with difference+1 and840with difference0. None of the24constant integer-sector differences fits the whole year; a fixed fractional correction also cannot equal two distinct values. An independently checked fixed-standard-time model passes all8,760synthetic positions, while incorrectly forcing common DST treatment misses840. These are exact model constraints, not cipher tests or p-values.

The IANA rule file is an implementation reference that explicitly disclaims authoritative history. OS TZif tables are pinned by hash and copied as tiny factual fixtures for byte-identical replay; the installed path identifies2026c.1.0. This does not establish what the clock displayed in1989, prove legal history from primary legislation, or select Sanborn's date. Prior research already disclosed the autumn-rule difference; the new work completes its whole-year interpretation test rather than announcing a blind date discovery.

## What remains open and why

The prior023 count of240registrations remains conditional on an unchanged inventory; it was not rerun as new coverage. Dated photographs demonstrate actual layout differences. The direct May1989 evidence supplies only five complete lower-band city names, plus the separate partial views already retained. Unknown1989cells cannot be filled from1969,1971,1974,1984 or1990 snapshots or today's city list. A literal plate program, fixed standard time, date-specific legal civil time and printed correction marks are different inputs; the experiment cannot choose among them.

The compass/direction branch still lacks a surveyed relation among true north, engraved labels/needle, stone axes and an intended viewpoint/receiver. Existing source-conditional ENE sunlight and opposite-shadow constraints remain narrow; they do not exclude nighttime pool illumination, reflections or artificial lighting. No new geographic search, angle/date-to-English tuning or claimed survey was performed.

A reproducible clock/direction key still needs an independently fixed historical version or consumed cells, origin/direction, epoch if time is used, city/band/rank/correction selection and a total reversible A–Z bridge. A24sector count alone cannot select those rules. The precise conservation-thesis/photograph leads are preserved; current permitted access supplies neither the missing inventory nor creator-selected extraction. No outreach, payment or denied-source retry follows.

**Completion boundary:** the stated automatic-civil model fails, while literal/single-date/standard-time mechanisms survive without a determined cipher bridge. The broader family is evidence-blocked for decoding, not exhausted. No actual K4 trials, recovered key or Site change; new results remain local. Original/replay UTC times are recorded separately.

A [separate late reviewer-control receipt](REVIEW-CONTROLS-046.md) strengthens active-calculation interruption, explicit wrong-DST and invalid-flag checks without changing this original model, source, receipt or large-run outcome.
