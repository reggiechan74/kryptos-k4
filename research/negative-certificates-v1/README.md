# Retained negative certificates v1

**Internal method utility, not a new cipher experiment, solver or novelty claim.** This read-only tool indexes already-retained exact negatives and checks a narrow sufficient containment condition. It performs no key fitting, ciphertext/key arithmetic or candidate search. It does not generate a proposed mechanism's schedule.

## Scope and result

The initial index contains all **96** ordinary-periodic AZ/additive rows from the immutable `results/MINIMUM-REPAIR-044-ORIGINAL.json`: **49 completed exact negatives**, **47 ineligible zero-minimum rows**. Selected source rows use `C=P+K mod 26`, unrestricted period-length keys and arbitrary plaintext outside the unchanged 24 crib coordinates. The source field `key_domains` describes *optimal corrected-ciphertext witnesses*, not a restriction on the keys tested; v1 deliberately does not interpret it as the original key domain.

Each record links a JSON pointer to the retained receipt. Receipt, frozen specification, implementation, runner and canonical data are SHA256-pinned and checked on every CLI invocation. The receipt's completed exactness is inherited from044's reviewed analytic method and controls, **not proved anew by this checker**. Source hashes preserve evidence integrity; they do not independently authenticate scientific truth. Original bytes are never modified. No historical solver is imported or executed.

Phase/reset, other signs/alphabets/equations, and external heuristic, skipped, unknown or incomplete reports are explicitly **not executable certificates** in this version. Extending them requires separate exact source/completeness/semantic review. No global coverage claim follows.

## Why a transfer is sound

Let `E(old)` be pairs of crib coordinates forced to use equal key symbols. An unrestricted old model contains the supplied candidate equality model exactly when `E(old) ⊆ E(candidate)`: the old model imposes fewer equalities. A completed old negative then excludes the narrower candidate relation. The reverse direction is invalid. All context must match: ordered plaintext/ciphertext/key alphabet, signs, modulus, original data identity, normalization, same-position alignment and exact coordinate list. No edits or reordering are permitted.

A candidate may use unrestricted residue values or nonempty explicit per-class allowed-value subsets. Correlated restrictions such as primitivity are not executable domain syntax: use an independently justified unrestricted relaxation, and document that implication in the proposal. A negative on that relaxation excludes its restricted subset. An old restricted key domain is not accepted by this proof rule. A free-key/zero-check model with a zero repair minimum is **not a negative** and cannot veto a proposal.

The output is **crib-only negative implication**, even for equal crib partitions. It never establishes full-message clock/operator equivalence, execution duplication, or admission of a proposal when no certificate matches. The caller must independently verify that the supplied partition is required for **every** admissible key/plaintext under the proposed mechanism; data-dependent, plaintext-dependent or partial schedules need particular care. The checker does not verify that semantic premise. A supplied partition alone is not evidence of a new mechanism.

## Use

From the repository root, assuming this directory is `research/negative-certificates-v1`:

```sh
# STATIC: verify source hashes and exact extraction (prints the index).
python3 research/negative-certificates-v1/checker.py --repo . \
  --index research/negative-certificates-v1/index.json

# STATIC: compare an already reviewed saved proposal partition; no target solver.
python3 research/negative-certificates-v1/checker.py --repo . \
  --index research/negative-certificates-v1/index.json --request proposal.json

# SYNTHETIC: only fresh artificial metadata/partition tests.
(cd research/negative-certificates-v1 && python3 -m unittest -v test_checker)
```

`request.schema.json` specifies the request. Copy the exact `context` object from the index; supply one integer partition label per coordinate, in that order. Labels are canonicalized by first appearance. Supply `domain: {"kind":"unrestricted_mod_q"}` or `{"kind":"per_class_values","allowed_values":[[0,1], ...]}` in canonical class order. Unknown fields/domains, duplicate JSON keys, nonfinite numbers, bool/float labels, changed context, missing rows or corrupted source hashes are rejected. The public interface is the CLI: `check_request(index,request)` is an internal **trusted-index** function used by synthetic tests, not an authentication API for user-provided indexes. The CLI always rebuilds and uses the pinned-source index; a supplied index must match exactly.

A successful `inherited_negative` is conditional on the explicit semantic premise above. Retain the request/output, mechanism definition, source references and human review alongside the proposal. `no_certificate` means only this finite index supplies no exclusion: it does not admit a run or establish novelty. Hash mismatch/missing evidence means **rejected**, not “probably equivalent.” Exit 2 is rejection; exit 0 is a completed metadata check, not necessarily an exclusion.

## Dependencies and limitations

- 044 frozen specification `research/MINIMUM-REPAIR-044-SPEC.md` explains the complete modal-frequency minimum: every phase can independently choose all 26 key residues; positive exact minimum forbids zero edits. Source files and hash pins are in `index.json` and `checker.py`.
- 064's retained `local-negative-transfers.json` and independent structural review motivated this utility:13 rows transferred six exclusions without reruns. These historical partitions were inspected, not regenerated. They are not fresh synthetic validation.
- The initial tool indexes all 49 negative periodic rows, not just the six distinct old periods appearing in064's 13 transfers. That is metadata extraction from an already complete receipt, **not 49 new experiments**.
- No phase/reset index or full-message equivalence checker is claimed. No external experiment totals are incorporated. No schedule, target admission or separate repository is created.
