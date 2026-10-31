# Results and integration boundary

## Generic proof and implementation

The small-union proof is an application of classical finite-affine-cover facts. A forbidden affine set removes a scalar value only when, after restriction to the base, its consistent equations have rank one in that scalar's row direction. With r < q, fewer than q proper affine intersections cannot collectively cover a remaining fiber. At r ≥ q, that reasoning fails: q parallel slices can cover a space, or q points can jointly remove a fiber. Exact inclusion–exclusion supplies a bounded fallback, exponential in the forbidden-set count.

The historical toy independently passed its stated well-formed prime-field checks, but accepted a composite modulus and mismatched vector length, relied on removable assertions, and lacked an INCOMPLETE API. It remains historical evidence, not the module to integrate.

The separate hardened module validates built-in integer prime q in [2,65521], dimensions [0,64], canonical residues and finite container/size/budget bounds. Malformed requests raise ValueError; certificate failures raise CertificateError; valid exhausted requests return INCOMPLETE with no partial masks/witnesses/evidence. Every EXACT result includes a feasibility witness even with no scalar queries. Distinct marginal witnesses need not form one jointly feasible vector.

Producer controls: 1,460 valid cases / 4,082 marginal witnesses, 23 malformed rejections, eight budget checks, normal and optimized Python. Independent controls: 10,931 valid cases (9,889 small-union / 1,042 inclusion–exclusion), 95,713 witness checks, 38,086 certificate replay **attempts including expected-negative tamper cases**, 46 malformed rejections, 74 budget checks, eight tamper rejections. Normal/optimized independent resource receipts were about 8.11/8.33 CPU seconds and 28,800/32,804 KiB RSS. These are retained resource measurements, not a speed comparison or a new rerun during publication.

## Source-operator distinctions

E consists of canonical full-Z26 equality descriptors in the unchanged 31-feature, at-most-three-coefficient six-lag model; full-symbol equality is evaluated before CRT reduction. Fixed alphabets and parameters must remain fixed across all inputs. The independently reviewed equality-value matrix has rank 26 before centering (the centered interaction rank is 25); it cannot equal the stipulated low-rank linear-chain interaction. This is global operator separation only.

The pinned Scott carry relation allows an adjacent pair of derived-key values per phase, not a deterministic carry update. Its exact global intersection with E is C = {b ± E12, b ± E34, b ± E56}, 156 distinct functions. The source loops periods 1–30, while notes report no hits through 24 and no complete carry-named result log was found. Remove C for no-duplication purposes; do not call the whole source loop a newly authenticated exact negative.

B contains descriptors whose parity component uses only constant and lag1. Its impossibility transfers from the retained recurrence receipt, SHA256 `03bbae7ed8950b72da8c132ad028ad714aa92126d77ce39bac33c816a0029f25`; the implication was independently checked without re-extracting canonical target data or running any target solver. This is not independent re-authentication of the original extraction.

E167's inspected fixed-position/current-symbol grammar, including the separately reviewed R6 equations, is globally different from E. Claims about skipped source domains, caps and completion remain scoped. Matbalez's public handoff lacks the underlying exact recurrence reports; finite public searches did not recover them. That is unresolved prior scope, not proof of novelty or permission to run a target.

## Next discriminating work

Develop and independently validate a synthetic compiler for **R = E ∖ (B ∪ C)**. It must prove each fixed-beta/support piece exact, preserve sparse witness lifts, compile canonical predicates rather than raw feature names, handle Boolean unions and r ≥ q fallbacks, and return INCOMPLETE without claiming partial projections exact when budgets are exhausted. No integrated residual result is established by the generic module audit. Fresh controls, a new freeze and explicit target-stage admission remain separate. All 68 cipher-family records stay unchanged; this is methodology, not another cipher experiment.
