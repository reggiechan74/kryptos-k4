> PUBLIC EVIDENCE DERIVATIVE — NON_RELAUNCH_READY. Historical statements and original hash commitments are preserved; original/public mapping is in PROVENANCE.json. Later completion is described in the package README.

# Independent operational recovery assessment

**DESIGN PASS for a new, explicitly bridged target-only execution namespace.** Loss of disposable private files does not require repeating the accepted mocks or disclosed controls. It does prevent pretending that the sanitized public package is the original executable authority/state. A narrow operational recovery is practical; no implementation or execution is approved by this assessment.

Responsibilities sequence 66 and the parent/publisher history identify published commit `3e128d9a617af377516a0b9878a942b29bf2e3b8`, and state that the target pair has not run. This review relies on that verified publication history; it did not perform another remote verification or update.

## Authenticated recovery available now

Restored public base:
`published-baseline/research/residual-pretarget-v1`.

`SOURCE-RECOVERY-READBACK.json`, SHA256 **6e51470cedd7d3678e67cbc0d0ecf6a11f282c421cc7b2bb694c7d0efb7fa19d**, independently checks:

- Seventeen exact-byte objects: seven operational sources, five mathematical modules, scientific CAPS, and four disclosed fixture/expectation files. Their original/public/provenance SHA256 values and sizes agree.
- The current interpreter binary remains `fa67443527ed9647f760d807e2a38f26340757123e643c4639cf273ed15d5ea7`, identical to the historical freeze. No scientific-runtime change is presently necessary.
- The recovered public provenance manifest is `aca150729cccae6821ff7fec01638d32c4970112276cf2df77122c96f8a2a7d8`.
- Public FREEZE derivative: `69a5aed776771861c01b8082995d666c1cb2ed109eac644a75bfc3d3ddafab56`; it accurately records original freeze `fe2864d656a426635731c7f4a0be07329c67eb5e4b0fe15e6fb10e8661c9f11d`, but is expressly NON_RELAUNCH_READY and not executable authority.
- Public state derivative: `f60427586ea1a79696d6d47411c3446ac6e7ef5a27d6f6419efa000c48bed3ca`; it preserves original state commitment `4604fe187ae86db291aefd51d852165f616a31f6f8476ef435c7c1bab3b3f789` and the accepted four-job prefix, 284 nominal consumed, no historical in-flight reservation.
- Public source/mock/control review derivatives and both resource-ledger derivatives match their public provenance hashes. In particular, the control review derivative `0116418d01e1b85250913fee170bf5a95e79b9628b6ede20ac2fd704773d5709` preserves the original independent review commitment `4167f05853f104ca07c435b6ca958bac36ca9552a2b0d479e1cc3863f5b34324`.

This is bounded source/ancestry authentication, not a full repository or certificate-archive restoration audit. No certificate archive was read or extracted; no target input was accessed. Original private approvals, original raw receipt bytes and original local state were not reconstructed.

## Why the historical executable cannot simply resume

The recovered original source is authentic, but its operational assumptions deliberately require the lost private namespace:

1. `common.read_authority` reads original controls acceptance and original per-job receipts/external-completion files at their old absolute paths.
2. `supervisor.validate_state_shape` and `require_next_job` require a seven-job original prefix; allocations, certificate limits and comparisons use positional assumptions such as `JOBS[2:6]`, a 456 runtime cap, and six prior jobs before sealing.
3. `seal_results.snapshot` requires those six originals plus all original stage approvals/acceptances.
4. `worker.py` and `common.py` bind original absolute operational/scientific paths and the original source-freeze identity.

Inventing look-alike approvals or inserting sanitized derivatives under those paths would make provenance claims false, even if numeric values agree. The remedy is a separately versioned operational protocol that accepts historical evidence as historical evidence, not relaxed hash checking or fabricated old files.

## Minimal proposed recovery

### 1. Immutable historical bridge

Create a new parent-owned recovery-origin/acceptance record that binds the published commit, public provenance/derivative hashes, original commitments, accepted source/mock/control reviews, original mathematical hashes, exact target input commitment, and original resource allocation. Explicitly record:

- Original prefix is historically accepted, not rerun or currently re-executed.
- 284 nominal seconds remain consumed; the two mocks and two controls cannot become executable again.
- Target normal/optimized and sealer remain unrun according to parent-held execution history, not merely because local files are absent.
- Lost private originals remain unavailable; public derivatives authenticate their own bytes, not the lost original bytes.

The parent must explicitly accept this recovery bridge. No proof requires recreating disposable private control grants whose accepted outcomes and commitments are already preserved in trusted history and publication.

### 2. New namespace and current-run state

Use a new local namespace and new schema/freeze. Allow only three current-run jobs: `K4-normal`, `K4-optimized`, and metadata `seal`. Start current `completed=[]`, current runtime allocation consumed=0, and no current reservation. Keep the historical consumed amount and historical measurements in a separate immutable bridge section. Do not populate the current completed list with synthetic historical receipt entries.

Parent-owned fresh target approval binds the new freeze and bridge, current publication checkpoint, exact two target commands and same raw-input hash. It is a new one-use authorization to execute previously unrun slots, not a reset of earlier permissions. The sealer remains separately gated after an accepted pair.

Maintain a durable parent-held grant/attempt journal outside the disposable execution namespace. Consume each permission before launch and retain its external completion. Another workspace loss, uncertain launch or missing receipt must leave that attempt consumed/uncertain, never automatically reusable. The local durable reservation and failure-stop logic must remain intact as well.

### 3. Narrow operational changes, unchanged science

Keep all five scientific modules, scientific caps, independent raw/interpretation module `input_check.py`, and bounded collector byte-identical where possible. Limit worker changes to operational paths and new ancestry/report binding; retain both converter bodies, R semantics, complete reference verification, digest exclusions, conditional/EMPTY interpretation and all scientific calls/caps.

Preserve authenticated source-byte loading and module registration. In particular, the unchanged decoder imports `affine_filter`, and both decoder/reference derive commitments from `__file__`; local path relocation must preserve those identities and exact source bytes. Do not substitute importlib cached bytecode or change scientific code to accommodate relocation.

Audit every old seven-job/index/cap assumption in common, supervisor and sealer, not just the visible job tuple. Fresh seal inventory must contain the bridge and new current-run artifacts; it must not claim old private files were revalidated or a historical source freeze equals the new freeze.

Use an acyclic commitment chain: recovered origin evidence → new source/command/cap freeze → independent review → parent recovery/target approval → one-use state/receipts → accepted pair → separately authorized seal. No embedded future approval/self hash or circular freeze binding.

### 4. Budget and finite output inventory

Preserve the single 600 nominal allocation. The accepted prefix consumed 284. The original target pair's 160 and sealer's 12 were earmarked but unrun; they are not a new reservation. The remaining 144 source/review/control-overhead allocation has already borne work and unmeasured overhead. Do not advertise all arithmetic remainder 316 as freely spendable or assume the 144 is untouched.

Historical known runtime components remain 19.957271 CPU seconds, with historical policy charge 72 and nominal 284 kept distinct. New receipts add current measurements once; do not recompute historical CPU from derivatives as though it were a fresh measurement. Preserve all older failed reservations and project-level limits unchanged.

Keep target 60/75 CPU, 1 GiB worker; 4/5 CPU, 256 MiB supervisor; 150-second outer wall and 60/30/45 cooperative phase limits. Keep logical/digest/certificate caps unchanged. Freeze exact recovered-history/current-output disk accounting within the existing 256 MiB stage envelope; absence of old local files is not a license for unbounded copies or certificate extraction.

## Preparation and execution gates

1. Parent may authorize source-only recovery implementation with the exact operational delta and no scientific or data changes.
2. Independent review must authenticate the complete new source/schema/commands/inventory/bridge and static differences before any launch.
3. A small, finite recovery-only operational metadata/authority check is recommended for the changed bridge/state/sealer rules. If approved, freeze its literal cases, counts, commands and resource charge first. It is a separately authorized recovery check, not a rerun of consumed old mocks or disclosed controls. No such check is authorized by this assessment, and no numeric allowance is silently assumed available.
4. Parent then separately grants only the unchanged target pair, normal first; independent normal receipt review precedes optimized. Changed pins, invalid reports, cap failures or uncertain completion stop without retry or retuning. Matched certified resource gates remain scientific INCOMPLETE.
5. Metadata seal and later publication/certificate copies retain their own gates. Bind the already verified publication checkpoint without falsely claiming that newly prepared recovery code was historically published.

## Verdict and limits

There is **no mathematical reason to repeat the two already accepted disclosed controls solely because their private working directory was lost**. The same mathematical bytes, caps, interpreter and accepted evidence are available. The necessary change is explicit operational ancestry and state semantics. Exact implementation review and parent authority remain real prerequisites, not an impossible demand for lost private files.

No new theorem, model-membership claim, worldwide novelty claim, first-six plaintext claim or K4 result is made. Bounded EXT-051 uncertainty and the global-operator versus finite-trace distinction remain unchanged. Original failed cohorts remain INCOMPLETE; no rescue or new draw is proposed.

The scoped standard-library metadata check used 0.122740419 CPU seconds internally. Shell/startup, source reading and this report's overhead are unmeasured preparation work, not zero. No prepared source was imported/executed, no implementation was written, and no tests, controls, solver/reference/generator, target arithmetic, seed/truth access or remote write occurred.

## Subsequent preparation decisions and completed restoration

Before this review's final handoff, the coordinator supplied final `RECOVERY-INVENTORY.json`, SHA256 `fc7908cdaa31e0716c88cb3f7c65db0833df5cbeae96144558ef32cbbdd1f05e`. An independent local readback authenticated all **76 listed files / 1,930,889 bytes**, including their Git blob hashes, without accessing target data or certificate archive/member payloads. This verifies the recovered local objects against the supplied immutable-commit inventory; remote commit verification remains the publisher's trusted history, not a new reviewer network operation. It does not resurrect excluded private authority or authorize relaunch.

The coordinator also relayed a separate parent authorization of **120 additional nominal CPU seconds for repair-only preparation**, from the previous 5,000 unallocated, making the project 23,920 allocated / 28,800, with 4,880 unallocated. This is distinct from the original 600; the original 144 overhead portion remains committed and is not reopened. Future recovery implementation/checks must be charged under an explicitly approved finite partition of that repair grant. No scientific test or target permission is inferred. The initial pre-update assessment is preserved as `RECOVERY-DESIGN-REVIEW.initial.md`; these additions change neither its scientific invariance requirements nor the original consumed-prefix accounting.
