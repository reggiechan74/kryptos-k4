# Item 2 conditional physical checks

[Findings](../../research/PHYSICAL-SOLAR-002-FINDINGS.md) · [frozen protocol](../../research/PHYSICAL-SOLAR-002-SPEC.md) · [original receipt](20261024T001728Z-f2895d4425214b2bbed15c832235acf2/manifest.json) · [complete outputs](20261024T001728Z-f2895d4425214b2bbed15c832235acf2/physical-checks.json).

The original run is a conditional physical calculation, not a K4 search. Numerical envelopes, 39 calendar samples and all 125 height scenarios are retained. Later replay/validation receipts must remain separate. Reproduce from repository root:

```sh
python3 experiments/physical_solar_002.py --spec-commit b2cc1dffdbb71b7a11c38f8041d220f3fce82932 --output /tmp/k4-physical-replay --kind replay
```
