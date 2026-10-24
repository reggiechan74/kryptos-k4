# ENE 049: complete frozen routes and three fixed keys give no crib survivor

**All 56,454 route descriptions and their 19 fixed arithmetic choices completed.** Exact route deduplication gives 34,569 permutations and 656,811 distinct route/arithmetic operators. None satisfies all 24 clue letters; the maximum is 8/24. This rejects the [declared finite model](ENE-ROUTE-049-SPEC.md), not an unknown key or every interpretation of EASTNORTHEAST.

[Original receipt](../results/ENE-ROUTE-049-ORIGINAL.json), [Python 3.12 replay](../results/ENE-ROUTE-049-REPLAY.json), [complete compressed permutation/alias catalogue](../results/ENE-ROUTE-049-CATALOGUE.json.gz), [engine](../experiments/ene_route_049.py), [UTC/resource replay logs](../results/048-050-REPLAY-VALIDATION.json).

Every width 1–97 and actual starting cell 0–96 was covered, with row-major ragged fill, both inverse directions and three fixed procedures: literal(+2,−1)without wrap; the same step on a finite wrapped geometric canvas with nonexistent cells skipped; and the separately rounded exact-ENE digital line without wrap. No blank carried a letter, and no source index was lost or repeated. All 28,227 independent coordinate traversals agree with compiled routes; both inverses and finite wrapped-orbit termination were checked. Literal 2:1 is 26.565051177°north of east; the digital 22.5°case fixes phase and lower-cell rounding. It is not a physical survey or a uniquely implied reading rule.

Arithmetic is either absent or uses AZ/KRYPTOS coordinates, three equations, and literal KRYPTOS/PALIMPSEST/ABSCISSAkeys from position 1. All 19 complete arithmetic maps were checked distinct. The printed tableau does not otherwise determine a key. Decoding readsR[i]=C[p[i]], then solvesR=σP+τK; encryption reverses both stages exactly. No fitted keyword, key phase, row-fill variant, ENE rounding or restart rule was added after results.

All 11,058 planted width/direction/arithmetic cases pass, with starting positions distributed across all 97 values; six whole-selector plants pass. Full independent reference traversal covers pathological widths and ragged cells. Additional regression checks independently verify the packed exact-match counter against direct letter comparison.

All 31 whole-search null maxima are 7 or 8, with 17 at least the actual 8. No partial English fragment or attractive route is promoted. These are conditional 73-position permutations and coarse whole-family diagnostics, not universal chance probabilities. The complete original runs 2026-10-24 T 19:45:19.185573+00:00 to 19:45:36.969399+00:00. A full Python 3.12 semantic replay agrees, taking 14.10 seconds with 132,644,864 bytes maximum RSS; registered limits were not changed.

Two permutations intersect the old 66-route catalogue, giving a conservative 36 fixed-arithmetic cases already inside that prior key-family coverage. Pure transposition was already independently excluded by the known-letter count deficit. These repeats are retained for identical null calibration and are not new negatives. K3/clock and occupied-cell families are also related prior work; no worldwide novelty claim or complete prior-catalogue union is made. See [overlap accounting](048-050-PRIOR-COVERAGE.md). Untested complements include other keys, phases, rounding/edge conventions and stage orders. No K4 solution, physical compass calibration, Site change or public push follows.

Original integration at `1cef25a`: all 718 tracked tests passed on Python 3.9 and Python 3.12; [UTC suite receipt and complete logs](../results/048-050-FINAL-VALIDATION.json). Original experiment, scientific replay and regression times are recorded separately. No public push occurred.

Reproduce from repository root, preserving original receipts:

```sh
python3 experiments/ene_route_049.py --output /tmp/ene-route-049-replay.json
```

Existing compressed catalogues are checked exactly instead of silently overwritten. New replay files receive new UTC times.

## Independent-audit control correction

The original negative results remain unchanged, but the earlier plant validation omitted assertions: 048 had not run its large plants through the actual source lookup; 049 had not checked the planted route/variant/plaintext in the returned selector hits. [The correction and current stronger receipts](048-049-CONTROL-CORRECTION.md) close those gaps and add the explicit 044 structural comparison. Earlier originals, replays and their timings are retained as historical artifacts, not silently overwritten. Current replay commands execute the strengthened controls. The new actual/null numerical payloads match the originals exactly.
