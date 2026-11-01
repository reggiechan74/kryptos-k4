# Public administrative derivative — NON_RELAUNCH_READY

> Historical evidence only; not executable authority or a current target result. Original document `execution-original/LOADER-AUTH-DECISION.md`, SHA256 `30ad78bb7beef1dc0efbf9b275c01b4769b6007bbc172668528924e70cee850a`, 2393 bytes. Only declared administrative sanitization was applied; see PROVENANCE.json. Original embedded hashes remain original commitments, not hashes of these public bytes. Current prefix status is separate in STATUS.json.

---

# Narrow source-authentication hardening — pre-freeze decision

Parent explicitly approved this operational source-only delta at 2026-11-01 01:46:34 UTC. It is part of the same 600 nominal CPU-second / 256 MiB reservation, not another allocation or execution grant.

## Reason and exact change

`-B` suppresses bytecode-cache writes; it does not itself exclude cached-bytecode reads. A source hash followed by `SourceFileLoader.exec_module` therefore does not guarantee that those exact authenticated source bytes are executed. Static inspection of the installed CPython primary source, `.../python/lib/python3.12/importlib/_bootstrap_external.py` (SHA256 `e6ad72f3f0f9b65c99ab52598cd02ab748511dcdce1dd51f18dace9be9a680c6`), confirms the read/return path at lines 1091–1130 and write-only `sys.dont_write_bytecode` check at line 1135. No module or cache was executed or replayed for this inspection.

For each operational bootstrap and pinned module loader: read capped bytes from the exact pinned path, verify SHA256 **before** compilation, compile those same bytes using the exact source filename, `dont_inherit=True` and the selected interpreter optimization mode, then execute in the same explicitly registered module. Preserve `__file__`, module name, `__package__`, `__spec__` and required `sys.modules` semantics. Do not consult or modify cached bytecode. Apply consistently to common, worker, supervisor, sealer and mock operational loading.

All five scientific source files, APIs, dictionaries, traversal, semantics and limits remain unchanged. The independent reviewer must inspect this precise operational delta. Finite future mock checks use only tiny nonscientific literal bytes/stubs for accepted bytes, wrong/changed pin rejection before compile and cache-loader bypass; no disk cache fixture, scientific import, process or new benchmark is introduced.

## Evidence limits and authority

This tightens a prospective source-authentication guarantee. **There is no evidence here that any historical cache was wrong, and no prior evidence is invalidated.** The original proposal and validation records remain unchanged.

The parent grant permits writing and statically reviewing this correction only. No mock, control, prepared-module import or target arithmetic/execution is authorized. All separate stage, publication/ledger and exact target-approval gates remain in force.
