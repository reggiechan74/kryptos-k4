# Independent negative-certificate index audit

31 October 2026 UTC. Reviewer: `/root/index_k4_negative_certificates/review_negative_index`.

**PASS within the deliberately bounded trust model.** Reviewed checker SHA256 `733b1ab87938af81c7f1e8d8dead5d3040462adcd262f94919b0b0e8d55e1e86`. This is a metadata/implication checker, not a new cryptanalysis experiment or independently re-proven historical solver.

## Static review

Read Responsibilities Page first. Independently checked retained044 receipt SHA256 `a270eea127fd1c11343034e390c6a25ff87c2ac21d24c9fc2648da98137840a2` and all four receipt dependencies: frozen specification, algorithm, runner and data. All match code-pinned hashes. Read the exact periodic method and runner; neither historical module was imported or run. The analytic minimum counts unavoidable same-phase disagreements with unrestricted keys and arbitrary unknown plaintext, so a strictly positive completed minimum rules out a zero-edit fit at these exact coordinates. This inherits the reviewed exactness of044; hashes alone cannot establish truth.

Checked all96 output pointers against original retained rows:49 completed positive minima are negative certificates;47 zero minima are ineligible, not negative evidence. Other alphabets/equations and phase/reset families are explicitly outside initial coverage. Their omission is not an exclusion.

## Fresh synthetic validation

`python independent_tests.py /path/to/checker.py` is classified **synthetic**, never archived-target replay. It independently enumerates all set partitions for lengths1–5 and binary block assignments. Containment is established by explicit synthetic vector-set inclusion, not by copying the production equality-edge test. All5,918 comparisons pass, including arbitrary label renamings. This exposes reversed containment and mixed/non-nested cases.

48 additional checks pass: equation/sign/modulus/alphabet-role/data/normalization/alignment/coordinate mismatches; duplicate/missing coordinates; short/long/empty/boolean/float/string/negative partitions; unknown domain claims; out-of-universe, boolean, duplicate and missing restricted values; skipped/heuristic/unknown/incomplete/compatible/ineligible statuses; restricted old domain; reversed implication; free-key supermodel without a negative; missing/corrupted source bytes; duplicate and nonfinite JSON. See TEST-RESULT.json.

Static command `checker.py --repo …` only reads/hashes retained evidence and computes coordinate partitions. All96 retained metadata pointers independently match; see STATIC-RESULT.json. No K4 values were subtracted, fitted or searched, no target schedule generated, no old solver run, no third-party program executed.

## Findings addressed

Initial review requested duplicate JSON-key rejection and typed exact JSON comparison of supplied index. Both are present in reviewed version. Ambiguous repeated fields fail closed. CLI always regenerates a trusted index from code-pinned bytes; a supplied index is a comparison artifact, never authority.

## Trust boundaries / limitations

- `check_request(index, request)` is an internal API for an already trusted index. It does not authenticate arbitrary caller-created indexes. The CLI supplies that authentication boundary. Tests deliberately construct fresh synthetic trusted-index fixtures to test logic, not to establish target evidence.
- A caller-supplied partition is not mechanically proven to model its proposed mechanism. Result is conditional on independent semantic verification that its equalities hold for every admissible key/plaintext. A fitted or sampled partition does not suffice.
- Old unrestricted key domains make any explicitly valid residue-subdomain safe for one-way implication. Restricted old domains are not supported. Unrecognized domain claims are rejected.
- Equal crib partitions are not full-message clock/operator equivalence. Strict crib containment transfers only the inherited negative. A weak/free containing model with zero, skipped or unknown result cannot exclude its children.
- No certificate means no indexed proof applies, not admission, novelty or permission to run. No global novelty or separate tool-repo claim is justified.

This audit ends at the bounded initial utility. New cipher selection, target execution and external provenance expansion remain separate reviewed decisions.
