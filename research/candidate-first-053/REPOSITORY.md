# Experiment 053: repository access and reproduction

**Materialization is required before running the original reproduction commands.** The oversized `results/control_null_receipts.json` is stored losslessly as `results/control_null_receipts.json.gz` because this connector limits individual requests to 16 MiB. No rows, scores, keys, nulls or diagnostics have been omitted from this file. This is ordinary Git storage, not Git LFS.

Read the unchanged [experiment overview](README.md) for the negative result, exact tested scope, original compact-package omissions and limitations. The original archive and frozen manifests are unchanged. [Transport manifest](GITHUB_TRANSPORT.json) records the stored and decoded byte sizes and SHA-256 hashes, plus the original Git blob hash.

## Reproduce from this repository

Use a new destination outside this source directory; the helper never overwrites frozen evidence:

```sh
python materialize_repository.py /tmp/candidate-first-053-reproduction
cd /tmp/candidate-first-053-reproduction
python reproduce_compact.py --validate
python reproduce_compact.py --verify-training
```

The offline helper verifies the compressed bytes, restores the exact original bytes into the new directory, and checks every payload listed in the original compact archive manifest. It does not retrieve data, train a different model, change hypotheses, or regenerate omitted full control receipts. A later numerical reproduction retains the limitations documented in the original overview.

`REPOSITORY.md`, `GITHUB_TRANSPORT.json`, `materialize_repository.py`, and repository-only directory guides were added at publication; they are not original experiment payloads. Gzip replaces only the storage representation of the explicitly mapped file. Other archived files remain byte-identical. No original archive ZIP is duplicated here.
