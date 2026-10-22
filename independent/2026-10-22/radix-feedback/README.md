# Replay the bounded K4 radix-feedback audit

This package is self-contained. It requires Python 3.8 or newer and no third-party packages, network connection, or repository checkout.

1. Extract the ZIP to a new folder, then open Terminal in that folder.
2. Verify the original files:

   `shasum -a 256 -c SHA256SUMS`

3. Replay without modifying the archived result:

   `python3 audit.py --output results.replay.json`

4. Confirm byte-for-byte equality:

   `cmp results.json results.replay.json`

5. Optionally run the separate implementation and compare its output:

   `python3 independent_verify.py > independent-results.replay.json`

   `cmp independent-results.json independent-results.replay.json`

The expected message is:

`PASS: 8/8 families excluded modulo 2 and modulo 26; 3264 synthetic roundtrips passed.`

The result is deterministic. It contains no runtime timestamps. Do not run Python with `-O` or `PYTHONOPTIMIZE`: verification assertions are required and optimized execution is rejected.

## Contents

- `REPORT.md`: readable result, scope, proof and exact certificates.
- `SPECIFICATION.json`: dated operational specification frozen before family testing, with prior candidate knowledge disclosed.
- `SCHEMA_AMENDMENT.json`: pre-test correction for the absent stored dense-vector field.
- `modeled-uppercase-geometry-001-core.json`: unchanged frozen geometry input.
- `audit.py`: primary replay and controls.
- `results.json`: deterministic primary output, including all training transitions and each excluded parity triple.
- `INDEPENDENT_REVIEW.md`: independent verification report.
- `independent_verify.py`: separate implementation that does not read the primary script.
- `independent-results.json`: deterministic output from the separate verifier.
- `SHA256SUMS`: hashes for every archived file except the manifest itself.

The first 13-letter public crib is the only real test data used. The Berlin holdout was not evaluated. This excludes only the precisely specified first-order affine frozen-feature family, not all geometric ciphers or all possible root-driven constructions.
