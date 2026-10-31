# Independent controlled preflight audit — study 064

**PASS for implementation and synthetic controls, not authorization for target compatibility.** All 224 plants retained; 109 have unique plaintext and 115 are ambiguous across periods 2–8. All 64 independently random nulls have empty solution sets; zero null fits was not an admission requirement. The 21 predeclared diagnostics contain 14 unique and 7 ambiguous plaintext sets. These are synthetic correctness results, not evidence for the K4 mechanism.

## Independence and sequence

This worker read the Responsibilities Page sequence3 and current project instructions before work. It did not inspect production implementation until after both source freezes, independent bank generation, and the sealed production output. Reference schedule recomputes prefix occurrence-span sums; production uses recursive previous-occurrence updates. Reference primitive-seed counting uses DSU inclusion-exclusion over proper-period subspaces; production uses divisor recursion. No external code or target ciphertext was used.

`FREEZE.json` records the independent source/protocol/master commitments at16:40:36UTC. Production freeze was communicated at16:41:21UTC with source/protocol hashes, before generation16:41:26–30UTC. `BANK-SEAL.json` seals every input and hidden expected/truth file. Only input was released before production output was sealed16:41:50UTC. Exact freeze integrity was rechecked after comparison in `FREEZE-VERIFICATION.json`. `secret-master.txt` is a now-released synthetic reproducibility seed, not a credential.

## Complete-set validation

`tiny_checks.py` exhausts binary ciphertexts lengths0–6, periods2–4, every position mask and every binary known-value assignment:167,961 exact relations,1,119,740 primitive-seed comparisons and2,540 round trips. Complete brute-force seed and projected plaintext sets agree; cross-period unions are deduplicated. AZ corners include empty/short strings, repeated and new symbols, unused coordinates, renaming invariance, constant keys, and finite-prefix versus cyclic period distinctions. All pass.

Blind audit compares2,163 independently represented exact relations across309cases, not merely one witness or a candidate count. Every relation's schedule, forced cylinder, used coordinates, proper-divisor exclusions and seed/projection counts match. It separately validates367 production primitive-key/full-plaintext certificates with reference encryption and known-value checks. All224 plants' full seed/plaintext truth is retained. No repair or failed case occurred.

Field naming differs without mathematical disagreement: reference `consistent` is forced-value consistency; production `forced_consistent` has that meaning, while production `consistent` means at least one primitive completion. The audit explicitly checks both. Raw outputs are preserved.

`REPRESENTATION.md` proves exact symbolic semantics and unused-coordinate projection; the cross-period result is a union, never a summed cardinality. A second plaintext, not a second key, establishes ambiguity. No claim of full recovery follows from mere seed compatibility.

## Resources and remaining gate

Reference exhaustive tiny checks7.652CPU seconds/8,960KiB RSS; generation3.924seconds/16,624KiB; blind audit0.637seconds/26,504KiB. Principal measured numerical work totals12.214CPU seconds. Source reading, file staging and hash checks are small unmetered orchestration overhead, not fabricated numerical timings. All comfortably within1CPUhour/2GiB allocation.

Prior-art partition coverage is handled by another independent worker. This audit does not certify that gate, global novelty, source authenticity or a target result. Coordinator must reconcile structural overlap, audited protocol and resource ledger, then obtain parent approval before any target key/crib compatibility calculation. No repository or Responsibilities Page was modified by this worker.
