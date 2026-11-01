# Public administrative derivative — NON_RELAUNCH_READY

> Historical evidence only; not executable authority or a current target result. Original document `execution-original/ACCOUNTING.md`, SHA256 `e5d20f75a12f4de884abd193d30a65bf340cedcbf225fb02d462742fad7404ce`, 3295 bytes. Only declared administrative sanitization was applied; see PROVENANCE.json. Original embedded hashes remain original commitments, not hashes of these public bytes. Current prefix status is separate in STATUS.json.

---

# Resource and one-use accounting

The parent reserved one new 600 nominal CPU-second allocation, bringing the project to 23,800 / 28,800, with 5,000 unallocated. RESOURCE-ALLOCATION.json separates the 456 runtime allocation from 144 for source preparation, review, control/accounting and unmeasured tails. These are reservations, not measured consumption. No old failed or unused reserve is reused, and no remainder authorizes a retry.

The scientific worker's own phase/wall/CPU timers begin after raw conversion and are **subsets**, not total process usage. The bounded collector records inclusive OS child user/system CPU, their sum, and supervisor-exclusive CPU samples separately. The supervisor's final write tail is explicitly unmeasured and its full nominal allowance remains charged. Do not add nested phase timers to OS process usage or report missing measurements as zero.

## Durable attempt boundary

After exact source, command and parent authority authentication, the supervisor durably writes the one-use marker with the full job reservation before checking active-input pins or disk availability. These authorized prelaunch failures consume the slot and retain marker/reserve; they are not mechanically repeatable successes or reusable grants.

- `launch_attempted=false`, `execution=null`: failure before a child launch was attempted. Keep the nominal slot consumed; child CPU is not invented.
- `launch_attempted=true`, `execution=null`: launch completion is uncertain. Do not claim no child, no CPU or successful reap; preserve evidence and stop.
- Accepted completion requires `launch_attempted=true`, a complete guarded/reaped OS receipt, all bounded artifact pins and later parent-owned external completion.
- If a crash prevents an internal receipt, the marker/reserve and partial namespace remain authoritative stop evidence. The external owner must record an INCOMPLETE/uncertain closeout, not retry or clear it.

On failure, a consumed/charged nominal slot and its retained in-flight marker identify the **same** unavailable reservation, not a second allocation. The retained reservation prohibits re-use and success sealing. It is not a new 600-second grant or permission to double-count physical CPU.

The 256 MiB stage limit is evidence disk, not process memory. Preserve worker 1 GiB / supervisor 256 MiB for each actual control and target slot, and the distinct frozen mock/sealer envelopes. Four certificates retain their full unchanged 32 MiB per-file ceilings. INVENTORY.json and FREEZE.json bind finite paths and caps; overflow stops the schedule rather than deleting controls, lowering scientific caps or dropping evidence.

Every later job also requires clean external completion of the prior prefix. The six-job accepted prefix has 444 nominal runtime seconds charged before the sealer reserves its own 12. Its own external completion remains pending until the parent records it; the sealer cannot certify itself. Failures instead get preserved INCOMPLETE inventory/ledger closeout and no clean terminal seal.

This source-only preparation has not run any prepared module, mock, actual control or target computation. Metadata/source inspection overhead is uninstrumented unless an individual static-review receipt says otherwise; it is not measured zero.
