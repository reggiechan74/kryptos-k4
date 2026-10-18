# Research policy

- Record exact reproducible commands, code commit, Python/environment version,
  input hashes, normalization, alphabet, direction, and indexing convention.
- Set fixed seeds for randomized work and record generator and seed. Record
  deterministic ordering and tie-breaking; no seed is needed for baseline checks.
- Specify finite parameter ranges, maximum candidates, runtime/memory limits,
  scoring function, and stopping rule before running an experiment.
- Keep experiments local and inexpensive by default. No expensive searches,
  paid submissions, paid APIs, or external submissions are authorized here.
- Report negative results only for the exact tested settings. A partial search
  cannot eliminate a whole cipher family. Distinguish exhausted, timed out,
  interrupted, and invalid runs.
- Label public facts, hypotheses, and unverified third-party experiments.
  Record positive/negative controls and failure cases. A crib match is evidence
  for a candidate, not a verified solution.
- Keep API secrets, credentials, private correspondence, and personal data out
  of source, logs, fixtures, commit metadata, and output artifacts. Use synthetic
  data and redact before committing. Do not add collaborators or publish this repo.
- Keep raw results and exact conclusions linked to an experiment ID and commit.
  New primary-source evidence may revise the baseline; retain provenance/history.
