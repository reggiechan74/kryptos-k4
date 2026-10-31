# Method-quality improvement: source-literal verification

31 October2026. **Decision: retain frozen v1 as an internal extraction aid.** No standalone repository, global novelty or K4-solution claim is warranted.

## Observed problem

During study062's pre-freeze route-eligibility reconstruction, the external source's E→A misspelling shift was copied as A→E. The incorrect original reconstruction, its outputs, correction and compute charges remain in062's provenance. This was not a changed cipher rule or a rescue after target failure.

## Bounded improvement

Use a read-only AST selector to compare the exact structurally declared iterable with expected strings, tied to an independently pinned source checksum. The tool never evaluates source expressions. It does not replace human verification of operator equations, alphabet roles, key domains or route coverage.

The v1 source/spec/development freeze SHA256 is `29e3912f38661c9304adf37586d22801b0c610bfd866abe899d976d982c263d8`. The independent reviewer authored81synthetic cases from the specification alone, sealed fixture freeze `a3f677bc9fe84c13b2ef11ad84bc87ed218a5f7556ff5b587babe5f209a70f34`, then inspected implementation. Three preplanned malformed-request supplements brought the CLI suite to84cases.

## Evidence

-84/84 independently expected statuses/exit codes; zero false accepts/rejects in that finite suite.
-Exact selected locations, hashes, expected values and limitation labels checked; no side-effect sentinel created.
-Four separately labelled nonblind checks of the actual pinned source: EA accepted, AE rejected for each of shifts_ST and shifts_KA. External source bytes are not redistributed.
-Four post-inspection error-path diagnostics fail closed: injected parser MemoryError/RecursionError, resource setup failure and missing input. These are not fresh blind tests or actual OS-exhaustion measurements.
-Measured independent84-case child CPU3.000281seconds,wall3.092359541seconds,peak31,973,376bytes; actual-source supplement0.163505CPU seconds. Original receipts give exact measurement scopes.
-Seven focused repository regression methods pass, including portable replay of all84CLI cases, byte-identical source/freeze/archive verification and explicit nonsemantic boundary regressions. This is integration replay, not another new holdout.

## Limits and next decision

The audit validates narrow literal extraction, not all malicious Python, source authenticity, runtime values or semantic domain equivalence. Every selected-dictionary key must be a string constant. Aliases, method updates, tuple-name shadowing, reflective writes and comprehension-body semantics remain outside scope even when extraction returns PASS.

No measured cipher-search bottleneck motivated this tool; the motivation was a concrete transcription error. Future syntax or semantic expansion requires a separately declared version and fresh independent cases, preserving v1 evidence. Current study063's numerical/source admission does not depend on this utility, and no063 outcome is inferred here. No original062 artifacts were modified.
