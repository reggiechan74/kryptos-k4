# Item 3 partial World Clock registration

[Findings](../../research/WORLD-CLOCK-003-FINDINGS.md) · [frozen protocol](../../research/WORLD-CLOCK-003-SPEC.md) · [original manifest](20261024T002946Z-c05cd21588cd43878a866f2fa1a99cb2/manifest.json) · [all registrations, conflicts and pair domains](20261024T002946Z-c05cd21588cd43878a866f2fa1a99cb2/registration-analysis.json).

The common-inventory assumption across three dates is conditional, not a verified 1989 ring. Every compatible registration is retained. Integer phase checks do not enumerate continuous physical phase. No K4 cipher evaluation or civil offset assignment.

```sh
python3 experiments/world_clock_003.py --spec-commit 53aa67b86da286d45012d957a25b4763c77ab04f --output /tmp/k4-clock-replay --kind replay
```

Replays create separate run snapshots; original evidence and pilot results remain unchanged.

[Fresh source evidence and conservative inventory](../../independent/2026-10-24/world-clock-item3/README.md) are separate from the numerical run. [Final validation](../WORLD-CLOCK-003-FINAL-VALIDATION.json) records both supported suites.
