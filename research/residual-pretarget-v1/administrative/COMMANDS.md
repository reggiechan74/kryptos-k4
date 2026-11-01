# Public administrative derivative — NON_RELAUNCH_READY

> Historical evidence only; not executable authority or a current target result. Original document `execution-original/COMMANDS.md`, SHA256 `21521aa6ad59d84498aec77fb35ac239105cf6742dfdbdd50314e08cdaea4a94`, 3566 bytes. Only declared administrative sanitization was applied; see PROVENANCE.json. Original embedded hashes remain original commitments, not hashes of these public bytes. Current prefix status is separate in STATUS.json.

---

# Exact finite command schedule — not permission to run

[COMMANDS.json](COMMANDS.json) contains every exact launch and child argv, interpreter identity, working directory, role, inner ID, output path and process envelope. The same seven job specifications are bound in the final FREEZE.json. Only whole argv tokens `${FREEZE_PIN}` and `${APPROVAL_PIN}` may be replaced by the final freeze hash and the separately issued parent stage-approval hash. There is no arbitrary command, input, path, retry, seed or parameter option.

Required working directory: `original-execution-namespace`. Every launch is the normal isolated interpreter running `supervisor.py`; only its frozen child gets `-O` in the two optimized jobs. Do not invoke workers directly or add a preparatory help/import command.

| Order | Exact job | Stage | Child mode | Separate permission / acceptance |
|---:|---|---|---|---|
| 1 | `mock-normal` | Operational mocks | Normal | Final source PASS plus parent mock-stage grant |
| 2 | `mock-optimized` | Operational mocks | `-O` | First job's clean immutable external completion |
| 3 | `CTRL-positive-normal` | Actual disclosed control | Normal | Both mocks independently accepted, then parent control-stage grant |
| 4 | `CTRL-empty-normal` | Actual disclosed control | Normal | Positive control's clean immutable external completion |
| 5 | `K4-normal` | Target | Normal | Both actual controls accepted, publication/ledger/main-permission checkpoint, exact parent target-stage grant |
| 6 | `K4-optimized` | Target | `-O` | Normal target's clean verified or certified-gate receipt and external completion |
| 7 | `seal` | Metadata only | Normal | Finalized accepted target pair and separate parent seal-stage grant |

**Count: two operational mock invocations, two actual normal-only controls, two target modes and one metadata sealer.** The finite named mock assertion manifest is frozen separately; those assertions do not add subprocesses or scientific controls. An EMPTY control requires producer `EMPTY` and reference `VERIFIED_EMPTY`, not `VERIFIED_EXACT`. All actual controls retain the same scientific engine and 60/30/45-second phase settings as the target.

Before any successor, a completed prior job must have its immutable parent-owned `external/<job>.json` receipt. Before a new stage, parent-owned acceptance and new stage approval are also required. Neither source, worker, supervisor nor sealer issues its own authority. Approval files are absent during source preparation.

Every job is one-use. Failure, mismatch, absent output, overshoot, overflow, unresolved marker/reserve, uncertain external completion or changed source stops all successors. Retain partials and the reserve/marker; no automatic retry, replacement fixture, extra benchmark, alternate target or rescue run. A failure receives an immutable INCOMPLETE closeout, not a clean success seal. The ordinary clean sealer is available only after a finalized accepted pair; matched certified resource gates remain scientific INCOMPLETE.

The single reservation is 600 nominal CPU seconds / 256 MiB evidence disk: 456 runtime allocations plus 144 for source preparation, review, control/accounting and unmeasured tails. Allocation is not measured consumption. Historical reserves are not available. The disk limit does not replace the 1 GiB scientific-worker / 256 MiB supervisor memory envelopes.

Existing main-update denial remains pending explicit user branch permission. This local command manifest is not publication or target authorization.
