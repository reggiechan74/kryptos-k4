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

## Audit preservation and current runners

The original files above are preserved byte-for-byte against
`data/audited-results-b83.json`. `AUDIT-001.json` records the focused validation.
Original run metadata is historical and refers to the code at its recorded
commit, not the subsequently hardened code. All 282 ROUTE-001 fits are vacuous
with zero repeated-phase comparisons; they are not positive candidates.

New replay commands require `--spec-commit FULL_SHA` and write unique directories
under `results/runs/`. Read `latest.json`, then the referenced `manifest.json`.
Only `status: completed` in that manifest makes its listed artifacts publishable.
A timeout, invalid baseline, interruption, or exception publishes an incomplete
manifest with no result artifacts, preserving prior runs. An abrupt process kill
may leave a hidden pending directory and a running pointer; neither is complete.
The original specification and results shared a commit; future new specs must
be committed first, with chronology checked from Git history. The offline runner
records a supplied full SHA and the local spec hash; it cannot itself prove that
the commit exists, contains those bytes, or predates execution.
