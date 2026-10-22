# Independently supplied followup artifacts

Received and reviewed on 22 October 2026. These are independent-worker originals,
not replacements for the repository's committed local specifications or runs.
All 40 received member byte hashes and the three archive hashes are recorded in
[TRANSFER-RECEIPT.json](TRANSFER-RECEIPT.json). Source code was inspected before
execution. Relative paths remain internal to each original package.

- [Calibration](calibration/REPORT.md): three toy generators, twelve worker-authored
  passages (six per split), eight fixed statistics, one logistic model. The label
  EVOLVING_ALPHABET uses rotate-and-swap, **not** the move-to-front rule. Local
  replay reproduced the classifier, all generated data and 199 label-null values
  exactly, plus 288 fixed-key inverses. It did not repeat the recurrence enumeration.
- [Evolving alphabet](evolving-alphabet/README.md): exactly the same four fixed
  move-to-front models as the local pilot; different independent implementations,
  seeds and nearby negative mechanism. Replay reproduced all deterministic outputs
  and the separate JavaScript rank oracle. This is replication, not four new K4 cases.
- [Historical clock](historical-clock/historical_clock_report.txt): partial dated
  observations and coordinate checks; no K4 letter encoder or 1989 inventory.
  The public package includes photo provenance only. No source photo or crop is
  included anywhere under this directory.

Local replay receipts are under
[results/independent-followup-review](../../results/independent-followup-review/).
The adapter [replay_independent_followup.py](../../experiments/replay_independent_followup.py)
copies packages to a **new** supplied scratch directory before execution. Its
120-second budget includes all command steps. To reproduce, provide installed
Python3, Node.js and a separate Python environment with the supplied pinned three
calibration libraries; package installation is not performed by the adapter.

```sh
python3 experiments/replay_independent_followup.py --output /new/scratch/directory --node /path/to/node --calibration-python /path/to/calibration/python
```

The received preregistrations and pre-run hashes are preserved. We can verify byte
integrity, definitions and numerical replay; their claimed pre-generation timing
is supplied provenance, not independently timestamped by this repository. Original
reported runtimes/platforms remain original; local replay metadata is separate.

The reported recurrence count is parameter descriptions, not novel models or
plaintexts. Its covered progressive/constant-key/autokey subsets and locally
verified exact contradiction certificates are documented in the
[followup findings](../../research/STRATEGY-FOLLOWUP-FINDINGS.md). Fixed parameters
always determine one decryption; nonunit recurrence coefficients can make fitted
seed/model recovery ambiguous without making fixed-parameter decoding multivalued.

Source photographs stay in the Mac task workspace outside the Git checkout.
The local visual review confirms NEW YORK between the specified panel seams in
the 1970 image, without inferring a civil-time error or unchanged1989placement.
The construction worker's separate artifact was not yet received at this integration
stage; the existing locally replayed CP result remains independently documented.
