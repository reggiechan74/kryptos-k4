# Reproduction and public-byte provenance

## Integrity before execution

Extract the archive in an isolated workspace. `PUBLIC-PROVENANCE.json` records every included artifact's original SHA256, distributed SHA256, byte count and whether it is unchanged. The same map is available beside the archive. Verify these public hashes before running code.

The original **83-file development freeze** and closeout manifest remain unchanged. Private handoff contents are omitted; selected prose copies are sanitized and explicitly annotated. Their original hashes are retained, but **sanitized prose is not byte-identical to frozen prose**. Original manifests intentionally continue to name original hashes and omitted handoffs; do not claim that a whole-original-manifest check over public prose copies will pass. Computational code, synthetic inputs, released labels/seeds, numeric outputs and audit receipts are unchanged. No unlicensed third-party source bodies are included.

Original code/receipt paths such as `/workspace/shared/sparse-law-pilot` are generic execution-environment provenance, not private account paths. The historical audit wrapper hardcodes that layout. To reproduce it unchanged, use an isolated environment with that layout; do not overwrite an existing worktree. Alternatively adapt paths in a separately versioned local copy and label the change. No modified wrapper is presented here as the frozen original.

## Portable selected checks

From extracted `sparse-law-pilot/`, the disclosed synthetic development tests are:

```sh
python3 -m unittest -v test_join
```

The source `reference.py`, `join.py`, fixture generator and `run_public.py` are unchanged. Original runner instructions and explicit synthetic-stage flag are in its source/protocol. Use a fresh output directory and the same documented resource limits; do not overwrite archived outputs. Released fixtures are no longer blind and any replay is a replay, not new validation.

The separately supplied `sparse-law-blind40-evaluate.py` accepts public-input path, released-label path and results directory. It verifies synthetic features/truth and witness replay; it does not invoke a K4 solver. The original independent audit and capped wrapper are retained in separate sibling directories. Toy verification programs under the two future-design directories establish only their stated finite algebra checks.

## Labels that must survive reproduction

- Development, original blind run, original independent audit, post-release capped repeat, and future design/toy checks are separate evidence stages.
- Exact conditional marginals are not their Cartesian-product joint relation.
- Coefficient aliases, globally identical functions and agreement only on one 91-position trace are distinct.
- Old developmental “same message plaintext” wording is explicitly limited to the modeled 91 positions; no first-six or full-97 recovery follows.
- The join writes a factorized relation in addition to primary projections/witnesses. Keep observed workload timings and stage breakdowns; future equal-contract benchmarks must be separately frozen.
