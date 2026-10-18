# Reproducible results

Each experiment is scoped in [the log](../research/EXPERIMENTS.md) and
[bounded specification](../research/BOUNDED-SPEC.md). No K4 solution is claimed.

| Artifact | Content |
| --- | --- |
| CTRL-001.json | All complete K1/K2/K3 fixture comparisons and hashes |
| STRUCT-001.json | Exact count and periodic-bijection witnesses, encoding feasibility |
| ROUTE-001-summary.json | Case counts, compatible periods, code/input hashes |
| ROUTE-001.json.gz | Complete route catalogue and all partial key assignments |
| RUNKEY-001.json | Literal-window counts, descriptive match histogram, no survivors |
| TRIFID-001.json | Fixed cubes/periods, no survivors |
| STAT-001-summary.json | Observed lag counts, calibration parameters, corrected tails |
| STAT-001.json.gz | All 9,999 null draws and 5,000 evaluation maxima |

Compressed files are ordinary UTF-8 JSON compressed by Python's standard-library
gzip with mtime zero. The summary records the uncompressed SHA256. For example:

```sh
python3 -m gzip -d -c results/ROUTE-001.json.gz
```

Use the commands in the experiment log to regenerate artifacts. Elapsed time
and environment metadata may change; deterministic draws and substantive outputs
are fixed by the documented implementation and seed. Original ciphertext and
corrected variants remain separately named in `data/controls.json`.
